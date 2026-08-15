"""
⚠️⚠️⚠️ 2026/08/15：這個檔案已經廢棄，不要再用！⚠️⚠️⚠️

原因：
1. 這個檔案原本在下面直接寫死一組真實的Channel Secret/Channel Access Token，
   已經被移除改成讀環境變數——但只要這個檔案曾經被git commit過（很可能已經commit了，
   建立日期是2026/05/07），那組真實金鑰就已經留在git歷史紀錄裡，不會因為這次改成
   讀環境變數就消失。**強烈建議帥哥鴻立刻去LINE Developers Console把當初申請這組
   Channel Secret/Access Token的channel直接刪除或重新產生token，視同這組金鑰已外洩。**
2. 這個檔案設計成獨立的Flask app（要另外用`python line_bot.py`啟動、監聽5000port），
   從來沒有真正部署上線過（`API_BASE`還寫死`http://localhost:8000`）。
3. 同樣的LINE Bot功能已經在2026/08/15第二十五輪重新設計、整合進正式運行的
   `backend/main.py`裡（新路由`POST /webhook/line-bot`），跟main.py同一個FastAPI
   process執行、不用另外啟動一個Flask服務、直接呼叫既有`_do_analyze()`分析引擎，
   不會有這個舊檔案裡格式化邏輯欄位對不上目前main.py分析結果的問題。

這個檔案保留只是為了不憑空刪掉帥哥鴻的東西，之後確認main.py那邊運作正常後，
可以考慮直接刪除這個檔案。

線上有位 LINE Bot（舊版原型，已廢棄）
"""

from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi,
    ReplyMessageRequest, TextMessage, FlexMessage, FlexContainer
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import requests
import json
import os

app = Flask(__name__)

# ── 設定區 ──────────────────────────────────────────────
# 2026/08/15：原本這裡寫死真實金鑰，已改成讀環境變數並清空——但這不代表舊金鑰
# 安全了，git歷史裡舊版本還留著，請務必去LINE Developers Console revoke掉。
CHANNEL_SECRET       = os.environ.get("LINE_BOT_CHANNEL_SECRET", "")
CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_BOT_CHANNEL_ACCESS_TOKEN", "")
API_BASE             = os.environ.get("BACKEND_URL", "http://localhost:8000")
# ──────────────────────────────────────────────────────

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler       = WebhookHandler(CHANNEL_SECRET)


def analyze_stock(stock_id: str, tf: str = "D") -> dict | None:
    """呼叫後端分析 API"""
    try:
        url  = f"{API_BASE}/api/analyze/{stock_id}?tf={tf}"
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"API 錯誤: {e}")
    return None


def format_message(data: dict) -> str:
    """格式化分析結果為 LINE 訊息"""
    stock_id   = data.get("stock_id", "")
    stock_name = data.get("stock_name", "")
    price      = data.get("price", 0)
    support    = data.get("support", 0)
    resistance = data.get("resistance", 0)
    trend      = data.get("trend", "")
    pattern    = data.get("pattern", "")
    stop_loss  = data.get("stop_loss", 0)
    target1    = data.get("target1", 0)
    rr         = data.get("risk_reward", 0)
    risk_label = data.get("risk_label", "")
    warning    = data.get("warning", "")
    channel    = data.get("channel", {})
    support_desc = data.get("support_desc", "")

    # 風險等級 emoji
    risk_emoji = {"high":"🔴","medium":"🟡","low":"🟢","watch":"⚪"}.get(
        data.get("risk_level","watch"), "⚪")

    # 損益比評語
    if rr >= 2:   rr_comment = "✅ 報酬大於風險"
    elif rr >= 1: rr_comment = "⚡ 風險報酬尚可"
    else:         rr_comment = "⚠️ 風險大於報酬"

    # 軌道資訊
    ch_desc = ""
    if channel:
        ch_desc = f"\n📐 軌道：{channel.get('desc','')}"
        ch_desc += f"\n　　{channel.get('position_desc','')}"

    msg = f"""📊 {stock_id} {stock_name}
{'─'*20}
💰 現價：{price}
{risk_emoji} 風險等級：{risk_label}
📈 趨勢：{trend}
🔷 型態：{pattern}
{'─'*20}
🟢 支撐：{support}
　　{support_desc}
🔴 壓力：{resistance}
{'─'*20}
🛡️ 防守位：{stop_loss}（{((stop_loss-price)/price*100):.1f}%）
🎯 目標1：{target1}（+{((target1-price)/price*100):.1f}%）
📊 風險報酬：{rr} {rr_comment}{ch_desc}
{'─'*20}
⚡ {warning}
{'─'*20}
*僅供參考，不構成投資建議*"""

    return msg


def parse_command(text: str):
    """
    解析使用者輸入
    支援格式：
    - 2330        → 日K分析
    - 2330 週     → 週K分析
    - 2330W       → 週K分析
    - 2330M       → 月K分析
    - /help       → 說明
    """
    text = text.strip().upper()

    if text in ["/HELP", "HELP", "說明", "?"]:
        return "help", None, None

    # 判斷時間框架
    tf = "D"
    if text.endswith("W") or "週" in text or "周" in text:
        tf = "W"
        text = text.replace("W","").replace("週","").replace("周","").strip()
    elif text.endswith("M") or "月" in text:
        tf = "M"
        text = text.replace("M","").replace("月","").strip()

    # 提取股票代號（4~5位數字）
    import re
    match = re.search(r'\d{4,5}', text)
    if match:
        stock_id = match.group()
        return "analyze", stock_id, tf

    return "unknown", None, None


HELP_MSG = """📊 線上有位 使用說明
{'─'*20}
輸入股票代號即可分析：

🔹 日K分析：
　2330

🔹 週K分析：
　2330W 或 2330週

🔹 月K分析：
　2330M 或 2330月

📌 範例：
　2330　　→ 台積電日K
　2317W　→ 鴻海週K
　2454M　→ 聯發科月K

⚠️ 本工具僅供技術分析參考
　不構成任何投資建議"""


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body      = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text    = event.message.text.strip()
    user_id = event.source.user_id

    action, stock_id, tf = parse_command(text)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if action == "help":
            reply = HELP_MSG
        elif action == "analyze" and stock_id:
            # 先回一個等待訊息
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=f"⏳ 分析 {stock_id} 中，請稍候...")]
                )
            )
            # 分析
            data = analyze_stock(stock_id, tf)
            if data:
                reply = format_message(data)
            else:
                reply = f"❌ 找不到股票代號：{stock_id}\n請確認代號是否正確（例：2330）"

            # 用 push 發送結果（因為 reply token 已用掉）
            line_bot_api.push_message(
                to=event.source.user_id if hasattr(event.source,'user_id') else event.source.group_id,
                messages=[TextMessage(text=reply)]
            )
            return
        else:
            reply = "請輸入股票代號（例：2330）\n輸入 /help 查看使用說明"

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply)]
            )
        )


if __name__ == "__main__":
    print("✅ 線上有位 LINE Bot 啟動中...")
    print(f"   後端 API: {API_BASE}")
    print(f"   Webhook URL 設定為: https://你的網域/callback")
    app.run(host="0.0.0.0", port=5000, debug=False)
