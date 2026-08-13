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
# 深度選股結果輸出（2026/07/26 新增）
# 對應 main.py 第5989行 _run_deep_analysis_job 呼叫：
#   from generator import generate_deep_analysis
#   generate_deep_analysis(results)
# results 格式對應新版 finmind_filter.py 的 run_deep_scan() 回傳格式，
# 欄位包含：matched_conditions / score / confidence / warnings /
# stop_loss / stop_loss_pct / risk_level / support / resistance 等
#
# 風格：混合 render_card（豐富度）+ generate_scan_result（風險分區）
# ──────────────────────────────────────────

def _deep_confidence_color(confidence: str) -> str:
    if "高信心" in (confidence or ""):
        return "#22c55e"
    if "中信心" in (confidence or ""):
        return "#f59e0b"
    return "#94a3b8"


def _deep_risk_color(risk_level: str) -> str:
    return {"低": "#22c55e", "中": "#f59e0b", "高": "#ef4444"}.get(risk_level, "#94a3b8")


def _deep_condition_label(cond: str) -> str:
    """把 matched_conditions 裡的內部代號轉成使用者看得懂的中文"""
    mapping = {
        "cond1_低檔起漲":                    "低檔起漲",
        "cond2_高點拉回起漲(買1)":            "高點拉回起漲（買1）",
        "cond3_均線突破(買2)":                "均線突破（買2）",
        "cond3_均線突破(買2)_量能未確認":      "均線突破（買2）⚠量能未確認",
        "MACD金叉":                          "MACD金叉",
        "MACD動能加速中":                     "MACD動能加速",
    }
    return mapping.get(cond, cond)


def _deep_conclusion(s: dict) -> str:
    """
    深度選股白話結論（2026/08/13新增，2026/08/13追加K棒突破隔日拉回敘事）。

    背景：main.py 個股解析（_do_analyze）會組出一句「靠近支撐XX，出現多頭K棒，操作：...」
    的白話結論，但深度選股原本只有條件徽章+警示清單，沒有整合成一句話的說明，使用者要
    自己拼湊。這裡用深度選股本來就有算的欄位（入選型態、金叉天數、量能、法人、防守位、
    損益比）組成同樣風格的白話句子，用詞跟個股解析統一用「防守位」「損益比」，不再各講各的。
    另外深度選股現在也接上了跟個股解析同一套K棒型態偵測（見 finmind_filter.py 的
    kbar_pattern/breakout_pullback_note，函式來自共用的 kbar_indicators.py），若當日符合
    「孕線＋前一天已突破/跌破」的情境，會附加跟個股解析一致的「突破隔日拉回」判斷。

    全部欄位都從 s（deep_analyze_stock 的回傳值）動態取值，沒有寫死任何股票代號或數字。
    """
    conds = s.get("matched_conditions") or []

    lead = "技術面轉強"
    for c in conds:
        if c.startswith("cond1_"):
            lead = "股價從相對低檔重新轉強"
            break
        if c.startswith("cond2_"):
            lead = "股價從高點拉回整理後再度轉強"
            break
        if c.startswith("cond3_"):
            lead = ("股價持續突破且量能同步放大確認" if "量能未確認" not in c
                     else "股價持續突破，但量能尚未明確放大，訊號稍弱")
            break

    days_ago = s.get("ma_cross_days_ago")
    if days_ago == 0:
        cross_desc = "月季線金叉發生在今日"
    elif days_ago:
        cross_desc = f"月季線金叉發生在{days_ago}個交易日前"
    else:
        cross_desc = "月季線呈多頭排列"

    above_pct = s.get("above_ma20_pct")
    above_desc = f"，現價高於月線 {above_pct}%" if above_pct is not None else ""
    macd_desc = "，MACD已同步金叉" if "MACD金叉" in conds else ""

    buy_days = s.get("consecutive_buy_days", 0) or 0
    if buy_days >= 3:
        inst_desc = f"，法人連續買超{buy_days}日"
    elif buy_days >= 1:
        inst_desc = "，法人近日轉為買超"
    else:
        inst_desc = ""

    stop_loss = s.get("stop_loss")
    stop_pct  = s.get("stop_loss_pct")
    rr_ratio  = s.get("rr_ratio")
    risk_level = s.get("risk_level", "中")
    confidence = s.get("confidence", "一般")
    score      = s.get("score", 0)

    pullback_note = s.get("breakout_pullback_note") or ""
    pullback_sentence = f"K棒觀察：{pullback_note}。" if pullback_note else ""

    return (
        f"{lead}，{cross_desc}{above_desc}{macd_desc}{inst_desc}，"
        f"綜合評分 {score} 分（{confidence}）。"
        f"操作參考：防守位 {stop_loss}（距現價 -{stop_pct}%，{risk_level}風險），"
        f"損益比約 {rr_ratio}x（以壓力 {s.get('resistance','—')} 為目標估算）。"
        f"{pullback_sentence}"
        f"實際進出場請以下方個股完整報告的即時分析為準。"
    )


def render_deep_card(s: dict) -> str:
    """深度選股個股卡片：風險等級配色 + 豐富內容（比照精選股卡片）"""
    risk_level  = s.get("risk_level", "中")
    risk_color  = _deep_risk_color(risk_level)
    conf_color  = _deep_confidence_color(s.get("confidence", ""))
    score       = s.get("score", 0)

    change      = s.get("change", 0)
    change_pct  = s.get("change_pct", 0)
    change_color = "#ef4444" if change > 0 else ("#22c55e" if change < 0 else "#94a3b8")
    change_sign  = "+" if change > 0 else ""

    cond_badges = "".join(
        f'<span style="font-size:10px;padding:2px 10px;border-radius:20px;'
        f'background:#1e293b;color:#a78bfa;font-weight:600">{_deep_condition_label(c)}</span>'
        for c in s.get("matched_conditions", [])
    )

    vol_ratio = s.get("vol_ratio", 0)
    vol_color = "#22c55e" if vol_ratio >= 1.5 else "#f59e0b" if vol_ratio >= 1.2 else "#94a3b8"

    warnings_html = ""
    if s.get("warnings"):
        warn_lines = "".join(f'<div>⚠️ {w}</div>' for w in s["warnings"])
        warnings_html = (
            f'<div style="background:#1a0a0a;border:1px solid #7f1d1d;border-radius:10px;'
            f'padding:10px 12px;font-size:11px;color:#fca5a5;line-height:1.6;margin-top:8px">'
            f'{warn_lines}</div>'
        )

    fund_parts = []
    if s.get("per") is not None:
        fund_parts.append(f'本益比 {s["per"]}')
    if s.get("dividend_yield") is not None:
        fund_parts.append(f'殖利率 {s["dividend_yield"]}%')
    if s.get("eps_ttm") is not None:
        eps_yoy = s.get("eps_yoy")
        yoy_txt = f'（YoY {eps_yoy:+.1f}%）' if eps_yoy is not None else ""
        fund_parts.append(f'近四季EPS {s["eps_ttm"]}{yoy_txt}')
    fund_html = ""
    if fund_parts:
        fund_html = (
            f'<div style="color:#64748b;font-size:11px;margin-top:6px">'
            f'{"　".join(fund_parts)}</div>'
        )

    return f"""
<div style="background:#0f172a;border:1px solid {risk_color}44;border-radius:16px;padding:20px;
     display:flex;flex-direction:column;gap:12px;position:relative;overflow:hidden">
  <div style="position:absolute;top:16px;right:16px;width:52px;height:52px;border-radius:50%;
       background:conic-gradient({conf_color} {min(score,10) * 36}deg, #1e293b 0deg);
       display:flex;align-items:center;justify-content:center">
    <div style="width:40px;height:40px;border-radius:50%;background:#0f172a;
         display:flex;align-items:center;justify-content:center;
         font-size:13px;font-weight:700;color:{conf_color}">{score}</div>
  </div>
  <div style="padding-right:60px">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
      <span style="font-size:17px;font-weight:700;color:#f1f5f9">{s['stock_id']}</span>
      <span style="font-size:13px;color:#64748b">{s.get('stock_name', '')}</span>
    </div>
    <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center">
      <span style="font-size:10px;padding:2px 8px;border-radius:20px;
            background:{conf_color}22;color:{conf_color};font-weight:700">{s.get('confidence','一般')}</span>
      <span style="font-size:10px;padding:2px 8px;border-radius:20px;
            background:{risk_color}22;color:{risk_color};font-weight:600">風險：{risk_level}</span>
      <span style="font-size:10px;padding:2px 8px;border-radius:20px;
            background:#1e293b;color:{vol_color}">📊 量比 {vol_ratio}x</span>
    </div>
    <div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:6px">{cond_badges}</div>
  </div>
  <div style="display:flex;gap:16px;font-size:12px;color:#64748b;flex-wrap:wrap">
    <span>現價 <strong style="color:#f1f5f9;font-size:15px">{s['price']}</strong>
      <span style="color:{change_color}">{change_sign}{change} ({change_sign}{change_pct}%)</span>
      {f'<span style="color:#475569;font-size:11px">（{s["price_date"]}）</span>' if s.get('price_date') else ""}</span>
    <span>MA5 <strong style="color:#94a3b8">{s.get('ma5','—')}</strong>
      MA20 <strong style="color:#94a3b8">{s.get('ma20','—')}</strong>
      MA60 <strong style="color:#94a3b8">{s.get('ma60','—')}</strong></span>
  </div>
  <div style="background:#1e293b;border-radius:10px;padding:12px;font-size:12px;line-height:1.8">
    <div style="color:#64748b">
      MACD DIF {s.get('macd_dif','—')}　DEA {s.get('macd_dea','—')}　柱 {s.get('macd_hist','—')}
      {f"　法人連買 {s['consecutive_buy_days']}日" if s.get('consecutive_buy_days', 0) >= 2 else ""}
    </div>
    {fund_html}
  </div>
  <div style="background:#111c34;border:1px solid #1e293b;border-radius:10px;padding:12px;
       font-size:12px;line-height:1.7;color:#cbd5e1">{_deep_conclusion(s)}</div>
  {warnings_html}
  <a href="/report/{s['stock_id']}" style="display:block;text-align:center;margin-top:2px;
     background:#1e293b;border:1px solid #334155;border-radius:10px;padding:10px;
     font-size:12px;font-weight:600;color:#a78bfa;text-decoration:none">
    📄 查看 {s['stock_id']} 完整個股報告（支撐壓力、防守位、目標價）→
  </a>
</div>"""


_AD_PUB = "ca-pub-1768270548115739"
_AD_SLOT_ARTICLE = "2793159185"   # 內文區廣告（跟全站其他頁面共用同一個真實廣告單元）
_AD_SLOT_BOTTOM   = "4182262477"  # 底部廣告（跟全站其他頁面共用同一個真實廣告單元）


def _ad_slot(slot_id: str, position_index: int = 0) -> str:
    """
    AdSense 廣告位，深色主題樣式，預留min-height避免CLS版位跳動。
    使用全站共用的兩個真實廣告單元ID（非auto佔位），依位置交替使用：
    偶數位置用內文廣告ID，奇數位置用底部廣告ID。
    """
    real_slot = _AD_SLOT_ARTICLE if position_index % 2 == 0 else _AD_SLOT_BOTTOM
    return f'''
<div style="min-height:250px;margin:20px 0;display:flex;align-items:center;justify-content:center;
     background:#0f172a;border:1px dashed #334155;border-radius:12px;overflow:hidden">
  <ins class="adsbygoogle" style="display:block;width:100%;min-height:250px"
       data-ad-client="{_AD_PUB}"
       data-ad-slot="{real_slot}"
       data-ad-format="auto"
       data-full-width-responsive="true"
       id="{slot_id}"></ins>
</div>
<script>try{{(adsbygoogle = window.adsbygoogle || []).push({{}});}}catch(e){{}}</script>'''


def render_track_record_table(records: list[dict]) -> str:
    """
    選股成效追蹤表：公開顯示過去選股滿20個交易日後的實際報酬率，
    讓使用者能檢驗這個機制的真實成效，而不是只看到「今天入選」的名單。
    records 由 main.py._get_deep_track_records() 提供，已經是滿20天、算出報酬率的紀錄。
    """
    if not records:
        return ""
    rows_html = []
    for r in records:
        pct = r.get("return_20d_pct")
        color = "#ef4444" if pct > 0 else ("#22c55e" if pct < 0 else "#94a3b8")
        sign = "+" if pct > 0 else ""
        rows_html.append(
            f'<tr style="border-bottom:1px solid #1e293b">'
            f'<td style="padding:8px 10px;font-size:12px;color:#e2e8f0">{r.get("stock_name","")}</td>'
            f'<td style="padding:8px 10px;font-size:12px;color:#64748b">{r.get("cross_date","")}</td>'
            f'<td style="padding:8px 10px;font-size:12px;color:#64748b;text-align:right">{r.get("pick_price","")}</td>'
            f'<td style="padding:8px 10px;font-size:12px;color:#64748b;text-align:right">{r.get("return_20d_price","")}</td>'
            f'<td style="padding:8px 10px;font-size:13px;font-weight:700;color:{color};text-align:right">{sign}{pct}%</td>'
            f'</tr>'
        )
    win_count = sum(1 for r in records if (r.get("return_20d_pct") or 0) > 0)
    win_rate = round(win_count / len(records) * 100) if records else 0
    return f'''
<div style="background:#0f172a;border:1px solid #1e293b;border-radius:14px;padding:20px;margin-bottom:24px">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px">
    <h2 style="font-size:16px;font-weight:700;color:#f1f5f9">📊 選股成效追蹤（滿20個交易日的實際報酬率）</h2>
    <span style="font-size:12px;color:#64748b">近{len(records)}筆　勝率 <b style="color:#e2e8f0">{win_rate}%</b></span>
  </div>
  <div style="overflow-x:auto">
  <table style="width:100%;border-collapse:collapse;min-width:480px">
    <thead><tr style="border-bottom:1px solid #334155">
      <th style="padding:0 10px 8px;font-size:11px;color:#64748b;text-align:left">股票</th>
      <th style="padding:0 10px 8px;font-size:11px;color:#64748b;text-align:left">金叉日期</th>
      <th style="padding:0 10px 8px;font-size:11px;color:#64748b;text-align:right">選股價</th>
      <th style="padding:0 10px 8px;font-size:11px;color:#64748b;text-align:right">20日後價</th>
      <th style="padding:0 10px 8px;font-size:11px;color:#64748b;text-align:right">報酬率</th>
    </tr></thead>
    <tbody>{"".join(rows_html)}</tbody>
  </table>
  </div>
  <p style="font-size:11px;color:#475569;margin-top:10px;line-height:1.6">
    每筆紀錄為選股當天收盤價，與其後第20個交易日收盤價的報酬率，已扣除人為挑選偏差（同一次金叉事件只記錄一次）。
    僅供檢視機制成效，不代表未來報酬，過去績效不保證未來結果。
  </p>
</div>'''


def generate_deep_analysis(results: list[dict], note: str = "", track_records: list[dict] | None = None) -> str:
    """
    深度選股結果輸出，依風險等級分三區（低/中/高），每區內依分數排序。
    對應 main.py _run_deep_analysis_job 的呼叫，輸出至
    stock_picker/output/deep_analysis.html（main.py 讀取這個固定路徑存進DB）

    2026/07/26 新增：
      - note 參數：公開版顯示「延遲一交易日」的說明
      - 3~5 則 AdSense 廣告位，依當日入選股票數量自動增減，避免內容少廣告多
      - 醒目的「即時資料在 App」導流CTA（比delay note更顯眼，是這頁的主要轉換點）
      - 補上全站規定的 cookie-consent.css / softglow-cookies.js，符合GDPR+AdSense規則

    2026/08/07 新增：
      - track_records 參數：選股滿20個交易日後的實際報酬率追蹤表，公開顯示，
        讓使用者能檢驗這個選股機制的真實成效
    """
    low_risk  = sorted([r for r in results if r.get("risk_level") == "低"],
                       key=lambda x: x.get("score", 0), reverse=True)
    mid_risk  = sorted([r for r in results if r.get("risk_level") == "中"],
                       key=lambda x: x.get("score", 0), reverse=True)
    high_risk = sorted([r for r in results if r.get("risk_level") == "高"],
                       key=lambda x: x.get("score", 0), reverse=True)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 固定加厚內容（不隨每日結果變動，給Google爬蟲穩定可索引的文字內容）
    seo_content = '''
<div style="background:#0f172a;border:1px solid #1e293b;border-radius:14px;padding:20px;margin-bottom:24px;line-height:1.8">
  <h2 style="font-size:16px;font-weight:700;color:#f1f5f9;margin-bottom:10px">什麼是深度選股？</h2>
  <p style="font-size:13px;color:#94a3b8;margin-bottom:14px">
    深度選股是從台股成交量前150大個股中，用「雙重確認＋加分」機制自動篩選出技術面剛轉強的股票。
    兩個條件必須同時成立才有資格入選：① 月季線金叉（20日均線由下往上穿越60日均線，且金叉後
    未再翻回空頭）② 股價站上月線（現價需在20日均線之上）。通過後系統再依 MACD金叉（快線由下
    往上穿越慢線，3日內發生）、股價位置（低檔起漲、高點拉回起漲、均線突破）、量能強弱、法人
    籌碼動向等因子加分，分數愈高代表訊號愈強。
  </p>
  <h2 style="font-size:16px;font-weight:700;color:#f1f5f9;margin-bottom:10px">防守位怎麼計算？</h2>
  <p style="font-size:13px;color:#94a3b8;margin-bottom:14px">
    系統會計算「起漲低點」（這波漲勢的月季線金叉那天到現在的最低價）、月線、
    前一根K棒低點這三個可能的防守位，再取其中「離現價最近、風險最低」的一個
    當作建議防守位，並換算成距現價的百分比，分為低（5%以內）、中（5~10%）、
    高（10%以上）三個風險等級，方便快速判斷承擔的下檔風險大小。
  </p>
  <h2 style="font-size:16px;font-weight:700;color:#f1f5f9;margin-bottom:10px">常見問題</h2>
  <div style="font-size:13px;color:#94a3b8">
    <p style="margin-bottom:10px"><b style="color:#e2e8f0">Q：這份名單多久更新一次？</b><br>
    A：每個交易日收盤後 17:00 自動掃描更新一次，本頁顯示的是延遲一個交易日的資料，即時結果需登入App查看。</p>
    <p style="margin-bottom:10px"><b style="color:#e2e8f0">Q：信心等級是怎麼判斷的？</b><br>
    A：依加分項目總分區分，5分以上為高信心🔥，3~4分為中信心⭐，1~2分為一般，分數愈高代表符合的技術訊號愈多重。</p>
    <p><b style="color:#e2e8f0">Q：這份名單可以直接照著買嗎？</b><br>
    A：不建議。本頁資料為技術面自動化篩選結果，僅供研究參考，不構成投資建議，請自行評估風險並設好防守位。</p>
  </div>
</div>'''

    section_meta = {
        "low":  ("🟢 低風險", "#22c55e", low_risk,  "防守位距現價5%以內"),
        "mid":  ("🟡 中風險", "#f59e0b", mid_risk,  "防守位距現價5~10%"),
        "high": ("🔴 高風險", "#ef4444", high_risk, "防守位距現價10%以上，謹慎操作"),
    }
    rendered_keys = [k for k in ("low", "mid", "high") if section_meta[k][2]]

    # 廣告位計數器：確保多則廣告交替使用兩個真實slot ID，而不是全部同一個
    _ad_counter = [0]
    def _next_ad(label: str) -> str:
        idx = _ad_counter[0]
        _ad_counter[0] += 1
        return _ad_slot(label, idx)

    def _section_html(key: str) -> str:
        title, color, items, note_text = section_meta[key]
        if len(items) >= 6:
            # 卡片數夠多時，這一區內部再插一則廣告，分成前後兩半
            half = len(items) // 2
            cards_first  = "\n".join(render_deep_card(s) for s in items[:half])
            cards_second = "\n".join(render_deep_card(s) for s in items[half:])
            return (
                f'<div style="margin-bottom:40px">'
                f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">'
                f'<h2 style="font-size:18px;font-weight:700;color:{color}">{title}</h2>'
                f'<span style="font-size:12px;color:#475569">{len(items)} 檔　{note_text}</span></div>'
                f'<div class="grid">{cards_first}</div>'
                f'{_next_ad(f"ad-{key}-split")}'
                f'<div class="grid">{cards_second}</div></div>'
            )
        cards = "\n".join(render_deep_card(s) for s in items)
        return (
            f'<div style="margin-bottom:40px">'
            f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">'
            f'<h2 style="font-size:18px;font-weight:700;color:{color}">{title}</h2>'
            f'<span style="font-size:12px;color:#475569">{len(items)} 檔　{note_text}</span></div>'
            f'<div class="grid">{cards}</div></div>'
        )

    # ── 組裝內容區塊，廣告依內容量自動插入 3~5 則 ──
    body_parts = [_next_ad("ad-top")]  # 廣告①：固定在最上方

    if not rendered_keys:
        body_parts.append(
            '<div style="padding:32px 0;text-align:center;color:#475569">當時無符合雙重確認條件的股票</div>'
        )
        body_parts.append(_next_ad("ad-empty-mid"))  # 廣告②：內容空白時補一則，維持最低3則
    else:
        for i, key in enumerate(rendered_keys):
            body_parts.append(_section_html(key))
            is_last = (i == len(rendered_keys) - 1)
            if not is_last:
                body_parts.append(_next_ad(f"ad-between-{key}"))  # 廣告：區塊間插入
            elif len(rendered_keys) == 1:
                # 只有一區時，硬性補一則廣告確保最低3則
                body_parts.append(_next_ad("ad-single-section-mid"))

    body_parts.append(_next_ad("ad-bottom"))  # 廣告：固定在最下方（配合免責聲明前）
    body = "".join(body_parts)

    track_table_html = render_track_record_table(track_records or [])

    total = len(results)
    high_conf_count = sum(1 for r in results if "高信心" in (r.get("confidence") or ""))

    note_banner = ""
    if note:
        note_banner = (
            f'<div style="background:#1e293b;border:1px solid #334155;border-radius:10px;'
            f'padding:12px 16px;margin-bottom:12px;font-size:12px;color:#94a3b8;text-align:center">'
            f'{note}</div>'
        )

    # 醒目的「即時資料在App」導流CTA，這是整頁的主要轉換目的
    live_cta = '''
<div onclick="location.href='https://softglow-ai.com/'"
  style="background:linear-gradient(135deg,#1a3a2a 0%,#0f2d1f 100%);border:1.5px solid #2d6a4f;
  border-radius:14px;padding:18px 20px;margin-bottom:24px;cursor:pointer;
  display:flex;justify-content:space-between;align-items:center;gap:12px;
  box-shadow:0 2px 16px rgba(29,158,117,0.2)">
  <div>
    <div style="font-size:16px;font-weight:800;color:#4ade80;margin-bottom:4px">📲 想看今天最新即時分析？</div>
    <div style="font-size:12px;color:#86efac;line-height:1.6">
      本頁資料為延遲一個交易日，即時深度選股結果、股票代號、完整防守位建議<br>
      都在 <b>App 內登入後</b> 立即查看，每個交易日 17:00 更新
    </div>
  </div>
  <div style="background:#22c55e;color:#02120a;font-size:13px;font-weight:800;padding:10px 18px;
    border-radius:10px;white-space:nowrap;flex-shrink:0">立即前往 ›</div>
</div>'''

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>深度選股 — {generated_at[:10]}</title>
<link rel="stylesheet" href="/js/cookie-consent.css">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#020817;color:#f1f5f9;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;min-height:100vh;padding:24px 16px 48px}}
.container{{max-width:1200px;margin:0 auto}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}}
.stat{{background:#0f172a;border:1px solid #1e293b;border-radius:10px;padding:10px 16px;font-size:12px;color:#64748b}}
.stat strong{{display:block;font-size:18px;font-weight:700;color:#f1f5f9;margin-bottom:2px}}
.disclaimer{{margin-top:32px;padding:16px;background:#0f172a;border-radius:10px;font-size:11px;color:#475569;line-height:1.7}}
@media(max-width:600px){{.grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="container">
  <div style="margin-bottom:20px">
    <h1 style="font-size:22px;font-weight:700;margin-bottom:6px">🎯 深度選股</h1>
    <p style="font-size:13px;color:#64748b">產生時間：{generated_at}　｜　篩選條件：月季線金叉＋站上月線（雙重確認）＋MACD金叉加分</p>
  </div>
  {note_banner}
  {live_cta}
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:28px">
    <div class="stat"><strong>{total}</strong>檔入選</div>
    <div class="stat"><strong style="color:#22c55e">{high_conf_count}</strong>檔高信心🔥</div>
    <div class="stat"><strong style="color:#22c55e">{len(low_risk)}</strong>低風險</div>
    <div class="stat"><strong style="color:#f59e0b">{len(mid_risk)}</strong>中風險</div>
    <div class="stat"><strong style="color:#ef4444">{len(high_risk)}</strong>高風險</div>
  </div>
  {track_table_html}
  {body}
  {seo_content}
  <div class="disclaimer">⚠️ 本頁面資料僅供參考，不構成買賣建議。防守位為系統依技術結構試算，非保證有效，股市有風險，請自行評估後決策。</div>
</div>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1768270548115739" crossorigin="anonymous"></script>
<script src="/js/softglow-cookies.js" defer></script>
</body>
</html>"""

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    deep_path = os.path.join(OUTPUT_DIR, "deep_analysis.html")
    with open(deep_path, "w", encoding="utf-8") as f:
        f.write(html)
    ad_count = html.count('class="adsbygoogle"')
    print(f"[generator] ✅ 深度選股輸出：{deep_path}（{total} 檔，高信心 {high_conf_count} 檔，廣告位 {ad_count} 則）")
    return deep_path
