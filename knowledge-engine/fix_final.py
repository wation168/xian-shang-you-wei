#!/usr/bin/env python3
"""
fix_final.py — Fix ALL remaining issues in one pass
1. softglow-common.js: Fuse keys 'titles' → 'names' (搜尋壞掉的根本原因)
2. homepage.html: 加搜尋/收藏按鈕 + 彩票連結
3. patterns/index.html: 黑底舊版 → 白底 V3 + 10 語言
4. Blog: 檢查新版 V3 是否存在

Run from: D:\\xian-shang-you-wei\\knowledge-engine
"""
import os, re, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(SCRIPT_DIR, "..", "backend", "frontend")
COMMON_DIR = os.path.join(BASE, "common")
PATTERNS_DIR = os.path.join(BASE, "patterns")
BLOG_DIR = os.path.join(BASE, "blog")

LANGS = ["zh-TW", "en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN"]
LANG_NAMES = {"zh-TW":"繁中","en":"EN","ja":"日本語","ko":"한국어","de":"DE","fr":"FR","es":"ES","pt":"PT","id":"ID","zh-CN":"简中"}


def sp(msg):
    try: print(msg)
    except: print(msg.encode("utf-8",errors="replace").decode("utf-8"))


# ═══════════════════════════════════════════════════════════════════════
# FIX 1: softglow-common.js — Fuse keys 'titles' → 'names'
# ═══════════════════════════════════════════════════════════════════════
def fix_search_keys():
    js_path = os.path.join(COMMON_DIR, "softglow-common.js")
    if not os.path.exists(js_path):
        sp("  [WARN] softglow-common.js not found")
        return False

    with open(js_path, "r", encoding="utf-8") as f:
        content = f.read()

    # The bug: Fuse keys use 'titles.xx' but search-index.json uses 'names.xx'
    old = "keys: ['titles.' + META.lang, 'titles.en', 'slug']"
    new = "keys: ['names.' + META.lang, 'names.en', 'slug']"

    if old in content:
        content = content.replace(old, new)
        with open(js_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True

    if "names." in content and "Fuse" in content:
        sp("  Already fixed")
        return False

    sp("  [WARN] Could not find Fuse keys pattern to replace")
    return False


# ═══════════════════════════════════════════════════════════════════════
# FIX 2: homepage.html — 加搜尋/收藏按鈕 + 彩票連結
# ═══════════════════════════════════════════════════════════════════════
def fix_homepage():
    hp_path = os.path.join(BASE, "homepage.html")
    if not os.path.exists(hp_path):
        sp("  [WARN] homepage.html not found")
        return False

    with open(hp_path, "r", encoding="utf-8") as f:
        content = f.read()

    changed = False

    # 1. Add softglow-common.css if missing
    if "softglow-common.css" not in content:
        content = content.replace("</head>",
            '<link rel="stylesheet" href="/common/softglow-common.css">\n'
            '<meta name="sg-slug" content="homepage">\n'
            '<meta name="sg-type" content="page">\n'
            '<meta name="sg-lang" content="zh-TW">\n'
            '</head>')
        changed = True

    # 2. Add nav-actions (search/bookmark) to nav if missing
    if "nav-actions" not in content:
        # Find the closing </div> of nav-links and add nav-actions after it
        nav_actions = '''
  <div class="nav-actions">
    <button class="act-btn primary" onclick="sgOpenSearch()" title="搜尋"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></button>
    <button class="act-btn primary" id="sgBmBtn" onclick="sgToggleBookmark()" ondblclick="sgToggleBmPanel()" title="收藏"><svg viewBox="0 0 24 24"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg></button>
  </div>'''
        # Insert before the closing of nav-inner
        content = content.replace('</div>\n</nav>', nav_actions + '\n</div>\n</nav>', 1)
        changed = True

    # 3. Add lottery link if missing
    if "lottery" not in content.lower():
        # Add lottery link to nav-links
        content = content.replace(
            '<a href="/about.html">關於</a>',
            '<a href="https://lottery.softglow-ai.com" target="_blank">🎰 彩票</a>\n    <a href="/about.html">關於</a>'
        )
        changed = True

    # 4. Add search overlay + bookmark panel + softglow-common.js before </body>
    if "sgSearchOverlay" not in content:
        overlay = '''
<!-- Search Overlay -->
<div class="search-overlay" id="sgSearchOverlay">
  <div class="search-box">
    <div class="search-input-wrap">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input class="search-input" id="sgSearchInput" type="text" placeholder="輸入關鍵字搜尋工具、型態、文章…" autocomplete="off">
    </div>
    <div class="search-results" id="sgSearchResults"></div>
  </div>
</div>
<div class="bm-panel" id="sgBmPanel">
  <div class="bm-header"><h3>我的收藏</h3><button class="bm-clear" onclick="window._sgClearBm()">全部清除</button></div>
  <div class="bm-list" id="sgBmList"></div>
</div>
<script src="/common/softglow-common.js"></script>'''
        content = content.replace("</body>", overlay + "\n</body>")
        changed = True

    if changed:
        with open(hp_path, "w", encoding="utf-8") as f:
            f.write(content)

    return changed


# ═══════════════════════════════════════════════════════════════════════
# FIX 3: patterns/index.html — 黑底舊版 → 白底 V3
# ═══════════════════════════════════════════════════════════════════════
def rebuild_patterns_index():
    """Scan actual pattern files and build V3 white-theme index pages for all 10 languages."""
    # Scan pattern slugs from disk
    patterns = []
    for fname in sorted(os.listdir(PATTERNS_DIR)):
        if not fname.endswith(".html") or fname in ("index.html", "en.html", "ja.html", "ko.html"):
            continue
        slug = fname[:-5]
        # Read title from file
        fpath = os.path.join(PATTERNS_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                head = f.read(3000)
            m = re.search(r"<title>(.*?)</title>", head)
            title = re.split(r"\s*[|—–]\s*", m.group(1))[0].strip() if m else slug.replace("-", " ").title()
        except:
            title = slug.replace("-", " ").title()
        patterns.append({"slug": slug, "title_zhTW": title})

    if not patterns:
        sp("  [WARN] No pattern files found")
        return 0

    # For other languages, read titles from their subdirectories
    for lang in LANGS:
        if lang == "zh-TW":
            continue
        lang_dir = os.path.join(PATTERNS_DIR, lang)
        if not os.path.isdir(lang_dir):
            continue
        for p in patterns:
            fpath = os.path.join(lang_dir, p["slug"] + ".html")
            if os.path.exists(fpath):
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        head = f.read(3000)
                    m = re.search(r"<title>(.*?)</title>", head)
                    if m:
                        title = re.split(r"\s*[|—–]\s*", m.group(1))[0].strip()
                        p[f"title_{lang}"] = title
                except:
                    pass

    pages_built = 0
    for lang in LANGS:
        dropdown_opts = []
        for l in LANGS:
            url = "/patterns/index.html" if l == "zh-TW" else f"/patterns/{l}.html"
            sel = " selected" if l == lang else ""
            dropdown_opts.append(f'<option value="{url}"{sel}>{LANG_NAMES[l]}</option>')
        dropdown = '<select onchange="location.href=this.value" style="padding:4px 8px;border-radius:6px;border:1px solid #CBD5E0;font-size:13px;background:#fff;color:#4A5568;cursor:pointer">' + "".join(dropdown_opts) + '</select>'

        page_title = {"zh-TW":"K棒型態完全解析","en":"Candlestick Patterns","ja":"ローソク足パターン","ko":"캔들스틱 패턴","de":"Kerzenmuster","fr":"Chandeliers japonais","es":"Patrones de velas","pt":"Padrões de velas","id":"Pola Candlestick","zh-CN":"K线形态解析"}.get(lang,"Candlestick Patterns")
        page_desc = {"zh-TW":"完整學習50+種K棒型態，含SVG圖解與實戰應用","en":"Learn 50+ candlestick patterns with charts and strategies"}.get(lang,"Learn 50+ candlestick patterns")
        tools_url = "/tools/" if lang == "zh-TW" else f"/tools/{lang}/"
        blog_url = "/blog/" if lang == "zh-TW" else f"/blog/{lang}/index.html"
        patterns_url = "/patterns/index.html" if lang == "zh-TW" else f"/patterns/{lang}.html"

        cards = []
        for p in patterns:
            title_key = f"title_{lang}" if lang != "zh-TW" else "title_zhTW"
            title = p.get(title_key, p.get("title_zhTW", p["slug"]))
            if lang == "zh-TW":
                url = f"/patterns/{p['slug']}.html"
            else:
                url = f"/patterns/{lang}/{p['slug']}.html"
            cards.append(f'<a href="{url}" class="card">{title}</a>')

        cards_html = "\n      ".join(cards)

        html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title} - SoftGlow</title>
<meta name="description" content="{page_desc}">
<meta name="robots" content="index, follow">
<link rel="stylesheet" href="/common/softglow-common.css">
<meta name="sg-slug" content="patterns-index">
<meta name="sg-type" content="page">
<meta name="sg-lang" content="{lang}">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;color:#2D3748;background:#fff;line-height:1.6}}
a{{color:#2563EB;text-decoration:none}}
.nav{{position:sticky;top:0;z-index:100;background:rgba(255,255,255,0.95);backdrop-filter:blur(8px);border-bottom:1px solid #E2E8F0}}
.nav-inner{{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;height:52px}}
.nav-logo{{font-size:17px;font-weight:700;color:#2D3748}}.nav-logo span{{color:#2563EB}}
.nav-links{{display:flex;gap:12px;align-items:center}}.nav-links a{{font-size:13px;color:#4A5568;font-weight:500}}
.nav-actions{{display:flex;gap:6px;align-items:center}}
.container{{max-width:1080px;margin:0 auto;padding:20px}}
.header{{text-align:center;padding:40px 0 20px}}
.header h1{{font-size:28px;font-weight:700;color:#1A202C}}
.header p{{color:#718096;margin-top:8px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin:24px 0}}
.card{{display:block;padding:14px 16px;background:#F7FAFC;border:1px solid #E2E8F0;border-radius:10px;font-size:14px;color:#2D3748;transition:all 0.15s}}
.card:hover{{background:#EBF5FF;border-color:#BEE3F8;text-decoration:none;transform:translateY(-1px)}}
.footer{{border-top:1px solid #E2E8F0;padding:24px 0;margin-top:40px}}
.footer-inner{{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;flex-wrap:wrap;gap:16px;font-size:12px;color:#A0AEC0}}
.footer-inner a{{color:#718096}}
@media(max-width:768px){{.grid{{grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:8px}}.card{{padding:12px;font-size:13px}}}}
</style>
</head>
<body>
<nav class="nav">
<div class="nav-inner">
  <a href="/" class="nav-logo">Soft<span>Glow</span></a>
  <div class="nav-links">
    <a href="{tools_url}">{"工具" if lang in ("zh-TW","zh-CN") else "Tools"}</a>
    <a href="{patterns_url}">{"K棒型態" if lang=="zh-TW" else "Patterns"}</a>
    <a href="{blog_url}">{"教學" if lang in ("zh-TW","zh-CN") else "Blog"}</a>
    <a href="/">{"首頁" if lang in ("zh-TW","zh-CN") else "Home"}</a>
  </div>
  <div class="nav-actions">
    {dropdown}
    <button class="act-btn primary" onclick="sgOpenSearch()" title="Search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></button>
    <button class="act-btn primary" id="sgBmBtn" onclick="sgToggleBookmark()" ondblclick="sgToggleBmPanel()" title="Bookmark"><svg viewBox="0 0 24 24"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg></button>
  </div>
</div>
</nav>

<div class="container">
  <div class="header">
    <h1>{page_title}</h1>
    <p>{len(patterns)} {"種型態" if lang in ("zh-TW","zh-CN") else " patterns"}</p>
  </div>
  <div class="grid">
      {cards_html}
  </div>
</div>

<footer class="footer">
<div class="footer-inner">
  <a href="/about.html">About</a>
  <a href="/contact.html">Contact</a>
  <a href="/privacy.html">Privacy</a>
  <a href="/terms.html">Terms</a>
  <span style="margin-left:auto">© 2026 SoftGlow</span>
</div>
</footer>

<div class="search-overlay" id="sgSearchOverlay">
  <div class="search-box">
    <div class="search-input-wrap">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input class="search-input" id="sgSearchInput" type="text" placeholder="Search..." autocomplete="off">
    </div>
    <div class="search-results" id="sgSearchResults"></div>
  </div>
</div>
<div class="bm-panel" id="sgBmPanel">
  <div class="bm-header"><h3>Bookmarks</h3><button class="bm-clear" onclick="window._sgClearBm()">Clear</button></div>
  <div class="bm-list" id="sgBmList"></div>
</div>
<script src="/common/softglow-common.js"></script>
</body>
</html>'''

        # Write file
        if lang == "zh-TW":
            out_path = os.path.join(PATTERNS_DIR, "index.html")
        else:
            out_path = os.path.join(PATTERNS_DIR, f"{lang}.html")

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        pages_built += 1

    return pages_built


# ═══════════════════════════════════════════════════════════════════════
# FIX 4: Check blog file status
# ═══════════════════════════════════════════════════════════════════════
def check_blog():
    """Check if blog files are old version (dark theme) or new V3."""
    old_count = 0
    new_count = 0
    missing = 0

    blog_slugs = ["kd-indicator", "macd-indicator", "rsi-indicator",
                   "moving-average-guide", "candlestick-patterns",
                   "support-resistance", "stop-loss-guide",
                   "profit-loss-ratio", "position-risk",
                   "institutional-investors", "stock-selection-guide"]

    for lang in LANGS:
        for slug in blog_slugs:
            if lang == "zh-TW":
                fpath = os.path.join(BLOG_DIR, f"{slug}.html")
            else:
                fpath = os.path.join(BLOG_DIR, lang, f"{slug}.html")

            if not os.path.exists(fpath):
                missing += 1
                continue

            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    head = f.read(1000)
                # Old version markers: dark theme colors, "線上有位" in nav
                if "var(--bg)" in head or "#0a0a12" in head or "#0d1117" in head:
                    old_count += 1
                else:
                    new_count += 1
            except:
                missing += 1

    return old_count, new_count, missing


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════
def main():
    sp("=" * 60)
    sp("Fix Final — All remaining issues")
    sp("=" * 60)

    # Fix 1: Search keys
    sp("\n[1/4] Fixing softglow-common.js search keys (titles→names)...")
    if fix_search_keys():
        sp("  ✓ Fixed: 'titles' → 'names'")
    else:
        sp("  → Already correct or file not found")

    # Fix 2: Homepage
    sp("\n[2/4] Fixing homepage (search/bookmark buttons + lottery link)...")
    if fix_homepage():
        sp("  ✓ Added: search button, bookmark button, lottery link")
    else:
        sp("  → Already has buttons or file not found")

    # Fix 3: Patterns index
    sp("\n[3/4] Rebuilding patterns index pages (black→white, 4→10 langs)...")
    count = rebuild_patterns_index()
    sp(f"  ✓ Built {count} index pages")

    # Fix 4: Blog check
    sp("\n[4/4] Checking blog file status...")
    old, new, missing = check_blog()
    sp(f"  Old (dark theme): {old}")
    sp(f"  New (V3 white):   {new}")
    sp(f"  Missing:          {missing}")
    if old > 0:
        sp(f"  ⚠ {old} blog pages still have dark theme!")
        sp(f"  → Run generate_blog.py to regenerate, or check if output is in wrong directory")
        # Check if blog cache exists
        cache_dir = os.path.join(BASE, ".blog-cache")
        if os.path.isdir(cache_dir):
            cache_count = len([f for f in os.listdir(cache_dir) if f.endswith(".json")])
            sp(f"  → Found .blog-cache/ with {cache_count} cached entries")

    # Summary
    sp(f"\n{'='*60}")
    sp("Done! Push:")
    sp("  cd D:\\xian-shang-you-wei")
    sp("  git add -A")
    sp('  git commit -m "fix: search keys + homepage buttons + patterns V3 + lottery"')
    sp("  git push")


if __name__ == "__main__":
    main()
