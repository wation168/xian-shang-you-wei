# -*- coding: utf-8 -*-
"""
全站過期內容掃描（第十八輪任務5重寫版）。

背景：
  原本的CTR/過期內容掃描腳本在本機、git歷史裡都找不到（推測是先前session做完
  沒有落地存檔）。本次依任務描述的需求重新寫一支：
    1. 不只抓「有年份字樣」的內容，也抓「去年/今年/最新/目前」這類相對時間詞
       （這類詞語意上一定會隨時間過期，比死板的年份字樣更容易漏抓真正的過期內容）
    2. 10語言都要有完整關鍵字清單，不能像原本的腳本一樣英文清單是空的
    3. 全站掃（tools/ + blog/，這是內容型頁面最容易放「時效性文字」的地方）

用法：
  python scan_outdated_content.py
  （預設掃描 D:\\xian-shang-you-wei\\backend\\frontend\\ 底下的 tools/ 和 blog/）

輸出：
  終端機印摘要；scripts/outdated_content_report.csv 完整明細（含前後文，方便人工複判）

注意：
  這支腳本只找「疑似過期」的訊號，不代表抓到的一定是錯的（例如「since 2015」是正常
  的歷史沿革敘述，不是過期內容），需要人工看「上下文」欄位判斷。
  只回報，不會自動修改任何內容。放在 scripts/ 底下執行，不要放進 backend。
"""

import os
import re
import csv

CURRENT_YEAR = 2026  # 系統日期 2026-08-08，見CLAUDE.md/總結.md

FRONTEND_ROOT = r"D:\xian-shang-you-wei\backend\frontend"
SCAN_SUBDIRS = ["tools", "blog"]

# 各語言資料夾 -> 語言顯示名稱（""=繁中根目錄）
LANG_FOLDERS = {
    "": "繁體中文（根目錄）",
    "en": "英文",
    "ja": "日文",
    "ko": "韓文",
    "de": "德文",
    "fr": "法文",
    "es": "西班牙文",
    "pt": "葡萄牙文",
    "id": "印尼文",
    "zh-CN": "簡體中文",
}

# 各語言「相對時間詞」清單（語意上一定會過期，比年份字樣更容易漏抓）
# 英文版之前是空的（原始bug），這次補齊
STALE_PHRASES = {
    "": ["去年", "今年", "最新版", "最新稅率", "最新利率", "目前的稅率", "目前利率", "現行稅率"],
    "en": [
        "last year", "this year", "current tax year", "latest rate", "latest rates",
        "current rate is", "current interest rate", "as of 2023", "as of 2024", "as of 2025",
        "up to date as of", "currently set at",
    ],
    "ja": ["昨年", "今年", "最新の税率", "現在の税率", "現行の税率"],
    "ko": ["작년", "올해", "최신 세율", "현재 세율", "현행 세율"],
    "de": ["letztes Jahr", "dieses Jahr", "aktueller Steuersatz", "neueste Rate", "derzeitiger Zinssatz"],
    "fr": ["l'année dernière", "cette année", "taux actuel", "dernier taux", "taux en vigueur"],
    "es": ["el año pasado", "este año", "tasa actual", "última tasa", "tipo vigente"],
    "pt": ["ano passado", "este ano", "taxa atual", "última taxa", "taxa vigente"],
    "id": ["tahun lalu", "tahun ini", "tarif saat ini", "tarif terbaru", "suku bunga saat ini"],
    "zh-CN": ["去年", "今年", "最新版", "最新税率", "最新利率", "目前的税率", "目前利率", "现行税率"],
}

YEAR_RE = re.compile(r"\b(20[0-2][0-9])\b")

# ISO日期格式(YYYY-MM-DD)或後面接年份的日期範圍，這是date input的預設值/placeholder，
# 不是「過期內容」的文字宣稱，排除掉（例如 placeholder="2025-01-01"）
YEAR_IS_DATE_VALUE_RE = re.compile(r"20[0-2][0-9]-\d{2}-\d{2}")

# 數字恰好是 HTML 屬性值本身（例如 placeholder="2000"、value="2000"），
# 這是金額/熱量等數字範例，不是年份宣稱，排除掉
ATTR_VALUE_RE = re.compile(r'(?:placeholder|value|min|max|step)="\d*$')

TAG_STRIP_RE = re.compile(r"<(script|style|svg)\b[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE)


def get_lang_key(scan_root, filepath):
    rel = os.path.relpath(filepath, scan_root)
    parts = rel.split(os.sep)
    if len(parts) >= 2 and parts[0] in LANG_FOLDERS:
        return parts[0]
    return ""


def strip_script_style(content):
    """拿掉 <script>/<style>/<svg> 內容，避免JSON-LD schema日期、GA追蹤碼、
    SVG圖表座標數字（例如 viewBox 或 path 座標剛好是4位數字）等誤判"""
    return TAG_STRIP_RE.sub("", content)


def snippet(content, start, end, pad=40):
    s = max(0, start - pad)
    e = min(len(content), end + pad)
    return content[s:e].replace("\n", " ").replace("\r", " ").strip()


def scan_file(filepath, lang_key):
    with open(filepath, encoding="utf-8", errors="ignore") as f:
        raw = f.read()
    content = strip_script_style(raw)

    rows = []

    # 年份字樣（排除當年2026與未來年份，只抓看起來會過期的舊年份）
    for m in YEAR_RE.finditer(content):
        year = int(m.group(1))
        if year >= CURRENT_YEAR:
            continue
        # 排除 ISO 日期格式（例如 date input 的 placeholder/value="2025-01-01"），
        # 這是表單預設值，不是「過期內容」的文字宣稱
        window = content[m.start():m.start() + 12]
        if YEAR_IS_DATE_VALUE_RE.match(window):
            continue
        # 排除數字本身就是HTML屬性值（例如 placeholder="2000" 這種金額/熱量範例）
        before = content[max(0, m.start() - 25):m.start()]
        if ATTR_VALUE_RE.search(before):
            continue
        rows.append(("年份字樣", f"出現「{year}」", snippet(content, m.start(), m.end())))

    # 相對時間詞 / 已停產型態關鍵字
    phrases = STALE_PHRASES.get(lang_key, [])
    for phrase in phrases:
        for m in re.finditer(re.escape(phrase), content, re.IGNORECASE):
            rows.append(("相對時間詞", f"出現「{phrase}」", snippet(content, m.start(), m.end())))

    return rows


def main():
    all_rows = []
    files_scanned = 0
    files_with_issues = 0

    for subdir in SCAN_SUBDIRS:
        scan_root = os.path.join(FRONTEND_ROOT, subdir)
        if not os.path.isdir(scan_root):
            print(f"跳過（資料夾不存在）：{scan_root}")
            continue
        print(f"掃描：{scan_root}")

        for dirpath, _, filenames in os.walk(scan_root):
            for fn in filenames:
                if not fn.endswith(".html"):
                    continue
                filepath = os.path.join(dirpath, fn)
                files_scanned += 1
                lang_key = get_lang_key(scan_root, filepath)
                lang_name = LANG_FOLDERS.get(lang_key, lang_key)
                rel_path = os.path.join(subdir, os.path.relpath(filepath, scan_root))

                hits = scan_file(filepath, lang_key)
                if hits:
                    files_with_issues += 1
                    for check_type, issue, ctx in hits:
                        all_rows.append({
                            "檔案": rel_path,
                            "語言": lang_name,
                            "檢查類型": check_type,
                            "問題內容": issue,
                            "上下文": ctx,
                        })

    print(f"\n共掃描 {files_scanned} 個html檔案")
    print(f"疑似有過期內容訊號的檔案數：{files_with_issues}")
    print(f"問題總筆數：{len(all_rows)}\n")

    if all_rows:
        by_lang = {}
        for row in all_rows:
            by_lang.setdefault(row["語言"], set()).add(row["檔案"])
        print("各語言中獎頁數：")
        for lang_name, files in sorted(by_lang.items(), key=lambda x: -len(x[1])):
            print(f"  {lang_name}: {len(files)} 頁")

        out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outdated_content_report.csv")
        with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["檔案", "語言", "檢查類型", "問題內容", "上下文"])
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"\n完整報告已輸出：{out_path}")
    else:
        print("沒有掃到任何疑似過期內容訊號。")


if __name__ == "__main__":
    main()
