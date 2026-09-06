#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_untranslated.py — 掃描非英文工具頁裡殘留的未翻譯內容
（更多工具連結顯示原始slug、貨幣符號未在地化、單位後綴殘留英文等）

用法：
  cd D:\\xian-shang-you-wei\\scripts
  python scan_untranslated.py

只掃描，不修改任何檔案。輸出 untranslated_report.csv
"""
import os, re, csv, sys, codecs
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, errors='replace')

BASE = r"D:\xian-shang-you-wei\backend\frontend\tools"
NON_EN_LANGS = ["zh-TW","ja","de","fr","es","pt","ko","id","zh-CN"]
# zh-TW工具頁實際上放在tools/根目錄，不是tools/zh-TW/，特別處理
ROOT_IS_ZHTW = True

# 每個語言「合法」使用的貨幣符號（用來判斷input-prefix是否殘留錯誤符號）
EXPECTED_CURRENCY = {
    "zh-TW": ["NT$","$"], "ja": ["¥"], "de": ["€"], "fr": ["€"],
    "es": ["€"], "pt": ["€"], "ko": ["₩"], "id": ["Rp"], "zh-CN": ["¥"],
}

# 一組粗略但實用的判斷：文字看起來像「未翻譯的原始slug」
SLUG_PATTERN = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)+$')

# 常見英文單字，如果出現在de/fr/es/pt/id的文字裡，高機率是漏翻
COMMON_EN_WORDS = set("""
the and or for with your years year months month enter calculate result results
value amount rate income expense insurance loan mortgage tax credit debt savings
please select choose click submit calculate estimate coverage payment
""".split())

def find_html_files():
    files = []
    for lang in NON_EN_LANGS:
        if lang == "zh-TW" and ROOT_IS_ZHTW:
            folder = BASE  # zh-TW直接在tools/根目錄
        else:
            folder = os.path.join(BASE, lang)
        if not os.path.isdir(folder):
            continue
        for f in os.listdir(folder):
            if f.endswith(".html") and f != "index.html":
                files.append((lang, os.path.join(folder, f)))
    return files

def check_more_tools_slugs(html, lang, path, issues):
    # 抓 more-tools / tool-pill / blog-card 區塊裡的連結文字
    for m in re.finditer(r'<a[^>]*class="(?:tool-pill|blog-card|related-link)"[^>]*>([^<]*)</a>', html):
        text = m.group(1).strip()
        if SLUG_PATTERN.match(text):
            issues.append((lang, path, "更多工具連結顯示原始slug", text))

def check_currency_prefix(html, lang, path, issues):
    expected = EXPECTED_CURRENCY.get(lang, [])
    for m in re.finditer(r'class="input-prefix">([^<]*)</span>', html):
        symbol = m.group(1).strip()
        if symbol and symbol not in expected:
            issues.append((lang, path, "input-prefix貨幣符號可能不符語言", symbol))

def check_english_leftover(html, lang, path, issues):
    if lang in ("ja","ko","zh-CN"):
        # CJK語言：label/suffix裡若整段是純英文字母，高度可疑
        for m in re.finditer(r'class="input-suffix">([^<]*)</span>', html):
            text = m.group(1).strip()
            if text and re.fullmatch(r'[A-Za-z\s]+', text) and text.lower() not in ("%",):
                issues.append((lang, path, "後綴疑似未翻譯(純英文字母)", text))
        for m in re.finditer(r'<label[^>]*>([^<]*)</label>', html):
            text = m.group(1).strip()
            if text and re.fullmatch(r'[A-Za-z0-9\s\(\)%]+', text):
                issues.append((lang, path, "輸入標籤疑似未翻譯(純英文)", text))
    else:
        # 拉丁語系：用常見英文字判斷
        for m in re.finditer(r'class="input-suffix">([^<]*)</span>', html):
            text = m.group(1).strip().lower()
            if text in COMMON_EN_WORDS:
                issues.append((lang, path, "後綴疑似未翻譯(常見英文字)", m.group(1).strip()))
        for m in re.finditer(r'<label[^>]*>([^<]*)</label>', html):
            words = re.findall(r'[a-zA-Z]+', m.group(1))
            hit = [w for w in words if w.lower() in COMMON_EN_WORDS]
            if hit:
                issues.append((lang, path, "輸入標籤疑似未翻譯(常見英文字)", m.group(1).strip()))

def main():
    files = find_html_files()
    print(f"[掃描範圍] {len(files)} 個檔案\n")
    issues = []
    for lang, path in files:
        try:
            with open(path, "rb") as f:
                html = f.read().decode("utf-8", errors="replace")
        except Exception as e:
            print(f"[錯誤] 讀取失敗 {path}: {e}")
            continue
        check_more_tools_slugs(html, lang, path, issues)
        check_currency_prefix(html, lang, path, issues)
        check_english_leftover(html, lang, path, issues)

    out_path = r"D:\xian-shang-you-wei\scripts\untranslated_report.csv"
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["語言","檔案路徑","問題類型","可疑內容"])
        for row in issues:
            w.writerow(row)

    print(f"[統計] 共發現 {len(issues)} 筆可疑項目")
    by_type = {}
    for _,_,t,_ in issues:
        by_type[t] = by_type.get(t,0)+1
    for t,c in sorted(by_type.items(), key=lambda x:-x[1]):
        print(f"  - {t}: {c} 筆")
    print(f"\n完整清單已輸出：{out_path}")
    print("這是掃描結果，尚未做任何修改。請人工檢視report確認範圍後再決定怎麼修。")

if __name__ == "__main__":
    main()
