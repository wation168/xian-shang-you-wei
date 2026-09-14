# patch apply.py chip leftover + industry/news titles
from pathlib import Path
p = Path(r"D:/xian-shang-you-wei/_ia1/apply.py")
t = p.read_text(encoding="utf-8")
old = "t = t.replace(old_chip2, new_chip_head, 1)\n"
if old not in t:
    raise SystemExit("no chip replace line")
add = r'''
leftover_src = (
    "          +'<div class=\"mkt-src\">'+_mktEsc((it.source||'')+' \u00b7 \u53f0\u5317 '+(it.as_of||''))+'</div>'\n"
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

old_news_box = "box.innerHTML = '<div class=\"mkt-meta\">'+_mktEsc(meta.join(' · ')||'\u4f86\u6e90\uff1a\u92d2\u4ea8')+'</div>'"
new_news_box = "box.innerHTML = '<h2>\u4eca\u5929\u8981\u805e</h2><div class=\"v5-sub\">'+_mktEsc(meta.join(' \u00b7 ')||'\u4f86\u6e90\uff1a\u92d2\u4ea8')+'</div>'"
if t.count(old_news_box) != 1:
    raise SystemExit("news box %s" % t.count(old_news_box))
t = t.replace(old_news_box, new_news_box, 1)
'''
# The add above is for apply.py to execute against index.html — insert before write
# apply.py already has news-item class replace; insert leftover+titles before the news replace
needle = '# news item class\n'
if needle not in t:
    raise SystemExit("no news marker")
t = t.replace(needle, add + "\n# news item class\n", 1)
p.write_text(t, encoding="utf-8")
print("apply.py patched", len(t))
