# Changelog

Tất cả thay đổi đáng chú ý của dự án được ghi lại tại đây.
Format: `## [ngày] — mô tả ngắn`, theo sau là danh sách thay đổi.

---

## [2026-05-13] — Cải thiện content pipeline, xoá bài mobile, token inline

### Thêm mới
- Popup xoá bài có ô nhập **GitHub Token inline** — mobile không cần vào `/admin` để lấy token, nhập ngay tại chỗ và tự lưu vào browser
- Skill `/end-session` — tự tổng hợp và cập nhật CHANGELOG khi kết thúc phiên

### Sửa lỗi
- **Content pipeline** 4 tầng hoàn chỉnh cho script `create_article.py`:
  - `strip_site_navigation`: dùng last-sponsor-line + look-ahead, không nhầm ảnh bài viết là sponsor
  - `remove_sponsor_blocks`: xoá cả block giữa `* * *` nếu bất kỳ đoạn nào chứa sponsor URL
  - `truncate_at_comments`: cắt tại `## Comments`, `Leave a comment`...
  - Xử lý được sponsor nhiều đoạn (CodeRabbit, WorkOS...) không có URL ở đoạn đầu
- Cập nhật lại nội dung 5 bài viết đã post theo rules mới — không còn sponsor/ads

---

## [2026-05-13] — Tổ chức .claude/, hoàn thiện tính năng xoá bài

### Thêm mới
- `.claude/rules/astro-conventions.md` — quy tắc Astro, path-scoped cho `.md` và `.astro`
- `.claude/rules/git-workflow.md` — quy trình git + lưu ý deploy GITHUB_TOKEN
- `.claude/skills/add-article/SKILL.md` — slash command `/add-article <url>`
- `.claude/skills/deploy/SKILL.md` — slash command `/deploy`
- `.claude/skills/fix-article/SKILL.md` — slash command `/fix-article`
- `.claude/agents/content-reviewer.md` — subagent review bài viết trước publish

### Sửa đổi
- `CLAUDE.md` — gọn lại còn ~60 dòng, trỏ sang `.claude/rules/` cho chi tiết

---

## [2026-05-13] — Popup xác nhận xoá bài, mobile delete button

### Thêm mới
- Popup xác nhận xoá (`<dialog id="delete-dialog">`) với nút Huỷ / Xoá đỏ
- JavaScript xoá file qua GitHub API: GET sha → DELETE → trigger deploy
- Mobile: nút ✕ luôn hiện (`opacity: 1`) vì không có hover trên touch

### Sửa đổi
- `Sidebar.astro` — đổi `<a href="github.com/delete/...">` thành `<button data-file>` + JS
- `[...slug].astro` — thêm delete-dialog HTML + CSS + script xử lý

---

## [2026-05-13] — GitHub Actions workflow thêm bài tự động

### Thêm mới
- `.github/workflows/add-article.yml` — workflow nhận URL, fetch qua r.jina.ai, tạo .md, commit, **trigger deploy**
- `.github/scripts/create_article.py` — Python script: strip navigation Substack, trích title, tạo slug, giữ ảnh, convert `<img>` HTML → markdown

### Sửa lỗi quan trọng
- `GITHUB_TOKEN` push KHÔNG trigger `push` event trong `deploy.yml` → thêm bước gọi `workflow_dispatch` API sau commit
- `fetch-depth: 0` để tránh shallow clone gây lỗi `git push`
- Strip navigation Substack (logo, Subscribe, Sign in) trước nội dung thực: heuristic 150 chars + NAV_PATTERN regex

### Sửa đổi
- `admin.astro` — đơn giản hoá: chỉ cần URL + category + GitHub Token → gọi Actions API
- `Sidebar.astro` — dropdown category động từ `getCollection('articles')` thay vì hardcode

---

## [2026-05-13] — Responsive mobile, tối ưu layout

### Thêm mới
- Mobile layout: sidebar ẩn → hamburger ☰ (vòng tròn) trong social links → popup `<dialog>` danh sách chủ đề
- Nút "Chủ đề" căn trái trong hàng social links, `flex-wrap: nowrap` để 1 dòng

### Sửa đổi
- `--sidebar-width`: `195px → 292px` (+50%)
- Font sidebar links: `14px → 12px`
- Article title: `text-transform: uppercase`
- Social links: `flex-wrap: nowrap` + `overflow-x: auto` + scrollbar ẩn

---

## [2026-05-13] — Khởi tạo dự án

### Thêm mới
- Dự án Astro 6 với GitHub Pages
- Layout 2 cột: sidebar trái + hero/bài viết phải
- Components: `StatusBar`, `Hero`, `Sidebar`, `BaseLayout`
- Content collections: `articles` với schema `title`, `category`, `categoryOrder`, `order`, `source`, `sourceLabel`
- Sidebar: nút "+ Thêm chủ đề" (→ `/admin`), "+ Thêm Section", nút ✕ xoá bài
- Nút **Edit** trên bài viết → GitHub editor
- Nút **Đọc bài gốc** khi có `source` field
- Avatar từ GitHub profile: `https://github.com/Bangkts.png`
- GitHub Actions: `deploy.yml` (Node.js 22), `add-article.yml`
- Trang `/admin`: form thêm bài tự động + thủ công
