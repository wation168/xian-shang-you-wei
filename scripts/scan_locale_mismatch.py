# -*- coding: utf-8 -*-
"""
掃描腳本：找出全站工具頁裡「內容講的地區/幣別，跟頁面語言對不上」的錯誤。

背景：
  es/life-insurance-calc.html 被發現內文寫「在英國」「英鎊」「英國保險公司」，
  但頁面是西班牙文版、幣別符號用€——明顯是拿UK模板翻譯時，只換了語言，
  沒把「英國」相關的地區內容一併改掉。這支腳本用兩種方式，在全站範圍抓出
  同類型的錯誤，讓你知道總共有多少頁中獎，不用一頁一頁人工檢查。

兩種檢查方式：
  A) 【高可信度、低誤判】locale格式字串不符
     檢查 JS 裡 toLocaleString('xx-YY', ...) 這類數字格式化語法，
     xx-YY 的語言代碼如果跟頁面 <html lang="xx"> 宣告的語言對不上，
     幾乎可以肯定是複製別的語言頁面時忘記改，這是最可靠的訊號。

  B) 【中可信度，需人工複判】地區關鍵字誤植
     每個語言各自維護一份「不該出現在這個語言頁面的地區詞彙」清單
     （例如西班牙文頁面不該出現「Reino Unido」「libras esterlinas」），
     掃到就列出來，附上前後文，方便你快速判斷是不是真的錯了
     （少數情況下該地區詞彙可能是正常提及，例如頁面本來就在講某國稅制，
     這時候不算錯誤，需要你人工看一下前後文再判斷）。

用法：
  python scan_locale_mismatch.py
  （預設掃描 D:\\xian-shang-you-wei\\backend\\frontend\\tools\\ 底下所有 .html）

  python scan_locale_mismatch.py "D:\\xian-shang-you-wei\\backend\\frontend"
  （也可以指定掃描根目錄，會自動找裡面的 tools 資料夾）

輸出：
  終端機印出摘要 + 明細；同時在腳本所在目錄產出
  locale_mismatch_report.csv，方便用Excel篩選、排序、批次處理。

放在 D:\\xian-shang-you-wei\\scripts\\ 底下執行，不要放進 backend。
"""

import os
import re
import sys
import csv

# ── 語言資料夾對應設定 ─────────────────────────────────────
# key: 資料夾名稱（相對於 tools/），value: (預期的html lang值, 語言顯示名稱)
LANG_FOLDERS = {
    "":       ("zh-TW", "繁體中文（根目錄）"),
    "en":     ("en",    "英文"),
    "ja":     ("ja",    "日文"),
    "ko":     ("ko",    "韓文"),
    "de":     ("de",    "德文"),
    "fr":     ("fr",    "法文"),
    "es":     ("es",    "西班牙文"),
    "pt":     ("pt",    "葡萄牙文"),
    "id":     ("id",    "印尼文"),
    "zh-CN":  ("zh-CN", "簡體中文"),
}

# ── B) 各語言「不該出現的地區詞彙」清單 ─────────────────────
# 每個語言各自一份，格式：(關鍵字, 說明)
# 這份清單先覆蓋目前已知最常見的「UK模板外洩」型態，之後發現新案例可以再加。
SUSPICIOUS_KEYWORDS = {
    "es": [
        ("Reino Unido", "西班牙文頁面出現「英國」"),
        ("británic", "西班牙文頁面出現「英國的/英國人」"),
        ("libras esterlinas", "西班牙文頁面出現「英鎊」文字"),
        ("£", "西班牙文頁面出現英鎊符號"),
    ],
    "pt": [
        ("Reino Unido", "葡萄牙文頁面出現「英國」"),
        ("britânic", "葡萄牙文頁面出現「英國的/英國人」"),
        ("libras esterlinas", "葡萄牙文頁面出現「英鎊」文字"),
        ("£", "葡萄牙文頁面出現英鎊符號"),
    ],
    "de": [
        ("Vereinigten Königreich", "德文頁面出現「英國」"),
        ("Vereinigtes Königreich", "德文頁面出現「英國」"),
        ("britisch", "德文頁面出現「英國的」"),
        ("£", "德文頁面出現英鎊符號"),
    ],
    "fr": [
        ("Royaume-Uni", "法文頁面出現「英國」"),
        ("britannique", "法文頁面出現「英國的」"),
        ("£", "法文頁面出現英鎊符號"),
    ],
    "ja": [
        ("イギリス", "日文頁面出現「英國」（請人工確認是否為該頁本來就該講的內容）"),
        ("£", "日文頁面出現英鎊符號"),
    ],
    "ko": [
        ("영국", "韓文頁面出現「英國」（請人工確認是否為該頁本來就該講的內容）"),
        ("£", "韓文頁面出現英鎊符號"),
    ],
    "id": [
        ("Britania Raya", "印尼文頁面出現「英國」"),
        ("£", "印尼文頁面出現英鎊符號"),
        # "Inggris" 太常見（印尼文也用來指英格蘭/英國），故意不放進來避免大量誤判
    ],
    "zh-CN": [
        ("英国", "簡體中文頁面出現「英國」（請人工確認是否為該頁本來就該講的內容）"),
        ("£", "簡體中文頁面出現英鎊符號"),
    ],
    "": [  # 繁體中文（根目錄）
        ("英國", "繁體中文頁面出現「英國」（請人工確認是否為該頁本來就該講的內容）"),
        ("£", "繁體中文頁面出現英鎊符號"),
    ],
    "en": [
        # 2026/08/08修正（第十八輪任務6）：原本假設「英文版本身就是UK模板來源，不用檢查」
        # 是錯的——多數英文工具頁是給廣泛英語系/國際受眾看的通用頁，只有少數幾個
        # （例如 bonus-tax、oven-converter）才是刻意做成UK限定內容，其餘英文頁如果
        # 混到UK專屬詞彙/幣別，就是模板外洩的地區bug，比照其他語言的檢查方式補上清單。
        ("£", "英文頁面出現英鎊符號"),
        ("GBP", "英文頁面出現GBP幣別代碼"),
        ("VAT", "英文頁面出現VAT（英國/歐盟增值稅用語，美式英文一般用sales tax）"),
        ("National Insurance", "英文頁面出現「National Insurance」（英國國民保險，美式用語應為Social Security/payroll tax）"),
        ("postcode", "英文頁面出現「postcode」（英式用語，美式英文用zip code）"),
        ("Stamp Duty", "英文頁面出現「Stamp Duty」（英國房產稅用語）"),
        ("Council Tax", "英文頁面出現「Council Tax」（英國地方稅用語）"),
        ("NHS", "英文頁面出現「NHS」（英國國民保健署）"),
        ("colour", "英文頁面出現英式拼字「colour」"),
        ("favourite", "英文頁面出現英式拼字「favourite」"),
        ("organise", "英文頁面出現英式拼字「organise」"),
        ("centre", "英文頁面出現英式拼字「centre」"),
        ("litre", "英文頁面出現英式拼字「litre」"),
        ("kilometre", "英文頁面出現英式拼字「kilometre」"),
        ("programme", "英文頁面出現英式拼字「programme」"),
    ],
}

# 已知刻意做成「UK限定內容」的英文工具頁（slug，不含.html），
# 這些頁面命中上面的UK關鍵字是預期行為，不算bug，掃描時排除
# 2026/08/08更正：原本清單只打了2個，漏掉另外4個（記憶記錄共6個），
# 導致payroll-tax/stamp-duty/take-home-pay被誤判成A類真bug——
# 不是比對邏輯壞掉，是清單內容本身沒打全，這次補齊。
KNOWN_UK_ONLY_EN_TOOLS = {
    "bonus-tax", "oven-converter", "payroll-tax", "stamp-duty",
    "wire-gauge", "take-home-pay",
    # vat-calculator：人工核對43筆全部是「VAT vs sales tax」比較說明內容，
    # 無任何£/National Insurance等其他UK專屬用語混入，本質就是VAT主題工具
    "vat-calculator",
}


def find_tools_dir(root):
    """從指定路徑找 tools 資料夾，找不到就假設 root 本身就是 tools 資料夾"""
    candidate = os.path.join(root, "tools")
    if os.path.isdir(candidate):
        return candidate
    candidate2 = os.path.join(root, "backend", "frontend", "tools")
    if os.path.isdir(candidate2):
        return candidate2
    return root


def get_lang_folder_key(tools_dir, filepath):
    """從檔案路徑判斷屬於哪個語言資料夾"""
    rel = os.path.relpath(filepath, tools_dir)
    parts = rel.split(os.sep)
    if len(parts) >= 2 and parts[0] in LANG_FOLDERS:
        return parts[0]
    return ""  # 根目錄 = 繁中


def extract_html_lang(content):
    m = re.search(r'<html[^>]*\blang="([^"]+)"', content)
    return m.group(1) if m else None


def check_locale_string_mismatch(content, declared_lang):
    """檢查 toLocaleString('xx-YY', ...) 是否跟頁面宣告語言不符"""
    results = []
    for m in re.finditer(r"toLocaleString\('([a-zA-Z\-]+)'", content):
        used_locale = m.group(1)
        used_lang_prefix = used_locale.split("-")[0].lower()
        declared_prefix = (declared_lang or "").split("-")[0].lower()
        if declared_prefix and used_lang_prefix != declared_prefix:
            # zh-TW / zh-CN 都算 zh 開頭，特別處理避免誤判
            if declared_prefix == "zh" and used_lang_prefix == "zh":
                continue
            results.append(used_locale)
    return results


def check_suspicious_keywords(content, lang_key):
    keywords = SUSPICIOUS_KEYWORDS.get(lang_key, [])
    hits = []
    for kw, desc in keywords:
        for m in re.finditer(re.escape(kw), content):
            start = max(0, m.start() - 30)
            end = min(len(content), m.end() + 30)
            snippet = content[start:end].replace("\n", " ").replace("\r", " ")
            hits.append((kw, desc, snippet))
    return hits


# 英文關鍵字裡，強訊號(幣別/稅制專有名詞，幾乎不會是巧合)vs弱訊號(單純拼字習慣，
# 有些國際英文寫作也會用英式拼字，需要人工複判)
EN_STRONG_SIGNALS = {"£", "GBP", "VAT", "National Insurance", "postcode", "Stamp Duty", "Council Tax", "NHS"}


def classify_en_hit(kw, file_slug):
    if file_slug in KNOWN_UK_ONLY_EN_TOOLS:
        return "B-UK限定工具例外清單內"
    if kw in EN_STRONG_SIGNALS:
        return "A-真bug需修"
    return "C-拼字習慣待評估"


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else r"D:\xian-shang-you-wei\backend\frontend"
    only_lang = sys.argv[2] if len(sys.argv) > 2 else None  # 例如傳 "en" 只掃英文
    tools_dir = find_tools_dir(root)

    if not os.path.isdir(tools_dir):
        print(f"找不到 tools 資料夾：{tools_dir}")
        print("請確認路徑，或用參數指定：python scan_locale_mismatch.py <根目錄路徑>")
        return

    if only_lang is not None:
        print(f"掃描目錄：{tools_dir}（只掃 {only_lang} 語言資料夾）\n")
    else:
        print(f"掃描目錄：{tools_dir}\n")

    all_rows = []
    files_scanned = 0
    files_with_issues = 0

    for dirpath, _, filenames in os.walk(tools_dir):
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            filepath = os.path.join(dirpath, fn)
            lang_key = get_lang_folder_key(tools_dir, filepath)
            if only_lang is not None and lang_key != only_lang:
                continue
            files_scanned += 1
            expected_lang, lang_name = LANG_FOLDERS.get(lang_key, (lang_key, lang_key))

            try:
                with open(filepath, encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception as e:
                print(f"  讀取失敗 {filepath}: {e}")
                continue

            declared_lang = extract_html_lang(content)
            rel_path = os.path.relpath(filepath, tools_dir)

            has_issue = False

            # A) locale字串不符
            mismatches = check_locale_string_mismatch(content, expected_lang)
            for mm in mismatches:
                has_issue = True
                all_rows.append({
                    "檔案": rel_path,
                    "語言資料夾": lang_name,
                    "html宣告lang": declared_lang or "(無)",
                    "檢查類型": "A-locale字串不符",
                    "分類": "A-真bug需修",
                    "問題內容": f"toLocaleString('{mm}') 跟頁面語言不符",
                    "上下文": "",
                })

            # B) 關鍵字誤植
            file_slug = os.path.splitext(fn)[0]
            kw_hits = check_suspicious_keywords(content, lang_key)
            for kw, desc, snippet in kw_hits:
                has_issue = True
                classification = classify_en_hit(kw, file_slug) if lang_key == "en" else ""
                all_rows.append({
                    "檔案": rel_path,
                    "語言資料夾": lang_name,
                    "html宣告lang": declared_lang or "(無)",
                    "檢查類型": "B-關鍵字疑似誤植",
                    "分類": classification,
                    "問題內容": desc,
                    "上下文": f"...{snippet}...",
                })

            if has_issue:
                files_with_issues += 1

    # ── 輸出摘要 ─────────────────────────────────────
    print(f"共掃描 {files_scanned} 個html檔案")
    print(f"發現疑似問題的檔案數：{files_with_issues}")
    print(f"問題總筆數：{len(all_rows)}\n")

    if all_rows:
        # 按語言分類統計
        by_lang = {}
        for row in all_rows:
            by_lang.setdefault(row["語言資料夾"], set()).add(row["檔案"])
        print("各語言中獎頁數：")
        for lang_name, files in sorted(by_lang.items(), key=lambda x: -len(x[1])):
            print(f"  {lang_name}: {len(files)} 頁")

        print("\n明細（最多列30筆，完整內容請看CSV）：")
        for row in all_rows[:30]:
            print(f"  [{row['檢查類型']}] {row['檔案']} — {row['問題內容']}")
            if row["上下文"]:
                print(f"      {row['上下文']}")
        if len(all_rows) > 30:
            print(f"  ...還有 {len(all_rows) - 30} 筆，完整內容看CSV")

        # ── 輸出CSV ─────────────────────────────────────
        out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "locale_mismatch_report.csv")
        with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["檔案", "語言資料夾", "html宣告lang", "檢查類型", "分類", "問題內容", "上下文"])
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"\n完整報告已輸出：{out_path}")
        print("可以用Excel打開，篩選『檢查類型』欄位：")
        print("  A類（locale字串不符）幾乎都是真的錯誤，可以直接排修復優先序")
        print("  B類（關鍵字疑似誤植）需要人工看『上下文』欄位判斷是否真的講錯地區，")
        print("      不是每一筆都算錯——例如頁面本來就在講某國稅制，提到該國是正常的")
    else:
        print("沒有掃到任何疑似問題，太好了。")


if __name__ == "__main__":
    main()
