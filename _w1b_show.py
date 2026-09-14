# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
main = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")
ilines = idx.splitlines()
mlines = main.splitlines()

def dump_around(text, needle, before=5, after=40, label=""):
    i = text.find(needle)
    print("===", label or needle, "at", i, "===")
    if i<0:
        return
    start = text.rfind("\n", 0, max(0,i-1))
    # print with rough line
    line = text[:i].count("\n")+1
    chunk = text[i:i+2500]
    print("LINE", line)
    print(chunk[:2200])
    print()

print("--- analyzeStock 429 ---")
i = idx.find("if(r.status===429)")
print("line", idx[:i].count("\n")+1)
print(idx[i:i+900])

print("\n--- analyze fail ---")
i = idx.find("分析失敗")
print("count", idx.count("分析失敗"))
while i>=0:
    print("L", idx[:i].count("\n")+1, idx[max(0,i-80):i+80].replace("\n"," | "))
    i = idx.find("分析失敗", i+1)

print("\n--- portfolio fetch ---")
for key in ["portfolio/analysis", "showPortfolioPage", "today_limit", "guest_limit"]:
    print(key, idx.count(key))

i = idx.find("/portfolio/analysis")
print("LINE", idx[:i].count("\n")+1)
print(idx[i-200:i+800])
