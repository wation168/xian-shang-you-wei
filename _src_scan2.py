# -*- coding: utf-8 -*-
from pathlib import Path
main = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")
lines = main.splitlines()
print("=== index-ish ===")
for i,l in enumerate(lines,1):
    if any(k in l for k in ["加權","櫃買","台指","TAIEX","TaiwanStockIndex","電子指數","金融指數","IX0001","發行量加權"]):
        print(f"{i}:{l[:180]}")
print("\n=== news ===")
for i,l in enumerate(lines,1):
    if "news" in l.lower() or "rss" in l.lower() or "cnyes" in l.lower():
        print(f"{i}:{l[:180]}")
print("\n=== sector/industry ===")
for i,l in enumerate(lines,1):
    if any(k in l for k in ["產業","sector","industry_strength","族群"]):
        print(f"{i}:{l[:180]}")
print("\n=== cron/schedule ===")
for i,l in enumerate(lines,1):
    if "cron" in l.lower() or "APScheduler" in l or "add_job" in l:
        print(f"{i}:{l[:180]}")
