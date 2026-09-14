# -*- coding: utf-8 -*-
from pathlib import Path
import re
root = Path(r"D:\xian-shang-you-wei")
main = (root/"backend/main.py").read_text(encoding="utf-8")
idx = (root/"backend/frontend/index.html").read_text(encoding="utf-8")

keys = [
    "GUEST_DAILY_LIMIT","FREE_DAILY_LIMIT","guest_day","_guest","daily_count",
    "analyze_count","query_count","quota","FREE_DAILY","referral_unlocked",
    "_is_referral","_deep_is_premium","_deep_mask","require_user","require_paid",
    "get_opening_picks","api_deep_analysis","get_chips","get_kline","add_portfolio",
    "_taipei","Asia/Taipei","portfolio","forum_get","create_alert",
]
print("=== MAIN HITS ===")
for k in keys:
    n = main.count(k)
    if n:
        print(f"{k}: {n}")

# print definition-ish lines
print("\n=== LIMIT / COUNTER LINES ===")
for i,line in enumerate(main.splitlines(),1):
    if re.search(r"GUEST_DAILY|FREE_DAILY|daily_limit|analyze_count|guest_usage|usage_date|query_used|today_count|_guest_ip|ip_daily", line, re.I):
        print(f"{i}:{line[:160]}")

print("\n=== FE GUEST / MASK ===")
for i,line in enumerate(idx.splitlines(),1):
    if re.search(r"guest_day|GUEST_|FREE_DAILY|isPaid|isPro|guestLimit|_applyResultMasks|dailyLimit|quota", line):
        if i<2500 or "guest" in line.lower() or "limit" in line.lower() or "mask" in line.lower() or "isPaid" in line:
            if any(x in line for x in ["guest_day","GUEST","FREE_","isPaid","isPro","guestLimit","_applyResultMasks","daily","quota","cnt>"]):
                print(f"{i}:{line.strip()[:180]}")
