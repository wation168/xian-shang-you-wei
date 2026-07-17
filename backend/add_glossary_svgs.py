#!/usr/bin/env python3
"""
add_glossary_svgs.py
為所有 Glossary 頁面加入分類對應的 SVG 概念圖
不需 API，零費用，純本機執行

Usage:
  cd D:\\xian-shang-you-wei\\backend
  python add_glossary_svgs.py
"""

import os, re
from pathlib import Path

GLOSSARY_DIR = Path("frontend/glossary")

COLORS = {
    "blue": "#2563EB", "blue_light": "#EBF5FF", "blue_dark": "#1D4ED8",
    "green": "#38A169", "green_light": "#F0FFF4",
    "red": "#E53E3E", "red_light": "#FFF5F5",
    "orange": "#DD6B20", "orange_light": "#FFFAF0",
    "purple": "#7C3AED", "purple_light": "#FAF5FF",
    "gray": "#718096", "gray_light": "#F7FAFC",
    "dark": "#2D3748", "bg": "#fff",
    "yellow": "#D69E2E", "teal": "#319795",
}

# ── SVG 模板（按分類）──────────────────────────────

def svg_investment_basics(slug):
    """成長曲線：複利 vs 單利"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">Compound vs Simple Growth</text>
  <!-- Axes -->
  <line x1="60" y1="245" x2="560" y2="245" stroke="#CBD5E0" stroke-width="1.5"/>
  <line x1="60" y1="45" x2="60" y2="245" stroke="#CBD5E0" stroke-width="1.5"/>
  <text x="310" y="270" text-anchor="middle" fill="{COLORS['gray']}" font-size="11">Time (Years)</text>
  <text x="25" y="145" text-anchor="middle" fill="{COLORS['gray']}" font-size="11" transform="rotate(-90,25,145)">Value</text>
  <!-- Grid lines -->
  <line x1="60" y1="145" x2="560" y2="145" stroke="#EDF2F7" stroke-dasharray="4"/>
  <line x1="60" y1="95" x2="560" y2="95" stroke="#EDF2F7" stroke-dasharray="4"/>
  <line x1="60" y1="195" x2="560" y2="195" stroke="#EDF2F7" stroke-dasharray="4"/>
  <!-- Simple interest (straight line) -->
  <line x1="60" y1="225" x2="540" y2="125" stroke="{COLORS['gray']}" stroke-width="2.5" stroke-dasharray="6,4"/>
  <!-- Compound interest (curve) -->
  <path d="M60,225 Q200,210 300,175 Q400,130 460,80 Q500,55 540,40" fill="none" stroke="{COLORS['blue']}" stroke-width="3"/>
  <!-- Labels -->
  <circle cx="430" cy="68" r="4" fill="{COLORS['blue']}"/>
  <text x="440" y="72" fill="{COLORS['blue']}" font-size="12" font-weight="600">Compound</text>
  <circle cx="430" cy="90" r="4" fill="{COLORS['gray']}"/>
  <text x="440" y="94" fill="{COLORS['gray']}" font-size="12">Simple</text>
  <!-- Year markers -->
  <text x="60" y="258" fill="{COLORS['gray']}" font-size="10">0</text>
  <text x="180" y="258" fill="{COLORS['gray']}" font-size="10">5</text>
  <text x="300" y="258" fill="{COLORS['gray']}" font-size="10">10</text>
  <text x="420" y="258" fill="{COLORS['gray']}" font-size="10">15</text>
  <text x="535" y="258" fill="{COLORS['gray']}" font-size="10">20</text>
</svg>'''

def svg_stock_trading(slug):
    """股價走勢圖"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">Stock Price Movement</text>
  <line x1="50" y1="245" x2="570" y2="245" stroke="#CBD5E0" stroke-width="1.5"/>
  <line x1="50" y1="40" x2="50" y2="245" stroke="#CBD5E0" stroke-width="1.5"/>
  <!-- Candlesticks -->
  <line x1="90" y1="120" x2="90" y2="190" stroke="{COLORS['green']}" stroke-width="1.5"/>
  <rect x="82" y="140" width="16" height="35" fill="{COLORS['green']}" rx="1"/>
  <line x1="140" y1="100" x2="140" y2="180" stroke="{COLORS['green']}" stroke-width="1.5"/>
  <rect x="132" y="115" width="16" height="45" fill="{COLORS['green']}" rx="1"/>
  <line x1="190" y1="85" x2="190" y2="160" stroke="{COLORS['green']}" stroke-width="1.5"/>
  <rect x="182" y="95" width="16" height="40" fill="{COLORS['green']}" rx="1"/>
  <line x1="240" y1="75" x2="240" y2="140" stroke="{COLORS['red']}" stroke-width="1.5"/>
  <rect x="232" y="85" width="16" height="35" fill="{COLORS['red']}" rx="1"/>
  <line x1="290" y1="95" x2="290" y2="165" stroke="{COLORS['red']}" stroke-width="1.5"/>
  <rect x="282" y="110" width="16" height="40" fill="{COLORS['red']}" rx="1"/>
  <line x1="340" y1="105" x2="340" y2="175" stroke="{COLORS['red']}" stroke-width="1.5"/>
  <rect x="332" y="125" width="16" height="30" fill="{COLORS['red']}" rx="1"/>
  <line x1="390" y1="100" x2="390" y2="170" stroke="{COLORS['green']}" stroke-width="1.5"/>
  <rect x="382" y="110" width="16" height="40" fill="{COLORS['green']}" rx="1"/>
  <line x1="440" y1="80" x2="440" y2="145" stroke="{COLORS['green']}" stroke-width="1.5"/>
  <rect x="432" y="90" width="16" height="35" fill="{COLORS['green']}" rx="1"/>
  <line x1="490" y1="65" x2="490" y2="130" stroke="{COLORS['green']}" stroke-width="1.5"/>
  <rect x="482" y="75" width="16" height="35" fill="{COLORS['green']}" rx="1"/>
  <!-- Volume bars -->
  <rect x="82" y="228" width="16" height="17" fill="{COLORS['green']}" opacity="0.4" rx="1"/>
  <rect x="132" y="220" width="16" height="25" fill="{COLORS['green']}" opacity="0.4" rx="1"/>
  <rect x="182" y="215" width="16" height="30" fill="{COLORS['green']}" opacity="0.4" rx="1"/>
  <rect x="232" y="225" width="16" height="20" fill="{COLORS['red']}" opacity="0.4" rx="1"/>
  <rect x="282" y="230" width="16" height="15" fill="{COLORS['red']}" opacity="0.4" rx="1"/>
  <rect x="332" y="232" width="16" height="13" fill="{COLORS['red']}" opacity="0.4" rx="1"/>
  <rect x="382" y="222" width="16" height="23" fill="{COLORS['green']}" opacity="0.4" rx="1"/>
  <rect x="432" y="210" width="16" height="35" fill="{COLORS['green']}" opacity="0.4" rx="1"/>
  <rect x="482" y="205" width="16" height="40" fill="{COLORS['green']}" opacity="0.4" rx="1"/>
</svg>'''

def svg_technical_analysis(slug):
    """RSI / MACD 指標圖"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">Technical Indicator Zones</text>
  <line x1="50" y1="245" x2="570" y2="245" stroke="#CBD5E0" stroke-width="1.5"/>
  <line x1="50" y1="40" x2="50" y2="245" stroke="#CBD5E0" stroke-width="1.5"/>
  <!-- Overbought zone -->
  <rect x="50" y="40" width="520" height="55" fill="{COLORS['red']}" opacity="0.08"/>
  <line x1="50" y1="95" x2="570" y2="95" stroke="{COLORS['red']}" stroke-dasharray="5,3" opacity="0.6"/>
  <text x="565" y="90" text-anchor="end" fill="{COLORS['red']}" font-size="11" font-weight="600">70 (Overbought)</text>
  <!-- Oversold zone -->
  <rect x="50" y="190" width="520" height="55" fill="{COLORS['green']}" opacity="0.08"/>
  <line x1="50" y1="190" x2="570" y2="190" stroke="{COLORS['green']}" stroke-dasharray="5,3" opacity="0.6"/>
  <text x="565" y="205" text-anchor="end" fill="{COLORS['green']}" font-size="11" font-weight="600">30 (Oversold)</text>
  <!-- Center line -->
  <line x1="50" y1="142" x2="570" y2="142" stroke="#CBD5E0" stroke-dasharray="3"/>
  <text x="565" y="140" text-anchor="end" fill="{COLORS['gray']}" font-size="10">50</text>
  <!-- RSI curve -->
  <path d="M60,142 Q90,130 120,110 Q150,80 180,65 Q210,55 230,70 Q260,95 290,142 Q310,170 340,195 Q360,210 380,205 Q410,185 430,142 Q450,110 470,90 Q490,75 510,85 Q530,100 550,120" fill="none" stroke="{COLORS['blue']}" stroke-width="2.5"/>
  <!-- Signal dots -->
  <circle cx="180" cy="65" r="5" fill="{COLORS['red']}" opacity="0.8"/>
  <text x="180" y="53" text-anchor="middle" fill="{COLORS['red']}" font-size="10">Sell</text>
  <circle cx="340" cy="195" r="5" fill="{COLORS['green']}" opacity="0.8"/>
  <text x="340" y="220" text-anchor="middle" fill="{COLORS['green']}" font-size="10">Buy</text>
</svg>'''

def svg_bonds(slug):
    """殖利率曲線"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">Yield Curve</text>
  <line x1="60" y1="240" x2="560" y2="240" stroke="#CBD5E0" stroke-width="1.5"/>
  <line x1="60" y1="45" x2="60" y2="240" stroke="#CBD5E0" stroke-width="1.5"/>
  <text x="310" y="268" text-anchor="middle" fill="{COLORS['gray']}" font-size="11">Maturity</text>
  <text x="25" y="142" text-anchor="middle" fill="{COLORS['gray']}" font-size="11" transform="rotate(-90,25,142)">Yield %</text>
  <!-- Normal yield curve -->
  <path d="M80,210 Q150,180 250,140 Q350,110 450,95 Q520,88 550,85" fill="none" stroke="{COLORS['blue']}" stroke-width="3"/>
  <!-- Inverted yield curve -->
  <path d="M80,120 Q150,135 250,155 Q350,175 450,190 Q520,195 550,198" fill="none" stroke="{COLORS['red']}" stroke-width="2.5" stroke-dasharray="6,4"/>
  <!-- Labels -->
  <circle cx="420" cy="55" r="4" fill="{COLORS['blue']}"/>
  <text x="430" y="59" fill="{COLORS['blue']}" font-size="12" font-weight="500">Normal</text>
  <circle cx="420" cy="73" r="4" fill="{COLORS['red']}"/>
  <text x="430" y="77" fill="{COLORS['red']}" font-size="12" font-weight="500">Inverted</text>
  <!-- Time labels -->
  <text x="80" y="255" fill="{COLORS['gray']}" font-size="10">3M</text>
  <text x="175" y="255" fill="{COLORS['gray']}" font-size="10">1Y</text>
  <text x="290" y="255" fill="{COLORS['gray']}" font-size="10">5Y</text>
  <text x="420" y="255" fill="{COLORS['gray']}" font-size="10">10Y</text>
  <text x="535" y="255" fill="{COLORS['gray']}" font-size="10">30Y</text>
</svg>'''

def svg_funds_etf(slug):
    """資產配置圓餅圖"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">Portfolio Allocation</text>
  <!-- Pie chart -->
  <circle cx="220" cy="155" r="95" fill="none" stroke="#E2E8F0" stroke-width="30"/>
  <circle cx="220" cy="155" r="95" fill="none" stroke="{COLORS['blue']}" stroke-width="30" stroke-dasharray="240 357" stroke-dashoffset="0" transform="rotate(-90 220 155)"/>
  <circle cx="220" cy="155" r="95" fill="none" stroke="{COLORS['green']}" stroke-width="30" stroke-dasharray="120 477" stroke-dashoffset="-240" transform="rotate(-90 220 155)"/>
  <circle cx="220" cy="155" r="95" fill="none" stroke="{COLORS['orange']}" stroke-width="30" stroke-dasharray="60 537" stroke-dashoffset="-360" transform="rotate(-90 220 155)"/>
  <circle cx="220" cy="155" r="95" fill="none" stroke="{COLORS['purple']}" stroke-width="30" stroke-dasharray="50 547" stroke-dashoffset="-420" transform="rotate(-90 220 155)"/>
  <!-- Legend -->
  <rect x="380" y="80" width="16" height="16" rx="3" fill="{COLORS['blue']}"/>
  <text x="402" y="93" fill="{COLORS['dark']}" font-size="13">Stocks 40%</text>
  <rect x="380" y="110" width="16" height="16" rx="3" fill="{COLORS['green']}"/>
  <text x="402" y="123" fill="{COLORS['dark']}" font-size="13">Bonds 20%</text>
  <rect x="380" y="140" width="16" height="16" rx="3" fill="{COLORS['orange']}"/>
  <text x="402" y="153" fill="{COLORS['dark']}" font-size="13">Real Estate 10%</text>
  <rect x="380" y="170" width="16" height="16" rx="3" fill="{COLORS['purple']}"/>
  <text x="402" y="183" fill="{COLORS['dark']}" font-size="13">Alternatives 8%</text>
  <rect x="380" y="200" width="16" height="16" rx="3" fill="#E2E8F0"/>
  <text x="402" y="213" fill="{COLORS['dark']}" font-size="13">Cash 22%</text>
</svg>'''

def svg_real_estate(slug):
    """房貸本金 vs 利息"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">Mortgage: Principal vs Interest Over Time</text>
  <line x1="60" y1="240" x2="560" y2="240" stroke="#CBD5E0" stroke-width="1.5"/>
  <!-- Stacked area -->
  <path d="M80,240 L80,100 Q200,120 320,160 Q440,200 540,235 L540,240 Z" fill="{COLORS['blue']}" opacity="0.3"/>
  <path d="M80,100 Q200,120 320,160 Q440,200 540,235" fill="none" stroke="{COLORS['blue']}" stroke-width="2"/>
  <path d="M80,240 L80,200 Q200,170 320,140 Q440,100 540,60 L540,235 Q440,200 320,160 Q200,120 80,100 Z" fill="{COLORS['green']}" opacity="0.3"/>
  <!-- Labels -->
  <rect x="380" y="56" width="14" height="14" rx="3" fill="{COLORS['blue']}" opacity="0.5"/>
  <text x="400" y="67" fill="{COLORS['dark']}" font-size="12">Interest</text>
  <rect x="380" y="76" width="14" height="14" rx="3" fill="{COLORS['green']}" opacity="0.5"/>
  <text x="400" y="87" fill="{COLORS['dark']}" font-size="12">Principal</text>
  <text x="80" y="258" fill="{COLORS['gray']}" font-size="10">Year 1</text>
  <text x="300" y="258" fill="{COLORS['gray']}" font-size="10">Year 15</text>
  <text x="520" y="258" fill="{COLORS['gray']}" font-size="10">Year 30</text>
</svg>'''

def svg_loans_credit(slug):
    """貸款還款時間軸"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">Debt Payoff: Avalanche vs Snowball</text>
  <line x1="60" y1="240" x2="560" y2="240" stroke="#CBD5E0" stroke-width="1.5"/>
  <line x1="60" y1="45" x2="60" y2="240" stroke="#CBD5E0" stroke-width="1.5"/>
  <!-- Avalanche (faster, saves more interest) -->
  <path d="M80,60 Q150,65 220,85 Q300,120 380,160 Q440,195 480,230 L480,240" fill="none" stroke="{COLORS['blue']}" stroke-width="3"/>
  <!-- Snowball (slower) -->
  <path d="M80,60 Q160,68 240,95 Q320,135 400,175 Q460,210 530,235 L530,240" fill="none" stroke="{COLORS['orange']}" stroke-width="2.5" stroke-dasharray="6,4"/>
  <!-- Savings area -->
  <path d="M480,230 Q500,238 530,235 L530,240 L480,240 Z" fill="{COLORS['green']}" opacity="0.3"/>
  <text x="505" y="232" text-anchor="middle" fill="{COLORS['green']}" font-size="9" font-weight="600">Saved</text>
  <!-- Labels -->
  <text x="25" y="145" text-anchor="middle" fill="{COLORS['gray']}" font-size="11" transform="rotate(-90,25,145)">Remaining Debt</text>
  <circle cx="400" cy="55" r="4" fill="{COLORS['blue']}"/>
  <text x="410" y="59" fill="{COLORS['blue']}" font-size="12" font-weight="500">Avalanche</text>
  <circle cx="400" cy="73" r="4" fill="{COLORS['orange']}"/>
  <text x="410" y="77" fill="{COLORS['orange']}" font-size="12" font-weight="500">Snowball</text>
</svg>'''

def svg_insurance(slug):
    """保險保障金字塔"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">Insurance Coverage Pyramid</text>
  <!-- Pyramid layers -->
  <polygon points="300,50 180,130 420,130" fill="{COLORS['purple']}" opacity="0.2" stroke="{COLORS['purple']}" stroke-width="1.5"/>
  <text x="300" y="105" text-anchor="middle" fill="{COLORS['purple']}" font-size="12" font-weight="600">Life Insurance</text>
  <polygon points="180,130 130,175 470,175 420,130" fill="{COLORS['blue']}" opacity="0.2" stroke="{COLORS['blue']}" stroke-width="1.5"/>
  <text x="300" y="160" text-anchor="middle" fill="{COLORS['blue']}" font-size="12" font-weight="600">Health Insurance</text>
  <polygon points="130,175 80,220 520,220 470,175" fill="{COLORS['green']}" opacity="0.2" stroke="{COLORS['green']}" stroke-width="1.5"/>
  <text x="300" y="205" text-anchor="middle" fill="{COLORS['green']}" font-size="12" font-weight="600">Property &amp; Auto</text>
  <polygon points="80,220 50,250 550,250 520,220" fill="{COLORS['teal']}" opacity="0.2" stroke="{COLORS['teal']}" stroke-width="1.5"/>
  <text x="300" y="242" text-anchor="middle" fill="{COLORS['teal']}" font-size="12" font-weight="600">Emergency Fund</text>
  <text x="560" y="60" text-anchor="end" fill="{COLORS['gray']}" font-size="10">Higher Priority ↑</text>
</svg>'''

def svg_tax(slug):
    """累進稅率階梯"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">Progressive Tax Brackets</text>
  <line x1="60" y1="245" x2="560" y2="245" stroke="#CBD5E0" stroke-width="1.5"/>
  <!-- Staircase -->
  <rect x="70" y="210" width="90" height="35" fill="{COLORS['green']}" opacity="0.6" rx="2"/>
  <text x="115" y="232" text-anchor="middle" fill="#fff" font-size="11" font-weight="600">10%</text>
  <rect x="160" y="175" width="90" height="70" fill="{COLORS['teal']}" opacity="0.6" rx="2"/>
  <text x="205" y="197" text-anchor="middle" fill="#fff" font-size="11" font-weight="600">12%</text>
  <rect x="250" y="140" width="90" height="105" fill="{COLORS['blue']}" opacity="0.6" rx="2"/>
  <text x="295" y="162" text-anchor="middle" fill="#fff" font-size="11" font-weight="600">22%</text>
  <rect x="340" y="105" width="90" height="140" fill="{COLORS['purple']}" opacity="0.6" rx="2"/>
  <text x="385" y="127" text-anchor="middle" fill="#fff" font-size="11" font-weight="600">24%</text>
  <rect x="430" y="70" width="90" height="175" fill="{COLORS['orange']}" opacity="0.6" rx="2"/>
  <text x="475" y="92" text-anchor="middle" fill="#fff" font-size="11" font-weight="600">32%</text>
  <text x="310" y="270" text-anchor="middle" fill="{COLORS['gray']}" font-size="11">Taxable Income →</text>
</svg>'''

def svg_retirement(slug):
    """退休儲蓄成長"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">Retirement Savings Growth</text>
  <line x1="60" y1="240" x2="560" y2="240" stroke="#CBD5E0" stroke-width="1.5"/>
  <line x1="60" y1="45" x2="60" y2="240" stroke="#CBD5E0" stroke-width="1.5"/>
  <!-- Accumulation phase -->
  <path d="M70,235 Q150,225 230,200 Q310,160 380,100 L380,240 L70,240 Z" fill="{COLORS['blue']}" opacity="0.15"/>
  <path d="M70,235 Q150,225 230,200 Q310,160 380,100" fill="none" stroke="{COLORS['blue']}" stroke-width="2.5"/>
  <!-- Distribution phase -->
  <path d="M380,100 Q430,110 470,135 Q510,170 550,220 L550,240 L380,240 Z" fill="{COLORS['orange']}" opacity="0.15"/>
  <path d="M380,100 Q430,110 470,135 Q510,170 550,220" fill="none" stroke="{COLORS['orange']}" stroke-width="2.5" stroke-dasharray="6,4"/>
  <!-- Retirement line -->
  <line x1="380" y1="45" x2="380" y2="240" stroke="{COLORS['red']}" stroke-dasharray="4" opacity="0.6"/>
  <text x="380" y="55" text-anchor="middle" fill="{COLORS['red']}" font-size="11" font-weight="600">Retirement</text>
  <text x="200" y="255" text-anchor="middle" fill="{COLORS['blue']}" font-size="11">Accumulation</text>
  <text x="470" y="255" text-anchor="middle" fill="{COLORS['orange']}" font-size="11">Distribution</text>
</svg>'''

def svg_macro(slug):
    """經濟週期"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">Business Cycle</text>
  <line x1="40" y1="200" x2="570" y2="200" stroke="#CBD5E0" stroke-width="1" stroke-dasharray="4"/>
  <text x="575" y="204" fill="{COLORS['gray']}" font-size="10">Trend</text>
  <!-- Cycle wave -->
  <path d="M50,200 Q100,120 170,90 Q240,60 280,100 Q320,145 360,200 Q400,250 450,240 Q500,230 530,180 Q545,150 560,130" fill="none" stroke="{COLORS['blue']}" stroke-width="3"/>
  <!-- Phase labels -->
  <text x="120" y="78" text-anchor="middle" fill="{COLORS['green']}" font-size="12" font-weight="600">Expansion</text>
  <text x="230" y="55" text-anchor="middle" fill="{COLORS['blue']}" font-size="12" font-weight="600">Peak</text>
  <text x="360" y="225" text-anchor="middle" fill="{COLORS['red']}" font-size="12" font-weight="600">Recession</text>
  <text x="450" y="250" text-anchor="middle" fill="{COLORS['orange']}" font-size="12" font-weight="600">Trough</text>
  <text x="530" y="120" text-anchor="middle" fill="{COLORS['green']}" font-size="12" font-weight="600">Recovery</text>
</svg>'''

def svg_risk_management(slug):
    """風險報酬比"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">Risk vs Reward</text>
  <line x1="60" y1="240" x2="560" y2="240" stroke="#CBD5E0" stroke-width="1.5"/>
  <line x1="60" y1="45" x2="60" y2="240" stroke="#CBD5E0" stroke-width="1.5"/>
  <text x="310" y="268" text-anchor="middle" fill="{COLORS['gray']}" font-size="11">Risk →</text>
  <text x="25" y="145" text-anchor="middle" fill="{COLORS['gray']}" font-size="11" transform="rotate(-90,25,145)">Return →</text>
  <!-- Efficient frontier curve -->
  <path d="M100,210 Q140,170 190,140 Q250,110 320,90 Q400,72 480,62" fill="none" stroke="{COLORS['blue']}" stroke-width="2.5"/>
  <!-- Asset dots -->
  <circle cx="120" cy="200" r="8" fill="{COLORS['green']}" opacity="0.7"/>
  <text x="120" y="222" text-anchor="middle" fill="{COLORS['green']}" font-size="10">Bonds</text>
  <circle cx="250" cy="118" r="8" fill="{COLORS['blue']}" opacity="0.7"/>
  <text x="250" y="138" text-anchor="middle" fill="{COLORS['blue']}" font-size="10">Stocks</text>
  <circle cx="400" cy="76" r="8" fill="{COLORS['orange']}" opacity="0.7"/>
  <text x="400" y="96" text-anchor="middle" fill="{COLORS['orange']}" font-size="10">Crypto</text>
  <circle cx="180" cy="160" r="6" fill="{COLORS['purple']}" opacity="0.5"/>
  <text x="180" y="180" text-anchor="middle" fill="{COLORS['purple']}" font-size="9">REITs</text>
</svg>'''

def svg_corporate_finance(slug):
    """損益表瀑布圖"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">Income Statement Waterfall</text>
  <line x1="40" y1="245" x2="570" y2="245" stroke="#CBD5E0" stroke-width="1"/>
  <!-- Bars -->
  <rect x="65" y="60" width="60" height="180" fill="{COLORS['blue']}" opacity="0.7" rx="3"/>
  <text x="95" y="52" text-anchor="middle" fill="{COLORS['dark']}" font-size="10" font-weight="600">Revenue</text>
  <rect x="155" y="100" width="60" height="140" fill="{COLORS['red']}" opacity="0.5" rx="3"/>
  <text x="185" y="92" text-anchor="middle" fill="{COLORS['dark']}" font-size="10">COGS</text>
  <rect x="245" y="100" width="60" height="80" fill="{COLORS['green']}" opacity="0.6" rx="3"/>
  <text x="275" y="92" text-anchor="middle" fill="{COLORS['dark']}" font-size="10" font-weight="600">Gross Profit</text>
  <rect x="335" y="130" width="60" height="50" fill="{COLORS['red']}" opacity="0.4" rx="3"/>
  <text x="365" y="122" text-anchor="middle" fill="{COLORS['dark']}" font-size="10">OpEx</text>
  <rect x="425" y="130" width="60" height="40" fill="{COLORS['teal']}" opacity="0.6" rx="3"/>
  <text x="455" y="122" text-anchor="middle" fill="{COLORS['dark']}" font-size="10" font-weight="600">EBITDA</text>
  <rect x="515" y="155" width="50" height="30" fill="{COLORS['green']}" opacity="0.8" rx="3"/>
  <text x="540" y="147" text-anchor="middle" fill="{COLORS['dark']}" font-size="10" font-weight="600">Net Income</text>
</svg>'''

def svg_business(slug):
    """損益平衡圖"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">Break-Even Analysis</text>
  <line x1="60" y1="240" x2="560" y2="240" stroke="#CBD5E0" stroke-width="1.5"/>
  <line x1="60" y1="45" x2="60" y2="240" stroke="#CBD5E0" stroke-width="1.5"/>
  <!-- Fixed costs line -->
  <line x1="60" y1="180" x2="540" y2="180" stroke="{COLORS['orange']}" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="545" y="178" fill="{COLORS['orange']}" font-size="10">Fixed Costs</text>
  <!-- Total costs line -->
  <line x1="60" y1="180" x2="540" y2="80" stroke="{COLORS['red']}" stroke-width="2"/>
  <text x="545" y="78" fill="{COLORS['red']}" font-size="10">Total Costs</text>
  <!-- Revenue line -->
  <line x1="60" y1="240" x2="540" y2="50" stroke="{COLORS['green']}" stroke-width="2.5"/>
  <text x="545" y="48" fill="{COLORS['green']}" font-size="10">Revenue</text>
  <!-- Break-even point -->
  <circle cx="310" cy="130" r="7" fill="none" stroke="{COLORS['blue']}" stroke-width="2.5"/>
  <text x="310" y="118" text-anchor="middle" fill="{COLORS['blue']}" font-size="12" font-weight="700">Break-Even</text>
  <!-- Zones -->
  <text x="180" y="220" text-anchor="middle" fill="{COLORS['red']}" font-size="11" opacity="0.7">Loss Zone</text>
  <text x="440" y="90" text-anchor="middle" fill="{COLORS['green']}" font-size="11" opacity="0.7">Profit Zone</text>
</svg>'''

def svg_forex(slug):
    """匯率走勢"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">EUR/USD Exchange Rate</text>
  <line x1="50" y1="240" x2="560" y2="240" stroke="#CBD5E0" stroke-width="1.5"/>
  <line x1="50" y1="45" x2="50" y2="240" stroke="#CBD5E0" stroke-width="1.5"/>
  <!-- Rate line -->
  <path d="M70,160 L110,150 L150,155 L190,140 L230,120 L270,130 L310,125 L350,110 L390,115 L430,100 L470,108 L510,95 L540,90" fill="none" stroke="{COLORS['blue']}" stroke-width="2.5"/>
  <!-- Fill area -->
  <path d="M70,160 L110,150 L150,155 L190,140 L230,120 L270,130 L310,125 L350,110 L390,115 L430,100 L470,108 L510,95 L540,90 L540,240 L70,240 Z" fill="{COLORS['blue']}" opacity="0.08"/>
  <!-- Spread visualization -->
  <rect x="260" y="122" width="40" height="16" fill="{COLORS['orange']}" opacity="0.3" rx="2"/>
  <text x="280" y="133" text-anchor="middle" fill="{COLORS['orange']}" font-size="8" font-weight="600">Spread</text>
  <!-- Labels -->
  <text x="45" y="100" text-anchor="end" fill="{COLORS['gray']}" font-size="10">1.10</text>
  <text x="45" y="160" text-anchor="end" fill="{COLORS['gray']}" font-size="10">1.05</text>
  <text x="45" y="220" text-anchor="end" fill="{COLORS['gray']}" font-size="10">1.00</text>
</svg>'''

def svg_crypto(slug):
    """區塊鏈示意"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">Blockchain Structure</text>
  <!-- Block 1 -->
  <rect x="30" y="80" width="130" height="130" rx="8" fill="#fff" stroke="{COLORS['blue']}" stroke-width="2"/>
  <text x="95" y="105" text-anchor="middle" fill="{COLORS['blue']}" font-size="12" font-weight="700">Block #1</text>
  <line x1="45" y1="115" x2="145" y2="115" stroke="#E2E8F0"/>
  <text x="50" y="133" fill="{COLORS['gray']}" font-size="9">Hash: 0x3a7f...</text>
  <text x="50" y="150" fill="{COLORS['gray']}" font-size="9">Prev: 0x0000...</text>
  <text x="50" y="167" fill="{COLORS['gray']}" font-size="9">Tx: 5 transactions</text>
  <text x="50" y="184" fill="{COLORS['gray']}" font-size="9">Nonce: 48291</text>
  <!-- Arrow 1→2 -->
  <line x1="160" y1="145" x2="200" y2="145" stroke="{COLORS['blue']}" stroke-width="2" marker-end="url(#arrowhead)"/>
  <!-- Block 2 -->
  <rect x="200" y="80" width="130" height="130" rx="8" fill="#fff" stroke="{COLORS['green']}" stroke-width="2"/>
  <text x="265" y="105" text-anchor="middle" fill="{COLORS['green']}" font-size="12" font-weight="700">Block #2</text>
  <line x1="215" y1="115" x2="315" y2="115" stroke="#E2E8F0"/>
  <text x="220" y="133" fill="{COLORS['gray']}" font-size="9">Hash: 0x8b2e...</text>
  <text x="220" y="150" fill="{COLORS['gray']}" font-size="9">Prev: 0x3a7f...</text>
  <text x="220" y="167" fill="{COLORS['gray']}" font-size="9">Tx: 12 transactions</text>
  <text x="220" y="184" fill="{COLORS['gray']}" font-size="9">Nonce: 73105</text>
  <!-- Arrow 2→3 -->
  <line x1="330" y1="145" x2="370" y2="145" stroke="{COLORS['green']}" stroke-width="2"/>
  <!-- Block 3 -->
  <rect x="370" y="80" width="130" height="130" rx="8" fill="#fff" stroke="{COLORS['purple']}" stroke-width="2"/>
  <text x="435" y="105" text-anchor="middle" fill="{COLORS['purple']}" font-size="12" font-weight="700">Block #3</text>
  <line x1="385" y1="115" x2="485" y2="115" stroke="#E2E8F0"/>
  <text x="390" y="133" fill="{COLORS['gray']}" font-size="9">Hash: 0xf1c9...</text>
  <text x="390" y="150" fill="{COLORS['gray']}" font-size="9">Prev: 0x8b2e...</text>
  <text x="390" y="167" fill="{COLORS['gray']}" font-size="9">Tx: 8 transactions</text>
  <text x="390" y="184" fill="{COLORS['gray']}" font-size="9">Nonce: 15830</text>
  <!-- Arrow 3→... -->
  <text x="520" y="150" fill="{COLORS['gray']}" font-size="20">···</text>
  <text x="300" y="245" text-anchor="middle" fill="{COLORS['gray']}" font-size="11">Each block contains a hash of the previous block, forming an immutable chain</text>
</svg>'''

def svg_math_stats(slug):
    """常態分布鐘形曲線"""
    return f'''<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width:100%;height:auto;margin:24px 0;display:block">
  <rect width="600" height="280" rx="12" fill="{COLORS['gray_light']}" stroke="#E2E8F0"/>
  <text x="300" y="28" text-anchor="middle" fill="{COLORS['dark']}" font-size="14" font-weight="600">Normal Distribution (Bell Curve)</text>
  <line x1="40" y1="230" x2="560" y2="230" stroke="#CBD5E0" stroke-width="1.5"/>
  <!-- Bell curve -->
  <path d="M60,228 Q100,225 150,215 Q200,190 240,140 Q270,90 300,55 Q330,90 360,140 Q400,190 450,215 Q500,225 540,228" fill="{COLORS['blue']}" opacity="0.1" stroke="{COLORS['blue']}" stroke-width="2.5"/>
  <!-- Standard deviation markers -->
  <line x1="300" y1="45" x2="300" y2="230" stroke="{COLORS['dark']}" stroke-dasharray="3" opacity="0.4"/>
  <text x="300" y="248" text-anchor="middle" fill="{COLORS['dark']}" font-size="11" font-weight="600">μ (Mean)</text>
  <line x1="195" y1="165" x2="195" y2="230" stroke="{COLORS['blue']}" stroke-dasharray="3" opacity="0.4"/>
  <text x="195" y="248" text-anchor="middle" fill="{COLORS['blue']}" font-size="10">-1σ</text>
  <line x1="405" y1="165" x2="405" y2="230" stroke="{COLORS['blue']}" stroke-dasharray="3" opacity="0.4"/>
  <text x="405" y="248" text-anchor="middle" fill="{COLORS['blue']}" font-size="10">+1σ</text>
  <line x1="120" y1="215" x2="120" y2="230" stroke="{COLORS['gray']}" stroke-dasharray="3" opacity="0.4"/>
  <text x="120" y="248" text-anchor="middle" fill="{COLORS['gray']}" font-size="10">-2σ</text>
  <line x1="480" y1="215" x2="480" y2="230" stroke="{COLORS['gray']}" stroke-dasharray="3" opacity="0.4"/>
  <text x="480" y="248" text-anchor="middle" fill="{COLORS['gray']}" font-size="10">+2σ</text>
  <!-- Percentage labels -->
  <text x="248" y="190" text-anchor="middle" fill="{COLORS['blue']}" font-size="13" font-weight="700">34.1%</text>
  <text x="352" y="190" text-anchor="middle" fill="{COLORS['blue']}" font-size="13" font-weight="700">34.1%</text>
  <text x="158" y="215" text-anchor="middle" fill="{COLORS['gray']}" font-size="11">13.6%</text>
  <text x="442" y="215" text-anchor="middle" fill="{COLORS['gray']}" font-size="11">13.6%</text>
</svg>'''


# ── 分類對應 SVG 函式 ──────────────────────────────

CATEGORY_SVG = {
    "investment-basics": svg_investment_basics,
    "stock-trading": svg_stock_trading,
    "technical-analysis": svg_technical_analysis,
    "bonds": svg_bonds,
    "funds-etf": svg_funds_etf,
    "real-estate": svg_real_estate,
    "loans-credit": svg_loans_credit,
    "insurance": svg_insurance,
    "tax": svg_tax,
    "retirement": svg_retirement,
    "macro": svg_macro,
    "risk-management": svg_risk_management,
    "corporate-finance": svg_corporate_finance,
    "business": svg_business,
    "forex": svg_forex,
    "crypto": svg_crypto,
    "math-stats": svg_math_stats,
}

# ── 術語 → 分類映射（從 generate_glossary.py 複製 slug→cat）──

def load_term_categories():
    """從 generate_glossary.py 的 GLOSSARY_TERMS 讀取分類"""
    # 嘗試匯入
    try:
        sys_path_backup = __import__('sys').path[:]
        __import__('sys').path.insert(0, '.')
        from generate_glossary import GLOSSARY_TERMS
        __import__('sys').path[:] = sys_path_backup
        return {t["slug"]: t["cat"] for t in GLOSSARY_TERMS}
    except:
        pass
    # Fallback: 從檔名的 meta tag 推斷
    return {}


def detect_category_from_html(content):
    """從 HTML 內容偵測分類"""
    # 從 breadcrumb 或 category badge 偵測
    for cat in CATEGORY_SVG:
        # Check if category name appears in the page
        if f'"{cat}"' in content or f"'{cat}'" in content:
            return cat
    return None


# ── 主程式 ──────────────────────────────────────────

def main():
    print("=" * 60)
    print("Add SVG Illustrations to Glossary Pages")
    print(f"Source: {GLOSSARY_DIR}")
    print("=" * 60)

    # 載入分類映射
    term_cats = load_term_categories()

    added = 0
    skipped = 0
    errors = 0

    # 遍歷所有 HTML 檔案
    for root, dirs, files in os.walk(GLOSSARY_DIR):
        # 跳過 .cache
        if ".cache" in root:
            continue
        for fname in files:
            if not fname.endswith(".html"):
                continue

            filepath = os.path.join(root, fname)
            slug = fname.replace(".html", "")

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            # 已經有 SVG 的跳過
            if 'viewBox="0 0 600 280"' in content:
                skipped += 1
                continue

            # 找分類
            cat = term_cats.get(slug)
            if not cat:
                cat = detect_category_from_html(content)
            if not cat:
                cat = "investment-basics"  # 預設

            # 取得 SVG
            svg_func = CATEGORY_SVG.get(cat, svg_investment_basics)
            svg = svg_func(slug)

            # 插入位置：第一個 <article> 之後的第一個 </h2> 之後
            insert_pattern = r'(<article class="article">.*?</h2>\s*)'
            match = re.search(insert_pattern, content, re.DOTALL)
            if match:
                insert_pos = match.end()
                content = content[:insert_pos] + "\n" + svg + "\n" + content[insert_pos:]
            else:
                # Fallback: 在 ad-calc 之後插入
                fallback = content.find('id="ad-calc"')
                if fallback > 0:
                    end_div = content.find('</div>', fallback)
                    if end_div > 0:
                        insert_pos = end_div + 6
                        content = content[:insert_pos] + "\n" + svg + "\n" + content[insert_pos:]
                    else:
                        errors += 1
                        continue
                else:
                    errors += 1
                    continue

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            added += 1

    print(f"\nDone: {added} SVGs added | {skipped} already had SVG | {errors} errors")


if __name__ == "__main__":
    main()
