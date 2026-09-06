# -*- coding: utf-8 -*-
"""
緊急修正:ev-vs-gas.html 的 evTaxCredit 欄位被前一批修正誤改。

背景:前一支 fix_currency_prefix_bugs.py 的「美國專屬關鍵字」判斷清單只認得
英文/西班牙文的講法,日文/韓文/德文/法文/葡萄牙文/印尼文/簡中/繁中版本的
內文是用當地語言寫「聯邦稅額抵免」,沒被清單抓到,導致 evTaxCredit(美國
聯邦EV稅務抵免,固定美金金額,跟頁面語言無關)被誤判成一般欄位,跟著改成
當地貨幣符號,產生「日本有¥7,500聯邦補助」這種錯誤資訊。

範圍:只處理 ev-vs-gas.html 這一個檔案、evTaxCredit 這一個欄位,強制改回 $。
不動其他任何檔案或欄位。

用法(一樣先dry-run再apply):
  python fix_ev_tax_credit_regression.py --root "D:\\xian-shang-you-wei\\backend\\frontend"
  python fix_ev_tax_credit_regression.py --root "D:\\xian-shang-you-wei\\backend\\frontend" --apply
"""

import argparse
import re
import shutil
from pathlib import Path

FIELD_PREFIX_RE = re.compile(
    r'(<span class="input-prefix">)([^<]*)(</span>'
    r'<input[^>]*id="evTaxCredit")'
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--backup-dir", default=None)
    args = ap.parse_args()

    root = Path(args.root)
    backup_dir = Path(args.backup_dir) if args.backup_dir else root.parent / "_evtaxcredit_backup"

    languages = ["en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN", "zh-TW"]
    touched = []

    for lang in languages:
        if lang == "zh-TW":
            path = root / "tools" / "ev-vs-gas.html"
        else:
            path = root / "tools" / lang / "ev-vs-gas.html"
        if not path.exists():
            continue

        html = path.read_text(encoding="utf-8")
        m = FIELD_PREFIX_RE.search(html)
        if not m:
            print(f"[{lang}] 找不到evTaxCredit欄位,跳過")
            continue

        current_prefix = m.group(2).strip()
        if current_prefix == "$":
            print(f"[{lang}] evTaxCredit已經是$,不用改")
            continue

        print(f"[{lang}] evTaxCredit: '{current_prefix}' → '$'")
        touched.append((lang, path, current_prefix))

        if args.apply:
            new_html = FIELD_PREFIX_RE.sub(r'\1$\3', html, count=1)
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, backup_dir / f"{lang}_ev-vs-gas.html.bak")
            path.write_text(new_html, encoding="utf-8")

    print(f"\n{'已套用' if args.apply else 'DRY-RUN,尚未寫入'}: 共{len(touched)}個語言版本需要修正")
    if args.apply and touched:
        print(f"已備份至: {backup_dir}")


if __name__ == "__main__":
    main()
