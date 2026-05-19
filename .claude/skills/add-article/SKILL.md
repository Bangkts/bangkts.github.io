---
name: add-article
description: Thêm bài viết mới từ URL vào bangkts.github.io — fetch nội dung, tạo file .md, commit và push
allowed-tools: Bash(curl *) Bash(git *) Bash(npm *) Read Write
---

# Thêm bài viết từ URL

Thêm bài viết từ URL: $ARGUMENTS

## Các bước thực hiện

1. **Xác định thông tin** từ $ARGUMENTS:
   - URL bài viết (bắt buộc)
   - Category (mặc định: "AI Notes")
   - Source label (mặc định: tên domain)

2. **Fetch nội dung** qua r.jina.ai (miễn phí, không cần auth):
   ```bash
   curl -s -H "Accept: text/markdown" "https://r.jina.ai/<URL>" -o /tmp/article.md
   ```

3. **Chạy Python script** để tạo file .md chuẩn Astro:
   ```bash
   python3 .github/scripts/create_article.py \
     --content-file /tmp/article.md \
     --url "<URL>" \
     --source-label "<LABEL>" \
     --category "<CATEGORY>" \
     --category-order <ORDER> \
     --output-dir src/content/articles/<folder>
   ```

4. **Build kiểm tra** không lỗi: `npm run build`

5. **Commit và push**:
   ```bash
   git add src/content/articles/
   git commit -m "feat: thêm bài <title>"
   git push
   ```

6. **Chờ deploy tự động**: `git push` từ máy local (bước 5) đã tự trigger `deploy.yml` — chờ ~2 phút rồi kiểm tra https://bangkts.github.io.

   > Lưu ý: chỉ khi push từ GitHub Actions mới cần trigger thủ công (GITHUB_TOKEN bị chặn). Khi chạy local, bước này không cần.

## Ví dụ sử dụng
```
/add-article https://blog.bytebytego.com/p/how-pinterest-built-mcp
/add-article https://blog.bytebytego.com/p/ten-bai AI Notes ByteByteGo
```
