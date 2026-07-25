#!/usr/bin/env python3
"""
generate_missing_patterns.py
生成 9 個缺失的 K棒型態頁面 × 10 語言 = 90 個 HTML
不需要 API，所有內容寫死在腳本裡。

用法：
  cd D:/xian-shang-you-wei/backend
  python generate_missing_patterns.py

輸出到 frontend/patterns/ 對應目錄
"""
import os, json
from datetime import date

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "patterns")
TODAY = date.today().strftime("%Y-%m-%d")
LANGS = ["zh-TW", "en", "ja", "ko", "de", "fr", "es", "pt", "id", "zh-CN"]

# ──────────────────────────────────────────────
# 9 個缺失的 Pattern 定義
# ──────────────────────────────────────────────
PATTERNS = {
    "advance-block": {
        "signal": "bearish", "candles": 3, "reliability": "medium", "win_rate": "55%",
        "names": {
            "zh-TW": "前進阻礙 (Advance Block)",
            "en": "Advance Block Candlestick Pattern",
            "ja": "アドバンスブロック (前進阻害)",
            "ko": "어드밴스 블록 캔들 패턴",
            "de": "Advance Block Kerzenmuster",
            "fr": "Configuration Advance Block",
            "es": "Patrón Advance Block (Bloque de Avance)",
            "pt": "Padrão Advance Block",
            "id": "Pola Candlestick Advance Block",
            "zh-CN": "前进阻碍 (Advance Block)",
        },
        "desc": {
            "zh-TW": "前進阻礙是三根白色蠟燭組成的看跌反轉型態。每根蠟燭的開盤價都在前一根的實體範圍內，但實體逐漸縮小、上影線逐漸加長，顯示多方動能減弱。",
            "en": "The Advance Block is a bearish reversal pattern consisting of three white candles. Each candle opens within the previous body but has progressively smaller bodies and longer upper shadows, indicating weakening bullish momentum.",
            "ja": "アドバンスブロックは3本の陽線で構成される弱気反転パターンです。各ローソクは前の実体内で開きますが、実体が徐々に小さくなり上ヒゲが長くなることで、強気の勢いが弱まっていることを示します。",
            "ko": "어드밴스 블록은 세 개의 양봉으로 구성된 약세 반전 패턴입니다. 각 캔들은 이전 몸체 내에서 시가가 형성되지만 몸체가 점점 작아지고 윗꼬리가 길어져 매수 모멘텀 약화를 나타냅니다.",
            "de": "Der Advance Block ist ein bärisches Umkehrmuster aus drei weißen Kerzen. Jede Kerze eröffnet innerhalb des vorherigen Körpers, hat aber zunehmend kleinere Körper und längere obere Schatten.",
            "fr": "L'Advance Block est une figure de retournement baissière composée de trois bougies blanches. Chaque bougie ouvre dans le corps précédent mais avec des corps de plus en plus petits.",
            "es": "El Advance Block es un patrón de reversión bajista formado por tres velas blancas. Cada vela abre dentro del cuerpo anterior pero con cuerpos progresivamente más pequeños.",
            "pt": "O Advance Block é um padrão de reversão de baixa composto por três velas brancas. Cada vela abre dentro do corpo anterior, mas com corpos progressivamente menores.",
            "id": "Advance Block adalah pola pembalikan bearish yang terdiri dari tiga candle putih. Setiap candle membuka dalam body sebelumnya tetapi dengan body yang semakin mengecil.",
            "zh-CN": "前进阻碍是三根白色蜡烛组成的看跌反转形态。每根蜡烛的开盘价都在前一根的实体范围内，但实体逐渐缩小、上影线逐渐加长。",
        },
    },
    "breakaway-bearish": {
        "signal": "bearish", "candles": 5, "reliability": "medium", "win_rate": "53%",
        "names": {
            "zh-TW": "看跌突破 (Bearish Breakaway)", "en": "Bearish Breakaway Candlestick Pattern",
            "ja": "弱気ブレイクアウェイ", "ko": "약세 브레이크어웨이 패턴",
            "de": "Bearish Breakaway Muster", "fr": "Breakaway Baissier",
            "es": "Breakaway Bajista", "pt": "Breakaway de Baixa",
            "id": "Pola Bearish Breakaway", "zh-CN": "看跌突破 (Bearish Breakaway)",
        },
        "desc": {
            "zh-TW": "看跌突破是五根蠟燭組成的反轉型態。始於一根長白蠟燭，接著向上跳空，然後三根小蠟燭逐漸走弱，最後一根長黑蠟燭收盤回補跳空缺口。",
            "en": "The Bearish Breakaway is a five-candle reversal pattern. It starts with a long white candle, gaps up, followed by three small weakening candles, and ends with a long black candle that closes the gap.",
            "ja": "弱気ブレイクアウェイは5本のローソク足で構成される反転パターンです。長い陽線から始まり、上方ギャップ後に3本の小さなローソクが続き、最後に長い陰線がギャップを埋めます。",
            "ko": "약세 브레이크어웨이는 다섯 개의 캔들로 구성된 반전 패턴입니다. 긴 양봉으로 시작하여 갭업 후 세 개의 작은 캔들이 이어지고, 마지막 긴 음봉이 갭을 메웁니다.",
            "de": "Das Bearish Breakaway ist ein Fünf-Kerzen-Umkehrmuster. Es beginnt mit einer langen weißen Kerze, gefolgt von einem Gap und drei schwächer werdenden Kerzen.",
            "fr": "Le Breakaway Baissier est un motif de retournement à cinq bougies commençant par une longue bougie blanche suivie d'un gap haussier.",
            "es": "El Breakaway Bajista es un patrón de reversión de cinco velas que comienza con una larga vela blanca seguida de un gap alcista.",
            "pt": "O Breakaway de Baixa é um padrão de reversão de cinco velas que começa com uma longa vela branca seguida de um gap de alta.",
            "id": "Bearish Breakaway adalah pola pembalikan lima candle yang dimulai dengan candle putih panjang diikuti gap naik.",
            "zh-CN": "看跌突破是五根蜡烛组成的反转形态。始于一根长白蜡烛，接着向上跳空，然后三根小蜡烛逐渐走弱，最后一根长黑蜡烛收盘回补跳空缺口。",
        },
    },
    "breakaway-bullish": {
        "signal": "bullish", "candles": 5, "reliability": "medium", "win_rate": "53%",
        "names": {
            "zh-TW": "看漲突破 (Bullish Breakaway)", "en": "Bullish Breakaway Candlestick Pattern",
            "ja": "強気ブレイクアウェイ", "ko": "강세 브레이크어웨이 패턴",
            "de": "Bullish Breakaway Muster", "fr": "Breakaway Haussier",
            "es": "Breakaway Alcista", "pt": "Breakaway de Alta",
            "id": "Pola Bullish Breakaway", "zh-CN": "看涨突破 (Bullish Breakaway)",
        },
        "desc": {
            "zh-TW": "看漲突破是五根蠟燭組成的反轉型態。始於一根長黑蠟燭，接著向下跳空，然後三根小蠟燭逐漸企穩，最後一根長白蠟燭收盤回補跳空缺口，標誌趨勢反轉。",
            "en": "The Bullish Breakaway is a five-candle reversal pattern. It starts with a long black candle, gaps down, followed by three small stabilizing candles, and ends with a long white candle closing the gap.",
            "ja": "強気ブレイクアウェイは5本のローソク足で構成される反転パターンです。長い陰線から始まり、下方ギャップ後に3本の小さなローソクが続き、最後に長い陽線がギャップを埋めます。",
            "ko": "강세 브레이크어웨이는 다섯 개의 캔들로 구성된 반전 패턴입니다. 긴 음봉으로 시작하여 갭다운 후 세 개의 작은 캔들이 이어지고, 마지막 긴 양봉이 갭을 메웁니다.",
            "de": "Das Bullish Breakaway ist ein Fünf-Kerzen-Umkehrmuster mit einer langen schwarzen Kerze, einem Gap nach unten und einer abschließenden langen weißen Kerze.",
            "fr": "Le Breakaway Haussier est un motif de retournement à cinq bougies avec une longue bougie noire, un gap baissier et une bougie blanche finale.",
            "es": "El Breakaway Alcista es un patrón de reversión de cinco velas con una larga vela negra, un gap bajista y una vela blanca final.",
            "pt": "O Breakaway de Alta é um padrão de reversão de cinco velas com uma longa vela negra, um gap de baixa e uma vela branca final.",
            "id": "Bullish Breakaway adalah pola pembalikan lima candle dengan candle hitam panjang, gap turun, dan candle putih panjang di akhir.",
            "zh-CN": "看涨突破是五根蜡烛组成的反转形态。始于一根长黑蜡烛，接着向下跳空，然后三根小蜡烛逐渐企稳，最后一根长白蜡烛收盘回补跳空缺口。",
        },
    },
    "deliberation": {
        "signal": "bearish", "candles": 3, "reliability": "low", "win_rate": "51%",
        "names": {
            "zh-TW": "考慮線 (Deliberation)", "en": "Deliberation Candlestick Pattern",
            "ja": "デリバレーション (考慮線)", "ko": "딜리버레이션 캔들 패턴",
            "de": "Deliberation Kerzenmuster", "fr": "Configuration Deliberation",
            "es": "Patrón Deliberation", "pt": "Padrão Deliberation",
            "id": "Pola Candlestick Deliberation", "zh-CN": "考虑线 (Deliberation)",
        },
        "desc": {
            "zh-TW": "考慮線是三根白色蠟燭組成的看跌反轉型態。前兩根為長白蠟燭，第三根為小實體（可能是十字星），在第二根高點附近跳空開出或開在其實體上方，顯示多方猶豫不決。",
            "en": "Deliberation is a bearish reversal pattern with three white candles. The first two are long, and the third is a small body (possibly a doji) that opens near the second candle's high, showing bullish indecision.",
            "ja": "デリバレーションは3本の陽線で構成される弱気反転パターンです。最初の2本は長く、3本目は小さな実体で、強気の躊躇を示します。",
            "ko": "딜리버레이션은 세 개의 양봉으로 구성된 약세 반전 패턴입니다. 처음 두 개는 긴 양봉이고 세 번째는 작은 몸체로 매수세의 주저를 나타냅니다.",
            "de": "Deliberation ist ein bärisches Umkehrmuster mit drei weißen Kerzen. Die ersten zwei sind lang, die dritte hat einen kleinen Körper.",
            "fr": "Le Deliberation est un motif de retournement baissier avec trois bougies blanches dont la troisième a un petit corps.",
            "es": "El Deliberation es un patrón de reversión bajista con tres velas blancas donde la tercera tiene un cuerpo pequeño.",
            "pt": "O Deliberation é um padrão de reversão de baixa com três velas brancas onde a terceira tem um corpo pequeno.",
            "id": "Deliberation adalah pola pembalikan bearish dengan tiga candle putih di mana candle ketiga memiliki body kecil.",
            "zh-CN": "考虑线是三根白色蜡烛组成的看跌反转形态。前两根为长白蜡烛，第三根为小实体，显示多方犹豫不决。",
        },
    },
    "homing-pigeon": {
        "signal": "bullish", "candles": 2, "reliability": "low", "win_rate": "52%",
        "names": {
            "zh-TW": "歸巢鴿 (Homing Pigeon)", "en": "Homing Pigeon Candlestick Pattern",
            "ja": "ホーミングピジョン (帰巣鳩)", "ko": "호밍 피전 캔들 패턴",
            "de": "Homing Pigeon Kerzenmuster", "fr": "Configuration Homing Pigeon",
            "es": "Patrón Homing Pigeon (Paloma Mensajera)", "pt": "Padrão Homing Pigeon",
            "id": "Pola Candlestick Homing Pigeon", "zh-CN": "归巢鸽 (Homing Pigeon)",
        },
        "desc": {
            "zh-TW": "歸巢鴿是兩根黑色蠟燭組成的看漲反轉型態，類似看跌孕線但由兩根陰線組成。第二根蠟燭的實體完全在第一根實體範圍內，顯示賣壓減弱，可能即將反轉。",
            "en": "The Homing Pigeon is a bullish reversal pattern with two black candles, similar to a bearish harami but with both candles being bearish. The second candle's body is entirely within the first, showing diminishing selling pressure.",
            "ja": "ホーミングピジョンは2本の陰線で構成される強気反転パターンで、弱気のはらみ線に似ていますが両方が陰線です。売り圧力の減少を示します。",
            "ko": "호밍 피전은 두 개의 음봉으로 구성된 강세 반전 패턴으로, 두 번째 캔들의 몸체가 첫 번째 안에 완전히 포함되어 매도 압력 감소를 나타냅니다.",
            "de": "Die Homing Pigeon ist ein bullisches Umkehrmuster mit zwei schwarzen Kerzen, ähnlich einem Harami, wobei die zweite Kerze vollständig im Körper der ersten liegt.",
            "fr": "Le Homing Pigeon est une figure de retournement haussière avec deux bougies noires, où le corps de la deuxième est entièrement contenu dans la première.",
            "es": "El Homing Pigeon es un patrón de reversión alcista con dos velas negras donde el cuerpo de la segunda está completamente dentro de la primera.",
            "pt": "O Homing Pigeon é um padrão de reversão de alta com duas velas negras onde o corpo da segunda está completamente dentro da primeira.",
            "id": "Homing Pigeon adalah pola pembalikan bullish dengan dua candle hitam di mana body candle kedua sepenuhnya berada dalam body pertama.",
            "zh-CN": "归巢鸽是两根黑色蜡烛组成的看涨反转形态，第二根蜡烛的实体完全在第一根实体范围内，显示卖压减弱。",
        },
    },
    "identical-three-crows": {
        "signal": "bearish", "candles": 3, "reliability": "high", "win_rate": "72%",
        "names": {
            "zh-TW": "相同三烏鴉 (Identical Three Crows)", "en": "Identical Three Crows Candlestick Pattern",
            "ja": "同事三羽烏", "ko": "동일 삼까마귀 캔들 패턴",
            "de": "Identical Three Crows Muster", "fr": "Trois Corbeaux Identiques",
            "es": "Tres Cuervos Idénticos", "pt": "Três Corvos Idênticos",
            "id": "Pola Identical Three Crows", "zh-CN": "相同三乌鸦 (Identical Three Crows)",
        },
        "desc": {
            "zh-TW": "相同三烏鴉是三根黑色長蠟燭組成的強烈看跌型態。每根蠟燭的開盤價等於或非常接近前一根的收盤價（沒有跳空），實體大小相近，顯示持續且穩定的拋售壓力。",
            "en": "Identical Three Crows is a strong bearish pattern with three long black candles. Each candle opens at or very near the previous close (no gap), with similar-sized bodies showing sustained selling pressure.",
            "ja": "同事三羽烏は3本の長い陰線で構成される強い弱気パターンです。各ローソクは前の終値とほぼ同じ位置で開き、持続的な売り圧力を示します。",
            "ko": "동일 삼까마귀는 세 개의 긴 음봉으로 구성된 강한 약세 패턴입니다. 각 캔들이 이전 종가에서 시가가 형성되어 지속적인 매도 압력을 보여줍니다.",
            "de": "Identical Three Crows ist ein starkes bärisches Muster mit drei langen schwarzen Kerzen, die jeweils nahe dem vorherigen Schlusskurs eröffnen.",
            "fr": "Les Trois Corbeaux Identiques forment un puissant motif baissier avec trois longues bougies noires ouvrant près de la clôture précédente.",
            "es": "Los Tres Cuervos Idénticos forman un fuerte patrón bajista con tres largas velas negras que abren cerca del cierre anterior.",
            "pt": "Os Três Corvos Idênticos formam um forte padrão de baixa com três longas velas negras abrindo perto do fechamento anterior.",
            "id": "Identical Three Crows adalah pola bearish kuat dengan tiga candle hitam panjang yang masing-masing membuka dekat penutupan sebelumnya.",
            "zh-CN": "相同三乌鸦是三根黑色长蜡烛组成的强烈看跌形态。每根蜡烛的开盘价等于或非常接近前一根的收盘价，显示持续且稳定的抛售压力。",
        },
    },
    "ladder-bottom": {
        "signal": "bullish", "candles": 5, "reliability": "medium", "win_rate": "56%",
        "names": {
            "zh-TW": "梯底 (Ladder Bottom)", "en": "Ladder Bottom Candlestick Pattern",
            "ja": "ラダーボトム (梯子底)", "ko": "래더 바텀 캔들 패턴",
            "de": "Ladder Bottom Kerzenmuster", "fr": "Configuration Ladder Bottom",
            "es": "Patrón Ladder Bottom (Fondo de Escalera)", "pt": "Padrão Ladder Bottom",
            "id": "Pola Candlestick Ladder Bottom", "zh-CN": "梯底 (Ladder Bottom)",
        },
        "desc": {
            "zh-TW": "梯底是五根蠟燭組成的看漲反轉型態。前三根為逐步下跌的長黑蠟燭（如階梯下降），第四根黑蠟燭帶有長上影線顯示買方嘗試反攻，第五根白蠟燭跳空開高確認反轉。",
            "en": "Ladder Bottom is a five-candle bullish reversal pattern. The first three are progressively lower long black candles (like descending stairs), the fourth has a long upper shadow, and the fifth is a white candle gapping up.",
            "ja": "ラダーボトムは5本のローソク足で構成される強気反転パターンです。最初の3本は段階的に下がる陰線で、4本目は長い上ヒゲを持ち、5本目は上方ギャップの陽線です。",
            "ko": "래더 바텀은 다섯 개의 캔들로 구성된 강세 반전 패턴입니다. 처음 세 개는 점진적으로 하락하는 긴 음봉이고, 네 번째는 긴 윗꼬리, 다섯 번째는 갭업 양봉입니다.",
            "de": "Das Ladder Bottom ist ein bullisches Fünf-Kerzen-Umkehrmuster mit drei absteigenden schwarzen Kerzen, einer vierten mit langem oberen Schatten und einer weißen Gap-up-Kerze.",
            "fr": "Le Ladder Bottom est un motif de retournement haussier à cinq bougies avec trois bougies noires descendantes suivies d'un gap haussier.",
            "es": "El Ladder Bottom es un patrón de reversión alcista de cinco velas con tres velas negras descendentes seguidas de un gap alcista.",
            "pt": "O Ladder Bottom é um padrão de reversão de alta de cinco velas com três velas negras descendentes seguidas de um gap de alta.",
            "id": "Ladder Bottom adalah pola pembalikan bullish lima candle dengan tiga candle hitam menurun diikuti gap naik.",
            "zh-CN": "梯底是五根蜡烛组成的看涨反转形态。前三根为逐步下跌的长黑蜡烛，第四根带有长上影线，第五根白蜡烛跳空开高确认反转。",
        },
    },
    "stick-sandwich": {
        "signal": "bullish", "candles": 3, "reliability": "low", "win_rate": "52%",
        "names": {
            "zh-TW": "條狀三明治 (Stick Sandwich)", "en": "Stick Sandwich Candlestick Pattern",
            "ja": "スティックサンドイッチ", "ko": "스틱 샌드위치 캔들 패턴",
            "de": "Stick Sandwich Kerzenmuster", "fr": "Configuration Stick Sandwich",
            "es": "Patrón Stick Sandwich", "pt": "Padrão Stick Sandwich",
            "id": "Pola Candlestick Stick Sandwich", "zh-CN": "条状三明治 (Stick Sandwich)",
        },
        "desc": {
            "zh-TW": "條狀三明治是三根蠟燭組成的看漲反轉型態。第一根為長黑蠟燭，第二根為白蠟燭（收盤價高於第一根），第三根為黑蠟燭，收盤價與第一根相同或接近，形成支撐價位。",
            "en": "The Stick Sandwich is a three-candle bullish reversal pattern. A long black candle is followed by a white candle closing higher, then another black candle closing at the same level as the first, establishing a support level.",
            "ja": "スティックサンドイッチは3本のローソク足で構成される強気反転パターンです。長い陰線の後に陽線、そして最初と同じ終値の陰線が続き、サポートレベルを形成します。",
            "ko": "스틱 샌드위치는 세 개의 캔들로 구성된 강세 반전 패턴입니다. 긴 음봉, 양봉, 그리고 첫 번째와 같은 종가의 음봉으로 지지선을 형성합니다.",
            "de": "Das Stick Sandwich ist ein bullisches Drei-Kerzen-Umkehrmuster, bei dem die dritte Kerze auf dem gleichen Niveau wie die erste schließt.",
            "fr": "Le Stick Sandwich est un motif de retournement haussier à trois bougies où la troisième bougie clôture au même niveau que la première.",
            "es": "El Stick Sandwich es un patrón de reversión alcista de tres velas donde la tercera cierra al mismo nivel que la primera.",
            "pt": "O Stick Sandwich é um padrão de reversão de alta de três velas onde a terceira fecha no mesmo nível da primeira.",
            "id": "Stick Sandwich adalah pola pembalikan bullish tiga candle di mana candle ketiga ditutup pada level yang sama dengan candle pertama.",
            "zh-CN": "条状三明治是三根蜡烛组成的看涨反转形态。第一根为长黑蜡烛，第二根为白蜡烛，第三根黑蜡烛收盘价与第一根相同，形成支撑价位。",
        },
    },
    "upside-gap-two-crows": {
        "signal": "bearish", "candles": 3, "reliability": "medium", "win_rate": "57%",
        "names": {
            "zh-TW": "上升跳空雙烏鴉 (Upside Gap Two Crows)", "en": "Upside Gap Two Crows Candlestick Pattern",
            "ja": "上放れ二羽烏 (上昇ギャップ二羽烏)", "ko": "상승 갭 투 크로우즈 패턴",
            "de": "Upside Gap Two Crows Muster", "fr": "Gap Haussier Deux Corbeaux",
            "es": "Gap Alcista Dos Cuervos", "pt": "Gap de Alta Dois Corvos",
            "id": "Pola Upside Gap Two Crows", "zh-CN": "上升跳空双乌鸦 (Upside Gap Two Crows)",
        },
        "desc": {
            "zh-TW": "上升跳空雙烏鴉是三根蠟燭組成的看跌反轉型態。第一根為長白蠟燭，第二根為小黑蠟燭（向上跳空開出），第三根為較大的黑蠟燭，吞沒第二根但仍在第一根上方收盤。",
            "en": "Upside Gap Two Crows is a three-candle bearish reversal pattern. A long white candle is followed by a small black candle gapping up, then a larger black candle engulfing the second but still closing above the first candle's close.",
            "ja": "上放れ二羽烏は3本のローソク足で構成される弱気反転パターンです。長い陽線の後に上方ギャップの小さな陰線、そしてそれを包む大きな陰線が続きます。",
            "ko": "상승 갭 투 크로우즈는 세 개의 캔들로 구성된 약세 반전 패턴입니다. 긴 양봉 뒤에 갭업한 작은 음봉, 그리고 두 번째를 감싸는 큰 음봉이 이어집니다.",
            "de": "Upside Gap Two Crows ist ein bärisches Drei-Kerzen-Umkehrmuster mit einer langen weißen Kerze, gefolgt von zwei schwarzen Kerzen mit Gap.",
            "fr": "Le Gap Haussier Deux Corbeaux est un motif de retournement baissier à trois bougies avec une longue bougie blanche suivie de deux bougies noires.",
            "es": "El Gap Alcista Dos Cuervos es un patrón de reversión bajista de tres velas con una larga vela blanca seguida de dos velas negras.",
            "pt": "O Gap de Alta Dois Corvos é um padrão de reversão de baixa de três velas com uma longa vela branca seguida de duas velas negras.",
            "id": "Upside Gap Two Crows adalah pola pembalikan bearish tiga candle dengan candle putih panjang diikuti dua candle hitam dengan gap.",
            "zh-CN": "上升跳空双乌鸦是三根蜡烛组成的看跌反转形态。第一根为长白蜡烛，第二根为小黑蜡烛向上跳空开出，第三根为较大的黑蜡烛吞没第二根。",
        },
    },
}

# Nav/UI labels per language
UI = {
    "zh-TW": {"tools": "工具", "patterns": "K棒型態", "home": "首頁", "back": "← 回到型態總覽", "faq_title": "常見問題", "pattern_def": "型態定義", "market_psych": "市場心理分析", "trading_rules": "交易規則", "notes": "注意事項", "signal": "信號", "candles": "蠟燭數", "reliability": "可靠度", "win_rate": "歷史勝率", "bullish": "看漲", "bearish": "看跌", "high": "高", "medium": "中", "low": "低"},
    "en": {"tools": "Tools", "patterns": "Candlestick Patterns", "home": "Home", "back": "← Back to Patterns", "faq_title": "FAQ", "pattern_def": "Pattern Definition", "market_psych": "Market Psychology", "trading_rules": "Trading Rules", "notes": "Important Notes", "signal": "Signal", "candles": "Candles", "reliability": "Reliability", "win_rate": "Win Rate", "bullish": "Bullish", "bearish": "Bearish", "high": "High", "medium": "Medium", "low": "Low"},
    "ja": {"tools": "ツール", "patterns": "ローソク足パターン", "home": "ホーム", "back": "← パターン一覧に戻る", "faq_title": "よくある質問", "pattern_def": "パターン定義", "market_psych": "市場心理分析", "trading_rules": "トレードルール", "notes": "注意事項", "signal": "シグナル", "candles": "ローソク数", "reliability": "信頼度", "win_rate": "勝率", "bullish": "強気", "bearish": "弱気", "high": "高", "medium": "中", "low": "低"},
    "ko": {"tools": "도구", "patterns": "캔들 패턴", "home": "홈", "back": "← 패턴 목록으로", "faq_title": "자주 묻는 질문", "pattern_def": "패턴 정의", "market_psych": "시장 심리 분석", "trading_rules": "트레이딩 규칙", "notes": "주의사항", "signal": "신호", "candles": "캔들 수", "reliability": "신뢰도", "win_rate": "승률", "bullish": "강세", "bearish": "약세", "high": "높음", "medium": "보통", "low": "낮음"},
    "de": {"tools": "Werkzeuge", "patterns": "Kerzenmuster", "home": "Start", "back": "← Zurück", "faq_title": "FAQ", "pattern_def": "Musterdefinition", "market_psych": "Marktpsychologie", "trading_rules": "Handelsregeln", "notes": "Hinweise", "signal": "Signal", "candles": "Kerzen", "reliability": "Zuverlässigkeit", "win_rate": "Gewinnrate", "bullish": "Bullisch", "bearish": "Bärisch", "high": "Hoch", "medium": "Mittel", "low": "Niedrig"},
    "fr": {"tools": "Outils", "patterns": "Chandeliers", "home": "Accueil", "back": "← Retour", "faq_title": "FAQ", "pattern_def": "Définition", "market_psych": "Psychologie du Marché", "trading_rules": "Règles de Trading", "notes": "Notes", "signal": "Signal", "candles": "Bougies", "reliability": "Fiabilité", "win_rate": "Taux de Réussite", "bullish": "Haussier", "bearish": "Baissier", "high": "Élevée", "medium": "Moyenne", "low": "Faible"},
    "es": {"tools": "Herramientas", "patterns": "Patrones", "home": "Inicio", "back": "← Volver", "faq_title": "Preguntas Frecuentes", "pattern_def": "Definición", "market_psych": "Psicología del Mercado", "trading_rules": "Reglas de Trading", "notes": "Notas", "signal": "Señal", "candles": "Velas", "reliability": "Fiabilidad", "win_rate": "Tasa de Éxito", "bullish": "Alcista", "bearish": "Bajista", "high": "Alta", "medium": "Media", "low": "Baja"},
    "pt": {"tools": "Ferramentas", "patterns": "Padrões", "home": "Início", "back": "← Voltar", "faq_title": "Perguntas Frequentes", "pattern_def": "Definição", "market_psych": "Psicologia do Mercado", "trading_rules": "Regras de Trading", "notes": "Notas", "signal": "Sinal", "candles": "Velas", "reliability": "Confiabilidade", "win_rate": "Taxa de Acerto", "bullish": "Alta", "bearish": "Baixa", "high": "Alta", "medium": "Média", "low": "Baixa"},
    "id": {"tools": "Alat", "patterns": "Pola Candlestick", "home": "Beranda", "back": "← Kembali", "faq_title": "FAQ", "pattern_def": "Definisi Pola", "market_psych": "Psikologi Pasar", "trading_rules": "Aturan Trading", "notes": "Catatan", "signal": "Sinyal", "candles": "Candle", "reliability": "Keandalan", "win_rate": "Win Rate", "bullish": "Bullish", "bearish": "Bearish", "high": "Tinggi", "medium": "Sedang", "low": "Rendah"},
    "zh-CN": {"tools": "工具", "patterns": "K线形态", "home": "首页", "back": "← 返回形态总览", "faq_title": "常见问题", "pattern_def": "形态定义", "market_psych": "市场心理分析", "trading_rules": "交易规则", "notes": "注意事项", "signal": "信号", "candles": "蜡烛数", "reliability": "可靠度", "win_rate": "历史胜率", "bullish": "看涨", "bearish": "看跌", "high": "高", "medium": "中", "low": "低"},
}


def lang_path(lang, slug):
    if lang == "zh-TW":
        return f"/patterns/{slug}.html"
    return f"/patterns/{lang}/{slug}.html"


def generate_page(slug, pdata, lang):
    ui = UI[lang]
    name = pdata["names"][lang]
    desc = pdata["desc"][lang]
    signal = pdata["signal"]
    signal_label = ui["bullish"] if signal == "bullish" else ui["bearish"]
    signal_css = f"signal-{signal}"
    rel = pdata["reliability"]
    rel_label = ui[rel]
    rel_css = f"reliability-{rel}"
    candles = pdata["candles"]
    win_rate = pdata["win_rate"]

    # hreflang tags
    hreflangs = []
    for l in LANGS:
        url = f"https://softglow-ai.com{lang_path(l, slug)}"
        hreflangs.append(f'<link rel="alternate" hreflang="{l}" href="{url}"/>')
    hreflangs.append(f'<link rel="alternate" hreflang="x-default" href="https://softglow-ai.com{lang_path("en", slug)}"/>')

    canonical = f"https://softglow-ai.com{lang_path(lang, slug)}"
    index_url = f"/patterns/index.html" if lang == "zh-TW" else f"/patterns/{lang}.html"

    # Schema
    article_schema = json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": name, "description": desc,
        "author": {"@type": "Organization", "name": "SoftGlow"},
        "publisher": {"@type": "Organization", "name": "SoftGlow", "url": "https://softglow-ai.com"},
        "datePublished": TODAY, "dateModified": TODAY,
        "mainEntityOfPage": canonical,
    }, ensure_ascii=False)

    breadcrumb_schema = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ui["home"], "item": "https://softglow-ai.com"},
            {"@type": "ListItem", "position": 2, "name": ui["patterns"], "item": f"https://softglow-ai.com{index_url}"},
            {"@type": "ListItem", "position": 3, "name": name},
        ]
    }, ensure_ascii=False)

    # Language switcher
    lang_buttons = []
    lang_labels = {"zh-TW": "繁中", "en": "EN", "ja": "日本語", "ko": "한국어", "de": "DE", "fr": "FR", "es": "ES", "pt": "PT", "id": "ID", "zh-CN": "简中"}
    for l in LANGS:
        active = ' active' if l == lang else ''
        lang_buttons.append(f'<a href="{lang_path(l, slug)}" class="lang-btn{active}">{lang_labels[l]}</a>')

    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://securepubads.g.doubleclick.net">
<link rel="preconnect" href="https://pagead2.googlesyndication.com">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name}</title>
<meta name="description" content="{desc[:160]}">
<meta name="robots" content="index, follow">
<meta name="sg-slug" content="{slug}">
<meta name="sg-type" content="pattern">
<meta name="sg-lang" content="{lang}">
<link rel="canonical" href="{canonical}">
{chr(10).join(hreflangs)}
<link rel="stylesheet" href="/common/softglow-common.css">
<script type="application/ld+json">{article_schema}</script>
<script type="application/ld+json">{breadcrumb_schema}</script>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:#2D3748;background:#fff;line-height:1.6;-webkit-font-smoothing:antialiased}}
a{{color:#2563EB;text-decoration:none}}
a:hover{{text-decoration:underline}}
.nav{{position:sticky;top:0;z-index:100;background:rgba(255,255,255,0.95);backdrop-filter:blur(8px);border-bottom:1px solid #E2E8F0}}
.nav-inner{{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;height:52px}}
.nav-logo{{font-size:17px;font-weight:700;color:#2D3748;letter-spacing:-0.5px}}
.nav-logo span{{color:#2563EB}}
.nav-links{{display:flex;gap:16px;align-items:center}}
.nav-links a{{font-size:13px;color:#4A5568;font-weight:500}}
.nav-links a:hover{{color:#2563EB;text-decoration:none}}
.breadcrumb{{max-width:1080px;margin:0 auto;padding:12px 20px;font-size:13px;color:#A0AEC0}}
.breadcrumb a{{color:#718096}}
.container{{max-width:860px;margin:0 auto;padding:0 20px}}
.hero{{background:#F7FAFC;border:1px solid #E2E8F0;border-radius:16px;padding:28px 32px;margin-bottom:24px}}
.hero h1{{font-size:24px;font-weight:700;color:#1A202C;margin-bottom:8px}}
.hero p{{font-size:15px;color:#4A5568;line-height:1.7;margin-bottom:16px}}
.hero-meta{{display:flex;flex-wrap:wrap;gap:10px}}
.meta-tag{{display:inline-flex;align-items:center;gap:5px;font-size:12px;padding:4px 12px;border-radius:20px;background:#EBF5FF;color:#2B6CB0;font-weight:500}}
.meta-tag.signal-bullish{{background:#E1F5EE;color:#085041}}
.meta-tag.signal-bearish{{background:#FCEBEB;color:#791F1F}}
.meta-tag.reliability-high{{background:#E1F5EE;color:#085041}}
.meta-tag.reliability-medium{{background:#FFF8E1;color:#92650D}}
.meta-tag.reliability-low{{background:#FCEBEB;color:#791F1F}}
.section{{margin-bottom:28px}}
.section h2{{font-size:19px;font-weight:700;color:#1A202C;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid #E2E8F0}}
.section p{{margin-bottom:12px;color:#4A5568;line-height:1.8;font-size:15px}}
.section ul{{margin:10px 0 16px 24px;color:#4A5568;font-size:15px}}
.section li{{margin-bottom:6px;line-height:1.7}}
.lang-bar{{display:flex;gap:6px;flex-wrap:wrap;margin:20px 0}}
.lang-btn{{font-size:12px;padding:4px 12px;border-radius:20px;background:#F7FAFC;border:1px solid #E2E8F0;color:#718096}}
.lang-btn:hover{{background:#EBF5FF;border-color:#BEE3F8;text-decoration:none}}
.lang-btn.active{{background:#2563EB;color:#fff;border-color:#2563EB}}
.footer{{border-top:1px solid #E2E8F0;padding:24px 0;margin-top:40px}}
.footer-inner{{max-width:1080px;margin:0 auto;padding:0 20px;display:flex;flex-wrap:wrap;gap:16px;font-size:12px;color:#A0AEC0}}
.footer-inner a{{color:#718096}}
@media(max-width:768px){{.hero{{padding:20px}}.hero h1{{font-size:20px}}}}
</style>
<link rel="stylesheet" href="/js/cookie-consent.css">
</head>
<body>
<nav class="nav"><div class="nav-inner">
  <a href="/" class="nav-logo">Soft<span>Glow</span></a>
  <div class="nav-links">
    <a href="/tools/">{ui["tools"]}</a>
    <a href="{index_url}">{ui["patterns"]}</a>
    <a href="/">{ui["home"]}</a>
  </div>
</div></nav>
<div class="breadcrumb">
  <a href="/">{ui["home"]}</a> › <a href="{index_url}">{ui["patterns"]}</a> › {name}
</div>
<div class="container">
<div class="hero">
  <h1>{name}</h1>
  <p>{desc}</p>
  <div class="hero-meta">
    <span class="meta-tag {signal_css}">{ui["signal"]}: {signal_label}</span>
    <span class="meta-tag">{ui["candles"]}: {candles}</span>
    <span class="meta-tag {rel_css}">{ui["reliability"]}: {rel_label}</span>
    <span class="meta-tag">{ui["win_rate"]}: {win_rate}</span>
  </div>
</div>
<div class="section"><h2>{ui["pattern_def"]}</h2><p>{desc}</p></div>
<div class="section"><h2>{ui["trading_rules"]}</h2>
<ul>
<li>{desc}</li>
</ul>
</div>
<div class="section"><h2>{ui["notes"]}</h2>
<p>{desc}</p>
</div>
<div class="lang-bar">
  {chr(10).join(lang_buttons)}
</div>
<p style="margin:20px 0"><a href="{index_url}">{ui["back"]}</a></p>
</div>
<footer class="footer"><div class="footer-inner">
  <a href="/about.html">About</a>
  <a href="/contact.html">Contact</a>
  <a href="/privacy.html">Privacy</a>
  <a href="/terms.html">Terms</a>
  <span style="margin-left:auto">&copy; 2026 SoftGlow</span>
</div></footer>
<script src="/common/softglow-common.js"></script>
<script>
setTimeout(function(){{
  var s=document.createElement('script');s.async=true;
  s.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1768270548115739';
  s.crossOrigin='anonymous';document.head.appendChild(s);
}},2000);
</script>
<script src="/js/softglow-cookies.js" defer></script>
</body>
</html>'''
    return html


def main():
    created = 0
    skipped = 0
    for slug, pdata in PATTERNS.items():
        for lang in LANGS:
            if lang == "zh-TW":
                fpath = os.path.join(BASE, f"{slug}.html")
            else:
                dpath = os.path.join(BASE, lang)
                os.makedirs(dpath, exist_ok=True)
                fpath = os.path.join(dpath, f"{slug}.html")

            if os.path.exists(fpath):
                skipped += 1
                continue

            html = generate_page(slug, pdata, lang)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(html)
            created += 1

    print(f"✅ Done! Created {created} pages, skipped {skipped} existing.")
    print(f"   Output: {BASE}")


if __name__ == "__main__":
    main()
