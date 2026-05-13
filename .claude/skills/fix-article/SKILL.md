---
name: fix-article
description: Sửa lỗi file .md bài viết — tên file sai, thiếu frontmatter, source rỗng
allowed-tools: Bash(find *) Bash(git *) Bash(npm *) Read Write
---

# Sửa lỗi bài viết

Kiểm tra và sửa file bài viết: $ARGUMENTS

## Các lỗi thường gặp và cách sửa

### 1. Tên file có khoảng trắng hoặc thiếu .md
```bash
# Tìm file bị lỗi
find src/content/articles -type f ! -name "*.md"
find src/content/articles -type f -name "* *"

# Đổi tên
mv "src/content/articles/folder/Ten Bai Co Dau" \
   "src/content/articles/folder/ten-bai-co-dau.md"
```

### 2. Thiếu frontmatter hoặc frontmatter sai schema
Kiểm tra bằng: `npm run build` — lỗi sẽ chỉ rõ file và field bị sai.

Frontmatter đúng chuẩn:
```yaml
---
title: "Tiêu đề"
category: "AI Notes"
categoryOrder: 3
order: 1
---
```

Lỗi phổ biến:
- `source: ""` → bỏ hẳn field source nếu không có URL
- Thiếu `categoryOrder` → thêm vào

### 3. Build thành công sau khi sửa
```bash
npm run build
git add -A
git commit -m "fix: sửa lỗi file bài viết"
git push
```
