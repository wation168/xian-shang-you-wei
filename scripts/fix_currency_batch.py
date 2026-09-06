#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_currency_batch.py — 批次修正 calc_js 裡寫死的英文貨幣符號
用法：
  cd D:\\xian-shang-you-wei\\scripts
  python fix_currency_batch.py                # dry-run，只印出會改什麼，不寫檔
  python fix_currency_batch.py --apply         # 真的寫入檔案（會先備份）

只處理「通用型」工具（A類），美國特定稅務/醫療保險制度工具（B類）
一律跳過，維持原本的 USD 顯示（這是刻意保留，不是漏改）。
"""
import os, re, sys, shutil, codecs
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, errors='replace')

BASE = r"D:\xian-shang-you-wei\backend\frontend\tools"

# 每個語言對應的貨幣符號 / toLocaleString 語系代碼
# 註: pt 目前先用歐元(葡萄牙)，因為現有 es 版precedent是用歐元；
#     若你的葡文版目標是巴西市場，這裡要改成 "R$" / "pt-BR"，跑之前先跟我確認
LOCALE_MAP = {
    "zh-TW": ("NT$", "zh-TW"),
    "ja":    ("¥",   "ja-JP"),
    "de":    ("€",   "de-DE"),
    "fr":    ("€",   "fr-FR"),
    "es":    ("€",   "es-ES"),
    "pt":    ("€",   "pt-PT"),   # ⚠️ 若目標巴西市場改 ("R$","pt-BR")
    "ko":    ("₩",   "ko-KR"),
    "id":    ("Rp",  "id-ID"),
    "zh-CN": ("¥",   "zh-CN"),
}

# A類：通用型工具，需要依語言在地化貨幣符號
A_CATEGORY = [
    "0-percent-financing","alimony-calculator","amazon-profit","annuity-calculator",
    "annuity-income","appliance-energy","asset-allocation","atr-calculator",
    "bollinger-bands","burn-rate-calculator","business-exit-value","business-loan-calc",
    "cagr","car-depreciation","car-insurance-calc","car-insurance-estimate",
    "car-lease-vs-buy","child-support","commute-cost","company-registration",
    "compound-interest-debt","customer-acquisition","dca-calculator","dcf-calculator",
    "debt-consolidation","disability-insurance","dropship-margin","employee-cost",
    "ev-vs-gas","fibonacci-retracement","franchise-roi","freelance-rate",
    "gas-bill","gross-profit-margin","health-insurance-estimate","heloc-vs-personal-loan",
    "home-affordability","home-energy-audit","home-insurance-calc","home-mortgage",
    "income-replacement","influencer-rate","insurance-premium-compare","inventory-turnover",
    "ivf-cost-calculator","landed-cost","lasik-cost-calculator","late-payment-interest",
    "lawyer-fee","led-savings","liability-insurance","life-insurance-calc",
    "life-insurance-needs","loan-affordability","loan-vs-lease","long-term-care",
    "medical-cost-estimator","medical-tourism-saving","medication-cost-compare","meeting-cost",
    "mortgage-refinance","mrr-calculator","notary-fee","options-profit",
    "overtime-calculator","paint-calculator","parking-cost","patent-cost",
    "pension-vs-lump-sum","personal-loan-calc","pet-insurance-calc","pip-value",
    "pivot-point","position-size","pricing-calculator","rehab-cost-estimator",
    "rental-income-tax","renters-insurance","retirement-savings-gap","retirement",
    "risk-reward","roi-calculator","roi-of-insurance","saas-ltv-cac",
    "salary-raise","salary-to-hourly","sales-commission","shipping-cost",
    "shopee-profit","solar-roi","startup-valuation","student-loan-refi",
    "student-loan","surgery-cost-estimator","tip-calculator","trademark-fee",
    "trading-fee","travel-insurance-calc","tuition-cost","water-bill",
    "withdrawal-rate","working-capital","youtube-revenue",
]

# B類：美國特定制度工具，維持USD不變，故意排除，不列入處理
B_CATEGORY_SKIPPED = [
    "capital-gains-tax","catch-up-contribution","court-fee","coverage-gap-finder",
    "effective-tax-rate","freelancer-tax","fsa-savings-calc","income-tax",
    "oop-maximum-calc","premium-vs-hdhp","property-tax","required-minimum-dist","vat-calculator",
]

# 抓 JS 裡寫死美元符號的常見寫法
PATTERNS = [
    (re.compile(r"'\$'\s*\+"), None),  # '$' + xxx  → 換成對應符號
    (re.compile(r'"\$"\s*\+'), None),  # "$" + xxx
    (re.compile(r"toLocaleString\('en-US'"), None),
    (re.compile(r'toLocaleString\("en-US"'), None),
]

def find_files():
    targets = []
    for lang in LOCALE_MAP:
        for slug in A_CATEGORY:
            path = os.path.join(BASE, lang, slug + ".html")
            if os.path.exists(path):
                targets.append((lang, slug, path))
    return targets

def fix_content(content, lang):
    symbol, locale_code = LOCALE_MAP[lang]
    original = content
    changed = False

    # 抓 <script> 區塊內的 calculate 相關函式，只在script內做替換，避免誤改文章內文
    def replace_in_script(m):
        nonlocal changed
        script_body = m.group(0)
        new_body = script_body
        new_body, n1 = re.subn(r"'\$'(\s*\+)", f"'{symbol}'\\1", new_body)
        new_body, n2 = re.subn(r'"\$"(\s*\+)', f'"{symbol}"\\1', new_body)
        new_body, n3 = re.subn(r"toLocaleString\('en-US'", f"toLocaleString('{locale_code}'", new_body)
        new_body, n4 = re.subn(r'toLocaleString\("en-US"', f'toLocaleString("{locale_code}"', new_body)
        if n1 + n2 + n3 + n4 > 0:
            changed = True
        return new_body

    new_content = re.sub(r"<script\b[^>]*>.*?</script>", replace_in_script, content, flags=re.DOTALL)
    return new_content, changed

def main():
    apply = "--apply" in sys.argv
    targets = find_files()
    print(f"[掃描範圍] {len(targets)} 個檔案 (A類{len(A_CATEGORY)}個工具 x 9個非英文語言，實際存在的檔案數)")
    print(f"[跳過] B類美國特定制度工具，共{len(B_CATEGORY_SKIPPED)}個工具不處理: {', '.join(B_CATEGORY_SKIPPED)}")
    print()

    changed_count = 0
    skipped_no_match = 0

    for lang, slug, path in targets:
        try:
            with open(path, "rb") as f:
                raw = f.read()
            content = raw.decode("utf-8")
        except Exception as e:
            print(f"[錯誤] 讀取失敗 {path}: {e}")
            continue

        new_content, changed = fix_content(content, lang)

        if not changed:
            skipped_no_match += 1
            continue

        changed_count += 1
        symbol, locale_code = LOCALE_MAP[lang]
        print(f"[{'將修改' if not apply else '已修改'}] {lang}/{slug}.html  →  貨幣符號改為 '{symbol}'，locale改為 '{locale_code}'")

        if apply:
            backup_path = path + ".bak"
            shutil.copy2(path, backup_path)
            with open(path, "wb") as f:
                f.write(new_content.encode("utf-8"))

    print()
    print(f"[統計] 有異動: {changed_count} 個檔案 | 掃描到但無需改動: {skipped_no_match} 個檔案")
    if not apply:
        print()
        print("=== 這是 DRY-RUN，尚未真的寫入任何檔案 ===")
        print("確認上面清單沒問題後，執行： python fix_currency_batch.py --apply")
        print("--apply 執行時會先幫每個被改的檔案存一份 .bak 備份，再寫入新內容")

if __name__ == "__main__":
    main()
