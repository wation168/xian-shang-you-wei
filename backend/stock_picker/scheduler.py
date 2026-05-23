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

def is_trading_day(d: date) -> bool:
    """簡單判斷是否為交易日（週一~五，不含國定假日）"""
    # 只排週末，國定假日需要自行維護或查 API
    return d.weekday() < 5


def main():
    logger.info("🕐 排程器啟動（台北時間）")
    logger.info("   按 Ctrl+C 停止")

    while True:
        # 每 30 秒檢查一次（目前無排程任務）
        time.sleep(30)


if __name__ == "__main__":
    main()
