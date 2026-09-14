# -*- coding: utf-8 -*-
from pathlib import Path
root = Path(r"D:\xian-shang-you-wei")
# find crawler
for p in root.rglob("*crawler*"):
    if p.is_file() and p.suffix in (".py",".md"):
        print("FILE", p)
main = (root/"backend/main.py").read_text(encoding="utf-8")
print("\n=== _fetch_stock_news ===")
i = main.find("def _fetch_stock_news")
print(main[i:i+900])
print("\n=== top_gainers return ===")
i = main.find("def get_top_gainers")
print(main[i:i+900])
print("\n=== FinMind dataset names ===")
for i,l in enumerate(main.splitlines(),1):
    if "dataset" in l.lower() or "TaiwanStock" in l:
        if "TaiwanStock" in l or "dataset" in l:
            print(f"{i}:{l.strip()[:160]}")
