---
description: Quy trình git và deploy cho bangkts.github.io
---

# Git & Deploy Workflow

## Quy trình chuẩn
1. Sửa code → `npm run build` kiểm tra không lỗi
2. `git add -A` → `git commit -m "type: mô tả"`
3. `git push` → GitHub Actions tự deploy (~2 phút)

## Lưu ý deploy QUAN TRỌNG
`GITHUB_TOKEN` push KHÔNG tự trigger `deploy.yml` (GitHub chặn để tránh loop).
Workflow `add-article.yml` sau khi commit phải gọi:
```bash
curl -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/repos/Bangkts/bangkts.github.io/actions/workflows/deploy.yml/dispatches" \
  -d '{"ref":"main"}'
```

## Permissions cần thiết trong workflow
```yaml
permissions:
  contents: write
  actions: write  # bắt buộc để trigger workflow khác
```

## Commit message format
- `feat:` tính năng mới
- `fix:` sửa lỗi
- `style:` thay đổi CSS/UI
- `docs:` cập nhật tài liệu
- `chore:` công việc bảo trì

## Nếu push bị reject (remote có commit mới hơn)
```bash
git pull --rebase && git push
```
