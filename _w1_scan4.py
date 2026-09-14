# -*- coding: utf-8 -*-
from pathlib import Path
main = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
lines = main.splitlines()
ilines = idx.splitlines()

def dump(src, a, b):
    for i in range(a, min(b, len(src))+1):
        print(f"{i}:{src[i-1]}")

print("=== query_log CREATE ===")
dump(lines, 2878, 2898)

print("\n=== portfolio analysis ===")
for i,l in enumerate(lines,1):
    if "portfolio" in l.lower() and (l.strip().startswith("def ") or l.strip().startswith("@app")):
        print(f"{i}:{l[:160]}")

print("\n=== forum defs ===")
for i,l in enumerate(lines,1):
    if "def forum_" in l or "/api/forum" in l:
        print(f"{i}:{l[:160]}")

print("\n=== FE analyzeStock guest 2305-2340 ===")
dump(ilines, 2300, 2345)
print("\n=== FE guest_day 2625-2645 ===")
dump(ilines, 2620, 2650)
print("\n=== FE _applyResultMasks 4913-4970 ===")
dump(ilines, 4913, 4972)
print("\n=== FE loadChips 3600-3625 ===")
dump(ilines, 3600, 3625)
