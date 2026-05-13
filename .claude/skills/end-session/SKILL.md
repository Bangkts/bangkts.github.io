---
name: end-session
description: Kết thúc phiên làm việc — tổng hợp thay đổi từ git log, cập nhật CHANGELOG.md, commit và push
allowed-tools: Bash(git *) Bash(npm *) Read Write
---

# Kết thúc phiên làm việc

Thực hiện các bước sau để đóng phiên đúng cách:

## Bước 1 — Đọc những gì đã thay đổi
```bash
# Lấy danh sách commit kể từ lần cập nhật CHANGELOG gần nhất
git log --oneline --since="$(git log --format='%ai' -- CHANGELOG.md | head -1)" \
  -- . ":(exclude)CHANGELOG.md"
```

Nếu lệnh trên không tiện, dùng:
```bash
git log --oneline -20
```

## Bước 2 — Cập nhật CHANGELOG.md
Thêm section mới vào **đầu file** (sau dòng tiêu đề), theo format:

```markdown
## [YYYY-MM-DD] — mô tả ngắn phiên làm việc

### Thêm mới
- ...

### Sửa đổi
- ...

### Sửa lỗi
- ...
```

Chỉ ghi những thay đổi **có ý nghĩa** — bỏ qua commit "chore:", "docs:" nhỏ.

## Bước 3 — Commit CHANGELOG
```bash
git add CHANGELOG.md
git commit -m "docs: cập nhật CHANGELOG phiên $(date +%Y-%m-%d)"
git push
```

## Bước 4 — Xác nhận với user
Báo cáo ngắn gọn:
- Những gì đã thay đổi trong phiên
- Link trang live: https://bangkts.github.io
- Nhắc việc cần làm tiếp (nếu có)
