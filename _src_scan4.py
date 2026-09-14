# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\stock_picker\crawler.py")
t = p.read_text(encoding="utf-8") if p.exists() else ""
print("exists", p.exists(), "len", len(t))
for i,l in enumerate(t.splitlines(),1):
    if "def fetch" in l or "rss" in l.lower() or "cnyes" in l.lower() or "http" in l.lower() and ("news" in l.lower() or "rss" in l.lower()):
        print(f"{i}:{l[:160]}")
print("--- fetch_cnyes ---")
i=t.find("def fetch_cnyes_news")
print(t[i:i+800] if i>=0 else "missing")
print("\n=== peers industry ===")
main=Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")
j=main.find("同產業個股列表")
print(main[j:j+700])
