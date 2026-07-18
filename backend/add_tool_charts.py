#!/usr/bin/env python3
"""add_tool_charts.py — Inject tools-chart.js into all tool pages.
Adds <script src="/tools/tools-chart.js" defer></script> before </body>.
Skips files that already have it.

Usage:
  python add_tool_charts.py              # dry-run
  python add_tool_charts.py --execute    # real run
"""
import os, sys, glob, shutil

BASE = r"D:\xian-shang-you-wei\backend\frontend\tools"
SCRIPT_TAG = '<script src="/tools/tools-chart.js" defer></script>'
DRY = '--execute' not in sys.argv

def process():
    if DRY:
        print("=== DRY RUN (add --execute to apply) ===\n")

    # Collect all tool HTML files (zh-TW root + 9 lang subdirs)
    patterns = [
        os.path.join(BASE, "*.html"),           # zh-TW
        os.path.join(BASE, "*", "*.html"),       # en/, ja/, ko/, etc.
    ]
    files = []
    for p in patterns:
        files.extend(glob.glob(p))

    # Exclude index pages
    files = [f for f in files if os.path.basename(f) != 'index.html']
    files.sort()

    total = len(files)
    injected = 0
    skipped = 0
    errors = 0

    for fpath in files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                html = f.read()

            # Skip if already has tools-chart.js
            if 'tools-chart.js' in html:
                skipped += 1
                continue

            # Find </body> and insert before it
            marker = '</body>'
            idx = html.lower().rfind(marker.lower())
            if idx == -1:
                print(f"  ⚠ No </body> found: {fpath}")
                errors += 1
                continue

            new_html = html[:idx] + SCRIPT_TAG + '\n' + html[idx:]

            if not DRY:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_html)

            injected += 1
        except Exception as e:
            print(f"  ❌ Error: {fpath} — {e}")
            errors += 1

    print(f"\nTotal files: {total}")
    print(f"  Will inject: {injected}")
    print(f"  Already has (skip): {skipped}")
    print(f"  Errors: {errors}")

    if DRY and injected > 0:
        print(f"\n👉 Run: python add_tool_charts.py --execute")

if __name__ == '__main__':
    # Backup first
    if '--execute' in sys.argv:
        bk = BASE + '_backup_charts'
        if not os.path.exists(bk):
            print(f"Backing up {BASE} → {bk} ...")
            shutil.copytree(BASE, bk)
            print("Backup done.\n")
        else:
            print(f"Backup already exists: {bk}\n")

    process()
