"""
thicken_all_markets.py — 全市場加厚腳本
27 頁 × 7 語言：zh-TW(10) + en(3) + id(4) + ja(4) + es(3) + ko(1) + zh-CN(2)
"""
import os, re

BASE = os.path.join(os.path.dirname(__file__), "..", "backend", "frontend", "tools")

PAGES = {
    # ===== zh-TW (root) =====
    ("", "salary-raise"): {
        "tables": [
            {"title": "台灣各產業平均調薪幅度（2026年）",
             "headers": ["產業", "平均調薪%", "中位數月薪", "備註"],
             "rows": [
                 ["半導體", "5-8%", "65,000", "台積電帶動"],
                 ["金融保險", "3-5%", "55,000", "穩定成長"],
                 ["軟體資訊", "4-7%", "60,000", "AI 需求推升"],
                 ["製造業", "2-4%", "42,000", "傳產較保守"],
                 ["餐飲服務", "2-3%", "32,000", "基本工資連動"],
                 ["醫療照護", "3-5%", "50,000", "護理人力缺"],
             ]},
            {"title": "調薪幅度 vs 實質購買力",
             "headers": ["調薪幅度", "CPI 通膨 2%", "實質增幅", "月薪5萬實際增加"],
             "rows": [
                 ["3%", "2%", "1%", "+500元/月"],
                 ["5%", "2%", "3%", "+1,500元/月"],
                 ["8%", "2%", "6%", "+3,000元/月"],
                 ["10%", "2%", "8%", "+4,000元/月"],
             ]},
        ],
        "extra": """<h2>談薪水的最佳時機</h2>
<p>根據人力銀行調查，台灣企業最常在年度考核後（1-3月）進行調薪。如果要主動談薪，建議在考核前一個月準備好績效數據和市場薪資比較。跳槽的薪資漲幅通常是 15-30%，遠高於內部調薪的 3-5%。但頻繁跳槽（2年內換3份以上）會被 HR 視為不穩定。</p>
<h2>用這個計算機談薪的技巧</h2>
<p>先用計算機算出調薪後的實際數字，再扣掉通膨影響。如果老闆說「幫你加薪 3%」，實際上扣掉 2% 通膨後只多了 1%。有了具體數字，談判更有說服力。</p>""",
    },
    ("", "paper-weight"): {
        "tables": [
            {"title": "常見紙張規格重量對照",
             "headers": ["規格", "單張重量", "500張重量", "常見用途"],
             "rows": [
                 ["A4 影印紙 (70g)", "4.36g", "2.18kg", "一般列印"],
                 ["A4 影印紙 (80g)", "4.99g", "2.49kg", "雙面列印"],
                 ["A4 厚卡紙 (120g)", "7.48g", "3.74kg", "名片、卡片"],
                 ["A3 影印紙 (80g)", "9.97g", "4.99kg", "海報、圖表"],
                 ["B5 筆記紙 (70g)", "3.13g", "1.57kg", "筆記本"],
             ]},
            {"title": "郵寄重量與郵資對照（中華郵政 2026年）",
             "headers": ["重量", "國內平信", "國內掛號", "備註"],
             "rows": [
                 ["20g以內", "8元", "33元", "約4張A4"],
                 ["50g以內", "8元", "33元", "約10張A4"],
                 ["100g以內", "12元", "37元", "約20張A4"],
                 ["250g以內", "20元", "45元", "約50張A4"],
                 ["500g以內", "32元", "57元", "約100張A4"],
             ]},
        ],
        "extra": """<h2>紙張基重（磅重）怎麼算</h2>
<p>台灣常用的紙張規格是「基重」，單位是 g/㎡（GSM）。一張 A4 的面積是 0.21 × 0.297 = 0.06237 ㎡，所以基重 80g/㎡ 的 A4 紙，單張重量 = 80 × 0.06237 = 約 4.99g。知道這個公式，任何尺寸的紙都能快速算出重量。</p>
<h2>大量郵寄的成本控制</h2>
<p>如果要寄 DM 或宣傳單，選 70g 比 80g 的紙每張省 0.63g。寄 1000 封的話，就省了 630g，可能從「100g以內」降到「50g以內」的郵資級距，每封省 4 元，1000 封就省 4000 元。</p>""",
    },
    ("", "pool-volume"): {
        "tables": [
            {"title": "常見泳池尺寸與水量",
             "headers": ["類型", "尺寸 (長×寬×深)", "水量", "備註"],
             "rows": [
                 ["家用充氣池", "3×2×0.7m", "4,200 公升", "約 4 噸水"],
                 ["小型庭院池", "6×3×1.2m", "21,600 公升", "約 22 噸水"],
                 ["標準家庭池", "8×4×1.5m", "48,000 公升", "約 48 噸水"],
                 ["半標準泳池", "25×10×1.5m", "375,000 公升", "社區常見"],
                 ["奧運標準池", "50×25×2m", "2,500,000 公升", "2500 噸水"],
             ]},
        ],
        "extra": """<h2>水費估算</h2>
<p>以台灣自來水費率估算，填滿一個標準家庭泳池（48噸）的水費約為 500-700 元。但泳池的主要成本不是水費，而是過濾系統的電費（每月約 1,000-3,000 元）和藥劑費（每月約 500-1,500 元）。建造前要先評估長期維護成本。</p>
<h2>不規則形狀的計算方法</h2>
<p>如果泳池不是標準的長方形，可以把它拆成幾個簡單形狀分別計算再加總。例如 L 型泳池拆成兩個長方形，圓形泳池用 π × 半徑² × 深度。腎形泳池可以近似為橢圓形：π × 長軸/2 × 短軸/2 × 深度 × 0.85（修正係數）。</p>""",
    },
    ("", "standard-deviation"): {
        "tables": [
            {"title": "標準差的實際意義（以投資為例）",
             "headers": ["標準差", "代表含義", "投資案例", "風險等級"],
             "rows": [
                 ["5%", "波動很小", "債券基金", "低"],
                 ["10-15%", "中等波動", "平衡型基金", "中"],
                 ["15-20%", "明顯波動", "台股大盤", "中高"],
                 ["25%+", "劇烈波動", "個股、加密貨幣", "高"],
             ]},
        ],
        "extra": """<h2>68-95-99.7 法則</h2>
<p>在常態分佈下，68% 的數據落在平均值 ±1 個標準差內，95% 落在 ±2 個標準差內，99.7% 落在 ±3 個標準差內。例如台股年化報酬率平均 8%、標準差 20%，代表有 68% 的機率年報酬落在 -12% 到 +28% 之間。超過 ±3σ（-52% 到 +68%）的機率只有 0.3%。</p>
<h2>Excel 快速計算</h2>
<p>在 Excel 中，母體標準差用 =STDEV.P()，樣本標準差用 =STDEV.S()。多數情況下應該用樣本標準差（STDEV.S），因為我們通常是從部分資料推估整體。兩者差異在分母：母體用 N，樣本用 N-1。</p>""",
    },
    ("", "ohms-law"): {
        "tables": [
            {"title": "家用電器常見電流/功率",
             "headers": ["電器", "功率 (W)", "電壓 110V 電流", "電壓 220V 電流"],
             "rows": [
                 ["LED 燈泡", "10W", "0.09A", "0.05A"],
                 ["電風扇", "50W", "0.45A", "0.23A"],
                 ["冷氣（1噸）", "900W", "8.18A", "4.09A"],
                 ["微波爐", "1,000W", "9.09A", "4.55A"],
                 ["吹風機", "1,200W", "10.91A", "5.45A"],
                 ["電熱水器", "3,000W", "—", "13.64A"],
                 ["電磁爐", "1,300W", "11.82A", "5.91A"],
             ]},
        ],
        "extra": """<h2>台灣家用電路安全須知</h2>
<p>台灣家用電壓為 110V/220V，一般插座迴路用 20A 無熔絲開關。單一迴路最大負載 = 110V × 20A = 2,200W。如果同一個迴路上接了冷氣（900W）+ 微波爐（1,000W）+ 吹風機（1,200W）= 3,100W，就會超過負載跳電。高功率電器應使用獨立迴路。</p>
<h2>歐姆定律三公式</h2>
<p>V = I × R（電壓 = 電流 × 電阻）、I = V / R（電流 = 電壓 / 電阻）、R = V / I（電阻 = 電壓 / 電流）。加上功率公式 P = V × I，四個公式就能解決所有基礎電路計算。記住一個三角形：上面是 V，下面左邊是 I，右邊是 R，蓋住你要求的值，剩下的就是公式。</p>""",
    },
    ("", "probability-calculator"): {
        "tables": [
            {"title": "日常生活中的機率",
             "headers": ["事件", "機率", "約等於", "備註"],
             "rows": [
                 ["擲硬幣正面", "50%", "1/2", ""],
                 ["擲骰子出6", "16.7%", "1/6", ""],
                 ["同花順（撲克）", "0.0015%", "1/65,000", ""],
                 ["威力彩頭獎", "0.0000054%", "1/1850萬", "6/38 + 1/8"],
                 ["被雷擊", "0.00011%", "1/百萬", "年機率"],
             ]},
        ],
        "extra": """<h2>獨立事件 vs 相依事件</h2>
<p>擲硬幣連續出 10 次正面後，下一次出正面的機率仍然是 50%——這是獨立事件。但從一副牌抽出紅心A後，再抽到紅心的機率從 13/52 變成 12/51——這是相依事件。賭徒謬誤就是把獨立事件誤認為相依事件。</p>
<h2>貝氏定理的直覺理解</h2>
<p>某種疾病盛行率 1%，檢測準確率 95%。你測出陽性，真的有病的機率是多少？答案不是 95%，而是約 16%。因為 99% 沒病的人中有 5% 會誤判為陽性（4.95人），而 1% 有病的人中 95% 會正確判斷（0.95人），所以陽性中真正有病的比例 = 0.95 / (0.95 + 4.95) ≈ 16%。</p>""",
    },
    ("", "gravel-calculator"): {
        "tables": [
            {"title": "碎石種類與用途",
             "headers": ["種類", "粒徑", "密度(噸/㎥)", "常見用途"],
             "rows": [
                 ["細碎石", "5-10mm", "1.5-1.6", "混凝土、鋪面"],
                 ["中碎石", "10-20mm", "1.4-1.5", "排水、車道"],
                 ["粗碎石", "20-40mm", "1.3-1.4", "地基、擋土牆"],
                 ["卵石", "30-50mm", "1.5-1.6", "庭園造景"],
                 ["級配料", "混合", "1.8-2.0", "路基、回填"],
             ]},
        ],
        "extra": """<h2>鋪設厚度建議</h2>
<p>停車場車道建議鋪設 10-15cm，人行步道 5-8cm，排水層 15-20cm。計算時記得加 10% 的損耗。例如 10㎡ 的車道，鋪 10cm 厚：10 × 0.1 × 1.5（密度）× 1.1（損耗）= 1.65 噸碎石。</p>""",
    },
    ("", "ev-charging-cost"): {
        "tables": [
            {"title": "台灣充電費用比較（2026年）",
             "headers": ["充電方式", "費率", "充滿60kWh費用", "備註"],
             "rows": [
                 ["家用（離峰）", "1.85元/度", "111元", "晚上10點後"],
                 ["家用（尖峰）", "5.44元/度", "326元", "夏季午間"],
                 ["Tesla超充", "10-12元/度", "600-720元", "依時段"],
                 ["公共慢充", "5-8元/度", "300-480元", "停車場"],
             ]},
        ],
        "extra": """<h2>電車 vs 油車每月燃料費比較</h2>
<p>以每月行駛 1,500 公里計算：電車（6km/度、家充 2.5元/度）= 625 元/月。油車（12km/L、95汽油 32元/L）= 4,000 元/月。電車每月省 3,375 元，一年省超過 4 萬元。但如果只能用公共快充，費用差距會縮小到每月省 1,500-2,000 元。</p>""",
    },
    ("", "percentage-calculator"): {
        "tables": [
            {"title": "常用百分比速算表",
             "headers": ["計算", "快速方法", "範例"],
             "rows": [
                 ["求10%", "數字去掉一個0", "350的10% = 35"],
                 ["求5%", "先算10%再除以2", "350的5% = 17.5"],
                 ["求25%", "除以4", "350的25% = 87.5"],
                 ["求1%", "小數點左移兩位", "350的1% = 3.5"],
                 ["求15%", "10% + 5%", "350的15% = 52.5"],
                 ["求增減%", "(新-舊)/舊×100", "(420-350)/350 = 20%"],
             ]},
        ],
        "extra": """<h2>百分比的常見誤解</h2>
<p>「漲50%再跌50%」不會回到原價。100元漲50%=150元，150元跌50%=75元，實際虧了25%。反過來也一樣：跌50%後需要漲100%才能回本。這就是為什麼投資中「少虧」比「多賺」更重要。</p>""",
    },

    # ===== en =====
    ("en", "class-rank"): {
        "tables": [
            {"title": "Class Rank Percentile Interpretation",
             "headers": ["Percentile", "Meaning", "College Admissions Impact"],
             "rows": [
                 ["Top 1%", "Valedictorian range", "Ivy League competitive"],
                 ["Top 5%", "Summa Cum Laude", "Top 50 universities"],
                 ["Top 10%", "Magna Cum Laude", "Most selective schools"],
                 ["Top 25%", "Cum Laude", "Competitive state schools"],
                 ["Top 50%", "Above average", "Most state universities"],
             ]},
            {"title": "GPA to Class Rank Conversion (Approximate)",
             "headers": ["GPA (4.0 scale)", "Typical Percentile", "Weighted GPA Equivalent"],
             "rows": [
                 ["4.0", "Top 5-10%", "4.5-5.0"],
                 ["3.7-3.9", "Top 10-20%", "4.2-4.5"],
                 ["3.5-3.6", "Top 20-30%", "4.0-4.2"],
                 ["3.0-3.4", "Top 30-50%", "3.5-4.0"],
                 ["2.5-2.9", "Top 50-70%", "3.0-3.5"],
             ]},
        ],
        "extra": """<h2>How Class Rank Is Calculated</h2>
<p>Most US high schools rank students by cumulative GPA. Some use weighted GPA (AP/Honors courses get extra points), others use unweighted. Your rank is your position among all students in your graduating class. For example, rank 15 out of 400 students means you're in the top 3.75 percentile. Some schools have moved to decile or quintile reporting instead of exact numerical rank.</p>
<h2>Does Class Rank Still Matter?</h2>
<p>About 50% of US colleges still consider class rank in admissions. It matters most for public universities with automatic admission policies — for example, Texas guarantees admission to the top 6% of each high school class. For private universities, GPA, test scores, and extracurriculars carry more weight. If your school doesn't rank, colleges will evaluate your GPA in the context of your school's course offerings and grade distribution.</p>
<h2>Strategies to Improve Your Rank</h2>
<p>Take AP and Honors courses if your school uses weighted GPA — an A in AP Chemistry (5.0) boosts your weighted GPA more than an A in regular Chemistry (4.0). However, a B in AP (4.0 weighted) equals an A in regular (4.0), so only take AP courses you can realistically earn an A in. Focus on consistent performance across all subjects rather than excelling in just one area.</p>""",
    },
    ("en", "parking-cost"): {
        "tables": [
            {"title": "Average Monthly Parking Costs by US City (2026)",
             "headers": ["City", "Monthly Rate", "Daily Max", "Airport Long-Term/Day"],
             "rows": [
                 ["New York (Manhattan)", "$500-800", "$40-65", "$18-39"],
                 ["San Francisco", "$300-500", "$30-50", "$18-36"],
                 ["Chicago", "$200-350", "$25-40", "$10-17"],
                 ["Los Angeles", "$150-300", "$15-30", "$12-30"],
                 ["Houston", "$100-200", "$10-20", "$7-12"],
                 ["Phoenix", "$80-150", "$8-15", "$5-10"],
             ]},
        ],
        "extra": """<h2>Hidden Parking Costs to Consider</h2>
<p>Monthly parking isn't just the sticker price. Many garages charge extra for SUVs or oversized vehicles ($50-100/month premium). Event surcharges can double daily rates near stadiums and arenas. Airport parking alternatives like off-site lots with shuttle service typically save 30-50% compared to on-airport garages. Ride-share costs both ways may be cheaper than airport parking for trips under 5 days.</p>
<h2>Commuter Parking Tax Benefits</h2>
<p>US employers can offer pre-tax parking benefits up to $315/month (2026 limit) through qualified transportation fringe benefits. This saves you 22-37% depending on your tax bracket. If your employer doesn't offer this benefit, ask HR — it costs the company nothing and saves you $800-1,400 per year in taxes.</p>""",
    },
    ("en", "retirement-age"): {
        "tables": [
            {"title": "Social Security Full Retirement Age by Birth Year",
             "headers": ["Birth Year", "Full Retirement Age", "Early (Age 62) Reduction", "Delayed (Age 70) Increase"],
             "rows": [
                 ["1955", "66 + 2 months", "-25.83%", "+29.33%"],
                 ["1956", "66 + 4 months", "-26.67%", "+28.67%"],
                 ["1957", "66 + 6 months", "-27.5%", "+28%"],
                 ["1958", "66 + 8 months", "-28.33%", "+27.33%"],
                 ["1959", "66 + 10 months", "-29.17%", "+26.67%"],
                 ["1960+", "67", "-30%", "+24%"],
             ]},
        ],
        "extra": """<h2>Early vs. Delayed Retirement: The Break-Even Point</h2>
<p>If your full retirement age benefit is $2,000/month, claiming at 62 gives you $1,400/month (30% reduction), while waiting until 70 gives you $2,480/month (24% increase). The break-even point between claiming at 62 vs. 67 is around age 78-80. If you expect to live past 80, delaying benefits is financially advantageous. If you have health concerns or need income immediately, claiming early makes more sense.</p>
<h2>The 4% Rule for Retirement Savings</h2>
<p>A common retirement guideline: you need 25 times your annual expenses saved. If you spend $50,000/year, you need $1.25 million. This assumes withdrawing 4% annually, adjusted for inflation, with a high probability of lasting 30+ years. However, recent research suggests 3.3-3.5% may be safer given current market conditions and longer life expectancies.</p>""",
    },

    # ===== id (Indonesian) =====
    ("id", "typing-speed"): {
        "tables": [
            {"title": "Standar Kecepatan Mengetik",
             "headers": ["Level", "WPM", "Keterangan", "Cocok Untuk"],
             "rows": [
                 ["Pemula", "10-25", "Masih lihat keyboard", "Pelajar"],
                 ["Menengah", "25-40", "Touch typing dasar", "Pekerja kantor"],
                 ["Cepat", "40-60", "Lancar tanpa lihat", "Admin, sekretaris"],
                 ["Profesional", "60-80", "Sangat cepat", "Programmer, penulis"],
                 ["Expert", "80-120+", "Kompetisi level", "Transcriptionist"],
             ]},
        ],
        "extra": """<h2>Tips Meningkatkan Kecepatan Mengetik</h2>
<p>Gunakan teknik touch typing — letakkan jari telunjuk kiri di huruf F dan jari telunjuk kanan di huruf J (ada tonjolan kecil sebagai penanda). Latihan 15 menit setiap hari lebih efektif daripada 2 jam seminggu sekali. Aplikasi gratis seperti TypingClub atau Keybr bisa membantu meningkatkan kecepatan dari 25 WPM ke 50 WPM dalam 2-4 minggu latihan rutin.</p>
<h2>Kecepatan Mengetik dan Produktivitas Kerja</h2>
<p>Rata-rata pekerja kantor mengetik sekitar 8,000 kata per hari. Dengan kecepatan 30 WPM, ini membutuhkan sekitar 4.4 jam mengetik murni. Meningkatkan ke 60 WPM memangkas waktu jadi 2.2 jam — menghemat lebih dari 2 jam setiap hari kerja untuk tugas lain yang lebih produktif.</p>""",
    },
    ("id", "future-value"): {
        "tables": [
            {"title": "Simulasi Investasi Bulanan Rp 1 Juta",
             "headers": ["Periode", "Return 7%/thn", "Return 10%/thn", "Return 15%/thn"],
             "rows": [
                 ["5 tahun", "Rp 71,6 juta", "Rp 77,4 juta", "Rp 87,1 juta"],
                 ["10 tahun", "Rp 173,1 juta", "Rp 204,8 juta", "Rp 274,6 juta"],
                 ["20 tahun", "Rp 520,9 juta", "Rp 764,9 juta", "Rp 1,49 miliar"],
                 ["30 tahun", "Rp 1,22 miliar", "Rp 2,26 miliar", "Rp 7,00 miliar"],
             ]},
        ],
        "extra": """<h2>Investasi di Indonesia: Pilihan Umum</h2>
<p>Deposito bank besar di Indonesia memberikan bunga sekitar 4-5% per tahun. Reksa dana pasar uang sekitar 5-6%. Reksa dana saham bisa memberikan 10-15% per tahun dalam jangka panjang, tetapi dengan volatilitas tinggi. SBN (Surat Berharga Negara) menawarkan 6-7% dengan risiko sangat rendah karena dijamin pemerintah. Untuk pemula, SBN dan reksa dana pasar uang adalah pilihan paling aman untuk memulai.</p>
<h2>Efek Compound Interest (Bunga Berbunga)</h2>
<p>Albert Einstein menyebutnya "keajaiban dunia ke-8". Rp 1 juta per bulan selama 30 tahun dengan return 10%/tahun menghasilkan Rp 2,26 miliar — padahal total setoran Anda hanya Rp 360 juta. Sisanya Rp 1,9 miliar berasal dari bunga berbunga. Semakin cepat mulai, semakin besar efeknya.</p>""",
    },
    ("id", "reading-time"): {
        "tables": [
            {"title": "Kecepatan Membaca Rata-Rata",
             "headers": ["Tipe Pembaca", "Kata/Menit", "Halaman/Jam", "Keterangan"],
             "rows": [
                 ["Lambat", "100-150", "5-7", "Membaca detail"],
                 ["Rata-rata", "200-250", "10-12", "Pembaca umum"],
                 ["Cepat", "300-400", "15-20", "Pembaca terlatih"],
                 ["Speed Reader", "500-700", "25-35", "Teknik khusus"],
             ]},
        ],
        "extra": """<h2>Tips Membaca Lebih Cepat</h2>
<p>Hindari subvokalisasi (membaca dalam hati). Gunakan jari atau pena sebagai pemandu mata. Perluas jangkauan mata — latih untuk menangkap 3-4 kata sekaligus, bukan satu per satu. Dengan latihan konsisten 20 menit/hari, kebanyakan orang bisa meningkatkan kecepatan baca 50-100% dalam sebulan tanpa mengorbankan pemahaman.</p>""",
    },
    ("id", "forex-profit"): {
        "tables": [
            {"title": "Pasangan Mata Uang Populer di Indonesia",
             "headers": ["Pair", "Spread Rata-rata", "Volatilitas Harian", "Sesi Aktif"],
             "rows": [
                 ["EUR/USD", "0.6-1.0 pip", "70-100 pip", "London, New York"],
                 ["USD/JPY", "0.7-1.2 pip", "60-90 pip", "Tokyo, New York"],
                 ["GBP/USD", "1.0-1.5 pip", "100-150 pip", "London"],
                 ["USD/IDR", "30-100 pip", "50-200 pip", "Jakarta"],
                 ["XAU/USD (Emas)", "2-4 pip", "150-300 pip", "London, New York"],
             ]},
        ],
        "extra": """<h2>Regulasi Forex di Indonesia</h2>
<p>Trading forex di Indonesia diawasi oleh Bappebti (Badan Pengawas Perdagangan Berjangka Komoditi). Pastikan broker Anda terdaftar di Bappebti — daftar resmi bisa dicek di bappebti.go.id. Broker ilegal tidak menjamin keamanan dana Anda. Leverage yang diizinkan di Indonesia hingga 1:100 untuk forex dan 1:50 untuk emas.</p>
<h2>Manajemen Risiko</h2>
<p>Aturan umum: jangan risiko lebih dari 1-2% modal per trade. Jika modal Anda Rp 10 juta, maksimal kerugian per trade adalah Rp 100.000-200.000. Gunakan stop loss di setiap posisi — tanpa stop loss, satu trade buruk bisa menghapus seluruh profit dari 10 trade sebelumnya.</p>""",
    },

    # ===== ja (Japanese) =====
    ("ja", "room-area"): {
        "tables": [
            {"title": "日本の部屋サイズ一覧（不動産表記）",
             "headers": ["表記", "面積（㎡）", "面積（坪）", "用途目安"],
             "rows": [
                 ["4.5畳", "7.29㎡", "2.2坪", "子供部屋"],
                 ["6畳", "9.72㎡", "2.9坪", "寝室（一人）"],
                 ["8畳", "12.96㎡", "3.9坪", "寝室（二人）"],
                 ["10畳", "16.2㎡", "4.9坪", "リビング（小）"],
                 ["12畳", "19.44㎡", "5.9坪", "リビング（中）"],
                 ["20畳", "32.4㎡", "9.8坪", "LDK"],
             ]},
        ],
        "extra": """<h2>畳・坪・㎡の換算方法</h2>
<p>1畳 = 1.62㎡（中京間基準、不動産広告の標準）。1坪 = 3.31㎡ = 約2畳。マンションの専有面積は壁芯計算（壁の中心線で測定）のため、実際の室内面積は5〜8%小さくなります。内法計算（壁の内側）の面積は登記簿で確認できます。</p>
<h2>家具配置に必要な面積</h2>
<p>ダブルベッドには約3畳、ダイニングテーブル（4人用）には約2畳、ソファ＋テレビには約4〜5畳のスペースが必要です。6畳の寝室にダブルベッドを置くと、残りスペースは約3畳。クローゼットを考慮すると、実質的な動線スペースは2畳程度になります。</p>""",
    },
    ("ja", "cooking-weight-volume"): {
        "tables": [
            {"title": "調味料の重量換算表（日本の計量スプーン基準）",
             "headers": ["調味料", "小さじ1 (5ml)", "大さじ1 (15ml)", "1カップ (200ml)"],
             "rows": [
                 ["砂糖（上白糖）", "3g", "9g", "130g"],
                 ["塩", "6g", "18g", "240g"],
                 ["醤油", "6g", "18g", "230g"],
                 ["味噌", "6g", "18g", "230g"],
                 ["みりん", "6g", "18g", "230g"],
                 ["酢", "5g", "15g", "200g"],
                 ["小麦粉（薄力粉）", "3g", "9g", "110g"],
                 ["バター", "4g", "12g", "180g"],
             ]},
        ],
        "extra": """<h2>日本とアメリカの計量の違い</h2>
<p>日本の1カップは200ml、アメリカの1カップは約237ml（8 fl oz）です。海外レシピを日本の計量カップで作ると約16%少なくなるため、注意が必要です。また、日本のレシピで「cc」と書かれている場合、1cc = 1ml として計算して問題ありません。</p>""",
    },
    ("ja", "salary-to-hourly"): {
        "tables": [
            {"title": "日本の月給→時給換算の目安",
             "headers": ["月給（総支給）", "時給換算", "年収", "備考"],
             "rows": [
                 ["20万円", "約1,190円", "240万円", "最低賃金付近"],
                 ["25万円", "約1,488円", "300万円", "新卒平均"],
                 ["30万円", "約1,786円", "360万円", "20代後半"],
                 ["35万円", "約2,083円", "420万円", "30代平均"],
                 ["40万円", "約2,381円", "480万円", "管理職手前"],
                 ["50万円", "約2,976円", "600万円", "管理職"],
             ]},
        ],
        "extra": """<h2>計算方法：月給÷（1日8時間×月21日）</h2>
<p>一般的な計算式は、月給 ÷ 168時間（8時間 × 21営業日）です。ただし、残業代の計算基礎となる「所定労働時間」は会社によって異なります（160〜176時間が一般的）。残業代の時給は通常の1.25倍、深夜（22時〜5時）は1.5倍、休日出勤は1.35倍です。</p>
<h2>パートタイムの時給相場（2026年）</h2>
<p>全国最低賃金は1,113円（2026年見込み）。都道府県別では東京が最も高く1,163円前後、最も低い地域でも1,050円を超えています。コンビニバイトは最低賃金〜最低賃金+50円程度、飲食店は+100〜200円、IT系アルバイトは1,500〜2,500円が相場です。</p>""",
    },
    ("ja", "insulation-calculator"): {
        "tables": [
            {"title": "日本の住宅断熱基準（省エネ等級）",
             "headers": ["等級", "UA値目安", "対象地域", "断熱材厚さ目安"],
             "rows": [
                 ["等級4（H28基準）", "0.87以下", "東京（6地域）", "壁75mm・天井155mm"],
                 ["等級5（ZEH基準）", "0.60以下", "東京（6地域）", "壁100mm・天井200mm"],
                 ["等級6", "0.46以下", "東京（6地域）", "壁120mm・天井250mm"],
                 ["等級7（最高）", "0.26以下", "東京（6地域）", "壁200mm・天井350mm"],
             ]},
        ],
        "extra": """<h2>断熱リフォームの費用対効果</h2>
<p>築30年以上の住宅は断熱等級2〜3程度の場合が多く、冷暖房費が年間15〜25万円かかります。等級5相当にリフォームすると冷暖房費が30〜40%削減でき、年間5〜10万円の節約になります。内窓（二重窓）の追加は1箇所5〜10万円で、最もコスパの良い断熱リフォームです。</p>""",
    },

    # ===== es (Spanish) =====
    ("es", "parking-cost"): {
        "tables": [
            {"title": "Coste Medio de Aparcamiento en Ciudades Españolas (2026)",
             "headers": ["Ciudad", "Precio/Hora (Centro)", "Abono Mensual", "Aeropuerto/Día"],
             "rows": [
                 ["Madrid", "2,50-3,90€", "150-250€", "10-18€"],
                 ["Barcelona", "2,80-4,20€", "160-280€", "12-20€"],
                 ["Valencia", "1,80-2,50€", "100-160€", "8-12€"],
                 ["Sevilla", "1,50-2,20€", "80-140€", "6-10€"],
                 ["Bilbao", "2,00-3,00€", "120-200€", "9-15€"],
             ]},
        ],
        "extra": """<h2>Zonas de Estacionamiento Regulado (SER/ORA)</h2>
<p>Las principales ciudades españolas utilizan zonas de estacionamiento regulado con colores: zona azul (residentes y rotación, 1-2h máximo), zona verde (residentes prioritarios) y zona naranja (alta rotación, 30min-1h). Las multas por exceso de tiempo oscilan entre 45-90€, reduciéndose un 50% si se pagan antes de 20 días.</p>
<h2>Alternativas para Ahorrar</h2>
<p>Aparcar en estaciones de Metro periféricas (Park & Ride) suele costar 2-5€/día. Aplicaciones como Telpark o EasyPark ofrecen descuentos del 10-15% en parkings concertados. Algunos centros comerciales ofrecen hasta 3 horas gratuitas con compra mínima.</p>""",
    },
    ("es", "customs-duty"): {
        "tables": [
            {"title": "Aranceles de Importación en España/UE (2026)",
             "headers": ["Categoría", "Arancel", "IVA", "Límite Exención"],
             "rows": [
                 ["Electrónica", "0-6%", "21%", "—"],
                 ["Ropa y textiles", "8-12%", "21%", "—"],
                 ["Calzado", "8-17%", "21%", "—"],
                 ["Alimentos", "0-20%", "10% (reducido)", "Controles sanitarios"],
                 ["Paquetes < 150€", "Exento", "21%", "Sin arancel"],
             ]},
        ],
        "extra": """<h2>Importar desde China: Lo que Debes Saber</h2>
<p>Desde julio 2021, la UE eliminó la exención de IVA para envíos menores de 22€. Ahora todos los paquetes pagan IVA del 21%. Los envíos superiores a 150€ además pagan aranceles. Plataformas como AliExpress y Shein cobran el IVA en el momento de la compra a través del sistema IOSS, por lo que no deberías recibir cargos adicionales en la entrega. Si compras directamente a un proveedor chino sin IOSS, Correos te cobrará el IVA + una tasa de gestión de 3-5€.</p>""",
    },
    ("es", "paint-calculator"): {
        "tables": [
            {"title": "Rendimiento por Tipo de Pintura",
             "headers": ["Tipo", "Rendimiento (㎡/litro)", "Manos", "Uso Recomendado"],
             "rows": [
                 ["Plástica mate", "10-12", "2", "Techos, zonas secas"],
                 ["Plástica satinada", "10-12", "2", "Salones, dormitorios"],
                 ["Esmalte al agua", "10-12", "2-3", "Cocinas, baños"],
                 ["Esmalte sintético", "12-14", "2", "Puertas, rejas metálicas"],
                 ["Imprimación", "8-10", "1", "Paredes nuevas, cambio de color"],
             ]},
        ],
        "extra": """<h2>Cómo Calcular la Pintura Necesaria</h2>
<p>Mide el perímetro de la habitación × la altura = superficie total de paredes. Resta ventanas (~1,5㎡ cada una) y puertas (~1,8㎡ cada una). Multiplica por 2 (dos manos) y divide por el rendimiento del bote (normalmente 10-12 ㎡/litro). Añade un 10% de margen. Por ejemplo: habitación de 4×3m, altura 2,5m = 35㎡ de pared − 3㎡ (ventana+puerta) = 32㎡. Con 2 manos = 64㎡ ÷ 11 ㎡/L = 5,8 litros → compra un bote de 4L + uno de 2,5L.</p>""",
    },

    # ===== ko (Korean) =====
    ("ko", "paper-weight"): {
        "tables": [
            {"title": "용지 종류별 무게 비교",
             "headers": ["용지 종류", "평량(g/㎡)", "A4 1장 무게", "500매 무게"],
             "rows": [
                 ["일반 복사지", "75-80g", "4.7-5.0g", "2.3-2.5kg"],
                 ["고급 복사지", "100g", "6.2g", "3.1kg"],
                 ["전단지용", "120g", "7.5g", "3.7kg"],
                 ["명함용", "200g", "12.5g", "6.2kg"],
                 ["포스터용", "150g", "9.3g", "4.7kg"],
             ]},
        ],
        "extra": """<h2>우편 발송 시 무게 계산</h2>
<p>우체국 일반우편은 25g까지 기본요금 440원, 50g까지 470원입니다. A4 복사지(80g) 1장이 약 5g이므로, 봉투(5g) 포함 시 4장까지가 25g 이내입니다. 대량 발송 시 용지 평량을 75g으로 낮추면 5장까지 기본요금으로 보낼 수 있어 비용을 절약할 수 있습니다.</p>""",
    },

    # ===== zh-CN (Simplified Chinese) =====
    ("zh-CN", "atr-calculator"): {
        "tables": [
            {"title": "ATR 数值与交易策略",
             "headers": ["ATR 水平", "含义", "止损设置建议", "适合策略"],
             "rows": [
                 ["低 ATR", "波动小，盘整期", "1.5-2 倍 ATR", "区间交易"],
                 ["中 ATR", "正常波动", "2-2.5 倍 ATR", "趋势跟踪"],
                 ["高 ATR", "波动剧烈", "2.5-3 倍 ATR", "突破交易"],
                 ["ATR 急升", "可能变盘", "扩大止损或观望", "谨慎操作"],
             ]},
        ],
        "extra": """<h2>ATR 止损法（海龟交易法则）</h2>
<p>经典的海龟交易法则使用 2 倍 ATR 作为止损距离。例如，某股票价格 50 元，14 日 ATR 为 2 元，则止损设在 50 - 2×2 = 46 元。ATR 会随市场波动自动调整，比固定百分比止损更加灵活。当 ATR 扩大时，止损自动放宽；当 ATR 缩小时，止损自动收紧。</p>
<h2>ATR 与仓位管理</h2>
<p>用 ATR 计算仓位大小：单笔风险金额 ÷ (N 倍 ATR × 每手数量) = 买入手数。假设账户 10 万元，单笔风险 1%（1000 元），ATR = 2 元，2 倍 ATR 止损 = 4 元，则买入数量 = 1000 ÷ 4 = 250 股。这种方法确保不同波动率的股票承担相同的风险金额。</p>""",
    },
    ("zh-CN", "paper-weight"): {
        "tables": [
            {"title": "常见纸张克重与用途",
             "headers": ["纸张类型", "克重(g/㎡)", "A4 单张重量", "用途"],
             "rows": [
                 ["打印纸", "70-80g", "4.4-5.0g", "日常打印复印"],
                 ["铜版纸", "128-157g", "8.0-9.8g", "宣传册、画册"],
                 ["卡纸", "200-300g", "12.5-18.7g", "名片、贺卡"],
                 ["牛皮纸", "80-120g", "5.0-7.5g", "包装、信封"],
                 ["新闻纸", "45-52g", "2.8-3.2g", "报纸、书籍"],
             ]},
        ],
        "extra": """<h2>快递重量与运费计算</h2>
<p>国内快递首重一般为 1kg，续重每 0.5-1kg 加收费用。以顺丰标快为例，首重 12-23 元（按距离），续重 2-14 元/kg。寄送文件时，A4 打印纸(80g) 100 张约 500g，加上档案袋约 50g，总重约 550g，刚好超过首重。选用 70g 纸张可将总重控制在 500g 以内，节省续重费用。</p>""",
    },
}


def build_table_html(table_data):
    html = f'<h3>{table_data["title"]}</h3>\n<table>\n<tr>'
    for h in table_data["headers"]:
        html += f'<th>{h}</th>'
    html += '</tr>\n'
    for row in table_data["rows"]:
        html += '<tr>'
        for cell in row:
            html += f'<td>{cell}</td>'
        html += '</tr>\n'
    html += '</table>'
    return html


def thicken_page(filepath, slug, data):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    articles = list(re.finditer(r'</article>', content))
    if not articles:
        print(f"  ❌ {slug}: no </article> tag found")
        return False

    insert_pos = articles[-1].start()
    new_html = "\n"
    for table_data in data.get("tables", []):
        new_html += build_table_html(table_data) + "\n"
    if data.get("extra"):
        new_html += data["extra"] + "\n"

    content = content[:insert_pos] + new_html + content[insert_pos:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    text = re.sub(r'<[^>]*>', '', content)
    text = text.replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
    print(f"  ✅ {slug}: thickened ({len(text)} chars)")
    return True


def main():
    success = 0
    fail = 0
    for (lang, slug), data in PAGES.items():
        if lang == "":
            filepath = os.path.join(BASE, f"{slug}.html")
        else:
            filepath = os.path.join(BASE, lang, f"{slug}.html")

        if os.path.exists(filepath):
            if thicken_page(filepath, f"{lang or 'zh-TW'}/{slug}", data):
                success += 1
            else:
                fail += 1
        else:
            print(f"  ❌ {lang or 'zh-TW'}/{slug}: file not found at {filepath}")
            fail += 1

    print(f"\n完成: {success} 成功, {fail} 失敗")


if __name__ == "__main__":
    main()
