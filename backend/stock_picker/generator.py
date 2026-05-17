"""
generator.py — 產出層（v2 純規則）
對篩選後的股票以規則文字生成分析，產出 HTML。
"""

import os
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")


# ──────────────────────────────────────────
# 規則式評分與文字生成
# ──────────────────────────────────────────
def rule_evaluate(stock: dict) -> dict:
    """以技術指標規則自動產生評分與說明"""
    trend    = stock.get("trend", "盤整")
    kline    = stock.get("kline_pattern", "常態K線")
    wr_pct   = int(stock.get("win_rate", 0.50) * 100)
    signal   = (stock.get("signal_label", "") or "").replace("✅ ", "").replace("⚠️ ", "")
    dif      = stock.get("macd_dif", 0.0)
    vol      = stock.get("vol_ratio", 1.0)
    tech_scr = stock.get("score", 0)
    cons_buy = stock.get("consecutive_buy_days", 0)
    inst5    = stock.get("inst_5d_total", 0)

    # 建構說明文字
    trend_text = {
        "上升": "均線多頭排列，技術結構偏強",
        "下降": "均線空頭排列，技術結構偏弱",
        "盤整": "均線糾結，等待突破方向",
    }.get(trend, "")

    reason_parts = []
    if trend_text:
        reason_parts.append(trend_text)
    if signal:
        reason_parts.append(f"{signal}確認方向")
    if vol >= 1.5:
        reason_parts.append(f"量能放大至 {vol:.1f}x 均量")
    if dif > 0:
        reason_parts.append(f"MACD DIF={dif:.2f} 在 0 軸以上，動能偏多")
    elif dif > -0.5:
        reason_parts.append(f"MACD DIF={dif:.2f} 接近 0 軸，觀察動能轉強")
    if cons_buy >= 3:
        reason_parts.append(f"法人連買 {cons_buy} 日（+{inst5:,} 張）")
    elif cons_buy >= 2:
        reason_parts.append(f"法人連買 {cons_buy} 日")
    if "常態" not in kline:
        reason_parts.append(f"{kline}（勝率{wr_pct}%）")

    reason = "，".join(reason_parts) + "。" if reason_parts else "技術指標觸發篩選條件。"

    # 觀察重點
    if trend == "上升":
        watch_point = "守住均線且量能持續放大可考慮進場追蹤"
    elif signal and "MA" in signal:
        watch_point = "均線金叉後確認站穩，縮量回測不破為加碼點"
    elif signal and "KD" in signal:
        watch_point = "KD金叉後等待強勢K棒確認，避免假突破"
    else:
        watch_point = "量能持續放大且守住均線再評估進場"

    # 風險
    if dif < 0:
        risk = "MACD 仍在 0 軸以下，注意動能轉弱風險"
    elif trend == "下降":
        risk = "均線仍呈空頭排列，須等待趨勢明確轉多再進場"
    else:
        risk = "技術指標翻空或跌破均線須留意停損"

    score = min(50 + tech_scr * 6, 88)
    return {
        "score":       score,
        "reason":      reason,
        "watch_point": watch_point,
        "risk":        risk,
    }


# ──────────────────────────────────────────
# HTML 產出
# ──────────────────────────────────────────
def score_color(score: int) -> str:
    if score >= 80: return "#22c55e"
    if score >= 60: return "#f59e0b"
    return "#94a3b8"


def score_label(score: int) -> str:
    if score >= 90: return "強力關注"
    if score >= 70: return "值得追蹤"
    if score >= 50: return "觀察中"
    return "暫不關注"


def render_card(stock: dict, eval_result: dict) -> str:
    s = stock
    e = eval_result
    score  = e.get("score", 0)
    color  = score_color(score)
    label  = score_label(score)
    signal = s.get("signal_label", "")

    inst_dir   = "買超" if s["inst_5d_total"] > 0 else ("賣超" if s["inst_5d_total"] < 0 else "持平")
    inst_color = "#22c55e" if s["inst_5d_total"] > 0 else ("#ef4444" if s["inst_5d_total"] < 0 else "#94a3b8")
    vol_color  = "#22c55e" if s["vol_ratio"] >= 1.5 else "#f59e0b" if s["vol_ratio"] >= 1.2 else "#94a3b8"
    vol_label  = "量大增" if s["vol_ratio"] >= 1.5 else "量增" if s["vol_ratio"] >= 1.2 else "量平"

    signal_badge = ""
    if signal:
        sig_bg, sig_fg = ("#14532d", "#86efac") if "死叉" not in signal else ("#7f1d1d", "#fca5a5")
        signal_badge = (
            f'<span style="font-size:10px;padding:2px 10px;border-radius:20px;'
            f'background:{sig_bg};color:{sig_fg};font-weight:700">{signal}</span>'
        )

    kws = list({kw for n in s["news"] for kw in n["keywords"]})[:4]
    kw_badges = "".join(
        f'<span style="font-size:10px;padding:2px 8px;border-radius:20px;'
        f'background:#7c3aed22;color:#a78bfa">{k}</span>' for k in kws
    )

    news_html = ""
    for n in s["news"][:2]:
        news_html += (
            f'<a href="{n["link"]}" target="_blank" style="display:block;font-size:11px;'
            f'color:#94a3b8;text-decoration:none;padding:4px 0;border-top:1px solid #1e293b;'
            f'line-height:1.4">{n["title"][:50]}{"…" if len(n["title"])>50 else ""}</a>'
        )

    inst_badge = (
        f'<span style="font-size:10px;padding:2px 8px;border-radius:20px;'
        f'background:#1e293b;color:{inst_color}">法人連{inst_dir} {s["consecutive_buy_days"]}日</span>'
    )

    return f"""
<div style="background:#0f172a;border:1px solid #1e293b;border-radius:16px;padding:20px;
     display:flex;flex-direction:column;gap:12px;position:relative;overflow:hidden">
  <div style="position:absolute;top:16px;right:16px;width:52px;height:52px;border-radius:50%;
       background:conic-gradient({color} {score * 3.6}deg, #1e293b 0deg);
       display:flex;align-items:center;justify-content:center">
    <div style="width:40px;height:40px;border-radius:50%;background:#0f172a;
         display:flex;align-items:center;justify-content:center;
         font-size:13px;font-weight:700;color:{color}">{score}</div>
  </div>
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
  <div style="display:flex;gap:16px;font-size:12px;color:#64748b;flex-wrap:wrap">
    <span>現價 <strong style="color:#f1f5f9;font-size:15px">{s['price']}</strong></span>
    <span>近5日均量 <strong style="color:#94a3b8">{s['avg_vol_5']:,}</strong> 張</span>
    <span>法人近5日 <strong style="color:{inst_color}">{s["inst_5d_total"]:+,}</strong> 張</span>
  </div>
  <div style="background:#1e293b;border-radius:10px;padding:12px;font-size:12px;line-height:1.6">
    <div style="color:#e2e8f0;margin-bottom:8px">{e.get('reason','')}</div>
    <div style="display:flex;flex-direction:column;gap:4px">
      <div><span style="color:#22c55e;font-weight:600">📍 觀察重點：</span>
           <span style="color:#94a3b8">{e.get('watch_point','')}</span></div>
      <div><span style="color:#f59e0b;font-weight:600">⚠️ 風險：</span>
           <span style="color:#94a3b8">{e.get('risk','')}</span></div>
    </div>
  </div>
  {f'<div style="margin-top:-4px">{news_html}</div>' if news_html else ''}
</div>"""


def render_page(stocks_with_eval: list[tuple[dict, dict]], generated_at: str) -> str:
    long_items = sorted(
        [(s, e) for s, e in stocks_with_eval if not s.get("is_risk")],
        key=lambda x: x[1].get("score", 0), reverse=True
    )
    risk_items = sorted(
        [(s, e) for s, e in stocks_with_eval if s.get("is_risk")],
        key=lambda x: x[1].get("score", 0), reverse=True
    )
    long_count = len(long_items)
    high_count = sum(1 for _, e in long_items if e.get("score", 0) >= 70)
    long_cards = "\n".join(render_card(s, e) for s, e in long_items)

    risk_section = ""
    if risk_items:
        risk_cards = "\n".join(render_card(s, e) for s, e in risk_items)
        risk_section = f"""
  <div style="margin-top:40px">
    <h2 style="font-size:18px;font-weight:700;color:#fca5a5;margin-bottom:16px">⚠️ 風險警示</h2>
    <div class="grid">{risk_cards}</div>
  </div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>選股名單 — {generated_at[:10]}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#020817;color:#f1f5f9;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;padding:24px 16px 48px}}
.container{{max-width:960px;margin:0 auto}}
.stats{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px}}
.stat{{background:#0f172a;border:1px solid #1e293b;border-radius:10px;padding:10px 16px;font-size:12px;color:#64748b}}
.stat strong{{display:block;font-size:18px;font-weight:700;color:#f1f5f9;margin-bottom:2px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
.disclaimer{{margin-top:32px;padding:16px;background:#0f172a;border-radius:10px;font-size:11px;color:#475569;line-height:1.7}}
@media(max-width:600px){{.grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="container">
  <div style="margin-bottom:28px">
    <h1 style="font-size:22px;font-weight:700;margin-bottom:6px">🔍 選股名單</h1>
    <p style="font-size:13px;color:#64748b">產生時間：{generated_at}　｜　篩選條件：均線/KD金叉＋量能放大＋MACD確認</p>
  </div>
  <div class="stats">
    <div class="stat"><strong>{long_count}</strong>檔做多候選</div>
    <div class="stat"><strong>{high_count}</strong>檔評分 70+</div>
    <div class="stat"><strong style="color:#22c55e">●</strong>盤後資料</div>
  </div>
  {f'<div><h2 style="font-size:18px;font-weight:700;color:#86efac;margin-bottom:16px">📈 做多候選</h2><div class="grid">{long_cards}</div></div>' if long_items else '<div style="padding:32px 0;text-align:center;color:#475569">今日無做多候選股票</div>'}
  {risk_section}
  <div class="disclaimer">⚠️ 本頁面資料僅供參考，不構成買賣建議。股市有風險，請自行評估後決策。</div>
</div>
</body>
</html>"""


# ──────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────
def generate_picks_html(filtered_stocks: list[dict]) -> str:
    """規則式評分，產出 latest.html，回傳輸出路徑"""
    stocks_with_eval = [(s, rule_evaluate(s)) for s in filtered_stocks]
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = render_page(stocks_with_eval, generated_at)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"stock_picks_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    latest_path = os.path.join(OUTPUT_DIR, "latest.html")
    with open(latest_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[generator] ✅ 選股輸出完成：{filepath}")
    return filepath


def run(filtered_stocks: list[dict], api_delay: float = 0.0) -> str:
    """向後相容介面，內部改用規則式評分"""
    return generate_picks_html(filtered_stocks)


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
        rl    = s.get("risk_level", "medium")
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
