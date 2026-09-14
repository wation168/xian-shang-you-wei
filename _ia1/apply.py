# -*- coding: utf-8 -*-
import os, ast
HERE = os.path.dirname(os.path.abspath(__file__))
IDX = r"D:\xian-shang-you-wei\backend\frontend\index.html"
css = open(os.path.join(HERE, "v5.css"), encoding="utf-8").read()
html = open(os.path.join(HERE, "home_flow.html"), encoding="utf-8").read()
if not html.endswith("\n"):
    html += "\n"
t = open(IDX, encoding="utf-8").read()

start = '  <div id="homeDash">\n'
end = '  <div class="result" id="resultEl">\n'
i = t.find(start)
j = t.find(end)
if i < 0 or j < i:
    raise SystemExit("homeDash markers fail %s %s" % (i, j))
t = t[:i] + html + "\n" + t[j:]

css_mark = ".hd-sec{margin-bottom:18px}"
if t.count(css_mark) != 1:
    raise SystemExit("css mark %s" % t.count(css_mark))
if "#homeFlow{" not in t:
    t = t.replace(css_mark, css + "\n" + css_mark, 1)

old_tabs = (
    '    <button class="desktop-tab-btn active" onclick="showPage(\'home\')" data-page="home">📊 分析</button>\n'
    '    <button class="desktop-tab-btn" onclick="showPage(\'watch\')" data-page="watch">⭐ 自選</button>\n'
    '    <button class="desktop-tab-btn" onclick="showPage(\'picks\')" data-page="picks">🔥 精選股</button>\n'
    '    <button class="desktop-tab-btn" onclick="showPage(\'portfolio\')" data-page="portfolio">💼 持股健檢</button>\n'
    '    <button class="desktop-tab-btn" onclick="showPage(\'forum\')" data-page="forum">💬 討論</button>\n'
    '    <button class="desktop-tab-btn" onclick="showPage(\'my\')" data-page="my">👤 我的</button>\n'
)
new_tabs = (
    '    <button class="desktop-tab-btn active" onclick="showPage(\'home\')" data-page="home">首頁</button>\n'
    '    <button class="desktop-tab-btn" onclick="_homeGo(\'picks\')" data-page="picks">發現機會</button>\n'
    '    <button class="desktop-tab-btn" onclick="_homeGo(\'analyze\')" data-page="home">個股分析</button>\n'
    '    <button class="desktop-tab-btn" onclick="_homeGo(\'deep\')" data-page="home">深度分析</button>\n'
    '    <button class="desktop-tab-btn" onclick="showPage(\'watch\')" data-page="watch">我的投資</button>\n'
    '    <button class="desktop-tab-btn" onclick="showPage(\'forum\')" data-page="forum">社群</button>\n'
)
if t.count(old_tabs) != 1:
    raise SystemExit("tabs mark %s" % t.count(old_tabs))
t = t.replace(old_tabs, new_tabs, 1)

# market chips → v5
old_chip = (
    "        return '<div class=\"mkt-chip\">'\n"
    "          +'<div class=\"mkt-name\">'+_mktEsc(it.name||'')+'</div>'\n"
    "          +'<div class=\"mkt-val\">'+_mktEsc(_mktFmt(it.value,2))+'</div>'\n"
    "          +_mktChgHtml(it.change, it.change_pct)\n"
    "          +'<div class=\"mkt-src\">'+_mktEsc((it.source||'')+' · 台北 '+(it.as_of||''))+'</div>'\n"
    "          +'</div>';\n"
)
# current file uses unicode escapes in the source string
old_chip2 = (
    "        return '<div class=\"mkt-chip\">'\n"
    "          +'<div class=\"mkt-name\">'+_mktEsc(it.name||'')+'</div>'\n"
    "          +'<div class=\"mkt-val\">'+_mktEsc(_mktFmt(it.value,2))+'</div>'\n"
    "          +_mktChgHtml(it.change, it.change_pct)\n"
)
new_chip_head = (
    "        const up = Number(it.change_pct)>0; const dn = Number(it.change_pct)<0;\n"
    "        const cls = up?'v5-up':(dn?'v5-dn':'v5-flat');\n"
    "        const sign = up?'+':'';\n"
    "        return '<div class=\"v5-market\">'\n"
    "          +'<span>'+_mktEsc(it.name||'')+'</span>'\n"
    "          +'<b>'+_mktEsc(_mktFmt(it.value,2))+'</b>'\n"
    "          +'<span class=\"'+cls+'\">'+_mktEsc(sign+_mktFmt(it.change_pct,2)+'%')+'</span>'\n"
    "          +'<div class=\"v5-src\">'+_mktEsc((it.source||'')+' · 台北 '+(it.as_of||''))+'</div>'\n"
    "          +'</div>';\n"
)
if t.count(old_chip2) != 1:
    raise SystemExit("chip head %s" % t.count(old_chip2))
# drop leftover mkt-src line if present after replace of head only
t = t.replace(old_chip2, new_chip_head, 1)

# after chips shown, set hero updated
old_show = "      if(meta) meta.textContent = bits.join(' · ');\n      _mktShow('homeMktRow');"
new_show = (
    "      if(meta) meta.textContent = bits.join(' · ');\n"
    "      const hu=document.getElementById('homeHeroUpdated');\n"
    "      if(hu && j.as_of) hu.textContent='上次更新：台北時間 '+j.as_of;\n"
    "      _mktShow('homeMktRow');"
)
if t.count(old_show) != 1:
    raise SystemExit("show mkt %s" % t.count(old_show))
t = t.replace(old_show, new_show, 1)

# industry rows → v5 bars
old_row = "        return '<div class=\"ind-row\"><div><div>'+_mktEsc(it.name||it.full_name||'')+'</div>'\n          +'<div class=\"mkt-src\">'+_mktEsc(it.source+' · 台北 '+it.as_of)+'</div></div>'\n          +'<span class=\"mkt-chg '+cls+'\">'+_mktEsc(sign+_mktFmt(p,2)+'%')+'</span></div>';"
# may be unicode escaped
idx_row = t.find("return '<div class=\"ind-row\"")
print("ind_row_pos", idx_row)
if idx_row < 0:
    idx_row = t.find("return '<div class=\"ind-row\">")
print("ind_row_pos2", t.find("ind-row"))


leftover_src = (
    "          +'<div class=\"mkt-src\">'+_mktEsc((it.source||'')+' \\u00b7 \\u53f0\\u5317 '+(it.as_of||''))+'</div>'\n"
    "          +'</div>';\n"
)
if t.count(leftover_src) != 1:
    raise SystemExit("leftover src %s" % t.count(leftover_src))
t = t.replace(leftover_src, "", 1)

# industry card title
old_ind_box = "box.innerHTML = '<div class=\"mkt-meta\">'+_mktEsc(meta.join(' · '))+'</div>'"
new_ind_box = "box.innerHTML = '<h2>\u9322\u5f80\u54ea</h2><div class=\"v5-sub\">'+_mktEsc(meta.join(' \u00b7 '))+'</div>'"
if t.count(old_ind_box) != 1:
    raise SystemExit("ind box %s" % t.count(old_ind_box))
t = t.replace(old_ind_box, new_ind_box, 1)

old_news_head = "box.innerHTML = '<div class=\"mkt-meta\">'+_mktEsc(meta.join(' \u00b7 ')||'"
new_news_head = "box.innerHTML = '<h2>\u4eca\u5929\u8981\u805e</h2><div class=\"v5-sub\">'+_mktEsc(meta.join(' \u00b7 ')||'"
if t.count(old_news_head) != 1:
    raise SystemExit("news head %s" % t.count(old_news_head))
t = t.replace(old_news_head, new_news_head, 1)

# news item class
t = t.replace('class="news-item"', 'class="v5-news-item"', 2)
t = t.replace("class=\"news-list\"", "class=\"v5-news\"")

for token in ("_homeGo", "deepLocked", "_loadHomeMarket", "homeWatchPreview", "wsGroupFilterM", "stockInput", "_check_daily_credit"):
    if token not in t and token != "_check_daily_credit":
        # credit is in main.py
        if token not in t:
            raise SystemExit("lost "+token)

# credit lives in main.py — skip
if "homeWatchPreview" not in t:
    raise SystemExit("lost watch preview")
if "home-ia-grid" in t and 'id="homeIaGrid"' in t:
    raise SystemExit("old 9-grid still in HTML")

open(IDX, "w", encoding="utf-8", newline="\n").write(t)
print("applied", len(t))
