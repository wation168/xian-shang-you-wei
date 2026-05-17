"""
scheduler.py — 每日盤後自動執行選股生成器

用法：
  python scheduler.py          ← 背景常駐，每日 14:30 自動跑
  python scheduler.py --now    ← 立刻執行一次（測試用）

依賴：無額外套件（使用 Python 內建 schedule 概念，純 time.sleep 實作）
"""

import os
import sys
import time
import logging
from datetime import datetime, date
from zoneinfo import ZoneInfo

# ── 設定 log ──
os.makedirs(os.path.join(os.path.dirname(__file__), "logs"), exist_ok=True)
log_path = os.path.join(os.path.dirname(__file__), "logs", "picker.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

TZ = ZoneInfo("Asia/Taipei")

# 每日執行時間（24小時制）
RUN_HOUR    = 14
RUN_MINUTE  = 35   # 14:35，確保盤後資料更新完畢
SCAN_HOUR   = 15
SCAN_MINUTE = 30   # 15:30，盤後全台掃描


def run_once():
    """執行一次完整選股流程"""
    logger.info("=" * 50)
    logger.info("🔍 選股生成器 開始執行")
    logger.info("=" * 50)
    try:
        # 動態 import，確保每次都重新載入最新狀態
        from crawler import fetch_cnyes_news, fetch_stock_name
        from finmind_filter import run_filter
        from generator import run as generate_html

        logger.info("[Step 1] 爬取鉅亨 RSS...")
        news_list = fetch_cnyes_news(max_items=100)
        all_codes = []
        for n in news_list:
            for c in n["codes"]:
                if c not in all_codes:
                    all_codes.append(c)
        logger.info(f"  → 取得 {len(news_list)} 則新聞，{len(all_codes)} 個候選代號")

        if not all_codes:
            logger.warning("沒有找到任何股票代號，跳過")
            return

        logger.info("[Step 2] 數值篩選...")
        filtered = run_filter(all_codes, news_list, max_results=20, delay=1.2)

        if not filtered:
            logger.warning("沒有股票通過篩選，跳過 HTML 產出")
            return

        logger.info("[Step 2.5] 補充股票名稱...")
        for stock in filtered:
            stock["name"] = fetch_stock_name(stock["stock_id"])

        logger.info(f"[Step 3] Claude 分析 {len(filtered)} 檔...")
        output_path = generate_html(filtered, api_delay=2.0)
        logger.info(f"✅ 完成：{output_path}")

    except Exception as e:
        logger.error(f"❌ 執行失敗：{e}", exc_info=True)


def is_trading_day(d: date) -> bool:
    """簡單判斷是否為交易日（週一~五，不含國定假日）"""
    # 只排週末，國定假日需要自行維護或查 API
    return d.weekday() < 5


def main():
    # --now 參數：立刻執行一次
    if "--now" in sys.argv:
        run_once()
        return

    logger.info(f"🕐 排程器啟動，選股 {RUN_HOUR:02d}:{RUN_MINUTE:02d}、全台掃描 {SCAN_HOUR:02d}:{SCAN_MINUTE:02d}（台北時間）")
    logger.info("   按 Ctrl+C 停止")

    last_run_date  = None
    last_scan_date = None

    while True:
        now = datetime.now(TZ)
        today = now.date()

        # 選股 14:35
        if (now.hour == RUN_HOUR and now.minute == RUN_MINUTE
                and is_trading_day(today)
                and last_run_date != today):
            last_run_date = today
            run_once()

        # 全台掃描 15:30
        if (now.hour == SCAN_HOUR and now.minute == SCAN_MINUTE
                and is_trading_day(today)
                and last_scan_date != today):
            last_scan_date = today
            logger.info("=" * 50)
            logger.info("📡 全台股掃描 開始執行")
            logger.info("=" * 50)
            try:
                from main_picker import run_full_scan
                run_full_scan()
                logger.info("✅ 全台股掃描完成")
            except Exception as e:
                logger.error(f"❌ 全台股掃描失敗：{e}", exc_info=True)

        # 每 30 秒檢查一次
        time.sleep(30)


if __name__ == "__main__":
    main()
