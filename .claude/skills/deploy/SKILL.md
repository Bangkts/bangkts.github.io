---
name: deploy
description: Build và deploy trang bangkts.github.io lên GitHub Pages
allowed-tools: Bash(npm *) Bash(git *)
---

# Deploy trang

Build production và push để trigger GitHub Actions deploy.

## Thực hiện

```bash
# 1. Build kiểm tra
npm run build

# 2. Nếu build thành công — push empty commit để trigger deploy
git commit --allow-empty -m "chore: trigger deploy"
git push
```

## Theo dõi tiến trình
Vào: https://github.com/Bangkts/bangkts.github.io/actions

Chờ dấu ✅ xanh (~2 phút) rồi vào https://bangkts.github.io để xác nhận.
