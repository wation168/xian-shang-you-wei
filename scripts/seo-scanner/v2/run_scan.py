#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoftGlow 本機 SEO Scanner v2 — 單一 CLI 入口。

用法（Windows 路徑友善）：
    python run_scan.py --root "D:/path/to/lottery" --site-name "樂透站" --out dashboard.html
    python run_scan.py --root "D:/path/to/tools" --lang zh-TW --out dashboard_tools.html
    python run_scan.py --root ... --gsc-csv optional.csv --out ...

不連網；只掃本機靜態 HTML。
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

# 確保套件可 import（從專案根執行）
sys.path.insert(0, str(Path(__file__).resolve().parent))

from seo_scanner.parse import scan_root
from seo_scanner.diagnose import run_all_checks
from seo_scanner.report import render_dashboard


def load_gsc_csv(path: Path) -> dict[str, int]:
    """讀 GSC 匯出 CSV，回傳 url/path 片段 → impressions。"""
    result: dict[str, int] = {}
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    reader = csv.DictReader(text.splitlines())
    if not reader.fieldnames:
        return result

    # 找 Page / 網頁 與 Impressions / 曝光
    fields = {f.lower().strip(): f for f in reader.fieldnames}
    page_col = None
    imp_col = None
    for key, orig in fields.items():
        if key in ("page", "網頁", "url", "landing page", "top pages"):
            page_col = orig
        if key in ("impressions", "曝光", "impression"):
            imp_col = orig
    if not page_col:
        # 模糊
        for key, orig in fields.items():
            if "page" in key or "url" in key or "網頁" in key:
                page_col = orig
                break
    if not imp_col:
        for key, orig in fields.items():
            if "impr" in key or "曝光" in key:
                imp_col = orig
                break
    if not page_col or not imp_col:
        print("警告：GSC CSV 找不到 Page/Impressions 欄，略過。", file=sys.stderr)
        return result

    for row in reader:
        url = (row.get(page_col) or "").strip()
        try:
            imp = int(float(row.get(imp_col) or 0))
        except ValueError:
            imp = 0
        if not url:
            continue
        # 存完整 URL 與 path leaf
        result[url] = imp
        leaf = url.rstrip("/").split("/")[-1]
        if leaf.endswith(".html"):
            leaf = leaf[:-5]
        result[leaf] = min(result.get(leaf, imp), imp) if leaf in result else imp
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="SoftGlow 本機 SEO Scanner v2（靜態 HTML，不連網）"
    )
    parser.add_argument(
        "--root",
        required=True,
        help="本機 HTML 根目錄（Windows 可用 D:/... 或 D:\\\\...）",
    )
    parser.add_argument("--site-name", default="SEO 站", help="報告標題用站名")
    parser.add_argument("--out", default="dashboard.html", help="輸出 HTML 路徑")
    parser.add_argument(
        "--lang",
        default=None,
        help="只掃某語言子資料夾（如 zh-TW、en），加速",
    )
    parser.add_argument(
        "--gsc-csv",
        default=None,
        help="可選：Search Console 匯出 CSV（含 Page 與 Impressions）",
    )
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not root.is_dir():
        print("錯誤：根目錄不存在：%s" % root, file=sys.stderr)
        return 1

    t0 = time.perf_counter()
    print("掃描中：%s ..." % root)
    pages = scan_root(root, lang_filter=args.lang)
    print("  擷取 %d 頁" % len(pages))

    gsc = None
    if args.gsc_csv:
        gsc_path = Path(args.gsc_csv)
        if gsc_path.is_file():
            gsc = load_gsc_csv(gsc_path)
            print("  載入 GSC 列數（鍵）：%d" % len(gsc))
        else:
            print("警告：找不到 GSC CSV：%s" % gsc_path, file=sys.stderr)

    issues, sim_pairs, summary = run_all_checks(pages, gsc_impressions=gsc)
    html = render_dashboard(pages, issues, sim_pairs, summary, site_name=args.site_name)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")

    elapsed = time.perf_counter() - t0
    pc = summary["priority_counts"]
    print("--- 摘要 ---")
    print("站名：%s" % args.site_name)
    print("頁數：%d" % summary["page_count"])
    print(
        "優先序：P0=%d  P1=%d  P2=%d  P3=%d"
        % (pc["P0"], pc["P1"], pc["P2"], pc["P3"])
    )
    print("問題總數：%d" % summary["issue_count"])
    print("相似度配對：%d" % len(sim_pairs))
    cs = summary.get("cluster_summary") or {}
    print(
        "相似 Cluster：總=%d  待處理=%d  已摺疊=%d"
        % (
            cs.get("cluster_count", 0),
            cs.get("actionable_cluster_count", 0),
            cs.get("folded_cluster_count", 0),
        )
    )
    for t in (cs.get("actionable_titles") or [])[:8]:
        print("  · %s" % t)
    ls = summary.get("link_opportunity_summary") or {}
    bc = ls.get("bucket_counts") or {}
    print(
        "內連 pairwise：%d  → Opportunity：總=%d  高價值=%d  摺疊=%d"
        % (
            summary.get("link_pair_count", 0),
            ls.get("opportunity_count", 0),
            ls.get("high_value_count", 0),
            ls.get("folded_count", 0),
        )
    )
    print(
        "  bucket：template=%d topic=%d strong_pair=%d hub=%d folded=%d"
        % (
            bc.get("template", 0),
            bc.get("topic", 0),
            bc.get("strong_pair", 0),
            bc.get("hub", 0),
            bc.get("folded", 0),
        )
    )
    for t in (ls.get("high_value_titles") or [])[:8]:
        print("  · %s" % t)
    print("耗時：%.2f 秒" % elapsed)
    print("報告：%s" % out.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
