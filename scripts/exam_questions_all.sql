create table if not exists exam_questions (
  id              uuid primary key default gen_random_uuid(),
  exam_name       text not null,
  subject         text not null,
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  4,
  '下表中的「獸」字依序最可能為何種字體？',
  '[{"key": "A", "text": "金文 → 楷書 → 小篆 → 隸書"}, {"key": "B", "text": "金文 → 小篆 → 隸書 → 楷書"}, {"key": "C", "text": "小篆 → 隸書 → 金文 → 楷書"}, {"key": "D", "text": "小篆 → 金文 → 楷書 → 隸書"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  6,
  '下列體育新聞的說明何者錯誤？',
  '[{"key": "A", "text": "東道主法國隊屈居第二：法國是主辦國"}, {"key": "B", "text": "我國九局下逆轉，一分氣走韓國：我國轉輸為贏"}, {"key": "C", "text": "波多黎各選手爆冷門奪金：各界看好波多黎各選手奪金"}, {"key": "D", "text": "我國女將輕取哥倫比亞，晉級八強：我國女將大勝哥倫比亞"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  12,
  '下列選項「」中的字，何組讀音相同？',
  '[{"key": "A", "text": "悲傷哽「咽」／食不下「咽」"}, {"key": "B", "text": "悶不「吭」聲／引「吭」高歌"}, {"key": "C", "text": "語帶「禪」機／「禪」讓政治"}, {"key": "D", "text": "「撒」謊成習／恃寵「撒」嬌"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  14,
  '「修身以為弓，矯思以為矢，立義以為的，定而後發，發必中矣。」句中「矯」
字的意義，與下列何者最接近？',
  '[{"key": "A", "text": "「矯」世勵俗"}, {"key": "B", "text": "「矯」若遊龍"}, {"key": "C", "text": "「矯」捷身手"}, {"key": "D", "text": "「矯」託天命"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  15,
  '下列文句中的成語，何者使用最恰當？',
  '[{"key": "A", "text": "這艘郵輪車水馬龍，可搭載數千名遊客"}, {"key": "B", "text": "他個性害羞，遇到陌生人時總是別開生面"}, {"key": "C", "text": "他為了得到好成績而因噎廢食，每晚都認真讀書"}, {"key": "D", "text": "這裡曾有許多珍藏，如今僅剩吉光片羽，令人唏噓"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  17,
  '下列文句，何者文意通暢、用詞最為恰當？',
  '[{"key": "A", "text": "此文件攸關計畫的成敗，你千萬要小心遞送"}, {"key": "B", "text": "在遇到困難時，他反而不屈不撓，堅持妥協"}, {"key": "C", "text": "他明明做錯事情還推給別人，真是死不賴帳"}, {"key": "D", "text": "疫情蔓延的時候，我們更要一起對抗意志力"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  19,
  '下列詞語「」中的注音寫成國字後，何者兩兩相同？',
  '[{"key": "A", "text": "杞人「ㄧㄡ」天／養尊處「ㄧㄡ」"}, {"key": "B", "text": "「ㄅㄢ」駁陸離／「ㄅㄢ」斕奪目"}, {"key": "C", "text": "自相「ㄇㄠˊ」盾／「ㄇㄠˊ」塞頓開"}, {"key": "D", "text": "細嚼「ㄇㄢˋ」嚥／「ㄇㄢˋ」不經心"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  26,
  '根據這張海報，下列關於綠能家電診所維修內容的敘述，何者最恰當？',
  '[{"key": "A", "text": "可電話預約時間，專人到府收件"}, {"key": "B", "text": "維修費用依家電的大小而有不同"}, {"key": "C", "text": "只要維修合於規定的家電，都需繳交工本費"}, {"key": "D", "text": "領件時若未攜帶取貨聯單，可以維修單代替"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  27,
  '下列四人聲稱曾到綠能家電診所送修電器，何人所述與這張海報的內容最相
符？',
  '[{"key": "A", "text": "小強：週一 14：00 送修咖啡機，週四 09：00 就拿到了"}, {"key": "B", "text": "小顏：週三 10：00 送修飲水機，週五 13：00 就領件了"}, {"key": "C", "text": "小燕：週六 16：00 送修電子鍋，接到通知後憑取貨聯單領回"}, {"key": "D", "text": "小龍：週二 08：00 送修熱水瓶，先繳交50元特殊材料費才能檢修"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  28,
  '根據本文，關於畫線處所象徵的意義，下列說明何者最不恰當？',
  '[{"key": "A", "text": "甲句中「每一個坑洞」：人生不同的挑戰"}, {"key": "B", "text": "乙句中「方正的直角」：作者獨特的個性"}, {"key": "C", "text": "丙句中「紙」：作者自己的本質"}, {"key": "D", "text": "丁句中「蟑螂」：卑鄙惡劣的個人特質"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  29,
  '作者透過本文所抒發的感慨，與下列何者最接近？',
  '[{"key": "A", "text": "要到失去之後，才知道曾經擁有的美好"}, {"key": "B", "text": "為了他人而改變自己，最後卻迷失自我"}, {"key": "C", "text": "年輕時未確定方向，等到一事無成才後悔莫及"}, {"key": "D", "text": "曾經轟轟烈烈的絢爛，誰知到頭來都是一場空"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  30,
  '關於小說中畫線處文句的說明，下列何者最恰當？',
  '[{"key": "A", "text": "甲：政府對人民的監控就像陽光一樣無孔不入"}, {"key": "B", "text": "乙：長時間的緊繃，讓人變得冷酷麻木"}, {"key": "C", "text": "丙：政府假稱瘟疫以掩蓋屠殺人民的真相"}, {"key": "D", "text": "丁：巡邏隊刻意威嚇居民，製造恐懼與猜疑"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  31,
  '對小說中的政府而言，「最壞情況」所指的最可能是下列何者？',
  '[{"key": "A", "text": "人心彼此猜疑，不再相互信任"}, {"key": "B", "text": "氣溫持續上升，民眾難以忍受"}, {"key": "C", "text": "疫情不斷惡化，人們失去求生欲"}, {"key": "D", "text": "群眾發生暴動，突破城門封鎖線"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  32,
  '根據本文，關於美秀美術館，最不可能推論出下列何者？',
  '[{"key": "A", "text": "美術館坐落在山間"}, {"key": "B", "text": "對環境清潔有高度的要求"}, {"key": "C", "text": "館區的電動車由機械人駕駛"}, {"key": "D", "text": "接待中心與美術館有一段距離"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  33,
  '根據本文，下列何者最能體現美秀美術館的烏托邦式美學？',
  '[{"key": "A", "text": "工作人員親切的微笑，流露內心的祥和"}, {"key": "B", "text": "降低人為聲音的干擾，以呈現寧靜氛圍"}, {"key": "C", "text": "所有物件一律為白色，象徵藝術的純淨"}, {"key": "D", "text": "讓觀眾貼近展品，顯現人與藝術無隔閡"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  34,
  '根據本文，作者認為紙本書對一般人的獨特價值最可能是下列何者？',
  '[{"key": "A", "text": "紙本書才能傳承經典與藝術"}, {"key": "B", "text": "閱讀紙本書不受晝夜的限制"}, {"key": "C", "text": "紙本書可讓文字散發不同的渲染力"}, {"key": "D", "text": "城鄉數位落差因紙本書才得以彌補"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  35,
  '關於本文的寫作分析，下列敘述何者最恰當？',
  '[{"key": "A", "text": "以多面向的特質比較來強調數位資訊不如紙本"}, {"key": "B", "text": "用夜以繼日來說明紙本閱讀是數位閱讀的延續"}, {"key": "C", "text": "透過圖表的分析，陳述紙本閱讀無限發展的可能"}, {"key": "D", "text": "藉由晝夜的對照，表達紙本與數位閱讀應該並存"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  37,
  '在這則寓言中，「這個走出洞穴後再回到洞內的人」最可能是象徵下列哪一種
人？',
  '[{"key": "A", "text": "受迫的奴隸"}, {"key": "B", "text": "孤獨的先知"}, {"key": "C", "text": "命運的主宰"}, {"key": "D", "text": "蒙昧的愚者"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  38,
  '根據這則寓言，下列何者最接近柏拉圖的想法？',
  '[{"key": "A", "text": "多數人相信的事未必為真"}, {"key": "B", "text": "自以為是往往會招致滅亡"}, {"key": "C", "text": "面向陽光，影子就會在你背後"}, {"key": "D", "text": "堅定信仰，心靈才能得到自由"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  39,
  '根據甲、乙兩文推論，漢文帝時各種錢幣的重量依序最可能是下列何者？',
  '[{"key": "A", "text": "四銖錢 ＞ 吳錢 ＞ 鄧通錢"}, {"key": "B", "text": "四銖錢 ＝ 鄧通錢 ＞ 吳錢"}, {"key": "C", "text": "吳錢 ＞ 四銖錢 ＞ 鄧通錢"}, {"key": "D", "text": "吳錢 ＞ 鄧通錢 ＝ 四銖錢"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  40,
  '根據甲、乙兩文，下列敘述何者最恰當？',
  '[{"key": "A", "text": "鄧通與吳王同時自鑄莢錢，導致莢錢過多"}, {"key": "B", "text": "鄧通與吳王所鑄銅錢上應有「半兩」字樣"}, {"key": "C", "text": "鄧通叛逆謀反，文帝遂下令禁止私鑄銅錢"}, {"key": "D", "text": "鄧通所鑄錢布天下，故文帝賜其銅山一座"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  41,
  '根據本文，下列文句省略的主語，何者是白敏中？',
  '[{"key": "A", "text": "病其與賀拔惎為友"}, {"key": "B", "text": "乃密令門人申意"}, {"key": "C", "text": "悉以實告"}, {"key": "D", "text": "大怒而去"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'chinese',
  42,
  '根據本文，王起說：「我原只得白敏中，今當更取賀拔惎矣。」這句話的原因，
最可能是下列何者？',
  '[{"key": "A", "text": "白敏中向王起推薦賀拔惎取代自己"}, {"key": "B", "text": "賀拔惎已知此次科考內幕，只好破格錄取封口"}, {"key": "C", "text": "比起白敏中的前倨後恭，賀拔惎的真誠顯得更為可貴"}, {"key": "D", "text": "白敏中把賀拔惎看得比狀元還重，可知賀拔惎有過人之處"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  1,
  '圖 ( 一 ) 數線上的 A、B、C、D 四點所表示的數分別為 a、b、c、d，且 O 為
原點。根據圖中各點的位置判斷，下列何者的值最小？',
  '[{"key": "A", "text": "a"}, {"key": "B", "text": "b"}, {"key": "C", "text": "c"}, {"key": "D", "text": "d"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  2,
  '計算多項式 6x2 + 4x 除以 2x2 後，得到的餘式為何？',
  '[{"key": "A", "text": "2"}, {"key": "B", "text": "4"}, {"key": "C", "text": "2x"}, {"key": "D", "text": "4x"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  3,
  '下列何者為 156 的質因數？',
  '[{"key": "A", "text": "11"}, {"key": "B", "text": "12"}, {"key": "C", "text": "13"}, {"key": "D", "text": "14"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  6,
  '2022 的值介於下列哪兩個數之間？',
  '[{"key": "A", "text": "25，30"}, {"key": "B", "text": "30，35"}, {"key": "C", "text": "35，40"}, {"key": "D", "text": "40，45"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  7,
  '已知坐標平面上有一直線 L 與一點 A。若 L 的方程式為 x = −2，A 點坐標為
(6,5)，則 A 點到直線 L 的距離為何？',
  '[{"key": "A", "text": "3"}, {"key": "B", "text": "4"}, {"key": "C", "text": "7"}, {"key": "D", "text": "8"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  8,
  '多項式 39x2 + 5x −14 可因式分解成 ( 3x + a )( bx + c )，其中 a、b、c 均為
整數，求 a + 2c 之值為何？',
  '[{"key": "A", "text": "−12"}, {"key": "B", "text": "−3"}, {"key": "C", "text": "3"}, {"key": "D", "text": "12"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  10,
  '已知一元二次方程式 ( x − 2 )2 = 3 的兩根為 a、b，且 a > b，求 2a + b 之值
為何？',
  '[{"key": "A", "text": "9"}, {"key": "B", "text": "−3"}, {"key": "C", "text": "6 + 3"}, {"key": "D", "text": "−6 + 3"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  12,
  '已知 p = 7.52 × 10 − 6，下列關於 p 值的敘述何者正確？',
  '[{"key": "A", "text": "小於 0"}, {"key": "B", "text": "介於 0 與 1 兩數之間，兩數中比較接近 0"}, {"key": "C", "text": "介於 0 與 1 兩數之間，兩數中比較接近 1"}, {"key": "D", "text": "大於 1"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'math',
  15,
  '如圖 ( 六 )，∆ABC 中，D 點在 AB 上，E 點在 BC 上，DE 為 AB 的中垂線。若
∠B = ∠C，且 ∠EAC > 90°，則根據圖中標示的角， 判斷下列敘述何者正確？',
  '[{"key": "A", "text": "∠1 = ∠2，∠1 < ∠3"}, {"key": "B", "text": "∠1 = ∠2，∠1 > ∠3"}, {"key": "C", "text": "∠1 ≠ ∠2，∠1 < ∠3"}, {"key": "D", "text": "∠1 ≠ ∠2，∠1 > ∠3"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
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
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  1,
  '某宗教的全球年度大型集會 表(一)
活動在2017年約有235萬人參
國家 人數 國家 人數
與。表(一)為該年參與者的來源
沙烏地阿拉伯 600,108 伊朗 86,500
國及其人數，此一宗教活動最
印尼 221,000 土耳其 79,000
可能為下列何者？
巴基斯坦 179,210 奈及利亞 79,000',
  '[{"key": "A", "text": "佛教浴佛節"}, {"key": "B", "text": "印度教大壺節"}, {"key": "C", "text": "伊斯蘭教朝覲"}, {"key": "D", "text": "天主教聖誕彌撒"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  2,
  '臺灣一處具有特殊泥岩惡地景觀的地點，於2020年
7月由地方政府審議通過為地質公園。該地位處板塊
交界附近及海岸山脈最南端，泥岩夾雜外來岩塊的地
層，為該地質公園主要特色。上述地質公園最可能位
於圖(一)中何處？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  3,
  '中國的氣候受地形、緯度、距海遠近等因素
影響，而有空間上的差異。圖(二)中甲、乙、
丙、丁哪一路線夏季氣候的空間變化趨勢，
具有明顯的「由溼熱，變乾熱」的特性？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  4,
  '根據經濟部 水利署的統計，截至2019年底，臺灣40座主要水庫中，淤積率超
過30%的共有15座，例如霧社水庫淤積率達74.8%、烏山頭水庫達49.2%，顯
示臺灣水庫淤積程度嚴重，影響水庫蓄水功能。下列何項策略最能有效改善
上述現象？',
  '[{"key": "A", "text": "強化集水區崩塌裸露地的植被復育"}, {"key": "B", "text": "擴大在河川下游種植防風林的面積"}, {"key": "C", "text": "減少都市不透水鋪面，增加雨水入滲"}, {"key": "D", "text": "增加地面水源供應，以取代地下水源"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  6,
  '圖(四)為中國歷史上某種官方文件的內容，
根據圖中內容判斷，當時政府製作此官方文件
的主要目的最可能為下列何者？',
  '[{"key": "A", "text": "配合科舉選拔人才，促進社會的流動"}, {"key": "B", "text": "掌握人力作為徵集賦稅和勞役的依據"}, {"key": "C", "text": "推行封建制度並保障貴族世襲的權力"}, {"key": "D", "text": "根據儒家思想，實施以仁為政的措施"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  7,
  '「柯因奈語」(Koine)，又稱「通用希臘語」，是大約發源於西元前四世紀
的國際性語言。此一語言因某帝國在政治上統一了愛琴海地區各希臘城邦，
融合了該地區多種方言發展而成；其後又伴隨帝國對外武力征服，向埃及、
西亞等地區擴散傳播，對於往後數百年間科學、文學和宗教的發展影響深
遠。上述的「某帝國」，最可能為下列何者？',
  '[{"key": "A", "text": "波斯帝國"}, {"key": "B", "text": "蒙兀兒帝國"}, {"key": "C", "text": "亞歷山大帝國"}, {"key": "D", "text": "阿茲提克帝國"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  8,
  '圖(五)是臺灣某考古遺址中，
同一文化層出土的四種石器。
圖中何者最適合作為判斷該文
化層所屬時代的證據？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  9,
  '某宮廟因違法擴建道路及廟宇建築，涉嫌竊占國土及濫墾山坡地，相關單位
多次介入協調，要求廟方自行拆除，但該廟負責人認為廟地選址及擴建的決
定皆為神明指示，堅決不願退讓，於是相關單位除了開罰六萬元外，並將
負責人移送法辦。上述內容最可能是關於下列哪二者之間的衝突？',
  '[{"key": "A", "text": "環境保育與經濟發展"}, {"key": "B", "text": "法律規範與宗教信仰"}, {"key": "C", "text": "傳統習俗與倫理道德觀念"}, {"key": "D", "text": "信仰宗教自由與人民財產權"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  10,
  '國中生小安寄了一封陳情信給某位公職人員，信中敘述父親因沉迷賭博，導致家
中債臺高築，害他的父母離異、家庭破碎，希望有人能幫幫他，讓父親不再沉溺
賭海。該名公職人員收到信後立刻啟動偵辦，循線破獲非法賭場，並依法對賭場
業者與賭徒提起公訴。根據上述內容判斷，小安寄信的對象應是下列何者？',
  '[{"key": "A", "text": "法官"}, {"key": "B", "text": "律師"}, {"key": "C", "text": "檢察官"}, {"key": "D", "text": "警察局局長"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  11,
  '創新科技公司為了讓其產品「LED省電
燈泡」的銷售量增加，在各大報紙刊登廣
告，內容如圖(六)所示。根據圖中內容判
斷，該公司最可能是採取下列何種方式來
達成目標？',
  '[{"key": "A", "text": "降低成本"}, {"key": "B", "text": "價格競爭"}, {"key": "C", "text": "建立品牌形象"}, {"key": "D", "text": "延長營業時間"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  12,
  '圖(七)呈現某國不同年分出生的
婦女，在育齡期間累積的生育數。
為了改變圖中資料呈現的趨勢以維
持人口結構穩定，下列何者最可能
是未來該國政府採行的作法？',
  '[{"key": "A", "text": "提高幼兒教育補助金額"}, {"key": "B", "text": "加強宣導節制生育觀念"}, {"key": "C", "text": "提供弱勢學童輔導課程"}, {"key": "D", "text": "增設高齡安養照護機構"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  13,
  '表(二)是四位同窗好友的 表(二)
相關資料。若僅根據表中 出生時
姓名 出生地 現況
內容判斷，何者最可能 父母的國籍
不曾具有我國國籍？ 王大軒 洛杉磯 中華民國 擔任立法委員',
  '[{"key": "A", "text": "王大軒 李大賢 臺中 美國 在澳洲工作"}, {"key": "B", "text": "李大賢 陳小涵 臺北 美國 擔任高雄市市議員"}, {"key": "C", "text": "陳小涵 林小潔 西雅圖 中華民國 在日本留學"}, {"key": "D", "text": "林小潔"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  14,
  '歐盟基於公眾健康及動物福利等理由，於2012年起，禁止境內農民以傳統格子
籠方式飼養蛋雞，並立法規定市售雞蛋必須明確標示其飼養方式，讓消費者可
以在平飼(即室內放養蛋雞)、放牧(除室內空間外，還提供蛋雞戶外活動空間)
等友善生產的蛋品之間做出選擇。上述友善飼養方式逐漸在臺灣推行，但所產
出的蛋品在臺灣市占率仍不高，其原因最可能為下列何者？',
  '[{"key": "A", "text": "食安問題頻傳"}, {"key": "B", "text": "蛋品品質不佳"}, {"key": "C", "text": "蛋品售價較高"}, {"key": "D", "text": "飲食習慣改變"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  16,
  '婆羅洲島分屬印尼、汶萊與馬來西亞三
國，圖(九)為其原始森林不同時期面積的
變化。圖中原始森林的變化趨勢與下列該
島何種變化趨勢最為相似？',
  '[{"key": "A", "text": "油田開採的面積"}, {"key": "B", "text": "都市聚落的範圍"}, {"key": "C", "text": "野生動物的棲地範圍"}, {"key": "D", "text": "熱帶作物的種植面積"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  17,
  '臺灣某茶商為了提高自有茶園的茶葉產量，以供應國內日益成長的罐裝茶及手
搖茶市場需求，且能與由越南、斯里蘭卡等產區進口的低價茶葉競爭，因而導
入滴灌技術，精準計算用水及肥料使用量。此外，也利用農業機具栽種茶苗，
並以無人機巡視，噴藥及採收時間則以網路平臺管理。上述各項措施，最主要
可達到下列何種成效？',
  '[{"key": "A", "text": "利於傳統茶園轉型成休閒農場"}, {"key": "B", "text": "降低勞力成本占總成本的比例"}, {"key": "C", "text": "提升茶葉品質以提高單位價格"}, {"key": "D", "text": "增加出口至東協國家的茶葉量"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  18,
  '圖(十)為全球四個著名岬角的位置資
訊，其中何者位於歐 亞大陸西部海岸？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  19,
  '「歷史事實」與「歷史解釋」的區別，在於歷史事實是客觀呈現過去發生的
事件；而歷史解釋則是後人運用歷史資料，對相關歷史事件進行的詮釋與評
價。下列敘述中，何者最適合歸類為「歷史事實」？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  20,
  '圖(十一)為臺灣某年報紙刊登的二則社
會新聞。根據內容判斷，新聞報導的
事情最早可能發生於下列何時？',
  '[{"key": "A", "text": "日本統治時期"}, {"key": "B", "text": "清帝國統治時期"}, {"key": "C", "text": "中華民國政府遷臺初期"}, {"key": "D", "text": "中華民國政府推動十大建設期間"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  21,
  '日本料理「天婦羅」，是將食材裹上澱粉漿之後下鍋油炸，這種料理源自於
天主教徒在齋戒期間，將食材油炸後食用。在沒有冷凍技術的時代，因為油
炸食物容易保存，所以水手於遠洋航行時也會準備油炸魚類作為糧食。葡萄
牙的天主教徒最初到日本傳教與貿易時，同時傳入這種料理。「天婦羅」傳入
日本的時代背景，最可能是下列何者？',
  '[{"key": "A", "text": "外國艦隊脅迫幕府開港，促使日本推動明治維新"}, {"key": "B", "text": "西方各國展開海外探險，建立到達東方的新航線"}, {"key": "C", "text": "日本受大唐文化的薰染，效法唐朝推動制度改革"}, {"key": "D", "text": "民主陣營為防堵共產勢力，派遣艦隊駐防太平洋"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  22,
  '一列火車在德國官方祕密安排下，從蘇黎世出發前往俄國，車上乘客包括
列寧及其布爾什維克黨同志，這些人曾因為反對俄國政府而流亡海外。列寧
等人沿途經過德國、瑞典、芬蘭，最後抵達俄國的首都彼得格勒(今聖彼得
堡)。半年後，他們領導革命，推翻臨時政府，組織新的政權，對俄國產生重
大影響。當時德國官方安排這班列車的目的，最可能為下列何者？',
  '[{"key": "A", "text": "與俄國結盟對抗拿破崙"}, {"key": "B", "text": "欲緩和冷戰東西對立局勢"}, {"key": "C", "text": "遵守《德蘇互不侵犯條約》"}, {"key": "D", "text": "為使俄國退出第一次世界大戰"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  23,
  '甲國政府自2019年起，要求記者須通過關於國家領袖思想的考試後，才能取
得記者證，藉以強化他們對國家領袖的效忠。圖(十二)是近年該國政府核發記
者證數量的變化，而表(三)則是無國界記者組織提出的全球新聞自由指數報告
中，該國近年的排名狀況，排名越前面代表新聞自由程度越高。根據相關資
訊判斷，關於甲國政府的此項作法，下列敘述何者最合理？
表(三)
時間(年) 新聞自由指數排名
2015 全球倒數第5
2016 全球倒數第5
2017 全球倒數第5
2018 全球倒數第5
2019 全球倒數第4
2020 全球倒數第4
圖(十二)',
  '[{"key": "A", "text": "政府藉由立法規範，以保障記者的新聞自由"}, {"key": "B", "text": "政府採取獎勵政策，以促使新聞產業蓬勃發展"}, {"key": "C", "text": "政府削減新聞記者人數，以便管控媒體報導內容"}, {"key": "D", "text": "政府透過管控記者思想，以影響閱聽人接收的新聞"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  24,
  '表(四)呈現阿森在近三屆我國總統選舉資格的 表(四)
變化情形。根據表中內容判斷，阿森在第14屆 總統選舉 總統選舉
屆次
至第15屆之間，最可能發生了下列哪一件事？ 參選資格 投票資格',
  '[{"key": "A", "text": "被政黨開除黨籍 13 不具備 具備"}, {"key": "B", "text": "遭法院監護宣告 14 不具備 具備"}, {"key": "C", "text": "遷移戶籍至其他縣市 15 不具備 不具備"}, {"key": "D", "text": "遭法院判處褫奪公權"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  25,
  '我國國會可對中央政府部分官員的人事提名案行使同意權，並在投票表決
前，藉由提問來審查被提名人是否適任。根據我國公職人員的法定職權判
斷，下列哪一個問題的提問對象最可能是大法官被提名人？',
  '[{"key": "A", "text": "如何提升違法官員彈劾案件的辦案效率"}, {"key": "B", "text": "如何落實嚴謹審核中央政府年度總決算"}, {"key": "C", "text": "我國仍維持死刑刑罰是否違反基本人權"}, {"key": "D", "text": "公務人員的選才制度是否有改善的空間"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  26,
  '圖(十三)為某條鐵路的路線圖，該鐵路全線的海拔
高度變化最可能為下列何者？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  27,
  '2014年中國 吉林省與俄羅斯合作擴建圖(十四)中
的甲港口，目前出口貨物可不經由大連港，透過
甲港口可大幅縮短與鄰近國家部分港口的航運時
間。擴建甲港口除上述目的外，最可能還含下列
何優勢？',
  '[{"key": "A", "text": "作為俄羅斯船隻通往大西洋的出海口"}, {"key": "B", "text": "加速俄羅斯將開發重心轉向歐俄平原"}, {"key": "C", "text": "作為中、俄兩國鴨綠江流域貨物出入的港口"}, {"key": "D", "text": "提供中國船隻藉由此港口通往北極海的捷徑"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  29,
  '世界氣象組織(WMO)定義熱浪標準為連續 5日的每日最高氣溫，皆高於歷年
最暖月的最高氣溫平均值5℃以上。表(五)為臺北測站1981至2010年氣溫相關
資料，根據上述定義，臺北在下列何種情形即達到此一熱浪標準？
表(五)
月分 1 2 3 4 5 6 7 8 9 10 11 12 年平均
氣溫(℃) 16.1 16.5 18.5 21.9 25.2 27.7 29.6 29.2 27.4 24.5 21.5 17.9 23.0
最高氣溫(℃) 19.1 19.6 22.1 25.7 29.2 32.0 34.3 33.8 31.1 27.5 24.2 20.7 26.6
最低氣溫(℃) 13.9 14.2 15.8 19.0 22.3 24.6 26.3 26.1 24.8 22.3 19.3 15.6 20.4',
  '[{"key": "A", "text": "連續5天出現31.6℃以上高溫"}, {"key": "B", "text": "連續5天出現34.3℃以上高溫"}, {"key": "C", "text": "連續5天出現34.6℃以上高溫"}, {"key": "D", "text": "連續5天出現39.3℃以上高溫"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  30,
  '以下是中國 天津某年慶祝元旦的相關報導：「政府要求各機關及各民眾團
體，在元旦上午參加慶祝中華民國成立的紀念大會。當晚民眾提燈遍遊街
市，高呼『勿忘國恥』、『抵制日貨』、『打倒貪官汙吏』、『打倒燒香化
紙、磕頭拜年的惡習』等口號。各街市商號張貼標語、懸燈結綵，國民黨黨
旗和國旗飄揚天際，蔚為盛況。」上述內容最可能是描繪下列何時的景象？',
  '[{"key": "A", "text": "1861-1895年自強運動期間"}, {"key": "B", "text": "1928-1937年十年建設期間"}, {"key": "C", "text": "1958-1961年農工大躍進期間"}, {"key": "D", "text": "1966-1976年文化大革命期間"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  31,
  '圖(十六)是某時期中國海外貿
易的進出口總額統計圖。觀察
圖中各區域與中國的貿易概
況，分析造成圖中第「Ⅱ」階
段變化的主要原因，最可能與
下列何者有關？',
  '[{"key": "A", "text": "朝廷驅逐在華的耶穌會傳教士"}, {"key": "B", "text": "玉米、馬鈴薯等美洲作物傳入"}, {"key": "C", "text": "義和團事變對社會經濟的衝擊"}, {"key": "D", "text": "鄭氏勢力擁兵東南與清廷對抗"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  32,
  '謝先生是王小姐的前夫，但謝先生屢次侵擾王小姐的住處，甚至還到她上班
的地方騷擾，最後謝先生因違反保護令的相關規定，被判處拘役四十天。根
據上述內容判斷，下列敘述何者正確？',
  '[{"key": "A", "text": "謝先生必須為自己的違法行為負起刑事責任"}, {"key": "B", "text": "王小姐因警察局所核發的保護令而獲得保障"}, {"key": "C", "text": "謝先生若不服判決可向地方法院提出民事訴訟"}, {"key": "D", "text": "王小姐可依《性別平等教育法》向謝先生求償"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  33,
  '開班會時，有些同學在玩牌、有些同學在吃東
西，阿偉認為吵雜聲使他聽不清楚其他人的發
言內容，影響到他參與會議的權利。圖(十七)是
當日班會的部分過程，阿偉應是在圖中哪一階
段要求主席處理上述問題？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  34,
  '某日阿蔚透過網路觀看立法院的議事實況轉播，根據我國現行法律規定，
他最可能看見下列何者的轉播情況？',
  '[{"key": "A", "text": "審理總統、副總統彈劾案"}, {"key": "B", "text": "表決對行政院的糾正提案"}, {"key": "C", "text": "召開行政院會議規畫施政方針"}, {"key": "D", "text": "行政院部會首長進行施政報告"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  35,
  '「紓解訟源」是近年司法改革的重點之一，其目的是希望讓民眾在提起訴訟
前，能透過公正且具有與法院確定判決相同效力的途徑來解決糾紛，這種方
式既可避免耗時的訴訟程序，也能減少司法資源的浪費。下列哪種處理方式
最符合「紓解訟源」的作法？',
  '[{"key": "A", "text": "不服行政處分，向上級機關提起訴願"}, {"key": "B", "text": "偷竊財物遭逮，嫌犯希望失主別追究"}, {"key": "C", "text": "車禍無人受傷，雙方私下和解賠償損失"}, {"key": "D", "text": "遭友積欠債務，至調解委員會聲請調解"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  37,
  '中國近代某一文章提到：「政府假借預備立憲的美名卻實行中央集權，假借
推行新政卻搜刮民間錢財，對外則割讓土地，並出賣採礦權與鐵路經營權。
人民反對政策，可能會被處死；如果人民自己出錢出力興修鐵路，又會被官方
沒收。政府應該要保護人民，結果人民反而受到政府的傷害，如此不顧人民
生命、財產的政府，誰還能忍受呢！」上文的主要訴求最可能是下列何者？',
  '[{"key": "A", "text": "因對外戰爭受到挫敗，提倡學習西方的軍事及工業技術"}, {"key": "B", "text": "推動制度層面的改革，以解決自強運動改革不彰的問題"}, {"key": "C", "text": "對改革結果感到失望，體認到革命也是救國的途徑之一"}, {"key": "D", "text": "主張全面改革思想文化，提倡西方科學精神與白話文學"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  38,
  '圖(十九)中的硬幣為位在南半球的某國於2019年
所發行。自歐洲人十八世紀移入該地以來，已有
約130種原住民語絕跡。該國希望藉由此硬幣的發
行，提醒人民保存、維護和活化原住民語的重要
性。上述硬幣最可能由下列何國發行？',
  '[{"key": "A", "text": "印度"}, {"key": "B", "text": "秘魯"}, {"key": "C", "text": "澳洲"}, {"key": "D", "text": "菲律賓"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  39,
  '小強參加辯論比賽，辯論主題是「目前甲國社會尚未達到性別平等」，若他
是站在正方的立場，須提出支持主題的論點，下列四張關於甲國不同面向的
統計圖，何者最適合小強作為強化論點的證據？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  40,
  '圖(二十)為小成在研究2017年非洲貿易現況時所發現的某些現象。非洲各國採
取下列何項措施，最可能有助於改善非洲這些現象？
圖(二十)',
  '[{"key": "A", "text": "限定與非洲其他國家的進口配額，保護本國產業"}, {"key": "B", "text": "改善與其他洲的交通運輸，降低貨物的運輸成本"}, {"key": "C", "text": "強化邊境的管制措施，防止鄰國非法貿易的進行"}, {"key": "D", "text": "簽署非洲自由貿易協定，降低非洲國家間的關稅"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  42,
  '圖(二十二)呈現甲、乙、丙三國的貿易情況。若甲國受匯
率變動的影響，使得某段時間的進、出口商品數量皆大幅
增加，則根據圖中內容判斷，該段時間甲國貨幣的匯率變
化，最可能為下列何者？',
  '[{"key": "A", "text": "相對乙、丙兩國貨幣皆升值"}, {"key": "B", "text": "相對乙、丙兩國貨幣皆貶值"}, {"key": "C", "text": "相對乙國貨幣升值，但相對丙國貨幣貶值"}, {"key": "D", "text": "相對乙國貨幣貶值，但相對丙國貨幣升值"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  43,
  '圖(二十三)是某一時期的政治宣傳漫畫，圖中
「大手」代表當時的國際組織，領導各國對
抗侵略者。根據內容判斷，該國際組織最可
能是下列何者？',
  '[{"key": "A", "text": "聯合國"}, {"key": "B", "text": "國際聯盟"}, {"key": "C", "text": "華沙公約組織"}, {"key": "D", "text": "石油輸出國家組織"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  44,
  '根據上文中裕鐸與洋行的會談結果，當時臺灣對外貿易的情況，最可能是下列何者？',
  '[{"key": "A", "text": "當時臺灣尚未對外開港，裕鐸嚴禁洋商在臺貿易"}, {"key": "B", "text": "當時臺灣尚未對外開港，實際上洋商已來臺貿易"}, {"key": "C", "text": "當時臺灣已經對外開港，洋商可在臺灣各港口貿易"}, {"key": "D", "text": "當時臺灣已經對外開港，裕鐸仍阻撓洋商在臺貿易"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  45,
  '根據上文，外國商人分析臺灣道重申外國商船不得在安平附近起卸貨物的原
因，最可能與下列何者有關？',
  '[{"key": "A", "text": "安平與鹿耳門泥沙淤積，易造成擱淺"}, {"key": "B", "text": "府城商人透過「郊」來維護自身利益"}, {"key": "C", "text": "日本出兵臺灣南部，清帝國提高警戒"}, {"key": "D", "text": "許多府城商人組成「郊」與洋行合作"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  46,
  '根據圖(二十四)中「墘」字地名的分布判斷，下列關於「墘」字地名的推論
何者最為合理？',
  '[{"key": "A", "text": "分布於閩南族群集中區，屬閩南族系的地名"}, {"key": "B", "text": "分布於客家族群集中區，屬客家族系的地名"}, {"key": "C", "text": "分布於現今原住民居住地，為原住民的地名"}, {"key": "D", "text": "受西班牙占領影響，為西班牙語音譯的地名"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  47,
  '根據圖(二十五)判斷，在日治時期小瑜的家鄉最可能以哪種產業活動為主？',
  '[{"key": "A", "text": "水稻耕作"}, {"key": "B", "text": "樟腦提煉"}, {"key": "C", "text": "茶葉種植"}, {"key": "D", "text": "海鹽晒製"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  48,
  '根據上文中地名的命名原則及圖(二十五)與圖(二十六)的資訊判斷，小瑜的家
鄉地名最可能為下列何者？',
  '[{"key": "A", "text": "海墘"}, {"key": "B", "text": "潭墘"}, {"key": "C", "text": "岸壁墘"}, {"key": "D", "text": "黑礁墘"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  49,
  '文中針對我國咖啡的相關敘述，下列何者最適當？',
  '[{"key": "A", "text": "咖啡產品貿易總額超越茶產品"}, {"key": "B", "text": "咖啡豆的進出口貿易呈現出超"}, {"key": "C", "text": "飲用咖啡的習慣受到文化交流影響"}, {"key": "D", "text": "國小內販售咖啡將會遭受刑罰處罰"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  50,
  '根據文中內容判斷，南韓政府的作法與下列何項敘述最相符？',
  '[{"key": "A", "text": "透過負向誘因影響校內師生的消費能力"}, {"key": "B", "text": "透過正向誘因影響校內商品的販售種類"}, {"key": "C", "text": "透過制度變革影響校內師生的消費能力"}, {"key": "D", "text": "透過制度變革影響校內商品的販售種類"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  51,
  '文中所提及南韓政府修改法律的目的，與下列我國的何項作法最類似？',
  '[{"key": "A", "text": "受監護宣告者自行訂定的契約不具效力"}, {"key": "B", "text": "雇主不得因性別因素而對員工有差別待遇"}, {"key": "C", "text": "國小學童不得出入有害身心發展的不良場所"}, {"key": "D", "text": "家庭暴力受害者可聲請保護令以避免受到傷害"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  52,
  '文中日本文學家描述的城市現象，與下列何者的關係最密切？',
  '[{"key": "A", "text": "工業革命"}, {"key": "B", "text": "宗教改革"}, {"key": "C", "text": "啟蒙運動"}, {"key": "D", "text": "文藝復興"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  53,
  '圖(二十八)是文中國家某空氣汙染嚴重的城市示意
圖。已知圖中某處為低技術勞動階級居住的區域，
根據上文及考量盛行風向的影響，此處最可能位於
圖中甲、乙、丙、丁何處？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'social',
  54,
  '文中關於城市居民居住區域分布所呈現的問題，是下列何者的關懷重點？',
  '[{"key": "A", "text": "社會主義"}, {"key": "B", "text": "民族主義"}, {"key": "C", "text": "帝國主義"}, {"key": "D", "text": "法西斯主義"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  1,
  '氣象報導時常可見「百帕」一詞，下列有關百帕的敘述何者正確？',
  '[{"key": "A", "text": "百帕是氣壓的單位"}, {"key": "B", "text": "百帕是溫度的單位"}, {"key": "C", "text": "百帕是風速的單位"}, {"key": "D", "text": "百帕是下雨的機會"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  3,
  '博物館的貴重畫冊常會保存在充滿氮氣的密閉容器中，以防止畫冊氧化。上述
使用氮氣的原因，主要是考量氮氣具有下列何種性質？',
  '[{"key": "A", "text": "密度較大"}, {"key": "B", "text": "比熱較小"}, {"key": "C", "text": "沸點較大"}, {"key": "D", "text": "活性較小"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  4,
  '人類將人工魚礁投入水底以增加藻類、珊瑚及魚類的棲息空間，這些魚礁最可
能被置放在下列哪一地區？',
  '[{"key": "A", "text": "溪流區"}, {"key": "B", "text": "河口區"}, {"key": "C", "text": "淺海區"}, {"key": "D", "text": "大洋區"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  5,
  '下列為四種植物對於環境刺激的感應，何者從接受刺激到出現反應，所需的時
間最長?',
  '[{"key": "A", "text": "朱槿植株受光刺激後向光彎曲"}, {"key": "B", "text": "捕蠅草受昆蟲刺激後葉片閉合"}, {"key": "C", "text": "酢漿草在太陽下山後葉片下垂"}, {"key": "D", "text": "含羞草受外力觸碰後小葉閉合"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  6,
  '住在英國的大介到紐西蘭歡度 表(一)
聖誕節(12/25)，他發現此時
紐西蘭的氣候型態與常見慶祝
活動和英國大不相同，其比較
如表(一)。根據表中資訊，下列
何者也是大介當時在紐西蘭可
發現的現象？',
  '[{"key": "A", "text": "紐西蘭的夜晚長度比英國長"}, {"key": "B", "text": "紐西蘭的白晝長度比英國長"}, {"key": "C", "text": "紐西蘭的白晝與夜晚長度大約相同"}, {"key": "D", "text": "紐西蘭的白晝與夜晚長度都和英國大約相同"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  7,
  '小真和小文到高山上旅遊，發現密封包裝的洋芋片其外包裝比在山
下膨脹許多，如圖(一)所示。以下為兩人對包裝的膨脹現象是否與
氣溫有關的對話：
小真：「包裝膨脹應該是因為山上氣溫較低，你看在山下的時候氣
溫高就不會。」
小文：「應該不是氣溫的關係吧！……」
圖(一)
已知上述對話中小文不同意小真的論點，則下列說法何者最不適合用來反駁
小真？',
  '[{"key": "A", "text": "我在平地的家中開冷氣時，溫度跟山上相同，洋芋片包裝卻沒有膨脹的現象"}, {"key": "B", "text": "你看這瓶玻璃瓶裝可樂，同樣到氣溫較低的山上，玻璃瓶卻沒有膨脹的現象"}, {"key": "C", "text": "山上的便利商店內有暖氣，溫度跟山下相同，可是洋芋片包裝也有膨脹的現象"}, {"key": "D", "text": "開車上山的過程中，車內空調讓溫度保持不變，可是洋芋片包裝也有膨脹的"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  8,
  '將月球、太陽、氫原子、口腔皮膜細胞依照體積
大小，標示於圖(二)中的體積尺度示意圖。圖中
越靠近數線左端的物質，體積越小；越靠近數線
右端的物質，體積越大。則下列四項甲、乙、 圖(二)
丙、丁的對應方式，何者最合理？',
  '[{"key": "A", "text": "甲－氫原子，乙－口腔皮膜細胞，丙－太陽，丁－月球"}, {"key": "B", "text": "甲－氫原子，乙－口腔皮膜細胞，丙－月球，丁－太陽"}, {"key": "C", "text": "甲－口腔皮膜細胞，乙－氫原子，丙－太陽，丁－月球"}, {"key": "D", "text": "甲－口腔皮膜細胞，乙－氫原子，丙－月球，丁－太陽"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  9,
  '製作蛋糕時，常會在白色的鮮奶油中加入些許色素混合，使其顏色變化增加
美觀，而鮮奶油仍維持原本的性質。做好的蛋糕需妥善冷藏，以防止鮮奶油腐壞
變質。關於上述鮮奶油「變色」和鮮奶油「變質」兩者的說明，下列何者最合理？',
  '[{"key": "A", "text": "兩者都是化學變化"}, {"key": "B", "text": "兩者都不是化學變化"}, {"key": "C", "text": "只有後者是化學變化"}, {"key": "D", "text": "只有前者是化學變化"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  10,
  '蘋果酸是蘋果等水果中含有的成分，化學式為 C H O ，分子中含有兩個—COOH
4 6 5
原子團，是蘋果的酸味來源，常作為食品添加劑。關於蘋果酸的說明，下列何
者正確？',
  '[{"key": "A", "text": "屬於有機化合物，也是電解質"}, {"key": "B", "text": "屬於有機化合物，也是非電解質"}, {"key": "C", "text": "屬於無機化合物，也是電解質"}, {"key": "D", "text": "屬於無機化合物，也是非電解質"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  11,
  '人類的 ABO 血型是由一對遺傳因子控制，而控制此血型的遺傳因子有 IA、IB
和 i 三種型式，其中 IA 和 IB 是顯性，i 是隱性，血型和基因型的關係如表(二)
所示。表(三)為甲～丁四組父母的血型配對，在不考慮突變的情況下，則表(三)
中的何種組別不可能生下 O 型血型的子女？
表(二) 表(三)',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  12,
  '小蘭想了解山坡地發生山崩時，不同因素對建築物破壞程度的影響，而設計以
下實驗，裝置如圖(三)所示。θ為斜面與水平面間的夾角，實驗方式是讓石塊
從斜面上滑落撞擊下方的模型房屋。表(四)則是小蘭 4 次實驗的一些參數。下
列有關此實驗的敘述，何者正確？
表(四)
圖(三)',
  '[{"key": "A", "text": "在實驗編號 1、2 中，石塊重量控制不變"}, {"key": "B", "text": "在實驗編號 3、4 中，斜面長度控制不變"}, {"key": "C", "text": "若要了解夾角θ的影響，可參考實驗編號 2、4 的結果"}, {"key": "D", "text": "若要了解斜面長度的影響，可參考實驗編號 1、3 的結果"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  13,
  '根據地震波波速變化可知，地球內部可分為地殼、地函、地核三層。上述分層
與岩石圈和軟流圈厚度範圍的關係，下列何者最合理？',
  '[{"key": "A", "text": "岩石圈的厚度範圍與地殼相等"}, {"key": "B", "text": "軟流圈的厚度範圍與地函相等"}, {"key": "C", "text": "岩石圈包括了地殼與一部分的地函"}, {"key": "D", "text": "軟流圈包括了地函與一部分的地殼"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  14,
  '下列選項中的四個活動，光線經過「」中的裝置後，哪一個不會改變光的傳播
方向？',
  '[{"key": "A", "text": "利用「針孔」成像觀察日食"}, {"key": "B", "text": "利用「放大鏡」觀察校園中的花朵"}, {"key": "C", "text": "利用「汽車後照鏡」觀察後方的車輛位置"}, {"key": "D", "text": "利用「三稜鏡」將陽光分散成七種不同顏色的光"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  15,
  '圖(四)為某一地區的地層剖面示意
圖，圖中灰色部分岩層飽含地下水。
關於甲、乙、丙、丁所指的各種交界
面，何者為地下水面？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  16,
  '水平桌面上畫有由大小相等正方形組成的方格，一條導線沿著桌面上的直線水平
放置，將導線通入穩定電流，如圖(五)所示。關於載流導線在桌面上 P、Q 兩點所
產生的磁場強度及方向，下列何者正確？',
  '[{"key": "A", "text": "強度相同，方向相同"}, {"key": "B", "text": "強度相同，方向不同"}, {"key": "C", "text": "強度不同，方向相同"}, {"key": "D", "text": "強度不同，方向不同"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  17,
  '圖(六)為實驗課的二臺顯微鏡，阿彥和阿秀想利用顯微鏡觀察一朵小花，若阿彥
要觀察萼片細胞的葉綠體大小，而阿秀要觀察雄蕊的數目，則最適合他們使用
的顯微鏡分別為何？',
  '[{"key": "A", "text": "兩人皆為複式顯微鏡"}, {"key": "B", "text": "兩人皆為解剖顯微鏡"}, {"key": "C", "text": "阿彥為複式顯微鏡，阿秀為解剖顯微鏡"}, {"key": "D", "text": "阿彥為解剖顯微鏡，阿秀為複式顯微鏡"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  18,
  '一株植物含有不同類型的細胞，以榕樹為例，關於其可行光合作用的細胞數目
甲
與可行呼吸作用的細胞數目之比較及其原因，下列何者最合理？
乙',
  '[{"key": "A", "text": "甲大於乙，因植物的部分細胞不具有粒線體"}, {"key": "B", "text": "甲小於乙，因植物的部分細胞不具有粒線體"}, {"key": "C", "text": "甲小於乙，因植物的部分細胞不具有葉綠體"}, {"key": "D", "text": "甲等於乙，因植物細胞皆具有葉綠體與粒線體"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  19,
  '「一氧化二氮無色、無味，在常溫常壓下為氣態。它會吸收地表輻射，也對
人體的中樞神經有作用，常在醫療上作為麻醉使用。」根據上述介紹，可知
一氧化二氮會造成溫室效應，其原因最可能是上述提到的何種特性？',
  '[{"key": "A", "text": "無色、無味"}, {"key": "B", "text": "會吸收地表輻射"}, {"key": "C", "text": "常溫常壓下為氣態"}, {"key": "D", "text": "對人體的中樞神經有作用"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  20,
  '圖(七)是近 30 年臺北和恆春不同月
的平均氣溫(折線圖)與平均降雨量
(柱狀圖)情形。根據圖中數據所做的
推論，下列何者最不合理？',
  '[{"key": "A", "text": "恆春的晝夜溫差較臺北小，約為 7℃"}, {"key": "B", "text": "臺北的每月平均降雨量都超過 50 mm"}, {"key": "C", "text": "相較於臺北，恆春大部分的降雨集中"}, {"key": "D", "text": "臺北不同月的平均氣溫變化較恆春"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  21,
  '圖(八)～圖(十)為一則新聞報導，有一種「自熱罐」飲料，罐身下方隔層有 CaO
和水，兩者混合後會放出熱量，可使飲料溫度上升至 60℃ 左右，且續熱半小時
以上，在寒冷的冬天相當方便。
圖(八) 圖(九) 圖(十)
小禾認為圖(十)中說明產生的物質有誤，應更正為何種物質？',
  '[{"key": "A", "text": "碳酸鈉"}, {"key": "B", "text": "硫酸鈣"}, {"key": "C", "text": "氫氧化鈉"}, {"key": "D", "text": "氫氧化鈣"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  22,
  '為避免攝取過量咖啡因，可先降低咖啡豆中的咖啡因含量。將咖啡豆浸泡
在有機溶劑中，咖啡因會溶於溶劑中，之後取出咖啡豆加熱，使溶劑揮發
掉。二氯甲烷是過往常用的有機溶劑，去除咖啡因效果好又易揮發，但後
來因安全疑慮而棄用，並改用乙酸乙酯。因為酯類_______，所以較無安
全性疑慮，美國食品藥物管理局許可使用乙酸乙酯來去除咖啡因，且無明
定殘留許可標準。
依據上述資訊，畫線處最適合填入下列何者？',
  '[{"key": "A", "text": "只由碳和氫兩種原子所組成"}, {"key": "B", "text": "是香蕉、柳丁等水果就含有的物質"}, {"key": "C", "text": "沸點比二氯甲烷高，而不易揮發去除"}, {"key": "D", "text": "是油脂與鹼性物質進行皂化反應後的產物"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  23,
  '圖(十一)為某地的一條食物鏈，圖(十二)則為依據此食物鏈各層級生物體總能量
所繪製成的能量塔示意圖(面積不代表實際能量大小)，若其中蛇類族群的總能量
約為 10,000 能量單位，則乙階層所含的總能量最接近下列何者？
圖(十一)
圖(十二)',
  '[{"key": "A", "text": "100 能量單位"}, {"key": "B", "text": "1,000 能量單位"}, {"key": "C", "text": "10,000 能量單位"}, {"key": "D", "text": "100,000 能量單位"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  24,
  '圖(十三)為臺灣附近的地面天氣簡圖，圖中黑色曲
線為等壓線。此時全臺各地皆受天氣系統甲的影
響，目前的地面風向大致以東北風為主。同時在
呂宋島東方海面的天氣系統乙則有機會發展為輕
度颱風。根據上述資訊，下列推論何者最合理？',
  '[{"key": "A", "text": "由天氣系統甲的位置判斷，其氣團性質與太平洋"}, {"key": "B", "text": "由天氣簡圖判斷，當天呂宋島北部的地面風向"}, {"key": "C", "text": "受天氣系統甲的影響，臺灣南部及東南部的雨勢"}, {"key": "D", "text": "未來若天氣系統乙移至呂宋島上方，會使呂宋島產生晴朗炎熱的天氣型態"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  26,
  '表(五)為某人體心臟內甲、乙兩個心室的血液中 O 含量，根 表(五)
2
據此表，推測此兩心室所連接的血管，下列敘述何者最合理？',
  '[{"key": "A", "text": "甲與大靜脈連接"}, {"key": "B", "text": "甲與肺靜脈連接"}, {"key": "C", "text": "乙與主動脈連接"}, {"key": "D", "text": "乙與肺動脈連接"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  27,
  '圖(十五)為甲和乙兩國在 2015 年，以及 2030 年時預計達成的發電方式比例圖：
圖(十五)
參考表(六)資料，假設沿用同樣的發電機組，僅考慮發電方式的比例改變，不
考慮其他因素，則與 2015 年相比，預測兩國在 2030 年平均每度電的碳排放量會
如何變化？ 表(六)',
  '[{"key": "A", "text": "兩國都會增加"}, {"key": "B", "text": "兩國都會減少"}, {"key": "C", "text": "甲國增加，乙國減少"}, {"key": "D", "text": "甲國減少，乙國增加"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  28,
  '小禮將一杯 20℃ 的純水分為甲、乙兩杯，甲、乙兩杯純水的質量分別為 M 、
甲
M ，他將兩杯水分別以相同的熱源加熱，並記錄其加熱時間與上升溫度。已知
乙
M ：M ＝3：2，若熱源發出的熱量完全被水吸收，且水的蒸發忽略不計，則
甲 乙
水的上升溫度與加熱時間之關係圖最接近下列何者？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  29,
  '「新聞報導某處養殖池的白蝦大量暴斃，調查後初步推測是高溫與暴雨，使養
殖池的溶氧量和 pH 值劇烈變化，導致水質改變所造成的。專家建議為避免白
蝦大量死亡，應注意水溫變化，可先用水車調整水中的溶氧量，並監控水中的
pH 值，投放熟石灰(氫氧化鈣)調整至合適的 pH 值。」關於上述專家建議的方
法，下列說明何者最合理？
',
  '[{"key": "A", "text": "使水中的溶氧量增加，pH 值增加"}, {"key": "B", "text": "使水中的溶氧量增加，pH 值減少"}, {"key": "C", "text": "使水中的溶氧量減少，pH 值增加"}, {"key": "D", "text": "使水中的溶氧量減少，pH 值減少"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  30,
  '圖(十六)分別為在鑰匙上鍍銅和鋅銅電池的裝置示意圖。已知圖中的 和
，其中一個代表電子流動方向，另一個代表電流流動方向。依據圖中資訊
判斷，鋅銅電池中乙電極進行的反應，應為下列何者？',
  '[{"key": "A", "text": "Cu2+ + 2e－ → Cu"}, {"key": "B", "text": "Cu → Cu2+ + 2e－"}, {"key": "C", "text": "Zn2+ + 2e－ → Zn"}, {"key": "D", "text": "Zn → Zn2+ + 2e－"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  31,
  '有一個帶電的離子含有 X、Y、Z 三種粒子(質子、電子、中子，未依照順序排
列)，且 X、Y、Z 的粒子數目依序為 N 、N 、N 。已知 X 粒子的質量最小，
X Y Z
關於此離子的說明，下列何者最合理？',
  '[{"key": "A", "text": "若為陽離子，且 N ＞N ＝N ，則 Z 為質子"}, {"key": "B", "text": "若為陽離子，且 N ＞N ＝N ，則 Z 為電子"}, {"key": "C", "text": "若為陰離子，且 N ＝N ＞N ，則 Z 為質子"}, {"key": "D", "text": "若為陰離子，且 N ＞N ＝N ，則 Z 為電子"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  32,
  '已知蜂蜜中含有分解澱粉的酵素。現有甲、乙兩試管皆裝有等量且濃度相同的
澱粉液，隨機在其中一支加入蜂蜜，另一支加入等量的水。將兩支試管充分搖
勻，靜置於適宜的溫度，待足夠的反應時間後，以碘液檢測。結果顯示甲呈現
藍黑色，乙呈現黃褐色。根據此結果，推測哪一支試管加入了蜂蜜及其理由，
下列何者最合理？',
  '[{"key": "A", "text": "甲，因未檢測出澱粉"}, {"key": "B", "text": "甲，因有檢測出澱粉"}, {"key": "C", "text": "乙，因未檢測出澱粉"}, {"key": "D", "text": "乙，因有檢測出澱粉"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  33,
  '有一槓桿其轉軸 O 點在槓桿中央，同時在距 O 點兩側 20 cm 處，垂直槓桿施
1 1
予大小為 F 的力，如圖(十七)所示，兩力對此槓桿產生的合力矩大小為 L 。
1
另有一槓桿其轉軸 O 點在槓桿的一端，在距 O 點 40 cm 處，垂直槓桿施予
2 2
大小為 F 的力，如圖(十八)所示，此力對此槓桿產生的力矩大小為 L 。關於
2
L 及 L 兩者的關係，下列何者正確？
1 2',
  '[{"key": "A", "text": "L ＝L"}, {"key": "B", "text": "L ＝2L"}, {"key": "C", "text": "2L ＝L"}, {"key": "D", "text": "L ＝0，且 L ＜L"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  34,
  '一條輕繩的一端固定於水平桌面的桌緣
上，拉直此繩使其呈水平後，再以固定
頻率鉛直上下振動，產生相同頻率的繩
波，其示意圖如圖(十九)所示。繩波上一
點 P 與桌面水平線的鉛直高度與時間的關
圖(十九)
係如表(七)所示，依據此表推論下列何者
最可能是此繩波的週期？
表(七)',
  '[{"key": "A", "text": "1.0 × 10-2 s"}, {"key": "B", "text": "1.5 × 10-2 s"}, {"key": "C", "text": "2.0 × 10-2 s"}, {"key": "D", "text": "3.0 × 10-2 s"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  35,
  '小萍比較人體血液中的尿素與氧氣在「流出甲器官後」的濃度變化，結果如
表(八)所示。根據上述，推測甲器官最可能是下列何者？ 表(八)',
  '[{"key": "A", "text": "膀胱"}, {"key": "B", "text": "肝臟"}, {"key": "C", "text": "肺臟"}, {"key": "D", "text": "腎臟"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  36,
  '阿忠與小志想要移動地上的書櫃，發現書櫃裝滿書時，他們無法推動書櫃，因
此將裡面的書先拿下，之後就可以輕鬆推動書櫃。兩人對此現象的解釋如下：
阿忠：由牛頓第二運動定律 F＝ma 可知，書櫃裝滿書時，質量 m 較大，因此
推動書櫃所需的力 F 也較大，而造成我們推不動書櫃。
小志：書櫃裝滿書時，書櫃垂直作用於地面的力較大，因此書櫃與地面間的
最大靜摩擦力較大，而造成我們推不動書櫃。
關於兩人的解釋是否合理？',
  '[{"key": "A", "text": "兩人均合理"}, {"key": "B", "text": "兩人均不合理"}, {"key": "C", "text": "只有阿忠合理"}, {"key": "D", "text": "只有小志合理"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  37,
  '小淳和朋友到新竹的新月沙灣玩水，他們在早上 8 點到達。他觀察當地的海浪
變化，發現下列現象：
①早上 10 點時，海浪打到沙灘上的位置，比他們 8 點剛到的時候低。
②中午 12 點用餐時，海浪打到沙灘上的位置比早上 10 點時更低了。
③下午 2 點，準備要離開時，海浪打到沙灘上的位置比中午 12 點時更高。
已知海浪打到沙灘上的位置變化是受到潮汐的影響，根據小淳的發現，推算
當地的滿潮或乾潮時間應在下列哪個時間範圍內？',
  '[{"key": "A", "text": "乾潮時間可能在早上 8 點～早上 10 點間"}, {"key": "B", "text": "乾潮時間可能在中午 12 點～下午 2 點間"}, {"key": "C", "text": "滿潮時間可能在早上 8 點～中午 12 點間"}, {"key": "D", "text": "滿潮時間可能在中午 12 點～下午 2 點間"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  38,
  '圖(二十)為一個內部為真空的密閉空心金屬球，其金屬成分為純銅。
小詩將此金屬球放入水裡，球會完全沒入水中，測得排開水的體積
為 V，再用天平量測其質量為 M，她發現利用密度 D＝M / V 計算出
的 D 值與課本上記載的純銅密度 8.96 g/cm3 明顯不同。若小詩的測
量與計算過程皆無錯誤，則下列何者最合理？ 圖(二十)',
  '[{"key": "A", "text": "D＜8.96 g/cm3，因為 M 為金屬成分的質量，但 V 大於金屬成分的體積"}, {"key": "B", "text": "D＜8.96 g/cm3，因為 V 為金屬成分的體積，但 M 小於金屬成分的質量"}, {"key": "C", "text": "D＞8.96 g/cm3，因為 M 為金屬成分的質量，但 V 小於金屬成分的體積"}, {"key": "D", "text": "D＞8.96 g/cm3，因為 V 為金屬成分的體積，但 M 大於金屬成分的質量"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  39,
  '細胞內的染色體組成會因為細胞種類的不同而有差異，編 表(九)
號甲、乙、丙和丁分別代表人體中不同的細胞，如表(九)
所示，下列何者不具有成對的性染色體？',
  '[{"key": "A", "text": "只有甲"}, {"key": "B", "text": "甲和丁"}, {"key": "C", "text": "丙和丁"}, {"key": "D", "text": "乙、丙和丁"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  40,
  '圖(二十一)為某地的地質剖面圖，已知此地
地層未倒轉，且乙岩層的沉積年代為距今
15,000 年～10,000 年前之間，下列有關其他
各岩層的沉積年代或形成年代，何者最合理？',
  '[{"key": "A", "text": "甲岩層的沉積年代距今至少 15,000 年"}, {"key": "B", "text": "丙岩層的沉積年代距今不到 10,000 年"}, {"key": "C", "text": "火成岩脈的形成時間距今至少 10,000 年"}, {"key": "D", "text": "火成岩脈的形成時間距今不到 15,000 年"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  41,
  '圖(二十二)為老師進行實驗的步驟示意圖，在步驟四乙瓶溶液倒入前，若要預測
甲瓶溶液顏色變化的可能情形，則下列的預測何者最合理？
(cid:908)
(cid:908)
(cid:1176)
(cid:1176)
(cid:1176) (cid:908)
圖(二十二)',
  '[{"key": "A", "text": "只有一種可能，會觀察到顏色由無色變成紅色"}, {"key": "B", "text": "只有一種可能，會觀察到顏色由紅色變成無色"}, {"key": "C", "text": "有兩種可能，會觀察到顏色由無色變成紅色或維持無色"}, {"key": "D", "text": "有兩種可能，會觀察到顏色由紅色變成無色或維持紅色"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  42,
  '完成步驟 2 後的發酵裝置圖，應為下列何者才合理？(考慮橡皮塞的有無和橡皮
管兩端的位置)',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  43,
  '牧牧和小歡兩人針對步驟 4，各自提出檢測方法：
牧牧：如圖(二十三)所示，在集氣瓶中加入適量的澄清石灰水溶液，搖晃後，若
變混濁，表示有二氧化碳，以推測收集氣體的過程，發酵還在進行。
小歡：如圖(二十四)所示，將有火焰的線香放入集氣瓶內，若線香持續燃燒，表
示有助燃性氣體，以推測收集氣體的過程，發酵還在進行。
依據實驗內容，判斷兩人的檢測說明是否合理？',
  '[{"key": "A", "text": "兩人皆合理"}, {"key": "B", "text": "兩人皆不合理"}, {"key": "C", "text": "只有牧牧合理"}, {"key": "D", "text": "只有小歡合理"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  44,
  '依據實驗內容與結果，可以判斷出下列何者？',
  '[{"key": "A", "text": "厭氧發酵溫度越高，微生物的活性反而會降低"}, {"key": "B", "text": "此厭氧發酵所產生的氣體，都屬於易溶於水的氣體"}, {"key": "C", "text": "三種溫度所產生的沼氣，甲烷的體積百分比都在 20% 左右"}, {"key": "D", "text": "表中排開水量數值越大，可表示當天該條件下的發酵速率越快"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  45,
  '根據圖(二十五)，推論此植物屬於下列何者？',
  '[{"key": "A", "text": "藻類"}, {"key": "B", "text": "蘚苔植物"}, {"key": "C", "text": "單子葉植物"}, {"key": "D", "text": "雙子葉植物"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  46,
  '根據本文，推論哪一位同學的作答結果正確？',
  '[{"key": "A", "text": "同學 1"}, {"key": "B", "text": "同學 2"}, {"key": "C", "text": "同學 3"}, {"key": "D", "text": "同學 4"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  47,
  '下列哪一個組裝方式符合圖(二十七)中的電路圖？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": "505005000 505005000"}, {"key": "C", "text": ""}, {"key": "D", "text": "505005000 505005000"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  48,
  '表(十二)為小玉報告中所記錄的電流值，若根據圖(二十七)
來判斷表中 I ＞I 是否合理，下列的判斷與論述何者
甲 乙
最適當？',
  '[{"key": "A", "text": "合理，因為負極為電子流流出端，而甲較靠近電池負極，所以 I ＞I 合理"}, {"key": "B", "text": "合理，因為甲測得的電流值應為流過丙與丁的電流值相加，所以 I ＞I 合理"}, {"key": "C", "text": "不合理，因為正極為電流流出端，而乙較靠近電池正極，所以 I ＞I 才合理"}, {"key": "D", "text": "不合理，因為乙測得的電流值應為流過丙與丁的電流值相加，所以 I ＞I"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  49,
  '關於此回合阿明和小豪的得分與卡牌放置組合，下列敘述何者正確？',
  '[{"key": "A", "text": "阿明得 2 分，且小豪的卡牌組合是錯誤的"}, {"key": "B", "text": "阿明得 2 分，但小豪的卡牌組合也是正確的"}, {"key": "C", "text": "小豪得 1 分，且小豪放置卡牌組合也是正確的"}, {"key": "D", "text": "小豪得 1 分，但小豪放置卡牌組合錯誤，會得分是因為阿明答錯"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'science',
  50,
  '根據本文，關於此回合兩人玩遊戲時的神經傳遞敘述，下列何者正確？',
  '[{"key": "A", "text": "兩人從接受刺激至產生反應的時間相同"}, {"key": "B", "text": "眼睛內的肌肉接收刺激"}, {"key": "C", "text": "刺激經由感覺神經元傳遞至腦幹並發出命令"}, {"key": "D", "text": "命令經由運動神經元傳遞至手指以按鈴搶答"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  1,
  'Look at the picture. The woman is putting on the
cake.',
  '[{"key": "A", "text": "candles"}, {"key": "B", "text": "forks"}, {"key": "C", "text": "plates"}, {"key": "D", "text": "strawberries"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  2,
  'The movie starts at two o’clock, let’s meet at the theater at one forty-five.',
  '[{"key": "A", "text": "so"}, {"key": "B", "text": "or"}, {"key": "C", "text": "if"}, {"key": "D", "text": "because"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  3,
  'Peter is afraid of the dark. He even leaves the on when sleeping.',
  '[{"key": "A", "text": "computer"}, {"key": "B", "text": "fans"}, {"key": "C", "text": "lights"}, {"key": "D", "text": "music"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  4,
  'Pam is a baseball player; she has more fans than any other player on her team.',
  '[{"key": "A", "text": "boring"}, {"key": "B", "text": "heavy"}, {"key": "C", "text": "popular"}, {"key": "D", "text": "rich"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  5,
  'I did not do my homework, so my teacher said I stay after school to finish it.',
  '[{"key": "A", "text": "failed to"}, {"key": "B", "text": "had to"}, {"key": "C", "text": "hoped to"}, {"key": "D", "text": "used to"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  6,
  'Kevin has only enough money for the bag or the shoes. That is a hard to
make because he likes them both.',
  '[{"key": "A", "text": "choice"}, {"key": "B", "text": "gift"}, {"key": "C", "text": "rule"}, {"key": "D", "text": "trick"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  7,
  'It was for us to answer the math question because we’ve done the same kind
of questions many times.',
  '[{"key": "A", "text": "common"}, {"key": "B", "text": "easy"}, {"key": "C", "text": "safe"}, {"key": "D", "text": "special"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  8,
  'Although it took me lots of time a big meal for ten people, I was happy that
everyone enjoyed it.',
  '[{"key": "A", "text": "prepare"}, {"key": "B", "text": "to prepare"}, {"key": "C", "text": "preparing"}, {"key": "D", "text": "prepared"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  9,
  'Don’t let the children swim in the river. We don’t know how it is. It could be
dangerous.',
  '[{"key": "A", "text": "deep"}, {"key": "B", "text": "far"}, {"key": "C", "text": "long"}, {"key": "D", "text": "thick"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  10,
  'Bob is of the boys in the family. He never does any housework. His brothers
at least take out the garbage sometimes.',
  '[{"key": "A", "text": "lazier"}, {"key": "B", "text": "the lazy"}, {"key": "C", "text": "the lazier"}, {"key": "D", "text": "the laziest"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  11,
  'Aunt Gina has lived in this town for more than sixty years, so she it very well.',
  '[{"key": "A", "text": "will know"}, {"key": "B", "text": "knew"}, {"key": "C", "text": "knows"}, {"key": "D", "text": "was going to know"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  12,
  'We won’t see the sun even after the typhoon leaves, because the news said that
heavier rain will soon .',
  '[{"key": "A", "text": "catch"}, {"key": "B", "text": "follow"}, {"key": "C", "text": "move"}, {"key": "D", "text": "stop"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  13,
  'Yesterday when I got home from work, my brother for dinner, so he invited me
to join him.',
  '[{"key": "A", "text": "goes out"}, {"key": "B", "text": "went out"}, {"key": "C", "text": "has gone out"}, {"key": "D", "text": "was going out"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  14,
  'You were not to lend Amy money. She never gives back what she borrows.',
  '[{"key": "A", "text": "crazy"}, {"key": "B", "text": "helpful"}, {"key": "C", "text": "wise"}, {"key": "D", "text": "wrong"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  15,
  'Have you found a summer job yet? Mr. Firth someone to take care of his kids
during the vacation. Maybe you can talk to him.',
  '[{"key": "A", "text": "has looked for"}, {"key": "B", "text": "is looking for"}, {"key": "C", "text": "looks for"}, {"key": "D", "text": "was looking for"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  16,
  'David looked out of the balcony window and saw a woman get in his car away.',
  '[{"key": "A", "text": "drive"}, {"key": "B", "text": "drove"}, {"key": "C", "text": "and drive"}, {"key": "D", "text": "and drove"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  17,
  'The police haven’t found the little girl who at a supermarket. They’ll keep
doing all they can to find her.',
  '[{"key": "A", "text": "took away"}, {"key": "B", "text": "taken away"}, {"key": "C", "text": "has taken away"}, {"key": "D", "text": "was taken away"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  18,
  'Buses to the airport only come once every hour, and we just missed . Why don’t
we take a taxi?',
  '[{"key": "A", "text": "another"}, {"key": "B", "text": "it"}, {"key": "C", "text": "one"}, {"key": "D", "text": "them"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  19,
  'Ariel every night for a week before her Chinese test and got a very good grade.',
  '[{"key": "A", "text": "studied"}, {"key": "B", "text": "studies"}, {"key": "C", "text": "has studied"}, {"key": "D", "text": "was going to study"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  20,
  'While reading this story, Brad saw the word “trolling” and didn’t know what it meant.
Josh turned off the screen and sat back. “Why are they trolling me like this?” He didn’t
understand. They wanted him to share what he thought about the show, and he did.
And now look what he got. In the end, all they wanted was nice words.
He found several meanings of the word in a dictionary. Which one should Brad
choose?',
  '[{"key": "A", "text": "To celebrate in song."}, {"key": "B", "text": "To make someone or something move around."}, {"key": "C", "text": "To pull a fishing line through the water, often from a boat."}, {"key": "D", "text": "To write something on the Internet to hurt someone or make them angry."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  21,
  'What does Tea-Rock celebrate?',
  '[{"key": "A", "text": "Their sales in 20 countries."}, {"key": "B", "text": "The coming out of their 20th kind of tea."}, {"key": "C", "text": "Their 20th year of business."}, {"key": "D", "text": "The opening of their 20th store in the USA."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  22,
  'Here is the postcard Jason is going to send to Tea-Rock 20. What else does he need to
put on the postcard before he sends it?',
  '[{"key": "A", "text": "His age."}, {"key": "B", "text": "His address."}, {"key": "C", "text": "His birthday."}, {"key": "D", "text": "Another picture of the tea cup."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  23,
  'What can we learn about sugar from the infographic?',
  '[{"key": "A", "text": "There are 4 g of sugar in 66 g of ice cream."}, {"key": "B", "text": "A woman can eat as much sugar a day as a man can."}, {"key": "C", "text": "Taiwan eats more sugar for each person than the US does."}, {"key": "D", "text": "400 ml of rice milk has less sugar than 400 ml of grape juice."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  24,
  'What can be a reason why the list of “Sugar that is hidden in foods and drinks”
is put in the infographic?',
  '[{"key": "A", "text": "To help us understand how sugar hurts our body."}, {"key": "B", "text": "To show what kinds of foods and drinks are popular with children."}, {"key": "C", "text": "To tell us that we often have more sugar than we can without knowing it."}, {"key": "D", "text": "To let us know how much sugar is enough to make foods and drinks taste good."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  25,
  'Why did Darrell tell Marina to go to Pinterest?',
  '[{"key": "A", "text": "To find some examples for her homework."}, {"key": "B", "text": "To shop for things that are needed for art classes."}, {"key": "C", "text": "To meet new friends who have the same interests."}, {"key": "D", "text": "To share her works and tell people how they are made."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  26,
  'What does it mean when you learn something from A to Z?',
  '[{"key": "A", "text": "You can learn it at any time."}, {"key": "B", "text": "You learn it in a baking class."}, {"key": "C", "text": "You learn everything about it."}, {"key": "D", "text": "You spend all your life learning it."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  27,
  'Which idea is talked about in the first paragraph of the reading?',
  '[{"key": "A", "text": "How you should do Tabata training."}, {"key": "B", "text": "What is the best time for Tabata training."}, {"key": "C", "text": "Who first had the idea of Tabata training."}, {"key": "D", "text": "How often you should do Tabata training."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  28,
  'Who might find that Tabata training is right for them?',
  '[{"key": "A", "text": "People who enjoy team sports."}, {"key": "B", "text": "People who want to start exercising."}, {"key": "C", "text": "People who want to fix their heart problems."}, {"key": "D", "text": "People who already have a habit of exercising."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  29,
  'Which is true about Tabata training?',
  '[{"key": "A", "text": "It is difficult to learn the moves."}, {"key": "B", "text": "You are free to choose your own moves."}, {"key": "C", "text": "You need a large space to do the exercises."}, {"key": "D", "text": "You cannot rest between moves if you want the afterburn."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  30,
  'There are four important points in the report:
a. What “No Overtime Day” is
b. Why “No Overtime Day” fails
c. Why there is “No Overtime Day” in the country
d. How workers deal with “No Overtime Day”
 order 排序
How are they ordered in the report?',
  '[{"key": "A", "text": "acdb."}, {"key": "B", "text": "adcb."}, {"key": "C", "text": "cabd."}, {"key": "D", "text": "cadb."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  31,
  'What does this mean in the report?',
  '[{"key": "A", "text": "The way workers show they are hard-working."}, {"key": "B", "text": "Restaurants and coffee shops open until very late at night."}, {"key": "C", "text": "Workers do not go home when they walk out of the office."}, {"key": "D", "text": "The number of workers who get paid more and rise higher in the company."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  32,
  'What can we learn from Figure 1 and Figure 2?',
  '[{"key": "A", "text": "Long working hours killed more women than men in 2014."}, {"key": "B", "text": "Long working hours kills more and more workers every year."}, {"key": "C", "text": "Men usually have a bigger chance to get paid more and rise higher when they"}, {"key": "D", "text": "Men and women have almost the same chance to get paid more and rise higher"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  33,
  'Which map is most likely the map of Cameroon in 1962?  likely 可能',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  34,
  'What does resentful mean in the reading?',
  '[{"key": "A", "text": "Sad."}, {"key": "B", "text": "Angry."}, {"key": "C", "text": "Careful."}, {"key": "D", "text": "Worried."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  35,
  'What does Cameroon’s government most likely think of Ambazonia?',
  '[{"key": "A", "text": "It plans to do business with Ambazonia."}, {"key": "B", "text": "It needs Ambazonia for money and help."}, {"key": "C", "text": "It does not want to be part of Ambazonia."}, {"key": "D", "text": "It does not agree that Ambazonia is a country."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  36,
  'What does Elisa Grant try to tell readers by talking about the history of Cameroon?',
  '[{"key": "A", "text": "Why speaking English is a way to get power."}, {"key": "B", "text": "Why English speakers in Cameroon have less power."}, {"key": "C", "text": "Why the two parts of Cameroon became one country."}, {"key": "D", "text": "Why only 20% of the people in Cameroon speak English."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  37,
  'What is recommended to people who are visiting the Southend Trail?',
  '[{"key": "A", "text": "Camping on the side trails."}, {"key": "B", "text": "Biking along the side trails."}, {"key": "C", "text": "Hiking one part of the trail a day."}, {"key": "D", "text": "Visiting the museum in the morning."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  38,
  'What does lodging mean in the reading?',
  '[{"key": "A", "text": "A meal to have."}, {"key": "B", "text": "A place to stay in."}, {"key": "C", "text": "A time for visiting."}, {"key": "D", "text": "A way of moving around."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  39,
  'Kaylen will start his trip from Cove. He plans to visit one of the old castles. He also
wants to go birdwatching near the river. Which parts of the trail should Kaylen go on?',
  '[{"key": "A", "text": "Parts 1 and 2."}, {"key": "B", "text": "Parts 1 and 2a."}, {"key": "C", "text": "Parts 2 and 3."}, {"key": "D", "text": "Parts 4 and 4a."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  40,
  '(A) in fact (B) at first (C) of course (D) for example',
  '[{"key": "A", "text": "in fact"}, {"key": "B", "text": "at first"}, {"key": "C", "text": "of course"}, {"key": "D", "text": "for example"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  41,
  '(A) take sit (B) Ms Easy (C) it makes (D) me steak',
  '[{"key": "A", "text": "take sit"}, {"key": "B", "text": "Ms Easy"}, {"key": "C", "text": "it makes"}, {"key": "D", "text": "me steak"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  42,
  '(A) strange (B) difficult (C) delicious (D) important',
  '[{"key": "A", "text": "strange"}, {"key": "B", "text": "difficult"}, {"key": "C", "text": "delicious"}, {"key": "D", "text": "important"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '111年國中教育會考',
  'english_reading',
  43,
  '(A) more than just games (B) often played in public
(C) not so popular as before (D) not first used to learn words
13 試題結束',
  '[{"key": "A", "text": "more than just games"}, {"key": "B", "text": "often played in public"}, {"key": "C", "text": "not so popular as before"}, {"key": "D", "text": "not first used to learn words"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  1,
  '以下是一則論文摘要：「本文旨在說明臺灣國民小學至大學學生閱讀興趣與閱
讀素養的關係，以及不同學齡階段的讀寫素養表現。不論年級，閱讀興趣與閱
讀素養有正向關聯，然由一般學生投資於閱讀的時間反映出閱讀興趣有加強之
必要。」若要以這段文字的核心概念標示一組關鍵詞，下列何者最恰當？',
  '[{"key": "A", "text": "臺灣、學齡階段"}, {"key": "B", "text": "國民小學、大學"}, {"key": "C", "text": "正向關聯、閱讀時間"}, {"key": "D", "text": "閱讀興趣、閱讀素養"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  2,
  '下列文句何者有語病？',
  '[{"key": "A", "text": "他不但才華出眾，而且和藹可親"}, {"key": "B", "text": "幸虧你事先做好準備，否則災情慘重"}, {"key": "C", "text": "原來他有難言之隱，難怪總是愁眉不展"}, {"key": "D", "text": "與其讓你在事後落淚，難道讓你犯錯懊悔"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  3,
  '「彎曲的生命旅路，常常會被安排與許多人與事錯身而過 甲甲 有些注定是淡漠的
乙乙 並淪為遺忘 丙丙 有些則產生強烈衝擊 丁丁 終至刻骨銘心。」這段文字中的甲、
乙、丙、丁四處，何者最適合使用標點符號中的分號？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  4,
  '下列文句，何者語詞使用最恰當？',
  '[{"key": "A", "text": "你到底看見了什麼？豈非這樣驚訝"}, {"key": "B", "text": "並非我與他相識，這件事絕不可能善罷甘休"}, {"key": "C", "text": "你所說的無非是老生常談，他哪裡聽得進去"}, {"key": "D", "text": "若非我故意和你唱反調，實在是你的做法不合理"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  5,
  '下列選項「」中的字，何組讀音相同？',
  '[{"key": "A", "text": "「迄」今未成／「屹」立不搖"}, {"key": "B", "text": "金鑲玉「嵌」／命運「坎」坷"}, {"key": "C", "text": "寂「寥」冷清／「謬」誤百出"}, {"key": "D", "text": "千叮萬「囑」／引人「矚」目"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  6,
  '「齒」的甲骨文字形是□□字，看起來像張口見齒的
樣子。小篆字形在上部增加了「止」字，用「止」表示聲音，
至此變成了□□字。
這段文字的空格處，依序應填入何種造字原則？',
  '[{"key": "A", "text": "象形／會意"}, {"key": "B", "text": "指事／形聲"}, {"key": "C", "text": "象形／形聲"}, {"key": "D", "text": "指事／會意"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  7,
  '「上個世代對於永續住宅的普遍想像，總是不出屋頂上鋪滿太陽能板、隨意利用
各種回收廢棄物蓋成的缺乏整體感的建築物。許多這類大剌剌表現出『友善地
球』的建築物，也因此極易成為建築純粹主義者嘲弄的對象。他們語帶不屑地
認為，這簡直是以粗鄙的解決手法打敗了高尚審美觀。」根據這段文字，下列
哪一種住宅的特點最符合「建築純粹主義者」的主張？',
  '[{"key": "A", "text": "符合審美要求"}, {"key": "B", "text": "講求永續發展"}, {"key": "C", "text": "呈現建材原貌"}, {"key": "D", "text": "滿足居住需求"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  8,
  '「陰刻」是在平面上刻出凹陷的立體線條，凹陷下去的字是「陰文」。「陽刻」
則是在平面上保留凸出的立體線條，將其餘部分刻除，凸出來的字是「陽文」。
據此判斷，下列何者是陽刻隸書章蓋在白紙上顯示出的樣子？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  9,
  '小平欲致贈匾額祝賀下列四個單位，匾額上所使用的題辭何者不恰當？
單位 題辭',
  '[{"key": "A", "text": "美滿家具店 版築有功"}, {"key": "B", "text": "幸福大飯店 貴客盈門"}, {"key": "C", "text": "健康醫院 仁心仁術"}, {"key": "D", "text": "快樂國小 桃李滿門"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  10,
  '「夏七月，赤日停天，亦無風，亦無雲。前後庭赫然如洪爐，無一鳥敢來飛。
汗出遍身，縱橫成渠。置飯於前，不可得吃。呼簟欲臥地上，則地濕如膏，
蒼蠅又來緣頸附鼻，驅之不去。正莫可如何，忽然疾澍澎湃之聲，如數百萬
金鼓。簷溜浩於瀑布。身汗頓收，地燥如掃，蒼蠅盡去，飯便得吃。不亦快
哉！」根據這段文字，作者心情轉變的關鍵最可能是下列何者？',
  '[{"key": "A", "text": "發現美麗的景致"}, {"key": "B", "text": "遠離擾人的蟲蠅"}, {"key": "C", "text": "聽見悅耳的鼓聲"}, {"key": "D", "text": "驟降消暑的大雨"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  11,
  '下列文句，何者用字完全正確？',
  '[{"key": "A", "text": "大考將近，更要懂得善用索碎的時間"}, {"key": "B", "text": "來到默生的環境不免會令人感到緊張"}, {"key": "C", "text": "我忘了帶錢，拜託你先幫我代墊報名費"}, {"key": "D", "text": "這項工程是讓我國邁向現代化的里程盃"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  12,
  '「少室周為趙簡子之右 ，聞牛談有力，請與之競，弗勝，致 右焉。簡子許之，
1 2
使少室周為宰，曰：『知賢而讓，可以為訓矣。』」根據文意脈絡，下列何者最
適合用來說明「訓」字的意義？
',
  '[{"key": "A", "text": "典範"}, {"key": "B", "text": "順從"}, {"key": "C", "text": "教誨"}, {"key": "D", "text": "解釋"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  13,
  '「茲鄭引輦 上高梁 而不能支。茲鄭倚轅而歌，前者止，後者趨，輦乃上。使茲鄭
1 2
無術以致人，則身雖絕力至死，輦猶不上也。今身不至勞苦而輦以上者，有術
以致人之故也。」這段文字的主旨最可能是下列何者？',
  '[{"key": "A", "text": "團結就是力量"}, {"key": "B", "text": "做事要講究方法"}, {"key": "C", "text": "堅持到底才能成功"}, {"key": "D", "text": "沒有付出就沒有收穫"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  14,
  '下列文句「」中的詞語，何者使用最恰當？',
  '[{"key": "A", "text": "寵物一生病就丟棄的人，真是「若即若離」"}, {"key": "B", "text": "他缺乏耐性，總是「急公好義」，莽莽撞撞"}, {"key": "C", "text": "經過這次教訓後，他「幡然悔悟」，痛改前非"}, {"key": "D", "text": "期末將近，大家都「庸庸碌碌」，忙得不可開交"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  15,
  '甲：花寒懶發鳥慵啼，信馬閑行到日西。何處未春先有思？柳條無力魏王堤。
―― 白居易〈魏王堤〉
乙：陰陰溪曲綠交加，小雨翻萍上淺沙。鵝鴨不知春去盡，爭隨流水趁桃花。
―― 晁沖之〈春日〉
關於這兩首詩的分析，下列敘述何者最恰當？',
  '[{"key": "A", "text": "甲詩描寫清晨春寒料峭的景象"}, {"key": "B", "text": "乙詩描寫春末溪邊所見的景致"}, {"key": "C", "text": "兩詩首二句皆對仗，表達情思"}, {"key": "D", "text": "兩詩皆屬七絕，只有偶句用韻"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  16,
  '「蓋天下有反覆之小人，亦有反覆之君子。人但知不反覆不足以為小人，庸知不
反覆亦不足以為君子。蓋小人之反覆也，因風氣勢利之所歸，以為變動；君子之
反覆也，因學識之層累疊進，以為變動。其反覆同，其所以為反覆者不同。」根
據這段文字，作者認為「不反覆亦不足以為君子」的原因，最可能是下列何者？',
  '[{"key": "A", "text": "小人若洗心革面，一反前非即可成為君子"}, {"key": "B", "text": "為應對小人反覆，不得不改變既有的策略"}, {"key": "C", "text": "順應民心的向背，選擇最適合現況的做法"}, {"key": "D", "text": "隨著所知的增長，會修正自己原本的觀點"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  17,
  '以上是根據聯合國《2019年永續發展目標報告》製作的圖表。下列關於圖表內容
的推論，何者最不恰當？',
  '[{"key": "A", "text": "甲： 82% 的全球女性未曾遭受來自伴侶的身體或性暴力"}, {"key": "B", "text": "乙 ：全球女性在職場上擔任管理職位的比例較男性少"}, {"key": "C", "text": "丙 ：全球女性的參政比例有所提升，但仍為少數"}, {"key": "D", "text": "丁：2018 年至少有30%的20 至24 歲南亞女性結過婚"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  18,
  '「商代人只在上、下午各吃一餐，因為農業社會耕作頗費體力，早上需好好補
充精力，下午因太陽將西下，無法再工作，不如早睡早起，故不必吃得多。
春秋晚期以來，隨著牛耕鐵器的廣泛使用，尤其是戰國時代鐵器的普及，生產
力大大提高。社會的面貌起了很大的變化，人們的生活內容漸漸豐富起來，許
多人開始在夜間從事非生產性的工作，富人娛樂活動增加，便多一餐以補充體
力。」根據這段文字，古人從兩餐變成三餐的原因，與下列何者最不相關？',
  '[{"key": "A", "text": "社會形態改變"}, {"key": "B", "text": "夜間活動增加"}, {"key": "C", "text": "耕作時間延長"}, {"key": "D", "text": "鐵器廣泛使用"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  19,
  '「傳統布農族社會在舉行重大的祭儀活動前，族人會聚集在一起用木杵搗米準備
製作小米酒，發現不同的木杵會產生不同的聲響，因而將其作為合奏的樂器。後
來每當族人聽到杵音傳來，就知道最近聚落即將舉辦慶典，杵音也因而具有傳遞
訊息的功能。」根據這段文字，下列關於傳統布農族社會的推論，何者最恰當？',
  '[{"key": "A", "text": "舉行重大慶典需要小米酒"}, {"key": "B", "text": "透過傳遞木杵來交換訊息"}, {"key": "C", "text": "依祭儀種類飲用不同的米酒"}, {"key": "D", "text": "以整齊的杵音宣告祭儀開始"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  20,
  '蘇軾〈西江月〉：「世事一場大夢，人生幾度新涼？夜來風葉已鳴廊，看取眉
頭鬢上。 酒賤常愁客少，月明多被雲妨。中秋誰與共孤光，把盞淒然北
望。」下列關於詞句的說明，何者最不恰當？',
  '[{"key": "A", "text": "「看取眉頭鬢上」表達自己年華老去"}, {"key": "B", "text": "「酒賤常愁客少」意謂難以維持生計"}, {"key": "C", "text": "「月明多被雲妨」比喻美好的事物不可能長久"}, {"key": "D", "text": "「中秋誰與共孤光」流露想與親友團聚的心願"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  21,
  '1866 至1900 年甲國茶葉出口歐洲略表 單位：萬擔
年分 出口總額 年分 出口總額
1866 120 1886 240
1869 150 1889 187
1872 170 1892 162
1879 198 1897 153
1882 201 1900 120
說明：
1866 至1886 年間，甲國茶葉出口逐年大幅增長。歐洲國家茶葉生產技術
發展起來後，甲國茶葉出口總額急轉直下。從1886 至1900 的十五年間，甲國
茶葉出口銳減，在歐洲茶葉市場的占有率也從原本幾乎100%，急遽下降至
10% 左右。
根據這份表格及說明，可以推論出下列何者？',
  '[{"key": "A", "text": "甲國的茶葉生產技術在1886 年後越來越差"}, {"key": "B", "text": "1900 年歐洲茶葉市場總交易量較1886 年少"}, {"key": "C", "text": "1900 年甲國茶葉出口歐洲總額衰退至1886 年的 50%"}, {"key": "D", "text": "1866 至1900 年間，甲國從茶葉出口國變成茶葉進口國"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  22,
  '「復北上，行石罅中，石峰片片夾起，路宛轉石間，塞者鑿之，陡者級之，斷者
架木通之，懸者植梯接之。下瞰峭壑陰森，楓松相間，五色紛披，燦若圖繡。
因念黃山當生平奇覽，而有奇若此，前未一探，茲遊快且愧矣！」根據這段文
字，下列敘述何者最恰當？',
  '[{"key": "A", "text": "作者對自己破壞自然環境感到慚愧"}, {"key": "B", "text": "黃山片片石峰色彩繽紛，有如織錦"}, {"key": "C", "text": "作者北上舊地重遊，乃因懷念黃山冬季美景"}, {"key": "D", "text": "此遊窺得黃山奇景，作者心中因而喜愧交集"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  23,
  '往歲士人多尚對偶為文，穆脩、張景輩始為平文，當時謂之古文。穆、張
嘗同造朝，適見有奔馬踐死一犬，二人各記其事。穆脩曰：「馬逸 ，有黃犬
1
遇蹄而斃。」張景曰：「有犬死奔馬之下。」時文體新變，二人之語皆拙澀，
當時已謂之工，傳之至今。
根據這段文字，關於穆脩、張景針對奔馬踐死一犬的記事，下列敘述何者最恰當？',
  '[{"key": "A", "text": "穆脩記事只著眼於犬"}, {"key": "B", "text": "張景記事只著眼於馬"}, {"key": "C", "text": "二人用語崇尚句式對偶"}, {"key": "D", "text": "二人用語皆為時人稱頌"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  24,
  '「錢塘江石堤為洪濤所激，歲歲摧決。杜偉長為轉運使，人有獻說，自浙江稅場
以東，移退數里為月堤，以避怒水。眾水工皆以為善，獨一老水工以為不然，
密諭其黨：『移堤則歲無水患，吾等何所衣食？』眾人樂其利，乃從而和之。
偉長不悟其計，費以巨萬，而江堤之害仍歲有之。」根據這段文字，下列敘述
何者最恰當？',
  '[{"key": "A", "text": "月堤耗時過久，使杜偉長浪費公帑"}, {"key": "B", "text": "水工們為保生計，阻礙了移堤工程"}, {"key": "C", "text": "老水工深知修築月堤無益於防堵水患"}, {"key": "D", "text": "杜偉長堅持移堤，導致年年發生水患"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  25,
  '根據本詩，下列敘述何者最恰當？',
  '[{"key": "A", "text": "第一節顯示車行至八堵之後天氣不佳"}, {"key": "B", "text": "第二節說明作者此行目的地是暖暖"}, {"key": "C", "text": "第三節可看出那那社名稱的由來"}, {"key": "D", "text": "第四節點出作者珍惜當下的心境"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  26,
  '關於本詩的寫作手法，下列敘述何者錯誤？',
  '[{"key": "A", "text": "以天氣的變化象徵越來越沉重的心情"}, {"key": "B", "text": "以重複出現的字詞形成詩歌的韻律"}, {"key": "C", "text": "運用諧音及詞義的雙關增添詩意"}, {"key": "D", "text": "預想尚未發生的情景收束全詩"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  27,
  '根據圖文，下列關於跳水比賽的敘述，何者最恰當？',
  '[{"key": "A", "text": "入水時水花的大小會影響分數高低"}, {"key": "B", "text": "史上第一場跳水比賽是在室內舉行"}, {"key": "C", "text": "奧運比賽的雙人賽必須配置7名評審"}, {"key": "D", "text": "使用跳板起跳就可以獲得比較高的分數"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  28,
  '根據圖文，下列關於跳水比賽規則的敘述，何者最恰當？',
  '[{"key": "A", "text": "毋須採計每一跳的得分，可擇優計算最後成績"}, {"key": "B", "text": "選手完成一次跳水，每名評審最高只能給 10 分"}, {"key": "C", "text": "若完成的動作比預定的難度更高，分數也會越高"}, {"key": "D", "text": "選手每一跳須完成的難度係數，由現場抽籤決定"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  30,
  '文中「活著的時候就心甘情願把自己埋進納骨塔」的涵義，與下列何者最接近？',
  '[{"key": "A", "text": "獲得精神食糧，沉浸書堆"}, {"key": "B", "text": "倡導終身學習，推廣閱讀"}, {"key": "C", "text": "喪失生命熱情，心如死灰"}, {"key": "D", "text": "甘心隱姓埋名，不慕榮利"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  31,
  '關於本文的寫作手法，下列敘述何者最恰當？',
  '[{"key": "A", "text": "藉由宏偉的建築，對比個人的渺小"}, {"key": "B", "text": "以不同年齡層的閱讀習慣，凸顯世代差異"}, {"key": "C", "text": "將靜態的閱讀比擬為交談，產生動態的效果"}, {"key": "D", "text": "視線推移自室內延伸至室外，強調知識的寬廣"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  32,
  '根據甲、乙兩文，下列敘述何者最恰當？',
  '[{"key": "A", "text": "1880年代剛果曾提出瓜分非洲礦產的主張"}, {"key": "B", "text": "月球大使館公司成立時，人類尚未踏上月球"}, {"key": "C", "text": "沒人能挑戰霍普販賣月球地產是因《太空政策》期刊的論文"}, {"key": "D", "text": "國家需實際登陸月球後，方可成為《外太空條約》的締約國"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  33,
  '小貞讀過甲、乙兩文後，發現甲文中的霍普與乙文中的艾維斯對某項議題有
歧見，這項議題最可能是下列何者？',
  '[{"key": "A", "text": "太空探索是否應以和平進行為原則"}, {"key": "B", "text": "國家是否可以獨占有利的登月地點"}, {"key": "C", "text": "私人是否可以主張月球土地的所有權"}, {"key": "D", "text": "非締約國是否可以破壞他國的探測器"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  34,
  '根據本文，下列敘述何者最恰當？',
  '[{"key": "A", "text": "「智慧家庭」的數據資料庫能保護網路隱私"}, {"key": "B", "text": "網路上的瀏覽紀錄、按讚喜好具有商業價值"}, {"key": "C", "text": "只要設好高強度的密碼，就不用擔心個資外洩"}, {"key": "D", "text": "「優化人工智慧」是指電腦全面取代人類工作"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  35,
  '下列何者最符合本文的觀點？',
  '[{"key": "A", "text": "廣告客製化意謂著消費者主導了市場走向"}, {"key": "B", "text": "生活中使用網路服務，其實是用隱私換來的"}, {"key": "C", "text": "企業與政府受到輿論壓力而開始保護個人資料"}, {"key": "D", "text": "科技日新月異，可以保護我們的隱私不受侵犯"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  36,
  '根據本文，拿破崙選擇在巴黎聖母院加冕的原因，最可能是下列何者？',
  '[{"key": "A", "text": "仿效查理曼大帝的做法"}, {"key": "B", "text": "承襲歷代法國王室的傳統"}, {"key": "C", "text": "強調自己是新帝國的開創者"}, {"key": "D", "text": "希望由教皇而非蘭斯大主教加冕"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  37,
  '根據本文，大衛選擇採用拿破崙為約瑟芬加冕的畫面，原因最可能是下列何者？',
  '[{"key": "A", "text": "強調皇后的重要性"}, {"key": "B", "text": "避免損及教廷顏面"}, {"key": "C", "text": "滿足拿破崙的虛榮"}, {"key": "D", "text": "聽從拿破崙的指示"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  38,
  '小銘畫了以下這張〈拿破崙的加冕禮〉的模擬圖，根據本文對雅克路易．大衛
原畫的描述，小銘的模擬圖與原畫相比後有明顯的錯誤，下列何者最可能是這
個錯誤？',
  '[{"key": "A", "text": "十字架擺放的位置"}, {"key": "B", "text": "拿破崙加冕的對象"}, {"key": "C", "text": "教皇給予祝福的手"}, {"key": "D", "text": "拿破崙母親的出席"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  39,
  '根據本文，下列何者最可能是仇鸞與嚴嵩一開始交惡的原因？ 1.內：宮廷',
  '[{"key": "A", "text": "嚴嵩私下上奏，詆毀仇鸞"}, {"key": "B", "text": "嚴嵩與曾銑結盟，疏遠仇鸞"}, {"key": "C", "text": "仇鸞向皇帝稟告嚴嵩父子的罪行"}, {"key": "D", "text": "仇鸞權位日重，不願嚴嵩仍以子視之"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  40,
  '下列文句的解說，何者最恰當？',
  '[{"key": "A", "text": "門者以非詔旨格之：守門者將徐階、李本擋下"}, {"key": "B", "text": "嵩還第，父子對泣：嚴嵩與仇鸞兩人盡釋前嫌"}, {"key": "C", "text": "炳訐鸞陰事，帝追戮之：皇帝認為陸炳毀謗死者，憤而殺之"}, {"key": "D", "text": "遣所乘龍舟過海子召嵩：皇帝以高規格召回嚴嵩，以示禮遇"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  41,
  '根據本文，關於梁王與楊朱的敘述，下列何者最恰當？',
  '[{"key": "A", "text": "梁王認為治理天下應重視禮樂之道"}, {"key": "B", "text": "梁王質疑楊朱是否具有治理天下的能力"}, {"key": "C", "text": "楊朱貶抑堯、舜，能治天下卻不能牧羊"}, {"key": "D", "text": "楊朱以牧羊為例，說明治天下須從小事做起"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'chinese',
  42,
  '下列文句，何者最能呼應文中「吞舟之魚，不游支流；鴻鵠高飛，不集汙池」
的涵義？',
  '[{"key": "A", "text": "狡兔死，良狗烹；高鳥盡，良弓藏"}, {"key": "B", "text": "高飛之鳥，死於美食；深泉之魚，死於芳餌"}, {"key": "C", "text": "騏驥千里，一日而達；駑馬十駕，旬亦至之"}, {"key": "D", "text": "剖三寸之蚌，難得明月之珠；探枳棘之巢，難求鳳凰之雛"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  1,
  '(−3)3 之值為何？',
  '[{"key": "A", "text": "−27"}, {"key": "B", "text": "−9"}, {"key": "C", "text": "9"}, {"key": "D", "text": "27"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  2,
  '下列何者為多項式 x2 − 36 的因式？',
  '[{"key": "A", "text": "x − 3"}, {"key": "B", "text": "x − 4"}, {"key": "C", "text": "x − 6"}, {"key": "D", "text": "x − 9"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  3,
  '圖(一)的立體圖形由相同大小的正方體積木堆疊
而成。判斷拿走圖(一)的哪一個積木後，此圖形
前視圖的形狀會改變？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  4,
  '化簡 135 的結果為下列何者？',
  '[{"key": "A", "text": "3 5"}, {"key": "B", "text": "27 5"}, {"key": "C", "text": "3 15"}, {"key": "D", "text": "9 15"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  5,
  '坐標平面上，一次函數 y = −2x − 6 的圖形通過下列哪一個點？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  6,
  '已知 a = −1，b = −1 ，c = −1 ，下列關於 a、b、c 三數的大小關係，何者
4 8
正確？',
  '[{"key": "A", "text": "a > c > b"}, {"key": "B", "text": "a > b > c"}, {"key": "C", "text": "b > c > a"}, {"key": "D", "text": "c > b > a"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  7,
  '如圖 ( 二 )，坐標平面上直線 L 的方程式為 x = −5，
直線 M 的方程式為 y = −3，P 點的坐標為 (a,b)。
根據圖 ( 二 ) 中 P 點位置判斷，下列關係何者正確？',
  '[{"key": "A", "text": "a < −5，b > −3"}, {"key": "B", "text": "a < −5，b < −3"}, {"key": "C", "text": "a > −5，b > −3"}, {"key": "D", "text": "a > −5，b < −3"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  8,
  '如圖 ( 三 )，梯形 ABCD 中，AD // BC。若 ∠ADC = 140°，且 BD⊥CD，
則 ∠DBC 的度數為何？ A D',
  '[{"key": "A", "text": "30"}, {"key": "B", "text": "40"}, {"key": "C", "text": "50"}, {"key": "D", "text": "60"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  9,
  '有多少個正整數是 18 的倍數，同時也是 216 的因數？',
  '[{"key": "A", "text": "2"}, {"key": "B", "text": "6"}, {"key": "C", "text": "10"}, {"key": "D", "text": "12"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  10,
  '利用公式解可得一元二次方程式 3x2 − 11x − 1 = 0 的兩解為 a、b，且 a > b，
求 a 值為何？
−11 + 109',
  '[{"key": "A", "text": "6"}, {"key": "B", "text": "6"}, {"key": "C", "text": "6"}, {"key": "D", "text": "6"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  11,
  '業者販售含咖啡因飲料時通常會以紅、黃、綠三色來標示每杯飲料的咖啡因
含量，各顏色的意義如表 ( 一 ) 所示。
表(ㄧ) 表(二)
我國建議每位成人一日的咖啡因攝取量不超過 300 毫克，歐盟則建議一日
不超過 400 毫克。表 ( 二 ) 為某商店美式咖啡的容量及咖啡因含量標示，已知
該店美式咖啡每毫升的咖啡因含量相同，判斷一位成人一日喝 2 杯該店中杯的
美式咖啡，其咖啡因攝取量是否符合我國或歐盟的建議？',
  '[{"key": "A", "text": "符合我國也符合歐盟"}, {"key": "B", "text": "不符合我國也不符合歐盟"}, {"key": "C", "text": "符合我國，不符合歐盟"}, {"key": "D", "text": "不符合我國，符合歐盟"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  12,
  '盒玩的販售方式是將一款玩具裝在盒子中販賣，購買者只能從外盒知道購買
的是哪一系列玩具，但無法知道是系列中的哪一款。圖 ( 四 )、圖 ( 五 ) 分別
為動物系列、汽車系列盒玩中所有可能出現的款式。
圖(四) 圖(五)
已知小友喜歡圖 ( 四 ) 中的 A 款、C 款，喜歡圖 ( 五 ) 中的 B 款，若他打算
購買圖(四)的盒玩一盒，且他買到圖(四)中每款玩具的機會相等；他也打算
購買圖 ( 五 ) 的盒玩一盒，且他買到圖 ( 五 ) 中每款玩具的機會相等，則他買
到的兩盒盒玩內的玩具都是他喜歡的款式的機率為何？
1',
  '[{"key": "A", "text": "15"}, {"key": "B", "text": "10"}, {"key": "C", "text": "11"}, {"key": "D", "text": "11"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  13,
  '如圖 ( 六 )，直角柱 ABCDEF 的底面為直角三角形。
若 ∠ABC = ∠DEF = 90°， BC > AB > BE，則連接 AE
後，下列敘述何者正確？',
  '[{"key": "A", "text": "∠ACB < ∠FDE，∠AEB > ∠ACB"}, {"key": "B", "text": "∠ACB < ∠FDE，∠AEB < ∠ACB"}, {"key": "C", "text": "∠ACB > ∠FDE，∠AEB > ∠ACB"}, {"key": "D", "text": "∠ACB > ∠FDE，∠AEB < ∠ACB"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  14,
  '坐標平面上有兩個二次函數的圖形，其頂點 P、Q 皆在 x 軸上，且有一水平線
與兩圖形相交於 A、B、C、D 四點，各點位置如圖 ( 七 ) 所示。若 AB = 10，
BC = 5，CD = 6，則 PQ 的長度為何？',
  '[{"key": "A", "text": "7"}, {"key": "B", "text": "8"}, {"key": "C", "text": "9"}, {"key": "D", "text": "10"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  15,
  '若想在等差數列 1 , 2 , 3 , 4 , 5中插入一些數，使得新的數列也是等差數列，且
新的數列的首項仍是 1，末項仍是 5，則新的數列的項數可能為下列何者？',
  '[{"key": "A", "text": "11"}, {"key": "B", "text": "15"}, {"key": "C", "text": "30"}, {"key": "D", "text": "33"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  16,
  '已知某速食店販售的套餐內容為一片雞排和一杯可樂，且一份套餐的價錢比
單點一片雞排再單點一杯可樂的總價錢便宜 40 元。阿俊打算到該速食店
買兩份套餐，若他發現店內有單點一片雞排就再送一片雞排的促銷活動，
且單點一片雞排再單點兩杯可樂的總價錢，比兩份套餐的總價錢便宜 10 元，
則根據題意可得到下列哪一個結論？',
  '[{"key": "A", "text": "一份套餐的價錢必為 140 元"}, {"key": "B", "text": "一份套餐的價錢必為 120 元"}, {"key": "C", "text": "單點一片雞排的價錢必為 90 元"}, {"key": "D", "text": "單點一片雞排的價錢必為 70 元"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  18,
  '樂樂停車場為 24 小時營業，其收費方式如
表(三)
表(三)所示。已知阿虹某日 10:00 進場
停車，停了 x 小時後離場，x 為整數。若
阿虹離場的時間介於當日的 20:00 ~ 24:00
間，則他此次停車的費用為多少元？',
  '[{"key": "A", "text": "5x + 30"}, {"key": "B", "text": "5x + 50"}, {"key": "C", "text": "5x + 150"}, {"key": "D", "text": "5x + 200"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  19,
  '圖 ( 九 ) 為一圓形紙片，A、B、C 為圓周上三點，其中 AC 為直徑。今以
AB 為摺線將紙片向右摺後，紙片蓋住部分的 AC，而 AB 上與 AC 重疊的點
為 D，如圖 ( 十 ) 所示。若 BC = 35°，則 AD 的度數為何？',
  '[{"key": "A", "text": "105"}, {"key": "B", "text": "110"}, {"key": "C", "text": "120"}, {"key": "D", "text": "145"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  20,
  '如圖 ( 十一 )，ΔABC 中，D 點在 BC 上，且 BD
的中垂線與 AB 相交於 E 點，CD 的中垂線與 AC
相交於 F 點。已知 ΔABC 的三個內角皆不相等，
根據圖(十一)中標示的角， 判斷下列敘述何者正確？',
  '[{"key": "A", "text": "∠1 = ∠3，∠2 = ∠4"}, {"key": "B", "text": "∠1 = ∠3，∠2 ≠ ∠4"}, {"key": "C", "text": "∠1 ≠ ∠3，∠2 = ∠4"}, {"key": "D", "text": "∠1 ≠ ∠3，∠2 ≠ ∠4"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  21,
  '圖(十二)
有一東西向的直線吊橋橫跨溪谷，小維、阿良分別從西橋頭、東橋頭同時開始
往吊橋的另一頭筆直地走過去， 如圖 ( 十二 ) 所示。 已知小維從西橋頭走了
84 步，阿良從東橋頭走了 60 步時，兩人在吊橋上的某點交會，且交會之後
阿良再走 70 步恰好走到西橋頭。若小維每步的距離相等，阿良每步的距離
相等，則交會之後小維再走多少步會恰好走到東橋頭？',
  '[{"key": "A", "text": "46"}, {"key": "B", "text": "50"}, {"key": "C", "text": "60"}, {"key": "D", "text": "72"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  22,
  '如圖 ( 十三 )，正方形 ABCD 與 ΔEBC 中，AD 分別與
EB、EC 相交於 F 點、G 點。若 ΔEBG 的面積為 6，
正方形 ABCD 的面積為 16，則 FG 與 BC 的長度比為何？',
  '[{"key": "A", "text": "3 : 5"}, {"key": "B", "text": "3 : 6"}, {"key": "C", "text": "3 : 7"}, {"key": "D", "text": "3 : 8"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  23,
  '如圖 ( 十四 )，矩形 ABCD 中， AB = 6，AD = 8，且有一點 P 從 B 點沿著
BD 往 D 點移動。若過 P 點作 AB 的垂線交 AB 於 E 點，過 P 點作 AD 的
垂線交 AD 於 F 點，則 EF 的長度最小為多少？
14',
  '[{"key": "A", "text": "5"}, {"key": "B", "text": "5"}, {"key": "C", "text": "5"}, {"key": "D", "text": "7"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  24,
  '圖(十五)為某機構於 2020 年繪製的四個國家 65 歲以上人口占總人口百分比
之折線圖，其中 2020 年之後的數值為推估值。
圖(十五)
根據圖 ( 十五 ) 推測，下列哪一個國家從進入「高齡社會」到進入「超高齡
社會」所花的時間最短？',
  '[{"key": "A", "text": "法國"}, {"key": "B", "text": "義大利"}, {"key": "C", "text": "美國"}, {"key": "D", "text": "韓國"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'math',
  25,
  '已知 2019 年我國進入「高齡社會」，預測 2025 年會進入「超高齡社會」。
假設我國 2019 年與 2025 年總人口數皆為 2300 萬人，且 2019 年我國 65 歲
以上人口占總人口的百分比恰好達到「高齡社會」的最低標準，則根據上述
預測， 關於我國 65 歲以上人口數，2025 年與 2019 年相比至少增加了多少萬人？',
  '[{"key": "A", "text": "138"}, {"key": "B", "text": "161"}, {"key": "C", "text": "322"}, {"key": "D", "text": "460"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  1,
  '近年來，在政府與民間的努力下，開發出米麵包、米蛋糕、米布丁、米鳳梨
酥、米冰淇淋等新米食。上述作法最可能達成下列何項效益？',
  '[{"key": "A", "text": "降低稻米生產成本"}, {"key": "B", "text": "減少水稻耕作人力"}, {"key": "C", "text": "減輕稻米過剩壓力"}, {"key": "D", "text": "確保米食安全管理"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  2,
  '交通部 公路總局為了滿足部分地區民眾就學、就醫及
洽公的需求，以及達成某項目的，推動「幸福巴士」
政策。圖(一)為2019年8月時設有營運路線的行政區分
布。根據上述及右圖資訊推論，該目的最可能為下列
何者？',
  '[{"key": "A", "text": "串連北中南的工業園區"}, {"key": "B", "text": "降低高速公路的車流量"}, {"key": "C", "text": "增加高鐵接駁的便利性"}, {"key": "D", "text": "彌補公共運輸網的不足"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  3,
  '格陵蘭島位處北極圈附近，某研究針對島上居民進行「氣候變遷對人類心理
影響」的抽樣調查，結果顯示大部分受訪者曾親身經歷全球暖化對生活帶來
的影響，氣候變遷正為北極地區居民帶來前所未有的壓力和焦慮。下列何者
最可能為當地居民擔憂的事情？',
  '[{"key": "A", "text": "日益變薄的冰層讓雪橇通行變得危險"}, {"key": "B", "text": "冰河侵蝕日漸增強導致耕地面積減少"}, {"key": "C", "text": "海中珊瑚大量死亡造成觀光收益下滑"}, {"key": "D", "text": "氣溫逐年變化使得冬天變長夏天變短"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  4,
  '表(一)為中國不同年分的人口普查部分資料。觀察表中幼年人口比例的變動，
下列何者最可能是造成2010到2020年微幅變化的原因之一？
表(一) 單位：%
年分
1953 1964 1982 1990 2000 2010 2020
年齡組成
0-14 歲 36.28 40.69 33.59 27.69 22.89 16.60 17.95
15-64 歲 59.31 55.75 61.50 66.74 70.15 74.53 68.55
65 歲以上 4.41 3.56 4.91 5.57 6.96 8.87 13.50',
  '[{"key": "A", "text": "開放生育第二胎"}, {"key": "B", "text": "實施一胎化政策"}, {"key": "C", "text": "重男輕女觀念式微"}, {"key": "D", "text": "嚴格限制人口移入"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  5,
  '清末一位知識分子提到：「今日多數的中國婦女終身只待在家中，不曾見過
什麼人、沒去過其他城市、身邊沒有學習的夥伴而孤陋寡聞，只能學一些無
關緊要的東西，而這些東西遠比不上有用的知識。這是因為現在還有毀壞人
體的風俗，這樣的風俗沒有廢除，新式的女子學校就無法設立。這項風俗延
續了數百年直到今日，是外國人眼中的笑柄。」上述「風俗」最可能是下列
何者？',
  '[{"key": "A", "text": "自幼纏足"}, {"key": "B", "text": "吸食鴉片"}, {"key": "C", "text": "剃度出家"}, {"key": "D", "text": "薙髮留辮"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  6,
  '表(二)為兩個雜誌社的成員，他們在某時期曾 表(二)
遭法院判刑入獄。隨著時局更迭，2019年政 雜 誌 社 成 員
府公告撤銷原本的有罪判決，讓他們獲得平 自由中國 雷震等人
反。表中人員當時被判刑，最可能與下列何 美麗島 黃信介等人
者有關？',
  '[{"key": "A", "text": "受威爾遜的影響，主張民族自決"}, {"key": "B", "text": "反對皇民化時期推動的統治措施"}, {"key": "C", "text": "挑戰戒嚴時期對人民權利的限制"}, {"key": "D", "text": "聲援六四天安門事件，發動遊行"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  8,
  '李科羅是一位天主教傳教士，1655年前往廈門傳教，並得到當地統治者「國
姓爺」的關照；他也為國姓爺父子擔任使者，出使菲律賓。但1663年李科羅
結束使者任務返回廈門時，卻遭當地的新統治者逮捕；他擔心被送往北京，
因此在洪水氾濫期間，趁亂逃亡，最後輾轉逃到臺灣。李科羅逃亡的原因，
最可能與下列何者有關？',
  '[{"key": "A", "text": "日本與荷蘭互相合作"}, {"key": "B", "text": "荷蘭與西班牙互相敵對"}, {"key": "C", "text": "鄭氏政權與英國互相合作"}, {"key": "D", "text": "清帝國與鄭氏政權互相敵對"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  9,
  '我國國民在面對新冠肺炎疫情時，可透過接種疫苗來降低染疫風險，但逾期
停留或逾期居留的外國人卻無法接種疫苗，一旦染疫後，可能也無法得到適
當的醫療服務，甚至危及他們的生命安全，因此有民間團體呼籲政府應將這
些人納入公費疫苗施打對象。後來，政府基於防疫需求與風險控管，在國內
疫苗供應充足的情況下，以專案方式為這些人施打疫苗。上述民間團體的呼
籲隱含下列哪一觀點？',
  '[{"key": "A", "text": "公民參政權應受到重視"}, {"key": "B", "text": "政府應得到人民定期授權"}, {"key": "C", "text": "基本人權應受到普遍性保障"}, {"key": "D", "text": "國家權力應受制衡以免遭濫用"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  12,
  '某日，小晴沒來上課，班上同學們問
《紀念日及節日實施辦法》第4條：
了老師才知道，因為小晴是太魯閣族
下列民俗節日，除春節放假三日
的原住民，所以他今天放假和家人一
外，其餘均放假一日：
起返回部落參與感恩祭。老師也藉機 一、春節。
以圖(五)中的法律規範，向同學們說
明小晴可以放假的依據。根據上述內
六、原住民族歲時祭儀：各該原住
容判斷，主管機關將原住民族的傳統
民族放假日期，由行政院原住
祭儀納入法律規範的原因，其主要考
民族委員會參酌各該原住民族
量最可能是下列何者？
習俗公告，並刊登政府公報。',
  '[{"key": "A", "text": "落實部落自治，提升地方行政效率"}, {"key": "B", "text": "推動觀光發展，增加青年工作機會"}, {"key": "C", "text": "凝聚居民認同，改善社區生活環境"}, {"key": "D", "text": "尊重多元文化，促進部落文化傳承"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  13,
  '棗椰樹屬於棕櫚科植物，主要分布在熱帶乾燥地區，其果實稱為椰棗，既可
作糧食，又是製糖的原料。全球有上億棵棗椰樹，其中前兩大分布區為西亞
和甲地區，椰棗也成為這些地區重要的出口農產品。上述甲地區最可能為下
列何者？',
  '[{"key": "A", "text": "北非"}, {"key": "B", "text": "南歐"}, {"key": "C", "text": "中美洲"}, {"key": "D", "text": "東南亞"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  14,
  '圖(六)的詩為唐代詩人登上今湖北 襄陽的一座山
頭，見石碑碑文有感而發之作。詩中「水落魚梁
淺」指山腳下的魚梁沙洲因水位變化而露出水面，
作者藉以說明環境與世事的變化。關於形成「水落
魚梁淺」現象的原因，下列推論何者最為適切？
圖(六)',
  '[{"key": "A", "text": "沙洲上游融冰增加造成水位升降"}, {"key": "B", "text": "季節性降水差異產生的水位變化"}, {"key": "C", "text": "海平面上升海水入侵內陸造成水位改變"}, {"key": "D", "text": "在沙洲下游河段興築大型堤壩導致水位的變化"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  17,
  '《周成過臺灣》是著名的民間傳說，其時代背景符合史實。故事描述周成拋
下故鄉泉州的妻兒，獨自來臺經商。適逢淡水、雞籠開港通商，周成在大稻
埕從事新興商品出口而致富。後來周成移情別戀，謀殺了來臺灣探視的妻
子，最終受到報應而死。根據上述內容，周成最有可能從事下列何種商品的
貿易？',
  '[{"key": "A", "text": "茶葉"}, {"key": "B", "text": "鹿皮"}, {"key": "C", "text": "蔗糖"}, {"key": "D", "text": "鴉片"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  18,
  '以下是某歷史人物在其著作中的相關內容：「我們可以假設人類在社會形成
以前，所有人都是平等的。然而人們為了解決集體生活所產生的問題，透過
公眾的協商形成公意，且將全部的權力，託付由公意組成的政府，因為能夠
代表公意的政府，是不受私念限制、必然公正的。政府依循公意制定法律、
建立秩序，人們只要守法、服從公意，就能得到真正的自由。」上述內容最
可能與下列何者有關？',
  '[{"key": "A", "text": "盧梭關於主權在民的主張"}, {"key": "B", "text": "希特勒針對種族主義的論述"}, {"key": "C", "text": "馬克思對於工廠制度的批評"}, {"key": "D", "text": "孟德斯鳩闡明三權分立的觀點"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  19,
  '圖(八)是霞喀羅國家步道的介紹圖，其舊名為「霞喀羅、薩克亞金警備道路」。
此道路的開闢，是因為過去臺灣統治者為達到某一目的而下令修築。根據圖中
內容判斷，統治者最初開闢這條道路的目的，最可能與下列何者有關？
(cid:23076)(cid:10909)(cid:10838)(cid:8909)(cid:26766)(cid:9702)(cid:12542)(cid:24376)(cid:23711) (cid:261)(cid:17722)(cid:17084)(cid:16236)(cid:20664)(cid:433)(cid:24715)(cid:14621)(cid:14475)(cid:25889)(cid:9710)(cid:24376)(cid:23711)
(cid:261)(cid:12604)(cid:8430)(cid:19707)(cid:17953)(cid:11610)(cid:10950)(cid:23457)(cid:11006)(cid:17373)(cid:17376)(cid:17730)(cid:24592)(cid:17332)
(cid:14883)(cid:24337)(cid:24714)(cid:18633)
(cid:19)(cid:78)(cid:80) (cid:21)(cid:21)(cid:78)(cid:80)
(cid:11)(cid:20)(cid:15)(cid:26)(cid:21)(cid:28)(cid:12) (cid:11)(cid:21)(cid:15)(cid:19)(cid:23)(cid:22)(cid:12) (cid:11)(cid:20)(cid:15)(cid:25)(cid:23)(cid:24)(cid:12) (cid:11)(cid:20)(cid:15)(cid:24)(cid:19)(cid:19)(cid:12)
(cid:28875)(cid:12714)(cid:21789)(cid:8229)(cid:13366)(cid:10773)(cid:16248)(cid:15413)(cid:12690)(cid:27030)(cid:11620)(cid:28629)(cid:9324)(cid:7691)(cid:16248)(cid:8234)(cid:11000)(cid:434)
圖(八)',
  '[{"key": "A", "text": "劃界封山的施行"}, {"key": "B", "text": "新式製糖的推動"}, {"key": "C", "text": "海運港口的整建"}, {"key": "D", "text": "理蕃政策的實施"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  20,
  '「關於我的『政治主張』，因為和蔣委員長在意見上的衝突，已經沒有和解的
跡象。我考慮了三種方法來解決此事，第一是辭職、第二是勸諫、第三是兵
諫。第一個方法因為我的國難家仇，和東北軍部下們的反對而不可行。最近我
試了第二個方法，但導致蔣委員長極端憤怒。因此我決定採取第三個方法，以
武力拘禁蔣委員長。」上述「政治主張」最可能為下列何者？',
  '[{"key": "A", "text": "立即停止內戰，聯合各黨派抗日"}, {"key": "B", "text": "反對洪憲帝制，起兵討伐袁世凱"}, {"key": "C", "text": "終結軍閥混戰，完成中國的統一"}, {"key": "D", "text": "攘外必先安內，全力剿滅共產黨"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  21,
  '雅加達自十七世紀以來一直是印尼的政治、經濟中心，不過由於人口過於集
中加上大量開發，對環境已產生過多負荷。近年來，雅加達的民眾飽受交通
壅塞、空氣汙染、地層下陷及水患之苦，因此印尼政府計畫將首都遷至婆羅
洲。但有生態專家提出警告，該處是紅毛猩猩的棲息地，遷都計畫所需的開
發過程必須謹慎評估，否則反而可能破壞環境，造成生態浩劫。上述討論內
容與下列何項議題最相符？',
  '[{"key": "A", "text": "歷史古都的文化保存"}, {"key": "B", "text": "遷移首都的機會成本"}, {"key": "C", "text": "都市人口結構的變化"}, {"key": "D", "text": "群島國家國土的擴張"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  22,
  '國際刑警組織共有195個成員國，總部建有一個存放上百萬名國際刑事罪犯檔
案的資料庫供成員國使用。我國目前受限於一個中國原則，無法加入此國際
組織，因此未能分享或接收該組織的情報資訊，所以難以確認入境我國的旅
客在境外是否有犯罪紀錄，而從我國潛逃出境的犯罪者也較難被繩之以法。
上述內容顯示一個中國原則對我國產生下列哪一影響？',
  '[{"key": "A", "text": "兩岸互信不足造成軍事衝突現象頻傳"}, {"key": "B", "text": "兩岸交流趨緩使得經濟貿易往來受阻"}, {"key": "C", "text": "資訊科技落差造成區域發展程度不均"}, {"key": "D", "text": "資訊傳達受限使得國內治安風險升高"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  23,
  '圖(九)呈現我國1998至2018年間，
(cid:21)(cid:24) (cid:19568) (cid:24719)
收入最高20%家庭與收入最低20% (cid:21)(cid:19) (cid:23725) (cid:22091)
(cid:20)(cid:24) (cid:15263) (cid:15413)
家庭的可支配所得成長率變化，其 (cid:12494) (cid:15209) (cid:9453)
(cid:20)(cid:19)
(cid:25653)
中灰階區塊是曾發生經濟成長率大 (cid:16965) (cid:24)
(cid:19)
幅衰退的兩段時間。根據圖中內容 (cid:11)(cid:8)(cid:12)
(cid:16)(cid:24)
判斷，上述兩個灰階區塊的數據， (cid:16)(cid:20)(cid:19)
(cid:16)(cid:20)(cid:24)
呈現出下列哪一現象？
(cid:20)(cid:28)(cid:28)(cid:27) (cid:21)(cid:19)(cid:19)(cid:21) (cid:21)(cid:19)(cid:19)(cid:25) (cid:21)(cid:19)(cid:20)(cid:19) (cid:21)(cid:19)(cid:20)(cid:23) (cid:21)(cid:19)(cid:20)(cid:27)(cid:11)(cid:11570)(cid:12)
(cid:13300)(cid:8227)(cid:13758)(cid:27030)(cid:21)(cid:19)(cid:8)(cid:10868)(cid:11627)
&家庭可支配所得：家庭可以自由使用 (cid:13300)(cid:8227)(cid:13758)(cid:7692)(cid:21)(cid:19)(cid:8)(cid:10868)(cid:11627)
於消費或儲蓄的所得。 圖(九)',
  '[{"key": "A", "text": "收入較高者的財富減損情況較嚴重"}, {"key": "B", "text": "收入較低者的生活面臨較嚴重衝擊"}, {"key": "C", "text": "經濟大幅衰退造成區域間發展不均"}, {"key": "D", "text": "經濟大幅衰退反而縮小了貧富差距"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  24,
  '甲在質詢行政院 衛生福利部部長時，指出某飲料製造商早已知道自家產品出
現變質問題，嚴重影響消費者權益，但該公司卻不主動回收處理，反而繼續
販售變質的產品，對於這種明知故犯的行為，政府應予以重罰。關於甲所擔
任的公職，下列敘述何者正確？',
  '[{"key": "A", "text": "負責審查法律是否違憲"}, {"key": "B", "text": "負責審查中央政府預算"}, {"key": "C", "text": "經由地方層級的選舉所產生"}, {"key": "D", "text": "由行政院院長提請總統任命"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  26,
  '圖(十一)為貫穿美洲的泛美
公路示意圖，主幹線北起美
國 阿拉斯加，南至智利。美
洲多國可透過這個公路系統
相互連結，但巴拿馬到哥倫
比亞之間的路段至今尚未修
建。根據圖中資訊判斷，該
路段未修建的原因之一最可
能為下列何者？',
  '[{"key": "A", "text": "年溫差大施工困難"}, {"key": "B", "text": "保護熱帶雨林生態"}, {"key": "C", "text": "運河阻隔難以跨越"}, {"key": "D", "text": "維護因紐特人文化"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  27,
  '西班牙海外島嶼的某座火
山於2021年 9月噴發，圖
(十二)為其噴發後熔岩流
及火山灰落塵分布的狀
況。根據圖中資訊判斷，
下列推論何者較為合理？',
  '[{"key": "A", "text": "當時的主要風向為西風"}, {"key": "B", "text": "該區域的地勢西高東低"}, {"key": "C", "text": "火山熔岩流向西流往太平洋"}, {"key": "D", "text": "火山噴發地點距海約6公里"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  28,
  '臺灣本島的經緯度約介於22°N～25°N，
120°E～122°E 之間，降水的空間分布受到
地形及季風的影響而有顯著差異。表(三)為
本島四個氣象測站的資料，根據各測站位置
及地形判斷，何者的年降水量可能最多？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  29,
  '「距今六千多年前，此地區的人們觀察到，大約每隔365天，天狼星在拂曉的
時候，和太陽同時位於東方的地平線上。因此他們定365天為一年，每年分為
12個月，每月30天，年末加上5天。這種遵循太陽週期的曆法，依自然現象將
一年分為『阿赫特』、『佩雷特』、『夏矛』三個季節，有別於同時期兩河流
域的月亮週期曆法。」根據上文，「此地區」的發明最可能與下列何者有關？',
  '[{"key": "A", "text": "推算河川氾濫情形，掌握農業生產"}, {"key": "B", "text": "公民參與城邦事務，展現民主精神"}, {"key": "C", "text": "基於因果輪迴觀念，建立階級制度"}, {"key": "D", "text": "追尋宇宙創世真理，崇奉一神信仰"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  30,
  '某中共領導人接見日本國會議員時提到：「戰後日本很快就發達起來，這經
驗很值得中國學習。當然，別人的經驗照搬也不行，中國有中國的條件，日
本有日本的條件。我們不但要引進發達國家的資金和技術，充分利用各國的
好經驗，並且要把這種經驗與中國的實際情況結合起來。」上述談話最可能
與下列何者有關？',
  '[{"key": "A", "text": "發起文化大革命，破除四舊"}, {"key": "B", "text": "推動農工大躍進，超英趕美"}, {"key": "C", "text": "沒收地主土地，分配給貧農"}, {"key": "D", "text": "實施改革開放，設經濟特區"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  31,
  '表(四)呈現甲國於兩次世界大戰中， 表(四)
在歐洲戰場開始參戰與結束參戰的 甲國在歐洲 第一次 第二次
原因。表中的「？」最適合填入下 戰場的情形 世界大戰 世界大戰
列何者？ 開始 支援「斯拉 德國毀約攻',
  '[{"key": "A", "text": "美國投下原子彈，敵國投降 參戰的原因 夫兄弟」 打國土"}, {"key": "B", "text": "簽署《凡爾賽條約》，戰敗投降 結束"}, {"key": "C", "text": "國內共產政權成立，向同盟國議和 參戰的原因"}, {"key": "D", "text": "美國反對無限制潛艇政策，援助協約國"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  32,
  '西元前十ㄧ世紀周人滅商後，其勢力持續向東方擴展，由於周管轄的土地與人
口在短時間內急速增加，為了天下的長治久安，因此周朝的統治者，設計出一
套有效的政治制度管理各地。上述政治制度的內容，最可能是下列何者？',
  '[{"key": "A", "text": "在領土內設置郡、縣，官員由國君直接任免"}, {"key": "B", "text": "實施科舉制度，促進社會各階層人才的流動"}, {"key": "C", "text": "將百姓編入戶籍，並以法律規範人民的義務"}, {"key": "D", "text": "依據貴族的身分等級，授予土地與冊封爵位"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  33,
  '「某位君主為了統治上的考量，需要招募許多能夠書寫的人才。一開始在他的
國度中，竟然找不到太多有文化的人，這是因為西羅馬帝國滅亡後，城市生活
逐漸消失，文化知識也幾乎被遺忘殆盡。因此這位君主特地聘請知名學者，來
主持文化復興工作，諸如設立新學校、抄寫古羅馬的重要拉丁文著作，使拉丁
文成為各地共通的文字系統。」上述學者的身分，最可能是下列何者？',
  '[{"key": "A", "text": "西元前五世紀的希臘哲學家"}, {"key": "B", "text": "西元八世紀的基督教教士"}, {"key": "C", "text": "西元十七世紀的歐洲天文學者"}, {"key": "D", "text": "西元十八世紀的啟蒙運動思想家"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  34,
  '在探討一國國內不同地區醫療資源差異時，通常會先觀察醫師人數和病床
數，由相關數據與人口數的相對關係，可大致推論一個地區的醫療資源是否
不足。表(五)是某國2018年四個地區關於人口與醫療資源的資料：
表(五)
地 人口總數 老年人口 醫師人數 平均每位醫師 病床數 平均每張病床
區 (人) 比例(%) (人) 負擔人數(人) (張) 負擔人數(人)
甲 2,562,738 19.50 9,719 263.7 19,951 128.5
乙 2,272,459 13.26 3,824 594.3 11,988 189.6
丙 673,309 19.42 881 764.3 3,204 210.1
丁 322,836 17.95 820 393.7 4,073 79.3
根據表中資料判斷，關於甲、乙、丙、丁四個地區的醫療資源，下列何項推
論最適當？',
  '[{"key": "A", "text": "老年人口最多的地區醫療資源最為不足"}, {"key": "B", "text": "人口總數最少的地區醫療資源最為不足"}, {"key": "C", "text": "相對於其他地區，乙地區的醫療資源最為不足"}, {"key": "D", "text": "相對於其他地區，丙地區的醫療資源最為不足"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  35,
  '「飢餓行銷」是一種常見的行銷手法，指的是業者在短時間內利用各種管道
宣傳大批民眾排隊購買的熱潮，營造該項商品都會很快被搶購一空的情況，
透過媒體將商品炒作成為時下流行的話題，進而引起民眾的消費欲望。關於
上述行銷手法對於消費市場的影響，下列敘述何者最適當？',
  '[{"key": "A", "text": "廠商間的競爭使消費者的選擇增加"}, {"key": "B", "text": "業者的行銷手法將提高市場競爭程度"}, {"key": "C", "text": "消費者受價格誘因影響而增加消費欲望"}, {"key": "D", "text": "民眾的購物意願受非金錢誘因影響而提高"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  36,
  '若有人為了在選舉時讓支持的候選人當選，配合動員把戶籍遷移到非實際居
住的行政區，企圖影響選舉結果，此種行為可能觸犯《刑法》，檢察官將代
表國家主動起訴違法者。根據上述內容判斷，關於某位違法遷移戶籍者在接
受偵查、審判的過程中，下列何種情況最可能出現？',
  '[{"key": "A", "text": "遭到落選者提起民事訴訟要求損害賠償"}, {"key": "B", "text": "在遭檢察官偵查的過程中度過18歲生日"}, {"key": "C", "text": "被查出是在投票日的六個月前遷移戶籍"}, {"key": "D", "text": "因為觸犯告訴乃論之罪而受到刑事處罰"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  37,
  '臺灣少子女化危機惡化的速度超乎想像，面對人口負成長的人口懸崖，有學
者認為政府過往提出的相關政策已是緩不濟急，或許可以透過社會增加的方
向，思考提高國民人數的對策。根據上述內容判斷，下列何項對策與該學者
的意見最相符？',
  '[{"key": "A", "text": "提高外籍移工僱用人數"}, {"key": "B", "text": "鼓勵各國人才歸化入籍"}, {"key": "C", "text": "推動老人長期照護政策"}, {"key": "D", "text": "增加公立幼兒托育中心"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  38,
  '表(六)為某作家的三部長篇 表(六)
小說內容簡介，該作家藉此 著作 內 容 簡 介
構築十九至二十世紀臺灣歷 刻畫多位臺灣青年在南洋戰場上被戰爭折
甲
史的發展過程。根據表中內 磨至精神崩潰，甚至喪生的悲慘命運。
容判斷，這三部小說呈現的 敘述客家族群在臺灣中部山區生產樟腦，
乙
時代先後順序，最可能是下 為保衛家園參與武裝抗日的故事。
列何者？ 描繪臺灣人藉由參加文化協會、組織農民
丙',
  '[{"key": "A", "text": "乙→甲→丙 運動，抵抗殖民統治的事蹟。"}, {"key": "B", "text": "丙→乙→甲"}, {"key": "C", "text": "丙→甲→乙"}, {"key": "D", "text": "乙→丙→甲"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  39,
  '明 清時期，蠶絲業是中國 江南地區的重要產業。當時產出的生絲，主要供應國
內需求，部分對外出口。下列何者最可能反映1830年代生絲出口的情況？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  40,
  '表(七)是甲、乙兩國匯率變動的情形。根據表中
內容判斷，若其他條件不變，且所有成本完全
反應在商品售價上，相較於去年，在今年甲、
乙兩國的市場中，最可能出現下列何種情形？',
  '[{"key": "A", "text": "甲國商品在乙國的銷售量下滑"}, {"key": "B", "text": "乙國商品在甲國的銷售量下滑"}, {"key": "C", "text": "甲國進口的乙國商品數量下降"}, {"key": "D", "text": "乙國進口的甲國商品價格下降"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  41,
  '圖(十三)是一座歷史建築，根據圖中內
容判斷，該建築最可能興建於下列何時
何地？',
  '[{"key": "A", "text": "西元前六世紀的波斯地區"}, {"key": "B", "text": "西元六世紀的阿拉伯半島"}, {"key": "C", "text": "西元十六世紀的印度半島"}, {"key": "D", "text": "西元十九世紀的南美地區"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  42,
  '為維護消費者權益，政府制定法律對市場上供應不實有機農產品的業者處以
罰鍰，同時也能保障生產真正有機農產品農民的權益。上述主管機關對不實
業者的處罰，與下列何者受到的處罰類型相同？',
  '[{"key": "A", "text": "小華拒絕歸還向同事借的相機"}, {"key": "B", "text": "大明竊取隔壁鄰居家中的財物"}, {"key": "C", "text": "官員制定政策引發許多民眾不滿"}, {"key": "D", "text": "父母縱容少年抽菸而遭行政處分"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  43,
  '甲國女性的就業率，長期以來皆大幅低於全國平均值，因此該國政府調查女
性勞動人口中未就業者的原因，表(八)是調查結果中的部分統計資料。關於此
資料的解讀，下列何者最適當？
表(八) 單位：%
原因 需照顧未滿 需照顧 65 歲 負責打理 健康狀況
其他
年齡(歲) 12 歲子女 以上家屬 家務 不佳
30-34 65.37 0.89 11.43 2.98 19.33
35-39 55.35 2.60 21.39 4.26 16.40
40-44 35.36 5.16 39.70 7.15 12.63
45-49 7.05 8.10 58.04 5.50 21.31
50-54 0.53 7.58 56.69 4.69 30.51',
  '[{"key": "A", "text": "老年人口比例呈現上升趨勢"}, {"key": "B", "text": "家庭職能因社會變遷而弱化"}, {"key": "C", "text": "家庭平權的觀念仍有待加強"}, {"key": "D", "text": "勞雇間的權力與資源不對等"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  44,
  '上文中「唐手佐久川」與王國的使節團得以前往中國，最可能與當時中國何
項外交政策有關？',
  '[{"key": "A", "text": "聯合西域部族對抗外患"}, {"key": "B", "text": "簽訂條約，開放五口通商"}, {"key": "C", "text": "與受冊封國家建立朝貢關係"}, {"key": "D", "text": "訂定澶淵之盟，以兄弟相稱"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  45,
  '上文提及「政治局勢發生變化」，造成「唐手」向外傳播，此一變化最可能
是指下列何者？',
  '[{"key": "A", "text": "中國因甲午戰爭失敗割讓領土"}, {"key": "B", "text": "天皇積極效法唐朝推展新制度"}, {"key": "C", "text": "珍珠港事變導致美國對日宣戰"}, {"key": "D", "text": "日本藉由牡丹社事件擴張勢力"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  48,
  '根據表(九)中資訊，小婷與體力、經驗較為不足的民眾，選擇的路線分別為下
列何者？',
  '[{"key": "A", "text": "小婷選甲；體力、經驗較為不足的民眾選丁"}, {"key": "B", "text": "小婷選乙；體力、經驗較為不足的民眾選丙"}, {"key": "C", "text": "小婷選丙；體力、經驗較為不足的民眾選乙"}, {"key": "D", "text": "小婷選丁；體力、經驗較為不足的民眾選甲"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  49,
  '根據上文及圖(十五)的資訊判斷，上述都市的氣候特色應為下列何者？',
  '[{"key": "A", "text": "一月寒冷且年溫差大"}, {"key": "B", "text": "一月溫暖且雨量較少"}, {"key": "C", "text": "全年低溫且雨量稀少"}, {"key": "D", "text": "終年有雨且夏雨較多"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  50,
  '文中提及奴隸的輸出地最可能包含下列何者？',
  '[{"key": "A", "text": "南洋群島"}, {"key": "B", "text": "朝鮮半島"}, {"key": "C", "text": "伊比利半島"}, {"key": "D", "text": "夏威夷群島"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  51,
  '文中提到船隻改走新的通航路線，是因此航路具備下列哪一優勢？',
  '[{"key": "A", "text": "大幅縮短至印度洋周邊的航行路程"}, {"key": "B", "text": "可避免通過滿布浮冰的大西洋海域"}, {"key": "C", "text": "可藉由北大西洋暖流加快航行速度"}, {"key": "D", "text": "有助於疏解前往南美洲擁擠的航路"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  52,
  '關於文中活動理念對臺灣帶來影響的過程，最適合以下列何者說明？',
  '[{"key": "A", "text": "法律修改程序的變化"}, {"key": "B", "text": "科技發展帶來的衝擊"}, {"key": "C", "text": "風俗習慣的文化傳承"}, {"key": "D", "text": "全球化下的文化交流"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  53,
  '根據圖(十六)判斷，關於這則宣傳標語所呈現的意義，下列敘述何者最適當？',
  '[{"key": "A", "text": "主張對實施體罰者提起訴訟加以處罰"}, {"key": "B", "text": "藉由改變家長價值觀來帶動社會變遷"}, {"key": "C", "text": "上街請願要求國家立法保障兒童福利"}, {"key": "D", "text": "推廣法治教育教導兒童保護自身權益"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'social',
  54,
  '關於文末前、後所提及我國的二項法規，下列敘述何者最適當？',
  '[{"key": "A", "text": "以法律位階而言，前者具有最高性"}, {"key": "B", "text": "以法律位階而言，後者具有固定性"}, {"key": "C", "text": "以修法程序而言，皆須經總統公布後才生效"}, {"key": "D", "text": "以修法程序而言，皆可由行政機關自行修訂"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  1,
  '若將某區域的原始森林育林成種植單一物種的樹林時，則此區域最可能出現下
列何種變化？',
  '[{"key": "A", "text": "生產者的物種數增加"}, {"key": "B", "text": "消費者的物種數增加"}, {"key": "C", "text": "食物網變得比較複雜"}, {"key": "D", "text": "生態系變得比較不穩定"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  2,
  '在太魯閣地區常見到岩層或岩石受力而彎曲成美麗
圖案，如圖(一)所示。這種彎曲的現象稱為下列何者？',
  '[{"key": "A", "text": "斷層"}, {"key": "B", "text": "褶皺"}, {"key": "C", "text": "順向坡"}, {"key": "D", "text": "逆向坡"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  3,
  '圖(二)為自製運動飲料的成分說
明圖，圖中X所指應為下列何類
物質？',
  '[{"key": "A", "text": "醣類"}, {"key": "B", "text": "有機酸"}, {"key": "C", "text": "蛋白質"}, {"key": "D", "text": "電解質"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  4,
  '豆腐乳為一種傳統發酵食品，其一做法是將豆腐接種毛黴菌以進行發酵，當豆
腐被菌絲完全覆蓋後，再加入調味料而製成。下列有關毛黴菌構造的敘述，何
者最合理？',
  '[{"key": "A", "text": "不具孢子"}, {"key": "B", "text": "不具粒線體"}, {"key": "C", "text": "不具葉綠體"}, {"key": "D", "text": "不具細胞壁"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  5,
  '圖(三)為某港口8/11～8/14的潮汐變化
圖，根據圖中資訊判斷，8/11的潮差
與8/14的潮差約相差多少公尺？',
  '[{"key": "A", "text": "2"}, {"key": "B", "text": "4"}, {"key": "C", "text": "5"}, {"key": "D", "text": "8"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  6,
  '阿東進行「水溫與加熱時間的關係」實驗，其裝置
如圖(四)所示。老師看到實驗裝置後，建議他改善
測量水溫的方式，阿東進行下列哪一個改善方式最
合適？',
  '[{"key": "A", "text": "將溫度計懸吊在水中，不接觸杯底"}, {"key": "B", "text": "調整支架使酒精燈的火焰靠近溫度計"}, {"key": "C", "text": "拿溫度計攪拌杯中的水，使水溫均勻"}, {"key": "D", "text": "將酒精燈的酒精裝滿，使火焰大小固定"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  7,
  '氫氣因燃燒過程不會產生二氧化碳，是能源轉型的目標之一。依據製造方法的不
同，可將氫氣分成幾類，其中四類如表(一)所示。在減碳環保的要求下，期望產
生的氫氣要盡量是綠氫。
表(一)
依據表中資訊，下列說明何者最合理？',
  '[{"key": "A", "text": "褐氫和灰氫在製造過程會使用化石燃料，而藍氫和綠氫皆沒有"}, {"key": "B", "text": "將風力發電所產生的電能，用來電解水而產生的氫氣屬於綠氫"}, {"key": "C", "text": "褐氫和灰氫作為燃料，在燃燒過程需要氧氣，而藍氫和綠氫則不用"}, {"key": "D", "text": "氫氣被分成表中的四類顏色，主要是依據製造過程消耗掉的電能多寡來分類"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  8,
  '「若食物中所含的糖分容易被人體快速吸收，則會使血糖急遽上升，而引起
某激素分泌增加，進而造成血糖快速下降，甚至形成餐後血糖過低的現象。」
根據上述，有關此激素的敘述，下列何者正確？',
  '[{"key": "A", "text": "是由肝臟分泌的胰島素"}, {"key": "B", "text": "是由肝臟分泌的升糖素"}, {"key": "C", "text": "是由胰島分泌的胰島素"}, {"key": "D", "text": "是由胰島分泌的升糖素"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  9,
  '舞臺劇演出時，通常會讓周遭的環境昏暗，再用聚光燈來照射演員，讓觀眾能
看見演員的表演。有關觀眾能看見演員表演的敘述，下列何者最合理？',
  '[{"key": "A", "text": "聚光燈發出的光線照射在演員上，演員吸收這些光線，因此觀眾能看見演員"}, {"key": "B", "text": "聚光燈發出的光線照射在演員上，演員折射這些光線，因此觀眾能看見演員"}, {"key": "C", "text": "聚光燈發出的光線照射在演員上，演員反射這些光線，因此觀眾能看見演員"}, {"key": "D", "text": "觀眾眼睛發出的光線照射在演員上，演員折射這些光線，因此觀眾能看見演員"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  10,
  '圖(五)為網友分享的海蝕平臺與火成岩脈
照片，有研究指出此地的火成岩脈是
岩漿侵入原有的岩層而形成，由於火成
岩脈抵抗海水侵蝕的能力較原有的岩層
強，因此會像牆一樣，立於海蝕平臺
之上。根據上述說明，下列有關此地的
火成岩脈、平臺上原有的岩層以及海水
侵蝕作用的發生先後順序，何者最合
理？ 圖(五)',
  '[{"key": "A", "text": "火成岩脈最先形成，岩層再沉積，最後海水侵蝕"}, {"key": "B", "text": "岩層最先沉積，火成岩脈再形成，最後海水侵蝕"}, {"key": "C", "text": "海水最先侵蝕，岩層再沉積，最後火成岩脈形成"}, {"key": "D", "text": "火成岩脈最先形成，海水再侵蝕，最後岩層沉積"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  11,
  '圖(六)為小琪進行實驗的步驟示意圖：
+
+
圖(六)
關於此實驗，下列說明何者正確？',
  '[{"key": "A", "text": "步驟一蒸發皿中的物質均為反應物"}, {"key": "B", "text": "步驟二的目的可以避免反應速率過快"}, {"key": "C", "text": "步驟三所加入的水是催化劑"}, {"key": "D", "text": "步驟四的目的是為了分離不同的生成物"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  12,
  '道耳頓提出原子說後，越來越多的科學發現及證據顯示，原始的原子說需要修
正。下列哪一項最可能是因為電子的發現，原子說需要修正的內容？',
  '[{"key": "A", "text": "物質均由原子組成，原子不可再分割"}, {"key": "B", "text": "相同元素的原子，有相同的質量和性質"}, {"key": "C", "text": "不同元素的原子，有不同的質量和性質"}, {"key": "D", "text": "化學反應是原子的重新排列組合，形成新的物質"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  13,
  '「白噪音」為一種人類可聽見的聲波，此聲波在各頻率的響度大致相同。在自
然界中，類似的聲音包括雨聲、海浪聲等，而家中電風扇所製造出的聲音也與
白噪音相似。科學家研究發現，嬰兒處在有此種白噪音的環境下，會比較容易
入睡。根據上述，下列響度與頻率的關係圖，何者最適合用來表示此種幫助入
睡的白噪音？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  14,
  '已知DDT是一種作為殺蟲劑的化合物，難以被生物代謝。表(二)為某地區
食物鏈中甲、乙、丙、丁四種生物體內含有的DDT濃度。已知其中一種生物為
生產者，根據上述，下列推論何者正確？ 表(二)',
  '[{"key": "A", "text": "食性關係可能為丙→甲→乙→丁"}, {"key": "B", "text": "食性關係可能為丁→乙→甲→丙"}, {"key": "C", "text": "丙生物最可能為此食物鏈中的生產者"}, {"key": "D", "text": "甲生物最可能為此食物鏈中的三級消費者"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  15,
  '阿正閱讀一篇報導寫著：日本學者分析史前
人類遺骸後，認為當時住在沖繩的史前人類很
可能來自於臺灣，研究團隊為了驗證從臺灣航
海遷徙的可能性，於2019年進行實驗。如圖(七)
所示，阿正認為研究團隊會選在夏天進行實驗，
是因為這時的洋流與季風風向有助於從臺灣航海
向北至沖繩列島，進而到達日本列島。根據
阿正的判斷，研究團隊進行實驗時的季風風向
圖(七)
與洋流應為下列何者？',
  '[{"key": "A", "text": "東北季風與黑潮"}, {"key": "B", "text": "西南季風與黑潮"}, {"key": "C", "text": "東北季風與中國沿岸流"}, {"key": "D", "text": "西南季風與中國沿岸流"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  16,
  '已知維管束植物可進行某種代謝作用，其反應式為：「甲+二氧化碳→氧氣+乙+水」。
有關甲的名稱及其在植物體內主要運送的構造，下列何者最合理？',
  '[{"key": "A", "text": "水，由木質部運送"}, {"key": "B", "text": "水，由韌皮部運送"}, {"key": "C", "text": "葡萄糖，由木質部運送"}, {"key": "D", "text": "葡萄糖，由韌皮部運送"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  17,
  '表(三)為四位學生對於有機化合物、無
機化合物中組成元素的說明，哪一位
學生的說明最合理？',
  '[{"key": "A", "text": "小玉"}, {"key": "B", "text": "小如"}, {"key": "C", "text": "小方"}, {"key": "D", "text": "阿德"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  18,
  '400米賽跑的距離剛好是室外標準跑道最內圈一圈的長度，比賽中選手需跑在自
己的跑道上，因內、外圈跑道長度的差異，不同跑道的選手起跑位置需作對應
調整，如圖(八)所示。在這項比賽中最先跑完400米的選手，他在比賽過程哪一
項物理量的大小必高於其他所有選手？',
  '[{"key": "A", "text": "平均速率"}, {"key": "B", "text": "平均速度"}, {"key": "C", "text": "過程中速率的最大值 3"}, {"key": "D", "text": "過程中速度的最大值 6"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  19,
  '如圖(九)所示，一個半圓形軌道固定在水平桌面，
軌道兩端均距水平桌面高度0.5 m，將一顆小球在
距水平桌面高度1.0 m處，由靜止自由落下滑入
半圓形軌道，若不計任何摩擦力或阻力，且小球
滑過軌道最低點後，向上達到最高點時的動能為
0，則最高點距水平桌面高度為下列何者？',
  '[{"key": "A", "text": "0.25 m"}, {"key": "B", "text": "0.5 m"}, {"key": "C", "text": "1.0 m"}, {"key": "D", "text": "1.5 m"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  20,
  '表(四)為生物研究保育中心網頁中四種植物的部分資料，有關此四種植物在分類
階層上的敘述，下列何者無法確定？ 表(四)',
  '[{"key": "A", "text": "Lil-2和Lil-3為同科的植物"}, {"key": "B", "text": "Lil-2和Myr-6為同目的植物"}, {"key": "C", "text": "Lil-2和Lil-1為不同屬的植物"}, {"key": "D", "text": "Lil-2和Myr-6為不同屬的植物"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  22,
  '人體感染微生物到發病前所經過的時間稱為「潛伏期」。圖(十一)為小杉體溫
恆定範圍及近十天每天早上的體溫紀錄，已知此段時間小杉感染了微生物X，
其潛伏期為1～3天，發病時的症狀之一為體溫無法維持在恆定範圍內，則下列
哪一天最可能為小杉初次感染此微生物的時間？',
  '[{"key": "A", "text": "第1天"}, {"key": "B", "text": "第3天"}, {"key": "C", "text": "第6天"}, {"key": "D", "text": "第8天"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  23,
  '甲、乙兩個質量相同的物體，靜置於無摩擦力的水平桌面上，甲、乙分別受到
水平外力F 、F 後作直線運動，兩外力分別施力不同長短的時間後移除。已知
甲 乙
兩物體在時間t＝0～60 s期間的速度(v)與時間(t)關係圖，如圖(十二)所示，則有關
兩物體在此期間受力情形的敘述，下列何者正確？',
  '[{"key": "A", "text": "F 施力時間較長，且外力大小F ＞F"}, {"key": "B", "text": "F 施力時間較長，但外力大小F ＜F"}, {"key": "C", "text": "F 施力時間較長，但外力大小F ＞F"}, {"key": "D", "text": "F 施力時間較長，且外力大小F ＜F"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  25,
  '在超市買到的蘋果可能是幾個月前就已經採摘下來了。為了長時間保存，會在
蘋果表面塗上食用蠟，減少與氧氣接觸。蘋果熟化過程會將澱粉轉成糖，過程
中會需要氧氣並產生二氧化碳，所以可藉由調整蘋果存放環境的氣體比例，減
緩蘋果的熟化過程，延長保存期限。上述提及調整存放環境的氣體比例，其示
意圖最可能為下列何者？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  26,
  '砒霜是一種毒物，主成分為三氧化二砷(As O )。古代製作砒霜的技術較不成
2 3
熟，砒霜中會含有少量的不純物質――硫或硫化物，硫或硫化物接觸到銀，
會使銀氧化產生黑色的硫化銀(Ag S)，這就是古裝劇中常見的以銀針試毒，
2
銀針變黑即表示有毒。依據上述，下列推論何者最合理？',
  '[{"key": "A", "text": "硫化物發生還原反應而使銀針變黑"}, {"key": "B", "text": "銀針變黑，是因為三氧化二砷被還原的結果"}, {"key": "C", "text": "砒霜的純度越高，與銀針反應變黑的結果越明顯"}, {"key": "D", "text": "將銀針改成活性較小的金屬如黃金，也會反應產生硫化物"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  27,
  '取甲、乙兩種化合物，分別在足量的氧氣中燃燒，反應式分別為：
關於甲、乙兩種化合物的比較與說明，下列何者正確？',
  '[{"key": "A", "text": "甲的分子量大於乙，且甲可能為醇類"}, {"key": "B", "text": "甲的分子量大於乙，且甲可能為烴類"}, {"key": "C", "text": "乙的分子量大於甲，且乙可能為醇類"}, {"key": "D", "text": "乙的分子量大於甲，且乙可能為烴類"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  28,
  '圖(十四)為小佐某天前往圖中甲地旅遊前所查詢
的地面天氣簡圖，圖中黑色實線為等壓線，已知
圖中 H 和 L 的天氣系統未來會向圖中箭頭所指
的方向移動，因此他認為接下來甲地應為晴朗
的天氣。下列關於天氣系統H的敘述，何者最能
用來說明小佐的看法？',
  '[{"key": "A", "text": "中心近地面的氣流下沉，水氣不易凝結"}, {"key": "B", "text": "中心近地面的氣流上升，水氣不易凝結"}, {"key": "C", "text": "中心近地面氣壓比附近外圍低，水氣含量較少"}, {"key": "D", "text": "中心近地面氣壓比附近外圍高，水氣含量較高"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  29,
  '小泉暑假時到武嶺一日遊，他從臺中住家開車出發，途中經清境農場稍作休息
後，再開車上武嶺，之後再返回臺中住家，如圖(十五)所示。根據圖中資訊，當
天不同時間時，小泉所在環境的氣壓與氣溫關係圖，何者最合理？
(cid:5378)(cid:1875)
圖(十五)',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  30,
  '圖(十六)為阿榮在購物網站上搜尋黑麻油所獲得的部分結果，圖中的數值為黑麻
油的內容物含量及價格，他比較甲、乙兩種品牌的含量，覺得數值有不合理之
處。下列關於甲、乙兩牌標示的敘述，何者最合理？
1 c.c.＝1 cm 3
圖(十六)',
  '[{"key": "A", "text": "甲牌有誤：c.c.與g都是質量的單位，所以兩者前面的數值應相同"}, {"key": "B", "text": "甲牌有誤：c.c.與g都是體積的單位，所以兩者前面的數值應相同"}, {"key": "C", "text": "乙牌有誤：黑麻油會浮於水面，所以mL前面的數值應大於g前面的數值"}, {"key": "D", "text": "乙牌有誤：黑麻油會浮於水面，所以g前面的數值應大於mL前面的數值"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  31,
  '阿芳利用複式顯微鏡觀察小魚尾鰭內血液流動的
方向，所觀察到的視野影像如圖(十七)所示，圖中
的箭頭表示血液流動方向。若將培養皿往左緩慢地
移動，則在視野中依序消失的血管，應為下列何者？',
  '[{"key": "A", "text": "小動脈、微血管、小靜脈"}, {"key": "B", "text": "小動脈、小靜脈、微血管"}, {"key": "C", "text": "小靜脈、微血管、小動脈"}, {"key": "D", "text": "小靜脈、小動脈、微血管"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  32,
  '下列為某牌口香糖廣告的說明：
人體口腔中的環境接近中性，在用餐後一段時
間會變酸，而增加蛀牙機率。除了每日正確刷
牙外，在餐後嚼食無糖口香糖，可刺激唾液分
泌，有效「平衡」口中酸性。此廣告搭配了兩
張圖用以輔助說明，一張為圖(十八)，另一張
圖最可能為下列何者？
圖(十八)',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  33,
  '一木塊靜置於粗糙的水平面上，分別對此木塊施以不同大小的水平外力，
木塊與水平面間對應的摩擦力大小及運動狀態如表(五)所示。若木塊與水平
面間的最大靜摩擦力大小為f ，根據表中資訊，推論f 的大小關係，下列何
s s
者最合理？ 表(五)',
  '[{"key": "A", "text": "f ＜200 gw"}, {"key": "B", "text": "200 gw＜f ＜250 gw"}, {"key": "C", "text": "250 gw＜f ＜300 gw"}, {"key": "D", "text": "f ＞300 gw"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  35,
  '圖(二十)為草莓花朵構造及其發育的示意圖，已知草莓是由花托處膨大而來，若
圖(二十一)中的 構造是由草莓的子房發育而成，則此 構造應稱為下列何者？
圖(二十) 圖(二十一)',
  '[{"key": "A", "text": "胚珠"}, {"key": "B", "text": "種子"}, {"key": "C", "text": "果實"}, {"key": "D", "text": "花粉"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  36,
  '小逸每天中午都會記錄升旗臺上的竿影變
化，他經過多年的測量發現在不考慮天氣
因素的情況下，每年的1月底及11月底各有
1次中午無竿影的紀錄。已知升旗臺上
的旗竿鉛直立於水平地面上，根據上述
資訊，升旗臺的所在位置最可能位於
圖(二十二)
圖(二十二)中甲、乙、丙、丁的哪一點？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  37,
  '如圖(二十三)所示，有一電路裝置固定放置
在水平面上，甲、乙兩段南北向的導線分別
置於兩馬蹄型磁鐵所形成的磁場中，磁場恰
好與甲、乙兩段導線垂直。判斷甲、乙兩段
導線在磁場中所受磁力的方向，下列敘述何
者正確？',
  '[{"key": "A", "text": "甲、乙均向東"}, {"key": "B", "text": "甲、乙均向西"}, {"key": "C", "text": "甲向東，乙向西"}, {"key": "D", "text": "甲向西，乙向東"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  38,
  '軟骨發育不全症是體染色體中FGFR3基因發生突變所造成，患者具有身材矮小、
四肢短小變形等特徵，若親代只有其中一方為患者，子代就會有50%以上的
罹病率。已知阿佑因發生突變而患有軟骨發育不全症，但其父母皆未患病，
若以F代表突變的FGFR3遺傳因子，f代表正常的FGFR3遺傳因子，則關於阿佑
父母基因型的推論，下列何者最合理？',
  '[{"key": "A", "text": "父：Ff、母：Ff"}, {"key": "B", "text": "父：Ff、母：ff"}, {"key": "C", "text": "父：FF、母：FF"}, {"key": "D", "text": "父：ff、母：ff"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  39,
  '小櫻查詢了網路上的資料後，在月曆上
把2個有特殊天文現象的日子作記號，如
圖(二十四)所示。資料顯示在當月9日晚間
可見到月食，而23日早上則可見到日食。
根據此月曆，下列有關不同日期的月相何
者最合理？',
  '[{"key": "A", "text": "2日應為下弦月"}, {"key": "B", "text": "16日應為滿月"}, {"key": "C", "text": "23日應為下弦月"}, {"key": "D", "text": "30日應為上弦月"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  40,
  '下列為一則新聞報導：
一場泳池慶生派對中，工作人員在泳池中倒入大量的液態氮，以製造
煙霧效果並且炒熱氣氛，最後卻造成數人昏迷送醫。有人分析：「氮氣和
池水中的氯會反應產生有毒的三氯化氮，對皮膚和呼吸道相當刺激。」
小莫看完報導後，認為三氯化氮雖然有毒，但應該不是此次意外的原因，應是
其他因素所致，下列何者最可能是她認為不是三氯化氮的理由？',
  '[{"key": "A", "text": "空氣中有大量氮氣，池水也會接觸氮氣，但一般泳池並沒有類似的意外"}, {"key": "B", "text": "池水溫度會因液態氮汽化而下降，反而會加快產生三氯化氮的反應速率"}, {"key": "C", "text": "泳池會加入較高濃度的氯氣用以殺菌消毒，故泳池的氯含量比自來水高"}, {"key": "D", "text": "液態氮汽化後所產生的氣體會溶於池水中，與池水中的氯接觸機會增加"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  41,
  '有甲、乙、丙三種固體純物質，三者對水的溶解情形及沸點如表(六)所示。有一份
參雜甲、乙、丙的混合物，可經由兩步驟(加熱、加水過濾)而分離出甲、乙、丙，
如圖(二十五)所示。
表(六)
依據上述資訊，下列推論何者最合理？',
  '[{"key": "A", "text": "◆可能是甲，步驟一是加水過濾"}, {"key": "B", "text": "◆可能是丙，步驟一是加水過濾"}, {"key": "C", "text": "○可能是甲，步驟二需加熱至300℃，才可使乙、丙分離"}, {"key": "D", "text": "○可能是丙，步驟二需加熱至1500℃，才可使甲、乙分離"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  42,
  '圖(二十六)、圖(二十七)兩種連接方式皆為
甲、乙兩個燈泡並聯，小明與阿華皆認為
圖(二十七)的接法，燈泡甲較不會因為線
路故障而不亮，以下為兩人的解釋：
小明：若燈泡乙的燈絲燒斷，在圖(二十六)
中會使得燈泡甲不亮，而在圖(二十七)
圖(二十六) 圖(二十七)
中燈泡甲仍會發亮。
阿華：若導線丙、丁其中一條斷裂，在圖(二十六)中會使得燈泡甲不亮，而在
圖(二十七)中燈泡甲仍會發亮。
關於兩人的解釋是否合理？',
  '[{"key": "A", "text": "兩人皆合理"}, {"key": "B", "text": "兩人皆不合理"}, {"key": "C", "text": "只有小明合理"}, {"key": "D", "text": "只有阿華合理"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  43,
  '若壯壯跟安安兩人對於早餐飲品的需求為：
壯壯：我想要攝取較多的胺基酸。
安安：我要減少攝取糖。
則根據營養比較表，在攝取相同容量飲品的情況下，推論兩人的選擇，下列何
者最合理？',
  '[{"key": "A", "text": "兩人皆宜選擇牛奶"}, {"key": "B", "text": "兩人皆宜選擇燕麥奶"}, {"key": "C", "text": "壯壯選擇牛奶，安安選擇燕麥奶"}, {"key": "D", "text": "壯壯選擇燕麥奶，安安選擇牛奶"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  44,
  '根據本文，若只考量碳排放對於環境的影響，在相同的碳排放量下，推論下列
何種飲品生產的量最多？',
  '[{"key": "A", "text": "牛奶"}, {"key": "B", "text": "米漿"}, {"key": "C", "text": "燕麥奶"}, {"key": "D", "text": "杏仁奶"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  45,
  '根據本文第一段的資訊，下列有關C 的敘述，何者最合理？
p',
  '[{"key": "A", "text": "風力發電機葉片轉動的速率愈快，C 值會愈大"}, {"key": "B", "text": "風力發電機葉片轉動的速率愈快，C 值會愈小"}, {"key": "C", "text": "風力發電機葉片由風力獲得能量的比例愈高，C 值會愈大"}, {"key": "D", "text": "風力發電機葉片由風力獲得能量的比例愈高，C 值會愈小"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  46,
  '根據圖(三十)，假設原始的風速v 為10 m/s，通過發電機後，最後的風速v 為多
1 2
少時，會接近最大的C 值？
p',
  '[{"key": "A", "text": "0"}, {"key": "B", "text": "3.3 m/s"}, {"key": "C", "text": "5.9 m/s"}, {"key": "D", "text": "10 m/s"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  47,
  '阿洋提出以下觀點：
清水浸泡洗滌方法中，不用添加物比使用添加物的洗滌效果好
清水直接沖洗比各種浸泡洗滌方法的效果好
根據本文，關於阿洋的觀點，下列敘述何者合理？',
  '[{"key": "A", "text": "比較乙、丙的結果，可知觀點 不恰當"}, {"key": "B", "text": "比較乙、丁的結果，可知觀點 不恰當"}, {"key": "C", "text": "比較甲、戊的結果，可知觀點 不恰當"}, {"key": "D", "text": "比較乙、戊的結果，可知觀點 不恰當"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  48,
  '根據本文，「前處理」最可能為下列何者？',
  '[{"key": "A", "text": "所有小白菜皆不浸泡農藥"}, {"key": "B", "text": "所有小白菜浸泡相同濃度的同一種農藥"}, {"key": "C", "text": "小白菜分別浸泡相同濃度的不同種農藥"}, {"key": "D", "text": "小白菜分別浸泡不同濃度的同一種農藥"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  49,
  '根據本文，圖(三十一)中模擬地震參數所得到的結果，與下列何種資料所呈現的
特性最直接相關？',
  '[{"key": "A", "text": "地震強度"}, {"key": "B", "text": "地震規模"}, {"key": "C", "text": "地震的位置"}, {"key": "D", "text": "斷層的類型"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'science',
  50,
  '根據本文，當模擬的地震參數固定時，可利用圖(三十二)來說明下列何者？',
  '[{"key": "A", "text": "當岩層越厚時，可能會有較高的土壤液化潛勢"}, {"key": "B", "text": "當砂土層越厚時，可能會有較高的土壤液化潛勢"}, {"key": "C", "text": "當地下水位越高時，可能會有較高的土壤液化潛勢"}, {"key": "D", "text": "當地層組成以砂土為主時，可能會有較高的土壤液化潛勢"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  1,
  'Look at the picture. The man is holding a of grapes in his hands.',
  '[{"key": "A", "text": "bag"}, {"key": "B", "text": "basket"}, {"key": "C", "text": "bowl"}, {"key": "D", "text": "box"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  2,
  'Dennis enjoys in public. He is proud of his beautiful voice.',
  '[{"key": "A", "text": "dancing"}, {"key": "B", "text": "drawing"}, {"key": "C", "text": "shopping"}, {"key": "D", "text": "singing"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  3,
  'Mrs. Johnson can’t hear very well. If you need to talk to her, you must .',
  '[{"key": "A", "text": "explain"}, {"key": "B", "text": "hurry"}, {"key": "C", "text": "listen"}, {"key": "D", "text": "shout"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  4,
  'People got very excited when they watched Ms. Smith at the party.',
  '[{"key": "A", "text": "danced"}, {"key": "B", "text": "dancing"}, {"key": "C", "text": "has danced"}, {"key": "D", "text": "to dance"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  5,
  'I tried on these shoes in several different , and I thought the white pair looked best on me.',
  '[{"key": "A", "text": "colors"}, {"key": "B", "text": "prices"}, {"key": "C", "text": "shapes"}, {"key": "D", "text": "sizes"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  6,
  'Rex did not feel the earthquake this morning. He in the park at the time.',
  '[{"key": "A", "text": "jogged"}, {"key": "B", "text": "was jogging"}, {"key": "C", "text": "has jogged"}, {"key": "D", "text": "would jog"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  7,
  'Mr. Lee has worked in the same store for ten years; he’s never thought about his job.',
  '[{"key": "A", "text": "changing"}, {"key": "B", "text": "finding"}, {"key": "C", "text": "remembering"}, {"key": "D", "text": "starting"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  8,
  'I didn’t take the bus today because it was . All the seats were taken and a lot of
students were standing.',
  '[{"key": "A", "text": "dirty"}, {"key": "B", "text": "fast"}, {"key": "C", "text": "full"}, {"key": "D", "text": "wrong"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  9,
  'Don’t go away when you’re cooking, the food might burn.',
  '[{"key": "A", "text": "but"}, {"key": "B", "text": "if"}, {"key": "C", "text": "or"}, {"key": "D", "text": "so"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  10,
  'Jerry wanted to know he was kicked off the soccer team, but no one gave him a
good reason.',
  '[{"key": "A", "text": "where"}, {"key": "B", "text": "when"}, {"key": "C", "text": "whether"}, {"key": "D", "text": "why"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  11,
  'Jenny is already forty, doesn’t have a job and often makes trouble for her parents. To them,
she is really a(n) .',
  '[{"key": "A", "text": "daughter"}, {"key": "B", "text": "example"}, {"key": "C", "text": "gift"}, {"key": "D", "text": "headache"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  12,
  'Ed and Jill camping this weekend, so they have to finish their homework by Friday.',
  '[{"key": "A", "text": "went"}, {"key": "B", "text": "were going"}, {"key": "C", "text": "are going"}, {"key": "D", "text": "have gone"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  13,
  'Doraemon, a blue Japanese robot cat, has hated mice since his ears by a mouse.',
  '[{"key": "A", "text": "bit"}, {"key": "B", "text": "bite"}, {"key": "C", "text": "were bitten"}, {"key": "D", "text": "have bitten"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  14,
  'If we play some interesting games in class, there more fun in learning English.',
  '[{"key": "A", "text": "are"}, {"key": "B", "text": "has"}, {"key": "C", "text": "will be"}, {"key": "D", "text": "will have"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  15,
  'The of this shop was so bad; I never got any answer after I emailed them my questions.',
  '[{"key": "A", "text": "item"}, {"key": "B", "text": "business"}, {"key": "C", "text": "price"}, {"key": "D", "text": "service"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  16,
  'It’s not easy to see those islands clearly from here on sunny days, and it’s even less
to see them on cloudy days.',
  '[{"key": "A", "text": "difficult"}, {"key": "B", "text": "lucky"}, {"key": "C", "text": "possible"}, {"key": "D", "text": "special"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  17,
  'Do you remember the CD I was looking for for months? I found it in a small shop.
Look, here it is!',
  '[{"key": "A", "text": "almost"}, {"key": "B", "text": "even"}, {"key": "C", "text": "finally"}, {"key": "D", "text": "still"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  18,
  'Business at Jane’s shop has not been good these days. And the new supermarket across the
street only makes things .',
  '[{"key": "A", "text": "easier"}, {"key": "B", "text": "worse"}, {"key": "C", "text": "more boring"}, {"key": "D", "text": "more convenient"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  19,
  'Scott wasn’t sure if the young woman before him was pulled him out of a car on fire.',
  '[{"key": "A", "text": "who"}, {"key": "B", "text": "the one"}, {"key": "C", "text": "the one she"}, {"key": "D", "text": "the one who"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  20,
  'I swimming for several years before I went to this high school. I gave it up because of
heavy schoolwork.',
  '[{"key": "A", "text": "have practiced"}, {"key": "B", "text": "am practicing"}, {"key": "C", "text": "practiced"}, {"key": "D", "text": "would practice"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  21,
  'Frank Kane is so good in the movie that many people he will win the best actor prize.',
  '[{"key": "A", "text": "expect"}, {"key": "B", "text": "forget"}, {"key": "C", "text": "notice"}, {"key": "D", "text": "plan"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  22,
  'The new medicine that just came out on the market thousands of lives.',
  '[{"key": "A", "text": "and saved"}, {"key": "B", "text": "has saved"}, {"key": "C", "text": "saving"}, {"key": "D", "text": "to save"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  23,
  'Now I often think of those days with Pip, my pet dog. When I read in my room, he
quietly beside me.',
  '[{"key": "A", "text": "will come and sit"}, {"key": "B", "text": "comes and sits"}, {"key": "C", "text": "has come and sat"}, {"key": "D", "text": "used to come and sit"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  24,
  'Amy went to Four Seasons’ Kitchen with her mother after she collected 15 stars. They
ordered two Garden Sandwiches, an Autumn Wind, and a Winter Snow. After using the
stars, how much did they pay for their meals?',
  '[{"key": "A", "text": "$290."}, {"key": "B", "text": "$230."}, {"key": "C", "text": "$220."}, {"key": "D", "text": "$160."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  25,
  'Amy wants to bring her friends to Four Seasons’ Kitchen in August. She looks at her
calendar to pick a time to go there. Which are the time and date she
 calendar 月曆
can choose?',
  '[{"key": "A", "text": "8:30 pm, August 1."}, {"key": "B", "text": "5:00 pm, August 11."}, {"key": "C", "text": "3:00 pm, August 13."}, {"key": "D", "text": "2:00 pm, August 28."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  26,
  'According to the notes, which is the WRONG way to help a baby bird that is out of its nest?',
  '[{"key": "A", "text": "Feed it before you take it to a hospital."}, {"key": "B", "text": "Leave it alone if it is not hurt and has feathers."}, {"key": "C", "text": "Call the animal center if you can’t find its nest."}, {"key": "D", "text": "Put it back in its nest if it is not hurt and has few feathers."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  27,
  'According to the notes, what do birds do if their babies have the smell of people on them?',
  '[{"key": "A", "text": "They keep taking care of them."}, {"key": "B", "text": "They push them out of the nest."}, {"key": "C", "text": "They clean them until the smell goes away."}, {"key": "D", "text": "They leave them behind and move to a new nest."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  28,
  'According to the reading, which is one of the reasons for food waste?',
  '[{"key": "A", "text": "Stores do not know how to pack food well."}, {"key": "B", "text": "Farmers do not have enough machines to collect food."}, {"key": "C", "text": "There is no refrigerator on the truck to keep food fresh."}, {"key": "D", "text": "Factories do not have enough trucks to carry food to stores."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  29,
  'Which is true about food waste at each stage in the three parts of the world?',
  '[{"key": "A", "text": "For each area, the highest percentage of food waste happens at Stage 5."}, {"key": "B", "text": "Europe has a lower percentage of food waste at Stage 3 than the other two areas."}, {"key": "C", "text": "North America & Oceania has a higher percentage of food waste at Stage 1 than"}, {"key": "D", "text": "South & Southeast Asia has a higher percentage of food waste at Stage 4 than the"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  30,
  'What is the trick that the mosquito uses in rain?',
  '[{"key": "A", "text": "It shakes its body fast enough to get water off."}, {"key": "B", "text": "It drops with the raindrop and then rolls off it."}, {"key": "C", "text": "It flies behind the raindrop and pushes it away."}, {"key": "D", "text": "It rides on the raindrop and lands on the ground."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  31,
  'What keeps a mosquito safe in the rain?',
  '[{"key": "A", "text": "It is very light."}, {"key": "B", "text": "It has no body hairs."}, {"key": "C", "text": "It is as big as a raindrop."}, {"key": "D", "text": "It is strong enough to fight the force of a raindrop."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  32,
  'When would it be dangerous for a mosquito in the rain?',
  '[{"key": "A", "text": "When it flies too close to the ground."}, {"key": "B", "text": "When the rain falls too hard and too fast."}, {"key": "C", "text": "When it is hit by raindrops too many times."}, {"key": "D", "text": "When it drops for more than 6 cm in the rain."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  33,
  'What do the three stories in the reading all talk about?',
  '[{"key": "A", "text": "Who Beethoven’s true love was."}, {"key": "B", "text": "Who played “For Elise” the best."}, {"key": "C", "text": "How “For Elise” became popular."}, {"key": "D", "text": "Why Beethoven wrote “For Elise.”"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  34,
  'What do we know about “For Elise” from the reading?',
  '[{"key": "A", "text": "It first appeared in the opera Fidelio."}, {"key": "B", "text": "The true “Elise” was Elise Barensfeld."}, {"key": "C", "text": "The manuscript was found after Beethoven died."}, {"key": "D", "text": "The manuscript is now kept by the city of Vienna."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  35,
  'What can we learn about the three women from the stories?',
  '[{"key": "A", "text": "They were called “Elise” by their friends."}, {"key": "B", "text": "Elisabeth Röckel was a close friend of Beethoven’s."}, {"key": "C", "text": "Therese Malfatti changed “For Elise” to “For Therese.”"}, {"key": "D", "text": "Elise Barensfeld was Beethoven’s student."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  36,
  'What idea does Jesse Cohen talk about in the reading?',
  '[{"key": "A", "text": "Not all kinds of toys are helpful for children’s learning."}, {"key": "B", "text": "Parents should give their children the right toys for their age."}, {"key": "C", "text": "Children should learn about their gender from playing with toys."}, {"key": "D", "text": "We should not let gender decide which toys children can play with."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  37,
  'In the third paragraph, why does Jesse Cohen think “this rule can be bad for children”?',
  '[{"key": "A", "text": "Children may not want to share their toys with others."}, {"key": "B", "text": "Children may have the wrong idea about following rules."}, {"key": "C", "text": "Children may not be able to learn from playing with toys."}, {"key": "D", "text": "Children may miss the chance to find out what they really like."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  38,
  'In the reading, after Jesse Cohen talks about an idea, he often gives an example to make it clear.
Below are four of the sentences in the third paragraph. Which is used as an example?',
  '[{"key": "A", "text": "“However, this rule can be bad for children.”"}, {"key": "B", "text": "“Dolls help with their early language use, and building toys are good for learning math and"}, {"key": "C", "text": "“Some doctors worry that children may use the same kind of thinking when they look for"}, {"key": "D", "text": "“If they do, they may miss something more important than just getting a chance to play"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  39,
  'What is the reading mostly about?',
  '[{"key": "A", "text": "Marie Colvin’s war reports."}, {"key": "B", "text": "Marie Colvin’s working life."}, {"key": "C", "text": "Marie Colvin’s schooldays at Yale."}, {"key": "D", "text": "Marie Colvin’s experiences in Homs."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  40,
  'What does it mean when someone has empathy?',
  '[{"key": "A", "text": "They are good at taking war photos."}, {"key": "B", "text": "They like to read other people’s life stories."}, {"key": "C", "text": "They are able to understand how other people feel."}, {"key": "D", "text": "They are good at helping people change their own lives."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  41,
  'Which is true about Marie Colvin?',
  '[{"key": "A", "text": "The chance to study at Yale made her leave her job in the Middle East."}, {"key": "B", "text": "The experience in Sri Lanka did not change her way of reporting news."}, {"key": "C", "text": "She was killed in Homs when she was interviewing soldiers there for her report."}, {"key": "D", "text": "She was not sure what to do in the future until she worked for the Sunday Times."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  42,
  '(A) what things are called
(B) how sports are played
(C) why different languages are spoken
(D) what words are often spelled differently',
  '[{"key": "A", "text": "what things are called"}, {"key": "B", "text": "how sports are played"}, {"key": "C", "text": "why different languages are spoken"}, {"key": "D", "text": "what words are often spelled differently"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '112年國中教育會考',
  'english_reading',
  43,
  '(A) how old they are
(B) who they speak to
(C) where they grew up
(D) whether they are men or women
12 試題結束',
  '[{"key": "A", "text": "how old they are"}, {"key": "B", "text": "who they speak to"}, {"key": "C", "text": "where they grew up"}, {"key": "D", "text": "whether they are men or women"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  1,
  '這則粉絲專頁貼文的用意，最可能是下列何者？',
  '[{"key": "A", "text": "徵求粉絲專頁新小編"}, {"key": "B", "text": "預告直播促銷的期程"}, {"key": "C", "text": "暗示秋刀魚產季將近"}, {"key": "D", "text": "宣布調漲秋刀魚價格"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  2,
  '下列文句，何者用字完全正確？',
  '[{"key": "A", "text": "那張字畫的真跡被竊後，至今不知所衷"}, {"key": "B", "text": "他只知言襲前人作法，完全不懂得變通"}, {"key": "C", "text": "你去失誤招領處詢問，也許能找回錢包"}, {"key": "D", "text": "樹欲靜而風不止，為人子女盡孝要及時"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  3,
  '下列文句中的謙詞，何者使用最恰當？',
  '[{"key": "A", "text": "足球賽後，亞軍隊伍向冠軍隊伍道賀：「承讓了，恭喜！」"}, {"key": "B", "text": "同樂會時，班長自告奮勇：「如果大家不嫌棄，我就獻醜了。」"}, {"key": "C", "text": "主席在會議的結語：「感謝各位提供的淺見，我們會審慎評估。」"}, {"key": "D", "text": "對宴會的主人說：「謝謝你準備的薄酌，讓大家吃得非常滿足。」"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  4,
  '某些問卷使用了否定詞，受訪者有時不易理解內容，感到混淆。根據下列問卷
題目，阿寶的立場與其選擇相符的是哪一個？
問卷題目 阿寶的立場 阿寶的選擇',
  '[{"key": "A", "text": "您是否同意廢除最低工資的設立？ 最低工資要受到保障 同意"}, {"key": "B", "text": "您是否同意禁止種植基因改造植物？ 反對基因改造 同意"}, {"key": "C", "text": "不同意"}, {"key": "D", "text": "不想多繳稅 不同意"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  5,
  '右側是某書店開幕的廣告文
案。根據內容，下列敘述何
者錯誤？',
  '[{"key": "A", "text": "融合節慶的元素"}, {"key": "B", "text": "邀請民眾蒞店同樂"}, {"key": "C", "text": "說明終身學習的重要"}, {"key": "D", "text": "點出書店開幕日晚上營業"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  6,
  '下列詞語中的「落」字，何者與「月落星沉」的「落」字意義相同？',
  '[{"key": "A", "text": "下「落」不明"}, {"key": "B", "text": "草木疏「落」"}, {"key": "C", "text": "丟三「落」四"}, {"key": "D", "text": "水「落」石出"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  7,
  '「人生，其實像一條從寬闊的平原走進森林的路。在平原上同伴可以結夥而行，
歡樂地前推後擠、相濡以沫。一旦進入森林，草叢和荊棘擋路，情形就變了，
各人專心走各人的路，尋找各人的方向。」這段文字的觀點與下列何者相去最遠？',
  '[{"key": "A", "text": "人生總有坎坷，不會永遠是平順坦途"}, {"key": "B", "text": "不論結伴或是獨行，皆應樂觀面對人生"}, {"key": "C", "text": "天下無不散的筵席，朋友總有分離的時候"}, {"key": "D", "text": "人的選擇不同，每個人都得自己去創造未來"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  8,
  '下列文句「」中的字，何者讀音正確？',
  '[{"key": "A", "text": "在賣場集滿點數就可「兌」換商品：ㄩㄝˋ"}, {"key": "B", "text": "一望無「垠」的海面上漂流著幾艘小船：ㄍㄣ"}, {"key": "C", "text": "這場音樂會的門票開賣不久就售「罄」：ㄑㄧㄥˋ"}, {"key": "D", "text": "櫃檯上的花瓶插了一束紫色的「桔」梗花：ㄓㄜˊ"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  9,
  '「由國家出資的遠征計畫，經費較高，卻少有重大發現。官方的主事者常
攜帶大批補給裝備，而非輕裝簡從。且受制於政治考量，無法自行選拔合適
的成員。反觀私人支持的遠征隊較能達成目標，主事者專心致志，可主導成
員的挑選，每個人都有擅長的領域。」根據本文，私人支持的遠征隊較能達
成目標的原因不包含下列何者？',
  '[{"key": "A", "text": "政治考量較少"}, {"key": "B", "text": "補給裝備較多"}, {"key": "C", "text": "主事者權限較大"}, {"key": "D", "text": "計畫成員較專業"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  11,
  '下列各項比賽優勝的獎牌題辭，何者搭配最恰當？
比賽項目 題辭',
  '[{"key": "A", "text": "演說 妙筆生花"}, {"key": "B", "text": "作文 新鶯出谷"}, {"key": "C", "text": "書法 鐵畫銀鉤"}, {"key": "D", "text": "歌唱 口若懸河"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  12,
  '「老農家貧在山住，耕種山田三四畝。苗疏稅多不得食，輸入官倉化為土。歲暮
鋤犁傍空室，呼兒登山收橡實。西江賈客珠百斛，船中養犬長食肉。」關於這首
詩的說明，下列敘述何者最恰當？',
  '[{"key": "A", "text": "就形式而言，是一首七言律詩"}, {"key": "B", "text": "就類別而言，是一首山居躬耕的閒適詩"}, {"key": "C", "text": "就內涵而言，描繪農民於繁重稅賦下艱困的生活"}, {"key": "D", "text": "就技巧而言，以農家與商賈對比，凸顯人情的可貴"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  13,
  '「遺忘就像舞臺打燈後的暗處，漆黑越大片，就越能凸顯光照的明亮。遺忘幫我
們揀選人生最值得珍惜的過往片段。因此，遺忘是無須哀悼的，忘的越多，就
越應該把眼光投向光照的所在，那才是值得留戀的人事代謝。」下列何者最接近
本文作者的觀點？',
  '[{"key": "A", "text": "生命中的人事代謝無須遺忘"}, {"key": "B", "text": "遺忘如同舞臺上光照的所在"}, {"key": "C", "text": "不被遺忘的事物才最值得珍惜"}, {"key": "D", "text": "遺忘越多越能看見人生光明面"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  14,
  '「玉慘花愁出鳳城，蓮花樓下柳青青。尊前一唱〈陽關曲〉，別個人人第五
程？ 尋好夢，夢難成。有誰知我此時情？枕前淚共階前雨，隔個窗兒滴到
明。」關於這闋詞的分析，下列敘述何者錯誤？',
  '[{"key": "A", "text": "首句情景交融，「慘」、「愁」二字點出別情"}, {"key": "B", "text": "下闋首句點出「我」為了追尋理想而遠離佳人"}, {"key": "C", "text": "末尾二句暗示「我」滿懷離情別緒，一夜未眠"}, {"key": "D", "text": "上闋描寫分別時的情景，下闋描寫別後的思情"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  15,
  '「溝通包含了三要素：內容、語調、非語言行為。若某人說話時的語調、手勢、
表情，和他所說的內容不一致或情境模糊時，人們比較容易受到語調和非語言
行為的影響。」下列情境，何者最符合這段文字的內容？',
  '[{"key": "A", "text": "說話用字過度簡潔，會讓人覺得沒有禮貌"}, {"key": "B", "text": "同樣的內容，由嚴肅的老師說出來比較具有說服力"}, {"key": "C", "text": "朋友收到禮物時臭著臉說「謝謝」，會覺得他其實並不開心"}, {"key": "D", "text": "聽廣播時，因看不到主持人的表情、手勢，無法判斷內容的真實性"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  16,
  '下列文句中的詞語，何者使用最恰當？',
  '[{"key": "A", "text": "飲食應注重營養均衡，五穀不分才健康"}, {"key": "B", "text": "這房子經歷風災依然堅固，真是不愧屋漏"}, {"key": "C", "text": "使用儀器以蠡測海後，他終於得到準確數據"}, {"key": "D", "text": "對於行將就木之人，世間的一切已無須牽掛"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  17,
  '下列選項中的文字，旨在強調求學必須先立定志向。依據文意判斷，何者斷句
最恰當？',
  '[{"key": "A", "text": "夫學者之欲至於聖賢猶射者，之求中夫正鵠也。不以聖賢為準的而學者是，"}, {"key": "B", "text": "夫學者之欲至於聖賢，猶射者之求中夫正鵠也。不以聖賢為準的而學者，"}, {"key": "C", "text": "夫學者之欲，至於聖賢猶射者之求中。夫正鵠也，不以聖賢為準的，而學者"}, {"key": "D", "text": "夫學者之欲至，於聖賢猶射者之求。中夫正鵠也不以聖賢為準，的而學者是"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  18,
  '漢靈帝時，陳留 蔡邕，以數上書陳奏，忤上旨意，又內寵惡之，慮不
免，乃亡命江海，遠跡吳郡。吳有燒桐以爨 者，邕聞火烈聲，曰：「此良材
1
也。」因請之，削之以琴，果有美音。而其尾焦，因名「焦尾琴」。
根據這則故事，下列敘述何者最恰當？
',
  '[{"key": "A", "text": "焦尾琴因蔡邕識材而製成"}, {"key": "B", "text": "吳人向來以燒桐製琴聞名"}, {"key": "C", "text": "焦尾琴製成後經火烤而音色優美"}, {"key": "D", "text": "蔡邕因忤逆上意而遭流放至吳郡"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  19,
  '「蝸以涎見覓，蟬以聲見黏，螢以光見獲。故愛身者，不貴赫赫之名。」這句話
的涵義與下列何者最接近？',
  '[{"key": "A", "text": "人過留名，雁過留聲"}, {"key": "B", "text": "所榮者善行，所恥者惡名"}, {"key": "C", "text": "名不可簡而成，譽不可巧而立"}, {"key": "D", "text": "樹大招風風損樹，人為名高傷喪身"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  21,
  '鞠武〈報燕太子丹書〉曰：「臣聞快於意者虧於行，甘於心者傷於性。今太子欲
滅悁悁 之恥，除久久之恨，此實臣所當糜軀碎首而不避也。私以為智者不冀僥
1
倖以要功，明者不苟從志以順心。事必成，然後舉；身必安，而後行。故發無
失舉之尤，動無蹉跌 之愧也。太子貴匹夫之勇，信一劍之任，而欲望功，臣以
2
為疏。」關於這段文字的寫作分析，下列敘述何者最恰當？',
  '[{"key": "A", "text": "分析個中利害關係，鼓勵太子須建功立業"}, {"key": "B", "text": "採取先抑後揚筆法，肯定太子能獨當一面"}, {"key": "C", "text": "以工整句式加強文氣，勸諫太子應謀定而後動"}, {"key": "D", "text": "列舉前人失敗的事例，提醒太子不宜心存僥倖"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  22,
  '賈人某，至直隸界，忽大雨雹，伏禾中。聞空中云：「此張不量田，勿傷
其稼。」天霽，他田偃壞，張田獨無恙。蓋張氏積粟甚富，每春間貧民皆就貸
焉。償時多寡不較，悉納之，未嘗執概取盈，故鄉人名之「不量」。
根據本文，「張田獨無恙」的原因最可能是下列何者？',
  '[{"key": "A", "text": "張氏行善積德，得到護佑"}, {"key": "B", "text": "貧民虔誠祈願，感動上天"}, {"key": "C", "text": "張氏田產甚多無法丈量，看不出損失"}, {"key": "D", "text": "賈人福澤深厚，連帶使張田倖免於難"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  23,
  '目前因鰲鼓溼地水位升高，使黑面琵鷺棲息處距離賞鳥亭長達300多公
尺。往年低水位時，會浮出大片沙洲，黑面琵鷺棲息在賞鳥亭前約50公尺處。
今年若要觀賞牠們，務必攜帶高倍望遠鏡。
賞鳥期從11月1日到明年2月18日，期間逢假日8時至16時將實施管制，
進入溼地的車輛從原本可自由進出南、北閘門，改為北閘門進，南閘門出。
根據本文，下列關於鰲鼓溼地賞鳥的敘述，何者最恰當？',
  '[{"key": "A", "text": "水位越低時，越需要使用高倍望遠鏡觀察"}, {"key": "B", "text": "黑面琵鷺的棲地會隨著賞鳥亭的位置改變"}, {"key": "C", "text": "賞鳥期間進入溼地的車輛全天候均須管制"}, {"key": "D", "text": "非假日到溼地賞鳥，車輛可從南閘門進入"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  24,
  '「夫繭，捨而不治，則腐蠹而棄。使女工繅 之，以為美錦，國君服而朝之。
1
身者，繭也，捨而不治，則智行腐蠹。使賢者教之，以為世士，則天下諸侯莫
敢不敬。」關於本文的分析，下列敘述何者最恰當？',
  '[{"key": "A", "text": "以繭為喻，說明教化對修身的重要"}, {"key": "B", "text": "以身著美錦，暗指上位者奢靡誤國"}, {"key": "C", "text": "以女工與賢者對照，強調環境的影響"}, {"key": "D", "text": "以腐蠹的蠶繭，嘲諷國政的敗壞衰頹"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  25,
  '關於文中的「我」，下列敘述何者最恰當？',
  '[{"key": "A", "text": "在愛丁堡的期間是帶有目的性的停留"}, {"key": "B", "text": "認為去大象咖啡館是一種偏頗的決定"}, {"key": "C", "text": "因沉浸在老圖書館的氛圍裡而忘卻時間"}, {"key": "D", "text": "討厭愛丁堡的寒冷而不願回想留學時光"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  26,
  '文末「那個尖銳的姿態，同時也是狹窄的。」這句話的意思，最可能是下列何者？',
  '[{"key": "A", "text": "粗心大意，挂一漏萬的情況一再出現"}, {"key": "B", "text": "年少時個性尖銳，只想處處與人爭鋒"}, {"key": "C", "text": "器量狹小，容不下別人一丁點的錯誤"}, {"key": "D", "text": "眼前只有單一的目標，視野不夠開闊"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  27,
  '根據本文，出版社把原書絲線的顏色改掉，造成的影響最可能是下列何者？',
  '[{"key": "A", "text": "失去原本的隱喻，使讀者無法感受作者諷刺的用意"}, {"key": "B", "text": "混淆勳章的配色，使讀者誤解不同貴族的代表顏色"}, {"key": "C", "text": "過度渲染舞蹈的功能，以為是貴族階層流行的風尚"}, {"key": "D", "text": "刻意淡化階級的對立，營造出社會繁榮和諧的假象"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  28,
  '根據本文，關於綏夫特《格理弗遊記》的敘述，下列何者最恰當？',
  '[{"key": "A", "text": "作者致力於創作兒童奇幻文學作品"}, {"key": "B", "text": "作者以虛構的情節反映現實的醜惡"}, {"key": "C", "text": "早期中文譯者將原書的四冊內容濃縮為兩冊"}, {"key": "D", "text": "早期譯者用「格物學」一詞是為免得罪當道"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  29,
  '根據本文，關於人類對地球資源的消耗，下列敘述何者最恰當？',
  '[{"key": "A", "text": "1990年之前，人類並未透支地球資源"}, {"key": "B", "text": "2022年人類耗用的地球資源是前一年的1.75倍"}, {"key": "C", "text": "每年的地球超載日之後，全球資源就會消耗殆盡"}, {"key": "D", "text": "美國人的生活方式比多數國家的人對地球造成更大的負擔"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  30,
  '根據本文，下列何者最可能使地球超載日延後？',
  '[{"key": "A", "text": "提升畜牧業整體產量"}, {"key": "B", "text": "加強野生動物保育工作"}, {"key": "C", "text": "增加飲食中蔬食的比例"}, {"key": "D", "text": "嚴防Covid-19疫情再爆發"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  31,
  '根據展覽概述，下列推論何者最恰當？',
  '[{"key": "A", "text": "北宋時期的畫作可繪於絲織品上"}, {"key": "B", "text": "范寬、郭熙、李唐三人係師出同門"}, {"key": "C", "text": "北宋山水畫的典範首重全然描繪實景"}, {"key": "D", "text": "三者中〈萬壑松風〉的成畫年代最早"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  32,
  '右圖是阿燦根據資料繪製的美術作
業，同學小群核對後發現有疏失處，
最可能是下列何者？',
  '[{"key": "A", "text": "展出的起迄日期有誤"}, {"key": "B", "text": "應該標明是首次合體展覽"}, {"key": "C", "text": "沒有按照畫家出生年分先後排序"}, {"key": "D", "text": "未得官方核定不宜以「國寶」稱之"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  34,
  '根據畫線處的文句，下列關係的說明，何者最接近文中「偽造影像的生成」與
「偽造影像的辨識」兩者之間的競爭？',
  '[{"key": "A", "text": "就像是光源和影子，透過光源的運用可使影子出現各種變化"}, {"key": "B", "text": "就像是投影機和螢幕，投影機投射的影像須藉螢幕顯示出來"}, {"key": "C", "text": "就像是自來水和水龍頭，當水龍頭開得越大，自來水的出水量就越大"}, {"key": "D", "text": "就像是駭客與防毒軟體，當駭客發展出新病毒，防毒軟體就會再更新"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  35,
  '根據本文，下列關於深偽技術或深偽影片的敘述，何者最恰當？',
  '[{"key": "A", "text": "美國媒體藉由皮爾模仿的深偽影片操縱民主"}, {"key": "B", "text": "演員可以透過深偽技術增進自己的表演技巧"}, {"key": "C", "text": "氾濫的深偽影片將導致民眾對社會的信任度下降"}, {"key": "D", "text": "深偽技術的爭議在人類的創意會被人工智慧取代"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  36,
  '根據本文，古阿明想透過畫作表達的意義，最可能是下列何者？',
  '[{"key": "A", "text": "以茶蟲代表大自然對人類開發的反撲"}, {"key": "B", "text": "以茶蟲象徵政府官員對老百姓的監控"}, {"key": "C", "text": "茶蟲不僅啃食茶葉，也啃食了古阿明一家日常生活所需"}, {"key": "D", "text": "茶蟲為了生存無所不吃，就像古阿明為了學畫多方嘗試"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  37,
  '根據本文，郭雲天對古阿明的畫作意見不多，原因最可能是下列何者？',
  '[{"key": "A", "text": "希望古阿明能自己發現缺失"}, {"key": "B", "text": "想要保留古阿明特有的創意"}, {"key": "C", "text": "古阿明作畫時太專注，給意見也聽不進去"}, {"key": "D", "text": "古阿明的畫作太完美，無法再提更多建議"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  38,
  '下列關於甲、乙二文文句的說明，何者最恰當？',
  '[{"key": "A", "text": "「一旦遇事，便與里巷人無異」是因書讀得不夠多"}, {"key": "B", "text": "「見一事則止知一事」意謂對事情的理解不夠全面"}, {"key": "C", "text": "「如何氣象」其意是思索今人當前所處的環境氛圍"}, {"key": "D", "text": "「我自己任性為之」意謂今人比古人更加不受拘束"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  39,
  '關於甲、乙二文的說明與比較，下列何者最恰當？',
  '[{"key": "A", "text": "甲文認為耳熟能詳的淺近道理，更勝於聖賢之言"}, {"key": "B", "text": "乙文以古人處事的標準，評斷自身舉措是否合宜"}, {"key": "C", "text": "二者都認為讀書應活用，不應拘泥於古人的看法"}, {"key": "D", "text": "二者都覺得古人讀書講究方法，比今人更有效率"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  40,
  '根據本文，下列文句「」中的字義，何者說明最恰當？',
  '[{"key": "A", "text": "妾夜「亡」布八匹：損壞"}, {"key": "B", "text": "令尹「信」盜之：隨意"}, {"key": "C", "text": "妾子「坐」而黜：受罰"}, {"key": "D", "text": "王「其」察之：難道"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  41,
  '根據本文，下列關於令尹與楚王的敘述何者最恰當？',
  '[{"key": "A", "text": "令尹打算偷盜布匹再將罪責嫁禍給他人"}, {"key": "B", "text": "令尹主張楚國盜賊橫行是須正視的問題"}, {"key": "C", "text": "楚王覺得宮中之物被盜應是令尹的責任"}, {"key": "D", "text": "楚王認為不論身分地位都應該遵守法律"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'chinese',
  42,
  '根據本文，江母見楚王的目的最可能是下列何者？',
  '[{"key": "A", "text": "想要替兒子江乙頂罪"}, {"key": "B", "text": "表達江乙被懲處的不公"}, {"key": "C", "text": "向楚王告發郢大夫的罪行"}, {"key": "D", "text": "建議楚王再用孫叔敖為令尹"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  1,
  '算式 − (− ) 之值為何？
7 4
19',
  '[{"key": "A", "text": "28"}, {"key": "B", "text": "28"}, {"key": "C", "text": "11"}, {"key": "D", "text": "3"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  3,
  '若二元一次聯立方程式 的解為 ，則 a + b 之值為何？
y = −3x y = b',
  '[{"key": "A", "text": "−28"}, {"key": "B", "text": "−14"}, {"key": "C", "text": "−4"}, {"key": "D", "text": "14"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  4,
  '若想在圖(二)的方格紙上沿著格線畫出坐標平面的 x 軸、
y 軸並標記原點，且以小方格邊長作為單位長，則下列
哪一種畫法可在方格紙的範圍內標出 (5,3)、 (−4,−4)、
(−3,4)、(3,−5) 四點？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": "y"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  5,
  '阿賢利用便利貼拼成一個聖誕樹圖案，
聖誕樹圖案共有 10 層，每一層由三列
的便利貼拼成，前 3 層如圖 ( 三 ) 所
示。若同一層中每一列皆比前一列多
2 張，且每一層第一列皆比前一層第一列
多 2 張，則此聖誕樹圖案由多少張便利貼
拼成？',
  '[{"key": "A", "text": "354"}, {"key": "B", "text": "360"}, {"key": "C", "text": "384"}, {"key": "D", "text": "390"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  6,
  '箱內有 50 顆白球和 10 顆紅球，小慧打算從箱內抽球 31 次，每次從箱內
抽出一球，如果抽出白球則將白球放回箱內，如果抽出紅球則不將紅球放回
箱內。已知小慧在前 30 次抽球中共抽出紅球 4 次，若她第 31 次抽球時箱內
的每顆球被抽出的機會相等，則這次她抽出紅球的機率為何？
1',
  '[{"key": "A", "text": "5"}, {"key": "B", "text": "6"}, {"key": "C", "text": "12"}, {"key": "D", "text": "28"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  7,
  '圖(四) 圖(五) 圖(六)
圖 ( 四 ) 有 A、 B 兩種圖案，其中 A 經過上下翻轉後與 B 相同，且圖案的
外圍是正方形，圖(五)是將四個 A 圖以緊密且不重疊的方式排列成大正方形，
圖 ( 六 ) 是將兩個 A 圖與兩個 B 圖以緊密且不重疊的方式排列成大正方形。
判斷圖(五)、 圖(六)是否為線對稱圖形？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  8,
  '若 a = 3.2 × 10−5， b = 7.5 × 10−5， c = 6.3 × 10−6，則 a、 b、c 三數的大小關係
為何？',
  '[{"key": "A", "text": "a < b < c"}, {"key": "B", "text": "a < c < b"}, {"key": "C", "text": "c < a < b"}, {"key": "D", "text": "c < b < a"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  9,
  '癌症分期是為了區別惡性腫瘤影響人體健康的程度，某國統計 2011 年確診
四種癌症一到四期的患者在 3 年後存活的比率 ( 3 年存活率 )，並依據癌症
類別與不同分期將資料整理成圖 ( 七 )。
圖(七)
甲、乙兩人對該國 2011 年確診上述四種癌症的患者提出看法如下：
( 甲 ) 一到四期的乳癌患者的 3 年存活率皆高於 50%
( 乙 ) 在這四種癌症中，三期與四期的 3 年存活率相差最多的是胃癌
對於甲、乙兩人的看法，下列判斷何者正確？',
  '[{"key": "A", "text": "甲、乙皆正確"}, {"key": "B", "text": "甲、乙皆錯誤"}, {"key": "C", "text": "甲正確，乙錯誤"}, {"key": "D", "text": "甲錯誤，乙正確"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  11,
  '將 化簡為 a + b 7，其中 a、b 為整數，求 a + b 之值為何？
4 − 7',
  '[{"key": "A", "text": "5"}, {"key": "B", "text": "3"}, {"key": "C", "text": "−9"}, {"key": "D", "text": "−15"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  12,
  '甲、乙兩個二次函數分別為 y = ( x + 20 )2 + 60、y = − ( x − 30 )2 + 60，判斷
下列敘述何者正確？',
  '[{"key": "A", "text": "甲有最大值，且其值為 x = 20 時的 y 值"}, {"key": "B", "text": "甲有最小值，且其值為 x = 20 時的 y 值"}, {"key": "C", "text": "乙有最大值，且其值為 x = 30 時的 y 值"}, {"key": "D", "text": "乙有最小值，且其值為 x = 30 時的 y 值"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  14,
  '小玲搭飛機出國旅遊，已知她搭飛機產生的
(cid:1538)(cid:915)(cid:1644)(cid:1172)(cid:1242)(cid:4479)(cid:1196)(cid:3311)(cid:960)(cid:1664)
碳排放量為 800 公斤，為了彌補這些碳排放量， (cid:1538)(cid:3197)(cid:2895)1(cid:998)(cid:1626)(cid:3170)(cid:1171)(cid:1937)(cid:4473)(cid:3048)(cid:1835)(cid:3782)
她決定上下班時從駕駛汽車改成搭公車。依據
(cid:581)(cid:33)
(cid:1342)(cid:1353)(cid:1611)(cid:506)0(cid:998)(cid:1040)
圖(九)的資訊，假設小玲每日上下班駕駛汽車
(cid:581)(cid:33)
(cid:998)(cid:1611)(cid:506)0.04(cid:998)(cid:1040)
或搭公車的來回總距離皆為 20 公里，則與
(cid:581)(cid:33)
(cid:5138)(cid:1611)(cid:506)0.05(cid:998)(cid:1040)
駕駛汽車相比，她至少要改搭公車上下班幾天，
(cid:581)(cid:33)
(cid:1555)(cid:1611)(cid:506)0.17(cid:998)(cid:1040)
減少產生的碳排放量才會超過她搭飛機產生的
圖(九)
碳排放量？',
  '[{"key": "A", "text": "310 天"}, {"key": "B", "text": "309 天"}, {"key": "C", "text": "308 天"}, {"key": "D", "text": "307 天"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  15,
  '甲、乙兩個最簡分數分別為 、 ，其中 a、b 為正整數。若將甲、乙通分
a b
化成相同的分母後，甲的分子變為 50，乙的分子變為 54，則下列關於 a 的
敘述，何者正確？',
  '[{"key": "A", "text": "a 是 3 的倍數，也是 5 的倍數"}, {"key": "B", "text": "a 是 3 的倍數，但不是 5 的倍數"}, {"key": "C", "text": "a 是 5 的倍數，但不是 3 的倍數"}, {"key": "D", "text": "a 不是 3 的倍數，也不是 5 的倍數"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  17,
  '∆ABC 中，∠B = 55°， ∠C = 65°。今分別以 B、C 為圓心，BC 長為半徑
畫圓B 、圓 C，關於 A 點位置，下列敘述何者正確？',
  '[{"key": "A", "text": "在圓 B 外部，在圓 C 內部"}, {"key": "B", "text": "在圓 B 外部，在圓 C 外部"}, {"key": "C", "text": "在圓 B 內部，在圓 C 內部"}, {"key": "D", "text": "在圓 B 內部，在圓 C 外部"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  18,
  '如圖 ( 十 )，平行四邊形 ABCD 與平行四邊形 EFGH 全等，且 A、 B、 C、D
的對應頂點分別是 H、 E、 F、 G， 其中 E 在 DC 上， F 在 BC 上， C 在 FG 上。
若 AB = 7，AD = 5，FC = 3，則四邊形 ECGH 的周長為何？',
  '[{"key": "A", "text": "21"}, {"key": "B", "text": "20"}, {"key": "C", "text": "19"}, {"key": "D", "text": "18"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  19,
  '圖 ( 十一 ) 的數線上有 A(−2)、O(0)、B(2) 三點。今打算在此數線上標示
P( p)、 Q(q) 兩點，且 p、 q 互為倒數， 若 P 在 A 的左側， 則下列敘述何者正確？',
  '[{"key": "A", "text": "Q 在 AO 上，且 AQ < QO"}, {"key": "B", "text": "Q 在 AO 上，且 AQ > QO"}, {"key": "C", "text": "Q 在 OB 上，且 OQ < QB"}, {"key": "D", "text": "Q 在 OB 上，且 OQ > QB"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  21,
  '如圖 ( 十三 )，AC、BD 皆為半圓，AC 與 BD 相交於 E 點，其中 A、 B、C、
D 在同一直線上，且 B 為 AC 的中點。若 CE = 58°，則 BE 的度數為何？',
  '[{"key": "A", "text": "58"}, {"key": "B", "text": "60"}, {"key": "C", "text": "62"}, {"key": "D", "text": "64"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  22,
  '如圖 ( 十四 )，ΔABC 內部有一點 D，且 ΔDAB、ΔDBC、ΔDCA 的面積
分別為 5、4、3 。若 ΔABC 的重心為 G，則下列敘述何者正確？',
  '[{"key": "A", "text": "ΔGBC 與 ΔDBC 的面積相同，且 DG 與 BC 平行"}, {"key": "B", "text": "ΔGBC 與 ΔDBC 的面積相同，且 DG 與 BC 不平行"}, {"key": "C", "text": "ΔGCA 與 ΔDCA 的面積相同，且 DG 與 AC 平行"}, {"key": "D", "text": "ΔGCA 與 ΔDCA 的面積相同，且 DG 與 AC 不平行"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  23,
  '如圖 ( 十五 )，等腰梯形紙片 ABCD 中，AD // BC，AB = DC，∠B = ∠C，
且 E 點在 BC 上，DE // AB。今以 DE 為摺線將 C 點向左摺後，C 點恰落在
AB 上，如圖 ( 十六 ) 所示。若 CE = 2，DE = 4，則圖 ( 十六 ) 的 BC 與 AC
的長度比為何？',
  '[{"key": "A", "text": "1：2"}, {"key": "B", "text": "1：3"}, {"key": "C", "text": "2：3"}, {"key": "D", "text": "3：5"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  24,
  '以下為甲、乙兩個關於成年女性理想體重的敘述：
(甲)有的女性使用算法 與算法 算出的理想體重會相同
(乙)有的女性使用算法 與算法 算出的理想體重會相同
對於甲、乙兩個敘述，下列判斷何者正確？',
  '[{"key": "A", "text": "甲、乙皆正確"}, {"key": "B", "text": "甲、乙皆錯誤"}, {"key": "C", "text": "甲正確，乙錯誤"}, {"key": "D", "text": "甲錯誤，乙正確"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'math',
  25,
  '無論我們使用哪一種算法計算理想體重，都可將個人的實際體重歸類為
表 ( 二 ) 的其中一種類別。
表(二)
當身高 1.8 公尺的成年男性使用算法 計算理想體重並根據表 ( 二 ) 歸類，
實際體重介於 70 × 90% 公斤至 70 × 110% 公斤之間會被歸類為正常。若將
上述身高 1.8 公尺且實際體重被歸類為正常的成年男性，重新以算法 計算
理想體重並根據表 ( 二 ) 歸類，則所有可能被歸類的類別為何？',
  '[{"key": "A", "text": "正常"}, {"key": "B", "text": "正常、過重"}, {"key": "C", "text": "正常、過輕"}, {"key": "D", "text": "正常、過重、過輕"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  1,
  '「格外品」意指市場規格之外但品質無虞的農產品，例如規格不符或賣相不
佳。格外品會被農民分享給親友或作為肥料跟飼料，盛產時還可能出現遭大
量棄置的問題。下列何項作法較能有效解決上述問題？',
  '[{"key": "A", "text": "推動從產地到餐桌的理念，降低食物里程"}, {"key": "B", "text": "善用食品加工，以利農產品的保存與食用"}, {"key": "C", "text": "鼓勵農民改採有機農法，提高農產品售價"}, {"key": "D", "text": "種植基因改造作物，增加單位面積的產量"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  2,
  '由波蘭、匈牙利、斯洛伐克、捷克組成的維謝格拉德集團，近年來約有20%
至30%的商品出口至德國，因此當德國經濟成長減緩時，該集團國家的產業
可能衰退。根據上文，集團成員國最可能採取下列何項政策，以減少產業衰
退所帶來的負面影響？',
  '[{"key": "A", "text": "加速產業創新轉型及尋找新的貿易夥伴"}, {"key": "B", "text": "採取促使各國貨幣升值的政策以利出口"}, {"key": "C", "text": "退出歐盟並從非洲國家引進廉價勞動力"}, {"key": "D", "text": "鼓勵國內勞力密集產業外移至西歐國家"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  3,
  '臺灣某些聚落是以相對位置來命
名，例如北門。下列為某地區兩個
地名由來的描述：在地勢較高處屯
兵設營，故稱為上營盤，其西北山
腳處則稱為營盤腳，又名下營盤。
圖(一)為營盤腳附近的等高線地形
圖，根據上述及圖中資訊判斷，上
營盤最可能位在圖中何處？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  4,
  '圖(二)為某網站繪製的世界語言使用圖，呈現
全球23種使用人數超過5,000萬人的語言，其
中使用人數排第五名的語言主要分布區為下
列何者？',
  '[{"key": "A", "text": "西亞、北非"}, {"key": "B", "text": "東亞、南亞"}, {"key": "C", "text": "南歐、南美洲"}, {"key": "D", "text": "北美洲、大洋洲"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  5,
  '彰化平原上曾有一個稱為「七十二庄」的組織，由漳州人和客家人聯合成
立，他們透過共同的宗教活動，強化組織內部的連結，以抵抗鄰近泉州人的
勢力。上述組織的成立，最可能與下列哪一現象有關？',
  '[{"key": "A", "text": "鄭氏推行軍屯制度"}, {"key": "B", "text": "清代民間械鬥頻傳"}, {"key": "C", "text": "清朝政府開山撫番"}, {"key": "D", "text": "日本鎮壓漢人抗日"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  6,
  '圖(三)為一首歌曲部分歌詞的翻譯，其內容聚
焦於中國歷史上某一事件。歌詞中「在東方的
血腥戰爭」，最可能是指下列何者？',
  '[{"key": "A", "text": "蒙古大軍南下滅宋，成功入主中國"}, {"key": "B", "text": "英國為鴉片貿易問題出兵攻打中國"}, {"key": "C", "text": "八個國家組成聯軍向中國發動攻擊 &洋鬼子：鄙視外國人的稱呼。"}, {"key": "D", "text": "國民政府誓師北伐，終結軍閥割據"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  7,
  '古代人們在繪製地圖時，通常會將自己所處的區域放在地圖
中央。圖(四)是某地區出土的古世界地圖及其說明，該地區
當時所使用的文字，最可能為下列何者？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  8,
  '「某國在十九世紀末設置一個機構，最初是顧及戰後返國的軍人，身上可能
帶有病菌，因而先送往此處進行消毒及隔離，後來也在此處收容戰爭俘虜。
在該國曾參與的甲午戰爭、第一次世界大戰、九一八事變，乃至於太平洋戰
爭，此機構都曾發揮隔離檢疫的功能。」上述「某國」最可能是下列何者？',
  '[{"key": "A", "text": "美國"}, {"key": "B", "text": "德國"}, {"key": "C", "text": "日本"}, {"key": "D", "text": "法國"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  9,
  '以下是學者對歷史上臺灣的土地開發模式，所做出的分析：「十七世紀時，
『甲』透過提供土地、耕牛、資金借貸，招募『乙』修築城堡、耕種稻米與
甘蔗。甲、乙兩者之間雖然互相依賴，但甲常透過強制力懲罰不願受約束的
乙。」上述「甲」與「乙」，最可能是下列何者？',
  '[{"key": "A", "text": "荷蘭 聯合東印度公司與漢人"}, {"key": "B", "text": "清帝國與福建、廣東的漢人"}, {"key": "C", "text": "顏思齊集團與沿海的原住民"}, {"key": "D", "text": "鄭氏政權與大肚王國原住民"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  10,
  '圖(五)是老師在黑板上解釋某法律的部分內容，
根據圖中內容判斷，下列何者是該法律最主要的
立法目的？',
  '[{"key": "A", "text": "避免家庭暴力事件的發生"}, {"key": "B", "text": "處理兒童及少年犯罪事件"}, {"key": "C", "text": "確保兒童及少年身心發展"}, {"key": "D", "text": "維護社會秩序及善良風俗"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  11,
  '表(一)是小津整理的交易媒介比較表，表中甲、乙最可能為下列哪一組合？
表(ㄧ)
交易媒介 甲 乙
須事先存入足夠金額，並搭配特定
特色一 可直接支付各項消費
設備才能使用
特色二 由國家發行並賦予價值 多由民間企業發行
特色三 可能會面臨兌換零錢的困擾 免去購物找零錢的困擾',
  '[{"key": "A", "text": "商品貨幣與儲值卡"}, {"key": "B", "text": "商品貨幣與信用卡"}, {"key": "C", "text": "法定貨幣與儲值卡"}, {"key": "D", "text": "法定貨幣與信用卡"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  12,
  '新聞報導：大法官解釋第748號解釋文，宣告《民法》中未有保障同性婚姻之
規定，違反《憲法》保障人民平等權與婚姻自由之意旨，相關機關應在兩年
內完成法律修正或制定，若屆時未完成修法，同性二人可依現行《民法》規
定辦理結婚登記。上述內容顯示出我國《憲法》的哪一項特性？',
  '[{"key": "A", "text": "規範範圍最廣"}, {"key": "B", "text": "法律位階最高"}, {"key": "C", "text": "修改程序困難"}, {"key": "D", "text": "條文內容簡要"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  13,
  '小央花費數萬元購買限量模型，將商品帶回家後遭到父母反對，並立刻陪同
小央返回店家要求退貨。根據我國法律規定，就小央的年齡而言，此項契約
須經法定代理人同意才具備效力，因此店家只能辦理退貨。根據上述內容判
斷，下列何者最可能是訂立該規定的用意？',
  '[{"key": "A", "text": "維護無行為能力人的權益"}, {"key": "B", "text": "矯正未成年人的犯罪行為"}, {"key": "C", "text": "保護限制行為能力人的權益"}, {"key": "D", "text": "預防未成年人從事犯罪行為"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  14,
  '我國原本允許進口新鮮山竹，但2003年時，因新鮮山竹有引進害蟲的疑慮，
所以政府禁止進口，於是市面上只能買到進口的冷凍山竹。2019年4月，政府
公告將開放經殺蟲處理的新鮮山竹進口；同年9月，新鮮山竹上架銷售，雖然
價格高於冷凍山竹，仍在短時間銷售一空，後來各店家也持續補貨販售。根
據上述內容判斷，政府的開放政策帶來下列何項影響？',
  '[{"key": "A", "text": "貿易出超金額因而擴大"}, {"key": "B", "text": "農業出口總額因而上升"}, {"key": "C", "text": "購物意願因價格變化而提高"}, {"key": "D", "text": "產品選擇因而變得更加多元"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  15,
  '圖(六)顯示臺灣某一沿海
地區的土地利用變遷，根
據圖中資訊判斷，下列關
於該地區土地利用轉變的
敘述何者正確？
圖(六)',
  '[{"key": "A", "text": "可利用的土地因海岸侵蝕嚴重而減少"}, {"key": "B", "text": "魚塭的面積變化呈現先減後增的趨勢"}, {"key": "C", "text": "新的市區用地主要是由魚塭填土而來"}, {"key": "D", "text": "聚落的範圍主要是由南向北逐漸擴張"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  17,
  '日本某地因位處冬季季風迎風面，季風經日本海挾帶豐沛
水氣形成大量降雪，待降雪季節結束，積雪剷除後的道路
兩側留下垂直壁立高達十多公尺的雪壁，吸引大量遊客前 (cid:17392)(cid:17392)(cid:17392)
來。上述雪壁景色最可能位於圖(八)中何地？
(cid:7447)',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  19,
  '圖(十)是二十世紀時，甲、乙二國領袖來往的信函，根據內容判斷，甲、乙二
國最可能是下列何者？
圖(十)',
  '[{"key": "A", "text": "甲：蘇聯、乙：東德"}, {"key": "B", "text": "甲：西德、乙：美國"}, {"key": "C", "text": "甲：美國、乙：蘇聯"}, {"key": "D", "text": "甲：蘇聯、乙：美國"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  21,
  '「十四世紀時，由於此物產的生產與銷售，帶動一股商業活動：中國結合自
身及波斯生產的原料，製作成具有特色的商品後，由中國銷往印度、埃及、
波斯等地。十六世紀起，此物產又由西班牙船隻載運，從馬尼拉運往墨西哥
城與利馬；在此同時，歐洲王公貴族對此物產風靡不已，紛紛下單訂作。」
此物產最可能是下列何者？
&利馬：位於今秘魯境內。',
  '[{"key": "A", "text": "番薯"}, {"key": "B", "text": "瓷器"}, {"key": "C", "text": "鴉片"}, {"key": "D", "text": "白銀"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  22,
  '表(二)呈現五個國家 表(二)
2010年某宗教信徒占 教徒占全國總
國家
該國總人口數的比 人口比例 (%) (cid:17392)(cid:17392)(cid:17392)
例，根據內容判斷， 柬埔寨 96.9 (cid:7359)(cid:7359)(cid:7359) (cid:7383)(cid:7383)(cid:7383)
(cid:7447)(cid:7447)(cid:7447)
此宗教的發源地最可 泰國 93.2
能位於圖(十二)中甲、 緬甸 80.1
圖(十二)
乙、丙、丁何處？ 不丹 74.7',
  '[{"key": "A", "text": "甲 斯里蘭卡 69.3"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  23,
  '表(三)是2022年8月時，我國前四大外籍移工來源國的部分資料：
表(三)
產業移工 社福移工 總人數
類別
( 營建業、製造業、漁業 ) ( 看護、家庭幫傭 ) 比例
越南 45.4% 12.7% 35.4%
國 菲律賓 25.3% 12.2% 21.3%
籍 印尼 16.1% 74.9% 34.1%
泰國 13.2% 0.2% 9.2%
性 男 71.4% 0.8% 49.8%
別 女 28.6% 99.2% 50.2%
根據表中資料，我們可觀察到關於外籍移工的何種現象？',
  '[{"key": "A", "text": "外籍移工的勞動權益因國籍而受到差別待遇"}, {"key": "B", "text": "外籍移工從事的工作類別存在明顯性別差異"}, {"key": "C", "text": "我國第二級產業主要外籍移工來源國為印尼"}, {"key": "D", "text": "我國第三級產業主要外籍移工來源國為越南"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  24,
  '小華整理客廳時發現一疊紙張，如圖(十三)。他拍照
上傳到社群網路詢問它的功能，以下是網友的回覆：
甲：「我們稱它為高速公路回數票，以前沒有電子收費
系統，經過收費站時將它拿給收費員當通行費。
在收費站前減速繳交回數票常會造成塞車，現在
圖(十三)
用電子收費就沒這個問題了。」
乙：「以前忘了帶錢時，把回數票當現金，少數店家也能接受，我還曾經用
它來買便當。」
關於上述高速公路回數票的說明及收費方式的變革，下列敘述何者最適當？',
  '[{"key": "A", "text": "科技發展使得交通運輸更順暢"}, {"key": "B", "text": "高速公路回數票可在銀行換外幣"}, {"key": "C", "text": "高速公路回數票具延遲支付功能"}, {"key": "D", "text": "科技發展讓交通工具的選擇更多元"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  25,
  '小惠在旅行的過程，曾借宿表(四)中四位親 表(四)
戚家，其中一位旁系血親參選當地的市民 行程 借宿地點 親戚稱謂
代表，因此在借宿的那天晚上，他也參與 第一天 新北市 姨丈
了掃街拜票。根據上述內容判斷，參選者 第二天 花蓮縣 舅舅
最可能是表中何者？
第三天 臺南市 姑姑',
  '[{"key": "A", "text": "姨丈"}, {"key": "B", "text": "舅舅"}, {"key": "C", "text": "姑姑"}, {"key": "D", "text": "伯母"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  27,
  '臺灣製鞋業在國內及海外約有3,000多家工廠，為
了拓展製鞋版圖，國內幾家製鞋大廠持續計畫在其
他國家籌設新廠。根據製鞋業的產業特色判斷，最
可能前往具備下列何種條件的國家設置新廠？',
  '[{"key": "A", "text": "人口眾多且所得較低"}, {"key": "B", "text": "原料豐富且地廣人稀"}, {"key": "C", "text": "動力充足且市場廣大"}, {"key": "D", "text": "資金豐沛且技術密集"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  28,
  '圖(十五)呈現雲林縣某一環境災害在前、後兩個時期分布的變化，可以觀察出
此災害最嚴重的地區在後期有向某地區轉移的現象，下列何項措施較有助於緩
解此災害在後期最嚴重的地區持續惡化？
(cid:49) (cid:20)(cid:28)(cid:28)(cid:20)(cid:16)(cid:21)(cid:19)(cid:19)(cid:19)(cid:11570) (cid:49) (cid:21)(cid:19)(cid:19)(cid:20)(cid:16)(cid:21)(cid:19)(cid:20)(cid:19)(cid:11570)
(cid:23)(cid:19) (cid:22)(cid:19)
(cid:28)(cid:19) (cid:22)(cid:19)
(cid:20)(cid:19) (cid:21)(cid:19) (cid:24)(cid:19) (cid:21)(cid:19)
(cid:27)(cid:19)
(cid:25)(cid:19) (cid:21)(cid:19) (cid:22)(cid:19) (cid:23)(cid:19) (cid:20)(cid:19)
(cid:26)(cid:19)
(cid:26)(cid:19)
(cid:26)(cid:19) (cid:23)(cid:19)
(cid:27)(cid:19)
(cid:24)(cid:19)
(cid:25)(cid:19)
(cid:25)(cid:19)
(cid:20)(cid:19) (cid:19437)(cid:18699)(cid:7369)(cid:25909)(cid:24717)(cid:11)(cid:8234)(cid:8388)(cid:12) (cid:20)(cid:19) (cid:19437)(cid:18699)(cid:7369)(cid:25909)(cid:24717)(cid:11)(cid:8234)(cid:8388)(cid:12)
(cid:19) (cid:20)(cid:19)(cid:3)(cid:78)(cid:80) (cid:19) (cid:20)(cid:19)(cid:3)(cid:78)(cid:80)
(cid:27030)(cid:25331) (cid:20664)(cid:25331) (cid:27030)(cid:25331) (cid:20664)(cid:25331)
圖(十五)',
  '[{"key": "A", "text": "提高自來水水費以減少用水"}, {"key": "B", "text": "鼓勵在高鐵沿線改種省水作物"}, {"key": "C", "text": "補助受影響居民墊高房舍與路基"}, {"key": "D", "text": "限制臺鐵通過此路段的運量與班次"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  29,
  '荔枝為臺灣受歡迎的水果之一，目前主要種植在中南
部。政府為了推廣臺灣荔枝，與澳洲合作，推動南半
球生產計畫，在澳洲尋找與臺灣荔枝種植的氣候條件
相似的地點，並於完成隔離檢疫後開始試種。根據上
文，圖(十六)中何處最有可能為試種的地點？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  30,
  '清末某位知識分子提出下述主張：「本世紀女權的問題，關鍵在於政治參與。
我認為女子能成為議員，也期望中國在海陸軍、財政部門、外交部門有女性任
職，更希望女子能被選舉為總統。我們必須以塑造尊重男女平權的新國民為起
點，並追求組織新政權為終極目標。」根據上文，此人認為應採取下列何種作
法，最可能創造理想中的女性政治參與環境？',
  '[{"key": "A", "text": "接受西域的胡人文化"}, {"key": "B", "text": "維護傳統的皇帝制度"}, {"key": "C", "text": "推翻清朝政府建立共和"}, {"key": "D", "text": "效法日本推動君主立憲"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  31,
  '圖(十七)是一張十八世紀末的漫畫及其說明，
作者所要傳遞的訊息，最可能是下列何者？',
  '[{"key": "A", "text": "對北美十三州宣布獨立表示反對"}, {"key": "B", "text": "對德意志帝國擴建海軍備感威脅"}, {"key": "C", "text": "對義大利統一建國運動提出異議"}, {"key": "D", "text": "對法國大革命向外蔓延感到不安"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  32,
  '「東漢末年戰亂頻仍，知識分子四散遷徙，人才難覓。曹丕在正式建立曹魏政
權前，為了改善人才選用方式，於延康元年(220年)實施此方法，在各郡設置中
正官，……。」上文中未完的內容，最適合放入下列何者？',
  '[{"key": "A", "text": "挑選各地賢能者，根據才學德行與資歷表現分為九等"}, {"key": "B", "text": "與耶穌會傳教士進行交流，引進西方科學知識與技術"}, {"key": "C", "text": "長期戰亂導致地方制度轉變，郡縣制度取代封建制度"}, {"key": "D", "text": "主辦地方層級的科舉考試，使平民任官機會逐漸增加"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  33,
  '目前的跨洋資訊傳輸多是透 表(五)
過海底電纜，表(五)為四條 電纜 西側端點所在位置 東側端點所在位置
海底電纜東、西端點的位置 甲 33.73°S，18.44°E 5.42°N，100.33°E
資訊。「太平洋光纖電纜網 乙 40.76°N，72.94°W 50.83°N，4.55°W
路」為一條橫跨太平洋的海 丙 38.73°N，9.15°W 31.26°N，32.31°E
底電纜，該電纜的興建可以
丁 24.86°N，121.83°E 33.91°N，118.42°W
提供兩個端點之間龐大的網
路流量需求，其中一端還能
進一步連接東南亞市場，此
條電纜最可能是表中何者？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  34,
  '圖(十八)是小安過去的網路貼文，圖(十九)是當時動物之家認養規定的部分內容：
圖(十八) 圖(十九)
根據圖(十八)、圖(十九)的內容判斷，小安參與的這兩次投票，先後順序最可
能為下列何者？',
  '[{"key": "A", "text": "地方選舉、中央選舉"}, {"key": "B", "text": "地方選舉、公民投票"}, {"key": "C", "text": "中央選舉、公民投票"}, {"key": "D", "text": "公民投票、中央選舉"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  35,
  '近年甲國新聞中常見關於殺人
案件的報導，許多人因而認為
治安不斷惡化，要求主管機關
首長下臺負責。曉晴想探究該
國社會治安情況，在網路上搜
尋到的資料如圖(二十)，圖中
顯示甲國近年殺人案件數，以
及用「殺人」為關鍵詞搜尋國
內網路新聞的搜尋結果數。根
圖(二十)
據上述內容判斷，下列何者最
可能是他探究的結論？',
  '[{"key": "A", "text": "社會治安不斷惡化顯示媒體未善盡監督政府責任"}, {"key": "B", "text": "媒體與社群網路的報導內容會影響公共意見方向"}, {"key": "C", "text": "公共意見雖經過反覆討論但形成後仍具有變動性 &變動性＝不穩定性"}, {"key": "D", "text": "閱聽大眾喜好常會影響新聞媒體產業的企業收入"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  36,
  '我國少子化與高齡化的情況日益嚴重，未來恐面臨勞動力不足的危機。政府
除了促進人口成長以減緩影響程度外，根據人力運用調查資料顯示，2018年
時約有150萬的壯年人口，因須承擔無酬勞動而未就業，有學者建議可設法提
高這些人參與市場勞動的意願。根據上述內容判斷，下列何者最可能是該學
者的建議之一？',
  '[{"key": "A", "text": "延後高齡勞工的退休年齡"}, {"key": "B", "text": "廣設優質平價的托育機構"}, {"key": "C", "text": "增加中小企業的就業機會"}, {"key": "D", "text": "健全國際志工的培訓制度"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  37,
  '中國實施「一帶一路」政策
規畫了許多經濟走廊，圖
(二十一)為部分經濟走廊示意
圖。其中有一條的規畫目的，
除可降低從波斯灣運石油至中
國須經印尼、馬來西亞間海峽
及南海的風險外，也兼具促進
中國西部地區與西亞、南亞國
家的能源和貿易往來，此經濟
走廊最可能為圖中何者？
圖(二十一)',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  38,
  '「自來水管在租界內埋設，沿街每十數步設置四尺高的吸水鐵桶，鐵桶下面
與水管連接，使用時將鐵桶上的機關轉開，水就會激射而下。自來水管理單
位有兩處，法國租界的管理處設在萬安里，英國租界的管理處就設在儲水的
水塔旁邊。管線外需要用水的居民也可以請水夫外送，不論遠近，每擔水都
收十文錢。」上述最可能是描寫下列何者的情形？',
  '[{"key": "A", "text": "十八世紀初的北京"}, {"key": "B", "text": "十八世紀末的廣州"}, {"key": "C", "text": "十九世紀初的廈門"}, {"key": "D", "text": "十九世紀末的上海"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  39,
  '藍蟹原產於美洲，因國際貿易蓬勃發展，透過船舶的壓艙水被帶往地中海，
由於該地氣候適宜生長又缺乏天敵，藍蟹數量大幅增加，而使原生物種的生
存空間受到擠壓。在法國 地中海沿岸，藍蟹已成為常被捕捉到的漁獲，但這
項食材在該國的食用者很少，使漁民生計受到衝擊；反觀北非 突尼西亞，在
原本漁獲減少的情況下，漁民轉而捕捉藍蟹販售，結果獲得不錯的收入。上
述關於二國漁民處境的內容，其所探討的主題最可能為下列何者？',
  '[{"key": "A", "text": "漁民如何在市場競爭中受惠"}, {"key": "B", "text": "漁民如何應對外來文化的衝擊"}, {"key": "C", "text": "全球化現象如何影響漁民的生活"}, {"key": "D", "text": "資訊科技發展如何便利漁民的生活"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  40,
  '我國某地方法院在一段時間內的刑事案件判決件數， (cid:7604)
(cid:13366)
以及其中屬於非告訴乃論刑事案件判決的件數，如圖 (cid:17392)
(二十二)。當地調解委員會在同一段時間內，也順利調解 (cid:7447)
了許多刑事案件。若上述調解成立的案件，當初都沒能
(cid:19)
(cid:13568)(cid:25681)(cid:11)(cid:11570)(cid:12)(cid:3)
調解成功，且這些案件皆改由該地方法院作出判決，則
圖(二十二)
關於圖中甲、乙線段的位置，下列何種變化最可能發生？',
  '[{"key": "A", "text": "甲線段上移，乙線段上移"}, {"key": "B", "text": "甲線段上移，乙線段不變"}, {"key": "C", "text": "甲線段下移，乙線段上移"}, {"key": "D", "text": "甲線段下移，乙線段不變"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  41,
  '英國的英格蘭足球超級聯賽，在最接近11月11日的比賽日，會舉辦紀念活
動：比賽前由軍人、球員與觀眾一起進行默哀儀式，各隊球衣上印有紅花圖
案，其餘參與者也在衣服上別著紅花。這是因為英國及其殖民地為紀念第一
次世界大戰犧牲將士，將11月11日訂為紀念日，許多殖民地在獨立後，仍保
留此節日。根據上文，下列何者最可能保有同樣的紀念活動？',
  '[{"key": "A", "text": "澳洲職業足球聯賽"}, {"key": "B", "text": "巴西足球甲級聯賽"}, {"key": "C", "text": "荷蘭足球甲級聯賽"}, {"key": "D", "text": "韓國職業足球聯賽"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  42,
  '1970年11月恆河出海口附近出現一座長3.5公里、寬3公里，最高點僅2公尺的
沙洲島，因其位處印度與孟加拉領海交界處，引發兩國領土爭議，但在爭議
還未解決之前，這座島嶼就消失了。根據當地自然環境判斷，該島嶼形成的
原因最可能是下列何者？',
  '[{"key": "A", "text": "位處板塊接觸帶，海底火山噴發"}, {"key": "B", "text": "恆河集水區的水土保持持續改善"}, {"key": "C", "text": "恆河河口附近的海平面持續上升"}, {"key": "D", "text": "豪雨侵襲，河流帶來大量堆積物"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  43,
  '表(六)為臺灣某時期四個主要港口，每十年的輸出額總和。根據表中資料，下
列何者的推論最恰當？
表(六) 單位：十萬元
年分 1896-1905 年 1906-1915 年 1916-1925 年 1926-1935 年
港口 對外國 對日本 對外國 對日本 對外國 對日本 對外國 對日本
基隆港 90 312 506 1,215 2,112 5,578 2,321 9,260
淡水港 708 5 563 7 467 0.5 157 0.2
安平港 144 135 49 259 25 67 16 65
打狗港 25 176 45 2,375 831 8,912 479 13,440',
  '[{"key": "A", "text": "打狗港的輸出額變化，可能受到殖民母國對糖業的資本挹注影響"}, {"key": "B", "text": "由於基隆離日本較近，其港口對殖民母國的輸出額占比較南部多"}, {"key": "C", "text": "表中各港口占臺灣對外輸出額比重，與十八世紀後期的情況相仿"}, {"key": "D", "text": "表中各港口輸出額的變動，應與當時的統治者推動十大建設有關"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  44,
  '文中巫童悲劇的發生，主要反映出下列何種現象？',
  '[{"key": "A", "text": "文化的差異形成文化位階"}, {"key": "B", "text": "法律的強制力高於宗教信仰"}, {"key": "C", "text": "民眾行為會受到社會規範影響"}, {"key": "D", "text": "公共意見是經由反覆辯論而形成"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  45,
  '文中關於巫童所受待遇的描述，最能凸顯下列何者的重要性？',
  '[{"key": "A", "text": "基本人權應受到普遍性的保障"}, {"key": "B", "text": "公權力的行使應受到法律約束"}, {"key": "C", "text": "自由信仰宗教的權利應受法律保障"}, {"key": "D", "text": "政府的權力應相互制衡以避免濫權"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  46,
  '根據文中第一段內容判斷，相較於電動機車，部分民眾喜愛使用電動自行車
的原因，最可能為下列何者？',
  '[{"key": "A", "text": "該產品的市場競爭程度日漸提升"}, {"key": "B", "text": "選擇使用該項產品的機會成本較低"}, {"key": "C", "text": "受匯率變化影響，產品販售價格調降"}, {"key": "D", "text": "負向誘因增加，民眾使用產品意願提高"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  47,
  '文中政府於2022年4月所做的變革，其過程須經下列哪一程序？',
  '[{"key": "A", "text": "公民投票複決"}, {"key": "B", "text": "憲法法庭審理"}, {"key": "C", "text": "行政機關移請覆議"}, {"key": "D", "text": "中央立法機關通過"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  48,
  '根據文中內容判斷，在修正規定施行前已持有微型電動二輪車者，關於其領
用車牌的敘述，下列何者最適當？',
  '[{"key": "A", "text": "最晚要在2024年5月3日領用車牌，以免遭受行政處罰"}, {"key": "B", "text": "最晚要在2024年5月3日領用車牌，以免遭受刑事處罰"}, {"key": "C", "text": "最晚要在2024年11月29日領用車牌，以免遭受行政處罰"}, {"key": "D", "text": "最晚要在2024年11月29日領用車牌，以免遭受刑事處罰"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  49,
  '根據上文及觀察圖(二十三)中不同年分各州眾議員席次的變化情形，可以推論
美國人口在這段期間有下列何項變動？',
  '[{"key": "A", "text": "南部州人口成長速度較東北部的州快"}, {"key": "B", "text": "美國各州持續呈現人口負成長的狀態"}, {"key": "C", "text": "加州因國際移民眾多而人口成長加快"}, {"key": "D", "text": "禁止移民的政策主導德州人口的變化"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  50,
  '影響美國各州人口多寡的因素眾多且不相同，觀察圖(二十三)中2020年眾議院
席次僅有1席的州，下列何者與這些州人口少的原因較無關聯？',
  '[{"key": "A", "text": "地形崎嶇"}, {"key": "B", "text": "工業就業機會少"}, {"key": "C", "text": "位居高緯且氣候嚴寒"}, {"key": "D", "text": "深受殖民地式經濟影響"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  51,
  '根據上文並參考圖(二十四)臺灣人口分布狀況，下
列關於各行政區立委席次分配的說明何者正確？',
  '[{"key": "A", "text": "屏東縣區域立委席次少於臺東縣"}, {"key": "B", "text": "新北市區域立委席次多於宜蘭縣"}, {"key": "C", "text": "彰化縣區域立委席次為全臺最少"}, {"key": "D", "text": "臺南市區域立委席次為全臺最多"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  52,
  '根據上文，「新電影」出現之前的戰後臺灣電影，最不可能播映下列何種劇情？',
  '[{"key": "A", "text": "中國 明朝年間，來自各路的武功高手在龍門客棧展開激烈戰鬥"}, {"key": "B", "text": "國軍將領對抗日軍時陣亡，蔣中正題字「英烈千秋」表示悼念"}, {"key": "C", "text": "男主角與豪門望族的女兒產生戀情，並捲入家族間的恩怨情仇"}, {"key": "D", "text": "主角因二二八事件遭到軍警處決，留下妻小長期受到政府監視"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  53,
  '根據上文，「新電影」發展之初，最可能以下列何者作為電影題材？',
  '[{"key": "A", "text": "宣揚政府推行南進政策所帶來的經濟成就"}, {"key": "B", "text": "關注一般農民、勞工等小人物生活中的困頓"}, {"key": "C", "text": "受到美援影響，將美國流行文化作為劇情主軸"}, {"key": "D", "text": "重視原住民文化，發揚原住民族音樂與神話傳說"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'social',
  54,
  '上文「削蘋果事件」中，國家企圖限制的人民權利類型，與下列何者最相似？',
  '[{"key": "A", "text": "對法庭上的被告宣告褫奪公權"}, {"key": "B", "text": "剝奪貪污罪犯應考公職的資格"}, {"key": "C", "text": "禁止過度血腥暴力影像的出版"}, {"key": "D", "text": "要求外國旅客入境應接受審查"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  2,
  '木糖醇是一種可以代替蔗糖的食品添加物。若要知道木糖醇是否和乙醇一樣
都是醇類，應查詢木糖醇的何項資訊？',
  '[{"key": "A", "text": "分子量"}, {"key": "B", "text": "組成的原子種類與排列方式"}, {"key": "C", "text": "組成的原子總數是否超過1000個"}, {"key": "D", "text": "氫和氧的原子數目比是否為1：1"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  3,
  '圖(二)為臺灣一週的氣溫預報圖，呈現不同地區的氣溫隨時間變化情況，圖中
橫坐標的刻度代表當日正午12點。
圖(二)
若媒體想根據圖(二)，以簡易標題說明未來幾天的天氣概況，下列哪一說法最合適？',
  '[{"key": "A", "text": "11/07起，北部轉冷，中、南部變更熱"}, {"key": "B", "text": "11/08起，全臺連日豪雨持續一週"}, {"key": "C", "text": "11/08起，冷空氣南下，當日北部氣溫驟降"}, {"key": "D", "text": "11/10起，中部天氣趨於穩定，日夜溫差逐日變小"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  5,
  '人體副甲狀腺分泌的激素是經由X所運送，若此激素分泌過多，會影響骨骼中
的Y含量，可能造成骨質疏鬆。根據上述說明，推論X和Y最可能為下列何者？',
  '[{"key": "A", "text": "X為血液，Y為鈣"}, {"key": "B", "text": "X為血液，Y為鉀"}, {"key": "C", "text": "X為消化液，Y為鈣"}, {"key": "D", "text": "X為消化液，Y為鉀"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  6,
  '小健家中電扇插頭處的電線被老鼠破壞而導致
銅線裸露，如圖(四)。小健取來絕緣膠帶試圖
修復，步驟如圖(五)。家人認為小健的修復方
式並不適當，其原因最可能為下列何者？',
  '[{"key": "A", "text": "插電後電扇雖會轉動，但轉動速率下降"}, {"key": "B", "text": "插電後電扇雖會轉動，但耗電量將上升"}, {"key": "C", "text": "插電後電線會發生短路，可能引發電線走火"}, {"key": "D", "text": "插電後，流過電扇的電流將變大，導致電扇"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  7,
  '虎門銷煙為清朝銷毀鴉片的歷史事件。把海水引入浸泡池浸泡鴉片，之後再加
入石灰等物質，石灰遇水會改變水溫，此改變也利於將鴉片溶於水中，等退潮
時再排入海中。關於上述銷毀鴉片的說明，下列何者最合理？',
  '[{"key": "A", "text": "石灰溶於水為放熱反應，而高溫使鴉片更易溶於水中"}, {"key": "B", "text": "石灰溶於水為吸熱反應，而高溫使鴉片更易溶於水中"}, {"key": "C", "text": "鴉片浸泡海水後會使水溫上升，使其與石灰反應速率加快"}, {"key": "D", "text": "鴉片浸泡海水後會使水溫下降，使其與石灰反應速率加快"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  8,
  '圖(六)是世界文學名著《小王子》中的某段場景與內容：
圖(六)
若以箭頭表示太陽光方向與地球自轉方向，下列何者最符合文中畫雙底線處的
狀態？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": "2"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  9,
  '醃漬高麗菜時，常會在高麗菜的葉片上灑鹽。圖(七)為正常
的葉片細胞示意圖，表(一)中的圖為小凱與小萍預測醃漬後
的葉片細胞可能的示意圖。推論醃漬後的示意圖與造成
葉片細胞變化的原因，下列何者正確？
圖(七)
表(一)',
  '[{"key": "A", "text": "小凱的圖正確，水由細胞內流至外界"}, {"key": "B", "text": "小凱的圖正確，鹽由細胞內流至外界"}, {"key": "C", "text": "小萍的圖正確，水由外界流至細胞內"}, {"key": "D", "text": "小萍的圖正確，鹽由外界流至細胞內"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  10,
  '圖(八)為中洋脊附近的剖面示意圖，並標示中洋脊
旁的X處與離中洋脊較遠的Y處、Z處海洋地殼。根
據上述，下列何者最可能為X處、Y處、Z處的海洋
地殼年齡關係？
圖(八)',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  11,
  '將裝有紅棕色二氧化氮(NO )氣體的密閉玻璃瓶放入冰水中，二氧化氮會互相
2
結合產生無色的四氧化二氮(N O )氣體，瓶內的顏色會逐漸變淡，反應式為：
2 4
正反應
2 NO N O
2 2 4
逆反應
當溫度下降至某溫度，且保持恆定，一段時間後玻璃瓶內的顏色便不再改變。
關於顏色不再改變時反應速率的說明，下列何者正確？',
  '[{"key": "A", "text": "正反應速率等於逆反應速率，且速率為0"}, {"key": "B", "text": "正反應速率等於逆反應速率，且速率不為0"}, {"key": "C", "text": "正反應速率不等於逆反應速率，且兩速率均不為0"}, {"key": "D", "text": "正反應速率不等於逆反應速率，且其中一速率為0"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  12,
  '老師選用基因型皆為Aa的雄、雌長翅果蠅進行交配，並要求學生觀察 1000 隻
第一子代果蠅的表現型與數量。已知小坪僅觀察到4隻長翅果蠅及6隻短翅果蠅
後，就直接推測其結果如表(二)。老師在小坪的紀錄本寫下：「理論上子代數量
不太可能出現這樣的比例。」根據上述資訊，老師寫下該評語是因為理論上第
一子代預測比例較可能為何？
表(二)',
  '[{"key": "A", "text": "應全為長翅"}, {"key": "B", "text": "應全為短翅"}, {"key": "C", "text": "長翅與短翅的比例應約為1：3"}, {"key": "D", "text": "長翅與短翅的比例應約為3：1"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  14,
  '圖(十)為某河川鯰魚族群在甲、乙、丙、丁不同時期
數量變化的情形，下列何者最能說明甲、乙、丙、丁
的變化情形？',
  '[{"key": "A", "text": "甲：出生＋遷入＜死亡＋遷出"}, {"key": "B", "text": "乙：出生＋遷入＞死亡＋遷出"}, {"key": "C", "text": "丙：出生＋死亡＞遷入＋遷出"}, {"key": "D", "text": "丁：出生＋死亡＜遷入＋遷出"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  16,
  '圖(十二) 為汽車上測量輪胎某項物理量的裝置，
圖中的psi為其中數值的單位。此單位可表示為
磅力
1 psi ＝ 1 ，其中磅力為力的單位，英寸為長度
平方英寸
的單位。根據上述資訊，此項裝置的功能最可能為量測
汽車輪胎的哪一項物理量？
圖(十二)',
  '[{"key": "A", "text": "每秒轉動次數"}, {"key": "B", "text": "胎內的氣體壓力"}, {"key": "C", "text": "施於地面的推力"}, {"key": "D", "text": "與地面間的摩擦力"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  17,
  '牙齒酸蝕是指酸性物質會使牙齒外層的琺瑯質
軟化，而容易損耗。小涵進行實驗一，探討不
同pH值與牙齒酸蝕後重量減少的關係。他選用
形狀大小很相近的豬牙齒，分別浸泡不同濃度
的鹽酸數日，實驗一的結果如表(三)。
小涵又進行實驗二，取形狀大小很相近的豬牙齒，分別浸泡在pH值介於2～4之
間的甲、乙、丙三杯飲料中數日，發現牙齒重量減少百分比為丙＜甲＜乙。若
實驗二只考慮pH值的影響，則依實驗一的結果，關於甲、乙、丙三杯飲料的推
測，下列何者最合理？',
  '[{"key": "A", "text": "乙杯最酸，其pH值最大"}, {"key": "B", "text": "乙杯最酸，其pH值最小"}, {"key": "C", "text": "丙杯最酸，其pH值最大"}, {"key": "D", "text": "丙杯最酸，其pH值最小"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  18,
  '以下為某篇關於重力波的報導：
「重力波」是愛因斯坦預言的物理現象之一。當帶有質量的物體進行
加速度運動時，會在時空中產生波動，這種波就是重力波，重力波的傳播
不需要介質，其傳播速率與電磁波相同，都以光速傳播……。
根據上述資訊，下列有關重力波的敘述何者最合理？',
  '[{"key": "A", "text": "與水波一樣都屬於力學波"}, {"key": "B", "text": "與電磁波一樣都屬於力學波"}, {"key": "C", "text": "與光波一樣都不屬於力學波"}, {"key": "D", "text": "與超聲波一樣都不屬於力學波"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  19,
  '已知甲～丁四者均為純物質，其所含元素的質量 表(四)
百分比如表(四)。表中哪些物質不可能是有機化合物？
(原子量：C＝12、H＝1、O＝16)',
  '[{"key": "A", "text": "甲、乙"}, {"key": "B", "text": "乙、丙"}, {"key": "C", "text": "丙、丁"}, {"key": "D", "text": "甲、丙"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  20,
  '已知刺絲胞動物皆生活在水中。小花看到某網友提到：「所有刺絲胞動物
都生活在海洋中。例如海月水母就是一種生活在海洋中的刺絲胞動物」，
若小花想驗證「所有刺絲胞動物都生活在海洋中」這句話是否成立，則下列
何種方法最能達到此目的？',
  '[{"key": "A", "text": "從海洋中找到海月水母"}, {"key": "B", "text": "從海月水母身上找到刺絲胞"}, {"key": "C", "text": "從淡水中找到一種刺絲胞動物"}, {"key": "D", "text": "從海洋中找到很多種刺絲胞動物"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  4,
  '一週後，記錄三條路線上發芽的種子數。
表(五)為學生記錄此實驗的相關數據，若三條路線的生長環境都相同，根據此結
果，下列敘述何者最合理？
表(五)',
  '[{"key": "A", "text": "甲、乙兩品牌的發芽比例相等"}, {"key": "B", "text": "乙、丙兩品牌的發芽比例相等"}, {"key": "C", "text": "甲品牌比乙、丙品牌容易發芽"}, {"key": "D", "text": "丙品牌比甲、乙品牌不容易發芽"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  22,
  '小書與小花將某株被子植物莖部的形成層外圍構造剔除，發現此株植物逐漸因
根部無法獲得養分而死亡，以下為兩人對此株植物的推論：
小書：此株植物較可能為雙子葉植物。
小花：此株植物較可能為單子葉植物。
下列對兩人推論的敘述何者正確？',
  '[{"key": "A", "text": "兩人均合理"}, {"key": "B", "text": "兩人均不合理"}, {"key": "C", "text": "只有小書合理"}, {"key": "D", "text": "只有小花合理"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  23,
  '某篇關於氫應用的報導說明如下：「金屬多以氧化物的形式封藏於岩石礦物
中，可利用氫和氧易起反應的特性，將氧從礦物中移除，留下可用的純金屬和
水。」關於上述畫線處提及的反應，下列說明何者最合理？',
  '[{"key": "A", "text": "因為氫被氧化，所以是氧化還原反應"}, {"key": "B", "text": "因為礦物被氧化，所以是氧化還原反應"}, {"key": "C", "text": "因為金屬氧化物溶於水呈酸性，所以是酸鹼中和反應"}, {"key": "D", "text": "因為金屬氧化物溶於水呈鹼性，所以是酸鹼中和反應"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  25,
  '圖(十四)為 、 兩種岩類的照片及說明， 為一種作用。 的碎屑物質經過
長時間的 後，會成為 。下列有關 、 、 的敘述，何者最合理？
(cid:33)(cid:33)(cid:33)(cid:2178)(cid:1175)(cid:1837)(cid:1759)(cid:4800)(cid:2015)(cid:917) (cid:1255)(cid:1154)(cid:4086)(cid:1254)(cid:3544)(cid:6210)(cid:2895)(cid:928)(cid:500)
(cid:1254)(cid:3544)(cid:1800)(cid:2220)(cid:1088)(cid:1254)(cid:1988)(cid:2133)(cid:500) (cid:33)(cid:33)(cid:33)(cid:1937)(cid:1759)(cid:4715)(cid:2178)(cid:3031)(cid:1992)(cid:1053)(cid:1139)
(cid:1222)(cid:1392)(cid:2053)(cid:5065)(cid:1712)(cid:1804)(cid:1486)(cid:1291)(cid:502) (cid:1923)(cid:4362)(cid:500)(cid:1066)(cid:3755)(cid:1296)(cid:1486)(cid:1291)(cid:1937)
(cid:1759)(cid:4715)(cid:1255)(cid:3755)(cid:928)(cid:1041)(cid:502)
圖(十四)',
  '[{"key": "A", "text": "為變質岩， 為沉積岩"}, {"key": "B", "text": "為火成岩， 為火成岩"}, {"key": "C", "text": "：高溫與高壓作用，岩石成分與結構發生變化"}, {"key": "D", "text": "：壓密與膠結作用，碎屑顆粒緊密膠結在一起"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  27,
  '在一大氣壓下，將一塊質量100 g的冰塊置於燒杯
中，以穩定熱源均勻加熱，其溫度與加熱時間的
關係如圖(十六)。根據此圖判斷下列何者正確？',
  '[{"key": "A", "text": "T 的數值為0"}, {"key": "B", "text": "t 可以表示冰塊的熔點"}, {"key": "C", "text": "當時間大於t ，燒杯中的水只會以氣態存在"}, {"key": "D", "text": "在t ～t 期間，燒杯中的水是以固體與氣體共存的狀態"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  28,
  '美環將兩種不同的天氣系統分為甲、乙類，並舉例說明，如表(六)所示。但他的
舉例有錯誤，應更正為下列何者才合理？
表(六)',
  '[{"key": "A", "text": "颱風移到乙類，另外兩者不變"}, {"key": "B", "text": "太平洋暖氣團移到乙類，另外兩者不變"}, {"key": "C", "text": "颱風移到乙類，蒙古大陸冷氣團移到甲類"}, {"key": "D", "text": "颱風與太平洋暖氣團移到乙類，蒙古大陸冷氣團移到甲類"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  30,
  '青蛙的染色體有13對，其中1對為性染色體。在不考慮突變的情況下，雌蛙卵巢
內經減數分裂後的卵子，應有幾條性染色體？',
  '[{"key": "A", "text": "1條"}, {"key": "B", "text": "2條"}, {"key": "C", "text": "13條"}, {"key": "D", "text": "26條"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  31,
  '小茵居住在臺灣，圖(十七)為他就讀學校的教室平面
圖。小茵發現每日正午時，陽光從窗戶照射進教室內
的範圍會變化，圖中白色區域為某日受到正午陽光直接
照射到的範圍。之後他連續二個月每天觀察，發現正午
陽光直接照射到的範圍，從第1排逐漸擴大至第3排，
再逐漸縮至第2排。推測下列何者最可能是小茵觀察
的時間區間？',
  '[{"key": "A", "text": "春分前至春分後"}, {"key": "B", "text": "夏至前至夏至後"}, {"key": "C", "text": "秋分前至秋分後"}, {"key": "D", "text": "冬至前至冬至後"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  32,
  '一一座座游游泳泳池池裡裡有有多多少少的的尿尿？？
安賽蜜是優酪乳中的甜味劑，不易被人體消化，會由尿液排出體外。研
究團隊檢測加拿大游泳池的安賽蜜濃度，一座84萬公升游泳池的安賽蜜濃度
為2.1×10 —7 g/L，再參考「……」，經換算後，可知該游泳池約含有75公升的
尿液。
上述「……」所指的最可能為下列何者？
',
  '[{"key": "A", "text": "該游泳池池水的密度"}, {"key": "B", "text": "加拿大人尿液的平均密度"}, {"key": "C", "text": "該游泳池含有安賽蜜的總質量"}, {"key": "D", "text": "加拿大人尿液中安賽蜜的平均濃度"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  33,
  '圖(十八)為人體的泌尿系統和其所連接血管的示意圖，其
中乙血管中的氧氣含量比甲血管多。有關丙器官的生理功
能及血液進出丙的路徑，下列敘述何者正確？',
  '[{"key": "A", "text": "形成尿素，甲→丙→乙"}, {"key": "B", "text": "形成尿素，乙→丙→甲"}, {"key": "C", "text": "形成尿液，甲→丙→乙"}, {"key": "D", "text": "形成尿液，乙→丙→甲"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  34,
  '將圖(十九)甲、乙、丙、丁四個不同材質的實心正立方體分別放入1 L水中，
水的密度為1.0 g/cm3。已知四種物體皆不與水發生化學反應，且不吸水也不
溶於水，則根據表(九)判斷，靜止平衡後，哪一個物體在液面下的體積最大？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  35,
  '圖(二十)為某小島發生一次規模為M、震央震度為5弱的震度分布圖，甲、乙、丙
為測站位置。表(十)為小方整理這些測站在不同次地震得到的資訊，其中只有
一次是圖(二十)地震的資訊。根據上述資訊，M的值或範圍應為下列何者？
表(十)
圖(二十)',
  '[{"key": "A", "text": "M＝5.2"}, {"key": "B", "text": "5.2＜M＜6.1"}, {"key": "C", "text": "M＝6.1"}, {"key": "D", "text": "M＞6.1"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  36,
  '已知下列各選項的示意圖，表示由透鏡主軸上P點發射的光線，經過透鏡後的
偏折情形，則哪一個選項中透鏡的焦距最可能為10 cm？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  38,
  '如圖(二十一)，在無摩擦力的水平面靜置一個質量為
M的木塊，今以水平外力F推動此木塊，使其沿力的
方向移動S的距離，外力對木塊所作的功完全轉換為
木塊的動能。小明與小華想要讓木塊獲得的動能變 圖(二十一)
為原本的2倍，他們分別提出以下策略：
兩人的策略是否合理？',
  '[{"key": "A", "text": "兩人皆合理"}, {"key": "B", "text": "只有小明合理"}, {"key": "C", "text": "只有小華合理"}, {"key": "D", "text": "兩人皆不合理"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  39,
  '小美在植物圖鑑中看到杜鵑花科(Ericaceae)中的金毛杜鵑(Rhododendron oldhamii)
後，若想要依學名搜尋與此植物同屬但不同物種的植物，則下列何種查詢方式
最能達到他的目的？',
  '[{"key": "A", "text": "學名第一個字為Ericaceae的植物"}, {"key": "B", "text": "學名第二個字為oldhamii的植物"}, {"key": "C", "text": "學名第一個字為Rhododendron的植物"}, {"key": "D", "text": "學名為Rhododendron oldhamii的植物"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  40,
  '下列哪一實驗裝置圖最適合用來表示以直流電源在鐵片上鍍銅？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": "FeFeFFee CuCCuCuFueFeFFee CuCCuCuuFeFeFFee CuCCuCuuFeFeFFee CuCCuCuu"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  41,
  '某工廠進行原料加工的製程如表(十一)。 表(十一)
當開始加工時，此原料中酵素X會持續
催化原料中物質甲轉變成物質乙，但超
過75℃後就無法再有催化的功能。若僅
考慮酵素X的作用，這段加工製程中，哪
兩時間點所含物質乙的量最相近？',
  '[{"key": "A", "text": "10:00 和 10:10"}, {"key": "B", "text": "10:15 和 10:25"}, {"key": "C", "text": "10:25 和 10:45"}, {"key": "D", "text": "10:50 和 11:00"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  42,
  '根據本文，過去食蛇龜曾面臨下列何種問題？',
  '[{"key": "A", "text": "棲地破壞"}, {"key": "B", "text": "環境汙染"}, {"key": "C", "text": "過度捕捉"}, {"key": "D", "text": "外來種引入"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  43,
  '根據本文，關於食蛇龜在IUCN的分類，下列何者最合理？',
  '[{"key": "A", "text": "屬於滅絕物種"}, {"key": "B", "text": "屬於低風險物種"}, {"key": "C", "text": "屬於未做評估物種"}, {"key": "D", "text": "屬於生存受脅物種"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  44,
  '根據本文，下列何者最符合該國政府對未來發電方式的期望？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  45,
  '根據本文，將燃煤發電改採燃氣發電為主，可達到下列何種目的？',
  '[{"key": "A", "text": "減少每發一度電時所需耗費的金錢"}, {"key": "B", "text": "減少每發一度電時空氣汙染物的排放"}, {"key": "C", "text": "增加再生能源在整體能源使用的比例"}, {"key": "D", "text": "增加每發一度電時所排放的溫室氣體量"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  46,
  '根據圖(二十四)，2021年的「住宅用電」可表示為下列何者？',
  '[{"key": "A", "text": "2.235 × 1010度"}, {"key": "B", "text": "2.235 × 1011度"}, {"key": "C", "text": "5.2729 × 1011度"}, {"key": "D", "text": "5.2729 × 1012度"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  47,
  '文中提及「一般認為冷氣時會影響住宅用電多寡，冷氣時增加會使住宅用電
增加，減少則使住宅用電減少」，下列哪一項數據最符合上述引號中的說
法？',
  '[{"key": "A", "text": "2017～2018年冷氣時與住宅用電的變化情形"}, {"key": "B", "text": "2020～2021年冷氣時與住宅用電的變化情形"}, {"key": "C", "text": "這五年中，冷氣時最低年分與住宅用電最低年分，兩者的對應關係"}, {"key": "D", "text": "這五年中，冷氣時最高年分與住宅用電最高年分，兩者的對應關係"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  48,
  '文中「冷氣時」選擇以超過28℃的時數計算，其原因可能與下列何者最相關？',
  '[{"key": "A", "text": "28℃為臺灣的平均氣溫"}, {"key": "B", "text": "氣溫28℃時冷氣機最耗電"}, {"key": "C", "text": "28℃以上的氣溫，會讓多數民眾選擇開冷氣機"}, {"key": "D", "text": "冷氣機設定為28℃時，冷房效果最佳最為省電"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  49,
  '圖(二十五)中的二氧化碳濃度變化資料，整張圖所呈現的時間範圍約為多久？',
  '[{"key": "A", "text": "5個星期"}, {"key": "B", "text": "5個月"}, {"key": "C", "text": "5年"}, {"key": "D", "text": "50年"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'science',
  50,
  '文末提及「氧氣的濃度也會有週期性變化」，其變化百分比與理由，下列何者
最合理？',
  '[{"key": "A", "text": "因CO 的分子量大於O ，故O 的變化百分比會比2～3%要小很多"}, {"key": "B", "text": "因CO 的分子量大於O ，故O 的變化百分比會比2～3%要大很多"}, {"key": "C", "text": "因大氣中O 的濃度比CO 高得多，故O 的變化百分比會比2～3%要小很多"}, {"key": "D", "text": "因大氣中O 的濃度比CO 高得多，故O 的變化百分比會比2～3%要大很多"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  1,
  'Look at the picture. There is under the door.',
  '[{"key": "A", "text": "an envelope"}, {"key": "B", "text": "a plant"}, {"key": "C", "text": "a sign"}, {"key": "D", "text": "an umbrella"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  2,
  'My hurts so much that I cannot even turn my head.',
  '[{"key": "A", "text": "arm"}, {"key": "B", "text": "knee"}, {"key": "C", "text": "neck"}, {"key": "D", "text": "stomach"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  3,
  'Our school basketball team won the national game last night. We are so them.',
  '[{"key": "A", "text": "popular with"}, {"key": "B", "text": "proud of"}, {"key": "C", "text": "sorry for"}, {"key": "D", "text": "worried about"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  4,
  'Tomorrow is Sam’s last day in the office. Nobody knows why he decided to .',
  '[{"key": "A", "text": "hide"}, {"key": "B", "text": "leave"}, {"key": "C", "text": "pack"}, {"key": "D", "text": "walk"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  5,
  'It’s not a good idea to go mountain climbing in this bad . We should wait until the
typhoon goes away.',
  '[{"key": "A", "text": "chance"}, {"key": "B", "text": "dream"}, {"key": "C", "text": "habit"}, {"key": "D", "text": "weather"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  6,
  'Chris loves walking with Anna on snowy days, but Anna hates very much.',
  '[{"key": "A", "text": "them"}, {"key": "B", "text": "so"}, {"key": "C", "text": "one"}, {"key": "D", "text": "it"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  7,
  'Lora likes to eat bananas that are already a little brown on the outside, and so I.',
  '[{"key": "A", "text": "am"}, {"key": "B", "text": "do"}, {"key": "C", "text": "have"}, {"key": "D", "text": "will"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  8,
  'Your refrigerator shouldn’t be making loud noises now, but if it does, just give me a
call and I’ll come check it again.',
  '[{"key": "A", "text": "already"}, {"key": "B", "text": "even"}, {"key": "C", "text": "finally"}, {"key": "D", "text": "still"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  9,
  'After winning money in the card game, Jay decided to try again. He felt that he might also
be a second time.',
  '[{"key": "A", "text": "famous"}, {"key": "B", "text": "interested"}, {"key": "C", "text": "lucky"}, {"key": "D", "text": "ready"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  10,
  'The knife doesn’t cut very well. It’s not as as before.',
  '[{"key": "A", "text": "bright"}, {"key": "B", "text": "heavy"}, {"key": "C", "text": "quick"}, {"key": "D", "text": "sharp"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  11,
  'John will stay with his sister until he an apartment.',
  '[{"key": "A", "text": "will find"}, {"key": "B", "text": "would find"}, {"key": "C", "text": "finds"}, {"key": "D", "text": "found"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  12,
  'Students to go on the school trip should ask their parents first.',
  '[{"key": "A", "text": "who want"}, {"key": "B", "text": "want"}, {"key": "C", "text": "who they want"}, {"key": "D", "text": "what they want"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  13,
  'The temple sits alone in the mountains at a height of 3,000m sea level.',
  '[{"key": "A", "text": "above"}, {"key": "B", "text": "at"}, {"key": "C", "text": "below"}, {"key": "D", "text": "in"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  14,
  'Patty spent several days planning to invite Charlie to dinner, she couldn’t say a word
when they met.',
  '[{"key": "A", "text": "but"}, {"key": "B", "text": "if"}, {"key": "C", "text": "or"}, {"key": "D", "text": "so"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  15,
  'I can’t tell you what I think of the movie because I it. I’ll probably watch it this
Saturday.',
  '[{"key": "A", "text": "am not seeing"}, {"key": "B", "text": "don’t see"}, {"key": "C", "text": "haven’t seen"}, {"key": "D", "text": "won’t see"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  16,
  'The new guy at the help desk answers calls like a . There are no ups and downs in
his voice and you can’t tell if he is happy or sad.',
  '[{"key": "A", "text": "father"}, {"key": "B", "text": "foreigner"}, {"key": "C", "text": "radio"}, {"key": "D", "text": "robot"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  17,
  'Jasmine planned to spend her summer in the country, but right after she got there, she started
to the noise in the city.',
  '[{"key": "A", "text": "enjoy"}, {"key": "B", "text": "mind"}, {"key": "C", "text": "miss"}, {"key": "D", "text": "notice"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  18,
  '“Bad traffic” is perhaps the excuse for being late when your boss knows it only takes
you five minutes to walk to work.',
  '[{"key": "A", "text": "easiest"}, {"key": "B", "text": "oldest"}, {"key": "C", "text": "smartest"}, {"key": "D", "text": "worst"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  19,
  'The housework in Mr. and Mrs. Wang’s family between them and their kids.
Everyone’s got their own job to do.',
  '[{"key": "A", "text": "is shared"}, {"key": "B", "text": "are shared"}, {"key": "C", "text": "shares"}, {"key": "D", "text": "share"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  20,
  'I want to find another dentist because pulled out a good tooth last time I went to him.',
  '[{"key": "A", "text": "I"}, {"key": "B", "text": "me"}, {"key": "C", "text": "mine"}, {"key": "D", "text": "myself"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  21,
  'Mom: Linda, you’ve been playing computer games all evening! Have you finished your
report?
Linda: Well, most of it this afternoon, and I’ll finish it by Friday.',
  '[{"key": "A", "text": "I would do"}, {"key": "B", "text": "I did"}, {"key": "C", "text": "I was doing"}, {"key": "D", "text": "I’ll do"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  22,
  'Why did Philip go out?',
  '[{"key": "A", "text": "To meet a woman."}, {"key": "B", "text": "To look for his father."}, {"key": "C", "text": "To ask the police for help."}, {"key": "D", "text": "To buy food for his brother."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  23,
  'Why was Philip’s father angry?',
  '[{"key": "A", "text": "He forgot his keys."}, {"key": "B", "text": "The woman was hiding from him."}, {"key": "C", "text": "The police didn’t believe what he said."}, {"key": "D", "text": "Philip and his brother went out at night."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  24,
  'Kevin is going to buy some fresh bread at Baker’s Kitchen. He loves white bread, his mom
likes farm bread, his father enjoys bagels, and his sister eats only challah. Which is the
earliest possible time for him to get all these breads for his family?',
  '[{"key": "A", "text": "11:00am."}, {"key": "B", "text": "4:00pm."}, {"key": "C", "text": "5:00pm."}, {"key": "D", "text": "7:00pm."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  25,
  'What do we know about Baker’s Kitchen?',
  '[{"key": "A", "text": "It is open five days a week."}, {"key": "B", "text": "Its breads are half price one hour before closing."}, {"key": "C", "text": "Its croissants and pretzels are sold on weekends."}, {"key": "D", "text": "Its members can save $100 when they shop on Fridays."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  26,
  'What is recommended to people who want to visit the festival?  recommend 推薦',
  '[{"key": "A", "text": "Using the free festival bus service."}, {"key": "B", "text": "Visiting the festival on the weekend."}, {"key": "C", "text": "Entering Satyr’s Park from Fox Street."}, {"key": "D", "text": "Parking in Garden Square and walking to the festival."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  27,
  'What can we learn about the farmers’ market from the map?',
  '[{"key": "A", "text": "The farmers’ market is next to the flower market."}, {"key": "B", "text": "The farmers’ market and the festival are on the same block."}, {"key": "C", "text": "You can go to the farmers’ market by taking Bus No. 157 to Puppy Street."}, {"key": "D", "text": "The nearest metro station to the farmers’ market is the Koala Street Station."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  28,
  'What kind of people do Yan’s and Chang’s friends most likely think  likely 可能
Yan and Chang are?',
  '[{"key": "A", "text": "They enjoy good food."}, {"key": "B", "text": "They don’t like to share."}, {"key": "C", "text": "They like to make friends."}, {"key": "D", "text": "They don’t like new things."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  29,
  'What is it in the second story?',
  '[{"key": "A", "text": "A big knife."}, {"key": "B", "text": "The horse."}, {"key": "C", "text": "Lunch."}, {"key": "D", "text": "One of Chang’s ducks or chickens."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  30,
  'Why does the writer talk about doctors and a health center in the reading?',
  '[{"key": "A", "text": "To explain Chen’s services."}, {"key": "B", "text": "To talk about Chen’s future plans."}, {"key": "C", "text": "To explain Chen’s love for books."}, {"key": "D", "text": "To show why bookstores are important."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  31,
  'Why is Chen Bing-Hong’s job important in the example he gave?',
  '[{"key": "A", "text": "It allows people to get books as gifts."}, {"key": "B", "text": "It saves people money on new books."}, {"key": "C", "text": "It gives people hope to follow their dreams."}, {"key": "D", "text": "It helps people think of special moments in the past."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  32,
  'What is his magic?',
  '[{"key": "A", "text": "Fixing books."}, {"key": "B", "text": "Making book owners smile."}, {"key": "C", "text": "Finding books that are long lost."}, {"key": "D", "text": "Changing his bookstore into a library."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  33,
  'According to the reading, why did Rohla and Kreytenberg open Habibi & Hawara?',
  '[{"key": "A", "text": "To help refugees live better in Austria."}, {"key": "B", "text": "To collect money to help Syria fight the war."}, {"key": "C", "text": "To help Austrians learn about the war in Syria."}, {"key": "D", "text": "To help refugees go back to their home countries."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  34,
  'What can we learn about Habibi & Hawara?',
  '[{"key": "A", "text": "It was moved from Syria to Austria."}, {"key": "B", "text": "It may finally be sold to its workers."}, {"key": "C", "text": "It has cooking classes in Syrian food."}, {"key": "D", "text": "It is an important meeting place for Syrians."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  35,
  'What does it mean when people beg to differ?',
  '[{"key": "A", "text": "They do not agree."}, {"key": "B", "text": "They look different."}, {"key": "C", "text": "They cannot speak for others."}, {"key": "D", "text": "They do not notice something."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  36,
  'What does it mean when someone is an advocate of something?',
  '[{"key": "A", "text": "They talk a lot but do little about it."}, {"key": "B", "text": "They believe it is good and should be done."}, {"key": "C", "text": "They have had some bad experiences with it."}, {"key": "D", "text": "They are one of the first people who have done it."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  37,
  'What is special about the extinct frog in Smith’s book?',
  '[{"key": "A", "text": "It can live in a dirty living space."}, {"key": "B", "text": "It might help fix a health problem."}, {"key": "C", "text": "It eats its babies when it cannot find food."}, {"key": "D", "text": "It is the first extinct animal that people studied."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  38,
  'Why does Ellen Zimmer use the words from Dr. Solomon Wang?',
  '[{"key": "A", "text": "To start a new topic."}, {"key": "B", "text": "To share a big dream."}, {"key": "C", "text": "To make her idea clearer."}, {"key": "D", "text": "To invite people to take action."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  39,
  'What does Ellen Zimmer most likely think about bringing back extinct animals?',
  '[{"key": "A", "text": "It is possible."}, {"key": "B", "text": "It is dangerous."}, {"key": "C", "text": "It is not possible."}, {"key": "D", "text": "It is not dangerous."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  40,
  '(A) is not a new idea
(B) has not been very useful
(C) may bring some problems
(D) is not welcomed by everyone',
  '[{"key": "A", "text": "is not a new idea"}, {"key": "B", "text": "has not been very useful"}, {"key": "C", "text": "may bring some problems"}, {"key": "D", "text": "is not welcomed by everyone"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  41,
  '(A) Portland
(B) New York
(C) Denver
(D) Pittsburgh',
  '[{"key": "A", "text": "Portland"}, {"key": "B", "text": "New York"}, {"key": "C", "text": "Denver"}, {"key": "D", "text": "Pittsburgh"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  42,
  '(A) had higher numbers of deaths
(B) stopped social distancing too soon
(C) began social distancing a second time
(D) had the most days of social distancing',
  '[{"key": "A", "text": "had higher numbers of deaths"}, {"key": "B", "text": "stopped social distancing too soon"}, {"key": "C", "text": "began social distancing a second time"}, {"key": "D", "text": "had the most days of social distancing"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '113年國中教育會考',
  'english_reading',
  43,
  '(A) Also
(B) At first
(C) However
(D) For example
14 試題結束',
  '[{"key": "A", "text": "Also"}, {"key": "B", "text": "At first"}, {"key": "C", "text": "However"}, {"key": "D", "text": "For example"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  1,
  '(cid:8)
根據資料，右側詐騙簡訊使用了哪一種話術？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  2,
  '「清代驗屍跟現代不同，驗屍一定是在『屍所』，即屍體所在之處，可能是案
發現場，也可能是陳屍處。清代的程序非常強調在屍所驗屍，禁止將屍體帶到
他處檢驗。同時十分強調涉案人、關係人和家屬必須在場，一般大眾也可以圍
觀。目的在於使驗屍過程中，關於屍傷屍狀的觀察都能夠『公同一干人眾，質
對明白』。」若要拍攝清代刑案電視劇，下列情節何者最符合本文的敘述？',
  '[{"key": "A", "text": "將屍體從案發現場帶至衙門驗屍"}, {"key": "B", "text": "官府開始驗屍時，家屬必須到場"}, {"key": "C", "text": "驗屍時將一干閒雜人等驅離現場"}, {"key": "D", "text": "家屬要求確認結果，被斷然拒絕"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  3,
  '根據下表中的字形，何者的造字原則與「月」字相同？',
  '[{"key": "A", "text": "小"}, {"key": "B", "text": "木"}, {"key": "C", "text": "出"}, {"key": "D", "text": "汝"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  4,
  '關於右側這首詩的解讀，下列何者最恰當？',
  '[{"key": "A", "text": "悲傷會過去，快樂會留下"}, {"key": "B", "text": "我的快樂等同於我的悲傷"}, {"key": "C", "text": "除了悲傷之外，我一無所有"}, {"key": "D", "text": "每個人的愛情都只有一種結果"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  6,
  '根據以上資料，下列推論何者最恰當？',
  '[{"key": "A", "text": "因疫情而封城，易誘發潛在的家庭暴力"}, {"key": "B", "text": "疫情期間女性受家暴後通報的意願較高"}, {"key": "C", "text": "家庭壓力上升造成女性收入與行動受限"}, {"key": "D", "text": "過度關注疫情，導致政府漠視性別平權"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  7,
  '(cid:308) (cid:308)
(cid:307) (cid:306)
(cid:307) (cid:306)
根據甲、乙二圖，下列敘述何者最恰當？',
  '[{"key": "A", "text": "皆指出如何區分漢語的聲調"}, {"key": "B", "text": "皆指出對聯「仄起平收」的原則"}, {"key": "C", "text": "皆說明貼的順序為上聯 → 橫批 → 下聯"}, {"key": "D", "text": "皆說明站在屋外、面向大門的右邊要貼下聯"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  8,
  '貫雲石〈小梁州〉秋
芙蓉映水菊花黃，滿目秋光。枯荷葉底鷺鷥藏。金風盪，飄動桂枝香。
雷峰塔畔登高望，見錢塘一派長江。湖水清，江潮漾。天邊斜月，新雁兩三行。
關於這首曲的分析，下列何者最恰當？',
  '[{"key": "A", "text": "題目為〈小梁州〉，是散曲中的小令"}, {"key": "B", "text": "在曲作的中間換韻，不是一韻到底"}, {"key": "C", "text": "以「菊花」、「金風」、「桂枝」呼應「秋」"}, {"key": "D", "text": "以「斜月」、「新雁」象徵世間繁華轉眼成空"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  10,
  '「蜂造之蜜出山崖、土穴者十居其八，而人家招蜂造釀而割取者，十居其二
也。北方乾燥，土穴所釀多出於此。南方卑溼，故有崖蜜而無穴蜜。西北半天
下，蓋與蔗漿分勝云。」根據本文，下列推論何者最恰當？',
  '[{"key": "A", "text": "穴蜜多產於乾燥之處"}, {"key": "B", "text": "崖蜜多為人工養育而來"}, {"key": "C", "text": "卑溼之地沒有天然的蜂造之蜜"}, {"key": "D", "text": "西北蜂蜜產量是東南蔗漿的一半"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  11,
  '「旅行回來，一篇遊記常要寫上許久，有的終究沒寫成。有時不知怎麼濃縮剪
裁，最後只是一片凌亂的札記和草稿。那些沒寫出來的，只好留待時間去處理
了。時間如果不是個偉大的作者，起碼是個傑出的編輯。也許它最後會告訴
我：不寫也罷！」根據文意脈絡，關於畫線處文句的解讀，下列何者最恰當？',
  '[{"key": "A", "text": "真正優秀的作品，經得起時間的考驗"}, {"key": "B", "text": "要寫出一篇好遊記，作者比編輯更重要"}, {"key": "C", "text": "成為傑出的編輯，需要時間與經驗的累積"}, {"key": "D", "text": "經過時間的沉澱，自然能釐清值得寫的是什麼"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  12,
  '「我的本行是科學而非文學甲甲也許這正是我的缺失乙乙也許這反而是我的長處，
無論如何我清楚明白丙丙科學需要人文的關懷丁丁而文學需要理性的自覺。」根據
文意脈絡，甲乙丙丁四處，何者最適合填入標點符號中的冒號？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  13,
  '下列文句中的語詞，何者使用最恰當？',
  '[{"key": "A", "text": "他奮力救人的義舉，淪為一段佳話"}, {"key": "B", "text": "我如此盡心，既然得到這樣的待遇"}, {"key": "C", "text": "此建案已延宕多時，如今終於竣工"}, {"key": "D", "text": "那件事能夠完成，不愧有你的幫忙"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  14,
  '下列文句「」中的字，何者讀音正確？',
  '[{"key": "A", "text": "有些玩笑話沒拿捏好分寸，就可能變成「揶」揄：ㄧㄝˊ"}, {"key": "B", "text": "這家賣場備有各種「晾」晒工具，提供消費者選購：ㄐㄧㄥ"}, {"key": "C", "text": "這齣音樂劇結合不同族群的元素，打破文化的「藩」籬：ㄆㄢ"}, {"key": "D", "text": "原以為勝券在握，卻因一時疏忽，竟從雲端「栽」了下來：ㄘㄞˊ"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  15,
  '蒲松齡《聊齋志異》共492篇，包括兩種作品：一是幾百字甚至幾十字的
奇聞逸事，另一是長達數千言的故事，是真正的短篇小說，兩種作品各占一
半。《聊齋志異》真正的短篇小說能從前人作品找到「本事」（原型）的約
百篇，意即近二分之一的篇章不是作者獨創，而是改寫前人作品。魯迅說此
書「亦頗有從唐傳奇轉化而出者」。
關於文中《聊齋志異》的說明，下列何者最恰當？',
  '[{"key": "A", "text": "有些唐傳奇故事是蒲松齡寫作的來源"}, {"key": "B", "text": "找不到原型的篇章數不及全書的一半"}, {"key": "C", "text": "全書能找到原型的作品大多是奇聞逸事"}, {"key": "D", "text": "書中的短篇小說篇幅僅幾百甚至幾十字"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  16,
  '下列文句，何者用字完全正確？',
  '[{"key": "A", "text": "所謂有志竟成，努力必能得到回報"}, {"key": "B", "text": "得饒人處且饒人，你何必趕進殺絕"}, {"key": "C", "text": "想到他的處境，我情不自盡地落淚"}, {"key": "D", "text": "眼不見為靜，把雜物塞進櫃子就好"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  17,
  '祖可〈小重山〉﹕「誰向江頭遺恨濃？碧波流不斷，楚山重。柳煙和雨隔疏
鐘。黃昏後，羅幕更朦朧。 桃李小園空。阿誰 猶笑語，拾殘紅。珠簾捲盡
1
夜來風。人不見，春在綠蕪中。」關於這闋詞的分析，下列何者最恰當？',
  '[{"key": "A", "text": "上片押平聲韻，下片轉押仄聲韻"}, {"key": "B", "text": "上片寫景抒情，下片敘事兼論理"}, {"key": "C", "text": "「碧波流不斷」將「遺恨濃」具體化"}, {"key": "D", "text": "藉由「綠蕪」來反襯「桃李」的豔冶"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  18,
  '皎然〈尋陸鴻漸不遇〉：「移家雖帶郭，野徑入桑麻。近種籬邊菊，秋來未著
花。扣門無犬吠，欲去問西家。報道山中去，歸來每日斜。」根據本詩，作者
此次訪友之行曾看見下列何者？',
  '[{"key": "A", "text": "荒蕪的農地"}, {"key": "B", "text": "盛開的菊花"}, {"key": "C", "text": "歸來的鴻漸"}, {"key": "D", "text": "鴻漸的鄰居"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  19,
  '下列文句中的詞語，何者使用最恰當？',
  '[{"key": "A", "text": "這部電影的戰爭場面逼真，其慘烈不可名狀"}, {"key": "B", "text": "他表面上雖然毫不在乎，但心裡卻不以為意"}, {"key": "C", "text": "他的心情不言而喻，大家都不知他是喜是怒"}, {"key": "D", "text": "長官對此事不置可否，讓下屬有明確的方向"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  20,
  '太祖以事責丞相李善長，劉基言：「善長勛舊，能調和諸將。」太祖曰：
「是數欲害汝，汝竟為之言耶？吾將相汝矣。」基頓首曰：「是如易柱，須得
大木。若束小木為之，且立覆。」
關於文中人物的敘述，下列何者最恰當？',
  '[{"key": "A", "text": "太祖因多次陷害劉基而心存愧疚"}, {"key": "B", "text": "太祖想以李善長替代劉基為丞相"}, {"key": "C", "text": "劉基認為李善長調和諸將就像束小木"}, {"key": "D", "text": "劉基認為李善長比自己適合擔任丞相"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  22,
  '安邑里巷口有賣餅者，吾每早過戶，未嘗不聞其歌。一日，召之與語，
貧窘可憐。因與萬錢，令多其本，日取餅以償之。欣然持錢而去。後過其戶，
則寂然不聞謳歌之聲。及呼乃至，謂曰：「爾何輟歌之遽乎？」曰：「本流既
大，所謀益增，不暇唱曲矣。」
關於文中的「吾」與賣餅者，下列敘述何者最恰當？',
  '[{"key": "A", "text": "「吾」喜歡吃賣餅者的餅，日日光顧"}, {"key": "B", "text": "賣餅者生意資本擴增後，工作更繁忙"}, {"key": "C", "text": "「吾」喜歡賣餅者的歌聲，勸他以此招攬生意"}, {"key": "D", "text": "賣餅者經濟狀況改善之後，就不想再繼續賣餅"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  24,
  '「世傳《碧雲騢》一卷為梅聖俞作，皆歷詆慶曆以來公卿隱過，雖范文正亦不
免。議者遂謂聖俞游諸公間，官竟不達，懟而為此以報之。君子成人之美，縱
使萬有一不至，猶當為賢者諱，況未必有實。聖俞賢者，豈至是哉？後聞之，
乃魏泰所為，嫁之聖俞也。此豈特累諸公，又將以誣聖俞？歐陽文忠《歸田錄》
自言不記人之過惡，君子之用心當如此也。」下列何者最符合本文的觀點？',
  '[{"key": "A", "text": "范文正也曾揭發公卿的過錯"}, {"key": "B", "text": "《碧雲騢》應非梅聖俞所作"}, {"key": "C", "text": "魏泰因官運不亨而怨懟梅聖俞"}, {"key": "D", "text": "《歸田錄》反對替賢者隱諱的筆法"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  25,
  '根據本文，下列關於公呆的敘述何者最恰當？',
  '[{"key": "A", "text": "若移至深海生活，可以延長生命"}, {"key": "B", "text": "噴水嚇阻敵人，反而暴露藏身處"}, {"key": "C", "text": "閉殼後像石頭，碰撞也不易破損"}, {"key": "D", "text": "群體死亡前，會一起躺平晒太陽"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  26,
  '關於本文的寫作分析，下列何者最恰當？',
  '[{"key": "A", "text": "以祖孫對話暗示不同世代價值觀的差異"}, {"key": "B", "text": "以作者童年拾蛤經驗抒發對親人的懷念"}, {"key": "C", "text": "藉北極圓蛤明彰顯生態永續發展的重要"}, {"key": "D", "text": "藉公呆的形象比喻活到老學到老的態度"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  27,
  '小原根據本文與圖(一)畫了一張灰面鵟鷹遷徙路線圖，如圖(二)。小嵐認為
小原在圖中標示的遷徙路線有疏漏和錯誤，他提出了下列說法。對照本文
後，何者可以成立？
圖(一)
圖(二)',
  '[{"key": "A", "text": "北上的路線應該在臺灣南部出海"}, {"key": "B", "text": "北上的路線少畫了經由蘭嶼的這條"}, {"key": "C", "text": "南下的路線不應該經由墾丁出海"}, {"key": "D", "text": "南下的路線少畫了從中國來的這條"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  28,
  '根據本文，八卦山成為灰面鵟鷹重要休息站的原因，最可能是下列何者？',
  '[{"key": "A", "text": "林相完整，雨量豐沛"}, {"key": "B", "text": "地形獨特，容易識別"}, {"key": "C", "text": "食物豐富，地形適合"}, {"key": "D", "text": "氣候溫暖，適合繁殖"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  29,
  '根據甲文，關於劇本的創作，下列敘述何者最恰當？',
  '[{"key": "A", "text": "增加對白的比例可讓電影更有視覺效果"}, {"key": "B", "text": "要看懂電影必須先學習視覺化寫作的技能"}, {"key": "C", "text": "視覺化寫作可讓讀劇本的人較容易掌握情境"}, {"key": "D", "text": "希區考克認為視覺化寫作是劇本最重要的部分"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  30,
  '關於乙劇本的寫作分析，下列何者最恰當？',
  '[{"key": "A", "text": "透過極簡的對白讓事件留有餘韻"}, {"key": "B", "text": "藉「關上」一詞讓角色間有衝突"}, {"key": "C", "text": "以節拍器故障凸顯角色性格的偏執"}, {"key": "D", "text": "用狀聲詞「喀啦」製造情節的轉折"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  31,
  '乙劇本畫線處的文句，最無法呼應甲文中哪一項視覺化寫作的要素？',
  '[{"key": "A", "text": "場景外觀"}, {"key": "B", "text": "場景事件"}, {"key": "C", "text": "角色外貌"}, {"key": "D", "text": "角色行動"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  32,
  '根據本文，那些人不停追問他人到底賺多少錢，其原因最不可能是下列何者？',
  '[{"key": "A", "text": "對貧窮的恐懼"}, {"key": "B", "text": "對未來想像的單一"}, {"key": "C", "text": "重視良好的生活品質"}, {"key": "D", "text": "認為工作的意義只在金錢"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  33,
  '根據文意脈絡，畫線處文句的涵義，與下列何者最接近？',
  '[{"key": "A", "text": "充分的實現自我"}, {"key": "B", "text": "不再與他人比較"}, {"key": "C", "text": "賺取足夠的金錢"}, {"key": "D", "text": "犧牲已到達極限"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  34,
  '根據本文，下列店家的說明何者最不可能是「縮水式漲價」？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  35,
  '根據本文，消費者對企業選擇的「另一條路」較不抗拒的原因，最可能是下列
何者？',
  '[{"key": "A", "text": "較可感受廠商回饋的誠意"}, {"key": "B", "text": "較符合實際上的使用需求"}, {"key": "C", "text": "較能與同類產品產生區隔"}, {"key": "D", "text": "較難直觀察覺價格的改變"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  36,
  '關於文中新、舊《五代史》對南唐君主的記載，下列敘述何者最恰當？',
  '[{"key": "A", "text": "《舊五代史》記錄李昪，是因為認同他的正統地位"}, {"key": "B", "text": "新、舊《五代史》都不肯承認南唐君主的帝王身分"}, {"key": "C", "text": "南唐君主在《舊五代史》的定位比在《新五代史》高"}, {"key": "D", "text": "《新五代史》不承認北方政權，故未提及李後主入宋"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  37,
  '根據本文，下列何者最接近作者的觀點？',
  '[{"key": "A", "text": "應該重視王朝興替的「正統情結」"}, {"key": "B", "text": "北方政權相對穩定，有利於人文建設"}, {"key": "C", "text": "肯定李氏三代重視文教，對文化的貢獻"}, {"key": "D", "text": "趙匡胤借「陳橋兵變」稱帝，是為僭越"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  39,
  '根據本文，公子光最無法接受誰擔任吳王？',
  '[{"key": "A", "text": "餘祭"}, {"key": "B", "text": "夷眛"}, {"key": "C", "text": "季子札"}, {"key": "D", "text": "僚"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  40,
  '根據文意脈絡，下列「」中的詞語，何者替換後意義仍相同？',
  '[{"key": "A", "text": "日前「令郎」訪逮：令尊"}, {"key": "B", "text": "「比來」，數於都下朋從處見此屏：近來"}, {"key": "C", "text": "豈意「一旦」不煩懇請：剎那"}, {"key": "D", "text": "「俗故」忽忽：老友"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  41,
  '關於文中的石月屏，下列敘述何者最恰當？',
  '[{"key": "A", "text": "若不是薛虢州贈送石月屏，司馬光無從見其真貌"}, {"key": "B", "text": "石月屏雖比文錦、白璧昂貴，但司馬光更重友情"}, {"key": "C", "text": "司馬光初獲石月屏時雖心喜，當下仍堅守節操婉拒"}, {"key": "D", "text": "石月屏自然生成，清氣可見，因此司馬光甚為喜愛"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'chinese',
  42,
  '根據本文，下列何者最可能是司馬光收下石月屏後的反應？',
  '[{"key": "A", "text": "欲登門回禮，惜薛公務繁忙，擬另擇日造訪"}, {"key": "B", "text": "獲贈禮物，喜出望外，故寫信向薛表達謝意"}, {"key": "C", "text": "受薛贈寶深感有愧，已經備好厚禮回贈致謝"}, {"key": "D", "text": "為辨優劣，邀請好友來家中共同鑑賞石月屏"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  1,
  '算式 710 × 72 ÷ 74 之值可用下列何者表示？',
  '[{"key": "A", "text": "73"}, {"key": "B", "text": "75"}, {"key": "C", "text": "78"}, {"key": "D", "text": "716"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  2,
  '計算 ( 5x2 − 2x ) − ( 4 − 3x ) 的結果，與下列何者相同？',
  '[{"key": "A", "text": "5x2 − 3x"}, {"key": "B", "text": "5x2 + x − 4"}, {"key": "C", "text": "5x2 − 5x + 4"}, {"key": "D", "text": "5x2 − 5x − 4"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  4,
  '若二元一次聯立方程式 37x + 2y = 81 的解為 x = a ，則 a + 2b 之值為何？
23x − 2y = 39 y = b',
  '[{"key": "A", "text": "33"}, {"key": "B", "text": "9"}, {"key": "C", "text": "−3"}, {"key": "D", "text": "−27"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  5,
  '如圖(二)， ∆ABC 中有 AD ，D 點在 BC 上。根據
圖中標示的度數，求 p + q + r 之值是多少？',
  '[{"key": "A", "text": "140"}, {"key": "B", "text": "150"}, {"key": "C", "text": "160"}, {"key": "D", "text": "180"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  7,
  '圖 ( 四 ) 為某國預估 50 年後的人口變動數直方圖，各組的數值若為正數表示
該組人口 50 年後會增加，若為負數表示該組人口 50 年後會減少。根據此圖預估
該國 60 歲以上的人口，50 年後會增加或減少多少人？
圖(四)',
  '[{"key": "A", "text": "增加 207 萬人"}, {"key": "B", "text": "增加 425 萬人"}, {"key": "C", "text": "減少 109 萬人"}, {"key": "D", "text": "減少 271 萬人"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  8,
  '計算 ( 2 3 + 6 ) × 2 的結果，與下列何者相同？',
  '[{"key": "A", "text": "4 3"}, {"key": "B", "text": "6 3"}, {"key": "C", "text": "2 3 + 2 6"}, {"key": "D", "text": "4 3 + 2 6"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  9,
  '某園區想將 20 個無障礙停車位設置在出入口附近，為了符合規定，規劃每個
停車位的長度為 600 公分，寬度為 200 公分，並且停車位旁需設置寬度為 150 公分
的下車區，相鄰的停車位可以共用下車區。若以圖 ( 五 ) 的方式讓這些停車位
相鄰，且兩個相鄰的停車位之間皆有下車區，則圖中的停車位及下車區的總寬度
是多少公分？',
  '[{"key": "A", "text": "6850"}, {"key": "B", "text": "7000"}, {"key": "C", "text": "7150"}, {"key": "D", "text": "7200"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  11,
  '阿嘉和小楊都有 5 張分別標示數字 1、2、3、4、5 的紙牌，圖(六)表示兩人
的牌中皆有三張牌被自己蓋住的情形。今兩人打算從自己蓋住的紙牌中翻
開一張牌，若阿嘉蓋住的牌中每張牌被翻開的機會相等，小楊蓋住的牌中每
張牌被翻開的機會相等，則比較兩人翻開的那張牌上的數字，阿嘉比小楊大
的機率為何？
1 3
1',
  '[{"key": "A", "text": "3"}, {"key": "B", "text": "5 2"}, {"key": "C", "text": "9"}, {"key": "D", "text": "9"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  12,
  '有甲、乙、丙三種三角形木片，其邊長如圖 ( 七 ) 所示，阿林、小博打算利
用這三種木片各自組合成一個正三角錐。首先兩人皆選一片甲當作底面，
接著阿林選三片乙當作側面，小博選三片丙當作側面，關於兩人選的木片
能不能組合成一個正三角錐，下列判斷何者正確？',
  '[{"key": "A", "text": "兩人皆能"}, {"key": "B", "text": "兩人皆不能"}, {"key": "C", "text": "阿林能，小博不能"}, {"key": "D", "text": "阿林不能，小博能"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  13,
  '已知甲方程式為 ( x − 4 )2 = 9，乙方程式為 ( x + 9 )2 = −4。關於甲、乙兩
方程式的解的情形，下列敘述何者正確？',
  '[{"key": "A", "text": "甲有兩個相異的解，乙無解"}, {"key": "B", "text": "甲有兩個相異的解，乙有兩個相異的解"}, {"key": "C", "text": "甲有兩個相同的解，乙無解"}, {"key": "D", "text": "甲有兩個相同的解，乙有兩個相異的解"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  14,
  '圖 ( 八 ) 為貝可咖啡店的菜單，店家今日
準備了 120 杯咖啡和 100 個三明治販售。
若今日準備的餐點全部售出且收入共為
8700 元，則售出早餐組合的收入在下列
哪一個範圍？',
  '[{"key": "A", "text": "4300 ～ 4399 元"}, {"key": "B", "text": "4400 ～ 4499 元"}, {"key": "C", "text": "4500 ～ 4599 元"}, {"key": "D", "text": "4600 ～ 4699 元"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  15,
  '如圖 ( 九 )，數線上由左至右有 A(a)、B(b)、C(c)、D(d)、E(e) 五點，且
AB = BC = CD = DE。若原點在 AE 上，且 a + b = e ，則下列關於原點
位置的敘述，何者正確？',
  '[{"key": "A", "text": "在 BC 上且較接近 B 點"}, {"key": "B", "text": "在 BC 上且較接近 C 點"}, {"key": "C", "text": "在 CD 上且較接近 C 點"}, {"key": "D", "text": "在 CD 上且較接近 D 點"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  16,
  '如圖 ( 十 )，∆ABC 中，D 點為 AB 的中點，E 點在 AB 上，F 點在 AC 上，
且 EF // BC。若 AF = 7，FC = 3，則下列敘述何者正確？',
  '[{"key": "A", "text": "DE > EB，DF 與 EC 平行"}, {"key": "B", "text": "DE > EB，DF 與 EC 不平行"}, {"key": "C", "text": "DE < EB，DF 與 EC 平行"}, {"key": "D", "text": "DE < EB，DF 與 EC 不平行"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  17,
  '圖 ( 十一 ) 是某種螺絲釘上螺紋的示意圖，圖中的虛線皆為水平線或鉛垂線，
圖上標示出角度，也標示出水平線間或鉛垂線間的距離。根據圖中的標示，
判斷此種螺絲釘的螺紋深度是螺紋間距的多少倍？
5',
  '[{"key": "A", "text": "8"}, {"key": "B", "text": "16"}, {"key": "C", "text": "8"}, {"key": "D", "text": "16"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  18,
  '已知 a、b、c 皆為正整數，且 a、b 兩數的最大公因數與最小公倍數分別為
11 與 88。關於 a、b、c 三數的最大公因數與最小公倍數，甲、乙兩人分別
提出看法如下：
甲： a、b、c 三數的最大公因數可能比 11 大
乙： a、b、c 三數的最小公倍數可能比 88 小
對於甲、乙兩人的看法，下列判斷何者正確？',
  '[{"key": "A", "text": "甲、乙皆正確"}, {"key": "B", "text": "甲、乙皆錯誤"}, {"key": "C", "text": "甲正確，乙錯誤"}, {"key": "D", "text": "甲錯誤，乙正確"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  19,
  '圖(十二)為金銀河影城的價目表。某
社團 16 人去此影城看電影，打算以比賽
獎金 6000 元購買電影票、爆米花與
飲料。若要讓每人拿到一張電影票和
一杯飲料，則最多可買多少盒爆米花？',
  '[{"key": "A", "text": "3"}, {"key": "B", "text": "4"}, {"key": "C", "text": "5"}, {"key": "D", "text": "6"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  20,
  '圖(十三)為一張五邊形紙片 ABCDE，F 點在 CD 上，且以 BE、BF、FE 為
摺線將紙片向內摺至同一平面後，A、C、D 恰重疊在同一點 P，如圖(十四)所
示。若 BE > FE > BF，則根據圖(十四)中標示的角， 判斷下列敘述何者正確？
6
圖(十三) 圖(十四)',
  '[{"key": "A", "text": "∠3 + ∠4 = 90°，∠1 + ∠2 > ∠5 + ∠6"}, {"key": "B", "text": "∠3 + ∠4 = 90°，∠1 + ∠2 < ∠5 + ∠6"}, {"key": "C", "text": "∠3 + ∠4 ≠ 90°，∠1 + ∠2 > ∠5 + ∠6"}, {"key": "D", "text": "∠3 + ∠4 ≠ 90°，∠1 + ∠2 < ∠5 + ∠6"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  21,
  '坐標平面上有二次函數 y = −( x + 7 )2 + 12 的圖形，今將此圖形向右平移 10
單位，平移過程中此圖形與 y 軸的交點也會跟著變化。假設此圖形與 y 軸的
交點為 P，判斷在平移過程中，P 點位置的變化情形為下列何者？',
  '[{"key": "A", "text": "持續向下"}, {"key": "B", "text": "持續向上"}, {"key": "C", "text": "先向下再向上"}, {"key": "D", "text": "先向上再向下"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  22,
  '如圖 ( 十五 )，∆ADG 的頂點 G 為 ∆ABC 的重心，DG 與 AB 相交於 E 點。
若 DE ： EG = 3：2， AE ： EB = 3：4， 則 ∆ADG 面積為 ∆ABC 面積的多少倍？
5',
  '[{"key": "A", "text": "12"}, {"key": "B", "text": "14"}, {"key": "C", "text": "15"}, {"key": "D", "text": "21"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  23,
  '如圖 ( 十六 )，∆ABC 的三個頂點都在一圓上，固定 A 點將 ∆ABC 依順時針
方向旋轉，旋轉後的三角形為 ∆AB′C′，且 B′ 會落在同一圓上，其中 AB 與
AC′ 的夾角為 x°。若 BC = 54°，CA = 62°，則 x 值為何？',
  '[{"key": "A", "text": "27"}, {"key": "B", "text": "31"}, {"key": "C", "text": "32"}, {"key": "D", "text": "37"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  24,
  '小桃騎乘該自行車時， 原本使用的前齒輪為 33 齒， 後齒輪為 21 齒。根據上
文，他從原本的前後齒輪組合切換成下列四種組合中的哪一種後，踩起來最
費力？',
  '[{"key": "A", "text": "前齒輪不變，後齒輪切換為 18 齒"}, {"key": "B", "text": "前齒輪不變，後齒輪切換為 24 齒"}, {"key": "C", "text": "前齒輪切換為 22 齒，後齒輪不變"}, {"key": "D", "text": "前齒輪切換為 44 齒，後齒輪不變"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'math',
  25,
  '即使是不同的前齒輪齒數與後齒輪齒數的組合，仍可能產生相同的齒輪比，
因此小桃這輛 18 段變速自行車實際上只能夠產生 14 種不同的齒輪比。根據
上文，判斷這輛自行車切換前齒輪齒數與後齒輪齒數的組合時，下列哪一個
齒輪比有最多種組合？
11',
  '[{"key": "A", "text": "6"}, {"key": "B", "text": "7"}, {"key": "C", "text": "8"}, {"key": "D", "text": "9"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  1,
  '一國若發生重大自然災害，可能會直接衝擊該國的經濟活動，而成為較脆弱
的投資環境。臺灣因位於地震帶常發生地震，且易受颱風侵襲，於2015年被
某金融機構列為最脆弱的十個國家之一。下列哪一國家最可能也因為常發生
上述二種自然災害而列名其中？',
  '[{"key": "A", "text": "日本"}, {"key": "B", "text": "伊朗"}, {"key": "C", "text": "北韓"}, {"key": "D", "text": "澳洲"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  2,
  '2019年底，臺灣的農場與牧場，正式迎來首批合法的農業移工，其中2名是酪農移
工，其餘 5名則是外展農業移工。外展農業移工意指由農會、漁會、農林漁牧有
關之合作社，或非營利組織等「外展機構」所聘僱的外國人，並由外展機構指派
其至服務的場所從事農務工作。上述政策的推行主要是為了因應下列何項問題？',
  '[{"key": "A", "text": "農業勞動力老化"}, {"key": "B", "text": "農產品的安全性"}, {"key": "C", "text": "農村失業率偏高"}, {"key": "D", "text": "稻米的生產過剩"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  3,
  '某部電影描述主角與母親及只會說華語的祖母，同住在美國 舊金山 華人聚集
的街區，並出現拿筷子吃飯、與家人共度春節及清明節等原鄉文化情節，而
主角雖然從小在美國長大，但在生活中仍經常使用華語。上述電影情節的文
化意涵及傳播方式，與下列何者呈現的概念最相近？',
  '[{"key": "A", "text": "利用國際婦女節倡導家務分工性別平權理念"}, {"key": "B", "text": "來自泰、緬的新住民與移工齊聚慶祝潑水節"}, {"key": "C", "text": "推行國語運動貶低母語所產生的不平等現象"}, {"key": "D", "text": "華人認為烏鴉象徵厄運，在日本則象徵吉祥"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  4,
  '圖(一)是某行政區內名為挖仔的聚落地圖。根
據該聚落所處環境特色判斷，其地名代表的意
義最可能為下列何者？',
  '[{"key": "A", "text": "位於岬灣海岸的灣澳"}, {"key": "B", "text": "鄰近溪流河道的轉彎處"}, {"key": "C", "text": "位處高山之間的小谷地"}, {"key": "D", "text": "台地上的低窪地蓄水成湖"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  5,
  '某研究於2018年調查發現，臺灣不同地區民眾對於各種社會議題的關注傾向與
程度有所差異，其中部分地區的民眾對於自身周遭環境的議題更加關切，例如
離島地區。下列何者最可能為離島地區民眾較為關注的議題？',
  '[{"key": "A", "text": "適當管制房價，降低民眾租屋或購屋的負擔"}, {"key": "B", "text": "落實區域間資源分配，讓民眾獲得同等醫療品質"}, {"key": "C", "text": "管制重工業廢水的排放，避免造成土壤重金屬汙染"}, {"key": "D", "text": "大規模土石流或崩塌，可能導致建築物毀損及人員傷亡"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  7,
  '中國史上某作家發表了一部著作，他在書中提倡 表(ㄧ)
六項女性應當恢復的自然權利，如表(一)所示。該
著作所提倡的主張，最可能與下列何者有關？',
  '[{"key": "A", "text": "隋 唐時期，西域民族風俗傳入中國"}, {"key": "B", "text": "宋 元時期，朱熹學術成就受到推崇"}, {"key": "C", "text": "明末清初，中國引入西方科學知識"}, {"key": "D", "text": "晚清時期，近代歐洲思潮傳入中國"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  8,
  '「十一世紀時，旅居中國的穆斯林商人，在生活方面可以依照自身的習俗行
事，例如他們在廣州的清真寺高塔上，懸掛旗幟、燈火來指引船隻出入港
口。但在貿易方面，仍須受到官方機構的管轄，此機構負責收取關稅、接
運貢品，並執行香料、珊瑚及象牙等進口商品的專賣，監督商家船隻的活
動。」上述的「機構」最可能是下列何者？',
  '[{"key": "A", "text": "洋行"}, {"key": "B", "text": "驛站"}, {"key": "C", "text": "市舶司"}, {"key": "D", "text": "總理各國事務衙門"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  9,
  '「巴黎和會引起中國強烈的民族情緒，在部分知識分子的心中，西方角色從啟
蒙者轉變為壓迫者，因此他們逐漸對維護帝國主義、資本主義的西方國家感到
失望。在五四運動後，有些知識分子開始轉向世界革命理論，試圖從俄國革命
家對於受壓迫民族的呼籲，以及俄國新政權宣布放棄沙皇時代在中國特權的聲
明中，找到改變中國的出路。」上述內容最可能與下列何者有關？',
  '[{"key": "A", "text": "中華民國的建立"}, {"key": "B", "text": "西安事變的發生"}, {"key": "C", "text": "中國共產黨的成立"}, {"key": "D", "text": "文化大革命的發動"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  10,
  '圖(三)是一幅歷史上的木刻版畫。根據畫中 (cid:514)(cid:1187)(cid:5313)(cid:1663)(cid:6176)(cid:516)(cid:567)
內容判斷，作者的立場最可能是下列何者？',
  '[{"key": "A", "text": "強調君士坦丁堡教會擁有基督教的領導權"}, {"key": "B", "text": "支持路德教派所提出因信得救的信仰主張"}, {"key": "C", "text": "主張只有希伯來民族能作為耶和華的選民"}, {"key": "D", "text": "認同羅耀拉等人所提倡天主教改革的理念"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  11,
  '一間跨國咖啡公司打算在某國的傳統文化觀光區設立分店，但卻因為品牌形
象與當地建築、傳統飲食習慣不同而引發居民抗議。該公司為此改變店面沿
用的品牌風格，除了採用相容於該區環境的色系，還將原本的英文招牌改用
當地文字呈現，並增加販售具當地料理特色的創意餐點，希望透過這些舉動
降低當地的反彈聲浪。上述跨國公司的舉動，與下列何者最相符？',
  '[{"key": "A", "text": "成立跨國企業，強化國際分工"}, {"key": "B", "text": "憑藉強勢文化，推動產業轉型"}, {"key": "C", "text": "尊重多元文化，促進文化融合"}, {"key": "D", "text": "凝聚社區認同，發展社區組織"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  12,
  '美國於2022年6月21日起，禁止進口來自中國 新疆的商品，因為美國政府認為
這些商品是強迫維吾爾人勞動的產物。如果企業想要繼續將在新疆生產的商
品出口至美國，則必須提出充足的證據，證明商品的生產過程沒有涉及強迫
勞動問題。美國執行上述管制措施的主要理由，最可能是下列何者？',
  '[{"key": "A", "text": "擴大對外貿易的出超金額"}, {"key": "B", "text": "減少全球化下的貿易障礙"}, {"key": "C", "text": "保障旅外國民的工作權益"}, {"key": "D", "text": "避免侵害人權的商業行為"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  13,
  '某大學於學期末時，在校內美食街設立意見回饋箱，消費者有任何建議都可以
寫在意見單上投入回饋箱中，學校會參考這些回饋的意見，藉以改善未來美食
街的營運方式。根據上述內容判斷，下列何項回饋意見最能提升市場的競爭程
度？',
  '[{"key": "A", "text": "廠商應提供校內師生購買餐點九折優惠"}, {"key": "B", "text": "應要求廠商提供餐點食材的生產履歷證明"}, {"key": "C", "text": "希望廠商販售份量較少且價格較便宜的餐點"}, {"key": "D", "text": "學校應招募更多廠商進駐美食街提供多元餐點"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  15,
  '表(二)是恬恬為了製作課堂報告所蒐 表(二)
集的資料，統計針對某候選人的新聞 占播報時間比例 (%)
電視臺
在各電視臺報導時間中所占比例。根 總比例 正面報導 負面報導
據表中資料判斷，下列何者最可能是 水果臺 36 28 4
恬恬探究這份資料後，建議閱聽人應 F News 12 4 6
注意的事項？ 西水新聞 7 3 2',
  '[{"key": "A", "text": "覺察媒體的報導內容與事實不符 W 電視 28 4 21"}, {"key": "B", "text": "解讀媒體報導中的性別刻板印象 統計時間："}, {"key": "C", "text": "留意媒體業者是否持有特定的立場 5 / 1 - 5 / 7 每日19 : 00 ~ 20 : 00的新聞"}, {"key": "D", "text": "關注媒體是否善盡監督政府的責任"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  16,
  '圖(五)為中國於2019至2025年間規劃推
動的「西部陸海新通道」，該通道利用
鐵路、公路及海運等多種運輸方式以促
進物流效率與經濟發展。根據圖中資訊
判斷，上述通道的推動最可能具有下列
何項效益？',
  '[{"key": "A", "text": "連結經北極海通往歐洲的航線"}, {"key": "B", "text": "節省與美墨加協定成員的海運時間"}, {"key": "C", "text": "增進與東南亞國協成員的貿易往來"}, {"key": "D", "text": "避免來自西亞的石油運輸受制於他國"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  17,
  '小荃想造訪一處風景優美的祕境，但在抵達祕境
的入口處，見有一告示牌寫著「上游水壩不定時
洩洪，請勿進入溪谷以確保生命安全」，於是決
定避開危險另覓他處。圖(六)為上述祕境附近的等
高線地形圖，圖中甲、乙、丙、丁何者最可能為
該祕境所在地點？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  18,
  '近年來由於新冠肺炎疫情造成嚴重的通貨膨脹，使得甲地的房價及物價高
漲，影響其生活品質。此外，因為在鄰國的乙地1天的薪水，在甲地約1小時
就賺得到，於是有一部分的甲地人搬至乙地居住，再利用遠距工作或每天通
勤至甲地上班，藉以降低房租及生活消費。上述甲地與乙地依序最可能位於
何國？',
  '[{"key": "A", "text": "法國、英國"}, {"key": "B", "text": "美國、墨西哥"}, {"key": "C", "text": "土耳其、希臘"}, {"key": "D", "text": "馬來西亞、新加坡"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  19,
  '圖(七)為2022年世界及甲區域的人口年齡及性別資料，根據人口組成判斷，
甲區域最可能為下列何者？
圖(七)',
  '[{"key": "A", "text": "歐洲"}, {"key": "B", "text": "北美洲"}, {"key": "C", "text": "東北亞"}, {"key": "D", "text": "漠南非洲"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  20,
  '圖(八)是博物館展覽對臺灣歷史上某陶
製漏斗狀工具使用方式的介紹。此種工
具在十八至十九世紀之間，最多被用於
圖(九)中何處？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  21,
  '以下是學者對於中國史上某制度的論述：「此制度的基本涵義是指統治者透
過任用非世襲的官員，建立中央集權的政府。這個制度初步發展於東周，
在秦王朝統一天下後全面施行，隋 唐等朝代都繼續沿用，也影響了周遭的
日本、朝鮮，是中國重要的制度。」根據上述內容判斷，該制度最可能是下
列何者？',
  '[{"key": "A", "text": "郡縣制度"}, {"key": "B", "text": "封建制度"}, {"key": "C", "text": "科舉制度"}, {"key": "D", "text": "九品官人法"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  23,
  '「1989年8月19日，奧地利及匈牙利曾在邊界
上相鄰的兩個小鎮間，舉辦一場野餐交流活
動。活動中，兩鎮之間的木製國界圍籬會被
打開三小時，象徵支持沒有隔閡的歐洲。然
而，這場野餐會卻成為政治性的脫逃活動。
當圍籬一打開，從其他國家特別前來此地的
數百男女就迅速衝過邊界，逃離受到共產集
團控制、實施計畫經濟的家鄉，抵達了『自
由的歐洲』。」上述利用野餐脫逃的民眾，
最可能來自圖(十一)中甲、乙、丙、丁何地？
圖(十一)',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  24,
  '某國中學生自治組織選舉前，針對二種投票 表(三)
方式進行調查，其中願意投票的人數比例如 投票方式 實體 網路
表(三)所示。根據上述內容判斷，關於此一 年級 投票 投票
調查結果，下列敘述何者最適當？
七 48% 93%',
  '[{"key": "A", "text": "實體投票比網路投票更能形成民意"}, {"key": "B", "text": "使用科技可能有洩漏個人資料的風險"}, {"key": "C", "text": "實體投票比網路投票更符合無記名原則"}, {"key": "D", "text": "使用科技能提升學生參與公共事務的程度 & 實體 投票：設置投票箱"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  25,
  '下列是某地方政府勞工局處理一件勞資糾紛的部分過程：
勞工局：「 根據貴公司的員工出勤紀錄，員工確實常加班工作，依法雇主應
給付加班費。」
雇主：「 可是我又沒強迫員工留下來加班，有時候他們留在公司也不一定是
為了工作，只是下班後不想那麼早離開而已。」
勞工局：「 依照《勞動事件法》規定，出勤紀錄內記載的勞工出勤時間，都
預設勞工是經雇主同意而加班工作。若雇主認為員工並非因加班
工作而留在公司，則須由雇主提出證明。」
根據上述《勞動事件法》的規定判斷，下列何者最可能是當初立法時考量的
理由？',
  '[{"key": "A", "text": "消除職場上出現的性別歧視行為"}, {"key": "B", "text": "確保勞工可維持基本的生活水準"}, {"key": "C", "text": "禁止超時工作以保障童工的身心健康"}, {"key": "D", "text": "平衡勞資雙方之間權力不對等的關係"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  26,
  '圖(十二)是甲國在近三十年間，
三種已婚女性的勞動力參與率。
根據圖中資訊，可推論出該國社
會存在下列何種現象？
& 勞動 力參與率：15歲以上
民間人口中，已有工作者
及正在找工作者的比率。
圖(十二)',
  '[{"key": "A", "text": "家務勞動影響了女性參與市場勞動的機會"}, {"key": "B", "text": "外籍配偶增多影響了該國女性的工作機會"}, {"key": "C", "text": "家庭型態變遷使女性承擔較多的家務勞動"}, {"key": "D", "text": "女性投入家務勞動的總時數比市場勞動多"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  27,
  '土耳其扼黑海出入馬摩拉海的咽喉，因為原有
天然航道的航運交通量日益增加，政府計畫興
建圖(十三)中的新運河，該計畫除了引發國內
正反意見的討論外，也引起黑海周邊國家的高
度關注。上述運河完工後所帶來的影響最可能
為下列何者？',
  '[{"key": "A", "text": "土耳其將會喪失原有的「歐 亞陸橋」稱號"}, {"key": "B", "text": "土耳其的經濟海域範圍將因此而大幅增加"}, {"key": "C", "text": "黑海的海洋生物進入馬摩拉海的機率下降"}, {"key": "D", "text": "船隻等候通過博斯普魯斯海峽的時間減少"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  28,
  '圖(十四)中的國家積極發展某一種綠色能源。
根據圖中資訊判斷，下列何者最可能為該國所
發展的綠色能源及選擇的理由？',
  '[{"key": "A", "text": "水力；因雨量豐沛且山高水深，水力動能大"}, {"key": "B", "text": "太陽能；因位處太陽直射範圍，輻射強度大"}, {"key": "C", "text": "風力；因位於盛行西風帶，風力強勁且穩定"}, {"key": "D", "text": "海洋能；因北大西洋暖流流經，洋流動能大"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  29,
  '小綸從網站上取得2021年中國各省級行政區年降水量資料，他以當年全國平
均降水量691.6毫米作為標準，若省級行政區的年降水量低於此一數值，則在
該區塗上深灰色。根據上述原則，小綸繪製出的地圖最可能為下列何者？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  30,
  '碳匯是指能夠吸收及儲存含碳化合物的天然或人工「倉庫」，如森林、草
原、濕地、土壤、海洋等。為了達成2050年「碳中和」目標，各國除了減少
二氧化碳的排放之外，也積極擴大國家的碳匯。根據上文所述，若要增加一
國的碳匯，則下列何種方法最為適切？',
  '[{"key": "A", "text": "以焚林的方式，快速取得種植經濟作物的土地"}, {"key": "B", "text": "於屋頂上方設置太陽能發電板，增加電力供給"}, {"key": "C", "text": "恢復曾經消失的農地，採友善環境的耕作方式"}, {"key": "D", "text": "選用當地食材以減少運輸距離，降低食物里程"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  31,
  '莎綺去北大武山登山的時候，
看到山路上有一些歷史建築如
圖(十五) 所示。根據圖中碑文
摘譯的內容判斷，若莎綺上網
檢索這些歷史建築興建的時
局背景，最可能會出現下列
何者？',
  '[{"key": "A", "text": "強化皇民化運動的推展"}, {"key": "B", "text": "宣傳日 俄戰爭即將勝利"}, {"key": "C", "text": "實施開山撫番推動漢化"}, {"key": "D", "text": "發起原住民族正名運動"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  32,
  '理加頭目所屬部落與鄰近部落衝突頻繁，而荷蘭人未能妥善協助調停，心生不滿
的他在日本人勸說下，帶族人前往日本尋求援助。理加返鄉後，立即遭到荷蘭人
的監禁，進而引發日人挾持臺灣長官的衝突事件，更導致江戶幕府一度關閉荷蘭
在日本的商館以作為制裁。上述事件最可能發生於下列何時何地？',
  '[{"key": "A", "text": "十六世紀的澎湖"}, {"key": "B", "text": "十七世紀的大員"}, {"key": "C", "text": "十八世紀的淡水"}, {"key": "D", "text": "十九世紀的卑南"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  33,
  '表(四)是某一時期臺灣鳳梨罐 貿易
頭銷售至美國、日本、中國大 對象
甲 乙 丙 丁
陸及西德的官方統計數據。根 年分
據表中內容判斷，甲、乙、
1946 0 0 0 60,696
丙、丁何者最可能是中國大
1950 38,134 203 0 0
陸？
1955 182,000 33,836 153,963 0',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  35,
  '甲、乙二則資料呈現不同時代官方興建公共建設的相關情況：
甲資料： 統治者為了加強對國內各地的控制，便於運送物資及兵力，下令修
鑿運河，強行徵召數百萬人民從事勞役。
乙資料： 某地方政府研擬興建社會住宅，當地議會要求依法召開公聽會聽取
附近居民的意見，作為後續制定政策的參考。
根據甲、乙二項資料判斷，關於不同時代官方興建公共建設作法的敘述，
下列何者最適當？',
  '[{"key": "A", "text": "甲資料顯示當時的市場勞動權利受法律保障"}, {"key": "B", "text": "乙資料顯示當時的政府權力受到約束與制衡"}, {"key": "C", "text": "二則資料皆顯示公共建設以促進公平正義為主要考量"}, {"key": "D", "text": "二則資料皆顯示公共意見是經由大眾反覆討論而形成"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  36,
  '老師安排同學至地方法院參觀，並讓甲、
乙、丙、丁四位同學在模擬法庭中扮演不同
的角色，如圖(十七)所示。根據我國法律規
定及圖中情境判斷，下列關於他們四人的臺
詞，何者最適當？',
  '[{"key": "A", "text": "甲：我依據相關犯罪事證依法起訴乙"}, {"key": "B", "text": "乙：我承認錯誤，我會儘早償還借款"}, {"key": "C", "text": "丙：我希望甲審酌證據後判決乙無罪"}, {"key": "D", "text": "丁：我判決原告勝訴，撤銷行政處分"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  37,
  '「社會企業」是近年頗受關注的概念，其中公司型的社會企業透過商業活動營
利，以改善社會或環境問題為目標，並非以讓出資者獲利為唯一考量，而企業
獲得的利潤，也將繼續投入改善社會或環境問題的商業活動，希望讓社會企業
得以永續經營。下列何種作法與上述提及的企業經營模式最相符？',
  '[{"key": "A", "text": "運用低價策略創造企業優勢"}, {"key": "B", "text": "制定法律推行友善勞工政策"}, {"key": "C", "text": "提倡公平貿易幫助小農發展"}, {"key": "D", "text": "募集善心捐款扶助弱勢群體"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  38,
  '某日新聞報導有位失智症患者將土地、房屋贈送給陌生人的糾紛，由於小明
的爺爺是中度失智症患者，家人擔心爺爺也會做出類似行為而導致權益受
損，便向律師諮詢。律師建議家屬可向法院提出聲請，對爺爺作出監護宣
告。上述律師的建議內容應是希望達成下列何項法律效果？',
  '[{"key": "A", "text": "讓爺爺成為無行為能力人，以保障其財產"}, {"key": "B", "text": "讓爺爺成為限制行為能力人，以保障其財產"}, {"key": "C", "text": "讓爺爺成為無行為能力人，以保障其契約自由"}, {"key": "D", "text": "讓爺爺成為限制行為能力人，以保障其契約自由"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  39,
  '2020年之前，臺灣與日本都面臨勞力短缺的問題，但日本提供比臺灣更高的
薪資吸引國際移工，因此許多菲律賓籍移工較願意前往日本工作。不過2022
年底時，許多在日本工作的菲律賓籍移工發現，雖然每個月都拿出相同金額
的日幣兌換成菲律賓披索匯回家鄉，但年底換到的菲律賓披索卻比年初減少
了約10%，因此他們打算改往澳洲工作。上述國際移工變更工作地的考量，
其原因之一最可能為下列何者？',
  '[{"key": "A", "text": "菲律賓披索相對日幣升值"}, {"key": "B", "text": "菲律賓披索相對新臺幣貶值"}, {"key": "C", "text": "去臺灣工作的機會成本比去日本低"}, {"key": "D", "text": "去澳洲工作的機會成本比去日本高"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  40,
  '「俄 烏戰爭以來，歐盟對
俄羅斯採取大規模的制裁措
施，其中立陶宛於2022年6月
18日，對經其領土進出俄羅
斯 加里寧格勒的貨運火車實
施限制，因而引發俄羅斯強
烈不滿。此一事件也凸顯出
加里寧格勒的重要性。」圖
(十八)顯示加里寧格勒的位
置，根據上文及圖中資訊判
斷，其重要性可用下列何者
來說明？
圖(十八)',
  '[{"key": "A", "text": "作為俄羅斯與東北亞國家間的貿易前哨站"}, {"key": "B", "text": "為俄羅斯貨物經波羅的海出太平洋的港口"}, {"key": "C", "text": "位處俄羅斯天然氣輸送至芬蘭的最短路徑上"}, {"key": "D", "text": "是俄羅斯對抗北大西洋公約組織的軍事基地"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  41,
  '表(五)為三個不同日期臺灣部分水 表(五)
庫的蓄水量百分比，這些水庫在 蓄水量百分比 (%)
所在
2021年5月31日的蓄水量狀況，可 水庫名稱 2020年 2020年 2021年
行政區
能與下列何者關係最為密切？ 5月31日11月30日5月31日',
  '[{"key": "A", "text": "2021年梅雨鋒面提早報到 翡翠水庫 新北市 80.9 94.6 62.1"}, {"key": "B", "text": "2021年夏末對流雨較不旺盛 石門水庫 桃園市 67.4 49.7 12.5"}, {"key": "C", "text": "2020年冬季迎風面的地形雨偏少"}, {"key": "D", "text": "2020年缺乏颱風帶來的豐沛雨量"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  42,
  '某民意代表在服務處設立法律諮詢服務站，表(六) 表(六)
是2020年及2021年法律諮詢服務件數的統計資料， 時間
2020 2021
在2020年的刑事案件中，超過半數屬於告訴乃論， 類型 年 年
而2021年則有過半數的刑事案件屬於非告訴乃論。
民事事件 200 230
根據上述內容判斷，在2020年及2021年的諮詢服務
刑事案件 180 150
中，可採調解方式處理的件數可能為下列何者？
法律諮詢',
  '[{"key": "A", "text": "2020年70件，2021年100件 服務總數 380 380"}, {"key": "B", "text": "2020年100件，2021年70件"}, {"key": "C", "text": "2020年300件，2021年300件"}, {"key": "D", "text": "2020年330件，2021年330件"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  43,
  '下列何項展品，最可能屬於該博物館的主要館藏？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  44,
  '圖(十九)神官雕像手中所持的物品，最可能是下列何者？',
  '[{"key": "A", "text": "玉米"}, {"key": "B", "text": "橄欖"}, {"key": "C", "text": "小麥"}, {"key": "D", "text": "稻米"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  45,
  '文中博物館的展品說明，最可能以何種語文為主？',
  '[{"key": "A", "text": "英文"}, {"key": "B", "text": "法文"}, {"key": "C", "text": "葡萄牙文"}, {"key": "D", "text": "西班牙文"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  46,
  '多數國家使用0～9這十個數字作為車牌編碼的組合，但我國僅使用其中九個
數字。根據文中內容判斷，其原因最可能為下列何者？',
  '[{"key": "A", "text": "倫理價值具有約束力"}, {"key": "B", "text": "民間習俗具有強制力"}, {"key": "C", "text": "法律規定受宗教信仰影響"}, {"key": "D", "text": "政府施政受社會規範影響"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  47,
  '文中關於民眾選擇車牌號碼的敘述，最適合用來說明下列哪一觀點？',
  '[{"key": "A", "text": "廠商之間的價格競爭將使消費者受惠"}, {"key": "B", "text": "市場的競爭程度越高對消費者越有利"}, {"key": "C", "text": "負向誘因促使民眾的行為發生改變"}, {"key": "D", "text": "不同人對同一誘因的感受有所不同"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  48,
  '某民眾的車牌被別人惡意拔走，導致他違反文末所述的規定而受罰。若該民
眾對此處罰不服，依法採行下列何種處理方式最適當？',
  '[{"key": "A", "text": "向中央立法機關提出訴願"}, {"key": "B", "text": "向地方行政機關提出請願"}, {"key": "C", "text": "透過行政救濟途徑維護權益"}, {"key": "D", "text": "透過刑事訴訟途徑維護權益"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  49,
  '巴斯人的宗教信仰，最可能是下列何者？',
  '[{"key": "A", "text": "祆教"}, {"key": "B", "text": "佛教"}, {"key": "C", "text": "猶太教"}, {"key": "D", "text": "基督教"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  50,
  '十九世紀上半葉，巴斯人與中國商人的主要貿易模式，最可能是下列何者？',
  '[{"key": "A", "text": "巴斯人賣瓷器到中國以換取茶葉"}, {"key": "B", "text": "巴斯人賣鴉片到中國以取得白銀"}, {"key": "C", "text": "巴斯人賣鹿皮到中國以獲得棉花"}, {"key": "D", "text": "巴斯人賣茶葉到中國以交換工業品"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  51,
  '關於圖(二十)墓碑文字的解讀，下列何者最適當？',
  '[{"key": "A", "text": "當時類似的巴斯墓葬，多集中於今日山東 青島一帶"}, {"key": "B", "text": "根據時間可確認，此人於《南京條約》簽訂前來華"}, {"key": "C", "text": "此人為孟買出身，顯示其生前主要與日本商行合作"}, {"key": "D", "text": "碑刻的紀年方式，反映巴斯人珍視薩珊王朝的歷史"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  52,
  '根據圖(二十一)中的資訊判斷，與英國產生領土紛爭的國家應為下列何者？',
  '[{"key": "A", "text": "南非"}, {"key": "B", "text": "澳洲"}, {"key": "C", "text": "阿根廷"}, {"key": "D", "text": "紐西蘭"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  53,
  '依據上文及圖(二十一)中的資訊判斷，該冰山漂流的方向應為下列何者？',
  '[{"key": "A", "text": "東北向西南"}, {"key": "B", "text": "西南向東北"}, {"key": "C", "text": "東南向西北"}, {"key": "D", "text": "西北向東南"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'social',
  54,
  '上述冰山若撞上南喬治亞島，其產生的影響最可能為下列何者？',
  '[{"key": "A", "text": "巨浪侵襲島嶼陸地，阻礙工業發展"}, {"key": "B", "text": "附近海水鹽度上升，改變海洋生態"}, {"key": "C", "text": "威脅北美洲與非洲之間的船隻安全"}, {"key": "D", "text": "島嶼海岸遭受破壞，危及動物棲地"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  1,
  '孕婦產檢時常使用超聲波來檢查腹中胎兒的生長情形，當醫生使用超聲波進行
檢查時，孕婦對超聲波的聽覺感受，下列說明何者最合理？',
  '[{"key": "A", "text": "孕婦會聽見低沉的轟隆聲"}, {"key": "B", "text": "孕婦會聽見尖銳刺耳的聲音"}, {"key": "C", "text": "因頻率過高，故孕婦聽不見超聲波"}, {"key": "D", "text": "因波速過快，故孕婦聽不見超聲波"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  2,
  '小陞想以圖(一)中的裝置或器材，測量一顆形狀不規則小石頭的密度，他應選
擇哪兩項來測量？
50mL
50
40
30 8
910
7
6
20 4 5
3
10 1 2
0
圖(一)',
  '[{"key": "A", "text": "甲與丁"}, {"key": "B", "text": "甲與丙"}, {"key": "C", "text": "乙與丁"}, {"key": "D", "text": "乙與丙"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  3,
  '有報導指出：「在都市觀察到麻雀的頻率有變少的趨勢，可能的原因很多，其
中之一為白尾八哥的入侵。白尾八哥築巢偏好的位置與麻雀相近，食物種類也
相似，甚至被觀察到會以麻雀幼鳥為食。」根據上述報導，白尾八哥與麻雀之
間最符合下列哪兩種交互作用？',
  '[{"key": "A", "text": "競爭、掠食"}, {"key": "B", "text": "競爭、共生"}, {"key": "C", "text": "共生、掠食"}, {"key": "D", "text": "寄生、掠食"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  4,
  '小志將物質分成元素、化合物和混合物三類，並舉例如表(一)。表中各例子所
含原子種類多寡的比較，下列何者正確？
表(一)',
  '[{"key": "A", "text": "笑氣＞硫磺"}, {"key": "B", "text": "硫磺＞笑氣"}, {"key": "C", "text": "硫磺＞花岡岩"}, {"key": "D", "text": "三個例子都一樣多"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  5,
  '圖(二)為一鋒面的剖面示意圖，黑色曲線表示鋒面，兩側分別為甲、乙空氣，箭頭
為空氣沿著鋒面上升的方向，並呈現鋒面附近的雲雨分布情形。關於此鋒面兩側
甲、乙空氣的性質比較，下列何者最合理？',
  '[{"key": "A", "text": "甲、乙皆為暖空氣"}, {"key": "B", "text": "甲、乙皆為冷空氣"}, {"key": "C", "text": "甲為暖空氣、乙為冷空氣"}, {"key": "D", "text": "甲為冷空氣、乙為暖空氣"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  6,
  '臺灣地下水資源豐富，許多地區都有取用地下水，若使用不當則可能造成
災害。小盈想在簡報中說明過度抽取地下水所造成的影響，則下列照片及其
說明何者最適合？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  7,
  '端午節有「立蛋」的習俗，網路上有民眾說只有在端午節
正午時，生雞蛋才可立得起來。如圖(三)，該說法的論點是
「端午節時太陽直射北半球，臺灣正好在北半球，因此只有
在端午節正午時，太陽對生雞蛋的引力與地球對生雞蛋的
引力會恰好相反，兩力相互拉扯才使得生雞蛋能夠直立。」
下列四種實驗設計及結果，何者最適合拿來反駁上述說法？',
  '[{"key": "A", "text": "將生雞蛋煮熟後剝殼，改於聖誕節正午時在臺灣成功立蛋"}, {"key": "B", "text": "使用同一種的生雞蛋，改於聖誕節正午時在臺灣成功立蛋"}, {"key": "C", "text": "把生雞蛋換成生鴨蛋，並於端午節正午時在臺灣成功立蛋"}, {"key": "D", "text": "另拿不同種的生雞蛋，並於端午節正午時在臺灣成功立蛋"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  8,
  '圖(四)為某蘆筍植株的示意圖，圖中甲部位經過日光照射，呈現
綠色；乙部位未受到日光照射，呈現白色。有關兩部位進行生理
作用時所釋出的氣體，下列敘述何者最合理？',
  '[{"key": "A", "text": "甲能釋出O ，但乙不能"}, {"key": "B", "text": "甲能釋出CO ，但乙不能"}, {"key": "C", "text": "乙能釋出O ，但甲不能"}, {"key": "D", "text": "乙能釋出CO ，但甲不能"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  9,
  '將一支未削尖的鉛筆置於桌面，鉛筆右端為軟質橡皮，左端為硬質木頭，在其
兩端分別以手指施水平力，且兩力作用於同一直線上，施力後保持靜止平衡，
如圖(五)。其中手指施於鉛筆左、右兩端力的大小分別為F 、F ，鉛筆施於
左 右
左、右兩端手指的反作用力大小分別為F′、F′。已知F 為1 N，若不考慮鉛筆
左 右 左
與桌面間的摩擦力，則下列關係何者正確？',
  '[{"key": "A", "text": "F′ ＜F ＜1 N"}, {"key": "B", "text": "F′ ＜F ＝1 N"}, {"key": "C", "text": "F′ ＝F ＜1 N"}, {"key": "D", "text": "F′ ＝F ＝1 N"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  10,
  '如圖(六)，甲、乙、丙三個金屬球，甲球帶負電，乙、丙兩球帶正電，剛開始乙球
距離甲球 2 m，距離丙球1 m，之後將乙球向左移動1 m，使乙球距離甲球
1 m，距離丙球 2 m。若甲、乙間的靜電力大小為 F ，乙、丙間的靜電力大小
甲乙
為 F ，則移動前後，有關 F 、F 的大小變化，下列何者正確？
乙丙 甲乙 乙丙',
  '[{"key": "A", "text": "F 變大，F 變大"}, {"key": "B", "text": "F 變大，F 變小"}, {"key": "C", "text": "F 變小，F 變大"}, {"key": "D", "text": "F 變小，F 變小"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  11,
  '某電玩公司為了防止兒童誤吞遊戲主機的遊戲卡，因而在遊戲卡塗上苯甲
地那銨。苯甲地那銨是非常苦的物質，其濃度只要達到______，也就是每1000 g
的溶液中含有30 mg的苯甲地那銨，便會苦到讓人難以忍受。上述空格最適合
填入下列何者？',
  '[{"key": "A", "text": "30%"}, {"key": "B", "text": "30 mg"}, {"key": "C", "text": "30 ppm"}, {"key": "D", "text": "30 g/cm3"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  13,
  '房產專家建議，若可以選擇，住在臺北的居民，其陽臺面對的方向盡量不要
朝向北邊、東北邊。因為冬天的時候容易下雨，且陽臺面對的方向易有強風，
雨水會直接打向陽臺，容易使晾晒的衣物淋溼。專家的這個建議是否適用於
其他地區？',
  '[{"key": "A", "text": "適用於臺南，因為冬天時位處季風迎風面的臺南氣候偏溼"}, {"key": "B", "text": "適用於基隆，因為冬天時位處季風背風面的基隆氣候偏溼"}, {"key": "C", "text": "不適用於宜蘭，因為冬天時位處季風迎風面的宜蘭氣候偏乾"}, {"key": "D", "text": "不適用於高雄，因為冬天時位處季風背風面的高雄氣候偏乾"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  14,
  '有三顆小球，在紅光照射下，觀察到小球分別呈現紅色、紅色、黑色，關於這
三顆小球在白光照射下所呈現顏色的推論，下列何者最合理？',
  '[{"key": "A", "text": "至少有一顆紅球"}, {"key": "B", "text": "至少有一顆黑球"}, {"key": "C", "text": "最多有兩顆白球"}, {"key": "D", "text": "最多有兩顆綠球"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  17,
  '已知Ca和Cl的原子序分別為20、17，Ca2+和Cl 的質子數和電子數如表(三)，
表中w、x、y、z的數值大小比較，下列何者正確？',
  '[{"key": "A", "text": "w＞z"}, {"key": "B", "text": "x＞y"}, {"key": "C", "text": "x＞z"}, {"key": "D", "text": "y＞w"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  18,
  '一個質量2 kg的長方體木塊靜置於水平
桌面上，若對木塊施一水平向東的
外力F，其摩擦力(f)與外力(F)的關係圖
如圖(九)。根據此圖判斷下列敘述何者
正確？',
  '[{"key": "A", "text": "最大靜摩擦力為300 gw"}, {"key": "B", "text": "外力F由0增加至300 gw時，木塊即開始向東運動"}, {"key": "C", "text": "若外力F小於400 gw時，則外力F越小，靜摩擦力也越小"}, {"key": "D", "text": "若外力F大於400 gw時，則外力F越大，動摩擦力也越大"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  19,
  '為為了了減減少少溫溫室室氣氣體體，，地地質質學學家家將將二二氧氧化化碳碳變變成成岩岩石石的的一一部部分分
將發電廠產生的二氧化碳灌入大量的水中，以管線將這些氣泡水輸送到
數公里遠的區域，接著透過高壓將氣泡水注入地下一千公尺深的岩層中，這
些氣泡水會和鈣、鎂等離子反應而「固化」，並填充岩層空隙。二氧化碳一
旦固化後，就能存在岩層中。
上述二氧化碳變成岩石一部分的過程，是利用下列二氧化碳(水溶液)的何種性質？',
  '[{"key": "A", "text": "密度大於空氣"}, {"key": "B", "text": "溶於水呈酸性"}, {"key": "C", "text": "可與鈣離子反應產生難溶於水的碳酸鹽"}, {"key": "D", "text": "可與鈉離子反應產生易溶於水的碳酸鹽"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  20,
  '一群健康成人吃了等量的食物甲或乙後，平均血糖濃度的變化如圖(十)。已
知健康成人空腹平均血糖濃度約為90 mg/dL，根據此圖推論，下列何者最合
理？',
  '[{"key": "A", "text": "進食後，甲比乙更早導致升糖素分泌量增加"}, {"key": "B", "text": "進食後，甲比乙更早導致胰島素分泌量增加"}, {"key": "C", "text": "進食後，乙比甲更早導致升糖素分泌量增加"}, {"key": "D", "text": "進食後，乙比甲更早導致胰島素分泌量增加"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  21,
  '購買高濃度的酒精，可自行稀釋及分裝成消毒用酒精，但並非所有的塑膠容器
都適合盛裝高濃度酒精，有些會被乙醇溶解或腐蝕而使容器變輕。下列研究將
三種為熱塑性聚合物材質的容器，分別在50℃和70℃的溫度下，浸入高濃度的
酒精中，容器的質量變化率如圖(十一)：
圖(十一)
僅依據上述資訊，下列說明何者最合理？',
  '[{"key": "A", "text": "三種材質中，PET最適合盛裝高濃度酒精"}, {"key": "B", "text": "在兩種溫度下，PP都是最不適合盛裝高濃度酒精"}, {"key": "C", "text": "鏈狀聚合物的材質比網狀聚合物更適合盛裝高濃度酒精"}, {"key": "D", "text": "與50℃相比，三種材質皆是在70℃的條件下容器耗損率較高"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  22,
  '圖(十二)為某植物的莖部剖面示意圖。若想利用某儀器探測其蒸散作用的
速率，關於實驗所需探測的圖中部位及對應理由，下列何者最合理？',
  '[{"key": "A", "text": "甲，因為它是運輸水分的部位"}, {"key": "B", "text": "甲，因為它是運輸有機養分的部位"}, {"key": "C", "text": "乙，因為它是運輸水分的部位"}, {"key": "D", "text": "乙，因為它是運輸有機養分的部位"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  23,
  '下列選項為四種在海面上的等壓線分布圖，已知各圖中涵蓋的空間範圍皆相同，
數值代表該等壓線的氣壓，單位為百帕。根據等壓線上的數值推論，下列
哪張圖中的甲處風速最大？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  24,
  '表(四)為部分鳥類資料，推論表中所有 表(四)
鳥類在分類上的敘述，何者是可能的？',
  '[{"key": "A", "text": "最多包含3個目、4個屬"}, {"key": "B", "text": "最多包含3個目、6個屬"}, {"key": "C", "text": "最多包含4個目、4個屬"}, {"key": "D", "text": "最多包含4個目、6個屬"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  25,
  '下列實驗探討鋅銅電池電極的面積大小對於電池電壓與電流的影響：
實驗器材：大電極(3.0 cm×8.0 cm)：大銅片、大鋅片各兩片
小電極(1.0 cm×8.0 cm)：小銅片、小鋅片各兩片
除了電極面積不同，其餘實驗條件皆相同，並以三用電表檢測電壓與電流，結果
如表(五)：
表(五)
關於此實驗的說明，下列何者合理？',
  '[{"key": "A", "text": "電極面積不同對於電功率變化的影響，負極大於正極"}, {"key": "B", "text": "電極面積不同對於電功率變化的影響，正極大於負極"}, {"key": "C", "text": "正極面積相同，負極面積不同，對於電壓值變化比例的影響大於電流值"}, {"key": "D", "text": "負極面積相同，正極面積不同，對於電壓值變化比例的影響大於電流值"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  26,
  '阿偉想要藉由實驗比較鋁和銅的比熱大小關係，若加熱條件相同，且忽略熱量
散失，則下列四種方式，哪一種最合理？',
  '[{"key": "A", "text": "分別加熱相同體積的鋁和銅，先開始熔化者比熱較小"}, {"key": "B", "text": "分別加熱相同體積的鋁和銅，溫度上升較快者比熱較小"}, {"key": "C", "text": "分別加熱相同質量的鋁和銅，先開始熔化者比熱較小"}, {"key": "D", "text": "分別加熱相同質量的鋁和銅，溫度上升較快者比熱較小"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  28,
  '有些物質可使棕色的碘液進行還原反應，反應後溶液呈無色，例如許多水果所
含有的維生素C。圖(十四)以維生素C和綠茶茶水分別進行實驗：
圖(十四)
僅依據本實驗結果，下列推論何者最合理？',
  '[{"key": "A", "text": "綠茶茶水中必定含有維生素C"}, {"key": "B", "text": "綠茶茶水中必定含有能被氧化的物質"}, {"key": "C", "text": "綠茶茶水進行氧化反應，維生素C進行還原反應"}, {"key": "D", "text": "因實驗結果溶液顏色改變，故綠茶茶水可做為酸鹼指示劑"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  29,
  '甲、乙、丙三個相同的試管中，分別裝有密度不同的X、Y兩種液體，兩種液體
不發生化學反應且互不相溶，所占體積及靜止平衡時的狀態如圖(十五)。若裝有
液體的甲、乙、丙三試管，其總質量分別為m 、m 、m ，則下列關係何者正
甲 乙 丙
確？',
  '[{"key": "A", "text": "m ＝m ＝m"}, {"key": "B", "text": "m ＞m ＞m"}, {"key": "C", "text": "m ＞m ＞m"}, {"key": "D", "text": "m ＞m ＞m"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  30,
  '假設孔雀魚的黑眼睛及紅眼睛由一對遺傳因子所控制，遺傳因子有顯性A與隱
性a兩種。將甲、乙兩隻黑眼睛孔雀魚交配，所生下的眾多子代有黑眼睛
及紅眼睛兩種，其中任意選擇兩隻黑眼睛的子代標記為丙、丁，此過程
如圖(十六)。在不考慮突變的情況下，推測甲、乙、丙、丁中，哪兩隻控制
眼睛顏色性狀的基因型一定相同？',
  '[{"key": "A", "text": "甲、乙"}, {"key": "B", "text": "甲、丙"}, {"key": "C", "text": "乙、丁"}, {"key": "D", "text": "丙、丁"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  31,
  '圖(十七)為甲、乙兩組電流磁效應實驗，兩組實驗所用材料相同，乙組較甲組
多連接一顆電池，銅線的擺放方向均為南北向。已知下列選項中磁針黑色部分
為N極，則甲、乙兩組實驗中磁針的偏轉方向，哪一組最合理？
圖(十七)',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  32,
  '在適當的條件下，H S和SO 會發生反應， 表(六)
2 2
生成H O和S。小如記錄某一反應裝置內
2
反應前、反應後各物質的質量，如表(六)。
下列何組數據最可能是上述反應後各物質
的質量？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  33,
  '如圖(十八)，地質鑽探是以鑽頭從地表垂直向下挖掘，
取得岩石樣本進行分析，如果有斷層通過某處的地下，便
可藉由地質鑽探了解斷層的特性。某次地震後，斷層破裂
至地表，其震央與地表上斷層的位置如圖(十九)，甲、乙
為斷層附近兩處可供地質鑽探使用的土地，若想進行鑽探
圖(十八)
並鑽至斷層面，下列選擇方式何者最能達到目的？',
  '[{"key": "A", "text": "若斷層為正斷層選甲處，若斷層為逆斷層則選乙處"}, {"key": "B", "text": "若斷層為逆斷層選甲處，若斷層為正斷層則選乙處"}, {"key": "C", "text": "無論是正斷層或逆斷層，皆選擇與震央不同側的甲處"}, {"key": "D", "text": "無論是正斷層或逆斷層，皆選擇與震央相同側的乙處"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  34,
  '甲、乙兩種生物的比較如表(七)。關於甲、乙所屬的分類，
依序為下列何者？',
  '[{"key": "A", "text": "原生生物界、真菌界"}, {"key": "B", "text": "原生生物界、植物界"}, {"key": "C", "text": "真菌界、原生生物界"}, {"key": "D", "text": "真菌界、原核生物界"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  35,
  '圖(二十)為細胞進行甲、乙兩種不同分裂方式的染色體
變化示意圖。若比較「以葉片繁殖出幼苗」及「以
種子萌芽成幼苗」的過程中發生的分裂方式，下列
敘述何者最合理？',
  '[{"key": "A", "text": "兩者皆進行甲"}, {"key": "B", "text": "兩者皆進行乙"}, {"key": "C", "text": "以葉片繁殖的進行甲，以種子萌芽的進行乙"}, {"key": "D", "text": "以葉片繁殖的進行乙，以種子萌芽的進行甲"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  36,
  '有甲、乙、丙三杯濃度相同的澱粉液，分別加入經不同條件 表(八)
處理的等量澱粉酶，經相同的作用時間後，以碘液與本氏液
分別檢測此三杯溶液，結果如表(八)。根據此結果推測，
哪杯澱粉液加入的澱粉酶應已完全失去作用？',
  '[{"key": "A", "text": "僅甲"}, {"key": "B", "text": "僅乙"}, {"key": "C", "text": "甲和丙"}, {"key": "D", "text": "乙和丙"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  37,
  '圖(二十一)為距離太陽最近的五顆行星其公轉軌道示意圖(未依實際距離及大小
繪製)，假設這五顆行星與太陽皆位於同一平面上，有關星體的排列方式，下列
敘述何者最合理？
圖(二十一)',
  '[{"key": "A", "text": "若地球、金星、水星呈一直線，地球可能位於金星與水星之間"}, {"key": "B", "text": "若太陽、地球、火星呈一直線，太陽可能位於地球與火星之間"}, {"key": "C", "text": "若金星、太陽、水星呈一直線，太陽不可能位於金星與水星之間"}, {"key": "D", "text": "若火星、地球、木星呈一直線，地球不可能位於火星與木星之間"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  40,
  '在燒瓶中裝水並加熱到沸騰後，停止加熱，塞住
瓶口，翻轉倒置燒瓶，使瓶內的空氣位於上方，
如圖(二十三)。此時拿一袋冰塊放在燒瓶的上方，
瓶內的氣壓會改變，而水會由下而上開始冒出氣
泡，是一種物理變化，如圖(二十四)。根據上述說
明，關於冰塊降溫造成此現象的解釋，下列何者
最合理？
圖(二十三) 圖(二十四)',
  '[{"key": "A", "text": "瓶內的水蒸氣凝結，接著藉由水汽化達到新的平衡"}, {"key": "B", "text": "瓶內的水蒸氣蒸發，接著藉由水汽化達到新的平衡"}, {"key": "C", "text": "瓶內的氣壓降低，接著藉由水分解反應產生氣體達到新的平衡"}, {"key": "D", "text": "瓶內的氣壓升高，接著藉由水分解反應產生氣體達到新的平衡"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  41,
  '圖(二十五)為一篇介紹零碳排放飛機文章中出現的燃料資訊圖，圖中顯示單位
質量與單位體積的燃料燃燒所產生的能量之比較。以產生相同的能量為前提，
與其他燃料比較，液化氫具有下列何種特點？',
  '[{"key": "A", "text": "液化氫會較重，但占用的空間小"}, {"key": "B", "text": "液化氫會較重，且占用的空間大"}, {"key": "C", "text": "液化氫會較輕，且占用的空間小"}, {"key": "D", "text": "液化氫會較輕，但占用的空間大"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  42,
  '瑞典學生拍攝影片表達節能的重要性，影片中請來奧運自行車選手踩單車
發電烤吐司，最終選手踩到精疲力竭，才烤好一片吐司，如圖(二十六)，過程
中發電的平均電功率約700 W，總共產生的電能約0.021 kWh。若以一度電3元
計算，上述過程產生的電能，其對應的電費應如何計算？',
  '[{"key": "A", "text": "700 ×3元  kWh亦寫作kW．h"}, {"key": "B", "text": "0.021×3元"}, {"key": "C", "text": "×3元"}, {"key": "D", "text": "×3元"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  43,
  '根據實驗結果，關於不同溫度對蒜頭變綠色的影響，下列說明何者最合理？',
  '[{"key": "A", "text": "全程在10℃，變色的速率最快"}, {"key": "B", "text": "全程在25℃，變色的速率最快"}, {"key": "C", "text": "先低溫處理，接著改在25℃放置會減緩變色的速率"}, {"key": "D", "text": "先低溫處理，接著改在25℃放置會加快變色的速率"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  44,
  '僅根據實驗三的結果，推測使蒜頭變綠色的有利環境，最可能是下列何者？',
  '[{"key": "A", "text": "酸性越弱的環境"}, {"key": "B", "text": "酸性越強的環境"}, {"key": "C", "text": "有– COOH原子團的環境"}, {"key": "D", "text": "沒有– COOH原子團的環境"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  45,
  '僅根據小花檢測的初步結果，下列推論何者最合理？',
  '[{"key": "A", "text": "出血時間過短，須進一步檢查"}, {"key": "B", "text": "出血時間於容許範圍內，可能無異常"}, {"key": "C", "text": "出血時間於容許範圍內，但可能罹患X減少症或其他凝血因子異常"}, {"key": "D", "text": "出血時間過長，可能罹患X減少症或其他凝血因子異常"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  46,
  '表中的X最可能為下列何者？',
  '[{"key": "A", "text": "淋巴"}, {"key": "B", "text": "白血球"}, {"key": "C", "text": "紅血球"}, {"key": "D", "text": "血小板"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  47,
  '阿貴在做砝碼質量為200 g的實驗時，他施一個鉛直向上的定力將彈簧秤以穩
定且緩慢的速度提高10 cm，並使砝碼上升5 cm，此過程彈簧秤拉力所作的功
為多少gw．cm？',
  '[{"key": "A", "text": "1000"}, {"key": "B", "text": "1500"}, {"key": "C", "text": "2000"}, {"key": "D", "text": "3000"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  48,
  '阿貴經多次重複同樣的實驗所得結果均與圖(二十九)相同，而圖中的三點連
線之延長線與縱軸F交點不是原點。若不考慮摩擦力，則關於交點不是原點的
原因，下列敘述何者最合理？',
  '[{"key": "A", "text": "此實驗的誤差很大"}, {"key": "B", "text": "此實驗裝置屬於費力的簡單機械"}, {"key": "C", "text": "阿貴所記錄彈簧秤讀數F，其數值同時受到彈簧秤質量及砝碼質量的影響"}, {"key": "D", "text": "阿貴所記錄彈簧秤讀數F，其數值同時受到動滑輪質量及砝碼質量的影響"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  49,
  '考量月球在甲、乙兩處的月相，下列俯視圖何者最可能是阿平進行模擬時，球
於兩處的亮暗面分布狀態？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'science',
  50,
  '根據圖(三十一)模擬的月球移動路徑，當月球由甲處移動至乙處的這段時間，
地球自轉或繞太陽公轉了幾圈？',
  '[{"key": "A", "text": "地球大約自轉了半圈"}, {"key": "B", "text": "地球大約自轉了15圈"}, {"key": "C", "text": "地球繞太陽大約公轉了半圈"}, {"key": "D", "text": "地球繞太陽大約公轉了15圈"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  1,
  'Look at the picture. A is flying over the houses.',
  '[{"key": "A", "text": "bird"}, {"key": "B", "text": "butterfly"}, {"key": "C", "text": "kite"}, {"key": "D", "text": "plane"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  2,
  'When I was a teenager, I was very . But now, it’s easier for me to talk to people.',
  '[{"key": "A", "text": "happy"}, {"key": "B", "text": "lazy"}, {"key": "C", "text": "popular"}, {"key": "D", "text": "shy"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  3,
  'Lena doesn’t want to go with John because she is afraid of water.',
  '[{"key": "A", "text": "dancing"}, {"key": "B", "text": "hiking"}, {"key": "C", "text": "sailing"}, {"key": "D", "text": "shopping"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  4,
  'Cindy enjoys her dad read stories to her before bed.',
  '[{"key": "A", "text": "to listen to"}, {"key": "B", "text": "listening to"}, {"key": "C", "text": "listen to"}, {"key": "D", "text": "listens to"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  5,
  'Dad is busy cooking in the kitchen. Dinner will be in ten minutes.',
  '[{"key": "A", "text": "free"}, {"key": "B", "text": "full"}, {"key": "C", "text": "medium"}, {"key": "D", "text": "ready"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  6,
  'There are so many new in the office. It’ll take me some time to remember who is
who.',
  '[{"key": "A", "text": "faces"}, {"key": "B", "text": "ideas"}, {"key": "C", "text": "rules"}, {"key": "D", "text": "tools"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  7,
  'I feel like a . I was looking for my keys for hours but they have been in my pocket
the whole time.',
  '[{"key": "A", "text": "fool"}, {"key": "B", "text": "ghost"}, {"key": "C", "text": "king"}, {"key": "D", "text": "stranger"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  8,
  'Mr. and Mrs. Wu have three daughters. Two are in high school, and is in
elementary school.',
  '[{"key": "A", "text": "each"}, {"key": "B", "text": "the other"}, {"key": "C", "text": "the one"}, {"key": "D", "text": "the next"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  9,
  'It is hard for trees to along this beach because of the strong winds from the sea.',
  '[{"key": "A", "text": "blow"}, {"key": "B", "text": "build"}, {"key": "C", "text": "follow"}, {"key": "D", "text": "grow"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  10,
  'Christmas and I want to visit my aunt abroad. Do you have any plans yet?',
  '[{"key": "A", "text": "came"}, {"key": "B", "text": "comes"}, {"key": "C", "text": "is coming"}, {"key": "D", "text": "was coming"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  11,
  'Jo won’t be happy if you’re late for his party tonight, so sure that you arrive on time.',
  '[{"key": "A", "text": "make"}, {"key": "B", "text": "makes"}, {"key": "C", "text": "to make"}, {"key": "D", "text": "is making"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  12,
  'You may have a long drive because of the terrible . There are usually a lot of cars
and buses during this time.',
  '[{"key": "A", "text": "experience"}, {"key": "B", "text": "machine"}, {"key": "C", "text": "service"}, {"key": "D", "text": "traffic"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  13,
  'In the future, there will be greater basketball players than Stephen Curry, but now
we believe he is the best!',
  '[{"key": "A", "text": "again"}, {"key": "B", "text": "already"}, {"key": "C", "text": "never"}, {"key": "D", "text": "perhaps"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  14,
  'I guess the rainwater has come in from the kitchen. See? of the windows are closed
except the one in the kitchen.',
  '[{"key": "A", "text": "All"}, {"key": "B", "text": "Both"}, {"key": "C", "text": "Most"}, {"key": "D", "text": "Some"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  15,
  'machines have been used to pick fruits for a long time, they were not used on
strawberry farms until several years ago.',
  '[{"key": "A", "text": "Although"}, {"key": "B", "text": "Because"}, {"key": "C", "text": "Before"}, {"key": "D", "text": "If"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  16,
  'There are online videos that teach you exercises you can do at home. They’ll you a
trip to the gym, and some money too.',
  '[{"key": "A", "text": "cost"}, {"key": "B", "text": "give"}, {"key": "C", "text": "keep"}, {"key": "D", "text": "save"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  17,
  'Jane’s parents are always happy to see their grandchildren, but mine less so when I
visit them with my kids.',
  '[{"key": "A", "text": "is"}, {"key": "B", "text": "are"}, {"key": "C", "text": "do"}, {"key": "D", "text": "does"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  18,
  'Before she about it, you should tell Daphne you broke her favorite cup.',
  '[{"key": "A", "text": "asks"}, {"key": "B", "text": "asked"}, {"key": "C", "text": "was asking"}, {"key": "D", "text": "will ask"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  19,
  'It was very windy this morning. Some of the shirts on the balcony were blown away
in the pond.',
  '[{"key": "A", "text": "fell"}, {"key": "B", "text": "and fell"}, {"key": "C", "text": "fallen"}, {"key": "D", "text": "and fallen"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  20,
  'What happened to Rex?',
  '[{"key": "A", "text": "He got lost."}, {"key": "B", "text": "He got hurt."}, {"key": "C", "text": "He bit people."}, {"key": "D", "text": "He ate too much."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  21,
  'How did the writer help Rex?',
  '[{"key": "A", "text": "By calling the police."}, {"key": "B", "text": "By making him exercise."}, {"key": "C", "text": "By taking him to see a doctor."}, {"key": "D", "text": "By looking for a new home for him."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  22,
  'What do we know about Mark from the dialogue?',
  '[{"key": "A", "text": "He made Linda unhappy."}, {"key": "B", "text": "He is looking for a new job."}, {"key": "C", "text": "He did not like Linda’s cake."}, {"key": "D", "text": "He is getting married to Jenny."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  23,
  'Which is most likely an example of stealing someone＇s thunder?  likely 可能',
  '[{"key": "A", "text": "Dennis never changes his mind except when his wife tells him to."}, {"key": "B", "text": "Melisa tells Tom she’ll go to the party but tells her mom she’ll stay home."}, {"key": "C", "text": "Jeff tells everyone he’ll move abroad when Ivy is still telling them about her baby."}, {"key": "D", "text": "Alisa says she doesn’t care what we have for lunch but also doesn’t like the restaurant"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  24,
  'What can you do with a White Lake City Card?',
  '[{"key": "A", "text": "Save 20% on children’s train tickets."}, {"key": "B", "text": "Visit any public museum in the city for free."}, {"key": "C", "text": "Take a train to places out of the three zones."}, {"key": "D", "text": "Move around the city by metro as much as you want."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  25,
  'Stacy is going to White Lake City and is staying at a hotel near the White Lake Main
Station. She wants to visit the Museum of White Lake City History on Friday and see
White Lake on Saturday. If she plans to buy (a) White Lake City Card(s), which of the four
choices will be best for her and cost her the least?',
  '[{"key": "A", "text": "A 3-day Card for Zone 1."}, {"key": "B", "text": "A Weekend Card for Zones 1-3."}, {"key": "C", "text": "A 1-day Card for Zone 1 and a Weekend Card for Zones 1-2."}, {"key": "D", "text": "A 1-day Card for Zones 1-2 and a Weekend Card for Zones 1-2."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  26,
  'What is Rolling Acres?',
  '[{"key": "A", "text": "A zoo."}, {"key": "B", "text": "A campground."}, {"key": "C", "text": "A vacation farm."}, {"key": "D", "text": "A family restaurant."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  27,
  'What do we learn from the first paragraph?  paragraph 段落',
  '[{"key": "A", "text": "What Libby does at Rolling Acres."}, {"key": "B", "text": "What visitors think of Rolling Acres."}, {"key": "C", "text": "Why Libby’s grandparents started Rolling Acres."}, {"key": "D", "text": "What the Larson family’s plans are for Rolling Acres."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  28,
  'What does making sacrifices mean?',
  '[{"key": "A", "text": "Learning to make money and use it wisely."}, {"key": "B", "text": "Getting to know different sides of your family."}, {"key": "C", "text": "Making excuses for failing to do something difficult."}, {"key": "D", "text": "Giving up something important to do something else."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  29,
  'What do the comics tell us?',
  '[{"key": "A", "text": "Enjoy life while we can."}, {"key": "B", "text": "Follow the old ways of life."}, {"key": "C", "text": "Save our planet before it’s too late."}, {"key": "D", "text": "Treat others the way we want to be treated."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  30,
  'What can we learn about the people in the comics?',
  '[{"key": "A", "text": "They made fire before starting a fight."}, {"key": "B", "text": "They fought for land and plants all the time."}, {"key": "C", "text": "They prayed to the statues beside a large fire."}, {"key": "D", "text": "They used statues to show how strong they were."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  31,
  'What does did it in Picture 7 mean?',
  '[{"key": "A", "text": "Fall to the ground."}, {"key": "B", "text": "Cut down the last trees."}, {"key": "C", "text": "Move the statues to fighting grounds."}, {"key": "D", "text": "Understand how important trees were."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  32,
  'What did Ariely try to find out in the origami study?',
  '[{"key": "A", "text": "If he could stop the IKEA effect."}, {"key": "B", "text": "Why people love making origami."}, {"key": "C", "text": "Why IKEA furniture is so famous."}, {"key": "D", "text": "If anyone shared his IKEA experience."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  33,
  'Which is true about the origami study?',
  '[{"key": "A", "text": "Buyers would spend less on builders’ origami than builders would."}, {"key": "B", "text": "Builders and buyers needed to decide a price on the origami they made."}, {"key": "C", "text": "Builders knew others would not pay as much for the origami as they would."}, {"key": "D", "text": "Buyers would spend more on builders’ origami after knowing how they were made."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  34,
  'Jerry just can’t get his daughter Mia to eat more vegetables at dinner. Every time he tries
to do so, there is always a lot of shouting and crying. If Jerry wants to have Mia eat more
vegetables by using the IKEA effect, what should he do?',
  '[{"key": "A", "text": "Tell Mia that he cooks the vegetables just for her."}, {"key": "B", "text": "Ask Mia to help him cook vegetables for her meal."}, {"key": "C", "text": "Give Mia her favorite candy after she eats vegetables."}, {"key": "D", "text": "Ask Mia what vegetables she likes and cook them for her."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  35,
  'What is the reading mainly about?',
  '[{"key": "A", "text": "The tips on using a picture to tell a story."}, {"key": "B", "text": "The change that electricity brought to people’s lives."}, {"key": "C", "text": "The history behind the picture of a UK electricity worker."}, {"key": "D", "text": "The story of a famous UK electricity worker from the 1970s."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  36,
  'In the UK in the 1970s, what did people most likely think of the UK electricity workers?',
  '[{"key": "A", "text": "They were not brave enough to fix their problems."}, {"key": "B", "text": "They worked like robots and never learned to change."}, {"key": "C", "text": "They were asking too much and did not know when to stop."}, {"key": "D", "text": "They did not care whether their job might hurt people’s health."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  37,
  'Why does the writer put the “ ” mark around the word dark in the last sentence?',
  '[{"key": "A", "text": "To say that the “dark” time was actually not dark."}, {"key": "B", "text": "To tell people that the word was said by the government."}, {"key": "C", "text": "To mean both the days without lights and the difficult lives people lived."}, {"key": "D", "text": "To show that the government and the electricity workers both lost their fights."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  38,
  '(A) starts (B) started (C) has started (D) will start',
  '[{"key": "A", "text": "starts"}, {"key": "B", "text": "started"}, {"key": "C", "text": "has started"}, {"key": "D", "text": "will start"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  39,
  '(A) he got quite scared of two things
(B) he still couldn’t understand two things
(C) he couldn’t stop thinking about two things
(D) he did two things that would change his life',
  '[{"key": "A", "text": "he got quite scared of two things"}, {"key": "B", "text": "he still couldn’t understand two things"}, {"key": "C", "text": "he couldn’t stop thinking about two things"}, {"key": "D", "text": "he did two things that would change his life"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  40,
  '(A) should be spent helping his mom
(B) should be a time of welcoming a new start
(C) should not be about him, but about his mom
(D) should not be celebrated for just one day, but for nine months',
  '[{"key": "A", "text": "should be spent helping his mom"}, {"key": "B", "text": "should be a time of welcoming a new start"}, {"key": "C", "text": "should not be about him, but about his mom"}, {"key": "D", "text": "should not be celebrated for just one day, but for nine months"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  41,
  '(A) first (B) last (C) only (D) other',
  '[{"key": "A", "text": "first"}, {"key": "B", "text": "last"}, {"key": "C", "text": "only"}, {"key": "D", "text": "other"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  42,
  '(A) made his head hurt (B) made his heart sing
(C) made him change his mind (D) made him give up baking',
  '[{"key": "A", "text": "made his head hurt"}, {"key": "B", "text": "made his heart sing"}, {"key": "C", "text": "made him change his mind"}, {"key": "D", "text": "made him give up baking"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '114年國中教育會考',
  'english_reading',
  43,
  '(A) is going to give (B) gives (C) has given (D) gave
13 試題結束',
  '[{"key": "A", "text": "is going to give"}, {"key": "B", "text": "gives"}, {"key": "C", "text": "has given"}, {"key": "D", "text": "gave"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  1,
  '下列文句中的「即」字，何者為「靠近」之意？',
  '[{"key": "A", "text": "被熱水燙傷之後，應該立「即」用大量冷水沖洗"}, {"key": "B", "text": "他們兩個人的關係若「即」若離，真令人難以捉摸"}, {"key": "C", "text": "本活動摸彩中獎者，憑票根「即」可至服務臺領取獎品"}, {"key": "D", "text": "我不是你的傭人，別以為我可以招之「即」來，揮之即去"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  2,
  '「臺灣 泰式餐館幾乎都供應的椒麻雞，其實是出身雲南的混血菜。滇、緬、
泰、越、寮位置鄰近，料理自然互相滲透，彼此影響。這道菜傳到泰北，再到臺
灣，背景是烽火連天的歲月。像當年孤軍，遊走在滇、緬、泰邊境，流著四川的
麻辣血源和泰國的酸辣風格。」關於料理的敘述，下列何者最接近本文的觀點？',
  '[{"key": "A", "text": "料理會因地緣關係而互相影響"}, {"key": "B", "text": "異鄉遊子對童年吃食特別難忘"}, {"key": "C", "text": "戰火頻仍地區的料理多半偏辣"}, {"key": "D", "text": "餐館會依消費者需求調整口味"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  4,
  '根據右列資料判斷，「鬲」最可
《說文解字》：「鬲，
能屬於下列哪一種造字法則？
鼎屬也，實五觳，斗',
  '[{"key": "A", "text": "象形"}, {"key": "B", "text": "指事"}, {"key": "C", "text": "會意"}, {"key": "D", "text": "形聲"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  5,
  '「散文貴在自由□體例的自由、選材的自由、篇幅的自由、表達思想的自由。
寫作者可以依憑自己的認知，採用喜歡的書寫方式。」根據文意脈絡，缺空處
最適合填入下列哪一個標點符號？',
  '[{"key": "A", "text": "、"}, {"key": "B", "text": "？"}, {"key": "C", "text": "……"}, {"key": "D", "text": "――"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  6,
  '下列文句，何者用字完全正確？',
  '[{"key": "A", "text": "看朋友有難，他一無反顧出面幫忙"}, {"key": "B", "text": "我只是區區一個無名小足，人微言輕"}, {"key": "C", "text": "各種詐騙手法層出不窮，令人防不慎防"}, {"key": "D", "text": "早上公車發生擦撞，幸好乘客都安然無恙"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  7,
  '下列文句「」中的字，何者讀音正確？',
  '[{"key": "A", "text": "海嘯過後，小鎮滿目「瘡」痍：ㄘㄤ"}, {"key": "B", "text": "此事部長的心意已決，不容他人置「喙」：ㄓㄨㄛˊ"}, {"key": "C", "text": "電影首映會當晚，導演「偕」同主要演員一起出席：ㄒㄧㄝˊ"}, {"key": "D", "text": "這兩者「孰」輕孰重，你要考慮清楚，以免將來後悔：ㄕㄡˊ"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  8,
  '根據資料，下列關於《第十二夜》的推論，何者最恰當？',
  '[{"key": "A", "text": "旨在陳述耶穌受難一事"}, {"key": "B", "text": "每年固定連續演出十二天"}, {"key": "C", "text": "劇名由來與主顯節的日期有關"}, {"key": "D", "text": "英國宮廷因此劇而有戲劇展演的習俗"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  9,
  '「烘書之情何所似，有如老翁撫病子。心知元氣不可復，但求無死斯足矣。書
燒之時又何其，有如慈父怒啼兒。恨死擲去不回顧，徐徐復自撫摩之。此情自
痴還自笑，心血既乾轉煩惱。上壽八十能幾何，為爾多累何其多。」關於這首
詩的說明，下列敘述何者最恰當？',
  '[{"key": "A", "text": "「心知元氣不可復」指作者時日無多而焚書"}, {"key": "B", "text": "「恨死擲去不回顧」代表愛書之情至死不渝"}, {"key": "C", "text": "「徐徐復自撫摩之」表達作者不忍書燒之情"}, {"key": "D", "text": "「上壽八十能幾何」意指書籍保存有其時限"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  10,
  '《魏三體石經》每字皆刻三種字體，右圖
為部分拓本，已知其中二種字體為古文、
1
篆書。據此判斷，圖中第三種字體應為下
列何者？',
  '[{"key": "A", "text": "行書"}, {"key": "B", "text": "草書"}, {"key": "C", "text": "楷書"}, {"key": "D", "text": "隸書 "}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  11,
  '所謂的「寫真式描寫」注重的是清楚明確，以細密的筆觸刻畫完整的形
象，讓讀者有身歷其境的真實感。其描寫則依次序按部就班，傳達時力求客
觀。但既是創作，就不可能像攝影一樣完全「再現」，也難免會滲入少許暗
示性、象徵性的語彙。
根據本文，下列何者最符合「寫真式描寫」？',
  '[{"key": "A", "text": "他們明明知道要滴下眉毛上的汗珠，才能撿起田中的麥穗，而為什麼要謝天"}, {"key": "B", "text": "他用兩手攀著上面，兩腳再向上縮，他肥胖的身子向左微傾，顯出努力的樣子"}, {"key": "C", "text": "頃刻間這周遭瀰漫了清晨富麗的溫柔，頃刻間你的心懷也分潤了白天誕生的光榮"}, {"key": "D", "text": "有一些事，卻像夏日的小河、冬天的落葉，像春花，也像秋草，似無所見，又非視"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  13,
  '齊高帝善草書，篤好不已，祖述子敬，稍乏風骨。嘗與王僧虔賭書，書
畢曰：「誰為第一？」對曰：「臣書臣中第一，陛下書帝中第一。」帝笑曰：
「卿可謂善自謀矣。」然高帝與僧虔賭書，亦猶雞之搏狸，稍不自知量力也。
關於文中人物書法的比較，下列敘述何者最恰當？',
  '[{"key": "A", "text": "作者認為高帝書法不如僧虔"}, {"key": "B", "text": "作者認為子敬書法天下第一"}, {"key": "C", "text": "子敬覺得高帝的草書缺乏風骨"}, {"key": "D", "text": "僧虔自認與高帝賭書猶雞之搏狸"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  14,
  '2010年在名古屋舉辦的《聯合國生物多樣性公約》第10次大會，通過的
20項「愛知目標」，其中一項目標是2020年底全球海洋保護區的面積要達到
10%（又稱10 × 20目標），但這項目標後來只達到6～8%。2022年在蒙特婁
舉行第15次大會，又擬定2030年以前全球的陸域和海域要有30%保護區（又
稱30 × 30目標）。
根據本文，「30 × 30目標」的兩個數字所代表的意義，最可能是下列何者？
前者 後者',
  '[{"key": "A", "text": "大會舉行的年分 海洋保護區的面積百分比"}, {"key": "B", "text": "陸域和海域保護區的面積百分比 預計達成目標的年分"}, {"key": "C", "text": "預計達成目標的年分 陸域和海域保護區的面積百分比"}, {"key": "D", "text": "海洋保護區的面積百分比 大會舉行的年分"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  15,
  '「吉爾吉斯毛氈地毯色彩鮮豔，圖案多樣，製作技藝與知識通常由家族的年長
婦女傳授，完成後可用上至少30年。年長者會在動工與結束時祈福，製作時需
靠團隊合作：在年長婦女的監督下，由年輕婦女執行，男性則負責剃羊毛、幫
忙壓製，最後拿去販賣。這不但是吉爾吉斯人最重要的工藝之一，也有助社群
凝聚，創造認同感與文化延續性，因此獲得聯合國教科文組織認可為文化遺
產。」根據本文，吉爾吉斯毛氈地毯有助社群凝聚、創造認同感與文化延續性
的原因，最不可能是下列何者？',
  '[{"key": "A", "text": "成品可以使用至少30年"}, {"key": "B", "text": "需要團隊分工合作才能完成"}, {"key": "C", "text": "由年長婦女教導年輕婦女製作"}, {"key": "D", "text": "年長者會在動工與結束時祈福"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  17,
  '「宋代 賈似道的《促織經》是橫跨哲學、文學、醫學與口傳知識的系統性著
作，足以與現代問世的偉大昆蟲手冊相提並論，而歐洲最早的昆蟲專書則是在
《促織經》成書將近三百年後才出版。但賈似道的企圖心與歐洲博物學家不同，
他不像他們那樣對收集充滿熱情，或想用自己的方式擁有自然界。他只想寫給喜
愛鬥蟋蟀的賭徒參考。」根據本文，下列關於《促織經》的推論何者最恰當？',
  '[{"key": "A", "text": "是歐洲昆蟲專書的啟蒙"}, {"key": "B", "text": "是中國最早的跨領域學術研究"}, {"key": "C", "text": "意在激發人們探索自然的熱情"}, {"key": "D", "text": "教人如何提高鬥蟋蟀的致勝機率"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  18,
  '「子產相鄭，往見壺丘子林，與其弟子坐，必以年。夫居相於萬乘之國，而能捨
1
之，謀志論行，而以心與人相索，其唯子產乎？故相鄭十八年，唯刑三人、殺二
人，桃李之垂於行者，莫之援也。」關於文中子產的敘述，下列何者最恰當？
2',
  '[{"key": "A", "text": "求才若渴，四處招募各國的賢士"}, {"key": "B", "text": "認為教育乃治國根本，極力興學"}, {"key": "C", "text": "推行嚴刑峻法，令人民路不拾遺 2.援：採摘"}, {"key": "D", "text": "跳脫身分貴賤的框架，以誠待人"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  19,
  '下列文句「」中的成語，何者使用最恰當？',
  '[{"key": "A", "text": "這篇作品文采出眾，「胸無點墨」的人是寫不出來的"}, {"key": "B", "text": "辛勤工作之餘也要適時休息，才能達到「休戚與共」"}, {"key": "C", "text": "這兩個友好的國家交流往來頻繁，關係「間不容髮」"}, {"key": "D", "text": "他嚮往「瓜田李下」的鄉間生活，毫不猶豫搬離市區"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  20,
  '蔣堂為淮南轉運使，屬縣依例致賀，皆投書即還。有一縣令使人，獨求回
書，左右諭之皆不聽，呵逐亦不去，曰：「寧得罪，不得書不敢回邑。」時蘇
子美在座頗駭怪，曰：「小吏如此野狠，其令可知。」蔣曰：「不然，令必能
者，使人不敢慢其命令如此。」乃為簡答之，方去。子美歸吳中月餘，得蔣書
曰：「縣令果能者。」遂為之延譽，後卒為名臣。
關於文中人物的敘述，下列何者最恰當？',
  '[{"key": "A", "text": "小吏仗勢欺人，目無尊長"}, {"key": "B", "text": "縣令治事有方，管理嚴格"}, {"key": "C", "text": "蔣堂寫信推薦蘇子美為吳中令"}, {"key": "D", "text": "蘇子美有識人之明而成為名臣"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  21,
  '或問：「世間何物最硬？」曰：「石頭與鋼鐵。」其人曰：「石可碎，鐵可鏨，
1
安得為硬？以弟看來為兄面上髭鬚最硬，鐵石總不如也。」問其故，答曰：「兄
面皮厚，竟被看出。」鬚者回嘲曰：「足下面皮更老，這等硬鬚還鑽不透。」
根據這則笑話，以鬚者的立場來看，下列何者最硬？',
  '[{"key": "A", "text": "石頭與鋼鐵"}, {"key": "B", "text": "鬚者的面皮 "}, {"key": "C", "text": "面皮上的髭鬚"}, {"key": "D", "text": "無鬚者的面皮"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  22,
  '「往年士大夫好講水利。有言欲涸梁山泊以為農田者，或詰之曰：『梁山泊涸
之，不幸秋夏之交，行潦四集，諸水並入，何以受之？』貢父適在坐，徐曰：
『卻於泊之傍鑿一池，大小正同，則可受其水矣。』坐中皆絕倒，言者大慚
沮。」關於文中眾人對水利的想法，下列敘述何者最恰當？',
  '[{"key": "A", "text": "為解決梁山泊秋夏淹水的問題，士大夫提議涸梁山泊為田"}, {"key": "B", "text": "提出詰問的人擔憂梁山泊因泥沙淤積而難以吸納大量洪水"}, {"key": "C", "text": "貢父表面提出方法，實則藉此凸顯欲涸梁山泊為田的荒謬"}, {"key": "D", "text": "眾人對貢父的想法不以為然，仍堅持涸梁山泊為田的建議"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  23,
  '【甲】寒梅清秀誰知？霜禽翠羽同期。瀟灑寒塘月淡，暗香幽意，一枝雪裡偏宜。
【乙】野橋當日誰栽？前村昨夜先開。雪散珍珠亂篩，多情嬌態，一枝風送香來。
甲、乙兩曲皆詠梅，下列關於二者的比較，何者敘述最恰當？',
  '[{"key": "A", "text": "甲以雪喻梅，乙以珍珠喻梅"}, {"key": "B", "text": "二者皆有視覺與嗅覺的摹寫"}, {"key": "C", "text": "皆於首句提問，次句明確回答"}, {"key": "D", "text": "二者的視線推移皆是由近而遠"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  24,
  '關於這二節詩的分析，下列敘述何者最恰當？',
  '[{"key": "A", "text": "第一節以「野性」暗示作者正值年少"}, {"key": "B", "text": "第二節以「切碎」呼應「零零落落」"}, {"key": "C", "text": "第一節穿插驚嘆語句，表達吃不到的遺憾"}, {"key": "D", "text": "第二節藉心肝腸肺的描摹，象徵人心險惡"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  25,
  '關於這二節詩的共同點，下列敘述何者最恰當？',
  '[{"key": "A", "text": "皆透過描寫食物帶出生活的況味"}, {"key": "B", "text": "皆引用典故連結食物與文化的關係"}, {"key": "C", "text": "皆各自運用兩種顏色的對比，意象鮮明"}, {"key": "D", "text": "皆以當季食材入詩，強調美好事物稍縱即逝"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  26,
  '根據甲文，下列關於垂直農場的推論，何者最恰當？',
  '[{"key": "A", "text": "產量與用水量皆高出土壤種植方式"}, {"key": "B", "text": "受天然風災直接的影響少於傳統農業"}, {"key": "C", "text": "亞洲因生產成本較低，更適合垂直農場的發展"}, {"key": "D", "text": "2050年全球將有七成的人必須吃垂直農場栽種的蔬菜"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  27,
  '「循環經濟」強調的是資源可持續回復，循環再生。乙文畫線處的做法，何者
最能呼應「循環經濟」？',
  '[{"key": "A", "text": "①"}, {"key": "B", "text": "②"}, {"key": "C", "text": "③"}, {"key": "D", "text": "④"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  28,
  '乙文提及「研究人員指出這種模式可能較適合用在農業而非畜牧業」，其原因
最可能是下列何者？',
  '[{"key": "A", "text": "友善動物"}, {"key": "B", "text": "生產效能"}, {"key": "C", "text": "產品價格"}, {"key": "D", "text": "消費需求"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  29,
  '根據甲、乙二文，「垂直農場」與「漂浮牧場」共同的特點不包含下列何者？',
  '[{"key": "A", "text": "可以減少食物里程"}, {"key": "B", "text": "設置地點都在城市"}, {"key": "C", "text": "生產所需的資金成本高"}, {"key": "D", "text": "運作時需投入大量人力"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  30,
  '根據本文，畫線處的文句何者最能看出爸爸對孩子的重視？',
  '[{"key": "A", "text": "①"}, {"key": "B", "text": "②"}, {"key": "C", "text": "③"}, {"key": "D", "text": "④"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  31,
  '本文中的「我」和馬爾萬，身分最可能是下列何者？',
  '[{"key": "A", "text": "移民到阿拉伯半島的基督徒"}, {"key": "B", "text": "為戰亂國家運送物資的船員"}, {"key": "C", "text": "來自戰爭地區的穆斯林難民"}, {"key": "D", "text": "幫災民遠離砲火摧殘的善人"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  32,
  '關於本文的寫作分析，下列敘述何者最恰當？',
  '[{"key": "A", "text": "藉記憶中的畫面，呈現霍姆斯的今昔變化"}, {"key": "B", "text": "列舉多個國家的名稱，凸顯了航程的漫長"}, {"key": "C", "text": "以等待日出的場景，傳達近鄉情怯的不安"}, {"key": "D", "text": "透過海的深廣，比喻母親話中溫暖的力量"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  33,
  '關於文中翰林供奉的敘述，下列何者最恰當？',
  '[{"key": "A", "text": "可獨立辦公"}, {"key": "B", "text": "有很多兼職收入"}, {"key": "C", "text": "薪水比照八品京官"}, {"key": "D", "text": "不能幫皇帝處理奏章"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  34,
  '根據本文，下列推論何者最恰當？',
  '[{"key": "A", "text": "尚書和侍郎通常也兼任翰林供奉"}, {"key": "B", "text": "翰林學士處理政務的能力優於翰林供奉"}, {"key": "C", "text": "翰林待詔是唐玄宗重要的行政幕僚之一"}, {"key": "D", "text": "翰林待詔與翰林學士的差別在專門品級的高低"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  35,
  '根據本文，下列關於投壺的敘述何者最恰當？',
  '[{"key": "A", "text": "主人要讓分給客人"}, {"key": "B", "text": "由先秦的娛樂競技演變而來"}, {"key": "C", "text": "參賽者各以四箭算一局勝負"}, {"key": "D", "text": "司正以三局分數的總和判定贏家"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  36,
  '右表為某場投壺比賽的計分表， 客人投壺狀況 主人投壺狀況
「」表示投中，「」表示未投
第一局        
中。根據本文及右表，下列敘述何
第二局        
者正確？
第三局        ',
  '[{"key": "A", "text": "第一局客人勝"}, {"key": "B", "text": "第二局主人勝"}, {"key": "C", "text": "第三局客人勝"}, {"key": "D", "text": "最終贏家是主人"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  37,
  '根據本文，關於熱帶大頭家蟻入侵肯亞保護區後的生態變化，下列敘述何者最
恰當？',
  '[{"key": "A", "text": "獅子數量減少"}, {"key": "B", "text": "斑馬易受獅子攻擊"}, {"key": "C", "text": "金合歡易受大象破壞"}, {"key": "D", "text": "舉尾蟻不再攻擊大象"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  38,
  '依據本文引述的研究發現，無法說明下列何者？',
  '[{"key": "A", "text": "設置保護區有助於維護自然原始生態"}, {"key": "B", "text": "外來物種可能會對本地生態造成衝擊"}, {"key": "C", "text": "面對環境的變遷，生命自會找到出路"}, {"key": "D", "text": "破壞生物間的互利關係恐有連鎖反應"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  39,
  '根據本文，下列「」中的字何者當動詞使用？',
  '[{"key": "A", "text": "「至」忠"}, {"key": "B", "text": "弗類「若」不孝也"}, {"key": "C", "text": "嘗從余「客」荔城"}, {"key": "D", "text": "傳之亦所以志余「過」也"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  40,
  '關於文中僮僕遂的敘述，下列何者最恰當？',
  '[{"key": "A", "text": "生母過世後，託人購買湯餅祭拜表達孝心"}, {"key": "B", "text": "提醒轎夫選擇平坦的道路，以免自己受傷"}, {"key": "C", "text": "雖想跟從主人前去杭城，最終仍聽命留下"}, {"key": "D", "text": "流落南方不幸染疫，死後輾轉歸葬於海山"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  41,
  '下列文句「」中文字的解釋，何者最恰當？',
  '[{"key": "A", "text": "田饒事魯哀公，而「不見察」：不懂得自我反省"}, {"key": "B", "text": "「見食相告」者，仁也：看到食物就通知夥伴"}, {"key": "C", "text": "夫黃鵠「一舉千里」：高踞樹頂，眼界開闊"}, {"key": "D", "text": "「遂去之燕」，燕以為相：離開了燕國"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'chinese',
  42,
  '根據本文，田饒認為哀公晉用人才的態度，與下列何者最接近？',
  '[{"key": "A", "text": "肥水不落外人田"}, {"key": "B", "text": "遠來的和尚會念經"}, {"key": "C", "text": "不求有功，但求無過"}, {"key": "D", "text": "內舉不避親，外舉不避仇"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  1,
  '解二元一次聯立方程式 ，得 x 值為何？
2x − 2y = 1',
  '[{"key": "A", "text": "−4"}, {"key": "B", "text": "−2"}, {"key": "C", "text": "2"}, {"key": "D", "text": "4"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  2,
  '如圖 ( 一 )，直角柱 ABCDEF 的底面為正三角形，圖中
標示各頂點名稱。判斷此角柱中的 ∠ABC、∠BCF 的度數
分別為何？',
  '[{"key": "A", "text": "∠ABC = 90°，∠BCF = 90°"}, {"key": "B", "text": "∠ABC = 60°，∠BCF = 60°"}, {"key": "C", "text": "∠ABC = 90°，∠BCF = 60°"}, {"key": "D", "text": "∠ABC = 60°，∠BCF = 90°"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  3,
  '若 504 的最簡根式為 a b，則 a + b 之值為何？',
  '[{"key": "A", "text": "13"}, {"key": "B", "text": "19"}, {"key": "C", "text": "20"}, {"key": "D", "text": "50"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  4,
  '已知甲袋中有三顆球，球上分別標記 2、 3、4 ；乙袋中有三顆球，球上分別標
記 3、 4、 5。阿翰打算從甲、乙兩袋中各抽出一球，若甲袋中每顆球被抽出的
機會相等，乙袋中每顆球被抽出的機會相等，則抽出的兩球上的數字，總和
為多少的機率最大？',
  '[{"key": "A", "text": "6"}, {"key": "B", "text": "7"}, {"key": "C", "text": "8"}, {"key": "D", "text": "9"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  5,
  '算式 2.45 × 98.7 − ( −0.55 ) × 98.7 之值介於下列哪兩個數之間？',
  '[{"key": "A", "text": "150，200"}, {"key": "B", "text": "200，250"}, {"key": "C", "text": "250，300"}, {"key": "D", "text": "300，350"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  6,
  '小彭的農園將收成的文旦根據每顆的重量分為小果、中果、大果，再根據每顆
的品質分為良級、優級、特級，分類後各類別的總重量如表 ( 一 ) 所示。
表(一)
因為被分類為良級或大果的文旦不受喜愛，所以小彭僅將其餘的文旦都包裝
成禮盒販售，求包裝成禮盒販售的文旦總共有多少公斤？',
  '[{"key": "A", "text": "620"}, {"key": "B", "text": "630"}, {"key": "C", "text": "700"}, {"key": "D", "text": "720"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  7,
  '計算多項式 4x2 − 3x − 5 除以 x + 2 後，所得商式與餘式兩者之和為何？',
  '[{"key": "A", "text": "4x + 6"}, {"key": "B", "text": "4x + 10"}, {"key": "C", "text": "−7x − 5"}, {"key": "D", "text": "−11x − 1"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  8,
  '有 一 培 養 皿 上 均 勻 分 布 細 菌， 圖 ( 二 ) 是 培 養 皿 與 其 俯 視 圖，
生 物 學 家 在 培 養 皿 上 選 定 四 個 圓 形 區 域， 區 域 面 積 越 大 所 含
細 菌 數 越 多。 若 圖 中 甲、 乙、 丙 三 個 區 域 細 菌 的 數 量 分 別 為
4.4 × 105 個、 7.3 × 106 個、 5.4 × 107 個，則下列何者可能是丁區域細菌
的數量？',
  '[{"key": "A", "text": "1.7 × 105 個"}, {"key": "B", "text": "1.7 × 106 個"}, {"key": "C", "text": "1.7 × 107 個"}, {"key": "D", "text": "1.7 × 108 個"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  9,
  '已知一元二次方程式 2x ( x + 7 ) − 10 ( x + 7 ) = 0 的兩根為 a、 b，且 a > b，
求 a + 2b 之值為何？',
  '[{"key": "A", "text": "−13"}, {"key": "B", "text": "−9"}, {"key": "C", "text": "−4"}, {"key": "D", "text": "−3"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  10,
  '某書店舉辦優惠活動，購買的書原價合計滿 1100 元折扣 200 元，圖 ( 三 )
為兄妹兩人的對話情形。
圖(三)
根據圖中的對話計算，妹妹要買的書原價為多少元？',
  '[{"key": "A", "text": "360"}, {"key": "B", "text": "380"}, {"key": "C", "text": "460"}, {"key": "D", "text": "480"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  11,
  'A(a)、B(b)、P(a + b) 三點在數線上的位置如圖 ( 四 ) 所示。若要在數線上
標示點 Q(b − a)，則關於 Q 點的位置，下列敘述何者正確？',
  '[{"key": "A", "text": "在 B 的右邊"}, {"key": "B", "text": "介於 A、B 之間"}, {"key": "C", "text": "介於 P、A 之間"}, {"key": "D", "text": "在 P 的左邊"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  12,
  '∆ABC 的邊上有三點 D、E、F，各點位置如圖 ( 五 ) 所示。若 BE = AF，
∠BED =∠AFC，ED = FC，則根據圖中標示的長度，求四邊形 ADEF 周長
為何？',
  '[{"key": "A", "text": "20"}, {"key": "B", "text": "22"}, {"key": "C", "text": "24"}, {"key": "D", "text": "25"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  13,
  '若坐標平面上有一直線 L 與 x 軸平行，且 L 通過點 ( −3 , −1 )，則 L 的方程式
為何？',
  '[{"key": "A", "text": "x = −3"}, {"key": "B", "text": "y = −3"}, {"key": "C", "text": "x = −1"}, {"key": "D", "text": "y = −1"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  14,
  '已知坐標平面上有二次函數 y = − ( x + 5 )2 − 20 的圖形，甲、乙兩人提出
以下看法：
【甲】此函數圖形上某個點的 y 坐標為 −15
【乙】此函數圖形上某個點的 y 坐標為 25
對於甲、乙兩人的看法，下列判斷何者正確？',
  '[{"key": "A", "text": "甲、乙皆正確"}, {"key": "B", "text": "甲、乙皆錯誤"}, {"key": "C", "text": "甲正確，乙錯誤"}, {"key": "D", "text": "甲錯誤，乙正確"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  15,
  '圖 ( 六 ) 有一正六邊形 ABCDEF 與一正 n 邊形的部分圖形，其中 G、E、H、
I 為正 n 邊形中連續的四個頂點，F 在 GE 上，C、D、H、I 四點共線。求 n 值
為何？',
  '[{"key": "A", "text": "8"}, {"key": "B", "text": "10"}, {"key": "C", "text": "12"}, {"key": "D", "text": "15"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  18,
  '如圖 ( 八 )， 圓 O 與菱形 ABCD 中， A、 B、 D 在圓上， C 在圓內，O 在 AC
上。若圓 O 的半徑為 13， BD = 24，則 CO 的長度為多少？',
  '[{"key": "A", "text": "2"}, {"key": "B", "text": "3"}, {"key": "C", "text": "4"}, {"key": "D", "text": "5"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  19,
  '已知一圓上有 A、B、C、D 四點，其位置如圖(九)所示，
其中 AB = 87°， BC = 91°， CD = 88°， AD = 94°。若在
此圓上找兩點 E、 F，使得四邊形 ABEF 為長方形，則
下列關於 E 點、F 點位置的敘述，何者正確？',
  '[{"key": "A", "text": "E 在 BC 上，F 在 CD 上"}, {"key": "B", "text": "E 在 BC 上，F 在 AD 上"}, {"key": "C", "text": "E 在 CD 上，F 在 CD 上"}, {"key": "D", "text": "E 在 CD 上，F 在 AD 上"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  20,
  '已知正整數 M 的因數中，除了 M 之外最大的因數是 22 × 11，正整數 N 的
因數中，除了 N 之外最大的因數是 3 × 13。甲、乙兩人提出以下看法：
【甲】 8 一定是 M 的因數
【乙】 9 一定是 N 的因數
對於甲、乙兩人的看法，下列判斷何者正確？',
  '[{"key": "A", "text": "甲、乙皆正確"}, {"key": "B", "text": "甲、乙皆錯誤"}, {"key": "C", "text": "甲正確，乙錯誤"}, {"key": "D", "text": "甲錯誤，乙正確"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  21,
  '如圖(十)，∆ABC 與 ∆ADE 中，D 點在 ∆ABC 外，
E 點在 AB 上，∠D = ∠DEA = ∠EAC = ∠C = 65°。
若 BC 上有一點 F， AF 與直線 DE 相交於 P 點，
且 BF = 5，FC = 8，BE = 6，則 AP 與 AF 的
長度比為何？',
  '[{"key": "A", "text": "4：5"}, {"key": "B", "text": "5：6"}, {"key": "C", "text": "6：7"}, {"key": "D", "text": "7：8"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  22,
  '如圖 ( 十一 )，平行四邊形 ABCD 中，AB = 20，
AD = 21。甲、乙兩人想找一點 P，使得 P 到 BC
的距離等於 P 到 AD 的距離，且 P 到 AB 的距離
等於 P 到 CD 的距離，其作法如下：
【甲】連接 AC、BD，兩線段相交於 P 點，
圖(十一)
則 P 即為所求
【乙】作 ∠C、∠D 的角平分線，兩直線相交於 P 點，則 P 即為所求
對於甲、乙兩人的作法，下列判斷何者正確？',
  '[{"key": "A", "text": "甲、乙皆正確"}, {"key": "B", "text": "甲、乙皆錯誤"}, {"key": "C", "text": "甲正確，乙錯誤"}, {"key": "D", "text": "甲錯誤，乙正確"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  23,
  '根據選文，時速錶符合法規的汽車行駛時，若指示速率為 120 公里 / 小時，
則實際速率的最小值與最大值分別是多少公里 / 小時？ ( 最小值用無條件進入
法取概數到個位，最大值用無條件捨去法取概數到個位 )',
  '[{"key": "A", "text": "最小值 105，最大值 120"}, {"key": "B", "text": "最小值 106，最大值 120"}, {"key": "C", "text": "最小值 120，最大值 136"}, {"key": "D", "text": "最小值 120，最大值 137"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  24,
  '根據選文，已知有一輛行駛中的汽車，其輪胎轉速為 x 圈 / 分鐘且輪胎周長為
200 公分。若此車的實際速率為 y 公里 / 小時，則 y 與 x 的關係為下列何者？',
  '[{"key": "A", "text": "y = 0.002x"}, {"key": "B", "text": "y = 0.12x"}, {"key": "C", "text": "y = 200x"}, {"key": "D", "text": "y = 12000x"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'math',
  25,
  '根據選文，已知原本甲、乙兩輛車上儀器測出的輪胎轉速跟實際的輪胎轉速
相等，兩車儀器設定的輪胎周長也與當時兩車安裝的輪胎周長相等。後來甲
的儀器發生故障，導致儀器測出的輪胎轉速比實際的輪胎轉速更高，而乙更
換輪胎，新輪胎周長比原本的更小，但儀器設定的仍是原本輪胎周長。若甲、
乙此時皆以 60 公里 / 小時的指示速率行駛，且甲、乙的實際速率分別為
p 公里 / 小時、q 公里 / 小時，則下列關係何者正確？',
  '[{"key": "A", "text": "p > 60，q > 60"}, {"key": "B", "text": "p > 60，q < 60"}, {"key": "C", "text": "p < 60，q > 60"}, {"key": "D", "text": "p < 60，q < 60"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  1,
  '農業部統計，受發生於2024年7月下旬的某次災害影響，全臺農業損失估計高
達33億元，其中以雲林縣、臺南市、嘉義縣的損失尤為慘重，三個行政區農
損合計超過全臺農損的一半。根據上述災害發生時間及受影響地區判斷，此
災害最可能為下列何者？',
  '[{"key": "A", "text": "颱風帶來的豪大雨淹沒農田"}, {"key": "B", "text": "強勁東北季風吹襲造成水稻倒伏"}, {"key": "C", "text": "梅雨季節的連續降雨造成果樹浸水"}, {"key": "D", "text": "強勁西南風越過山脈形成熱風使作物枯黃"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  2,
  '日本於2019年4月起，擴大從越南、菲律賓、印尼、泰國、柬埔寨、中國、
緬甸、尼泊爾和蒙古招募外籍移工，以補充其看護、餐飲和建築等行業嚴重
短缺的勞動力。下列何者因同樣面臨勞動力短缺及外籍移工來源國高度重疊
的關係，而受上述政策執行的衝擊最大？',
  '[{"key": "A", "text": "印度"}, {"key": "B", "text": "美國"}, {"key": "C", "text": "德國"}, {"key": "D", "text": "臺灣"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  4,
  '某一平埔族族群居住在雪山山脈與中央山脈之間的平原地區，他們利用竹筏
穿梭於溪流與海岸間，進行漁獵及採集活動。依據上述判斷，該平埔族族群
的生活空間最可能位於現今哪一行政區？',
  '[{"key": "A", "text": "宜蘭縣"}, {"key": "B", "text": "苗栗縣"}, {"key": "C", "text": "屏東縣"}, {"key": "D", "text": "臺東縣"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  5,
  '圖(二)為2019年世界多數國家都市化程度
與該國人均國民所得的統計圖，圖中以
此兩種統計值的世界平均值為基準，劃
分成甲、乙、丙、丁四個區塊。根據各
洲經濟及都市發展特色判斷，歐洲西半
部的國家最可能位於圖中哪一區塊？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  6,
  '羅馬帝國時期的作家普魯塔克在書中提到，西元前八世紀的某政權曾有「殺
嬰」習俗，將不夠健壯的嬰兒放在山上等死。然而部分研究指出當時先天有
缺陷的人仍受到照顧，所謂的「棄嬰山」可能只是處決罪犯之處，且文獻上
也提到該政權曾選出身體有缺陷的國王。普魯塔克的說法，可能是基於當時
人們熟知該政權過於重視軍事教育，所產生的錯誤印象。上述政權最可能是
下列何者？',
  '[{"key": "A", "text": "埃及"}, {"key": "B", "text": "蘇美"}, {"key": "C", "text": "巴比倫"}, {"key": "D", "text": "斯巴達"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  8,
  '「不安的情緒逐漸發酵，社會上出現『牙刷主義』一說：權貴們將資產轉至
外國，並取得外國居留權，萬一局勢惡化，只要帶牙刷就能遠走高飛。政府
為因應民心浮動、《中美共同防禦條約》不久後失效等危機，再次端出數年
前『莊敬自強，處變不驚』口號，發起愛國捐獻、青年從軍報國，電臺日夜
播放〈龍的傳人〉等愛國歌曲。」上述內容最可能與下列何者有關？',
  '[{"key": "A", "text": "美國在韓戰後協防臺灣海峽"}, {"key": "B", "text": "美國宣布將與中華民國斷交"}, {"key": "C", "text": "國 共內戰使政府敗退至臺灣"}, {"key": "D", "text": "臺灣受到同盟國軍機的空襲"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  9,
  '十七世紀中期，臺灣某地區原住民因能說西班牙語，
且多人曾受洗為天主教徒，所以被荷蘭 聯合東印度公
司認為是「具西班牙人特質」的族群。上述族群最可
能分布在圖(四)甲、乙、丙、丁哪一區域？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  10,
  '家住屏東的小萱在觀賞日本動畫時，發現劇中主角的考卷上每一道試題都畫
上「 」，但卻是拿到零分，與自己考卷全被畫上「 」時拿到滿分是不一
樣的情況。查詢資料後，小萱才知道在日本畫「 」與畫「 」代表的都是有
錯誤，而把答案畫上「 」才是代表答對的意思。上述內容最適合用來說明
下列哪一現象？',
  '[{"key": "A", "text": "各國移民的習俗多元並存"}, {"key": "B", "text": "社會制度隨著時間而變動"}, {"key": "C", "text": "不同文化間存在些許差異"}, {"key": "D", "text": "文化交流後產生位階高低"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  11,
  '圖(五)是新奇科技購物網站更新前的網頁資訊，
某日該網頁內容調整後，幾分鐘內商品突然銷
售一空，甚至還多了數百筆的訂單等候補貨。
下列何者最可能是造成上述情況的原因？
圖(五)',
  '[{"key": "A", "text": "供貨量變更為19臺"}, {"key": "B", "text": "供貨量變更為999臺"}, {"key": "C", "text": "售價變更為9,999元"}, {"key": "D", "text": "售價變更為20,999元"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  12,
  '臭蟲又稱床蝨，因常躲在床墊中而得名，人類被叮咬後皮膚會紅腫且奇癢無
比。臭蟲會隨人群移動而擴散，例如：2023年法國爆發臭蟲危機，因觀光
客、商務旅客及國際移工的遷移，使得臭蟲經由藏在行李中，蔓延至許多國
家。上述內容最主要在探討下列何項議題？',
  '[{"key": "A", "text": "國際移工引入帶來的文化衝突"}, {"key": "B", "text": "區域糾紛擴大引發的民生困境"}, {"key": "C", "text": "高度工業化與氣候變遷的關係"}, {"key": "D", "text": "經濟全球化對人類生活的影響"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  13,
  '表(一)為二位我國某縣縣民的部 表(一)
分資料，根據我國法律規定判 姓名 陳小花 吳阿杰
斷，關於此二位縣民的敘述，下 年齡 25 歲 28 歲
列何者正確？ 設籍時間 7 個月 5 個月',
  '[{"key": "A", "text": "皆具備完全行為能力 現況 受監護宣告 被宣告褫奪公權"}, {"key": "B", "text": "皆曾受到刑事處罰判決"}, {"key": "C", "text": "皆無法參選該縣公職人員"}, {"key": "D", "text": "皆不具備該縣縣長投票資格"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  14,
  '小蔓一歲時親生父母離婚，之後與母親同住。四歲時，母親與阿德再婚，小蔓
和他們兩人一起組成現在的家庭。若阿德婚後未曾進行任何法律程序改變家中
成員關係，僅根據上述內容判斷，小蔓與阿德間的親屬關係應為下列何者？',
  '[{"key": "A", "text": "姻親"}, {"key": "B", "text": "配偶"}, {"key": "C", "text": "旁系血親"}, {"key": "D", "text": "直系血親"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  15,
  '一處坐落於海拔2,430公尺山脊上的古城遺跡，是美洲
三大古文明代表性的建築之一，其建築精妙之處是將
打磨過的方形石塊疊砌起來，且在沒有使用砂漿的情
況下使其能如拼圖般緊密結合。此外，建築中的梯形
門窗和向內微傾斜的牆面等，皆可降低建築物在地震
中倒塌的可能性。上述古城遺跡最可能位於圖(六)中
何處？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  16,
  '表(二)顯示2016至2019年歐洲與亞洲之間，行經北極 表(二)
地區某條海運航線的航行次數統計。根據表中數字判 年分 航行次數(次)
斷，此種變化除了受到全球經濟持續成長所帶動的海 2016 1,705
運需求增加外，最可能還受下列何者的影響？ 2017 1,908',
  '[{"key": "A", "text": "海冰融化大幅增加"}, {"key": "B", "text": "全球生態保育意識興起"}, {"key": "C", "text": "巴拿馬運河通行費調漲"}, {"key": "D", "text": "《區域全面經濟夥伴協定》生效"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  17,
  '報導指出：「在俄 烏戰爭爆發之前的3年裡，歐盟成員國平均每月從俄羅斯
進口約1,520萬噸原油和石油產品，到了2023年3月，該值已下降至140萬噸。
歐盟預計2027年切斷從俄羅斯的化石燃料進口，擺脫對其能源依賴。」下列
何項措施無助於達成上述目標？',
  '[{"key": "A", "text": "制定公共場所更嚴格的暖氣供應標準"}, {"key": "B", "text": "促使石油輸出國家組織維持減產政策"}, {"key": "C", "text": "與其他第三國簽署天然氣的進口協議"}, {"key": "D", "text": "積極發展綠能以增加替代性能源產量"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  18,
  '中國 黃河是世界上含沙量最高的河流，但2024年1月，有遊客在陝西 壺口瀑
布拍攝到「清流飛瀑」的壯觀景象，其實早在2020年就曾有報導指出，壺口
的黃河河水變清了。事實上「黃河清」很罕見，歷史上的記載只有43次。黃河
於2024年1月出現上述景象，最可能與下列何者關係較為密切？',
  '[{"key": "A", "text": "瀑布上游流經黃土高原，支流帶入大量泥沙"}, {"key": "B", "text": "瀑布上游實施造林固沙政策，減少泥沙流入"}, {"key": "C", "text": "瀑布下游恰逢雨季，大量降水使得流量增加"}, {"key": "D", "text": "瀑布下游興築壩堤，以壩堤攔阻泥沙變良田"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  20,
  '表(三)是中國歷史上三則與生活相關的資料：
表(三)
西元七世紀時，從中亞引進的馬匹最受歡迎，其高大、速度快，深
資料一
受貴族和皇室喜愛。
西元七世紀，羊肉的消費量大為提高。八世紀上半葉，隴右(今甘肅)
資料二
飼養的羊隻，成長了二倍多。
資料三 西元八世紀中期，貴族婦女騎馬出門，戴胡帽並展露出妝容。
上述資料最可能與下列何者有關？',
  '[{"key": "A", "text": "商 周到秦 漢的族群交流"}, {"key": "B", "text": "魏 晉到隋 唐的民族互動"}, {"key": "C", "text": "宋朝到元朝的國際交流"}, {"key": "D", "text": "明 清時期東亞世界的變遷"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  22,
  '十九世紀晚期美國政府取得一處亞洲殖民地，曾陷入要延續先前的殖民體
系，或允許該地獨立的兩難。美國總統決定延續殖民體系，結合當時流行的
學說，發表一段談話：「美國必須以現代教育和基督教文化，教化欠缺能力
的殖民地人民，提升其素質。靠著神的恩典，盡我們所能做到最好。」上述
談話，最能體現下列何者？',
  '[{"key": "A", "text": "因信得救"}, {"key": "B", "text": "天賦人權"}, {"key": "C", "text": "社會達爾文主義"}, {"key": "D", "text": "極權政治的興起"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  23,
  '甲國面臨勞動力不足的窘境，因此該國政府研擬放寬外國籍人士申請永久居
留的條件，並開放配偶、親屬可一同移入長期居留，希望提高外國籍勞工居
住在該國提供勞動力的意願。藉由上述政策而取得在甲國永久居留資格者，
與甲國國民在權利義務的異同，若從我國法律規定的角度分析，下列何項敘
述最適當？',
  '[{"key": "A", "text": "皆具有參與公民投票的資格"}, {"key": "B", "text": "皆具有發表時事評論的自由"}, {"key": "C", "text": "皆具有擔任民意代表的機會"}, {"key": "D", "text": "皆具有接受國民教育的義務"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  25,
  '「我國原本由宏都拉斯進口大量白蝦，但2023年與該國斷交後，我國恢復對
該國產品課徵關稅，部分進口業者的營運遭受衝擊，進口量大幅下滑。我國
官員受訪時提及，2025年將開放貝里斯的白蝦零關稅進口至我國，以增加商
品供應來源。」僅根據上述內容判斷，關於此二項進口政策變化產生的各別
影響，下列何項推論最合理？',
  '[{"key": "A", "text": "受到對貝里斯政策的影響，我國市場上白蝦的售價下降"}, {"key": "B", "text": "受到對貝里斯政策的影響，貝里斯的貿易出超金額下降"}, {"key": "C", "text": "受到對宏都拉斯政策的影響，宏都拉斯的貿易出超金額上升"}, {"key": "D", "text": "受到對宏都拉斯政策的影響，我國白蝦市場的競爭程度上升"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  26,
  '在公民課的分組活動中，小華 表(四)
與同組同學打算以短劇的方 甲 當事人至法院提告對方違反契約
途徑
式，呈現民眾解決民事紛爭的 乙 被害人委任律師向法院提出自訴
途徑及結果。表(四)是該組同 丙 被告遭到法院判決處以罰金
結果
學在討論時提出的各種情境， 丁 雙方在法院達成訴訟上和解
若小華負責編寫劇本，他應選
擇下列何項組合才符合我國的
法律規定？',
  '[{"key": "A", "text": "甲、丙"}, {"key": "B", "text": "甲、丁"}, {"key": "C", "text": "乙、丙"}, {"key": "D", "text": "乙、丁"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  27,
  '因應國際趨勢，跨國企業近年將部分生產線從中國分散至其他國家。其中甲
國2020年的人口金字塔顯示壯年人口比例近70%，且未來數十年仍占極高比
例，再加上該國工資明顯低於中國，而成為跨國企業布局的主要選擇之一。
依據上述資訊，甲國的人口金字塔最可能為下列何者？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  28,
  '「2018年1月23日17時32分(臺灣時間)，於阿拉斯加南方海域發生規模8.0的地
震，震央在西經149.20度，北緯56.00度。該區域的海嘯警報中心研判可能引
發海嘯，經初步推算，該地震所引發的海嘯，將不會影響臺灣。」根據震央
位置判斷，上述海嘯警報中心應是下列何者？',
  '[{"key": "A", "text": "太平洋海嘯警報中心"}, {"key": "B", "text": "印度洋海嘯警報中心"}, {"key": "C", "text": "加勒比海海嘯警報中心"}, {"key": "D", "text": "東北大西洋暨地中海及相連海域海嘯警報中心"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  29,
  '根據學者研究，臺灣地名中的「坑」為閩南族群與客家族群通用來指稱溪谷
的用字，常與「頭」、「尾」連用來辨別聚落在溪谷內的位置。例如閩南族
群的地名「坑頭」，是指聚落位在溪流的上游；客家族群則是依開墾順序命
名，拓墾通常由河谷下游往上游進行，最後開墾的聚落則以「坑尾」命名。
下列哪一示意圖最符合上述兩族群坑頭及坑尾聚落位置的命名原則？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": "7"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  30,
  '以下為一份契約的內容：「立賣契人竹塹社 一均。因本社稅賦繁重，加上能
捕到的鹿變少，經過內部共同討論，願將本社管轄的貓兒錠一處草地，由漢
人郭弈榮承買，時價銀二十兩。該處土地由郭弈榮開築埤圳，招募佃戶，開
墾後報官取得土地權利，並且每年仍補貼竹塹社的稅賦銀二十兩。」對於上
述契約內容的理解，下列何者最適當？',
  '[{"key": "A", "text": "官府的賦稅，影響原住民土地經營方式"}, {"key": "B", "text": "竹塹社原住民，當時被官府歸類為生番"}, {"key": "C", "text": "漢人承買土地，是為了捕獵更多的鹿隻"}, {"key": "D", "text": "竹塹社受到漢人脅迫，舉社向東部遷徙"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  31,
  '「法國國王為課徵新稅以解決財政危機，決定重新恢復自1614年以來未再召
開的諮詢機關，各界為此選出1,139名代表，來到凡爾賽宮進行稅制改革。代
表們帶著來自全國各階層的陳情書，其內容遠遠超出財政危機的問題。」上
述「諮詢機關」，最可能是下列何者？',
  '[{"key": "A", "text": "巴黎和會"}, {"key": "B", "text": "三級會議"}, {"key": "C", "text": "關稅同盟"}, {"key": "D", "text": "聯合國大會"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  32,
  '一位檢察官在法庭陳述意見時提到：「本次的違法事件，就是臺灣人意圖謀
反，目的是從帝國手中奪取臺灣。帝國目前對臺灣的統治，實在過於優厚，而
臺灣人不知感恩，竟然要求設置臺灣議會。臺灣人如果反對現行統治方針，不
願做日本國民，那就離開臺灣吧。」上述「統治方針」應是下列何者？',
  '[{"key": "A", "text": "實施軍事戒嚴"}, {"key": "B", "text": "終止動員戡亂"}, {"key": "C", "text": "貫徹民族自決"}, {"key": "D", "text": "推行內地延長"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  33,
  '以下是中國某時期重要人才選用方式的敘述：「脫穎而出者由皇帝親授官
職，經過十餘年的歷練，就有機會執掌國政。當時人為此曾評論道：『就算
是今日帶領數十萬大軍伐遼，從契丹人手中奪回燕雲十六州，其榮耀都比不
上呢！』」上文「脫穎而出」的方式，最可能為下列何者？',
  '[{"key": "A", "text": "通過科舉考試入仕"}, {"key": "B", "text": "向天朝納貢受冊封"}, {"key": "C", "text": "奉旨前往德國留學"}, {"key": "D", "text": "依九品官人法獲評上品"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  35,
  '老師在課堂上講解權力分立的概念，說明如何透過分權制衡的機制，以避免
政府濫權或侵害人民的權利，這種政府體制運作的原則，廣為多數民主國家
所採用。下列何者的互動關係符合上述概念？',
  '[{"key": "A", "text": "總統任命執政黨的黨員擔任行政院院長"}, {"key": "B", "text": "縣長推動觀光活動以籌措地方政府財源"}, {"key": "C", "text": "行政院對於窒礙難行的法案提出覆議"}, {"key": "D", "text": "民眾為表達對政策不滿上街遊行抗議"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  36,
  '臺北市為維護選舉時的市容景觀和秩序，制定《臺北市競選廣告物管理自治
條例》，透過地方法規限制競選廣告的設置，違規者將被處以罰鍰，並限期
移除廣告。但有人認為該法規的規範不夠明確，參選者仍可以形象廣告的方
式刊登廣告，以致許多民眾覺得競選廣告並沒有減少，希望相關單位能予以
修正。關於上述法規的敘述，下列何者最適當？',
  '[{"key": "A", "text": "臺北市採行正向誘因，處理競選廣告違規問題"}, {"key": "B", "text": "該條例若需修正，應由立法院依照規定三讀通過"}, {"key": "C", "text": "違規受罰者若不服處分，可提起訴願進行權利救濟"}, {"key": "D", "text": "政府透過刑事處罰手段，預防選舉期間發生犯罪行為"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  37,
  '甲團體常透過統計數據評鑑某中央政府機關的公職人 表(五)
員，並在社群媒體上公布報告，表(五)為其中一位公職 各項會議
91.7%
人員的統計數據。有民眾認為這些數據僅能呈現工作 平均出席率
量，無法看出工作品質，因此留言建議可以增列其他 法律修正案
12 件
評鑑項目。根據上述內容判斷，增列下列哪一項目最 的提案件數
有助於評鑑此種公職人員的表現？
預算審查
80.3%',
  '[{"key": "A", "text": "對不當施政的糾正案件數 參與率"}, {"key": "B", "text": "各類訴訟案件的審理進度"}, {"key": "C", "text": "公共工程預算的編列金額"}, {"key": "D", "text": "對各部會首長的質詢內容"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  38,
  '有環保團體推出「掃了再買」APP，民眾只要使用這個APP掃描商品條碼，就
能看到商品製造商有沒有因違反環保法規遭罰的紀錄。該團體希望藉此能提
供消費者更充足的資訊，幫助他們在購物時判斷是否要購買，甚至改變原先
的選擇，並期許生產者為其生產行為負起責任，而優良企業也能獲得消費者
肯定。關於上述環保團體推出的手機APP，下列敘述何者最適當？',
  '[{"key": "A", "text": "有助於增加消費者的購物支出"}, {"key": "B", "text": "呈現出法律變革影響科技發展"}, {"key": "C", "text": "揭露各企業曾經發生的民事紛爭"}, {"key": "D", "text": "藉由影響個人偏好改變消費行為"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  39,
  '「官軍從鹿港登陸以後，很快就摧破賊巢、痛殲匪眾。只是現在『逆首』竄
入內山，而內山情勢複雜，因此搜捕的工作必須加快。昨日又有官員建議，
為了紀念這次事件，除了將諸羅改名嘉義外，臺灣二字也應該一併改名。我
認為這就是放著修建城池、增設兵卒的正經事不管，只留心在沒用的地方，
以後不許再提臺灣改名的事。」文中「逆首」最可能是下列何者？',
  '[{"key": "A", "text": "朱一貴"}, {"key": "B", "text": "林爽文"}, {"key": "C", "text": "余清芳"}, {"key": "D", "text": "莫那魯道"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  40,
  '某研究案根據1750至1850年代各國船
隻的航海日誌，將航行軌跡繪製成
圖(十一)。儘管船隻可能前往世界各
地，但仍以各國殖民地或勢力範圍為
主要目的地，例如圖中法國船隻，軌
跡主要集中於北美和西印度群島的法
國殖民地。圖中「甲」、「乙」最可
能是下列何者？',
  '[{"key": "A", "text": "甲：英國、乙：荷蘭"}, {"key": "B", "text": "甲：荷蘭、乙：西班牙"}, {"key": "C", "text": "甲：葡萄牙、乙：英國"}, {"key": "D", "text": "甲：西班牙、乙：葡萄牙"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  41,
  '甲國進口商小莫固定在每星期一、四，以 日期 受訪內容
相同乙幣價格，從乙國進口相同數量的某
就匯率來說，6 月初至
6 月 8 日
商品至國內販售，並在交易當天將甲幣 今，每次花費的成本一
星期一
兌換為乙幣完成付款，表(六)是他在2020 次比一次低。
年6月8日及6月22日的受訪內容。根據表
就匯率來說，今天所花
6 月 22 日
中內容判斷，下列何者最可能是該年6月 費的成本是 6 月至今各
星期一
時，每一甲幣兌換乙幣的匯率變化？ 次中最高的。',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": "10 請翻頁繼續作答"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  42,
  '「2023年4月15日，北非的蘇丹爆發內戰，民間武
裝集團突襲機場，衝突很快就從機場延燒到首都
喀土穆，現今戰事已延燒到蘇丹全境，各國也開始撤
離境內的外交人員及公民。」根據圖(十二)中的資訊
判斷，上述內戰爆發的影響最可能是下列何者？',
  '[{"key": "A", "text": "若內戰惡化，難民將會大量湧入鄰國肯亞"}, {"key": "B", "text": "蘇丹港若遭封鎖，將阻斷波斯灣的石油輸出"}, {"key": "C", "text": "南部橄欖園若遭破壞，將使全球橄欖油價格飆升"}, {"key": "D", "text": "若喀土穆被占領且鄰近大河遭控制，將影響埃及用水"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  43,
  '我國在2007年修正了《民法》中關於子女姓氏的規 表(七)
定，將原本子女從父姓的原則，修改為父母應以書
出生登記 約定
面方式，約定子女從父姓或從母姓。表(七)是2012至
年分 總人數 從母姓
2018年關於新生兒約定從母姓的統計數據。根據表 ( 人 ) 比例 (%)
中資料判斷，對於修法後新生兒姓氏的變化，下列
2012 229,760 1.5
何種說法最合理？
2013 199,113 1.6',
  '[{"key": "A", "text": "新生兒約定從母姓的比例顯示性別歧視日趨嚴重"}, {"key": "B", "text": "選擇新生兒姓氏時仍會受到其他社會規範的影響"}, {"key": "C", "text": "法律變遷促使多數人改變新生兒姓氏的選擇結果"}, {"key": "D", "text": "基於傳宗接代需求約定從母姓的新生兒多為男嬰"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  44,
  '依據上文，建物設置「五腳基」的目的，最可能為下列何者？',
  '[{"key": "A", "text": "防止蚊蟲及毒蛇的侵擾"}, {"key": "B", "text": "因應冬季道路積雪行走不便"}, {"key": "C", "text": "躲避強風發生時產生的沙塵暴"}, {"key": "D", "text": "避免溼熱氣候下強烈日晒及雨淋"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  45,
  '上文中提及的洋樓，最主要分布於下列中國的哪一地區？',
  '[{"key": "A", "text": "西部的高山地區"}, {"key": "B", "text": "北部的平原地區"}, {"key": "C", "text": "東南部沿海地區"}, {"key": "D", "text": "西北部綠洲地帶"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  46,
  '根據圖(十四)中內容判斷，阿華廣傳訊息所達成的效果，最可能是下列何者？',
  '[{"key": "A", "text": "透過社群網路影響公共意見"}, {"key": "B", "text": "善用大眾媒體爭取婚姻自由"}, {"key": "C", "text": "利用網路科技提供醫學新知"}, {"key": "D", "text": "成立民間團體推動法律變革"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  47,
  '根據表(八)與表(九)的資訊判斷，關於圖(十四)中阿華所傳遞的訊息，下列何
項解讀最適當？',
  '[{"key": "A", "text": "內容符合事實，因我國通過修法之後導致累積感染者人數增加"}, {"key": "B", "text": "內容符合事實，因我國的愛滋病毒盛行率比東南亞鄰近國家高"}, {"key": "C", "text": "內容與事實不符，因我國統計數據顯示新增感染者人數逐年減少"}, {"key": "D", "text": "內容與事實不符，因我國的愛滋病毒盛行率比歐、美先進國家低"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  48,
  '根據文中小明檢視網路訊息的過程判斷，顯示下列何者的重要性？',
  '[{"key": "A", "text": "對於跨越國界傳播的疾病，世界各國應共同合作防堵疫情"}, {"key": "B", "text": "對於各種媒體傳播的資訊，閱聽大眾應具備媒體識讀能力"}, {"key": "C", "text": "對於行政機關推動的政策，政府施政應秉持性別平等立場"}, {"key": "D", "text": "對於網路串流平臺的作品，使用者應避免侵害智慧財產權"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  49,
  '上文中所述最適合製糖的作物，其主要生長環境最可能為下列何者？',
  '[{"key": "A", "text": "年雨量小於500mm"}, {"key": "B", "text": "最冷月均溫10°C以下"}, {"key": "C", "text": "海拔1,000公尺以上的山坡地"}, {"key": "D", "text": "南緯25度到北緯25度之間的地區"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  50,
  '上文廠歌歌詞的創作背景及圖(十六)描繪的情景，與下列臺灣哪一產業發展階
段的特色最相符？',
  '[{"key": "A", "text": "外銷食品加工產品扶植國內輕工業"}, {"key": "B", "text": "設立加工出口區吸引大量外商投資"}, {"key": "C", "text": "因應石油危機推動交通、能源等基礎建設"}, {"key": "D", "text": "持續推動農業轉型升級並發展高科技產業"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  51,
  '上文提及糖廠的多元化發展，其最主要的目的為下列何者？',
  '[{"key": "A", "text": "降低生產的運輸成本"}, {"key": "B", "text": "減少粗糖的關稅成本"}, {"key": "C", "text": "提高產業的附加價值"}, {"key": "D", "text": "增加甘蔗的種植面積"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  52,
  '上述中國商人家族所經營的事業，最可能為下列何者？',
  '[{"key": "A", "text": "調查戶口作為掌握稅收依據"}, {"key": "B", "text": "投資鐵路興築與煤鐵礦開採"}, {"key": "C", "text": "承辦國營企業，推行大躍進"}, {"key": "D", "text": "設置市舶司，造船往來西洋"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  53,
  '文中「航空公路建設獎券」的發行，最可能與下列何者有關？',
  '[{"key": "A", "text": "改革開放在沿海設經濟特區"}, {"key": "B", "text": "北伐結束後十年建設的展開"}, {"key": "C", "text": "庚子後新政推動的改革項目"}, {"key": "D", "text": "因應能源危機推行十大建設"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'social',
  54,
  '上文中國人得以自由使用租界內體育場館，最可能與下列何者有關？',
  '[{"key": "A", "text": "甲午戰爭結束，中國對日本割地賠款"}, {"key": "B", "text": "一次大戰爆發，日本占領德國租借地"}, {"key": "C", "text": "日 俄戰爭結束，日本驅逐俄羅斯勢力"}, {"key": "D", "text": "太平洋戰爭爆發，日本向同盟國宣戰"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  1,
  '小翔將上皿天平靜置於水平桌面上，發現天平的指針靜止時偏向左邊，便進行
歸零的動作。已知天平歸零後，指針靜止時指在中央的刻度上，則小翔所作的
歸零動作最可能為下列何者？',
  '[{"key": "A", "text": "將左邊的校準螺絲向內旋入"}, {"key": "B", "text": "將兩端的校準螺絲均向內旋緊"}, {"key": "C", "text": "在左邊的秤盤上放上一張秤量紙"}, {"key": "D", "text": "使用砝碼夾將指針撥往中央的刻度"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  2,
  '下列為某種物質的介紹：
早在史前時代，人們就透過採礦、冶煉等過程，獲取「它」用以製造器
具等，對於早期人類文明的進步影響深遠。在自然界，它多數是和其他元素
結合，而以化合物的形式存在。它具有良好的導電性、導熱性和延展性，可
拉成細絲，製成很薄的箔片，因此電線、通訊電纜等多以它為原料。
上述中的「它」應屬於下列何種物質？',
  '[{"key": "A", "text": "化合物"}, {"key": "B", "text": "聚合物"}, {"key": "C", "text": "金屬元素"}, {"key": "D", "text": "非金屬元素"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  3,
  '鈍氣又稱惰性氣體，是指氦(He)、氖(Ne)、氬(Ar)等元素，位於週期表中的第18族，
這些元素具有下列何種性質？',
  '[{"key": "A", "text": "熔點均高於室溫"}, {"key": "B", "text": "有相似的化學性質"}, {"key": "C", "text": "有相似的物理性質"}, {"key": "D", "text": "均由雙原子所組成"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  4,
  '敏敏針對某段海岸線進行研究，他將不
同時期的海岸線套疊在2018年的海岸線
圖上，如圖(一)。根據圖中資訊，可呈現
出下列何項事實？',
  '[{"key": "A", "text": "2015至2016年，此段海岸線大致往陸地"}, {"key": "B", "text": "2017至2018年，此段海岸線大致往海"}, {"key": "C", "text": "從2015年開始，海岸線的沉積與侵蝕速率大致相等"}, {"key": "D", "text": "從2015年開始，對海岸線的侵蝕作用比沉積作用大"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  5,
  '如圖(二)，在水平地面上畫上正方形的方格，平面鏡
與牆壁互相垂直，且均豎立於地面上。若持雷射筆
在方格上S點或T點，令雷射光沿著水平面分別
照射平面鏡上的P、Q、R三點，則以下列何種方式
照射，其反射的雷射光不會照射到牆壁上？',
  '[{"key": "A", "text": "S → Q"}, {"key": "B", "text": "S → P"}, {"key": "C", "text": "T → R"}, {"key": "D", "text": "T → P"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  6,
  '圖(三)比較了斑馬魚幼魚與其構造和病毒的大小。圖(四)為透過顯微鏡觀察斑馬魚
幼魚時的畫面。根據圖中資訊，推測灰色斑塊最可能為下列何者？
圖(三) 圖(四)',
  '[{"key": "A", "text": "一個血紅素蛋白"}, {"key": "B", "text": "一個病毒"}, {"key": "C", "text": "一個粒線體"}, {"key": "D", "text": "一個細胞"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  3,
  '在劇烈搖晃前，學校的跑馬燈警示強度幾級的震波將在幾秒後到達。
某次地震發生後，某學校跑馬燈的警示如圖(六)。
圖(六)
根據上述資訊，我們可以得知下列何者？',
  '[{"key": "A", "text": "地震波到達後，會使學校持續搖晃13秒"}, {"key": "B", "text": "地震波到達後，會使各縣市都有震度4級的搖晃"}, {"key": "C", "text": "在劇烈搖晃前，大約有13秒的時間可以避難"}, {"key": "D", "text": "在劇烈搖晃前，可得知此地震釋放的能量為規模4"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  9,
  '在冬季轉換為春季且濕度大的時候，若室內的溫度比室外低，空氣吹入室內很容
易在磁磚牆面形成水珠，此現象稱為返潮。關於上述空氣吹入室內在磁磚牆面
形成水珠的說明，下列何者最合理？',
  '[{"key": "A", "text": "空氣內的水分遇到較高溫的牆面凝結而形成"}, {"key": "B", "text": "空氣內的水分遇到較高溫的牆面汽化而形成"}, {"key": "C", "text": "空氣內的水分遇到較低溫的牆面凝結而形成"}, {"key": "D", "text": "空氣內的水分遇到較低溫的牆面汽化而形成"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  10,
  '圖(七)為人體的中樞神經系統示意圖。阿強參加賽跑
時，一聽到槍聲響起便邁開步伐起跑，關於此過程涉
及的神經系統運作，下列敘述何者正確？',
  '[{"key": "A", "text": "由甲產生槍聲的聽覺"}, {"key": "B", "text": "由乙調節呼吸的快慢"}, {"key": "C", "text": "由丙維持身體的平衡"}, {"key": "D", "text": "由丁主掌步伐的大小"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  11,
  '圖(八)記錄了某人盡力吸氣後、盡力呼氣後，肺部中分別容納
的氣體量。依此圖判斷胸腔變化，下列敘述何者正確？',
  '[{"key": "A", "text": "動作甲：橫膈上升且肋骨上舉"}, {"key": "B", "text": "動作甲：橫膈下降且肋骨下降"}, {"key": "C", "text": "動作乙：橫膈上升且肋骨下降"}, {"key": "D", "text": "動作乙：橫膈下降且肋骨上舉"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  4,
  '將產物分離出來並測量其質量，結果如表(一)：
表(一)
從上述資訊，是否可知道鹼的濃度與反應速率之關係？',
  '[{"key": "A", "text": "可以，鹼的濃度加倍，反應速率會變快為四倍"}, {"key": "B", "text": "可以，鹼的濃度增加，反應速率會先增後微降"}, {"key": "C", "text": "不行，因為本實驗所使用鹼的濃度並不相同"}, {"key": "D", "text": "不行，因為實驗並未記錄各組反應所需的時間"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  13,
  '人類早在幾千年前就開始種植「玉米的祖先」作為糧食，但其口感和
現在的玉米差異極大。經過長時間的育種，人類不斷利用具有某些特徵的
植株進行雜交，漸漸地，雜交植株產生的「玉米粒」從原本較小且具有堅硬
外殼的樣貌，變成趨近於現代玉米的樣貌。
上述人類對玉米育種過程的敘述，下列何者最合理？',
  '[{"key": "A", "text": "經由營養器官進行無性生殖"}, {"key": "B", "text": "經由生殖器官進行有性生殖"}, {"key": "C", "text": "親代與子代的表現型都相同"}, {"key": "D", "text": "親代與子代的基因型都相同"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  14,
  '小芳連續14天朝南方觀察住家附近的月相，其中第8天到第14天的月相如圖(九)。
圖(九)
根據觀察結果，下列何者最可能是他前7天所觀察到的月相變化？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  15,
  '阿笙和朋友某日傍晚5點到海邊時，發現海水水位在當天最高的位置，便和
朋友相約隔日再來。已知此地每天有兩次乾潮與兩次滿潮，若隔日他們想在
海水退潮期間的一半到達此地，選擇下列哪個時段最合適？',
  '[{"key": "A", "text": "上午5點～6點"}, {"key": "B", "text": "上午8點～9點"}, {"key": "C", "text": "上午11點～12點"}, {"key": "D", "text": "下午2點～3點"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  16,
  '小忠被室友大勇的打鼾聲吵得無法入眠，因此決定用手機量測大勇睡著時的
打鼾聲，以實際數據來呈現此問題，其過程如圖(十)：
圖(十)
以上對話中「……」處小忠說出下列哪一句話，最符合他想呈現的問題？',
  '[{"key": "A", "text": "你發出70 dB的打鼾聲"}, {"key": "B", "text": "你發出250 Hz的打鼾聲"}, {"key": "C", "text": "你發出的打鼾聲每秒傳播340 m"}, {"key": "D", "text": "你發出的打鼾聲振動一次只要0.004秒"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  17,
  '已知甲、乙兩星體位於太陽系，筱萍提出兩種方式判斷星體層級，如圖(十一)。
根據恆星與其他星體的主要區分方法，圖中方式一與方式二是否正確？',
  '[{"key": "A", "text": "僅方式一正確"}, {"key": "B", "text": "僅方式二正確"}, {"key": "C", "text": "兩種方式皆正確"}, {"key": "D", "text": "兩種方式皆錯誤"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  18,
  '將物品放入圖(十二)的量筒中，由物品放入前、後的液面刻度差，可知該物品的
體積。下列何者適合以上述方法測量其體積？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  19,
  '「天然氣的主成分是甲烷(CH )，已知產生相同熱量時，燃燒天然氣的二氧化碳
4
(CO )排放量約只有燃燒煤炭的一半，儘管如此，燃燒1公噸的甲烷仍會產生
2
數公噸的二氧化碳，與淨零碳排放的目標有差異。」若要知道上述數公噸
二氧化碳排放量的實際值為多少，需要甲烷和二氧化碳的下列何項資訊才能
計算出來？',
  '[{"key": "A", "text": "沸點"}, {"key": "B", "text": "密度"}, {"key": "C", "text": "比熱"}, {"key": "D", "text": "分子量"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  20,
  '蝦子的頭部有個稱為「觸角腺」的構造，可以過濾體內的液體，再將其中有用
的物質吸收，並排出多餘的含氮廢物。依上述資訊推測，觸角腺的功能最類似
人體哪個器官的功能？',
  '[{"key": "A", "text": "肝臟"}, {"key": "B", "text": "大腸"}, {"key": "C", "text": "腎臟"}, {"key": "D", "text": "尿道"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  21,
  '某魚池中原僅有黑色鯉魚，小瑛將50隻紅色鯉魚放入此魚池。一段時間後，再
由此魚池隨機捕捉50隻鯉魚，發現其中5隻為紅色鯉魚。若從放入鯉魚到捕捉
前，沒有鯉魚遷入、遷出、出生、死亡，且根據捉放法計算出來的黑色鯉魚數
量為 X，則下列敘述何者正確？',
  '[{"key": "A", "text": "X為500隻，此數值為黑色鯉魚的實際數量"}, {"key": "B", "text": "X為500隻，此數值為黑色鯉魚的可能數量"}, {"key": "C", "text": "X為450隻，此數值為黑色鯉魚的實際數量"}, {"key": "D", "text": "X為450隻，此數值為黑色鯉魚的可能數量"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  22,
  '小明進行圖(十三)中的四次實驗，實驗中的槓桿、砝碼皆相同，槓桿每段長度皆
為5 cm，進行實驗一、二後，他根據結果推論出論點一，進行實驗三後，他
提出論點二，之後進行實驗四，則下列敘述何者最合理？
圖(十三)',
  '[{"key": "A", "text": "實驗三的結果與論點一相符"}, {"key": "B", "text": "實驗四的結果與論點一不相符"}, {"key": "C", "text": "實驗四的結果可以證明論點二不正確"}, {"key": "D", "text": "實驗四的結果無法使用論點二來說明"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  23,
  '網路流傳一種說法：「使用加食鹽的熱水拖地，地板會
比較快乾。」小綺想要找出影響地板乾燥速率的變因，
使用表(二)中四組的水來拖地，當中的哪兩組相互比較，
最不可能達到他的目的？',
  '[{"key": "A", "text": "第一組和第二組"}, {"key": "B", "text": "第一組和第三組"}, {"key": "C", "text": "第二組和第三組"}, {"key": "D", "text": "第二組和第四組"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  24,
  '已知綠色植物可同時進行光合作用與呼吸作用，而光合作用的過程如下：
關於甲、乙、丙三種物質的敘述，下列何者最合理？',
  '[{"key": "A", "text": "甲主要由植物從土壤中吸收"}, {"key": "B", "text": "乙主要由植物根部排出至土壤"}, {"key": "C", "text": "乙與呼吸作用的產物相同"}, {"key": "D", "text": "丙可作為呼吸作用的反應物"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  25,
  '若某動物的黑白毛色僅由一對遺傳因子控制，黑色為顯性的特徵、白色為隱性的
特徵。斌斌以黑棋代表顯性遺傳因子、白棋代表隱性遺傳因子，進行毛色遺傳的
模擬實驗，於甲、乙兩個袋子皆放入50顆黑棋與50顆白棋混勻，再分別從兩袋
各隨機抽出一顆棋子配對並記錄結果，接著各自放回原袋中混勻，反覆進行100次
配對。關於結果紀錄中，毛色為黑、毛色為白的子代數量，最可能依序為何？',
  '[{"key": "A", "text": "49、51"}, {"key": "B", "text": "78、22"}, {"key": "C", "text": "26、74"}, {"key": "D", "text": "100、0"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  26,
  '如圖(十四)，圖中某海域東、西兩側的陸地，受到板塊間相互運動的影響，距離
逐年增加，此海域面積有逐漸擴大的趨勢。根據上述資訊，下列推論何者最合理？',
  '[{"key": "A", "text": "此海域底部可發現岩漿湧出所形成的火成岩"}, {"key": "B", "text": "此海域底部可發現地球上最古老的海洋地殼"}, {"key": "C", "text": "圖中此海域東、西兩側的陸地目前在同一板塊上"}, {"key": "D", "text": "圖中此海域東、西兩側的陸地之間有海溝的存在"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  27,
  '小華想藉由某地的氣象觀測資料來區分
當地的對流層和平流層，他預計繪製的
圖表橫軸與縱軸資料類型如圖(十五)。依
據上述資訊，關於甲、乙兩圖呈現的趨勢
是否可用來區分對流層和平流層的說明，
下列何者最合理？ 圖(十五)',
  '[{"key": "A", "text": "甲圖可以，因氣溫在對流層隨高度上升而降低，在平流層則不會"}, {"key": "B", "text": "乙圖可以，因氣壓在對流層隨高度上升而降低，在平流層則不會"}, {"key": "C", "text": "兩圖都不可以，因氣溫與氣壓無論在對流層或平流層皆大致固定"}, {"key": "D", "text": "兩圖都可以，因氣溫與氣壓在對流層皆隨高度上升而降低，在平流層則不會"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  28,
  '延長線可延長電器的使用距離，並讓多個電器使用
同一插座，圖(十六)為一延長線外包裝的安全注意
事項，其中「壓鈕」的功能等同於無熔絲開關，則
關於此注意事項中的超載，最可能是指下列何者？',
  '[{"key": "A", "text": "流經電器的電流值超過電器可負荷的最大電流值"}, {"key": "B", "text": "輸入電器的電壓值超過電器可負荷的最大電壓值"}, {"key": "C", "text": "流經延長線的電流值超過延長線可負荷的最大"}, {"key": "D", "text": "輸入延長線的電壓值超過延長線可負荷的最大"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  29,
  '穿山龍為一種藥用植物，也俗稱棒槌瓜，葉呈掌狀，花朵為白色，種子的構造具有翅。
根據上述資訊，下列推論何者最合理？',
  '[{"key": "A", "text": "棒槌瓜的學名為穿山龍"}, {"key": "B", "text": "成熟葉背可見孢子囊堆"}, {"key": "C", "text": "其植株具有果實的構造"}, {"key": "D", "text": "其植株具有毬果的構造"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  30,
  '將甲、乙、丙三個質量相等的金屬塊，分別以相同
的穩定熱源加熱，其溫度(T)與加熱時間(t)的關係如
圖(十七)。若加熱過程中無熱量散失，甲、乙、丙的
比熱分別為S 、S 、S ，則下列比熱的大小關係何者
甲 乙 丙
最合理？',
  '[{"key": "A", "text": "S ＝S ＜S"}, {"key": "B", "text": "S ＝S ＞S"}, {"key": "C", "text": "S"}, {"key": "D", "text": "S ＞S ＝S"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  31,
  '下列選項為在金屬鑰匙上鍍銅的電鍍裝置示意圖，圖中直流電源正、負極的標示
和電鍍液中銅離子的移動方向，何者正確？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  32,
  '一個密度均勻的長方體木塊，長、寬、高分別為30 cm、20 cm、10 cm，置於水
平桌面，此時木塊對於桌面所造成的壓力為 P。今先將此木塊的長截去10 cm，
即甲部分，再將寬截去10 cm，即乙部分，最後將高截去2 cm，即丙部分，如
圖(十八)，則此時木塊對桌面所造成的壓力應為下列何者？
4',
  '[{"key": "A", "text": "P"}, {"key": "B", "text": "P"}, {"key": "C", "text": "P"}, {"key": "D", "text": "3P"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  33,
  '將一個陶瓷材質的碗放入水槽中，碗內裝有水，碗體為實心，圖(十九)中甲、
乙分別為靜止平衡時的假想剖面示意圖。已知此種陶瓷的密度大於水，根據
「碗內外的水面高度」，判斷甲、乙兩張示意圖是否合理？',
  '[{"key": "A", "text": "甲、乙都合理"}, {"key": "B", "text": "甲、乙都不合理"}, {"key": "C", "text": "甲合理、乙不合理"}, {"key": "D", "text": "甲不合理、乙合理"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  34,
  '圖(二十) 為某網站分析
臺灣在此季節較為乾熱，
而日本、中國多發生暴雨
原因時所使用的示意圖，
圖中粗黑曲線為等壓線，
甲為某天氣系統，而受到
甲 與 圖 中 北 方 高 壓 的
影響，使鋒面長期存在於
日本到中國間，導致圖中
的區域暴雨。根據上述
資訊，圖中的甲以及所提到
的鋒面最可能為下列何者？
圖(二十)',
  '[{"key": "A", "text": "甲為低氣壓，鋒面是冷鋒"}, {"key": "B", "text": "甲為低氣壓，鋒面是滯留鋒"}, {"key": "C", "text": "甲為高氣壓，鋒面是冷鋒"}, {"key": "D", "text": "甲為高氣壓，鋒面是滯留鋒"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  35,
  '圖(二十ㄧ)中四個磁針的黑色部分代表 N 極，且均放置於
水平桌面上導線的正上方。小惠想藉由觀察磁針是否發生偏
轉來判斷電路的電流是否接通，則下列哪一個磁針最不適合
作為判斷的依據？',
  '[{"key": "A", "text": "甲"}, {"key": "B", "text": "乙"}, {"key": "C", "text": "丙"}, {"key": "D", "text": "丁"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  36,
  '取20 g蔗糖置入20 g水中，攪拌均勻後得到甲杯水溶液，另取30 g蔗糖置入20 g
水中，攪拌均勻後得到乙杯水溶液。已知蔗糖均完全溶解，則甲和乙兩杯蔗糖
水溶液的重量百分率濃度比是多少？',
  '[{"key": "A", "text": "1：1"}, {"key": "B", "text": "2：3"}, {"key": "C", "text": "4：5"}, {"key": "D", "text": "5：6"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  37,
  '蘇蘇在試管中加入蛋白質溶液與人體消化液中以
蛋白質為受質的某酵素，充分混合後放置於適宜
作用的穩定環境，蘇蘇接著每隔一段時間測量試管
中蛋白質與 X 物質的濃度，結果如圖(二十二)。已
知X物質為蛋白質被分解後的產物，則關於此 0
酵素的推論，下列何者最合理？
圖(二十二)',
  '[{"key": "A", "text": "可能由膽汁中取得此酵素"}, {"key": "B", "text": "可能由胰液中取得此酵素"}, {"key": "C", "text": "此酵素催化 X 物質的分解"}, {"key": "D", "text": "此酵素催化 X 物質的合成"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  38,
  '圖(二十三)為嘉義在6/1～隔年1/1的白天
時數變化圖，已知某城市位於北半球且緯度
比臺灣高，則下列有關此城市與嘉義在
相同日期間的白天時數圖，何者最合理？
圖(二十三)',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": ""}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  39,
  '甲、乙兩人討論從人體肺臟、肝臟流出的血液進入心臟之路徑，以下為兩人看法：
甲：肺臟流出的血液會由血管最先進入右心房。
乙：肝臟流出的血液會由血管最先進入右心室。
甲、乙兩人的看法是否正確？',
  '[{"key": "A", "text": "僅甲正確"}, {"key": "B", "text": "僅乙正確"}, {"key": "C", "text": "兩人皆正確"}, {"key": "D", "text": "兩人皆錯誤"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  41,
  '地表附近有甲、乙、丙三個相同的
小球，分別受到F 、F 、F 三個鉛
甲 乙 丙
直向上的外力作用，外力作用時小球
的運動情形如圖(二十五)。若過程中
重力加速度大小固定，且不考慮空
氣阻力，則三個外力的大小關係
應為下列何者？',
  '[{"key": "A", "text": "F ＝F ＜F"}, {"key": "B", "text": "F ＝F ＞F"}, {"key": "C", "text": "F ＞F ＞F"}, {"key": "D", "text": "F ＞F ＞F"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  42,
  '圖(二十七)中，造成兩種結果差異的其其他他原原因因，最可能為下列何者？',
  '[{"key": "A", "text": "該市酸雨的發生機率高，超過50%"}, {"key": "B", "text": "環保署與該市環保局對於酸雨的定義不同"}, {"key": "C", "text": "環保署所測出的該市雨水pH值太接近5.0"}, {"key": "D", "text": "單一測站的測量結果會與多個測站平均值有差異"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  43,
  '將表(三)的資料分成甲、乙兩組，最可能是想用來了解下列哪一個問題？',
  '[{"key": "A", "text": "位於東北季風迎、背風面是否會影響判定酸雨的標準"}, {"key": "B", "text": "位於東北季風迎、背風面是否會影響雨水pH值的平均"}, {"key": "C", "text": "各地區雨水pH值的平均高低是否影響酸雨發生的機率"}, {"key": "D", "text": "各地區雨水pH值的平均高低是否影響人為汙染物的種類"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  44,
  '根據本文，下列對圖(二十九)數據的敘述何者正確？',
  '[{"key": "A", "text": "0～1時之間沒有發生蒸散作用"}, {"key": "B", "text": "3～4時之間沒有發生蒸散作用"}, {"key": "C", "text": "12～13時的平均蒸散速率為一天中最大值"}, {"key": "D", "text": "6～7時的平均蒸散速率較7～8時的平均蒸散速率大"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  45,
  '若依據暄暄的方式操作實驗，但將實驗裝置移至通風良好的乾燥室內放置
兩天，則最不可能發生下列哪一種情況？',
  '[{"key": "A", "text": "第一、二天記錄到的氣泡移動距離總和相近"}, {"key": "B", "text": "在兩天的相同時段中，氣泡移動的距離相近"}, {"key": "C", "text": "植物氣孔關閉減緩蒸散，使管中氣泡移動量很小"}, {"key": "D", "text": "植物從氣孔吸收水分向下運輸，使管中氣泡向左移動"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  46,
  '科學家想要觀察水滴以不同的速度，衝擊石英板時的變化情形，若不考慮空氣
阻力，則他調整下列哪一項實驗條件最合理？',
  '[{"key": "A", "text": "調整水滴的溫度，以改變水滴的密度"}, {"key": "B", "text": "調整針頭的孔徑，以改變水滴的直徑與重量"}, {"key": "C", "text": "調整針頭的高度，以改變水滴落下的垂直距離"}, {"key": "D", "text": "調整攝影機的設定，以改變攝影機每秒拍攝畫面的張數"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  47,
  '根據本文，已知石英板作用在水滴的力為F ′，F′即F的反作用力，則
圖(三十一)中呈現的四個狀態，哪一個狀態下F′的大小最大？',
  '[{"key": "A", "text": ""}, {"key": "B", "text": ""}, {"key": "C", "text": ""}, {"key": "D", "text": "13"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  48,
  '組別一、四通入針筒內的兩種氣體，可依序使用下列何種反應來製備？',
  '[{"key": "A", "text": "鹽酸和鎂帶反應、雙氧水分解反應"}, {"key": "B", "text": "鹽酸和鎂帶反應、鹽酸和碳酸鈣反應"}, {"key": "C", "text": "雙氧水分解反應、鹽酸和鎂帶反應"}, {"key": "D", "text": "雙氧水分解反應、鹽酸和碳酸鈣反應"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  49,
  '若忽略針筒內鐵粉所占去的體積，試判斷組別二針筒內的氧氣是否完全耗盡？',
  '[{"key": "A", "text": "全耗盡，消耗氣體比例等於氧氣含量"}, {"key": "B", "text": "全耗盡，消耗氣體比例已超過氧氣含量"}, {"key": "C", "text": "未耗盡，消耗氣體比例高於氧氣含量的"}, {"key": "D", "text": "未耗盡，消耗氣體比例接近氧氣含量的一半"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'science',
  50,
  '依據活性大小，判斷組別四針筒內的鐵粉理論上是否與氣體發生氧化還原反應？',
  '[{"key": "A", "text": "因鐵的活性較小，故鐵粉不會被氧化"}, {"key": "B", "text": "因鐵的活性較小，反應後鐵粉會被氧化"}, {"key": "C", "text": "因鐵的活性較小，反應後氣體會被氧化"}, {"key": "D", "text": "因鐵的活性較大，反應後鐵粉會被氧化"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  1,
  'Look at the picture. All of the students who are exercising are wearing .',
  '[{"key": "A", "text": "caps"}, {"key": "B", "text": "glasses"}, {"key": "C", "text": "jackets"}, {"key": "D", "text": "pants"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  2,
  'Rita her dogs many times a day. That’s why they’re too fat.',
  '[{"key": "A", "text": "feeds"}, {"key": "B", "text": "kisses"}, {"key": "C", "text": "walks"}, {"key": "D", "text": "washes"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  3,
  'You can ask Sophia anything about butterflies and bees. She has great of insects.',
  '[{"key": "A", "text": "chances"}, {"key": "B", "text": "knowledge"}, {"key": "C", "text": "news"}, {"key": "D", "text": "power"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  4,
  'Adam slept last night because he kept waking up from bad dreams.',
  '[{"key": "A", "text": "deeply"}, {"key": "B", "text": "early"}, {"key": "C", "text": "terribly"}, {"key": "D", "text": "quickly"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  5,
  'Tara enjoys being with all kinds of animals; she even a snake as a pet.',
  '[{"key": "A", "text": "drops"}, {"key": "B", "text": "gives"}, {"key": "C", "text": "keeps"}, {"key": "D", "text": "makes"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  6,
  'Little Eric chose the doll big brown eyes because it was the cutest in the store.',
  '[{"key": "A", "text": "at"}, {"key": "B", "text": "in"}, {"key": "C", "text": "on"}, {"key": "D", "text": "with"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  7,
  'After four hours of mountain climbing, Rosa’s legs got , so she took a rest on the top
of the mountain.',
  '[{"key": "A", "text": "dirty"}, {"key": "B", "text": "sick"}, {"key": "C", "text": "sore"}, {"key": "D", "text": "strong"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  8,
  'Having three cups of coffee a day can’t be bad for our health, ?',
  '[{"key": "A", "text": "can it"}, {"key": "B", "text": "can they"}, {"key": "C", "text": "is it"}, {"key": "D", "text": "are they"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  9,
  'You can’t push that door open with only one hand. It’s too heavy. You have to use !',
  '[{"key": "A", "text": "all"}, {"key": "B", "text": "another"}, {"key": "C", "text": "both"}, {"key": "D", "text": "one"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  10,
  'Alan works hard in his new job, and he wants to know his boss feels about him.',
  '[{"key": "A", "text": "how"}, {"key": "B", "text": "that"}, {"key": "C", "text": "whether"}, {"key": "D", "text": "why"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  11,
  'I thought the girl was Kate, but it was her sister, Candy. They sounded almost the
same.',
  '[{"key": "A", "text": "answered the phone"}, {"key": "B", "text": "she answered the phone"}, {"key": "C", "text": "who answered the phone"}, {"key": "D", "text": "and answered the phone"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  12,
  'Ken is going abroad with a woman he met online, though he doesn’t know well.',
  '[{"key": "A", "text": "her"}, {"key": "B", "text": "each other"}, {"key": "C", "text": "any"}, {"key": "D", "text": "another"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  13,
  'Joe is happy he is not at the of the class now. His grades are better than half of his
classmates’ this school year.',
  '[{"key": "A", "text": "side"}, {"key": "B", "text": "front"}, {"key": "C", "text": "center"}, {"key": "D", "text": "bottom"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  14,
  'Look! There is not a cloud in the sky. I think the chances of getting some rain today are
really .',
  '[{"key": "A", "text": "far"}, {"key": "B", "text": "good"}, {"key": "C", "text": "possible"}, {"key": "D", "text": "small"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  15,
  'On windy days, the flowers in my garden like shy children with their heads down.',
  '[{"key": "A", "text": "bow"}, {"key": "B", "text": "fall"}, {"key": "C", "text": "rise"}, {"key": "D", "text": "smell"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  16,
  'Mr. Olson went to the doctor when he found he his hair. He hoped he would be able
to keep his thick hair.',
  '[{"key": "A", "text": "was losing"}, {"key": "B", "text": "is losing"}, {"key": "C", "text": "will lose"}, {"key": "D", "text": "has lost"}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  17,
  'Do you know what Lindsey’s first job was? Before becoming a movie star, she the
floors at the supermarket.',
  '[{"key": "A", "text": "mops"}, {"key": "B", "text": "is mopping"}, {"key": "C", "text": "has mopped"}, {"key": "D", "text": "mopped"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  18,
  'Our dog Lassie hides under the bed every time the moon comes out. She has been for
years, but we don’t know why.',
  '[{"key": "A", "text": "it"}, {"key": "B", "text": "like this"}, {"key": "C", "text": "like us"}, {"key": "D", "text": "that"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  19,
  'Tom: Sam, could you help me in the kitchen now?
Sam: No, I TV. It’s the most important game of the season.',
  '[{"key": "A", "text": "watch"}, {"key": "B", "text": "watched"}, {"key": "C", "text": "have watched"}, {"key": "D", "text": "am watching"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  20,
  'Amanda wants to make fruit tea by following The Best Fruit Tea You Can Make at Home.
She has several kinds of fruit in the kitchen: apples, bananas, oranges, papayas, pears, and
strawberries. Which are some of the fruits she can use to make the fruit tea?',
  '[{"key": "A", "text": "Oranges, papayas and pears."}, {"key": "B", "text": "Apples, bananas and oranges."}, {"key": "C", "text": "Apples, oranges and strawberries."}, {"key": "D", "text": "Bananas, papayas and strawberries."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  21,
  'According to the reading, which is correct when we make the fruit tea?',
  '[{"key": "A", "text": "Boiling water with sugar in it."}, {"key": "B", "text": "Making sure to take out the fruit."}, {"key": "C", "text": "Putting in the fruit and the lemon juice at the same time."}, {"key": "D", "text": "Leaving the teabags in the pot of hot water for 2 to 3 minutes."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  22,
  'According to the comics, what kind of person is Hawkins?',
  '[{"key": "A", "text": "He sees good things in people."}, {"key": "B", "text": "He never goes to work on time."}, {"key": "C", "text": "He blindly follows other people."}, {"key": "D", "text": "He talks about things he can’t do."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  23,
  'What does it mean when we say someone bombed something?',
  '[{"key": "A", "text": "They gave it up."}, {"key": "B", "text": "They failed at it."}, {"key": "C", "text": "They were fine with it."}, {"key": "D", "text": "They were careful about it."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  24,
  'Which question can the brochure answer?',
  '[{"key": "A", "text": "Can I order tickets online?"}, {"key": "B", "text": "How much are the tickets?"}, {"key": "C", "text": "How can I get to the Marigolds’ Home?"}, {"key": "D", "text": "When can I visit the Marigolds’ Home?"}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  25,
  'What breaks the rules for visitors to the Marigolds’ Home?',
  '[{"key": "A", "text": "Eating burgers in the Rose Garden."}, {"key": "B", "text": "Taking pictures in the Main House."}, {"key": "C", "text": "Entering the Rabbit’s Temple without shoes."}, {"key": "D", "text": "Taking pet dogs for a walk on the playground."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  26,
  'After shopping at the gift shop of the Main House, Lizzy walks out and sees the Family
Library in front of her. She wants to visit the Rose Garden. How can she get there?',
  '[{"key": "A", "text": "Turn left and walk past the Main House, then go straight and turn right at the corner."}, {"key": "B", "text": "T urn left and walk past Sir Archie’s House, then turn right and walk past the Main"}, {"key": "C", "text": "T urn right and go straight to the Farmyard, then turn right and go straight, then turn left"}, {"key": "D", "text": "Turn right and walk through the Butterfly Garden, then walk past the Rabbit’s Temple"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  27,
  'Why was Beatrice Harrison called the Nightingale Lady?',
  '[{"key": "A", "text": "She wrote songs about nightingales."}, {"key": "B", "text": "She sang as beautifully as a nightingale did."}, {"key": "C", "text": "She taught nightingales to sing in a radio show."}, {"key": "D", "text": "She was famous for playing music with nightingales."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  28,
  'Which is NOT used in the reading to mean the nightingale(s) ?',
  '[{"key": "A", "text": "Her visitor."}, {"key": "B", "text": "The little singers."}, {"key": "C", "text": "The artist."}, {"key": "D", "text": "Her garden friends."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  29,
  'Why does Alex Jackson write about Rose Lacey?',
  '[{"key": "A", "text": "Because she died."}, {"key": "B", "text": "Because she is very sick."}, {"key": "C", "text": "Because she is moving away."}, {"key": "D", "text": "Because she is leaving for another job."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  30,
  'How did Rose Lacey and Alex Jackson get to know each other?',
  '[{"key": "A", "text": "They met at a party."}, {"key": "B", "text": "They were relatives."}, {"key": "C", "text": "They worked in the same office."}, {"key": "D", "text": "They took a course on movies together."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  31,
  'What is special about Rose Lacey’s articles?',
  '[{"key": "A", "text": "They are important to movie makers."}, {"key": "B", "text": "They talk about movies from a fresh angle."}, {"key": "C", "text": "They give interesting information about actors."}, {"key": "D", "text": "They are good examples of how to write stories."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  32,
  'Why does the title say “Glass Bottles’ Second Life” ?  title 標題',
  '[{"key": "A", "text": "People collect sea glass and use it to make new glass bottles."}, {"key": "B", "text": "People collect sea glass at the beach and use it to make wishes."}, {"key": "C", "text": "Glass bottles that are thrown into the sea become the homes of sea animals."}, {"key": "D", "text": "Glass bottles that are thrown into the sea become sea glass which is used in art pieces."}]'::jsonb,
  'D',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  33,
  'According to the reading, how is sea glass made?',
  '[{"key": "A", "text": "Sea glass becomes rounder after it is pushed up to the beach."}, {"key": "B", "text": "Colder sea water helps pieces of glass become sea glass faster."}, {"key": "C", "text": "Pieces of glass become white on the outside after many years in the sea."}, {"key": "D", "text": "Glass bottles break into pieces when they are dug out from the sea floor."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  34,
  'According to the reading, why will less sea glass be found in the future?',
  '[{"key": "A", "text": "People do not make as many glass items as before."}, {"key": "B", "text": "People have learned not to throw garbage into the sea."}, {"key": "C", "text": "Artists are using too much sea glass in their art pieces."}, {"key": "D", "text": "Waves are not big enough to push sea glass up to the beach."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  35,
  'What does the prevalence of English mean?',
  '[{"key": "A", "text": "That English is very common."}, {"key": "B", "text": "That English is not welcomed."}, {"key": "C", "text": "That English is easy and simple."}, {"key": "D", "text": "That English is not a national language."}]'::jsonb,
  'A',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  36,
  'In the first reading, which is one of the ways that Anna Adams uses to make readers believe
in her ideas?',
  '[{"key": "A", "text": "Sharing her own life stories."}, {"key": "B", "text": "Borrowing from people’s experience."}, {"key": "C", "text": "Using examples from another language."}, {"key": "D", "text": "Showing information from news reports."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  37,
  'Which words in the second reading are NOT used to describe Icelandic?',
  '[{"key": "A", "text": "A language in its sickbed."}, {"key": "B", "text": "A dying language."}, {"key": "C", "text": "Our first language."}, {"key": "D", "text": "This beautiful language."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  38,
  'Are Anna Adams and Gunnar Eggertsson worried about the future of Icelandic?',
  '[{"key": "A", "text": "No, they are not."}, {"key": "B", "text": "Yes, they both are."}, {"key": "C", "text": "Adams is, but Eggertsson is not."}, {"key": "D", "text": "Adams is not, but Eggertsson is."}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  39,
  'Which idea do Anna Adams and Gunnar Eggertsson both talk about in the readings?',
  '[{"key": "A", "text": "Whether Icelanders speak better English than Icelandic."}, {"key": "B", "text": "Whether the number of Icelandic speakers is big enough."}, {"key": "C", "text": "Whether school subjects should be taught only in Icelandic."}, {"key": "D", "text": "Whether Iceland should allow more foreigners to work in Iceland."}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  40,
  '(A) give you a piece of good land
(B) choose a person to be the next king
(C) put the beautiful ones in my castle
(D) decide who will work in my garden',
  '[{"key": "A", "text": "give you a piece of good land"}, {"key": "B", "text": "choose a person to be the next king"}, {"key": "C", "text": "put the beautiful ones in my castle"}, {"key": "D", "text": "decide who will work in my garden"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  41,
  '(A) But he lost his pot a few weeks later
(B) Months passed but nothing grew from it
(C) But soon the plant that grew from it died
(D) The seed grew into a big tree in a short time',
  '[{"key": "A", "text": "But he lost his pot a few weeks later"}, {"key": "B", "text": "Months passed but nothing grew from it"}, {"key": "C", "text": "But soon the plant that grew from it died"}, {"key": "D", "text": "The seed grew into a big tree in a short time"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  42,
  '(A) the last one to give up
(B) the first one to share good news
(C) the first one to bring his pot to the king
(D) the only one to take good care of his plant',
  '[{"key": "A", "text": "the last one to give up"}, {"key": "B", "text": "the first one to share good news"}, {"key": "C", "text": "the first one to bring his pot to the king"}, {"key": "D", "text": "the only one to take good care of his plant"}]'::jsonb,
  'B',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
insert into exam_questions (exam_name, subject, question_number, question_text, options, correct_option, has_figure) values (
  '115年國中教育會考',
  'english_reading',
  43,
  '(A) wise
(B) strong
(C) honest
(D) popular
14 試題結束',
  '[{"key": "A", "text": "wise"}, {"key": "B", "text": "strong"}, {"key": "C", "text": "honest"}, {"key": "D", "text": "popular"}]'::jsonb,
  'C',
  false
) on conflict (exam_name, subject, question_number) do update set
  question_text = excluded.question_text,
  options = excluded.options,
  correct_option = excluded.correct_option,
  has_figure = excluded.has_figure;
