# -*- coding: utf-8 -*-
"""
i18n_data.py
補齊 ja/ko/fr/de/es/pt/id 七種語言的 FAQ 題目模板 + 稅務/領獎資訊在地化翻譯。
原本 enrich_lottery_pages.py / enrich_lottery_v2.py 的 gen_faq() 只有 zh / else(英文) 兩個分支，
這份資料表補上真正的 7 語言在地化內容。
"""

# ============================================================
# 每種彩票的 tax / claim 各語言翻譯
# 英文原文（供對照，來自 enrich_lottery_v2.py 的 LOTTERIES 字典）：
#   powerball:      tax="37% federal + state tax"  claim="Winners have 180 days to 1 year depending on state. Jackpots can be taken as annuity (30 years) or lump sum (approx. 60% of advertised amount)."
#   mega-millions:  tax="37% federal + state tax"  claim="Winners have 180 days to 1 year depending on state."
#   euromillions:   tax="Varies by country. UK, France, Germany: tax-free. Spain: 20% over €40,000."  claim="Winners typically have 90 days to 1 year depending on country."
#   lotto-max:      tax="Tax-free in Canada."  claim="Winners have 1 year from the draw date."
#   uk-lotto:       tax="Tax-free in the UK."  claim="Winners have 180 days."
#   el-gordo:       tax="20% on amounts over €40,000."  claim="Winners have 3 months."
#   superenalotto:  tax="20% on amounts over €500."  claim="Winners have 90 days."
#   lotto-6aus49:   tax="Tax-free in Germany."  claim="Winners have 13 weeks."
#   oz-lotto:       tax="Tax-free in Australia."  claim="Winners typically have 6 years (varies by state)."
#   taiwan-bingo:   tax="10% (NT$5,001-20M), 20% (over NT$20M)"  claim="Winners have 3 months. Prizes are paid in full."
#   taiwan-lotto:   tax="10% (NT$5,001-20M), 20% (over NT$20M)"  claim="Winners have 3 months."
#   daily-cash:     tax="10% (NT$5,001-20M), 20% (over NT$20M)"  claim="Fixed first prize NT$8 million. Winners have 3 months."
#   mega-sena:      tax="30% on amounts over R$1,903.98."  claim="Winners have 90 days."
#   korea-lotto:    tax="22% on amounts over ₩50 million."  claim="Winners have 1 year."
#   japan-loto6:    tax="20.315% on all winnings."  claim="Winners have 1 year."
# ============================================================

TAX_CLAIM_I18N = {
"powerball": {
  "ja":{"tax":"連邦税37%＋州税が課されます。","claim":"当選者は州によって180日〜1年以内に請求が必要です。ジャックポットは年金方式（30年分割）または一時金（表示額の約60%）を選択できます。"},
  "ko":{"tax":"연방세 37% + 주세가 부과됩니다。","claim":"주(州)에 따라 당첨금 청구 기한은 180일~1년입니다. 잭팟은 연금 방식(30년 분할) 또는 일시불(공시 금액의 약 60%) 중 선택할 수 있습니다."},
  "fr":{"tax":"Impôt fédéral de 37 % + impôt d'État.","claim":"Les gagnants disposent de 180 jours à 1 an selon l'État. Le jackpot peut être perçu sous forme de rente (30 ans) ou de capital unique (environ 60 % du montant annoncé)."},
  "de":{"tax":"37 % Bundessteuer + Landessteuer.","claim":"Gewinner haben je nach Bundesstaat 180 Tage bis 1 Jahr Zeit. Der Jackpot kann als Rente (30 Jahre) oder als Einmalzahlung (ca. 60 % des ausgewiesenen Betrags) ausgezahlt werden."},
  "es":{"tax":"37% de impuesto federal + impuesto estatal.","claim":"Los ganadores tienen entre 180 días y 1 año, según el estado. El premio mayor puede cobrarse como anualidad (30 años) o en pago único (aprox. 60% del monto anunciado)."},
  "pt":{"tax":"37% de imposto federal + imposto estadual.","claim":"Os ganhadores têm de 180 dias a 1 ano, dependendo do estado. O prêmio pode ser recebido como anuidade (30 anos) ou pagamento único (aprox. 60% do valor anunciado)."},
  "id":{"tax":"Pajak federal 37% + pajak negara bagian.","claim":"Pemenang memiliki waktu 180 hari hingga 1 tahun tergantung negara bagian. Jackpot dapat diambil sebagai anuitas (30 tahun) atau sekaligus (sekitar 60% dari jumlah yang diumumkan)."},
},
"mega-millions": {
  "ja":{"tax":"連邦税37%＋州税が課されます。","claim":"州によって異なりますが、当選者は180日〜1年以内に請求が必要です。"},
  "ko":{"tax":"연방세 37% + 주세가 부과됩니다。","claim":"주에 따라 당첨금 청구 기한은 180일~1년입니다."},
  "fr":{"tax":"Impôt fédéral de 37 % + impôt d'État.","claim":"Les gagnants disposent de 180 jours à 1 an selon l'État."},
  "de":{"tax":"37 % Bundessteuer + Landessteuer.","claim":"Gewinner haben je nach Bundesstaat 180 Tage bis 1 Jahr Zeit."},
  "es":{"tax":"37% de impuesto federal + impuesto estatal.","claim":"Los ganadores tienen entre 180 días y 1 año, según el estado."},
  "pt":{"tax":"37% de imposto federal + imposto estadual.","claim":"Os ganhadores têm de 180 dias a 1 ano, dependendo do estado."},
  "id":{"tax":"Pajak federal 37% + pajak negara bagian.","claim":"Pemenang memiliki waktu 180 hari hingga 1 tahun tergantung negara bagian."},
},
"euromillions": {
  "ja":{"tax":"国によって異なります。英国・フランス・ドイツは非課税。スペインは4万ユーロ超の部分に20%課税。","claim":"国により異なりますが、通常90日〜1年以内に請求が必要です。"},
  "ko":{"tax":"국가별로 다릅니다. 영국·프랑스·독일은 비과세. 스페인은 4만 유로 초과분에 20% 과세。","claim":"국가에 따라 다르지만 보통 90일~1년 이내에 청구해야 합니다."},
  "fr":{"tax":"Varie selon le pays. Royaume-Uni, France, Allemagne : exonéré d'impôt. Espagne : 20 % au-delà de 40 000 €.","claim":"Les gagnants disposent généralement de 90 jours à 1 an selon le pays."},
  "de":{"tax":"Abhängig vom Land. Großbritannien, Frankreich, Deutschland: steuerfrei. Spanien: 20 % auf Beträge über 40.000 €.","claim":"Gewinner haben je nach Land in der Regel 90 Tage bis 1 Jahr Zeit."},
  "es":{"tax":"Varía según el país. Reino Unido, Francia, Alemania: libre de impuestos. España: 20% sobre importes superiores a 40.000 €.","claim":"Los ganadores suelen tener entre 90 días y 1 año, según el país."},
  "pt":{"tax":"Varia por país. Reino Unido, França, Alemanha: isento de impostos. Espanha: 20% sobre valores acima de €40.000.","claim":"Os ganhadores geralmente têm de 90 dias a 1 ano, dependendo do país."},
  "id":{"tax":"Bervariasi menurut negara. Inggris, Prancis, Jerman: bebas pajak. Spanyol: 20% untuk jumlah di atas €40.000.","claim":"Pemenang biasanya memiliki waktu 90 hari hingga 1 tahun tergantung negara."},
},
"lotto-max": {
  "ja":{"tax":"カナダでは非課税です。","claim":"抽選日から1年以内に請求が必要です。"},
  "ko":{"tax":"캐나다에서는 비과세입니다。","claim":"추첨일로부터 1년 이내에 청구해야 합니다."},
  "fr":{"tax":"Exonéré d'impôt au Canada.","claim":"Les gagnants ont 1 an à compter de la date du tirage."},
  "de":{"tax":"In Kanada steuerfrei.","claim":"Gewinner haben 1 Jahr ab dem Ziehungsdatum Zeit."},
  "es":{"tax":"Libre de impuestos en Canadá.","claim":"Los ganadores tienen 1 año a partir de la fecha del sorteo."},
  "pt":{"tax":"Isento de impostos no Canadá.","claim":"Os ganhadores têm 1 ano a partir da data do sorteio."},
  "id":{"tax":"Bebas pajak di Kanada.","claim":"Pemenang memiliki waktu 1 tahun sejak tanggal undian."},
},
"uk-lotto": {
  "ja":{"tax":"英国では非課税です。","claim":"当選者は180日以内に請求が必要です。"},
  "ko":{"tax":"영국에서는 비과세입니다。","claim":"당첨자는 180일 이내에 청구해야 합니다."},
  "fr":{"tax":"Exonéré d'impôt au Royaume-Uni.","claim":"Les gagnants disposent de 180 jours."},
  "de":{"tax":"Im Vereinigten Königreich steuerfrei.","claim":"Gewinner haben 180 Tage Zeit."},
  "es":{"tax":"Libre de impuestos en el Reino Unido.","claim":"Los ganadores tienen 180 días."},
  "pt":{"tax":"Isento de impostos no Reino Unido.","claim":"Os ganhadores têm 180 dias."},
  "id":{"tax":"Bebas pajak di Inggris.","claim":"Pemenang memiliki waktu 180 hari."},
},
"el-gordo": {
  "ja":{"tax":"4万ユーロを超える部分に20%課税されます。","claim":"当選者は3ヶ月以内に請求が必要です。"},
  "ko":{"tax":"4만 유로 초과분에 20% 과세됩니다。","claim":"당첨자는 3개월 이내에 청구해야 합니다."},
  "fr":{"tax":"20 % sur les montants dépassant 40 000 €.","claim":"Les gagnants disposent de 3 mois."},
  "de":{"tax":"20 % auf Beträge über 40.000 €.","claim":"Gewinner haben 3 Monate Zeit."},
  "es":{"tax":"20% sobre los importes que superen los 40.000 €.","claim":"Los ganadores tienen 3 meses."},
  "pt":{"tax":"20% sobre valores acima de €40.000.","claim":"Os ganhadores têm 3 meses."},
  "id":{"tax":"Pajak 20% untuk jumlah di atas €40.000.","claim":"Pemenang memiliki waktu 3 bulan."},
},
"superenalotto": {
  "ja":{"tax":"500ユーロを超える部分に20%課税されます。","claim":"当選者は90日以内に請求が必要です。"},
  "ko":{"tax":"500 유로 초과분에 20% 과세됩니다。","claim":"당첨자는 90일 이내에 청구해야 합니다."},
  "fr":{"tax":"20 % sur les montants dépassant 500 €.","claim":"Les gagnants disposent de 90 jours."},
  "de":{"tax":"20 % auf Beträge über 500 €.","claim":"Gewinner haben 90 Tage Zeit."},
  "es":{"tax":"20% sobre los importes que superen los 500 €.","claim":"Los ganadores tienen 90 días."},
  "pt":{"tax":"20% sobre valores acima de €500.","claim":"Os ganhadores têm 90 dias."},
  "id":{"tax":"Pajak 20% untuk jumlah di atas €500.","claim":"Pemenang memiliki waktu 90 hari."},
},
"lotto-6aus49": {
  "ja":{"tax":"ドイツでは非課税です。","claim":"当選者は13週間以内に請求が必要です。"},
  "ko":{"tax":"독일에서는 비과세입니다。","claim":"당첨자는 13주 이내에 청구해야 합니다."},
  "fr":{"tax":"Exonéré d'impôt en Allemagne.","claim":"Les gagnants disposent de 13 semaines."},
  "de":{"tax":"In Deutschland steuerfrei.","claim":"Gewinner haben 13 Wochen Zeit."},
  "es":{"tax":"Libre de impuestos en Alemania.","claim":"Los ganadores tienen 13 semanas."},
  "pt":{"tax":"Isento de impostos na Alemanha.","claim":"Os ganhadores têm 13 semanas."},
  "id":{"tax":"Bebas pajak di Jerman.","claim":"Pemenang memiliki waktu 13 minggu."},
},
"oz-lotto": {
  "ja":{"tax":"オーストラリアでは非課税です。","claim":"当選者は通常6年以内（州により異なる）に請求が必要です。"},
  "ko":{"tax":"호주에서는 비과세입니다。","claim":"당첨자는 보통 6년 이내(주마다 다름)에 청구해야 합니다."},
  "fr":{"tax":"Exonéré d'impôt en Australie.","claim":"Les gagnants ont généralement 6 ans (selon l'État)."},
  "de":{"tax":"In Australien steuerfrei.","claim":"Gewinner haben in der Regel 6 Jahre Zeit (je nach Bundesstaat)."},
  "es":{"tax":"Libre de impuestos en Australia.","claim":"Los ganadores suelen tener 6 años (varía según el estado)."},
  "pt":{"tax":"Isento de impostos na Austrália.","claim":"Os ganhadores geralmente têm 6 anos (varia por estado)."},
  "id":{"tax":"Bebas pajak di Australia.","claim":"Pemenang biasanya memiliki waktu 6 tahun (bervariasi menurut negara bagian)."},
},
"taiwan-bingo": {
  "ja":{"tax":"10%（500万〜2,000万台湾ドル）、20%（2,000万台湾ドル超）。","claim":"当選者は3ヶ月以内に請求が必要です。賞金は全額支払われます。"},
  "ko":{"tax":"10%(NT$5,001~2,000만), 20%(NT$2,000만 초과)。","claim":"당첨자는 3개월 이내에 청구해야 하며, 상금은 전액 지급됩니다."},
  "fr":{"tax":"10 % (5 001 à 20 M NT$), 20 % (au-delà de 20 M NT$).","claim":"Les gagnants disposent de 3 mois. Les gains sont versés intégralement."},
  "de":{"tax":"10 % (5.001–20 Mio. NT$), 20 % (über 20 Mio. NT$).","claim":"Gewinner haben 3 Monate Zeit. Die Gewinne werden vollständig ausgezahlt."},
  "es":{"tax":"10% (NT$5.001-20M), 20% (más de NT$20M).","claim":"Los ganadores tienen 3 meses. Los premios se pagan en su totalidad."},
  "pt":{"tax":"10% (NT$5.001-20M), 20% (acima de NT$20M).","claim":"Os ganhadores têm 3 meses. Os prêmios são pagos integralmente."},
  "id":{"tax":"10% (NT$5.001-20 juta), 20% (di atas NT$20 juta).","claim":"Pemenang memiliki waktu 3 bulan. Hadiah dibayarkan penuh."},
},
"taiwan-lotto": {
  "ja":{"tax":"10%（500万〜2,000万台湾ドル）、20%（2,000万台湾ドル超）。","claim":"当選者は3ヶ月以内に請求が必要です。"},
  "ko":{"tax":"10%(NT$5,001~2,000만), 20%(NT$2,000만 초과)。","claim":"당첨자는 3개월 이내에 청구해야 합니다."},
  "fr":{"tax":"10 % (5 001 à 20 M NT$), 20 % (au-delà de 20 M NT$).","claim":"Les gagnants disposent de 3 mois."},
  "de":{"tax":"10 % (5.001–20 Mio. NT$), 20 % (über 20 Mio. NT$).","claim":"Gewinner haben 3 Monate Zeit."},
  "es":{"tax":"10% (NT$5.001-20M), 20% (más de NT$20M).","claim":"Los ganadores tienen 3 meses."},
  "pt":{"tax":"10% (NT$5.001-20M), 20% (acima de NT$20M).","claim":"Os ganhadores têm 3 meses."},
  "id":{"tax":"10% (NT$5.001-20 juta), 20% (di atas NT$20 juta).","claim":"Pemenang memiliki waktu 3 bulan."},
},
"daily-cash": {
  "ja":{"tax":"10%（500万〜2,000万台湾ドル）、20%（2,000万台湾ドル超）。","claim":"1等は800万台湾ドル固定です。当選者は3ヶ月以内に請求が必要です。"},
  "ko":{"tax":"10%(NT$5,001~2,000만), 20%(NT$2,000만 초과)。","claim":"1등 상금은 NT$800만으로 고정되어 있습니다. 당첨자는 3개월 이내에 청구해야 합니다."},
  "fr":{"tax":"10 % (5 001 à 20 M NT$), 20 % (au-delà de 20 M NT$).","claim":"Le premier prix est fixé à 8 M NT$. Les gagnants disposent de 3 mois."},
  "de":{"tax":"10 % (5.001–20 Mio. NT$), 20 % (über 20 Mio. NT$).","claim":"Der erste Preis ist auf 8 Mio. NT$ festgelegt. Gewinner haben 3 Monate Zeit."},
  "es":{"tax":"10% (NT$5.001-20M), 20% (más de NT$20M).","claim":"El primer premio es fijo, NT$8 millones. Los ganadores tienen 3 meses."},
  "pt":{"tax":"10% (NT$5.001-20M), 20% (acima de NT$20M).","claim":"O primeiro prêmio é fixo em NT$8 milhões. Os ganhadores têm 3 meses."},
  "id":{"tax":"10% (NT$5.001-20 juta), 20% (di atas NT$20 juta).","claim":"Hadiah pertama tetap NT$8 juta. Pemenang memiliki waktu 3 bulan."},
},
"mega-sena": {
  "ja":{"tax":"1,903.98レアルを超える部分に30%課税されます。","claim":"当選者は90日以内に請求が必要です。"},
  "ko":{"tax":"1,903.98 헤알 초과분에 30% 과세됩니다。","claim":"당첨자는 90일 이내에 청구해야 합니다."},
  "fr":{"tax":"30 % sur les montants dépassant 1 903,98 R$.","claim":"Les gagnants disposent de 90 jours."},
  "de":{"tax":"30 % auf Beträge über 1.903,98 R$.","claim":"Gewinner haben 90 Tage Zeit."},
  "es":{"tax":"30% sobre los importes que superen los R$1.903,98.","claim":"Los ganadores tienen 90 días."},
  "pt":{"tax":"30% sobre valores acima de R$1.903,98.","claim":"Os ganhadores têm 90 dias."},
  "id":{"tax":"Pajak 30% untuk jumlah di atas R$1.903,98.","claim":"Pemenang memiliki waktu 90 hari."},
},
"korea-lotto": {
  "ja":{"tax":"5,000万ウォンを超える部分に22%課税されます。","claim":"当選者は1年以内に請求が必要です。"},
  "ko":{"tax":"5천만 원 초과분에 22% 과세됩니다。","claim":"당첨자는 1년 이내에 청구해야 합니다."},
  "fr":{"tax":"22 % sur les montants dépassant 50 millions ₩.","claim":"Les gagnants disposent de 1 an."},
  "de":{"tax":"22 % auf Beträge über 50 Mio. ₩.","claim":"Gewinner haben 1 Jahr Zeit."},
  "es":{"tax":"22% sobre los importes que superen los 50 millones de ₩.","claim":"Los ganadores tienen 1 año."},
  "pt":{"tax":"22% sobre valores acima de ₩50 milhões.","claim":"Os ganhadores têm 1 ano."},
  "id":{"tax":"Pajak 22% untuk jumlah di atas ₩50 juta.","claim":"Pemenang memiliki waktu 1 tahun."},
},
"japan-loto6": {
  "ja":{"tax":"当選金全額に対して20.315%が課税されます。","claim":"当選者は1年以内に請求が必要です。"},
  "ko":{"tax":"당첨금 전액에 20.315% 세금이 부과됩니다。","claim":"당첨자는 1년 이내에 청구해야 합니다."},
  "fr":{"tax":"20,315 % sur la totalité des gains.","claim":"Les gagnants disposent de 1 an."},
  "de":{"tax":"20,315 % auf den gesamten Gewinn.","claim":"Gewinner haben 1 Jahr Zeit."},
  "es":{"tax":"20,315% sobre la totalidad de las ganancias.","claim":"Los ganadores tienen 1 año."},
  "pt":{"tax":"20,315% sobre o valor total do prêmio.","claim":"Os ganhadores têm 1 ano."},
  "id":{"tax":"Pajak 20,315% atas seluruh kemenangan.","claim":"Pemenang memiliki waktu 1 tahun."},
},
}

# ============================================================
# 各語言的 FAQ 題目/答案模板（不含彩票專屬的 tax/claim，那部分從 TAX_CLAIM_I18N 抓）
# 用 {n}{range}{pick}{bonus_text}{bet}{days}{time}{odds} 做變數代換
# ============================================================

FAQ_TEMPLATES = {
"ja": {
  "bonus_text": "、さらに1から{brange}の中からボーナス数字を{bonus}個選びます",
  "q1": "{n}の遊び方は？", "a1": "1から{range}の中から{pick}個の数字を選びます{bonus_text}。1口{bet}、{days}の{time}に抽選が行われます。",
  "q2": "{n}の当選確率は？", "a2": "ジャックポットの当選確率は{odds}です。当選者がいない場合、賞金は次回に繰り越されます。",
  "q3": "{n}の当選金には税金がかかりますか？",
  "q4": "{n}の当選金の受け取り方法は？",
  "q5": "{n}の抽選結果はどこで確認できますか？",
  "a5": "このページでは最新の当選番号、抽選履歴、統計分析、無料の番号生成ツールを提供しており、毎日自動更新されます。",
  "faq_title": "よくある質問",
},
"ko": {
  "bonus_text": ", 그리고 1부터 {brange}까지 중 보너스 번호 {bonus}개를 추가로 선택합니다",
  "q1": "{n}는 어떻게 하나요?", "a1": "1부터 {range}까지의 숫자 중 {pick}개를 선택합니다{bonus_text}. 1건당 {bet}이며, {days} {time}에 추첨합니다.",
  "q2": "{n}의 당첨 확률은 얼마인가요?", "a2": "1등 당첨 확률은 {odds}입니다. 당첨자가 없으면 상금은 다음 회차로 이월됩니다.",
  "q3": "{n} 당첨금에 세금이 부과되나요?",
  "q4": "{n} 당첨금은 어떻게 수령하나요?",
  "q5": "{n} 추첨 결과는 어디서 확인하나요?",
  "a5": "이 페이지에서는 최신 당첨 번호, 역대 기록, 통계 분석, 무료 번호 생성기를 제공하며 매일 자동으로 업데이트됩니다.",
  "faq_title": "자주 묻는 질문",
},
"fr": {
  "bonus_text": ", plus {bonus} numéro(s) bonus parmi 1 et {brange}",
  "q1": "Comment jouer au {n} ?", "a1": "Choisissez {pick} numéros parmi 1 et {range}{bonus_text}. Mise : {bet}. Tirages : {days} à {time}.",
  "q2": "Quelles sont les chances de gagner au {n} ?", "a2": "Les chances de remporter le jackpot sont de {odds}. Si personne ne gagne, le jackpot est reporté au tirage suivant.",
  "q3": "Les gains du {n} sont-ils imposés ?",
  "q4": "Comment réclamer un gain au {n} ?",
  "q5": "Où puis-je consulter les résultats du {n} ?",
  "a5": "Cette page fournit les derniers numéros gagnants, l'historique des tirages, des analyses statistiques et des générateurs de numéros gratuits, mise à jour quotidiennement.",
  "faq_title": "Questions fréquentes",
},
"de": {
  "bonus_text": ", plus {bonus} Bonuszahl(en) aus 1 bis {brange}",
  "q1": "Wie spielt man {n}?", "a1": "Wählen Sie {pick} Zahlen aus 1 bis {range}{bonus_text}. Einsatz: {bet}. Ziehungen: {days} um {time}.",
  "q2": "Wie hoch sind die Gewinnchancen bei {n}?", "a2": "Die Jackpot-Gewinnchance liegt bei {odds}. Wird der Jackpot nicht gewonnen, wird er auf die nächste Ziehung übertragen.",
  "q3": "Werden {n}-Gewinne besteuert?",
  "q4": "Wie beansprucht man einen {n}-Gewinn?",
  "q5": "Wo kann ich die {n}-Ergebnisse einsehen?",
  "a5": "Diese Seite bietet die neuesten Gewinnzahlen, Ziehungshistorie, statistische Analysen und kostenlose Zahlengeneratoren, täglich aktualisiert.",
  "faq_title": "Häufig gestellte Fragen",
},
"es": {
  "bonus_text": ", más {bonus} número(s) de bonificación del 1 al {brange}",
  "q1": "¿Cómo se juega a {n}?", "a1": "Elige {pick} números del 1 al {range}{bonus_text}. Costo: {bet}. Sorteos: {days} a las {time}.",
  "q2": "¿Cuáles son las probabilidades de ganar en {n}?", "a2": "La probabilidad de ganar el premio mayor es de {odds}. Si nadie gana, el bote se acumula para el siguiente sorteo.",
  "q3": "¿Los premios de {n} están sujetos a impuestos?",
  "q4": "¿Cómo se cobra un premio de {n}?",
  "q5": "¿Dónde puedo consultar los resultados de {n}?",
  "a5": "Esta página ofrece los últimos números ganadores, historial de sorteos, análisis estadístico y generadores de números gratuitos, actualizados diariamente.",
  "faq_title": "Preguntas frecuentes",
},
"pt": {
  "bonus_text": ", mais {bonus} número(s) bônus de 1 a {brange}",
  "q1": "Como jogar {n}?", "a1": "Escolha {pick} números de 1 a {range}{bonus_text}. Aposta: {bet}. Sorteios: {days} às {time}.",
  "q2": "Quais são as chances de ganhar no {n}?", "a2": "A probabilidade de ganhar o prêmio principal é de {odds}. Se ninguém ganhar, o valor acumula para o próximo sorteio.",
  "q3": "Os prêmios do {n} são tributados?",
  "q4": "Como resgatar um prêmio do {n}?",
  "q5": "Onde posso conferir os resultados do {n}?",
  "a5": "Esta página fornece os últimos números sorteados, histórico de sorteios, análise estatística e geradores de números gratuitos, atualizados diariamente.",
  "faq_title": "Perguntas frequentes",
},
"id": {
  "bonus_text": ", ditambah {bonus} angka bonus dari 1 hingga {brange}",
  "q1": "Bagaimana cara bermain {n}?", "a1": "Pilih {pick} angka dari 1 hingga {range}{bonus_text}. Biaya: {bet}. Undian: {days} pukul {time}.",
  "q2": "Berapa peluang menang {n}?", "a2": "Peluang memenangkan jackpot adalah {odds}. Jika tidak ada pemenang, hadiah akan diakumulasikan ke undian berikutnya.",
  "q3": "Apakah kemenangan {n} dikenakan pajak?",
  "q4": "Bagaimana cara klaim hadiah {n}?",
  "q5": "Di mana saya bisa melihat hasil {n}?",
  "a5": "Halaman ini menyediakan nomor kemenangan terbaru, riwayat undian, analisis statistik, dan generator nomor gratis, diperbarui setiap hari.",
  "faq_title": "Pertanyaan yang Sering Diajukan",
},
}

# ============================================================
# how-to-play 步驟區塊（build_howto_block）的 7 語言翻譯
# {bonus_text} 用另一組（跟FAQ的不同措辭，配合howto步驟的簡短風格）
# ============================================================

HOWTO_TEMPLATES = {
"ja": {
  "bonus_text": "、さらに1〜{brange}からボーナス{bonus}個",
  "step1": "1〜{range}から{pick}個選択{bonus_text}", "step2": "1口 {bet}",
  "step3": "抽選：{days} {time}", "step4": "ジャックポット確率：{odds}",
  "t_how": "{n}の遊び方", "t_tax": "税務と受け取り方法", "l_tax": "税率", "l_claim": "受け取り方法",
},
"ko": {
  "bonus_text": ", 1~{brange}에서 보너스 {bonus}개 추가",
  "step1": "1~{range}에서 {pick}개 선택{bonus_text}", "step2": "1건당 {bet}",
  "step3": "추첨: {days} {time}", "step4": "잭팟 확률: {odds}",
  "t_how": "{n} 하는 법", "t_tax": "세금 및 수령 방법", "l_tax": "세율", "l_claim": "수령",
},
"fr": {
  "bonus_text": ", plus {bonus} bonus parmi 1-{brange}",
  "step1": "Choisir {pick} numéros parmi 1-{range}{bonus_text}", "step2": "Coût : {bet} par mise",
  "step3": "Tirages : {days} à {time}", "step4": "Probabilité jackpot : {odds}",
  "t_how": "Comment jouer au {n}", "t_tax": "Impôts et réclamation", "l_tax": "Impôt", "l_claim": "Réclamation",
},
"de": {
  "bonus_text": ", plus {bonus} Bonuszahl(en) aus 1-{brange}",
  "step1": "{pick} Zahlen aus 1-{range} wählen{bonus_text}", "step2": "Kosten: {bet} pro Einsatz",
  "step3": "Ziehungen: {days} um {time}", "step4": "Jackpot-Chance: {odds}",
  "t_how": "So spielen Sie {n}", "t_tax": "Steuern & Gewinnabholung", "l_tax": "Steuer", "l_claim": "Abholung",
},
"es": {
  "bonus_text": ", más {bonus} bonus del 1-{brange}",
  "step1": "Elegir {pick} números del 1-{range}{bonus_text}", "step2": "Costo: {bet} por apuesta",
  "step3": "Sorteos: {days} a las {time}", "step4": "Probabilidad de bote: {odds}",
  "t_how": "Cómo jugar a {n}", "t_tax": "Impuestos y cobro", "l_tax": "Impuesto", "l_claim": "Cobro",
},
"pt": {
  "bonus_text": ", mais {bonus} bônus de 1-{brange}",
  "step1": "Escolher {pick} números de 1-{range}{bonus_text}", "step2": "Custo: {bet} por aposta",
  "step3": "Sorteios: {days} às {time}", "step4": "Probabilidade do prêmio: {odds}",
  "t_how": "Como jogar {n}", "t_tax": "Impostos e resgate", "l_tax": "Imposto", "l_claim": "Resgate",
},
"id": {
  "bonus_text": ", ditambah {bonus} bonus dari 1-{brange}",
  "step1": "Pilih {pick} angka dari 1-{range}{bonus_text}", "step2": "Biaya: {bet} per taruhan",
  "step3": "Undian: {days} pukul {time}", "step4": "Peluang jackpot: {odds}",
  "t_how": "Cara Bermain {n}", "t_tax": "Pajak & Klaim Hadiah", "l_tax": "Pajak", "l_claim": "Klaim",
},
}

# ============================================================
# 歷史紀錄頁 (history) 專用 FAQ 模板 — 3 題，避免跟 intro/results 內容重複
# ============================================================
HISTORY_FAQ = {
"zh-TW": {"title":"常見問題", "q":[
  ("{n}的歷史開獎紀錄可以查多久以前的？","本頁收錄{n}發行以來的完整開獎紀錄，可透過日期或號碼搜尋查詢任一期的開獎結果。"),
  ("如何查詢特定號碼的歷史出現次數？","使用本頁的號碼搜尋功能，輸入 1 到 {range} 之間的號碼，即可看到該號碼在歷史上出現的所有期數與最近一次出現的日期。"),
  ("歷史開獎紀錄對選號有幫助嗎？","每次開獎都是獨立事件，歷史紀錄不能預測未來結果，但能幫助您了解號碼的長期出現規律，建議搭配統計分析頁面一起參考。"),
]},
"zh-CN": {"title":"常见问题", "q":[
  ("{n}的历史开奖记录可以查多久以前的？","本页收录{n}发行以来的完整开奖记录，可通过日期或号码搜索查询任一期的开奖结果。"),
  ("如何查询特定号码的历史出现次数？","使用本页的号码搜索功能，输入 1 到 {range} 之间的号码，即可看到该号码在历史上出现的所有期数与最近一次出现的日期。"),
  ("历史开奖记录对选号有帮助吗？","每次开奖都是独立事件，历史记录不能预测未来结果，但能帮助您了解号码的长期出现规律，建议搭配统计分析页面一起参考。"),
]},
"en": {"title":"FAQ", "q":[
  ("How far back does the {n} draw history go?","This page includes the complete draw history since {n} launched. You can search by date or number to find results for any specific draw."),
  ("How do I check how often a specific number has appeared?","Use the number search tool on this page. Enter any number from 1 to {range} to see every draw it appeared in and the date it was last drawn."),
  ("Is draw history useful for picking numbers?","Each draw is an independent event, so history can't predict future results. However, it can help you understand long-term number patterns — pair it with the Statistics page for a fuller picture."),
]},
"ja": {"title":"よくある質問", "q":[
  ("{n}の過去の開催結果はどこまで遡って見られますか？","このページには{n}の発行開始以来の完全な開催履歴が収録されており、日付または番号で特定の回の結果を検索できます。"),
  ("特定の番号の過去の出現回数はどう調べますか？","このページの番号検索機能を使い、1〜{range}の番号を入力すると、その番号が出現したすべての回と最後に出現した日付が表示されます。"),
  ("履歴データは選号の参考になりますか？","各抽選は独立した事象のため、履歴は将来の結果を予測するものではありませんが、長期的な出現傾向を把握するのに役立ちます。統計分析ページと合わせてご参照ください。"),
]},
"ko": {"title":"자주 묻는 질문", "q":[
  ("{n}의 과거 추첨 기록은 언제까지 조회할 수 있나요?","이 페이지에는 {n} 출시 이후의 전체 추첨 기록이 수록되어 있으며, 날짜 또는 번호로 특정 회차의 결과를 검색할 수 있습니다."),
  ("특정 번호의 과거 출현 횟수는 어떻게 확인하나요?","이 페이지의 번호 검색 기능을 사용해 1~{range} 사이의 번호를 입력하면, 해당 번호가 출현한 모든 회차와 마지막 출현 날짜를 볼 수 있습니다."),
  ("과거 기록이 번호 선택에 도움이 되나요?","각 추첨은 독립적인 사건이므로 과거 기록이 미래 결과를 예측하지는 않지만, 장기적인 출현 패턴을 이해하는 데 도움이 됩니다. 통계 분석 페이지와 함께 참고하시길 권장합니다."),
]},
"fr": {"title":"Questions fréquentes", "q":[
  ("Jusqu'à quand remonte l'historique des tirages {n} ?","Cette page contient l'historique complet des tirages depuis le lancement de {n}. Vous pouvez rechercher par date ou par numéro pour retrouver les résultats d'un tirage précis."),
  ("Comment vérifier combien de fois un numéro est sorti ?","Utilisez l'outil de recherche par numéro sur cette page. Entrez un numéro entre 1 et {range} pour voir tous les tirages où il est apparu et sa dernière date de sortie."),
  ("L'historique des tirages est-il utile pour choisir ses numéros ?","Chaque tirage est un événement indépendant, l'historique ne peut donc pas prédire les résultats futurs. Il peut cependant aider à comprendre les tendances à long terme — à combiner avec la page Statistiques."),
]},
"de": {"title":"Häufig gestellte Fragen", "q":[
  ("Wie weit reicht die Ziehungshistorie von {n} zurück?","Diese Seite enthält die vollständige Ziehungshistorie seit dem Start von {n}. Sie können nach Datum oder Zahl suchen, um Ergebnisse einer bestimmten Ziehung zu finden."),
  ("Wie prüfe ich, wie oft eine bestimmte Zahl gezogen wurde?","Nutzen Sie die Zahlensuche auf dieser Seite. Geben Sie eine Zahl von 1 bis {range} ein, um alle Ziehungen mit dieser Zahl und das Datum der letzten Ziehung zu sehen."),
  ("Ist die Ziehungshistorie hilfreich für die Zahlenwahl?","Jede Ziehung ist ein unabhängiges Ereignis, die Historie kann also keine zukünftigen Ergebnisse vorhersagen. Sie hilft aber, langfristige Muster zu erkennen — kombinieren Sie sie mit der Statistik-Seite."),
]},
"es": {"title":"Preguntas frecuentes", "q":[
  ("¿Hasta cuándo se remonta el historial de sorteos de {n}?","Esta página incluye el historial completo de sorteos desde el lanzamiento de {n}. Puedes buscar por fecha o número para encontrar los resultados de un sorteo específico."),
  ("¿Cómo compruebo cuántas veces ha salido un número?","Usa la herramienta de búsqueda por número de esta página. Introduce un número del 1 al {range} para ver todos los sorteos en los que apareció y la fecha de su última salida."),
  ("¿El historial de sorteos es útil para elegir números?","Cada sorteo es un evento independiente, por lo que el historial no puede predecir resultados futuros. Sin embargo, puede ayudarte a entender patrones a largo plazo — combínalo con la página de Estadísticas."),
]},
"pt": {"title":"Perguntas frequentes", "q":[
  ("Até quando vai o histórico de sorteios do {n}?","Esta página inclui o histórico completo de sorteios desde o lançamento do {n}. Você pode pesquisar por data ou número para encontrar os resultados de um sorteio específico."),
  ("Como verifico quantas vezes um número saiu?","Use a ferramenta de busca por número desta página. Digite um número de 1 a {range} para ver todos os sorteios em que ele apareceu e a data da última vez que saiu."),
  ("O histórico de sorteios é útil para escolher números?","Cada sorteio é um evento independente, então o histórico não prevê resultados futuros. Porém, ajuda a entender padrões de longo prazo — combine com a página de Estatísticas."),
]},
"id": {"title":"Pertanyaan yang Sering Diajukan", "q":[
  ("Seberapa jauh riwayat undian {n} bisa dilihat?","Halaman ini berisi riwayat undian lengkap sejak {n} diluncurkan. Anda dapat mencari berdasarkan tanggal atau nomor untuk menemukan hasil undian tertentu."),
  ("Bagaimana cara memeriksa berapa kali angka tertentu muncul?","Gunakan alat pencarian nomor di halaman ini. Masukkan angka 1 hingga {range} untuk melihat semua undian tempat angka itu muncul dan tanggal terakhir munculnya."),
  ("Apakah riwayat undian berguna untuk memilih angka?","Setiap undian adalah kejadian independen, jadi riwayat tidak dapat memprediksi hasil masa depan. Namun, riwayat dapat membantu memahami pola jangka panjang — gunakan bersama halaman Statistik."),
]},
}

# ============================================================
# 統計分析頁 (statistics) 專用 FAQ 模板 — 3 題
# ============================================================
STATS_FAQ = {
"zh-TW": {"title":"常見問題", "q":[
  ("什麼是{n}的熱門號碼和冷門號碼？","熱門號碼是歷史上出現次數最多的號碼，冷門號碼是最久沒有出現的號碼。本頁統計數據每日根據最新開獎結果自動更新。"),
  ("號碼出現次數的統計數據準確嗎？","統計數據是根據所有歷史開獎紀錄實際計算得出，數字本身準確，但請注意每次開獎都是獨立事件，過去的出現次數不影響未來中獎機率。"),
  ("應該選熱門號碼還是冷門號碼？","兩種策略都沒有科學根據能提高中獎機率，因為每次開獎都是獨立隨機事件。統計數據僅供參考，選號請理性看待。"),
]},
"zh-CN": {"title":"常见问题", "q":[
  ("什么是{n}的热门号码和冷门号码？","热门号码是历史上出现次数最多的号码，冷门号码是最久没有出现的号码。本页统计数据每日根据最新开奖结果自动更新。"),
  ("号码出现次数的统计数据准确吗？","统计数据是根据所有历史开奖记录实际计算得出，数字本身准确，但请注意每次开奖都是独立事件，过去的出现次数不影响未来中奖概率。"),
  ("应该选热门号码还是冷门号码？","两种策略都没有科学根据能提高中奖概率，因为每次开奖都是独立随机事件。统计数据仅供参考，选号请理性看待。"),
]},
"en": {"title":"FAQ", "q":[
  ("What are hot and cold numbers for {n}?","Hot numbers are those that have appeared most frequently in the draw history. Cold numbers are those that haven't appeared in the longest time. This page's statistics update automatically after every new draw."),
  ("Are the number frequency statistics accurate?","The statistics are calculated directly from the complete draw history, so the figures themselves are accurate. However, each draw is an independent event — past frequency doesn't affect future odds."),
  ("Should I pick hot numbers or cold numbers?","Neither strategy has any scientific basis for improving your odds, since every draw is an independent random event. Use these statistics for reference only and play responsibly."),
]},
"ja": {"title":"よくある質問", "q":[
  ("{n}のホット番号・コールド番号とは何ですか？","ホット番号は過去に最も多く出現した番号、コールド番号は最も長く出現していない番号です。本ページの統計は最新の抽選結果に基づき毎日自動更新されます。"),
  ("番号の出現回数の統計は正確ですか？","統計は全ての過去の開催記録から実際に計算されているため数値自体は正確ですが、各抽選は独立した事象であり、過去の出現回数が将来の当選確率に影響することはありません。"),
  ("ホット番号とコールド番号、どちらを選ぶべきですか？","各抽選は独立したランダムな事象であるため、どちらの戦略にも当選確率を高める科学的根拠はありません。統計はあくまで参考情報としてご利用ください。"),
]},
"ko": {"title":"자주 묻는 질문", "q":[
  ("{n}의 핫 넘버와 콜드 넘버란 무엇인가요?","핫 넘버는 과거 가장 많이 출현한 번호이고, 콜드 넘버는 가장 오랫동안 출현하지 않은 번호입니다. 이 페이지의 통계는 매 추첨 후 자동으로 업데이트됩니다."),
  ("번호 출현 횟수 통계는 정확한가요?","통계는 전체 과거 추첨 기록을 바탕으로 실제 계산된 것이므로 수치 자체는 정확합니다. 다만 각 추첨은 독립적인 사건이므로 과거 출현 횟수가 미래 당첨 확률에 영향을 주지는 않습니다."),
  ("핫 넘버와 콜드 넘버 중 어느 쪽을 선택해야 하나요?","각 추첨은 독립적인 무작위 사건이므로 두 전략 모두 당첨 확률을 높인다는 과학적 근거는 없습니다. 통계는 참고용으로만 활용하시기 바랍니다."),
]},
"fr": {"title":"Questions fréquentes", "q":[
  ("Que sont les numéros chauds et froids pour {n} ?","Les numéros chauds sont ceux qui sont sortis le plus souvent dans l'historique. Les numéros froids sont ceux qui ne sont pas sortis depuis le plus longtemps. Les statistiques de cette page se mettent à jour automatiquement après chaque tirage."),
  ("Les statistiques de fréquence des numéros sont-elles fiables ?","Les statistiques sont calculées directement à partir de l'historique complet des tirages, les chiffres sont donc exacts. Cependant, chaque tirage est un événement indépendant — la fréquence passée n'influence pas les probabilités futures."),
  ("Faut-il choisir des numéros chauds ou froids ?","Aucune des deux stratégies n'a de base scientifique pour améliorer vos chances, car chaque tirage est un événement aléatoire indépendant. Utilisez ces statistiques à titre indicatif uniquement."),
]},
"de": {"title":"Häufig gestellte Fragen", "q":[
  ("Was sind heiße und kalte Zahlen bei {n}?","Heiße Zahlen sind jene, die in der Ziehungshistorie am häufigsten vorkamen. Kalte Zahlen sind jene, die am längsten nicht gezogen wurden. Die Statistiken dieser Seite werden nach jeder Ziehung automatisch aktualisiert."),
  ("Sind die Häufigkeitsstatistiken der Zahlen genau?","Die Statistiken werden direkt aus der vollständigen Ziehungshistorie berechnet, die Zahlen selbst sind also korrekt. Jede Ziehung ist jedoch ein unabhängiges Ereignis — vergangene Häufigkeit beeinflusst nicht die zukünftigen Chancen."),
  ("Sollte ich heiße oder kalte Zahlen wählen?","Keine der beiden Strategien hat eine wissenschaftliche Grundlage zur Verbesserung Ihrer Gewinnchancen, da jede Ziehung ein unabhängiges Zufallsereignis ist. Nutzen Sie diese Statistiken nur als Orientierung."),
]},
"es": {"title":"Preguntas frecuentes", "q":[
  ("¿Qué son los números calientes y fríos de {n}?","Los números calientes son los que más veces han salido en el historial. Los números fríos son los que llevan más tiempo sin salir. Las estadísticas de esta página se actualizan automáticamente tras cada sorteo."),
  ("¿Son precisas las estadísticas de frecuencia de números?","Las estadísticas se calculan directamente a partir del historial completo de sorteos, por lo que las cifras son exactas. Sin embargo, cada sorteo es un evento independiente: la frecuencia pasada no afecta las probabilidades futuras."),
  ("¿Debo elegir números calientes o fríos?","Ninguna de las dos estrategias tiene base científica para mejorar tus probabilidades, ya que cada sorteo es un evento aleatorio independiente. Usa estas estadísticas solo como referencia."),
]},
"pt": {"title":"Perguntas frequentes", "q":[
  ("O que são números quentes e frios para {n}?","Números quentes são os que mais saíram no histórico. Números frios são os que ficaram mais tempo sem sair. As estatísticas desta página são atualizadas automaticamente após cada sorteio."),
  ("As estatísticas de frequência dos números são precisas?","As estatísticas são calculadas diretamente a partir do histórico completo de sorteios, então os números em si são precisos. No entanto, cada sorteio é um evento independente — a frequência passada não afeta as probabilidades futuras."),
  ("Devo escolher números quentes ou frios?","Nenhuma das duas estratégias tem base científica para melhorar suas chances, já que cada sorteio é um evento aleatório independente. Use essas estatísticas apenas como referência."),
]},
"id": {"title":"Pertanyaan yang Sering Diajukan", "q":[
  ("Apa itu angka panas dan dingin untuk {n}?","Angka panas adalah angka yang paling sering muncul dalam riwayat undian. Angka dingin adalah angka yang paling lama tidak muncul. Statistik di halaman ini diperbarui otomatis setelah setiap undian."),
  ("Apakah statistik frekuensi angka ini akurat?","Statistik dihitung langsung dari seluruh riwayat undian, jadi angkanya akurat. Namun, setiap undian adalah kejadian independen — frekuensi masa lalu tidak memengaruhi peluang di masa depan."),
  ("Sebaiknya saya pilih angka panas atau dingin?","Kedua strategi ini tidak memiliki dasar ilmiah untuk meningkatkan peluang menang, karena setiap undian adalah kejadian acak yang independen. Gunakan statistik ini hanya sebagai referensi."),
]},
}

# ============================================================
# number-generator.html（通用選號入口頁）10語言加厚內容
# meta_desc: 修正原本是空字串的bug
# intro: 介紹段落
# faq: 3題FAQ
# ============================================================
NG_CONTENT = {
"zh-TW": {"meta_desc":"免費線上樂透選號工具，提供隨機、熱門號碼、冷門號碼、生日、星座等 12 種選號方式，支援全球 15 大彩票，包含威力彩、大樂透、Powerball、EuroMillions 等。",
  "intro":"這裡提供 12 種不同的選號方式，從純隨機亂數到根據生日、星座、歷史熱門/冷門號碼等各種邏輯，適用於全球 15 種主要彩票。所有工具完全免費，選完號碼後可以直接前往對應彩票的開獎結果頁面核對。",
  "faq_title":"常見問題", "faq":[
    ("這些選號工具真的能提高中獎機率嗎？","不能。彩票開獎是完全隨機且獨立的事件，任何選號方式（包含熱門/冷門號碼統計）都無法改變中獎機率，這些工具僅提供趣味性與便利性。"),
    ("我可以同時使用多種選號方式嗎？","可以，每種工具都是獨立頁面，您可以多次使用不同方式產生號碼並互相比較，找出自己喜歡的組合。"),
    ("選出來的號碼會自動儲存嗎？","目前選號工具僅在頁面上顯示結果，不會自動儲存。建議產生號碼後自行截圖或記錄下來。"),
]},
"zh-CN": {"meta_desc":"免费在线彩票选号工具，提供随机、热门号码、冷门号码、生日、星座等 12 种选号方式，支持全球 15 大彩票，包含威力彩、大乐透、Powerball、EuroMillions 等。",
  "intro":"这里提供 12 种不同的选号方式，从纯随机数字到根据生日、星座、历史热门/冷门号码等各种逻辑，适用于全球 15 种主要彩票。所有工具完全免费，选完号码后可以直接前往对应彩票的开奖结果页面核对。",
  "faq_title":"常见问题", "faq":[
    ("这些选号工具真的能提高中奖概率吗？","不能。彩票开奖是完全随机且独立的事件，任何选号方式（包含热门/冷门号码统计）都无法改变中奖概率，这些工具仅提供趣味性与便利性。"),
    ("我可以同时使用多种选号方式吗？","可以，每种工具都是独立页面，您可以多次使用不同方式生成号码并互相比较，找出自己喜欢的组合。"),
    ("选出来的号码会自动保存吗？","目前选号工具仅在页面上显示结果，不会自动保存。建议生成号码后自行截图或记录下来。"),
]},
"en": {"meta_desc":"Free online lottery number generator with 12 methods — random, hot numbers, cold numbers, birthday, zodiac, and more — covering 15 major global lotteries including Powerball, EuroMillions, and more.",
  "intro":"Choose from 12 different number generation methods, from pure random draws to birthday, zodiac, and historical hot/cold number logic, covering 15 major lotteries worldwide. All tools are completely free — after generating your numbers, head straight to the matching lottery's results page to check them.",
  "faq_title":"FAQ", "faq":[
    ("Can these number generators actually improve my odds of winning?","No. Lottery draws are completely random and independent events. No number-picking method — including hot/cold number statistics — can change your odds. These tools are for fun and convenience only."),
    ("Can I use more than one method?","Yes, each tool is a separate page. You can generate numbers with different methods and compare the results to find a combination you like."),
    ("Are my generated numbers saved automatically?","No, the generators only display results on the page and don't save them. We recommend taking a screenshot or writing down any numbers you want to keep."),
]},
"ja": {"meta_desc":"無料のオンライン宝くじ番号生成ツール。ランダム、ホット番号、コールド番号、誕生日、星座など12種類の方式に対応し、Powerball、EuroMillionsなど世界15大宝くじをカバー。",
  "intro":"純粋なランダム生成から誕生日、星座、過去のホット/コールド番号に基づくロジックまで、12種類の選号方式をご用意しています。世界15大宝くじに対応しており、すべて無料でご利用いただけます。番号を生成したら、該当する宝くじの開催結果ページで確認できます。",
  "faq_title":"よくある質問", "faq":[
    ("これらの選号ツールは本当に当選確率を上げられますか？","いいえ。宝くじの抽選は完全にランダムで独立した事象であり、ホット/コールド番号統計を含むどの選号方法も当選確率を変えることはできません。これらのツールは娯楽と利便性のためのものです。"),
    ("複数の方式を同時に使えますか？","はい、各ツールは独立したページなので、異なる方式で番号を生成して比較し、お好みの組み合わせを見つけることができます。"),
    ("生成した番号は自動保存されますか？","いいえ、選号ツールはページ上に結果を表示するのみで自動保存はされません。スクリーンショットを撮るなどして記録することをお勧めします。"),
]},
"ko": {"meta_desc":"무료 온라인 복권 번호 생성기. 무작위, 핫 넘버, 콜드 넘버, 생일, 별자리 등 12가지 방식 지원, Powerball, EuroMillions 등 전 세계 15대 복권을 다룹니다.",
  "intro":"순수 무작위 생성부터 생일, 별자리, 과거 핫/콜드 넘버 로직까지 12가지 번호 생성 방식을 제공합니다. 전 세계 15대 복권을 지원하며 모든 도구는 완전 무료입니다. 번호를 생성한 후에는 해당 복권의 추첨 결과 페이지에서 바로 확인할 수 있습니다.",
  "faq_title":"자주 묻는 질문", "faq":[
    ("이 선택 도구들이 실제로 당첨 확률을 높여주나요?","아닙니다. 복권 추첨은 완전히 무작위이며 독립적인 사건입니다. 핫/콜드 넘버 통계를 포함한 어떤 번호 선택 방법도 당첨 확률을 바꿀 수 없습니다. 이 도구들은 재미와 편의를 위한 것입니다."),
    ("여러 방식을 동시에 사용할 수 있나요?","네, 각 도구는 별도의 페이지이므로 여러 방식으로 번호를 생성하고 비교하여 원하는 조합을 찾을 수 있습니다."),
    ("생성된 번호가 자동으로 저장되나요?","아니요, 선택 도구는 페이지에 결과만 표시하며 자동 저장되지 않습니다. 스크린샷을 찍거나 직접 기록해 두시는 것을 권장합니다."),
]},
"fr": {"meta_desc":"Générateur de numéros de loterie en ligne gratuit avec 12 méthodes — aléatoire, numéros chauds, numéros froids, anniversaire, signe astrologique — couvrant 15 grandes loteries mondiales dont Powerball et EuroMillions.",
  "intro":"Choisissez parmi 12 méthodes de génération de numéros différentes, du tirage purement aléatoire aux logiques basées sur l'anniversaire, le signe astrologique ou l'historique des numéros chauds/froids, couvrant 15 grandes loteries mondiales. Tous les outils sont entièrement gratuits — une fois vos numéros générés, rendez-vous directement sur la page de résultats de la loterie correspondante pour les vérifier.",
  "faq_title":"Questions fréquentes", "faq":[
    ("Ces générateurs peuvent-ils vraiment améliorer mes chances de gagner ?","Non. Les tirages de loterie sont des événements totalement aléatoires et indépendants. Aucune méthode de sélection — y compris les statistiques de numéros chauds/froids — ne peut modifier vos chances. Ces outils sont là pour le plaisir et la commodité."),
    ("Puis-je utiliser plusieurs méthodes ?","Oui, chaque outil est une page distincte. Vous pouvez générer des numéros avec différentes méthodes et comparer les résultats pour trouver la combinaison qui vous plaît."),
    ("Mes numéros générés sont-ils enregistrés automatiquement ?","Non, les générateurs affichent uniquement les résultats sur la page sans les enregistrer. Nous vous recommandons de faire une capture d'écran ou de noter les numéros que vous souhaitez conserver."),
]},
"de": {"meta_desc":"Kostenloser Online-Lotterie-Zahlengenerator mit 12 Methoden — zufällig, heiße Zahlen, kalte Zahlen, Geburtstag, Sternzeichen — für 15 große Lotterien weltweit, darunter Powerball und EuroMillions.",
  "intro":"Wählen Sie aus 12 verschiedenen Methoden zur Zahlengenerierung, von reinem Zufall bis hin zu Logik basierend auf Geburtstag, Sternzeichen oder historischen heißen/kalten Zahlen, für 15 große Lotterien weltweit. Alle Tools sind völlig kostenlos — nach der Generierung Ihrer Zahlen können Sie direkt zur Ergebnisseite der entsprechenden Lotterie wechseln, um sie zu überprüfen.",
  "faq_title":"Häufig gestellte Fragen", "faq":[
    ("Können diese Zahlengeneratoren meine Gewinnchancen wirklich verbessern?","Nein. Lotterieziehungen sind völlig zufällige und unabhängige Ereignisse. Keine Auswahlmethode — einschließlich Statistiken zu heißen/kalten Zahlen — kann Ihre Gewinnchancen verändern. Diese Tools dienen nur der Unterhaltung und dem Komfort."),
    ("Kann ich mehrere Methoden verwenden?","Ja, jedes Tool ist eine eigene Seite. Sie können Zahlen mit verschiedenen Methoden generieren und die Ergebnisse vergleichen, um Ihre bevorzugte Kombination zu finden."),
    ("Werden meine generierten Zahlen automatisch gespeichert?","Nein, die Generatoren zeigen die Ergebnisse nur auf der Seite an und speichern sie nicht. Wir empfehlen, einen Screenshot zu machen oder die gewünschten Zahlen zu notieren."),
]},
"es": {"meta_desc":"Generador de números de lotería en línea gratuito con 12 métodos: aleatorio, números calientes, números fríos, cumpleaños, signo zodiacal, y más, cubriendo 15 grandes loterías mundiales como Powerball y EuroMillions.",
  "intro":"Elige entre 12 métodos diferentes de generación de números, desde el sorteo puramente aleatorio hasta lógicas basadas en cumpleaños, signo zodiacal o números calientes/fríos históricos, cubriendo 15 loterías principales de todo el mundo. Todas las herramientas son completamente gratuitas: una vez generados tus números, ve directamente a la página de resultados de la lotería correspondiente para verificarlos.",
  "faq_title":"Preguntas frecuentes", "faq":[
    ("¿Estos generadores realmente pueden mejorar mis probabilidades de ganar?","No. Los sorteos de lotería son eventos completamente aleatorios e independientes. Ningún método de selección —incluidas las estadísticas de números calientes/fríos— puede cambiar tus probabilidades. Estas herramientas son solo para diversión y comodidad."),
    ("¿Puedo usar más de un método?","Sí, cada herramienta es una página independiente. Puedes generar números con diferentes métodos y comparar los resultados para encontrar la combinación que prefieras."),
    ("¿Mis números generados se guardan automáticamente?","No, los generadores solo muestran los resultados en la página y no los guardan. Recomendamos tomar una captura de pantalla o anotar los números que quieras conservar."),
]},
"pt": {"meta_desc":"Gerador de números de loteria online gratuito com 12 métodos: aleatório, números quentes, números frios, aniversário, signo, e mais, cobrindo 15 grandes loterias mundiais como Powerball e EuroMillions.",
  "intro":"Escolha entre 12 métodos diferentes de geração de números, desde o sorteio puramente aleatório até lógicas baseadas em aniversário, signo ou números quentes/frios históricos, cobrindo 15 grandes loterias mundiais. Todas as ferramentas são totalmente gratuitas — após gerar seus números, vá direto à página de resultados da loteria correspondente para conferi-los.",
  "faq_title":"Perguntas frequentes", "faq":[
    ("Esses geradores realmente podem melhorar minhas chances de ganhar?","Não. Os sorteios de loteria são eventos completamente aleatórios e independentes. Nenhum método de seleção — incluindo estatísticas de números quentes/frios — pode alterar suas chances. Essas ferramentas são apenas para diversão e conveniência."),
    ("Posso usar mais de um método?","Sim, cada ferramenta é uma página separada. Você pode gerar números com métodos diferentes e comparar os resultados para encontrar a combinação que preferir."),
    ("Meus números gerados são salvos automaticamente?","Não, os geradores apenas exibem os resultados na página e não os salvam. Recomendamos tirar uma captura de tela ou anotar os números que deseja guardar."),
]},
"id": {"meta_desc":"Generator nomor lotere online gratis dengan 12 metode — acak, angka panas, angka dingin, ulang tahun, zodiak, dan lainnya — mencakup 15 lotere besar dunia termasuk Powerball dan EuroMillions.",
  "intro":"Pilih dari 12 metode pembuatan nomor yang berbeda, mulai dari undian acak murni hingga logika berdasarkan ulang tahun, zodiak, atau angka panas/dingin historis, mencakup 15 lotere besar di seluruh dunia. Semua alat sepenuhnya gratis — setelah membuat nomor Anda, langsung kunjungi halaman hasil lotere yang sesuai untuk memeriksanya.",
  "faq_title":"Pertanyaan yang Sering Diajukan", "faq":[
    ("Apakah generator nomor ini benar-benar bisa meningkatkan peluang menang saya?","Tidak. Undian lotere adalah kejadian yang sepenuhnya acak dan independen. Tidak ada metode pemilihan nomor — termasuk statistik angka panas/dingin — yang dapat mengubah peluang Anda. Alat ini hanya untuk hiburan dan kenyamanan."),
    ("Bisakah saya menggunakan lebih dari satu metode?","Ya, setiap alat adalah halaman terpisah. Anda dapat membuat nomor dengan metode berbeda dan membandingkan hasilnya untuk menemukan kombinasi yang Anda sukai."),
    ("Apakah nomor yang saya buat disimpan otomatis?","Tidak, generator hanya menampilkan hasil di halaman dan tidak menyimpannya secara otomatis. Kami sarankan mengambil tangkapan layar atau mencatat nomor yang ingin Anda simpan."),
]},
}

# ============================================================
# index.html（彩票站首頁）10語言加厚內容 — 只加一小段介紹文字，不加FAQ（純目錄頁）
# ============================================================
INDEX_INTRO = {
"zh-TW":"SoftGlow 全球彩票每日自動更新 15 種全球主要彩票的最新開獎號碼，涵蓋美國 Powerball、Mega Millions，歐洲 EuroMillions、UK Lotto，以及台灣威力彩、大樂透、今彩539 等亞洲彩票。每個彩種都提供開獎結果、歷史紀錄、號碼統計分析，並搭配 12 種免費線上選號工具，協助您快速產生號碼組合。",
"zh-CN":"SoftGlow 全球彩票每日自动更新 15 种全球主要彩票的最新开奖号码，涵盖美国 Powerball、Mega Millions，欧洲 EuroMillions、UK Lotto，以及台湾威力彩、大乐透、今彩539 等亚洲彩票。每个彩种都提供开奖结果、历史记录、号码统计分析，并搭配 12 种免费在线选号工具，协助您快速生成号码组合。",
"en":"SoftGlow Global Lottery automatically updates the latest winning numbers for 15 major lotteries worldwide every day, including Powerball and Mega Millions in the US, EuroMillions and UK Lotto in Europe, and Taiwan's Power Lottery, Super Lotto, and Daily Cash 539 in Asia. Every lottery includes results, draw history, and number statistics, along with 12 free online number generators to help you quickly create a combination.",
"ja":"SoftGlowグローバル宝くじは、米国のPowerballやMega Millions、欧州のEuroMillionsやUK Lotto、そして台湾のパワー宝くじ、スーパーロト、今彩539など、世界15大宝くじの最新当選番号を毎日自動更新しています。各宝くじには開催結果、履歴、番号統計分析があり、12種類の無料オンライン番号生成ツールで番号の組み合わせを素早く作成できます。",
"ko":"SoftGlow 글로벌 복권은 미국의 Powerball, Mega Millions, 유럽의 EuroMillions, UK Lotto, 그리고 대만의 파워 복권, 슈퍼 로또, 데일리 캐시 539 등 전 세계 15대 복권의 최신 당첨 번호를 매일 자동으로 업데이트합니다. 각 복권마다 추첨 결과, 역대 기록, 번호 통계 분석을 제공하며, 12가지 무료 온라인 번호 생성 도구로 빠르게 번호 조합을 만들 수 있습니다.",
"fr":"SoftGlow Loterie Mondiale met à jour automatiquement chaque jour les derniers numéros gagnants de 15 grandes loteries mondiales, dont Powerball et Mega Millions aux États-Unis, EuroMillions et UK Lotto en Europe, ainsi que les loteries taïwanaises. Chaque loterie propose des résultats, un historique des tirages et des analyses statistiques, avec 12 générateurs de numéros gratuits en ligne.",
"de":"SoftGlow Globale Lotterie aktualisiert täglich automatisch die neuesten Gewinnzahlen von 15 großen Lotterien weltweit, darunter Powerball und Mega Millions in den USA, EuroMillions und UK Lotto in Europa sowie taiwanesische Lotterien. Jede Lotterie bietet Ergebnisse, Ziehungshistorie und Zahlenstatistiken, ergänzt durch 12 kostenlose Online-Zahlengeneratoren.",
"es":"SoftGlow Lotería Global actualiza automáticamente cada día los últimos números ganadores de 15 grandes loterías mundiales, incluyendo Powerball y Mega Millions en EE.UU., EuroMillions y UK Lotto en Europa, y loterías taiwanesas. Cada lotería incluye resultados, historial de sorteos y análisis estadístico, junto con 12 generadores de números gratuitos en línea.",
"pt":"SoftGlow Loteria Global atualiza automaticamente todos os dias os últimos números sorteados de 15 grandes loterias mundiais, incluindo Powerball e Mega Millions nos EUA, EuroMillions e UK Lotto na Europa, e loterias taiwanesas. Cada loteria inclui resultados, histórico de sorteios e análise estatística, além de 12 geradores de números gratuitos online.",
"id":"SoftGlow Lotere Global secara otomatis memperbarui nomor kemenangan terbaru dari 15 lotere besar dunia setiap hari, termasuk Powerball dan Mega Millions di AS, EuroMillions dan UK Lotto di Eropa, serta lotere Taiwan. Setiap lotere menyediakan hasil, riwayat undian, dan analisis statistik, dilengkapi 12 generator nomor gratis online.",
}
