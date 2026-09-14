# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding="utf-8")
t = open(r"D:/xian-shang-you-wei/backend/frontend/index.html", encoding="utf-8").read()
print("len", len(t))
for pat in [
    r"\.search-box input\{[^}]+\}",
    r"\.search-box input::placeholder\{[^}]+\}",
    r"\.m-hint\{[^}]+\}",
    r"\.home-ia-ttl\{[^}]+\}",
    r"\.status\{[^}]+\}",
]:
    print("PAT", pat)
    for m in re.finditer(pat, t):
        print(" ", m.group(0))
print("edf6ff leftover search/ttl", ".search-box input{color:#edf6ff}" in t, ".home-ia-ttl{font-size:16px;color:#edf6ff}" in t)
print("m-hint 9", ".m-hint{font-size:9px" in t)
print("status 11 text3", ".status{font-size:11px;color:var(--text3)" in t)
print("status 13 text2", ".status{font-size:13px;color:var(--text2)" in t)
