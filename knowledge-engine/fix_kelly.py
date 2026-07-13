#!/usr/bin/env python3
"""
SoftGlow Blog Generator v1.0
Generates 12 articles x 10 languages = 120 HTML pages via Haiku API.
Includes: caching, retry, Korean encoding fix, JSON repair, schema, hreflang, AdSense.

Usage:
  cd D:\\xian-shang-you-wei\\backend\\frontend
  set ANTHROPIC_API_KEY=sk-ant-api03-...
  python generate_blog.py

Options:
  --slug kd-indicator        Generate one article only
  --langs en,ja              Generate specific languages only
  --no-cache                 Ignore cache, regenerate all
"""

import os, sys, re, json, time, argparse, traceback, hashlib
try:
    import requests
except ImportError:
    print("[ERROR] pip install requests --break-system-packages"); sys.exit(1)

# ── Config ──────────────────────────────────────────────────────────────────
API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 8192
MAX_RETRIES = 3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(BASE_DIR, "blog")
CACHE_DIR = os.path.join(BASE_DIR, ".blog-cache")

LANGS = ["zh-TW", "en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN"]

# ── 12 Articles ─────────────────────────────────────────────────────────────
ARTICLES = [
    {
        "slug": "kd-indicator",
        "topic": "KD Stochastic Indicator: complete guide on calculation, golden cross/death cross, overbought/oversold zones, and practical trading strategies",
        "category": "technical-indicator",
    },
    {
        "slug": "macd-indicator",
        "topic": "MACD Indicator: histogram analysis, signal line crossovers, divergence signals, and trend reversal identification",
        "category": "technical-indicator",
    },
    {
        "slug": "rsi-indicator",
        "topic": "RSI Relative Strength Index: calculation formula, period settings, divergence reading, and combined indicator strategies",
        "category": "technical-indicator",
    },
    {
        "slug": "moving-average-guide",
        "topic": "Moving Averages complete guide: SMA vs EMA, MA arrangements, Granville's 8 rules, and practical trend-following applications",
        "category": "technical-indicator",
    },
    {
        "slug": "candlestick-patterns",
        "topic": "Candlestick Patterns: reading market language through reversal and continuation patterns including hammer, engulfing, morning star, evening star",
        "category": "candlestick",
    },
    {
        "slug": "support-resistance",
        "topic": "Support and Resistance levels: identifying key price zones, role reversal principle, and using technical indicators to confirm key levels",
        "category": "technical-analysis",
    },
    {
        "slug": "stop-loss-guide",
        "topic": "Stop Loss placement guide: where to set stops, percentage-based vs technical stops, trailing stops, and common mistakes",
        "category": "risk-management",
    },
    {
        "slug": "profit-loss-ratio",
        "topic": "Risk-Reward Ratio: calculation, why 2:1 minimum matters, how to evaluate trade quality, and practical position sizing",
        "category": "risk-management",
    },
    {
        "slug": "position-risk",
        "topic": "Position Risk management: understanding where price sits relative to support/resistance, risk assessment before entry, and position sizing",
        "category": "risk-management",
    },
    {
        "slug": "institutional-investors",
        "topic": "Institutional Investors and smart money flow: reading institutional buying/selling data, foreign investors, dealers, and investment trust signals",
        "category": "market-analysis",
    },
    {
        "slug": "stock-selection-guide",
        "topic": "Stock Selection 5-step guide for retail investors: screening criteria, fundamental checks, technical timing, entry rules, and exit planning",
        "category": "strategy",
    },
    {
        "slug": "index",
        "topic": "Financial education blog index page: overview of all available trading and investment tutorials covering technical indicators, risk management, candlestick patterns, and trading strategies",
        "category": "index",
    },
]

# ── Language config ─────────────────────────────────────────────────────────
LANG_CONFIG = {
    "zh-TW": {"name": "繁體中文", "writing_lang": "Traditional Chinese", "nav_blog": "教學文章", "nav_tools": "工具", "nav_patterns": "K棒型態", "nav_home": "首頁", "faq_title": "常見問題"},
    "en":    {"name": "English", "writing_lang": "English", "nav_blog": "Articles", "nav_tools": "Tools", "nav_patterns": "Patterns", "nav_home": "Home", "faq_title": "FAQ"},
    "ja":    {"name": "日本語", "writing_lang": "Japanese", "nav_blog": "学習記事", "nav_tools": "ツール", "nav_patterns": "ローソク足", "nav_home": "ホーム", "faq_title": "よくある質問"},
    "ko":    {"name": "한국어", "writing_lang": "Korean", "nav_blog": "학습 기사", "nav_tools": "도구", "nav_patterns": "캔들 패턴", "nav_home": "홈", "faq_title": "자주 묻는 질문"},
    "de":    {"name": "Deutsch", "writing_lang": "German", "nav_blog": "Artikel", "nav_tools": "Tools", "nav_patterns": "Kerzenmuster", "nav_home": "Startseite", "faq_title": "Häufig gestellte Fragen"},
    "fr":    {"name": "Français", "writing_lang": "French", "nav_blog": "Articles", "nav_tools": "Outils", "nav_patterns": "Chandeliers", "nav_home": "Accueil", "faq_title": "Questions fréquentes"},
    "es":    {"name": "Español", "writing_lang": "Spanish", "nav_blog": "Artículos", "nav_tools": "Herramientas", "nav_patterns": "Velas", "nav_home": "Inicio", "faq_title": "Preguntas frecuentes"},
    "pt":    {"name": "Português", "writing_lang": "Portuguese", "nav_blog": "Artigos", "nav_tools": "Ferramentas", "nav_patterns": "Padrões", "nav_home": "Início", "faq_title": "Perguntas frequentes"},
    "id":    {"name": "Bahasa Indonesia", "writing_lang": "Indonesian", "nav_blog": "Artikel", "nav_tools": "Alat", "nav_patterns": "Pola Candlestick", "nav_home": "Beranda", "faq_title": "Pertanyaan Umum"},
    "zh-CN": {"name": "简体中文", "writing_lang": "Simplified Chinese", "nav_blog": "教学文章", "nav_tools": "工具", "nav_patterns": "K线形态", "nav_home": "首页", "faq_title": "常见问题"},
}

# ── URL helpers ─────────────────────────────────────────────────────────────
def blog_url(slug, lang):
    if lang == "zh-TW":
        return f"/blog/{slug}.html"
    return f"/blog/{lang}/{slug}.html"

def blog_canonical(slug, lang):
    return f"https://softglow-ai.com{blog_url(slug, lang)}"

def build_hreflang(slug):
    tags = []
    for lang in LANGS:
        url = blog_canonical(slug, lang)
        hreflang = lang.lower()
        tags.append(f'<link rel="alternate" hreflang="{hreflang}" href="{url}">')
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{blog_canonical(slug, "en")}">')
    return "\n".join(tags)

def build_lang_buttons(slug, current_lang):
    buttons = []
    for lang in LANGS:
        url = blog_url(slug, lang)
        cls = "lang-btn active" if lang == current_lang else "lang-btn"
        name = LANG_CONFIG[lang]["name"]
        buttons.append(f'<a href="{url}" class="{cls}">{name}</a>')
    return "\n    ".join(buttons)

# ── API call ────────────────────────────────────────────────────────────────
def call_api(api_key, prompt, system_prompt):
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.post(
                API_URL,
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": MODEL,
                    "max_tokens": MAX_TOKENS,
                    "messages": [{"role": "user", "content": prompt}],
                    "system": system_prompt,
                },
                timeout=120,
            )
            if r.status_code == 529 or r.status_code == 429:
                wait = (attempt + 1) * 15
                print(f"    Rate limited ({r.status_code}), waiting {wait}s...")
                time.sleep(wait)
                continue
            if r.status_code != 200:
                print(f"    [ERR] API {r.status_code}: {r.text[:200]}")
                time.sleep(5)
                continue

            # Korean encoding fix: use content bytes, not resp.json()
            data = json.loads(r.content.decode("utf-8"))
            text = data["content"][0]["text"]
            return text

        except Exception as e:
            print(f"    [ERR] {e}")
            time.sleep(5)

    return None

# ── JSON extraction & repair ────────────────────────────────────────────────
def extract_json(text):
    """Extract JSON from API response, with repair for truncated output."""
    if not text:
        return None

    # Find outermost { }
    start = text.find("{")
    if start < 0:
        return None

    # Try parsing as-is
    candidate = text[start:]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        pass

    # Repair: find last valid closing brace
    depth = 0
    last_valid = -1
    in_string = False
    escape_next = False
    for i, ch in enumerate(candidate):
        if escape_next:
            escape_next = False
            continue
        if ch == "\\":
            escape_next = True
            continue
        if ch == '"' and not escape_next:
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                last_valid = i
                break

    if last_valid > 0:
        try:
            return json.loads(candidate[: last_valid + 1])
        except json.JSONDecodeError:
            pass

    # Last resort: brute force close
    trimmed = candidate.rstrip()
    for fix in ['"}]}', '"]}', '"}', '"]', "}", "]}"]:
        try:
            return json.loads(trimmed + fix)
        except json.JSONDecodeError:
            continue

    return None

# ── Cache ───────────────────────────────────────────────────────────────────
def cache_path(slug, lang):
    return os.path.join(CACHE_DIR, f"{slug}_{lang}.json")

def load_cache(slug, lang):
    p = cache_path(slug, lang)
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return None

def save_cache(slug, lang, data):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(cache_path(slug, lang), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── Generate article content via API ────────────────────────────────────────
def generate_article(api_key, slug, topic, category, lang, lang_config):
    is_index = (slug == "index")
    writing_lang = lang_config["writing_lang"]

    if is_index:
        system_prompt = f"""You are a financial education content writer. Write in {writing_lang}.
Output a JSON object with these fields:
- "seo_title": page title for blog index (max 60 chars)
- "seo_desc": meta description (max 155 chars)
- "intro_html": 2-3 paragraphs introducing the blog section, explaining what readers will find (HTML format)
- "articles_intro": a sentence like "Explore our tutorials below"
Return ONLY valid JSON, no markdown fences."""

        prompt = f"""Create a blog index page for a financial education platform. The blog covers: technical indicators (KD, MACD, RSI, Moving Averages), candlestick patterns, support/resistance, stop loss, risk-reward ratio, position risk, institutional investors analysis, and stock selection guide.

Write in {writing_lang}. Make the content engaging and educational. The platform is called SoftGlow."""
    else:
        system_prompt = f"""You are a financial education expert writer. Write a comprehensive tutorial article in {writing_lang}.
Output a JSON object with these fields:
- "seo_title": article title (max 60 chars)
- "seo_desc": meta description (max 155 chars)
- "article_html": complete article in HTML (use h2, h3, p, ul, ol, table tags). Minimum 1500 words for Latin languages or 800 characters for CJK. Include practical examples, common mistakes, and actionable advice.
- "faq": array of 5 objects with "q" and "a" fields (question and answer)
Return ONLY valid JSON, no markdown fences, no code blocks."""

        prompt = f"""Write a comprehensive educational article about: {topic}

Requirements:
- Write entirely in {writing_lang}
- Target audience: beginner to intermediate retail investors
- Include: concept explanation, calculation method (if applicable), practical application, common mistakes, real examples
- Use HTML tags for formatting (h2, h3, p, ul, ol, strong, table)
- Minimum length: 1500 words (Latin) or 800+ characters (CJK)
- 5 FAQ questions with concise answers
- Do NOT include success rate percentages. Use reliability levels: high/medium/low only.
- Professional but accessible tone"""

    raw = call_api(api_key, prompt, system_prompt)
    data = extract_json(raw)

    if not data:
        print(f"    [ERR] Failed to parse JSON for {slug}_{lang}")
        return None

    return data

# ── HTML template ───────────────────────────────────────────────────────────
def build_article_html(slug, lang, data, lang_config, article_info):
    is_index = (slug == "index")
    lc = lang_config
    seo_title = data.get("seo_title", slug)
    seo_desc = data.get("seo_desc", "")
    hreflang = build_hreflang(slug)
    lang_buttons = build_lang_buttons(slug, lang)
    canonical = blog_canonical(slug, lang)
    build_date = time.strftime("%Y-%m-%d")

    # Breadcrumb
    breadcrumb_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://softglow-ai.com/"},
            {"@type": "ListItem", "position": 2, "name": lc["nav_blog"], "item": "https://softglow-ai.com" + blog_url("index", lang)},
            {"@type": "ListItem", "position": 3, "name": seo_title},
        ]
    }, ensure_ascii=False)

    # Article schema
    article_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": seo_title,
        "description": seo_desc,
        "url": canonical,
        "publisher": {"@type": "Organization", "name": "SoftGlow"},
        "datePublished": build_date,
        "dateModified": build_date,
    }, ensure_ascii=False)

    # FAQ schema + HTML
    faq_html = ""
    faq_schema_str = ""
    if not is_index:
        faqs = data.get("faq", [])
        if faqs:
            faq_items = []
            faq_html_parts = []
            for fq in faqs[:5]:
                q = fq.get("q", "")
                a = fq.get("a", "")
                faq_items.append({
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a}
                })
                faq_html_parts.append(
                    f'<div class="faq-item">\n'
                    f'  <div class="faq-q">{q}</div>\n'
                    f'  <div class="faq-a">{a}</div>\n'
                    f'</div>'
                )
            faq_schema = {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": faq_items
            }
            faq_schema_str = f'<script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>'
            faq_html = "\n".join(faq_html_parts)

    # Article list for index page
    articles_list_html = ""
    if is_index:
        intro_html = data.get("intro_html", "")
        articles_intro = data.get("articles_intro", "")
        article_links = []
        for art in ARTICLES:
            if art["slug"] == "index":
                continue
            url = blog_url(art["slug"], lang)
            # Try to get a nice title from cache
            cached = load_cache(art["slug"], lang)
            title = cached.get("seo_title", art["slug"].replace("-", " ").title()) if cached else art["slug"].replace("-", " ").title()
            article_links.append(
                f'<a href="{url}" class="article-card">\n'
                f'  <h3>{title}</h3>\n'
                f'</a>'
            )
        articles_list_html = "\n".join(article_links)
        body_content = f"""
  <div class="section">
    {intro_html}
    <p>{articles_intro}</p>
  </div>
  <div class="articles-grid">
    {articles_list_html}
  </div>"""
    else:
        article_content = data.get("article_html", "")
        body_content = f"""
  <article class="section article-content">
    {article_content}
  </article>

  <div class="ad-slot" id="ad-3" aria-hidden="true"></div>

  <section class="section">
    <h2>{lc["faq_title"]}</h2>
    {faq_html}
  </section>

  <div class="ad-slot" id="ad-4" aria-hidden="true"></div>"""

    # Related articles (for non-index pages)
    related_html = ""
    if not is_index:
        related_links = []
        for art in ARTICLES:
            if art["slug"] == "index" or art["slug"] == slug:
                continue
            url = blog_url(art["slug"], lang)
            cached = load_cache(art["slug"], lang)
            title = cached.get("seo_title", art["slug"].replace("-", " ").title()) if cached else art["slug"].replace("-", " ").title()
            related_links.append(f'<a href="{url}" class="related-link">{title}</a>')
        related_html = "\n    ".join(related_links[:5])

    # Tool recommendations
    tool_slugs = ["compound-interest", "rsi-calculator", "macd-calculator", "position-size", "risk-reward"]
    tool_links = []
    for ts in tool_slugs:
        tool_url = f"/tools/{ts}.html" if lang == "zh-TW" else f"/tools/{lang}/{ts}.html"
        tool_links.append(f'<a href="{tool_url}" class="related-link">{ts.replace("-", " ").title()}</a>')
    tool_links_html = "\n    ".join(tool_links)

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{seo_title}</title>
<meta name="description" content="{seo_desc}">
<meta name="robots" content="index, follow">
<meta name="sg-slug" content="{slug}">
<meta name="sg-type" content="blog">
<meta name="sg-lang" content="{lang}">
<link rel="canonical" href="{canonical}">
{hreflang}
<script type="application/ld+json">{breadcrumb_json}</script>
<script type="application/ld+json">{article_schema}</script>
{faq_schema_str}
<link rel="stylesheet" href="/common/softglow-common.css">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:#2D3748;background:#fff;line-height:1.8;-webkit-font-smoothing:antialiased}}
a{{color:#2563EB;text-decoration:none}}
a:hover{{text-decoration:underline}}
.nav{{position:sticky;top:0;z-index:100;background:rgba(255,255,255,0.97);backdrop-filter:blur(8px);border-bottom:1px solid #E2E8F0}}
.nav-inner{{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;height:52px}}
.nav-logo{{font-size:17px;font-weight:700;color:#2D3748;letter-spacing:-0.5px}}
.nav-logo span{{color:#2563EB}}
.nav-links{{display:flex;gap:16px;align-items:center}}
.nav-links a{{font-size:13px;color:#4A5568;font-weight:500}}
.nav-links a:hover{{color:#2563EB;text-decoration:none}}
.nav-actions{{display:flex;gap:8px;align-items:center}}
.nav-actions button{{background:none;border:none;cursor:pointer;padding:6px;border-radius:6px;color:#718096}}
.nav-actions button:hover{{background:#F7FAFC;color:#2563EB}}
.breadcrumb{{max-width:1080px;margin:0 auto;padding:12px 20px;font-size:13px;color:#A0AEC0}}
.breadcrumb a{{color:#718096}}
.container{{max-width:1080px;margin:0 auto;padding:0 20px}}
.layout{{display:grid;grid-template-columns:1fr 320px;gap:32px;align-items:start}}
.section{{margin-bottom:32px}}
.article-content{{line-height:1.9}}
.article-content h2{{font-size:22px;font-weight:700;color:#1A202C;margin:32px 0 12px;padding-top:16px;border-top:1px solid #EDF2F7}}
.article-content h3{{font-size:18px;font-weight:600;color:#2D3748;margin:24px 0 10px}}
.article-content p{{margin-bottom:16px;color:#4A5568}}
.article-content ul,.article-content ol{{margin:12px 0 16px 24px;color:#4A5568}}
.article-content li{{margin-bottom:8px}}
.article-content table{{width:100%;border-collapse:collapse;margin:16px 0}}
.article-content th{{text-align:left;padding:10px 12px;background:#F7FAFC;border:1px solid #E2E8F0;font-size:13px;font-weight:600;color:#4A5568}}
.article-content td{{padding:10px 12px;border:1px solid #E2E8F0;font-size:14px}}
.article-content strong{{color:#1A202C}}
.faq-item{{border-bottom:1px solid #E2E8F0;padding:16px 0}}
.faq-q{{font-size:15px;font-weight:600;color:#2D3748;cursor:pointer;display:flex;justify-content:space-between;align-items:center}}
.faq-q::after{{content:"+";font-size:18px;color:#A0AEC0;transition:transform 0.2s}}
.faq-item.open .faq-q::after{{content:"-"}}
.faq-a{{font-size:14px;color:#718096;line-height:1.7;max-height:0;overflow:hidden;transition:max-height 0.3s,padding 0.3s}}
.faq-item.open .faq-a{{max-height:500px;padding-top:10px}}
.ad-slot{{background:#F7FAFC;border:1px dashed #CBD5E0;border-radius:8px;min-height:250px;display:flex;align-items:center;justify-content:center;color:#A0AEC0;font-size:12px;margin:24px 0}}
.sidebar{{position:sticky;top:68px}}
.related-card{{background:#F7FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:20px;margin-bottom:20px}}
.related-card h3{{font-size:15px;font-weight:600;margin-bottom:12px;color:#1A202C}}
.related-link{{display:block;padding:8px 0;border-bottom:1px solid #EDF2F7;font-size:13px;color:#2563EB}}
.related-link:last-child{{border-bottom:none}}
.related-link:hover{{text-decoration:none;color:#1D4ED8}}
.articles-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;margin:24px 0}}
.article-card{{display:block;padding:20px;background:#F7FAFC;border:1px solid #E2E8F0;border-radius:12px;transition:border-color 0.2s}}
.article-card:hover{{border-color:#2563EB;text-decoration:none}}
.article-card h3{{font-size:15px;font-weight:600;color:#1A202C;margin:0}}
.lang-bar{{display:flex;gap:6px;flex-wrap:wrap;margin:24px 0}}
.lang-btn{{font-size:12px;padding:4px 12px;border-radius:20px;background:#F7FAFC;border:1px solid #E2E8F0;color:#718096}}
.lang-btn:hover{{background:#EBF5FF;border-color:#BEE3F8;text-decoration:none}}
.lang-btn.active{{background:#2563EB;color:#fff;border-color:#2563EB}}
.disclaimer{{font-size:12px;color:#A0AEC0;margin:24px 0;padding:16px;background:#FAFAFA;border-radius:8px}}
.footer{{border-top:1px solid #E2E8F0;padding:24px 0;margin-top:40px}}
.footer-inner{{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;flex-wrap:wrap;gap:16px;font-size:12px;color:#A0AEC0}}
.footer-inner a{{color:#718096}}
@media(max-width:768px){{
  .layout{{grid-template-columns:1fr}}
  .sidebar{{position:static}}
  .nav-links{{gap:10px}}
}}
</style>
</head>
<body>

<nav class="nav">
<div class="nav-inner">
  <a href="/" class="nav-logo">Soft<span>Glow</span></a>
  <div class="nav-links">
    <a href="/tools/{'' if lang == 'zh-TW' else lang + '/'}">{lc["nav_tools"]}</a>
    <a href="{blog_url('index', lang)}">{lc["nav_blog"]}</a>
    <a href="/patterns/{'index.html' if lang == 'zh-TW' else lang + '/'}">{lc["nav_patterns"]}</a>
    <a href="/">{lc["nav_home"]}</a>
  </div>
  <div class="nav-actions">
    <button onclick="document.getElementById('sgSearchOverlay').classList.add('show')" title="Search">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
    </button>
    <button onclick="window._sgToggleBm&&window._sgToggleBm()" title="Bookmarks">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
    </button>
  </div>
</div>
</nav>

<div class="breadcrumb">
  <a href="/">{lc["nav_home"]}</a> &rsaquo; <a href="{blog_url('index', lang)}">{lc["nav_blog"]}</a>{'' if is_index else f' &rsaquo; {seo_title}'}
</div>

<div class="container">
<div class="layout">

<div class="main">
  <h1 style="font-size:28px;font-weight:700;color:#1A202C;margin-bottom:8px">{seo_title}</h1>
  <p style="font-size:14px;color:#718096;margin-bottom:24px">{seo_desc}</p>

  <div class="ad-slot" id="ad-1" aria-hidden="true"></div>

  {body_content}

  <div class="disclaimer">
    {seo_desc} &mdash; Last updated: {build_date}
  </div>

  <div class="lang-bar">
    {lang_buttons}
  </div>
</div>

<aside class="sidebar">
  <div class="ad-slot" id="ad-side" aria-hidden="true"></div>
  {'<div class="related-card"><h3>' + lc["nav_blog"] + '</h3>' + related_html + '</div>' if not is_index else ''}
  <div class="related-card">
    <h3>{lc["nav_tools"]}</h3>
    {tool_links_html}
  </div>
</aside>

</div>
</div>

<footer class="footer">
<div class="footer-inner">
  <a href="/about.html">About</a>
  <a href="/contact.html">Contact</a>
  <a href="/privacy.html">Privacy</a>
  <a href="/terms.html">Terms</a>
  <span style="margin-left:auto">&copy; 2026 SoftGlow</span>
</div>
</footer>

<!-- Search Overlay -->
<div class="search-overlay" id="sgSearchOverlay">
  <div class="search-box">
    <div class="search-input-wrap">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input class="search-input" id="sgSearchInput" type="text" placeholder="Search..." autocomplete="off">
    </div>
    <div class="search-results" id="sgSearchResults"></div>
  </div>
</div>

<!-- Bookmark Panel -->
<div class="bm-panel" id="sgBmPanel">
  <div class="bm-header">
    <h3>Bookmarks</h3>
    <button class="bm-clear" onclick="window._sgClearBm&&window._sgClearBm()">Clear</button>
  </div>
  <div class="bm-list" id="sgBmList"></div>
</div>

<script src="/common/softglow-common.js"></script>
<script>
document.querySelectorAll('.faq-q').forEach(function(q){{
  q.addEventListener('click',function(){{this.parentElement.classList.toggle('open');}});
}});
</script>

<!-- AdSense delayed load -->
<script>
setTimeout(function(){{
  var s=document.createElement('script');
  s.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1768270548115739';
  s.async=true;s.crossOrigin='anonymous';
  document.head.appendChild(s);
}},2000);
</script>

<!-- Generator: blog-gen v1.0 | {slug} | {lang} | {build_date} -->
</body>
</html>"""
    return html

# ── File output ─────────────────────────────────────────────────────────────
def write_html(slug, lang, html):
    if lang == "zh-TW":
        out_dir = BLOG_DIR
    else:
        out_dir = os.path.join(BLOG_DIR, lang)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{slug}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path

# ── Main ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", help="Generate one article only")
    parser.add_argument("--langs", help="Comma-separated langs (default: all 10)")
    parser.add_argument("--no-cache", action="store_true", help="Ignore cache")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("[ERROR] set ANTHROPIC_API_KEY")
        sys.exit(1)

    langs = args.langs.split(",") if args.langs else LANGS
    articles = ARTICLES
    if args.slug:
        articles = [a for a in ARTICLES if a["slug"] == args.slug]
        if not articles:
            print(f"[ERROR] slug '{args.slug}' not found")
            sys.exit(1)

    total = len(articles) * len(langs)
    generated = 0
    skipped = 0
    errors = 0
    done = 0

    print(f"SoftGlow Blog Generator v1.0")
    print(f"{'=' * 60}")
    print(f"Articles: {len(articles)} | Languages: {len(langs)} | Total: {total}")
    print(f"Cache: {CACHE_DIR}")
    print(f"Output: {BLOG_DIR}")
    print()

    # Generate articles first (not index), then index last so it can read cached titles
    sorted_articles = [a for a in articles if a["slug"] != "index"] + [a for a in articles if a["slug"] == "index"]

    for article in sorted_articles:
        slug = article["slug"]
        topic = article["topic"]
        category = article["category"]

        for lang in langs:
            done += 1
            lc = LANG_CONFIG[lang]

            # Check cache
            if not args.no_cache:
                cached = load_cache(slug, lang)
                if cached:
                    print(f"  [{done}/{total}] {slug}_{lang} CACHED")
                    html = build_article_html(slug, lang, cached, lc, article)
                    write_html(slug, lang, html)
                    skipped += 1
                    continue

            print(f"  [{done}/{total}] {slug}_{lang} API...", end=" ", flush=True)
            data = generate_article(api_key, slug, topic, category, lang, lc)

            if data is None:
                print("FAILED")
                errors += 1
                continue

            save_cache(slug, lang, data)
            html = build_article_html(slug, lang, data, lc, article)
            out = write_html(slug, lang, html)
            generated += 1
            print("OK")

            # Rate limit: 0.5s between calls
            time.sleep(0.5)

    print(f"\n{'=' * 60}")
    print(f"Done! Generated: {generated} | Cached: {skipped} | Errors: {errors}")
    print(f"Output: {BLOG_DIR}")
    print()
    print("Next steps:")
    print("  1. python generate_search_index.py   (rebuild search index)")
    print("  2. git add -A && git commit && git push")


if __name__ == "__main__":
    main()
