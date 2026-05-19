# Changelog

Tất cả thay đổi đáng chú ý của dự án được ghi lại tại đây.
Format: `## [YYYY-MM-DD HH:MM:SS] — mô tả ngắn`, theo sau là danh sách thay đổi.

---

## [2026-05-19 10:41:33] — Pipeline format headings + fix sponsor detection nuốt cả bài

### Thêm mới
- `format_numbered_items()` trong [create_article.py](.github/scripts/create_article.py): pattern `N - Title [Body]` ở đầu dòng → heading `### N. Title` + tách body ra dòng riêng. Skip dòng trong code block. Chỉ match dash `-` (không match dấu chấm `.`) để tránh nhầm với numbered list trong prompt examples.
- Flag `--sections` cho `create_article.py`: cho phép user cung cấp danh sách section header thủ công khi jina không fetch về được. Format `"Name@N|Name@text|..."` — vị trí là số mục hoặc text marker. Section names tự được dịch theo nếu kèm `--translate`.
- Flag `--section-level` (1 hoặc 2, mặc định 2) để chọn heading level.

### Sửa đổi
- Bài Anatoli Kopadze: cấu trúc đầy đủ 6 section H2 (Start Here / Claude Is Not What You Think / What Even Regular Users Don't Know / How to Spend Fewer Tokens... / Ready to Use Right Now / The Actual Point) + 18 đề mục H3, khớp với bài gốc trên X.
- Skill [`/add-article`](.claude/skills/add-article/SKILL.md): document flag `--sections` và `--translate` với ví dụ cụ thể.

### Sửa lỗi
- **Sponsor detection nuốt cả bài** (gặp khi thêm bài Figma Help "Workflow lab: Code to canvas"): pattern `get\s+started\s*(for\s+free)?` match cả câu "Get started with X" thường. Bài không có `* * *` ngăn cách → toàn bài là 1 section → 1 câu match = xoá sạch 7918 chars.
  - Tighten `SPONSOR_CTA`: bắt buộc suffix `for free|today|now` sau `get started` / `sign up`.
  - Giới hạn `remove_sponsor_blocks`: chỉ flag section khi `len < 1500 chars`. Sponsor block thực sự thường ngắn, nội dung chính dài hơn nên an toàn.

---

## [2026-05-19 09:36:45] — Fix bài Anatoli Kopadze rỗng, sửa skill add-article, tính năng dịch VI

### Thêm mới
- Tính năng tự động dịch bài sang tiếng Việt bằng `deep-translator` (không cần API key)
- Pipeline dịch giữ nguyên thuật ngữ chuyên ngành (AI/LLM, prompt engineering...)
- YouTube link tự render thành clickable thumbnail
- Thêm các bài mới: Pinterest MCP, Databricks rate limiting, Grab AI agents, Anatoli Kopadze về Claude, EP215 Anatomy of an AI Agent

### Sửa đổi
- Skill `/add-article` ([SKILL.md](.claude/skills/add-article/SKILL.md)):
  - Bỏ command sai `$(git config credential.helper)` (trả về tên helper, không phải token)
  - Làm rõ: `git push` từ local đã tự trigger `deploy.yml`, không cần curl thủ công
  - Cảnh báo GITHUB_TOKEN chỉ áp dụng cho push trong GitHub Actions

### Sửa lỗi
- Bài "Anatoli Kopadze on X" có file `.md` chỉ có frontmatter, body rỗng → fetch lại qua `r.jina.ai`, dịch sang VI, 299 dòng nội dung
- Escape dấu nháy đơn trong YAML title để tránh lỗi build Astro
- Bảo vệ toàn bộ `![alt](url)` khi dịch, tránh Google Translate phá vỡ cú pháp ảnh
- Lọc sponsor/ads và comments khỏi nội dung bài viết bằng look-ahead pattern

### Lưu ý môi trường
- Cài `deep-translator` qua `pip3 install deep-translator` để skill `/add-article` có thể dịch (script không tự động cài)

---

## [2026-05-13 15:29:08] — Cập nhật format timestamp CHANGELOG

### Sửa đổi
- Format timestamp trong CHANGELOG.md từ `[YYYY-MM-DD]` → `[YYYY-MM-DD HH:MM:SS]`
- Cập nhật tất cả entry cũ sang format mới
- Skill `/end-session` dùng `date '+%Y-%m-%d %H:%M:%S'` khi commit

---

## [2026-05-13 15:26:05] — Cải thiện content pipeline, xoá bài mobile, token inline

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

## [2026-05-13 14:03:00] — Tổ chức .claude/, hoàn thiện tính năng xoá bài

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

## [2026-05-13 11:00:00] — GitHub Actions workflow thêm bài tự động

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

## [2026-05-13 09:00:00] — Responsive mobile, tối ưu layout

### Thêm mới
- Mobile layout: sidebar ẩn → hamburger ☰ (vòng tròn) trong social links → popup `<dialog>` danh sách chủ đề
- Nút "Chủ đề" căn trái trong hàng social links, `flex-wrap: nowrap` để 1 dòng

### Sửa đổi
- `--sidebar-width`: `195px → 292px` (+50%)
- Font sidebar links: `14px → 12px`
- Article title: `text-transform: uppercase`
- Social links: `flex-wrap: nowrap` + `overflow-x: auto` + scrollbar ẩn

---

## [2026-05-13 08:00:00] — Khởi tạo dự án

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
