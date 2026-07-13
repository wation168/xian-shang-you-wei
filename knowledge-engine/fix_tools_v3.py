#!/usr/bin/env python3
"""
fix_tools_v3.py — Upgrade all tool pages to V3 architecture
1. Add softglow-common.css + sg-meta tags to <head>
2. Replace nav with V3 nav (nav-links + nav-actions with 4 buttons + lang dropdown)
3. Remove duplicate lang-bar div
4. Add search overlay + bookmark panel before </body>
5. Add softglow-common.js script

Run from: D:\\xian-shang-you-wei\\knowledge-engine
"""
import os, re, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(SCRIPT_DIR, "..", "backend", "frontend", "tools")

LANGS = ["zh-TW", "en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN"]
LANG_NAMES = {
    "zh-TW": "繁中", "en": "EN", "ja": "日本語", "ko": "한국어",
    "de": "DE", "fr": "FR", "es": "ES", "pt": "PT", "id": "ID", "zh-CN": "简中"
}

NAV = {
    "tools": {"zh-TW":"工具","en":"Tools","ja":"ツール","ko":"도구","de":"Tools","fr":"Outils","es":"Herramientas","pt":"Ferramentas","id":"Alat","zh-CN":"工具"},
    "patterns": {"zh-TW":"K棒型態","en":"Patterns","ja":"ローソク足","ko":"캔들 패턴","de":"Muster","fr":"Chandeliers","es":"Patrones","pt":"Padrões","id":"Pola","zh-CN":"K线形态"},
    "blog": {"zh-TW":"教學文章","en":"Blog","ja":"ブログ","ko":"블로그","de":"Blog","fr":"Blog","es":"Blog","pt":"Blog","id":"Blog","zh-CN":"博客"},
    "home": {"zh-TW":"首頁","en":"Home","ja":"ホーム","ko":"홈","de":"Startseite","fr":"Accueil","es":"Inicio","pt":"Início","id":"Beranda","zh-CN":"首页"},
}

SEARCH_HINT = {
    "zh-TW":"搜尋工具、型態、文章…","en":"Search tools, patterns, articles…",
    "ja":"ツール、パターン、記事を検索…","ko":"도구, 패턴, 기사 검색…",
    "de":"Tools, Muster, Artikel suchen…","fr":"Rechercher outils, modèles, articles…",
    "es":"Buscar herramientas, patrones, artículos…","pt":"Pesquisar ferramentas, padrões, artigos…",
    "id":"Cari alat, pola, artikel…","zh-CN":"搜索工具、形态、文章…",
}

BM_TITLE = {"zh-TW":"我的收藏","en":"Bookmarks","ja":"ブックマーク","ko":"북마크","de":"Lesezeichen","fr":"Favoris","es":"Favoritos","pt":"Favoritos","id":"Bookmark","zh-CN":"我的收藏"}
BM_CLEAR = {"zh-TW":"全部清除","en":"Clear all","ja":"全て削除","ko":"모두 삭제","de":"Alle löschen","fr":"Tout effacer","es":"Borrar todo","pt":"Limpar tudo","id":"Hapus semua","zh-CN":"全部清除"}


def sp(msg):
    try: print(msg)
    except: print(msg.encode("utf-8",errors="replace").decode("utf-8"))


def detect_lang(filepath):
    parts = filepath.replace("\\","/").split("/")
    for lang in LANGS:
        if lang in parts:
            return lang
    return "zh-TW"


def detect_slug(filepath):
    return os.path.basename(filepath).replace(".html","")


def get_tool_url(slug, lang):
    return f"/tools/{slug}.html" if lang == "zh-TW" else f"/tools/{lang}/{slug}.html"


def build_lang_select(slug, lang):
    opts = []
    for l in LANGS:
        url = get_tool_url(slug, l)
        sel = " selected" if l == lang else ""
        opts.append(f'<option value="{url}"{sel}>{LANG_NAMES[l]}</option>')
    return '<select class="lang-select" onchange="location.href=this.value">' + "".join(opts) + '</select>'


def build_v3_nav(slug, lang):
    tools_url = "/tools/" if lang == "zh-TW" else f"/tools/{lang}/"
    patterns_url = "/patterns/index.html" if lang == "zh-TW" else f"/patterns/{lang}.html"
    blog_url = "/blog/" if lang == "zh-TW" else f"/blog/{lang}/index.html"
    lang_select = build_lang_select(slug, lang)

    return f'''<nav class="nav">
<div class="nav-inner">
  <a href="/" class="nav-logo">Soft<span>Glow</span></a>
  <div class="nav-links">
    <a href="{tools_url}">{NAV["tools"].get(lang,"Tools")}</a>
    <a href="{patterns_url}">{NAV["patterns"].get(lang,"Patterns")}</a>
    <a href="{blog_url}">{NAV["blog"].get(lang,"Blog")}</a>
    <a href="/">{NAV["home"].get(lang,"Home")}</a>
  </div>
  <div class="nav-actions">
    {lang_select}
    <button class="act-btn primary" onclick="sgOpenSearch()" title="Search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></button>
    <button class="act-btn primary" id="sgBmBtn" onclick="sgToggleBookmark()" ondblclick="sgToggleBmPanel()" title="Bookmark"><svg viewBox="0 0 24 24"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg></button>
    <button class="act-btn secondary" onclick="sgShare()" title="Share"><svg viewBox="0 0 24 24"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg></button>
    <button class="act-btn secondary" onclick="sgPrint()" title="Print"><svg viewBox="0 0 24 24"><path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg></button>
  </div>
</div>
</nav>'''


def build_search_overlay(lang):
    hint = SEARCH_HINT.get(lang, SEARCH_HINT["en"])
    return f'''
<!-- Search Overlay -->
<div class="search-overlay" id="sgSearchOverlay">
  <div class="search-box">
    <div class="search-input-wrap">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input class="search-input" id="sgSearchInput" type="text" placeholder="{hint}" autocomplete="off">
    </div>
    <div class="search-results" id="sgSearchResults"></div>
  </div>
</div>

<!-- Bookmark Panel -->
<div class="bm-panel" id="sgBmPanel">
  <div class="bm-header">
    <h3>{BM_TITLE.get(lang, "Bookmarks")}</h3>
    <button class="bm-clear" onclick="window._sgClearBm()">{BM_CLEAR.get(lang, "Clear all")}</button>
  </div>
  <div class="bm-list" id="sgBmList"></div>
</div>

<script src="/common/softglow-common.js"></script>'''


def fix_tool_page(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except:
        return False

    original = content
    lang = detect_lang(filepath)
    slug = detect_slug(filepath)

    # 1. Add softglow-common.css if not present
    if "softglow-common.css" not in content:
        # Insert before </head> or before existing <link rel="stylesheet">
        css_link = '<link rel="stylesheet" href="/common/softglow-common.css">'
        if "</head>" in content:
            content = content.replace("</head>", css_link + "\n</head>")

    # 2. Add sg-meta tags if not present
    if 'name="sg-slug"' not in content:
        meta_tags = f'<meta name="sg-slug" content="{slug}">\n<meta name="sg-type" content="tool">\n<meta name="sg-lang" content="{lang}">'
        if "</head>" in content:
            content = content.replace("</head>", meta_tags + "\n</head>")

    # 3. Replace entire <nav>...</nav> with V3 nav
    new_nav = build_v3_nav(slug, lang)
    nav_pattern = r'<nav class="nav">.*?</nav>'
    if re.search(nav_pattern, content, re.DOTALL):
        content = re.sub(nav_pattern, new_nav, content, count=1, flags=re.DOTALL)

    # 4. Remove duplicate lang-bar div (my earlier fix added this)
    lang_bar_pattern = r'<div class="lang-bar"[^>]*>.*?</div>\s*'
    content = re.sub(lang_bar_pattern, '', content, count=1, flags=re.DOTALL)

    # 5. Add search overlay + bookmark panel + softglow-common.js before </body>
    if "sgSearchOverlay" not in content:
        overlay = build_search_overlay(lang)
        content = content.replace("</body>", overlay + "\n</body>")

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    sp("=" * 60)
    sp("Fix Tools V3 — Add search/bookmark/share/print to all tools")
    sp("=" * 60)

    if not os.path.isdir(TOOLS_DIR):
        sp(f"[ERROR] {TOOLS_DIR} not found")
        sys.exit(1)

    fixed = 0
    total = 0
    for root, _, files in os.walk(TOOLS_DIR):
        for fname in files:
            if not fname.endswith(".html") or fname == "index.html":
                continue
            fp = os.path.join(root, fname)
            total += 1
            if fix_tool_page(fp):
                fixed += 1

    sp(f"\nScanned: {total} | Fixed: {fixed}")
    sp(f"\nNext:")
    sp(f"  cd D:\\xian-shang-you-wei")
    sp(f"  git add -A")
    sp(f'  git commit -m "feat: V3 nav + search/bookmark/share/print on all tools"')
    sp(f"  git push")


if __name__ == "__main__":
    main()
