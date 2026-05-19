#!/usr/bin/env python3
"""
Nhận nội dung markdown từ r.jina.ai và tạo file .md đúng chuẩn Astro.

Các bước xử lý:
  1. strip_jina_header     — bỏ metadata jina (Title:, URL Source:, ...)
  2. strip_site_navigation — bỏ navigation/UI ở đầu trang
  3. remove_sponsor_blocks — bỏ quảng cáo/sponsor ở đầu và giữa bài
  4. truncate_at_comments  — cắt tại phần comments/replies cuối bài
  5. fix_images            — chuẩn hoá ảnh (HTML → markdown, bỏ base64)
"""

import argparse
import re
import unicodedata
from pathlib import Path


# ── Thuật ngữ chuyên ngành cần giữ nguyên tiếng Anh ───────────────────────
# Google Translate thường dịch sai những từ này
TECH_TERMS = [
    # AI / LLM core
    "Prompt Engineering", "Prompt Injection", "Prompt",
    "Injection attack", "SQL Injection", "Injection",
    "Token", "Tokens", "Tokenization", "Tokenizer",
    "Embedding", "Embeddings",
    "Fine-tuning", "Fine-tune", "Fine-tuned",
    "Pre-training", "Pre-trained",
    "Inference",
    "Context window", "Context length",
    "Retrieval-Augmented Generation",
    "Chain-of-thought",
    "Zero-shot", "Few-shot", "One-shot",
    "System prompt", "System message",
    "Tool use", "Function calling",
    "Agent", "Agents", "Agentic",
    "Reasoning",
    "Hallucination", "Hallucinate",
    "Grounding",
    "Alignment",
    "RLHF", "RLAIF",
    "InstructGPT", "ChatGPT", "GPT",
    "Transformer", "Attention mechanism", "Self-attention",
    "Neural network", "Deep learning",
    "Backpropagation", "Gradient descent",
    "Overfitting", "Underfitting",
    "Hyperparameter",
    "Batch size", "Learning rate",
    "Epoch", "Iteration",
    "Dropout", "Regularization",
    "Softmax", "ReLU", "Sigmoid",
    "Cross-entropy", "Loss function",
    "Benchmark", "Evaluation",
    "Vector", "Vectors",
    "Cosine similarity",
    "Semantic search",
    "Vector database",
    # DevOps / Software
    "Deploy", "Deployment",
    "Pipeline",
    "Cache", "Caching",
    "Latency", "Throughput",
    "Endpoint",
    "Webhook",
    "Payload", "Schema",
    "Index", "Indexing",
    "Query",
    "Middleware",
    "Microservice",
    "Container", "Docker",
    "Kubernetes",
    "CI/CD",
    "Rollback",
    "Load balancing",
    "Rate limiting",
    "Timeout",
    "Retry",
    "Logging", "Observability", "Telemetry",
    "Tracing",
    # Data
    "Dataset",
    "Feature engineering",
    "Data pipeline",
    "ETL",
    "Schema",
    "Migration",
]

# ── Patterns ───────────────────────────────────────────────────────────────

# URL tracking/sponsor điển hình
SPONSOR_URL = re.compile(
    r'go\.\w+\.com/'           # go.bytebytego.com, go.company.com
    r'|utm_[a-z_]+'            # UTM tracking params
    r'|/sponsored'
    r'|/ref=[a-z]'
    r'|aff_id=|affid=',
    re.IGNORECASE,
)

# Text CTA của quảng cáo — yêu cầu suffix cụ thể để tránh false positive
# với câu thường (vd: "Get started with X" trong bài tutorial không phải sponsor)
SPONSOR_CTA = re.compile(
    r'try\s+\w+\s+(for\s+)?free'
    r'|get\s+started\s+(for\s+free|today|now)'
    r'|sign\s+up\s+(for\s+free|today|now)'
    r'|start\s+(your\s+)?(free\s+)?trial'
    r'|\[.{2,60}→\]\(https?://'    # [text →](url) — CTA link với mũi tên
    r'|\[give\s+your',
    re.IGNORECASE,
)

# Dấu hiệu bắt đầu phần comments
COMMENT_START = re.compile(
    r'^#{1,4}\s*(all\s+comments?|comments?|discussion|replies?|reader\s+comments?)\s*$'
    r'|^(leave\s+a\s+comment|top\s+new\s+|join\s+the\s+discussion'
    r'|\d+\s+comments?\s*$)',
    re.IGNORECASE,
)

# Navigation/UI của trang (dùng trong strip_site_navigation)
NAV_TEXT = re.compile(
    r'subscribe|sign in|sign up|newsletter|discover more|'
    r'join over|become a member|by subscribing|already have an account|'
    r'terms of use|privacy policy|information collection',
    re.IGNORECASE,
)

# Dòng chỉ chứa ảnh (markdown image + optional link wrapper)
IMAGE_ONLY = re.compile(r'^\[?!\[[^\]]*\]\([^)]+\)\]?(?:\([^)]+\))?$')

# Horizontal rule
HORIZ_RULE = re.compile(r'^\s*(\*\s*){3,}\s*$|^\s*(-\s*){3,}\s*$|^\s*(_\s*){3,}\s*$')


# ── Các hàm xử lý ─────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.replace("đ", "d").replace("Đ", "d")
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text).strip("-")
    return text


def extract_title(content: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("title:"):
            title = stripped[6:].strip().strip('"\'')
            if title:
                return title
    for line in content.splitlines():
        if line.strip().startswith("# "):
            return line.strip()[2:].strip()
    return "Bài viết mới"


def fix_images(content: str) -> str:
    """Convert <img> HTML → markdown, bỏ base64."""
    content = re.sub(
        r'<img[^>]+src=["\']([^"\']+)["\'][^>]*/?>',
        lambda m: f'![]({m.group(1)})',
        content, flags=re.IGNORECASE,
    )
    content = re.sub(r'!\[[^\]]*\]\(data:[^)]+\)', '', content)
    return content


def extract_youtube_id(url: str) -> str:
    """Trích video ID từ các dạng URL YouTube."""
    for pat in [
        r'youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})',
        r'youtu\.be/([a-zA-Z0-9_-]{11})',
        r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        r'youtube\.com/v/([a-zA-Z0-9_-]{11})',
        r'youtube\.com/shorts/([a-zA-Z0-9_-]{11})',
    ]:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return ""


def convert_youtube(content: str) -> str:
    """
    Chuyển YouTube embeds/URLs thành ảnh thumbnail có thể click.
    Format: [![▶ Xem video](thumb)](youtube_url)
    """
    # 1. <iframe> YouTube
    def replace_iframe(m: re.Match) -> str:
        src = re.search(r'src=["\']([^"\']+)["\']', m.group(0))
        if not src:
            return m.group(0)
        vid = extract_youtube_id(src.group(1))
        if not vid:
            return m.group(0)
        thumb = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
        url   = f"https://www.youtube.com/watch?v={vid}"
        return f'\n[![▶ Xem video trên YouTube]({thumb})]({url})\n'

    content = re.sub(
        r'<iframe[^>]+youtube[^>]+>.*?</iframe>',
        replace_iframe,
        content, flags=re.IGNORECASE | re.DOTALL,
    )

    # 2. URL YouTube đứng một mình (không nằm trong [](...))
    def replace_bare_url(m: re.Match) -> str:
        url = m.group(0)
        vid = extract_youtube_id(url)
        if not vid:
            return url
        thumb = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
        return f'[![▶ Xem video trên YouTube]({thumb})]({url})'

    content = re.sub(
        r'(?<!\()(https?://(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)[^\s\)\]"]+)',
        replace_bare_url,
        content,
    )

    return content


def protect_tech_terms(content: str) -> tuple:
    """
    Bảo vệ thuật ngữ chuyên ngành trước khi dịch.
    Trả về (content_with_placeholders, {placeholder: original_term}).
    """
    term_map: dict = {}
    # Sắp xếp dài trước để tránh match một phần của cụm từ dài hơn
    sorted_terms = sorted(TECH_TERMS, key=len, reverse=True)

    for i, term in enumerate(sorted_terms):
        placeholder = f"__TERM{i:03d}__"
        # Dùng word boundary, case-sensitive
        escaped = re.escape(term)
        pattern = rf'(?<!\w){escaped}(?!\w)'
        if re.search(pattern, content):
            term_map[placeholder] = term
            content = re.sub(pattern, placeholder, content)

    return content, term_map


def restore_tech_terms(content: str, term_map: dict) -> str:
    """Khôi phục thuật ngữ chuyên ngành sau khi dịch."""
    for placeholder, original in term_map.items():
        content = content.replace(placeholder, original)
    return content


def strip_jina_header(lines: list) -> list:
    """Bỏ metadata header của jina.ai (Title:, URL Source:, Markdown Content:, ...)."""
    META = re.compile(
        r'^(title|url source|url|published time|published|author|description'
        r'|markdown content|byline|site name|warning)\s*:',
        re.IGNORECASE,
    )
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s == "" or META.match(s) or re.match(r'^[=\-]{3,}$', s):
            i += 1
        else:
            break
    return lines[i:]


def strip_site_navigation(lines: list) -> list:
    """
    Bỏ navigation/UI và tất cả sponsor block ở đầu trang.

    Chiến lược:
    1. Tìm vị trí sponsor URL/CTA CUỐI CÙNG trong 150 dòng đầu
    2. Bắt đầu nội dung từ đoạn văn thực NGAY SAU vị trí đó
    Cách này xử lý được sponsor block nhiều đoạn (không cần biết kích thước block).
    """
    MAX_SCAN = 150

    # Tìm dòng sponsor/nav cuối cùng trong phần đầu
    # Chỉ track SPONSOR và NAV thực sự, KHÔNG track ảnh article
    last_sponsor_line = -1
    for i, line in enumerate(lines[:MAX_SCAN]):
        s = line.strip()
        if SPONSOR_URL.search(s) or SPONSOR_CTA.search(s) or NAV_TEXT.search(s):
            last_sponsor_line = i

    # Tìm đoạn văn thực đầu tiên SAU last_sponsor_line
    start = last_sponsor_line + 1
    for i, line in enumerate(lines[start:], start=start):
        s = line.strip()
        if not s:
            continue
        if IMAGE_ONLY.match(s) or NAV_TEXT.search(s):
            continue
        if SPONSOR_URL.search(s) or SPONSOR_CTA.search(s):
            continue
        if len(s) < 80 and not s.startswith('##'):
            continue
        return lines[i:]

    # Fallback: không tìm thấy → trả về từ đầu
    return lines


def is_sponsor_paragraph(para: str) -> bool:
    """True nếu đoạn văn là quảng cáo/sponsor."""
    # Chứa URL tracking/sponsor
    if SPONSOR_URL.search(para):
        return True
    # Chứa CTA điển hình của quảng cáo
    if SPONSOR_CTA.search(para):
        return True
    return False


def remove_sponsor_blocks(content: str) -> str:
    """
    Bỏ các block quảng cáo nằm giữa bài (inline sponsor).

    ByteByteGo thường đặt sponsor trong block giữa * * * separators:
      * * *
      [ảnh sponsor] + mô tả nhiều đoạn + [CTA →](sponsor-url)
      * * *

    Chiến lược:
    1. Tách nội dung theo * * * separators thành các sections
    2. Nếu section nào chứa sponsor URL/CTA → bỏ toàn bộ section đó
    3. Ghép lại các section sạch
    """
    # Tách theo horizontal rule (*** hoặc --- hoặc ___)
    HR_SPLIT = re.compile(
        r'\n\s*(\*\s*){3,}\s*\n|\n\s*(-\s*){3,}\s*\n|\n\s*(_\s*){3,}\s*\n'
    )
    sections = HR_SPLIT.split(content)

    clean_sections = []
    for section in sections:
        if section is None:
            continue
        # Bỏ section là ký tự horizontal rule lặp
        stripped = section.strip()
        if re.match(r'^[\*\-\_\s]{1,5}$', stripped):
            continue
        # Bỏ section chứa sponsor — CHỈ khi section ngắn (< 1500 chars)
        # Section dài là nội dung chính, có thể chứa câu giống CTA nhưng không phải sponsor
        if len(stripped) < 1500 and is_sponsor_paragraph(stripped):
            continue
        clean_sections.append(section)

    result = '\n\n'.join(s for s in clean_sections if s.strip())

    # Dọn thêm: bỏ từng paragraph đơn lẻ còn sót có sponsor
    paragraphs = re.split(r'\n{2,}', result)
    final = [p for p in paragraphs if not is_sponsor_paragraph(p.strip())]
    return '\n\n'.join(final)


def truncate_at_comments(content: str) -> str:
    """Cắt nội dung tại điểm bắt đầu phần comments/replies."""
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if COMMENT_START.match(line.strip()):
            return '\n'.join(lines[:i]).strip()
    return content


# Các từ thường mở đầu một câu mới — dùng để tách title khỏi body khi jina gộp chung
# Chỉ giữ những từ KHÔNG xuất hiện trong giữa tiêu đề
_BODY_STARTERS = {
    'Every', 'Most', 'Before', 'After', 'When', 'If', 'While',
    'Pasting', 'Stop', 'Here', "Here's", 'Add', 'Click', 'Save',
    "Don't", 'Then', 'Now', 'Some', 'These', 'Those', 'Each',
}

# Chỉ match dash/gạch ngang (`-`, `–`, `—`), KHÔNG match dấu chấm `.` —
# để tránh nhầm với numbered list trong prompt/code (1., 2., 3.)
NUMBERED_ITEM_RE = re.compile(r'^(\d{1,2})\s*[-–—]\s+(.+)$')


def format_numbered_items(content: str) -> str:
    """Pattern 'N - Title [Body]' đầu dòng → heading '### N. Title' + body riêng.

    Áp dụng cho listicles kiểu '1 - Foo bar Some text...'. Tách title khỏi body
    nếu jina gộp chung dòng bằng cách scan các từ mở đầu câu trong _BODY_STARTERS.
    Bỏ qua dòng trong code block ```...```.
    """
    lines = content.split('\n')
    result = []
    in_code = False
    for line in lines:
        if line.lstrip().startswith('```'):
            in_code = not in_code
            result.append(line)
            continue
        if in_code:
            result.append(line)
            continue

        m = NUMBERED_ITEM_RE.match(line)
        if not m:
            result.append(line)
            continue

        num = m.group(1)
        rest = m.group(2).strip()
        title_part, body_part = rest, ''

        words = rest.split(' ')
        for i in range(1, len(words)):
            w = words[i].strip()
            if w in _BODY_STARTERS and i >= 2 and len(words) - i >= 5:
                title_part = ' '.join(words[:i]).strip(' \t,')
                body_part  = ' '.join(words[i:]).strip()
                break

        result.append(f'### {num}. {title_part}')
        if body_part:
            result.append('')
            result.append(body_part)
    return '\n'.join(result)


def parse_sections_spec(spec: str) -> list:
    """Parse '--sections' arg dạng 'Name@N|Name@N|Name@text' → [(name, target)].

    Target có thể là:
    - int: insert TRƯỚC heading '### N. ...'
    - str: insert TRƯỚC dòng đầu tiên chứa text này (case-insensitive)
    """
    if not spec:
        return []
    result = []
    for entry in spec.split('|'):
        entry = entry.strip()
        if '@' not in entry:
            continue
        name, target = entry.rsplit('@', 1)
        name, target = name.strip(), target.strip()
        if not name or not target:
            continue
        try:
            result.append((name, int(target)))
        except ValueError:
            result.append((name, target))
    return result


def insert_sections(content: str, sections: list, level: int = 2) -> str:
    """Insert section heading trước numbered item hoặc text marker.

    `sections`: list (name, target). target = int (item N) hoặc str (text).
    `level`: heading level (1 = '#', 2 = '##').
    Sections phải được insert TRƯỚC khi dịch để translate_markdown xử lý cả heading.
    """
    if not sections:
        return content

    prefix = '#' * level
    lines = content.split('\n')

    item_re = re.compile(r'^###\s+(\d{1,2})\.\s+')
    item_pos = {}
    for i, line in enumerate(lines):
        m = item_re.match(line)
        if m:
            item_pos[int(m.group(1))] = i

    resolved = []
    for name, target in sections:
        if isinstance(target, int):
            pos = item_pos.get(target)
        else:
            t = target.lower()
            pos = next((i for i, ln in enumerate(lines) if t in ln.lower()), None)
        if pos is not None:
            resolved.append((name, pos))

    # Insert từ cuối lên để không lệch index
    resolved.sort(key=lambda x: x[1], reverse=True)
    for name, pos in resolved:
        lines[pos:pos] = ['', f'{prefix} {name}', '']

    return '\n'.join(lines)


def clean_content(raw: str) -> str:
    """Pipeline đầy đủ: header → nav → sponsor → comments → images → youtube → numbered."""
    lines = raw.splitlines()
    lines = strip_jina_header(lines)
    lines = strip_site_navigation(lines)
    content = '\n'.join(lines)
    content = remove_sponsor_blocks(content)
    content = truncate_at_comments(content)
    content = fix_images(content)
    content = convert_youtube(content)        # YouTube → clickable thumbnail
    content = format_numbered_items(content)  # 'N - Title' → '### N. Title'
    content = re.sub(r'\n{3,}', '\n\n', content).strip()
    return content


def translate_markdown(content: str) -> str:
    """
    Dịch nội dung Markdown từ tiếng Anh sang tiếng Việt.
    Giữ nguyên: code blocks, inline code, URLs, ảnh, frontmatter keys.
    Dịch: tiêu đề, đoạn văn, heading, bullet points.
    Dùng deep-translator (Google Translate, không cần API key).
    """
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        print("⚠ deep-translator chưa cài. Bỏ qua dịch thuật.")
        return content

    translator = GoogleTranslator(source='en', target='vi')

    # ── Bảo vệ thuật ngữ chuyên ngành TRƯỚC TIÊN ────────────────
    content, term_map = protect_tech_terms(content)

    # ── Bảo vệ các phần cấu trúc không dịch ─────────────────────
    placeholders: dict = {}
    counter = [0]

    def protect(text: str, prefix: str = "PLACEHOLDER") -> str:
        key = f"__{prefix}_{counter[0]}__"
        placeholders[key] = text
        counter[0] += 1
        return key

    # 1. Code blocks ```...```
    content = re.sub(
        r'```[\s\S]*?```',
        lambda m: protect(m.group(0), "CODE"),
        content,
    )

    # 2. Inline code `...`
    content = re.sub(
        r'`[^`\n]+`',
        lambda m: protect(m.group(0), "INLINE"),
        content,
    )

    # 3. Ảnh ![alt](url) — bảo vệ TOÀN BỘ, không tách ra
    # Google Translate sẽ phá vỡ cú pháp nếu chỉ bảo vệ một phần
    content = re.sub(
        r'!\[[^\]]*\]\([^)]+\)',
        lambda m: protect(m.group(0), "IMG"),
        content,
        flags=re.DOTALL,
    )

    # 4. Link [text](url) — bảo vệ URL, dịch text riêng sau
    # Lưu (text, url) để khôi phục sau khi dịch
    link_store: dict = {}

    def protect_link(match: re.Match) -> str:
        text = match.group(1)
        url  = match.group(2)
        key  = f"__LNK_{counter[0]}__"
        link_store[key] = (text, url)
        counter[0] += 1
        return key

    content = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        protect_link,
        content,
    )

    # ── Dịch từng dòng ──────────────────────────────────────────
    def safe_translate(text: str) -> str:
        """Dịch an toàn — bỏ qua dòng trống, placeholder, code."""
        if not text.strip():
            return text
        if text.strip().startswith('__') and text.strip().endswith('__'):
            return text  # placeholder thuần
        # Giới hạn 4500 ký tự mỗi request Google Translate
        if len(text) <= 4500:
            try:
                return translator.translate(text)
            except Exception:
                return text
        # Dòng quá dài: dịch từng đoạn 4000 ký tự
        chunks, cur = [], ""
        for word in text.split(" "):
            if len(cur) + len(word) + 1 > 4000:
                try:
                    chunks.append(translator.translate(cur.strip()))
                except Exception:
                    chunks.append(cur.strip())
                cur = word
            else:
                cur += (" " if cur else "") + word
        if cur:
            try:
                chunks.append(translator.translate(cur.strip()))
            except Exception:
                chunks.append(cur.strip())
        return " ".join(chunks)

    lines = content.splitlines()
    result_lines = []

    for line in lines:
        stripped = line.strip()

        # Bỏ qua dòng trống
        if not stripped:
            result_lines.append(line)
            continue

        # Bỏ qua frontmatter separators và các field key (không dịch key)
        if stripped == '---':
            result_lines.append(line)
            continue

        # Heading: dịch phần text sau ##
        heading_match = re.match(r'^(#{1,6}\s+)(.*)', line)
        if heading_match:
            prefix = heading_match.group(1)
            text   = heading_match.group(2)
            result_lines.append(prefix + safe_translate(text))
            continue

        # Bullet list: dịch phần text sau - hoặc *
        bullet_match = re.match(r'^(\s*[-*+]\s+)(.*)', line)
        if bullet_match:
            prefix = bullet_match.group(1)
            text   = bullet_match.group(2)
            result_lines.append(prefix + safe_translate(text))
            continue

        # Numbered list
        num_match = re.match(r'^(\s*\d+\.\s+)(.*)', line)
        if num_match:
            prefix = num_match.group(1)
            text   = num_match.group(2)
            result_lines.append(prefix + safe_translate(text))
            continue

        # Blockquote
        quote_match = re.match(r'^(>\s*)(.*)', line)
        if quote_match:
            prefix = quote_match.group(1)
            text   = quote_match.group(2)
            result_lines.append(prefix + safe_translate(text))
            continue

        # Dòng thường
        result_lines.append(safe_translate(line))

    translated = '\n'.join(result_lines)

    # ── Khôi phục links: dịch text, giữ URL ─────────────────────
    for key, (text, url) in link_store.items():
        try:
            vi_text = translator.translate(text) if text.strip() else text
        except Exception:
            vi_text = text
        translated = translated.replace(key, f'[{vi_text}]({url})')

    # ── Khôi phục các placeholder còn lại (IMG, CODE, INLINE) ────
    for key, original in placeholders.items():
        translated = translated.replace(key, original)

    # ── Khôi phục thuật ngữ chuyên ngành ─────────────────────────
    translated = restore_tech_terms(translated, term_map)

    return translated


def translate_frontmatter_title(frontmatter: str) -> str:
    """Chỉ dịch title trong frontmatter, giữ nguyên các field khác."""
    try:
        from deep_translator import GoogleTranslator
        translator = GoogleTranslator(source='en', target='vi')

        def translate_title(match):
            original_title = match.group(1)
            try:
                vi_title = translator.translate(original_title)
                return f'title: "{vi_title}"'
            except Exception:
                return match.group(0)

        return re.sub(r'^title:\s*"([^"]+)"', translate_title,
                      frontmatter, flags=re.MULTILINE)
    except ImportError:
        return frontmatter


def next_order(output_dir: str) -> int:
    path = Path(output_dir)
    if not path.exists():
        return 1
    return len(list(path.glob("*.md"))) + 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-file",   required=True)
    parser.add_argument("--url",            required=True)
    parser.add_argument("--source-label",   default="")
    parser.add_argument("--category",       required=True)
    parser.add_argument("--category-order", type=int, default=99)
    parser.add_argument("--output-dir",     required=True)
    parser.add_argument("--translate",      action="store_true", default=False)
    parser.add_argument("--sections",       default="",
                        help="Danh sách section header (pipe-separated). "
                             "Format: 'Name@N|Name@text|...'. N = số mục, text = marker.")
    parser.add_argument("--section-level",  type=int, default=2,
                        help="Heading level cho section (1=H1, 2=H2). Mặc định 2.")
    args = parser.parse_args()

    with open(args.content_file, "r", encoding="utf-8") as f:
        raw = f.read()

    title = extract_title(raw)
    body  = clean_content(raw)

    # Insert section headers TRƯỚC khi dịch để translate_markdown xử lý cả heading
    sections = parse_sections_spec(args.sections)
    if sections:
        body = insert_sections(body, sections, level=args.section_level)
        print(f"✓ Đã chèn {len(sections)} section header")

    # Dịch sang tiếng Việt nếu được yêu cầu
    if args.translate:
        print("Đang dịch sang tiếng Việt...")
        body = translate_markdown(body)
        print("✓ Dịch xong")

    slug  = slugify(title)[:60] or "bai-viet-moi"
    order = next_order(args.output_dir)

    # Loại bỏ dấu nháy kép bên trong title để tránh lỗi YAML
    safe_title = title.replace('"', "'").replace('\n', ' ').strip()

    frontmatter_lines = [
        "---",
        f'title: "{safe_title}"',
        f'category: "{args.category}"',
        f"categoryOrder: {args.category_order}",
        f"order: {order}",
        f'source: "{args.url}"',
    ]
    if args.source_label:
        frontmatter_lines.append(f'sourceLabel: "{args.source_label}"')
    frontmatter_lines.append("---")

    markdown = "\n".join(frontmatter_lines) + f"\n\n{body}\n"

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output_dir) / f"{slug}.md"

    counter = 1
    while output_path.exists():
        output_path = Path(args.output_dir) / f"{slug}-{counter}.md"
        counter += 1

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✓ Tạo file: {output_path}")
    print(f"OUTPUT_FILE={output_path}")


if __name__ == "__main__":
    main()
