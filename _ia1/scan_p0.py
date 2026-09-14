# -*- coding: utf-8 -*-
t = open(r"D:/xian-shang-you-wei/backend/frontend/index.html", encoding="utf-8").read()
needles = [
    "search-box input",
    ".m-hint",
    "home-ia-ttl",
    "edf6ff",
    "statusBar",
    "#statusBar",
    ".status",
]
for n in needles:
    i = 0
    c = 0
    while True:
        p = t.find(n, i)
        if p < 0:
            break
        c += 1
        if c <= 8:
            print("====", n, p, "====")
            print(t[max(0,p-80):p+220])
            print()
        i = p + len(n)
    print("COUNT", n, c)
