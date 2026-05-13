# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Hãy sử dụng hoàn toàn bằng tiếng Việt mỗi khi bắt đầu.

## Bắt đầu phiên làm việc mới

1. **Đọc `CHANGELOG.md`** — nắm trạng thái mới nhất của dự án trước khi làm bất cứ điều gì
2. Đọc các file liên quan đến task trước khi sửa
3. **Kết thúc phiên** — gõ `/end-session` để Claude tự tổng hợp thay đổi và cập nhật `CHANGELOG.md`

## Thông tin dự án

- **Repo**: https://github.com/Bangkts/bangkts.github.io
- **Live**: https://bangkts.github.io
- **Stack**: Astro 6 · Markdown · GitHub Pages · GitHub Actions
- **Local**: /Users/bangnguyen/GitLesson

## Lệnh thường dùng

```bash
npm run dev      # Dev server tại http://localhost:4321
npm run build    # Build production (kiểm tra trước khi push)
npm run preview  # Xem bản build
```

## Layout

2 cột: sidebar trái (292px) + cột phải (hero trên, bài viết dưới).
Mobile: sidebar ẩn → hamburger ☰ trong social links → popup dialog.

## Thêm bài viết

**Tự động (khuyên dùng):** Vào `/admin` → paste URL → chọn category → 🚀 → ~3 phút.

**Thủ công:** Tạo `src/content/articles/<folder>/ten-bai.md`:
```yaml
---
title: "Tiêu đề"
category: "AI Notes"
categoryOrder: 3
order: 1
source: "https://..."      # bỏ field này nếu không có URL
sourceLabel: "ByteByteGo"
---
```

**Qua sidebar:** Nút "+ Thêm chủ đề" → mở `/admin` với category đã chọn.

## Skills có sẵn

| Lệnh | Mô tả |
|---|---|
| `/add-article <url>` | Fetch bài từ URL, tạo .md, commit, push |
| `/deploy` | Build + trigger deploy lên GitHub Pages |
| `/fix-article <file>` | Sửa lỗi tên file, frontmatter sai |

Dùng agent `content-reviewer` để review bài trước khi publish.

## Quy tắc chi tiết

- Astro conventions: `.claude/rules/astro-conventions.md`
- Git & deploy workflow: `.claude/rules/git-workflow.md`

## Lưu ý kỹ thuật cốt lõi

- Tên file `.md`: không dấu, không khoảng trắng, có đuôi `.md`
- `source: ""` rỗng → lỗi Zod schema → bỏ field đi
- `entry.id` trong Astro v6 glob loader không có `.md` → thêm thủ công khi tạo URL
- `GITHUB_TOKEN` push không trigger `deploy.yml` → `add-article.yml` phải gọi `workflow_dispatch` API sau commit
