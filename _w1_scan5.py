# -*- coding: utf-8 -*-
from pathlib import Path
main = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
lines = main.splitlines()
ilines = idx.splitlines()

def dump(src,a,b):
    for i in range(a,min(b,len(src))+1):
        print(f"{i}:{src[i-1]}")

print("=== /portfolio/analysis ===")
dump(lines, 9951, 10040)

print("\n=== forum_get_posts is_paid ===")
dump(lines, 10539, 10585)

print("\n=== get_chips require ===")
dump(lines, 6105, 6120)

print("\n=== get_kline ===")
dump(lines, 3496, 3510)

print("\n=== me/quota queries_limit 6725-6790 ===")
dump(lines, 6725, 6795)

print("\n=== FE _incFreeQueryCount / _getFreeQueryCount / _hasPremium ===")
for i,l in enumerate(ilines,1):
    if "_incFreeQueryCount" in l or "_getFreeQueryCount" in l or "function _hasPremium" in l or "function _incFree" in l or "function _getFree" in l:
        print(f"{i}:{l[:160]}")
