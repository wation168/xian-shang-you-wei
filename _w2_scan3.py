# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
main = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")

print("=== hotkeys loader ===")
i = idx.find("hotkeysEl")
print("count", idx.count("hotkeysEl"))
for i,line in enumerate(idx.splitlines(),1):
    if "hotkeys" in line.lower() or "top_gainers" in line:
        print(f"{i}:{line.strip()[:180]}")

print("\n=== chips / analyze entry ===")
for s in ["function loadChips", "function analyzeStock", "function showUpgradeModal", "C._currentId", "_currentId"]:
    i = idx.find(s)
    print(s, "L", idx[:i].count("\n")+1 if i>=0 else None)

print("\n=== top_gainers docstring ===")
i = main.find("def get_top_gainers")
print(main[i:i+350])

print("\n=== stats ===")
i = main.find("/api/stats")
print(main[i:i+250])

print("\n=== index/taiex/twii in main ===")
for i,line in enumerate(main.splitlines(),1):
    low=line.lower()
    if any(k in low for k in ["taiex","twii","加權","大盤","ix0001","tse_index"]):
        print(f"{i}:{line.strip()[:160]}")
