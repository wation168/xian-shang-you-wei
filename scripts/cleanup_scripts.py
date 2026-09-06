#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cleanup_scripts.py — 清理 scripts/ 及專案根目錄殘留檔案
用法：
  cd D:\\xian-shang-you-wei\\scripts
  python cleanup_scripts.py            # dry-run，只列出會刪什麼，不真的刪
  python cleanup_scripts.py --apply    # 真的刪除（.bak類直接刪；一次性腳本移到 _archive/ 資料夾，不直接刪）
"""
import os, sys, glob, shutil, codecs
if hasattr(sys.stdout, 'buffer'):
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, errors='replace')

BASE = r"D:\xian-shang-you-wei"
ARCHIVE_DIR = os.path.join(BASE, "scripts", "_archive_20260809")

# A類：.bak備份檔，直接刪除（git歷史可復原，不需要這些散落副本）
BAK_PATTERNS = [
    r"backend\**\*.bak_*",
    r"backend\*.bak_*",
    r"backend\main.py.bak*",
]

# B類：一次性腳本，任務已完成，移到 _archive 資料夾（不直接刪，保留但歸檔）
B_CATEGORY_SCRIPTS = [
    "_fix_hsa_de.py","_fix_hsa_es.py","_fix_hsa_fr.py","_fix_hsa_id.py",
    "_fix_hsa_ja.py","_fix_hsa_ko.py","_fix_hsa_pt.py","_fix_hsa_root.py","_fix_hsa_zhcn.py",
    "_fix_roth_de.py","_fix_roth_en.py","_fix_roth_es.py","_fix_roth_fr.py","_fix_roth_id.py",
    "_fix_roth_ja.py","_fix_roth_ko.py","_fix_roth_pt.py","_fix_roth_root.py","_fix_roth_zhcn.py",
    "apply_meta_fixes.py","fix_legal_footer_links.py","fix_moving_average_desc.py",
    "deploy_fixed_langs.py","extract_meta.py",
    "backtest_combo.py","backtest_defense_ma5_bias.py","backtest_dip.py","backtest_dip2.py",
    "backtest_ma5_10_gate.py","backtest_ma5_10_trail.py","backtest_rr_trend_adjust.py",
    "backtest_short.py","backtest_trend.py","backtest_trend_ma5cross.py",
    "diagnose_dow_trend.py","test_dow_trend_ma_buffer_compare.py","test_dow_trend_ma_correction.py",
]

# 舊的部署前備份資料夾（4個），移到archive
B_CATEGORY_DIRS = [
    "_backup_before_deploy_20260807_094953",
    "_backup_before_deploy_20260807_125859",
    "_backup_before_deploy_20260807_132916",
    "_backup_before_deploy_20260807_135809",
]

# C類：不動，明確保留（會重複使用的掃描工具/報告/量測系統素材）
KEEP_LIST = [
    "scan_locale_mismatch.py","scan_outdated_content.py",
    "outdated_content_report.csv","locale_mismatch_report.csv",
    "fix_currency_batch.py","cleanup_scripts.py",
]

def find_bak_files():
    result = []
    for root, dirs, files in os.walk(os.path.join(BASE, "backend")):
        for f in files:
            if ".bak" in f or ".bak_" in f:
                result.append(os.path.join(root, f))
    return result

def main():
    apply = "--apply" in sys.argv
    scripts_dir = os.path.join(BASE, "scripts")

    print("=== A類：.bak備份檔（將直接刪除） ===")
    bak_files = find_bak_files()
    for f in bak_files:
        print(f"  [{'將刪除' if not apply else '已刪除'}] {f}")
    print(f"共 {len(bak_files)} 個 .bak 檔案\n")

    print("=== B類：一次性腳本（將移到 _archive_20260809/ 歸檔，不直接刪） ===")
    b_found = []
    for name in B_CATEGORY_SCRIPTS:
        path = os.path.join(scripts_dir, name)
        if os.path.exists(path):
            b_found.append(path)
            print(f"  [{'將歸檔' if not apply else '已歸檔'}] {name}")
    for dname in B_CATEGORY_DIRS:
        path = os.path.join(scripts_dir, dname)
        if os.path.isdir(path):
            b_found.append(path)
            print(f"  [{'將歸檔' if not apply else '已歸檔'}] {dname}/ (資料夾)")
    print(f"共 {len(b_found)} 項\n")

    print("=== C類：明確保留，不動 ===")
    for name in KEEP_LIST:
        print(f"  [保留] {name}")
    print()

    if not apply:
        print("=== 這是 DRY-RUN，尚未真的刪除/移動任何檔案 ===")
        print("確認上面清單沒問題後，執行： python cleanup_scripts.py --apply")
        return

    # 真的執行
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    for f in bak_files:
        try:
            os.remove(f)
        except Exception as e:
            print(f"[錯誤] 刪除失敗 {f}: {e}")

    for path in b_found:
        try:
            dest = os.path.join(ARCHIVE_DIR, os.path.basename(path))
            shutil.move(path, dest)
        except Exception as e:
            print(f"[錯誤] 歸檔失敗 {path}: {e}")

    print(f"\n完成。.bak檔案已刪除，一次性腳本已移至 {ARCHIVE_DIR}")

if __name__ == "__main__":
    main()
