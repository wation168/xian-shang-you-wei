# -*- coding: utf-8 -*-
from pathlib import Path
main = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")
lines = main.splitlines()

def dump(start, end):
    for i in range(start, min(end, len(lines))+1):
        print(f"{i}:{lines[i-1]}")

# find function defs around counters
needles = [
    "def _check_daily", "def _inc_counter", "def _cval", "def _guest",
    "def _taipei", "CREATE TABLE", "analyze_count", "query_count",
    "def require_user", "def require_paid", "def _is_referral",
    "def _deep_is_premium", "def _deep_mask", "def get_opening_picks",
    "def api_deep_analysis", "def get_chips", "def get_kline",
    "def add_portfolio", "def report_generate", "FREE_DAILY",
]
print("=== DEF LINES ===")
for i,l in enumerate(lines,1):
    if any(n in l for n in ["def _check","def _inc_","def _cval","def _guest","def require_","def _is_referral","def _deep_","def get_opening","def api_deep","def get_chips","def get_kline","def add_portfolio","def report_generate","def forum_","CREATE TABLE users","daily_used","query_date"]):
        if l.strip().startswith("def ") or "CREATE TABLE" in l or "daily" in l.lower() and ("used" in l or "count" in l or "date" in l):
            print(f"{i}:{l[:140]}")

print("\n--- around 3380-3480 ---")
dump(3360, 3480)
print("\n--- around 110-140 ---")
dump(110, 140)
