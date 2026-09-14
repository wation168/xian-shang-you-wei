# -*- coding: utf-8 -*-
p = r"D:/xian-shang-you-wei/backend/frontend/index.html"
t = open(p, encoding="utf-8").read()
old = "#homeDash.result-open #homeFlow{display:none}\n"
if t.count(old) != 1:
    raise SystemExit("css count %s" % t.count(old))
t = t.replace(old, "", 1)
old2 = '<span class="v5-tag">熱門</span><b>市場熱門標的</b><span class="v5-lock">既有強勢列</span>'
new2 = '<span class="v5-tag">常用</span><b>最近看過的標的</b><span class="v5-lock">常用／熱鍵</span>'
if t.count(old2) != 1:
    raise SystemExit("copy count %s" % t.count(old2))
t = t.replace(old2, new2, 1)
if "#homeDash.result-open #homeFlow{display:none}" in t:
    raise SystemExit("hide rule still present")
if "#homeFlow{display:none}" in t:
    raise SystemExit("forbidden homeFlow display none still present")
if t.count("#homeDash.result-open .hd-sec{display:none}") != 1:
    raise SystemExit("lost hd-sec hide")
if 'id="homeFlow"' not in t:
    raise SystemExit("lost homeFlow")
open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ok", len(t))
print("hide_rule", "#homeDash.result-open #homeFlow{display:none}" in t)
print("forbidden", "#homeFlow{display:none}" in t)
print("hdsec", t.count("#homeDash.result-open .hd-sec{display:none}"))
print("quotes_tag_ok", "最近看過的標的" in t)
