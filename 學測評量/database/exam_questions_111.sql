-- ============================================================
-- exam_questions：國中教育會考考古題（跨課次，不掛在單一curriculum lesson下）
-- 跟 questions 表分開的原因：questions.curriculum_id 是 not null，
-- 但會考題目是跨三年課程的綜合應用題，無法對應到單一課次，
-- 所以新開一張表，不硬塞進 questions（照schema設計原則：每張表各司其職）
-- ============================================================

create table if not exists exam_questions (
  id              uuid primary key default gen_random_uuid(),
  exam_name       text not null,          -- 例如 '111年國中教育會考'
  subject         text not null,          -- 'chinese' | 'math' | ...
  question_number smallint not null,
  question_text   text not null,
  options         jsonb not null,
  correct_option  text,
  has_figure      boolean not null default false,
  created_at      timestamptz not null default now(),
  unique (exam_name, subject, question_number)
);

insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  1,
  '這張圖最可能在傳達下列何種訊息？',
  '[{"key": "A", "text": "透過大量傳播，知識就會變成真理"}, {"key": "B", "text": "與其獨自苦讀，不如多與他人交流"}, {"key": "C", "text": "反覆誦讀，有助於將資訊內化為大腦深層的記憶"}, {"key": "D", "text": "能統整所學並轉述給別人，才算是真正掌握知識"}]'::jsonb,
  'D',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  2,
  '黃醫師的眼科診所開業，親友們登門慶賀。君翰帶來一方寫著「杏林之
光」的匾額，聊表心意。思涵見狀馬上說：「如果寫『近悅遠來』更好。」
偉同則說：「可是，我覺得『眾望所歸』更恰當。」最後嘉恩才說：「其
實，『桃李芬芳』才是最合適的選擇。」
根據這段對話，誰的做法或說法最恰當？',
  '[{"key": "A", "text": "君翰"}, {"key": "B", "text": "思涵"}, {"key": "C", "text": "偉同"}, {"key": "D", "text": "嘉恩"}]'::jsonb,
  'A',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  3,
  '「臺灣原住民的布只有形制屬傳統或較現代的分別，像圓領的剪裁、鈕扣和棉布的使
用等，都是受漢人的影響而來。泰雅族的貝珠鈴衣，是貝珠串底下加銅鈴裝飾，銅
鈴也是和漢人交易而來。日治時代的原住民服裝，還出現以漢人棉布做底、日本布
做袖口、原住民圖案做主要裝飾的混搭法。」這段文字的主旨最可能是下列何者？',
  '[{"key": "A", "text": "不同文化的碰撞，可融合並產生新的火花"}, {"key": "B", "text": "外來文化的入侵，讓在地的傳統文化日漸消失"}, {"key": "C", "text": "臺灣原住民的文化，影響了漢人與日本人的穿著"}, {"key": "D", "text": "觀察不同族群的服飾，就能了解不同文化的差異"}]'::jsonb,
  'A',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  4,
  '下表中的「獸」字依序最可能為何種字體？',
  '[{"key": "A", "text": "金文 → 楷書 → 小篆 → 隸書"}, {"key": "B", "text": "金文 → 小篆 → 隸書 → 楷書"}, {"key": "C", "text": "小篆 → 隸書 → 金文 → 楷書"}, {"key": "D", "text": "小篆 → 金文 → 楷書 → 隸書"}]'::jsonb,
  'B',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  5,
  '「過去賭客玩拉霸機時，需要把紙鈔塞進機器裡，所以會看見皮夾裡的鈔票越
來越少，能提醒自己適時收手。但現在他們用卡片玩拉霸機，卡片僅會記錄
他們的輸贏情況。賭客難以意識到自己正不斷輸錢，只能隱約記得花了多少
錢。」這段文字的主旨與下列何者最接近？',
  '[{"key": "A", "text": "欲望會創造新的發明"}, {"key": "B", "text": "科技的進步使生活更便利"}, {"key": "C", "text": "長期沉溺於賭博之中容易讓人迷失自我"}, {"key": "D", "text": "不用現金支付使人對花錢的感受變得較遲鈍"}]'::jsonb,
  'D',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  6,
  '下列體育新聞的說明何者錯誤？',
  '[{"key": "A", "text": "東道主法國隊屈居第二：法國是主辦國"}, {"key": "B", "text": "我國九局下逆轉，一分氣走韓國：我國轉輸為贏"}, {"key": "C", "text": "波多黎各選手爆冷門奪金：各界看好波多黎各選手奪金"}, {"key": "D", "text": "我國女將輕取哥倫比亞，晉級八強：我國女將大勝哥倫比亞"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  7,
  '「敘述記憶是件難事。記憶是一個整體，敘述的時候必須選擇將它一片片的切
下，即使是一塊肉、一棵菜甲甲切下來後就再也拼不完整了，就算拼湊起來了乙乙
也只算是死的標本，生命已蕩然丙丙何況記憶大部分的時候更像一陣風，來無影
去無蹤的，要想將風片切下來，豈不完全是一場徒勞嗎丁丁」這段文字中的甲、
乙、丙、丁四處，何者最適合使用標點符號中的句號？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  8,
  '陸公嘗於市遇一佳硯，議價未定。既還邸，使門人往，以一金易歸。門
人持硯歸，公訝其不類。門人堅證其是。公曰：「向觀硯有鴝鵒眼，今何無
之？」答曰：「吾嫌其微凸，路遇石工，令磨而平之。」公大惋惜。
下列關於故事中人物的敘述，何者最恰當？',
  '[{"key": "A", "text": "門人買錯硯臺卻不知道"}, {"key": "B", "text": "陸公惋惜是因石工技藝不佳"}, {"key": "C", "text": "門人請人磨平硯眼是自作聰明"}, {"key": "D", "text": "陸公對門人購硯的價格感到驚訝"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  9,
  '「美國有名男子在家中裝攝影機，24小時在網路上播放他的生活，因此成為
名人，甚且登上雜誌封面。這透露著有些人不再介意被窺視，甚至樂於被窺
視。人有時會覺得孤寂，希望被注意，讓人覺得自己很重要。那些被窺視的
人，既然知道鏡頭在哪裡，是否會有表演的性質呢？」根據這段文字，下列
何者最接近作者的觀點？',
  '[{"key": "A", "text": "大眾的隱私權常常不受到尊重"}, {"key": "B", "text": "網路直播者多少帶有表演性質"}, {"key": "C", "text": "滿足他人偷窺欲就可成為名人"}, {"key": "D", "text": "孤寂的人總是害怕他人的眼光"}]'::jsonb,
  'B',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  10,
  '「名不可以倖取也。天下之事，固有外似而中實不然者。倖其似而竊其名，非
不可以欺一時，然他日人即其似而求其真，則情現實吐，無不立敗。」下列
何者最能與這段文字的意旨相呼應？',
  '[{"key": "A", "text": "因其貌不揚被小看，沒想到靠著精湛演技成為影帝"}, {"key": "B", "text": "不勞而獲的錢財，因為來得容易，往往被輕易揮霍"}, {"key": "C", "text": "以作弊手段考上名校，最後卻因適應不良而中輟學業"}, {"key": "D", "text": "當不切實際的夢想碰到冷酷的現實，也只能化為泡影"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  12,
  '下列選項「」中的字，何組讀音相同？',
  '[{"key": "A", "text": "悲傷哽「咽」／食不下「咽」"}, {"key": "B", "text": "悶不「吭」聲／引「吭」高歌"}, {"key": "C", "text": "語帶「禪」機／「禪」讓政治"}, {"key": "D", "text": "「撒」謊成習／恃寵「撒」嬌"}]'::jsonb,
  'D',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  13,
  '「所謂中菜西吃，是將原本大盤共享且同桌擺放的宴席菜式，改為西餐般一人一
份、一道道依序送上。但中菜向來比西菜更講究沸熱燙口，分開上菜後，熱度鑊
氣全消。其次，拋卻一桌多道同食，享受各種味道交錯的樂趣。更嚴重的是，
為了美觀便利，連烹調手法都起了變化。例如原本該整魚整肉整蔬大鍋蒸煮煨
燉，卻改為小塊小盅個別處理，光這點就足以讓同冶一爐、渾然一體之味傷損逸
散。」根據這段文字，作者不愛中菜西吃的原因最不可能包含下列何者？',
  '[{"key": "A", "text": "中式食法多道並陳，西式則否"}, {"key": "B", "text": "中菜較西菜更講究菜餚的熱度"}, {"key": "C", "text": "西餐的上菜速度及料理方式費時又費工"}, {"key": "D", "text": "西式食法盡失中菜大鍋烹煮整肉的風味"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  14,
  '「修身以為弓，矯思以為矢，立義以為的，定而後發，發必中矣。」句中「矯」
字的意義，與下列何者最接近？',
  '[{"key": "A", "text": "「矯」世勵俗"}, {"key": "B", "text": "「矯」若遊龍"}, {"key": "C", "text": "「矯」捷身手"}, {"key": "D", "text": "「矯」託天命"}]'::jsonb,
  'A',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  15,
  '下列文句中的成語，何者使用最恰當？',
  '[{"key": "A", "text": "這艘郵輪車水馬龍，可搭載數千名遊客"}, {"key": "B", "text": "他個性害羞，遇到陌生人時總是別開生面"}, {"key": "C", "text": "他為了得到好成績而因噎廢食，每晚都認真讀書"}, {"key": "D", "text": "這裡曾有許多珍藏，如今僅剩吉光片羽，令人唏噓"}]'::jsonb,
  'D',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  16,
  '某古典戲曲中有一段唱詞：「俺讀些稗官詞寄牢騷，對江山吃一斗苦松醪 。
1
小鼓兒顫杖輕敲，寸板兒軟手頻搖。一字字臣忠子孝，一聲聲龍吟虎嘯。快舌
尖鋼刀出鞘，響喉嚨轟雷烈炮。呀！似這般冷嘲、熱挑，用不著筆抄、墨描，勸
英豪一盤錯帳速勾了。」據此判斷，唱詞中「俺」的職業最可能是下列何者？',
  '[{"key": "A", "text": "說書人"}, {"key": "B", "text": "算命師"}, {"key": "C", "text": "外交使臣"}, {"key": "D", "text": "監察御史"}]'::jsonb,
  'A',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  17,
  '下列文句，何者文意通暢、用詞最為恰當？',
  '[{"key": "A", "text": "此文件攸關計畫的成敗，你千萬要小心遞送"}, {"key": "B", "text": "在遇到困難時，他反而不屈不撓，堅持妥協"}, {"key": "C", "text": "他明明做錯事情還推給別人，真是死不賴帳"}, {"key": "D", "text": "疫情蔓延的時候，我們更要一起對抗意志力"}]'::jsonb,
  'A',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  18,
  '「粥之既熟，水米成交，猶米之釀而為酒矣。慮其太厚而入水於粥，猶入水於酒
也，水入而酒成糟粕，其味尚可咀乎？故熬前挹水必限以數，使其勺不能增，
滴無可減。」根據這段文字，作者對於熬粥的看法，下列敘述何者最恰當？',
  '[{"key": "A", "text": "熬煮前須加足適量的水"}, {"key": "B", "text": "熬煮時可適度添加米飯"}, {"key": "C", "text": "熬煮過程中可加酒提味"}, {"key": "D", "text": "熬煮過久容易生出糟粕"}]'::jsonb,
  'A',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  19,
  '下列詞語「」中的注音寫成國字後，何者兩兩相同？',
  '[{"key": "A", "text": "杞人「ㄧㄡ」天／養尊處「ㄧㄡ」"}, {"key": "B", "text": "「ㄅㄢ」駁陸離／「ㄅㄢ」斕奪目"}, {"key": "C", "text": "自相「ㄇㄠˊ」盾／「ㄇㄠˊ」塞頓開"}, {"key": "D", "text": "細嚼「ㄇㄢˋ」嚥／「ㄇㄢˋ」不經心"}]'::jsonb,
  'B',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  20,
  '「江南二月試羅衣 ，春盡燕山雪尚飛。應是子規 啼不到，故鄉雖好不思歸。」
1 2
關於這首詩的分析，下列說明何者最恰當？
',
  '[{"key": "A", "text": "就體裁而言，這是一首七言律詩"}, {"key": "B", "text": "就形式而言，對仗工整，句句押韻"}, {"key": "C", "text": "以「試羅衣」、「雪尚飛」對比兩地氣候差異"}, {"key": "D", "text": "以遊子口吻寫出羈旅在外、難以返回的鄉愁"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  22,
  '「學者如取水，終日取而不能踰其量，故操瓢者止於瓢，操盎者止於盎；教者如分
火，終日分而未嘗虧其體，故散為十燈而明自若，散為千燈而明自若。故善學者
________，善教者________。」根據文意脈絡，畫線處依序填入下列何者最恰當？',
  '[{"key": "A", "text": "不自隘其器／不自吝其光"}, {"key": "B", "text": "如逆水行舟／似雪中取火"}, {"key": "C", "text": "宜自知其量／宜自晦其光"}, {"key": "D", "text": "無一時之患／有終身之憂"}]'::jsonb,
  'A',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  23,
  '莊子釣於濮水，楚王使大夫二人往先焉，曰：「願以境內累矣 ！」莊子持
1
竿不顧，曰：「吾聞楚有神龜，死已三千歲矣，王巾笥 而藏之廟堂之上。
2
此龜者，寧其死為留骨而貴乎，寧其生而曳尾於塗中乎？」二大夫曰：「寧
生而曳尾塗中。」莊子曰：「往矣！吾將曳尾於塗中。」
根據這段文字，下列何者與莊子的想法最接近？',
  '[{"key": "A", "text": "人死留名，虎死留皮"}, {"key": "B", "text": "不慕榮利，唯願逍遙"}, {"key": "C", "text": "神龜雖壽，猶有竟時"}, {"key": "D", "text": "寧鳴而死，不默而生"}]'::jsonb,
  'B',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  24,
  '「世人之事君者，皆以孫叔敖之遇楚莊王為幸，自有道者論之則不然，此楚國
之幸。楚莊王好周遊田獵，馳騁弋射，歡樂無遺，盡付其境內之勞與諸侯之
憂於孫叔敖。孫叔敖日夜不息，不得顧及養生之事，故使莊王功績著乎竹
帛，傳乎後世。」關於這段文字的寫作手法，下列說明何者最恰當？',
  '[{"key": "A", "text": "先提出世俗看法，再以不同論點反駁"}, {"key": "B", "text": "先從正、反兩面論述，再另舉他例說明"}, {"key": "C", "text": "先記敘孫叔敖事蹟，再評論楚莊王功績"}, {"key": "D", "text": "先以楚莊王觀點闡述，再從孫叔敖立場反駁"}]'::jsonb,
  'A',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  25,
  '【甲】 【乙】
衛福部公布107年國人
107
十大死因：與十年前相較，
癌症與心臟疾病依舊高居死
因前兩位，糖尿病、事故傷
害、慢性下呼吸道疾病順位
不變，肺炎、高血壓性疾
病、腎臟疾病順位上升，腦
血管疾病、慢性肝病與蓄意
自我傷害順位下降。
根據甲、乙兩項資料，關於民國97年國人主要死亡原因，無法明確推論出下
列何者？',
  '[{"key": "A", "text": "慢性肝病為當時國人十大死因之一"}, {"key": "B", "text": "腦血管疾病為當時國人第三大死因"}, {"key": "C", "text": "蓄意自我傷害為當時國人十大死因之一"}, {"key": "D", "text": "肺炎、高血壓性疾病、腎臟疾病皆為當時國人十大死因"}]'::jsonb,
  'D',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  26,
  '根據這張海報，下列關於綠能家電診所維修內容的敘述，何者最恰當？',
  '[{"key": "A", "text": "可電話預約時間，專人到府收件"}, {"key": "B", "text": "維修費用依家電的大小而有不同"}, {"key": "C", "text": "只要維修合於規定的家電，都需繳交工本費"}, {"key": "D", "text": "領件時若未攜帶取貨聯單，可以維修單代替"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  27,
  '下列四人聲稱曾到綠能家電診所送修電器，何人所述與這張海報的內容最相
符？',
  '[{"key": "A", "text": "小強：週一 14：00 送修咖啡機，週四 09：00 就拿到了"}, {"key": "B", "text": "小顏：週三 10：00 送修飲水機，週五 13：00 就領件了"}, {"key": "C", "text": "小燕：週六 16：00 送修電子鍋，接到通知後憑取貨聯單領回"}, {"key": "D", "text": "小龍：週二 08：00 送修熱水瓶，先繳交50元特殊材料費才能檢修"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  28,
  '根據本文，關於畫線處所象徵的意義，下列說明何者最不恰當？',
  '[{"key": "A", "text": "甲句中「每一個坑洞」：人生不同的挑戰"}, {"key": "B", "text": "乙句中「方正的直角」：作者獨特的個性"}, {"key": "C", "text": "丙句中「紙」：作者自己的本質"}, {"key": "D", "text": "丁句中「蟑螂」：卑鄙惡劣的個人特質"}]'::jsonb,
  'D',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  29,
  '作者透過本文所抒發的感慨，與下列何者最接近？',
  '[{"key": "A", "text": "要到失去之後，才知道曾經擁有的美好"}, {"key": "B", "text": "為了他人而改變自己，最後卻迷失自我"}, {"key": "C", "text": "年輕時未確定方向，等到一事無成才後悔莫及"}, {"key": "D", "text": "曾經轟轟烈烈的絢爛，誰知到頭來都是一場空"}]'::jsonb,
  'B',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  30,
  '關於小說中畫線處文句的說明，下列何者最恰當？',
  '[{"key": "A", "text": "甲：政府對人民的監控就像陽光一樣無孔不入"}, {"key": "B", "text": "乙：長時間的緊繃，讓人變得冷酷麻木"}, {"key": "C", "text": "丙：政府假稱瘟疫以掩蓋屠殺人民的真相"}, {"key": "D", "text": "丁：巡邏隊刻意威嚇居民，製造恐懼與猜疑"}]'::jsonb,
  'B',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  31,
  '對小說中的政府而言，「最壞情況」所指的最可能是下列何者？',
  '[{"key": "A", "text": "人心彼此猜疑，不再相互信任"}, {"key": "B", "text": "氣溫持續上升，民眾難以忍受"}, {"key": "C", "text": "疫情不斷惡化，人們失去求生欲"}, {"key": "D", "text": "群眾發生暴動，突破城門封鎖線"}]'::jsonb,
  'D',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  32,
  '根據本文，關於美秀美術館，最不可能推論出下列何者？',
  '[{"key": "A", "text": "美術館坐落在山間"}, {"key": "B", "text": "對環境清潔有高度的要求"}, {"key": "C", "text": "館區的電動車由機械人駕駛"}, {"key": "D", "text": "接待中心與美術館有一段距離"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  33,
  '根據本文，下列何者最能體現美秀美術館的烏托邦式美學？',
  '[{"key": "A", "text": "工作人員親切的微笑，流露內心的祥和"}, {"key": "B", "text": "降低人為聲音的干擾，以呈現寧靜氛圍"}, {"key": "C", "text": "所有物件一律為白色，象徵藝術的純淨"}, {"key": "D", "text": "讓觀眾貼近展品，顯現人與藝術無隔閡"}]'::jsonb,
  'B',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  34,
  '根據本文，作者認為紙本書對一般人的獨特價值最可能是下列何者？',
  '[{"key": "A", "text": "紙本書才能傳承經典與藝術"}, {"key": "B", "text": "閱讀紙本書不受晝夜的限制"}, {"key": "C", "text": "紙本書可讓文字散發不同的渲染力"}, {"key": "D", "text": "城鄉數位落差因紙本書才得以彌補"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  35,
  '關於本文的寫作分析，下列敘述何者最恰當？',
  '[{"key": "A", "text": "以多面向的特質比較來強調數位資訊不如紙本"}, {"key": "B", "text": "用夜以繼日來說明紙本閱讀是數位閱讀的延續"}, {"key": "C", "text": "透過圖表的分析，陳述紙本閱讀無限發展的可能"}, {"key": "D", "text": "藉由晝夜的對照，表達紙本與數位閱讀應該並存"}]'::jsonb,
  'D',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  36,
  '假設右圖是寓言中所指的洞穴，則根據寓言
的內容，甲、乙、丙三處依序最可能是下列
何者？',
  '[{"key": "A", "text": "被鍊著的人／營火／舉雕像的人"}, {"key": "B", "text": "被鍊著的人／舉雕像的人／營火"}, {"key": "C", "text": "舉雕像的人／營火／被鍊著的人"}, {"key": "D", "text": "舉雕像的人／被鍊著的人／營火"}]'::jsonb,
  'B',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  37,
  '在這則寓言中，「這個走出洞穴後再回到洞內的人」最可能是象徵下列哪一種
人？',
  '[{"key": "A", "text": "受迫的奴隸"}, {"key": "B", "text": "孤獨的先知"}, {"key": "C", "text": "命運的主宰"}, {"key": "D", "text": "蒙昧的愚者"}]'::jsonb,
  'B',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  38,
  '根據這則寓言，下列何者最接近柏拉圖的想法？',
  '[{"key": "A", "text": "多數人相信的事未必為真"}, {"key": "B", "text": "自以為是往往會招致滅亡"}, {"key": "C", "text": "面向陽光，影子就會在你背後"}, {"key": "D", "text": "堅定信仰，心靈才能得到自由"}]'::jsonb,
  'A',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  39,
  '根據甲、乙兩文推論，漢文帝時各種錢幣的重量依序最可能是下列何者？',
  '[{"key": "A", "text": "四銖錢 ＞ 吳錢 ＞ 鄧通錢"}, {"key": "B", "text": "四銖錢 ＝ 鄧通錢 ＞ 吳錢"}, {"key": "C", "text": "吳錢 ＞ 四銖錢 ＞ 鄧通錢"}, {"key": "D", "text": "吳錢 ＞ 鄧通錢 ＝ 四銖錢"}]'::jsonb,
  'D',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  40,
  '根據甲、乙兩文，下列敘述何者最恰當？',
  '[{"key": "A", "text": "鄧通與吳王同時自鑄莢錢，導致莢錢過多"}, {"key": "B", "text": "鄧通與吳王所鑄銅錢上應有「半兩」字樣"}, {"key": "C", "text": "鄧通叛逆謀反，文帝遂下令禁止私鑄銅錢"}, {"key": "D", "text": "鄧通所鑄錢布天下，故文帝賜其銅山一座"}]'::jsonb,
  'B',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  41,
  '根據本文，下列文句省略的主語，何者是白敏中？',
  '[{"key": "A", "text": "病其與賀拔惎為友"}, {"key": "B", "text": "乃密令門人申意"}, {"key": "C", "text": "悉以實告"}, {"key": "D", "text": "大怒而去"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  42,
  '根據本文，王起說：「我原只得白敏中，今當更取賀拔惎矣。」這句話的原因，
最可能是下列何者？',
  '[{"key": "A", "text": "白敏中向王起推薦賀拔惎取代自己"}, {"key": "B", "text": "賀拔惎已知此次科考內幕，只好破格錄取封口"}, {"key": "C", "text": "比起白敏中的前倨後恭，賀拔惎的真誠顯得更為可貴"}, {"key": "D", "text": "白敏中把賀拔惎看得比狀元還重，可知賀拔惎有過人之處"}]'::jsonb,
  'D',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  1,
  '圖 ( 一 ) 數線上的 A、B、C、D 四點所表示的數分別為 a、b、c、d，且 O 為
原點。根據圖中各點的位置判斷，下列何者的值最小？',
  '[{"key": "A", "text": "a"}, {"key": "B", "text": "b"}, {"key": "C", "text": "c"}, {"key": "D", "text": "d"}]'::jsonb,
  'A',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  2,
  '計算多項式 6x2 + 4x 除以 2x2 後，得到的餘式為何？',
  '[{"key": "A", "text": "2"}, {"key": "B", "text": "4"}, {"key": "C", "text": "2x"}, {"key": "D", "text": "4x"}]'::jsonb,
  'D',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  3,
  '下列何者為 156 的質因數？',
  '[{"key": "A", "text": "11"}, {"key": "B", "text": "12"}, {"key": "C", "text": "13"}, {"key": "D", "text": "14"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  4,
  '圖 ( 二 ) 為一個長方體的展開圖，且長方體的底面為
正方形。根據圖中標示的長度，求此長方體的體積
為何？',
  '[{"key": "A", "text": "144"}, {"key": "B", "text": "224"}, {"key": "C", "text": "264"}, {"key": "D", "text": "300"}]'::jsonb,
  'B',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  5,
  '算式 + − ( − ) 之值為何？
22 18 22 18
4',
  '[{"key": "A", "text": "11"}, {"key": "B", "text": "10"}, {"key": "C", "text": "9"}, {"key": "D", "text": "4"}]'::jsonb,
  'A',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  6,
  '2022 的值介於下列哪兩個數之間？',
  '[{"key": "A", "text": "25，30"}, {"key": "B", "text": "30，35"}, {"key": "C", "text": "35，40"}, {"key": "D", "text": "40，45"}]'::jsonb,
  'D',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  7,
  '已知坐標平面上有一直線 L 與一點 A。若 L 的方程式為 x = −2，A 點坐標為
(6,5)，則 A 點到直線 L 的距離為何？',
  '[{"key": "A", "text": "3"}, {"key": "B", "text": "4"}, {"key": "C", "text": "7"}, {"key": "D", "text": "8"}]'::jsonb,
  'D',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  8,
  '多項式 39x2 + 5x −14 可因式分解成 ( 3x + a )( bx + c )，其中 a、b、c 均為
整數，求 a + 2c 之值為何？',
  '[{"key": "A", "text": "−12"}, {"key": "B", "text": "−3"}, {"key": "C", "text": "3"}, {"key": "D", "text": "12"}]'::jsonb,
  'A',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  9,
  '箱子內有分別標示號碼 1 ~ 6 的球，每個號碼各 2 顆，總共 12 顆。已知小茹先
從箱內抽出 5 顆球且不將球放回箱內，這 5 顆球的號碼分別是 1、 2、2、3、5。
今阿純打算從此箱內剩下的球中抽出 1 顆球，若箱內剩下的每顆球被他抽出
的機會相等，則他抽出的球的號碼，與小茹已抽出的 5 顆球中任意一顆球
的號碼相同的機率是多少？
3',
  '[{"key": "A", "text": "6"}, {"key": "B", "text": "6"}, {"key": "C", "text": "7"}, {"key": "D", "text": "7"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  10,
  '已知一元二次方程式 ( x − 2 )2 = 3 的兩根為 a、b，且 a > b，求 2a + b 之值
為何？',
  '[{"key": "A", "text": "9"}, {"key": "B", "text": "−3"}, {"key": "C", "text": "6 + 3"}, {"key": "D", "text": "−6 + 3"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  11,
  '根據圖 ( 三 ) 中兩人的對話紀錄，求
出哥哥買遊戲機的預算為多少元？
(cid:9420)(cid:9420)',
  '[{"key": "A", "text": "3800"}, {"key": "B", "text": "4800"}, {"key": "C", "text": "5800"}, {"key": "D", "text": "6800"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  12,
  '已知 p = 7.52 × 10 − 6，下列關於 p 值的敘述何者正確？',
  '[{"key": "A", "text": "小於 0"}, {"key": "B", "text": "介於 0 與 1 兩數之間，兩數中比較接近 0"}, {"key": "C", "text": "介於 0 與 1 兩數之間，兩數中比較接近 1"}, {"key": "D", "text": "大於 1"}]'::jsonb,
  'B',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  13,
  '如圖 ( 四 )，AB 為圓 O 的一弦，且 C 點在 AB 上。若 AC = 6，
BC = 2，AB 的弦心距為 3，則 OC 的長度為何？',
  '[{"key": "A", "text": "3"}, {"key": "B", "text": "4"}, {"key": "C", "text": "11"}]'::jsonb,
  'D',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  14,
  '某國主計處調查 2017 年該國所有受僱員工的年薪資料，並公布調查結果如
圖 ( 五 ) 的直方圖所示。
2017(cid:1283)(cid:1689)(cid:4287)(cid:2473)(cid:960)(cid:1283)(cid:5522)(cid:1001)(cid:1138)
120 (cid:1139)(cid:1441)(cid:4775)
100
100
60(cid:4068)(cid:993)
80 8080
80
65
60
45
40 40
40
30
25
20 18
20 5 5 10 16 1412 10 9 8 8 7 6
0
12 0 24 36 48 60 72 84 96 108 120 132 144
圖(五)
已知總調查人數為 750 萬人，根據圖中資訊計算，該國受僱員工年薪低於平均數
的人數占總調查人數的百分率為下列何者？',
  '[{"key": "A", "text": "6%"}, {"key": "B", "text": "50%"}, {"key": "C", "text": "68%"}, {"key": "D", "text": "73%"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  15,
  '如圖 ( 六 )，∆ABC 中，D 點在 AB 上，E 點在 BC 上，DE 為 AB 的中垂線。若
∠B = ∠C，且 ∠EAC > 90°，則根據圖中標示的角， 判斷下列敘述何者正確？',
  '[{"key": "A", "text": "∠1 = ∠2，∠1 < ∠3"}, {"key": "B", "text": "∠1 = ∠2，∠1 > ∠3"}, {"key": "C", "text": "∠1 ≠ ∠2，∠1 < ∠3"}, {"key": "D", "text": "∠1 ≠ ∠2，∠1 > ∠3"}]'::jsonb,
  'B',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  16,
  '緩降機是火災發生時避難的逃生設備， (cid:4117)(cid:1254)(cid:2190) ((cid:3394)(cid:1359)(cid:59)(cid:998)(cid:1025))
0.4
圖 ( 七 ) 是廠商提供的緩降機安裝示意
(cid:1005)(cid:5449)
圖，圖中呈現在三樓安裝緩降機時，使 (cid:4887)(cid:2398)(cid:5138)(cid:1068)(cid:6223)
1.6 (cid:1276)(cid:1220)(cid:2981)
用此緩降機直接緩降到一樓地面的所需
(cid:927)(cid:4788)
繩長 ( 不計安全帶 )。若某棟建築的每個
(cid:4054)
樓層高度皆為 3 公尺，則根據圖 ( 七 ) (cid:914) (cid:5445)
(cid:4887)(cid:4887) (cid:4788)
的安裝方式在該建築八樓安裝緩降機 (cid:5859)(cid:951)
(cid:2398)(cid:2398) (cid:2863) (cid:1804)
時，使用此緩降機直接緩降到一樓地面 (cid:5138)(cid:5138) (cid:2123) (cid:4641)
(cid:5859)
的所需繩長 ( 不計安全帶 ) 為多少公尺？ (cid:1276)(cid:1276) (cid:914)(cid:4788) (cid:1999)
(cid:4152)(cid:4152)',
  '[{"key": "D", "text": "25.6"}]'::jsonb,
  'A',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  17,
  '圖 ( 八 ) 為兩直線 L、M 與 ∆ABC 相交的情形，其中
L、M 分別與 BC、AB 平行。根據圖中標示的角度，
求 ∠B 的度數為何？',
  '[{"key": "A", "text": "55"}, {"key": "B", "text": "60"}, {"key": "C", "text": "65"}, {"key": "D", "text": "70"}]'::jsonb,
  'A',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  18,
  '某鞋店正舉辦開學特惠活動，圖 ( 九 ) 為活動說明。
圖(九)
小徹打算在該店同時購買一雙球鞋及一雙皮鞋，且他有一張所有購買的商品
定價皆打 8 折的折價券。若小徹計算後發現使用折價券與參加特惠活動兩者
的花費相差 50 元，則下列敘述何者正確？',
  '[{"key": "A", "text": "使用折價券的花費較少，且兩雙鞋的定價相差 100 元"}, {"key": "B", "text": "使用折價券的花費較少，且兩雙鞋的定價相差 250 元"}, {"key": "C", "text": "參加特惠活動的花費較少，且兩雙鞋的定價相差 100 元"}, {"key": "D", "text": "參加特惠活動的花費較少，且兩雙鞋的定價相差 250 元"}]'::jsonb,
  'B',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  19,
  '如 圖 ( 十 )，∆ABC 的 重 心 為 G， BC 的
中點為 D， 今以 G 為圓心， GD 長為半徑
畫一圓，且作 A 點到圓 G 的兩切線段 AE、
AF，其中 E、F 均為切點。根據圖中標示的
角與角度，求 ∠1 與 ∠2 的度數和為多少？',
  '[{"key": "B", "text": "35"}, {"key": "C", "text": "40"}, {"key": "D", "text": "45"}]'::jsonb,
  'B',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  20,
  '圖 ( 十一 ) 為一張正三角形紙片 ABC，其中 D 點在 AB 上，E 點在 BC 上。
今以 DE 為摺線將 B 點往右摺後，BD、BE 分別與 AC 相交於 F 點、G 點，
如圖 ( 十二 ) 所示。若 AD = 10，AF = 16，DF = 14，BF = 8，則 CG 的長度
為多少？',
  '[{"key": "A", "text": "7"}, {"key": "B", "text": "8"}, {"key": "C", "text": "9"}, {"key": "D", "text": "10"}]'::jsonb,
  'C',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  21,
  '有一直徑為 AB 的圓，且圓上有 C、D、E、F 四點，
其位置如圖 ( 十三 ) 所示。若 AC = 6， AD = 8，
AE = 5，AF = 9，AB = 10，則下列弧長關係何者
正確？',
  '[{"key": "A", "text": "AC + AD = AB，AE + AF = AB"}, {"key": "B", "text": "AC + AD = AB，AE + AF ≠ AB"}, {"key": "C", "text": "AC + AD ≠ AB，AE + AF = AB"}, {"key": "D", "text": "AC + AD ≠ AB，AE + AF ≠ AB"}]'::jsonb,
  'B',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  23,
  '∆ABC 的邊上有 D、E、F 三點，各點位置如圖( 十四 ) 所示。若 ∠B = ∠FAC，
BD = AC，∠BDE = ∠C，則根據圖中標示的長度，求四邊形 ADEF 與
∆ABC 的面積比為何？',
  '[{"key": "A", "text": "1 : 3"}, {"key": "B", "text": "1 : 4"}, {"key": "C", "text": "2 : 5"}, {"key": "D", "text": "3 : 8"}]'::jsonb,
  'D',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  24,
  '已知日光燈管的發光效率為光通量與功率的比值， 甲、 乙兩人根據表 ( 一 )、
表 ( 二 ) 的資訊提出以下看法：
( 甲 ) PA-20 日光燈管的發光效率比 PB-14 日光燈管高
( 乙 ) PA 日光燈管中，功率較大的燈管其發光效率較高
關於甲、乙兩人的看法，下列敘述何者正確？',
  '[{"key": "A", "text": "甲、乙皆正確"}, {"key": "B", "text": "甲、乙皆錯誤"}, {"key": "C", "text": "甲正確，乙錯誤"}, {"key": "D", "text": "甲錯誤，乙正確"}]'::jsonb,
  'D',
  false
);
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  25,
  '有一間公司請水電工程廠商安裝日光燈管， 廠商提供兩種方案如表(三)所示。
表(三)
(cid:1041)(cid:2594) (cid:2172)(cid:960)(cid:995)(cid:2514) (cid:2172)(cid:960)(cid:3748)(cid:1172) (cid:1430)(cid:1527)(cid:2577)(cid:3748)
( )
(cid:2935)(cid:1153)(cid:1041)(cid:2594) (cid:1276)(cid:4152)90(cid:1037)PA-40(cid:1042)(cid:1216)(cid:5161)(cid:4485) 45000(cid:993)
(cid:2282)(cid:4253)(cid:1041)(cid:2594) (cid:1276)(cid:4152)120(cid:1037)PB-28(cid:1042)(cid:1216)(cid:5161)(cid:4485) 60000(cid:993)
n
已知 n 支功率皆為 w 瓦的燈管都使用 t 小時後消耗的電能(度) = × w × t，
1000
若每支燈管使用時間皆相同， 且只考慮燈管消耗的電能並以每度 5 元計算電費，
則兩種方案相比，燈管使用時間至少要超過多少小時，採用省電方案所節省
的電費才會高於兩者相差的施工費用？',
  '[{"key": "A", "text": "12200"}, {"key": "B", "text": "12300"}, {"key": "C", "text": "12400"}, {"key": "D", "text": "12500"}]'::jsonb,
  'D',
  false
);
