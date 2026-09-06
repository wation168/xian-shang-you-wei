# -*- coding: utf-8 -*-
"""
自動修正 input-prefix 貨幣符號bug —— 預設 dry-run,不會真的修改檔案。

修正範圍(只處理下列3類,其餘LOCALIZE類這支不動,之後另外處理):
  - MISMATCH: 同頁符號不一致(input-prefix / 內文 / JS計算結果三方沒對齊)
  - TYPO:     欄位語意跟符號對不上(金額欄位標%、百分比欄位標貨幣符號)
  - 全形/半形符號不一致(￥ vs ¥)

判斷「正確答案」的依據優先順序:
  1. JS計算邏輯實際輸出的符號(toLocaleString那幾行,這是計算邏輯的真實來源,
     不是憑空猜的語言對照表)
  2. 如果一個檔案裡完全找不到JS計算輸出符號,才退回用語言預設對照表

不處理的:
  - EXCEPTION白名單(美國制度專屬工具,如401k/income-tax等)
  - PLACEHOLDER白名單(技術分析/報價類工具)
  - LOCALIZE類(美制單位换算,如加侖/英里,工程量不同,由另一支腳本處理)
  - customRatio這類「比例」欄位(不是貨幣)

用法:
  先dry-run看會改哪些檔案、改幾筆(不會寫入):
    python fix_currency_prefix_bugs.py --root "D:\\xian-shang-you-wei\\backend\\frontend"

  確認dry-run結果沒問題後,加 --apply 才會真的寫入(且會先備份.bak):
    python fix_currency_prefix_bugs.py --root "D:\\xian-shang-you-wei\\backend\\frontend" --apply
"""

import argparse
import re
import shutil
from pathlib import Path
from collections import Counter

LOCALE_CURRENCY = {
    "en": "$", "es": "€", "fr": "€", "de": "€", "pt": "€",
    "ja": "¥", "ko": "₩", "id": "Rp", "zh-CN": "¥", "zh-TW": "NT$",
}

US_INSTITUTION_TOOLS = {
    "401k-contribution", "catch-up-contribution", "fsa-savings-calc",
    "hsa-contribution-calc", "roth-vs-traditional", "income-tax",
    "capital-gains-tax", "payroll-tax", "bonus-tax", "take-home-pay",
}

TECHNICAL_TOOLS_KEYWORDS = [
    "candlestick", "pivot-point", "support-resistance", "macd",
    "rsi-calculator", "bollinger", "stochastic", "fibonacci",
    "gann-", "dow-theory", "elliott-wave", "moving-average",
    "chart-pattern", "average-down", "dividend-yield", "stock-",
    "atr-calculator", "obv-", "adx-", "cci-", "williams-r",
    "ichimoku", "keltner", "vwap", "heikin-ashi", "volume-profile",
]

# 不是貨幣、是比例/其他符號的欄位,整個跳過不處理
SKIP_FIELD_IDS = {"customRatio"}

# 欄位本身是「稅務抵免/政府補助」類字眼,這種不能單純換符號解決
# (換符號≠內容正確,例如美國聯邦EV補助$7,500,換成€不代表歐洲有一樣的補助)
# 內文含美國專屬關鍵字時,這類欄位整個跳過,留給人工判斷
US_CREDIT_FIELD_HINTS = {"credit", "rebate", "incentive", "subsidy"}
US_SPECIFIC_KEYWORDS = [
    "IRS", "Estados Unidos", "United States", "federal tax credit",
    "crédito fiscal federal", "401(k)", "401k", "Social Security", "Medicare",
    "IRS Notice", "HSA", "HDHP", "FSA", "IRA", "W-2", "Form 1040",
    "健康貯蓄口座", "高額控除健康保険",
]

CURRENCY_SYMBOLS = ["€", "£", "¥", "₩", "R$", "Rp", "NT$", "$", "￥"]
# 正規表示式用的符號清單要用CURRENCY_SYMBOLS動態產生,不要另外手key一份
# (先前這裡漏了£,導致stamp-duty.html這種正確使用£的頁面被誤判)
_CALC_SYMBOL_ALT = "|".join(re.escape(s) for s in
                             sorted(CURRENCY_SYMBOLS, key=len, reverse=True))
FULLWIDTH_TO_HALFWIDTH = {"￥": "¥"}

MONEY_FIELD_HINTS = {
    "price", "cost", "payment", "fee", "income", "insurance", "value",
    "amount", "salary", "wage", "expense", "deposit", "loan", "rent",
    "credit", "maintenance", "registration", "charge",
}
PERCENT_FIELD_HINTS_STRONG = {"percent", "percentage", "apr", "ratio"}
PERCENT_FIELD_QUALIFIERS = {"interest", "tax", "growth", "return", "inflation",
                             "discount", "commission"}
# 純OHLC報價型欄位(開高低收/前一日收盤),不管工具叫什麼名字,這種欄位
# 本質上就是「輸入一個報價數字」,不是「輸入你的當地金額」,直接排除
OHLC_FIELD_WORDS = {"open", "close", "high", "low", "previous", "current", "price"}

_CALC_SYMBOL_RE = re.compile(
    r"textContent\s*=\s*'(" + _CALC_SYMBOL_ALT + r")'\s*\+"
)

INPUT_PREFIX_RE = re.compile(
    r'(<div class="input-row"><span class="input-prefix">)([^<]*)(</span>'
    r'<input[^>]*id=")([^"]+)("[^>]*>)'
)
ARTICLE_RE = re.compile(r'(<article.*?</article>)', re.S)


def split_camel_words(field_id: str) -> set:
    parts = field_id.replace("_", " ")
    parts = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', parts)
    return set(w.lower() for w in parts.split() if w)


def detect_calc_symbol(html: str, lang: str):
    """從JS計算輸出找真正在用的貨幣符號。

    回傳 (symbol, confidence):
      confidence = 'js'       —— 從JS計算結果直接找到,最高信心
      confidence = 'majority' —— JS找不到,改用同頁所有input-prefix的多數決
                                  (自己跟自己比,不對語言做任何假設)
      confidence = None       —— 兩種訊號都沒有明確答案,不做任何修改,整個檔案跳過

    刻意不用「這個語言預設應該用什麼符號」當保底,因為像
    severance-calculator.html(台灣勞基法專屬,標題就寫Taiwan)、
    stamp-duty.html(英國印花稅專屬)這類「工具本身鎖定特定國家、
    跟頁面語言無關」的情況,套語言預設猜測一定會猜錯。
    """
    matches = _CALC_SYMBOL_RE.findall(html)
    matches = [FULLWIDTH_TO_HALFWIDTH.get(m, m) for m in matches]
    if matches:
        symbol, count = Counter(matches).most_common(1)[0]
        return symbol, "js"

    # JS抓不到符號 → 改看同頁所有input-prefix欄位自己的多數決
    simple_prefixes = re.findall(r'<span class="input-prefix">([^<]*)</span>', html)
    simple_prefixes = [FULLWIDTH_TO_HALFWIDTH.get(p.strip(), p.strip()) for p in simple_prefixes]
    currency_prefixes = [p for p in simple_prefixes if p in CURRENCY_SYMBOLS]

    if not currency_prefixes:
        return None, None

    symbol, count = Counter(currency_prefixes).most_common(1)[0]
    if count / len(currency_prefixes) > 0.5:
        return symbol, "majority"
    # 沒有明確多數(例如一半一半),不確定,不猜
    return None, None


def process_file(path: Path, lang: str, apply: bool, backup_dir: Path):
    basename = path.stem
    if basename in US_INSTITUTION_TOOLS:
        return None  # EXCEPTION,不動
    if any(kw in basename for kw in TECHNICAL_TOOLS_KEYWORDS):
        return None  # PLACEHOLDER,不動

    original = path.read_bytes()
    try:
        html = original.decode("utf-8")
    except UnicodeDecodeError:
        html = original.decode("utf-8", errors="replace")

    calc_symbol, confidence = detect_calc_symbol(html, lang)
    if calc_symbol is None:
        # 兩種訊號都沒有明確答案(JS抓不到、input-prefix也沒有明確多數),
        # 不確定就不動,整個檔案跳過,留給人工判斷比較安全
        return None

    has_us_keyword = any(kw in html for kw in US_SPECIFIC_KEYWORDS)
    expected_symbol = LOCALE_CURRENCY.get(lang, "$")

    # 算出「輸入框自己的多數決」,拿來跟JS結果對照,判斷是否真的互相矛盾
    # (不是只看JS結果跟語言預設是否不同——那樣會誤傷stamp-duty這種
    # JS跟輸入框本來就一致、只是這個工具本身跟頁面語言常態不同的情況)
    simple_prefixes = re.findall(r'<span class="input-prefix">([^<]*)</span>', html)
    simple_prefixes = [FULLWIDTH_TO_HALFWIDTH.get(p.strip(), p.strip()) for p in simple_prefixes]
    currency_prefixes = [p for p in simple_prefixes if p in CURRENCY_SYMBOLS]
    input_majority = None
    if currency_prefixes:
        sym, count = Counter(currency_prefixes).most_common(1)[0]
        if count / len(currency_prefixes) > 0.5:
            input_majority = sym

    # 安全檢查:JS結果 跟 輸入框多數決 真的互相矛盾,而且輸入框那邊剛好符合
    # 這個語言正常該用的符號、內文又沒有美國專屬關鍵字 —— 這種情況代表
    # 「輸入框本來是對的(符合當地內容),JS計算邏輯本身才是還沒在地化的
    # 真bug」,不能自動把輸入框改成配合JS,那樣會把真bug偽裝成一致、更難發現
    if (confidence == "js" and input_majority is not None
            and input_majority != calc_symbol
            and input_majority == expected_symbol
            and not has_us_keyword):
        return {"file": path, "lang": lang, "calc_symbol": calc_symbol,
                "confidence": "SUSPECT_JS_NOT_LOCALIZED",
                "changes": [], "skipped_for_review": [
                    ("(整頁)", calc_symbol,
                     f"JS計算結果為{calc_symbol},但輸入框多數為{input_majority}"
                     f"(符合{lang}語言常態),內文無美國專屬關鍵字,"
                     f"疑似JS計算邏輯本身未在地化(非本次批次範圍)")
                ]}
    changes = []
    skipped_for_review = []
    new_html = html

    # --- 修正 input-prefix ---
    def replace_prefix(m):
        open_tag, prefix, mid_tag, field_id, close_tag = m.groups()
        prefix = prefix.strip()
        if field_id in SKIP_FIELD_IDS:
            return m.group(0)

        words = split_camel_words(field_id)

        # 純OHLC報價欄位(開高低收),不管工具叫什麼名字都跳過,這是報價
        # 佔位符不是當地金額(補強TECHNICAL_TOOLS_KEYWORDS清單可能有漏的情況)
        if words and words.issubset(OHLC_FIELD_WORDS):
            return m.group(0)

        # 稅務抵免/補助類欄位,且內文有美國專屬關鍵字 → 跳過,留給人工判斷
        if has_us_keyword and bool(words & US_CREDIT_FIELD_HINTS):
            skipped_for_review.append((field_id, prefix,
                "欄位為稅務抵免/補助類且內文含美國專屬關鍵字,不自動改,需人工判斷"))
            return m.group(0)

        looks_money = bool(words & MONEY_FIELD_HINTS)
        looks_percent = bool(words & PERCENT_FIELD_HINTS_STRONG) or (
            "rate" in words and bool(words & PERCENT_FIELD_QUALIFIERS)
        )

        target = None
        reason = None
        if looks_money and prefix == "%":
            target = calc_symbol
            reason = f"TYPO: 金額欄位誤標%,改為{calc_symbol}"
        elif looks_percent and prefix in CURRENCY_SYMBOLS:
            target = "%"
            reason = f"TYPO: 百分比欄位誤標{prefix},改為%"
        elif prefix in CURRENCY_SYMBOLS and prefix != calc_symbol:
            target = calc_symbol
            reason = f"MISMATCH: 輸入框{prefix}與計算結果{calc_symbol}不一致"
        elif prefix in FULLWIDTH_TO_HALFWIDTH:
            target = FULLWIDTH_TO_HALFWIDTH[prefix]
            reason = f"全形轉半形: {prefix}→{target}"

        if target is not None and target != prefix:
            changes.append((field_id, prefix, target, reason))
            return f"{open_tag}{target}{mid_tag}{field_id}{close_tag}"
        return m.group(0)

    new_html = INPUT_PREFIX_RE.sub(replace_prefix, new_html)

    # --- 修正內文(article區塊)裡跟計算結果不一致的貨幣符號 ---
    def replace_article_symbols(m):
        block = m.group(1)
        new_block = block
        for sym in CURRENCY_SYMBOLS:
            if sym == calc_symbol:
                continue
            if sym in new_block:
                count = new_block.count(sym)
                new_block = new_block.replace(sym, calc_symbol)
                changes.append(("(內文)", sym, calc_symbol,
                                 f"MISMATCH: 內文出現{count}次{sym},統一改為{calc_symbol}"))
        return new_block

    new_html = ARTICLE_RE.sub(replace_article_symbols, new_html)

    if not changes and not skipped_for_review:
        return None

    if apply and changes:
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / f"{lang}_{path.name}.bak"
        shutil.copy2(path, backup_path)
        path.write_bytes(new_html.encode("utf-8"))

    return {"file": path, "lang": lang, "calc_symbol": calc_symbol, "confidence": confidence,
             "changes": changes, "skipped_for_review": skipped_for_review}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true", help="真的寫入檔案(預設只dry-run)")
    ap.add_argument("--backup-dir", default=None, help="備份資料夾,預設在root旁邊建立")
    args = ap.parse_args()

    root = Path(args.root)
    backup_dir = Path(args.backup_dir) if args.backup_dir else root.parent / "_currency_prefix_backup"

    languages = ["en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN", "zh-TW"]
    all_file_results = []

    for lang in languages:
        if lang == "zh-TW":
            lang_dir = root / "tools"
            html_files = list(lang_dir.glob("*.html"))
        else:
            lang_dir = root / "tools" / lang
            html_files = list(lang_dir.rglob("*.html")) if lang_dir.exists() else []

        for html_file in html_files:
            result = process_file(html_file, lang, args.apply, backup_dir)
            if result:
                all_file_results.append(result)

    total_changes = sum(len(r["changes"]) for r in all_file_results)
    total_skipped = sum(len(r["skipped_for_review"]) for r in all_file_results)
    suspect_js_files = [r for r in all_file_results if r["confidence"] == "SUSPECT_JS_NOT_LOCALIZED"]
    normal_results = [r for r in all_file_results if r["confidence"] != "SUSPECT_JS_NOT_LOCALIZED"]

    print(f"\n{'=== 已套用修改 ===' if args.apply else '=== DRY-RUN(尚未寫入任何檔案) ==='}")
    print(f"受影響檔案數: {len(normal_results)}")
    print(f"總修改筆數: {total_changes}")
    print(f"跳過待人工判斷筆數(美國補助類欄位): {sum(len(r['skipped_for_review']) for r in normal_results)}")
    print(f"疑似JS計算邏輯本身未在地化(整檔跳過,非本次批次範圍): {len(suspect_js_files)}")

    print("\n=== 前20個檔案的修改明細(抽樣預覽) ===")
    shown = 0
    for r in normal_results:
        if not r["changes"] and not r["skipped_for_review"]:
            continue
        if shown >= 20:
            break
        shown += 1
        print(f"\n[{r['lang']}] {r['file'].name}  (計算結果符號={r['calc_symbol']}, 判斷依據={r['confidence']})")
        for field_id, old, new, reason in r["changes"][:5]:
            print(f"    {field_id}: '{old}' → '{new}'  ({reason})")
        if len(r["changes"]) > 5:
            print(f"    ...還有{len(r['changes'])-5}筆")
        for field_id, prefix, reason in r["skipped_for_review"]:
            print(f"    [跳過待判斷] {field_id} (目前={prefix})  {reason}")

    if total_skipped:
        print(f"\n=== 全部跳過待人工判斷清單(美國補助類欄位) ===")
        for r in normal_results:
            for field_id, prefix, reason in r["skipped_for_review"]:
                print(f"[{r['lang']}] {r['file'].name} / {field_id} (目前={prefix})")

    if suspect_js_files:
        print(f"\n=== 疑似JS計算邏輯本身未在地化清單(整檔跳過,共{len(suspect_js_files)}個) ===")
        for r in suspect_js_files:
            print(f"[{r['lang']}] {r['file'].name}  (JS結果={r['calc_symbol']})")

    if args.apply:
        print(f"\n已備份原始檔至: {backup_dir}")
    else:
        print("\n這是dry-run,沒有任何檔案被修改。確認數量合理後,加上 --apply 參數才會真的寫入。")


if __name__ == "__main__":
    main()
