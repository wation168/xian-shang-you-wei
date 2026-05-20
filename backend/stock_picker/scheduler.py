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
UNIFIED_HOUR   = 16
UNIFIED_MINUTE = 30   # 16:30，確保收盤後 FinMind 資料同步完畢


def run_once():
    """執行一次統合選股流程（全台掃描 + 新聞選股）"""
    logger.info("=" * 50)
    logger.info("🔍 統合選股 開始執行")
    logger.info("=" * 50)
    try:
        from main_picker import run_unified_scan
        run_unified_scan()
        logger.info("✅ 統合選股完成")
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

    last_run_date = None

    while True:
        now = datetime.now(TZ)
        today = now.date()

        # 統合選股 15:30
        if (now.hour == UNIFIED_HOUR and now.minute == UNIFIED_MINUTE
                and is_trading_day(today)
                and last_run_date != today):
            last_run_date = today
            run_once()

        # 每 30 秒檢查一次
        time.sleep(30)


if __name__ == "__main__":
    main()
