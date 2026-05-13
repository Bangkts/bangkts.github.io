#!/usr/bin/env python3
"""
Nhận nội dung markdown từ r.jina.ai và tạo file .md đúng chuẩn Astro.

Các bước xử lý:
  1. strip_jina_header     — bỏ metadata jina (Title:, URL Source:, ...)
  2. strip_site_navigation — bỏ navigation/UI ở đầu trang
  3. remove_sponsor_blocks — bỏ quảng cáo/sponsor ở đầu và giữa bài
  4. truncate_at_comments  — cắt tại phần comments/replies cuối bài
  5. fix_images            — chuẩn hoá ảnh (HTML → markdown, bỏ base64)
"""

import argparse
import re
import unicodedata
from pathlib import Path


# ── Patterns ───────────────────────────────────────────────────────────────

# URL tracking/sponsor điển hình
SPONSOR_URL = re.compile(
    r'go\.\w+\.com/'           # go.bytebytego.com, go.company.com
    r'|utm_[a-z_]+'            # UTM tracking params
    r'|/sponsored'
    r'|/ref=[a-z]'
    r'|aff_id=|affid=',
    re.IGNORECASE,
)

# Text CTA của quảng cáo
SPONSOR_CTA = re.compile(
    r'try\s+\w+\s+(for\s+)?free'
    r'|get\s+started\s*(for\s+free)?'
    r'|sign\s+up\s+(for\s+free|today)'
    r'|start\s+(your\s+)?(free\s+)?trial'
    r'|\[.{2,60}→\]\(https?://'    # [text →](url) — CTA link với mũi tên
    r'|\[give\s+your',
    re.IGNORECASE,
)

# Dấu hiệu bắt đầu phần comments
COMMENT_START = re.compile(
    r'^#{1,4}\s*(all\s+comments?|comments?|discussion|replies?|reader\s+comments?)\s*$'
    r'|^(leave\s+a\s+comment|top\s+new\s+|join\s+the\s+discussion'
    r'|\d+\s+comments?\s*$)',
    re.IGNORECASE,
)

# Navigation/UI của trang (dùng trong strip_site_navigation)
NAV_TEXT = re.compile(
    r'subscribe|sign in|sign up|newsletter|discover more|'
    r'join over|become a member|by subscribing|already have an account|'
    r'terms of use|privacy policy|information collection',
    re.IGNORECASE,
)

# Dòng chỉ chứa ảnh (markdown image + optional link wrapper)
IMAGE_ONLY = re.compile(r'^\[?!\[[^\]]*\]\([^)]+\)\]?(?:\([^)]+\))?$')

# Horizontal rule
HORIZ_RULE = re.compile(r'^\s*(\*\s*){3,}\s*$|^\s*(-\s*){3,}\s*$|^\s*(_\s*){3,}\s*$')


# ── Các hàm xử lý ─────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.replace("đ", "d").replace("Đ", "d")
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text).strip("-")
    return text


def extract_title(content: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("title:"):
            title = stripped[6:].strip().strip('"\'')
            if title:
                return title
    for line in content.splitlines():
        if line.strip().startswith("# "):
            return line.strip()[2:].strip()
    return "Bài viết mới"


def fix_images(content: str) -> str:
    """Convert <img> HTML → markdown, bỏ base64."""
    content = re.sub(
        r'<img[^>]+src=["\']([^"\']+)["\'][^>]*/?>',
        lambda m: f'![]({m.group(1)})',
        content, flags=re.IGNORECASE,
    )
    content = re.sub(r'!\[[^\]]*\]\(data:[^)]+\)', '', content)
    return content


def strip_jina_header(lines: list) -> list:
    """Bỏ metadata header của jina.ai (Title:, URL Source:, Markdown Content:, ...)."""
    META = re.compile(
        r'^(title|url source|url|published time|published|author|description'
        r'|markdown content|byline|site name|warning)\s*:',
        re.IGNORECASE,
    )
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s == "" or META.match(s) or re.match(r'^[=\-]{3,}$', s):
            i += 1
        else:
            break
    return lines[i:]


def strip_site_navigation(lines: list) -> list:
    """
    Bỏ navigation/UI và tất cả sponsor block ở đầu trang.

    Chiến lược:
    1. Tìm vị trí sponsor URL/CTA CUỐI CÙNG trong 150 dòng đầu
    2. Bắt đầu nội dung từ đoạn văn thực NGAY SAU vị trí đó
    Cách này xử lý được sponsor block nhiều đoạn (không cần biết kích thước block).
    """
    MAX_SCAN = 150

    # Tìm dòng sponsor/nav cuối cùng trong phần đầu
    # Chỉ track SPONSOR và NAV thực sự, KHÔNG track ảnh article
    last_sponsor_line = -1
    for i, line in enumerate(lines[:MAX_SCAN]):
        s = line.strip()
        if SPONSOR_URL.search(s) or SPONSOR_CTA.search(s) or NAV_TEXT.search(s):
            last_sponsor_line = i

    # Tìm đoạn văn thực đầu tiên SAU last_sponsor_line
    start = last_sponsor_line + 1
    for i, line in enumerate(lines[start:], start=start):
        s = line.strip()
        if not s:
            continue
        if IMAGE_ONLY.match(s) or NAV_TEXT.search(s):
            continue
        if SPONSOR_URL.search(s) or SPONSOR_CTA.search(s):
            continue
        if len(s) < 80 and not s.startswith('##'):
            continue
        return lines[i:]

    # Fallback: không tìm thấy → trả về từ đầu
    return lines


def is_sponsor_paragraph(para: str) -> bool:
    """True nếu đoạn văn là quảng cáo/sponsor."""
    # Chứa URL tracking/sponsor
    if SPONSOR_URL.search(para):
        return True
    # Chứa CTA điển hình của quảng cáo
    if SPONSOR_CTA.search(para):
        return True
    return False


def remove_sponsor_blocks(content: str) -> str:
    """
    Bỏ các block quảng cáo nằm giữa bài (inline sponsor).

    ByteByteGo thường đặt sponsor trong block giữa * * * separators:
      * * *
      [ảnh sponsor] + mô tả nhiều đoạn + [CTA →](sponsor-url)
      * * *

    Chiến lược:
    1. Tách nội dung theo * * * separators thành các sections
    2. Nếu section nào chứa sponsor URL/CTA → bỏ toàn bộ section đó
    3. Ghép lại các section sạch
    """
    # Tách theo horizontal rule (*** hoặc --- hoặc ___)
    HR_SPLIT = re.compile(
        r'\n\s*(\*\s*){3,}\s*\n|\n\s*(-\s*){3,}\s*\n|\n\s*(_\s*){3,}\s*\n'
    )
    sections = HR_SPLIT.split(content)

    clean_sections = []
    for section in sections:
        if section is None:
            continue
        # Bỏ section là ký tự horizontal rule lặp
        stripped = section.strip()
        if re.match(r'^[\*\-\_\s]{1,5}$', stripped):
            continue
        # Bỏ section chứa sponsor
        if is_sponsor_paragraph(stripped):
            continue
        clean_sections.append(section)

    result = '\n\n'.join(s for s in clean_sections if s.strip())

    # Dọn thêm: bỏ từng paragraph đơn lẻ còn sót có sponsor
    paragraphs = re.split(r'\n{2,}', result)
    final = [p for p in paragraphs if not is_sponsor_paragraph(p.strip())]
    return '\n\n'.join(final)


def truncate_at_comments(content: str) -> str:
    """Cắt nội dung tại điểm bắt đầu phần comments/replies."""
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if COMMENT_START.match(line.strip()):
            return '\n'.join(lines[:i]).strip()
    return content


def clean_content(raw: str) -> str:
    """Pipeline đầy đủ: header → nav → sponsor → comments → images."""
    lines = raw.splitlines()
    lines = strip_jina_header(lines)
    lines = strip_site_navigation(lines)
    content = '\n'.join(lines)
    content = remove_sponsor_blocks(content)
    content = truncate_at_comments(content)
    content = fix_images(content)
    # Dọn nhiều dòng trắng liên tiếp
    content = re.sub(r'\n{3,}', '\n\n', content).strip()
    return content


def next_order(output_dir: str) -> int:
    path = Path(output_dir)
    if not path.exists():
        return 1
    return len(list(path.glob("*.md"))) + 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-file",   required=True)
    parser.add_argument("--url",            required=True)
    parser.add_argument("--source-label",   default="")
    parser.add_argument("--category",       required=True)
    parser.add_argument("--category-order", type=int, default=99)
    parser.add_argument("--output-dir",     required=True)
    args = parser.parse_args()

    with open(args.content_file, "r", encoding="utf-8") as f:
        raw = f.read()

    title = extract_title(raw)
    body  = clean_content(raw)
    slug  = slugify(title)[:60] or "bai-viet-moi"
    order = next_order(args.output_dir)

    frontmatter_lines = [
        "---",
        f'title: "{title}"',
        f'category: "{args.category}"',
        f"categoryOrder: {args.category_order}",
        f"order: {order}",
        f'source: "{args.url}"',
    ]
    if args.source_label:
        frontmatter_lines.append(f'sourceLabel: "{args.source_label}"')
    frontmatter_lines.append("---")

    markdown = "\n".join(frontmatter_lines) + f"\n\n{body}\n"

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output_dir) / f"{slug}.md"

    counter = 1
    while output_path.exists():
        output_path = Path(args.output_dir) / f"{slug}-{counter}.md"
        counter += 1

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✓ Tạo file: {output_path}")
    print(f"OUTPUT_FILE={output_path}")


if __name__ == "__main__":
    main()
