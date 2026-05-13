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
import os
import re
import sys
import unicodedata
from pathlib import Path


def slugify(text: str) -> str:
    """Chuyển text thành slug không dấu, dùng dấu gạch ngang."""
    # Chuẩn hoá unicode → decompose dấu
    text = unicodedata.normalize("NFD", text)
    # Bỏ dấu combining (tất cả combining characters)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    # Chuyển đ → d
    text = text.replace("đ", "d").replace("Đ", "d")
    # Lowercase
    text = text.lower()
    # Giữ chữ cái, số, space, gạch ngang
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    # Thay nhiều khoảng trắng/gạch ngang bằng 1 gạch ngang
    text = re.sub(r"[\s-]+", "-", text).strip("-")
    return text


def extract_title(content: str) -> str:
    """Lấy title từ output của r.jina.ai (dòng 'Title: ...')."""
    for line in content.splitlines():
        line = line.strip()
        if line.lower().startswith("title:"):
            title = line[6:].strip()
            # Bỏ dấu nháy nếu có
            title = title.strip('"\'')
            if title:
                return title
    # Fallback: dòng # heading đầu tiên
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return "Bài viết mới"


def clean_content(content: str) -> str:
    """Bỏ phần header metadata của r.jina.ai, giữ nội dung bài."""
    lines = content.splitlines()
    # Tìm dòng trống đầu tiên sau phần header (Title/URL/...)
    # Header thường có dạng: Title: ...\nURL Source: ...\nPublished Time: ...\n\n
    in_header = True
    header_end = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if in_header:
            # Các dòng header có pattern "Key: Value" hoặc trống
            if stripped == "" and i > 0:
                # Kiểm tra xem đã qua header chưa
                header_end = i + 1
                in_header = False
                break

    if header_end > 0:
        return "\n".join(lines[header_end:]).strip()
    return content.strip()


def next_order(output_dir: str) -> int:
    """Đếm số file .md hiện có + 1 để tính order tiếp theo."""
    path = Path(output_dir)
    if not path.exists():
        return 1
    md_files = list(path.glob("*.md"))
    return len(md_files) + 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-file", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--source-label", default="")
    parser.add_argument("--category", required=True)
    parser.add_argument("--category-order", type=int, default=99)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    # Đọc nội dung từ file
    with open(args.content_file, "r", encoding="utf-8") as f:
        raw = f.read()

    title = extract_title(raw)
    body  = clean_content(raw)
    slug  = slugify(title)[:60]
    order = next_order(args.output_dir)

    if not slug:
        slug = "bai-viet-moi"

    # Tạo frontmatter
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
    frontmatter = "\n".join(frontmatter_lines)

    markdown = f"{frontmatter}\n\n{body}\n"

    # Đảm bảo thư mục tồn tại
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    output_path = Path(args.output_dir) / f"{slug}.md"

    # Tránh ghi đè nếu trùng tên
    counter = 1
    while output_path.exists():
        output_path = Path(args.output_dir) / f"{slug}-{counter}.md"
        counter += 1

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✓ Tạo file: {output_path}")
    # Output tên file để workflow dùng
    print(f"OUTPUT_FILE={output_path}")


if __name__ == "__main__":
    main()
