# -*- coding: utf-8 -*-
from pathlib import Path
import re
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
main = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")

pages = sorted(set(re.findall(r"showPage\(['\"]([^'\"]+)['\"]\)", idx)))
print("PAGES", pages)

print("\n=== tabs ===")
for i,line in enumerate(idx.splitlines(),1):
    s=line.strip()
    if ("desktop-tab" in s or "class=\"nav-btn" in s or "class='nav-btn" in s) and "function" not in s:
        print(f"{i}:{s[:200]}")

print("\n=== API GET ===")
for i,line in enumerate(main.splitlines(),1):
    if "@app.get(" in line and "/api/" in line:
        print(f"{i}:{line.strip()[:160]}")

print("\n=== stockInput / home search ===")
for i,line in enumerate(idx.splitlines(),1):
    if "stockInput" in line or "id=\"home" in line or "class=\"search" in line:
        if i<1400:
            print(f"{i}:{line.strip()[:180]}")
