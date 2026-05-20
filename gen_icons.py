from PIL import Image, ImageDraw, ImageFont
import math, os

FONT_PATH = "C:/Windows/Fonts/msjh.ttc"
OUT_DIR = "frontend"

BG      = "#1a1a2e"
WHITE   = "#ffffff"
GRAY    = "#a0a0b8"
RED     = "#ef4444"
RED_VOL = "#ef4444"

def rounded_rect_mask(size, radius):
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, size[0]-1, size[1]-1], radius=radius, fill=255)
    return mask

def make_icon(px):
    img = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    bg  = Image.new("RGBA", (px, px), BG)
    r   = int(px * 0.18)
    mask = rounded_rect_mask((px, px), r)
    img.paste(bg, mask=mask)
    draw = ImageDraw.Draw(img)

    s = px / 192  # scale factor

    # ── 上方大字「線上有位」──────────────────────────────────
    fs_big  = int(28 * s)
    fs_sub  = int(11 * s)
    fs_bot  = int(10 * s)
    try:
        font_big = ImageFont.truetype(FONT_PATH, fs_big)
        font_sub = ImageFont.truetype(FONT_PATH, fs_sub)
        font_bot = ImageFont.truetype(FONT_PATH, fs_bot)
    except Exception:
        font_big = font_sub = font_bot = ImageFont.load_default()

    title = "線上有位"
    bbox  = draw.textbbox((0, 0), title, font=font_big)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    tx = (px - tw) // 2
    ty = int(12 * s)
    draw.text((tx, ty), title, font=font_big, fill=WHITE)

    # ── 副標「softglow-ai.com」────────────────────────────────
    sub = "softglow-ai.com"
    sbbox = draw.textbbox((0, 0), sub, font=font_sub)
    sw = sbbox[2]-sbbox[0]
    sy = ty + th + int(4 * s)
    draw.text(((px - sw) // 2, sy), sub, font=font_sub, fill=GRAY)

    # ── 走勢折線區域 ─────────────────────────────────────────
    chart_top    = sy + int(fs_sub * 1.6) + int(6 * s)
    chart_bottom = px - int(30 * s)   # 留給底部文字
    chart_left   = int(14 * s)
    chart_right  = px - int(14 * s)
    chart_w      = chart_right - chart_left
    chart_h      = chart_bottom - chart_top

    vol_h_max = int(chart_h * 0.28)   # 量能柱最大高度
    line_bottom = chart_bottom - vol_h_max - int(6 * s)
    line_top    = chart_top + int(4 * s)
    line_h      = line_bottom - line_top

    # 走勢折點（模擬股價，從左下往右上，有起伏）
    pts_norm = [
        (0.00, 0.82), (0.10, 0.70), (0.18, 0.75), (0.28, 0.58),
        (0.38, 0.62), (0.48, 0.44), (0.58, 0.50), (0.68, 0.32),
        (0.78, 0.38), (0.88, 0.20), (1.00, 0.10),
    ]
    pts = [
        (chart_left + int(x * chart_w), line_top + int(y * line_h))
        for x, y in pts_norm
    ]
    lw = max(2, int(2.5 * s))
    draw.line(pts, fill=RED, width=lw, joint="curve")
    # 最後一點畫小圓點
    last = pts[-1]
    dot_r = max(2, int(3 * s))
    draw.ellipse([last[0]-dot_r, last[1]-dot_r, last[0]+dot_r, last[1]+dot_r], fill=RED)

    # ── 量能柱 ────────────────────────────────────────────────
    n_bars = 10
    bar_gap = int(3 * s)
    bar_total_w = chart_w - bar_gap
    bar_w = max(2, bar_total_w // n_bars - bar_gap)
    vol_heights = [0.25, 0.30, 0.35, 0.45, 0.40, 0.55, 0.60, 0.70, 0.80, 1.00]
    for i, vh in enumerate(vol_heights):
        bx = chart_left + i * (bar_w + bar_gap)
        bh = int(vol_h_max * vh)
        by_top  = chart_bottom - bh
        by_bot  = chart_bottom
        alpha = int(180 + 75 * vh)
        draw.rectangle([bx, by_top, bx + bar_w, by_bot],
                       fill=(*bytes.fromhex(RED[1:]), alpha))

    # ── 底部文字 ──────────────────────────────────────────────
    bot_text = "▲ 股市位置導航系統"
    bbbox = draw.textbbox((0, 0), bot_text, font=font_bot)
    bw = bbbox[2]-bbbox[0]
    draw.text(((px - bw) // 2, px - int(18 * s)), bot_text, font=font_bot, fill=GRAY)

    return img

for size in (192, 512):
    icon = make_icon(size)
    path = os.path.join(OUT_DIR, f"icon-{size}.png")
    icon.save(path, "PNG")
    print(f"saved {path}  ({size}x{size})")

favicon = make_icon(32)
fav_path = os.path.join(OUT_DIR, "favicon.ico")
favicon.save(fav_path, "ICO", sizes=[(32, 32)])
print(f"saved {fav_path}  (32x32)")
