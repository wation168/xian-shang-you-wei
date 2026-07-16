#!/usr/bin/env python3
"""
SoftGlow converter 工具下拉選單修復
====================================
把所有 converter/轉換工具的 <input type="text"> 改成 <select> 下拉選單
同時修復 JS 中用 innerHTML 動態塞 option 的邏輯

用法：
  cd D:/xian-shang-you-wei
  python fix_converter_dropdowns.py --dry-run
  python fix_converter_dropdowns.py
"""

import os
import re
import sys
import argparse
from pathlib import Path

# ============================================================
# 專案路徑
# ============================================================
CANDIDATE_ROOTS = [
    r"D:\xian-shang-you-wei",
    r"C:\xian-shang-you-wei",
    os.path.expanduser("~/xian-shang-you-wei"),
    os.path.dirname(os.path.abspath(__file__)),
    os.getcwd(),
]

def find_project_root(override=None):
    if override and os.path.isdir(override):
        for sub in ["backend/frontend/tools", "frontend/tools"]:
            if os.path.isdir(os.path.join(override, sub)):
                return override
    for root in CANDIDATE_ROOTS:
        if os.path.isdir(os.path.join(root, "backend", "frontend", "tools")):
            return root
    print("❌ 找不到專案目錄，請用 --root 指定")
    sys.exit(1)

LANGS = ["zh-TW", "en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN"]

# ============================================================
# 每個 converter 工具的下拉選單定義
# key = input 的 id, value = {options, default_from, default_to}
# ============================================================

CURRENCY_OPTIONS = {
    "zh-TW": [
        ("USD", "美元 (USD)"), ("EUR", "歐元 (EUR)"), ("GBP", "英鎊 (GBP)"),
        ("JPY", "日圓 (JPY)"), ("TWD", "新台幣 (TWD)"), ("CNY", "人民幣 (CNY)"),
        ("KRW", "韓元 (KRW)"), ("AUD", "澳幣 (AUD)"), ("CAD", "加幣 (CAD)"),
        ("CHF", "瑞郎 (CHF)"), ("HKD", "港幣 (HKD)"), ("SGD", "新加坡幣 (SGD)"),
        ("NZD", "紐幣 (NZD)"), ("SEK", "瑞典克朗 (SEK)"), ("NOK", "挪威克朗 (NOK)"),
        ("INR", "印度盧比 (INR)"), ("BRL", "巴西雷亞爾 (BRL)"),
        ("MXN", "墨西哥披索 (MXN)"), ("ZAR", "南非蘭特 (ZAR)"),
        ("TRY", "土耳其里拉 (TRY)"), ("IDR", "印尼盾 (IDR)"),
    ],
    "zh-CN": [
        ("USD", "美元 (USD)"), ("EUR", "欧元 (EUR)"), ("GBP", "英镑 (GBP)"),
        ("JPY", "日元 (JPY)"), ("CNY", "人民币 (CNY)"), ("TWD", "新台币 (TWD)"),
        ("KRW", "韩元 (KRW)"), ("AUD", "澳元 (AUD)"), ("CAD", "加元 (CAD)"),
        ("CHF", "瑞郎 (CHF)"), ("HKD", "港币 (HKD)"), ("SGD", "新加坡元 (SGD)"),
        ("NZD", "纽元 (NZD)"), ("SEK", "瑞典克朗 (SEK)"), ("NOK", "挪威克朗 (NOK)"),
        ("INR", "印度卢比 (INR)"), ("BRL", "巴西雷亚尔 (BRL)"),
        ("MXN", "墨西哥比索 (MXN)"), ("ZAR", "南非兰特 (ZAR)"),
        ("TRY", "土耳其里拉 (TRY)"), ("IDR", "印尼盾 (IDR)"),
    ],
    "en": [
        ("USD", "US Dollar (USD)"), ("EUR", "Euro (EUR)"), ("GBP", "British Pound (GBP)"),
        ("JPY", "Japanese Yen (JPY)"), ("AUD", "Australian Dollar (AUD)"),
        ("CAD", "Canadian Dollar (CAD)"), ("CHF", "Swiss Franc (CHF)"),
        ("CNY", "Chinese Yuan (CNY)"), ("HKD", "Hong Kong Dollar (HKD)"),
        ("SGD", "Singapore Dollar (SGD)"), ("KRW", "Korean Won (KRW)"),
        ("TWD", "Taiwan Dollar (TWD)"), ("NZD", "New Zealand Dollar (NZD)"),
        ("SEK", "Swedish Krona (SEK)"), ("NOK", "Norwegian Krone (NOK)"),
        ("INR", "Indian Rupee (INR)"), ("BRL", "Brazilian Real (BRL)"),
        ("MXN", "Mexican Peso (MXN)"), ("ZAR", "South African Rand (ZAR)"),
        ("TRY", "Turkish Lira (TRY)"), ("IDR", "Indonesian Rupiah (IDR)"),
    ],
    "ja": [
        ("JPY", "日本円 (JPY)"), ("USD", "米ドル (USD)"), ("EUR", "ユーロ (EUR)"),
        ("GBP", "英ポンド (GBP)"), ("CNY", "中国元 (CNY)"), ("KRW", "韓国ウォン (KRW)"),
        ("AUD", "豪ドル (AUD)"), ("CAD", "カナダドル (CAD)"), ("CHF", "スイスフラン (CHF)"),
        ("HKD", "香港ドル (HKD)"), ("SGD", "シンガポールドル (SGD)"),
        ("TWD", "台湾ドル (TWD)"), ("NZD", "NZドル (NZD)"),
        ("SEK", "スウェーデンクローナ (SEK)"), ("NOK", "ノルウェークローネ (NOK)"),
        ("INR", "インドルピー (INR)"), ("BRL", "ブラジルレアル (BRL)"),
        ("MXN", "メキシコペソ (MXN)"), ("ZAR", "南アランド (ZAR)"),
        ("TRY", "トルコリラ (TRY)"), ("IDR", "インドネシアルピア (IDR)"),
    ],
    "ko": [
        ("KRW", "한국 원 (KRW)"), ("USD", "미국 달러 (USD)"), ("EUR", "유로 (EUR)"),
        ("GBP", "영국 파운드 (GBP)"), ("JPY", "일본 엔 (JPY)"), ("CNY", "중국 위안 (CNY)"),
        ("AUD", "호주 달러 (AUD)"), ("CAD", "캐나다 달러 (CAD)"),
        ("CHF", "스위스 프랑 (CHF)"), ("HKD", "홍콩 달러 (HKD)"),
        ("SGD", "싱가포르 달러 (SGD)"), ("TWD", "대만 달러 (TWD)"),
        ("NZD", "뉴질랜드 달러 (NZD)"), ("SEK", "스웨덴 크로나 (SEK)"),
        ("NOK", "노르웨이 크로네 (NOK)"), ("INR", "인도 루피 (INR)"),
        ("BRL", "브라질 레알 (BRL)"), ("MXN", "멕시코 페소 (MXN)"),
        ("ZAR", "남아공 랜드 (ZAR)"), ("TRY", "터키 리라 (TRY)"),
        ("IDR", "인도네시아 루피아 (IDR)"),
    ],
    "de": [
        ("EUR", "Euro (EUR)"), ("USD", "US-Dollar (USD)"), ("GBP", "Britisches Pfund (GBP)"),
        ("JPY", "Japanischer Yen (JPY)"), ("CHF", "Schweizer Franken (CHF)"),
        ("AUD", "Australischer Dollar (AUD)"), ("CAD", "Kanadischer Dollar (CAD)"),
        ("CNY", "Chinesischer Yuan (CNY)"), ("KRW", "Südkoreanischer Won (KRW)"),
        ("HKD", "Hongkong-Dollar (HKD)"), ("SGD", "Singapur-Dollar (SGD)"),
        ("TWD", "Taiwan-Dollar (TWD)"), ("NZD", "Neuseeland-Dollar (NZD)"),
        ("SEK", "Schwedische Krone (SEK)"), ("NOK", "Norwegische Krone (NOK)"),
        ("INR", "Indische Rupie (INR)"), ("BRL", "Brasilianischer Real (BRL)"),
        ("MXN", "Mexikanischer Peso (MXN)"), ("ZAR", "Südafrikanischer Rand (ZAR)"),
        ("TRY", "Türkische Lira (TRY)"), ("IDR", "Indonesische Rupiah (IDR)"),
    ],
    "fr": [
        ("EUR", "Euro (EUR)"), ("USD", "Dollar US (USD)"), ("GBP", "Livre sterling (GBP)"),
        ("JPY", "Yen japonais (JPY)"), ("CHF", "Franc suisse (CHF)"),
        ("AUD", "Dollar australien (AUD)"), ("CAD", "Dollar canadien (CAD)"),
        ("CNY", "Yuan chinois (CNY)"), ("KRW", "Won sud-coréen (KRW)"),
        ("HKD", "Dollar de Hong Kong (HKD)"), ("SGD", "Dollar de Singapour (SGD)"),
        ("TWD", "Dollar taïwanais (TWD)"), ("NZD", "Dollar néo-zélandais (NZD)"),
        ("SEK", "Couronne suédoise (SEK)"), ("NOK", "Couronne norvégienne (NOK)"),
        ("INR", "Roupie indienne (INR)"), ("BRL", "Réal brésilien (BRL)"),
        ("MXN", "Peso mexicain (MXN)"), ("ZAR", "Rand sud-africain (ZAR)"),
        ("TRY", "Livre turque (TRY)"), ("IDR", "Roupie indonésienne (IDR)"),
    ],
    "es": [
        ("EUR", "Euro (EUR)"), ("USD", "Dólar estadounidense (USD)"),
        ("GBP", "Libra esterlina (GBP)"), ("JPY", "Yen japonés (JPY)"),
        ("MXN", "Peso mexicano (MXN)"), ("AUD", "Dólar australiano (AUD)"),
        ("CAD", "Dólar canadiense (CAD)"), ("CHF", "Franco suizo (CHF)"),
        ("CNY", "Yuan chino (CNY)"), ("KRW", "Won surcoreano (KRW)"),
        ("HKD", "Dólar de Hong Kong (HKD)"), ("SGD", "Dólar de Singapur (SGD)"),
        ("TWD", "Dólar taiwanés (TWD)"), ("BRL", "Real brasileño (BRL)"),
        ("ZAR", "Rand sudafricano (ZAR)"), ("TRY", "Lira turca (TRY)"),
        ("INR", "Rupia india (INR)"), ("IDR", "Rupia indonesia (IDR)"),
    ],
    "pt": [
        ("BRL", "Real brasileiro (BRL)"), ("USD", "Dólar americano (USD)"),
        ("EUR", "Euro (EUR)"), ("GBP", "Libra esterlina (GBP)"),
        ("JPY", "Iene japonês (JPY)"), ("AUD", "Dólar australiano (AUD)"),
        ("CAD", "Dólar canadense (CAD)"), ("CHF", "Franco suíço (CHF)"),
        ("CNY", "Yuan chinês (CNY)"), ("KRW", "Won sul-coreano (KRW)"),
        ("HKD", "Dólar de Hong Kong (HKD)"), ("SGD", "Dólar de Singapura (SGD)"),
        ("TWD", "Dólar taiwanês (TWD)"), ("MXN", "Peso mexicano (MXN)"),
        ("ZAR", "Rand sul-africano (ZAR)"), ("TRY", "Lira turca (TRY)"),
        ("INR", "Rupia indiana (INR)"), ("IDR", "Rupia indonésia (IDR)"),
    ],
    "id": [
        ("IDR", "Rupiah Indonesia (IDR)"), ("USD", "Dolar AS (USD)"),
        ("EUR", "Euro (EUR)"), ("GBP", "Poundsterling (GBP)"),
        ("JPY", "Yen Jepang (JPY)"), ("AUD", "Dolar Australia (AUD)"),
        ("CAD", "Dolar Kanada (CAD)"), ("CHF", "Franc Swiss (CHF)"),
        ("CNY", "Yuan Tiongkok (CNY)"), ("KRW", "Won Korea (KRW)"),
        ("HKD", "Dolar Hong Kong (HKD)"), ("SGD", "Dolar Singapura (SGD)"),
        ("TWD", "Dolar Taiwan (TWD)"), ("BRL", "Real Brasil (BRL)"),
        ("MXN", "Peso Meksiko (MXN)"), ("ZAR", "Rand Afrika Selatan (ZAR)"),
        ("TRY", "Lira Turki (TRY)"), ("INR", "Rupee India (INR)"),
    ],
}

# 長度單位
LENGTH_OPTIONS = {
    "zh-TW": [("mm","毫米 (mm)"),("cm","公分 (cm)"),("m","公尺 (m)"),("km","公里 (km)"),("in","英寸 (in)"),("ft","英尺 (ft)"),("yd","碼 (yd)"),("mi","英里 (mi)")],
    "zh-CN": [("mm","毫米 (mm)"),("cm","厘米 (cm)"),("m","米 (m)"),("km","公里 (km)"),("in","英寸 (in)"),("ft","英尺 (ft)"),("yd","码 (yd)"),("mi","英里 (mi)")],
    "en": [("mm","Millimeter (mm)"),("cm","Centimeter (cm)"),("m","Meter (m)"),("km","Kilometer (km)"),("in","Inch (in)"),("ft","Foot (ft)"),("yd","Yard (yd)"),("mi","Mile (mi)")],
    "ja": [("mm","ミリメートル (mm)"),("cm","センチメートル (cm)"),("m","メートル (m)"),("km","キロメートル (km)"),("in","インチ (in)"),("ft","フィート (ft)"),("yd","ヤード (yd)"),("mi","マイル (mi)")],
    "ko": [("mm","밀리미터 (mm)"),("cm","센티미터 (cm)"),("m","미터 (m)"),("km","킬로미터 (km)"),("in","인치 (in)"),("ft","피트 (ft)"),("yd","야드 (yd)"),("mi","마일 (mi)")],
    "de": [("mm","Millimeter (mm)"),("cm","Zentimeter (cm)"),("m","Meter (m)"),("km","Kilometer (km)"),("in","Zoll (in)"),("ft","Fuß (ft)"),("yd","Yard (yd)"),("mi","Meile (mi)")],
    "fr": [("mm","Millimètre (mm)"),("cm","Centimètre (cm)"),("m","Mètre (m)"),("km","Kilomètre (km)"),("in","Pouce (in)"),("ft","Pied (ft)"),("yd","Yard (yd)"),("mi","Mile (mi)")],
    "es": [("mm","Milímetro (mm)"),("cm","Centímetro (cm)"),("m","Metro (m)"),("km","Kilómetro (km)"),("in","Pulgada (in)"),("ft","Pie (ft)"),("yd","Yarda (yd)"),("mi","Milla (mi)")],
    "pt": [("mm","Milímetro (mm)"),("cm","Centímetro (cm)"),("m","Metro (m)"),("km","Quilômetro (km)"),("in","Polegada (in)"),("ft","Pé (ft)"),("yd","Jarda (yd)"),("mi","Milha (mi)")],
    "id": [("mm","Milimeter (mm)"),("cm","Sentimeter (cm)"),("m","Meter (m)"),("km","Kilometer (km)"),("in","Inci (in)"),("ft","Kaki (ft)"),("yd","Yard (yd)"),("mi","Mil (mi)")],
}

# 重量單位
WEIGHT_OPTIONS = {
    "zh-TW": [("mg","毫克 (mg)"),("g","公克 (g)"),("kg","公斤 (kg)"),("oz","盎司 (oz)"),("lb","磅 (lb)"),("ton","公噸 (t)")],
    "zh-CN": [("mg","毫克 (mg)"),("g","克 (g)"),("kg","千克 (kg)"),("oz","盎司 (oz)"),("lb","磅 (lb)"),("ton","公吨 (t)")],
    "en": [("mg","Milligram (mg)"),("g","Gram (g)"),("kg","Kilogram (kg)"),("oz","Ounce (oz)"),("lb","Pound (lb)"),("ton","Metric Ton (t)")],
    "ja": [("mg","ミリグラム (mg)"),("g","グラム (g)"),("kg","キログラム (kg)"),("oz","オンス (oz)"),("lb","ポンド (lb)"),("ton","メートルトン (t)")],
    "ko": [("mg","밀리그램 (mg)"),("g","그램 (g)"),("kg","킬로그램 (kg)"),("oz","온스 (oz)"),("lb","파운드 (lb)"),("ton","미터톤 (t)")],
    "de": [("mg","Milligramm (mg)"),("g","Gramm (g)"),("kg","Kilogramm (kg)"),("oz","Unze (oz)"),("lb","Pfund (lb)"),("ton","Metrische Tonne (t)")],
    "fr": [("mg","Milligramme (mg)"),("g","Gramme (g)"),("kg","Kilogramme (kg)"),("oz","Once (oz)"),("lb","Livre (lb)"),("ton","Tonne métrique (t)")],
    "es": [("mg","Miligramo (mg)"),("g","Gramo (g)"),("kg","Kilogramo (kg)"),("oz","Onza (oz)"),("lb","Libra (lb)"),("ton","Tonelada métrica (t)")],
    "pt": [("mg","Miligrama (mg)"),("g","Grama (g)"),("kg","Quilograma (kg)"),("oz","Onça (oz)"),("lb","Libra (lb)"),("ton","Tonelada métrica (t)")],
    "id": [("mg","Miligram (mg)"),("g","Gram (g)"),("kg","Kilogram (kg)"),("oz","Ons (oz)"),("lb","Pon (lb)"),("ton","Metrik Ton (t)")],
}

# 溫度單位
TEMP_OPTIONS = {
    "zh-TW": [("C","攝氏 (°C)"),("F","華氏 (°F)"),("K","克耳文 (K)")],
    "zh-CN": [("C","摄氏 (°C)"),("F","华氏 (°F)"),("K","开尔文 (K)")],
    "en": [("C","Celsius (°C)"),("F","Fahrenheit (°F)"),("K","Kelvin (K)")],
    "ja": [("C","摂氏 (°C)"),("F","華氏 (°F)"),("K","ケルビン (K)")],
    "ko": [("C","섭씨 (°C)"),("F","화씨 (°F)"),("K","켈빈 (K)")],
    "de": [("C","Celsius (°C)"),("F","Fahrenheit (°F)"),("K","Kelvin (K)")],
    "fr": [("C","Celsius (°C)"),("F","Fahrenheit (°F)"),("K","Kelvin (K)")],
    "es": [("C","Celsius (°C)"),("F","Fahrenheit (°F)"),("K","Kelvin (K)")],
    "pt": [("C","Celsius (°C)"),("F","Fahrenheit (°F)"),("K","Kelvin (K)")],
    "id": [("C","Celsius (°C)"),("F","Fahrenheit (°F)"),("K","Kelvin (K)")],
}

# 體積單位
VOLUME_OPTIONS = {
    "zh-TW": [("ml","毫升 (mL)"),("l","公升 (L)"),("cup","杯 (cup)"),("floz","液量盎司 (fl oz)"),("tbsp","湯匙 (tbsp)"),("tsp","茶匙 (tsp)"),("gal","加侖 (gal)"),("pt","品脫 (pt)"),("qt","夸脫 (qt)"),("m3","立方公尺 (m³)")],
    "zh-CN": [("ml","毫升 (mL)"),("l","升 (L)"),("cup","杯 (cup)"),("floz","液量盎司 (fl oz)"),("tbsp","汤匙 (tbsp)"),("tsp","茶匙 (tsp)"),("gal","加仑 (gal)"),("pt","品脱 (pt)"),("qt","夸脱 (qt)"),("m3","立方米 (m³)")],
    "en": [("ml","Milliliter (mL)"),("l","Liter (L)"),("cup","Cup"),("floz","Fluid Ounce (fl oz)"),("tbsp","Tablespoon (tbsp)"),("tsp","Teaspoon (tsp)"),("gal","Gallon (gal)"),("pt","Pint (pt)"),("qt","Quart (qt)"),("m3","Cubic Meter (m³)")],
    "ja": [("ml","ミリリットル (mL)"),("l","リットル (L)"),("cup","カップ"),("floz","液量オンス (fl oz)"),("tbsp","大さじ"),("tsp","小さじ"),("gal","ガロン (gal)"),("pt","パイント (pt)"),("qt","クォート (qt)"),("m3","立方メートル (m³)")],
    "ko": [("ml","밀리리터 (mL)"),("l","리터 (L)"),("cup","컵"),("floz","액량 온스 (fl oz)"),("tbsp","큰술 (tbsp)"),("tsp","작은술 (tsp)"),("gal","갤런 (gal)"),("pt","파인트 (pt)"),("qt","쿼트 (qt)"),("m3","세제곱미터 (m³)")],
    "de": [("ml","Milliliter (mL)"),("l","Liter (L)"),("cup","Tasse (cup)"),("floz","Flüssigunze (fl oz)"),("tbsp","Esslöffel (EL)"),("tsp","Teelöffel (TL)"),("gal","Gallone (gal)"),("pt","Pinte (pt)"),("qt","Quart (qt)"),("m3","Kubikmeter (m³)")],
    "fr": [("ml","Millilitre (mL)"),("l","Litre (L)"),("cup","Tasse (cup)"),("floz","Once liquide (fl oz)"),("tbsp","Cuillère à soupe"),("tsp","Cuillère à café"),("gal","Gallon (gal)"),("pt","Pinte (pt)"),("qt","Quart (qt)"),("m3","Mètre cube (m³)")],
    "es": [("ml","Mililitro (mL)"),("l","Litro (L)"),("cup","Taza (cup)"),("floz","Onza líquida (fl oz)"),("tbsp","Cucharada (tbsp)"),("tsp","Cucharadita (tsp)"),("gal","Galón (gal)"),("pt","Pinta (pt)"),("qt","Cuarto (qt)"),("m3","Metro cúbico (m³)")],
    "pt": [("ml","Mililitro (mL)"),("l","Litro (L)"),("cup","Xícara (cup)"),("floz","Onça líquida (fl oz)"),("tbsp","Colher de sopa"),("tsp","Colher de chá"),("gal","Galão (gal)"),("pt_unit","Pinta (pt)"),("qt","Quarto (qt)"),("m3","Metro cúbico (m³)")],
    "id": [("ml","Mililiter (mL)"),("l","Liter (L)"),("cup","Cangkir (cup)"),("floz","Ons cairan (fl oz)"),("tbsp","Sendok makan (sdm)"),("tsp","Sendok teh (sdt)"),("gal","Galon (gal)"),("pt","Pint (pt)"),("qt","Kuart (qt)"),("m3","Meter kubik (m³)")],
}

# 房間形狀
SHAPE_OPTIONS = {
    "zh-TW": [("rectangle","長方形"),("square","正方形"),("triangle","三角形"),("circle","圓形"),("trapezoid","梯形")],
    "zh-CN": [("rectangle","长方形"),("square","正方形"),("triangle","三角形"),("circle","圆形"),("trapezoid","梯形")],
    "en": [("rectangle","Rectangle"),("square","Square"),("triangle","Triangle"),("circle","Circle"),("trapezoid","Trapezoid")],
    "ja": [("rectangle","長方形"),("square","正方形"),("triangle","三角形"),("circle","円形"),("trapezoid","台形")],
    "ko": [("rectangle","직사각형"),("square","정사각형"),("triangle","삼각형"),("circle","원형"),("trapezoid","사다리꼴")],
    "de": [("rectangle","Rechteck"),("square","Quadrat"),("triangle","Dreieck"),("circle","Kreis"),("trapezoid","Trapez")],
    "fr": [("rectangle","Rectangle"),("square","Carré"),("triangle","Triangle"),("circle","Cercle"),("trapezoid","Trapèze")],
    "es": [("rectangle","Rectángulo"),("square","Cuadrado"),("triangle","Triángulo"),("circle","Círculo"),("trapezoid","Trapecio")],
    "pt": [("rectangle","Retângulo"),("square","Quadrado"),("triangle","Triângulo"),("circle","Círculo"),("trapezoid","Trapézio")],
    "id": [("rectangle","Persegi Panjang"),("square","Persegi"),("triangle","Segitiga"),("circle","Lingkaran"),("trapezoid","Trapesium")],
}

# 油耗單位
FUEL_OPTIONS = {
    "zh-TW": [("kml","公里/公升 (km/L)"),("l100","公升/百公里 (L/100km)"),("mpg_us","英里/加侖 美制 (MPG)"),("mpg_uk","英里/加侖 英制 (MPG)")],
    "zh-CN": [("kml","公里/升 (km/L)"),("l100","升/百公里 (L/100km)"),("mpg_us","英里/加仑 美制 (MPG)"),("mpg_uk","英里/加仑 英制 (MPG)")],
    "en": [("kml","km/L"),("l100","L/100km"),("mpg_us","MPG (US)"),("mpg_uk","MPG (UK)")],
    "ja": [("kml","km/L"),("l100","L/100km"),("mpg_us","MPG（米国）"),("mpg_uk","MPG（英国）")],
    "ko": [("kml","km/L"),("l100","L/100km"),("mpg_us","MPG (미국)"),("mpg_uk","MPG (영국)")],
    "de": [("kml","km/L"),("l100","L/100km"),("mpg_us","MPG (US)"),("mpg_uk","MPG (UK)")],
    "fr": [("kml","km/L"),("l100","L/100km"),("mpg_us","MPG (US)"),("mpg_uk","MPG (UK)")],
    "es": [("kml","km/L"),("l100","L/100km"),("mpg_us","MPG (US)"),("mpg_uk","MPG (UK)")],
    "pt": [("kml","km/L"),("l100","L/100km"),("mpg_us","MPG (US)"),("mpg_uk","MPG (UK)")],
    "id": [("kml","km/L"),("l100","L/100km"),("mpg_us","MPG (US)"),("mpg_uk","MPG (UK)")],
}

# 時區
TIMEZONE_OPTIONS_ALL = [
    ("UTC-12","UTC-12 Baker Island"),("UTC-11","UTC-11 Samoa"),("UTC-10","UTC-10 Hawaii"),
    ("UTC-9","UTC-9 Alaska"),("UTC-8","UTC-8 Pacific (LA)"),("UTC-7","UTC-7 Mountain (Denver)"),
    ("UTC-6","UTC-6 Central (Chicago)"),("UTC-5","UTC-5 Eastern (NYC)"),
    ("UTC-4","UTC-4 Atlantic"),("UTC-3","UTC-3 São Paulo"),
    ("UTC-2","UTC-2"),("UTC-1","UTC-1 Azores"),
    ("UTC+0","UTC+0 London"),("UTC+1","UTC+1 Berlin/Paris"),
    ("UTC+2","UTC+2 Cairo"),("UTC+3","UTC+3 Moscow"),
    ("UTC+4","UTC+4 Dubai"),("UTC+5","UTC+5 Karachi"),
    ("UTC+5:30","UTC+5:30 Mumbai"),("UTC+6","UTC+6 Dhaka"),
    ("UTC+7","UTC+7 Bangkok/Jakarta"),("UTC+8","UTC+8 Taipei/Singapore"),
    ("UTC+9","UTC+9 Tokyo/Seoul"),("UTC+10","UTC+10 Sydney"),
    ("UTC+11","UTC+11 Solomon"),("UTC+12","UTC+12 Auckland"),
]

# ============================================================
# 每個 converter 工具要修哪些 input → select
# ============================================================
# 格式: "slug": { "input_id_pattern": OPTIONS_DICT, ... }
# input_id_pattern 用 regex 比對 id 屬性

TOOL_FIX_MAP = {
    "currency-converter": {
        "fields": [
            {"id_regex": r"fromCurren", "options_key": "CURRENCY", "default": "USD"},
            {"id_regex": r"toCurren", "options_key": "CURRENCY", "default": "TWD"},
        ],
        "remove_domcontentloaded_populate": True,  # 移除 JS 中動態塞 option 的舊碼
    },
    "length-converter": {
        "fields": [
            {"id_regex": r"from(?:Unit|Length)", "options_key": "LENGTH", "default": "m"},
            {"id_regex": r"to(?:Unit|Length)", "options_key": "LENGTH", "default": "km"},
        ],
    },
    "weight-converter": {
        "fields": [
            {"id_regex": r"from(?:Unit|Weight)", "options_key": "WEIGHT", "default": "kg"},
            {"id_regex": r"to(?:Unit|Weight)", "options_key": "WEIGHT", "default": "lb"},
        ],
    },
    "temperature-converter": {
        "fields": [
            {"id_regex": r"from(?:Unit|Temp)", "options_key": "TEMP", "default": "C"},
            {"id_regex": r"to(?:Unit|Temp)", "options_key": "TEMP", "default": "F"},
        ],
    },
    "volume-converter": {
        "fields": [
            {"id_regex": r"from(?:Unit|Volume)", "options_key": "VOLUME", "default": "ml"},
            {"id_regex": r"to(?:Unit|Volume)", "options_key": "VOLUME", "default": "l"},
        ],
    },
    "cooking-conversion": {
        "fields": [
            {"id_regex": r"from(?:Unit|Cook)", "options_key": "VOLUME", "default": "cup"},
            {"id_regex": r"to(?:Unit|Cook)", "options_key": "VOLUME", "default": "ml"},
        ],
    },
    "gas-mileage": {
        "fields": [
            {"id_regex": r"from(?:Unit|Fuel|Mileage)", "options_key": "FUEL", "default": "kml"},
            {"id_regex": r"to(?:Unit|Fuel|Mileage)", "options_key": "FUEL", "default": "l100"},
        ],
    },
    "fuel-cost": {
        "fields": [
            {"id_regex": r"(?:fuel|gas)(?:Unit|Type)", "options_key": "FUEL", "default": "kml"},
        ],
    },
    "timezone-converter": {
        "fields": [
            {"id_regex": r"from(?:Tz|Time|Zone)", "options_key": "TIMEZONE", "default": "UTC+8"},
            {"id_regex": r"to(?:Tz|Time|Zone)", "options_key": "TIMEZONE", "default": "UTC+0"},
        ],
    },
    "room-area": {
        "fields": [
            {"id_regex": r"(?:shape|roomShape|shapeSelect)", "options_key": "SHAPE", "default": "rectangle"},
        ],
    },
}

OPTIONS_MAP = {
    "CURRENCY": CURRENCY_OPTIONS,
    "LENGTH": LENGTH_OPTIONS,
    "WEIGHT": WEIGHT_OPTIONS,
    "TEMP": TEMP_OPTIONS,
    "VOLUME": VOLUME_OPTIONS,
    "SHAPE": SHAPE_OPTIONS,
    "FUEL": FUEL_OPTIONS,
    "TIMEZONE": {lang: TIMEZONE_OPTIONS_ALL for lang in LANGS},
}

# ============================================================
# 核心修復函式
# ============================================================

def build_select_html(element_id, options, default_val):
    """把 option list 組成 <select> HTML"""
    opts = []
    for val, label in options:
        sel = ' selected' if val == default_val else ''
        opts.append(f'<option value="{val}"{sel}>{label}</option>')
    return f'<select id="{element_id}" onchange="if(typeof calculate===\'function\')calculate()">{"".join(opts)}</select>'


def fix_file(filepath, lang, slug, tool_config, dry_run=False):
    """修復單一檔案"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    changes = []
    
    for field in tool_config.get("fields", []):
        id_regex = field["id_regex"]
        options_key = field["options_key"]
        default_val = field["default"]
        
        # 取得該語言的選項
        opts_dict = OPTIONS_MAP[options_key]
        options = opts_dict.get(lang, opts_dict.get("en", []))
        
        # 找到 <input type="text" id="XXX" ...> 並替換為 <select>
        # 支援各種 attribute 順序
        pattern = re.compile(
            r'<input\s+[^>]*?id=["\']([^"\']*?' + id_regex + r'[^"\']*?)["\'][^>]*?type=["\']text["\'][^>]*?>|'
            r'<input\s+[^>]*?type=["\']text["\'][^>]*?id=["\']([^"\']*?' + id_regex + r'[^"\']*?)["\'][^>]*?>',
            re.IGNORECASE
        )
        
        for match in pattern.finditer(content):
            element_id = match.group(1) or match.group(2)
            old_html = match.group(0)
            new_html = build_select_html(element_id, options, default_val)
            content = content.replace(old_html, new_html, 1)
            changes.append(f"  input#{element_id} → <select> ({len(options)} options)")
    
    # 移除 DOMContentLoaded 中動態塞 option 的舊碼（currency-converter 特有）
    if tool_config.get("remove_domcontentloaded_populate"):
        # 匹配整個 DOMContentLoaded 區塊（塞 currency option 的）
        dom_pattern = re.compile(
            r"window\.addEventListener\(['\"]DOMContentLoaded['\"],\s*function\s*\(\)\s*\{[^}]*?forEach\s*\(\s*(?:function\s*\(\s*curr\s*\)|curr\s*=>)\s*\{[^}]*?innerHTML[^}]*?\}[^}]*?\}\s*\)\s*;?",
            re.DOTALL
        )
        if dom_pattern.search(content):
            content = dom_pattern.sub("/* dropdown options now in HTML */", content)
            changes.append("  removed DOMContentLoaded option populator")
    
    if content != original:
        if not dry_run:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        return changes
    return []


def main():
    parser = argparse.ArgumentParser(description="修復 converter 工具下拉選單")
    parser.add_argument("--root", help="專案根目錄")
    parser.add_argument("--dry-run", action="store_true", help="只掃描不修改")
    args = parser.parse_args()
    
    project_root = find_project_root(args.root)
    
    # 找 frontend/tools 目錄
    tools_dir = os.path.join(project_root, "backend", "frontend", "tools")
    if not os.path.isdir(tools_dir):
        tools_dir = os.path.join(project_root, "frontend", "tools")
    
    print(f"{'='*60}")
    print(f"SoftGlow Converter 下拉選單修復")
    print(f"{'='*60}")
    print(f"專案路徑：{project_root}")
    print(f"工具目錄：{tools_dir}")
    print(f"模式：{'DRY-RUN（不修改）' if args.dry_run else '執行修復'}")
    print()
    
    total_fixed = 0
    total_scanned = 0
    
    for slug, config in TOOL_FIX_MAP.items():
        print(f"\n🔧 {slug}")
        
        for lang in LANGS:
            # 決定檔案路徑
            if lang == "zh-TW":
                filepath = os.path.join(tools_dir, f"{slug}.html")
            else:
                filepath = os.path.join(tools_dir, lang, f"{slug}.html")
            
            if not os.path.isfile(filepath):
                # 也試試其他可能的命名
                alt_slugs = [slug]
                if "room-area" in slug:
                    alt_slugs.extend(["room-area-calculator", "room-area-calc"])
                for alt in alt_slugs:
                    if lang == "zh-TW":
                        alt_path = os.path.join(tools_dir, f"{alt}.html")
                    else:
                        alt_path = os.path.join(tools_dir, lang, f"{alt}.html")
                    if os.path.isfile(alt_path):
                        filepath = alt_path
                        break
                else:
                    continue
            
            total_scanned += 1
            changes = fix_file(filepath, lang, slug, config, args.dry_run)
            
            if changes:
                total_fixed += 1
                status = "(dry-run)" if args.dry_run else "✅"
                print(f"  {status} {lang}: {os.path.basename(filepath)}")
                for c in changes:
                    print(f"    {c}")
            else:
                # 檢查是否已經是 select 了
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                has_select = False
                for field in config.get("fields", []):
                    if re.search(r'<select[^>]*id=["\'][^"\']*' + field["id_regex"], content, re.I):
                        has_select = True
                        break
                if has_select:
                    print(f"  ⏭️  {lang}: 已經是 select，跳過")
                else:
                    print(f"  ⚠️  {lang}: 找不到匹配的 input（可能 ID 不同）")
    
    print(f"\n{'='*60}")
    print(f"📊 修復總結")
    print(f"{'='*60}")
    print(f"  掃描檔案：{total_scanned}")
    print(f"  修復檔案：{total_fixed}")
    
    if args.dry_run:
        print(f"\n  ℹ️ Dry-run 模式，未修改任何檔案")
        print(f"  移除 --dry-run 即可執行")
    else:
        print(f"\n  ✅ 完成！下一步：")
        print(f"  cd {project_root}")
        print(f"  git add -A")
        print(f'  git commit -m "fix: converter tools input→select dropdowns"')
        print(f"  git push")


if __name__ == "__main__":
    main()
