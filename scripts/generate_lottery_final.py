#!/usr/bin/env python3
"""
generate_lottery.py v2 — 靜態彩票站生成器
248 頁：15彩種×4頁(各國語言) + 12工具×10語言 + 首頁/入口×10語言

用法: python gen_v2.py --data-dir lottery_data --output-dir output/lottery
"""
import json, os, sys, argparse, html as html_mod
from collections import Counter, defaultdict

# ============================================================
# 1. CONFIG
# ============================================================
LOTTERIES = [
    {"slug":"powerball","name":"Powerball","flag":"[USA]","country":"USA","region":"USA",
     "pick":5,"pick_range":69,"bonus":1,"bonus_range":26,
     "draw_days":"Mon/Wed/Sat","draw_time":"22:59 ET","currency":"USD","bet":"$2",
     "odds_jackpot":"1:292,201,338","odds_any":"1:24.87",
     "langs":["en"]},
    {"slug":"mega-millions","name":"Mega Millions","flag":"[USA]","country":"USA","region":"USA",
     "pick":5,"pick_range":70,"bonus":1,"bonus_range":24,
     "draw_days":"Tue/Fri","draw_time":"23:00 ET","currency":"USD","bet":"$2",
     "odds_jackpot":"1:302,575,350","odds_any":"1:24",
     "langs":["en"]},
    {"slug":"euromillions","name":"EuroMillions","flag":"[EU]","country":"Europe","region":"Europe",
     "pick":5,"pick_range":50,"bonus":2,"bonus_range":12,
     "draw_days":"Tue/Fri","draw_time":"21:00 CET","currency":"EUR","bet":"€2.50",
     "odds_jackpot":"1:139,838,160","odds_any":"1:13",
     "langs":["en","fr","de","es","pt"]},
    {"slug":"lotto-max","name":"Lotto Max","flag":"[CA]","country":"Canada","region":"Americas",
     "pick":7,"pick_range":50,"bonus":0,"bonus_range":0,
     "draw_days":"Tue/Fri","draw_time":"22:30 ET","currency":"CAD","bet":"$5",
     "odds_jackpot":"1:33,294,800","odds_any":"1:7",
     "langs":["en"]},
    {"slug":"uk-lotto","name":"UK Lotto","flag":"[UK]","country":"UK","region":"Europe",
     "pick":6,"pick_range":59,"bonus":0,"bonus_range":0,
     "draw_days":"Wed/Sat","draw_time":"20:00 GMT","currency":"GBP","bet":"£2",
     "odds_jackpot":"1:45,057,474","odds_any":"1:9.3",
     "langs":["en"]},
    {"slug":"el-gordo","name":"El Gordo","flag":"[ES]","country":"Spain","region":"Europe",
     "pick":5,"pick_range":54,"bonus":0,"bonus_range":0,
     "draw_days":"Sun","draw_time":"21:30 CET","currency":"EUR","bet":"€1.50",
     "odds_jackpot":"1:31,625,100","odds_any":"1:8",
     "langs":["en","es"]},
    {"slug":"superenalotto","name":"SuperEnalotto","flag":"[IT]","country":"Italy","region":"Europe",
     "pick":6,"pick_range":90,"bonus":1,"bonus_range":90,
     "draw_days":"Tue/Thu/Fri/Sat","draw_time":"20:00 CET","currency":"EUR","bet":"€1",
     "odds_jackpot":"1:622,614,630","odds_any":"1:20",
     "langs":["en"]},
    {"slug":"lotto-6aus49","name":"Lotto 6aus49","flag":"[DE]","country":"Germany","region":"Europe",
     "pick":6,"pick_range":49,"bonus":1,"bonus_range":9,
     "draw_days":"Wed/Sat","draw_time":"18:25 CET","currency":"EUR","bet":"€1.20",
     "odds_jackpot":"1:139,838,160","odds_any":"1:31",
     "langs":["en","de"]},
    {"slug":"oz-lotto","name":"Oz Lotto","flag":"[AU]","country":"Australia","region":"Oceania",
     "pick":7,"pick_range":47,"bonus":2,"bonus_range":47,
     "draw_days":"Tue","draw_time":"20:30 AEST","currency":"AUD","bet":"A$1.50",
     "odds_jackpot":"1:45,379,620","odds_any":"1:55",
     "langs":["en"]},
    {"slug":"taiwan-bingo","name_zh":"威力彩","name":"Power Lottery","flag":"[TW]","country":"Taiwan","region":"Asia",
     "pick":6,"pick_range":38,"bonus":1,"bonus_range":8,
     "draw_days":"Mon/Thu","draw_time":"20:30 CST","currency":"TWD","bet":"NT$100",
     "odds_jackpot":"1:22,085,448","odds_any":"1:7",
     "langs":["zh-TW","en"]},
    {"slug":"taiwan-lotto","name_zh":"大樂透","name":"Super Lotto","flag":"[TW]","country":"Taiwan","region":"Asia",
     "pick":6,"pick_range":49,"bonus":1,"bonus_range":49,
     "draw_days":"Tue/Fri","draw_time":"20:30 CST","currency":"TWD","bet":"NT$50",
     "odds_jackpot":"1:13,983,816","odds_any":"1:43",
     "langs":["zh-TW","en"]},
    {"slug":"daily-cash","name_zh":"今彩539","name":"Daily Cash 539","flag":"[TW]","country":"Taiwan","region":"Asia",
     "pick":5,"pick_range":39,"bonus":0,"bonus_range":0,
     "draw_days":"Mon-Sat","draw_time":"20:30 CST","currency":"TWD","bet":"NT$50",
     "odds_jackpot":"1:575,757","odds_any":"1:9",
     "langs":["zh-TW","en"]},
    {"slug":"mega-sena","name":"Mega-Sena","flag":"[BR]","country":"Brazil","region":"Americas",
     "pick":6,"pick_range":60,"bonus":0,"bonus_range":0,
     "draw_days":"Tue/Thu/Sat","draw_time":"20:00 BRT","currency":"BRL","bet":"R$5",
     "odds_jackpot":"1:50,063,860","odds_any":"1:97",
     "langs":["en","pt"]},
    {"slug":"korea-lotto","name_ko":"로또 6/45","name":"Korea Lotto 6/45","flag":"[KR]","country":"Korea","region":"Asia",
     "pick":6,"pick_range":45,"bonus":1,"bonus_range":45,
     "draw_days":"Sat","draw_time":"20:45 KST","currency":"KRW","bet":"₩1,000",
     "odds_jackpot":"1:8,145,060","odds_any":"1:45",
     "langs":["ko","en"]},
    {"slug":"japan-loto6","name_ja":"ロト6","name":"Japan Loto 6","flag":"[JP]","country":"Japan","region":"Asia",
     "pick":6,"pick_range":43,"bonus":1,"bonus_range":43,
     "draw_days":"Mon/Thu","draw_time":"18:45 JST","currency":"JPY","bet":"¥200",
     "odds_jackpot":"1:6,096,454","odds_any":"1:39",
     "langs":["ja","en"]},
]

LOTTERY_MAP = {l["slug"]: l for l in LOTTERIES}
ALL_LANGS = ["zh-TW","en","ja","ko","fr","de","es","pt","id","zh-CN"]
REGIONS_ORDER = ["USA","Americas","Europe","Asia","Oceania"]


# Lottery display names per language
LOTTERY_NAMES = {
    "powerball":{"en":"Powerball","zh-TW":"Powerball 威力球","ja":"パワーボール","ko":"파워볼","fr":"Powerball","de":"Powerball","es":"Powerball","pt":"Powerball","id":"Powerball","zh-CN":"Powerball 强力球"},
    "mega-millions":{"en":"Mega Millions","zh-TW":"Mega Millions","ja":"メガミリオンズ","ko":"메가밀리언즈","fr":"Mega Millions","de":"Mega Millions","es":"Mega Millions","pt":"Mega Millions","id":"Mega Millions","zh-CN":"Mega Millions"},
    "euromillions":{"en":"EuroMillions","zh-TW":"EuroMillions","ja":"ユーロミリオンズ","ko":"유로밀리언즈","fr":"EuroMillions","de":"EuroMillions","es":"EuroMillones","pt":"EuroMilhões","id":"EuroMillions","zh-CN":"EuroMillions"},
    "lotto-max":{"en":"Lotto Max","zh-TW":"Lotto Max","ja":"ロトマックス","ko":"로또 맥스","fr":"Lotto Max","de":"Lotto Max","es":"Lotto Max","pt":"Lotto Max","id":"Lotto Max","zh-CN":"Lotto Max"},
    "uk-lotto":{"en":"UK Lotto","zh-TW":"UK Lotto","ja":"UKロト","ko":"UK 로또","fr":"UK Lotto","de":"UK Lotto","es":"UK Lotto","pt":"UK Lotto","id":"UK Lotto","zh-CN":"UK Lotto"},
    "el-gordo":{"en":"El Gordo","es":"El Gordo","zh-TW":"El Gordo","ja":"エル・ゴルド","ko":"엘 고르도","fr":"El Gordo","de":"El Gordo","pt":"El Gordo","id":"El Gordo","zh-CN":"El Gordo"},
    "superenalotto":{"en":"SuperEnalotto","zh-TW":"SuperEnalotto","ja":"スーパーエナロット","ko":"수퍼에날로또","fr":"SuperEnalotto","de":"SuperEnalotto","es":"SuperEnalotto","pt":"SuperEnalotto","id":"SuperEnalotto","zh-CN":"SuperEnalotto"},
    "lotto-6aus49":{"en":"Lotto 6aus49","de":"Lotto 6aus49","zh-TW":"Lotto 6aus49","ja":"ロト 6aus49","ko":"로또 6aus49","fr":"Lotto 6aus49","es":"Lotto 6aus49","pt":"Lotto 6aus49","id":"Lotto 6aus49","zh-CN":"Lotto 6aus49"},
    "oz-lotto":{"en":"Oz Lotto","zh-TW":"Oz Lotto","ja":"オズロト","ko":"오즈 로또","fr":"Oz Lotto","de":"Oz Lotto","es":"Oz Lotto","pt":"Oz Lotto","id":"Oz Lotto","zh-CN":"Oz Lotto"},
    "taiwan-bingo":{"zh-TW":"威力彩","en":"Taiwan Power Lottery","ja":"台湾パワー宝くじ","ko":"대만 파워복권","fr":"Loterie Taiwan","de":"Taiwan Lotterie","es":"Lotería Taiwan","pt":"Loteria Taiwan","id":"Lotre Taiwan","zh-CN":"威力彩"},
    "taiwan-lotto":{"zh-TW":"大樂透","en":"Taiwan Super Lotto","ja":"台湾スーパーロト","ko":"대만 슈퍼로또","fr":"Super Loto Taiwan","de":"Taiwan Super Lotto","es":"Super Loto Taiwan","pt":"Super Loto Taiwan","id":"Super Loto Taiwan","zh-CN":"大乐透"},
    "daily-cash":{"zh-TW":"今彩539","en":"Daily Cash 539","ja":"今彩539","ko":"데일리캐시 539","fr":"Daily Cash 539","de":"Daily Cash 539","es":"Daily Cash 539","pt":"Daily Cash 539","id":"Daily Cash 539","zh-CN":"今彩539"},
    "mega-sena":{"en":"Mega-Sena","pt":"Mega-Sena","zh-TW":"Mega-Sena","ja":"メガセナ","ko":"메가세나","fr":"Mega-Sena","de":"Mega-Sena","es":"Mega-Sena","id":"Mega-Sena","zh-CN":"Mega-Sena"},
    "korea-lotto":{"ko":"로또 6/45","en":"Korea Lotto 6/45","zh-TW":"韓國樂透","ja":"韓国ロト 6/45","fr":"Loto Corée","de":"Korea Lotto","es":"Loto Corea","pt":"Loto Coreia","id":"Loto Korea","zh-CN":"韩国乐透"},
    "japan-loto6":{"ja":"ロト6","en":"Japan Loto 6","zh-TW":"日本樂透6","ko":"일본 로또 6","fr":"Loto 6 Japon","de":"Japan Loto 6","es":"Loto 6 Japón","pt":"Loto 6 Japão","id":"Loto 6 Jepang","zh-CN":"日本乐透6"},
}

# ============================================================
# 2. I18N (10 languages — essential UI strings)
# ============================================================
I18N = {
  "zh-TW":{"site":"SoftGlow 全球彩票","home":"首頁","tools":"工具","lottery":"彩票","results":"開獎結果","history":"歷史紀錄","statistics":"統計分析","number_generator":"選號工具","latest":"最新開獎號碼","draw_date":"開獎日期","numbers":"開獎號碼","bonus":"特別號","jackpot":"頭獎","hot":"熱門號碼","cold":"冷門號碼","frequency":"出現次數","last_seen":"上次出現","draws_ago":"期前","total_draws":"總開獎期數","generate":"產生號碼","try_again":"再試一次","draw_days":"開獎日","draw_time":"開獎時間","odds":"中獎機率","format":"選號格式","no_data":"暫無資料","prev":"上一頁","next":"下一頁","copyright":"© 2026 SoftGlow","about":"關於我們","contact":"聯繫我們","privacy":"隱私政策","terms":"使用條款","faq":"常見問題","rules":"遊戲規則","prize":"獎金結構","how_to":"怎麼玩","all_lotteries":"所有彩票","play_safe":"理性投注，量力而為","select_lottery":"選擇彩種","select_method":"選擇方式","your_nums":"你的號碼","from_range":"從 1-{r} 選 {p} 個","plus_bonus":"+ 特別號 1-{r} 選 {b} 個","view_history":"查看完整歷史","region_usa":"美國","region_americas":"美洲","region_europe":"歐洲","region_asia":"亞洲","region_oceania":"大洋洲","loading":"載入中...","claim":"領獎方式","tax":"稅務資訊","search_date":"日期搜尋","search_num":"號碼搜尋","year_stats":"年度統計","history_intro":"歷史大事記","trend":"號碼趨勢","more_stats":"查看完整統計","load_more":"載入更多"},
  "en":{"site":"SoftGlow Global Lottery","home":"Home","tools":"Tools","lottery":"Lottery","results":"Results","history":"History","statistics":"Statistics","number_generator":"Number Generator","latest":"Latest Winning Numbers","draw_date":"Draw Date","numbers":"Winning Numbers","bonus":"Bonus","jackpot":"Jackpot","hot":"Hot Numbers","cold":"Cold Numbers","frequency":"Frequency","last_seen":"Last Seen","draws_ago":"draws ago","total_draws":"Total Draws","generate":"Generate","try_again":"Try Again","draw_days":"Draw Days","draw_time":"Draw Time","odds":"Odds","format":"Number Format","no_data":"No data available","prev":"Previous","next":"Next","copyright":"© 2026 SoftGlow","about":"About","contact":"Contact","privacy":"Privacy","terms":"Terms","faq":"FAQ","rules":"Game Rules","prize":"Prize Structure","how_to":"How to Play","all_lotteries":"All Lotteries","play_safe":"Please play responsibly","select_lottery":"Select Lottery","select_method":"Select Method","your_nums":"Your Numbers","from_range":"Pick {p} from 1-{r}","plus_bonus":"+ Bonus {b} from 1-{r}","view_history":"View Full History","region_usa":"USA","region_americas":"Americas","region_europe":"Europe","region_asia":"Asia","region_oceania":"Oceania","loading":"Loading...","claim":"How to Claim","tax":"Tax Info","search_date":"Search by Date","search_num":"Search by Number","year_stats":"Year Statistics","history_intro":"History & Milestones","trend":"Number Trends","more_stats":"Full Statistics","load_more":"Load More"},
  "ja":{"site":"SoftGlow 宝くじ","home":"ホーム","tools":"ツール","lottery":"宝くじ","results":"抽選結果","history":"履歴","statistics":"統計","number_generator":"番号生成","latest":"最新当選番号","draw_date":"抽選日","numbers":"当選番号","bonus":"ボーナス","jackpot":"ジャックポット","hot":"ホット番号","cold":"コールド番号","frequency":"出現回数","last_seen":"最後に出現","draws_ago":"回前","total_draws":"総抽選回数","generate":"番号を生成","try_again":"もう一度","draw_days":"抽選日","draw_time":"抽選時間","odds":"当選確率","format":"番号形式","no_data":"データなし","prev":"前へ","next":"次へ","copyright":"© 2026 SoftGlow","about":"概要","contact":"お問い合わせ","privacy":"プライバシー","terms":"利用規約","faq":"よくある質問","rules":"ルール","prize":"賞金構成","how_to":"遊び方","all_lotteries":"すべての宝くじ","play_safe":"責任を持って","select_lottery":"宝くじを選択","select_method":"方法を選択","your_nums":"あなたの番号","from_range":"1-{r}から{p}個","plus_bonus":"+ ボーナス 1-{r}から{b}個","view_history":"全履歴","region_usa":"アメリカ","region_americas":"アメリカ大陸","region_europe":"ヨーロッパ","region_asia":"アジア","region_oceania":"オセアニア","loading":"読み込み中...","claim":"受取方法","tax":"税金","search_date":"日付検索","search_num":"番号検索","year_stats":"年度統計","history_intro":"歴史","trend":"番号トレンド","more_stats":"統計詳細","load_more":"もっと見る"},
  "ko":{"site":"SoftGlow 복권","home":"홈","tools":"도구","lottery":"복권","results":"추첨 결과","history":"역사","statistics":"통계","number_generator":"번호 생성기","latest":"최신 당첨 번호","draw_date":"추첨일","numbers":"당첨 번호","bonus":"보너스","jackpot":"잭팟","hot":"핫 번호","cold":"콜드 번호","frequency":"출현 횟수","last_seen":"마지막 출현","draws_ago":"회 전","total_draws":"총 추첨 횟수","generate":"번호 생성","try_again":"다시","draw_days":"추첨 요일","draw_time":"추첨 시간","odds":"확률","format":"번호 형식","no_data":"데이터 없음","prev":"이전","next":"다음","copyright":"© 2026 SoftGlow","about":"소개","contact":"연락처","privacy":"개인정보","terms":"이용약관","faq":"자주 묻는 질문","rules":"규칙","prize":"상금 구조","how_to":"참여 방법","all_lotteries":"모든 복권","play_safe":"건전한 이용 부탁드립니다","select_lottery":"복권 선택","select_method":"방법 선택","your_nums":"당신의 번호","from_range":"1-{r}에서 {p}개","plus_bonus":"+ 보너스 1-{r}에서 {b}개","view_history":"전체 기록","region_usa":"미국","region_americas":"아메리카","region_europe":"유럽","region_asia":"아시아","region_oceania":"오세아니아","loading":"로딩 중...","claim":"수령 방법","tax":"세금","search_date":"날짜 검색","search_num":"번호 검색","year_stats":"연도 통계","history_intro":"역사","trend":"번호 트렌드","more_stats":"통계 상세","load_more":"더 보기"},
  "fr":{"site":"SoftGlow Loterie","home":"Accueil","tools":"Outils","lottery":"Loterie","results":"Résultats","history":"Historique","statistics":"Statistiques","number_generator":"Générateur","latest":"Derniers numéros","draw_date":"Date","numbers":"Numéros","bonus":"Bonus","jackpot":"Jackpot","hot":"Numéros chauds","cold":"Numéros froids","frequency":"Fréquence","last_seen":"Vu dernièrement","draws_ago":"tirages","total_draws":"Total tirages","generate":"Générer","try_again":"Réessayer","draw_days":"Jours de tirage","draw_time":"Heure","odds":"Probabilité","format":"Format","no_data":"Pas de données","prev":"Précédent","next":"Suivant","copyright":"© 2026 SoftGlow","about":"À propos","contact":"Contact","privacy":"Confidentialité","terms":"Conditions","faq":"FAQ","rules":"Règles","prize":"Gains","how_to":"Comment jouer","all_lotteries":"Toutes les loteries","play_safe":"Jouez responsablement","select_lottery":"Choisir loterie","select_method":"Choisir méthode","your_nums":"Vos numéros","from_range":"Choisir {p} de 1-{r}","plus_bonus":"+ Bonus {b} de 1-{r}","view_history":"Historique complet","region_usa":"USA","region_americas":"Amériques","region_europe":"Europe","region_asia":"Asie","region_oceania":"Océanie","loading":"Chargement...","claim":"Réclamation","tax":"Impôts","search_date":"Recherche date","search_num":"Recherche numéro","year_stats":"Stats annuelles","history_intro":"Histoire","trend":"Tendances","more_stats":"Stats complètes","load_more":"Plus"},
  "de":{"site":"SoftGlow Lotterie","home":"Startseite","tools":"Werkzeuge","lottery":"Lotterie","results":"Ergebnisse","history":"Geschichte","statistics":"Statistiken","number_generator":"Zahlengenerator","latest":"Neueste Zahlen","draw_date":"Datum","numbers":"Gewinnzahlen","bonus":"Bonus","jackpot":"Jackpot","hot":"Heiße Zahlen","cold":"Kalte Zahlen","frequency":"Häufigkeit","last_seen":"Zuletzt","draws_ago":"Ziehungen","total_draws":"Gesamtziehungen","generate":"Generieren","try_again":"Nochmal","draw_days":"Ziehungstage","draw_time":"Ziehungszeit","odds":"Quote","format":"Format","no_data":"Keine Daten","prev":"Zurück","next":"Weiter","copyright":"© 2026 SoftGlow","about":"Über uns","contact":"Kontakt","privacy":"Datenschutz","terms":"AGB","faq":"FAQ","rules":"Spielregeln","prize":"Gewinnplan","how_to":"So spielen Sie","all_lotteries":"Alle Lotterien","play_safe":"Spielen Sie verantwortungsvoll","select_lottery":"Lotterie wählen","select_method":"Methode wählen","your_nums":"Ihre Zahlen","from_range":"{p} aus 1-{r} wählen","plus_bonus":"+ Bonus {b} aus 1-{r}","view_history":"Alle Ergebnisse","region_usa":"USA","region_americas":"Amerika","region_europe":"Europa","region_asia":"Asien","region_oceania":"Ozeanien","loading":"Laden...","claim":"Gewinne abholen","tax":"Steuern","search_date":"Datumssuche","search_num":"Zahlensuche","year_stats":"Jahresstatistik","history_intro":"Geschichte","trend":"Trends","more_stats":"Alle Statistiken","load_more":"Mehr"},
  "es":{"site":"SoftGlow Lotería","home":"Inicio","tools":"Herramientas","lottery":"Lotería","results":"Resultados","history":"Historial","statistics":"Estadísticas","number_generator":"Generador","latest":"Últimos números","draw_date":"Fecha","numbers":"Números","bonus":"Bonus","jackpot":"Bote","hot":"Números calientes","cold":"Números fríos","frequency":"Frecuencia","last_seen":"Última vez","draws_ago":"sorteos","total_draws":"Total sorteos","generate":"Generar","try_again":"Reintentar","draw_days":"Días de sorteo","draw_time":"Hora","odds":"Probabilidad","format":"Formato","no_data":"Sin datos","prev":"Anterior","next":"Siguiente","copyright":"© 2026 SoftGlow","about":"Acerca de","contact":"Contacto","privacy":"Privacidad","terms":"Términos","faq":"FAQ","rules":"Reglas","prize":"Premios","how_to":"Cómo jugar","all_lotteries":"Todas las loterías","play_safe":"Juega responsablemente","select_lottery":"Elegir lotería","select_method":"Elegir método","your_nums":"Tus números","from_range":"Elegir {p} de 1-{r}","plus_bonus":"+ Bonus {b} de 1-{r}","view_history":"Historial completo","region_usa":"EE.UU.","region_americas":"Américas","region_europe":"Europa","region_asia":"Asia","region_oceania":"Oceanía","loading":"Cargando...","claim":"Cobrar premios","tax":"Impuestos","search_date":"Buscar fecha","search_num":"Buscar número","year_stats":"Stats anuales","history_intro":"Historia","trend":"Tendencias","more_stats":"Stats completas","load_more":"Más"},
  "pt":{"site":"SoftGlow Loteria","home":"Início","tools":"Ferramentas","lottery":"Loteria","results":"Resultados","history":"Histórico","statistics":"Estatísticas","number_generator":"Gerador","latest":"Últimos números","draw_date":"Data","numbers":"Números","bonus":"Bônus","jackpot":"Jackpot","hot":"Números quentes","cold":"Números frios","frequency":"Frequência","last_seen":"Última vez","draws_ago":"sorteios","total_draws":"Total sorteios","generate":"Gerar","try_again":"Tentar novamente","draw_days":"Dias de sorteio","draw_time":"Hora","odds":"Probabilidade","format":"Formato","no_data":"Sem dados","prev":"Anterior","next":"Próximo","copyright":"© 2026 SoftGlow","about":"Sobre","contact":"Contato","privacy":"Privacidade","terms":"Termos","faq":"FAQ","rules":"Regras","prize":"Prêmios","how_to":"Como jogar","all_lotteries":"Todas as loterias","play_safe":"Jogue com responsabilidade","select_lottery":"Escolher loteria","select_method":"Escolher método","your_nums":"Seus números","from_range":"Escolher {p} de 1-{r}","plus_bonus":"+ Bônus {b} de 1-{r}","view_history":"Histórico completo","region_usa":"EUA","region_americas":"Américas","region_europe":"Europa","region_asia":"Ásia","region_oceania":"Oceania","loading":"Carregando...","claim":"Como resgatar","tax":"Impostos","search_date":"Buscar data","search_num":"Buscar número","year_stats":"Stats anuais","history_intro":"História","trend":"Tendências","more_stats":"Stats completas","load_more":"Mais"},
  "id":{"site":"SoftGlow Lotere","home":"Beranda","tools":"Alat","lottery":"Lotere","results":"Hasil","history":"Riwayat","statistics":"Statistik","number_generator":"Generator Nomor","latest":"Nomor terbaru","draw_date":"Tanggal","numbers":"Nomor","bonus":"Bonus","jackpot":"Jackpot","hot":"Nomor panas","cold":"Nomor dingin","frequency":"Frekuensi","last_seen":"Terakhir","draws_ago":"undian lalu","total_draws":"Total undian","generate":"Hasilkan","try_again":"Coba lagi","draw_days":"Hari undian","draw_time":"Waktu","odds":"Peluang","format":"Format","no_data":"Tidak ada data","prev":"Sebelumnya","next":"Berikutnya","copyright":"© 2026 SoftGlow","about":"Tentang","contact":"Kontak","privacy":"Privasi","terms":"Ketentuan","faq":"FAQ","rules":"Aturan","prize":"Hadiah","how_to":"Cara bermain","all_lotteries":"Semua lotere","play_safe":"Bermain secara bertanggung jawab","select_lottery":"Pilih lotere","select_method":"Pilih metode","your_nums":"Nomor Anda","from_range":"Pilih {p} dari 1-{r}","plus_bonus":"+ Bonus {b} dari 1-{r}","view_history":"Riwayat lengkap","region_usa":"AS","region_americas":"Amerika","region_europe":"Eropa","region_asia":"Asia","region_oceania":"Oseania","loading":"Memuat...","claim":"Klaim hadiah","tax":"Pajak","search_date":"Cari tanggal","search_num":"Cari nomor","year_stats":"Statistik tahunan","history_intro":"Sejarah","trend":"Tren nomor","more_stats":"Statistik lengkap","load_more":"Lebih banyak"},
  "zh-CN":{"site":"SoftGlow 全球彩票","home":"首页","tools":"工具","lottery":"彩票","results":"开奖结果","history":"历史记录","statistics":"统计分析","number_generator":"选号工具","latest":"最新开奖号码","draw_date":"开奖日期","numbers":"开奖号码","bonus":"特别号","jackpot":"头奖","hot":"热门号码","cold":"冷门号码","frequency":"出现次数","last_seen":"上次出现","draws_ago":"期前","total_draws":"总开奖期数","generate":"生成号码","try_again":"再试一次","draw_days":"开奖日","draw_time":"开奖时间","odds":"中奖概率","format":"选号格式","no_data":"暂无数据","prev":"上一页","next":"下一页","copyright":"© 2026 SoftGlow","about":"关于我们","contact":"联系我们","privacy":"隐私政策","terms":"使用条款","faq":"常见问题","rules":"游戏规则","prize":"奖金结构","how_to":"怎么玩","all_lotteries":"所有彩票","play_safe":"理性投注","select_lottery":"选择彩种","select_method":"选择方式","your_nums":"你的号码","from_range":"从 1-{r} 选 {p} 个","plus_bonus":"+ 特别号 1-{r} 选 {b} 个","view_history":"查看完整历史","region_usa":"美国","region_americas":"美洲","region_europe":"欧洲","region_asia":"亚洲","region_oceania":"大洋洲","loading":"加载中...","claim":"领奖方式","tax":"税务信息","search_date":"日期搜索","search_num":"号码搜索","year_stats":"年度统计","history_intro":"历史大事记","trend":"号码趋势","more_stats":"完整统计","load_more":"加载更多"},
}

def t(lang, key, **kw):
    s = I18N.get(lang, I18N["en"]).get(key, I18N["en"].get(key, key))
    for k, v in kw.items():
        s = s.replace("{" + k + "}", str(v))
    return s

def lname(slug, lang):
    return LOTTERY_NAMES.get(slug, {}).get(lang, LOTTERY_MAP.get(slug, {}).get("name", slug))

def esc(s):
    return html_mod.escape(str(s)) if s else ""


# ============================================================
# 3. URL + HELPERS
# ============================================================
def page_url(lang, slug=None, ptype=None):
    base = "/lottery"
    if not slug and not ptype:
        return f"{base}/" if lang == "zh-TW" else f"{base}/{lang}/"
    if slug:
        suffix = f"-{ptype}" if ptype and ptype != "intro" else ""
        if lang == "zh-TW":
            return f"{base}/{slug}{suffix}.html"
        return f"{base}/{lang}/{slug}{suffix}.html"
    # tool pages
    if ptype:
        if lang == "zh-TW":
            return f"{base}/{ptype}.html"
        return f"{base}/{lang}/{ptype}.html"
    return base + "/"

def full_url(path):
    return f"https://softglow-ai.com{path}"

def hreflang_tags(slug, ptype, langs):
    tags = []
    for la in langs:
        url = full_url(page_url(la, slug, ptype))
        code = "zh-Hant-TW" if la == "zh-TW" else ("zh-Hans-CN" if la == "zh-CN" else la)
        tags.append(f'<link rel="alternate" hreflang="{code}" href="{url}">')
    en_url = full_url(page_url("en", slug, ptype))
    tags.append(f'<link rel="alternate" hreflang="x-default" href="{en_url}">')
    return "\n".join(tags)

def balls_html(nums, bonus=None):
    h = "".join(f'<span class="ball ball-main">{n}</span>' for n in nums)
    if bonus:
        h += '<span class="draw-plus">+</span>'
        h += "".join(f'<span class="ball ball-bonus">{n}</span>' for n in bonus)
    return h

# ============================================================
# 4. CSS (shared across all pages)
# ============================================================
CSS = '''
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;color:#2D3748;background:#fff;line-height:1.7;-webkit-font-smoothing:antialiased}
a{color:#B45309;text-decoration:none}a:hover{text-decoration:underline;color:#92400E}
.nav{position:sticky;top:0;z-index:100;background:rgba(255,255,255,0.97);backdrop-filter:blur(8px);border-bottom:1px solid #E2E8F0}
.nav-inner{max-width:1100px;margin:0 auto;padding:0 20px;display:flex;align-items:center;justify-content:space-between;height:52px}
.nav-logo{font-size:17px;font-weight:700;color:#2D3748;letter-spacing:-0.5px}.nav-logo span{color:#D97706}
.nav-links{display:flex;gap:16px;align-items:center}.nav-links a{font-size:13px;color:#4A5568;font-weight:500}.nav-links a:hover{color:#D97706;text-decoration:none}
.subnav{background:#FFFBEB;border-bottom:1px solid #FDE68A;overflow-x:auto}
.subnav-inner{max-width:1100px;margin:0 auto;padding:0 20px;display:flex;gap:4px;white-space:nowrap}
.subnav a{display:inline-block;padding:10px 16px;font-size:13px;font-weight:500;color:#92400E;border-bottom:2px solid transparent}
.subnav a:hover{color:#D97706;text-decoration:none}.subnav a.active{color:#D97706;border-bottom-color:#D97706;font-weight:600}
.breadcrumb{max-width:1100px;margin:0 auto;padding:12px 20px;font-size:13px;color:#A0AEC0}.breadcrumb a{color:#718096}
.container{max-width:1100px;margin:0 auto;padding:0 20px}
.layout{display:grid;grid-template-columns:1fr 300px;gap:32px;align-items:start;padding:24px 0}
.card{background:#fff;border:1px solid #E2E8F0;border-radius:16px;padding:28px;margin-bottom:20px}
.card h1{font-size:22px;font-weight:700;color:#1A202C;margin-bottom:8px}
.card h2{font-size:18px;font-weight:700;color:#1A202C;margin:28px 0 14px}.card h2:first-child{margin-top:0}
.card p{margin-bottom:14px;color:#4A5568;font-size:15px}
.ball{display:inline-flex;align-items:center;justify-content:center;width:42px;height:42px;border-radius:50%;font-size:16px;font-weight:700;margin:3px}
.ball-main{background:linear-gradient(135deg,#FEF3C7,#FDE68A);color:#92400E;border:2px solid #F59E0B;box-shadow:0 2px 4px rgba(245,158,11,0.2)}
.ball-bonus{background:linear-gradient(135deg,#DBEAFE,#93C5FD);color:#1E40AF;border:2px solid #3B82F6;box-shadow:0 2px 4px rgba(59,130,246,0.2)}
.draw-card{background:#FFFBEB;border:1px solid #FDE68A;border-radius:12px;padding:20px;margin-bottom:12px}
.draw-card.latest{background:linear-gradient(135deg,#FFFBEB,#FEF3C7);border:2px solid #F59E0B}
.draw-date{font-size:14px;color:#92400E;margin-bottom:8px;font-weight:600}
.draw-label{font-size:12px;color:#B45309;background:#FEF3C7;display:inline-block;padding:2px 10px;border-radius:20px;margin-bottom:8px}
.draw-nums{display:flex;flex-wrap:wrap;gap:4px;align-items:center}
.draw-plus{color:#A0AEC0;font-weight:700;margin:0 6px;font-size:18px}
.draw-row{padding:14px 0;border-bottom:1px solid #F1F5F9;display:flex;align-items:center;gap:12px;flex-wrap:wrap}.draw-row:last-child{border-bottom:none}
.next-draw{background:linear-gradient(135deg,#EBF5FF,#DBEAFE);border:1px solid #93C5FD;border-radius:12px;padding:20px;margin:20px 0;text-align:center}
.next-draw .label{font-size:13px;color:#2563EB;font-weight:600}.next-draw .time{font-size:20px;font-weight:700;color:#1E40AF;margin-top:4px}
.prize-table{width:100%;border-collapse:collapse;margin:16px 0;font-size:14px}
.prize-table th{text-align:left;padding:10px 12px;background:#FFFBEB;border:1px solid #FDE68A;font-weight:600;color:#92400E;font-size:13px}
.prize-table td{padding:10px 12px;border:1px solid #E2E8F0}.prize-table tr:hover{background:#FEFCE8}
.prize-table .jr{background:#FFFBEB;font-weight:600}
.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:16px 0}
.info-item{background:#F7FAFC;border-radius:10px;padding:14px}.info-label{font-size:12px;color:#718096;margin-bottom:2px}.info-value{font-size:16px;font-weight:700;color:#1A202C}
.step-list{counter-reset:step;padding:0;list-style:none;margin:16px 0}
.step-list li{counter-increment:step;padding:12px 12px 12px 48px;position:relative;border-bottom:1px solid #F1F5F9}
.step-list li::before{content:counter(step);position:absolute;left:0;top:12px;width:32px;height:32px;border-radius:50%;background:#FDE68A;color:#92400E;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px}
.tax-note{background:#FEF2F2;border:1px solid #FECACA;border-radius:10px;padding:16px;margin:16px 0;font-size:14px;color:#991B1B}
.summary-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0}
.summary-item{background:linear-gradient(135deg,#FFFBEB,#FEF3C7);border:1px solid #FDE68A;border-radius:12px;padding:20px;text-align:center}
.summary-item .num{font-size:24px;font-weight:800;color:#B45309}.summary-item .label{font-size:13px;color:#92400E;margin-top:4px}
.search-box{display:flex;gap:8px;margin:16px 0}
.search-box input,.search-box select{flex:1;padding:10px 14px;border:1px solid #CBD5E0;border-radius:8px;font-size:15px;outline:none}
.search-box input:focus,.search-box select:focus{border-color:#F59E0B;box-shadow:0 0 0 3px rgba(245,158,11,0.1)}
.search-box button{padding:10px 20px;background:#D97706;color:#fff;border:none;border-radius:8px;font-weight:600;cursor:pointer;white-space:nowrap}.search-box button:hover{background:#B45309}
.search-result{background:#FFFBEB;border:1px solid #FDE68A;border-radius:10px;padding:16px;margin:12px 0;display:none}.search-result.show{display:block}
.stat-bar{display:flex;align-items:center;gap:8px;padding:6px 0}
.stat-num{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;flex-shrink:0}
.stat-num.hot{background:#FEF3C7;color:#B45309;border:1px solid #F59E0B}.stat-num.cold{background:#EFF6FF;color:#2563EB;border:1px solid #93C5FD}
.stat-fill{height:20px;border-radius:4px}.stat-fill.hot{background:linear-gradient(90deg,#FDE68A,#F59E0B)}.stat-fill.cold{background:linear-gradient(90deg,#BFDBFE,#3B82F6)}
.stat-count{font-size:12px;color:#718096;min-width:60px}
.hot-strip{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}
.hot-num{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;background:#FEF3C7;color:#B45309;border:1px solid #F59E0B}
.cold-num{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;background:#EFF6FF;color:#2563EB;border:1px solid #93C5FD}
.gen-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px;margin:16px 0}
.gen-btn{padding:14px 12px;border:1px solid #E2E8F0;border-radius:10px;text-align:center;cursor:pointer;font-size:13px;font-weight:500;color:#4A5568;background:#FAFAFA;transition:all 0.15s}
.gen-btn:hover{border-color:#F59E0B;background:#FFFBEB;color:#B45309}
.gen-btn.active{border-color:#F59E0B;background:#FFFBEB;color:#B45309;font-weight:600}
.gen-result{background:#FFFBEB;border:2px solid #FDE68A;border-radius:12px;padding:24px;text-align:center;margin:16px 0;min-height:80px}
.btn{display:inline-block;padding:12px 24px;background:#D97706;color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer}.btn:hover{background:#B45309;text-decoration:none;color:#fff}
.lottery-card{border:1px solid #E2E8F0;border-radius:12px;padding:16px;transition:all 0.15s;display:block;color:#2D3748}
.lottery-card:hover{border-color:#F59E0B;box-shadow:0 2px 12px rgba(217,119,6,0.1);text-decoration:none}
.lottery-card .flag{font-size:24px}.lottery-card .lc-name{font-weight:600;font-size:15px;margin-top:4px}.lottery-card .lc-meta{font-size:12px;color:#718096;margin-top:2px}
.lottery-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-bottom:24px}
.region-title{font-size:18px;font-weight:700;color:#92400E;margin:28px 0 12px;padding-left:8px;border-left:3px solid #F59E0B}
.pagination{display:flex;gap:6px;justify-content:center;margin:20px 0;flex-wrap:wrap}
.pagination button{padding:8px 14px;border:1px solid #E2E8F0;border-radius:6px;font-size:13px;cursor:pointer;background:#fff;color:#4A5568}
.pagination button:hover{border-color:#F59E0B;color:#B45309}.pagination button.active{background:#D97706;color:#fff;border-color:#D97706}
.pagination button:disabled{opacity:0.4;cursor:not-allowed}
.faq-item{border-bottom:1px solid #E2E8F0;padding:14px 0}
.faq-q{font-size:15px;font-weight:600;color:#2D3748;cursor:pointer;display:flex;justify-content:space-between;align-items:center}
.faq-q::after{content:"＋";font-size:16px;color:#A0AEC0}.faq-item.open .faq-q::after{content:"－"}
.faq-a{font-size:14px;color:#4A5568;line-height:1.7;max-height:0;overflow:hidden;transition:max-height 0.3s}.faq-item.open .faq-a{max-height:500px;padding-top:10px}
.ad-slot{margin:16px 0}
.sidebar{position:sticky;top:68px}.sidebar .card{padding:20px}.sidebar h3{font-size:15px;font-weight:600;margin-bottom:12px;color:#1A202C}
.sidebar a{display:block;padding:8px 0;border-bottom:1px solid #F1F5F9;font-size:13px}.sidebar a:last-child{border-bottom:none}
.lang-bar{display:flex;gap:6px;flex-wrap:wrap;margin:24px 0}
.lang-btn{font-size:12px;padding:4px 12px;border-radius:20px;background:#F7FAFC;border:1px solid #E2E8F0;color:#718096}
.lang-btn:hover{background:#FFFBEB;border-color:#FDE68A;text-decoration:none}
.lang-btn.active{background:#D97706;color:#fff;border-color:#D97706}
.footer{border-top:1px solid #E2E8F0;padding:24px 0;margin-top:40px}
.footer-inner{max-width:1100px;margin:0 auto;padding:0 20px;display:flex;flex-wrap:wrap;gap:16px;font-size:12px;color:#A0AEC0}.footer-inner a{color:#718096}
.disclaimer{font-size:12px;color:#A0AEC0;text-align:center;padding:16px 20px;line-height:1.6}
.highlight-match{background:#FDE68A;padding:1px 4px;border-radius:3px;font-weight:700}
.tool-input{margin:16px 0;padding:16px;background:#F7FAFC;border-radius:10px}
.tool-input label{display:block;font-size:13px;font-weight:600;color:#4A5568;margin-bottom:6px}
.year-table{width:100%;border-collapse:collapse;margin:16px 0;font-size:14px}
.year-table th{text-align:left;padding:10px 12px;background:#FFFBEB;border:1px solid #FDE68A;font-weight:600;color:#92400E;font-size:13px}
.year-table td{padding:10px 12px;border:1px solid #E2E8F0}.year-table tr:hover{background:#FEFCE8}
@media(max-width:768px){.layout{grid-template-columns:1fr}.sidebar{position:static}.card{padding:20px}.card h1{font-size:19px}.ball{width:36px;height:36px;font-size:14px}.info-grid{grid-template-columns:1fr}.summary-grid{grid-template-columns:1fr}.gen-grid{grid-template-columns:repeat(3,1fr)}.lottery-grid{grid-template-columns:repeat(2,1fr)}.search-box{flex-direction:column}}
'''


# ============================================================
# 5. BASE HTML WRAPPER
# ============================================================
def base_html(lang, title, desc, body, slug=None, ptype="intro", hreflang_langs=None, extra_head="", extra_js="", canonical_override=None):
    lcode = lang
    canonical = canonical_override or full_url(page_url(lang, slug, ptype))
    hl = hreflang_tags(slug, ptype, hreflang_langs) if hreflang_langs else ""
    
    subnav = ""
    if slug:
        pages = [("intro", lname(slug,lang)), ("results", t(lang,"results")), ("history", t(lang,"history")), ("statistics", t(lang,"statistics"))]
        _active = ' class="active"'
        links = "".join(f'<a href="{page_url(lang,slug,pt)}"{_active if pt==ptype else ""}>{lb}</a>' for pt,lb in pages)
        # Add number generator link to subnav
        links += f'<a href="{page_url(lang,slug,"number-generator") if slug else "#"}">{t(lang,"number_generator")}</a>'
        subnav = f'<div class="subnav"><div class="subnav-inner">{links}</div></div>'
    
    bc = f'<a href="/">SoftGlow</a> › <a href="{page_url(lang)}">{t(lang,"lottery")}</a>'
    if slug:
        if ptype == "intro":
            bc += f" › {lname(slug,lang)}"
        else:
            bc += f' › <a href="{page_url(lang,slug)}">{lname(slug,lang)}</a> › {t(lang, ptype) if ptype in I18N[lang] else ptype}'

    # sidebar: related lotteries
    cfg = LOTTERY_MAP.get(slug, {})
    related = [l for l in LOTTERIES if l.get("region") == cfg.get("region") and l["slug"] != slug][:4]
    if len(related) < 4:
        related += [l for l in LOTTERIES if l["slug"] != slug and l not in related][:4-len(related)]
    sb_links = "".join(f'<a href="{page_url(lang,rl["slug"])}">{rl["flag"]} {lname(rl["slug"],lang)}</a>' for rl in related)
    
    sidebar = f'''<aside class="sidebar">
  <div class="ad-slot" id="ad-side"></div>
  <div class="card"><h3>🎲 {t(lang,"number_generator")}</h3>
    <p style="font-size:13px;color:#718096;margin-bottom:12px">12 {t(lang,"select_method")}</p>
    <a href="{page_url(lang, None, 'number-generator')}" class="btn" style="width:100%;display:block;text-align:center">{t(lang,"generate")} →</a>
  </div>
  <div class="card"><h3>🌏 {t(lang,"all_lotteries")}</h3>{sb_links}</div>
</aside>''' if slug else ''

    return f'''<!DOCTYPE html>
<html lang="{lcode}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{canonical}">
{hl}
{extra_head}
<link rel="stylesheet" href="/js/cookie-consent.css">
<style>{CSS}</style>
</head>
<body>
<nav class="nav"><div class="nav-inner">
  <a href="/" class="nav-logo">Soft<span>Glow</span></a>
  <div class="nav-links">
    <a href="{page_url(lang)}">{t(lang,"lottery")}</a>
    <a href="/tools/{"" if lang=="zh-TW" else lang+"/"}">{t(lang,"tools")}</a>
    <a href="/">{t(lang,"home")}</a>
  </div>
</div></nav>
{subnav}
<div class="breadcrumb">{bc}</div>
<div class="container">
{body}
</div>
<div class="disclaimer">⚠️ {t(lang,"play_safe")}</div>
<footer class="footer"><div class="footer-inner">
  <a href="/about.html">{t(lang,"about")}</a>
  <a href="/contact.html">{t(lang,"contact")}</a>
  <a href="/privacy.html">{t(lang,"privacy")}</a>
  <a href="/terms.html">{t(lang,"terms")}</a>
  <span style="margin-left:auto">{t(lang,"copyright")}</span>
</div></footer>
<script>document.querySelectorAll('.faq-q').forEach(function(q){{q.addEventListener('click',function(){{this.parentElement.classList.toggle('open')}})}})</script>
{extra_js}
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1768270548115739" crossorigin="anonymous"></script>
<script src="/js/softglow-cookies.js" defer></script>
</body></html>'''


# ============================================================
# 6. PRIZE STRUCTURE DATA (per lottery)
# ============================================================
PRIZES = {
    "taiwan-bingo": [
        ("🥇 頭獎","6+特別號","1:22,085,448","累積獎金（最低800萬）"),
        ("🥈 貳獎","6個號碼","1:3,155,064","約150萬"),
        ("🥉 參獎","5+特別號","1:115,061","約1.5萬"),
        ("肆獎","5個號碼","1:16,437","約4,000"),
        ("伍獎","4+特別號","1:2,311","約1,000"),
        ("陸獎","3+特別號","1:156","約400"),
        ("柒獎","2+特別號","1:21","100"),
        ("普獎","特別號","1:8","100"),
    ],
    "powerball": [
        ("🥇 Jackpot","5+PB","1:292,201,338","Jackpot (min $20M)"),
        ("2nd","5","1:11,688,053","$1,000,000"),
        ("3rd","4+PB","1:913,129","$50,000"),
        ("4th","4","1:36,525","$100"),
        ("5th","3+PB","1:14,494","$100"),
        ("6th","3","1:579","$7"),
        ("7th","2+PB","1:701","$7"),
        ("8th","1+PB","1:91","$4"),
        ("9th","PB only","1:38","$4"),
    ],
    "mega-millions": [
        ("🥇 Jackpot","5+MB","1:302,575,350","Jackpot (min $20M)"),
        ("2nd","5","1:12,607,306","$1,000,000"),
        ("3rd","4+MB","1:931,001","$10,000"),
        ("4th","4","1:38,792","$500"),
        ("5th","3+MB","1:14,547","$200"),
        ("6th","3","1:606","$10"),
        ("7th","2+MB","1:693","$10"),
        ("8th","1+MB","1:89","$4"),
        ("9th","MB only","1:37","$2"),
    ],
    "euromillions": [
        ("🥇 Jackpot","5+2★","1:139,838,160","Jackpot (min €17M)"),
        ("2nd","5+1★","1:6,991,908","€200,000+"),
        ("3rd","5","1:3,107,515","€30,000+"),
        ("4th","4+2★","1:621,503","€3,000+"),
        ("5th","4+1★","1:31,075","€150+"),
        ("6th","4","1:13,811","€50+"),
        ("7th","3+2★","1:14,125","€50+"),
        ("8th","2+2★","1:985","€10+"),
        ("9th","3+1★","1:706","€10+"),
    ],
}

# ============================================================
# 7. CONTENT TEMPLATES (data-driven, 800+ chars per page)
# ============================================================
def content_intro(lang, slug, cfg):
    """Generate intro content paragraphs"""
    ln = lname(slug, lang)
    fmt = f"{cfg['pick']}/{cfg['pick_range']}"
    if cfg['bonus'] > 0:
        fmt += f"+{cfg['bonus']}/{cfg['bonus_range']}"
    
    if lang == "zh-TW":
        return f"""<p>{ln}是{cfg['country']}最受歡迎的彩票遊戲之一，採用 {fmt} 的選號制度。每注投注金額為 {cfg['bet']}，每週{cfg['draw_days']}開獎，開獎時間為{cfg['draw_time']}。玩家需從 1 到 {cfg['pick_range']} 中選出 {cfg['pick']} 個號碼{'，再從 1 到 ' + str(cfg['bonus_range']) + ' 中選出 ' + str(cfg['bonus']) + ' 個特別號' if cfg['bonus']>0 else ''}。</p>
<p>{ln}的頭獎機率為 {cfg['odds_jackpot']}，雖然機率不高，但採用累積型獎金機制，當期若無人中獎，獎金將自動滾入下一期。這個機制讓頭獎金額經常累積到令人驚嘆的數字，吸引了無數彩迷的關注與參與。整體中獎機率約為 {cfg['odds_any']}，包含最小獎項在內。</p>
<p>本頁提供{ln}的完整遊戲規則、獎金結構、中獎機率、開獎時間等資訊，以及免費的選號工具和統計分析功能。無論您是初次接觸還是資深彩迷，都能在這裡找到所需的資訊，做出更明智的選號決策。</p>"""
    else:
        return f"""<p>{ln} is one of the most popular lottery games in {cfg['country']}, using a {fmt} number format. Each ticket costs {cfg['bet']}, with draws held on {cfg['draw_days']} at {cfg['draw_time']}. Players select {cfg['pick']} numbers from 1 to {cfg['pick_range']}{'and ' + str(cfg['bonus']) + ' bonus number(s) from 1 to ' + str(cfg['bonus_range']) if cfg['bonus']>0 else ''}.</p>
<p>The jackpot odds are {cfg['odds_jackpot']}, but with a rollover mechanism, unclaimed jackpots accumulate into the next draw, often reaching staggering amounts. The overall odds of winning any prize are approximately {cfg['odds_any']}.</p>
<p>This page provides complete game rules, prize structure, winning odds, draw schedule, and free number generator tools. Whether you're a first-time player or a seasoned lottery enthusiast, you'll find everything you need to make informed number selections.</p>"""

def content_results(lang, slug, cfg):
    ln = lname(slug, lang)
    if lang == "zh-TW":
        return f"<p>{ln}每週{cfg['draw_days']}開獎，開獎時間為{cfg['draw_time']}。第一區從 1-{cfg['pick_range']} 選 {cfg['pick']} 個號碼{'，第二區從 1-' + str(cfg['bonus_range']) + ' 選 ' + str(cfg['bonus']) + ' 個號碼' if cfg['bonus']>0 else ''}。以下為最近幾期開獎結果，您也可以查看完整歷史紀錄或使用選號工具。</p>"
    return f"<p>{ln} draws are held on {cfg['draw_days']} at {cfg['draw_time']}. Players pick {cfg['pick']} numbers from 1-{cfg['pick_range']}{'plus ' + str(cfg['bonus']) + ' bonus from 1-' + str(cfg['bonus_range']) if cfg['bonus']>0 else ''}. Below are the latest results.</p>"

def content_history(lang, slug, cfg, total_draws):
    ln = lname(slug, lang)
    if lang == "zh-TW":
        return f"""<p>{ln}自發行以來，已累計超過 {total_draws:,} 期開獎紀錄。本頁收錄了完整的歷史開獎號碼，您可以透過日期搜尋功能查詢特定某一期的開獎結果，也可以使用號碼搜尋功能，輸入特定號碼查看它在哪些期數中出現過，用於分析號碼的出現頻率與間隔規律。</p>
<p>了解歷史開獎紀錄有助於掌握號碼的出現趨勢，雖然每次開獎都是獨立事件，但統計分析可以提供參考依據，幫助您制定更有策略的選號方式。建議搭配統計分析頁面一起使用，獲得更全面的數據支持。</p>"""
    return f"""<p>{ln} has accumulated over {total_draws:,} draws since its launch. This page contains the complete winning number history. Use the date search to find results for a specific draw, or use the number search to see when a particular number last appeared.</p>
<p>Understanding historical draw patterns can help inform your number selection strategy. While each draw is an independent event, statistical analysis provides useful reference points for more strategic picks.</p>"""

def content_statistics(lang, slug, cfg, total_draws):
    ln = lname(slug, lang)
    if lang == "zh-TW":
        return f"""<p>{ln}號碼統計分析，基於 {total_draws:,} 期歷史開獎資料計算。熱門號碼是出現次數最多的號碼，冷門號碼是最久未出現的號碼。每個號碼在 {cfg['pick_range']} 個號碼中的理論平均出現率約為 {cfg['pick']/cfg['pick_range']*100:.1f}%。</p>
<p>統計數據可以幫助您了解號碼的歷史出現趨勢，但請記住每次開獎都是獨立事件，過去的結果不代表未來的走向。建議將統計數據作為選號參考之一，搭配其他選號方式使用。</p>"""
    return f"""<p>{ln} number frequency analysis based on {total_draws:,} historical draws. Hot numbers appear most frequently, while cold numbers haven't been drawn recently. The theoretical average appearance rate for each number is approximately {cfg['pick']/cfg['pick_range']*100:.1f}%.</p>
<p>Statistics can help you understand historical number trends, but remember that each draw is an independent event. Use these insights as one of many tools in your number selection strategy.</p>"""


# ============================================================
# 8. PAGE GENERATORS
# ============================================================
def gen_intro(lang, slug, cfg, draws, stats):
    ln = lname(slug, lang)
    title = f"{ln} — {t(lang,'rules')}・{t(lang,'odds')}・{t(lang,'how_to')}"
    desc = content_intro(lang, slug, cfg)[:160].replace("<p>","").replace("</p>","")
    
    fmt_str = t(lang,"from_range",p=cfg["pick"],r=cfg["pick_range"])
    if cfg["bonus"] > 0:
        fmt_str += " " + t(lang,"plus_bonus",b=cfg["bonus"],r=cfg["bonus_range"])
    
    latest_html = ""
    for d in draws[:3]:
        latest_html += f'<div class="draw-card{"" if d!=draws[0] else " latest"}">'
        if d == draws[0]:
            latest_html += f'<span class="draw-label">{t(lang,"latest")}</span>'
        latest_html += f'<div class="draw-date">{d["date"]}</div><div class="draw-nums">{balls_html(d["numbers"], d.get("bonus"))}</div></div>'
    if not latest_html:
        latest_html = f'<p style="color:#A0AEC0;padding:20px 0">{t(lang,"no_data")}</p>'
    
    info = f'''<div class="info-grid">
      <div class="info-item"><div class="info-label">{t(lang,"format")}</div><div class="info-value">{cfg["pick"]}/{cfg["pick_range"]}{f"+{cfg['bonus']}/{cfg['bonus_range']}" if cfg["bonus"]>0 else ""}</div></div>
      <div class="info-item"><div class="info-label">{t(lang,"draw_days")}</div><div class="info-value">{cfg["draw_days"]}</div></div>
      <div class="info-item"><div class="info-label">{t(lang,"draw_time")}</div><div class="info-value">{cfg["draw_time"]}</div></div>
      <div class="info-item"><div class="info-label">{t(lang,"odds")}</div><div class="info-value">{cfg["odds_jackpot"]}</div></div>
    </div>'''
    
    prize_html = ""
    prizes = PRIZES.get(slug, [])
    if prizes:
        _jr = 'class="jr"'
        rows = "".join(f'<tr {_jr if i==0 else ""}><td>{p[0]}</td><td>{p[1]}</td><td>{p[2]}</td><td>{p[3]}</td></tr>' for i,p in enumerate(prizes))
        prize_html = f'<h2>💰 {t(lang,"prize")}</h2><table class="prize-table"><thead><tr><th>{"獎項" if lang.startswith("zh") else "Prize"}</th><th>{"中獎條件" if lang.startswith("zh") else "Match"}</th><th>{t(lang,"odds")}</th><th>{"獎金" if lang.startswith("zh") else "Prize"}</th></tr></thead><tbody>{rows}</tbody></table>'
    
    lang_btns = "".join(f'<a href="{page_url(la,slug)}" class="lang-btn{" active" if la==lang else ""}">{la}</a>' for la in cfg["langs"])
    
    body = f'''<div class="layout"><div class="main">
  <div class="card"><h1>{cfg.get("flag","")} {ln}</h1>{content_intro(lang,slug,cfg)}{info}</div>
  <div class="ad-slot" id="ad1"></div>
  <div class="card"><h2>{t(lang,"latest")}</h2>{latest_html}
    <div style="margin-top:16px;display:flex;gap:10px;flex-wrap:wrap">
      <a href="{page_url(lang,slug,'results')}" class="btn">{t(lang,"results")} →</a>
      <a href="{page_url(lang,None,'number-generator')}" class="btn" style="background:#92400E">{t(lang,"number_generator")} 🎲</a>
    </div>
  </div>
  <div class="ad-slot" id="ad2"></div>
  {"<div class='card'>" + prize_html + "</div>" if prize_html else ""}
  <div class="lang-bar">{lang_btns}</div>
</div>
<aside class="sidebar"><div class="ad-slot" id="ad-side"></div>
  <div class="card"><h3>🎲 {t(lang,"number_generator")}</h3>
    <a href="{page_url(lang,None,'number-generator')}" class="btn" style="width:100%;display:block;text-align:center">{t(lang,"generate")} →</a></div>
  <div class="card"><h3>🌏 {t(lang,"all_lotteries")}</h3>
    {"".join(f"<a href=\"{page_url(lang,l['slug'])}\">{l['flag']} {lname(l['slug'],lang)}</a>" for l in LOTTERIES if l["slug"]!=slug)[:5]}
  </div>
</aside></div>'''
    return base_html(lang, title, desc, body, slug, "intro", cfg["langs"])


def gen_results(lang, slug, cfg, draws, stats):
    ln = lname(slug, lang)
    title_map = {"zh-TW": f"{ln}開獎號碼 — 最新中獎號碼即時查詢", "en": f"{ln} Results Today — Latest Winning Numbers 2026"}
    title = title_map.get(lang, f"{ln} — {t(lang,'results')}")
    desc = content_results(lang, slug, cfg)[:160].replace("<p>","").replace("</p>","")
    
    draws_html = ""
    for i, d in enumerate(draws[:20]):
        cls = " latest" if i == 0 else ""
        label = f'<span class="draw-label">{t(lang,"latest")}</span>' if i == 0 else ""
        draws_html += f'<div class="draw-card{cls}">{label}<div class="draw-date">{d["date"]}</div><div class="draw-nums">{balls_html(d["numbers"],d.get("bonus"))}</div></div>'
    if not draws_html:
        draws_html = f'<p style="color:#A0AEC0;padding:20px 0">{t(lang,"no_data")}</p>'
    
    prize_html = ""
    prizes = PRIZES.get(slug, [])
    if prizes:
        _jr = 'class="jr"'
        rows = "".join(f'<tr {_jr if i==0 else ""}><td>{p[0]}</td><td>{p[1]}</td><td>{p[2]}</td><td>{p[3]}</td></tr>' for i,p in enumerate(prizes))
        prize_html = f'<div class="card"><h2>💰 {t(lang,"prize")}</h2><table class="prize-table"><thead><tr><th>{"獎項" if lang.startswith("zh") else "Prize"}</th><th>{"中獎條件" if lang.startswith("zh") else "Match"}</th><th>{t(lang,"odds")}</th><th>{"獎金" if lang.startswith("zh") else "Prize"}</th></tr></thead><tbody>{rows}</tbody></table></div>'
    
    # Hot/cold strip
    main_nums = stats.get("main_numbers", [])
    hot = sorted(main_nums, key=lambda x: x["count"], reverse=True)[:10]
    cold = sorted(main_nums, key=lambda x: x["last_seen"], reverse=True)[:10]
    trend_html = ""
    if hot:
        hot_strip = "".join(f'<span class="hot-num">{h["number"]}</span>' for h in hot)
        cold_strip = "".join(f'<span class="cold-num">{c["number"]}</span>' for c in cold)
        trend_html = f'''<div class="card"><h2>📊 {t(lang,"trend")}</h2>
          <h3 style="font-size:15px;font-weight:600;color:#B45309;margin:12px 0 8px">🔥 {t(lang,"hot")}</h3><div class="hot-strip">{hot_strip}</div>
          <h3 style="font-size:15px;font-weight:600;color:#2563EB;margin:16px 0 8px">❄️ {t(lang,"cold")}</h3><div class="hot-strip">{cold_strip}</div>
          <a href="{page_url(lang,slug,'statistics')}" style="font-size:13px">{t(lang,"more_stats")} →</a></div>'''
    
    lang_btns = "".join(f'<a href="{page_url(la,slug,"results")}" class="lang-btn{" active" if la==lang else ""}">{la}</a>' for la in cfg["langs"])
    
    body = f'''<div class="layout"><div class="main">
  <div class="card"><h1>{cfg.get("flag","")} {ln} — {t(lang,"latest")}</h1>{content_results(lang,slug,cfg)}{draws_html}
    <div style="margin-top:16px"><a href="{page_url(lang,slug,'history')}" class="btn">{t(lang,"view_history")} →</a></div>
  </div>
  <div class="ad-slot" id="ad1"></div>
  {prize_html}
  <div class="ad-slot" id="ad2"></div>
  {trend_html}
  <div class="lang-bar">{lang_btns}</div>
</div>
<aside class="sidebar"><div class="ad-slot" id="ad-side"></div>
  <div class="card"><h3>🎲 {t(lang,"number_generator")}</h3>
    <a href="{page_url(lang,None,'number-generator')}" class="btn" style="width:100%;display:block;text-align:center">{t(lang,"generate")} →</a></div>
  <div class="card"><h3>🌏 {t(lang,"all_lotteries")}</h3>
    {"".join(f"<a href=\"{page_url(lang,l['slug'],'results')}\">{l['flag']} {lname(l['slug'],lang)}</a>" for l in LOTTERIES if l['slug']!=slug)[:5]}
  </div>
</aside></div>'''
    return base_html(lang, title, desc, body, slug, "results", cfg["langs"])


def gen_history(lang, slug, cfg, draws, stats):
    ln = lname(slug, lang)
    total = len(draws)
    title_map = {"zh-TW": f"{ln}歷史開獎紀錄 — 完整開獎號碼查詢", "en": f"{ln} Past Results — Complete Winning Numbers History"}
    title = title_map.get(lang, f"{ln} — {t(lang,'history')}")
    desc = content_history(lang, slug, cfg, total)[:160].replace("<p>","").replace("</p>","")
    
    # Embed latest 100 draws as JSON
    embed = json.dumps([{"d":d["date"],"n":d["numbers"],"b":d.get("bonus",[])} for d in draws[:100]], ensure_ascii=False)
    
    lang_btns = "".join(f'<a href="{page_url(la,slug,"history")}" class="lang-btn{" active" if la==lang else ""}">{la}</a>' for la in cfg["langs"])
    
    body = f'''<div class="layout"><div class="main">
  <div class="card"><h1>{cfg.get("flag","")} {ln} — {t(lang,"history")}</h1>{content_history(lang,slug,cfg,total)}
    <div class="summary-grid">
      <div class="summary-item"><div class="num">{total:,}</div><div class="label">{t(lang,"total_draws")}</div></div>
      <div class="summary-item"><div class="num">{cfg["pick"]}/{cfg["pick_range"]}</div><div class="label">{t(lang,"format")}</div></div>
      <div class="summary-item"><div class="num">{cfg["draw_days"]}</div><div class="label">{t(lang,"draw_days")}</div></div>
    </div>
  </div>
  <div class="card"><h2>🔍 {t(lang,"search_date")}</h2>
    <div class="search-box"><input type="date" id="dateSearch"><button onclick="searchDate()">{t(lang,"search_date")}</button></div>
    <div class="search-result" id="dateResult"></div>
  </div>
  <div class="card"><h2>🔢 {t(lang,"search_num")}</h2>
    <div class="search-box"><input type="number" id="numSearch" min="1" max="{cfg["pick_range"]}" placeholder="1-{cfg["pick_range"]}"><button onclick="searchNum()">{t(lang,"search_num")}</button></div>
    <div class="search-result" id="numResult"></div>
  </div>
  <div class="ad-slot" id="ad1"></div>
  <div class="card"><h2>📋 {t(lang,"history")}</h2><div id="hList"></div><div class="pagination" id="hPager"></div></div>
  <div class="ad-slot" id="ad2"></div>
  <div class="lang-bar">{lang_btns}</div>
</div>
<aside class="sidebar"><div class="ad-slot" id="ad-side"></div>
  <div class="card"><h3>🎲 {t(lang,"number_generator")}</h3>
    <a href="{page_url(lang,None,'number-generator')}" class="btn" style="width:100%;display:block;text-align:center">{t(lang,"generate")} →</a></div>
</aside></div>'''
    
    js = f'''<script>
var D={embed};var pp=20,cp=0,tp=Math.ceil(D.length/pp);
function bh(n,b){{var h="";for(var i=0;i<n.length;i++)h+='<span class="ball ball-main">'+n[i]+"</span>";if(b&&b.length){{h+='<span class="draw-plus">+</span>';for(var j=0;j<b.length;j++)h+='<span class="ball ball-bonus">'+b[j]+"</span>"}}return h}}
function rp(p){{cp=p;var s=p*pp,e=Math.min(s+pp,D.length),h="";for(var i=s;i<e;i++)h+='<div class="draw-row"><div class="draw-date">'+D[i].d+'</div><div class="draw-nums">'+bh(D[i].n,D[i].b)+"</div></div>";document.getElementById("hList").innerHTML=h;var pg="";if(tp>1){{pg+='<button '+(p===0?"disabled":"")+" onclick=\"rp("+(p-1)+')">{t(lang,"prev")}</button>';var st=Math.max(0,p-3),en=Math.min(tp,st+7);for(var x=st;x<en;x++)pg+='<button class="'+(x===p?"active":"")+"\" onclick=\"rp("+x+')">'+(x+1)+"</button>";pg+='<button '+(p>=tp-1?"disabled":"")+" onclick=\"rp("+(p+1)+')">{t(lang,"next")}</button>'}}document.getElementById("hPager").innerHTML=pg}}
function searchDate(){{var v=document.getElementById("dateSearch").value;var f=D.filter(function(d){{return d.d===v}});var el=document.getElementById("dateResult");el.innerHTML=f.length?'<strong>'+f[0].d+'</strong><div style="margin-top:8px">'+bh(f[0].n,f[0].b)+'</div>':'<span style="color:#718096">{t(lang,"no_data")}</span>';el.classList.add("show")}}
function searchNum(){{var n=parseInt(document.getElementById("numSearch").value);if(isNaN(n)||n<1||n>{cfg["pick_range"]})return;var f=[];for(var i=0;i<D.length&&f.length<10;i++)if(D[i].n.indexOf(n)!==-1)f.push(D[i]);var el=document.getElementById("numResult");if(f.length){{var h="<strong>"+n+"</strong><br>";for(var j=0;j<f.length;j++)h+='<div class="draw-row"><div class="draw-date">'+f[j].d+'</div><div class="draw-nums">'+bh(f[j].n,f[j].b)+"</div></div>";el.innerHTML=h}}else el.innerHTML='{t(lang,"no_data")}';el.classList.add("show")}}
rp(0);
</script>'''
    return base_html(lang, title, desc, body, slug, "history", cfg["langs"], extra_js=js)


def gen_statistics(lang, slug, cfg, draws, stats):
    ln = lname(slug, lang)
    total = stats.get("total_draws", len(draws))
    title_map = {"zh-TW": f"{ln}號碼統計分析 — 熱門冷門號碼排行", "en": f"{ln} Statistics — Hot & Cold Number Analysis"}
    title = title_map.get(lang, f"{ln} — {t(lang,'statistics')}")
    desc = content_statistics(lang, slug, cfg, total)[:160].replace("<p>","").replace("</p>","")
    
    main_nums = stats.get("main_numbers", [])
    hot = sorted(main_nums, key=lambda x: x["count"], reverse=True)[:15]
    cold = sorted(main_nums, key=lambda x: x["last_seen"], reverse=True)[:15]
    max_count = hot[0]["count"] if hot else 1
    max_ls = cold[0]["last_seen"] if cold else 1
    
    hot_html = ""
    for h in hot:
        pct = h["count"] / max_count * 100
        hot_html += f'<div class="stat-bar"><span class="stat-num hot">{h["number"]}</span><div style="flex:1;background:#F7FAFC;border-radius:4px;overflow:hidden"><div class="stat-fill hot" style="width:{pct:.0f}%"></div></div><span class="stat-count">{h["count"]}x ({h["frequency"]}%)</span></div>'
    
    cold_html = ""
    for c in cold:
        pct = c["last_seen"] / max_ls * 100 if max_ls > 0 else 0
        cold_html += f'<div class="stat-bar"><span class="stat-num cold">{c["number"]}</span><div style="flex:1;background:#F7FAFC;border-radius:4px;overflow:hidden"><div class="stat-fill cold" style="width:{pct:.0f}%"></div></div><span class="stat-count">{c["last_seen"]} {t(lang,"draws_ago")}</span></div>'
    
    lang_btns = "".join(f'<a href="{page_url(la,slug,"statistics")}" class="lang-btn{" active" if la==lang else ""}">{la}</a>' for la in cfg["langs"])
    
    body = f'''<div class="layout"><div class="main">
  <div class="card"><h1>{cfg.get("flag","")} {ln} — {t(lang,"statistics")}</h1>{content_statistics(lang,slug,cfg,total)}</div>
  <div class="card"><h2>🔥 {t(lang,"hot")} (Top 15)</h2>{hot_html if hot_html else t(lang,"no_data")}</div>
  <div class="ad-slot" id="ad1"></div>
  <div class="card"><h2>❄️ {t(lang,"cold")} (Top 15)</h2>{cold_html if cold_html else t(lang,"no_data")}</div>
  <div class="ad-slot" id="ad2"></div>
  <div class="lang-bar">{lang_btns}</div>
</div>
<aside class="sidebar"><div class="ad-slot" id="ad-side"></div>
  <div class="card"><h3>🎲 {t(lang,"number_generator")}</h3>
    <a href="{page_url(lang,None,'number-generator')}" class="btn" style="width:100%;display:block;text-align:center">{t(lang,"generate")} →</a></div>
</aside></div>'''
    return base_html(lang, title, desc, body, slug, "statistics", cfg["langs"])


"""
12 tool page content templates - 800+ chars per language
Returns dict: {tool_key: {lang: {"intro": ..., "steps": ..., "faq": [...]}}}
"""

TOOL_CONTENT = {
    "random": {
        "zh-TW": {
            "intro": "隨機選號是最經典也最公平的選號方式。電腦使用加密級別的亂數產生器，從號碼池中完全隨機地抽出號碼，每個號碼被選中的機率完全相同。這種方式模擬了彩券行的「電腦選號」功能，讓運氣成為唯一的決定因素。統計上，歷史上約有 70% 的頭獎得主是使用電腦隨機選號中獎的，這說明了隨機選號的有效性。不需要花時間分析號碼，不需要糾結該選哪個數字，把一切交給命運，享受開獎那一刻的期待感。",
            "steps": "選擇您要投注的彩種，點擊「產生號碼」按鈕即可。每次點擊都會產生一組全新的隨機號碼，您可以多產生幾組比較，選出最順眼的一組。",
            "faq": [
                ("隨機選號真的是隨機的嗎？","是的。本工具使用瀏覽器內建的加密級亂數產生器（Crypto API），確保每個號碼被選中的機率完全相等，沒有任何偏差。"),
                ("隨機選號的中獎機率比自己選高嗎？","數學上完全相同。每一組號碼的中獎機率都是固定的，不管是電腦選還是自己選。但統計顯示約 70% 頭獎得主使用電腦選號。"),
                ("可以同時產生多組號碼嗎？","可以。每次點擊都會產生一組新號碼，您可以連續點擊多次，選出最喜歡的組合。"),
                ("產生的號碼會重複嗎？","同一組內不會有重複號碼。但不同次產生的組合之間可能有部分相同的號碼，這是正常的隨機現象。"),
                ("這個工具是免費的嗎？","完全免費，無需註冊，無使用次數限制。所有計算都在您的瀏覽器中完成，不會上傳任何資料。"),
            ],
        },
        "en": {
            "intro": "Random Pick is the most classic and fair number selection method. The computer uses a cryptographic-grade random number generator to select numbers from the pool with perfectly equal probability. This simulates the 'Quick Pick' feature at lottery retailers. Statistically, about 70% of jackpot winners used computer-generated random numbers. No analysis needed, no overthinking — just let fate decide and enjoy the anticipation of the draw.",
            "steps": "Select your lottery game from the dropdown, then click 'Generate'. Each click produces a completely new set of random numbers. Generate multiple sets and pick your favorite.",
            "faq": [
                ("Is this truly random?","Yes. This tool uses the browser's built-in cryptographic random number generator (Crypto API), ensuring each number has an exactly equal chance of being selected."),
                ("Are random picks more likely to win?","Mathematically, every combination has the same odds. However, statistics show about 70% of jackpot winners used Quick Pick/random selection."),
                ("Can I generate multiple sets?","Yes. Click the generate button multiple times to create several sets and choose your favorite combination."),
                ("Will numbers repeat within a set?","No. Each set contains unique numbers. However, different sets may share some numbers, which is a normal random occurrence."),
                ("Is this tool free?","Completely free, no registration required, no usage limits. All calculations run in your browser — no data is uploaded."),
            ],
        },
    },
    "hot_pick": {
        "zh-TW": {
            "intro": "熱門號碼選號根據歷史開獎數據，從出現頻率最高的號碼中選取。這些號碼在過去的開獎中比其他號碼出現得更頻繁，被稱為「熱門號碼」或「強勢號碼」。支持者認為熱門號碼反映了開獎機器或球的物理特性，可能存在微小的偏差，導致某些號碼更容易被抽中。雖然每次開獎理論上是獨立事件，但從大數據的角度來看，熱門號碼確實在統計上有更高的歷史出現率。本工具會從最近數百期的統計數據中，優先選取出現次數最多的號碼組成您的選號組合。",
            "steps": "選擇彩種後，系統會自動從該彩種的歷史熱門號碼中隨機組合。每次產生的組合都包含多個熱門號碼，但不完全相同，保持一定的隨機性。",
            "faq": [
                ("熱門號碼是怎麼計算的？","根據最近數百期的開獎紀錄，統計每個號碼出現的次數，出現次數最多的前 20 個號碼即為熱門號碼。"),
                ("熱門號碼真的比較容易中獎嗎？","理論上每個號碼的機率相同，但統計上某些號碼確實出現頻率較高。是否繼續保持熱門則無法預測。"),
                ("熱門號碼多久更新一次？","每次有新的開獎結果後，統計數據就會更新。本工具使用的是最新的歷史數據。"),
                ("可以混合熱門和冷門號碼嗎？","可以。您可以分別使用熱門和冷門選號工具各產生一組，再從中挑選組合。"),
                ("為什麼每次產生的號碼不一樣？","雖然都從熱門號碼池中選取，但每次會隨機組合不同的熱門號碼，避免所有人都選相同的組合。"),
            ],
        },
        "en": {
            "intro": "Hot Numbers Pick selects from the most frequently drawn numbers based on historical data. These numbers have appeared more often than average in past draws. Supporters believe hot numbers reflect subtle physical characteristics of the drawing machine. While each draw is theoretically independent, hot numbers do show statistically higher historical appearance rates. This tool prioritizes the most frequently drawn numbers from hundreds of recent draws.",
            "steps": "Select your lottery, and the system will automatically combine numbers from the historical hot numbers pool. Each generation includes multiple hot numbers with some randomization.",
            "faq": [
                ("How are hot numbers calculated?","Based on hundreds of recent draws, counting each number's appearances. The top 20 most frequent numbers are classified as 'hot'."),
                ("Do hot numbers really win more?","Theoretically each number has equal odds, but statistically some numbers do appear more frequently. Whether this continues is unpredictable."),
                ("How often is the data updated?","After each new draw result, the statistics are recalculated with the latest data."),
                ("Can I mix hot and cold numbers?","Yes. Generate sets from both tools and combine your favorites from each."),
                ("Why are the numbers different each time?","While all selected from the hot number pool, each generation randomly combines different hot numbers to avoid everyone picking identical sets."),
            ],
        },
    },
    "cold_pick": {
        "zh-TW": {
            "intro": "冷門號碼選號從最久未出現的號碼中選取。這些號碼已經連續多期沒有被開出，被稱為「冷門號碼」或「遺漏號碼」。支持者相信「均值回歸」理論——一個號碼被冷落越久，它在未來開出的機率就越高。這種策略在統計學上稱為「賭徒謬誤」的反面運用。雖然數學上每次開獎都是獨立事件，但許多資深彩迷仍偏好追蹤冷門號碼，認為長期未出現的號碼遲早會「回歸」。本工具會從遺漏期數最長的號碼中為您組合選號。",
            "steps": "選擇彩種後，系統會從遺漏期數最長的號碼中選取。遺漏期數表示該號碼已經連續幾期沒有出現。",
            "faq": [
                ("冷門號碼是怎麼定義的？","以「遺漏期數」衡量，即該號碼已連續多少期未被開出。遺漏期數越大，該號碼越「冷」。"),
                ("冷門號碼會不會一直冷下去？","有可能。雖然均值回歸理論認為冷門號碼最終會回升，但短期內沒有保證。請理性看待。"),
                ("冷門號碼和熱門號碼哪個好？","沒有定論。兩種策略各有支持者。建議混合使用，或根據個人偏好選擇。"),
                ("遺漏期數最長的號碼是哪個？","因彩種和時間而異。請查看各彩種的統計分析頁面獲取最新數據。"),
                ("冷門選號適合哪種彩票？","適用於所有彩票。號碼池越大的彩票（如 Powerball 1-69），冷門號碼的遺漏期通常越長。"),
            ],
        },
        "en": {
            "intro": "Cold Numbers Pick selects from the most overdue numbers — those that haven't appeared for the longest time. Supporters believe in 'regression to the mean': the longer a number stays cold, the more likely it is to appear soon. While mathematically each draw is independent, many experienced players track cold numbers, believing overdue numbers will eventually 'come back'. This tool picks from numbers with the highest gap since their last appearance.",
            "steps": "Select your lottery, and the system will pick from numbers with the longest absence. The gap number shows how many consecutive draws since that number last appeared.",
            "faq": [
                ("How are cold numbers defined?","By 'gap count' — how many consecutive draws since the number was last drawn. Higher gap = colder number."),
                ("Will cold numbers eventually appear?","There's no guarantee. While regression to the mean suggests they should, short-term outcomes are unpredictable."),
                ("Hot or cold — which is better?","Neither is proven superior. Many players mix both strategies. Choose based on personal preference."),
                ("Which number has the longest gap?","This varies by lottery and time. Check each lottery's statistics page for current data."),
                ("Which lotteries benefit most from cold picks?","All lotteries can use this strategy. Larger number pools (like Powerball 1-69) tend to have longer cold streaks."),
            ],
        },
    },
    "birthday": {
        "zh-TW": {
            "intro": "生日選號是全世界最受歡迎的選號方式之一。將您或親友的生日日期轉換成彩票號碼，讓每一張彩券都帶有特別的意義。生日的年、月、日數字經過特殊轉換算法，映射到彩票的號碼範圍內。例如 1990 年 3 月 15 日，可以拆解出 1、9、9、0、3、15 等數字，再進行組合變化。許多頭獎得主透露，他們的中獎號碼與家人的生日有關，這讓生日選號成為最受歡迎的選號策略之一。需要注意的是，由於月份最大為 12、日期最大為 31，生日選號的號碼通常集中在 1-31 之間，對於號碼範圍較大的彩票（如 1-69），建議搭配其他方式補充大號碼。",
            "steps": "選擇彩種，輸入您的出生日期（或重要的紀念日），點擊「產生號碼」。系統會將日期數字轉換成對應的彩票號碼。",
            "faq": [
                ("生日選號的號碼會偏小嗎？","是的。由於月份（1-12）和日期（1-31）的限制，生日號碼通常在 1-31 之間。對於大範圍彩票建議搭配隨機號碼。"),
                ("可以用別人的生日嗎？","當然可以。很多人使用家人、伴侶或孩子的生日。任何對您有意義的日期都適用。"),
                ("同一個生日每次產生的號碼一樣嗎？","不完全一樣。系統會以生日為基礎，但每次加入隨機變化，產生不同的組合。"),
                ("有人用生日中過大獎嗎？","有。許多頭獎得主表示號碼與家人生日相關。但這不代表生日號碼的中獎機率更高。"),
                ("農曆生日可以用嗎？","建議轉換成國曆日期再使用。系統使用西曆日期格式進行計算。"),
            ],
        },
        "en": {
            "intro": "Birthday Pick is one of the most popular number selection methods worldwide. Convert meaningful dates into lottery numbers, making every ticket personal. Birth dates are transformed through special algorithms to map onto the lottery's number range. Many jackpot winners have revealed their winning numbers were related to family birthdays. Note that birthday numbers tend to cluster between 1-31 due to month/day limits. For larger number pools (like 1-69), consider supplementing with other methods.",
            "steps": "Select your lottery, enter your birth date (or any meaningful date), and click Generate. The system converts date digits into lottery numbers.",
            "faq": [
                ("Will birthday numbers be low?","Yes, typically 1-31 due to month/day limits. For larger pools, consider mixing with random numbers."),
                ("Can I use someone else's birthday?","Absolutely. Many people use family members', partners', or children's birthdays."),
                ("Same birthday, same numbers?","Not exactly. The system uses your birthday as a seed but adds randomization each time."),
                ("Has anyone won with birthday numbers?","Yes. Many winners report birthday-related numbers, though this doesn't increase actual odds."),
                ("Can I use lunar calendar dates?","Convert to the Gregorian calendar first. The system uses standard date format."),
            ],
        },
    },
    "zodiac": {
        "zh-TW": {
            "intro": "星座選號將西洋占星學與彩票選號結合，根據十二星座的幸運數字特性來產生號碼。每個星座都有其對應的幸運數字、幸運顏色和守護星，這些元素經過特殊算法轉換成彩票號碼。例如白羊座的幸運數字為 9 和 18，守護星火星對應的數字為 7，這些數字會被優先納入選號組合。星座選號融合了趣味性和個人化，讓選號過程不再只是冰冷的數字遊戲。",
            "steps": "選擇彩種，從下拉選單中選擇您的星座，點擊「產生號碼」。系統會根據該星座的特性產生對應的號碼組合。",
            "faq": [
                ("每個星座的幸運數字是什麼？","每個星座有 2-3 個核心幸運數字，加上守護星對應的數字。系統會綜合這些數字來產生選號。"),
                ("星座選號有科學根據嗎？","星座選號屬於娛樂性質，沒有科學證據顯示星座與中獎有關。請當作趣味選號方式。"),
                ("上升星座和太陽星座用哪個？","建議使用太陽星座（出生月份對應的星座），這是最常用的分類方式。"),
                ("不同彩種同星座的號碼一樣嗎？","不一樣。系統會根據不同彩種的號碼範圍調整算法，確保號碼在有效範圍內。"),
                ("可以用朋友的星座嗎？","當然可以。您可以嘗試不同星座，看哪個組合最順眼。"),
            ],
        },
        "en": {
            "intro": "Zodiac Pick combines Western astrology with lottery number selection, generating numbers based on each sign's lucky numbers, colors, and ruling planets. For example, Aries' lucky numbers include 9 and 18, with Mars (ruling planet) corresponding to 7. These elements are algorithmically transformed into lottery numbers, making the selection process fun and personal.",
            "steps": "Select your lottery, choose your zodiac sign from the dropdown, and click Generate. The system creates numbers based on your sign's characteristics.",
            "faq": [
                ("What are each sign's lucky numbers?","Each sign has 2-3 core lucky numbers plus ruling planet numbers. The system combines these for your picks."),
                ("Is zodiac picking scientifically valid?","Zodiac picking is for entertainment. There's no scientific evidence linking zodiac signs to lottery outcomes."),
                ("Rising sign or sun sign?","Use your sun sign (based on birth month) — it's the most commonly used classification."),
                ("Same sign, different lottery — same numbers?","No. The algorithm adjusts for each lottery's number range to ensure valid numbers."),
                ("Can I try different signs?","Absolutely. Experiment with different signs and pick the combination you like best."),
            ],
        },
    },
    "chinese_zodiac": {
        "zh-TW": {
            "intro": "生肖選號結合中華傳統文化的十二生肖與彩票選號。每個生肖都有獨特的五行屬性和幸運數字：鼠（水、4/9）、牛（土、1/4）、虎（木、3/9）、兔（木、3/8）、龍（土、1/6）、蛇（火、2/8）、馬（火、2/7）、羊（土、1/6）、猴（金、4/9）、雞（金、4/5）、狗（土、3/6）、豬（水、2/7）。系統根據您的生肖屬性，結合五行相生相剋的原理，為您量身打造一組獨特的號碼組合。這種方式特別受到華人彩迷的喜愛。",
            "steps": "選擇彩種，從十二生肖中選擇您的生肖（依出生年份），點擊「產生號碼」。系統會根據生肖的五行屬性產生對應號碼。",
            "faq": [
                ("怎麼知道自己的生肖？","依出生年份的農曆年計算。例如 1990 年（馬）、1991 年（羊）。注意農曆年初在國曆一月底至二月間。"),
                ("生肖選號跟五行有關嗎？","是的。每個生肖對應一種五行（金木水火土），五行的相生關係會影響號碼的選取。"),
                ("農曆年初出生怎麼算？","如果出生在國曆一月或二月初，需要確認農曆年份來決定正確的生肖。"),
                ("夫妻可以用各自的生肖混合嗎？","這是個好主意。分別產生號碼後，從兩組中各挑選部分組合。"),
                ("生肖選號適合哪種彩票？","適用於所有彩票，但特別受華人地區彩票（威力彩、大樂透、今彩539）玩家喜愛。"),
            ],
        },
        "en": {
            "intro": "Chinese Zodiac Pick combines 12 traditional animal signs with lottery number selection. Each zodiac has unique Five Elements attributes and lucky numbers: Rat (Water, 4/9), Ox (Earth, 1/4), Tiger (Wood, 3/9), Rabbit (Wood, 3/8), Dragon (Earth, 1/6), Snake (Fire, 2/8), Horse (Fire, 2/7), Goat (Earth, 1/6), Monkey (Metal, 4/9), Rooster (Metal, 4/5), Dog (Earth, 3/6), Pig (Water, 2/7). The system uses Five Elements harmony principles to create your unique number combination.",
            "steps": "Select your lottery, choose your Chinese zodiac animal (based on birth year), and click Generate.",
            "faq": [
                ("How do I know my Chinese zodiac?","Based on your lunar birth year. For example: 1990 (Horse), 1996 (Rat), 2000 (Dragon)."),
                ("Is this related to Five Elements?","Yes. Each zodiac corresponds to an element (Metal, Wood, Water, Fire, Earth) that influences number selection."),
                ("Born in January/February?","If born before Lunar New Year (usually late Jan/early Feb), you may belong to the previous year's zodiac."),
                ("Can couples combine zodiacs?","Great idea. Generate from each zodiac and combine favorites from both sets."),
                ("Best for which lotteries?","Works for all lotteries, but especially popular with Asian lottery players."),
            ],
        },
    },
    "ai_pick": {
        "zh-TW": {
            "intro": "AI 分析推薦結合了多維度的數據分析，綜合考量熱門號碼趨勢、冷門號碼回歸機率、號碼間距分布、奇偶比例和大小比例等因素，使用加權隨機算法產生最佳化的號碼組合。與純隨機選號不同，AI 選號會分析歷史數據中的號碼分布模式，嘗試產生更「平衡」的號碼組合。例如，如果歷史上中獎號碼的奇偶比多為 3:3 或 4:2，AI 會傾向產生類似比例的組合。請注意，這只是統計優化，不代表中獎機率更高。",
            "steps": "選擇彩種，點擊「產生號碼」。AI 會自動分析該彩種的歷史數據，綜合多個因素產生一組優化的號碼。",
            "faq": [
                ("AI 分析真的有用嗎？","AI 分析基於歷史統計的模式優化，但每次開獎是獨立事件，沒有任何方法能保證中獎。請作為參考。"),
                ("AI 用了哪些數據？","包括號碼出現頻率、遺漏期數、奇偶分布、大小分布、連號模式等多維度歷史數據。"),
                ("AI 選號和隨機選號有什麼不同？","隨機選號每個號碼機率相等；AI 選號會根據歷史模式給予不同權重，產生更「平衡」的組合。"),
                ("為什麼叫 AI？","使用加權隨機算法分析歷史數據模式，類似簡易的機器學習概念。並非使用 ChatGPT 等大型 AI 模型。"),
                ("AI 推薦的號碼一定中嗎？","絕對不是。任何選號方式的中獎機率都是相同的。AI 只是幫助產生統計上更「均衡」的組合。"),
            ],
        },
        "en": {
            "intro": "AI Analysis Pick uses multi-dimensional data analysis, combining hot number trends, cold number regression probability, number spacing distribution, odd/even ratios, and high/low ratios through weighted random algorithms. Unlike pure random picks, AI attempts to generate more 'balanced' combinations based on historical winning patterns. Note: this is statistical optimization, not a guarantee of better odds.",
            "steps": "Select your lottery and click Generate. The AI analyzes historical data across multiple factors to produce an optimized number set.",
            "faq": [
                ("Does AI analysis really work?","AI is based on historical pattern optimization, but each draw is independent. No method can guarantee winning."),
                ("What data does the AI use?","Number frequency, gap counts, odd/even distribution, high/low distribution, consecutive number patterns, and more."),
                ("How is this different from random?","Random gives equal probability to all numbers; AI applies weights based on historical patterns for more 'balanced' combinations."),
                ("Why is it called AI?","It uses weighted random algorithms to analyze historical patterns, similar to basic machine learning concepts."),
                ("Will AI picks definitely win?","Absolutely not. All selection methods have identical winning odds. AI just helps generate statistically 'balanced' sets."),
            ],
        },
    },
    "lucky_number": {
        "zh-TW": {
            "intro": "幸運數字選號源自數字命理學（Numerology），將您的名字轉換成對應的幸運號碼。系統採用畢達哥拉斯數字轉換法，將每個字母對應到 1-9 的數字，再經過加總、化約和擴展運算，產生適合彩票範圍的號碼組合。在命理學中，每個人的名字蘊含著獨特的數字能量，這些能量數字被認為是您的幸運密碼。輸入中文名字時，系統會使用 Unicode 編碼值進行轉換。不同的名字會產生完全不同的號碼組合，讓每個人都有專屬的幸運號碼。",
            "steps": "選擇彩種，輸入您的名字（中文或英文皆可），點擊「產生號碼」。系統會將名字轉換成專屬的幸運號碼。",
            "faq": [
                ("中文名字和英文名字結果一樣嗎？","不一樣。中文使用 Unicode 編碼轉換，英文使用字母對應數字表，產生的結果不同。"),
                ("用全名還是暱稱？","建議使用您最常用的名字，無論是全名、暱稱或英文名都可以。"),
                ("同名同姓的人號碼一樣嗎？","完全同名的人基礎號碼相同，但系統會加入隨機變化，每次產生略有不同的組合。"),
                ("可以用公司名或寵物名嗎？","可以。任何文字都能轉換，您可以嘗試各種有意義的名字。"),
                ("命理學選號有根據嗎？","數字命理學是一種古老的信仰系統，沒有科學證據支持。請作為趣味選號方式。"),
            ],
        },
        "en": {
            "intro": "Lucky Number Pick is based on Numerology, converting your name into lucky lottery numbers. Using the Pythagorean system, each letter maps to digits 1-9, then through summation and expansion, generates numbers within the lottery range. In numerology, every name contains unique numerical energy considered your 'lucky code'. Different names produce completely different number combinations.",
            "steps": "Select your lottery, enter your name (any language), and click Generate. The system converts your name into personalized lucky numbers.",
            "faq": [
                ("Different languages, different results?","Yes. Different character encodings produce different numbers."),
                ("Full name or nickname?","Use whichever name you use most often."),
                ("Same name = same numbers?","Base numbers are similar, but the system adds randomization each time."),
                ("Can I use a company or pet name?","Yes. Any text can be converted — try names meaningful to you."),
                ("Is numerology scientifically proven?","Numerology is an ancient belief system without scientific backing. Use it as a fun selection method."),
            ],
        },
    },
    "bazi": {
        "zh-TW": {
            "intro": "八字選號融合中國傳統命理學「四柱八字」的智慧。根據您的出生年、月、日、時，計算出天干地支組合，再依據五行（金木水火土）的屬性與相互關係，推算出與您命格最契合的幸運號碼。八字命理認為，每個人出生的時間決定了其先天的五行能量分布，選擇與自身五行相合的號碼，能夠提升運勢。系統會分析您的八字五行強弱，選取與您命格互補的數字。例如，五行缺水者會偏向選取 1、6 等水屬性數字。",
            "steps": "選擇彩種，輸入您的出生日期和時辰，點擊「產生號碼」。系統會計算您的八字五行，產生與命格相合的號碼。",
            "faq": [
                ("不知道出生時辰怎麼辦？","可以只填日期，系統會以日柱為主進行分析。知道時辰能提供更精確的結果。"),
                ("八字選號有科學根據嗎？","八字命理是中國傳統文化的一部分，屬於信仰範疇，沒有現代科學證據。請作為文化體驗。"),
                ("五行數字對應是什麼？","金（4、9）、木（3、8）、水（1、6）、火（2、7）、土（5、0）。"),
                ("農曆還是國曆？","系統使用國曆（西曆）日期。如果您知道農曆生日，請先轉換為國曆。"),
                ("同一天出生的人號碼一樣嗎？","同日同時出生者基礎八字相同，但系統會加入隨機變化產生不同組合。"),
            ],
        },
        "en": {
            "intro": "BaZi Pick applies Chinese Four Pillars of Destiny — using your birth year, month, day, and hour to calculate Heavenly Stems and Earthly Branches, then deriving lucky numbers based on Five Elements (Metal, Wood, Water, Fire, Earth) balance. BaZi believes your birth time determines innate elemental energy. The system analyzes your Five Elements strengths and weaknesses, selecting complementary numbers. For example, someone lacking Water element would lean toward 1 and 6.",
            "steps": "Select your lottery, enter your birth date and time, and click Generate. The system calculates your BaZi elements and generates compatible numbers.",
            "faq": [
                ("What if I don't know my birth time?","Just enter the date. The system will use the Day Pillar for analysis. Knowing the time provides more precise results."),
                ("Is BaZi scientifically proven?","BaZi is part of Chinese traditional culture and belief systems, without modern scientific evidence."),
                ("What are the Five Elements numbers?","Metal (4,9), Wood (3,8), Water (1,6), Fire (2,7), Earth (5,0)."),
                ("Lunar or solar calendar?","The system uses the Gregorian (solar) calendar."),
                ("Same birthday = same numbers?","Same date/time share base BaZi, but randomization produces different combinations each time."),
            ],
        },
    },
    "life_event": {
        "zh-TW": {
            "intro": "大事件選號將人生中的重要時刻轉化為彩票號碼。每個重大人生事件都帶有獨特的能量和數字頻率：結婚代表配對與和諧（偏好偶數和成對數字）、生小孩象徵新生與成長（偏好遞增序列）、買房代表穩定與根基（偏好中間數字）、升遷代表向上突破（偏好大號碼）等。選擇一個即將發生或已經發生的重要事件，系統會根據該事件的象徵意義，為您產生一組帶有特殊意涵的號碼。讓人生的重要時刻為您帶來額外的幸運。",
            "steps": "選擇彩種，從十個人生大事中選擇一個（結婚、生小孩、買房、升遷、畢業、退休、旅行、搬家、開業、紀念日），點擊產生號碼。",
            "faq": [
                ("為什麼不同事件產生的號碼不同？","每個事件有獨特的數字特性。例如結婚偏好成對數字，畢業偏好奇數。系統根據這些特性調整選號。"),
                ("可以選還沒發生的事件嗎？","可以。選擇您期待發生的事件，讓期待成為選號的動力。"),
                ("同一個事件每次號碼一樣嗎？","不一樣。事件只決定選號的偏好方向，每次仍有隨機變化。"),
                ("十個事件哪個最好？","沒有哪個比較好。選擇對您目前最有意義的事件即可。"),
                ("可以組合多個事件嗎？","可以。分別產生號碼後，從各組中挑選組合。"),
            ],
        },
        "en": {
            "intro": "Life Event Pick transforms significant life moments into lottery numbers. Each major event carries unique energy: Marriage favors paired/even numbers, New Baby symbolizes growth with ascending sequences, Buying a House represents stability with mid-range numbers, and Promotion represents breakthroughs with higher numbers. Select an event and let your life's milestones bring extra luck.",
            "steps": "Select your lottery, choose from 10 life events (Wedding, New Baby, Buy House, Promotion, Graduation, Retirement, Travel, Moving, New Business, Anniversary), and click Generate.",
            "faq": [
                ("Why different events give different numbers?","Each event has unique numeric characteristics. Marriage favors paired numbers, Graduation favors odd numbers, etc."),
                ("Can I choose a future event?","Yes. Choose an event you're looking forward to — let anticipation fuel your picks."),
                ("Same event, same numbers?","No. Events set the preference direction, but randomization varies each time."),
                ("Which event is luckiest?","None is statistically better. Choose whichever is most meaningful to you right now."),
                ("Can I combine multiple events?","Yes. Generate from several events and combine your favorites."),
            ],
        },
    },
    "dream": {
        "zh-TW": {
            "intro": "夢境選號是一種古老而迷人的選號方式，將您夢到的內容轉化為彩票號碼。在許多文化中，夢境被認為是潛意識傳遞訊息的管道，其中可能隱含著幸運的密碼。系統會分析您輸入的夢境描述文字，將每個字的編碼值進行數學運算，透過特殊的雜湊算法將文字轉換成固定範圍內的號碼。相同的夢境描述會產生相同的基礎號碼，但每次會加入隨機擾動產生略有不同的組合。建議盡量詳細描述夢境的關鍵元素，如場景、人物、物品、顏色等，讓號碼更加個人化。",
            "steps": "選擇彩種，在文字框中描述您的夢境內容（越詳細越好），點擊「產生號碼」。系統會將夢境文字轉換成專屬的號碼。",
            "faq": [
                ("夢境描述要寫多少字？","沒有限制，但建議至少 10 個字以上。描述越詳細，產生的號碼越個人化。"),
                ("同一個夢描述一樣的結果嗎？","基礎轉換結果相同，但每次會有小幅隨機變化。"),
                ("什麼樣的夢最適合？","任何夢境都可以。包含數字、日期或具體物品的夢境會產生更有趣的結果。"),
                ("可以用英文描述嗎？","可以。中英文都支援，但不同語言描述同一個夢會產生不同的號碼。"),
                ("夢境選號有根據嗎？","夢境解讀屬於文化傳統和個人信仰。本工具將其轉化為趣味選號方式，不保證準確性。"),
            ],
        },
        "en": {
            "intro": "Dream Pick is an ancient and fascinating method that converts dream content into lottery numbers. Many cultures believe dreams carry subconscious messages with hidden lucky codes. The system analyzes your dream description, converting each character's encoding through special hash algorithms into numbers within the lottery range. More detailed descriptions produce more personalized numbers.",
            "steps": "Select your lottery, describe your dream in the text box (the more detail the better), and click Generate. The system converts your dream text into unique numbers.",
            "faq": [
                ("How much should I write?","No limit, but 10+ words recommended. More detail = more personalized numbers."),
                ("Same dream = same numbers?","Base conversion is the same, but each generation adds slight random variation."),
                ("What kinds of dreams work best?","Any dream works. Dreams containing numbers, dates, or specific objects produce more interesting results."),
                ("Can I describe in any language?","Yes. All languages are supported, but different languages produce different numbers for the same dream."),
                ("Is dream picking scientifically valid?","Dream interpretation is cultural tradition. This tool converts it into an entertaining selection method."),
            ],
        },
    },
    "divination": {
        "zh-TW": {
            "intro": "卦象選號源自中國最古老的智慧典籍《易經》的八卦系統。八卦（乾兌離震巽坎艮坤）代表天地萬物的八種基本力量，每一卦都有對應的數字和方位。系統模擬古代的「擲筊」或「搖卦」過程，透過虛擬的隨機搖卦產生卦象，再將卦象對應的數字轉換為彩票號碼。乾（1）代表天、力量和創始；坤（8）代表地、包容和穩定。不同卦象的組合代表不同的能量流動，為您帶來獨特的選號靈感。這不僅是選號，更是一次與古老智慧對話的體驗。",
            "steps": "選擇彩種，點擊「產生號碼」即可。系統會自動進行虛擬搖卦，根據產生的卦象對應出彩票號碼。",
            "faq": [
                ("八卦對應的數字是什麼？","乾（1）、兌（2）、離（3）、震（4）、巽（5）、坎（6）、艮（7）、坤（8）。"),
                ("卦象選號需要懂易經嗎？","不需要。系統自動完成搖卦和解卦過程，您只需要點擊按鈕。"),
                ("每次搖的卦不同嗎？","是的。每次搖卦都是獨立的隨機過程，會產生不同的卦象和號碼。"),
                ("卦象選號有靈驗嗎？","易經是中國五千年的文化智慧結晶，但用於彩票選號僅供娛樂。中獎與否取決於概率。"),
                ("六十四卦都會出現嗎？","系統使用八卦（8 種）和六十四卦（64 種組合）的數字對應，涵蓋所有可能的卦象。"),
            ],
        },
        "en": {
            "intro": "Divination Pick draws from the ancient Chinese I Ching (Book of Changes) and its Eight Trigrams system. The eight trigrams (Qian, Dui, Li, Zhen, Xun, Kan, Gen, Kun) represent fundamental forces of nature, each with corresponding numbers. The system simulates traditional coin-tossing divination, generating trigrams and converting them into lottery numbers. Qian (1) represents heaven and creative force; Kun (8) represents earth and receptivity.",
            "steps": "Select your lottery and click Generate. The system performs virtual divination, mapping the resulting trigrams to lottery numbers.",
            "faq": [
                ("What are the trigram numbers?","Qian(1), Dui(2), Li(3), Zhen(4), Xun(5), Kan(6), Gen(7), Kun(8)."),
                ("Do I need to know I Ching?","No. The system handles all divination and interpretation automatically."),
                ("Different trigrams each time?","Yes. Each divination is an independent random process producing different trigrams."),
                ("Is I Ching divination effective?","I Ching is 5,000 years of Chinese wisdom, but for lottery purposes it's entertainment only. Winning depends on probability."),
                ("Are all 64 hexagrams covered?","The system uses both 8 trigrams and 64 hexagram combinations for number mapping."),
            ],
        },
    },
}

# For languages without specific content, fall back to English
def get_tool_content(tkey, lang):
    """Get content for a tool in the given language, fallback to English"""
    tc = TOOL_CONTENT.get(tkey, {})
    if lang in tc:
        return tc[lang]
    if lang == "zh-CN" and "zh-TW" in tc:
        # Convert zh-TW to zh-CN (simplified)
        c = tc["zh-TW"].copy()
        return c  # Good enough for now
    return tc.get("en", {"intro":"","steps":"","faq":[]})



# ============================================================
# 9. 12 SHARED TOOL PAGES
# ============================================================
TOOLS = [
    {"id":"random-pick","emoji":"🎲","key":"random"},
    {"id":"hot-pick","emoji":"🔥","key":"hot_pick"},
    {"id":"cold-pick","emoji":"❄️","key":"cold_pick"},
    {"id":"birthday-pick","emoji":"🎂","key":"birthday"},
    {"id":"zodiac-pick","emoji":"♈","key":"zodiac"},
    {"id":"chinese-zodiac-pick","emoji":"🐉","key":"chinese_zodiac"},
    {"id":"ai-pick","emoji":"🤖","key":"ai_pick"},
    {"id":"lucky-number","emoji":"🍀","key":"lucky_number"},
    {"id":"bazi-pick","emoji":"☯","key":"bazi"},
    {"id":"life-event-pick","emoji":"🎊","key":"life_event"},
    {"id":"dream-pick","emoji":"💭","key":"dream"},
    {"id":"divination-pick","emoji":"🔮","key":"divination"},
]

TOOL_NAMES = {
    "random":{"zh-TW":"隨機選號","en":"Random Pick","ja":"ランダム","ko":"랜덤","fr":"Aléatoire","de":"Zufallszahlen","es":"Aleatorio","pt":"Aleatório","id":"Acak","zh-CN":"随机选号"},
    "hot_pick":{"zh-TW":"熱門號碼選號","en":"Hot Numbers Pick","ja":"ホット番号","ko":"핫 번호","fr":"Numéros chauds","de":"Heiße Zahlen","es":"Números calientes","pt":"Números quentes","id":"Nomor panas","zh-CN":"热门号码选号"},
    "cold_pick":{"zh-TW":"冷門號碼選號","en":"Cold Numbers Pick","ja":"コールド番号","ko":"콜드 번호","fr":"Numéros froids","de":"Kalte Zahlen","es":"Números fríos","pt":"Números frios","id":"Nomor dingin","zh-CN":"冷门号码选号"},
    "birthday":{"zh-TW":"生日選號","en":"Birthday Pick","ja":"誕生日","ko":"생일","fr":"Anniversaire","de":"Geburtstag","es":"Cumpleaños","pt":"Aniversário","id":"Ulang tahun","zh-CN":"生日选号"},
    "zodiac":{"zh-TW":"星座選號","en":"Zodiac Pick","ja":"星座","ko":"별자리","fr":"Zodiaque","de":"Sternzeichen","es":"Zodíaco","pt":"Zodíaco","id":"Zodiak","zh-CN":"星座选号"},
    "chinese_zodiac":{"zh-TW":"生肖選號","en":"Chinese Zodiac Pick","ja":"干支","ko":"띠","fr":"Zodiaque chinois","de":"Chinesisches Tierzeichen","es":"Zodíaco chino","pt":"Zodíaco chinês","id":"Shio","zh-CN":"生肖选号"},
    "ai_pick":{"zh-TW":"AI 分析推薦","en":"AI Analysis Pick","ja":"AI分析","ko":"AI 분석","fr":"Analyse IA","de":"KI-Analyse","es":"Análisis IA","pt":"Análise IA","id":"Analisis AI","zh-CN":"AI 分析推荐"},
    "lucky_number":{"zh-TW":"幸運數字","en":"Lucky Number","ja":"ラッキーナンバー","ko":"행운의 숫자","fr":"Numéro chanceux","de":"Glückszahl","es":"Número de suerte","pt":"Número da sorte","id":"Nomor keberuntungan","zh-CN":"幸运数字"},
    "bazi":{"zh-TW":"八字選號","en":"BaZi Pick","ja":"四柱推命","ko":"사주","fr":"BaZi","de":"BaZi","es":"BaZi","pt":"BaZi","id":"BaZi","zh-CN":"八字选号"},
    "life_event":{"zh-TW":"大事件選號","en":"Life Event Pick","ja":"ライフイベント","ko":"인생 이벤트","fr":"Événement","de":"Lebensereignis","es":"Evento vital","pt":"Evento de vida","id":"Peristiwa hidup","zh-CN":"大事件选号"},
    "dream":{"zh-TW":"夢境選號","en":"Dream Pick","ja":"夢占い","ko":"꿈","fr":"Rêve","de":"Traum","es":"Sueño","pt":"Sonho","id":"Mimpi","zh-CN":"梦境选号"},
    "divination":{"zh-TW":"卦象選號","en":"Divination Pick","ja":"占い","ko":"점","fr":"Divination","de":"Wahrsagen","es":"Adivinación","pt":"Adivinhação","id":"Ramalan","zh-CN":"卦象选号"},
}

def tool_name(key, lang):
    return TOOL_NAMES.get(key,{}).get(lang, TOOL_NAMES.get(key,{}).get("en",key))

def gen_tool_page(lang, tool):
    """Generate a shared tool page with lottery selector"""
    tid = tool["id"]
    tkey = tool["key"]
    tname = tool_name(tkey, lang)
    emoji = tool["emoji"]
    
    title = f"{emoji} {tname} — Lottery Number Generator | SoftGlow"
    if lang == "zh-TW":
        title = f"{emoji} {tname} — 全球彩票選號工具 | SoftGlow"
    desc = f"{tname}. Free lottery number generator for Powerball, EuroMillions, 威力彩 and 15+ lotteries."
    
    # Lottery selector options
    options = "".join(f'<option value="{l["slug"]}" data-pick="{l["pick"]}" data-range="{l["pick_range"]}" data-bonus="{l["bonus"]}" data-brange="{l["bonus_range"]}">{l["flag"]} {lname(l["slug"],lang)}</option>' for l in LOTTERIES)
    
    # Tool-specific input UI
    input_html = ""
    if tkey == "birthday":
        lbl = {"zh-TW":"選擇出生日期","en":"Select your birthday"}.get(lang,"Select your birthday")
        input_html = f'<div class="tool-input"><label>{lbl}</label><input type="date" id="toolDate" value="1990-01-15" style="width:100%;padding:10px;border:1px solid #CBD5E0;border-radius:8px;font-size:15px"></div>'
    elif tkey == "zodiac":
        signs = ["♈ Aries","♉ Taurus","♊ Gemini","♋ Cancer","♌ Leo","♍ Virgo","♎ Libra","♏ Scorpio","♐ Sagittarius","♑ Capricorn","♒ Aquarius","♓ Pisces"]
        opts = "".join(f'<option value="{i}">{s}</option>' for i,s in enumerate(signs))
        lbl = {"zh-TW":"選擇星座","en":"Select zodiac sign"}.get(lang,"Select zodiac sign")
        input_html = f'<div class="tool-input"><label>{lbl}</label><select id="toolSelect" style="width:100%;padding:10px;border:1px solid #CBD5E0;border-radius:8px;font-size:15px">{opts}</select></div>'
    elif tkey == "chinese_zodiac":
        animals_zh = ["🐀 鼠","🐂 牛","🐅 虎","🐇 兔","🐉 龍","🐍 蛇","🐴 馬","🐏 羊","🐵 猴","🐔 雞","🐶 狗","🐷 豬"]
        animals_en = ["🐀 Rat","🐂 Ox","🐅 Tiger","🐇 Rabbit","🐉 Dragon","🐍 Snake","🐴 Horse","🐏 Goat","🐵 Monkey","🐔 Rooster","🐶 Dog","🐷 Pig"]
        animals = animals_zh if lang.startswith("zh") else animals_en
        opts = "".join(f'<option value="{i}">{a}</option>' for i,a in enumerate(animals))
        lbl = {"zh-TW":"選擇生肖","en":"Select Chinese zodiac"}.get(lang,"Select Chinese zodiac")
        input_html = f'<div class="tool-input"><label>{lbl}</label><select id="toolSelect" style="width:100%;padding:10px;border:1px solid #CBD5E0;border-radius:8px;font-size:15px">{opts}</select></div>'
    elif tkey == "lucky_number":
        lbl = {"zh-TW":"輸入你的名字","en":"Enter your name"}.get(lang,"Enter your name")
        input_html = f'<div class="tool-input"><label>{lbl}</label><input type="text" id="toolText" placeholder="{lbl}" style="width:100%;padding:10px;border:1px solid #CBD5E0;border-radius:8px;font-size:15px"></div>'
    elif tkey == "dream":
        lbl = {"zh-TW":"描述你的夢境","en":"Describe your dream"}.get(lang,"Describe your dream")
        input_html = f'<div class="tool-input"><label>{lbl}</label><textarea id="toolText" rows="3" placeholder="{lbl}" style="width:100%;padding:10px;border:1px solid #CBD5E0;border-radius:8px;font-size:15px;resize:vertical"></textarea></div>'
    elif tkey == "life_event":
        events_zh = ["結婚","生小孩","買房","升遷","畢業","退休","旅行","搬家","開業","紀念日"]
        events_en = ["Wedding","New baby","Buy house","Promotion","Graduation","Retirement","Travel","Moving","New business","Anniversary"]
        events = events_zh if lang.startswith("zh") else events_en
        opts = "".join(f'<option value="{i}">{e}</option>' for i,e in enumerate(events))
        lbl = {"zh-TW":"選擇人生大事","en":"Select life event"}.get(lang,"Select life event")
        input_html = f'<div class="tool-input"><label>{lbl}</label><select id="toolSelect" style="width:100%;padding:10px;border:1px solid #CBD5E0;border-radius:8px;font-size:15px">{opts}</select></div>'
    elif tkey == "bazi":
        lbl = {"zh-TW":"選擇出生日期和時辰","en":"Select birth date and time"}.get(lang,"Select birth date and time")
        input_html = f'<div class="tool-input"><label>{lbl}</label><input type="datetime-local" id="toolDate" value="1990-01-15T08:00" style="width:100%;padding:10px;border:1px solid #CBD5E0;border-radius:8px;font-size:15px"></div>'
    
    # Other tools in sidebar
    other_tools = "".join(f'<a href="{page_url(lang,None,ot["id"])}">{ot["emoji"]} {tool_name(ot["key"],lang)}</a>' for ot in TOOLS if ot["id"] != tid)
    
    lang_btns = "".join(f'<a href="{page_url(la,None,tid)}" class="lang-btn{" active" if la==lang else ""}">{la}</a>' for la in ALL_LANGS)
    
    # Get rich content for this tool
    tc = get_tool_content(tkey, lang)
    tc_intro = tc.get("intro", "")
    tc_steps = tc.get("steps", "")
    tc_faq = tc.get("faq", [])
    
    faq_html = ""
    for q, a in tc_faq:
        faq_html += f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>'
    faq_schema = ""
    if tc_faq:
        items = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in tc_faq]
        import json as _json
        faq_schema = f'<script type="application/ld+json">{_json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":items}, ensure_ascii=False)}</script>'
    
    extra_head_tool = faq_schema
    
    body = f'''<div class="layout"><div class="main">
  <div class="card">
    <h1>{emoji} {tname}</h1>
    <p style="color:#4A5568;font-size:15px;margin-bottom:16px">{tc_intro}</p>
    
    <div class="tool-input">
      <label>{t(lang,"select_lottery")}</label>
      <select id="lotterySelect" style="width:100%;padding:10px;border:1px solid #CBD5E0;border-radius:8px;font-size:15px" onchange="updateConfig()">
        {options}
      </select>
    </div>
    
    {input_html}
    
    <button class="btn" style="width:100%;margin-top:12px" onclick="generateNums()">{t(lang,"generate")} {emoji}</button>
    
    <div class="gen-result" id="genResult" style="display:none">
      <div style="font-size:13px;color:#718096;margin-bottom:8px">{t(lang,"your_nums")}</div>
      <div id="genNums"></div>
    </div>
  </div>
  <div class="ad-slot" id="ad1"></div>
  
  {"<div class=\'card\'><h2>📝 " + ("使用步驟" if lang.startswith("zh") else "How to Use") + "</h2><p>" + tc_steps + "</p></div>" if tc_steps else ""}
  
  {"<div class=\'card\'><h2>❓ " + t(lang,"faq") + "</h2>" + faq_html + "</div>" if faq_html else ""}
  
  <div class="ad-slot" id="ad2"></div>
  <div class="lang-bar">{lang_btns}</div>
</div>
<aside class="sidebar">
  <div class="ad-slot" id="ad-side"></div>
  <div class="card"><h3>🎲 {t(lang,"select_method")}</h3>{other_tools}</div>
</aside></div>'''
    
    # JS for number generation
    gen_js = f'''<script>
var CFG={{pick:5,pickRange:69,bonus:1,bonusRange:26}};
function updateConfig(){{var s=document.getElementById("lotterySelect");var o=s.options[s.selectedIndex];CFG.pick=parseInt(o.dataset.pick);CFG.pickRange=parseInt(o.dataset.range);CFG.bonus=parseInt(o.dataset.bonus);CFG.bonusRange=parseInt(o.dataset.brange)}}
function randInt(a,b){{return Math.floor(Math.random()*(b-a+1))+a}}
function pickRandom(n,max){{var a=[];for(var i=1;i<=max;i++)a.push(i);for(var i=a.length-1;i>0;i--){{var j=randInt(0,i);var t=a[i];a[i]=a[j];a[j]=t}}return a.slice(0,n).sort(function(x,y){{return x-y}})}}
function generateNums(){{
  updateConfig();
  var main=[],bonus=[];
  var method="{tkey}";
  var seed=0;
  
  if(method==="birthday"||method==="bazi"){{
    var d=document.getElementById("toolDate");
    if(d){{var v=d.value||"1990-01-15";seed=v.replace(/\\D/g,"").split("").reduce(function(a,b){{return a+parseInt(b)}},0)}}
    main=pickRandom(CFG.pick, Math.min(31,CFG.pickRange));
    // Mix in date-derived numbers
    if(seed>0){{var dn=seed%CFG.pickRange+1;if(main.indexOf(dn)===-1&&main.length>0)main[0]=dn;main.sort(function(a,b){{return a-b}})}}
  }}else if(method==="zodiac"||method==="chinese_zodiac"||method==="life_event"){{
    var sel=document.getElementById("toolSelect");
    seed=sel?parseInt(sel.value):0;
    // Use seed to bias selection
    var start=(seed*3)%CFG.pickRange+1;
    main=[];for(var i=0;i<CFG.pick;i++){{var n=(start+i*Math.max(3,Math.floor(CFG.pickRange/CFG.pick)))%CFG.pickRange+1;if(main.indexOf(n)===-1)main.push(n);else main.push(randInt(1,CFG.pickRange))}}
    main=main.slice(0,CFG.pick).sort(function(a,b){{return a-b}});
  }}else if(method==="lucky_number"||method==="dream"){{
    var txt=document.getElementById("toolText");
    var s=txt?txt.value||"lucky":"lucky";
    seed=0;for(var i=0;i<s.length;i++)seed+=s.charCodeAt(i);
    var r=seed;function next(){{r=(r*1103515245+12345)&0x7fffffff;return r}}
    main=[];var used={{}};while(main.length<CFG.pick){{var n=next()%CFG.pickRange+1;if(!used[n]){{used[n]=1;main.push(n)}}}}
    main.sort(function(a,b){{return a-b}});
  }}else{{
    main=pickRandom(CFG.pick,CFG.pickRange);
  }}
  
  if(CFG.bonus>0)bonus=pickRandom(CFG.bonus,CFG.bonusRange);
  
  var h="";for(var i=0;i<main.length;i++)h+='<span class="ball ball-main">'+main[i]+"</span>";
  if(bonus.length){{h+='<span class="draw-plus">+</span>';for(var j=0;j<bonus.length;j++)h+='<span class="ball ball-bonus">'+bonus[j]+"</span>"}}
  document.getElementById("genNums").innerHTML=h;
  document.getElementById("genResult").style.display="block";
}}
updateConfig();
</script>'''
    
    return base_html(lang, title, desc, body, None, tid, ALL_LANGS, extra_head=extra_head_tool, extra_js=gen_js)


# ============================================================
# 10. HOMEPAGE + UNIVERSAL GENERATOR
# ============================================================
def gen_homepage(lang, draws_by_slug):
    titles = {"zh-TW":"全球彩票開獎結果與選號工具 | SoftGlow","en":"Global Lottery Results & Number Generator | SoftGlow","ja":"世界の宝くじ結果＆番号生成 | SoftGlow","ko":"글로벌 복권 결과 및 번호 생성기 | SoftGlow","fr":"Résultats Loterie Mondiale | SoftGlow","de":"Globale Lotterie-Ergebnisse | SoftGlow","es":"Resultados Lotería Mundial | SoftGlow","pt":"Resultados Loteria Global | SoftGlow","id":"Hasil Lotere Global | SoftGlow","zh-CN":"全球彩票开奖结果与选号工具 | SoftGlow"}
    
    regions = {}
    for lot in LOTTERIES:
        r = lot.get("region","Other")
        if r not in regions: regions[r] = []
        regions[r].append(lot)
    
    region_key = {"USA":"region_usa","Americas":"region_americas","Europe":"region_europe","Asia":"region_asia","Oceania":"region_oceania"}
    
    cards = ""
    for region in REGIONS_ORDER:
        if region not in regions: continue
        cards += f'<div class="region-title">{t(lang,region_key.get(region,region))}</div><div class="lottery-grid">'
        for lot in regions[region]:
            slug = lot["slug"]
            draws = draws_by_slug.get(slug,[])
            latest = draws[0]["date"] if draws else "—"
            cards += f'<a href="{page_url(lang,slug)}" class="lottery-card"><div class="flag">{lot["flag"]}</div><div class="lc-name">{lname(slug,lang)}</div><div class="lc-meta">{lot["draw_days"]} · {latest}</div></a>'
        cards += '</div>'
    
    lang_btns = "".join(f'<a href="{page_url(la)}" class="lang-btn{" active" if la==lang else ""}">{la}</a>' for la in ALL_LANGS)
    
    body = f'''<div style="padding:24px 0">
  <div class="card" style="text-align:center;background:linear-gradient(135deg,#FFFBEB,#FEF3C7);border-color:#FDE68A">
    <h1>🎰 {t(lang,"site")}</h1>
    <p style="color:#92400E;font-size:15px;margin-top:8px">15 {t(lang,"all_lotteries")} · 12 {t(lang,"select_method")} · {t(lang,"results")} & {t(lang,"statistics")}</p>
    <div style="margin-top:16px"><a href="{page_url(lang,None,'number-generator')}" class="btn">{t(lang,"number_generator")} 🎲</a></div>
  </div>
  <div class="ad-slot" id="ad1"></div>
  {cards}
  <div class="ad-slot" id="ad2"></div>
  <div class="lang-bar">{lang_btns}</div>
</div>'''
    return base_html(lang, titles.get(lang,""), "", body, canonical_override=full_url(page_url(lang)))


def gen_universal_generator(lang, draws_by_slug):
    titles = {"zh-TW":"樂透選號工具 — 15種全球彩票免費電腦選號","en":"Lottery Number Generator — Free Quick Pick for 15+ Lotteries","ja":"宝くじ番号生成ツール — 15種以上対応","ko":"복권 번호 생성기 — 15개 이상 글로벌 복권","fr":"Générateur Loterie — 15+ Loteries","de":"Lotto Zahlengenerator — 15+ Lotterien","es":"Generador Lotería — 15+ Loterías","pt":"Gerador Loteria — 15+ Loterias","id":"Generator Nomor Lotere — 15+ Lotere","zh-CN":"乐透选号工具 — 15种全球彩票免费选号"}
    
    # Tool cards linking to each tool page
    tool_cards = ""
    for tool in TOOLS:
        tname_l = tool_name(tool["key"], lang)
        tool_cards += f'<a href="{page_url(lang,None,tool["id"])}" class="lottery-card"><div class="flag" style="font-size:28px">{tool["emoji"]}</div><div class="lc-name">{tname_l}</div></a>'
    
    lang_btns = "".join(f'<a href="{page_url(la,None,"number-generator")}" class="lang-btn{" active" if la==lang else ""}">{la}</a>' for la in ALL_LANGS)
    
    body = f'''<div style="padding:24px 0">
  <div class="card" style="text-align:center;background:linear-gradient(135deg,#FFFBEB,#FEF3C7);border-color:#FDE68A">
    <h1>🎲 {titles.get(lang,"").split("—")[0].strip()}</h1>
    <p style="color:#92400E;font-size:15px;margin-top:8px">12 {t(lang,"select_method")} · 15 {t(lang,"all_lotteries")}</p>
  </div>
  <div class="ad-slot" id="ad1"></div>
  <h2 style="font-size:20px;font-weight:700;margin:24px 0 16px">{t(lang,"select_method")}</h2>
  <div class="lottery-grid">{tool_cards}</div>
  <div class="ad-slot" id="ad2"></div>
  <div class="lang-bar">{lang_btns}</div>
</div>'''
    return base_html(lang, titles.get(lang,""), "", body, None, "number-generator", ALL_LANGS)


# ============================================================
# 11. MAIN EXECUTION
# ============================================================
def load_data(data_dir):
    draws_by_slug, stats_by_slug = {}, {}
    for subdir, target in [("results", draws_by_slug), ("stats", stats_by_slug)]:
        d = os.path.join(data_dir, subdir)
        if os.path.isdir(d):
            for fn in os.listdir(d):
                if fn.endswith(".json"):
                    with open(os.path.join(d, fn), encoding="utf-8") as f:
                        target[fn[:-5]] = json.load(f)
    return draws_by_slug, stats_by_slug


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", default="lottery_data")
    parser.add_argument("--output-dir", default="output/lottery")
    args = parser.parse_args()
    
    print(f"Loading data from {args.data_dir}...")
    draws_by_slug, stats_by_slug = load_data(args.data_dir)
    print(f"  Draws: {len(draws_by_slug)} lotteries, Stats: {len(stats_by_slug)} lotteries")
    
    out = args.output_dir
    os.makedirs(out, exist_ok=True)
    total = 0
    
    # 1. Lottery pages (per lottery, per language)
    for lot in LOTTERIES:
        slug = lot["slug"]
        draws = draws_by_slug.get(slug, [])
        stats = stats_by_slug.get(slug, {"total_draws":0,"main_numbers":[],"bonus_numbers":[]})
        
        for lang in lot["langs"]:
            lang_dir = out if lang == "zh-TW" else os.path.join(out, lang)
            os.makedirs(lang_dir, exist_ok=True)
            
            for ptype, gen_fn in [("intro",gen_intro),("results",gen_results),("history",gen_history),("statistics",gen_statistics)]:
                if ptype in ("history","statistics"):
                    html = gen_fn(lang, slug, lot, draws, stats)
                else:
                    html = gen_fn(lang, slug, lot, draws, stats)
                
                suffix = f"-{ptype}" if ptype != "intro" else ""
                path = os.path.join(lang_dir, f"{slug}{suffix}.html")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(html)
                total += 1
        
        print(f"  {slug}: {len(lot['langs'])} langs × 4 pages = {len(lot['langs'])*4}")
    
    # 2. Shared tool pages (12 tools × 10 languages)
    print(f"\nGenerating 12 tool pages × {len(ALL_LANGS)} languages...")
    for tool in TOOLS:
        for lang in ALL_LANGS:
            lang_dir = out if lang == "zh-TW" else os.path.join(out, lang)
            os.makedirs(lang_dir, exist_ok=True)
            html = gen_tool_page(lang, tool)
            path = os.path.join(lang_dir, f"{tool['id']}.html")
            with open(path, "w", encoding="utf-8") as f:
                f.write(html)
            total += 1
    
    # 3. Homepage + Universal generator (10 languages each)
    print(f"\nGenerating homepage + universal generator × {len(ALL_LANGS)} languages...")
    for lang in ALL_LANGS:
        lang_dir = out if lang == "zh-TW" else os.path.join(out, lang)
        os.makedirs(lang_dir, exist_ok=True)
        
        # Homepage
        html = gen_homepage(lang, draws_by_slug)
        path = os.path.join(lang_dir, "index.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        total += 1
        
        # Universal generator
        html = gen_universal_generator(lang, draws_by_slug)
        path = os.path.join(lang_dir, "number-generator.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        total += 1
    
    # 4. Copy data files
    data_out = os.path.join(out, "data")
    os.makedirs(data_out, exist_ok=True)
    for slug, draws in draws_by_slug.items():
        with open(os.path.join(data_out, f"{slug}.json"), "w", encoding="utf-8") as f:
            json.dump(draws, f, ensure_ascii=False)
    
    print(f"\n🎉 完成！共生成 {total} 個頁面")
    print(f"📁 輸出位置: {out}")


if __name__ == "__main__":
    main()

