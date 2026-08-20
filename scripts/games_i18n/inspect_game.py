# -*- coding: utf-8 -*-
"""一次把「做一款遊戲多語言化」需要的全部資訊倒出來，減少來回查檔。
用法：python3 inspect_game.py {slug}"""
import re, sys, os

slug = sys.argv[1]
SRC = "/mnt/user-data/uploads/games/%s.html" % slug
h = open(SRC, encoding="utf-8").read()

def g(p, d="(無)"):
    m = re.search(p, h, re.S)
    return m.group(1) if m else d

print("=" * 70)
print("TITLE:", g(r"<title>(.*?)</title>"))
print("DESC :", g(r'name="description" content="(.*?)"'))
print("H1   :", g(r"<h1>(.*?)</h1>"))
print("SUB  :", g(r'class="game-subtitle">(.*?)</p>'))
ld = re.search(r'"@type": "WebApplication", "name": "(.*?)".*?"description": "(.*?)"', h, re.S)
if ld:
    print("LDNAME:", ld.group(1))
    print("LDDESC:", ld.group(2))

print("\n" + "=" * 70 + "\n遊戲卡片內部版面（h1/subtitle/ga-widget 之間，這段要做成 body.html）:")
m = re.search(r'<p class="game-subtitle">.*?</p>(.*?)(<div class="ga-widget"|</div>\s*\n\s*<div class="ad-container)', h, re.S)
print(m.group(1).strip() if m else "(抓不到，請手動看)")

print("\n" + "=" * 70 + "\n文章:")
for i, a in enumerate(re.findall(r'<article class="article">(.*?)</article>', h, re.S)):
    print(f"--- ART{i} ---")
    for mm in re.finditer(r"<h2>(.*?)</h2>", a):
        print("H2:", mm.group(1).strip())
    for mm in re.finditer(r"<p>(.*?)</p>", a, re.S):
        print("P :", mm.group(1).strip())

print("\n" + "=" * 70 + "\nFAQ:")
for mm in re.finditer(r'faq-q">(.*?)</div>\s*<div class="faq-a">(.*?)</div>', h, re.S):
    print("Q:", mm.group(1).strip())
    print("A:", mm.group(2).strip(), "\n")

sh = "shared/%s.js" % slug
if os.path.isfile(sh):
    src = open(sh, encoding="utf-8").read()
    src_nc = re.sub(r"/\*[\s\S]*?\*/", "", src)
    src_nc = re.sub(r"//[^\n]*", "", src_nc)
    fn = "g" + slug.replace("-", "") + "T"
    keys = sorted(set(re.findall(re.escape(fn) + r"\('([A-Za-z0-9_]+)'", src_nc)))
    print("=" * 70)
    print("共用JS已存在（agent草稿）。取字函式:", fn)
    print("需要的 i18n keys:", keys)
    print("有用到 ratings 陣列:", ".ratings" in src_nc)
    cfg = re.search(r"const [A-Z_]+_CONFIG = \{(.*?)\n\};", src_nc, re.S)
    if cfg:
        print("CONFIG:", cfg.group(1).strip()[:600])
    print("純函式:", re.findall(r"^function (\w+)", src_nc, re.M))
else:
    print("=" * 70)
    print("尚無 shared/%s.js —— 需要自己從原始檔的 <script> 抽出來" % slug)
    ss = re.findall(r"<script>(.*?)</script>", h, re.S)
    print("原始檔 inline script 段數:", len(ss), "各段長度:", [len(x) for x in ss])
