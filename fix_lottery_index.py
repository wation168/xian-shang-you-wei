# -*- coding: utf-8 -*-
"""
fix_lottery_index.py
Fix lottery index pages - only show lotteries that exist in each language folder
"""

import os
import re

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend", "frontend", "lottery")

# 所有彩種 slug（跟 generate_lottery_final.py 一致）
ALL_LOTTERIES = [
    "powerball", "mega-millions", "lotto-max", "mega-sena",
    "euromillions", "uk-lotto", "el-gordo", "superenalotto", "lotto-6aus49",
    "taiwan-bingo", "taiwan-lotto", "daily-cash",
    "korea-lotto", "japan-loto6", "oz-lotto"
]

# 語言 → 資料夾對應（根目錄 = zh-TW）
LANG_FOLDERS = {
    "zh-TW": "",  # root
    "en": "en",
    "ja": "ja",
    "ko": "ko",
    "fr": "fr",
    "de": "de",
    "es": "es",
    "pt": "pt",
    "id": "id",
    "zh-CN": "zh-CN",
}

# 彩種資訊（用於生成卡片）
LOTTERY_INFO = {
    "powerball":      {"flag": "[USA]", "region": "usa"},
    "mega-millions":  {"flag": "[USA]", "region": "usa"},
    "lotto-max":      {"flag": "[CA]",  "region": "americas"},
    "mega-sena":      {"flag": "[BR]",  "region": "americas"},
    "euromillions":   {"flag": "[EU]",  "region": "europe"},
    "uk-lotto":       {"flag": "[UK]",  "region": "europe"},
    "el-gordo":       {"flag": "[ES]",  "region": "europe"},
    "superenalotto":  {"flag": "[IT]",  "region": "europe"},
    "lotto-6aus49":   {"flag": "[DE]",  "region": "europe"},
    "taiwan-bingo":   {"flag": "[TW]",  "region": "asia"},
    "taiwan-lotto":   {"flag": "[TW]",  "region": "asia"},
    "daily-cash":     {"flag": "[TW]",  "region": "asia"},
    "korea-lotto":    {"flag": "[KR]",  "region": "asia"},
    "japan-loto6":    {"flag": "[JP]",  "region": "asia"},
    "oz-lotto":       {"flag": "[AU]",  "region": "oceania"},
}

# 各語言的翻譯
I18N = {
    "zh-TW": {
        "title": "全球彩票開獎號碼與選號工具 | SoftGlow",
        "desc": "追蹤全球 15 大彩票最新開獎號碼，威力彩、大樂透、Powerball、EuroMillions 等，12 種智慧選號工具免費使用。",
        "h1": "🎰 SoftGlow 全球彩票",
        "subtitle": "15 大彩種 · 12 種選號方式 · 開獎結果與統計",
        "btn": "智慧選號 🎲",
        "regions": {"usa": "美國", "americas": "美洲", "europe": "歐洲", "asia": "亞洲", "oceania": "大洋洲"},
        "lottery_names": {
            "powerball": "Powerball 威力球", "mega-millions": "Mega Millions",
            "lotto-max": "Lotto Max", "mega-sena": "Mega-Sena",
            "euromillions": "EuroMillions 歐洲百萬", "uk-lotto": "UK Lotto",
            "el-gordo": "El Gordo", "superenalotto": "SuperEnalotto",
            "lotto-6aus49": "Lotto 6aus49",
            "taiwan-bingo": "威力彩", "taiwan-lotto": "大樂透", "daily-cash": "今彩539",
            "korea-lotto": "韓國樂透", "japan-loto6": "日本 Loto 6", "oz-lotto": "Oz Lotto",
        },
        "disclaimer": "⚠️ 彩券有風險，請理性投注",
        "nav_lottery": "彩票", "nav_tools": "工具", "nav_home": "首頁",
        "about": "關於", "contact": "聯繫", "privacy": "隱私", "terms": "條款",
        "no_lotteries": "此語言版本僅提供選號工具，彩種資訊請切換至英文版查看。",
    },
    "en": {
        "title": "Global Lottery Results & Number Generator | SoftGlow",
        "desc": "Track latest lottery results for Powerball, Mega Millions, EuroMillions and 12 more. Free number generators with 12 smart picking methods.",
        "h1": "🎰 SoftGlow Lottery",
        "subtitle": "15 Lotteries · 12 Number Picking Methods · Results & Statistics",
        "btn": "Number Generator 🎲",
        "regions": {"usa": "USA", "americas": "Americas", "europe": "Europe", "asia": "Asia", "oceania": "Oceania"},
        "lottery_names": {
            "powerball": "Powerball", "mega-millions": "Mega Millions",
            "lotto-max": "Lotto Max", "mega-sena": "Mega-Sena",
            "euromillions": "EuroMillions", "uk-lotto": "UK Lotto",
            "el-gordo": "El Gordo", "superenalotto": "SuperEnalotto",
            "lotto-6aus49": "Lotto 6aus49",
            "taiwan-bingo": "Taiwan Power Lottery", "taiwan-lotto": "Taiwan Super Lotto",
            "daily-cash": "Daily Cash 539",
            "korea-lotto": "Korea Lotto 6/45", "japan-loto6": "Japan Loto 6", "oz-lotto": "Oz Lotto",
        },
        "disclaimer": "⚠️ Please gamble responsibly",
        "nav_lottery": "Lottery", "nav_tools": "Tools", "nav_home": "Home",
        "about": "About", "contact": "Contact", "privacy": "Privacy", "terms": "Terms",
        "no_lotteries": "This language version only provides number generator tools. Switch to English for lottery results.",
    },
    "ja": {
        "title": "世界の宝くじ当選番号＆ナンバージェネレーター | SoftGlow",
        "desc": "パワーボール、メガミリオンズ、ユーロミリオンズなど世界15の宝くじ最新当選番号。12種類の番号選択ツール無料。",
        "h1": "🎰 SoftGlow 宝くじ",
        "subtitle": "15の宝くじ · 12の選番方法 · 当選結果＆統計",
        "btn": "ナンバージェネレーター 🎲",
        "regions": {"usa": "アメリカ", "americas": "南北アメリカ", "europe": "ヨーロッパ", "asia": "アジア", "oceania": "オセアニア"},
        "lottery_names": {
            "powerball": "パワーボール", "mega-millions": "メガミリオンズ",
            "lotto-max": "ロトマックス", "mega-sena": "メガセナ",
            "euromillions": "ユーロミリオンズ", "uk-lotto": "UKロト",
            "el-gordo": "エルゴルド", "superenalotto": "スーパーエナロット",
            "lotto-6aus49": "ロト 6aus49",
            "taiwan-bingo": "台湾威力彩", "taiwan-lotto": "台湾大楽透",
            "daily-cash": "今彩539",
            "korea-lotto": "韓国ロト", "japan-loto6": "ロト6", "oz-lotto": "オズロト",
        },
        "disclaimer": "⚠️ 責任ある遊び方をお願いします",
        "nav_lottery": "宝くじ", "nav_tools": "ツール", "nav_home": "ホーム",
        "about": "概要", "contact": "お問い合わせ", "privacy": "プライバシー", "terms": "利用規約",
        "no_lotteries": "この言語版では番号生成ツールのみ提供しています。宝くじ情報は英語版をご覧ください。",
    },
    "ko": {
        "title": "세계 복권 당첨번호 & 번호 생성기 | SoftGlow",
        "desc": "파워볼, 메가밀리언즈, 유로밀리언즈 등 세계 15개 복권 최신 당첨번호. 12가지 스마트 번호 선택 도구 무료.",
        "h1": "🎰 SoftGlow 복권",
        "subtitle": "15개 복권 · 12가지 번호 선택 · 결과 & 통계",
        "btn": "번호 생성기 🎲",
        "regions": {"usa": "미국", "americas": "아메리카", "europe": "유럽", "asia": "아시아", "oceania": "오세아니아"},
        "lottery_names": {
            "powerball": "파워볼", "mega-millions": "메가밀리언즈",
            "lotto-max": "로또 맥스", "mega-sena": "메가세나",
            "euromillions": "유로밀리언즈", "uk-lotto": "UK 로또",
            "el-gordo": "엘고르도", "superenalotto": "슈퍼에날로또",
            "lotto-6aus49": "로또 6aus49",
            "taiwan-bingo": "대만 위리차이", "taiwan-lotto": "대만 대락투",
            "daily-cash": "데일리 캐시 539",
            "korea-lotto": "로또 6/45", "japan-loto6": "일본 로또 6", "oz-lotto": "오즈 로또",
        },
        "disclaimer": "⚠️ 책임감 있게 즐기세요",
        "nav_lottery": "복권", "nav_tools": "도구", "nav_home": "홈",
        "about": "소개", "contact": "연락", "privacy": "개인정보", "terms": "이용약관",
        "no_lotteries": "이 언어 버전은 번호 생성 도구만 제공합니다. 복권 정보는 영어 버전을 확인하세요.",
    },
    "de": {
        "title": "Globale Lotterie-Ergebnisse & Zahlengenerator | SoftGlow",
        "desc": "Aktuelle Lotterieziehungen für EuroMillions, Lotto 6aus49, Powerball und mehr. 12 kostenlose Zahlengeneratoren.",
        "h1": "🎰 SoftGlow Lotterie",
        "subtitle": "15 Lotterien · 12 Auswahlmethoden · Ergebnisse & Statistiken",
        "btn": "Zahlengenerator 🎲",
        "regions": {"usa": "USA", "americas": "Amerika", "europe": "Europa", "asia": "Asien", "oceania": "Ozeanien"},
        "lottery_names": {
            "powerball": "Powerball", "mega-millions": "Mega Millions",
            "lotto-max": "Lotto Max", "mega-sena": "Mega-Sena",
            "euromillions": "EuroMillions", "uk-lotto": "UK Lotto",
            "el-gordo": "El Gordo", "superenalotto": "SuperEnalotto",
            "lotto-6aus49": "Lotto 6aus49",
            "taiwan-bingo": "Taiwan Power Lottery", "taiwan-lotto": "Taiwan Super Lotto",
            "daily-cash": "Daily Cash 539",
            "korea-lotto": "Korea Lotto", "japan-loto6": "Japan Loto 6", "oz-lotto": "Oz Lotto",
        },
        "disclaimer": "⚠️ Bitte spielen Sie verantwortungsvoll",
        "nav_lottery": "Lotterie", "nav_tools": "Werkzeuge", "nav_home": "Startseite",
        "about": "Über uns", "contact": "Kontakt", "privacy": "Datenschutz", "terms": "AGB",
        "no_lotteries": "Diese Sprachversion bietet nur Zahlengenerator-Tools. Für Lotterie-Ergebnisse wechseln Sie zur englischen Version.",
    },
    "fr": {
        "title": "Résultats de Loterie Mondiale & Générateur de Numéros | SoftGlow",
        "desc": "Suivez les résultats EuroMillions, Powerball, Mega Millions et plus. 12 générateurs de numéros gratuits.",
        "h1": "🎰 SoftGlow Loterie",
        "subtitle": "15 Loteries · 12 Méthodes de Sélection · Résultats & Statistiques",
        "btn": "Générateur de Numéros 🎲",
        "regions": {"usa": "États-Unis", "americas": "Amériques", "europe": "Europe", "asia": "Asie", "oceania": "Océanie"},
        "lottery_names": {
            "powerball": "Powerball", "mega-millions": "Mega Millions",
            "lotto-max": "Lotto Max", "mega-sena": "Mega-Sena",
            "euromillions": "EuroMillions", "uk-lotto": "UK Lotto",
            "el-gordo": "El Gordo", "superenalotto": "SuperEnalotto",
            "lotto-6aus49": "Lotto 6aus49",
            "taiwan-bingo": "Loterie Taiwan", "taiwan-lotto": "Super Loto Taiwan",
            "daily-cash": "Daily Cash 539",
            "korea-lotto": "Loto Corée", "japan-loto6": "Loto 6 Japon", "oz-lotto": "Oz Lotto",
        },
        "disclaimer": "⚠️ Jouez de manière responsable",
        "nav_lottery": "Loterie", "nav_tools": "Outils", "nav_home": "Accueil",
        "about": "À propos", "contact": "Contact", "privacy": "Confidentialité", "terms": "Conditions",
        "no_lotteries": "Cette version linguistique ne propose que des outils de génération de numéros. Consultez la version anglaise pour les résultats.",
    },
    "es": {
        "title": "Resultados de Lotería Global & Generador de Números | SoftGlow",
        "desc": "Sigue los resultados de EuroMillions, El Gordo, Powerball y más. 12 generadores de números gratuitos.",
        "h1": "🎰 SoftGlow Lotería",
        "subtitle": "15 Loterías · 12 Métodos de Selección · Resultados & Estadísticas",
        "btn": "Generador de Números 🎲",
        "regions": {"usa": "EE.UU.", "americas": "Américas", "europe": "Europa", "asia": "Asia", "oceania": "Oceanía"},
        "lottery_names": {
            "powerball": "Powerball", "mega-millions": "Mega Millions",
            "lotto-max": "Lotto Max", "mega-sena": "Mega-Sena",
            "euromillions": "EuroMillions", "uk-lotto": "UK Lotto",
            "el-gordo": "El Gordo", "superenalotto": "SuperEnalotto",
            "lotto-6aus49": "Lotto 6aus49",
            "taiwan-bingo": "Lotería Taiwan", "taiwan-lotto": "Super Loto Taiwan",
            "daily-cash": "Daily Cash 539",
            "korea-lotto": "Loto Corea", "japan-loto6": "Loto 6 Japón", "oz-lotto": "Oz Lotto",
        },
        "disclaimer": "⚠️ Juegue con responsabilidad",
        "nav_lottery": "Lotería", "nav_tools": "Herramientas", "nav_home": "Inicio",
        "about": "Acerca de", "contact": "Contacto", "privacy": "Privacidad", "terms": "Términos",
        "no_lotteries": "Esta versión solo ofrece herramientas de generación de números. Consulte la versión en inglés para resultados.",
    },
    "pt": {
        "title": "Resultados de Loteria Global & Gerador de Números | SoftGlow",
        "desc": "Acompanhe resultados da Mega-Sena, EuroMillions, Powerball e mais. 12 geradores de números grátis.",
        "h1": "🎰 SoftGlow Loteria",
        "subtitle": "15 Loterias · 12 Métodos de Seleção · Resultados & Estatísticas",
        "btn": "Gerador de Números 🎲",
        "regions": {"usa": "EUA", "americas": "Américas", "europe": "Europa", "asia": "Ásia", "oceania": "Oceania"},
        "lottery_names": {
            "powerball": "Powerball", "mega-millions": "Mega Millions",
            "lotto-max": "Lotto Max", "mega-sena": "Mega-Sena",
            "euromillions": "EuroMillions", "uk-lotto": "UK Lotto",
            "el-gordo": "El Gordo", "superenalotto": "SuperEnalotto",
            "lotto-6aus49": "Lotto 6aus49",
            "taiwan-bingo": "Loteria Taiwan", "taiwan-lotto": "Super Loto Taiwan",
            "daily-cash": "Daily Cash 539",
            "korea-lotto": "Loto Coreia", "japan-loto6": "Loto 6 Japão", "oz-lotto": "Oz Lotto",
        },
        "disclaimer": "⚠️ Jogue com responsabilidade",
        "nav_lottery": "Loteria", "nav_tools": "Ferramentas", "nav_home": "Início",
        "about": "Sobre", "contact": "Contato", "privacy": "Privacidade", "terms": "Termos",
        "no_lotteries": "Esta versão oferece apenas ferramentas de geração de números. Consulte a versão em inglês para resultados.",
    },
    "id": {
        "title": "Hasil Lotere Global & Generator Nomor | SoftGlow",
        "desc": "Pantau hasil Powerball, Mega Millions, EuroMillions dan lainnya. 12 generator nomor gratis.",
        "h1": "🎰 SoftGlow Lotere",
        "subtitle": "15 Lotere · 12 Metode Pemilihan · Hasil & Statistik",
        "btn": "Generator Nomor 🎲",
        "regions": {"usa": "AS", "americas": "Amerika", "europe": "Eropa", "asia": "Asia", "oceania": "Oseania"},
        "lottery_names": {
            "powerball": "Powerball", "mega-millions": "Mega Millions",
            "lotto-max": "Lotto Max", "mega-sena": "Mega-Sena",
            "euromillions": "EuroMillions", "uk-lotto": "UK Lotto",
            "el-gordo": "El Gordo", "superenalotto": "SuperEnalotto",
            "lotto-6aus49": "Lotto 6aus49",
            "taiwan-bingo": "Lotre Taiwan", "taiwan-lotto": "Super Loto Taiwan",
            "daily-cash": "Daily Cash 539",
            "korea-lotto": "Loto Korea", "japan-loto6": "Loto 6 Jepang", "oz-lotto": "Oz Lotto",
        },
        "disclaimer": "⚠️ Bermain secara bertanggung jawab",
        "nav_lottery": "Lotere", "nav_tools": "Alat", "nav_home": "Beranda",
        "about": "Tentang", "contact": "Kontak", "privacy": "Privasi", "terms": "Ketentuan",
        "no_lotteries": "Versi bahasa ini hanya menyediakan alat generator nomor. Kunjungi versi bahasa Inggris untuk hasil lotere.",
    },
    "zh-CN": {
        "title": "全球彩票开奖号码与选号工具 | SoftGlow",
        "desc": "追踪全球15大彩票最新开奖号码，威力彩、Powerball、EuroMillions等，12种智能选号工具免费使用。",
        "h1": "🎰 SoftGlow 全球彩票",
        "subtitle": "15大彩种 · 12种选号方式 · 开奖结果与统计",
        "btn": "智能选号 🎲",
        "regions": {"usa": "美国", "americas": "美洲", "europe": "欧洲", "asia": "亚洲", "oceania": "大洋洲"},
        "lottery_names": {
            "powerball": "Powerball 威力球", "mega-millions": "Mega Millions",
            "lotto-max": "Lotto Max", "mega-sena": "Mega-Sena",
            "euromillions": "EuroMillions 欧洲百万", "uk-lotto": "UK Lotto",
            "el-gordo": "El Gordo", "superenalotto": "SuperEnalotto",
            "lotto-6aus49": "Lotto 6aus49",
            "taiwan-bingo": "威力彩", "taiwan-lotto": "大乐透", "daily-cash": "今彩539",
            "korea-lotto": "韩国乐透", "japan-loto6": "日本 Loto 6", "oz-lotto": "Oz Lotto",
        },
        "disclaimer": "⚠️ 彩票有风险，请理性投注",
        "nav_lottery": "彩票", "nav_tools": "工具", "nav_home": "首页",
        "about": "关于", "contact": "联系", "privacy": "隐私", "terms": "条款",
        "no_lotteries": "此语言版本仅提供选号工具，彩种信息请切换至英文版查看。",
    },
}

# Region display order
REGION_ORDER = ["usa", "americas", "europe", "asia", "oceania"]
REGION_LOTTERIES = {
    "usa": ["powerball", "mega-millions"],
    "americas": ["lotto-max", "mega-sena"],
    "europe": ["euromillions", "uk-lotto", "el-gordo", "superenalotto", "lotto-6aus49"],
    "asia": ["taiwan-bingo", "taiwan-lotto", "daily-cash", "korea-lotto", "japan-loto6"],
    "oceania": ["oz-lotto"],
}


def scan_existing_lotteries(lang_folder_path):
    """掃描語言資料夾，回傳實際存在的彩種 slug 清單"""
    existing = []
    if not os.path.isdir(lang_folder_path):
        return existing
    files = os.listdir(lang_folder_path)
    for slug in ALL_LOTTERIES:
        # 彩種介紹頁 = {slug}.html
        if f"{slug}.html" in files:
            existing.append(slug)
    return existing


def generate_index_html(lang, existing_lotteries):
    """生成該語言的 index.html"""
    t = I18N[lang]
    folder = LANG_FOLDERS[lang]
    lang_path = f"/lottery/{folder}/" if folder else "/lottery/"
    lang_code = lang.lower().replace("-", "-") if lang != "zh-TW" else "zh-TW"
    
    # HTML lang attribute
    html_lang_map = {
        "zh-TW": "zh-TW", "en": "en", "ja": "ja", "ko": "ko",
        "de": "de", "fr": "fr", "es": "es", "pt": "pt", "id": "id", "zh-CN": "zh-CN"
    }
    html_lang = html_lang_map.get(lang, "en")
    tools_path = f"/tools/{folder}/" if folder else "/tools/"
    
    # Build lottery grid sections - only regions that have at least one existing lottery
    lottery_sections = []
    has_any_lottery = len(existing_lotteries) > 0
    
    if has_any_lottery:
        for region in REGION_ORDER:
            region_lotteries = [s for s in REGION_LOTTERIES[region] if s in existing_lotteries]
            if not region_lotteries:
                continue
            region_name = t["regions"][region]
            cards = []
            for slug in region_lotteries:
                info = LOTTERY_INFO[slug]
                name = t["lottery_names"][slug]
                href = f"{lang_path}{slug}.html"
                cards.append(
                    f'<a href="{href}" class="lottery-card">'
                    f'<div class="flag">{info["flag"]}</div>'
                    f'<div class="lc-name">{name}</div>'
                    f'</a>'
                )
            lottery_sections.append(
                f'<div class="region-title">{region_name}</div>'
                f'<div class="lottery-grid">{"".join(cards)}</div>'
            )
    
    lottery_html = "\n  ".join(lottery_sections) if lottery_sections else (
        f'<div style="background:#FEF3C7;border:1px solid #FDE68A;border-radius:12px;padding:24px;margin:20px 0;text-align:center;color:#92400E;font-size:15px">'
        f'{t["no_lotteries"]}<br><a href="/lottery/en/" style="color:#B45309;font-weight:600;margin-top:8px;display:inline-block">English Version →</a>'
        f'</div>'
    )
    
    # Lang bar
    lang_btns = []
    for l, f in LANG_FOLDERS.items():
        path = f"/lottery/{f}/" if f else "/lottery/"
        active = " active" if l == lang else ""
        label = l
        lang_btns.append(f'<a href="{path}" class="lang-btn{active}">{label}</a>')
    lang_bar = "".join(lang_btns)
    
    # Count existing lotteries for subtitle
    count = len(existing_lotteries)
    subtitle_text = t["subtitle"]
    if count < 15 and count > 0:
        # Replace "15" with actual count in subtitle
        subtitle_text = subtitle_text.replace("15", str(count))
    
    html = f'''<!DOCTYPE html>
<html lang="{html_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t["title"]}</title>
<meta name="description" content="{t["desc"]}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://softglow-ai.com{lang_path}">
<link rel="stylesheet" href="/js/cookie-consent.css">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:#2D3748;background:#fff;line-height:1.7;-webkit-font-smoothing:antialiased}}
a{{color:#B45309;text-decoration:none}}a:hover{{text-decoration:underline;color:#92400E}}
.nav{{position:sticky;top:0;z-index:100;background:rgba(255,255,255,0.97);backdrop-filter:blur(8px);border-bottom:1px solid #E2E8F0}}
.nav-inner{{max-width:1100px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;height:52px}}
.nav-logo{{font-size:17px;font-weight:700;color:#2D3748;letter-spacing:-0.5px}}.nav-logo span{{color:#D97706}}
.nav-links{{display:flex;gap:16px;align-items:center}}.nav-links a{{font-size:13px;color:#4A5568;font-weight:500}}.nav-links a:hover{{color:#D97706;text-decoration:none}}
.breadcrumb{{max-width:1100px;margin:0 auto;padding:12px 20px;font-size:13px;color:#A0AEC0}}.breadcrumb a{{color:#718096}}
.container{{max-width:1100px;margin:0 auto;padding:0 20px}}
.card{{background:#fff;border:1px solid #E2E8F0;border-radius:16px;padding:28px;margin-bottom:20px}}
.btn{{display:inline-block;padding:12px 24px;background:#D97706;color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer}}.btn:hover{{background:#B45309;text-decoration:none;color:#fff}}
.lottery-card{{border:1px solid #E2E8F0;border-radius:12px;padding:16px;transition:all 0.15s;display:block;color:#2D3748}}
.lottery-card:hover{{border-color:#F59E0B;box-shadow:0 2px 12px rgba(217,119,6,0.1);text-decoration:none}}
.lottery-card .flag{{font-size:24px}}.lottery-card .lc-name{{font-weight:600;font-size:15px;margin-top:4px}}
.lottery-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-bottom:24px}}
.region-title{{font-size:18px;font-weight:700;color:#92400E;margin:28px 0 12px;padding-left:8px;border-left:3px solid #F59E0B}}
.lang-bar{{display:flex;gap:6px;flex-wrap:wrap;margin:24px 0}}
.lang-btn{{font-size:12px;padding:4px 12px;border-radius:20px;background:#F7FAFC;border:1px solid #E2E8F0;color:#718096}}
.lang-btn:hover{{background:#FFFBEB;border-color:#FDE68A;text-decoration:none}}
.lang-btn.active{{background:#D97706;color:#fff;border-color:#D97706}}
.ad-slot{{margin:16px 0}}
.footer{{border-top:1px solid #E2E8F0;padding:24px 0;margin-top:40px}}
.footer-inner{{max-width:1100px;margin:0 auto;padding:0 20px;display:flex;flex-wrap:wrap;gap:16px;font-size:12px;color:#A0AEC0}}.footer-inner a{{color:#718096}}
.disclaimer{{font-size:12px;color:#A0AEC0;text-align:center;padding:16px 20px;line-height:1.6}}
@media(max-width:768px){{.lottery-grid{{grid-template-columns:repeat(2,1fr)}}}}
</style>
</head>
<body>
<nav class="nav"><div class="nav-inner">
  <a href="/" class="nav-logo">Soft<span>Glow</span></a>
  <div class="nav-links">
    <a href="{lang_path}">{t["nav_lottery"]}</a>
    <a href="{tools_path}">{t["nav_tools"]}</a>
    <a href="/">{t["nav_home"]}</a>
  </div>
</div></nav>

<div class="breadcrumb"><a href="/">SoftGlow</a> › <a href="{lang_path}">{t["nav_lottery"]}</a></div>
<div class="container">
<div style="padding:24px 0">
  <div class="card" style="text-align:center;background:linear-gradient(135deg,#FFFBEB,#FEF3C7);border-color:#FDE68A">
    <h1>{t["h1"]}</h1>
    <p style="color:#92400E;font-size:15px;margin-top:8px">{subtitle_text}</p>
    <div style="margin-top:16px"><a href="{lang_path}number-generator.html" class="btn">{t["btn"]}</a></div>
  </div>
  <div class="ad-slot" id="ad1"></div>
  {lottery_html}
  <div class="ad-slot" id="ad2"></div>
  <div class="lang-bar">{lang_bar}</div>
</div>
</div>
<div class="disclaimer">{t["disclaimer"]}</div>
<footer class="footer"><div class="footer-inner">
  <a href="/about.html">{t["about"]}</a>
  <a href="/contact.html">{t["contact"]}</a>
  <a href="/privacy.html">{t["privacy"]}</a>
  <a href="/terms.html">{t["terms"]}</a>
  <span style="margin-left:auto">© 2026 SoftGlow</span>
</div></footer>
<script>document.querySelectorAll('.faq-q').forEach(function(q){{q.addEventListener('click',function(){{this.parentElement.classList.toggle('open')}})}})</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1768270548115739" crossorigin="anonymous"></script>
<script src="/js/softglow-cookies.js" defer></script>
</body></html>'''
    return html


def main():
    print("=" * 60)
    print("修復彩票 index.html — 只顯示實際存在的彩種")
    print("=" * 60)
    
    if not os.path.isdir(BASE_DIR):
        print(f"❌ 找不到目錄: {BASE_DIR}")
        print("   請確認在 D:\\xian-shang-you-wei\\backend 下執行")
        return
    
    total_fixed = 0
    
    for lang, folder in LANG_FOLDERS.items():
        if folder:
            lang_dir = os.path.join(BASE_DIR, folder)
        else:
            lang_dir = BASE_DIR
        
        existing = scan_existing_lotteries(lang_dir)
        
        index_path = os.path.join(lang_dir, "index.html")
        
        # Generate new index
        html = generate_index_html(lang, existing)
        
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        total_fixed += 1
        lottery_count = len(existing)
        status = f"✅ {lottery_count} 彩種" if lottery_count > 0 else "⚠️ 僅工具頁"
        print(f"  {lang:6s} → {status:20s} | {index_path}")
    
    print()
    print(f"共修復 {total_fixed} 個 index.html")
    print()
    print("各語言彩種分佈：")
    for lang, folder in LANG_FOLDERS.items():
        lang_dir = os.path.join(BASE_DIR, folder) if folder else BASE_DIR
        existing = scan_existing_lotteries(lang_dir)
        if existing:
            print(f"  {lang:6s}: {', '.join(existing)}")
        else:
            print(f"  {lang:6s}: (僅工具頁)")


if __name__ == "__main__":
    main()
