# -*- coding: utf-8 -*-
"""
批次修正24個檔案的JS計算邏輯未在地化問題。

這批檔案的JS計算輸出全部是同款寫死美金的格式:
  '$' + X.toLocaleString('en-US', {...})
但輸入框本身早就是正確的當地符號(已用3個樣本樣本ja/de/zh-TW確認),
代表這是跟先前那次「貨幣JS修復」同一種病灶,只是這24個檔案沒被那次涵蓋到。

做法:把 '$' + X.toLocaleString('en-US' 換成 '{當地符號}' + X.toLocaleString('{當地locale}'
不動輸入框、不動其他任何邏輯。

處理範圍(7語言、共24個檔案,只鎖定這份清單,不會影響清單外的檔案):
  ja: freelancer-tax, property-tax
  ko: freelancer-tax, property-tax
  de: freelancer-tax, property-tax, oop-maximum-calc
  fr: freelancer-tax, property-tax, oop-maximum-calc
  id: freelancer-tax, property-tax
  zh-CN: freelancer-tax, property-tax, oop-maximum-calc
  zh-TW: 0-percent-financing, freelancer-tax, mortgage-refinance,
         overtime-calculator, personal-loan-calc, position-size,
         rental-income-tax, renters-insurance, solar-roi

用法(先dry-run再apply):
  python fix_js_not_localized_batch.py --root "D:\\xian-shang-you-wei\\backend\\frontend"
  python fix_js_not_localized_batch.py --root "D:\\xian-shang-you-wei\\backend\\frontend" --apply
"""

import argparse
import re
import shutil
from pathlib import Path

LOCALE_MAP = {
    "ja": ("¥", "ja-JP"),
    "ko": ("₩", "ko-KR"),
    "de": ("€", "de-DE"),
    "fr": ("€", "fr-FR"),
    "id": ("Rp", "id-ID"),
    "zh-CN": ("¥", "zh-CN"),
    "zh-TW": ("NT$", "zh-TW"),
}

FILES = {
    "ja": ["freelancer-tax", "property-tax"],
    "ko": ["freelancer-tax", "property-tax"],
    "de": ["freelancer-tax", "property-tax", "oop-maximum-calc"],
    "fr": ["freelancer-tax", "property-tax", "oop-maximum-calc"],
    "id": ["freelancer-tax", "property-tax"],
    "zh-CN": ["freelancer-tax", "property-tax", "oop-maximum-calc"],
    "zh-TW": [
        "0-percent-financing", "freelancer-tax", "mortgage-refinance",
        "overtime-calculator", "personal-loan-calc", "position-size",
        "rental-income-tax", "renters-insurance", "solar-roi",
    ],
}

DOLLAR_ENUS_RE = re.compile(r"'\$'\s*\+\s*(\w+)\.toLocaleString\('en-US'")


def process_file(path: Path, lang: str, apply: bool, backup_dir: Path):
    symbol, locale = LOCALE_MAP[lang]
    html = path.read_bytes().decode("utf-8")

    matches = DOLLAR_ENUS_RE.findall(html)
    if not matches:
        return "no_pattern_found(可能已修正或格式不同,需人工確認)"

    new_html = DOLLAR_ENUS_RE.sub(
        lambda m: f"'{symbol}' + {m.group(1)}.toLocaleString('{locale}'", html
    )

    if apply:
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup_dir / f"{lang}_{path.name}")
        path.write_bytes(new_html.encode("utf-8"))

    return f"ok({len(matches)}處改為{symbol}/{locale})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--backup-dir", default=None)
    args = ap.parse_args()

    root = Path(args.root)
    backup_dir = Path(args.backup_dir) if args.backup_dir else root.parent / "_js_not_localized_backup"

    total_ok = 0
    total_files = 0

    for lang, tools in FILES.items():
        for tool in tools:
            if lang == "zh-TW":
                path = root / "tools" / f"{tool}.html"
            else:
                path = root / "tools" / lang / f"{tool}.html"
            total_files += 1
            if not path.exists():
                print(f"[{lang}] {tool}: 檔案不存在,跳過")
                continue
            result = process_file(path, lang, args.apply, backup_dir)
            print(f"[{lang}] {tool}: {result}")
            if result.startswith("ok"):
                total_ok += 1

    print(f"\n{'已套用' if args.apply else 'DRY-RUN,尚未寫入'}: {total_ok}/{total_files} 個檔案")
    if args.apply and total_ok:
        print(f"已備份至: {backup_dir}")


if __name__ == "__main__":
    main()
