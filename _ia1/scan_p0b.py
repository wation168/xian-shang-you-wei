# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8")
t = open(r"D:/xian-shang-you-wei/backend/frontend/index.html", encoding="utf-8").read()
# dump surrounding CSS blocks
for label, p in [
    ("search override", t.find(".search-box input{color:#edf6ff}")),
    ("placeholder", t.find("placeholder")),
    ("stockInput css", t.find("#stockInput")),
    ("search-wrap", t.find(".search-wrap input")),
    ("status css", t.find(".status{font-size:11px")),
    ("home-ia-ttl override", t.find(".home-ia-ttl{font-size:16px;color:#edf6ff}")),
    ("m-hint", t.find(".m-hint{")),
]:
    print("====", label, p, "====")
    print(t[max(0,p-400):p+350])
    print()
