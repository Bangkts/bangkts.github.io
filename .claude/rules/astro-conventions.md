---
description: Quy tắc Astro Content Collections cho bangkts.github.io
paths:
  - "src/content/**/*.md"
  - "src/content.config.ts"
  - "src/components/*.astro"
  - "src/pages/**/*.astro"
---

# Astro Conventions

## Frontmatter bắt buộc cho mọi file .md
```yaml
---
title: "Tiêu đề bài viết"
category: "Tên Category"
categoryOrder: 1        # System Design=1, Programming=2, AI Notes=3
order: 1                # Thứ tự trong category
---
```

## Frontmatter tuỳ chọn
```yaml
source: "https://url-bai-goc.com"   # KHÔNG để rỗng — bỏ field nếu không có
sourceLabel: "ByteByteGo"
```

## Tên file .md
- Không dấu tiếng Việt
- Không khoảng trắng — dùng dấu gạch ngang
- Luôn có extension `.md`
- Ví dụ đúng: `how-pinterest-mcp.md`
- Ví dụ sai: `How Pinterest MCP` (thiếu .md, có khoảng trắng)

## Thêm category mới
Tạo folder mới trong `src/content/articles/<ten-folder>/`
Dropdown trong `/admin` tự cập nhật sau lần build tiếp theo.

## Astro v6 glob loader
`entry.id` KHÔNG có `.md` → khi tạo edit/delete URL phải thêm `.md` thủ công:
```javascript
const editUrl = `.../${entry.id}.md`  // đúng
const editUrl = `.../${entry.id}`     // sai
```
