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

   > Lưu ý: jina trả về **plain markdown**, KHÔNG giữ được heading H1/H2 từ trang gốc nếu trang dùng JS render (X.com, một số Substack). Bài fetch về có thể thiếu section header.

3. **Phát hiện listicle & hỏi user về section header** (quan trọng — đừng bỏ qua):
   ```bash
   grep -cE "^[0-9]+ - " /tmp/article.md
   ```
   - Nếu ≥ 5 dòng match → bài là **listicle** (vd "10 bí mật", "18 steps...")
   - Listicle thường có **section header** (chữ to in đậm phân nhóm các đề mục)
   - jina KHÔNG fetch về được — phải **HỎI USER**:
     > "Bài có N đề mục dạng listicle. Trên web gốc có section header nào phân nhóm các đề mục không? Nếu có, gửi tên + vị trí mỗi section theo format `Section1@N|Section2@N|...` (N = số đề mục mà section đứng trước). Nếu không có, trả lời 'không'."
   - Khi user trả lời, dùng giá trị đó cho flag `--sections` ở bước 4.

4. **Chạy Python script** để tạo file .md chuẩn Astro:
   ```bash
   python3 .github/scripts/create_article.py \
     --content-file /tmp/article.md \
     --url "<URL>" \
     --source-label "<LABEL>" \
     --category "<CATEGORY>" \
     --category-order <ORDER> \
     --output-dir src/content/articles/<folder> \
     --translate          # tuỳ chọn: dịch sang tiếng Việt
   ```

   - Script tự nhận diện pattern `N - Title` ở đầu dòng (listicle) → heading H3
   - Nếu bài có **section header** (chữ to in đậm phân nhóm các đề mục), jina **không fetch về được** → cần cung cấp thủ công qua flag `--sections`:
     ```bash
     --sections "Start Here@1|What Even Regular Users Don't Know@6|The Actual Point@Claude is not smarter"
     ```
     Format mỗi entry: `Tên Section@<vị trí>`. Vị trí có 2 dạng:
     - `<số>` → chèn TRƯỚC đề mục `### N.` (vd `@6` chèn trước mục 6)
     - `<text>` → chèn TRƯỚC dòng đầu tiên chứa text (vd `@Claude is not smarter` — dùng cho section conclusion sau item cuối)
     - Mặc định `--section-level 2` (H2); đổi nếu cần H1.

5. **Build kiểm tra** không lỗi: `npm run build`

6. **Commit và push**:
   ```bash
   git add src/content/articles/
   git commit -m "feat: thêm bài <title>"
   git push
   ```

7. **Chờ deploy tự động**: `git push` từ máy local (bước 6) đã tự trigger `deploy.yml` — chờ ~2 phút rồi kiểm tra https://bangkts.github.io.

   > Lưu ý: chỉ khi push từ GitHub Actions mới cần trigger thủ công (GITHUB_TOKEN bị chặn). Khi chạy local, bước này không cần.

## Ví dụ sử dụng
```
/add-article https://blog.bytebytego.com/p/how-pinterest-built-mcp
/add-article https://blog.bytebytego.com/p/ten-bai AI Notes ByteByteGo
```

## Ví dụ bài listicle có section header
Bài X.com "How to Actually Use Claude. 18 steps...":
```bash
--sections "Start Here@1|Claude Is Not What You Think@4|What Even Regular Users Don't Know@6|How to Spend Fewer Tokens and Get More@10|Ready to Use Right Now@14|The Actual Point@Claude is not smarter"
```
- Mục 1-3 trong section "Start Here"
- Mục 4-5 trong "Claude Is Not What You Think"
- Mục 6-9 trong "What Even Regular Users Don't Know"
- ...
- Section cuối "The Actual Point" dùng text marker vì nó là kết luận sau item 18
