# -*- coding: utf-8 -*-
"""
遊戲區索引頁產生器 /games/index.html (zh-TW) + /games/{loc}/index.html (其餘9語言)

跟 build.py 是同一套設計原則的延伸（版面/文字分離、缺key直接失敗不靜默 fallback），
但這個頁面本身沒有互動邏輯，純粹是13款遊戲的卡片牆，所以不需要 shared/{slug}.js
那一套，只需要 locales.py（共用外框）＋ content/gindex.py（索引頁專屬文字）＋
每款遊戲 content/g{slug}.py 的 tileDesc（卡片描述，10語言都已經翻好，直接借用，
不必為索引頁重新寫一次）。

輸出：
  out/games/index.html          繁中（根目錄，網址不變，SEO資產不流失）
  out/games/{loc}/index.html    其餘9語言
"""
import json
import os

import locales as LOC
from build import ad, AD_CLIENT, load_content

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "out", "games")
SITE = "https://softglow-ai.com"

# 卡片牆順序＋emoji：照抄原始 /mnt/user-data/uploads/games/index.html 的 GAMES 陣列，
# 語言無關（emoji不用翻譯），10語言共用同一份順序，不重新排序、不因語言而異
GAMES_ORDER = [
    ("reaction-time-test", "⚡"),
    ("whack-a-mole", "🔨"),
    ("memory-match", "🃏"),
    ("piano-tiles", "🎹"),
    ("gomoku", "⚫"),
    ("snake", "🐍"),
    ("halloween-spell-draw", "🎃"),
    ("2048", "🔢"),
    ("sudoku", "🧩"),
    ("sliding-puzzle", "🔲"),
    ("chess", "♟️"),
    ("number-bomb", "💣"),
    ("minesweeper", "🚩"),
]


def load_index_content():
    import importlib.util
    path = os.path.join(BASE, "content", "gindex.py")
    spec = importlib.util.spec_from_file_location("gindex", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.L


def hreflangs_index():
    rows = []
    for loc in LOC.LOCALES:
        rows.append('<link rel="alternate" hreflang="%s" href="%s%s">'
                    % (loc, SITE, LOC.index_url(loc)))
    rows.append('<link rel="alternate" hreflang="x-default" href="%s%s">'
                % (SITE, LOC.index_url("en")))
    return "\n".join(rows)


def lang_select_index(cur):
    opts = []
    for loc, label in LOC.LANG_SWITCH:
        sel = " selected" if loc == cur else ""
        opts.append('<option value="%s"%s>%s</option>' % (LOC.index_url(loc), sel, label))
    return ('<select class="lang-select" onchange="location.href=this.value">%s</select>'
            % "".join(opts))


def build_index():
    idx_content = load_index_content()
    # 每款遊戲的10語言 tileDesc 一次讀出來，避免每個語言迴圈裡重複 import 13次
    game_content = {slug: load_content(slug) for slug, _ in GAMES_ORDER}
    written = []

    for loc in LOC.LOCALES:
        if loc not in idx_content:
            raise KeyError("games索引頁缺少語言 %s 的內容" % loc)
        c = idx_content[loc]
        ch = LOC.CHROME[loc]
        pfx = LOC.url_prefix(loc)
        url = SITE + LOC.index_url(loc)

        games_list = []
        for slug, emoji in GAMES_ORDER:
            mod = game_content[slug]
            if loc not in mod.L:
                raise KeyError("%s 缺少語言 %s 的內容" % (slug, loc))
            games_list.append({
                "slug": slug,
                "name": LOC.GAME_NAMES[slug][loc],
                "emoji": emoji,
                "desc": mod.L[loc]["tileDesc"],
                "status": "live",
            })

        ld = {
            "@context": "https://schema.org", "@type": "CollectionPage",
            "name": c["h1"], "url": url, "description": c["ldDesc"],
            "inLanguage": loc,
        }

        html = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://securepubads.g.doubleclick.net">
<link rel="preconnect" href="https://pagead2.googlesyndication.com">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
{hreflang}
<script type="application/ld+json">{ld}</script>
<link rel="stylesheet" href="/tools/tools.css">
<link rel="stylesheet" href="/games/games.css">
<link rel="stylesheet" href="/common/softglow-common.css">
<meta name="sg-slug" content="games-index">
<meta name="sg-type" content="game">
<meta name="sg-lang" content="{loc}">
<link rel="stylesheet" href="/js/cookie-consent.css">
<style>
.games-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin-top:20px}}
.game-tile{{display:block;background:#fff;border-radius:14px;padding:20px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.08);text-decoration:none;transition:transform .15s ease}}
.game-tile:hover{{transform:translateY(-3px)}}
.game-tile .gt-emoji{{font-size:36px;display:block;margin-bottom:10px}}
.game-tile .gt-name{{font-size:16px;font-weight:700;color:#1e3a5f}}
.game-tile .gt-desc{{font-size:12px;color:#94a3b8;margin-top:4px}}
.game-tile.gt-soon{{opacity:.55;cursor:default}}
</style>
</head>
<body>
<nav class="nav">
<div class="nav-inner">
  <a href="/" class="nav-logo">Soft<span>Glow</span></a>
  <div class="nav-links">
    <a href="/tools{pfx}/">{navTools}</a>
    <a href="/games{pfx}/">{navGames}</a>
    <a href="{patternsHref}">{navPatterns}</a>
    <a href="{blogHref}">{navBlog}</a>
    <a href="/">{navHome}</a>
  </div>
  <div class="nav-actions">
    {langsel}
    <button class="act-btn primary" onclick="sgOpenSearch()" title="Search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></button>
    <button class="act-btn primary" id="sgBmBtn" onclick="sgToggleBookmark()" ondblclick="sgToggleBmPanel()" title="Bookmark"><svg viewBox="0 0 24 24"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg></button>
    <button class="act-btn secondary" onclick="sgShare()" title="Share"><svg viewBox="0 0 24 24"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg></button>
  </div>
</div>
</nav>
<div class="breadcrumb"><a href="/">{bcHome}</a> &gt; {navGames}</div>
<div class="container">
<div class="layout">
<div class="main">
  <div class="game-card">
    <h1>{h1}</h1>
    <p class="game-subtitle">{subtitle}</p>

    <div class="games-grid" id="gamesGrid"></div>
    <noscript>
      <div class="games-grid">
        <a class="game-tile" href="{firstGameHref}">
          <span class="gt-emoji">{firstEmoji}</span>
          <div class="gt-name">{firstName}</div>
          <div class="gt-desc">{firstDesc}</div>
        </a>
      </div>
    </noscript>
  </div>

  {ad_calc}

  <article class="article"><h2>{articleH2}</h2><p>{articleP}</p></article>

  <div class="more-tools"><h3>{moreToolsHeading}</h3><div class="tools-grid">
    <a class="tool-pill" href="{typingSpeedHref}">{typingSpeedName}</a>
    <a class="tool-pill" href="/tools{pfx}/">{browseAllTools}</a>
  </div></div>

</div>
<aside class="sidebar">
  {ad_side}
</aside>
</div></div>
<footer class="footer"><div class="footer-inner"><a href="/about.html">{footAbout}</a><a href="/contact.html">{footContact}</a><a href="/home/{loc}/privacy.html">{footPrivacy}</a><a href="/home/{loc}/terms.html">{footTerms}</a><span style="margin-left:auto">&copy; 2026 SoftGlow</span></div></footer>

<script>
const CONFIG = {{ adLoadDelayMs: 2000 }};
const GAMES = {games_json};

function renderGameTile(g) {{
  const emoji = '<span class="gt-emoji">' + g.emoji + '</span>';
  const name  = '<div class="gt-name">' + g.name + '</div>';
  const desc  = '<div class="gt-desc">' + g.desc + '</div>';
  if (g.status === 'live' && g.slug) {{
    return '<a class="game-tile" href="{gameHrefPrefix}' + g.slug + '.html">' + emoji + name + desc + '</a>';
  }}
  return '<div class="game-tile gt-soon">' + emoji + name + desc + '</div>';
}}

(function () {{
  const grid = document.getElementById('gamesGrid');
  if (grid) grid.innerHTML = GAMES.map(renderGameTile).join('');
}})();

setTimeout(function(){{var s=document.createElement('script');s.async=true;s.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ad_client}';s.crossOrigin='anonymous';document.head.appendChild(s);s.onload=function(){{document.querySelectorAll('ins.adsbygoogle').forEach(function(ad){{if(ad.offsetWidth>0){{try{{(adsbygoogle=window.adsbygoogle||[]).push({{}})}}catch(e){{}}}}}})}};}},CONFIG.adLoadDelayMs);
</script>

<!-- Search Overlay -->
<div class="search-overlay" id="sgSearchOverlay">
  <div class="search-box">
    <div class="search-input-wrap">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input class="search-input" id="sgSearchInput" type="text" placeholder="{searchPlaceholder}" autocomplete="off">
    </div>
    <div class="search-results" id="sgSearchResults"></div>
  </div>
</div>

<!-- Bookmark Panel -->
<div class="bm-panel" id="sgBmPanel">
  <div class="bm-header">
    <h3>{bmTitle}</h3>
    <button class="bm-clear" onclick="window._sgClearBm()">{bmClear}</button>
  </div>
  <div class="bm-list" id="sgBmList"></div>
</div>

<script src="/common/softglow-common.js"></script>
<script src="/js/softglow-cookies.js" defer></script>
</body>
</html>
""".format(
            lang=ch["htmlLang"], title=c["title"], desc=c["desc"], url=url,
            hreflang=hreflangs_index(),
            ld=json.dumps(ld, ensure_ascii=False),
            loc=loc, pfx=pfx,
            patternsHref=("/patterns/index.html" if loc == "zh-TW" else "/patterns/%s.html" % loc),
            blogHref=("/blog/" if loc == "zh-TW" else "/blog/%s/index.html" % loc),
            navTools=ch["navTools"], navGames=ch["navGames"], navPatterns=ch["navPatterns"],
            navBlog=ch["navBlog"], navHome=ch["navHome"], bcHome=ch["bcHome"],
            langsel=lang_select_index(loc),
            h1=c["h1"], subtitle=c["subtitle"],
            firstGameHref=LOC.game_url(loc, games_list[0]["slug"]),
            firstEmoji=games_list[0]["emoji"], firstName=games_list[0]["name"], firstDesc=games_list[0]["desc"],
            ad_calc=ad("lg", "4182262477", "ad-calc"),
            ad_side=ad("lg", "1655301946", "ad-side"),
            articleH2=c["articleH2"], articleP=c["articleP"],
            moreToolsHeading=c["moreToolsHeading"],
            typingSpeedHref=("/tools/typing-speed.html" if loc == "zh-TW" else "/tools/%s/typing-speed.html" % loc),
            typingSpeedName=c["typingSpeedName"], browseAllTools=c["browseAllTools"],
            footAbout=ch["footAbout"], footContact=ch["footContact"],
            footPrivacy=ch["footPrivacy"], footTerms=ch["footTerms"],
            games_json=json.dumps(games_list, ensure_ascii=False),
            gameHrefPrefix=("/games/" if loc == "zh-TW" else "/games/%s/" % loc),
            ad_client=AD_CLIENT,
            searchPlaceholder=ch["searchPlaceholder"],
            bmTitle=ch["bmTitle"], bmClear=ch["bmClear"],
        )

        dest_dir = OUT if loc == "zh-TW" else os.path.join(OUT, loc)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, "index.html")
        with open(dest, "w", encoding="utf-8") as f:
            f.write(html)
        written.append(dest)

    return written


if __name__ == "__main__":
    total = build_index()
    print("已產出 %d 個索引頁：" % len(total))
    for p in total:
        print("  " + os.path.relpath(p, BASE))
