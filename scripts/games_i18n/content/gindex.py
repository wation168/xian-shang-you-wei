# -*- coding: utf-8 -*-
"""
遊戲區索引頁 /games/{loc}/index.html 的10語言文字內容。
跟單一遊戲的 content/g{slug}.py 是同一種格式，但這裡只有索引頁本身需要的欄位
（title/desc/h1/subtitle/ldDesc/articleH2/articleP/moreToolsHeading/typingSpeedName/
browseAllTools），不需要 ui/i18n/faq——索引頁沒有互動邏輯，純展示13款遊戲的卡片。

繁中(zh-TW)的文字完全照抄原始 /mnt/user-data/uploads/games/index.html，不重新翻譯，
避免既有SEO資產被改動；其餘9語言是新翻譯，語氣比照13款遊戲內容檔已經建立的風格
（不逐字直譯，貼近當地玩家會用的說法）。
"""

L = {

"zh-TW": {
  "title": "免費線上小遊戲 - 純網頁遊戲，免下載免安裝 | SoftGlow",
  "desc": "SoftGlow 免費線上小遊戲專區，純網頁遊戲免下載免安裝，開瀏覽器就能玩。反應力測試、記憶翻牌、打地鼠等持續新增中。",
  "h1": "免費線上小遊戲",
  "subtitle": "純網頁遊戲，免下載免安裝，開瀏覽器就能玩，成績可以直接分享給朋友比較。",
  "ldDesc": "SoftGlow 免費線上小遊戲專區，純網頁遊戲免下載免安裝。",
  "articleH2": "關於這個遊戲專區",
  "articleP": "這裡的遊戲全部都是純網頁小遊戲，不需要下載安裝任何App，也不需要註冊帳號，打開頁面就能直接玩。所有遊戲都在你的瀏覽器裡執行，不會佔用伺服器資源，你的成績也只會儲存在你自己的裝置上。我們會持續新增更多輕量、好上手的小遊戲，歡迎常回來看看。",
  "moreToolsHeading": "相關工具",
  "typingSpeedName": "打字速度測試",
  "browseAllTools": "瀏覽全部工具",
},

"en": {
  "title": "Free Online Games - No Download, Play Instantly | SoftGlow",
  "desc": "Free online games at SoftGlow — no download, no install, just open your browser and play. Reaction time test, memory match, whack-a-mole, and more, with new games added regularly.",
  "h1": "Free Online Games",
  "subtitle": "Pure browser games — no download, no install, just open the page and play. Share your score with friends and see who comes out on top.",
  "ldDesc": "SoftGlow's free online games hub — pure browser games, no download or install required.",
  "articleH2": "About this games hub",
  "articleP": "Every game here runs entirely in your browser — no app to download, no account to create, just open the page and start playing. Nothing runs on our servers, and your scores are stored only on your own device. We're steadily adding more lightweight, easy-to-pick-up games, so check back often.",
  "moreToolsHeading": "Related Tools",
  "typingSpeedName": "Typing Speed Calculator",
  "browseAllTools": "Browse all tools",
},

"de": {
  "title": "Kostenlose Online-Spiele - Ohne Download sofort spielen | SoftGlow",
  "desc": "Kostenlose Online-Spiele bei SoftGlow — ohne Download, ohne Installation, einfach Browser öffnen und loslegen. Reaktionstest, Memory-Spiel, Hau den Maulwurf und mehr, laufend neue Spiele.",
  "h1": "Kostenlose Online-Spiele",
  "subtitle": "Reine Browser-Spiele — ohne Download, ohne Installation, einfach die Seite öffnen und spielen. Teile dein Ergebnis mit Freunden und vergleicht eure Punktzahlen.",
  "ldDesc": "SoftGlows kostenloser Bereich für Online-Spiele — reine Browser-Spiele, ohne Download oder Installation.",
  "articleH2": "Über diesen Spielebereich",
  "articleP": "Alle Spiele hier laufen komplett in deinem Browser — keine App zum Herunterladen, kein Konto nötig, einfach die Seite öffnen und loslegen. Nichts läuft auf unseren Servern, und deine Ergebnisse werden nur auf deinem eigenen Gerät gespeichert. Wir fügen laufend weitere leichte, leicht verständliche Spiele hinzu, schau also gerne öfter vorbei.",
  "moreToolsHeading": "Ähnliche Werkzeuge",
  "typingSpeedName": "Tippgeschwindigkeit-Rechner",
  "browseAllTools": "Alle Werkzeuge ansehen",
},

"es": {
  "title": "Juegos Online Gratis - Sin Descargas, Juega al Instante | SoftGlow",
  "desc": "Juegos online gratis en SoftGlow — sin descargas, sin instalación, abre el navegador y juega. Test de reacción, juego de memoria, golpea al topo y más, con nuevos juegos añadidos regularmente.",
  "h1": "Juegos Online Gratis",
  "subtitle": "Juegos puramente de navegador — sin descargas, sin instalación, abre la página y juega. Comparte tu puntuación con amigos y ved quién gana.",
  "ldDesc": "La zona de juegos online gratuitos de SoftGlow — juegos de navegador puros, sin descarga ni instalación.",
  "articleH2": "Sobre esta zona de juegos",
  "articleP": "Todos los juegos de aquí funcionan completamente en tu navegador — sin apps que descargar, sin necesidad de crear una cuenta, solo abre la página y empieza a jugar. Nada se ejecuta en nuestros servidores, y tus puntuaciones se guardan únicamente en tu propio dispositivo. Seguimos añadiendo más juegos ligeros y fáciles de aprender, así que vuelve a menudo.",
  "moreToolsHeading": "Herramientas relacionadas",
  "typingSpeedName": "Calculadora de Velocidad de Escritura",
  "browseAllTools": "Ver todas las herramientas",
},

"fr": {
  "title": "Jeux en Ligne Gratuits - Sans Téléchargement, Jouez Instantanément | SoftGlow",
  "desc": "Jeux en ligne gratuits sur SoftGlow — sans téléchargement, sans installation, ouvrez votre navigateur et jouez. Test de temps de réaction, jeu de mémoire, tape la taupe et plus, avec de nouveaux jeux ajoutés régulièrement.",
  "h1": "Jeux en Ligne Gratuits",
  "subtitle": "Des jeux purement navigateur — sans téléchargement, sans installation, ouvrez la page et jouez. Partagez votre score avec vos amis et voyez qui l'emporte.",
  "ldDesc": "L'espace jeux en ligne gratuits de SoftGlow — des jeux purement navigateur, sans téléchargement ni installation.",
  "articleH2": "À propos de cet espace jeux",
  "articleP": "Tous les jeux ici fonctionnent entièrement dans votre navigateur — aucune application à télécharger, aucun compte à créer, ouvrez simplement la page et commencez à jouer. Rien ne tourne sur nos serveurs, et vos scores sont enregistrés uniquement sur votre propre appareil. Nous ajoutons régulièrement de nouveaux jeux légers et faciles à prendre en main, alors revenez souvent.",
  "moreToolsHeading": "Outils similaires",
  "typingSpeedName": "Calculateur de Vitesse de Dactylographie",
  "browseAllTools": "Voir tous les outils",
},

"id": {
  "title": "Game Online Gratis - Tanpa Download, Main Langsung | SoftGlow",
  "desc": "Game online gratis di SoftGlow — tanpa download, tanpa instalasi, cukup buka browser dan mainkan. Tes waktu reaksi, permainan memori, pukul tikus tanah, dan lainnya, dengan game baru yang terus ditambahkan.",
  "h1": "Game Online Gratis",
  "subtitle": "Game berbasis browser murni — tanpa download, tanpa instalasi, cukup buka halaman dan mainkan. Bagikan skormu ke teman dan lihat siapa yang menang.",
  "ldDesc": "Area game online gratis SoftGlow — game berbasis browser murni, tanpa download atau instalasi.",
  "articleH2": "Tentang area game ini",
  "articleP": "Semua game di sini berjalan sepenuhnya di browser kamu — tidak perlu download aplikasi, tidak perlu bikin akun, cukup buka halamannya dan langsung main. Tidak ada yang berjalan di server kami, dan skormu hanya disimpan di perangkatmu sendiri. Kami terus menambahkan game ringan dan mudah dimainkan, jadi sering-sering mampir ya.",
  "moreToolsHeading": "Alat Terkait",
  "typingSpeedName": "Kalkulator Kecepatan Mengetik",
  "browseAllTools": "Lihat semua alat",
},

"ja": {
  "title": "無料オンラインゲーム - ダウンロード不要ですぐ遊べる | SoftGlow",
  "desc": "SoftGlowの無料オンラインゲームコーナー。ダウンロード・インストール不要、ブラウザを開くだけですぐ遊べます。反応速度テスト、メモリーゲーム、モグラたたきなど、随時追加中。",
  "h1": "無料オンラインゲーム",
  "subtitle": "純粋なブラウザゲームなので、ダウンロードもインストールも不要。ページを開くだけで遊べて、スコアを友達とシェアして比べられます。",
  "ldDesc": "SoftGlowの無料オンラインゲームコーナー。ダウンロード・インストール不要の純粋なブラウザゲーム。",
  "articleH2": "このゲームコーナーについて",
  "articleP": "ここにあるゲームはすべてブラウザだけで完結する純粋なウェブゲームで、アプリのダウンロードもアカウント登録も必要ありません。ページを開けばすぐに遊べます。サーバー側のリソースは一切使わず、スコアはあなたの端末にだけ保存されます。今後も軽量で遊びやすいゲームを追加していく予定なので、ぜひ定期的にチェックしてみてください。",
  "moreToolsHeading": "関連ツール",
  "typingSpeedName": "タイピング速度計算機",
  "browseAllTools": "ツール一覧を見る",
},

"ko": {
  "title": "무료 온라인 게임 - 다운로드 없이 바로 플레이 | SoftGlow",
  "desc": "SoftGlow의 무료 온라인 게임 코너. 다운로드나 설치 없이 브라우저만 열면 바로 즐길 수 있습니다. 반응 속도 테스트, 카드 짝 맞추기, 두더지 잡기 등 계속 추가되고 있습니다.",
  "h1": "무료 온라인 게임",
  "subtitle": "순수 브라우저 게임이라 다운로드도 설치도 필요 없습니다. 페이지를 열기만 하면 바로 플레이할 수 있고, 점수를 친구와 공유해서 비교할 수 있습니다.",
  "ldDesc": "SoftGlow의 무료 온라인 게임 코너 — 다운로드나 설치가 필요 없는 순수 브라우저 게임.",
  "articleH2": "이 게임 코너에 대해",
  "articleP": "여기 있는 게임은 모두 브라우저에서만 실행되는 순수 웹 게임으로, 앱을 다운로드하거나 계정을 만들 필요가 없습니다. 페이지를 열면 바로 플레이할 수 있습니다. 서버 자원을 전혀 사용하지 않으며, 점수는 사용자의 기기에만 저장됩니다. 가볍고 배우기 쉬운 게임을 계속 추가하고 있으니 자주 들러 주세요.",
  "moreToolsHeading": "관련 도구",
  "typingSpeedName": "타이핑 속도 계산기",
  "browseAllTools": "전체 도구 보기",
},

"pt": {
  "title": "Jogos Online Grátis - Sem Download, Jogue na Hora | SoftGlow",
  "desc": "Jogos online grátis no SoftGlow — sem download, sem instalação, basta abrir o navegador e jogar. Teste de tempo de reação, jogo da memória, bate-toupeira e mais, com novos jogos adicionados regularmente.",
  "h1": "Jogos Online Grátis",
  "subtitle": "Jogos puramente de navegador — sem download, sem instalação, basta abrir a página e jogar. Compartilhe sua pontuação com amigos e veja quem se sai melhor.",
  "ldDesc": "A área de jogos online grátis do SoftGlow — jogos puramente de navegador, sem download ou instalação.",
  "articleH2": "Sobre esta área de jogos",
  "articleP": "Todos os jogos aqui rodam inteiramente no seu navegador — sem app para baixar, sem conta para criar, basta abrir a página e começar a jogar. Nada roda em nossos servidores, e suas pontuações ficam salvas apenas no seu próprio dispositivo. Estamos sempre adicionando mais jogos leves e fáceis de jogar, então volte sempre para conferir.",
  "moreToolsHeading": "Ferramentas relacionadas",
  "typingSpeedName": "Calculadora de Velocidade de Digitação",
  "browseAllTools": "Ver todas as ferramentas",
},

"zh-CN": {
  "title": "免费在线小游戏 - 纯网页游戏，免下载免安装 | SoftGlow",
  "desc": "SoftGlow免费在线小游戏专区，纯网页游戏免下载免安装，打开浏览器就能玩。反应力测试、记忆翻牌、打地鼠等持续新增中。",
  "h1": "免费在线小游戏",
  "subtitle": "纯网页游戏，免下载免安装，打开浏览器就能玩，成绩可以直接分享给朋友比较。",
  "ldDesc": "SoftGlow免费在线小游戏专区，纯网页游戏免下载免安装。",
  "articleH2": "关于这个游戏专区",
  "articleP": "这里的游戏全部都是纯网页小游戏，不需要下载安装任何App，也不需要注册账号，打开页面就能直接玩。所有游戏都在你的浏览器里运行，不会占用服务器资源，你的成绩也只会保存在你自己的设备上。我们会持续新增更多轻量、好上手的小游戏，欢迎常回来看看。",
  "moreToolsHeading": "相关工具",
  "typingSpeedName": "打字速度计算器",
  "browseAllTools": "浏览全部工具",
},

}
