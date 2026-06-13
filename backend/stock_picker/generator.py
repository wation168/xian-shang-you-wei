"""
generator.py — 產出層（v2 純規則）
對篩選後的股票以規則文字生成分析，產出 HTML + picks_data.json。
"""

import os
import json
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
  <a href="https://softglow-ai.com/?stock={s['stock_id']}&report=1"
     style="display:flex;align-items:center;justify-content:space-between;
            background:#1e3a5f;border:1px solid #2563eb44;border-radius:10px;
            padding:10px 14px;text-decoration:none;margin-top:4px">
    <div>
      <div style="font-size:12px;font-weight:700;color:#93c5fd">📄 完整個股報告</div>
      <div style="font-size:11px;color:#64748b;margin-top:2px">含新聞題材、支撐壓力、操作建議</div>
    </div>
    <span style="font-size:13px;color:#3b82f6;font-weight:700">立即產出 →</span>
  </a>
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

def _stock_signals(stock: dict) -> list[str]:
    """從股票資料萃取技術訊號標籤"""
    sigs = []
    lbl = (stock.get("signal_label") or "").replace("✅ ", "").replace("⚠️ ", "")
    if lbl:
        sigs.append(lbl)
    if stock.get("macd_dif", 0) > 0:
        sigs.append("MACD多方")
    vr = stock.get("vol_ratio", 0)
    if vr >= 1.5:
        sigs.append(f"量{vr:.1f}x")
    cbd = stock.get("consecutive_buy_days", 0)
    if cbd >= 2:
        sigs.append(f"法人連買{cbd}日")
    return sigs[:4]


def generate_picks_html(filtered_stocks: list[dict]) -> tuple[str, list[dict]]:
    """
    規則式評分，產出 latest.html + picks_data.json
    回傳 (輸出路徑, picks_list)
    picks_list = [{"stock_id", "stock_name", "score", "signals"}, ...]
    """
    stocks_with_eval = [(s, rule_evaluate(s)) for s in filtered_stocks]
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 結構化 picks list（供 /admin/run-scan 和 /picks 端點使用）
    picks_list = sorted(
        [
            {
                "stock_id":   s["stock_id"],
                "stock_name": s.get("name", ""),
                "score":      e["score"],
                "signals":    _stock_signals(s),
            }
            for s, e in stocks_with_eval
            if not s.get("is_risk")
        ],
        key=lambda x: x["score"],
        reverse=True,
    )

    html = render_page(stocks_with_eval, generated_at)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename  = f"stock_picks_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    filepath  = os.path.join(OUTPUT_DIR, filename)
    for path in (filepath, os.path.join(OUTPUT_DIR, "latest.html")):
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    json_path = os.path.join(OUTPUT_DIR, "picks_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"generated_at": generated_at, "picks": picks_list}, f, ensure_ascii=False)

    print(f"[generator] ✅ 選股輸出完成：{filepath}（{len(picks_list)} 支入選）")
    return filepath, picks_list


def run(filtered_stocks: list[dict], api_delay: float = 0.0) -> str:
    """向後相容介面，回傳輸出路徑"""
    filepath, _ = generate_picks_html(filtered_stocks)
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


# ──────────────────────────────────────────
# 深度選股報告 HTML 產出
# ──────────────────────────────────────────

def generate_deep_analysis(stocks: list[dict], generated_at: str = "") -> str:
    """
    產出深度選股報告 deep_analysis.html
    stocks: run_deep_scan() 回傳的清單
    """
    import os
    from datetime import datetime
    from zoneinfo import ZoneInfo

    if not generated_at:
        generated_at = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y/%m/%d %H:%M")

    def _sign_color(v):
        """正數紅色，負數綠色（台股慣例）"""
        if v > 0:
            return "#ef4444"
        elif v < 0:
            return "#22c55e"
        return "#94a3b8"

    def _inst_row(label, val):
        color = _sign_color(val)
        sign = "+" if val > 0 else ""
        return f'<div style="display:flex;justify-content:space-between;padding:3px 0;font-size:12px"><span style="color:#94a3b8">{label}</span><span style="color:{color};font-weight:600">{sign}{val:,} 張</span></div>'

    def _broker_table(title, items, key):
        if not items:
            return f'<div style="color:#64748b;font-size:12px">無資料</div>'
        rows = "".join(
            f'<tr><td style="padding:3px 6px;font-size:11px;color:#94a3b8">{i+1}</td>'
            f'<td style="padding:3px 6px;font-size:12px;color:#e2e8f0">{item["broker"]}</td>'
            f'<td style="padding:3px 6px;font-size:12px;text-align:right;color:#f1f5f9;font-weight:600">{item[key]:,}</td></tr>'
            for i, item in enumerate(items)
        )
        return f'<table style="width:100%;border-collapse:collapse">{rows}</table>'

    def _kd_label(signal):
        m = {"golden_cross": ("🟡 KD金叉", "#f59e0b"),
             "bullish": ("📈 K>D", "#22c55e"),
             "bearish": ("📉 K<D", "#ef4444"),
             "neutral": ("➖ 中性", "#94a3b8")}
        return m.get(signal, ("—", "#94a3b8"))

    def _macd_label(signal):
        m = {"strong_bullish": ("🚀 軸上增強", "#ef4444"),
             "bullish": ("📈 軸上", "#f59e0b"),
             "weak": ("😐 偏弱", "#94a3b8"),
             "bearish": ("📉 軸下", "#64748b")}
        return m.get(signal, ("—", "#94a3b8"))

    def _ma_label(trend):
        m = {"bullish": ("🔼 多頭排列", "#ef4444"),
             "bearish": ("🔽 空頭排列", "#22c55e"),
             "mixed": ("↔️ 糾結", "#94a3b8")}
        return m.get(trend, ("—", "#94a3b8"))

    cards = ""
    for s in stocks:
        kd_txt, kd_col     = _kd_label(s.get("kd_signal", ""))
        macd_txt, macd_col = _macd_label(s.get("macd_signal", ""))
        ma_txt, ma_col     = _ma_label(s.get("ma_trend", ""))

        inst_raw = s.get("inst", {})
        inst = {k: round(v / 1000) if isinstance(v, (int, float)) else v for k, v in inst_raw.items()}
        broker = s.get("broker", {})
        buyers      = broker.get("buyers",  [])
        sellers     = broker.get("sellers", [])
        broker_date = broker.get("date", "")

        ma60_str  = f'{s["ma60"]}' if s.get("ma60") else "—"
        rr        = s.get("rr_ratio", 0)
        rr_color  = "#16a34a" if rr >= 2 else "#d97706" if rr >= 1 else "#c0392b"

        change     = s.get("change", 0)
        change_pct = s.get("change_pct", 0)
        chg_color  = "#c0392b" if change > 0 else "#16a34a" if change < 0 else "#888"
        chg_sign   = "+" if change > 0 else ""
        chg_str    = f"{chg_sign}{change} ({chg_sign}{change_pct}%)"

        price      = s['price']
        support    = s['support']
        resistance = s['resistance']
        sup_pct    = round((support - price) / price * 100, 1) if price else 0
        res_pct    = round((resistance - price) / price * 100, 1) if price else 0
        # 距現價超過 15% 改顯示描述文字
        if abs(sup_pct) > 15:
            support_disp = "長線參考"
            sup_pct_str = f"距現價 {sup_pct}%"
        else:
            support_disp = support
            sup_pct_str = f"{sup_pct}%"
        if abs(res_pct) > 15:
            resistance_disp = "長線參考"
            res_pct_str = f"距現價 +{abs(res_pct)}%"
        else:
            resistance_disp = resistance
            res_pct_str = f"+{res_pct}%" if res_pct > 0 else f"{res_pct}%"

        cards += f"""
<div class="card">
  <div class="card-top">
    <div>
      <span class="sname">{s['stock_name']}</span><span class="scode">{s['stock_id']}</span>
    </div>
    <div class="pblock">
      <div class="pbig">{price}</div>
      <div class="pchg" style="color:{chg_color}">{chg_str}</div>
      <div class="pdate">{s.get('date','')}</div>
    </div>
  </div>

  <div class="grid2 mb10">
    <div class="cell">
      <div class="clbl">KD 指標</div>
      <div class="cval" style="color:{kd_col}">{kd_txt}</div>
      <div class="csub">K={s['K']}　D={s['D']}</div>
    </div>
    <div class="cell">
      <div class="clbl">MACD</div>
      <div class="cval" style="color:{macd_col}">{macd_txt}</div>
      <div class="csub">DIF={s['dif']}　DEA={s['dea']}</div>
    </div>
    <div class="cell">
      <div class="clbl">均線排列</div>
      <div class="cval" style="color:{ma_col}">{ma_txt}</div>
      <div class="csub">MA5={s['ma5']} MA20={s['ma20']} MA60={ma60_str}</div>
    </div>
    <div class="cell">
      <div class="clbl">量能比</div>
      <div class="cval volvol">{s['vol_ratio']}x</div>
      <div class="csub">5日均 {s['avg_vol_5']:,} vs 20日均 {s['avg_vol_20']:,} 張</div>
    </div>
  </div>

  <div class="prow mb10">
    <div class="pc">
      <div class="pclbl">支撐</div>
      <div class="pcval" style="color:#16a34a">{support_disp}</div>
      <div class="pcpct" style="color:#16a34a">{sup_pct_str}</div>
    </div>
    <div class="pc pcsep">
      <div class="pclbl">現價</div>
      <div class="pcval">{price}</div>
      <div class="pcpct" style="color:{chg_color}">{chg_str}</div>
    </div>
    <div class="pc pcsep2">
      <div class="pclbl">壓力</div>
      <div class="pcval" style="color:#c0392b">{resistance_disp}</div>
      <div class="pcpct" style="color:#c0392b">{res_pct_str}</div>
    </div>
    <div class="pc">
      <div class="pclbl">損益比</div>
      <div class="pcval" style="color:{rr_color}">{rr}</div>
    </div>
  </div>

  <div class="cell full mb10">
    <div class="clbl">法人籌碼（近3日合計）</div>
    {_inst_row("外資", inst.get('foreign_3d', 0))}
    {_inst_row("投信", inst.get('invest_3d', 0))}
    {_inst_row("自營", inst.get('dealer_3d', 0))}
    <div class="idivider"></div>
    {_inst_row("合計", inst.get('total_3d', 0))}
  </div>

  <div class="grid2 mb10">
    <div class="cell">
      <div class="clbl">基本面</div>
      <div style="display:flex;justify-content:space-between;padding:3px 0;font-size:12px">
        <span style="color:#94a3b8">本益比 PER</span>
        <span style="font-weight:600;color:#e2eaf5">{f'{s["per"]}x' if s.get("per") else "—"}</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:3px 0;font-size:12px">
        <span style="color:#94a3b8">殖利率</span>
        <span style="font-weight:600;color:{'#22c55e' if s.get('dividend_yield') else '#94a3b8'}">{f'{s["dividend_yield"]}%' if s.get("dividend_yield") else "—"}</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:3px 0;font-size:12px">
        <span style="color:#94a3b8">股價淨值比</span>
        <span style="font-weight:600;color:#e2eaf5">{f'{s["pbr"]}x' if s.get("pbr") else "—"}</span>
      </div>
    </div>
    <div class="cell">
      <div class="clbl">近四季EPS</div>
      <div style="font-size:20px;font-weight:700;color:{'#ef4444' if (s.get('eps_ttm') or 0) > 0 else '#22c55e' if (s.get('eps_ttm') or 0) < 0 else '#94a3b8'};margin-bottom:4px">
        {f'${s["eps_ttm"]}' if s.get("eps_ttm") is not None else "—"}
      </div>
      {'<div style="font-size:12px;font-weight:600;color:' + ("#ef4444" if (s.get("eps_yoy") or 0) > 0 else "#22c55e") + '">YoY ' + (f'+{s["eps_yoy"]}%' if (s.get("eps_yoy") or 0) > 0 else f'{s["eps_yoy"]}%') + '</div>' if s.get("eps_yoy") is not None else '<div style="font-size:12px;color:#94a3b8">成長率 —</div>'}
      <div style="font-size:10px;color:#64748b;margin-top:4px">累計四季每股盈餘</div>
    </div>
  </div>

  <div class="grid2 mb10">
    <div class="cell">
      <div class="clbl" style="color:#16a34a">買方前{len(buyers)}大 {broker_date}</div>
      {_broker_table("買方", buyers, "buy_vol")}
    </div>
    <div class="cell">
      <div class="clbl" style="color:#c0392b">賣方前{len(sellers)}大 {broker_date}</div>
      {_broker_table("賣方", sellers, "sell_vol")}
    </div>
  </div>

  <a href="https://softglow-ai.com/?stock={s['stock_id']}&report=1" class="cta">
    <div>
      <div class="cta-t">完整個股報告</div>
      <div class="cta-s">含新聞題材、支撐壓力、操作建議</div>
    </div>
    <span class="cta-a">立即產出 →</span>
  </a>
</div>"""

    if not cards:
        cards = '<div style="text-align:center;padding:60px 0;font-size:15px;opacity:.5">今日無符合條件的股票</div>'

    html = f"""<!DOCTYPE html>
<html lang="zh-TW" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>每日深度選股 | 線上有位</title>
<style>
:root{{--bg:#060d1a;--sf:#0f1f35;--card:#13243d;--cell:#0a1628;--bd:#1e3a5f;--tx:#e2eaf5;--sub:#6b8aad;--mt:#3a5270}}
[data-theme=light]{{--bg:#f0f4f8;--sf:#dde6f0;--card:#fff;--cell:#eaf0f8;--bd:#b8cfe8;--tx:#0f2744;--sub:#4a6080;--mt:#8aaac8}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--tx);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;padding:16px;transition:background .3s,color .3s}}
.container{{max-width:820px;margin:0 auto}}
.ph{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:24px;padding-bottom:14px;border-bottom:1px solid var(--bd)}}
.ph h1{{font-size:21px;font-weight:600;margin-bottom:4px}}
.ph p{{font-size:12px;color:var(--sub);margin-top:3px}}
.tbtn{{background:var(--sf);border:1px solid var(--bd);color:var(--tx);border-radius:8px;padding:6px 14px;font-size:12px;cursor:pointer}}
.card{{background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:18px;margin-bottom:16px}}
.card-top{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px}}
.sname{{font-size:19px;font-weight:600}}
.scode{{font-size:13px;color:var(--sub);margin-left:6px}}
.pblock{{text-align:right}}
.pbig{{font-size:22px;font-weight:700;line-height:1.1}}
.pchg{{font-size:13px;font-weight:600;margin-top:2px}}
.pdate{{font-size:11px;color:var(--mt);margin-top:2px}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.mb10{{margin-bottom:10px}}
.cell{{background:var(--cell);border-radius:10px;padding:10px 12px}}
.cell.full{{grid-column:span 2}}
.clbl{{font-size:10px;color:var(--sub);font-weight:600;text-transform:uppercase;letter-spacing:.4px;margin-bottom:5px}}
.cval{{font-size:13px;font-weight:600;margin-bottom:3px}}
.csub{{font-size:11px;color:var(--sub)}}
.volvol{{font-size:17px!important;color:#d97706!important}}
.prow{{display:flex;justify-content:space-around;background:var(--cell);border-radius:10px;padding:12px;text-align:center}}
.pc{{flex:1}}
.pcsep{{border-left:1px solid var(--bd);border-right:1px solid var(--bd)}}
.pcsep2{{border-right:1px solid var(--bd)}}
.pclbl{{font-size:10px;color:var(--sub);font-weight:600;margin-bottom:4px}}
.pcval{{font-size:15px;font-weight:700}}
.pcpct{{font-size:11px;font-weight:600;margin-top:3px}}
.idivider{{border-top:1px solid var(--bd);margin:5px 0}}
.cta{{display:flex;align-items:center;justify-content:space-between;background:var(--sf);border:1px solid #2563eb88;border-radius:10px;padding:12px 14px;text-decoration:none}}
.cta-t{{font-size:13px;font-weight:600;color:#93c5fd}}
.cta-s{{font-size:11px;color:var(--sub);margin-top:2px}}
.cta-a{{font-size:13px;color:#3b82f6;font-weight:700;white-space:nowrap}}
.disc{{margin-top:24px;padding:14px;background:var(--sf);border-radius:10px;font-size:11px;color:var(--sub);line-height:1.8;border:1px solid var(--bd)}}
@media(max-width:600px){{.grid2{{grid-template-columns:1fr}}.cell.full{{grid-column:span 1}}.prow{{gap:4px}}.pcval{{font-size:13px}}}}
</style>
</head>
<body>
<div class="container">
  <div class="ph">
    <div>
      <h1>🔬 每日深度選股</h1>
      <p>產生時間：{generated_at}　｜　共 {len(stocks)} 檔入選</p>
      <p>篩選條件：KD金叉 + MACD軸上動能增強 + 量能≥1.5倍</p>
    </div>
    <button class="tbtn" onclick="(function(){{var h=document.documentElement,d=h.getAttribute('data-theme')==='dark';h.setAttribute('data-theme',d?'light':'dark');document.querySelector('.tbtn').textContent=d?'🌙 深色':'☀️ 白天'}})()">☀️ 白天</button>
  </div>
  {cards}
  <div class="disc">⚠️ 本頁面資料僅供參考，不構成買賣建議。股市有風險，請自行評估後決策。<br>資料來源：FinMind、臺灣證券交易所 (TWSE)</div>
</div>
</body>
</html>"""

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, "deep_analysis.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[generator] ✅ 深度選股輸出：{out_path}（{len(stocks)} 檔）")
    return out_path
