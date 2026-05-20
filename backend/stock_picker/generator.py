"""
generator.py — 產出層（v2 純規則）
對篩選後的股票以規則文字生成分析，產出 HTML + picks_data.json。
"""

import os
import json
from datetime import datetime

OUTPUT_DIR   = os.path.join(os.path.dirname(__file__), "output")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://softglow-ai.com")


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


def _card_tags(s: dict) -> str:
    """選出 2~3 個最具代表性的標籤 HTML（依優先順序）"""
    badges = []

    cbd = s.get("consecutive_buy_days", 0)
    if cbd >= 2:
        badges.append(
            f'<span style="font-size:10px;padding:3px 10px;border-radius:20px;'
            f'background:#14532d;color:#86efac;font-weight:700">法人連買{cbd}日</span>'
        )

    sig = s.get("signal_label", "")
    if sig and len(badges) < 3:
        sig_bg = "#14532d" if "死叉" not in sig else "#7f1d1d"
        sig_fg = "#86efac" if "死叉" not in sig else "#fca5a5"
        clean  = sig.replace("✅ ", "").replace("⚠️ ", "")
        badges.append(
            f'<span style="font-size:10px;padding:3px 10px;border-radius:20px;'
            f'background:{sig_bg};color:{sig_fg};font-weight:700">{clean}</span>'
        )

    vr = s.get("vol_ratio", 1.0)
    if vr >= 1.2 and len(badges) < 3:
        vc = "#22c55e" if vr >= 1.5 else "#f59e0b"
        badges.append(
            f'<span style="font-size:10px;padding:3px 10px;border-radius:20px;'
            f'background:#1e293b;color:{vc}">量增 {vr:.1f}x</span>'
        )

    if s.get("trend") == "上升" and len(badges) < 3:
        badges.append(
            f'<span style="font-size:10px;padding:3px 10px;border-radius:20px;'
            f'background:#1e293b;color:#22c55e">多頭趨勢</span>'
        )

    return "".join(badges[:3])


def _card_headline(s: dict) -> str:
    """根據最強訊號自動產生一句話摘要，每張卡片不同"""
    cbd   = s.get("consecutive_buy_days", 0)
    vr    = s.get("vol_ratio", 1.0)
    sig   = s.get("signal_label", "")
    trend = s.get("trend", "盤整")
    dif   = s.get("macd_dif", 0.0)
    inst5 = s.get("inst_5d_total", 0)

    if cbd >= 3:
        return f"法人連買 {cbd} 日，累積 {inst5:+,} 張，籌碼持續集中"
    if cbd == 2:
        return f"法人連買 2 日，近5日 {inst5:+,} 張，短線有買盤進場"
    if "雙均線" in sig:
        return "MA5/MA20 雙均線金叉，短中期趨勢同步走強"
    if "MA5穿MA20" in sig:
        return "MA5 穿越 MA20 金叉，短線多頭動能啟動"
    if "MA20穿MA60" in sig:
        return "MA20 穿越 MA60，中期趨勢確認轉多"
    if "KD金叉" in sig:
        return "KD 由超賣區金叉，動能由弱轉強，注意量能配合"
    if vr >= 1.5 and trend == "上升":
        return f"量能放大 {vr:.1f} 倍，搭配多頭趨勢，主力介入跡象明顯"
    if vr >= 1.5:
        return f"成交量急增至均量 {vr:.1f} 倍，異常量能值得追蹤"
    if trend == "上升" and dif > 0:
        return "均線多頭排列且 MACD 在 0 軸以上，雙重多頭確認"
    if trend == "上升":
        return "均線多頭排列，趨勢偏強，等待量能放大確認"
    if dif > 0:
        return f"MACD DIF {dif:.2f} 維持 0 軸以上，多方動能持續"
    return "技術面整理中，等待方向訊號明確"


def render_card(stock: dict, eval_result: dict) -> str:
    s      = stock
    e      = eval_result
    score  = e.get("score", 0)
    color  = score_color(score)
    stock_url = f"{FRONTEND_URL}/?stock={s['stock_id']}"

    tags_html = _card_tags(s)
    headline  = _card_headline(s)

    return f"""
<div style="background:#0f172a;border:1px solid #1e293b;border-radius:16px;padding:20px;
     display:flex;flex-direction:column;gap:14px;position:relative;overflow:hidden;
     cursor:pointer;transition:border-color .2s"
     onmouseenter="this.style.borderColor='#334155'" onmouseleave="this.style.borderColor='#1e293b'"
     onclick="if(!event.target.closest('a'))window.top.location.href='{stock_url}'">
  <div style="position:absolute;top:16px;right:16px;width:52px;height:52px;border-radius:50%;
       background:conic-gradient({color} {score * 3.6}deg, #1e293b 0deg);
       display:flex;align-items:center;justify-content:center">
    <div style="width:40px;height:40px;border-radius:50%;background:#0f172a;
         display:flex;align-items:center;justify-content:center;
         font-size:13px;font-weight:700;color:{color}">{score}</div>
  </div>
  <div style="padding-right:68px">
    <div style="display:flex;align-items:baseline;gap:8px;margin-bottom:10px">
      <span style="font-size:20px;font-weight:800;color:#f1f5f9">{s['stock_id']}</span>
      <span style="font-size:13px;color:#64748b">{s.get('name', '')}</span>
    </div>
    <div style="display:flex;gap:6px;flex-wrap:wrap">{tags_html}</div>
  </div>
  <div style="font-size:13px;color:#cbd5e1;line-height:1.6;
       padding:10px 14px;background:#1e293b;border-radius:8px;
       border-left:3px solid {color}">{headline}</div>
  <div style="font-size:12px;color:#22c55e;text-align:right;letter-spacing:0.3px">
    點擊查看完整技術分析 →</div>
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
        stock_url = f"{FRONTEND_URL}/?stock={s['stock_id']}"
        return (
            f'<div style="background:{bg};border:1px solid {border};border-radius:14px;padding:16px;font-size:12px;'
            f'cursor:pointer;transition:border-color .2s"'
            f' onmouseenter="this.style.borderColor=\'#475569\'" onmouseleave="this.style.borderColor=\'{border}\'"'
            f' onclick="window.top.location.href=\'{stock_url}\'">'
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
