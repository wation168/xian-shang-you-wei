# -*- coding: utf-8 -*-
"""
遊戲區多語言頁面產生器（2026/08/17 建立）

輸入：
  locales.py            共用外框字典（13款遊戲共用，翻一次）
  content/g{slug}.py    單一遊戲的各語言文字（SEO內容＋UI字典）
  templates/{slug}.body.html / {slug}.css   單一遊戲的版面（語言無關）
  shared/{slug}.js      單一遊戲的邏輯（語言無關，文字全走 GAME_I18N）

輸出：
  out/games/{slug}.html            繁中（根目錄，網站既有慣例）
  out/games/{loc}/{slug}.html      其餘9語言
  out/games/shared/{slug}.js       共用邏輯（10語言共用同一份）

設計原則（《新工具規劃守則.md》第七節精神延伸到建置流程本身）：
  * 版面/邏輯/文字三者分離，任何一項改動都只需要改一個地方
  * 產生器不做「聰明的猜測」：字典缺key就直接讓建置失敗，不靜默 fallback
    （避免第十九輪「AI翻譯漏翻卻沒人發現」那類問題重演）
"""
import json
import os
import re
import importlib.util

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "out", "games")
SITE = "https://softglow-ai.com"
AD_CLIENT = "ca-pub-1768270548115739"

import locales as LOC


def load_content(slug):
    modname = "g" + slug.replace("-", "_")
    path = os.path.join(BASE, "content", "g%s.py" % slug.replace("-", "_"))
    spec = importlib.util.spec_from_file_location(modname, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fill(tmpl, ui, chrome):
    """把 {{ui.xxx}} / {{chrome.xxx}} 換成實際文字。缺key直接拋錯，不靜默留空。"""
    def repl(m):
        ns, key = m.group(1), m.group(2)
        src = ui if ns == "ui" else chrome
        if key not in src:
            raise KeyError("template placeholder {{%s.%s}} 在字典裡找不到" % (ns, key))
        return src[key]
    return re.sub(r"\{\{(ui|chrome)\.([A-Za-z0-9_]+)\}\}", repl, tmpl)


def ad(kind, slot, elid):
    if kind == "lg":
        return ('<div class="ad-container ad-container-lg" id="%s"><ins class="adsbygoogle" '
                'style="min-width:160px;min-height:250px;display:block;min-height:250px;" '
                'data-ad-client="%s" data-ad-slot="%s" data-ad-format="auto" '
                'data-full-width-responsive="true"></ins></div>' % (elid, AD_CLIENT, slot))
    return ('<div class="ad-container" id="%s"><ins class="adsbygoogle" '
            'style="min-width:160px;min-height:250px;display:block;text-align:center;min-height:100px;" '
            'data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="%s" '
            'data-ad-slot="%s"></ins></div>' % (elid, AD_CLIENT, slot))


# 相關遊戲固定推薦順序（語言無關，只有名稱會在地化）
REL_ORDER = ["2048", "sudoku", "minesweeper", "chess", "snake", "piano-tiles",
             "memory-match", "gomoku", "sliding-puzzle", "number-bomb",
             "whack-a-mole", "reaction-time-test", "halloween-spell-draw"]


def related_pills(loc, slug, n=5):
    picks = [s for s in REL_ORDER if s != slug][:n]
    out = []
    for s in picks:
        out.append('    <a class="tool-pill" href="%s">%s</a>' % (
            LOC.game_url(loc, s), LOC.GAME_NAMES[s][loc]))
    return "\n".join(out)


def lang_select(slug, cur):
    opts = []
    for loc, label in LOC.LANG_SWITCH:
        sel = " selected" if loc == cur else ""
        opts.append('<option value="%s"%s>%s</option>' % (LOC.game_url(loc, slug), sel, label))
    return ('<select class="lang-select" onchange="location.href=this.value">%s</select>'
            % "".join(opts))


def hreflangs(slug):
    rows = []
    for loc in LOC.LOCALES:
        rows.append('<link rel="alternate" hreflang="%s" href="%s%s">'
                    % (loc, SITE, LOC.game_url(loc, slug)))
    rows.append('<link rel="alternate" hreflang="x-default" href="%s%s">'
                % (SITE, LOC.game_url("en", slug)))
    return "\n".join(rows)


def ga_lang_pack(loc, slug):
    """games-auth.js 用的語言包。gameNames/scoreUnit 只帶這一頁需要的，減少每頁體積。"""
    ch = LOC.CHROME[loc]
    pack = dict(ch["ga"])
    pack["gameNames"] = {slug: LOC.GAME_NAMES[slug][loc]}
    kind = LOC.SCORE_UNIT_KIND.get(slug)
    if kind:
        pack["scoreUnit"] = {slug: LOC.SCORE_UNITS[kind][loc]}
    return pack


def build_game(slug):
    mod = load_content(slug)
    body_tmpl = open(os.path.join(BASE, "templates", "%s.body.html" % slug), encoding="utf-8").read()
    # 有些遊戲（如 reaction-time-test）樣式全在 games.css，沒有頁內 <style>，允許沒有這個檔案
    css_path = os.path.join(BASE, "templates", "%s.css" % slug)
    css = open(css_path, encoding="utf-8").read() if os.path.isfile(css_path) else ""
    # 剝掉CSS註解：原始樣式裡有中文開發註解，直接灌進9個外語頁面既是雜訊也是語言純度破口。
    # 註解的權威保存位置是 templates/{slug}.css 原始檔，不是產出的HTML。
    css = re.sub(r"/\*[\s\S]*?\*/", "", css)
    css = "\n".join(ln for ln in css.split("\n") if ln.strip()).rstrip("\n")
    written = []

    for loc in LOC.LOCALES:
        if loc not in mod.L:
            raise KeyError("%s 缺少語言 %s 的內容" % (slug, loc))
        c = mod.L[loc]
        ch = LOC.CHROME[loc]
        gname = LOC.GAME_NAMES[slug][loc]
        pfx = LOC.url_prefix(loc)
        url = SITE + LOC.game_url(loc, slug)

        # ── JSON-LD（用 json.dumps 產生，保證格式合法）──
        ld_app = {
            "@context": "https://schema.org", "@type": "WebApplication",
            "name": c["ldName"], "url": url, "description": c["ldDesc"],
            "applicationCategory": "GameApplication", "operatingSystem": "Web",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "inLanguage": loc,
        }
        ld_faq = {
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in c["faq"]
            ],
        }

        # ── 文章區 ──
        arts = []
        for block in c["articles"]:
            parts = []
            for heading, paras in block:
                parts.append("<h2>%s</h2>" % heading)
                parts.extend("<p>%s</p>" % p for p in paras)
            arts.append('  <article class="article">%s</article>' % "".join(parts))

        # ── FAQ 區 ──
        faq_items = "\n".join(
            '  <div class="faq-item"><div class="faq-q">%s</div><div class="faq-a">%s</div></div>' % (q, a)
            for q, a in c["faq"])

        body = fill(body_tmpl, c["ui"], ch)

        lb_block = ""
        mounts = ""
        if getattr(mod, "HAS_LEADERBOARD", False):
            lb_block = ('\n    <div class="ga-widget" id="gaWidget"></div>\n'
                        '    <div class="ga-leaderboard"><h3>%s</h3><div id="gaLeaderboard"></div></div>'
                        % ch["leaderboardTitle"].replace("{game}", gname))
            mounts = ("gaMountAuthWidget('gaWidget');\n"
                      "gaMountLeaderboard('gaLeaderboard', '%s');\n"
                      "gaInitFullscreenToggle();\n"
                      "gaInitLoginReminder('%s');" % (slug, slug))
        else:
            mounts = "gaInitFullscreenToggle();"

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
<script type="application/ld+json">{ld_app}</script>
<script type="application/ld+json">{ld_faq}</script>
<link rel="stylesheet" href="/tools/tools.css">
<link rel="stylesheet" href="/games/games.css">
<link rel="stylesheet" href="/common/softglow-common.css">
<meta name="sg-slug" content="{slug}">
<meta name="sg-type" content="game">
<meta name="sg-lang" content="{loc}">
<link rel="stylesheet" href="/js/cookie-consent.css">
<script src="https://accounts.google.com/gsi/client" async></script>
<style>
{css}
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
<div class="breadcrumb"><a href="/">{bcHome}</a> &gt; <a href="/games{pfx}/">{navGames}</a> &gt; {gname}</div>
<div class="container">
<div class="layout">
<div class="main">
  <div class="game-card">
    <h1>{h1}</h1>
    <p class="game-subtitle">{subtitle}</p>

{body}
{lb_block}
  </div>

{ad_calc}

{art0}

{ad_mid}

{art1}

{ad_bottom}

  <section class="faq"><h2>{faqHeading}</h2>
{faq_items}
  </section>

  <div class="more-tools"><h3>{relatedGames}</h3><div class="tools-grid">
{rel}
    <a class="tool-pill" href="/games{pfx}/">{moreGames}</a>
  </div></div>

</div>
<aside class="sidebar">
{ad_side}
  <div class="related-card"><h3>{moreGames}</h3><a class="tool-pill" href="/games{pfx}/" style="display:block;margin-top:8px">{browseAll}</a></div>
{ad_side2}
</aside>
</div></div>
<footer class="footer"><div class="footer-inner"><a href="/about.html">{footAbout}</a><a href="/contact.html">{footContact}</a><a href="/home/{loc}/privacy.html">{footPrivacy}</a><a href="/home/{loc}/terms.html">{footTerms}</a><span style="margin-left:auto">&copy; 2026 SoftGlow</span></div></footer>

<!-- Language pack for this page. Game logic lives in /games/shared/{slug}.js and is -->
<!-- shared by all 10 locales; it contains no user-facing text, only lookups into these dicts. -->
<script>
window.GAME_I18N = {game_i18n};
window.GA_LANG_PACK = {ga_pack};
</script>
<script src="/games/shared/{slug}.js"></script>

<script>
(function(){{var AD_DELAY_MS=2000;setTimeout(function(){{var s=document.createElement('script');s.async=true;s.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ad_client}';s.crossOrigin='anonymous';document.head.appendChild(s);s.onload=function(){{document.querySelectorAll('ins.adsbygoogle').forEach(function(ad){{if(ad.offsetWidth>0){{try{{(adsbygoogle=window.adsbygoogle||[]).push({{}})}}catch(e){{}}}}}})}};}},AD_DELAY_MS);}})();
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

<script src="/games/games-auth.js"></script>
<script>
{mounts}
</script>
<script src="/common/softglow-common.js"></script>
<script src="/js/softglow-cookies.js" defer></script>
</body>
</html>
""".format(
            lang=ch["htmlLang"], title=c["title"], desc=c["desc"], url=url,
            hreflang=hreflangs(slug),
            ld_app=json.dumps(ld_app, ensure_ascii=False),
            ld_faq=json.dumps(ld_faq, ensure_ascii=False),
            slug=slug, loc=loc, css=css, pfx=pfx,
            patternsHref=("/patterns/index.html" if loc == "zh-TW" else "/patterns/%s.html" % loc),
            blogHref=("/blog/" if loc == "zh-TW" else "/blog/%s/index.html" % loc),
            navTools=ch["navTools"], navGames=ch["navGames"], navPatterns=ch["navPatterns"],
            navBlog=ch["navBlog"], navHome=ch["navHome"], bcHome=ch["bcHome"],
            langsel=lang_select(slug, loc),
            gname=gname, h1=c["h1"], subtitle=c["subtitle"], body=body, lb_block=lb_block,
            ad_calc=ad("lg", "4182262477", "ad-calc"),
            ad_mid=ad("sm", "2793159185", "ad-mid"),
            ad_bottom=ad("lg", "4182262477", "ad-bottom"),
            ad_side=ad("lg", "1655301946", "ad-side"),
            ad_side2=ad("sm", "2793159185", "ad-side2"),
            art0=arts[0], art1=arts[1] if len(arts) > 1 else "",
            faqHeading=ch["faqHeading"], faq_items=faq_items,
            relatedGames=ch["relatedGames"], rel=related_pills(loc, slug),
            moreGames=ch["moreGames"], browseAll=ch["browseAll"],
            footAbout=ch["footAbout"], footContact=ch["footContact"],
            footPrivacy=ch["footPrivacy"], footTerms=ch["footTerms"],
            searchPlaceholder=ch["searchPlaceholder"],
            bmTitle=ch["bmTitle"], bmClear=ch["bmClear"],
            game_i18n=json.dumps(c["i18n"], ensure_ascii=False, indent=None),
            ga_pack=json.dumps(ga_lang_pack(loc, slug), ensure_ascii=False),
            ad_client=AD_CLIENT, mounts=mounts,
        )

        dest_dir = OUT if loc == "zh-TW" else os.path.join(OUT, loc)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, "%s.html" % slug)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(html)
        written.append(dest)

    # 共用邏輯JS（10語言共用同一份，只複製一次）
    sh_dir = os.path.join(OUT, "shared")
    os.makedirs(sh_dir, exist_ok=True)
    src_js = os.path.join(BASE, "shared", "%s.js" % slug)
    dst_js = os.path.join(sh_dir, "%s.js" % slug)
    with open(src_js, encoding="utf-8") as f:
        js = f.read()
    with open(dst_js, "w", encoding="utf-8") as f:
        f.write(js)
    written.append(dst_js)

    # games-auth.js（13款遊戲、10語言全部共用同一份；文字走 GA_LANG_PACK，預設值＝繁中原文）
    ga_src = os.path.join(BASE, "shared", "games-auth.js")
    ga_dst = os.path.join(OUT, "games-auth.js")
    with open(ga_src, encoding="utf-8") as f:
        gajs = f.read()
    with open(ga_dst, "w", encoding="utf-8") as f:
        f.write(gajs)
    written.append(ga_dst)
    return written


if __name__ == "__main__":
    import sys
    slugs = sys.argv[1:] or ["2048"]
    total = []
    for s in slugs:
        total += build_game(s)
    print("已產出 %d 個檔案：" % len(total))
    for p in total:
        print("  " + os.path.relpath(p, BASE))
