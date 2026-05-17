"""
generator.py — 產出層
1. 對每檔通過篩選的股票，呼叫 Claude API 給分 + 說明
2. 組合成 HTML 卡片頁面，寫入 output/stock_picks_YYYYMMDD.html
"""

import os
import json
import time
import urllib.request
from datetime import datetime


ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


# ──────────────────────────────────────────
# Claude API 呼叫
# ──────────────────────────────────────────
def claude_evaluate(stock: dict) -> dict:
    """
    呼叫 Claude API 對單一股票評分 + 生成說明
    回傳 {score: 0~100, reason: str, watch_point: str, risk: str}
    """
    factors = "\n".join(f"- {f}" for f in stock["score_factors"])
    news_text = ""
    if stock["news"]:
        news_text = "\n最近相關新聞：\n" + "\n".join(
            f"- {n['title']}" for n in stock["news"][:3]
        )

    prompt = f"""你是台股技術面與籌碼面分析師。
以下是一檔台股的客觀數據，這檔股票是透過以下三個條件篩選出來的：
1. 鉅亨近期有題材新聞（有故事）
2. 法人連續買超（籌碼回流）
3. 成交量明顯放大（量先價行跡象）

股票代號：{stock['stock_id']}
現價：{stock['price']}
量化指標：
{factors}
{news_text}

請以 JSON 格式回答，不要輸出任何其他文字：
{{
  "score": <整數 0~100，綜合題材、籌碼、量能給出關注分數>,
  "reason": "<50字以內，說明為何值得關注，強調籌碼回流＋量能放大的共振情況>",
  "watch_point": "<30字以內，具體說明何時適合進一步追蹤或等待的訊號>",
  "risk": "<30字以內，最主要的一個風險點>"
}}

評分參考：
- 90+：題材、籌碼、量能三者明確共振，強力關注
- 70~89：兩項以上條件良好，值得追蹤
- 50~69：條件初現，需觀察量能是否持續
- 50以下：條件薄弱，暫不關注"""

    headers = {
        "Content-Type": "application/json",
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
    }
    body = json.dumps({
        "model": "claude-sonnet-4-5",
        "max_tokens": 400,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()

    try:
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())

        text = data["content"][0]["text"].strip()
        # 移除可能的 markdown code fence
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())

    except Exception as e:
        print(f"[generator] Claude API 失敗 {stock['stock_id']}：{e}")
        return {
            "score": 0,
            "reason": "分析暫時無法取得",
            "watch_point": "—",
            "risk": "—",
        }


# ──────────────────────────────────────────
# HTML 產出
# ──────────────────────────────────────────
def score_color(score: int) -> str:
    if score >= 80: return "#22c55e"   # 綠
    if score >= 60: return "#f59e0b"   # 橘
    return "#94a3b8"                   # 灰


def score_label(score: int) -> str:
    if score >= 90: return "強力關注"
    if score >= 70: return "值得追蹤"
    if score >= 50: return "觀察中"
    return "暫不關注"


def render_card(stock: dict, eval_result: dict) -> str:
    s = stock
    e = eval_result
    score       = e.get("score", 0)
    color       = score_color(score)
    label       = score_label(score)
    signal      = s.get("signal_label", "")
    is_risk     = s.get("is_risk", False)

    inst_dir   = "買超" if s["inst_5d_total"] > 0 else ("賣超" if s["inst_5d_total"] < 0 else "持平")
    inst_color = "#22c55e" if s["inst_5d_total"] > 0 else ("#ef4444" if s["inst_5d_total"] < 0 else "#94a3b8")
    vol_color  = "#22c55e" if s["vol_ratio"] >= 1.5 else "#f59e0b" if s["vol_ratio"] >= 1.2 else "#94a3b8"
    vol_label  = "量大增" if s["vol_ratio"] >= 1.5 else "量增" if s["vol_ratio"] >= 1.2 else "量平"

    # 型態標籤 badge
    signal_badge = ""
    if signal:
        if "死叉" in signal or "空" in signal:
            sig_bg, sig_fg = "#7f1d1d", "#fca5a5"
        else:
            sig_bg, sig_fg = "#14532d", "#86efac"
        signal_badge = (
            f'<span style="font-size:10px;padding:2px 10px;border-radius:20px;'
            f'background:{sig_bg};color:{sig_fg};font-weight:700">{signal}</span>'
        )

    # 題材關鍵字 badges
    kws = list({kw for n in s["news"] for kw in n["keywords"]})[:4]
    kw_badges = "".join(
        f'<span style="font-size:10px;padding:2px 8px;border-radius:20px;'
        f'background:#7c3aed22;color:#a78bfa">{k}</span>'
        for k in kws
    )

    # 新聞連結
    news_html = ""
    for n in s["news"][:2]:
        news_html += (
            f'<a href="{n["link"]}" target="_blank" style="display:block;font-size:11px;'
            f'color:#94a3b8;text-decoration:none;padding:4px 0;border-top:1px solid #1e293b;'
            f'line-height:1.4" onmouseover="this.style.color=\'#e2e8f0\'"'
            f' onmouseout="this.style.color=\'#94a3b8\'">'
            f'{n["title"][:50]}{"…" if len(n["title"])>50 else ""}'
            f'</a>'
        )

    # 卡片邊框：風險警示用紅色
    card_border = "#7f1d1d" if is_risk else "#1e293b"
    card_bg     = "#1a0a0a" if is_risk else "#0f172a"

    # 法人顯示（風險警示無法人資料時不顯示）
    inst_badge = (
        f'<span style="font-size:10px;padding:2px 8px;border-radius:20px;'
        f'background:#1e293b;color:{inst_color}">法人連{inst_dir} {s["consecutive_buy_days"]}日</span>'
    ) if not is_risk else ""

    return f"""
<div style="background:{card_bg};border:1px solid {card_border};border-radius:16px;padding:20px;
     display:flex;flex-direction:column;gap:12px;position:relative;overflow:hidden">

  <!-- 評分圓圈 -->
  <div style="position:absolute;top:16px;right:16px;width:52px;height:52px;border-radius:50%;
       background:conic-gradient({color} {score * 3.6}deg, #1e293b 0deg);
       display:flex;align-items:center;justify-content:center">
    <div style="width:40px;height:40px;border-radius:50%;background:{card_bg};
         display:flex;align-items:center;justify-content:center;
         font-size:13px;font-weight:700;color:{color}">{score}</div>
  </div>

  <!-- 標頭 -->
  <div style="padding-right:60px">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
      <span style="font-size:17px;font-weight:700;color:#f1f5f9">{s['stock_id']}</span>
      <span style="font-size:13px;color:#64748b">{s.get('name', '')}</span>
    </div>
    <div style="display:flex;gap:6px;flex-wrap:wrap">
      {signal_badge}
      <span style="font-size:10px;padding:2px 8px;border-radius:20px;
            background:{color}22;color:{color};font-weight:600">{label}</span>
      <span style="font-size:10px;padding:2px 8px;border-radius:20px;
            background:#1e293b;color:{vol_color}">📊 {vol_label} {s['vol_ratio']}x</span>
      {inst_badge}
      {kw_badges}
    </div>
  </div>

  <!-- 數據列 -->
  <div style="display:flex;gap:16px;font-size:12px;color:#64748b;flex-wrap:wrap">
    <span>現價 <strong style="color:#f1f5f9;font-size:15px">{s['price']}</strong></span>
    <span>近5日均量 <strong style="color:#94a3b8">{s['avg_vol_5']:,}</strong> 張</span>
    {f'<span>法人近5日 <strong style="color:{inst_color}">{s["inst_5d_total"]:+,}</strong> 張</span>' if not is_risk else ''}
    {f'<span>近20日 <strong style="color:{inst_color}">{s["inst_20d_total"]:+,}</strong> 張</span>' if not is_risk else ''}
  </div>

  <!-- Claude 分析 -->
  <div style="background:#1e293b;border-radius:10px;padding:12px;font-size:12px;line-height:1.6">
    <div style="color:#e2e8f0;margin-bottom:8px">{e.get('reason','')}</div>
    <div style="display:flex;flex-direction:column;gap:4px">
      <div><span style="color:#22c55e;font-weight:600">📍 觀察重點：</span>
           <span style="color:#94a3b8">{e.get('watch_point','')}</span></div>
      <div><span style="color:#f59e0b;font-weight:600">⚠️ 風險：</span>
           <span style="color:#94a3b8">{e.get('risk','')}</span></div>
    </div>
  </div>

  <!-- 相關新聞 -->
  {f'<div style="margin-top:-4px">{news_html}</div>' if news_html else ''}
</div>"""


def render_page(stocks_with_eval: list[tuple[dict, dict]], generated_at: str) -> str:
    """組合完整 HTML 頁面（做多候選 + 風險警示兩區塊）"""
    # 分離做多候選與風險警示
    long_items = [(s, e) for s, e in stocks_with_eval if not s.get("is_risk")]
    risk_items = [(s, e) for s, e in stocks_with_eval if s.get("is_risk")]

    # 各自依分數排序
    long_items = sorted(long_items, key=lambda x: x[1].get("score", 0), reverse=True)
    risk_items = sorted(risk_items, key=lambda x: x[1].get("score", 0), reverse=True)

    long_count = len(long_items)
    risk_count = len(risk_items)
    high_count = sum(1 for _, e in long_items if e.get("score", 0) >= 70)

    long_cards = "\n".join(render_card(s, e) for s, e in long_items)
    risk_cards = "\n".join(render_card(s, e) for s, e in risk_items)

    # 風險區塊 HTML（有死叉才顯示）
    risk_section = ""
    if risk_items:
        risk_section = f"""
  <div style="margin-top:40px">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
      <h2 style="font-size:18px;font-weight:700;color:#fca5a5">⚠️ 風險警示</h2>
      <span style="font-size:12px;color:#94a3b8">以下個股出現死叉型態，有題材但需注意下跌風險</span>
    </div>
    <div style="background:#7f1d1d22;border:1px solid #7f1d1d;border-radius:10px;
         padding:12px 16px;font-size:12px;color:#fca5a5;margin-bottom:16px;line-height:1.6">
      ⚠️ 以下股票雖有新聞題材，但均線出現死亡交叉（MA20 下穿 MA60），
      短期趨勢偏空，不建議追買，可列入空方觀察或等待止跌訊號。
    </div>
    <div class="grid">
      {risk_cards}
    </div>
  </div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>選股名單 — {generated_at[:10]}</title>
<style>
* {{ box-sizing:border-box; margin:0; padding:0 }}
body {{ background:#020817; color:#f1f5f9; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
       min-height:100vh; padding:24px 16px 48px }}
.container {{ max-width:960px; margin:0 auto }}
.header {{ margin-bottom:28px }}
.header h1 {{ font-size:22px; font-weight:700; margin-bottom:6px }}
.header p  {{ font-size:13px; color:#64748b; line-height:1.6 }}
.stats {{ display:flex; gap:12px; flex-wrap:wrap; margin-bottom:20px }}
.stat {{ background:#0f172a; border:1px solid #1e293b; border-radius:10px;
         padding:10px 16px; font-size:12px; color:#64748b }}
.stat strong {{ display:block; font-size:18px; font-weight:700; color:#f1f5f9; margin-bottom:2px }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(300px, 1fr)); gap:16px }}
.disclaimer {{ margin-top:32px; padding:16px; background:#0f172a; border-radius:10px;
               font-size:11px; color:#475569; line-height:1.7 }}
@media(max-width:600px){{ .grid{{ grid-template-columns:1fr }} }}
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <h1>🔍 選股名單</h1>
    <p>產生時間：{generated_at}　｜　篩選條件：有題材新聞 ＋ 型態偵測 ＋ 量能確認　｜　由 Claude AI 評分</p>
  </div>

  <div class="stats">
    <div class="stat"><strong>{long_count}</strong>檔做多候選</div>
    <div class="stat"><strong>{high_count}</strong>檔評分 70+</div>
    <div class="stat"><strong style="color:#fca5a5">{risk_count}</strong>檔風險警示</div>
    <div class="stat"><strong style="color:#22c55e">●</strong>盤後資料</div>
  </div>

  <!-- 做多候選 -->
  {f'<div style="margin-bottom:12px"><h2 style="font-size:18px;font-weight:700;color:#86efac;margin-bottom:16px">📈 做多候選</h2><div class="grid">{long_cards}</div></div>' if long_items else '<div style="padding:32px 0;text-align:center;color:#475569">今日無做多候選股票</div>'}

  {risk_section}

  <div class="disclaimer">
    ⚠️ 本頁面資料僅供參考，不構成買賣建議。股市有風險，請自行評估後決策。
    所有分析結果均為系統自動產出，實際走勢以市場為準。
  </div>

</div>
</body>
</html>"""


# ──────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────
def run(filtered_stocks: list[dict], api_delay: float = 2.0) -> str:
    """
    主函式：對篩選後的股票列表呼叫 Claude 評分，產出 HTML
    回傳：輸出檔案路徑
    """
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("請設定環境變數 ANTHROPIC_API_KEY")

    print(f"[generator] 開始對 {len(filtered_stocks)} 檔股票進行 Claude 分析...")
    stocks_with_eval = []

    for i, stock in enumerate(filtered_stocks, 1):
        print(f"[generator] ({i}/{len(filtered_stocks)}) 分析 {stock['stock_id']}...")
        eval_result = claude_evaluate(stock)
        print(f"  → 評分：{eval_result.get('score', '?')} | {eval_result.get('reason', '')[:40]}")
        stocks_with_eval.append((stock, eval_result))
        if i < len(filtered_stocks):
            time.sleep(api_delay)

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = render_page(stocks_with_eval, generated_at)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"stock_picks_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    # 同時寫一份 latest.html 供固定連結存取
    latest_path = os.path.join(OUTPUT_DIR, "latest.html")
    with open(latest_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[generator] ✅ 輸出完成：{filepath}")
    return filepath


def generate_scan_result(stocks_data: list[dict]) -> str:
    """全台股掃描：分低/中/高風險三區輸出 scan_result.html"""
    low_risk    = sorted([s for s in stocks_data if s.get("risk_level") == "low"],
                         key=lambda x: x.get("rr_ratio", 0), reverse=True)
    medium_risk = sorted([s for s in stocks_data if s.get("risk_level") == "medium"],
                         key=lambda x: x.get("rr_ratio", 0), reverse=True)
    high_risk   = sorted([s for s in stocks_data if s.get("risk_level") == "high"],
                         key=lambda x: x.get("rr_ratio", 0), reverse=True)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def _scan_card(s: dict) -> str:
        rl = s.get("risk_level", "medium")
        border = "#14532d" if rl == "low" else ("#7f1d1d" if rl == "high" else "#1e293b")
        bg     = "#0a1f0f" if rl == "low" else ("#1a0a0a" if rl == "high" else "#0f172a")
        trend  = s.get("trend", "整理")
        tc     = "#22c55e" if trend == "多頭" else ("#ef4444" if trend == "空頭" else "#94a3b8")
        wr     = s.get("win_rate", 0.50)
        wrc    = "#22c55e" if wr > 0.55 else ("#ef4444" if wr < 0.50 else "#94a3b8")
        kline  = s.get("kline_pattern", "")
        kline_html = (f'<div style="color:#a78bfa;margin-top:4px;font-size:11px">{kline}</div>'
                      if kline and "常態" not in kline else "")
        return (
            f'<div style="background:{bg};border:1px solid {border};border-radius:14px;padding:16px;font-size:12px">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">'
            f'<div><span style="font-size:15px;font-weight:700;color:#f1f5f9">{s["stock_id"]}</span>'
            f'<span style="color:#64748b;margin-left:6px">{s.get("name","")}</span></div>'
            f'<span style="font-size:14px;font-weight:700;color:#e2e8f0">NT${s["price"]}</span></div>'
            f'<div style="display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px">'
            f'<span style="padding:2px 8px;border-radius:20px;background:#1e293b;color:{tc}">{trend}</span>'
            f'<span style="padding:2px 8px;border-radius:20px;background:#1e293b;color:#94a3b8">RR {s.get("rr_ratio",0)}x</span>'
            f'<span style="padding:2px 8px;border-radius:20px;background:#1e293b;color:{wrc}">勝率 {int(wr*100)}%</span>'
            f'</div>'
            f'<div style="color:#64748b;line-height:1.8">'
            f'<div>MA5 <b style="color:#e2e8f0">{s["ma5"]}</b>　MA20 <b style="color:#e2e8f0">{s["ma20"]}</b>　MA60 <b style="color:#e2e8f0">{s["ma60"]}</b></div>'
            f'<div>支撐 <b style="color:#22c55e">{s["support"]}</b>　壓力 <b style="color:#f59e0b">{s["resistance"]}</b></div>'
            f'{kline_html}</div></div>'
        )

    def _section(title, color, items, note):
        if not items:
            return ""
        cards = "\n".join(_scan_card(s) for s in items[:150])
        return (
            f'<div style="margin-bottom:40px">'
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">'
            f'<h2 style="font-size:18px;font-weight:700;color:{color}">{title}</h2>'
            f'<span style="font-size:12px;color:#475569">{len(items)} 檔　{note}</span></div>'
            f'<div class="grid">{cards}</div></div>'
        )

    body = (
        _section("🟢 低風險", "#22c55e", low_risk,    "MA5>MA20>MA60，趨勢多頭") +
        _section("🟡 中風險", "#f59e0b", medium_risk, "均線整理，等待方向") +
        _section("🔴 高風險", "#ef4444", high_risk,   "趨勢空頭，謹慎操作")
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>全台股掃描 — {generated_at[:10]}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#020817;color:#f1f5f9;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;padding:24px 16px 48px}}
.container{{max-width:1200px;margin:0 auto}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}}
.stat{{background:#0f172a;border:1px solid #1e293b;border-radius:10px;padding:10px 16px;font-size:12px;color:#64748b}}
.stat strong{{display:block;font-size:18px;font-weight:700;color:#f1f5f9;margin-bottom:2px}}
.disclaimer{{margin-top:32px;padding:16px;background:#0f172a;border-radius:10px;font-size:11px;color:#475569;line-height:1.7}}
@media(max-width:600px){{.grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="container">
  <div style="margin-bottom:28px">
    <h1 style="font-size:22px;font-weight:700;margin-bottom:6px">📡 全台股掃描</h1>
    <p style="font-size:13px;color:#64748b">產生時間：{generated_at}　｜　掃描 {len(stocks_data)} 檔　｜　技術面風險分級</p>
  </div>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:28px">
    <div class="stat"><strong style="color:#22c55e">{len(low_risk)}</strong>低風險</div>
    <div class="stat"><strong style="color:#f59e0b">{len(medium_risk)}</strong>中風險</div>
    <div class="stat"><strong style="color:#ef4444">{len(high_risk)}</strong>高風險</div>
    <div class="stat"><strong>{len(stocks_data)}</strong>掃描總數</div>
  </div>
  {body}
  <div class="disclaimer">⚠️ 本頁面資料僅供參考，不構成買賣建議。股市有風險，請自行評估後決策。</div>
</div>
</body>
</html>"""

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    scan_path = os.path.join(OUTPUT_DIR, "scan_result.html")
    with open(scan_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[generator] ✅ 全台掃描輸出：{scan_path}（{len(stocks_data)} 檔）")
    return scan_path


if __name__ == "__main__":
    # 單獨測試：用假資料跑一次
    dummy = [{
        "stock_id": "2330",
        "name": "台積電",
        "price": 750.0,
        "high_60": 1080.0,
        "drawdown_pct": 30.6,
        "consecutive_buy_days": 5,
        "inst_5d_total": 12000,
        "inst_20d_total": 35000,
        "vol_ratio": 1.5,
        "avg_vol_5": 25000,
        "news": [{"title": "外資連5日買超台積電", "link": "#", "keywords": ["外資買"]}],
        "score_factors": [
            "回檔幅度 30.6%（60日高點 1080，現價 750）",
            "法人連續買超 5 天，近5日合計 +12,000 張",
            "量能：近5日均量是60日均量的 1.5x（放大）",
            "鉅亨題材新聞 1 則，關鍵字：外資買",
        ],
    }]
    run(dummy)
