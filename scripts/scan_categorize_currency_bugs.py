# -*- coding: utf-8 -*-
"""
掃描分類腳本 — 只掃描,不修改任何檔案。

用途:把 untranslated_report.csv 裡「input-prefix貨幣符號可能不符語言」這類問題,
依照下列5條規則自動分類,產出分類報告給人工看數字決定下一步,不會動到任何原始檔案。

分類規則:
  1. EXCEPTION   — 美國獨有制度/補助(401k、聯邦稅、EV聯邦稅務抵免等),維持USD不動
  2. LOCALIZE    — 通用型內容但現在寫死美制單位/美金(汽油/車輛相關,加侖/英里),
                   需要換貨幣符號 + 用數學換算單位(公升/公里),本腳本只負責標記,
                   實際換算由第二支腳本處理
  3. TYPO        — 純打字bug(符號打錯,如車價欄位打成%而非$),直接標記待修正
  4. PLACEHOLDER — 純價格佔位符(股票報價/技術分析工具的開高低收),不算bug,排除
  5. MISMATCH    — 同頁符號不一致(輸入框$、內文€),直接標記待修正

用法:
  python scan_categorize_currency_bugs.py --root "D:\\xian-shang-you-wei\\backend\\frontend"

輸出:
  categorized_report.csv — 全部檔案的分類結果
  終端機印出各分類筆數統計
"""

import argparse
import csv
import os
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# 分類用的關鍵字/白名單 —— 這些清單目前是初版,實際跑出來的 UNCLASSIFIED
# 名單要人工看過,才能決定要不要補進下面的清單裡
# ---------------------------------------------------------------------------

# 語言 -> 該語言正確的貨幣符號(沿用先前貨幣JS修復那次用的同一套對照表)
LOCALE_CURRENCY = {
    "en": "$", "es": "€", "fr": "€", "de": "€", "pt": "€",
    "ja": "¥", "ko": "₩", "id": "Rp", "zh-CN": "¥", "zh-TW": "NT$",
}
# 注意:es/pt 官方語言涵蓋多國,一部分頁面刻意用當地國家貨幣(巴西Real等)
# 這是已知的簡化假設,LOCALIZE類別會再細分,不會直接依此表硬改

# 已知的「美國獨有制度」工具(不分語言,一律排除,維持USD)
# 這份是目前已確認的清單,如果實際掃描時 UNCLASSIFIED 裡還有明顯美國專屬工具,
# 之後要補進來
US_INSTITUTION_TOOLS = {
    "401k-contribution", "catch-up-contribution", "fsa-savings-calc",
    "hsa-contribution-calc", "roth-vs-traditional", "income-tax",
    "capital-gains-tax", "payroll-tax", "bonus-tax", "take-home-pay",
}

# 內文裡出現這些字樣,強烈暗示是美國專屬制度(用來抓 US_INSTITUTION_TOOLS
# 清單之外、但其實也是美國專屬的工具,例如 ev-vs-gas.html 的聯邦稅務抵免)
US_SPECIFIC_KEYWORDS = [
    "IRS", "Estados Unidos", "United States", "federal tax credit",
    "crédito fiscal federal", "401(k)", "Social Security", "Medicare",
    "IRS Notice",
]

# 純價格佔位符工具(股票/外匯/技術分析類),$在這裡只是報價欄位不是翻譯問題
TECHNICAL_TOOLS_KEYWORDS = [
    "candlestick", "pivot-point", "support-resistance", "macd",
    "rsi-calculator", "bollinger", "stochastic", "fibonacci",
    "gann-", "dow-theory", "elliott-wave", "moving-average",
    "chart-pattern", "average-down", "dividend-yield", "stock-",
]

# 暗示「金額」欄位的 id 關鍵字(用來抓 TYPO:這種欄位卻標成 % 就是打錯)
# 注意:比對時是拆解 camelCase 後逐字比對,不是字串包含,避免 registration
# 誤觸發 ratio 這種意外命中
MONEY_FIELD_HINTS = {
    "price", "cost", "payment", "fee", "income", "insurance", "value",
    "amount", "salary", "wage", "expense", "deposit", "loan", "rent",
    "credit", "maintenance", "registration", "charge",
}
# 暗示「百分比」欄位的字(單獨出現就很明確是百分比,用字組完全比對)
PERCENT_FIELD_HINTS_STRONG = {"percent", "percentage", "apr", "ratio"}
# 「rate」「interest」這類字本身模稜兩可(electricityRate是價格不是%,
# mortgageInterest是金額不是%),只有跟這些字組合出現才視為百分比欄位
PERCENT_FIELD_QUALIFIERS = {"interest", "tax", "growth", "return", "inflation",
                             "discount", "commission", "interestrate"}
# 欄位本身是「稅務抵免/政府補助」類字眼,才可能是美國制度專屬(而不是整頁
# 只要提到一次IRS,所有欄位都算美國專屬——那樣gasPrice/vehiclePrice會被誤蓋掉)
US_CREDIT_FIELD_HINTS = {"credit", "rebate", "incentive", "subsidy"}


def split_camel_words(field_id: str) -> set:
    """把 camelCase / snake_case 的欄位id拆成小寫單字集合"""
    # 先處理 snake_case
    parts = field_id.replace("_", " ")
    # 再處理 camelCase: 在小寫轉大寫的地方插入空格
    parts = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', parts)
    return set(w.lower() for w in parts.split() if w)

# 美制單位標記(加侖/英里),出現這些且不在US_INSTITUTION_TOOLS或US_SPECIFIC裡
# 才會被標成 LOCALIZE
IMPERIAL_UNIT_HINTS = ["/gal", "gallon", "milla", "mile", "/mi"]

INPUT_PREFIX_RE = re.compile(
    r'<div class="input-row">\s*<span class="input-prefix">([^<]*)</span>'
    r'\s*<input[^>]*id="([^"]+)"[^>]*>(?:\s*<span class="input-suffix">([^<]*)</span>)?',
    re.IGNORECASE,
)
ARTICLE_RE = re.compile(r'<article.*?</article>', re.S)
CURRENCY_SYMBOLS = ["€", "£", "¥", "₩", "R$", "Rp", "NT$", "$"]


def find_body_currency_symbols(html: str) -> set:
    """從 <article> 內文找出出現過的貨幣符號(排除純$佔位的input區塊)"""
    symbols = set()
    for m in ARTICLE_RE.finditer(html):
        body = m.group(0)
        for sym in CURRENCY_SYMBOLS:
            if sym in body:
                symbols.add(sym)
    return symbols


def classify_file(path: Path, lang: str) -> list:
    """回傳這個檔案裡每個 input-prefix 欄位的分類結果(可能多筆)"""
    try:
        html = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        html = path.read_text(encoding="utf-8", errors="replace")

    basename = path.stem  # 檔名不含 .html
    results = []

    # 規則1: 美國制度白名單 → 整個檔案都算 EXCEPTION
    is_known_us_tool = basename in US_INSTITUTION_TOOLS
    has_us_keyword = any(kw in html for kw in US_SPECIFIC_KEYWORDS)

    # 規則4: 技術分析/報價類白名單 → 整個檔案都算 PLACEHOLDER
    is_technical_tool = any(kw in basename for kw in TECHNICAL_TOOLS_KEYWORDS)

    if is_technical_tool:
        results.append({
            "language": lang, "file": basename, "field_id": "(全頁)",
            "category": "PLACEHOLDER", "detail": "技術分析/報價類工具,$為佔位符",
        })
        return results

    if is_known_us_tool:
        results.append({
            "language": lang, "file": basename, "field_id": "(全頁)",
            "category": "EXCEPTION", "detail": "已知美國制度專屬工具,維持USD",
        })
        return results

    body_symbols = find_body_currency_symbols(html)
    expected_symbol = LOCALE_CURRENCY.get(lang, "$")

    has_imperial_unit_file = any(kw in html for kw in IMPERIAL_UNIT_HINTS)

    for prefix, field_id, suffix in INPUT_PREFIX_RE.findall(html):
        prefix = prefix.strip()
        words = split_camel_words(field_id)

        # 規則3: TYPO —— 用「完整單字」比對,不是字串包含
        looks_money = bool(words & MONEY_FIELD_HINTS)
        looks_percent_strong = bool(words & PERCENT_FIELD_HINTS_STRONG)
        # 弱訊號(rate/interest)只有跟限定詞組合出現才算百分比,
        # 例如 interestRate、taxRate 算,但 electricityRate、mortgageInterest 不算
        # 只有「rate」當觸發字才算——interest本身模稜兩可(mortgageInterest是
        # 金額不是利率),只能當輔助限定字,不能自己觸發自己
        looks_percent_weak = "rate" in words and bool(words & PERCENT_FIELD_QUALIFIERS)
        looks_percent = looks_percent_strong or looks_percent_weak

        if looks_money and prefix == "%":
            results.append({
                "language": lang, "file": basename, "field_id": field_id,
                "category": "TYPO", "detail": "金額欄位卻標記%,應為貨幣符號",
            })
            continue
        if looks_percent and prefix in CURRENCY_SYMBOLS:
            results.append({
                "language": lang, "file": basename, "field_id": field_id,
                "category": "TYPO", "detail": f"百分比欄位卻標記{prefix},應為%",
            })
            continue

        # 規則5: MISMATCH —— 內文出現跟input不同的貨幣符號(頁面內部不一致)
        other_symbols = body_symbols - {prefix}
        if other_symbols and prefix in CURRENCY_SYMBOLS:
            results.append({
                "language": lang, "file": basename, "field_id": field_id,
                "category": "MISMATCH",
                "detail": f"輸入框用{prefix},內文卻出現{','.join(other_symbols)}",
            })
            continue

        # 規則1(欄位層級補充): 只有「這個欄位本身」是稅務抵免/補助類字眼、
        # 且整頁有美國專屬關鍵字時,才算EXCEPTION候選——不是整頁其他欄位
        # (例如gasPrice、vehiclePrice)也一併算美國專屬,那些要走LOCALIZE
        is_credit_field = bool(words & US_CREDIT_FIELD_HINTS)
        if has_us_keyword and is_credit_field:
            results.append({
                "language": lang, "file": basename, "field_id": field_id,
                "category": "EXCEPTION_CANDIDATE",
                "detail": "欄位為稅務抵免/補助類,且內文含美國專屬關鍵字,建議人工確認",
            })
            continue

        # 規則2: LOCALIZE —— 用了美制單位,且不是美國專屬制度欄位
        field_has_imperial_unit = suffix and any(u in suffix.lower() for u in ["gal", "mile", "milla"])
        if has_imperial_unit_file or field_has_imperial_unit:
            results.append({
                "language": lang, "file": basename, "field_id": field_id,
                "category": "LOCALIZE",
                "detail": f"使用美制單位({suffix or '見同頁其他欄位'}),需換算當地貨幣+單位",
            })
            continue

        # 規則5(補充): prefix符號跟語言預期不符,但內文沒抓到對照符號可比對
        if prefix != expected_symbol and prefix in CURRENCY_SYMBOLS:
            results.append({
                "language": lang, "file": basename, "field_id": field_id,
                "category": "MISMATCH",
                "detail": f"輸入框用{prefix},{lang}語言預期應為{expected_symbol}",
            })
            continue

        # 都沒中規則 → 待人工看,不要用弱訊號硬猜
        results.append({
            "language": lang, "file": basename, "field_id": field_id,
            "category": "UNCLASSIFIED", "detail": f"prefix={prefix}",
        })

    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="backend/frontend 資料夾路徑")
    ap.add_argument("--out", default="categorized_report.csv")
    args = ap.parse_args()

    root = Path(args.root)
    all_results = []

    # 語言資料夾清單(照你們10語言設定,zh-TW先前確認乾淨但仍一併掃描保險)
    languages = ["en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN", "zh-TW"]

    for lang in languages:
        # zh-TW是預設語言,檔案直接放在 tools/ 底下,沒有子資料夾
        # 其他語言在 tools/{lang}/ 底下
        if lang == "zh-TW":
            lang_dir = root / "tools"
            pattern = "*.html"  # 只抓這層,不要 rglob 進其他語言子資料夾
            html_files = [p for p in lang_dir.glob(pattern)]
        else:
            lang_dir = root / "tools" / lang
            html_files = list(lang_dir.rglob("*.html")) if lang_dir.exists() else []

        if not html_files:
            print(f"[跳過] 找不到語言資料夾或無檔案: {lang_dir}")
            continue

        for html_file in html_files:
            all_results.extend(classify_file(html_file, lang))

    # 輸出 CSV
    with open(args.out, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["language", "file", "field_id", "category", "detail"])
        writer.writeheader()
        writer.writerows(all_results)

    # 統計
    from collections import Counter
    cat_counter = Counter(r["category"] for r in all_results)
    print("\n=== 分類統計 ===")
    for cat, count in cat_counter.most_common():
        print(f"{cat:20s}  {count}")
    print(f"\n總計 {len(all_results)} 筆,已輸出至 {args.out}")


if __name__ == "__main__":
    main()
