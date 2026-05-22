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


def _trading_rec(s: dict) -> tuple[str, str]:
    """回傳 (建議文字, 顏色) based on trend + signals"""
    trend = s.get("trend", "盤整")
    cbd   = s.get("consecutive_buy_days", 0)
    dif   = s.get("macd_dif", 0.0)
    sig   = s.get("signal_label", "")
    kd_k  = s.get("kd_k", 50)

    if trend == "上升" and cbd >= 3 and dif > 0:
        return "✅ 做多：法人連買+多頭趨勢+MACD正值，三重確認，可考慮分批進場", "#22c55e"
    if trend == "上升" and "金叉" in sig:
        return "✅ 做多：均線/KD金叉配合多頭趨勢，量能放大可分批進場", "#22c55e"
    if trend == "上升" and cbd >= 1:
        return "✅ 偏多：多頭趨勢+法人介入，等待回測均線不破後追進", "#86efac"
    if trend == "上升":
        return "👀 觀望：多頭趨勢但法人未明顯介入，等待量能放大確認", "#f59e0b"
    if trend == "盤整" and "金叉" in sig:
        return "👀 觀望：均線糾結，金叉需量能配合突破確認，可小量試探", "#f59e0b"
    if kd_k <= 20:
        return "👀 觀望（低檔）：KD 進入超賣區，等待金叉確認後再評估進場", "#f59e0b"
    if trend == "下降":
        return "⚠️ 注意停損：均線空頭排列，非多頭佈局時機，持有者設好停損", "#ef4444"
    return "👀 觀望：技術面方向未明，等待明確訊號再評估進場時機", "#94a3b8"


def _render_report(s: dict, e: dict) -> str:
    """展開報告區塊 HTML（K棒/技術/法人/支撐壓力/建議）"""
    sid   = s["stock_id"]
    price = s.get("price", 0)

    # K棒型態
    kline   = s.get("kline_pattern", "常態K線")
    wr_pct  = int(s.get("win_rate", 0.50) * 100)
    vr      = s.get("vol_ratio", 1.0)
    streak  = s.get("kbar_streak", 0)
    streak_txt = (f"連{abs(streak)}{'紅' if streak > 0 else '黑'}K" if abs(streak) >= 2
                  else "無連K訊號")
    vol_txt = (f"量能放大 {vr:.1f}x 均量" if vr >= 1.5 else
               f"量能正常 {vr:.1f}x"         if vr >= 0.8 else
               f"量能萎縮 {vr:.1f}x，主力觀望")

    # MA
    ma5   = s.get("ma5")
    ma20  = s.get("ma20")
    ma60  = s.get("ma60")
    trend = s.get("trend", "盤整")
    tc    = "#22c55e" if trend == "上升" else ("#ef4444" if trend == "下降" else "#94a3b8")
    trend_desc = "MA5>MA20>MA60" if trend == "上升" else ("MA5<MA20<MA60" if trend == "下降" else "均線糾結")
    ma_rows = ""
    if ma5 and ma20:
        ma_rows += (f'<div class="rpt-row"><span class="rpt-label">MA5 / MA20</span>'
                    f'<span class="rpt-val">{ma5} / {ma20}</span></div>')
    if ma60:
        ma_rows += (f'<div class="rpt-row"><span class="rpt-label">MA60</span>'
                    f'<span class="rpt-val">{ma60}</span></div>')

    # KD
    kd_k      = s.get("kd_k", 50.0)
    kd_d      = s.get("kd_d", 50.0)
    kd_cross  = s.get("kd_cross", False)
    kd_zone   = "超買" if kd_k >= 80 else ("超賣" if kd_k <= 20 else "中性")
    kd_zc     = "#ef4444" if kd_k >= 80 else ("#22c55e" if kd_k <= 20 else "#94a3b8")
    cross_tag = ' <span style="color:#22c55e;font-size:11px">金叉</span>' if kd_cross else ""

    # MACD
    dif   = s.get("macd_dif", 0.0)
    dea   = s.get("macd_dea", 0.0)
    mc    = "#22c55e" if dif > 0 else "#ef4444"
    macd_note = "DIF 在 0 軸以上，多方動能" if dif > 0 else "DIF 在 0 軸以下，空方動能"

    # 法人
    cbd   = s.get("consecutive_buy_days", 0)
    inst5 = s.get("inst_5d_total", 0)
    for5  = s.get("inst_foreign_5d", 0)
    inv5  = s.get("inst_invest_5d", 0)
    dal5  = s.get("inst_dealer_5d", 0)
    def _ic(v): return "#22c55e" if v > 0 else ("#ef4444" if v < 0 else "#64748b")
    inst_head = (f'<div style="font-size:12px;color:#86efac;margin-bottom:6px">'
                 f'連買 {cbd} 日（近5日合計 {inst5:+,} 張）</div>' if cbd >= 1 else
                 '<div style="font-size:12px;color:#64748b;margin-bottom:6px">近期無明顯連買訊號</div>')

    # 支撐壓力
    support    = s.get("support", round(price * 0.95, 2))
    resistance = s.get("resistance", round(price * 1.05, 2))
    sup_note_parts = []
    if ma20: sup_note_parts.append(f"MA20:{ma20}")
    if ma60: sup_note_parts.append(f"MA60:{ma60}")
    sup_note_parts.append(f"近低:{support}")
    sup_note = " / ".join(sup_note_parts)

    # 新聞
    news = s.get("news", [])
    news_html = ""
    if news:
        items = "".join(
            f'<a href="{n["link"]}" target="_blank" rel="noopener" style="display:block;font-size:12px;'
            f'color:#60a5fa;text-decoration:none;padding:4px 0;border-bottom:1px solid #1e293b;line-height:1.5">'
            f'📰 {n["title"][:38]}{"…" if len(n["title"])>38 else ""}</a>'
            for n in news[:3]
        )
        news_html = f'<div class="rpt-sec" style="margin-top:0">{items}</div>'

    # 操作建議
    rec_txt, rec_color = _trading_rec(s)

    return (
        f'<div style="display:flex;flex-direction:column;gap:8px;padding-top:6px">'

        # K棒型態
        f'<div class="rpt-sec">'
        f'<div class="rpt-title">📊 K棒型態</div>'
        f'<div style="font-size:13px;color:#a78bfa;font-weight:600;margin-bottom:6px">'
        f'{kline}（勝率 {wr_pct}%）</div>'
        f'<div class="rpt-row"><span class="rpt-label">連K</span>'
        f'<span class="rpt-val">{streak_txt}</span></div>'
        f'<div class="rpt-row"><span class="rpt-label">量能</span>'
        f'<span class="rpt-val">{vol_txt}</span></div>'
        f'</div>'

        # 技術面
        f'<div class="rpt-sec">'
        f'<div class="rpt-title">📈 技術面</div>'
        f'<div class="rpt-row"><span class="rpt-label">均線排列</span>'
        f'<span style="font-weight:600;color:{tc}">{trend}（{trend_desc}）</span></div>'
        f'{ma_rows}'
        f'<div class="rpt-row"><span class="rpt-label">KD（K/D）</span>'
        f'<span class="rpt-val">{kd_k:.0f} / {kd_d:.0f}'
        f' <span style="color:{kd_zc};font-size:11px">（{kd_zone}）</span>{cross_tag}</span></div>'
        f'<div class="rpt-row"><span class="rpt-label">MACD DIF / DEA</span>'
        f'<span style="font-weight:600;color:{mc}">{dif:.3f} / {dea:.3f}</span></div>'
        f'<div style="font-size:11px;color:#64748b;margin-top:2px">{macd_note}</div>'
        f'</div>'

        # 法人籌碼
        f'<div class="rpt-sec">'
        f'<div class="rpt-title">🏦 法人籌碼（近5日）</div>'
        f'{inst_head}'
        f'<div class="rpt-row"><span class="rpt-label">外資</span>'
        f'<span style="font-weight:600;color:{_ic(for5)}">{for5:+,} 張</span></div>'
        f'<div class="rpt-row"><span class="rpt-label">投信</span>'
        f'<span style="font-weight:600;color:{_ic(inv5)}">{inv5:+,} 張</span></div>'
        f'<div class="rpt-row"><span class="rpt-label">自營</span>'
        f'<span style="font-weight:600;color:{_ic(dal5)}">{dal5:+,} 張</span></div>'
        f'</div>'

        # 支撐壓力
        f'<div class="rpt-sec">'
        f'<div class="rpt-title">🎯 支撐壓力</div>'
        f'<div class="rpt-row"><span class="rpt-label">現價</span>'
        f'<span class="rpt-val">{price}</span></div>'
        f'<div class="rpt-row"><span class="rpt-label">支撐</span>'
        f'<span style="font-weight:600;color:#22c55e">{support}</span></div>'
        f'<div class="rpt-row"><span class="rpt-label">壓力</span>'
        f'<span style="font-weight:600;color:#f59e0b">{resistance}</span></div>'
        f'<div style="font-size:11px;color:#475569;margin-top:4px">{sup_note}</div>'
        f'</div>'

        # 操作建議
        f'<div style="background:#0a0f1e;border:1px solid {rec_color};border-radius:8px;padding:12px">'
        f'<div class="rpt-title">💡 操作建議</div>'
        f'<div style="font-size:13px;font-weight:600;color:{rec_color};line-height:1.6">{rec_txt}</div>'
        f'</div>'

        f'{news_html}'
        f'</div>'
    )


def render_card(stock: dict, eval_result: dict) -> str:
    s   = stock
    sid = s["stock_id"]
    name  = s.get("name", "")
    price = s.get("price", 0)
    trend = s.get("trend", "盤整")

    # 風險等級 badge
    if trend == "上升":
        risk_label, risk_color, risk_bg = "多頭", "#22c55e", "#14532d"
    elif trend == "下降":
        risk_label, risk_color, risk_bg = "空頭", "#ef4444", "#7f1d1d"
    else:
        risk_label, risk_color, risk_bg = "觀望", "#f59e0b", "#451a03"

    # 支撐壓力
    support    = s.get("support", round(price * 0.95, 2))
    resistance = s.get("resistance", round(price * 1.05, 2))
    chan_range  = resistance - support

    # 軌道位置 0–100%
    if chan_range > 0 and price > 0:
        pos_pct = int(min(100, max(0, (price - support) / chan_range * 100)))
    else:
        pos_pct = 50
    bar_filled = round(pos_pct / 10)
    bar_html   = "█" * bar_filled + "░" * (10 - bar_filled)
    pos_label  = "偏上" if pos_pct >= 70 else ("偏下" if pos_pct <= 30 else "中段")
    pos_desc   = "靠近壓力位" if pos_pct >= 80 else ("靠近支撐位" if pos_pct <= 20 else "通道中段")
    pos_color  = "#ef4444" if pos_pct >= 80 else ("#22c55e" if pos_pct <= 20 else "#94a3b8")

    # K棒方向
    streak = s.get("kbar_streak", 0)
    if streak >= 2:
        kbar_dir, kbar_color = f"連{streak}紅K", "#22c55e"
    elif streak <= -2:
        kbar_dir, kbar_color = f"連{abs(streak)}黑K", "#ef4444"
    else:
        kbar_dir, kbar_color = "整理中", "#94a3b8"

    # 操作建議（短版）
    rec_txt, rec_color = _trading_rec(s)
    rec_icon = rec_txt[0] if rec_txt else ""
    rec_core = rec_txt.split("：")[1].split("，")[0] if "：" in rec_txt else rec_txt[:18]

    # K線型態
    kline  = s.get("kline_pattern", "常態K線")
    wr_pct = int(s.get("win_rate", 0.50) * 100)

    # 防守位距現價 %
    stop_dist = round((price - support) / price * 100, 1) if price > 0 else 0
    rr        = s.get("rr_ratio", 0)
    rr_txt    = f"  損益比 {rr}x" if rr else ""

    # 趨勢
    trend_c    = "#22c55e" if trend == "上升" else ("#ef4444" if trend == "下降" else "#94a3b8")
    trend_desc = "MA5>MA20>MA60" if trend == "上升" else ("MA5<MA20<MA60" if trend == "下降" else "均線糾結")

    stock_url  = f"{FRONTEND_URL}/?stock={sid}"
    report_url = f"{FRONTEND_URL}/?stock={sid}&report=1"
    name_esc   = name.replace("'", "\\'")

    return (
        f'<div style="background:#0f172a;border:1px solid #1e293b;border-radius:16px;overflow:hidden;'
        f'transition:border-color .2s" '
        f'onmouseenter="this.style.borderColor=\'#334155\'" onmouseleave="this.style.borderColor=\'#1e293b\'">'

        # 標題列（點擊跳轉 /?stock=SID）
        f'<div style="display:flex;align-items:center;gap:8px;padding:14px 16px 12px;'
        f'cursor:pointer;border-bottom:1px solid #1e293b;background:#0a0f1e" '
        f'onclick="window.top.location.href=\'{stock_url}\'">'
        f'<span style="font-size:17px;font-weight:800;color:#f1f5f9">{sid}</span>'
        f'<span style="font-size:13px;color:#64748b;flex:1">{name}</span>'
        f'<button id="wpick-{sid}" '
        f'onclick="event.stopPropagation();try{{window.parent.addWatch(\'{sid}\',\'{name_esc}\');'
        f'this.textContent=\'✓ 已加入\';this.style.color=\'#22c55e\'}}catch(e){{}}" '
        f'style="padding:3px 10px;background:#1e293b;border:1px solid #334155;border-radius:20px;'
        f'color:#94a3b8;font-size:11px;cursor:pointer;font-family:inherit;white-space:nowrap">+ 自選</button>'
        f'<span style="padding:3px 10px;border-radius:20px;background:{risk_bg};color:{risk_color};'
        f'font-size:11px;font-weight:700;white-space:nowrap">{risk_label}</span>'
        f'</div>'

        # 卡片主體
        f'<div style="padding:14px 16px;display:flex;flex-direction:column;gap:10px">'

        # 摘要一行
        f'<div style="font-size:12px;padding:8px 12px;background:#0a0f1e;border-radius:8px;'
        f'border-left:3px solid {rec_color};display:flex;gap:8px;flex-wrap:wrap;line-height:1.6">'
        f'<span style="color:{pos_color}">{pos_desc}</span>'
        f'<span style="color:#334155">|</span>'
        f'<span style="color:{kbar_color}">{kbar_dir}</span>'
        f'<span style="color:#334155">|</span>'
        f'<span style="color:{rec_color}">{rec_icon} {rec_core}</span>'
        f'</div>'

        # 條列資訊
        f'<div style="display:flex;flex-direction:column">'
        f'<div style="display:flex;justify-content:space-between;padding:6px 0;'
        f'border-bottom:.5px solid #1e293b;font-size:12px">'
        f'<span style="color:#64748b">K線型態</span>'
        f'<span style="color:#a78bfa;font-weight:600">{kline}'
        f'<span style="color:#475569;font-weight:400"> 勝率{wr_pct}%</span></span>'
        f'</div>'
        f'<div style="display:flex;justify-content:space-between;padding:6px 0;'
        f'border-bottom:.5px solid #1e293b;font-size:12px">'
        f'<span style="color:#64748b">防守位</span>'
        f'<span style="color:#e2e8f0;font-weight:600">{support}'
        f'<span style="color:#64748b;font-weight:400"> (-{stop_dist}%){rr_txt}</span></span>'
        f'</div>'
        f'<div style="display:flex;justify-content:space-between;padding:6px 0;'
        f'border-bottom:.5px solid #1e293b;font-size:12px">'
        f'<span style="color:#64748b">支撐 / 壓力</span>'
        f'<span><span style="color:#22c55e;font-weight:600">{support}</span>'
        f'<span style="color:#475569"> / </span>'
        f'<span style="color:#f59e0b;font-weight:600">{resistance}</span></span>'
        f'</div>'
        f'<div style="display:flex;justify-content:space-between;padding:6px 0;'
        f'border-bottom:.5px solid #1e293b;font-size:12px">'
        f'<span style="color:#64748b">趨勢</span>'
        f'<span style="color:{trend_c};font-weight:600">{trend}'
        f'<span style="color:#475569;font-weight:400">（{trend_desc}）</span></span>'
        f'</div>'
        f'<div style="display:flex;justify-content:space-between;padding:6px 0;font-size:12px">'
        f'<span style="color:#64748b">軌道位置</span>'
        f'<span style="color:#64748b;font-family:monospace;font-size:11px">{bar_html}'
        f'<span style="font-family:inherit;color:#475569"> {pos_pct}% {pos_label}</span></span>'
        f'</div>'
        f'</div>'

        # 完整個股報告按鈕
        f'<button onclick="window.top.location.href=\'{report_url}\'" class="btn-report">'
        f'📄 完整個股報告&nbsp;&nbsp;立即產出 →</button>'

        f'</div>'
        f'</div>'
    )


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
.btn-report{{width:100%;padding:10px 14px;background:#1e293b;border:1px solid #334155;border-radius:8px;
  color:#94a3b8;font-size:12px;cursor:pointer;text-align:left;display:flex;align-items:center;gap:6px;
  font-family:inherit;transition:.15s}}
.btn-report:hover{{background:#253347;border-color:#475569;color:#e2e8f0}}
.rpt-sec{{background:#0a0f1e;border:1px solid #1e293b;border-radius:8px;padding:12px}}
.rpt-title{{font-size:10px;font-weight:700;color:#475569;letter-spacing:.6px;margin-bottom:8px;text-transform:uppercase}}
.rpt-row{{display:flex;justify-content:space-between;align-items:center;padding:3px 0;font-size:12px;border-top:.5px solid #1e293b}}
.rpt-row:first-of-type{{border-top:none}}
.rpt-label{{color:#64748b}}
.rpt-val{{font-weight:600;color:#e2e8f0}}
@media(max-width:600px){{.grid{{grid-template-columns:1fr}}}}
</style>
<script>
function toggleReport(id){{
  var el=document.getElementById('rpt-'+id);
  var btn=document.getElementById('btn-'+id);
  if(el.style.display==='none'){{
    el.style.display='block';
    btn.innerHTML='▲ 收合報告';
    btn.style.color='#64748b';
  }}else{{
    el.style.display='none';
    btn.innerHTML='📄 完整個股報告&nbsp;&nbsp;立即產出 →';
    btn.style.color='#94a3b8';
  }}
}}
</script>
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
