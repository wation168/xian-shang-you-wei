# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
i = idx.find("function showPage")
print("LINE", idx[:i].count("\n")+1)
print(idx[i:i+1800])
print("\n=== pageOverlay / pageContent ===")
for n,line in enumerate(idx.splitlines(),1):
    if "pageOverlay" in line or "pageContent" in line or "desktopMain" in line:
        if n<1400 or "function" in line:
            print(f"{n}:{line.strip()[:160]}")
