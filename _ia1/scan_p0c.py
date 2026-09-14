# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8")
t = open(r"D:/xian-shang-you-wei/backend/frontend/index.html", encoding="utf-8").read()
print("len", len(t))
print("edf6ff search", t.count(".search-box input{color:#edf6ff}"))
print("1a1a18 search", t.count(".search-box input{color:#1a1a18}"))
print("placeholder rule", t.count("::placeholder"))
print("m-hint 9px", ".m-hint{font-size:9px" in t)
print("m-hint 12px", ".m-hint{font-size:12px" in t)
print("home-ia-ttl edf6ff", ".home-ia-ttl{font-size:16px;color:#edf6ff}" in t)
print("status 11", ".status{font-size:11px;color:var(--text3)" in t)
# print exact current rules
import re
for pat in [r"\.search-box input\{[^}]+\}", r"\.search-box input::placeholder\{[^}]+\}", r"\.m-hint\{[^}]+\}", r"\.home-ia-ttl\{[^}]+\}", r"\.status\{[^}]+\}", r"\.search-box\{[^}]+\}"]:
    print("PAT", pat)
    for m in re.finditer(pat, t):
        print(" ", m.group(0)[:200])
