# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html")
t = p.read_text(encoding="utf-8")
print(t[t.find(":root[data-theme=\"dark\"]"):t.find(":root[data-theme=\"dark\"]")+450])
print("====")
print(t[t.find(":root:not([data-theme])"):t.find(":root:not([data-theme])")+350])
print("==== home-ia-card deep line")
for line in t.splitlines():
    if "home-ia-ttl\">DEEP" in line or "homeIaUpgrade" in line:
        print(line[:200])
