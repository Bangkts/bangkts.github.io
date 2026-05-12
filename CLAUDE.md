# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Hãy sử dụng hoàn toàn bằng tiếng Việt mỗi khi bắt đầu.

## Thông tin dự án

- **Tên dự án**: Trang hiển thị bài viết cá nhân của Bằng Nguyễn
- **GitHub repo**: https://github.com/Bangkts/bangkts.github.io
- **URL triển khai**: https://bangkts.github.io
- **Tham khảo thiết kế**: https://hueanmy.github.io

## Yêu cầu

### Layout (theo file `required features.png`)
- Dòng trạng thái trên cùng (StatusBar): text ngắn + dấu chấm xanh
- Hero section: avatar tròn + tên "Bằng Nguyễn" + bio + social links
- Hai cột bên dưới:
  - **Sidebar trái (~240px)**: danh sách bài viết nhóm theo category, highlight bài đang xem
  - **Vùng nội dung phải**: render nội dung bài viết Markdown được chọn

### Bài viết
- Mỗi bài viết là một file `.md` trong `src/content/articles/<category>/`
- Thêm bài mới = tạo file `.md` mới, tự động xuất hiện trong sidebar, không cần sửa code
- Frontmatter bắt buộc: `title`, `category`, `order` (tùy chọn)

### Triển khai
- Build bằng `npm run build` → output vào `dist/`
- Deploy lên GitHub Pages qua GitHub Actions (file `.github/workflows/deploy.yml`)
- Mỗi lần push lên branch `main` sẽ tự động build và deploy

## Lệnh thường dùng

```bash
npm run dev      # Chạy dev server tại http://localhost:4321
npm run build    # Build production vào dist/
npm run preview  # Xem trước bản build
```

## Tech stack

- **Framework**: Astro (static site generator)
- **Nội dung**: Markdown với Astro Content Collections
- **Styling**: CSS thuần (scoped trong Astro components)
- **Deploy**: GitHub Pages via GitHub Actions

## Cách thêm bài viết mới

1. Tạo file: `src/content/articles/<tên-category>/tên-bài.md`
2. Thêm frontmatter:
   ```
   ---
   title: "Tiêu đề bài viết"
   category: "Tên Category"
   order: 1
   ---
   ```
3. Viết nội dung Markdown bên dưới
4. Push lên GitHub → tự động deploy
