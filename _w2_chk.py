# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
i = idx.find("function _homeGo")
print(idx[i:i+1800])
print("==== cards ====")
n=0
for line in idx.splitlines():
    if "home-ia-card" in line:
        n+=1
        print(line.strip()[:120])
print("count lines", n, "substr", idx.count("home-ia-card"))
print("homeIaGrid count", idx.count("id=\"homeIaGrid\""))
