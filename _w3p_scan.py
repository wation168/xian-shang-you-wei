# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
for i,line in enumerate(idx.splitlines()[:180],1):
    if ":root" in line or "--bg" in line or "data-theme" in line or "search-box" in line or "topbar" in line or "body" in line[:20]:
        print(f"{i}:{line[:160]}")
print("--- cycleTheme ---")
i=idx.find("function cycleTheme")
print(idx[i:i+400] if i>=0 else "none")
