"""
main_picker.py — 一鍵執行：爬取 → 篩選 → 分析 → 輸出

用法：
  python main_picker.py

環境變數：
  FINMIND_TOKEN      必填
  ANTHROPIC_API_KEY  必填
"""

import os
import sys
from crawler import fetch_cnyes_news, fetch_stock_name
from finmind_filter import run_filter
from generator import run as generate_html


def main():
    # 環境變數檢查
    if not os.environ.get("FINMIND_TOKEN"):
        print("❌ 請設定 FINMIND_TOKEN")
        sys.exit(1)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ 請設定 ANTHROPIC_API_KEY")
        sys.exit(1)

    print("=" * 50)
    print("🔍 低基期選股生成器 啟動")
    print("=" * 50)

    # ── Step 1：抓鉅亨新聞，萃取候選代號 ──
    print("\n[Step 1] 爬取鉅亨 RSS 新聞...")
    news_list = fetch_cnyes_news(max_items=100)

    # 從新聞萃取所有出現過的股票代號
    all_codes = []
    for n in news_list:
        for c in n["codes"]:
            if c not in all_codes:
                all_codes.append(c)

    print(f"  → 共萃取到 {len(all_codes)} 個候選代號：{all_codes[:10]}{'...' if len(all_codes)>10 else ''}")

    if not all_codes:
        print("⚠️ 沒有從新聞中找到任何股票代號，流程結束")
        sys.exit(0)

    # ── Step 2：數值篩選 ──
    print(f"\n[Step 2] 數值篩選（回檔/法人/量能）...")
    filtered = run_filter(all_codes, news_list, max_results=20, delay=1.2)

    if not filtered:
        print("⚠️ 沒有股票通過篩選條件，流程結束")
        sys.exit(0)

    # 補上股票名稱
    print("\n[Step 2.5] 補充股票名稱...")
    for stock in filtered:
        stock["name"] = fetch_stock_name(stock["stock_id"])

    # ── Step 3：Claude 評分 + 輸出 HTML ──
    print(f"\n[Step 3] Claude API 分析 + 產出 HTML（共 {len(filtered)} 檔）...")
    output_path = generate_html(filtered, api_delay=2.0)

    print("\n" + "=" * 50)
    print(f"✅ 完成！輸出檔案：{output_path}")
    print(f"   同時更新：{output_path.replace(output_path.split('/')[-1], 'latest.html')}")
    print("=" * 50)


if __name__ == "__main__":
    if "--schedule" in sys.argv:
        # 排程模式：常駐背景，每日 14:35 自動跑
        from scheduler import main as schedule_main
        schedule_main()
    else:
        main()
