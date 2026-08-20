# -*- coding: utf-8 -*-
"""
遊戲區索引頁 /games/{loc}/index.html 的結構驗證，跟 tests/verify.py 同一套精神，
針對索引頁的特性做調整（沒有 shared/{slug}.js、沒有i18n字典、是13款遊戲的卡片牆）：

  A JSON-LD 用 json.loads 實際解析
  B 頁內 inline <script> 丟 node --check 驗語法
  C GAMES 陣列有13款、且13款都真的有對應的 {slug}.html 檔案存在（各語言版本都要有）
  D getElementById 用到的 id 必須存在
  E <div> 開合配對
  F 拉丁語系頁面不得出現中日韓文字；ja/ko/zh-CN 不得殘留繁中專用字串
  G hreflang 10語言+x-default 齊全、canonical 指向自己
  H html lang 屬性正確
  I 語言切換下拉的10個選項都指向存在的索引頁檔案
"""
import json
import os
import re
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
import locales as LOC
from build_index import GAMES_ORDER

OUT = os.path.join(BASE, "out", "games")
SITE = "https://softglow-ai.com"

CJK = re.compile(r"[一-鿿぀-ヿ가-힯]")
LATIN_LOCALES = ["en", "de", "es", "fr", "id", "pt"]
TRAD_ONLY = ["常見問題", "遊戲結束", "重新開始", "分享成績", "瀏覽全部遊戲",
             "登入才能把成績", "數字方塊遊戲", "電腦用方向鍵", "免費線上小遊戲",
             "相關工具", "瀏覽全部工具"]

results = {"pass": 0, "fail": 0}
def ok(name, cond, detail=""):
    if cond:
        results["pass"] += 1
    else:
        results["fail"] += 1
        print("  ✗ %s %s" % (name, detail))


def node_check(js, label):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
        p = f.name
    try:
        r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
        ok("node --check %s" % label, r.returncode == 0, r.stderr.strip()[:300])
    finally:
        os.unlink(p)


def verify_index():
    print("── 驗證 games索引頁 ──")
    expected_slugs = set(s for s, _ in GAMES_ORDER)
    ok("GAMES_ORDER 剛好13款", len(GAMES_ORDER) == 13, str(len(GAMES_ORDER)))

    for loc in LOC.LOCALES:
        rel = "index.html" if loc == "zh-TW" else "%s/index.html" % loc
        path = os.path.join(OUT, rel)
        tag = "[%s/index]" % loc
        ok("%s 檔案存在" % tag, os.path.isfile(path), path)
        if not os.path.isfile(path):
            continue
        html = open(path, encoding="utf-8").read()

        # A JSON-LD
        lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        ok("%s JSON-LD 有1段" % tag, len(lds) == 1, "found=%d" % len(lds))
        for i, ld in enumerate(lds):
            try:
                json.loads(ld)
                ok("%s JSON-LD#%d 解析成功" % (tag, i), True)
            except Exception as e:
                ok("%s JSON-LD#%d 解析成功" % (tag, i), False, str(e)[:200])

        # B inline script 語法
        inline = re.findall(r"<script(?![^>]*\bsrc=)(?![^>]*ld\+json)[^>]*>(.*?)</script>", html, re.S)
        inline = [s for s in inline if s.strip()]
        for i, s in enumerate(inline):
            node_check(s, "%s inline#%d" % (tag, i))

        # C GAMES 陣列完整性：13款都在、且每款對應的語言版檔案真的存在
        m = re.search(r"const GAMES = (\[.*?\]);", html, re.S)
        ok("%s 找得到GAMES陣列" % tag, m is not None)
        if m:
            games = json.loads(m.group(1))
            got_slugs = set(g["slug"] for g in games)
            ok("%s GAMES陣列有13款且slug跟GAMES_ORDER一致" % tag, got_slugs == expected_slugs,
               str(expected_slugs - got_slugs) + " / extra=" + str(got_slugs - expected_slugs))
            for g in games:
                game_path = os.path.join(OUT, g["slug"] + ".html") if loc == "zh-TW" else \
                            os.path.join(OUT, loc, g["slug"] + ".html")
                ok("%s %s 對應的遊戲頁存在" % (tag, g["slug"]), os.path.isfile(game_path), game_path)
                ok("%s %s name/desc/emoji都非空字串" % (tag, g["slug"]),
                   bool(g.get("name")) and bool(g.get("desc")) and bool(g.get("emoji")))

        # D getElementById 一致性
        ids_declared = set(re.findall(r'\bid="([^"]+)"', html))
        ids_used = set(re.findall(r"getElementById\('([^']+)'\)", html))
        missing = sorted(i for i in ids_used if i not in ids_declared)
        ok("%s getElementById 的id都存在" % tag, not missing, str(missing))

        # E div 配對
        opens = len(re.findall(r"<div\b", html))
        closes = len(re.findall(r"</div>", html))
        ok("%s <div>開合配對" % tag, opens == closes, "open=%d close=%d" % (opens, closes))

        # F 語言純度（跟 tests/verify.py 一樣，先把語言切換下拉的原生文字選項挖掉再檢查，
        # 那些是「繁中/日本語/한국어/简中」這種刻意用原生文字顯示的語言名稱，不是漏翻）
        pure = re.sub(r'<select class="lang-select".*?</select>', "", html, flags=re.S)
        if loc in LATIN_LOCALES:
            cjk = CJK.findall(pure)
            ok("%s 拉丁語系不含中日韓文字" % tag, not cjk, "".join(sorted(set(cjk)))[:40])
        if loc in ("ja", "ko", "zh-CN"):
            leaked = [w for w in TRAD_ONLY if w in pure]
            ok("%s 不含繁中專用字串殘留" % tag, not leaked, str(leaked))

        # G hreflang + canonical
        hrefs = re.findall(r'hreflang="([^"]+)" href="([^"]+)"', html)
        got_locs = set(h[0] for h in hrefs) - {"x-default"}
        ok("%s hreflang涵蓋10語言" % tag, got_locs == set(LOC.LOCALES), str(set(LOC.LOCALES) - got_locs))
        ok("%s 有x-default" % tag, "x-default" in set(h[0] for h in hrefs))
        canon = re.search(r'<link rel="canonical" href="([^"]+)">', html)
        expect_url = SITE + LOC.index_url(loc)
        ok("%s canonical指向自己" % tag, canon and canon.group(1) == expect_url,
           str(canon.group(1) if canon else None) + " expect " + expect_url)

        # H html lang
        htmllang = re.search(r'<html lang="([^"]+)">', html)
        ok("%s html lang正確" % tag, htmllang and htmllang.group(1) == loc,
           str(htmllang.group(1) if htmllang else None))

        # I 語言切換下拉的每個選項都指向存在的索引頁
        opts = re.findall(r'<option value="([^"]+)"', html)
        ok("%s 語言切換有10個選項" % tag, len(opts) == 10, str(len(opts)))
        for o in opts:
            rel_path = o.lstrip("/") + "index.html" if o.endswith("/") else o.lstrip("/")
            opt_path = os.path.join(BASE, "out", rel_path)
            ok("%s 切換選項 %s 對應檔案存在" % (tag, o), os.path.isfile(opt_path), opt_path)

    print("\n索引頁結構驗證：%d 通過, %d 失敗" % (results["pass"], results["fail"]))
    return results["fail"] == 0


if __name__ == "__main__":
    ok_ = verify_index()
    sys.exit(0 if ok_ else 1)
