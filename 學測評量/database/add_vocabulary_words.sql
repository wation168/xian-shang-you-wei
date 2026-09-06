-- ============================================================
-- vocabulary_words 資料表建立 + 資料匯入
-- 來源：pedia.cloud.edu.tw 教育百科生字詞彙表（老師會員貢獻，
--       非出版社官方逐字校對，但紮根於真實課本）
-- 範圍：目前只涵蓋114學年度下學期，之後可補上學期
-- 產生時間：2026/08/01
-- ============================================================

-- 1. 建立 vocabulary_words 表
create table vocabulary_words (
  id              uuid primary key default gen_random_uuid(),
  curriculum_id   uuid not null references curriculum(id) on delete cascade,
  words_preview   text not null,   -- 生字/詞彙預覽清單（逗號分隔，來源網站僅顯示前幾個+刪節號，非完整清單）
  source          text not null default '教育百科生字詞彙表',
  created_at      timestamptz not null default now()
);

create index idx_vocabulary_words_curriculum on vocabulary_words(curriculum_id);

-- ============================================================
-- 國語：206/207筆沿用既有curriculum課次，1筆新課次另外補上
-- ============================================================

insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='南一' and lesson_number=1),
  '充,太,開心,大哭,青草...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='南一' and lesson_number=2),
  '蜻,蜓,顏色,綠色,蜻蜓...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='南一' and lesson_number=3),
  '樂,音,入口,會場,布置...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='南一' and lesson_number=4),
  '誰,跟,恐,龍,豚...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='南一' and lesson_number=5),
  '輕,給,輕輕,突然,可是...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='南一' and lesson_number=6),
  '居,孩,常,躲,發...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='南一' and lesson_number=7),
  '啊,師,老,謝,感...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='南一' and lesson_number=8),
  '秋,果,長大,長,地方...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='南一' and lesson_number=9),
  '樣,園,您,學,汗...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='南一' and lesson_number=10),
  '肚子,世界,井,隻,除...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='南一' and lesson_number=11),
  '怪,呀,鴨,塘,星星...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='南一' and lesson_number=12),
  '甜,分享,收成,不能,加油...'
);
-- 補新課次：1年級/南一/上學期 第8課「魔法文字」（curriculum原本沒有這筆，來源版本較新）
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='chinese' and school_level_id=1), 1, '上', '南一', 8, '魔法文字');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='南一' and lesson_number=8),
  '日,門,手,人,水...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='南一' and lesson_number=1),
  '上,加,來,也,魚...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='南一' and lesson_number=2),
  '地,開,出,招,車...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='南一' and lesson_number=3),
  '我,的,你,抱,吹...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='南一' and lesson_number=4),
  '友,一下子,爸,到,青...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='南一' and lesson_number=5),
  '什,麼,星,哪,球...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='南一' and lesson_number=6),
  '話,缸,兩,都,悄...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='南一' and lesson_number=7),
  '了,請,幸福,天,家...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='康軒' and lesson_number=1),
  '靜,要,花草,白雲,天空...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='康軒' and lesson_number=2),
  '快,身上,新芽,輕快,沒有...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='康軒' and lesson_number=3),
  '音,媽,上桌,好吃,過後...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='康軒' and lesson_number=4),
  '口,享,受,溫,暖...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='康軒' and lesson_number=5),
  '公,陪伴,光,陽光,澆水...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='康軒' and lesson_number=6),
  '奶,跟,班,床,弟...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='康軒' and lesson_number=7),
  '黑,糖,棉,作,變...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='康軒' and lesson_number=8),
  '妹妹,雙,穿,金魚,魚缸...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='康軒' and lesson_number=9),
  '刷,低,馬,淨,洗...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='康軒' and lesson_number=10),
  '說說笑笑,地,化,趣,線...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='康軒' and lesson_number=11),
  '福,第,次,謝,生日...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='康軒' and lesson_number=12),
  '幫,加油,一會兒,休息,清楚...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='康軒' and lesson_number=1),
  '手,拍,拍手,下,上...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='康軒' and lesson_number=2),
  '誰,這,是,的,我...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='康軒' and lesson_number=3),
  '陪,好朋友,高,山,到...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='康軒' and lesson_number=4),
  '隻,子,小,課,兩...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='康軒' and lesson_number=5),
  '裡,主人,外,有,什...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='康軒' and lesson_number=6),
  '一頭,紅花,白花,小路,那...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='翰林' and lesson_number=1),
  '裡,春,就是,暖和,天氣...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='翰林' and lesson_number=2),
  '手,愛,稻,苗,唱歌...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='翰林' and lesson_number=3),
  '涼,好像,妹妹,衣服,拍照...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='翰林' and lesson_number=4),
  '卡,片,畫,寫,話...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='翰林' and lesson_number=5),
  '先,急,但是,下課,可以...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='翰林' and lesson_number=6),
  '葉子,毛,陽,光,兒...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='翰林' and lesson_number=7),
  '自,今,家,每,都...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='翰林' and lesson_number=8),
  '教,等,忍不住,然,不好意思...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='翰林' and lesson_number=9),
  '得,覺,康,健,步...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='翰林' and lesson_number=10),
  '聽見,棵,樹,打,雷...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='翰林' and lesson_number=11),
  '學,橡,擦,確,鉛筆...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='下' and publisher='翰林' and lesson_number=12),
  '段,同學,動物,一段,時間...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='翰林' and lesson_number=1),
  '走,起,一起,前,向...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='翰林' and lesson_number=2),
  '大,風,吹,們,來...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='翰林' and lesson_number=3),
  '一個,火,車,山洞,火車...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='翰林' and lesson_number=4),
  '少,請,太,星,高...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='翰林' and lesson_number=5),
  '看,下去,棉花糖,天上,滑梯...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='翰林' and lesson_number=6),
  '陪,千,子,空,說...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=1 and semester='上' and publisher='翰林' and lesson_number=7),
  '回,哈哈大笑,音,到,谷...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='南一' and lesson_number=1),
  '火紅,受,藏,心情,時候...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='南一' and lesson_number=2),
  '哥,盆,合,勇敢,淨...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='南一' and lesson_number=3),
  '啦,結果,大喊,抓住,竟然...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='南一' and lesson_number=4),
  '姐,懶,滾,水珠,微微...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='南一' and lesson_number=5),
  '忍,清涼,寶貝,海浪,清...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='南一' and lesson_number=6),
  '決定,浪費,康復,封,信...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='南一' and lesson_number=7),
  '答,答案,大街,傘,烏...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='南一' and lesson_number=8),
  '摘花,布告牌,各位,重新,欣賞...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='南一' and lesson_number=9),
  '息,拿,讀,精,采...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='南一' and lesson_number=10),
  '原狀,明白,銀,女,願...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='南一' and lesson_number=11),
  '講,論,颳,勵,失敗...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='南一' and lesson_number=12),
  '北極,由,極,磚,牆壁...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='南一' and lesson_number=1),
  '白,呼,成功,第一次,用力...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='南一' and lesson_number=2),
  '最,梯子,白紙,好像,沿...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='南一' and lesson_number=3),
  '室,教,勇,故事,騎車...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='南一' and lesson_number=4),
  '包,遊,戲,剩,一塊...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='南一' and lesson_number=5),
  '種,全,一座,下午,大王...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='南一' and lesson_number=6),
  '留,自,該,如,吧...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='南一' and lesson_number=7),
  '耕,以,運,幸,路...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='南一' and lesson_number=8),
  '嚇,鹿,喝,直到,速度...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='南一' and lesson_number=9),
  '法,主,隨,更,定...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='南一' and lesson_number=10),
  '依依不捨,群,靜,抬,非...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='南一' and lesson_number=11),
  '接,牛,糯,變,湯圓...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='南一' and lesson_number=12),
  '調,魚兒,迷宮,調色盤,顏料...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='康軒' and lesson_number=1),
  '池,顏,景色,到處,燕子...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='康軒' and lesson_number=2),
  '剪,慶,且,衣裳,驚喜...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='康軒' and lesson_number=3),
  '如果,表情,各自,突然,變壞...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='康軒' and lesson_number=4),
  '永,窗,避,散發,光芒...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='康軒' and lesson_number=5),
  '貝,不管,寶,堅固,辛苦...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='康軒' and lesson_number=6),
  '哥哥,腳踏車,牛排,教,室...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='康軒' and lesson_number=7),
  '鼻,一模一樣,請,之,辦...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='康軒' and lesson_number=8),
  '相信,議,鴕,經過,奇怪...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='康軒' and lesson_number=9),
  '抓,派,帝,皇,貪...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='康軒' and lesson_number=10),
  '蹦蹦跳跳,琅琅,熊,朝,踮...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='康軒' and lesson_number=11),
  '庫,索,奧,圖書館,參加...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='康軒' and lesson_number=12),
  '量,到底,底,巨人,頭髮...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='康軒' and lesson_number=1),
  '老師,聲,矮,學年,希望...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='康軒' and lesson_number=2),
  '臉,餐,醬,早餐,全家...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='康軒' and lesson_number=3),
  '叔,巷,美麗,模樣,打扮...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='康軒' and lesson_number=4),
  '最,可,賽,拔,運動會...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='康軒' and lesson_number=5),
  '碗,划船,捕,活,識...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='康軒' and lesson_number=6),
  '親朋好友,如意,鎮,餅,節...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='康軒' and lesson_number=7),
  '滿,街,棒,直,西...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='康軒' and lesson_number=8),
  '喝,法,瓶,熊,但是...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='康軒' and lesson_number=9),
  '然,沿,少,沉,牽...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='康軒' and lesson_number=10),
  '季,貨,春,雖,待...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='康軒' and lesson_number=11),
  '充,念,戴,扁,面具...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='康軒' and lesson_number=12),
  '居然,妙,聊,牠們,圓鼓鼓...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='翰林' and lesson_number=1),
  '昭和草,旅,世界,自由,探險...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='翰林' and lesson_number=2),
  '提,漠,等不及,轉,令...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='翰林' and lesson_number=3),
  '紫,同伴,這些,樹木,終於...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='翰林' and lesson_number=4),
  '爺,剛,淹,農夫,口渴...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='翰林' and lesson_number=5),
  '利,露出,方式,微笑,謝謝...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='翰林' and lesson_number=6),
  '自從,禮貌,學校,從,臺...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='翰林' and lesson_number=7),
  '幾,顏料,神奇,橙色,混合...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='翰林' and lesson_number=8),
  '晨,離開,凡事,孩,求助...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='翰林' and lesson_number=9),
  '呼,驗,敗,絲,費...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='翰林' and lesson_number=10),
  '打破,醜,鴨,其,特...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='翰林' and lesson_number=11),
  '算,吐,顧,離,蜘蛛...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='下' and publisher='翰林' and lesson_number=12),
  '運動,夜夜,體操,嚇一跳,桂樹...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='翰林' and lesson_number=1),
  '颳,候,彩虹,美麗,出現...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='翰林' and lesson_number=2),
  '熟,師,辦,舞,老師...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='翰林' and lesson_number=3),
  '一點,享,臣,袖,驚...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='翰林' and lesson_number=4),
  '明,頂,影,蝦,蟆...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='翰林' and lesson_number=5),
  '夕,螃蟹,可愛,注意,夕陽...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='翰林' and lesson_number=6),
  '盡頭,眼睛,月,奶,晚...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='翰林' and lesson_number=7),
  '安,平,保,節,清...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='翰林' and lesson_number=8),
  '介,米線,各種,青菜,介紹...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='翰林' and lesson_number=9),
  '蛋,苔,名,胖,蒸...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='翰林' and lesson_number=10),
  '突然,異口同聲,減,表,讀...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='翰林' and lesson_number=11),
  '底,慌,仔,擠,妖...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=2 and semester='上' and publisher='翰林' and lesson_number=12),
  '隻,肚皮,倒,肚,詠...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=1),
  '首,撐,吼叫,嘴巴,恐龍...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=2),
  '參,容,另外,羨慕,洋娃娃...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=3),
  '玉,炎,糖水,搓洗,容器...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=4),
  '驚,有名,丞相,曹操,楊修...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=5),
  '錢,偏偏,陽光普照,千萬,厲害...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=6),
  '松鼠,混亂,村,猴,抖...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=7),
  '堂,幢,棋,塔,抹...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=8),
  '底,叔,海底,郵筒,上岸...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=9),
  '示,磚,治,籠,燈...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=10),
  '岩石,沖刷,鹹,之,川...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=11),
  '不僅,築巢,適合,現代,柴火...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=12),
  '社,商店,社區,萬華,建築...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='南一' and lesson_number=1),
  '化,泥,足球,開朗,平安...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='南一' and lesson_number=2),
  '走廊,提,愁,言,些...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='南一' and lesson_number=3),
  '無,盡責,得意忘形,總是,表情...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='南一' and lesson_number=4),
  '溫,夕陽,比賽,加緊,店家...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='南一' and lesson_number=5),
  '鈴,注,消防員,原諒,發脾氣...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='南一' and lesson_number=6),
  '幕,杯,撞,流,溼...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='南一' and lesson_number=7),
  '藝,仔,摺,捏,藏...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='南一' and lesson_number=8),
  '視,框,整齊,機會,鏡...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='南一' and lesson_number=9),
  '敲,體,毒,藥,淘...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='南一' and lesson_number=10),
  '印象,呆頭呆腦,極,熊,雪...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='南一' and lesson_number=11),
  '雞,肉,威,額頭,石虎...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='南一' and lesson_number=12),
  '退,放屁,擊退,演技,逼真...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=1),
  '晨,願,飛翔,耀眼,鮮豔...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=2),
  '溝,軟,輕紗,屋簷,垂掛...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=3),
  '區,架,鏡,髮,拾...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=4),
  '齒,鋸,工匠,魯班,王宮...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=5),
  '爾,費,市議會,議員,費用...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=6),
  '節省,周,票,碼,技...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=7),
  '禮,枝椏,梢,抬,取...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=8),
  '豆腐,雕塑,鬼斧神工,柳,香菇...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=9),
  '伐,縫,敵,持,保...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=10),
  '水藻,夫婦,漁,夫,婦...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=11),
  '逃,獵,砰,老虎,布幕...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=12),
  '救,毫無,唉聲嘆氣,糟糕,千萬...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=1),
  '舟,字,練習,看似,口訣...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=2),
  '喊,名,傘,已,穫...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=3),
  '機,葡萄,料,實,留...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=4),
  '葵,擺,觸,小丑魚,海葵...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=5),
  '通,朝,努,總,段...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=6),
  '肚子,黏人,膠水,女,非...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=7),
  '憶,坡,蒼,嚼,愈...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=8),
  '敗,守,護,功,型...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=9),
  '智,慧,態,鞍,蓮...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=10),
  '妙計,強壯,狐,里,兄...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=11),
  '隨,築,顯,極,愉悅...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=12),
  '蛇,驚訝,蟒蛇,後退,帽子...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=1),
  '不願,潔白,牆壁,來來往往,究竟...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=2),
  '微笑,微,訣,缸,豎...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=3),
  '休克,臂,跪,腕,膝蓋...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=4),
  '凝,廣大,松針,苔蘚,柔媚...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=5),
  '師傅,發酵,乾燥,烘焙,講究...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=6),
  '山丘,象,集,驚,漿...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=7),
  '罐,醃,菌,醃漬,疑惑...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=8),
  '交談,展現,活潑,光芒,徐...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=9),
  '圾,垃,取,免,端...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=10),
  '大胃王,大拇指,員,幕,無...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=11),
  '糞,鷹,維妙維肖,佛寺,屋梁...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=12),
  '老鼠,賽,鶴,蝟,夏天...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=1),
  '牠,待,悲傷,縮短,快樂...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=2),
  '爛,鬆,餐,嘟,房...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=3),
  '因為,喊,睡,餘,分鐘...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=4),
  '錢,飼,歉,憤,鼻...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=5),
  '且,便條,冰箱,安排,按時...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=6),
  '膠水,解,削,擦,桿...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=7),
  '坡,橇,乘,航,蔚...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=8),
  '灘,應該,蟹,愛護,物品...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=9),
  '捲,岸,淺,般,沿...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=10),
  '束,飾,互,惜,俗...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=11),
  '傅,關,聯,擾,除夕...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=12),
  '客廳,廳,擠,鏡,團圓...'
);
-- 補新課次：4年級/南一/下學期 第13課「𪹚龍慶元宵」（curriculum原本沒有這筆，來源版本較新）
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='chinese' and school_level_id=1), 4, '下', '南一', 13, '𪹚龍慶元宵');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=13),
  '懷,慶,神采飛揚,象徵,穿梭...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=2),
  '優美,音效,製作,表達,搭配...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=3),
  '甩,自豪,受邀,肯定,顧慮...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=4),
  '翩翩,晾乾,奮力,破曉,絕技...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=5),
  '激動,嘆,健全,四肢,蹟...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=6),
  '通,裂,付,關,糊...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=7),
  '雅,憂,凋,昏,橙...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=8),
  '必,瑩,煤,善意,安慰...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=9),
  '喘,浹,折,喚,填...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=10),
  '計算機,慧,燃,誕,啟...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=11),
  '改,五線譜,跨欄,廚師,找尋...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=12),
  '詳,安詳,寧靜,順利,聚集...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=1),
  '漫,戶,相伴,迎接,收穫...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=2),
  '汽,彷彿,矯正,餐桌,牙齒...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=3),
  '獲,存,辣,酸,志...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=4),
  '聆,翻,淺淺,搧風,島嶼...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=5),
  '挑戰,爭,佩,驕傲,過程...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=6),
  '護,鋼,亞,尺,層...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=7),
  '值,統,麵,念,渡...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=8),
  '踮,辮子,滑雪板,冷絲絲,臉龐...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=9),
  '褐,促,振,碎,者...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=10),
  '花轎,隊伍,妞,郎,丈...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=11),
  '拚,婆婆,齒頰留香,陰森森,面無血色...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=12),
  '漸,漸漸,笑納,隱約,傍晚...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=1),
  '環,潔,自言自語,格格不入,舒暢...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=2),
  '缺,絆腳石,顧慮,慚愧,到達...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=3),
  '勤,選,啟,宣,拭目以待...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=4),
  '粽,推,陳,稻米,蘿蔔糕...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=5),
  '封面,封,過敏,發癢,麥芽糖...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=6),
  '插,拌,磚,昂,繁...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=7),
  '惡,致,遷,均,配...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=8),
  '獨,厚,研究,究,輕而易舉...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=9),
  '試,號,僅,姆,斯...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=10),
  '耗盡,豪,忽,瞧,灘...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=11),
  '淚,孤,皎潔,嫦娥,吳剛...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=12),
  '聖,壓住,齊天大聖,掏出,咒語...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=1),
  '串,泳,煩惱,水陸,轉身...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=2),
  '警,偷,則,捨,繩...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=3),
  '喧,優美,喧鬧,此起彼落,指揮...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=4),
  '濃,馬偕,醫院,生命,奉獻...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=5),
  '注意,盡力,舒適,凱,勒...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=6),
  '谷底,攀登,訓練,秀,稱...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=7),
  '郁,麵,義,醬,材...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=8),
  '經濟,臨,樓,代,連通橋...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=9),
  '鬱,防,堤,窪,勢...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=10),
  '臉龐,榮華富貴,幻,旋,扁...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=11),
  '遲,背心,懷錶,上鎖,鑰匙...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=12),
  '蹦,內心,蹦蹦跳跳,手舞足蹈,嘖嘖稱奇...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=1),
  '雄,苗,金燦燦,稻穗,季節...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=2),
  '碳,建築,興致,煙囪,導覽...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=3),
  '敏,傍,橘,迴盪,黯淡...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=4),
  '共,餘,予,並列,召喚...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=5),
  '旗,家庭,人偶,未來,主人翁...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=6),
  '遍,潔,碎,簇,桐...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=7),
  '壘,支,討,輸,反...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=8),
  '愈,領,喘,拚,挨罵...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=9),
  '霧,似,捉,棧,眺...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=10),
  '椅子,芭,焰,擔,搧...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=11),
  '賺,搬,梯,合租,瘦弱...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=12),
  '布告欄,鐘聲,任務,收穫,踴躍...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='翰林' and lesson_number=1),
  '甜蜜,島,童話,臺灣,香蕉...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='翰林' and lesson_number=2),
  '彷彿,陀,恐,區,汽...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='翰林' and lesson_number=3),
  '蔬,蔬菜,耕耘,軌道,鏡頭...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='翰林' and lesson_number=4),
  '碑,兄弟,飛翔,老鷹,無論...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='翰林' and lesson_number=5),
  '輪,答案,尋找,徊,科學家...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='翰林' and lesson_number=6),
  '平均,月餅,揭開,館,億...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='翰林' and lesson_number=7),
  '禁,滋味,必要,麵,焦...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='翰林' and lesson_number=8),
  '江,根本,脫口而出,帥氣,俠...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='翰林' and lesson_number=9),
  '惡,人民,懶,晉,盡...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='翰林' and lesson_number=10),
  '海藻,汙染,珊,瑚,礁...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='翰林' and lesson_number=11),
  '浪潮,纏住,海豚,嘗鮮,虎鯨...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=4 and semester='上' and publisher='翰林' and lesson_number=12),
  '籟,天籟,優美,舉辦,嘉賓...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=1),
  '盞,廳,純粹,入場券,書籤...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=2),
  '鑽,轟,隆,途,鑑...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=3),
  '蓮霧,嚴,庫,澀,餘...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=4),
  '沾,貪,饒,謀,老闆...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=5),
  '逞,倘若,默,批評,幽默...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=6),
  '刃,姨,缺,喻,馨...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=7),
  '任,癢,湊,絢,枚...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=8),
  '癟,嚼,礦,打瞌睡,銅板...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=9),
  '症,裁,瀏覽,誇,靜謐...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=10),
  '渺小,絮,斜,傑,滔...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=11),
  '研,價,兵馬俑,皇帝,君王...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=12),
  '根據,鳥瞰,埃及,蘊含,切割...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='南一' and lesson_number=1),
  '某,灘,比較,謹慎,焦急...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='南一' and lesson_number=2),
  '延長線,平穩,師傅,豐富,障...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='南一' and lesson_number=3),
  '橡皮擦,慈,慚,愧,評語...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='南一' and lesson_number=4),
  '乳白色,渲染,臭美,滲入,岩漿...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='南一' and lesson_number=5),
  '斧,醉心,縱,氣勢雄偉,鬼斧神工...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='南一' and lesson_number=6),
  '繁殖,緩,顯,悲,愈...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='南一' and lesson_number=7),
  '鱗,磁,棟,杆,弧...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='南一' and lesson_number=8),
  '鄉,蓋子,疊羅漢,大蒜,辣椒...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='南一' and lesson_number=9),
  '賺,挖,亡,款,基...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='南一' and lesson_number=10),
  '扭,誼,互,繫,鍋...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='南一' and lesson_number=11),
  '恍,悟,昂,瀑布,財富...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='南一' and lesson_number=12),
  '歸心似箭,輕舟,白帝城,敏銳,描寫...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=1),
  '聆聽,簽名,傻瓜,神態自若,繼續...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=2),
  '婉,緊閉,委,懂,羞...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=3),
  '普,承認,價,承,搏...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=4),
  '骨,急診,緊繃,情緒,疫情...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=5),
  '沉浸,湧現,激發,閱讀,龍冠鳳紋玉飾...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=6),
  '必須,魔,唷,伏,吁...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=7),
  '延,瀰,霧,寺,江...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=8),
  '珊,瑚,積,噸,垃...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=9),
  '玻,玻,襯,凸,璃...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=10),
  '澤,狼,鵡,洶,堪...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=11),
  '霆,俯,啄,貪婪,發抖...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=12),
  '保佑,藤蔓,檢驗,犧牲,一命嗚呼...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=1),
  '帳,蚊,全力以赴,基金會,雜誌...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=2),
  '不斷,斷,德國,似乎,血液...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=3),
  '冷箭,挫,折,陡峭,強勁...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=4),
  '慨,滋,恆久,黃澄澄,稻穗...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=5),
  '售,霸,項目,霸主,銷售...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=6),
  '樣貌,判,貌,益,隊...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=7),
  '緻,絡,脈,鄰,逸...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=8),
  '震撼,性,恐懼,武器,康復...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=9),
  '幼,予,屢,減,鍛...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=10),
  '扉,幽,詠,閒,確...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=11),
  '吼,喉,嚨,疤痕,鐵罐...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=12),
  '烤,躍躍欲試,烤爐,倒塌,木筏...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=1),
  '足跡,音符,坎坷,澎湃,無垠...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=2),
  '掠,降,綻,灑,嘩...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=3),
  '簽證,拘,厚,欲,璞...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=4),
  '私,採訪,重殘,和藹,爽朗...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=5),
  '礙,領悟,錶,瞄,慎...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=6),
  '厲鬼,草蓆,聯絡簿,瀰,暫...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=7),
  '遺,陰,澈,渠,鑑...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=8),
  '詼,哏,繁,泛,詳...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=9),
  '謹慎,疏失,劍,榮,仗...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=10),
  '手腕,白皙,呎,鼻,廓...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=11),
  '恍,丞,庫,推辭,都督...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=12),
  '止血,避免,儘管,茅屋,睿智...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=1),
  '周遭,堅定,耐勞,多元,刺蝟...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=2),
  '熟,威,直笛,吹奏,簡單...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=3),
  '羞恥,肝,完璧歸趙,諸侯,挺身而出...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=4),
  '雨後春筍,餐廳,眾多,根據,逐漸...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=5),
  '院,錯愕,利潤,公司,吔...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=6),
  '焚化,飲,織,複,極...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=7),
  '鳴,乎,茂,寂,曠...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=8),
  '盼,葫,幼苗,鄰居,藤蔓...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=9),
  '圃,暑,掀,褐,側...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=10),
  '洋,丈,詞,髮,飾...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=11),
  '籃,聰,擇,脆,編...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=12),
  '糟,奇蹟,政府,開闢,柵欄...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='南一' and lesson_number=1),
  '盾,矛,霎時,煞車,尿尿...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='南一' and lesson_number=2),
  '狩獵,喉嚨,黎明,奄奄一息,小心翼翼...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='南一' and lesson_number=3),
  '邏,捷,輯,例,楊梅...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='南一' and lesson_number=4),
  '邇,楷模,氣餒,沮喪,屹立不搖...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='南一' and lesson_number=5),
  '洶湧,凶猛,急湍,強勁,不偏不倚...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='南一' and lesson_number=6),
  '犯,汰,蠢,愚,按...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='南一' and lesson_number=7),
  '懇,敦,咀,殷,彌...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='南一' and lesson_number=8),
  '厭,驪歌,鳳凰樹,忌諱,德性...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='南一' and lesson_number=9),
  '誦讀,綺麗,空曠,蒲公英,門檻...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='南一' and lesson_number=1),
  '塵,爽,腳跡,陰霾,書頁...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='南一' and lesson_number=2),
  '咂,瀉,賴,舒適,茂盛...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='南一' and lesson_number=3),
  '皆,舍,鋪陳,孤寂,籬笆...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='南一' and lesson_number=4),
  '襯,惹,摟,運動衫,肌膚...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='南一' and lesson_number=5),
  '載歌載舞,益,副,監,陌生...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='南一' and lesson_number=6),
  '誌,奪,隕,凌,駕...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='南一' and lesson_number=7),
  '衡,芽,苞,壤,搔...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='南一' and lesson_number=8),
  '飢渴,自怨自艾,手臂,火焰,熄滅...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='南一' and lesson_number=9),
  '江,欠,否,策,鎖...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='南一' and lesson_number=10),
  '詫異,變幻莫測,亦,傾,頃...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='南一' and lesson_number=11),
  '泛,枇,杷,斥責,嚴肅...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='南一' and lesson_number=12),
  '煎熬,酣,拮据,抄寫,躡手躡腳...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='康軒' and lesson_number=1),
  '掠食者,獨立,心馳神往,輾轉,櫛比鱗次...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='康軒' and lesson_number=2),
  '愜,回眸,興味盎然,杏,眸...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='康軒' and lesson_number=3),
  '鬆,供應,欄,瑞士,名列前茅...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='康軒' and lesson_number=4),
  '誼,摯,抒發,漂泊,餘暉...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='康軒' and lesson_number=5),
  '樁,巡視,裹,棚,剖...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='康軒' and lesson_number=6),
  '陰,斑,猶,孜,廠...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='康軒' and lesson_number=7),
  '窣,誦,宇,宙,浩...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='康軒' and lesson_number=8),
  '構築,諺語,羹,全力以赴,一輩子...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='康軒' and lesson_number=9),
  '曙光,生涯,溝通,窘境,俗話...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=1),
  '尷尬,年級,壓軸,爭奪,委屈...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=2),
  '縷,碗,綢,繆,毋...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=3),
  '茁,揭示,卓越,培養,總裁...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=4),
  '彰,煮,豬,鼎邊趖,颳風...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=5),
  '熬煮,砂,混,焦,舀...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=6),
  '徜徉,習慣,舞蹈,歐,榜...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=7),
  '皆,乏,恰,謹,批...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=8),
  '猾,隙,竄,旨,悠...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=9),
  '薰,僮,倘,姓,崗...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=10),
  '暖烘烘,耶,郊,慈,祥...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=11),
  '某,煥,橇,鈴,迴...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=12),
  '儘管,螞蟻,包括,瀰漫,薔薇...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='翰林' and lesson_number=1),
  '建築,彰,購,遛達,陌生...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='翰林' and lesson_number=2),
  '摒,怖,頤,盜,衰...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='翰林' and lesson_number=3),
  '孤陋寡聞,欠缺,嗤之以鼻,倨傲,每逢...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='翰林' and lesson_number=4),
  '纍,苦澀,言簡意賅,描述,致使...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='翰林' and lesson_number=5),
  '飛梭,鈴,逝,恆,恬...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='翰林' and lesson_number=6),
  '斤,妨,凌,績,濟...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='翰林' and lesson_number=7),
  '掘,釐,燃,驅使,由衷...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='翰林' and lesson_number=8),
  '要旨,茁壯,柢,鍛鍊,精湛...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='下' and publisher='翰林' and lesson_number=9),
  '阱,雛鳥,胸膛,光芒,啾啾...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=1),
  '晃,皺,儲存,註定,蝴蝶...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=2),
  '寂寞,眼眶,固執,辯論,雙胞胎...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=3),
  '婆,杏,智慧,警惕,分辨...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=4),
  '翹,垂,奧妙,仿生學,從容不迫...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=5),
  '典型,酥,庇,栽,施工...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=6),
  '侃,競,詼,嘲,醜...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=7),
  '銅,涵,鋼,鏽,眨...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=8),
  '墩,塗,撇,攏,咧...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=9),
  '吊,柱,絢,騰,井...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=10),
  '殷勤,樸實,莊,暢,黍...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=11),
  '蟹,挽,糟蹋,哀愁,岩岸...'
);
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=12),
  '莖,絲毫,監牢,誣告,反駁...'
);

-- ============================================================
-- 社會：新資料整組取代（版本衝突較大，依規則以新為準）
-- ============================================================

-- 3年級 / 南一 / 下學期：刪除舊課次，改用教育百科114_2新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=3 and semester='下' and publisher='南一';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '下', '南一', 1, '居住的地方');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=1),
  '石滬,身分證,都市,大眾運輸,鄉村...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '下', '南一', 2, '地方生活');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=2),
  '原住民,守望相助,志工,衛生所,村長'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '下', '南一', 3, '生活理財');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=3),
  '保險,醫療,賠償,記帳,理財...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '下', '南一', 4, '居住地方的地名與故事');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=4),
  '引水,諸羅'
);

-- 3年級 / 康軒 / 下學期：刪除舊課次，改用教育百科114_2新資料（共6課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=3 and semester='下' and publisher='康軒';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '下', '康軒', 1, '我們居住的地方');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=1),
  '門牌,鄰里,戶口名簿,身分證,部落...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '下', '康軒', 2, '居住地方的風貌');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=2),
  '電信,通訊,向心力,義賣,偏見...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '下', '康軒', 3, '消費與生活');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=3),
  '禮券,消費,銅錢,紙鈔,風潮...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '下', '康軒', 4, '消費與選擇');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=4),
  '過度,綠色消費,身心障礙,統一發票,雲端...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '下', '康軒', 5, '家鄉的地名');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=5),
  '開墾,行政區'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '下', '康軒', 6, '家鄉的故事');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=6),
  '人文,琉璃珠,祭典,節慶,瑠公圳...'
);

-- 3年級 / 康軒 / 上學期：刪除舊課次，改用教育百科109_1新資料（共3課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=3 and semester='上' and publisher='康軒';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '上', '康軒', 1, '和諧的相處');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=1),
  '公平,觀念,發展,欣賞,變遷...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '上', '康軒', 2, '校園安全');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=2),
  '霸凌,暗藏'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '上', '康軒', 3, '清領前期的臺灣');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=3),
  '荷蘭王國（Kingdom of the Netherlands）,熱蘭遮城,荷治時期,新港文書'
);

-- 3年級 / 翰林 / 下學期：刪除舊課次，改用教育百科114_2新資料（共5課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=3 and semester='下' and publisher='翰林';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '下', '翰林', 1, '我居住的地方');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=1),
  '伊斯蘭教,都市,鄉村,生活習慣,門牌...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '下', '翰林', 2, '多元的生活的空間');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=2),
  '養殖,蜂炮,藝文活動,捕撈,公共設施...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '下', '翰林', 3, '生活中的各行各業');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=3),
  '自然資源,藥師,分工,線上購物,畜牧業...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '下', '翰林', 4, '生活與工作的轉變');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=4),
  '農業社會,人力,社會變遷,空服員'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '下', '翰林', 5, '儲蓄與消費的選擇');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=5),
  '購物袋,統一發票,行動支付,壓歲錢,零用錢...'
);

-- 3年級 / 翰林 / 上學期：刪除舊課次，改用教育百科109_1新資料（共12課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=3 and semester='上' and publisher='翰林';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '上', '翰林', 1, '我會快樂學習');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=1),
  '效率,規律,端正,善用,休閒'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '上', '翰林', 2, '善用學習資源');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=2),
  '專家,興趣,學者,遺址,網路...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '上', '翰林', 3, '家庭與我');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=3),
  '效率,規律,端正,失業,隱私'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '上', '翰林', 4, '家庭的活動');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=4),
  '向心力,氣氛,營造,亞運,參與...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '上', '翰林', 5, '班級自治活動');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=5),
  '考慮,公平,規律,制定,自治...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '上', '翰林', 6, '班級會議');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=6),
  '表決,表達,流程,尊重,充分...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '上', '翰林', 7, '我和我的同學');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=7),
  '專長,障礙,相處,鼓勵,內向...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '上', '翰林', 8, '參加校園團隊活動');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=8),
  '豐富,主動,欣賞,充實,參與...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '上', '翰林', 9, '互助合作');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=9),
  '合作,展現,分工合作,競爭,觀摩...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '上', '翰林', 10, '校園安全維護');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=10),
  '共同,提醒,損壞,維護,安全...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '上', '翰林', 11, '居住的地方');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=11),
  '長輩,訪問,景觀,拜訪,資料...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 3, '上', '翰林', 12, '家庭倫理');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=12),
  '親人,稱呼,往來,熱絡,親密'
);

-- 4年級 / 南一 / 下學期：刪除舊課次，改用教育百科114_2新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=4 and semester='下' and publisher='南一';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '下', '南一', 1, '家鄉的地形與氣候');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=1),
  '台地,盆地,丘陵,梯田'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '下', '南一', 2, '家鄉的產業與創新');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=2),
  '自動化,製造業,茶樹,畜牧業,漁業...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '下', '南一', 3, '家鄉的人口');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=3),
  '人口,新生兒,保健,生育'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '下', '南一', 4, '多元文化與願景');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=4),
  '泰雅族,祭祀,婚喪喜慶,魯凱族,竹筒飯...'
);

-- 4年級 / 南一 / 上學期：刪除舊課次，改用教育百科109_1新資料（共1課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=4 and semester='上' and publisher='南一';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '上', '南一', 1, '科技的進步與家鄉的生活');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=1),
  '拔火罐,草藥,負壓效應,溫熱療法'
);

-- 4年級 / 康軒 / 下學期：刪除舊課次，改用教育百科114_2新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=4 and semester='下' and publisher='康軒';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '下', '康軒', 1, '家鄉的產業');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=1),
  '牧場,機能,丘陵,轉型,產銷...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '下', '康軒', 2, '家鄉的人口');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=2),
  '戶籍登記,檜木,金礦,礦產,丘陵...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '下', '康軒', 3, '家鄉的交通');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=3),
  '謠言,通訊,遊艇,渡輪,船舶...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '下', '康軒', 4, '家鄉風情畫');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=4),
  '人文,黑面琵鷺,溼地,石滬,節慶...'
);

-- 4年級 / 康軒 / 上學期：刪除舊課次，改用教育百科109_1新資料（共3課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=4 and semester='上' and publisher='康軒';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '上', '康軒', 1, '美麗的家鄉');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=1),
  '灌溉,平坦,土石流,寬廣,公共建設...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '上', '康軒', 2, '家鄉');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=2),
  '觀光,巡禮,推動,三合院,媽祖...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '上', '康軒', 3, '家鄉生活');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=3),
  '發展,廢棄物,遊憩,早期,演變...'
);

-- 4年級 / 翰林 / 下學期：刪除舊課次，改用教育百科114_2新資料（共5課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=4 and semester='下' and publisher='翰林';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '下', '翰林', 1, '家鄉的水資源');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=1),
  '水井,水資源,舢舨,灌溉,汙水處理...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '下', '翰林', 2, '家鄉的山與海');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=2),
  '林場,山林,樟腦,近海漁業,造船...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '下', '翰林', 3, '家鄉的農牧生活');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=3),
  '化學肥料,產銷,農耕,廚餘,家畜...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '下', '翰林', 4, '家鄉的老故事');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=4),
  '鹿港鎮,木臼,布袋戲,舞獅,舞龍...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 4, '下', '翰林', 5, '家鄉的新風貌');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=5),
  '商圈,年貨,集散,迪化街,人口老化...'
);

-- 5年級 / 南一 / 下學期：刪除舊課次，改用教育百科114_2新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=5 and semester='下' and publisher='南一';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '下', '南一', 1, '唐山到臺灣');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=1),
  '海流,季風,艋舺,港市,民變...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '下', '南一', 2, '開港通商後的臺灣');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=2),
  '學堂,電報,牡丹社事件,滬尾,領事館'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '下', '南一', 3, '臺灣電力的發展');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=3),
  '核廢料,核能發電,地熱,油燈'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '下', '南一', 4, '經濟與生活');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=4),
  '網路購物,詐騙,股票,基金,外幣...'
);

-- 5年級 / 康軒 / 下學期：刪除舊課次，改用教育百科114_2新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=5 and semester='下' and publisher='康軒';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '下', '康軒', 1, '我們的經濟活動');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=1),
  '身心,回饋,消費者,價值觀,理財...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '下', '康軒', 2, '清帝國時期臺灣的發展與改變');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=2),
  '炮臺,傳教士,鴉片,洋行,通商...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '下', '康軒', 3, '日治時期人民與政府的關係');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=3),
  '霧社事件,噍吧哖事件,文面,殖民,甲午戰爭...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '下', '康軒', 4, '日治時期的社會變遷');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=4),
  '嘉南大圳,樟腦,糖廠,烏山頭水庫,濁水溪...'
);

-- 5年級 / 康軒 / 上學期：刪除舊課次，改用教育百科109_1新資料（共10課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=5 and semester='上' and publisher='康軒';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '上', '康軒', 1, '繩紋');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=1),
  '考古,貝塚,先民,煉鐵,記載...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '上', '康軒', 2, '臺灣的先民-原住民族文化');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=2),
  '頭目,遷移,風俗,精緻,祭典...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '上', '康軒', 3, '世界發現臺灣-海上來的紅毛人');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=3),
  '逐步,據點,壯麗,蔗糖,天主教...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '上', '康軒', 4, '世界發現臺灣-鄭氏時代的經營');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=4),
  '將領,領土,屯墾,選拔,駐守...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '上', '康軒', 5, '臺灣我的家');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=5),
  '候鳥,遷徙,大洋洲,太平洋（Pacific Ocean）,鄰近...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '上', '康軒', 6, '臺灣的經度和緯度');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=6),
  '假想,界線,赤道,經度,經線...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '上', '康軒', 7, '臺灣的地形');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=7),
  '起伏,丘陵,平原,平坦,隆起...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '上', '康軒', 8, '清領前期的社會與文化');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=8),
  '碑,錮婢,朱一貴,示禁碑,朱一貴事件'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '上', '康軒', 9, '清領前期的社會與文化-商業組織');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=9),
  '商,艋舺,會館,一府二鹿三艋舺,三郊...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '上', '康軒', 10, '清領後期的臺灣');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=10),
  '樟腦,樟腦寮,腦寮'
);

-- 5年級 / 翰林 / 下學期：刪除舊課次，改用教育百科114_2新資料（共3課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=5 and semester='下' and publisher='翰林';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '下', '翰林', 1, '日本統治下的臺灣');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=1),
  '甲午戰爭,公共衛生,割讓,巡撫,殖民...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '下', '翰林', 2, '走向民主的中華民國');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=2),
  '公共事務,戒嚴,二二八事件,集會,地方自治...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '下', '翰林', 3, '從臺灣探索世界文化');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=3),
  '伊斯蘭教,社會發展,曆法,祭典,小米...'
);

-- 5年級 / 翰林 / 上學期：刪除舊課次，改用教育百科109_1新資料（共6課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=5 and semester='上' and publisher='翰林';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '上', '翰林', 1, '認識我們家的家園');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=1),
  '赤道,西半球,經度,經線,北半球...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '上', '翰林', 2, '山海之歌');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=2),
  '臺地,丘陵,平原,盆地,山地...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '上', '翰林', 3, '氣候變奏曲');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=3),
  '氣溫,落山風,梅雨,焚風,北回歸線...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '上', '翰林', 4, '生活的泉源');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=4),
  '豐水期,枯水期,德基水庫,翡翠水庫,水力發電...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '上', '翰林', 5, '唐山過台灣');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=5),
  '科舉,反清復明,儒學,私塾,書院...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 5, '上', '翰林', 6, '台灣傳統社會與文化與文化的形成');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=6),
  '泰雅族,打耳祭,排灣族,達悟族,阿美族...'
);

-- 6年級 / 南一 / 下學期：刪除舊課次，改用教育百科114_2新資料（共3課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=6 and semester='下' and publisher='南一';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 6, '下', '南一', 1, '生活中的世界文化');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=6 and semester='下' and publisher='南一' and lesson_number=1),
  '佛教,祭祀,有機,機械化,陰符經...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 6, '下', '南一', 2, '科技與生活息息相關');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=6 and semester='下' and publisher='南一' and lesson_number=2),
  '虛擬實境,協定,全球暖化,螢光劑,塑化劑...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 6, '下', '南一', 3, '關懷臺灣與國際議題');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=6 and semester='下' and publisher='南一' and lesson_number=3),
  '壟斷,人權,世界人權宣言,導盲磚,世界展望會...'
);

-- 6年級 / 康軒 / 下學期：刪除舊課次，改用教育百科114_2新資料（共2課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=6 and semester='下' and publisher='康軒';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 6, '下', '康軒', 1, '世界多元文化與科技發展對臺灣的影響');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=6 and semester='下' and publisher='康軒' and lesson_number=1),
  '甲骨文,人工智慧,疫苗,生物科技,再生能源...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 6, '下', '康軒', 2, '臺灣走向世界');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=6 and semester='下' and publisher='康軒' and lesson_number=2),
  '蝗災,齋戒,世界展望會,國際奧林匹克委員會,能見度...'
);

-- 6年級 / 康軒 / 上學期：刪除舊課次，改用教育百科109_1新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=6 and semester='上' and publisher='康軒';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 6, '上', '康軒', 1, '日治時代的殖民統治');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=1),
  '悲憤,效忠,喚醒,割讓,抗爭...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 6, '上', '康軒', 2, '日治時代的經濟發展');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=2),
  '砍伐,壟斷,賦稅,流通,奠定...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 6, '上', '康軒', 3, '日治時代的社會變遷');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=3),
  '風俗習慣,鄉土,改良,榻榻米,工藝...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 6, '上', '康軒', 4, '鄉村與都市');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=4),
  '都市,鄉村,運輸,疏離,熱絡...'
);

-- 6年級 / 翰林 / 下學期：刪除舊課次，改用教育百科114_2新資料（共3課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=6 and semester='下' and publisher='翰林';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 6, '下', '翰林', 1, '永續的經濟發展');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=6 and semester='下' and publisher='翰林' and lesson_number=1),
  '大眾運輸,自動化,人工智慧,世界貿易組織'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 6, '下', '翰林', 2, '促進社會永續發展');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=6 and semester='下' and publisher='翰林' and lesson_number=2),
  '全民健保,就業服務,托育,地球村,聯合國...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 6, '下', '翰林', 3, '環境永續的地球村');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=6 and semester='下' and publisher='翰林' and lesson_number=3),
  '外來種,全球暖化,土地沙漠化,絕種,再生資源...'
);

-- 6年級 / 翰林 / 上學期：刪除舊課次，改用教育百科110_1新資料（共1課）
delete from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
  and grade=6 and semester='上' and publisher='翰林';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='social' and school_level_id=1), 6, '上', '翰林', 1, '自然資源');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=1),
  '多樣性,開發,淡水,國家公園,載量...'
);


-- ============================================================
-- 自然科學：新資料整組取代（版本衝突較大，依規則以新為準）
-- ============================================================

-- 3年級 / 南一 / 下學期：刪除舊課次，改用教育百科114_2新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=3 and semester='下' and publisher='南一';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '下', '南一', 1, '種菜好好玩');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=1),
  '根,菜園,莖,果實,種子...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '下', '南一', 2, '溫度與物質變化的關係');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=2),
  '液態,水蒸氣,凝結,蒸發,凝固...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '下', '南一', 3, '天氣特派員');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=3),
  '氣溫,降雨,觀測,雲量,近海...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '下', '南一', 4, '廚房中的科學');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='下' and publisher='南一' and lesson_number=4),
  '冰糖,調味料,溶解,食鹽'
);

-- 3年級 / 南一 / 上學期：刪除舊課次，改用教育百科114_1新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=3 and semester='上' and publisher='南一';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '南一', 1, '認識植物');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='南一' and lesson_number=1),
  '種子,土壤,花萼,雌蕊,雄蕊...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '南一', 2, '空氣和水');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='南一' and lesson_number=2),
  '流動,傳動,壓縮,物質'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '南一', 3, '認識動物');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='南一' and lesson_number=3),
  '翅膀,脊椎,鰭,軀幹'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '南一', 4, '磁鐵');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='南一' and lesson_number=4),
  '磁力,磁鐵'
);

-- 3年級 / 康軒 / 下學期：刪除舊課次，改用教育百科114_2新資料（共3課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=3 and semester='下' and publisher='康軒';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '下', '康軒', 1, '田園樂');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=1),
  '點播,莖,撒播,肥料,土壤...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '下', '康軒', 2, '溫度變化對物質的影響');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=2),
  '水蒸氣,蒸發,氣態,曝晒,凝固...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '下', '康軒', 3, '我是動物解說員');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='下' and publisher='康軒' and lesson_number=3),
  '野生動物,構造,四肢,軀幹,尾巴...'
);

-- 3年級 / 康軒 / 上學期：刪除舊課次，改用教育百科114_1新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=3 and semester='上' and publisher='康軒';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '康軒', 1, '多采多姿的植物');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=1),
  '鬚根,葉序,葉柄,葉脈,葉緣...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '康軒', 2, '生活中的力');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=2),
  '浮力,風力,彈力,磁極,磁力'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '康軒', 3, '奇妙的空氣');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=3),
  '流動,打氣筒,空氣汙染'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '康軒', 4, '廚房裡的科學');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='康軒' and lesson_number=4),
  '鹼性,酸性,水溶液,溶解,檸檬酸'
);

-- 3年級 / 翰林 / 下學期：刪除舊課次，改用教育百科114_2新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=3 and semester='下' and publisher='翰林';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '下', '翰林', 1, '快樂小農夫');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=1),
  '日照,驅蟲劑,移植,發芽,播種...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '下', '翰林', 2, '千變萬化的水');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=2),
  '發電,節約,凝結,蒸發,凝固...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '下', '翰林', 3, '天氣停看聽');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=3),
  '天氣預報,降雨,氣象,毫米,雨量...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '下', '翰林', 4, '動物王國');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='下' and publisher='翰林' and lesson_number=4),
  '若蟲,構造,多樣性,軀幹,鰭...'
);

-- 3年級 / 翰林 / 上學期：刪除舊課次，改用教育百科113_1新資料（共10課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=3 and semester='上' and publisher='翰林';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '翰林', 1, '植物的莖');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=1),
  '木本,莖,草本,攀爬,爬牆虎...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '翰林', 2, '植物的葉與根');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=2),
  '葉脈,葉形,水稻,葉緣,平行脈...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '翰林', 3, '植物的繁衍與資源永續');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=3),
  '雌蕊,雄蕊,花瓣,花萼,種子...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '翰林', 4, '分辨物質的方法');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=4),
  '食鹽,放大鏡'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '翰林', 5, '物質在水中溶解了');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=5),
  '溶解,量筒,平視,溫度計'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '翰林', 6, '風力與風向');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=6),
  '方位,指北針,風向,風力'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '翰林', 7, '奇妙的空氣');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=7),
  '流動,物質'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '翰林', 8, '空氣、風與生活');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=8),
  '沙丘,風力發電,風帆'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '翰林', 9, '磁鐵的磁力');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=9),
  '磁極,磁力,磁鐵'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 3, '上', '翰林', 10, '磁鐵的祕密');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=3 and semester='上' and publisher='翰林' and lesson_number=10),
  '吸附'
);

-- 4年級 / 南一 / 下學期：刪除舊課次，改用教育百科114_2新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=4 and semester='下' and publisher='南一';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '下', '南一', 1, '生活中有趣的力');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=1),
  '油土,浮體,浮力,作用點'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '下', '南一', 2, '昆蟲家族');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=2),
  '觸角,完全變態,蛹,成蟲,若蟲'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '下', '南一', 3, '水的移動');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=3),
  '連通管原理,水面,虹吸現象,縫隙,毛細現象'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '下', '南一', 4, '了解臺灣的環境');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='下' and publisher='南一' and lesson_number=4),
  '防災,地貌,地震,礫石,地表...'
);

-- 4年級 / 南一 / 上學期：刪除舊課次，改用教育百科114_1新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=4 and semester='上' and publisher='南一';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '上', '南一', 1, '地球的夥伴-日月星辰');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=1),
  '高度角,天體,月相,農曆'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '上', '南一', 2, '水中世界');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=2),
  '沉水,水質,水域,浮水,鰓...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '上', '南一', 3, '光和能源');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=3),
  '火力發電,二氧化碳,節能減碳,能源,能量...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '上', '南一', 4, '電路好好玩');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='上' and publisher='南一' and lesson_number=4),
  '電路,通路,斷路,導電,不良導體...'
);

-- 4年級 / 康軒 / 下學期：刪除舊課次，改用教育百科114_2新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=4 and semester='下' and publisher='康軒';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '下', '康軒', 1, '白天和夜晚的天空');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=1),
  '光害,滿月,指北針,高度角,方位...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '下', '康軒', 2, '水的移動');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=2),
  '毛細現象,擴散,細縫,虹吸現象,連通管原理...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '下', '康軒', 3, '昆蟲大解密');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=3),
  '竹節蟲,口器,蜜源,龍蝨,觸角...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '下', '康軒', 4, '自然資源與利用');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='下' and publisher='康軒' and lesson_number=4),
  '永續,土石流,水土保持,地層下陷,空氣汙染...'
);

-- 4年級 / 康軒 / 上學期：刪除舊課次，改用教育百科114_1新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=4 and semester='上' and publisher='康軒';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '上', '康軒', 1, '地表的靜與動');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=1),
  '沙丘,礫石,地震,震央,震度...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '上', '康軒', 2, '水生生物與環境');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=2),
  '水域,水流,水質,漂浮,沉水...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '上', '康軒', 3, '有趣的聲光現象');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=3),
  '振動,介質,光源,反光,反射...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '上', '康軒', 4, '好玩的電路');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='上' and publisher='康軒' and lesson_number=4),
  '正極,觸電,負極,燈絲,導線...'
);

-- 4年級 / 翰林 / 下學期：刪除舊課次，改用教育百科114_2新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=4 and semester='下' and publisher='翰林';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '下', '翰林', 1, '生活中的力');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=1),
  '水力,風力,活塞,動力,浮力...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '下', '翰林', 2, '水的奇妙現象');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=2),
  '引水,虹吸現象,水平面,連通管原理'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '下', '翰林', 3, '變動的大地');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=3),
  '地震,強風,洪水,沙丘,地表...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '下', '翰林', 4, '能源與電路');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='下' and publisher='翰林' and lesson_number=4),
  '電能,再生能源,光能,熱能,動能...'
);

-- 4年級 / 翰林 / 上學期：刪除舊課次，改用教育百科114_1新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=4 and semester='上' and publisher='翰林';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '上', '翰林', 1, '閃亮的天空');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='上' and publisher='翰林' and lesson_number=1),
  '殘月,滿月,望月,眉月,新月...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '上', '翰林', 2, '水域環境');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='上' and publisher='翰林' and lesson_number=2),
  '睡蓮,浮葉植物,水蘊草,沉水植物,葉柄...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '上', '翰林', 3, '物質變變變');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='上' and publisher='翰林' and lesson_number=3),
  '固態,物質,流水,沖刷,液態...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 4, '上', '翰林', 4, '聲光世界真有趣');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=4 and semester='上' and publisher='翰林' and lesson_number=4),
  '振動,物質,固體,液體,氣體...'
);

-- 5年級 / 南一 / 下學期：刪除舊課次，改用教育百科114_2新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=5 and semester='下' and publisher='南一';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '下', '南一', 1, '星星的世界');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=1),
  '太陽系,天狼星,北斗七星,仙后座,牧夫座...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '下', '南一', 2, '認識燃燒與生鏽');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=2),
  '酸性,鏽,雙氧水,燃點,助燃...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '下', '南一', 3, '動物的生活');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=3),
  '覓食,二分法,母體,卵黃,胎生...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '下', '南一', 4, '聲音與樂器');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='下' and publisher='南一' and lesson_number=4),
  '噪音管制法,噪音,分貝,振動,空氣柱...'
);

-- 5年級 / 南一 / 上學期：刪除舊課次，改用教育百科114_1新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=5 and semester='上' and publisher='南一';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '上', '南一', 1, '太陽與光');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='上' and publisher='南一' and lesson_number=1),
  '春分,軌跡,夏至,秋分,冬至...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '上', '南一', 2, '植物世界');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='上' and publisher='南一' and lesson_number=2),
  '攀緣莖,光合作用,板根,塊根,大花咸豐草...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '上', '南一', 3, '水溶液');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='上' and publisher='南一' and lesson_number=3),
  '溶質,溶劑,石蕊試紙,酸性,鹼性...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '上', '南一', 4, '力與運動');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='上' and publisher='南一' and lesson_number=4),
  '摩擦力,砝碼,彈性限度,彈簧,磁力...'
);

-- 5年級 / 康軒 / 下學期：刪除舊課次，改用教育百科114_2新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=5 and semester='下' and publisher='康軒';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '下', '康軒', 1, '力與運動');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=1),
  '拉力,接觸力,砝碼,彈簧秤,彈性疲乏...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '下', '康軒', 2, '大地的奧祕');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=2),
  '下游,石墨,石膏,硫磺,風化作用...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '下', '康軒', 3, '植物世界面面觀');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=3),
  '落地生根,孢子囊群,蕨類植物,大花咸豐草,羊蹄甲...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '下', '康軒', 4, '熱的作用與傳播');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='下' and publisher='康軒' and lesson_number=4),
  '散熱,保溫,熱輻射,輻射,循環...'
);

-- 5年級 / 康軒 / 上學期：刪除舊課次，改用教育百科114_1新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=5 and semester='上' and publisher='康軒';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '上', '康軒', 1, '動物世界');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=1),
  '紅尾伯勞,黑面琵鷺,遷移,社會行為,築巢...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '上', '康軒', 2, '探索聲光世界');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=2),
  '隔音牆,聚光,凸透鏡,音調,音色...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '上', '康軒', 3, '神祕的天空');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=3),
  '北斗七星,高度角,夏至,春分,秋分...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '上', '康軒', 4, '燃燒與生鏽');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='上' and publisher='康軒' and lesson_number=4),
  '合金,電鍍,防鏽,燃點,助燃...'
);

-- 5年級 / 翰林 / 下學期：刪除舊課次，改用教育百科114_2新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=5 and semester='下' and publisher='翰林';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '下', '翰林', 1, '探索星空的奧祕');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=1),
  '星座,光害,仙后座,北斗七星,北極星...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '下', '翰林', 2, '空氣與燃燒');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=2),
  '燃點,氧氣,氮,氬氣,雙氧水...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '下', '翰林', 3, '防止生鏽與保存食物');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=3),
  '真空,鐵鏽,變因,操作變因,控制變因...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '下', '翰林', 4, '揭祕動物的世界');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='下' and publisher='翰林' and lesson_number=4),
  '口器,覓食,關節,肌肉,骨骼...'
);

-- 5年級 / 翰林 / 上學期：刪除舊課次，改用教育百科114_1新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=5 and semester='上' and publisher='翰林';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '上', '翰林', 1, '太陽的祕密');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=1),
  '綠色能源,晝夜,日晷,夏至,春分...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '上', '翰林', 2, '千變萬化的植物');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=2),
  '子房,授粉,胚珠,花粉,傳播...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '上', '翰林', 3, '神奇的水溶液');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=3),
  '鹼性,導電,中性,酸性,石蕊試紙...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 5, '上', '翰林', 4, '力與運動');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=5 and semester='上' and publisher='翰林' and lesson_number=4),
  '摩擦力,彈性限度,砝碼,彈簧,動能...'
);

-- 6年級 / 南一 / 下學期：刪除舊課次，改用教育百科114_2新資料（共3課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=6 and semester='下' and publisher='南一';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '下', '南一', 1, '巧妙的施力工具');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='下' and publisher='南一' and lesson_number=1),
  '支點,齒輪,鏈條,槓桿,抗力點...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '下', '南一', 2, '地球的環境與生態');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='下' and publisher='南一' and lesson_number=2),
  '生態系,分解者,次級消費者,初級消費者,生產者...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '下', '南一', 3, '我們只有一個地球');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='下' and publisher='南一' and lesson_number=3),
  '水力發電,風力發電,太陽能,絕種,復育...'
);

-- 6年級 / 南一 / 上學期：刪除舊課次，改用教育百科114_1新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=6 and semester='上' and publisher='南一';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '上', '南一', 1, '多樣的天氣變化');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='上' and publisher='南一' and lesson_number=1),
  '冰雹,冰晶,熱帶氣旋,颱風,滯留鋒...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '上', '南一', 2, '熱對物質的影響');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='上' and publisher='南一' and lesson_number=2),
  '熱脹冷縮,傳導,對流,輻射,保溫...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '上', '南一', 3, '變動的大地');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='上' and publisher='南一' and lesson_number=3),
  '石灰岩,遺跡,遺骸,風化作用,硫磺...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '上', '南一', 4, '奇妙的電磁世界');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='上' and publisher='南一' and lesson_number=4),
  '電磁波,線圈,磁場,電磁鐵,地磁...'
);

-- 6年級 / 康軒 / 下學期：刪除舊課次，改用教育百科114_2新資料（共3課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=6 and semester='下' and publisher='康軒';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '下', '康軒', 1, '簡單機械');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='下' and publisher='康軒' and lesson_number=1),
  '支點,抗力點,天平,尖嘴鉗,輪軸...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '下', '康軒', 2, '能量與生活');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='下' and publisher='康軒' and lesson_number=2),
  '風力發電,能量,動能,發光二極體,能源...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '下', '康軒', 3, '地球的生態');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='下' and publisher='康軒' and lesson_number=3),
  '石蓴,生產者,消費者,族群,群集...'
);

-- 6年級 / 康軒 / 上學期：刪除舊課次，改用教育百科114_1新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=6 and semester='上' and publisher='康軒';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '上', '康軒', 1, '探索天氣的變化');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=1),
  '等壓線,氣態,甲烷,化石燃料,大氣層...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '上', '康軒', 2, '水溶液');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=2),
  '水溶液,石蕊試紙,發光二極體,導電,溶劑...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '上', '康軒', 3, '動物大解密');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=3),
  '二分法,養殖,呼吸系統,器官,石灰水...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '上', '康軒', 4, '電磁作用');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='上' and publisher='康軒' and lesson_number=4),
  '指北針,磁性,地磁,電磁鐵,線圈...'
);

-- 6年級 / 翰林 / 下學期：刪除舊課次，改用教育百科114_2新資料（共3課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=6 and semester='下' and publisher='翰林';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '下', '翰林', 1, '簡單機械');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='下' and publisher='翰林' and lesson_number=1),
  '作用點,槓桿,支點,抗力點,輪軸...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '下', '翰林', 2, '生活中的聲音');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='下' and publisher='翰林' and lesson_number=2),
  '弦樂器,空氣柱,管樂器,打擊樂器,音調...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '下', '翰林', 3, '寰宇永續護地球');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='下' and publisher='翰林' and lesson_number=3),
  '永續,寰宇,節約能源,水域,生態系...'
);

-- 6年級 / 翰林 / 上學期：刪除舊課次，改用教育百科114_1新資料（共4課）
delete from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
  and grade=6 and semester='上' and publisher='翰林';
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '上', '翰林', 1, '熱的影響與傳播');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=1),
  '粒子,熱脹冷縮,對流,傳導,傳播...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '上', '翰林', 2, '多變的天氣');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=2),
  '地下水,冷氣團,滯留鋒,暖鋒,冷鋒...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '上', '翰林', 3, '發現大地的奧祕');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=3),
  '板岩,花崗片麻岩,方解石,長石,石英...'
);
insert into curriculum (subject_id, grade, semester, publisher, lesson_number, lesson_name) values
((select id from subjects where code='science' and school_level_id=1), 6, '上', '翰林', 4, '電磁與生活');
insert into vocabulary_words (curriculum_id, words_preview) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1)
   and grade=6 and semester='上' and publisher='翰林' and lesson_number=4),
  '指北針,電磁鐵,磁場,線圈,串聯...'
);
