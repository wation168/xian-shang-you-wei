# -*- coding: utf-8 -*-
"""
路由匹配順序驗證（不import main.py——它不是可import的模組）

做法：從改好的 main.py 裡「按出現順序」抓出所有 /games 相關的 @app.get 路徑，
用同樣的順序在一個乾淨的 FastAPI app 上註冊 stub handler，再用 TestClient 實際發請求，
確認每個網址被導到「預期的那一條路由」。

這一步要驗的核心風險是：新加的 /games/shared/{filename}.js 會不會被既有的
/games/{filename}.js 搶先吃掉，以及 /games/{locale} 會不會誤吃 /games/games.css。
FastAPI 是按註冊順序比對的，光看程式碼很容易想錯，所以實際跑一次最保險。
"""
import re
import sys
import os

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.testclient import TestClient

MAIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py")
src = open(MAIN, encoding="utf-8").read()

# 依原始碼順序抓出所有 /games 開頭的 GET 路由，以及它下面接的函式名稱
pat = re.compile(r'@app\.get\("(/games[^"]*)"[^)]*\)|async def (\w+)\(')
routes = []          # [(path, funcname)]
pending = []
for m in pat.finditer(src):
    if m.group(1):
        pending.append(m.group(1))
    elif pending:
        for p in pending:
            routes.append((p, m.group(2)))
        pending = []

print("從 main.py 抓到 %d 條 /games 路由（依註冊順序）：" % len(routes))
for p, f in routes:
    print("   %-42s → %s" % (p, f))

app = FastAPI()
for p, f in routes:
    def make(fn=f):
        # 兩個參數都給預設值：路徑裡有的會被當path param綁定，沒有的變成可選query param，
        # 這樣同一個stub簽章就能套用到所有路由（用 **kwargs 會被FastAPI判成缺參數而回422）
        async def h(filename: str = "", locale: str = ""):
            return PlainTextResponse(fn)
        return h
    app.get(p)(make())

client = TestClient(app)

# 這些檔案在磁碟上是否存在不影響路由匹配，stub 只回傳「命中哪條路由的函式名」
CASES = [
    # 網址,                              預期命中的 handler
    ("/games/games.css",                 "serve_games_css"),
    ("/games/games-auth.js",             "serve_games_js"),
    ("/games/shared/2048.js",            "serve_games_shared_js"),
    ("/games/shared/minesweeper.js",     "serve_games_shared_js"),
    ("/games/2048.html",                 "serve_games_html"),
    ("/games/index.html",                "serve_games_html"),
    ("/games/",                          "serve_games_index"),
    ("/games",                           "serve_games_index"),
    ("/games/en/2048.html",              "serve_games_locale_html"),
    ("/games/ja/minesweeper.html",       "serve_games_locale_html"),
    ("/games/zh-CN/chess.html",          "serve_games_locale_html"),
    ("/games/en/",                       "serve_games_locale_index"),
    ("/games/en",                        "serve_games_locale_index"),
    ("/games/pt",                        "serve_games_locale_index"),
]

passed = failed = 0
print("\n路由匹配結果：")
for url, expect in CASES:
    r = client.get(url)
    got = r.text if r.status_code == 200 else "HTTP%d" % r.status_code
    if got == expect:
        passed += 1
    else:
        failed += 1
        print("  ✗ %-34s 預期 %s，實際 %s" % (url, expect, got))

# 額外：語言白名單必須完全等於網站既有的9語言（不能多也不能少）
m = re.search(r'_GAMES_LOCALES = \(([^)]*)\)', src)
locs = sorted(re.findall(r'"([^"]+)"', m.group(1))) if m else []
expect_locs = sorted(["en", "ja", "ko", "es", "pt", "id", "de", "fr", "zh-CN"])
if locs == expect_locs:
    passed += 1
else:
    failed += 1
    print("  ✗ _GAMES_LOCALES 內容不符：%s" % locs)

# 額外：sitemap 必須排除 shared 資料夾（那底下只有共用JS，不是可索引頁面）
if 'if os.path.isdir(_lang_path) and _lang_dir not in (".", "..", "shared")' in src:
    passed += 1
else:
    failed += 1
    print("  ✗ sitemap 沒有排除 shared 資料夾")

print("\n路由驗證：%d 通過, %d 失敗" % (passed, failed))
sys.exit(1 if failed else 0)
