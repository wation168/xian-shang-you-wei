#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoftGlow 工具頁「相關工具」側邊欄修復腳本（全語言批次版）

背景：zh-TW 以外的 9 個語言目錄（de/en/es/fr/id/ja/ko/pt/zh-CN）下，
每個工具頁的側邊欄 <div class="related-card"><h3>...</h3></div> 是空的，
沒有任何連結；但頁面底部的「更多工具」tool-pill 區塊在每個語言都已經
正確產生（正確的 href 與正確翻譯的文字）。

這個腳本會：
  1. 走訪每個語言目錄下的所有 .html 檔案
  2. 只處理側邊欄是空的檔案（已經有連結的檔案會被安全跳過，不會被
     修改第二次 —— 可以放心重複執行這個腳本，不會造成任何損壞或
     重複寫入）
  3. 從同一個檔案底部「更多工具」區塊，取前 5 個 <a class="tool-pill">
     連結，複製一份放進側邊欄
  4. 完全不需要任何跨檔案查表或分類對照 —— 每個檔案的資料都來自它
     自己，所以不會有語系配對錯誤的風險

用法（在 Windows CMD 或 PowerShell，於 repo 根目錄 D:\\xian-shang-you-wei 執行）：

    python fix_sidebar_all_languages.py

預設會處理：
    backend\\frontend\\tools\\de
    backend\\frontend\\tools\\en
    backend\\frontend\\tools\\es
    backend\\frontend\\tools\\fr
    backend\\frontend\\tools\\id
    backend\\frontend\\tools\\ja
    backend\\frontend\\tools\\ko
    backend\\frontend\\tools\\pt
    backend\\frontend\\tools\\zh-CN

如果你的 repo 路徑不同，可以加參數指定根目錄：

    python fix_sidebar_all_languages.py --root "D:\\xian-shang-you-wei"

先預覽不寫入（dry-run，只印出會改哪些檔案，不實際修改）：

    python fix_sidebar_all_languages.py --dry-run

執行完會印出統計：
    fixed        = 實際被修好的檔案數
    already_ok   = 已經有連結、安全跳過的檔案數（例如你曾經手動測試過的
                   4 個 income-tax.html 就會落在這裡）
    no_card      = 這個檔案根本沒有側邊欄結構（例如 bazi-calculator.html
                   這類獨立手刻頁面），安全跳過
    no_pills     = 有側邊欄但找不到底部工具清單可複製，安全跳過（正常
                   情況下不應該出現，如果出現請檢查該檔案）

跑完之後，用 git diff 檢查改動範圍，再視需要 commit + push。
"""

import argparse
import glob
import json
import os
import re
import sys

LANGS = ["de", "en", "es", "fr", "id", "ja", "ko", "pt", "zh-CN"]

EMPTY_PATTERN = re.compile(r'(<div class="related-card"><h3>[^<]*</h3>)</div>')
PILL_PATTERN = re.compile(r'<a class="tool-pill" href="([^"]+)">([^<]+)</a>')


def fix_file(path, dry_run=False):
    with open(path, encoding="utf-8") as f:
        src = f.read()

    m = EMPTY_PATTERN.search(src)
    if not m:
        if 'class="related-card"' in src:
            return "already_ok"
        else:
            return "no_card"

    pills = PILL_PATTERN.findall(src)
    if not pills:
        return "no_pills"

    chosen = pills[:5]
    links_html = "".join(
        f'<a class="related-link" href="{href}">{text}</a>' for href, text in chosen
    )
    new_src = src[: m.start()] + m.group(1) + links_html + "</div>" + src[m.end():]

    # 安全檢查：確保這個檔案裡只有一個 related-card 區塊被處理到
    if new_src.count('class="related-card"') != 1:
        return "unexpected_structure"

    if not dry_run:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_src)

    return f"fixed:{len(chosen)}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--root",
        default=".",
        help="repo 根目錄（預設為目前目錄，即 D:\\xian-shang-you-wei）",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="只顯示會修改哪些檔案，不實際寫入",
    )
    args = ap.parse_args()

    tools_root = os.path.join(args.root, "backend", "frontend", "tools")
    if not os.path.isdir(tools_root):
        print(f"[錯誤] 找不到目錄：{tools_root}")
        print("請用 --root 指定正確的 repo 根目錄，例如：")
        print(r'  python fix_sidebar_all_languages.py --root "D:\xian-shang-you-wei"')
        sys.exit(1)

    summary = {}
    detail_fixed = []
    detail_unexpected = []

    for lang in LANGS:
        lang_dir = os.path.join(tools_root, lang)
        if not os.path.isdir(lang_dir):
            print(f"[跳過] 語言目錄不存在：{lang_dir}")
            continue

        html_files = sorted(glob.glob(os.path.join(lang_dir, "*.html")))
        for path in html_files:
            status = fix_file(path, dry_run=args.dry_run)
            key = status.split(":")[0]
            summary[key] = summary.get(key, 0) + 1
            if key == "fixed":
                detail_fixed.append(path)
            elif key == "unexpected_structure":
                detail_unexpected.append(path)

    print("\n=== 統計 ===")
    for k in ["fixed", "already_ok", "no_card", "no_pills", "unexpected_structure"]:
        if k in summary:
            print(f"  {k}: {summary[k]}")

    if args.dry_run:
        print("\n(dry-run 模式，沒有實際寫入任何檔案)")

    if detail_unexpected:
        print("\n[警告] 以下檔案結構異常，建議人工檢查（沒有被修改）：")
        for p in detail_unexpected:
            print(f"  {p}")

    print(f"\n共修好 {summary.get('fixed', 0)} 個檔案。")
    print("建議接下來執行：git status / git diff 確認改動範圍，再 commit + push。")


if __name__ == "__main__":
    main()
