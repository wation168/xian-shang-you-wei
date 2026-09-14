# -*- coding: utf-8 -*-
from pathlib import Path
p = Path(r"D:\xian-shang-you-wei\backend\main.py")
t = p.read_text(encoding="utf-8")
old = "FREE_DAILY_LIMIT = 3   # 免費會員每日查詢次數\nGUEST_DAILY_LIMIT = 10  # 遊客（未登入）每日查詢次數"
new = "FREE_DAILY_LIMIT = 5   # 免費會員：完整分析＋健檢共用 daily_credit\nGUEST_DAILY_LIMIT = 3   # 遊客：個股查詢／完整分析 daily_credit"
if old not in t:
    raise SystemExit("constants anchor missing")
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("constants OK")
