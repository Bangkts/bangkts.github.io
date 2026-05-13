#!/usr/bin/env python3
"""
Nhận nội dung markdown từ r.jina.ai và tạo file .md đúng chuẩn Astro.

Usage:
  python create_article.py \
    --content-file /tmp/article.md \
    --url "https://blog.bytebytego.com/p/..." \
    --source-label "ByteByteGo" \
    --category "AI Notes" \
    --category-order 3 \
    --output-dir src/content/articles/ai-notes
"""

import argparse
import re
import unicodedata
from pathlib import Path


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.replace("đ", "d").replace("Đ", "d")
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text).strip("-")
    return text


def extract_title(content: str) -> str:
    """Lấy title từ dòng 'Title: ...' trong header jina."""
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("title:"):
            title = stripped[6:].strip().strip('"\'')
            if title:
                return title
    # Fallback: H1 heading đầu tiên
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
    """Bỏ phần metadata header của jina.ai (Title:, URL Source:, ...)."""
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
    Bỏ phần navigation/UI của trang.
    Tìm đoạn văn thực đầu tiên: dài >= 150 ký tự, không phải UI/nav/ảnh đơn.
    """
    NAV_TEXT = re.compile(
        r'subscribe|sign in|sign up|newsletter|discover more|'
        r'join over|become a member|by subscribing|already have an account|'
        r'terms of use|privacy policy|information collection|'
        r'sponsored|advertisement',
        re.IGNORECASE,
    )
    # Dòng chỉ chứa ảnh (markdown image + optional link wrapper)
    IMAGE_ONLY = re.compile(r'^\[?!\[[^\]]*\]\([^)]+\)\]?(?:\([^)]+\))?$')

    MAX_SCAN = 150
    best_start = 0

    for i, line in enumerate(lines[:MAX_SCAN]):
        s = line.strip()
        if not s:
            continue
        # Bỏ qua: dòng chỉ có ảnh
        if IMAGE_ONLY.match(s):
            continue
        # Bỏ qua: dòng navigation/subscription
        if NAV_TEXT.search(s):
            continue
        # Bỏ qua: dòng quá ngắn (< 80 chars) trừ khi là heading ##
        if len(s) < 80 and not s.startswith('##'):
            continue
        # Đây là nội dung thực
        best_start = i
        break

    return lines[best_start:]


def clean_content(raw: str) -> str:
    lines = raw.splitlines()
    lines = strip_jina_header(lines)
    lines = strip_site_navigation(lines)
    body = "\n".join(lines).strip()
    # Dọn nhiều dòng trắng liên tiếp
    body = re.sub(r'\n{3,}', '\n\n', body)
    return fix_images(body)


def next_order(output_dir: str) -> int:
    path = Path(output_dir)
    if not path.exists():
        return 1
    return len(list(path.glob("*.md"))) + 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-file", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--source-label", default="")
    parser.add_argument("--category", required=True)
    parser.add_argument("--category-order", type=int, default=99)
    parser.add_argument("--output-dir", required=True)
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
