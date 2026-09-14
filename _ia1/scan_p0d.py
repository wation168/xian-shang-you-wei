# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding="utf-8")
t = open(r"D:/xian-shang-you-wei/backend/frontend/index.html", encoding="utf-8").read()
p = t.find("edf6ff")
while p >= 0:
    print("at", p, repr(t[max(0,p-40):p+40]))
    p = t.find("edf6ff", p+1)
print("--- search-box input all ---")
for m in re.finditer(r".{0,20}search-box input.{0,80}", t):
    print(repr(m.group(0)))
print("--- m-hint ---")
p = t.find(".m-hint")
print(repr(t[p:p+160]))
