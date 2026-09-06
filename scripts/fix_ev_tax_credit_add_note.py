# -*- coding: utf-8 -*-
"""
在 ev-vs-gas.html 的 evTaxCredit 欄位下方,加一句提示文字:
「這是美國聯邦補助金額,其他國家請查詢當地政策」(依各語言翻譯)

不動計算邏輯、不動貨幣符號(evTaxCredit已在前一次回歸修正中確認統一為$),
只在既有的 <small class="input-help"> 說明文字後面,補一句提醒。

用法(一樣先dry-run再apply):
  python fix_ev_tax_credit_add_note.py --root "D:\\xian-shang-you-wei\\backend\\frontend"
  python fix_ev_tax_credit_add_note.py --root "D:\\xian-shang-you-wei\\backend\\frontend" --apply
"""

import argparse
import re
import shutil
from pathlib import Path

# 各語言的提示句(接在原本的input-help說明文字後面)
NOTES = {
    "en": " This is a U.S. federal incentive — check your own country's EV incentives.",
    "es": " Este es un incentivo federal de EE. UU.; consulta los incentivos de tu país.",
    "ja": " これは米国連邦政府の優遇措置です。お住まいの国の優遇制度をご確認ください。",
    "ko": " 이것은 미국 연방 인센티브입니다. 거주 국가의 전기차 인센티브를 확인하세요.",
    "de": " Dies ist ein US-Bundesanreiz — prüfen Sie die Anreize in Ihrem Land.",
    "fr": " Il s'agit d'une incitation fédérale américaine ; vérifiez les incitations de votre pays.",
    "pt": " Este é um incentivo federal dos EUA; verifique os incentivos do seu país.",
    "id": " Ini adalah insentif federal AS; periksa insentif kendaraan listrik di negara Anda.",
    "zh-CN": " 这是美国联邦补贴金额,请查询您所在国家的电动车补贴政策。",
    "zh-TW": " 這是美國聯邦補助金額,請查詢您所在國家的電動車補助政策。",
}

# 找出 evTaxCredit input-row 後面緊接著的那個 <small class="input-help">...</small>
# (欄位順序固定:label → input-row → </div> → small.input-help)
HELP_AFTER_CREDIT_RE = re.compile(
    r'(<input[^>]*id="evTaxCredit"[^>]*></div>\s*</div>\s*<small class="input-help">)'
    r'([^<]*)'
    r'(</small>)'
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--backup-dir", default=None)
    args = ap.parse_args()

    root = Path(args.root)
    backup_dir = Path(args.backup_dir) if args.backup_dir else root.parent / "_evtaxcredit_note_backup"

    languages = ["en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN", "zh-TW"]
    touched = []

    for lang in languages:
        if lang == "zh-TW":
            path = root / "tools" / "ev-vs-gas.html"
        else:
            path = root / "tools" / lang / "ev-vs-gas.html"
        if not path.exists():
            print(f"[{lang}] 檔案不存在,跳過")
            continue

        original = path.read_bytes()
        html = original.decode("utf-8")

        note = NOTES.get(lang, NOTES["en"])
        if note.strip() in html:
            print(f"[{lang}] 已經加過提示文字,不重複加")
            continue

        m = HELP_AFTER_CREDIT_RE.search(html)
        if not m:
            print(f"[{lang}] 找不到evTaxCredit後面的說明文字區塊,跳過(需人工確認)")
            continue

        new_html = HELP_AFTER_CREDIT_RE.sub(
            lambda mm: mm.group(1) + mm.group(2) + note + mm.group(3),
            html, count=1,
        )
        touched.append((lang, path))
        print(f"[{lang}] 將加上提示: {note.strip()[:50]}...")

        if args.apply:
            backup_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, backup_dir / f"{lang}_ev-vs-gas.html.bak")
            path.write_bytes(new_html.encode("utf-8"))

    print(f"\n{'已套用' if args.apply else 'DRY-RUN,尚未寫入'}: 共{len(touched)}個語言版本")
    if args.apply and touched:
        print(f"已備份至: {backup_dir}")


if __name__ == "__main__":
    main()
