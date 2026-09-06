# -*- coding: utf-8 -*-
"""
修正 zh-TW/position-size.html:用 .toFixed(2) 格式,不是 .toLocaleString('en-US'),
跟主批次腳本的規則不同,這支專門處理這一個檔案。

'$' + X.toFixed(2)  →  'NT$' + X.toFixed(2)

用法:
  python fix_position_size_zhtw.py --root "D:\\xian-shang-you-wei\\backend\\frontend"
  python fix_position_size_zhtw.py --root "D:\\xian-shang-you-wei\\backend\\frontend" --apply
"""

import argparse
import re
import shutil
from pathlib import Path

DOLLAR_TOFIXED_RE = re.compile(r"'\$'\s*\+\s*(\w+)\.toFixed\(2\)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--backup-dir", default=None)
    args = ap.parse_args()

    root = Path(args.root)
    backup_dir = Path(args.backup_dir) if args.backup_dir else root.parent / "_position_size_backup"
    path = root / "tools" / "position-size.html"

    if not path.exists():
        print(f"找不到檔案: {path}")
        return

    html = path.read_bytes().decode("utf-8")
    matches = DOLLAR_TOFIXED_RE.findall(html)
    if not matches:
        print("找不到預期的'$' + X.toFixed(2)格式,可能已修正或結構不同,需人工確認")
        return

    print(f"找到{len(matches)}處,將改為 'NT$' + X.toFixed(2)")
    new_html = DOLLAR_TOFIXED_RE.sub(r"'NT$' + \1.toFixed(2)", html)

    if args.apply:
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup_dir / "position-size.html.bak")
        path.write_bytes(new_html.encode("utf-8"))
        print(f"已套用,備份至: {backup_dir}")
    else:
        print("DRY-RUN,尚未寫入")


if __name__ == "__main__":
    main()
