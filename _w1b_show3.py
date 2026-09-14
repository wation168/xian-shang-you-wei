# -*- coding: utf-8 -*-
from pathlib import Path
idx = Path(r"D:\xian-shang-you-wei\backend\frontend\index.html").read_text(encoding="utf-8")

i = idx.find("function renderAnalysisCards")
print("=== renderAnalysisCards LINE", idx[:i].count("\n")+1)
print(idx[i:i+1600])

i = idx.find("id=\"deepSection\"")
print("\n=== deepSection HTML LINE", idx[:i].count("\n")+1)
print(idx[i:i+1200])

print("\n=== _hasPremium ===")
i = idx.find("function _hasPremium")
print("LINE", idx[:i].count("\n")+1)
print(idx[i:i+400])

print("\n=== FreeLimitModal ===")
i = idx.find("function _showFreeLimitModal")
print(idx[i:i+400] if i>=0 else "NO _showFreeLimitModal")
i = idx.find("id=\"freeLimitModal\"")
print("modal html", i, "LINE", idx[:i].count("\n")+1 if i>=0 else None)
if i>=0:
    print(idx[i:i+600])
