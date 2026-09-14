# -*- coding: utf-8 -*-
from pathlib import Path
main = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
lines = main.splitlines()
ilines = idx.splitlines()

def dump(src, start, end):
    for i in range(start, min(end, len(src))+1):
        print(f"{i}:{src[i-1]}")

print("=== query_log schema / guest increment ===")
for i,l in enumerate(lines,1):
    if "query_log" in l or "CREATE TABLE" in l and ("query" in l or "member" in l):
        print(f"{i}:{l[:180]}")

print("\n=== analyze guest/free increment 4650-4730 ===")
dump(lines, 4648, 4735)

print("\n=== report_generate 8716-8760 ===")
dump(lines, 8716, 8765)

print("\n=== add_portfolio 9888-9930 ===")
dump(lines, 9888, 9935)

print("\n=== opening picks 7360-7420 ===")
dump(lines, 7360, 7425)

print("\n=== deep 10188-10280 ===")
dump(lines, 10188, 10280)
