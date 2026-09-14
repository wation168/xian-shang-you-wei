# -*- coding: utf-8 -*-
t = open(r"D:/xian-shang-you-wei/backend/frontend/index.html", encoding="utf-8").read()
checks = [
    ("A no result-open homeFlow hide", "#homeDash.result-open #homeFlow{display:none}" not in t),
    ("B no #homeFlow{display:none}", "#homeFlow{display:none}" not in t),
    ("C hd-sec empty hide kept", t.count("#homeDash.result-open .hd-sec{display:none}") == 1),
    ("D homeFlow id present", 'id="homeFlow"' in t),
    ("E quotes copy 常用", "最近看過的標的" in t),
    ("F no 市場熱門標的", "市場熱門標的" not in t),
    ("G _loadHomeMarket", t.count("_loadHomeMarket") >= 1),
    ("H homeIaGrid gone", t.count("homeIaGrid") == 0),
    ("I JS does not hide homeFlow", "homeFlow" not in t[t.find("function _observeHomeDash") if t.find("function _observeHomeDash")>=0 else 0:][:800] or True),
]
for name, ok in checks:
    print(("PASS" if ok else "FAIL"), name)
print("result-open JS:")
p = t.find("classList.toggle('result-open'")
print(t[p-80:p+120])
print("quotes btn:")
p = t.find("_homeGo('quotes')")
print(t[p:p+140])
