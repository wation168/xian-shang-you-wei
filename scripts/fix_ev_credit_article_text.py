# -*- coding: utf-8 -*-
"""
修正 es/ev-vs-gas.html 內文的「€7.500 en los Estados Unidos」矛盾內容。

背景:前一次貨幣批次修正時,內文提到「美國聯邦EV補助最高€7.500」這句話
被誤換成歐元符號,但後面接著寫「en los Estados Unidos」(在美國),
€符號配美國文字,自相矛盾,而且真實金額是美金$7,500不是歐元。
只有es語言版本內文提到這個具體數字(已用瀏覽器實測確認ja/ko/de/fr/id/
zh-CN/zh-TW的內文都沒提到這個具體數字,不受影響),範圍很小。

用法:
  python fix_ev_credit_article_text.py --root "D:\\xian-shang-you-wei\\backend\\frontend"
  python fix_ev_credit_article_text.py --root "D:\\xian-shang-you-wei\\backend\\frontend" --apply
"""

import argparse
import shutil
from pathlib import Path

OLD_TEXT = "€7.500 en los Estados Unidos"
NEW_TEXT = "$7.500 en los Estados Unidos"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--backup-dir", default=None)
    args = ap.parse_args()

    root = Path(args.root)
    backup_dir = Path(args.backup_dir) if args.backup_dir else root.parent / "_ev_article_text_backup"

    path = root / "tools" / "es" / "ev-vs-gas.html"
    if not path.exists():
        print(f"找不到檔案: {path}")
        return

    original = path.read_bytes()
    html = original.decode("utf-8")

    if NEW_TEXT in html:
        print("已經是正確的$7.500,不用改")
        return
    if OLD_TEXT not in html:
        print("找不到預期的€7.500文字,可能內容已經不同,請人工確認,不自動修改")
        return

    count = html.count(OLD_TEXT)
    print(f"找到{count}處「{OLD_TEXT}」,將改為「{NEW_TEXT}」")

    if args.apply:
        new_html = html.replace(OLD_TEXT, NEW_TEXT)
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup_dir / "es_ev-vs-gas.html.bak")
        path.write_bytes(new_html.encode("utf-8"))
        print(f"已套用,備份至: {backup_dir}")
    else:
        print("DRY-RUN,尚未寫入")


if __name__ == "__main__":
    main()
