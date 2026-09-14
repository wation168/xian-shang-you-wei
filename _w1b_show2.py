# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")
main = Path(r"D:\xian-shang-you-wei\backend\main.py").read_text(encoding="utf-8")

i = idx.find("async function analyzeStock")
print("=== analyzeStock start errors ===")
print(idx[i:i+2200])
print("\n\n=== _applyResultMasks ===")
i = idx.find("function _applyResultMasks")
print("LINE", idx[:i].count("\n")+1)
print(idx[i:i+1800])

print("\n\n=== deepSection / lock / blur ===")
for s in ["deepSection", "dcard-", "lock-ov", "locked", "kbar_simple", "型態"]:
    print(s, idx.count(s))

print("\n=== report_generate sig ===")
i = main.find("def report_generate")
print("LINE", main[:i].count("\n")+1)
print(main[i:i+250])

print("\n=== _is_referral_active ===")
i = main.find("def _is_referral_active")
print("LINE", main[:i].count("\n")+1)
print(main[i:i+450])
