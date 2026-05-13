# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Hãy sử dụng hoàn toàn bằng tiếng Việt mỗi khi bắt đầu.

## Thông tin dự án

- **Tên dự án**: Trang hiển thị bài viết cá nhân của Bằng Nguyễn
- **GitHub repo**: https://github.com/Bangkts/bangkts.github.io
- **URL triển khai**: https://bangkts.github.io
- **Tham khảo thiết kế**: https://hueanmy.github.io

## Yêu cầu

### Layout
- Dòng trạng thái trên cùng (StatusBar): text ngắn + dấu chấm xanh
- Hero section: avatar tròn + tên "Bằng Nguyễn" + bio + social links
- Hai cột:
  - **Cột trái (292px)**: sidebar danh sách bài viết nhóm theo category
  - **Cột phải**: top = hero, dưới = nội dung bài viết Markdown

### Bài viết
- Mỗi bài viết là một file `.md` trong `src/content/articles/<category>/`
- Frontmatter bắt buộc: `title`, `category`, `categoryOrder`, `order`
- Frontmatter tuỳ chọn: `source` (URL gốc), `sourceLabel` (tên nguồn)
- Thêm bài mới = tạo file `.md` mới → tự xuất hiện trong sidebar

### Triển khai
- Build: `npm run build` → output vào `dist/`
- Deploy: GitHub Actions tự động khi push lên `main`
- Có 2 workflow: `deploy.yml` (deploy trang) và `add-article.yml` (thêm bài tự động)

## Lệnh thường dùng

```bash
npm run dev      # Dev server tại http://localhost:4321
npm run build    # Build production
npm run preview  # Xem bản build
```

## Tech stack

- **Framework**: Astro 6 (static site generator)
- **Nội dung**: Markdown với Astro Content Collections
- **Styling**: CSS thuần (scoped trong Astro components)
- **Deploy**: GitHub Pages via GitHub Actions

## Cách thêm bài viết

### Cách 1 — Tự động từ URL (khuyên dùng)
1. Vào `https://bangkts.github.io/admin`
2. Paste URL bài viết gốc
3. Chọn category, nhập tên nguồn
4. Bấm **🚀 Thêm bài tự động**
5. Đợi ~3 phút → bài xuất hiện trên trang

**Cơ chế:** Admin page gọi GitHub Actions API → workflow `add-article.yml` chạy server-side:
- Fetch nội dung qua `r.jina.ai` (miễn phí, không cần auth)
- Script Python xử lý: strip navigation, trích title, tạo slug, giữ ảnh
- Commit file `.md` → trigger `deploy.yml` bằng workflow_dispatch API

**Lưu ý quan trọng:** `GITHUB_TOKEN` push KHÔNG tự trigger `push` event trong `deploy.yml`. Workflow `add-article.yml` phải gọi `workflow_dispatch` API sau khi commit mới deploy được.

### Cách 2 — Qua sidebar (nút "+ Thêm chủ đề")
Click "+ Thêm chủ đề" trong sidebar → mở `/admin` với category pre-selected.

### Cách 3 — Viết tay trực tiếp
Tạo file: `src/content/articles/<folder>/ten-bai.md`

```markdown
---
title: "Tiêu đề bài viết"
category: "Tên Category"
categoryOrder: 1
order: 1
source: "https://url-bai-goc.com"
sourceLabel: "Tên nguồn"
---

Nội dung Markdown ở đây...
```

Push lên GitHub → tự động deploy.

## Cấu trúc file quan trọng

```
src/
├── content/
│   ├── config.ts                  # Schema: title, category, categoryOrder, order, source, sourceLabel
│   └── articles/
│       ├── system-design/         # categoryOrder: 1
│       ├── programming/           # categoryOrder: 2
│       └── ai-notes/              # categoryOrder: 3
├── components/
│   ├── Hero.astro                 # Avatar + tên + bio + social links
│   ├── Sidebar.astro              # Nav sidebar với nút thêm/xoá
│   └── StatusBar.astro            # Dòng trạng thái
├── pages/
│   ├── admin.astro                # Trang thêm bài (URL → tự động hoặc tay)
│   └── articles/[...slug].astro   # Render bài viết
└── styles/global.css

.github/
├── workflows/
│   ├── deploy.yml                 # Deploy lên GitHub Pages
│   └── add-article.yml            # Tự động thêm bài từ URL
└── scripts/
    └── create_article.py          # Python script: jina output → .md chuẩn Astro
```

## Tính năng quản lý nội dung

### Xoá bài viết
- Nút ✕ trong sidebar: ẩn khi không hover (desktop), luôn hiện trên mobile
- Click ✕ → popup xác nhận → GitHub API xoá file + trigger deploy
- Cần GitHub Token lưu trong `/admin` ⚙️
- Nếu xoá bài đang xem → tự redirect về trang chủ sau 2 giây

### Sửa bài viết
- Nút **Edit** góc phải tiêu đề → mở GitHub editor file `.md`
- URL format: `github.com/Bangkts/bangkts.github.io/edit/main/src/content/articles/<id>.md`
- Lưu ý: `entry.id` trong Astro v6 glob loader **không có** `.md` → phải thêm thủ công

## Lưu ý kỹ thuật

- File `.md` phải có extension `.md` và tên không dấu, dùng dấu gạch ngang
- Tên file có khoảng trắng hoặc thiếu `.md` → Astro không nhận
- `source: ""` (chuỗi rỗng) sẽ lỗi schema — bỏ field đó nếu không có URL
- Sidebar width: 292px (CSS var `--sidebar-width`)
- Font sidebar links: 12px
- **`GITHUB_TOKEN` push KHÔNG trigger `push` event** → `add-article.yml` phải gọi `workflow_dispatch` API sau commit
- jina.ai trả về navigation Substack trước bài → `create_article.py` skip bằng heuristic 150 chars + NAV_PATTERN
- Dropdown category trong admin là **dynamic** — lấy từ `getCollection('articles')` lúc build
- Mobile: sidebar ẩn, dùng popup dialog (hamburger ☰) — nút ✕ xoá luôn hiện trên mobile
