# -*- coding: utf-8 -*-
"""
pt語言的2個「複雜」工具(employee-cost、car-insurance-estimate),因牽涉
稅制/保險市場,兩國規則差異大,這次先統一改回葡萄牙(€/pt-PT),
跟現有輸入框一致,不加下拉選單。

只做最單純的符號+locale修正:'R$' + X.toLocaleString('en-GB', ...)
→ '€' + X.toLocaleString('pt-PT', ...)

用法(先dry-run再apply):
  python fix_pt_complex_unify_portugal.py --root "D:\\xian-shang-you-wei\\backend\\frontend"
  python fix_pt_complex_unify_portugal.py --root "D:\\xian-shang-you-wei\\backend\\frontend" --apply
"""

import argparse
import re
import shutil
from pathlib import Path

TOOLS = ["employee-cost", "car-insurance-estimate"]

RS_ENGB_RE = re.compile(r"'R\$'(\s*\+\s*\w+\.toLocaleString\(')en-GB(')")


def process_file(path: Path, apply: bool, backup_dir: Path):
    original = path.read_bytes()
    html = original.decode("utf-8")

    matches = RS_ENGB_RE.findall(html)
    if not matches:
        return "no_rs_engb_pattern(可能已修正或結構不同,需人工確認)"

    new_html = RS_ENGB_RE.sub(r"'€'\1pt-PT\2", html)

    if apply:
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup_dir / path.name)
        path.write_bytes(new_html.encode("utf-8"))

    return f"ok({len(matches)}處改為€/pt-PT)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--backup-dir", default=None)
    args = ap.parse_args()

    root = Path(args.root)
    backup_dir = Path(args.backup_dir) if args.backup_dir else root.parent / "_pt_complex_unify_backup"

    for tool in TOOLS:
        path = root / "tools" / "pt" / f"{tool}.html"
        if not path.exists():
            print(f"[{tool}] 檔案不存在,跳過")
            continue
        result = process_file(path, args.apply, backup_dir)
        print(f"[{tool}] {result}")

    print(f"\n{'已套用' if args.apply else 'DRY-RUN,尚未寫入'}")
    if args.apply:
        print(f"已備份至: {backup_dir}")


if __name__ == "__main__":
    main()
