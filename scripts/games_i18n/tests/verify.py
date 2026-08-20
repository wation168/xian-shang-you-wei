# -*- coding: utf-8 -*-
"""
產出檔案的結構驗證（每產一批就跑一次）

檢查項目（沿用歷次踩過的坑整理而成）：
  A JSON-LD 一律用 json.loads 實際解析，不是肉眼看
  B 頁內每一段 inline <script> 都丟 node --check 驗語法
  C getElementById(...) 用到的 id 必須真的存在於 HTML 的 id= 屬性
  D <div> 開合標籤配對
  E 樣板佔位符 {{ui.x}} / {{chrome.x}} 不能漏換
  F 靜態HTML裡不能殘留 {s}/{v} 這種變數佔位（只有 GAME_I18N 字典裡才該有）
  G 共用JS用到的每一個 i18n key，每個語言的字典都必須有（缺一個就失敗）
  H 拉丁語系頁面不得出現任何中日韓文字；ja/ko/zh-CN 不得殘留繁中專用字串
  I hreflang 10語言 + x-default 齊全，canonical 指向自己
  J html lang 屬性正確、共用JS與games-auth.js都有引用
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

OUT = os.path.join(BASE, "out", "games")
SITE = "https://softglow-ai.com"

CJK = re.compile(r"[一-鿿぀-ヿ가-힯]")
LATIN_LOCALES = ["en", "de", "es", "fr", "id", "pt"]
# 繁中專用字串：出現在 ja/ko/zh-CN 頁面就代表有漏翻
TRAD_ONLY = ["常見問題", "遊戲結束", "重新開始", "分享成績", "瀏覽全部遊戲",
             "登入才能把成績", "數字方塊遊戲", "電腦用方向鍵"]

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


def _count_config_array_entries(src, field_name):
    # 針對「陣列名稱跟CONFIG欄位同名」的情況（例如數獨的
    # difficulties: [ {key:'easy',clues:38}, ... ]，或鋼琴塊的
    # songKeys: ['twinkle','mary',...]），用深度掃描數出最外層陣列裡有幾個
    # 頂層元素（不管是物件還是純字串/數字），藉此推出這個陣列「應該」有幾個語言字串。
    # 純數字門檻陣列（xxxThresholds）不會走這條路，那個是掃描 [\d, Infinity] 的簡單regex。
    m = re.search(r"\b" + re.escape(field_name) + r"\s*:\s*\[", src)
    if not m:
        return None
    i, n = m.end(), len(src)
    depth = 1  # 已經吃掉最外層的 [
    commas_at_top = 0
    seen_content = False
    in_str = None  # None 或 目前字串的引號字元，字串內部的逗號/括號不能算數
    while i < n and depth > 0:
        c = src[i]
        if in_str:
            if c == "\\":
                i += 2
                continue
            if c == in_str:
                in_str = None
            i += 1
            continue
        if c in ("'", '"', "`"):
            in_str = c
            seen_content = True
        elif c in "[{(":
            depth += 1
            seen_content = True
        elif c in "]})":
            depth -= 1
        elif c == "," and depth == 1:
            commas_at_top += 1
        elif not c.isspace():
            seen_content = True
        i += 1
    if not seen_content:
        return None
    # 陣列結尾常見拖尾逗號（trailing comma），不能多算一個空元素——
    # 用「有沒有在最後一個逗號之後、']'之前還出現過非空白字元」來判斷。
    tail = src[m.end():i]
    last_comma = tail.rfind(",")
    has_trailing_comma = last_comma != -1 and not tail[last_comma + 1:-1].strip()
    count = commas_at_top if has_trailing_comma else commas_at_top + 1
    return count or None


def i18n_keys_used(slug):
    src = open(os.path.join(OUT, "shared", "%s.js" % slug), encoding="utf-8").read()
    # 註解裡常會出現「透過 gXxxT('key') 讀取」這類說明文字，先剝掉註解再抽，
    # 否則會把說明用的假key當成真的要求，導致每個語言都被誤判成缺key
    src = re.sub(r"/\*[\s\S]*?\*/", "", src)
    src = re.sub(r"//[^\n]*", "", src)
    fn = "g" + slug.replace("-", "") + "T"  # g2048T
    keys = set(re.findall(re.escape(fn) + r"\('([A-Za-z0-9_]+)'", src))
    # 陣列型文字（評語分級、難度名稱等）不是透過 gXxxT() 取的，而是直接讀 GAME_I18N.<名稱>，
    # 這裡把用到的陣列名稱抓出來，並從 CONFIG 的 xxxThresholds 推出應有的長度，
    # 之後逐語言比對「陣列存在、長度正確、每一項都有內容」——
    # 不寫死5級，因為各遊戲分級數不同（例如反應力測試是6級）
    arrays = set(re.findall(r"window\.GAME_I18N\.([A-Za-z0-9_]+)", src))
    thresholds = {}
    for m in re.finditer(r"(\w*[Tt]hresholds)\s*:\s*\[([^\]]*)\]", src):
        thresholds[m.group(1)] = len([x for x in m.group(2).split(",") if x.strip()])
    fallback_len = max(thresholds.values()) if thresholds else None
    # 一款遊戲可能同時有好幾個陣列型文字、彼此長度天生不同（例如數獨同時有4級難度
    # 名稱和5級評語文字）。先試著找「跟陣列同名的CONFIG物件陣列」取得專屬長度，
    # 找不到才退回舊邏輯（用單一 xxxThresholds 長度套用在所有陣列上）。
    array_lens = {}
    for arr in arrays:
        # 陣列名稱不一定跟CONFIG欄位同名（例如踩地雷的 GAME_I18N.difficulties
        # 對應的CONFIG欄位其實叫 difficultyTable），這裡多試幾種常見命名變化。
        candidates = [arr]
        if arr.endswith("ies"):
            singular = arr[:-3] + "y"
            candidates += [singular + "Table", singular + "List", singular]
        elif arr.endswith("s"):
            singular = arr[:-1]
            candidates += [singular + "Table", singular + "List", singular]
        candidates += [arr + "Table", arr + "List"]
        own_len = None
        for cand in candidates:
            own_len = _count_config_array_entries(src, cand)
            if own_len:
                break
        array_lens[arr] = own_len or fallback_len
    return keys, arrays, array_lens


def verify_game(slug):
    print("── 驗證 %s ──" % slug)
    keys_used, arrays_used, array_lens = i18n_keys_used(slug)
    ok("共用JS至少用到一個i18n key（確認文字真的走字典）", len(keys_used) > 0)

    shared = open(os.path.join(OUT, "shared", "%s.js" % slug), encoding="utf-8").read()
    node_check(shared, "shared/%s.js" % slug)

    for loc in LOC.LOCALES:
        rel = "%s.html" % slug if loc == "zh-TW" else "%s/%s.html" % (loc, slug)
        path = os.path.join(OUT, rel)
        ok("[%s] 檔案存在" % loc, os.path.isfile(path), path)
        if not os.path.isfile(path):
            continue
        html = open(path, encoding="utf-8").read()
        tag = "[%s/%s]" % (loc, slug)

        # A JSON-LD
        lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        ok("%s JSON-LD 有2段" % tag, len(lds) == 2, "found=%d" % len(lds))
        for i, ld in enumerate(lds):
            try:
                obj = json.loads(ld)
                ok("%s JSON-LD#%d 解析成功" % (tag, i), True)
                if obj.get("@type") == "FAQPage":
                    ok("%s FAQPage 有5題" % tag, len(obj["mainEntity"]) == 5,
                       str(len(obj.get("mainEntity", []))))
            except Exception as e:
                ok("%s JSON-LD#%d 解析成功" % (tag, i), False, str(e)[:200])

        # B inline script 語法
        # 排除 src= 外連與 ld+json（JSON-LD 由上面的 json.loads 專門驗，不該丟給 node --check）
        inline = re.findall(r"<script(?![^>]*\bsrc=)(?![^>]*ld\+json)[^>]*>(.*?)</script>", html, re.S)
        inline = [s for s in inline if s.strip()]
        for i, s in enumerate(inline):
            node_check(s, "%s inline#%d" % (tag, i))

        # C getElementById 一致性
        ids_declared = set(re.findall(r'\bid="([^"]+)"', html))
        ids_used = set(re.findall(r"getElementById\('([^']+)'\)", html))
        ids_used |= set(re.findall(r'getElementById\("([^"]+)"\)', html))
        # 共用JS裡的 getElementById 也要一起比對（那才是真正操作這一頁的程式碼）
        ids_used |= set(re.findall(r"getElementById\('([^']+)'\)", shared))
        # gaWidget/gaLeaderboard 由 games-auth.js 掛載，以字串參數傳入，額外納入
        ids_used |= set(re.findall(r"gaMount\w+\('([^']+)'", html))
        missing = sorted(i for i in ids_used if i not in ids_declared
                         and not i.endswith("Name") and not i.endswith("Google"))
        ok("%s getElementById 的id都存在" % tag, not missing, str(missing))

        # D div 配對
        opens = len(re.findall(r"<div\b", html))
        closes = len(re.findall(r"</div>", html))
        ok("%s <div>開合配對" % tag, opens == closes, "open=%d close=%d" % (opens, closes))

        # E 佔位符沒漏換
        ok("%s 無殘留樣板佔位符" % tag, "{{" not in html)

        # F 靜態HTML不得殘留變數佔位（先把 GAME_I18N/GA_LANG_PACK 字典區塊挖掉再檢查）
        stripped = re.sub(r"window\.GAME_I18N = .*?;\nwindow\.GA_LANG_PACK = .*?;", "", html, flags=re.S)
        leftover = re.findall(r"\{[svr]\}|\{game\}", stripped)
        ok("%s 靜態內容無未代入的變數佔位" % tag, not leftover, str(leftover))

        # G i18n key 完整性
        m = re.search(r"window\.GAME_I18N = (\{.*?\});", html, re.S)
        ok("%s 有 GAME_I18N 字典" % tag, bool(m))
        if m:
            try:
                d = json.loads(m.group(1))
                miss = sorted(k for k in keys_used if k not in d)
                ok("%s 字典涵蓋共用JS所有key" % tag, not miss, "缺:" + str(miss))
                for arr in sorted(arrays_used):
                    v = d.get(arr)
                    ok("%s %s 是陣列" % (tag, arr), isinstance(v, list), str(v)[:60])
                    if isinstance(v, list):
                        expected_len = array_lens.get(arr)
                        if expected_len:
                            ok("%s %s 長度與CONFIG門檻數一致(%d)" % (tag, arr, expected_len),
                               len(v) == expected_len, "實際%d" % len(v))
                        ok("%s %s 每項都有內容" % (tag, arr),
                           all(isinstance(x, str) and x.strip() for x in v))
            except Exception as e:
                ok("%s GAME_I18N 解析成功" % tag, False, str(e)[:200])

        m2 = re.search(r"window\.GA_LANG_PACK = (\{.*?\});", html, re.S)
        ok("%s 有 GA_LANG_PACK 字典" % tag, bool(m2))
        if m2:
            try:
                p = json.loads(m2.group(1))
                need = ["loginToRank", "emptyBoard", "loadingBoard", "logoutBtn",
                        "loginTip", "lineBtn", "fsEnter", "fsExit", "badge",
                        "reminderTitle", "reminderSub", "reminderSkip"]
                miss = [k for k in need if k not in p]
                ok("%s GA_LANG_PACK 必要key齊全" % tag, not miss, "缺:" + str(miss))
            except Exception as e:
                ok("%s GA_LANG_PACK 解析成功" % tag, False, str(e)[:200])

        # H 語言純度
        # 語言切換下拉的選項標籤（日本語/한국어/简中/繁中）本來就該保留各語言原生寫法，
        # HTML註解也不是給使用者看的內容，兩者先剝掉再檢查，避免誤判
        pure = re.sub(r"<!--.*?-->", "", html, flags=re.S)
        pure = re.sub(r'<select class="lang-select".*?</select>', "", pure, flags=re.S)
        if loc in LATIN_LOCALES:
            found = CJK.findall(pure)
            ok("%s 無中日韓文字殘留" % tag, not found, "".join(sorted(set(found)))[:60])
        if loc in ("ja", "ko", "zh-CN"):
            bad = [s for s in TRAD_ONLY if s in pure]
            ok("%s 無繁中專用字串殘留" % tag, not bad, str(bad))

        # I hreflang / canonical
        hl = re.findall(r'hreflang="([^"]+)"', html)
        ok("%s hreflang 齊全（10語言+x-default）" % tag,
           sorted(hl) == sorted(LOC.LOCALES + ["x-default"]), str(sorted(hl)))
        can = re.search(r'<link rel="canonical" href="([^"]+)">', html)
        ok("%s canonical 指向自己" % tag,
           bool(can) and can.group(1) == SITE + LOC.game_url(loc, slug),
           can.group(1) if can else "無")

        # J lang 屬性與引用
        lang = re.search(r'<html lang="([^"]+)">', html)
        ok("%s html lang 正確" % tag,
           bool(lang) and lang.group(1) == LOC.CHROME[loc]["htmlLang"],
           lang.group(1) if lang else "無")
        ok("%s 有引用共用邏輯JS" % tag, '/games/shared/%s.js' % slug in html)
        ok("%s 有引用games-auth.js" % tag, '/games/games-auth.js' in html)
        ok("%s 導覽/麵包屑指向本語言遊戲區" % tag, 'href="/games%s/"' % LOC.url_prefix(loc) in html)


if __name__ == "__main__":
    slugs = sys.argv[1:] or ["2048"]
    for s in slugs:
        verify_game(s)
    print("\n結構驗證：%d 通過, %d 失敗" % (results["pass"], results["fail"]))
    sys.exit(1 if results["fail"] else 0)
