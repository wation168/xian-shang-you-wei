-- ============================================================
-- 生字/詞彙練習題目 自動產生（由 generate_vocab_questions.py v2 產生）
-- 題型：single_choice（認字歸類）+ true_false（是非題）
-- 已排除 38 筆curriculum資料庫裡不存在的課次（詳見 skipped_lessons.txt）
-- ============================================================

insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 1年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "抹"}, {"key": "B", "text": "瞧"}, {"key": "C", "text": "按時"}, {"key": "D", "text": "充"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第1課節錄）。正確答案「充」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=1),
  'true_false',
  '「抹」是「南一版 1年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第1課節錄）。「抹」出自其他課，非「南一版 1年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 1年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "蜻"}, {"key": "B", "text": "楷模"}, {"key": "C", "text": "嫦娥"}, {"key": "D", "text": "腳跡"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第2課節錄）。正確答案「蜻」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=2),
  'true_false',
  '「蜓」是「南一版 1年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第2課節錄）。「蜓」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 1年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "陪"}, {"key": "B", "text": "樹"}, {"key": "C", "text": "吹奏"}, {"key": "D", "text": "樂"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第3課節錄）。正確答案「樂」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=3),
  'true_false',
  '「陪」是「南一版 1年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第3課節錄）。「陪」出自其他課，非「南一版 1年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 1年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "誰"}, {"key": "B", "text": "蔚"}, {"key": "C", "text": "舟"}, {"key": "D", "text": "薰"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第4課節錄）。正確答案「誰」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=4),
  'true_false',
  '「跟」是「南一版 1年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第4課節錄）。「跟」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=5),
  'single_choice',
  '下列何者是「南一版 1年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "輕"}, {"key": "B", "text": "下午"}, {"key": "C", "text": "豚"}, {"key": "D", "text": "芽"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第5課節錄）。正確答案「輕」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=5),
  'true_false',
  '「豚」是「南一版 1年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第5課節錄）。「豚」出自其他課，非「南一版 1年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=6),
  'single_choice',
  '下列何者是「南一版 1年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "丈"}, {"key": "B", "text": "狩獵"}, {"key": "C", "text": "居"}, {"key": "D", "text": "僮"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第6課節錄）。正確答案「居」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=6),
  'true_false',
  '「孩」是「南一版 1年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第6課節錄）。「孩」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=7),
  'single_choice',
  '下列何者是「南一版 1年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "說"}, {"key": "B", "text": "駕"}, {"key": "C", "text": "啊"}, {"key": "D", "text": "活潑"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第7課節錄）。正確答案「啊」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=7),
  'true_false',
  '「駕」是「南一版 1年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第7課節錄）。「駕」出自其他課，非「南一版 1年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=8),
  'single_choice',
  '下列何者是「南一版 1年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "秋"}, {"key": "B", "text": "下"}, {"key": "C", "text": "斷"}, {"key": "D", "text": "櫛比鱗次"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第8課節錄）。正確答案「秋」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=8),
  'true_false',
  '「果」是「南一版 1年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第8課節錄）。「果」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=9),
  'single_choice',
  '下列何者是「南一版 1年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "珊"}, {"key": "B", "text": "護"}, {"key": "C", "text": "出"}, {"key": "D", "text": "樣"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第9課節錄）。正確答案「樣」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=9),
  'true_false',
  '「護」是「南一版 1年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第9課節錄）。「護」出自其他課，非「南一版 1年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=10),
  'single_choice',
  '下列何者是「南一版 1年級下學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "臉"}, {"key": "B", "text": "名"}, {"key": "C", "text": "彰"}, {"key": "D", "text": "肚子"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第10課節錄）。正確答案「肚子」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=10),
  'true_false',
  '「世界」是「南一版 1年級下學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第10課節錄）。「世界」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=11),
  'single_choice',
  '下列何者是「南一版 1年級下學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "猶"}, {"key": "B", "text": "快樂"}, {"key": "C", "text": "怪"}, {"key": "D", "text": "上"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第11課節錄）。正確答案「怪」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=11),
  'true_false',
  '「上」是「南一版 1年級下學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第11課節錄）。「上」出自其他課，非「南一版 1年級下學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=12),
  'single_choice',
  '下列何者是「南一版 1年級下學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "甜"}, {"key": "B", "text": "馨"}, {"key": "C", "text": "運動會"}, {"key": "D", "text": "凝"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第12課節錄）。正確答案「甜」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='南一' and lesson_number=12),
  'true_false',
  '「分享」是「南一版 1年級下學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級下學期 國語科 第12課節錄）。「分享」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 1年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "恐"}, {"key": "B", "text": "此起彼落"}, {"key": "C", "text": "慌"}, {"key": "D", "text": "上"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級上學期 國語科 第1課節錄）。正確答案「上」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='南一' and lesson_number=1),
  'true_false',
  '「慌」是「南一版 1年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級上學期 國語科 第1課節錄）。「慌」出自其他課，非「南一版 1年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 1年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "地"}, {"key": "B", "text": "憂"}, {"key": "C", "text": "嚇一跳"}, {"key": "D", "text": "破曉"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級上學期 國語科 第2課節錄）。正確答案「地」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='南一' and lesson_number=2),
  'true_false',
  '「開」是「南一版 1年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級上學期 國語科 第2課節錄）。「開」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 1年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "失敗"}, {"key": "B", "text": "辣椒"}, {"key": "C", "text": "我"}, {"key": "D", "text": "億"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級上學期 國語科 第3課節錄）。正確答案「我」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='南一' and lesson_number=3),
  'true_false',
  '「辣椒」是「南一版 1年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級上學期 國語科 第3課節錄）。「辣椒」出自其他課，非「南一版 1年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 1年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "玻"}, {"key": "B", "text": "友"}, {"key": "C", "text": "耐勞"}, {"key": "D", "text": "作"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級上學期 國語科 第4課節錄）。正確答案「友」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='南一' and lesson_number=4),
  'true_false',
  '「一下子」是「南一版 1年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級上學期 國語科 第4課節錄）。「一下子」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='南一' and lesson_number=5),
  'single_choice',
  '下列何者是「南一版 1年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "臺"}, {"key": "B", "text": "穫"}, {"key": "C", "text": "總裁"}, {"key": "D", "text": "什"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級上學期 國語科 第5課節錄）。正確答案「什」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='南一' and lesson_number=5),
  'true_false',
  '「穫」是「南一版 1年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級上學期 國語科 第5課節錄）。「穫」出自其他課，非「南一版 1年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='南一' and lesson_number=6),
  'single_choice',
  '下列何者是「南一版 1年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "嗤之以鼻"}, {"key": "B", "text": "幫"}, {"key": "C", "text": "急診"}, {"key": "D", "text": "話"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級上學期 國語科 第6課節錄）。正確答案「話」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='南一' and lesson_number=6),
  'true_false',
  '「缸」是「南一版 1年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級上學期 國語科 第6課節錄）。「缸」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='南一' and lesson_number=7),
  'single_choice',
  '下列何者是「南一版 1年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "碗"}, {"key": "B", "text": "鍋"}, {"key": "C", "text": "了"}, {"key": "D", "text": "烤"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級上學期 國語科 第7課節錄）。正確答案「了」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='南一' and lesson_number=7),
  'true_false',
  '「碗」是「南一版 1年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 1年級上學期 國語科 第7課節錄）。「碗」出自其他課，非「南一版 1年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 1年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "凌"}, {"key": "B", "text": "屋簷"}, {"key": "C", "text": "靜"}, {"key": "D", "text": "鏡"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第1課節錄）。正確答案「靜」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「凌」是「康軒版 1年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第1課節錄）。「凌」出自其他課，非「康軒版 1年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 1年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "快"}, {"key": "B", "text": "微笑"}, {"key": "C", "text": "吳剛"}, {"key": "D", "text": "清楚"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第2課節錄）。正確答案「快」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「身上」是「康軒版 1年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第2課節錄）。「身上」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 1年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "刷"}, {"key": "B", "text": "價"}, {"key": "C", "text": "義"}, {"key": "D", "text": "音"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第3課節錄）。正確答案「音」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「義」是「康軒版 1年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第3課節錄）。「義」出自其他課，非「康軒版 1年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 1年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "口"}, {"key": "B", "text": "例"}, {"key": "C", "text": "究竟"}, {"key": "D", "text": "遛達"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第4課節錄）。正確答案「口」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「享」是「康軒版 1年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第4課節錄）。「享」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=5),
  'single_choice',
  '下列何者是「康軒版 1年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "公"}, {"key": "B", "text": "肚子"}, {"key": "C", "text": "渺小"}, {"key": "D", "text": "飲"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第5課節錄）。正確答案「公」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=5),
  'true_false',
  '「肚子」是「康軒版 1年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第5課節錄）。「肚子」出自其他課，非「康軒版 1年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=6),
  'single_choice',
  '下列何者是「康軒版 1年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "奶"}, {"key": "B", "text": "幢"}, {"key": "C", "text": "優美"}, {"key": "D", "text": "戴"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第6課節錄）。正確答案「奶」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=6),
  'true_false',
  '「跟」是「康軒版 1年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第6課節錄）。「跟」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=7),
  'single_choice',
  '下列何者是「康軒版 1年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "肌膚"}, {"key": "B", "text": "黑"}, {"key": "C", "text": "窣"}, {"key": "D", "text": "渡"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第7課節錄）。正確答案「黑」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=7),
  'true_false',
  '「窣」是「康軒版 1年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第7課節錄）。「窣」出自其他課，非「康軒版 1年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=8),
  'single_choice',
  '下列何者是「康軒版 1年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "打瞌睡"}, {"key": "B", "text": "爭"}, {"key": "C", "text": "醜"}, {"key": "D", "text": "妹妹"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第8課節錄）。正確答案「妹妹」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=8),
  'true_false',
  '「雙」是「康軒版 1年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第8課節錄）。「雙」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=9),
  'single_choice',
  '下列何者是「康軒版 1年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "請"}, {"key": "B", "text": "激發"}, {"key": "C", "text": "嫦娥"}, {"key": "D", "text": "刷"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第9課節錄）。正確答案「刷」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=9),
  'true_false',
  '「請」是「康軒版 1年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第9課節錄）。「請」出自其他課，非「康軒版 1年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=10),
  'single_choice',
  '下列何者是「康軒版 1年級下學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "飾"}, {"key": "B", "text": "說說笑笑"}, {"key": "C", "text": "先"}, {"key": "D", "text": "靜"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第10課節錄）。正確答案「說說笑笑」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=10),
  'true_false',
  '「地」是「康軒版 1年級下學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第10課節錄）。「地」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=11),
  'single_choice',
  '下列何者是「康軒版 1年級下學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "智"}, {"key": "B", "text": "福"}, {"key": "C", "text": "傍晚"}, {"key": "D", "text": "調色盤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第11課節錄）。正確答案「福」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=11),
  'true_false',
  '「智」是「康軒版 1年級下學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第11課節錄）。「智」出自其他課，非「康軒版 1年級下學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=12),
  'single_choice',
  '下列何者是「康軒版 1年級下學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "胸膛"}, {"key": "B", "text": "磁"}, {"key": "C", "text": "最"}, {"key": "D", "text": "幫"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第12課節錄）。正確答案「幫」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='康軒' and lesson_number=12),
  'true_false',
  '「加油」是「康軒版 1年級下學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級下學期 國語科 第12課節錄）。「加油」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 1年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "蟹"}, {"key": "B", "text": "緩"}, {"key": "C", "text": "手"}, {"key": "D", "text": "次"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級上學期 國語科 第1課節錄）。正確答案「手」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「蟹」是「康軒版 1年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級上學期 國語科 第1課節錄）。「蟹」出自其他課，非「康軒版 1年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 1年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "奇怪"}, {"key": "B", "text": "說"}, {"key": "C", "text": "誰"}, {"key": "D", "text": "昂"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級上學期 國語科 第2課節錄）。正確答案「誰」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「這」是「康軒版 1年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級上學期 國語科 第2課節錄）。「這」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 1年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "陪"}, {"key": "B", "text": "聽見"}, {"key": "C", "text": "豪"}, {"key": "D", "text": "渡"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級上學期 國語科 第3課節錄）。正確答案「陪」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「聽見」是「康軒版 1年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級上學期 國語科 第3課節錄）。「聽見」出自其他課，非「康軒版 1年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 1年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "滋"}, {"key": "B", "text": "隻"}, {"key": "C", "text": "旋"}, {"key": "D", "text": "功"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級上學期 國語科 第4課節錄）。正確答案「隻」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「子」是「康軒版 1年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級上學期 國語科 第4課節錄）。「子」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='康軒' and lesson_number=5),
  'single_choice',
  '下列何者是「康軒版 1年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "彩虹"}, {"key": "B", "text": "裡"}, {"key": "C", "text": "帝"}, {"key": "D", "text": "凝"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級上學期 國語科 第5課節錄）。正確答案「裡」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='康軒' and lesson_number=5),
  'true_false',
  '「彩虹」是「康軒版 1年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級上學期 國語科 第5課節錄）。「彩虹」出自其他課，非「康軒版 1年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='康軒' and lesson_number=6),
  'single_choice',
  '下列何者是「康軒版 1年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "一頭"}, {"key": "B", "text": "錶"}, {"key": "C", "text": "盞"}, {"key": "D", "text": "汽"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級上學期 國語科 第6課節錄）。正確答案「一頭」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='康軒' and lesson_number=6),
  'true_false',
  '「紅花」是「康軒版 1年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 1年級上學期 國語科 第6課節錄）。「紅花」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 1年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "裡"}, {"key": "B", "text": "顯"}, {"key": "C", "text": "材"}, {"key": "D", "text": "避免"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第1課節錄）。正確答案「裡」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「顯」是「翰林版 1年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第1課節錄）。「顯」出自其他課，非「翰林版 1年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 1年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "慈"}, {"key": "B", "text": "手"}, {"key": "C", "text": "螃蟹"}, {"key": "D", "text": "臣"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第2課節錄）。正確答案「手」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「愛」是「翰林版 1年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第2課節錄）。「愛」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 1年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "試"}, {"key": "B", "text": "鴨"}, {"key": "C", "text": "介"}, {"key": "D", "text": "涼"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第3課節錄）。正確答案「涼」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「鴨」是「翰林版 1年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第3課節錄）。「鴨」出自其他課，非「翰林版 1年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 1年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "賴"}, {"key": "B", "text": "卡"}, {"key": "C", "text": "洗"}, {"key": "D", "text": "毋"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第4課節錄）。正確答案「卡」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「片」是「翰林版 1年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第4課節錄）。「片」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=5),
  'single_choice',
  '下列何者是「翰林版 1年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "巡視"}, {"key": "B", "text": "先"}, {"key": "C", "text": "智"}, {"key": "D", "text": "擇"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第5課節錄）。正確答案「先」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=5),
  'true_false',
  '「擇」是「翰林版 1年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第5課節錄）。「擇」出自其他課，非「翰林版 1年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=6),
  'single_choice',
  '下列何者是「翰林版 1年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "緊繃"}, {"key": "B", "text": "葉子"}, {"key": "C", "text": "星"}, {"key": "D", "text": "輯"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第6課節錄）。正確答案「葉子」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=6),
  'true_false',
  '「毛」是「翰林版 1年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第6課節錄）。「毛」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=7),
  'single_choice',
  '下列何者是「翰林版 1年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "自"}, {"key": "B", "text": "急診"}, {"key": "C", "text": "疑惑"}, {"key": "D", "text": "另外"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第7課節錄）。正確答案「自」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=7),
  'true_false',
  '「另外」是「翰林版 1年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第7課節錄）。「另外」出自其他課，非「翰林版 1年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=8),
  'single_choice',
  '下列何者是「翰林版 1年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "教"}, {"key": "B", "text": "格格不入"}, {"key": "C", "text": "鹹"}, {"key": "D", "text": "批"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第8課節錄）。正確答案「教」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=8),
  'true_false',
  '「等」是「翰林版 1年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第8課節錄）。「等」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=9),
  'single_choice',
  '下列何者是「翰林版 1年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "枚"}, {"key": "B", "text": "櫛比鱗次"}, {"key": "C", "text": "得"}, {"key": "D", "text": "便條"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第9課節錄）。正確答案「得」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=9),
  'true_false',
  '「櫛比鱗次」是「翰林版 1年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第9課節錄）。「櫛比鱗次」出自其他課，非「翰林版 1年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=10),
  'single_choice',
  '下列何者是「翰林版 1年級下學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "聽見"}, {"key": "B", "text": "里"}, {"key": "C", "text": "症"}, {"key": "D", "text": "貪"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第10課節錄）。正確答案「聽見」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=10),
  'true_false',
  '「棵」是「翰林版 1年級下學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第10課節錄）。「棵」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=11),
  'single_choice',
  '下列何者是「翰林版 1年級下學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "淺"}, {"key": "B", "text": "編"}, {"key": "C", "text": "學"}, {"key": "D", "text": "糯"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第11課節錄）。正確答案「學」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=11),
  'true_false',
  '「淺」是「翰林版 1年級下學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第11課節錄）。「淺」出自其他課，非「翰林版 1年級下學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=12),
  'single_choice',
  '下列何者是「翰林版 1年級下學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "遍"}, {"key": "B", "text": "坎坷"}, {"key": "C", "text": "最"}, {"key": "D", "text": "段"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第12課節錄）。正確答案「段」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='下' and publisher='翰林' and lesson_number=12),
  'true_false',
  '「同學」是「翰林版 1年級下學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級下學期 國語科 第12課節錄）。「同學」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 1年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "逐漸"}, {"key": "B", "text": "走"}, {"key": "C", "text": "曠"}, {"key": "D", "text": "任"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級上學期 國語科 第1課節錄）。正確答案「走」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「逐漸」是「翰林版 1年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級上學期 國語科 第1課節錄）。「逐漸」出自其他課，非「翰林版 1年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 1年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "試"}, {"key": "B", "text": "爾"}, {"key": "C", "text": "大"}, {"key": "D", "text": "沉"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級上學期 國語科 第2課節錄）。正確答案「大」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「風」是「翰林版 1年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級上學期 國語科 第2課節錄）。「風」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 1年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "人民"}, {"key": "B", "text": "首"}, {"key": "C", "text": "一個"}, {"key": "D", "text": "抖"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級上學期 國語科 第3課節錄）。正確答案「一個」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「人民」是「翰林版 1年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級上學期 國語科 第3課節錄）。「人民」出自其他課，非「翰林版 1年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 1年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "影"}, {"key": "B", "text": "少"}, {"key": "C", "text": "溼"}, {"key": "D", "text": "貌"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級上學期 國語科 第4課節錄）。正確答案「少」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「請」是「翰林版 1年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級上學期 國語科 第4課節錄）。「請」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='翰林' and lesson_number=5),
  'single_choice',
  '下列何者是「翰林版 1年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "承認"}, {"key": "B", "text": "看"}, {"key": "C", "text": "巨人"}, {"key": "D", "text": "予"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級上學期 國語科 第5課節錄）。正確答案「看」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='翰林' and lesson_number=5),
  'true_false',
  '「巨人」是「翰林版 1年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級上學期 國語科 第5課節錄）。「巨人」出自其他課，非「翰林版 1年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='翰林' and lesson_number=6),
  'single_choice',
  '下列何者是「翰林版 1年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "貪"}, {"key": "B", "text": "兵馬俑"}, {"key": "C", "text": "陪"}, {"key": "D", "text": "什"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級上學期 國語科 第6課節錄）。正確答案「陪」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='翰林' and lesson_number=6),
  'true_false',
  '「千」是「翰林版 1年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級上學期 國語科 第6課節錄）。「千」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='翰林' and lesson_number=7),
  'single_choice',
  '下列何者是「翰林版 1年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "我"}, {"key": "B", "text": "回"}, {"key": "C", "text": "籟"}, {"key": "D", "text": "掠食者"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級上學期 國語科 第7課節錄）。正確答案「回」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=1 and semester='上' and publisher='翰林' and lesson_number=7),
  'true_false',
  '「我」是「翰林版 1年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 1年級上學期 國語科 第7課節錄）。「我」出自其他課，非「翰林版 1年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 2年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "王宮"}, {"key": "B", "text": "情緒"}, {"key": "C", "text": "火紅"}, {"key": "D", "text": "焦急"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第1課節錄）。正確答案「火紅」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=1),
  'true_false',
  '「王宮」是「南一版 2年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第1課節錄）。「王宮」出自其他課，非「南一版 2年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 2年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "仔"}, {"key": "B", "text": "慶"}, {"key": "C", "text": "憂"}, {"key": "D", "text": "哥"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第2課節錄）。正確答案「哥」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=2),
  'true_false',
  '「盆」是「南一版 2年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第2課節錄）。「盆」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 2年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "孤寂"}, {"key": "B", "text": "參"}, {"key": "C", "text": "啦"}, {"key": "D", "text": "相信"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第3課節錄）。正確答案「啦」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=3),
  'true_false',
  '「相信」是「南一版 2年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第3課節錄）。「相信」出自其他課，非「南一版 2年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 2年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "姐"}, {"key": "B", "text": "綺麗"}, {"key": "C", "text": "居"}, {"key": "D", "text": "鬆"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第4課節錄）。正確答案「姐」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=4),
  'true_false',
  '「懶」是「南一版 2年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第4課節錄）。「懶」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=5),
  'single_choice',
  '下列何者是「南一版 2年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "耕耘"}, {"key": "B", "text": "議"}, {"key": "C", "text": "忍"}, {"key": "D", "text": "偷"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第5課節錄）。正確答案「忍」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=5),
  'true_false',
  '「偷」是「南一版 2年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第5課節錄）。「偷」出自其他課，非「南一版 2年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=6),
  'single_choice',
  '下列何者是「南一版 2年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "淹"}, {"key": "B", "text": "言"}, {"key": "C", "text": "洋"}, {"key": "D", "text": "決定"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第6課節錄）。正確答案「決定」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=6),
  'true_false',
  '「浪費」是「南一版 2年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第6課節錄）。「浪費」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=7),
  'single_choice',
  '下列何者是「南一版 2年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "答"}, {"key": "B", "text": "轟"}, {"key": "C", "text": "妹妹"}, {"key": "D", "text": "熬煮"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第7課節錄）。正確答案「答」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=7),
  'true_false',
  '「熬煮」是「南一版 2年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第7課節錄）。「熬煮」出自其他課，非「南一版 2年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=8),
  'single_choice',
  '下列何者是「南一版 2年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "釐"}, {"key": "B", "text": "湯圓"}, {"key": "C", "text": "小路"}, {"key": "D", "text": "摘花"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第8課節錄）。正確答案「摘花」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=8),
  'true_false',
  '「布告牌」是「南一版 2年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第8課節錄）。「布告牌」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=9),
  'single_choice',
  '下列何者是「南一版 2年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "垃"}, {"key": "B", "text": "註定"}, {"key": "C", "text": "息"}, {"key": "D", "text": "盡頭"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第9課節錄）。正確答案「息」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=9),
  'true_false',
  '「盡頭」是「南一版 2年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第9課節錄）。「盡頭」出自其他課，非「南一版 2年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=10),
  'single_choice',
  '下列何者是「南一版 2年級下學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鼻"}, {"key": "B", "text": "微"}, {"key": "C", "text": "原狀"}, {"key": "D", "text": "擇"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第10課節錄）。正確答案「原狀」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=10),
  'true_false',
  '「明白」是「南一版 2年級下學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第10課節錄）。「明白」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=11),
  'single_choice',
  '下列何者是「南一版 2年級下學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "醜"}, {"key": "B", "text": "輕舟"}, {"key": "C", "text": "講"}, {"key": "D", "text": "節省"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第11課節錄）。正確答案「講」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=11),
  'true_false',
  '「輕舟」是「南一版 2年級下學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第11課節錄）。「輕舟」出自其他課，非「南一版 2年級下學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=12),
  'single_choice',
  '下列何者是「南一版 2年級下學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "臣"}, {"key": "B", "text": "熟"}, {"key": "C", "text": "其"}, {"key": "D", "text": "北極"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第12課節錄）。正確答案「北極」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='南一' and lesson_number=12),
  'true_false',
  '「由」是「南一版 2年級下學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級下學期 國語科 第12課節錄）。「由」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 2年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "異口同聲"}, {"key": "B", "text": "滲入"}, {"key": "C", "text": "辛苦"}, {"key": "D", "text": "白"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第1課節錄）。正確答案「白」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=1),
  'true_false',
  '「滲入」是「南一版 2年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第1課節錄）。「滲入」出自其他課，非「南一版 2年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 2年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "抹"}, {"key": "B", "text": "最"}, {"key": "C", "text": "向"}, {"key": "D", "text": "節"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第2課節錄）。正確答案「最」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=2),
  'true_false',
  '「梯子」是「南一版 2年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第2課節錄）。「梯子」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 2年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "焰"}, {"key": "B", "text": "室"}, {"key": "C", "text": "鮮豔"}, {"key": "D", "text": "找尋"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第3課節錄）。正確答案「室」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=3),
  'true_false',
  '「鮮豔」是「南一版 2年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第3課節錄）。「鮮豔」出自其他課，非「南一版 2年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 2年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "烤爐"}, {"key": "B", "text": "次"}, {"key": "C", "text": "包"}, {"key": "D", "text": "書籤"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第4課節錄）。正確答案「包」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=4),
  'true_false',
  '「遊」是「南一版 2年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第4課節錄）。「遊」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=5),
  'single_choice',
  '下列何者是「南一版 2年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "種"}, {"key": "B", "text": "閱讀"}, {"key": "C", "text": "灘"}, {"key": "D", "text": "健"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第5課節錄）。正確答案「種」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=5),
  'true_false',
  '「閱讀」是「南一版 2年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第5課節錄）。「閱讀」出自其他課，非「南一版 2年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=6),
  'single_choice',
  '下列何者是「南一版 2年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "少"}, {"key": "B", "text": "肯定"}, {"key": "C", "text": "留"}, {"key": "D", "text": "蝴蝶"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第6課節錄）。正確答案「留」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=6),
  'true_false',
  '「自」是「南一版 2年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第6課節錄）。「自」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=7),
  'single_choice',
  '下列何者是「南一版 2年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "彌"}, {"key": "B", "text": "餘"}, {"key": "C", "text": "耕"}, {"key": "D", "text": "殷勤"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第7課節錄）。正確答案「耕」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=7),
  'true_false',
  '「餘」是「南一版 2年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第7課節錄）。「餘」出自其他課，非「南一版 2年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=8),
  'single_choice',
  '下列何者是「南一版 2年級上學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "掏出"}, {"key": "B", "text": "圖書館"}, {"key": "C", "text": "嚇"}, {"key": "D", "text": "愜"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第8課節錄）。正確答案「嚇」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=8),
  'true_false',
  '「鹿」是「南一版 2年級上學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第8課節錄）。「鹿」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=9),
  'single_choice',
  '下列何者是「南一版 2年級上學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "機會"}, {"key": "B", "text": "法"}, {"key": "C", "text": "樹木"}, {"key": "D", "text": "碎"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第9課節錄）。正確答案「法」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=9),
  'true_false',
  '「樹木」是「南一版 2年級上學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第9課節錄）。「樹木」出自其他課，非「南一版 2年級上學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=10),
  'single_choice',
  '下列何者是「南一版 2年級上學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "依依不捨"}, {"key": "B", "text": "灘"}, {"key": "C", "text": "玻"}, {"key": "D", "text": "拚"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第10課節錄）。正確答案「依依不捨」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=10),
  'true_false',
  '「群」是「南一版 2年級上學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第10課節錄）。「群」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=11),
  'single_choice',
  '下列何者是「南一版 2年級上學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "尷尬"}, {"key": "B", "text": "接"}, {"key": "C", "text": "剖"}, {"key": "D", "text": "澈"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第11課節錄）。正確答案「接」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=11),
  'true_false',
  '「澈」是「南一版 2年級上學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第11課節錄）。「澈」出自其他課，非「南一版 2年級上學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=12),
  'single_choice',
  '下列何者是「南一版 2年級上學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "走廊"}, {"key": "B", "text": "調"}, {"key": "C", "text": "茂"}, {"key": "D", "text": "凋"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第12課節錄）。正確答案「調」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='南一' and lesson_number=12),
  'true_false',
  '「魚兒」是「南一版 2年級上學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 2年級上學期 國語科 第12課節錄）。「魚兒」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 2年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "姐"}, {"key": "B", "text": "池"}, {"key": "C", "text": "嘟"}, {"key": "D", "text": "蔚"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第1課節錄）。正確答案「池」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「蔚」是「康軒版 2年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第1課節錄）。「蔚」出自其他課，非「康軒版 2年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 2年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "離"}, {"key": "B", "text": "倒塌"}, {"key": "C", "text": "剪"}, {"key": "D", "text": "跨欄"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第2課節錄）。正確答案「剪」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「慶」是「康軒版 2年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第2課節錄）。「慶」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 2年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "畫"}, {"key": "B", "text": "如果"}, {"key": "C", "text": "安"}, {"key": "D", "text": "盞"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第3課節錄）。正確答案「如果」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「盞」是「康軒版 2年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第3課節錄）。「盞」出自其他課，非「康軒版 2年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 2年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "陰霾"}, {"key": "B", "text": "永"}, {"key": "C", "text": "明白"}, {"key": "D", "text": "雪"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第4課節錄）。正確答案「永」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「窗」是「康軒版 2年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第4課節錄）。「窗」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=5),
  'single_choice',
  '下列何者是「康軒版 2年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "窗"}, {"key": "B", "text": "貝"}, {"key": "C", "text": "我"}, {"key": "D", "text": "鋪陳"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第5課節錄）。正確答案「貝」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=5),
  'true_false',
  '「鋪陳」是「康軒版 2年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第5課節錄）。「鋪陳」出自其他課，非「康軒版 2年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=6),
  'single_choice',
  '下列何者是「康軒版 2年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "種"}, {"key": "B", "text": "答案"}, {"key": "C", "text": "哥哥"}, {"key": "D", "text": "垂掛"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第6課節錄）。正確答案「哥哥」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=6),
  'true_false',
  '「腳踏車」是「康軒版 2年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第6課節錄）。「腳踏車」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=7),
  'single_choice',
  '下列何者是「康軒版 2年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "清楚"}, {"key": "B", "text": "霸"}, {"key": "C", "text": "鼻"}, {"key": "D", "text": "啦"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第7課節錄）。正確答案「鼻」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=7),
  'true_false',
  '「啦」是「康軒版 2年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第7課節錄）。「啦」出自其他課，非「康軒版 2年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=8),
  'single_choice',
  '下列何者是「康軒版 2年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "老虎"}, {"key": "B", "text": "相信"}, {"key": "C", "text": "寂"}, {"key": "D", "text": "晾乾"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第8課節錄）。正確答案「相信」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=8),
  'true_false',
  '「議」是「康軒版 2年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第8課節錄）。「議」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=9),
  'single_choice',
  '下列何者是「康軒版 2年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "圃"}, {"key": "B", "text": "雛鳥"}, {"key": "C", "text": "抓"}, {"key": "D", "text": "縱"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第9課節錄）。正確答案「抓」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=9),
  'true_false',
  '「雛鳥」是「康軒版 2年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第9課節錄）。「雛鳥」出自其他課，非「康軒版 2年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=10),
  'single_choice',
  '下列何者是「康軒版 2年級下學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "建築"}, {"key": "B", "text": "蹦蹦跳跳"}, {"key": "C", "text": "休克"}, {"key": "D", "text": "白紙"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第10課節錄）。正確答案「蹦蹦跳跳」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=10),
  'true_false',
  '「琅琅」是「康軒版 2年級下學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第10課節錄）。「琅琅」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=11),
  'single_choice',
  '下列何者是「康軒版 2年級下學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "經過"}, {"key": "B", "text": "砂"}, {"key": "C", "text": "漿"}, {"key": "D", "text": "庫"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第11課節錄）。正確答案「庫」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=11),
  'true_false',
  '「經過」是「康軒版 2年級下學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第11課節錄）。「經過」出自其他課，非「康軒版 2年級下學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=12),
  'single_choice',
  '下列何者是「康軒版 2年級下學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鱗"}, {"key": "B", "text": "孤陋寡聞"}, {"key": "C", "text": "喝"}, {"key": "D", "text": "量"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第12課節錄）。正確答案「量」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='康軒' and lesson_number=12),
  'true_false',
  '「到底」是「康軒版 2年級下學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級下學期 國語科 第12課節錄）。「到底」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 2年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "態"}, {"key": "B", "text": "池"}, {"key": "C", "text": "腳踏車"}, {"key": "D", "text": "老師"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第1課節錄）。正確答案「老師」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「腳踏車」是「康軒版 2年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第1課節錄）。「腳踏車」出自其他課，非「康軒版 2年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 2年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "疑惑"}, {"key": "B", "text": "扭"}, {"key": "C", "text": "一輩子"}, {"key": "D", "text": "臉"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第2課節錄）。正確答案「臉」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「餐」是「康軒版 2年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第2課節錄）。「餐」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 2年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "轉"}, {"key": "B", "text": "叔"}, {"key": "C", "text": "唱歌"}, {"key": "D", "text": "避免"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第3課節錄）。正確答案「叔」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「轉」是「康軒版 2年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第3課節錄）。「轉」出自其他課，非「康軒版 2年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 2年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "拘"}, {"key": "B", "text": "最"}, {"key": "C", "text": "床"}, {"key": "D", "text": "牙齒"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第4課節錄）。正確答案「最」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「可」是「康軒版 2年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第4課節錄）。「可」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=5),
  'single_choice',
  '下列何者是「康軒版 2年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "溫"}, {"key": "B", "text": "宙"}, {"key": "C", "text": "恐懼"}, {"key": "D", "text": "碗"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第5課節錄）。正確答案「碗」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=5),
  'true_false',
  '「宙」是「康軒版 2年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第5課節錄）。「宙」出自其他課，非「康軒版 2年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=6),
  'single_choice',
  '下列何者是「康軒版 2年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "尋找"}, {"key": "B", "text": "喉嚨"}, {"key": "C", "text": "親朋好友"}, {"key": "D", "text": "搧風"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第6課節錄）。正確答案「親朋好友」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=6),
  'true_false',
  '「如意」是「康軒版 2年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第6課節錄）。「如意」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=7),
  'single_choice',
  '下列何者是「康軒版 2年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "重殘"}, {"key": "B", "text": "第"}, {"key": "C", "text": "削"}, {"key": "D", "text": "滿"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第7課節錄）。正確答案「滿」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=7),
  'true_false',
  '「第」是「康軒版 2年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第7課節錄）。「第」出自其他課，非「康軒版 2年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=8),
  'single_choice',
  '下列何者是「康軒版 2年級上學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "抱"}, {"key": "B", "text": "喝"}, {"key": "C", "text": "瑚"}, {"key": "D", "text": "通"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第8課節錄）。正確答案「喝」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=8),
  'true_false',
  '「法」是「康軒版 2年級上學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第8課節錄）。「法」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=9),
  'single_choice',
  '下列何者是「康軒版 2年級上學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "大"}, {"key": "B", "text": "桿"}, {"key": "C", "text": "然"}, {"key": "D", "text": "緊繃"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第9課節錄）。正確答案「然」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=9),
  'true_false',
  '「大」是「康軒版 2年級上學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第9課節錄）。「大」出自其他課，非「康軒版 2年級上學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=10),
  'single_choice',
  '下列何者是「康軒版 2年級上學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "蘊含"}, {"key": "B", "text": "橙色"}, {"key": "C", "text": "碳"}, {"key": "D", "text": "季"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第10課節錄）。正確答案「季」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=10),
  'true_false',
  '「貨」是「康軒版 2年級上學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第10課節錄）。「貨」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=11),
  'single_choice',
  '下列何者是「康軒版 2年級上學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "充"}, {"key": "B", "text": "獨立"}, {"key": "C", "text": "驅使"}, {"key": "D", "text": "會場"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第11課節錄）。正確答案「充」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=11),
  'true_false',
  '「會場」是「康軒版 2年級上學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第11課節錄）。「會場」出自其他課，非「康軒版 2年級上學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=12),
  'single_choice',
  '下列何者是「康軒版 2年級上學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "字"}, {"key": "B", "text": "的"}, {"key": "C", "text": "渡"}, {"key": "D", "text": "居然"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第12課節錄）。正確答案「居然」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='康軒' and lesson_number=12),
  'true_false',
  '「妙」是「康軒版 2年級上學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 2年級上學期 國語科 第12課節錄）。「妙」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 2年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "昭和草"}, {"key": "B", "text": "狐"}, {"key": "C", "text": "陌生"}, {"key": "D", "text": "缸"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第1課節錄）。正確答案「昭和草」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「陌生」是「翰林版 2年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第1課節錄）。「陌生」出自其他課，非「翰林版 2年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 2年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "抓"}, {"key": "B", "text": "提"}, {"key": "C", "text": "配"}, {"key": "D", "text": "飾"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第2課節錄）。正確答案「提」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「漠」是「翰林版 2年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第2課節錄）。「漠」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 2年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "紫"}, {"key": "B", "text": "福"}, {"key": "C", "text": "棚"}, {"key": "D", "text": "諺語"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第3課節錄）。正確答案「紫」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「福」是「翰林版 2年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第3課節錄）。「福」出自其他課，非「翰林版 2年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 2年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "爺"}, {"key": "B", "text": "潔"}, {"key": "C", "text": "亞"}, {"key": "D", "text": "打破"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第4課節錄）。正確答案「爺」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「剛」是「翰林版 2年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第4課節錄）。「剛」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=5),
  'single_choice',
  '下列何者是「翰林版 2年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "貪"}, {"key": "B", "text": "凸"}, {"key": "C", "text": "利"}, {"key": "D", "text": "愜"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第5課節錄）。正確答案「利」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=5),
  'true_false',
  '「愜」是「翰林版 2年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第5課節錄）。「愜」出自其他課，非「翰林版 2年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=6),
  'single_choice',
  '下列何者是「翰林版 2年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "江"}, {"key": "B", "text": "製作"}, {"key": "C", "text": "自從"}, {"key": "D", "text": "糊"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第6課節錄）。正確答案「自從」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=6),
  'true_false',
  '「禮貌」是「翰林版 2年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第6課節錄）。「禮貌」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=7),
  'single_choice',
  '下列何者是「翰林版 2年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "愉悅"}, {"key": "B", "text": "沾"}, {"key": "C", "text": "幾"}, {"key": "D", "text": "儘管"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第7課節錄）。正確答案「幾」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=7),
  'true_false',
  '「愉悅」是「翰林版 2年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第7課節錄）。「愉悅」出自其他課，非「翰林版 2年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=8),
  'single_choice',
  '下列何者是「翰林版 2年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "晨"}, {"key": "B", "text": "生日"}, {"key": "C", "text": "原諒"}, {"key": "D", "text": "鏡"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第8課節錄）。正確答案「晨」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=8),
  'true_false',
  '「離開」是「翰林版 2年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第8課節錄）。「離開」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=9),
  'single_choice',
  '下列何者是「翰林版 2年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "呼"}, {"key": "B", "text": "獨"}, {"key": "C", "text": "礦"}, {"key": "D", "text": "節省"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第9課節錄）。正確答案「呼」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=9),
  'true_false',
  '「獨」是「翰林版 2年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第9課節錄）。「獨」出自其他課，非「翰林版 2年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=10),
  'single_choice',
  '下列何者是「翰林版 2年級下學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "軌道"}, {"key": "B", "text": "打破"}, {"key": "C", "text": "褐"}, {"key": "D", "text": "呆頭呆腦"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第10課節錄）。正確答案「打破」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=10),
  'true_false',
  '「醜」是「翰林版 2年級下學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第10課節錄）。「醜」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=11),
  'single_choice',
  '下列何者是「翰林版 2年級下學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "護"}, {"key": "B", "text": "烤"}, {"key": "C", "text": "豐富"}, {"key": "D", "text": "算"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第11課節錄）。正確答案「算」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=11),
  'true_false',
  '「烤」是「翰林版 2年級下學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第11課節錄）。「烤」出自其他課，非「翰林版 2年級下學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=12),
  'single_choice',
  '下列何者是「翰林版 2年級下學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "揭開"}, {"key": "B", "text": "愁"}, {"key": "C", "text": "搭配"}, {"key": "D", "text": "運動"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第12課節錄）。正確答案「運動」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='下' and publisher='翰林' and lesson_number=12),
  'true_false',
  '「夜夜」是「翰林版 2年級下學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級下學期 國語科 第12課節錄）。「夜夜」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 2年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "開朗"}, {"key": "B", "text": "梯"}, {"key": "C", "text": "狐"}, {"key": "D", "text": "颳"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第1課節錄）。正確答案「颳」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「狐」是「翰林版 2年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第1課節錄）。「狐」出自其他課，非「翰林版 2年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 2年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "擊退"}, {"key": "B", "text": "缸"}, {"key": "C", "text": "熟"}, {"key": "D", "text": "最"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第2課節錄）。正確答案「熟」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「師」是「翰林版 2年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第2課節錄）。「師」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 2年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "寫"}, {"key": "B", "text": "貪"}, {"key": "C", "text": "一點"}, {"key": "D", "text": "善意"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第3課節錄）。正確答案「一點」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「寫」是「翰林版 2年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第3課節錄）。「寫」出自其他課，非「翰林版 2年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 2年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鋸"}, {"key": "B", "text": "明"}, {"key": "C", "text": "僮"}, {"key": "D", "text": "架"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第4課節錄）。正確答案「明」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「頂」是「翰林版 2年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第4課節錄）。「頂」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=5),
  'single_choice',
  '下列何者是「翰林版 2年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "牠們"}, {"key": "B", "text": "夕"}, {"key": "C", "text": "暢"}, {"key": "D", "text": "建築"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第5課節錄）。正確答案「夕」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=5),
  'true_false',
  '「牠們」是「翰林版 2年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第5課節錄）。「牠們」出自其他課，非「翰林版 2年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=6),
  'single_choice',
  '下列何者是「翰林版 2年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "盡頭"}, {"key": "B", "text": "孤寂"}, {"key": "C", "text": "阱"}, {"key": "D", "text": "迴盪"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第6課節錄）。正確答案「盡頭」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=6),
  'true_false',
  '「眼睛」是「翰林版 2年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第6課節錄）。「眼睛」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=7),
  'single_choice',
  '下列何者是「翰林版 2年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "隻"}, {"key": "B", "text": "綻"}, {"key": "C", "text": "瀑布"}, {"key": "D", "text": "安"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第7課節錄）。正確答案「安」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=7),
  'true_false',
  '「綻」是「翰林版 2年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第7課節錄）。「綻」出自其他課，非「翰林版 2年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=8),
  'single_choice',
  '下列何者是「翰林版 2年級上學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "健"}, {"key": "B", "text": "介"}, {"key": "C", "text": "大喊"}, {"key": "D", "text": "言簡意賅"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第8課節錄）。正確答案「介」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=8),
  'true_false',
  '「米線」是「翰林版 2年級上學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第8課節錄）。「米線」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=9),
  'single_choice',
  '下列何者是「翰林版 2年級上學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "蛋"}, {"key": "B", "text": "縮短"}, {"key": "C", "text": "速度"}, {"key": "D", "text": "車"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第9課節錄）。正確答案「蛋」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=9),
  'true_false',
  '「速度」是「翰林版 2年級上學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第9課節錄）。「速度」出自其他課，非「翰林版 2年級上學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=10),
  'single_choice',
  '下列何者是「翰林版 2年級上學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "光芒"}, {"key": "B", "text": "橡皮擦"}, {"key": "C", "text": "抓住"}, {"key": "D", "text": "突然"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第10課節錄）。正確答案「突然」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=10),
  'true_false',
  '「異口同聲」是「翰林版 2年級上學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第10課節錄）。「異口同聲」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=11),
  'single_choice',
  '下列何者是「翰林版 2年級上學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "輾轉"}, {"key": "B", "text": "鈴"}, {"key": "C", "text": "底"}, {"key": "D", "text": "渺小"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第11課節錄）。正確答案「底」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=11),
  'true_false',
  '「輾轉」是「翰林版 2年級上學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第11課節錄）。「輾轉」出自其他課，非「翰林版 2年級上學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=12),
  'single_choice',
  '下列何者是「翰林版 2年級上學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "潔"}, {"key": "B", "text": "隻"}, {"key": "C", "text": "教"}, {"key": "D", "text": "辣椒"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第12課節錄）。正確答案「隻」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=2 and semester='上' and publisher='翰林' and lesson_number=12),
  'true_false',
  '「肚皮」是「翰林版 2年級上學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 2年級上學期 國語科 第12課節錄）。「肚皮」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 3年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "抬"}, {"key": "B", "text": "隻"}, {"key": "C", "text": "首"}, {"key": "D", "text": "頤"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第1課節錄）。正確答案「首」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=1),
  'true_false',
  '「隻」是「南一版 3年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第1課節錄）。「隻」出自其他課，非「南一版 3年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 3年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "幸福"}, {"key": "B", "text": "護"}, {"key": "C", "text": "錢"}, {"key": "D", "text": "參"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第2課節錄）。正確答案「參」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=2),
  'true_false',
  '「容」是「南一版 3年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第2課節錄）。「容」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 3年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "婆"}, {"key": "B", "text": "相信"}, {"key": "C", "text": "滋"}, {"key": "D", "text": "玉"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第3課節錄）。正確答案「玉」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=3),
  'true_false',
  '「婆」是「南一版 3年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第3課節錄）。「婆」出自其他課，非「南一版 3年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 3年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "驚"}, {"key": "B", "text": "釐"}, {"key": "C", "text": "詞"}, {"key": "D", "text": "桐"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第4課節錄）。正確答案「驚」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=4),
  'true_false',
  '「有名」是「南一版 3年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第4課節錄）。「有名」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=5),
  'single_choice',
  '下列何者是「南一版 3年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "輕紗"}, {"key": "B", "text": "錢"}, {"key": "C", "text": "入口"}, {"key": "D", "text": "傻瓜"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第5課節錄）。正確答案「錢」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=5),
  'true_false',
  '「入口」是「南一版 3年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第5課節錄）。「入口」出自其他課，非「南一版 3年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=6),
  'single_choice',
  '下列何者是「南一版 3年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "洋"}, {"key": "B", "text": "好朋友"}, {"key": "C", "text": "洋娃娃"}, {"key": "D", "text": "松鼠"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第6課節錄）。正確答案「松鼠」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=6),
  'true_false',
  '「混亂」是「南一版 3年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第6課節錄）。「混亂」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=7),
  'single_choice',
  '下列何者是「南一版 3年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "保佑"}, {"key": "B", "text": "廳"}, {"key": "C", "text": "蹦蹦跳跳"}, {"key": "D", "text": "堂"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第7課節錄）。正確答案「堂」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=7),
  'true_false',
  '「廳」是「南一版 3年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第7課節錄）。「廳」出自其他課，非「南一版 3年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=8),
  'single_choice',
  '下列何者是「南一版 3年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "底"}, {"key": "B", "text": "木筏"}, {"key": "C", "text": "疑惑"}, {"key": "D", "text": "參"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第8課節錄）。正確答案「底」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=8),
  'true_false',
  '「叔」是「南一版 3年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第8課節錄）。「叔」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=9),
  'single_choice',
  '下列何者是「南一版 3年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "示"}, {"key": "B", "text": "蜘蛛"}, {"key": "C", "text": "皆"}, {"key": "D", "text": "靜"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第9課節錄）。正確答案「示」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=9),
  'true_false',
  '「蜘蛛」是「南一版 3年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第9課節錄）。「蜘蛛」出自其他課，非「南一版 3年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=10),
  'single_choice',
  '下列何者是「南一版 3年級下學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "學年"}, {"key": "B", "text": "顧慮"}, {"key": "C", "text": "世界"}, {"key": "D", "text": "岩石"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第10課節錄）。正確答案「岩石」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=10),
  'true_false',
  '「沖刷」是「南一版 3年級下學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第10課節錄）。「沖刷」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=11),
  'single_choice',
  '下列何者是「南一版 3年級下學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "什"}, {"key": "B", "text": "不僅"}, {"key": "C", "text": "微"}, {"key": "D", "text": "鴨"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第11課節錄）。正確答案「不僅」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=11),
  'true_false',
  '「微」是「南一版 3年級下學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第11課節錄）。「微」出自其他課，非「南一版 3年級下學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=12),
  'single_choice',
  '下列何者是「南一版 3年級下學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "貌"}, {"key": "B", "text": "反"}, {"key": "C", "text": "社"}, {"key": "D", "text": "耗盡"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第12課節錄）。正確答案「社」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=12),
  'true_false',
  '「商店」是「南一版 3年級下學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 國語科 第12課節錄）。「商店」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 3年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "美麗"}, {"key": "B", "text": "法"}, {"key": "C", "text": "某"}, {"key": "D", "text": "化"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第1課節錄）。正確答案「化」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=1),
  'true_false',
  '「美麗」是「南一版 3年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第1課節錄）。「美麗」出自其他課，非「南一版 3年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 3年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "走廊"}, {"key": "B", "text": "自"}, {"key": "C", "text": "癟"}, {"key": "D", "text": "第"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第2課節錄）。正確答案「走廊」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=2),
  'true_false',
  '「提」是「南一版 3年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第2課節錄）。「提」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 3年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "臉龐"}, {"key": "B", "text": "楊梅"}, {"key": "C", "text": "收穫"}, {"key": "D", "text": "無"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第3課節錄）。正確答案「無」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=3),
  'true_false',
  '「收穫」是「南一版 3年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第3課節錄）。「收穫」出自其他課，非「南一版 3年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 3年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "溫"}, {"key": "B", "text": "遷"}, {"key": "C", "text": "陰"}, {"key": "D", "text": "雖"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第4課節錄）。正確答案「溫」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=4),
  'true_false',
  '「夕陽」是「南一版 3年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第4課節錄）。「夕陽」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=5),
  'single_choice',
  '下列何者是「南一版 3年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "智慧"}, {"key": "B", "text": "恐龍"}, {"key": "C", "text": "曙光"}, {"key": "D", "text": "鈴"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第5課節錄）。正確答案「鈴」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=5),
  'true_false',
  '「智慧」是「南一版 3年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第5課節錄）。「智慧」出自其他課，非「南一版 3年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=6),
  'single_choice',
  '下列何者是「南一版 3年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "蟹"}, {"key": "B", "text": "耶"}, {"key": "C", "text": "瀏覽"}, {"key": "D", "text": "幕"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第6課節錄）。正確答案「幕」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=6),
  'true_false',
  '「杯」是「南一版 3年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第6課節錄）。「杯」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=7),
  'single_choice',
  '下列何者是「南一版 3年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "體"}, {"key": "B", "text": "藝"}, {"key": "C", "text": "些"}, {"key": "D", "text": "慈"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第7課節錄）。正確答案「藝」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=7),
  'true_false',
  '「些」是「南一版 3年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第7課節錄）。「些」出自其他課，非「南一版 3年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=8),
  'single_choice',
  '下列何者是「南一版 3年級上學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "山丘"}, {"key": "B", "text": "唷"}, {"key": "C", "text": "吹"}, {"key": "D", "text": "視"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第8課節錄）。正確答案「視」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=8),
  'true_false',
  '「框」是「南一版 3年級上學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第8課節錄）。「框」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=9),
  'single_choice',
  '下列何者是「南一版 3年級上學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "敲"}, {"key": "B", "text": "架"}, {"key": "C", "text": "此起彼落"}, {"key": "D", "text": "義"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第9課節錄）。正確答案「敲」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=9),
  'true_false',
  '「義」是「南一版 3年級上學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第9課節錄）。「義」出自其他課，非「南一版 3年級上學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=10),
  'single_choice',
  '下列何者是「南一版 3年級上學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "印象"}, {"key": "B", "text": "勒"}, {"key": "C", "text": "驚喜"}, {"key": "D", "text": "猾"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第10課節錄）。正確答案「印象」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=10),
  'true_false',
  '「呆頭呆腦」是「南一版 3年級上學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第10課節錄）。「呆頭呆腦」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=11),
  'single_choice',
  '下列何者是「南一版 3年級上學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鬆"}, {"key": "B", "text": "雞"}, {"key": "C", "text": "畫"}, {"key": "D", "text": "互"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第11課節錄）。正確答案「雞」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=11),
  'true_false',
  '「鬆」是「南一版 3年級上學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第11課節錄）。「鬆」出自其他課，非「南一版 3年級上學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=12),
  'single_choice',
  '下列何者是「南一版 3年級上學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "瑞士"}, {"key": "B", "text": "法"}, {"key": "C", "text": "退"}, {"key": "D", "text": "購"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第12課節錄）。正確答案「退」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=12),
  'true_false',
  '「放屁」是「南一版 3年級上學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 國語科 第12課節錄）。「放屁」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "漫"}, {"key": "B", "text": "虎鯨"}, {"key": "C", "text": "晨"}, {"key": "D", "text": "選"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第1課節錄）。正確答案「晨」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「選」是「康軒版 3年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第1課節錄）。「選」出自其他課，非「康軒版 3年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "溝"}, {"key": "B", "text": "身上"}, {"key": "C", "text": "路"}, {"key": "D", "text": "經過"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第2課節錄）。正確答案「溝」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「軟」是「康軒版 3年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第2課節錄）。「軟」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "剖"}, {"key": "B", "text": "靜"}, {"key": "C", "text": "區"}, {"key": "D", "text": "紅花"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第3課節錄）。正確答案「區」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「紅花」是「康軒版 3年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第3課節錄）。「紅花」出自其他課，非「康軒版 3年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鏡"}, {"key": "B", "text": "鍋"}, {"key": "C", "text": "齒"}, {"key": "D", "text": "疫情"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第4課節錄）。正確答案「齒」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「鋸」是「康軒版 3年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第4課節錄）。「鋸」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=5),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "爾"}, {"key": "B", "text": "銅板"}, {"key": "C", "text": "壓軸"}, {"key": "D", "text": "簽名"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第5課節錄）。正確答案「爾」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=5),
  'true_false',
  '「壓軸」是「康軒版 3年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第5課節錄）。「壓軸」出自其他課，非「康軒版 3年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=6),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "溼"}, {"key": "B", "text": "節省"}, {"key": "C", "text": "謝"}, {"key": "D", "text": "藥"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第6課節錄）。正確答案「節省」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=6),
  'true_false',
  '「周」是「康軒版 3年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第6課節錄）。「周」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=7),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "禮"}, {"key": "B", "text": "婆婆"}, {"key": "C", "text": "溝"}, {"key": "D", "text": "純粹"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第7課節錄）。正確答案「禮」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=7),
  'true_false',
  '「婆婆」是「康軒版 3年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第7課節錄）。「婆婆」出自其他課，非「康軒版 3年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=8),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "瀰"}, {"key": "B", "text": "每"}, {"key": "C", "text": "豆腐"}, {"key": "D", "text": "貨"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第8課節錄）。正確答案「豆腐」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=8),
  'true_false',
  '「雕塑」是「康軒版 3年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第8課節錄）。「雕塑」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=9),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "伐"}, {"key": "B", "text": "褐"}, {"key": "C", "text": "擠"}, {"key": "D", "text": "驚喜"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第9課節錄）。正確答案「伐」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=9),
  'true_false',
  '「驚喜」是「康軒版 3年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第9課節錄）。「驚喜」出自其他課，非「康軒版 3年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=10),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "陡峭"}, {"key": "B", "text": "表"}, {"key": "C", "text": "水藻"}, {"key": "D", "text": "棵"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第10課節錄）。正確答案「水藻」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=10),
  'true_false',
  '「夫婦」是「康軒版 3年級下學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第10課節錄）。「夫婦」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=11),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "逃"}, {"key": "B", "text": "扉"}, {"key": "C", "text": "瀑布"}, {"key": "D", "text": "慧"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第11課節錄）。正確答案「逃」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=11),
  'true_false',
  '「慧」是「康軒版 3年級下學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第11課節錄）。「慧」出自其他課，非「康軒版 3年級下學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=12),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "救"}, {"key": "B", "text": "凌"}, {"key": "C", "text": "羞"}, {"key": "D", "text": "寺"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第12課節錄）。正確答案「救」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=12),
  'true_false',
  '「毫無」是「康軒版 3年級下學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 國語科 第12課節錄）。「毫無」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "寺"}, {"key": "B", "text": "斜"}, {"key": "C", "text": "舟"}, {"key": "D", "text": "激動"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第1課節錄）。正確答案「舟」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「激動」是「康軒版 3年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第1課節錄）。「激動」出自其他課，非「康軒版 3年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "斤"}, {"key": "B", "text": "可愛"}, {"key": "C", "text": "喊"}, {"key": "D", "text": "泳"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第2課節錄）。正確答案「喊」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「名」是「康軒版 3年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第2課節錄）。「名」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "奧妙"}, {"key": "B", "text": "受"}, {"key": "C", "text": "機"}, {"key": "D", "text": "抬"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第3課節錄）。正確答案「機」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「抬」是「康軒版 3年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第3課節錄）。「抬」出自其他課，非「康軒版 3年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "統"}, {"key": "B", "text": "凌"}, {"key": "C", "text": "葵"}, {"key": "D", "text": "手腕"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第4課節錄）。正確答案「葵」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「擺」是「康軒版 3年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第4課節錄）。「擺」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=5),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "嚨"}, {"key": "B", "text": "禮"}, {"key": "C", "text": "鱗"}, {"key": "D", "text": "通"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第5課節錄）。正確答案「通」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=5),
  'true_false',
  '「嚨」是「康軒版 3年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第5課節錄）。「嚨」出自其他課，非「康軒版 3年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=6),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "婆"}, {"key": "B", "text": "必"}, {"key": "C", "text": "肚子"}, {"key": "D", "text": "淘"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第6課節錄）。正確答案「肚子」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=6),
  'true_false',
  '「黏人」是「康軒版 3年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第6課節錄）。「黏人」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=7),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "參加"}, {"key": "B", "text": "化"}, {"key": "C", "text": "錢"}, {"key": "D", "text": "憶"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第7課節錄）。正確答案「憶」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=7),
  'true_false',
  '「錢」是「康軒版 3年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第7課節錄）。「錢」出自其他課，非「康軒版 3年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=8),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "年級"}, {"key": "B", "text": "擇"}, {"key": "C", "text": "好像"}, {"key": "D", "text": "敗"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第8課節錄）。正確答案「敗」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=8),
  'true_false',
  '「守」是「康軒版 3年級上學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第8課節錄）。「守」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=9),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鹿"}, {"key": "B", "text": "遲"}, {"key": "C", "text": "幻"}, {"key": "D", "text": "智"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第9課節錄）。正確答案「智」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=9),
  'true_false',
  '「遲」是「康軒版 3年級上學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第9課節錄）。「遲」出自其他課，非「康軒版 3年級上學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=10),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "妙計"}, {"key": "B", "text": "願"}, {"key": "C", "text": "肚子"}, {"key": "D", "text": "到達"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第10課節錄）。正確答案「妙計」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=10),
  'true_false',
  '「強壯」是「康軒版 3年級上學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第10課節錄）。「強壯」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=11),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "飾"}, {"key": "B", "text": "茅屋"}, {"key": "C", "text": "隨"}, {"key": "D", "text": "棵"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第11課節錄）。正確答案「隨」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=11),
  'true_false',
  '「飾」是「康軒版 3年級上學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第11課節錄）。「飾」出自其他課，非「康軒版 3年級上學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=12),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "蛇"}, {"key": "B", "text": "昂"}, {"key": "C", "text": "學年"}, {"key": "D", "text": "嚨"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第12課節錄）。正確答案「蛇」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=12),
  'true_false',
  '「驚訝」是「康軒版 3年級上學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 國語科 第12課節錄）。「驚訝」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "不願"}, {"key": "B", "text": "遛達"}, {"key": "C", "text": "底"}, {"key": "D", "text": "惜"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第1課節錄）。正確答案「不願」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「底」是「翰林版 3年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第1課節錄）。「底」出自其他課，非「翰林版 3年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "從"}, {"key": "B", "text": "黑"}, {"key": "C", "text": "鍛鍊"}, {"key": "D", "text": "微笑"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第2課節錄）。正確答案「微笑」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「微」是「翰林版 3年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第2課節錄）。「微」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "酸"}, {"key": "B", "text": "髮"}, {"key": "C", "text": "休克"}, {"key": "D", "text": "啟"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第3課節錄）。正確答案「休克」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「髮」是「翰林版 3年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第3課節錄）。「髮」出自其他課，非「翰林版 3年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "凝"}, {"key": "B", "text": "混合"}, {"key": "C", "text": "漿"}, {"key": "D", "text": "尿尿"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第4課節錄）。正確答案「凝」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「廣大」是「翰林版 3年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第4課節錄）。「廣大」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=5),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "果"}, {"key": "B", "text": "愈"}, {"key": "C", "text": "師傅"}, {"key": "D", "text": "呆頭呆腦"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第5課節錄）。正確答案「師傅」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=5),
  'true_false',
  '「呆頭呆腦」是「翰林版 3年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第5課節錄）。「呆頭呆腦」出自其他課，非「翰林版 3年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=6),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "砂"}, {"key": "B", "text": "奮力"}, {"key": "C", "text": "山丘"}, {"key": "D", "text": "嘉賓"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第6課節錄）。正確答案「山丘」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=6),
  'true_false',
  '「象」是「翰林版 3年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第6課節錄）。「象」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=7),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "罐"}, {"key": "B", "text": "充"}, {"key": "C", "text": "學"}, {"key": "D", "text": "避免"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第7課節錄）。正確答案「罐」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=7),
  'true_false',
  '「避免」是「翰林版 3年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第7課節錄）。「避免」出自其他課，非「翰林版 3年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=8),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "潔白"}, {"key": "B", "text": "交談"}, {"key": "C", "text": "牛"}, {"key": "D", "text": "孤陋寡聞"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第8課節錄）。正確答案「交談」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=8),
  'true_false',
  '「展現」是「翰林版 3年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第8課節錄）。「展現」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=9),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "圾"}, {"key": "B", "text": "水珠"}, {"key": "C", "text": "奶"}, {"key": "D", "text": "傍晚"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第9課節錄）。正確答案「圾」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=9),
  'true_false',
  '「水珠」是「翰林版 3年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第9課節錄）。「水珠」出自其他課，非「翰林版 3年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=10),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "大胃王"}, {"key": "B", "text": "姓"}, {"key": "C", "text": "鹿"}, {"key": "D", "text": "揭示"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第10課節錄）。正確答案「大胃王」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=10),
  'true_false',
  '「大拇指」是「翰林版 3年級下學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第10課節錄）。「大拇指」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=11),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "蓮霧"}, {"key": "B", "text": "糞"}, {"key": "C", "text": "症"}, {"key": "D", "text": "好吃"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第11課節錄）。正確答案「糞」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=11),
  'true_false',
  '「好吃」是「翰林版 3年級下學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第11課節錄）。「好吃」出自其他課，非「翰林版 3年級下學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=12),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "促"}, {"key": "B", "text": "如意"}, {"key": "C", "text": "卓越"}, {"key": "D", "text": "老鼠"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第12課節錄）。正確答案「老鼠」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=12),
  'true_false',
  '「賽」是「翰林版 3年級下學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 國語科 第12課節錄）。「賽」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 3年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "牠"}, {"key": "B", "text": "豆腐"}, {"key": "C", "text": "惡"}, {"key": "D", "text": "摯"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第1課節錄）。正確答案「牠」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「豆腐」是「翰林版 3年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第1課節錄）。「豆腐」出自其他課，非「翰林版 3年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 3年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "爛"}, {"key": "B", "text": "郁"}, {"key": "C", "text": "兄"}, {"key": "D", "text": "凌"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第2課節錄）。正確答案「爛」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「鬆」是「翰林版 3年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第2課節錄）。「鬆」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 3年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "屢"}, {"key": "B", "text": "因為"}, {"key": "C", "text": "磚"}, {"key": "D", "text": "清楚"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第3課節錄）。正確答案「因為」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「磚」是「翰林版 3年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第3課節錄）。「磚」出自其他課，非「翰林版 3年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 3年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "北極"}, {"key": "B", "text": "錢"}, {"key": "C", "text": "龍"}, {"key": "D", "text": "嘩"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第4課節錄）。正確答案「錢」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「飼」是「翰林版 3年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第4課節錄）。「飼」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=5),
  'single_choice',
  '下列何者是「翰林版 3年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "且"}, {"key": "B", "text": "德性"}, {"key": "C", "text": "蹦"}, {"key": "D", "text": "跪"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第5課節錄）。正確答案「且」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=5),
  'true_false',
  '「跪」是「翰林版 3年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第5課節錄）。「跪」出自其他課，非「翰林版 3年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=6),
  'single_choice',
  '下列何者是「翰林版 3年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "香蕉"}, {"key": "B", "text": "膠水"}, {"key": "C", "text": "直笛"}, {"key": "D", "text": "築"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第6課節錄）。正確答案「膠水」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=6),
  'true_false',
  '「解」是「翰林版 3年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第6課節錄）。「解」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=7),
  'single_choice',
  '下列何者是「翰林版 3年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "川"}, {"key": "B", "text": "苗"}, {"key": "C", "text": "坡"}, {"key": "D", "text": "不偏不倚"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第7課節錄）。正確答案「坡」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=7),
  'true_false',
  '「川」是「翰林版 3年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第7課節錄）。「川」出自其他課，非「翰林版 3年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=8),
  'single_choice',
  '下列何者是「翰林版 3年級上學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "挽"}, {"key": "B", "text": "灘"}, {"key": "C", "text": "反"}, {"key": "D", "text": "減"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第8課節錄）。正確答案「灘」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=8),
  'true_false',
  '「應該」是「翰林版 3年級上學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第8課節錄）。「應該」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=9),
  'single_choice',
  '下列何者是「翰林版 3年級上學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "捲"}, {"key": "B", "text": "奮力"}, {"key": "C", "text": "攀登"}, {"key": "D", "text": "練習"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第9課節錄）。正確答案「捲」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=9),
  'true_false',
  '「攀登」是「翰林版 3年級上學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第9課節錄）。「攀登」出自其他課，非「翰林版 3年級上學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=10),
  'single_choice',
  '下列何者是「翰林版 3年級上學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "遲"}, {"key": "B", "text": "好像"}, {"key": "C", "text": "培養"}, {"key": "D", "text": "束"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第10課節錄）。正確答案「束」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=10),
  'true_false',
  '「飾」是「翰林版 3年級上學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第10課節錄）。「飾」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=11),
  'single_choice',
  '下列何者是「翰林版 3年級上學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "這些"}, {"key": "B", "text": "乎"}, {"key": "C", "text": "傅"}, {"key": "D", "text": "由衷"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第11課節錄）。正確答案「傅」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=11),
  'true_false',
  '「乎」是「翰林版 3年級上學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第11課節錄）。「乎」出自其他課，非「翰林版 3年級上學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=12),
  'single_choice',
  '下列何者是「翰林版 3年級上學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "旨"}, {"key": "B", "text": "仔"}, {"key": "C", "text": "健"}, {"key": "D", "text": "客廳"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第12課節錄）。正確答案「客廳」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=12),
  'true_false',
  '「廳」是「翰林版 3年級上學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 國語科 第12課節錄）。「廳」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 4年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "構築"}, {"key": "B", "text": "優美"}, {"key": "C", "text": "曹操"}, {"key": "D", "text": "飛梭"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第2課節錄）。正確答案「優美」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=2),
  'true_false',
  '「音效」是「南一版 4年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第2課節錄）。「音效」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 4年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "甩"}, {"key": "B", "text": "轉身"}, {"key": "C", "text": "兩"}, {"key": "D", "text": "過敏"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第3課節錄）。正確答案「甩」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=3),
  'true_false',
  '「過敏」是「南一版 4年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第3課節錄）。「過敏」出自其他課，非「南一版 4年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 4年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "翩翩"}, {"key": "B", "text": "翹"}, {"key": "C", "text": "吊"}, {"key": "D", "text": "介紹"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第4課節錄）。正確答案「翩翩」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=4),
  'true_false',
  '「晾乾」是「南一版 4年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第4課節錄）。「晾乾」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=5),
  'single_choice',
  '下列何者是「南一版 4年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "激動"}, {"key": "B", "text": "全家"}, {"key": "C", "text": "鄉"}, {"key": "D", "text": "岩石"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第5課節錄）。正確答案「激動」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=5),
  'true_false',
  '「全家」是「南一版 4年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第5課節錄）。「全家」出自其他課，非「南一版 4年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=6),
  'single_choice',
  '下列何者是「南一版 4年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "郁"}, {"key": "B", "text": "耕"}, {"key": "C", "text": "通"}, {"key": "D", "text": "楊梅"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第6課節錄）。正確答案「通」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=6),
  'true_false',
  '「裂」是「南一版 4年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第6課節錄）。「裂」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=7),
  'single_choice',
  '下列何者是「南一版 4年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "雅"}, {"key": "B", "text": "愈"}, {"key": "C", "text": "嘆"}, {"key": "D", "text": "金魚"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第7課節錄）。正確答案「雅」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=7),
  'true_false',
  '「愈」是「南一版 4年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第7課節錄）。「愈」出自其他課，非「南一版 4年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=8),
  'single_choice',
  '下列何者是「南一版 4年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "淨"}, {"key": "B", "text": "必"}, {"key": "C", "text": "搏"}, {"key": "D", "text": "太"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第8課節錄）。正確答案「必」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=8),
  'true_false',
  '「瑩」是「南一版 4年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第8課節錄）。「瑩」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=9),
  'single_choice',
  '下列何者是「南一版 4年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "喘"}, {"key": "B", "text": "汙染"}, {"key": "C", "text": "複"}, {"key": "D", "text": "建築"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第9課節錄）。正確答案「喘」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=9),
  'true_false',
  '「建築」是「南一版 4年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第9課節錄）。「建築」出自其他課，非「南一版 4年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=10),
  'single_choice',
  '下列何者是「南一版 4年級下學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "捨"}, {"key": "B", "text": "客廳"}, {"key": "C", "text": "摘花"}, {"key": "D", "text": "計算機"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第10課節錄）。正確答案「計算機」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=10),
  'true_false',
  '「慧」是「南一版 4年級下學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第10課節錄）。「慧」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=11),
  'single_choice',
  '下列何者是「南一版 4年級下學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "承"}, {"key": "B", "text": "改"}, {"key": "C", "text": "礦"}, {"key": "D", "text": "看"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第11課節錄）。正確答案「改」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=11),
  'true_false',
  '「承」是「南一版 4年級下學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第11課節錄）。「承」出自其他課，非「南一版 4年級下學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=12),
  'single_choice',
  '下列何者是「南一版 4年級下學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "詳"}, {"key": "B", "text": "建築"}, {"key": "C", "text": "髮"}, {"key": "D", "text": "極"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第12課節錄）。正確答案「詳」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=12),
  'true_false',
  '「安詳」是「南一版 4年級下學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 國語科 第12課節錄）。「安詳」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 4年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "顯"}, {"key": "B", "text": "夫"}, {"key": "C", "text": "留"}, {"key": "D", "text": "漫"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第1課節錄）。正確答案「漫」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=1),
  'true_false',
  '「留」是「南一版 4年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第1課節錄）。「留」出自其他課，非「南一版 4年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 4年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "凋"}, {"key": "B", "text": "混合"}, {"key": "C", "text": "汽"}, {"key": "D", "text": "小丑魚"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第2課節錄）。正確答案「汽」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=2),
  'true_false',
  '「彷彿」是「南一版 4年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第2課節錄）。「彷彿」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 4年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "似"}, {"key": "B", "text": "臉"}, {"key": "C", "text": "確"}, {"key": "D", "text": "獲"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第3課節錄）。正確答案「獲」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=3),
  'true_false',
  '「確」是「南一版 4年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第3課節錄）。「確」出自其他課，非「南一版 4年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 4年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "基金會"}, {"key": "B", "text": "聆"}, {"key": "C", "text": "綺麗"}, {"key": "D", "text": "聆聽"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第4課節錄）。正確答案「聆」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=4),
  'true_false',
  '「翻」是「南一版 4年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第4課節錄）。「翻」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=5),
  'single_choice',
  '下列何者是「南一版 4年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "上桌"}, {"key": "B", "text": "挑戰"}, {"key": "C", "text": "恬"}, {"key": "D", "text": "盞"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第5課節錄）。正確答案「挑戰」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=5),
  'true_false',
  '「上桌」是「南一版 4年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第5課節錄）。「上桌」出自其他課，非「南一版 4年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=6),
  'single_choice',
  '下列何者是「南一版 4年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "吹奏"}, {"key": "B", "text": "護"}, {"key": "C", "text": "糖水"}, {"key": "D", "text": "脈"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第6課節錄）。正確答案「護」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=6),
  'true_false',
  '「鋼」是「南一版 4年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第6課節錄）。「鋼」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=7),
  'single_choice',
  '下列何者是「南一版 4年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "視"}, {"key": "B", "text": "樸實"}, {"key": "C", "text": "溫"}, {"key": "D", "text": "值"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第7課節錄）。正確答案「值」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=7),
  'true_false',
  '「溫」是「南一版 4年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第7課節錄）。「溫」出自其他課，非「南一版 4年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=8),
  'single_choice',
  '下列何者是「南一版 4年級上學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "玉"}, {"key": "B", "text": "桿"}, {"key": "C", "text": "守"}, {"key": "D", "text": "踮"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第8課節錄）。正確答案「踮」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=8),
  'true_false',
  '「辮子」是「南一版 4年級上學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第8課節錄）。「辮子」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=9),
  'single_choice',
  '下列何者是「南一版 4年級上學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "敵"}, {"key": "B", "text": "步"}, {"key": "C", "text": "自"}, {"key": "D", "text": "褐"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第9課節錄）。正確答案「褐」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=9),
  'true_false',
  '「步」是「南一版 4年級上學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第9課節錄）。「步」出自其他課，非「南一版 4年級上學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=10),
  'single_choice',
  '下列何者是「南一版 4年級上學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鄰"}, {"key": "B", "text": "花轎"}, {"key": "C", "text": "金魚"}, {"key": "D", "text": "亦"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第10課節錄）。正確答案「花轎」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=10),
  'true_false',
  '「隊伍」是「南一版 4年級上學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第10課節錄）。「隊伍」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=11),
  'single_choice',
  '下列何者是「南一版 4年級上學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "避"}, {"key": "B", "text": "老闆"}, {"key": "C", "text": "複"}, {"key": "D", "text": "拚"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第11課節錄）。正確答案「拚」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=11),
  'true_false',
  '「複」是「南一版 4年級上學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第11課節錄）。「複」出自其他課，非「南一版 4年級上學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=12),
  'single_choice',
  '下列何者是「南一版 4年級上學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "漸"}, {"key": "B", "text": "陰森森"}, {"key": "C", "text": "裡"}, {"key": "D", "text": "試"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第12課節錄）。正確答案「漸」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=12),
  'true_false',
  '「漸漸」是「南一版 4年級上學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 國語科 第12課節錄）。「漸漸」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "環"}, {"key": "B", "text": "鹿"}, {"key": "C", "text": "心馳神往"}, {"key": "D", "text": "身上"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第1課節錄）。正確答案「環」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「身上」是「康軒版 4年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第1課節錄）。「身上」出自其他課，非「康軒版 4年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "倘若"}, {"key": "B", "text": "缺"}, {"key": "C", "text": "閱讀"}, {"key": "D", "text": "加"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第2課節錄）。正確答案「缺」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「絆腳石」是「康軒版 4年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第2課節錄）。「絆腳石」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "島嶼"}, {"key": "B", "text": "滲入"}, {"key": "C", "text": "熊"}, {"key": "D", "text": "勤"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第3課節錄）。正確答案「勤」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「熊」是「康軒版 4年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第3課節錄）。「熊」出自其他課，非「康軒版 4年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "傅"}, {"key": "B", "text": "注意"}, {"key": "C", "text": "粽"}, {"key": "D", "text": "避"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第4課節錄）。正確答案「粽」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「推」是「康軒版 4年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第4課節錄）。「推」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=5),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "麼"}, {"key": "B", "text": "突然"}, {"key": "C", "text": "封面"}, {"key": "D", "text": "爺"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第5課節錄）。正確答案「封面」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=5),
  'true_false',
  '「突然」是「康軒版 4年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第5課節錄）。「突然」出自其他課，非「康軒版 4年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=6),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "毋"}, {"key": "B", "text": "摯"}, {"key": "C", "text": "親朋好友"}, {"key": "D", "text": "插"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第6課節錄）。正確答案「插」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=6),
  'true_false',
  '「拌」是「康軒版 4年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第6課節錄）。「拌」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=7),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "改"}, {"key": "B", "text": "熟"}, {"key": "C", "text": "師"}, {"key": "D", "text": "惡"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第7課節錄）。正確答案「惡」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=7),
  'true_false',
  '「師」是「康軒版 4年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第7課節錄）。「師」出自其他課，非「康軒版 4年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=8),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "逞"}, {"key": "B", "text": "鳴"}, {"key": "C", "text": "獨"}, {"key": "D", "text": "迴盪"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第8課節錄）。正確答案「獨」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=8),
  'true_false',
  '「厚」是「康軒版 4年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第8課節錄）。「厚」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=9),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "齊天大聖"}, {"key": "B", "text": "試"}, {"key": "C", "text": "塘"}, {"key": "D", "text": "布告欄"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第9課節錄）。正確答案「試」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=9),
  'true_false',
  '「布告欄」是「康軒版 4年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第9課節錄）。「布告欄」出自其他課，非「康軒版 4年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=10),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "橡皮擦"}, {"key": "B", "text": "耗盡"}, {"key": "C", "text": "橡"}, {"key": "D", "text": "潔"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第10課節錄）。正確答案「耗盡」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=10),
  'true_false',
  '「豪」是「康軒版 4年級下學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第10課節錄）。「豪」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=11),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "直笛"}, {"key": "B", "text": "淚"}, {"key": "C", "text": "魯班"}, {"key": "D", "text": "陰"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第11課節錄）。正確答案「淚」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=11),
  'true_false',
  '「直笛」是「康軒版 4年級下學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第11課節錄）。「直笛」出自其他課，非「康軒版 4年級下學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=12),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "自從"}, {"key": "B", "text": "豐富"}, {"key": "C", "text": "剛"}, {"key": "D", "text": "聖"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第12課節錄）。正確答案「聖」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=12),
  'true_false',
  '「壓住」是「康軒版 4年級下學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 國語科 第12課節錄）。「壓住」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "節"}, {"key": "B", "text": "鏡頭"}, {"key": "C", "text": "串"}, {"key": "D", "text": "隨"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第1課節錄）。正確答案「串」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「隨」是「康軒版 4年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第1課節錄）。「隨」出自其他課，非「康軒版 4年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "時候"}, {"key": "B", "text": "子"}, {"key": "C", "text": "警"}, {"key": "D", "text": "蒸"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第2課節錄）。正確答案「警」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「偷」是「康軒版 4年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第2課節錄）。「偷」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鞍"}, {"key": "B", "text": "喧"}, {"key": "C", "text": "苔"}, {"key": "D", "text": "黍"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第3課節錄）。正確答案「喧」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「黍」是「康軒版 4年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第3課節錄）。「黍」出自其他課，非「康軒版 4年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "青草"}, {"key": "B", "text": "濃"}, {"key": "C", "text": "微微"}, {"key": "D", "text": "奶"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第4課節錄）。正確答案「濃」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「馬偕」是「康軒版 4年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第4課節錄）。「馬偕」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=5),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "留"}, {"key": "B", "text": "求助"}, {"key": "C", "text": "瀰"}, {"key": "D", "text": "注意"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第5課節錄）。正確答案「注意」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=5),
  'true_false',
  '「求助」是「康軒版 4年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第5課節錄）。「求助」出自其他課，非「康軒版 4年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=6),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "均"}, {"key": "B", "text": "放屁"}, {"key": "C", "text": "亦"}, {"key": "D", "text": "谷底"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第6課節錄）。正確答案「谷底」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=6),
  'true_false',
  '「攀登」是「康軒版 4年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第6課節錄）。「攀登」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=7),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "員"}, {"key": "B", "text": "郁"}, {"key": "C", "text": "昭和草"}, {"key": "D", "text": "笑納"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第7課節錄）。正確答案「郁」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=7),
  'true_false',
  '「笑納」是「康軒版 4年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第7課節錄）。「笑納」出自其他課，非「康軒版 4年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=8),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "卓越"}, {"key": "B", "text": "研"}, {"key": "C", "text": "經濟"}, {"key": "D", "text": "推"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第8課節錄）。正確答案「經濟」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=8),
  'true_false',
  '「臨」是「康軒版 4年級上學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第8課節錄）。「臨」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=9),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "請"}, {"key": "B", "text": "棧"}, {"key": "C", "text": "鬱"}, {"key": "D", "text": "鄰"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第9課節錄）。正確答案「鬱」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=9),
  'true_false',
  '「請」是「康軒版 4年級上學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第9課節錄）。「請」出自其他課，非「康軒版 4年級上學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=10),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鋼"}, {"key": "B", "text": "建築"}, {"key": "C", "text": "臉龐"}, {"key": "D", "text": "欣賞"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第10課節錄）。正確答案「臉龐」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=10),
  'true_false',
  '「榮華富貴」是「康軒版 4年級上學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第10課節錄）。「榮華富貴」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=11),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "到"}, {"key": "B", "text": "書籤"}, {"key": "C", "text": "遲"}, {"key": "D", "text": "鹿"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第11課節錄）。正確答案「遲」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=11),
  'true_false',
  '「書籤」是「康軒版 4年級上學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第11課節錄）。「書籤」出自其他課，非「康軒版 4年級上學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=12),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "儲存"}, {"key": "B", "text": "就是"}, {"key": "C", "text": "蹦"}, {"key": "D", "text": "抓住"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第12課節錄）。正確答案「蹦」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=12),
  'true_false',
  '「內心」是「康軒版 4年級上學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 國語科 第12課節錄）。「內心」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "音"}, {"key": "B", "text": "雄"}, {"key": "C", "text": "爾"}, {"key": "D", "text": "暖"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第1課節錄）。正確答案「雄」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「音」是「翰林版 4年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第1課節錄）。「音」出自其他課，非「翰林版 4年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "製作"}, {"key": "B", "text": "碳"}, {"key": "C", "text": "瘦弱"}, {"key": "D", "text": "激動"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第2課節錄）。正確答案「碳」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「建築」是「翰林版 4年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第2課節錄）。「建築」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "教"}, {"key": "B", "text": "閱讀"}, {"key": "C", "text": "敏"}, {"key": "D", "text": "次"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第3課節錄）。正確答案「敏」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「閱讀」是「翰林版 4年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第3課節錄）。「閱讀」出自其他課，非「翰林版 4年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "懂"}, {"key": "B", "text": "共"}, {"key": "C", "text": "稻穗"}, {"key": "D", "text": "也"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第4課節錄）。正確答案「共」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「餘」是「翰林版 4年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第4課節錄）。「餘」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=5),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "閒"}, {"key": "B", "text": "自從"}, {"key": "C", "text": "旗"}, {"key": "D", "text": "朝"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第5課節錄）。正確答案「旗」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=5),
  'true_false',
  '「閒」是「翰林版 4年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第5課節錄）。「閒」出自其他課，非「翰林版 4年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=6),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "遍"}, {"key": "B", "text": "飾"}, {"key": "C", "text": "巡視"}, {"key": "D", "text": "拚"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第6課節錄）。正確答案「遍」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=6),
  'true_false',
  '「潔」是「翰林版 4年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第6課節錄）。「潔」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=7),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "經過"}, {"key": "B", "text": "由"}, {"key": "C", "text": "壘"}, {"key": "D", "text": "路"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第7課節錄）。正確答案「壘」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=7),
  'true_false',
  '「路」是「翰林版 4年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第7課節錄）。「路」出自其他課，非「翰林版 4年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=8),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "村"}, {"key": "B", "text": "愈"}, {"key": "C", "text": "那"}, {"key": "D", "text": "象"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第8課節錄）。正確答案「愈」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=8),
  'true_false',
  '「領」是「翰林版 4年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第8課節錄）。「領」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=9),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "靜謐"}, {"key": "B", "text": "隻"}, {"key": "C", "text": "霧"}, {"key": "D", "text": "縫"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第9課節錄）。正確答案「霧」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=9),
  'true_false',
  '「靜謐」是「翰林版 4年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第9課節錄）。「靜謐」出自其他課，非「翰林版 4年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=10),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "椅子"}, {"key": "B", "text": "詠"}, {"key": "C", "text": "斯"}, {"key": "D", "text": "打"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第10課節錄）。正確答案「椅子」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=10),
  'true_false',
  '「芭」是「翰林版 4年級下學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第10課節錄）。「芭」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=11),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "賺"}, {"key": "B", "text": "雞"}, {"key": "C", "text": "的"}, {"key": "D", "text": "臺灣"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第11課節錄）。正確答案「賺」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=11),
  'true_false',
  '「臺灣」是「翰林版 4年級下學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第11課節錄）。「臺灣」出自其他課，非「翰林版 4年級下學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=12),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "布告欄"}, {"key": "B", "text": "冷絲絲"}, {"key": "C", "text": "磚"}, {"key": "D", "text": "喊"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第12課節錄）。正確答案「布告欄」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=12),
  'true_false',
  '「鐘聲」是「翰林版 4年級下學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 國語科 第12課節錄）。「鐘聲」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 4年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "橇"}, {"key": "B", "text": "濟"}, {"key": "C", "text": "甜蜜"}, {"key": "D", "text": "高"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第1課節錄）。正確答案「甜蜜」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「高」是「翰林版 4年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第1課節錄）。「高」出自其他課，非「翰林版 4年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 4年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "變幻莫測"}, {"key": "B", "text": "夜夜"}, {"key": "C", "text": "島"}, {"key": "D", "text": "彷彿"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第2課節錄）。正確答案「彷彿」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「陀」是「翰林版 4年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第2課節錄）。「陀」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 4年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "肯定"}, {"key": "B", "text": "蔬"}, {"key": "C", "text": "致"}, {"key": "D", "text": "軟"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第3課節錄）。正確答案「蔬」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「軟」是「翰林版 4年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第3課節錄）。「軟」出自其他課，非「翰林版 4年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 4年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "碑"}, {"key": "B", "text": "浪潮"}, {"key": "C", "text": "發酵"}, {"key": "D", "text": "幸"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第4課節錄）。正確答案「碑」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「兄弟」是「翰林版 4年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第4課節錄）。「兄弟」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=5),
  'single_choice',
  '下列何者是「翰林版 4年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "銷售"}, {"key": "B", "text": "一塊"}, {"key": "C", "text": "輪"}, {"key": "D", "text": "到底"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第5課節錄）。正確答案「輪」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=5),
  'true_false',
  '「銷售」是「翰林版 4年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第5課節錄）。「銷售」出自其他課，非「翰林版 4年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=6),
  'single_choice',
  '下列何者是「翰林版 4年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "平均"}, {"key": "B", "text": "熄滅"}, {"key": "C", "text": "邇"}, {"key": "D", "text": "通"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第6課節錄）。正確答案「平均」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=6),
  'true_false',
  '「月餅」是「翰林版 4年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第6課節錄）。「月餅」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=7),
  'single_choice',
  '下列何者是「翰林版 4年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "橡皮擦"}, {"key": "B", "text": "禁"}, {"key": "C", "text": "彩虹"}, {"key": "D", "text": "這些"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第7課節錄）。正確答案「禁」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=7),
  'true_false',
  '「這些」是「翰林版 4年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第7課節錄）。「這些」出自其他課，非「翰林版 4年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=8),
  'single_choice',
  '下列何者是「翰林版 4年級上學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "猾"}, {"key": "B", "text": "江"}, {"key": "C", "text": "一個"}, {"key": "D", "text": "縱"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第8課節錄）。正確答案「江」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=8),
  'true_false',
  '「根本」是「翰林版 4年級上學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第8課節錄）。「根本」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=9),
  'single_choice',
  '下列何者是「翰林版 4年級上學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "熬煮"}, {"key": "B", "text": "惡"}, {"key": "C", "text": "刃"}, {"key": "D", "text": "廓"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第9課節錄）。正確答案「惡」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=9),
  'true_false',
  '「熬煮」是「翰林版 4年級上學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第9課節錄）。「熬煮」出自其他課，非「翰林版 4年級上學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=10),
  'single_choice',
  '下列何者是「翰林版 4年級上學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "天籟"}, {"key": "B", "text": "福"}, {"key": "C", "text": "海藻"}, {"key": "D", "text": "覺"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第10課節錄）。正確答案「海藻」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=10),
  'true_false',
  '「汙染」是「翰林版 4年級上學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第10課節錄）。「汙染」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=11),
  'single_choice',
  '下列何者是「翰林版 4年級上學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "浪潮"}, {"key": "B", "text": "輕快"}, {"key": "C", "text": "掠"}, {"key": "D", "text": "煞車"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第11課節錄）。正確答案「浪潮」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=11),
  'true_false',
  '「掠」是「翰林版 4年級上學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第11課節錄）。「掠」出自其他課，非「翰林版 4年級上學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=12),
  'single_choice',
  '下列何者是「翰林版 4年級上學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "織"}, {"key": "B", "text": "籟"}, {"key": "C", "text": "水藻"}, {"key": "D", "text": "頤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第12課節錄）。正確答案「籟」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=12),
  'true_false',
  '「天籟」是「翰林版 4年級上學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 國語科 第12課節錄）。「天籟」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 5年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "盞"}, {"key": "B", "text": "米線"}, {"key": "C", "text": "絲"}, {"key": "D", "text": "嘩"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第1課節錄）。正確答案「盞」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=1),
  'true_false',
  '「嘩」是「南一版 5年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第1課節錄）。「嘩」出自其他課，非「南一版 5年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 5年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "億"}, {"key": "B", "text": "鑽"}, {"key": "C", "text": "徐"}, {"key": "D", "text": "盞"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第2課節錄）。正確答案「鑽」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=2),
  'true_false',
  '「轟」是「南一版 5年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第2課節錄）。「轟」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 5年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "兄"}, {"key": "B", "text": "俠"}, {"key": "C", "text": "到"}, {"key": "D", "text": "蓮霧"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第3課節錄）。正確答案「蓮霧」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=3),
  'true_false',
  '「俠」是「南一版 5年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第3課節錄）。「俠」出自其他課，非「南一版 5年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 5年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "批評"}, {"key": "B", "text": "餘"}, {"key": "C", "text": "沾"}, {"key": "D", "text": "一模一樣"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第4課節錄）。正確答案「沾」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=4),
  'true_false',
  '「貪」是「南一版 5年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第4課節錄）。「貪」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=5),
  'single_choice',
  '下列何者是「南一版 5年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鏡"}, {"key": "B", "text": "逞"}, {"key": "C", "text": "繩"}, {"key": "D", "text": "竄"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第5課節錄）。正確答案「逞」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=5),
  'true_false',
  '「繩」是「南一版 5年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第5課節錄）。「繩」出自其他課，非「南一版 5年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=6),
  'single_choice',
  '下列何者是「南一版 5年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "避免"}, {"key": "B", "text": "橙色"}, {"key": "C", "text": "刃"}, {"key": "D", "text": "鄰居"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第6課節錄）。正確答案「刃」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=6),
  'true_false',
  '「姨」是「南一版 5年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第6課節錄）。「姨」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=7),
  'single_choice',
  '下列何者是「南一版 5年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "老"}, {"key": "B", "text": "拘"}, {"key": "C", "text": "任"}, {"key": "D", "text": "一模一樣"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第7課節錄）。正確答案「任」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=7),
  'true_false',
  '「拘」是「南一版 5年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第7課節錄）。「拘」出自其他課，非「南一版 5年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=8),
  'single_choice',
  '下列何者是「南一版 5年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "癟"}, {"key": "B", "text": "汽"}, {"key": "C", "text": "一起"}, {"key": "D", "text": "您"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第8課節錄）。正確答案「癟」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=8),
  'true_false',
  '「嚼」是「南一版 5年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第8課節錄）。「嚼」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=9),
  'single_choice',
  '下列何者是「南一版 5年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "智"}, {"key": "B", "text": "症"}, {"key": "C", "text": "按時"}, {"key": "D", "text": "盡力"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第9課節錄）。正確答案「症」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=9),
  'true_false',
  '「智」是「南一版 5年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第9課節錄）。「智」出自其他課，非「南一版 5年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=10),
  'single_choice',
  '下列何者是「南一版 5年級下學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "直笛"}, {"key": "B", "text": "渺小"}, {"key": "C", "text": "珊"}, {"key": "D", "text": "名列前茅"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第10課節錄）。正確答案「渺小」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=10),
  'true_false',
  '「絮」是「南一版 5年級下學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第10課節錄）。「絮」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=11),
  'single_choice',
  '下列何者是「南一版 5年級下學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "季"}, {"key": "B", "text": "研"}, {"key": "C", "text": "霧"}, {"key": "D", "text": "踮"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第11課節錄）。正確答案「研」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=11),
  'true_false',
  '「季」是「南一版 5年級下學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第11課節錄）。「季」出自其他課，非「南一版 5年級下學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=12),
  'single_choice',
  '下列何者是「南一版 5年級下學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "稻穗"}, {"key": "B", "text": "根據"}, {"key": "C", "text": "暖"}, {"key": "D", "text": "冷絲絲"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第12課節錄）。正確答案「根據」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=12),
  'true_false',
  '「鳥瞰」是「南一版 5年級下學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 國語科 第12課節錄）。「鳥瞰」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 5年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "大胃王"}, {"key": "B", "text": "吁"}, {"key": "C", "text": "下午"}, {"key": "D", "text": "某"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第1課節錄）。正確答案「某」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=1),
  'true_false',
  '「吁」是「南一版 5年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第1課節錄）。「吁」出自其他課，非「南一版 5年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 5年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "磚"}, {"key": "B", "text": "延長線"}, {"key": "C", "text": "月"}, {"key": "D", "text": "扁"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第2課節錄）。正確答案「延長線」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=2),
  'true_false',
  '「平穩」是「南一版 5年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第2課節錄）。「平穩」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 5年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "夜夜"}, {"key": "B", "text": "橡皮擦"}, {"key": "C", "text": "斜"}, {"key": "D", "text": "醜"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第3課節錄）。正確答案「橡皮擦」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=3),
  'true_false',
  '「斜」是「南一版 5年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第3課節錄）。「斜」出自其他課，非「南一版 5年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 5年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "研究"}, {"key": "B", "text": "洋"}, {"key": "C", "text": "乳白色"}, {"key": "D", "text": "模樣"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第4課節錄）。正確答案「乳白色」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=4),
  'true_false',
  '「渲染」是「南一版 5年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第4課節錄）。「渲染」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=5),
  'single_choice',
  '下列何者是「南一版 5年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鋼"}, {"key": "B", "text": "斧"}, {"key": "C", "text": "可愛"}, {"key": "D", "text": "汗"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第5課節錄）。正確答案「斧」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=5),
  'true_false',
  '「鋼」是「南一版 5年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第5課節錄）。「鋼」出自其他課，非「南一版 5年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=6),
  'single_choice',
  '下列何者是「南一版 5年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "繁殖"}, {"key": "B", "text": "奧妙"}, {"key": "C", "text": "岩漿"}, {"key": "D", "text": "但是"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第6課節錄）。正確答案「繁殖」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=6),
  'true_false',
  '「緩」是「南一版 5年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第6課節錄）。「緩」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=7),
  'single_choice',
  '下列何者是「南一版 5年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "伏"}, {"key": "B", "text": "解"}, {"key": "C", "text": "鷹"}, {"key": "D", "text": "鱗"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第7課節錄）。正確答案「鱗」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=7),
  'true_false',
  '「伏」是「南一版 5年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第7課節錄）。「伏」出自其他課，非「南一版 5年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=8),
  'single_choice',
  '下列何者是「南一版 5年級上學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "挑戰"}, {"key": "B", "text": "平穩"}, {"key": "C", "text": "輕而易舉"}, {"key": "D", "text": "鄉"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第8課節錄）。正確答案「鄉」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=8),
  'true_false',
  '「蓋子」是「南一版 5年級上學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第8課節錄）。「蓋子」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=9),
  'single_choice',
  '下列何者是「南一版 5年級上學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "獨"}, {"key": "B", "text": "棋"}, {"key": "C", "text": "啄"}, {"key": "D", "text": "賺"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第9課節錄）。正確答案「賺」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=9),
  'true_false',
  '「棋」是「南一版 5年級上學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第9課節錄）。「棋」出自其他課，非「南一版 5年級上學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=10),
  'single_choice',
  '下列何者是「南一版 5年級上學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "扭"}, {"key": "B", "text": "我"}, {"key": "C", "text": "爾"}, {"key": "D", "text": "費"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第10課節錄）。正確答案「扭」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=10),
  'true_false',
  '「誼」是「南一版 5年級上學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第10課節錄）。「誼」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=11),
  'single_choice',
  '下列何者是「南一版 5年級上學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "底"}, {"key": "B", "text": "滋味"}, {"key": "C", "text": "恍"}, {"key": "D", "text": "包括"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第11課節錄）。正確答案「恍」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=11),
  'true_false',
  '「滋味」是「南一版 5年級上學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第11課節錄）。「滋味」出自其他課，非「南一版 5年級上學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=12),
  'single_choice',
  '下列何者是「南一版 5年級上學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "寂"}, {"key": "B", "text": "露出"}, {"key": "C", "text": "參加"}, {"key": "D", "text": "歸心似箭"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第12課節錄）。正確答案「歸心似箭」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=12),
  'true_false',
  '「輕舟」是「南一版 5年級上學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 國語科 第12課節錄）。「輕舟」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "因為"}, {"key": "B", "text": "麥芽糖"}, {"key": "C", "text": "賴"}, {"key": "D", "text": "聆聽"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第1課節錄）。正確答案「聆聽」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「因為」是「康軒版 5年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第1課節錄）。「因為」出自其他課，非「康軒版 5年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "庫"}, {"key": "B", "text": "腕"}, {"key": "C", "text": "冷絲絲"}, {"key": "D", "text": "婉"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第2課節錄）。正確答案「婉」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「緊閉」是「康軒版 5年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第2課節錄）。「緊閉」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "普"}, {"key": "B", "text": "待"}, {"key": "C", "text": "嚴"}, {"key": "D", "text": "顯"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第3課節錄）。正確答案「普」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「嚴」是「康軒版 5年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第3課節錄）。「嚴」出自其他課，非「康軒版 5年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鄰居"}, {"key": "B", "text": "家庭"}, {"key": "C", "text": "山丘"}, {"key": "D", "text": "骨"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第4課節錄）。正確答案「骨」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「急診」是「康軒版 5年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第4課節錄）。「急診」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=5),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "音"}, {"key": "B", "text": "糞"}, {"key": "C", "text": "偷"}, {"key": "D", "text": "沉浸"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第5課節錄）。正確答案「沉浸」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=5),
  'true_false',
  '「偷」是「康軒版 5年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第5課節錄）。「偷」出自其他課，非「康軒版 5年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=6),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "必須"}, {"key": "B", "text": "子"}, {"key": "C", "text": "澆水"}, {"key": "D", "text": "潔"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第6課節錄）。正確答案「必須」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=6),
  'true_false',
  '「魔」是「康軒版 5年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第6課節錄）。「魔」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=7),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鬼斧神工"}, {"key": "B", "text": "延"}, {"key": "C", "text": "飛翔"}, {"key": "D", "text": "現代"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第7課節錄）。正確答案「延」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=7),
  'true_false',
  '「飛翔」是「康軒版 5年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第7課節錄）。「飛翔」出自其他課，非「康軒版 5年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=8),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "否"}, {"key": "B", "text": "珊"}, {"key": "C", "text": "頂"}, {"key": "D", "text": "聽見"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第8課節錄）。正確答案「珊」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=8),
  'true_false',
  '「瑚」是「康軒版 5年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第8課節錄）。「瑚」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=9),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "孤"}, {"key": "B", "text": "玻"}, {"key": "C", "text": "段"}, {"key": "D", "text": "您"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第9課節錄）。正確答案「玻」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=9),
  'true_false',
  '「孤」是「康軒版 5年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第9課節錄）。「孤」出自其他課，非「康軒版 5年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=10),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "懶"}, {"key": "B", "text": "爽"}, {"key": "C", "text": "傘"}, {"key": "D", "text": "澤"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第10課節錄）。正確答案「澤」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=10),
  'true_false',
  '「狼」是「康軒版 5年級下學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第10課節錄）。「狼」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=11),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "陽"}, {"key": "B", "text": "誣告"}, {"key": "C", "text": "愁"}, {"key": "D", "text": "霆"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第11課節錄）。正確答案「霆」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=11),
  'true_false',
  '「愁」是「康軒版 5年級下學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第11課節錄）。「愁」出自其他課，非「康軒版 5年級下學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=12),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "保佑"}, {"key": "B", "text": "雙胞胎"}, {"key": "C", "text": "蓋子"}, {"key": "D", "text": "給"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第12課節錄）。正確答案「保佑」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=12),
  'true_false',
  '「藤蔓」是「康軒版 5年級下學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 國語科 第12課節錄）。「藤蔓」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "帳"}, {"key": "B", "text": "敗"}, {"key": "C", "text": "段"}, {"key": "D", "text": "詠"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第1課節錄）。正確答案「帳」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「詠」是「康軒版 5年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第1課節錄）。「詠」出自其他課，非「康軒版 5年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "自由"}, {"key": "B", "text": "不斷"}, {"key": "C", "text": "大哭"}, {"key": "D", "text": "玻"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第2課節錄）。正確答案「不斷」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「斷」是「康軒版 5年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第2課節錄）。「斷」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "喘"}, {"key": "B", "text": "居"}, {"key": "C", "text": "派"}, {"key": "D", "text": "冷箭"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第3課節錄）。正確答案「冷箭」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「居」是「康軒版 5年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第3課節錄）。「居」出自其他課，非「康軒版 5年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "慨"}, {"key": "B", "text": "繁"}, {"key": "C", "text": "臉"}, {"key": "D", "text": "政府"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第4課節錄）。正確答案「慨」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「滋」是「康軒版 5年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第4課節錄）。「滋」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=5),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "音"}, {"key": "B", "text": "售"}, {"key": "C", "text": "夫"}, {"key": "D", "text": "政府"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第5課節錄）。正確答案「售」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=5),
  'true_false',
  '「音」是「康軒版 5年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第5課節錄）。「音」出自其他課，非「康軒版 5年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=6),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "露出"}, {"key": "B", "text": "樣貌"}, {"key": "C", "text": "敗"}, {"key": "D", "text": "老師"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第6課節錄）。正確答案「樣貌」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=6),
  'true_false',
  '「判」是「康軒版 5年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第6課節錄）。「判」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=7),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鼻"}, {"key": "B", "text": "芽"}, {"key": "C", "text": "戴"}, {"key": "D", "text": "緻"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第7課節錄）。正確答案「緻」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=7),
  'true_false',
  '「鼻」是「康軒版 5年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第7課節錄）。「鼻」出自其他課，非「康軒版 5年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=8),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "震撼"}, {"key": "B", "text": "捲"}, {"key": "C", "text": "諺語"}, {"key": "D", "text": "白皙"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第8課節錄）。正確答案「震撼」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=8),
  'true_false',
  '「性」是「康軒版 5年級上學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第8課節錄）。「性」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=9),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "栽"}, {"key": "B", "text": "幼"}, {"key": "C", "text": "凱"}, {"key": "D", "text": "領"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第9課節錄）。正確答案「幼」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=9),
  'true_false',
  '「領」是「康軒版 5年級上學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第9課節錄）。「領」出自其他課，非「康軒版 5年級上學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=10),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鋸"}, {"key": "B", "text": "謹慎"}, {"key": "C", "text": "甩"}, {"key": "D", "text": "扉"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第10課節錄）。正確答案「扉」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=10),
  'true_false',
  '「幽」是「康軒版 5年級上學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第10課節錄）。「幽」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=11),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鄰"}, {"key": "B", "text": "謝"}, {"key": "C", "text": "坡"}, {"key": "D", "text": "吼"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第11課節錄）。正確答案「吼」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=11),
  'true_false',
  '「坡」是「康軒版 5年級上學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第11課節錄）。「坡」出自其他課，非「康軒版 5年級上學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=12),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "庫"}, {"key": "B", "text": "壓軸"}, {"key": "C", "text": "牆壁"}, {"key": "D", "text": "烤"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第12課節錄）。正確答案「烤」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=12),
  'true_false',
  '「躍躍欲試」是「康軒版 5年級上學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 國語科 第12課節錄）。「躍躍欲試」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "飛翔"}, {"key": "B", "text": "獵"}, {"key": "C", "text": "棵"}, {"key": "D", "text": "足跡"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第1課節錄）。正確答案「足跡」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「棵」是「翰林版 5年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第1課節錄）。「棵」出自其他課，非「翰林版 5年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "並列"}, {"key": "B", "text": "抓"}, {"key": "C", "text": "猾"}, {"key": "D", "text": "掠"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第2課節錄）。正確答案「掠」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「降」是「翰林版 5年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第2課節錄）。「降」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "慎"}, {"key": "B", "text": "簽證"}, {"key": "C", "text": "陽"}, {"key": "D", "text": "旨"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第3課節錄）。正確答案「簽證」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「旨」是「翰林版 5年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第3課節錄）。「旨」出自其他課，非「翰林版 5年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "唱歌"}, {"key": "B", "text": "雕塑"}, {"key": "C", "text": "私"}, {"key": "D", "text": "非"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第4課節錄）。正確答案「私」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「採訪」是「翰林版 5年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第4課節錄）。「採訪」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=5),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "萬華"}, {"key": "B", "text": "礙"}, {"key": "C", "text": "表"}, {"key": "D", "text": "自豪"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第5課節錄）。正確答案「礙」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=5),
  'true_false',
  '「表」是「翰林版 5年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第5課節錄）。「表」出自其他課，非「翰林版 5年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=6),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "最"}, {"key": "B", "text": "開朗"}, {"key": "C", "text": "厲鬼"}, {"key": "D", "text": "適合"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第6課節錄）。正確答案「厲鬼」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=6),
  'true_false',
  '「草蓆」是「翰林版 5年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第6課節錄）。「草蓆」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=7),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "雙"}, {"key": "B", "text": "傍"}, {"key": "C", "text": "向"}, {"key": "D", "text": "遺"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第7課節錄）。正確答案「遺」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=7),
  'true_false',
  '「雙」是「翰林版 5年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第7課節錄）。「雙」出自其他課，非「翰林版 5年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=8),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "呼"}, {"key": "B", "text": "載歌載舞"}, {"key": "C", "text": "安"}, {"key": "D", "text": "詼"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第8課節錄）。正確答案「詼」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=8),
  'true_false',
  '「哏」是「翰林版 5年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第8課節錄）。「哏」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=9),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "謹慎"}, {"key": "B", "text": "星"}, {"key": "C", "text": "裡"}, {"key": "D", "text": "淨"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第9課節錄）。正確答案「謹慎」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=9),
  'true_false',
  '「淨」是「翰林版 5年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第9課節錄）。「淨」出自其他課，非「翰林版 5年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=10),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "榜"}, {"key": "B", "text": "手腕"}, {"key": "C", "text": "睡"}, {"key": "D", "text": "款"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第10課節錄）。正確答案「手腕」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=10),
  'true_false',
  '「白皙」是「翰林版 5年級下學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第10課節錄）。「白皙」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=11),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "爽朗"}, {"key": "B", "text": "礦"}, {"key": "C", "text": "直笛"}, {"key": "D", "text": "恍"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第11課節錄）。正確答案「恍」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=11),
  'true_false',
  '「礦」是「翰林版 5年級下學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第11課節錄）。「礦」出自其他課，非「翰林版 5年級下學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=12),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "嘉賓"}, {"key": "B", "text": "賺"}, {"key": "C", "text": "蓮霧"}, {"key": "D", "text": "止血"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第12課節錄）。正確答案「止血」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=12),
  'true_false',
  '「避免」是「翰林版 5年級下學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 國語科 第12課節錄）。「避免」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 5年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "耗盡"}, {"key": "B", "text": "自言自語"}, {"key": "C", "text": "周遭"}, {"key": "D", "text": "擾"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第1課節錄）。正確答案「周遭」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「擾」是「翰林版 5年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第1課節錄）。「擾」出自其他課，非「翰林版 5年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 5年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "可以"}, {"key": "B", "text": "撐"}, {"key": "C", "text": "熟"}, {"key": "D", "text": "陰霾"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第2課節錄）。正確答案「熟」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「威」是「翰林版 5年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第2課節錄）。「威」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 5年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "碗"}, {"key": "B", "text": "嚨"}, {"key": "C", "text": "羞恥"}, {"key": "D", "text": "雨後春筍"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第3課節錄）。正確答案「羞恥」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「嚨」是「翰林版 5年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第3課節錄）。「嚨」出自其他課，非「翰林版 5年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 5年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "陰"}, {"key": "B", "text": "書頁"}, {"key": "C", "text": "雨後春筍"}, {"key": "D", "text": "予"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第4課節錄）。正確答案「雨後春筍」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「餐廳」是「翰林版 5年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第4課節錄）。「餐廳」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=5),
  'single_choice',
  '下列何者是「翰林版 5年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "齊天大聖"}, {"key": "B", "text": "裹"}, {"key": "C", "text": "院"}, {"key": "D", "text": "蔬菜"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第5課節錄）。正確答案「院」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=5),
  'true_false',
  '「蔬菜」是「翰林版 5年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第5課節錄）。「蔬菜」出自其他課，非「翰林版 5年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=6),
  'single_choice',
  '下列何者是「翰林版 5年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "焚化"}, {"key": "B", "text": "隨"}, {"key": "C", "text": "小丑魚"}, {"key": "D", "text": "好像"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第6課節錄）。正確答案「焚化」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=6),
  'true_false',
  '「飲」是「翰林版 5年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第6課節錄）。「飲」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=7),
  'single_choice',
  '下列何者是「翰林版 5年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鳴"}, {"key": "B", "text": "統"}, {"key": "C", "text": "米線"}, {"key": "D", "text": "丞"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第7課節錄）。正確答案「鳴」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=7),
  'true_false',
  '「米線」是「翰林版 5年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第7課節錄）。「米線」出自其他課，非「翰林版 5年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=8),
  'single_choice',
  '下列何者是「翰林版 5年級上學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "樸實"}, {"key": "B", "text": "盼"}, {"key": "C", "text": "封面"}, {"key": "D", "text": "餘"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第8課節錄）。正確答案「盼」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=8),
  'true_false',
  '「葫」是「翰林版 5年級上學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第8課節錄）。「葫」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=9),
  'single_choice',
  '下列何者是「翰林版 5年級上學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "豬"}, {"key": "B", "text": "圃"}, {"key": "C", "text": "沿"}, {"key": "D", "text": "下課"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第9課節錄）。正確答案「圃」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=9),
  'true_false',
  '「沿」是「翰林版 5年級上學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第9課節錄）。「沿」出自其他課，非「翰林版 5年級上學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=10),
  'single_choice',
  '下列何者是「翰林版 5年級上學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "甜蜜"}, {"key": "B", "text": "洋"}, {"key": "C", "text": "強勁"}, {"key": "D", "text": "額頭"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第10課節錄）。正確答案「洋」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=10),
  'true_false',
  '「丈」是「翰林版 5年級上學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第10課節錄）。「丈」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=11),
  'single_choice',
  '下列何者是「翰林版 5年級上學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "籃"}, {"key": "B", "text": "牆壁"}, {"key": "C", "text": "蜻"}, {"key": "D", "text": "橡皮擦"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第11課節錄）。正確答案「籃」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=11),
  'true_false',
  '「牆壁」是「翰林版 5年級上學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第11課節錄）。「牆壁」出自其他課，非「翰林版 5年級上學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=12),
  'single_choice',
  '下列何者是「翰林版 5年級上學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "芽"}, {"key": "B", "text": "馬偕"}, {"key": "C", "text": "糟"}, {"key": "D", "text": "夫"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第12課節錄）。正確答案「糟」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=12),
  'true_false',
  '「奇蹟」是「翰林版 5年級上學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 國語科 第12課節錄）。「奇蹟」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 6年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "卡"}, {"key": "B", "text": "喉嚨"}, {"key": "C", "text": "錯愕"}, {"key": "D", "text": "盾"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第1課節錄）。正確答案「盾」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=1),
  'true_false',
  '「喉嚨」是「南一版 6年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第1課節錄）。「喉嚨」出自其他課，非「南一版 6年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 6年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "仔"}, {"key": "B", "text": "撐"}, {"key": "C", "text": "旋"}, {"key": "D", "text": "狩獵"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第2課節錄）。正確答案「狩獵」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=2),
  'true_false',
  '「喉嚨」是「南一版 6年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第2課節錄）。「喉嚨」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 6年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "蹦"}, {"key": "B", "text": "拿"}, {"key": "C", "text": "邏"}, {"key": "D", "text": "免"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第3課節錄）。正確答案「邏」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=3),
  'true_false',
  '「免」是「南一版 6年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第3課節錄）。「免」出自其他課，非「南一版 6年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 6年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "弧"}, {"key": "B", "text": "來"}, {"key": "C", "text": "上鎖"}, {"key": "D", "text": "邇"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第4課節錄）。正確答案「邇」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=4),
  'true_false',
  '「楷模」是「南一版 6年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第4課節錄）。「楷模」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=5),
  'single_choice',
  '下列何者是「南一版 6年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "褐"}, {"key": "B", "text": "洶湧"}, {"key": "C", "text": "杆"}, {"key": "D", "text": "誰"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第5課節錄）。正確答案「洶湧」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=5),
  'true_false',
  '「杆」是「南一版 6年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第5課節錄）。「杆」出自其他課，非「南一版 6年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=6),
  'single_choice',
  '下列何者是「南一版 6年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "有名"}, {"key": "B", "text": "狩獵"}, {"key": "C", "text": "海浪"}, {"key": "D", "text": "犯"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第6課節錄）。正確答案「犯」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=6),
  'true_false',
  '「汰」是「南一版 6年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第6課節錄）。「汰」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=7),
  'single_choice',
  '下列何者是「南一版 6年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "跪"}, {"key": "B", "text": "到處"}, {"key": "C", "text": "懇"}, {"key": "D", "text": "驚"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第7課節錄）。正確答案「懇」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=7),
  'true_false',
  '「到處」是「南一版 6年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第7課節錄）。「到處」出自其他課，非「南一版 6年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=8),
  'single_choice',
  '下列何者是「南一版 6年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "煥"}, {"key": "B", "text": "厭"}, {"key": "C", "text": "輯"}, {"key": "D", "text": "吁"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第8課節錄）。正確答案「厭」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=8),
  'true_false',
  '「驪歌」是「南一版 6年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第8課節錄）。「驪歌」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=9),
  'single_choice',
  '下列何者是「南一版 6年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "旅"}, {"key": "B", "text": "誼"}, {"key": "C", "text": "公"}, {"key": "D", "text": "誦讀"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第9課節錄）。正確答案「誦讀」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=9),
  'true_false',
  '「公」是「南一版 6年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 國語科 第9課節錄）。「公」出自其他課，非「南一版 6年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 6年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "掘"}, {"key": "B", "text": "生命"}, {"key": "C", "text": "塵"}, {"key": "D", "text": "魚"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第1課節錄）。正確答案「塵」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=1),
  'true_false',
  '「掘」是「南一版 6年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第1課節錄）。「掘」出自其他課，非「南一版 6年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 6年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "咂"}, {"key": "B", "text": "愈"}, {"key": "C", "text": "聯絡簿"}, {"key": "D", "text": "駕"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第2課節錄）。正確答案「咂」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=2),
  'true_false',
  '「瀉」是「南一版 6年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第2課節錄）。「瀉」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 6年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "如意"}, {"key": "B", "text": "戶"}, {"key": "C", "text": "湧現"}, {"key": "D", "text": "皆"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第3課節錄）。正確答案「皆」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=3),
  'true_false',
  '「如意」是「南一版 6年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第3課節錄）。「如意」出自其他課，非「南一版 6年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 6年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "屢"}, {"key": "B", "text": "室"}, {"key": "C", "text": "襯"}, {"key": "D", "text": "讀"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第4課節錄）。正確答案「襯」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=4),
  'true_false',
  '「惹」是「南一版 6年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第4課節錄）。「惹」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=5),
  'single_choice',
  '下列何者是「南一版 6年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "快樂"}, {"key": "B", "text": "載歌載舞"}, {"key": "C", "text": "籬笆"}, {"key": "D", "text": "餘"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第5課節錄）。正確答案「載歌載舞」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=5),
  'true_false',
  '「餘」是「南一版 6年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第5課節錄）。「餘」出自其他課，非「南一版 6年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=6),
  'single_choice',
  '下列何者是「南一版 6年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "季"}, {"key": "B", "text": "棚"}, {"key": "C", "text": "誌"}, {"key": "D", "text": "惡"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第6課節錄）。正確答案「誌」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=6),
  'true_false',
  '「奪」是「南一版 6年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第6課節錄）。「奪」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=7),
  'single_choice',
  '下列何者是「南一版 6年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "衡"}, {"key": "B", "text": "皆"}, {"key": "C", "text": "一座"}, {"key": "D", "text": "厭"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第7課節錄）。正確答案「衡」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=7),
  'true_false',
  '「厭」是「南一版 6年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第7課節錄）。「厭」出自其他課，非「南一版 6年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=8),
  'single_choice',
  '下列何者是「南一版 6年級上學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "顧慮"}, {"key": "B", "text": "季"}, {"key": "C", "text": "按"}, {"key": "D", "text": "飢渴"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第8課節錄）。正確答案「飢渴」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=8),
  'true_false',
  '「自怨自艾」是「南一版 6年級上學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第8課節錄）。「自怨自艾」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=9),
  'single_choice',
  '下列何者是「南一版 6年級上學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "親朋好友"}, {"key": "B", "text": "議員"}, {"key": "C", "text": "江"}, {"key": "D", "text": "自"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第9課節錄）。正確答案「江」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=9),
  'true_false',
  '「親朋好友」是「南一版 6年級上學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第9課節錄）。「親朋好友」出自其他課，非「南一版 6年級上學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=10),
  'single_choice',
  '下列何者是「南一版 6年級上學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鍛鍊"}, {"key": "B", "text": "金燦燦"}, {"key": "C", "text": "詫異"}, {"key": "D", "text": "搔"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第10課節錄）。正確答案「詫異」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=10),
  'true_false',
  '「變幻莫測」是「南一版 6年級上學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第10課節錄）。「變幻莫測」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=11),
  'single_choice',
  '下列何者是「南一版 6年級上學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "的"}, {"key": "B", "text": "隊"}, {"key": "C", "text": "泛"}, {"key": "D", "text": "載歌載舞"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第11課節錄）。正確答案「泛」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=11),
  'true_false',
  '「載歌載舞」是「南一版 6年級上學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第11課節錄）。「載歌載舞」出自其他課，非「南一版 6年級上學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=12),
  'single_choice',
  '下列何者是「南一版 6年級上學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "煎熬"}, {"key": "B", "text": "慧"}, {"key": "C", "text": "故事"}, {"key": "D", "text": "輕輕"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第12課節錄）。正確答案「煎熬」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=12),
  'true_false',
  '「酣」是「南一版 6年級上學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 國語科 第12課節錄）。「酣」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 6年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "驗"}, {"key": "B", "text": "掠食者"}, {"key": "C", "text": "館"}, {"key": "D", "text": "摟"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第1課節錄）。正確答案「掠食者」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「驗」是「康軒版 6年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第1課節錄）。「驗」出自其他課，非「康軒版 6年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 6年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "如意"}, {"key": "B", "text": "可愛"}, {"key": "C", "text": "擾"}, {"key": "D", "text": "愜"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第2課節錄）。正確答案「愜」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「回眸」是「康軒版 6年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第2課節錄）。「回眸」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 6年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鬆"}, {"key": "B", "text": "優美"}, {"key": "C", "text": "廠"}, {"key": "D", "text": "糖水"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第3課節錄）。正確答案「鬆」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「糖水」是「康軒版 6年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第3課節錄）。「糖水」出自其他課，非「康軒版 6年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 6年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "江"}, {"key": "B", "text": "治"}, {"key": "C", "text": "盡頭"}, {"key": "D", "text": "誼"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第4課節錄）。正確答案「誼」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「摯」是「康軒版 6年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第4課節錄）。「摯」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=5),
  'single_choice',
  '下列何者是「康軒版 6年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "抓"}, {"key": "B", "text": "礁"}, {"key": "C", "text": "樁"}, {"key": "D", "text": "合租"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第5課節錄）。正確答案「樁」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=5),
  'true_false',
  '「礁」是「康軒版 6年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第5課節錄）。「礁」出自其他課，非「康軒版 6年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=6),
  'single_choice',
  '下列何者是「康軒版 6年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "裡"}, {"key": "B", "text": "陰"}, {"key": "C", "text": "值"}, {"key": "D", "text": "興致"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第6課節錄）。正確答案「陰」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=6),
  'true_false',
  '「斑」是「康軒版 6年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第6課節錄）。「斑」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=7),
  'single_choice',
  '下列何者是「康軒版 6年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "窣"}, {"key": "B", "text": "晉"}, {"key": "C", "text": "根本"}, {"key": "D", "text": "幼苗"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第7課節錄）。正確答案「窣」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=7),
  'true_false',
  '「晉」是「康軒版 6年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第7課節錄）。「晉」出自其他課，非「康軒版 6年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=8),
  'single_choice',
  '下列何者是「康軒版 6年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "雙"}, {"key": "B", "text": "洗"}, {"key": "C", "text": "洋"}, {"key": "D", "text": "構築"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第8課節錄）。正確答案「構築」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=8),
  'true_false',
  '「諺語」是「康軒版 6年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第8課節錄）。「諺語」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=9),
  'single_choice',
  '下列何者是「康軒版 6年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "礁"}, {"key": "B", "text": "曙光"}, {"key": "C", "text": "分辨"}, {"key": "D", "text": "盡力"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第9課節錄）。正確答案「曙光」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=9),
  'true_false',
  '「分辨」是「康軒版 6年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 國語科 第9課節錄）。「分辨」出自其他課，非「康軒版 6年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "尷尬"}, {"key": "B", "text": "頭髮"}, {"key": "C", "text": "滋"}, {"key": "D", "text": "學校"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第1課節錄）。正確答案「尷尬」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「頭髮」是「康軒版 6年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第1課節錄）。「頭髮」出自其他課，非「康軒版 6年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "楊修"}, {"key": "B", "text": "拿"}, {"key": "C", "text": "湯圓"}, {"key": "D", "text": "縷"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第2課節錄）。正確答案「縷」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「碗」是「康軒版 6年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第2課節錄）。「碗」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "茁"}, {"key": "B", "text": "大王"}, {"key": "C", "text": "飲"}, {"key": "D", "text": "型"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第3課節錄）。正確答案「茁」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「飲」是「康軒版 6年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第3課節錄）。「飲」出自其他課，非「康軒版 6年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "上桌"}, {"key": "B", "text": "彰"}, {"key": "C", "text": "疏失"}, {"key": "D", "text": "曹操"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第4課節錄）。正確答案「彰」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「煮」是「康軒版 6年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第4課節錄）。「煮」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=5),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "膠水"}, {"key": "B", "text": "自由"}, {"key": "C", "text": "凝"}, {"key": "D", "text": "熬煮"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第5課節錄）。正確答案「熬煮」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=5),
  'true_false',
  '「膠水」是「康軒版 6年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第5課節錄）。「膠水」出自其他課，非「康軒版 6年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=6),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "蟒蛇"}, {"key": "B", "text": "陪伴"}, {"key": "C", "text": "先"}, {"key": "D", "text": "徜徉"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第6課節錄）。正確答案「徜徉」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=6),
  'true_false',
  '「習慣」是「康軒版 6年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第6課節錄）。「習慣」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=7),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "千萬"}, {"key": "B", "text": "皆"}, {"key": "C", "text": "敏銳"}, {"key": "D", "text": "水珠"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第7課節錄）。正確答案「皆」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=7),
  'true_false',
  '「水珠」是「康軒版 6年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第7課節錄）。「水珠」出自其他課，非「康軒版 6年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=8),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "抓住"}, {"key": "B", "text": "可以"}, {"key": "C", "text": "猾"}, {"key": "D", "text": "雜誌"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第8課節錄）。正確答案「猾」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=8),
  'true_false',
  '「隙」是「康軒版 6年級上學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第8課節錄）。「隙」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=9),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "眾多"}, {"key": "B", "text": "薰"}, {"key": "C", "text": "堤"}, {"key": "D", "text": "醜"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第9課節錄）。正確答案「薰」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=9),
  'true_false',
  '「堤」是「康軒版 6年級上學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第9課節錄）。「堤」出自其他課，非「康軒版 6年級上學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=10),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "妙"}, {"key": "B", "text": "暖烘烘"}, {"key": "C", "text": "根據"}, {"key": "D", "text": "乎"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第10課節錄）。正確答案「暖烘烘」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=10),
  'true_false',
  '「耶」是「康軒版 6年級上學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第10課節錄）。「耶」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=11),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "言簡意賅"}, {"key": "B", "text": "顏色"}, {"key": "C", "text": "某"}, {"key": "D", "text": "輕而易舉"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第11課節錄）。正確答案「某」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=11),
  'true_false',
  '「顏色」是「康軒版 6年級上學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第11課節錄）。「顏色」出自其他課，非「康軒版 6年級上學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=12),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "儘管"}, {"key": "B", "text": "糯"}, {"key": "C", "text": "顏色"}, {"key": "D", "text": "盡責"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第12課節錄）。正確答案「儘管」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=12),
  'true_false',
  '「螞蟻」是「康軒版 6年級上學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 國語科 第12課節錄）。「螞蟻」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 6年級下學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "遍"}, {"key": "B", "text": "避免"}, {"key": "C", "text": "建築"}, {"key": "D", "text": "村"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第1課節錄）。正確答案「建築」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「遍」是「翰林版 6年級下學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第1課節錄）。「遍」出自其他課，非「翰林版 6年級下學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 6年級下學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "摒"}, {"key": "B", "text": "鏡"}, {"key": "C", "text": "襯"}, {"key": "D", "text": "幻"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第2課節錄）。正確答案「摒」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「怖」是「翰林版 6年級下學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第2課節錄）。「怖」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 6年級下學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "孤陋寡聞"}, {"key": "B", "text": "緻"}, {"key": "C", "text": "眺"}, {"key": "D", "text": "焦"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第3課節錄）。正確答案「孤陋寡聞」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「焦」是「翰林版 6年級下學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第3課節錄）。「焦」出自其他課，非「翰林版 6年級下學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 6年級下學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "擾"}, {"key": "B", "text": "纍"}, {"key": "C", "text": "黎明"}, {"key": "D", "text": "敗"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第4課節錄）。正確答案「纍」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「苦澀」是「翰林版 6年級下學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第4課節錄）。「苦澀」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=5),
  'single_choice',
  '下列何者是「翰林版 6年級下學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "踮"}, {"key": "B", "text": "朝"}, {"key": "C", "text": "姆"}, {"key": "D", "text": "飛梭"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第5課節錄）。正確答案「飛梭」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=5),
  'true_false',
  '「朝」是「翰林版 6年級下學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第5課節錄）。「朝」出自其他課，非「翰林版 6年級下學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=6),
  'single_choice',
  '下列何者是「翰林版 6年級下學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "空"}, {"key": "B", "text": "斤"}, {"key": "C", "text": "跨欄"}, {"key": "D", "text": "康復"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第6課節錄）。正確答案「斤」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=6),
  'true_false',
  '「妨」是「翰林版 6年級下學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第6課節錄）。「妨」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=7),
  'single_choice',
  '下列何者是「翰林版 6年級下學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "剪"}, {"key": "B", "text": "掘"}, {"key": "C", "text": "畫"}, {"key": "D", "text": "雛鳥"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第7課節錄）。正確答案「掘」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=7),
  'true_false',
  '「剪」是「翰林版 6年級下學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第7課節錄）。「剪」出自其他課，非「翰林版 6年級下學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=8),
  'single_choice',
  '下列何者是「翰林版 6年級下學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "妨"}, {"key": "B", "text": "要旨"}, {"key": "C", "text": "煩惱"}, {"key": "D", "text": "底"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第8課節錄）。正確答案「要旨」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=8),
  'true_false',
  '「茁壯」是「翰林版 6年級下學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第8課節錄）。「茁壯」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=9),
  'single_choice',
  '下列何者是「翰林版 6年級下學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "煎熬"}, {"key": "B", "text": "阱"}, {"key": "C", "text": "襯"}, {"key": "D", "text": "斜"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第9課節錄）。正確答案「阱」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=9),
  'true_false',
  '「煎熬」是「翰林版 6年級下學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 國語科 第9課節錄）。「煎熬」出自其他課，非「翰林版 6年級下學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 6年級上學期 國語科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "皇帝"}, {"key": "B", "text": "勵"}, {"key": "C", "text": "辣"}, {"key": "D", "text": "晃"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第1課節錄）。正確答案「晃」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「勵」是「翰林版 6年級上學期 國語科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第1課節錄）。「勵」出自其他課，非「翰林版 6年級上學期 國語科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 6年級上學期 國語科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "寂寞"}, {"key": "B", "text": "犧牲"}, {"key": "C", "text": "宇"}, {"key": "D", "text": "臭美"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第2課節錄）。正確答案「寂寞」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「眼眶」是「翰林版 6年級上學期 國語科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第2課節錄）。「眼眶」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 6年級上學期 國語科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "剪"}, {"key": "B", "text": "劍"}, {"key": "C", "text": "婆"}, {"key": "D", "text": "留"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第3課節錄）。正確答案「婆」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「劍」是「翰林版 6年級上學期 國語科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第3課節錄）。「劍」出自其他課，非「翰林版 6年級上學期 國語科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 6年級上學期 國語科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "翹"}, {"key": "B", "text": "商店"}, {"key": "C", "text": "橡"}, {"key": "D", "text": "雜誌"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第4課節錄）。正確答案「翹」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「垂」是「翰林版 6年級上學期 國語科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第4課節錄）。「垂」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=5),
  'single_choice',
  '下列何者是「翰林版 6年級上學期 國語科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "典型"}, {"key": "B", "text": "誼"}, {"key": "C", "text": "白帝城"}, {"key": "D", "text": "恆久"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第5課節錄）。正確答案「典型」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=5),
  'true_false',
  '「誼」是「翰林版 6年級上學期 國語科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第5課節錄）。「誼」出自其他課，非「翰林版 6年級上學期 國語科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=6),
  'single_choice',
  '下列何者是「翰林版 6年級上學期 國語科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "吼叫"}, {"key": "B", "text": "簽證"}, {"key": "C", "text": "侃"}, {"key": "D", "text": "閒"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第6課節錄）。正確答案「侃」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=6),
  'true_false',
  '「競」是「翰林版 6年級上學期 國語科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第6課節錄）。「競」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=7),
  'single_choice',
  '下列何者是「翰林版 6年級上學期 國語科 第7課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "最"}, {"key": "B", "text": "纍"}, {"key": "C", "text": "室"}, {"key": "D", "text": "銅"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第7課節錄）。正確答案「銅」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=7),
  'true_false',
  '「室」是「翰林版 6年級上學期 國語科 第7課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第7課節錄）。「室」出自其他課，非「翰林版 6年級上學期 國語科 第7課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=8),
  'single_choice',
  '下列何者是「翰林版 6年級上學期 國語科 第8課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鑑"}, {"key": "B", "text": "墩"}, {"key": "C", "text": "兄弟"}, {"key": "D", "text": "異口同聲"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第8課節錄）。正確答案「墩」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=8),
  'true_false',
  '「塗」是「翰林版 6年級上學期 國語科 第8課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第8課節錄）。「塗」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=9),
  'single_choice',
  '下列何者是「翰林版 6年級上學期 國語科 第9課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "由"}, {"key": "B", "text": "胖"}, {"key": "C", "text": "吊"}, {"key": "D", "text": "晚"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第9課節錄）。正確答案「吊」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=9),
  'true_false',
  '「胖」是「翰林版 6年級上學期 國語科 第9課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第9課節錄）。「胖」出自其他課，非「翰林版 6年級上學期 國語科 第9課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=10),
  'single_choice',
  '下列何者是「翰林版 6年級上學期 國語科 第10課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "汙染"}, {"key": "B", "text": "辦"}, {"key": "C", "text": "殷勤"}, {"key": "D", "text": "便條"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第10課節錄）。正確答案「殷勤」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=10),
  'true_false',
  '「樸實」是「翰林版 6年級上學期 國語科 第10課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第10課節錄）。「樸實」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=11),
  'single_choice',
  '下列何者是「翰林版 6年級上學期 國語科 第11課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "蟹"}, {"key": "B", "text": "付"}, {"key": "C", "text": "消防員"}, {"key": "D", "text": "軌道"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第11課節錄）。正確答案「蟹」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=11),
  'true_false',
  '「消防員」是「翰林版 6年級上學期 國語科 第11課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第11課節錄）。「消防員」出自其他課，非「翰林版 6年級上學期 國語科 第11課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=12),
  'single_choice',
  '下列何者是「翰林版 6年級上學期 國語科 第12課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "活潑"}, {"key": "B", "text": "莖"}, {"key": "C", "text": "汙染"}, {"key": "D", "text": "鐵罐"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第12課節錄）。正確答案「莖」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='chinese' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=12),
  'true_false',
  '「絲毫」是「翰林版 6年級上學期 國語科 第12課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 國語科 第12課節錄）。「絲毫」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 3年級下學期 社會科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "石滬"}, {"key": "B", "text": "社會發展"}, {"key": "C", "text": "熱絡"}, {"key": "D", "text": "全球暖化"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 社會科 第1課節錄）。正確答案「石滬」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=1),
  'true_false',
  '「全球暖化」是「南一版 3年級下學期 社會科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 社會科 第1課節錄）。「全球暖化」出自其他課，非「南一版 3年級下學期 社會科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 3年級下學期 社會科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "新港文書"}, {"key": "B", "text": "原住民"}, {"key": "C", "text": "購物袋"}, {"key": "D", "text": "身心障礙"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 社會科 第2課節錄）。正確答案「原住民」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=2),
  'true_false',
  '「守望相助」是「南一版 3年級下學期 社會科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 社會科 第2課節錄）。「守望相助」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 3年級下學期 社會科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "引水"}, {"key": "B", "text": "社會變遷"}, {"key": "C", "text": "保險"}, {"key": "D", "text": "行動支付"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 社會科 第3課節錄）。正確答案「保險」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=3),
  'true_false',
  '「社會變遷」是「南一版 3年級下學期 社會科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 社會科 第3課節錄）。「社會變遷」出自其他課，非「南一版 3年級下學期 社會科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 3年級下學期 社會科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "虛擬實境"}, {"key": "B", "text": "艋舺"}, {"key": "C", "text": "引水"}, {"key": "D", "text": "先民"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 社會科 第4課節錄）。正確答案「引水」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=4),
  'true_false',
  '「諸羅」是「南一版 3年級下學期 社會科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 社會科 第4課節錄）。「諸羅」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 社會科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "集散"}, {"key": "B", "text": "機械化"}, {"key": "C", "text": "鄉村"}, {"key": "D", "text": "門牌"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 社會科 第1課節錄）。正確答案「門牌」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「鄉村」是「康軒版 3年級下學期 社會科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 社會科 第1課節錄）。「鄉村」出自其他課，非「康軒版 3年級下學期 社會科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 社會科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "轉型"}, {"key": "B", "text": "丘陵"}, {"key": "C", "text": "電信"}, {"key": "D", "text": "婚喪喜慶"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 社會科 第2課節錄）。正確答案「電信」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「通訊」是「康軒版 3年級下學期 社會科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 社會科 第2課節錄）。「通訊」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 社會科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "牧場"}, {"key": "B", "text": "禮券"}, {"key": "C", "text": "節慶"}, {"key": "D", "text": "海流"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 社會科 第3課節錄）。正確答案「禮券」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「海流」是「康軒版 3年級下學期 社會科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 社會科 第3課節錄）。「海流」出自其他課，非「康軒版 3年級下學期 社會科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 社會科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "過度"}, {"key": "B", "text": "貝塚"}, {"key": "C", "text": "嘉南大圳"}, {"key": "D", "text": "陰符經"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 社會科 第4課節錄）。正確答案「過度」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「綠色消費」是「康軒版 3年級下學期 社會科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 社會科 第4課節錄）。「綠色消費」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=5),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 社會科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "推動"}, {"key": "B", "text": "地熱"}, {"key": "C", "text": "身心障礙"}, {"key": "D", "text": "開墾"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 社會科 第5課節錄）。正確答案「開墾」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=5),
  'true_false',
  '「推動」是「康軒版 3年級下學期 社會科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 社會科 第5課節錄）。「推動」出自其他課，非「康軒版 3年級下學期 社會科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=6),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 社會科 第6課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "人文"}, {"key": "B", "text": "公共事務"}, {"key": "C", "text": "觀光"}, {"key": "D", "text": "油燈"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 社會科 第6課節錄）。正確答案「人文」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=6),
  'true_false',
  '「琉璃珠」是「康軒版 3年級下學期 社會科 第6課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 社會科 第6課節錄）。「琉璃珠」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 社會科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "分工"}, {"key": "B", "text": "公平"}, {"key": "C", "text": "抗爭"}, {"key": "D", "text": "部落"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 社會科 第1課節錄）。正確答案「公平」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「分工」是「康軒版 3年級上學期 社會科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 社會科 第1課節錄）。「分工」出自其他課，非「康軒版 3年級上學期 社會科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 社會科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "地熱"}, {"key": "B", "text": "霸凌"}, {"key": "C", "text": "演變"}, {"key": "D", "text": "疏離"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 社會科 第2課節錄）。正確答案「霸凌」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「暗藏」是「康軒版 3年級上學期 社會科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 社會科 第2課節錄）。「暗藏」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 社會科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "荷蘭王國（Kingdom of the Netherlands）"}, {"key": "B", "text": "就業服務"}, {"key": "C", "text": "義賣"}, {"key": "D", "text": "魯凱族"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 社會科 第3課節錄）。正確答案「荷蘭王國（Kingdom of the Netherlands）」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「義賣」是「康軒版 3年級上學期 社會科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 社會科 第3課節錄）。「義賣」出自其他課，非「康軒版 3年級上學期 社會科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 社會科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "伊斯蘭教"}, {"key": "B", "text": "新港文書"}, {"key": "C", "text": "樟腦"}, {"key": "D", "text": "祭典"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 社會科 第1課節錄）。正確答案「伊斯蘭教」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「祭典」是「翰林版 3年級下學期 社會科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 社會科 第1課節錄）。「祭典」出自其他課，非「翰林版 3年級下學期 社會科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 社會科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "魯凱族"}, {"key": "B", "text": "網路購物"}, {"key": "C", "text": "都市"}, {"key": "D", "text": "養殖"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 社會科 第2課節錄）。正確答案「養殖」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「蜂炮」是「翰林版 3年級下學期 社會科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 社會科 第2課節錄）。「蜂炮」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 社會科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "自然資源"}, {"key": "B", "text": "甲骨文"}, {"key": "C", "text": "機械化"}, {"key": "D", "text": "記帳"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 社會科 第3課節錄）。正確答案「自然資源」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「記帳」是「翰林版 3年級下學期 社會科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 社會科 第3課節錄）。「記帳」出自其他課，非「翰林版 3年級下學期 社會科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 社會科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "民變"}, {"key": "B", "text": "農業社會"}, {"key": "C", "text": "先民"}, {"key": "D", "text": "電信"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 社會科 第4課節錄）。正確答案「農業社會」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「人力」是「翰林版 3年級下學期 社會科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 社會科 第4課節錄）。「人力」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=5),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 社會科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "購物袋"}, {"key": "B", "text": "公共事務"}, {"key": "C", "text": "梯田"}, {"key": "D", "text": "遊憩"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 社會科 第5課節錄）。正確答案「購物袋」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=5),
  'true_false',
  '「遊憩」是「翰林版 3年級下學期 社會科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 社會科 第5課節錄）。「遊憩」出自其他課，非「翰林版 3年級下學期 社會科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 4年級下學期 社會科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "榻榻米"}, {"key": "B", "text": "公共建設"}, {"key": "C", "text": "國際奧林匹克委員會"}, {"key": "D", "text": "台地"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 社會科 第1課節錄）。正確答案「台地」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=1),
  'true_false',
  '「榻榻米」是「南一版 4年級下學期 社會科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 社會科 第1課節錄）。「榻榻米」出自其他課，非「南一版 4年級下學期 社會科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 4年級下學期 社會科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "港市"}, {"key": "B", "text": "嘉南大圳"}, {"key": "C", "text": "布袋戲"}, {"key": "D", "text": "自動化"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 社會科 第2課節錄）。正確答案「自動化」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=2),
  'true_false',
  '「製造業」是「南一版 4年級下學期 社會科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 社會科 第2課節錄）。「製造業」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 4年級下學期 社會科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "熱蘭遮城"}, {"key": "B", "text": "再生資源"}, {"key": "C", "text": "通商"}, {"key": "D", "text": "人口"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 社會科 第3課節錄）。正確答案「人口」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=3),
  'true_false',
  '「通商」是「南一版 4年級下學期 社會科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 社會科 第3課節錄）。「通商」出自其他課，非「南一版 4年級下學期 社會科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 4年級下學期 社會科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "泰雅族"}, {"key": "B", "text": "土地沙漠化"}, {"key": "C", "text": "保險"}, {"key": "D", "text": "捕撈"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 社會科 第4課節錄）。正確答案「泰雅族」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=4),
  'true_false',
  '「祭祀」是「南一版 4年級下學期 社會科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 社會科 第4課節錄）。「祭祀」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 社會科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "有機"}, {"key": "B", "text": "牧場"}, {"key": "C", "text": "生育"}, {"key": "D", "text": "文面"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 社會科 第1課節錄）。正確答案「牧場」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「生育」是「康軒版 4年級下學期 社會科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 社會科 第1課節錄）。「生育」出自其他課，非「康軒版 4年級下學期 社會科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 社會科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "戶籍登記"}, {"key": "B", "text": "人文"}, {"key": "C", "text": "大眾運輸"}, {"key": "D", "text": "平坦"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 社會科 第2課節錄）。正確答案「戶籍登記」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「檜木」是「康軒版 4年級下學期 社會科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 社會科 第2課節錄）。「檜木」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 社會科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "人工智慧"}, {"key": "B", "text": "濁水溪"}, {"key": "C", "text": "謠言"}, {"key": "D", "text": "機能"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 社會科 第3課節錄）。正確答案「謠言」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「濁水溪」是「康軒版 4年級下學期 社會科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 社會科 第3課節錄）。「濁水溪」出自其他課，非「康軒版 4年級下學期 社會科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 社會科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "人文"}, {"key": "B", "text": "鄉土"}, {"key": "C", "text": "學堂"}, {"key": "D", "text": "協定"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 社會科 第4課節錄）。正確答案「人文」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「黑面琵鷺」是「康軒版 4年級下學期 社會科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 社會科 第4課節錄）。「黑面琵鷺」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 社會科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "殖民"}, {"key": "B", "text": "灌溉"}, {"key": "C", "text": "貝塚"}, {"key": "D", "text": "機械化"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 社會科 第1課節錄）。正確答案「灌溉」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「殖民」是「康軒版 4年級上學期 社會科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 社會科 第1課節錄）。「殖民」出自其他課，非「康軒版 4年級上學期 社會科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 社會科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "汙水處理"}, {"key": "B", "text": "暗藏"}, {"key": "C", "text": "農業社會"}, {"key": "D", "text": "觀光"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 社會科 第2課節錄）。正確答案「觀光」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「巡禮」是「康軒版 4年級上學期 社會科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 社會科 第2課節錄）。「巡禮」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 社會科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "壯麗"}, {"key": "B", "text": "偏見"}, {"key": "C", "text": "發展"}, {"key": "D", "text": "通訊"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 社會科 第3課節錄）。正確答案「發展」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「通訊」是「康軒版 4年級上學期 社會科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 社會科 第3課節錄）。「通訊」出自其他課，非「康軒版 4年級上學期 社會科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 社會科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "水井"}, {"key": "B", "text": "公平"}, {"key": "C", "text": "造船"}, {"key": "D", "text": "義賣"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 社會科 第1課節錄）。正確答案「水井」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「義賣」是「翰林版 4年級下學期 社會科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 社會科 第1課節錄）。「義賣」出自其他課，非「翰林版 4年級下學期 社會科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 社會科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "觀念"}, {"key": "B", "text": "早期"}, {"key": "C", "text": "林場"}, {"key": "D", "text": "盆地"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 社會科 第2課節錄）。正確答案「林場」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「山林」是「翰林版 4年級下學期 社會科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 社會科 第2課節錄）。「山林」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 社會科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "推動"}, {"key": "B", "text": "化學肥料"}, {"key": "C", "text": "部落"}, {"key": "D", "text": "早期"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 社會科 第3課節錄）。正確答案「化學肥料」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「部落」是「翰林版 4年級下學期 社會科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 社會科 第3課節錄）。「部落」出自其他課，非「翰林版 4年級下學期 社會科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 社會科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "門牌"}, {"key": "B", "text": "祭典"}, {"key": "C", "text": "原住民"}, {"key": "D", "text": "鹿港鎮"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 社會科 第4課節錄）。正確答案「鹿港鎮」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「木臼」是「翰林版 4年級下學期 社會科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 社會科 第4課節錄）。「木臼」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=5),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 社會科 第5課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "都市"}, {"key": "B", "text": "商圈"}, {"key": "C", "text": "原住民"}, {"key": "D", "text": "觀光"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 社會科 第5課節錄）。正確答案「商圈」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=5),
  'true_false',
  '「都市」是「翰林版 4年級下學期 社會科 第5課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 社會科 第5課節錄）。「都市」出自其他課，非「翰林版 4年級下學期 社會科 第5課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 5年級下學期 社會科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "疫苗"}, {"key": "B", "text": "齋戒"}, {"key": "C", "text": "海流"}, {"key": "D", "text": "身分證"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 社會科 第1課節錄）。正確答案「海流」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=1),
  'true_false',
  '「疫苗」是「南一版 5年級下學期 社會科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 社會科 第1課節錄）。「疫苗」出自其他課，非「南一版 5年級下學期 社會科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 5年級下學期 社會科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "轉型"}, {"key": "B", "text": "學堂"}, {"key": "C", "text": "灌溉"}, {"key": "D", "text": "殖民"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 社會科 第2課節錄）。正確答案「學堂」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=2),
  'true_false',
  '「電報」是「南一版 5年級下學期 社會科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 社會科 第2課節錄）。「電報」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 5年級下學期 社會科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "霧社事件"}, {"key": "B", "text": "台地"}, {"key": "C", "text": "考古"}, {"key": "D", "text": "核廢料"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 社會科 第3課節錄）。正確答案「核廢料」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=3),
  'true_false',
  '「台地」是「南一版 5年級下學期 社會科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 社會科 第3課節錄）。「台地」出自其他課，非「南一版 5年級下學期 社會科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 5年級下學期 社會科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "茶樹"}, {"key": "B", "text": "先民"}, {"key": "C", "text": "演變"}, {"key": "D", "text": "網路購物"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 社會科 第4課節錄）。正確答案「網路購物」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=4),
  'true_false',
  '「詐騙」是「南一版 5年級下學期 社會科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 社會科 第4課節錄）。「詐騙」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 社會科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "養殖"}, {"key": "B", "text": "身心"}, {"key": "C", "text": "祭典"}, {"key": "D", "text": "魯凱族"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 社會科 第1課節錄）。正確答案「身心」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「祭典」是「康軒版 5年級下學期 社會科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 社會科 第1課節錄）。「祭典」出自其他課，非「康軒版 5年級下學期 社會科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 社會科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "新生兒"}, {"key": "B", "text": "再生能源"}, {"key": "C", "text": "炮臺"}, {"key": "D", "text": "祭祀"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 社會科 第2課節錄）。正確答案「炮臺」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「傳教士」是「康軒版 5年級下學期 社會科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 社會科 第2課節錄）。「傳教士」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 社會科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "霧社事件"}, {"key": "B", "text": "牧場"}, {"key": "C", "text": "導盲磚"}, {"key": "D", "text": "記帳"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 社會科 第3課節錄）。正確答案「霧社事件」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「牧場」是「康軒版 5年級下學期 社會科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 社會科 第3課節錄）。「牧場」出自其他課，非「康軒版 5年級下學期 社會科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 社會科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "行政區"}, {"key": "B", "text": "社會發展"}, {"key": "C", "text": "空服員"}, {"key": "D", "text": "嘉南大圳"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 社會科 第4課節錄）。正確答案「嘉南大圳」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「樟腦」是「康軒版 5年級下學期 社會科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 社會科 第4課節錄）。「樟腦」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 社會科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "改良"}, {"key": "B", "text": "考古"}, {"key": "C", "text": "藥師"}, {"key": "D", "text": "殖民"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 社會科 第1課節錄）。正確答案「考古」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「改良」是「康軒版 5年級上學期 社會科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 社會科 第1課節錄）。「改良」出自其他課，非「康軒版 5年級上學期 社會科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 社會科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "保險"}, {"key": "B", "text": "舞獅"}, {"key": "C", "text": "紙鈔"}, {"key": "D", "text": "頭目"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 社會科 第2課節錄）。正確答案「頭目」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「遷移」是「康軒版 5年級上學期 社會科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 社會科 第2課節錄）。「遷移」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 社會科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "喚醒"}, {"key": "B", "text": "綠色消費"}, {"key": "C", "text": "逐步"}, {"key": "D", "text": "運輸"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 社會科 第3課節錄）。正確答案「逐步」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「綠色消費」是「康軒版 5年級上學期 社會科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 社會科 第3課節錄）。「綠色消費」出自其他課，非「康軒版 5年級上學期 社會科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 社會科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "將領"}, {"key": "B", "text": "轉型"}, {"key": "C", "text": "農業社會"}, {"key": "D", "text": "變遷"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 社會科 第4課節錄）。正確答案「將領」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「領土」是「康軒版 5年級上學期 社會科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 社會科 第4課節錄）。「領土」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 社會科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "開墾"}, {"key": "B", "text": "甲午戰爭"}, {"key": "C", "text": "文面"}, {"key": "D", "text": "油燈"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 社會科 第1課節錄）。正確答案「甲午戰爭」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「開墾」是「翰林版 5年級下學期 社會科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 社會科 第1課節錄）。「開墾」出自其他課，非「翰林版 5年級下學期 社會科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 社會科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "守望相助"}, {"key": "B", "text": "公共事務"}, {"key": "C", "text": "電報"}, {"key": "D", "text": "水井"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 社會科 第2課節錄）。正確答案「公共事務」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「戒嚴」是「翰林版 5年級下學期 社會科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 社會科 第2課節錄）。「戒嚴」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 社會科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "身分證"}, {"key": "B", "text": "水資源"}, {"key": "C", "text": "伊斯蘭教"}, {"key": "D", "text": "壯麗"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 社會科 第3課節錄）。正確答案「伊斯蘭教」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「壯麗」是「翰林版 5年級下學期 社會科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 社會科 第3課節錄）。「壯麗」出自其他課，非「翰林版 5年級下學期 社會科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 6年級下學期 社會科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "統一發票"}, {"key": "B", "text": "公共事務"}, {"key": "C", "text": "產銷"}, {"key": "D", "text": "佛教"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 社會科 第1課節錄）。正確答案「佛教」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=1),
  'true_false',
  '「統一發票」是「南一版 6年級下學期 社會科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 社會科 第1課節錄）。「統一發票」出自其他課，非「南一版 6年級下學期 社會科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 6年級下學期 社會科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "機能"}, {"key": "B", "text": "虛擬實境"}, {"key": "C", "text": "貝塚"}, {"key": "D", "text": "農業社會"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 社會科 第2課節錄）。正確答案「虛擬實境」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=2),
  'true_false',
  '「協定」是「南一版 6年級下學期 社會科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 社會科 第2課節錄）。「協定」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 6年級下學期 社會科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "壟斷"}, {"key": "B", "text": "全民健保"}, {"key": "C", "text": "礦產"}, {"key": "D", "text": "糖廠"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 社會科 第3課節錄）。正確答案「壟斷」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=3),
  'true_false',
  '「礦產」是「南一版 6年級下學期 社會科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 社會科 第3課節錄）。「礦產」出自其他課，非「南一版 6年級下學期 社會科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 6年級下學期 社會科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鄉村"}, {"key": "B", "text": "甲骨文"}, {"key": "C", "text": "人權"}, {"key": "D", "text": "檜木"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 社會科 第1課節錄）。正確答案「甲骨文」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「檜木」是「康軒版 6年級下學期 社會科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 社會科 第1課節錄）。「檜木」出自其他課，非「康軒版 6年級下學期 社會科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 6年級下學期 社會科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "蝗災"}, {"key": "B", "text": "鄉村"}, {"key": "C", "text": "二二八事件"}, {"key": "D", "text": "地熱"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 社會科 第2課節錄）。正確答案「蝗災」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「齋戒」是「康軒版 6年級下學期 社會科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 社會科 第2課節錄）。「齋戒」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 社會科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "就業服務"}, {"key": "B", "text": "線上購物"}, {"key": "C", "text": "紙鈔"}, {"key": "D", "text": "悲憤"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 社會科 第1課節錄）。正確答案「悲憤」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「紙鈔」是「康軒版 6年級上學期 社會科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 社會科 第1課節錄）。「紙鈔」出自其他課，非「康軒版 6年級上學期 社會科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 社會科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "砍伐"}, {"key": "B", "text": "零用錢"}, {"key": "C", "text": "巡禮"}, {"key": "D", "text": "觀念"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 社會科 第2課節錄）。正確答案「砍伐」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「壟斷」是「康軒版 6年級上學期 社會科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 社會科 第2課節錄）。「壟斷」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 社會科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "布袋戲"}, {"key": "B", "text": "風俗習慣"}, {"key": "C", "text": "人文"}, {"key": "D", "text": "頭目"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 社會科 第3課節錄）。正確答案「風俗習慣」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「人文」是「康軒版 6年級上學期 社會科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 社會科 第3課節錄）。「人文」出自其他課，非「康軒版 6年級上學期 社會科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 社會科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "都市"}, {"key": "B", "text": "絕種"}, {"key": "C", "text": "產銷"}, {"key": "D", "text": "舢舨"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 社會科 第4課節錄）。正確答案「都市」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「鄉村」是「康軒版 6年級上學期 社會科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 社會科 第4課節錄）。「鄉村」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 6年級下學期 社會科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "人權"}, {"key": "B", "text": "原住民"}, {"key": "C", "text": "全民健保"}, {"key": "D", "text": "學堂"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 社會科 第2課節錄）。正確答案「全民健保」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「就業服務」是「翰林版 6年級下學期 社會科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 社會科 第2課節錄）。「就業服務」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 6年級下學期 社會科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "核廢料"}, {"key": "B", "text": "生物科技"}, {"key": "C", "text": "外來種"}, {"key": "D", "text": "船舶"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 社會科 第3課節錄）。正確答案「外來種」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='social' and school_level_id=1) and grade=6 and semester='下' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「船舶」是「翰林版 6年級下學期 社會科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級下學期 社會科 第3課節錄）。「船舶」出自其他課，非「翰林版 6年級下學期 社會科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 3年級下學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "驅蟲劑"}, {"key": "B", "text": "根"}, {"key": "C", "text": "雌蕊"}, {"key": "D", "text": "綠色能源"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 自然科學科 第1課節錄）。正確答案「根」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=1),
  'true_false',
  '「驅蟲劑」是「南一版 3年級下學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 自然科學科 第1課節錄）。「驅蟲劑」出自其他課，非「南一版 3年級下學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 3年級下學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "地層下陷"}, {"key": "B", "text": "液態"}, {"key": "C", "text": "莖"}, {"key": "D", "text": "尾巴"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 自然科學科 第2課節錄）。正確答案「液態」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=2),
  'true_false',
  '「水蒸氣」是「南一版 3年級下學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 自然科學科 第2課節錄）。「水蒸氣」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 3年級下學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "完全變態"}, {"key": "B", "text": "覓食"}, {"key": "C", "text": "氣溫"}, {"key": "D", "text": "導電"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 自然科學科 第3課節錄）。正確答案「氣溫」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=3),
  'true_false',
  '「導電」是「南一版 3年級下學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 自然科學科 第3課節錄）。「導電」出自其他課，非「南一版 3年級下學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 3年級下學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "冷鋒"}, {"key": "B", "text": "遺骸"}, {"key": "C", "text": "冰糖"}, {"key": "D", "text": "雄蕊"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 自然科學科 第4課節錄）。正確答案「冰糖」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='南一' and lesson_number=4),
  'true_false',
  '「調味料」是「南一版 3年級下學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級下學期 自然科學科 第4課節錄）。「調味料」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 3年級上學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "太陽能"}, {"key": "B", "text": "種子"}, {"key": "C", "text": "花瓣"}, {"key": "D", "text": "連通管原理"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 自然科學科 第1課節錄）。正確答案「種子」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=1),
  'true_false',
  '「連通管原理」是「南一版 3年級上學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 自然科學科 第1課節錄）。「連通管原理」出自其他課，非「南一版 3年級上學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 3年級上學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "風力"}, {"key": "B", "text": "北斗七星"}, {"key": "C", "text": "流動"}, {"key": "D", "text": "地震"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 自然科學科 第2課節錄）。正確答案「流動」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=2),
  'true_false',
  '「傳動」是「南一版 3年級上學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 自然科學科 第2課節錄）。「傳動」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 3年級上學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "噪音"}, {"key": "B", "text": "翅膀"}, {"key": "C", "text": "毛細現象"}, {"key": "D", "text": "打氣筒"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 自然科學科 第3課節錄）。正確答案「翅膀」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=3),
  'true_false',
  '「打氣筒」是「南一版 3年級上學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 自然科學科 第3課節錄）。「打氣筒」出自其他課，非「南一版 3年級上學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 3年級上學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "線圈"}, {"key": "B", "text": "磁力"}, {"key": "C", "text": "中性"}, {"key": "D", "text": "能源"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 自然科學科 第4課節錄）。正確答案「磁力」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='南一' and lesson_number=4),
  'true_false',
  '「磁鐵」是「南一版 3年級上學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 3年級上學期 自然科學科 第4課節錄）。「磁鐵」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "點播"}, {"key": "B", "text": "板岩"}, {"key": "C", "text": "酸性"}, {"key": "D", "text": "縫隙"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 自然科學科 第1課節錄）。正確答案「點播」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「縫隙」是「康軒版 3年級下學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 自然科學科 第1課節錄）。「縫隙」出自其他課，非「康軒版 3年級下學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "水蒸氣"}, {"key": "B", "text": "雌蕊"}, {"key": "C", "text": "滯留鋒"}, {"key": "D", "text": "食鹽"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 自然科學科 第2課節錄）。正確答案「水蒸氣」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「蒸發」是「康軒版 3年級下學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 自然科學科 第2課節錄）。「蒸發」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 3年級下學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "野生動物"}, {"key": "B", "text": "綠色能源"}, {"key": "C", "text": "雌蕊"}, {"key": "D", "text": "天平"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 自然科學科 第3課節錄）。正確答案「野生動物」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「雌蕊」是「康軒版 3年級下學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級下學期 自然科學科 第3課節錄）。「雌蕊」出自其他課，非「康軒版 3年級下學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "滿月"}, {"key": "B", "text": "沖刷"}, {"key": "C", "text": "鬚根"}, {"key": "D", "text": "凝固"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 自然科學科 第1課節錄）。正確答案「鬚根」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「滿月」是「康軒版 3年級上學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 自然科學科 第1課節錄）。「滿月」出自其他課，非「康軒版 3年級上學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "月相"}, {"key": "B", "text": "器官"}, {"key": "C", "text": "鰭"}, {"key": "D", "text": "浮力"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 自然科學科 第2課節錄）。正確答案「浮力」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「風力」是「康軒版 3年級上學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 自然科學科 第2課節錄）。「風力」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "浮力"}, {"key": "B", "text": "流動"}, {"key": "C", "text": "土石流"}, {"key": "D", "text": "鏽"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 自然科學科 第3課節錄）。正確答案「流動」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「浮力」是「康軒版 3年級上學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 自然科學科 第3課節錄）。「浮力」出自其他課，非「康軒版 3年級上學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 3年級上學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "溶劑"}, {"key": "B", "text": "鰭"}, {"key": "C", "text": "鹼性"}, {"key": "D", "text": "播種"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 自然科學科 第4課節錄）。正確答案「鹼性」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「酸性」是「康軒版 3年級上學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 3年級上學期 自然科學科 第4課節錄）。「酸性」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "日照"}, {"key": "B", "text": "線圈"}, {"key": "C", "text": "太陽系"}, {"key": "D", "text": "物質"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 自然科學科 第1課節錄）。正確答案「日照」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「物質」是「翰林版 3年級下學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 自然科學科 第1課節錄）。「物質」出自其他課，非「翰林版 3年級下學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "滿月"}, {"key": "B", "text": "胚珠"}, {"key": "C", "text": "發電"}, {"key": "D", "text": "對流"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 自然科學科 第2課節錄）。正確答案「發電」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「節約」是「翰林版 3年級下學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 自然科學科 第2課節錄）。「節約」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "天氣預報"}, {"key": "B", "text": "軌跡"}, {"key": "C", "text": "壓縮"}, {"key": "D", "text": "磁性"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 自然科學科 第3課節錄）。正確答案「天氣預報」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「壓縮」是「翰林版 3年級下學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 自然科學科 第3課節錄）。「壓縮」出自其他課，非「翰林版 3年級下學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 3年級下學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "滿月"}, {"key": "B", "text": "虹吸現象"}, {"key": "C", "text": "若蟲"}, {"key": "D", "text": "晝夜"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 自然科學科 第4課節錄）。正確答案「若蟲」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='下' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「構造」是「翰林版 3年級下學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級下學期 自然科學科 第4課節錄）。「構造」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 3年級上學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鐵鏽"}, {"key": "B", "text": "雄蕊"}, {"key": "C", "text": "彈性限度"}, {"key": "D", "text": "木本"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 自然科學科 第1課節錄）。正確答案「木本」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「雄蕊」是「翰林版 3年級上學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 自然科學科 第1課節錄）。「雄蕊」出自其他課，非「翰林版 3年級上學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 3年級上學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鹼性"}, {"key": "B", "text": "莖"}, {"key": "C", "text": "葉脈"}, {"key": "D", "text": "石英"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 自然科學科 第2課節錄）。正確答案「葉脈」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「葉形」是「翰林版 3年級上學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 自然科學科 第2課節錄）。「葉形」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 3年級上學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "雌蕊"}, {"key": "B", "text": "傳播"}, {"key": "C", "text": "築巢"}, {"key": "D", "text": "中性"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 自然科學科 第3課節錄）。正確答案「雌蕊」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「築巢」是「翰林版 3年級上學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 自然科學科 第3課節錄）。「築巢」出自其他課，非「翰林版 3年級上學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 3年級上學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "木本"}, {"key": "B", "text": "脊椎"}, {"key": "C", "text": "線圈"}, {"key": "D", "text": "食鹽"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 自然科學科 第4課節錄）。正確答案「食鹽」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=3 and semester='上' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「放大鏡」是「翰林版 3年級上學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 3年級上學期 自然科學科 第4課節錄）。「放大鏡」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 4年級下學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "油土"}, {"key": "B", "text": "二分法"}, {"key": "C", "text": "水域"}, {"key": "D", "text": "晝夜"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 自然科學科 第1課節錄）。正確答案「油土」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=1),
  'true_false',
  '「二分法」是「南一版 4年級下學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 自然科學科 第1課節錄）。「二分法」出自其他課，非「南一版 4年級下學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 4年級下學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "等壓線"}, {"key": "B", "text": "彈簧"}, {"key": "C", "text": "觸角"}, {"key": "D", "text": "花萼"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 自然科學科 第2課節錄）。正確答案「觸角」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=2),
  'true_false',
  '「完全變態」是「南一版 4年級下學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 自然科學科 第2課節錄）。「完全變態」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 4年級下學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "方位"}, {"key": "B", "text": "竹節蟲"}, {"key": "C", "text": "連通管原理"}, {"key": "D", "text": "石蕊試紙"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 自然科學科 第3課節錄）。正確答案「連通管原理」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=3),
  'true_false',
  '「竹節蟲」是「南一版 4年級下學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 自然科學科 第3課節錄）。「竹節蟲」出自其他課，非「南一版 4年級下學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 4年級下學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "水蘊草"}, {"key": "B", "text": "防災"}, {"key": "C", "text": "雨量"}, {"key": "D", "text": "菜園"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 自然科學科 第4課節錄）。正確答案「防災」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='南一' and lesson_number=4),
  'true_false',
  '「地貌」是「南一版 4年級下學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級下學期 自然科學科 第4課節錄）。「地貌」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 4年級上學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "高度角"}, {"key": "B", "text": "節約"}, {"key": "C", "text": "降雨"}, {"key": "D", "text": "光害"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 自然科學科 第1課節錄）。正確答案「高度角」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=1),
  'true_false',
  '「節約」是「南一版 4年級上學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 自然科學科 第1課節錄）。「節約」出自其他課，非「南一版 4年級上學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 4年級上學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "雙氧水"}, {"key": "B", "text": "傳動"}, {"key": "C", "text": "冰晶"}, {"key": "D", "text": "沉水"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 自然科學科 第2課節錄）。正確答案「沉水」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=2),
  'true_false',
  '「水質」是「南一版 4年級上學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 自然科學科 第2課節錄）。「水質」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 4年級上學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "水土保持"}, {"key": "B", "text": "水溶液"}, {"key": "C", "text": "火力發電"}, {"key": "D", "text": "花粉"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 自然科學科 第3課節錄）。正確答案「火力發電」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=3),
  'true_false',
  '「花粉」是「南一版 4年級上學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 自然科學科 第3課節錄）。「花粉」出自其他課，非「南一版 4年級上學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 4年級上學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "脊椎"}, {"key": "B", "text": "電路"}, {"key": "C", "text": "支點"}, {"key": "D", "text": "水域"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 自然科學科 第4課節錄）。正確答案「電路」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='南一' and lesson_number=4),
  'true_false',
  '「通路」是「南一版 4年級上學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 4年級上學期 自然科學科 第4課節錄）。「通路」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "氣體"}, {"key": "B", "text": "北斗七星"}, {"key": "C", "text": "光害"}, {"key": "D", "text": "草本"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 自然科學科 第1課節錄）。正確答案「光害」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「草本」是「康軒版 4年級下學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 自然科學科 第1課節錄）。「草本」出自其他課，非「康軒版 4年級下學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "控制變因"}, {"key": "B", "text": "毛細現象"}, {"key": "C", "text": "拉力"}, {"key": "D", "text": "水力"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 自然科學科 第2課節錄）。正確答案「毛細現象」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「擴散」是「康軒版 4年級下學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 自然科學科 第2課節錄）。「擴散」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "望月"}, {"key": "B", "text": "傳導"}, {"key": "C", "text": "竹節蟲"}, {"key": "D", "text": "磁鐵"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 自然科學科 第3課節錄）。正確答案「竹節蟲」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「望月」是「康軒版 4年級下學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 自然科學科 第3課節錄）。「望月」出自其他課，非「康軒版 4年級下學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 4年級下學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "永續"}, {"key": "B", "text": "沙丘"}, {"key": "C", "text": "水質"}, {"key": "D", "text": "粒子"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 自然科學科 第4課節錄）。正確答案「永續」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「土石流」是「康軒版 4年級下學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級下學期 自然科學科 第4課節錄）。「土石流」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "熱能"}, {"key": "B", "text": "沙丘"}, {"key": "C", "text": "雨量"}, {"key": "D", "text": "春分"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 自然科學科 第1課節錄）。正確答案「沙丘」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「春分」是「康軒版 4年級上學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 自然科學科 第1課節錄）。「春分」出自其他課，非「康軒版 4年級上學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "水蒸氣"}, {"key": "B", "text": "石英"}, {"key": "C", "text": "水域"}, {"key": "D", "text": "大氣層"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 自然科學科 第2課節錄）。正確答案「水域」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「水流」是「康軒版 4年級上學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 自然科學科 第2課節錄）。「水流」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "二氧化碳"}, {"key": "B", "text": "紅尾伯勞"}, {"key": "C", "text": "振動"}, {"key": "D", "text": "風力"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 自然科學科 第3課節錄）。正確答案「振動」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「風力」是「康軒版 4年級上學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 自然科學科 第3課節錄）。「風力」出自其他課，非「康軒版 4年級上學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 4年級上學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "凝固"}, {"key": "B", "text": "正極"}, {"key": "C", "text": "磁鐵"}, {"key": "D", "text": "觸角"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 自然科學科 第4課節錄）。正確答案「正極」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「觸電」是「康軒版 4年級上學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 4年級上學期 自然科學科 第4課節錄）。「觸電」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "熱脹冷縮"}, {"key": "B", "text": "導線"}, {"key": "C", "text": "導電"}, {"key": "D", "text": "水力"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 自然科學科 第1課節錄）。正確答案「水力」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「導線」是「翰林版 4年級下學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 自然科學科 第1課節錄）。「導線」出自其他課，非「翰林版 4年級下學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "溶劑"}, {"key": "B", "text": "引水"}, {"key": "C", "text": "口器"}, {"key": "D", "text": "莖"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 自然科學科 第2課節錄）。正確答案「引水」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「虹吸現象」是「翰林版 4年級下學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 自然科學科 第2課節錄）。「虹吸現象」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "地震"}, {"key": "B", "text": "氣象"}, {"key": "C", "text": "傳導"}, {"key": "D", "text": "石灰岩"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 自然科學科 第3課節錄）。正確答案「地震」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「氣象」是「翰林版 4年級下學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 自然科學科 第3課節錄）。「氣象」出自其他課，非「翰林版 4年級下學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 4年級下學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "雌蕊"}, {"key": "B", "text": "二氧化碳"}, {"key": "C", "text": "電能"}, {"key": "D", "text": "石灰岩"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 自然科學科 第4課節錄）。正確答案「電能」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='下' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「再生能源」是「翰林版 4年級下學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級下學期 自然科學科 第4課節錄）。「再生能源」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 4年級上學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "反射"}, {"key": "B", "text": "果實"}, {"key": "C", "text": "殘月"}, {"key": "D", "text": "尾巴"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 自然科學科 第1課節錄）。正確答案「殘月」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「尾巴」是「翰林版 4年級上學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 自然科學科 第1課節錄）。「尾巴」出自其他課，非「翰林版 4年級上學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 4年級上學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "睡蓮"}, {"key": "B", "text": "群集"}, {"key": "C", "text": "生態系"}, {"key": "D", "text": "構造"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 自然科學科 第2課節錄）。正確答案「睡蓮」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「浮葉植物」是「翰林版 4年級上學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 自然科學科 第2課節錄）。「浮葉植物」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 4年級上學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "彈性疲乏"}, {"key": "B", "text": "固態"}, {"key": "C", "text": "築巢"}, {"key": "D", "text": "氬氣"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 自然科學科 第3課節錄）。正確答案「固態」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「彈性疲乏」是「翰林版 4年級上學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 自然科學科 第3課節錄）。「彈性疲乏」出自其他課，非「翰林版 4年級上學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 4年級上學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "蛹"}, {"key": "B", "text": "引水"}, {"key": "C", "text": "振動"}, {"key": "D", "text": "燈絲"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 自然科學科 第4課節錄）。正確答案「振動」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=4 and semester='上' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「物質」是「翰林版 4年級上學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 4年級上學期 自然科學科 第4課節錄）。「物質」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 5年級下學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "眉月"}, {"key": "B", "text": "傳動"}, {"key": "C", "text": "成蟲"}, {"key": "D", "text": "太陽系"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 自然科學科 第1課節錄）。正確答案「太陽系」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=1),
  'true_false',
  '「成蟲」是「南一版 5年級下學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 自然科學科 第1課節錄）。「成蟲」出自其他課，非「南一版 5年級下學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 5年級下學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "能量"}, {"key": "B", "text": "生態系"}, {"key": "C", "text": "氮"}, {"key": "D", "text": "酸性"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 自然科學科 第2課節錄）。正確答案「酸性」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=2),
  'true_false',
  '「鏽」是「南一版 5年級下學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 自然科學科 第2課節錄）。「鏽」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 5年級下學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "北斗七星"}, {"key": "B", "text": "葉形"}, {"key": "C", "text": "覓食"}, {"key": "D", "text": "液態"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 自然科學科 第3課節錄）。正確答案「覓食」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=3),
  'true_false',
  '「葉形」是「南一版 5年級下學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 自然科學科 第3課節錄）。「葉形」出自其他課，非「南一版 5年級下學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 5年級下學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "噪音管制法"}, {"key": "B", "text": "絕種"}, {"key": "C", "text": "雄蕊"}, {"key": "D", "text": "雨量"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 自然科學科 第4課節錄）。正確答案「噪音管制法」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='南一' and lesson_number=4),
  'true_false',
  '「噪音」是「南一版 5年級下學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級下學期 自然科學科 第4課節錄）。「噪音」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 5年級上學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "春分"}, {"key": "B", "text": "燃點"}, {"key": "C", "text": "二分法"}, {"key": "D", "text": "葉脈"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 自然科學科 第1課節錄）。正確答案「春分」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=1),
  'true_false',
  '「葉脈」是「南一版 5年級上學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 自然科學科 第1課節錄）。「葉脈」出自其他課，非「南一版 5年級上學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 5年級上學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "攀緣莖"}, {"key": "B", "text": "觸電"}, {"key": "C", "text": "降雨"}, {"key": "D", "text": "鹼性"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 自然科學科 第2課節錄）。正確答案「攀緣莖」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=2),
  'true_false',
  '「光合作用」是「南一版 5年級上學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 自然科學科 第2課節錄）。「光合作用」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 5年級上學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "溶質"}, {"key": "B", "text": "星座"}, {"key": "C", "text": "觸電"}, {"key": "D", "text": "毛細現象"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 自然科學科 第3課節錄）。正確答案「溶質」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=3),
  'true_false',
  '「毛細現象」是「南一版 5年級上學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 自然科學科 第3課節錄）。「毛細現象」出自其他課，非「南一版 5年級上學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 5年級上學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "摩擦力"}, {"key": "B", "text": "花瓣"}, {"key": "C", "text": "水溶液"}, {"key": "D", "text": "降雨"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 自然科學科 第4課節錄）。正確答案「摩擦力」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='南一' and lesson_number=4),
  'true_false',
  '「砝碼」是「南一版 5年級上學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 5年級上學期 自然科學科 第4課節錄）。「砝碼」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "尾巴"}, {"key": "B", "text": "拉力"}, {"key": "C", "text": "磁力"}, {"key": "D", "text": "雙氧水"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 自然科學科 第1課節錄）。正確答案「拉力」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「磁力」是「康軒版 5年級下學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 自然科學科 第1課節錄）。「磁力」出自其他課，非「康軒版 5年級下學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "電磁鐵"}, {"key": "B", "text": "磁鐵"}, {"key": "C", "text": "高度角"}, {"key": "D", "text": "下游"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 自然科學科 第2課節錄）。正確答案「下游」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「石墨」是「康軒版 5年級下學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 自然科學科 第2課節錄）。「石墨」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "落地生根"}, {"key": "B", "text": "光害"}, {"key": "C", "text": "骨骼"}, {"key": "D", "text": "光能"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 自然科學科 第3課節錄）。正確答案「落地生根」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「光能」是「康軒版 5年級下學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 自然科學科 第3課節錄）。「光能」出自其他課，非「康軒版 5年級下學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 5年級下學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "連通管原理"}, {"key": "B", "text": "聚光"}, {"key": "C", "text": "四肢"}, {"key": "D", "text": "散熱"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 自然科學科 第4課節錄）。正確答案「散熱」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「保溫」是「康軒版 5年級下學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級下學期 自然科學科 第4課節錄）。「保溫」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "覓食"}, {"key": "B", "text": "紅尾伯勞"}, {"key": "C", "text": "氣態"}, {"key": "D", "text": "指北針"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 自然科學科 第1課節錄）。正確答案「紅尾伯勞」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「氣態」是「康軒版 5年級上學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 自然科學科 第1課節錄）。「氣態」出自其他課，非「康軒版 5年級上學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "再生能源"}, {"key": "B", "text": "砝碼"}, {"key": "C", "text": "鐵鏽"}, {"key": "D", "text": "隔音牆"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 自然科學科 第2課節錄）。正確答案「隔音牆」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「聚光」是「康軒版 5年級上學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 自然科學科 第2課節錄）。「聚光」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "北斗七星"}, {"key": "B", "text": "方解石"}, {"key": "C", "text": "對流"}, {"key": "D", "text": "磁場"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 自然科學科 第3課節錄）。正確答案「北斗七星」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「方解石」是「康軒版 5年級上學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 自然科學科 第3課節錄）。「方解石」出自其他課，非「康軒版 5年級上學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 5年級上學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "噪音管制法"}, {"key": "B", "text": "鹼性"}, {"key": "C", "text": "風力"}, {"key": "D", "text": "合金"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 自然科學科 第4課節錄）。正確答案「合金」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「電鍍」是「康軒版 5年級上學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 5年級上學期 自然科學科 第4課節錄）。「電鍍」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "星座"}, {"key": "B", "text": "母體"}, {"key": "C", "text": "反光"}, {"key": "D", "text": "液態"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 自然科學科 第1課節錄）。正確答案「星座」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「液態」是「翰林版 5年級下學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 自然科學科 第1課節錄）。「液態」出自其他課，非「翰林版 5年級下學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "滿月"}, {"key": "B", "text": "導電"}, {"key": "C", "text": "肌肉"}, {"key": "D", "text": "燃點"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 自然科學科 第2課節錄）。正確答案「燃點」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「氧氣」是「翰林版 5年級下學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 自然科學科 第2課節錄）。「氧氣」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "對流"}, {"key": "B", "text": "真空"}, {"key": "C", "text": "分貝"}, {"key": "D", "text": "生產者"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 自然科學科 第3課節錄）。正確答案「真空」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「生產者」是「翰林版 5年級下學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 自然科學科 第3課節錄）。「生產者」出自其他課，非「翰林版 5年級下學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 5年級下學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "口器"}, {"key": "B", "text": "地震"}, {"key": "C", "text": "磁場"}, {"key": "D", "text": "翅膀"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 自然科學科 第4課節錄）。正確答案「口器」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='下' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「覓食」是「翰林版 5年級下學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級下學期 自然科學科 第4課節錄）。「覓食」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 5年級上學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "凝固"}, {"key": "B", "text": "北斗七星"}, {"key": "C", "text": "綠色能源"}, {"key": "D", "text": "滿月"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 自然科學科 第1課節錄）。正確答案「綠色能源」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「滿月」是「翰林版 5年級上學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 自然科學科 第1課節錄）。「滿月」出自其他課，非「翰林版 5年級上學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 5年級上學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "子房"}, {"key": "B", "text": "磁力"}, {"key": "C", "text": "次級消費者"}, {"key": "D", "text": "調味料"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 自然科學科 第2課節錄）。正確答案「子房」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「授粉」是「翰林版 5年級上學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 自然科學科 第2課節錄）。「授粉」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 5年級上學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "鹼性"}, {"key": "B", "text": "連通管原理"}, {"key": "C", "text": "散熱"}, {"key": "D", "text": "熱帶氣旋"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 自然科學科 第3課節錄）。正確答案「鹼性」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「熱帶氣旋」是「翰林版 5年級上學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 自然科學科 第3課節錄）。「熱帶氣旋」出自其他課，非「翰林版 5年級上學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 5年級上學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "摩擦力"}, {"key": "B", "text": "生態系"}, {"key": "C", "text": "驅蟲劑"}, {"key": "D", "text": "二氧化碳"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 自然科學科 第4課節錄）。正確答案「摩擦力」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=5 and semester='上' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「彈性限度」是「翰林版 5年級上學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 5年級上學期 自然科學科 第4課節錄）。「彈性限度」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 6年級下學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "支點"}, {"key": "B", "text": "串聯"}, {"key": "C", "text": "爬牆虎"}, {"key": "D", "text": "尖嘴鉗"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 自然科學科 第1課節錄）。正確答案「支點」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=1),
  'true_false',
  '「爬牆虎」是「南一版 6年級下學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 自然科學科 第1課節錄）。「爬牆虎」出自其他課，非「南一版 6年級下學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 6年級下學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "生態系"}, {"key": "B", "text": "石蓴"}, {"key": "C", "text": "尖嘴鉗"}, {"key": "D", "text": "引水"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 自然科學科 第2課節錄）。正確答案「生態系」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=2),
  'true_false',
  '「分解者」是「南一版 6年級下學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 自然科學科 第2課節錄）。「分解者」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 6年級下學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "水力發電"}, {"key": "B", "text": "漂浮"}, {"key": "C", "text": "放大鏡"}, {"key": "D", "text": "水蘊草"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 自然科學科 第3課節錄）。正確答案「水力發電」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='下' and publisher='南一' and lesson_number=3),
  'true_false',
  '「放大鏡」是「南一版 6年級下學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級下學期 自然科學科 第3課節錄）。「放大鏡」出自其他課，非「南一版 6年級下學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=1),
  'single_choice',
  '下列何者是「南一版 6年級上學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "冰雹"}, {"key": "B", "text": "鏽"}, {"key": "C", "text": "導電"}, {"key": "D", "text": "硫磺"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 自然科學科 第1課節錄）。正確答案「冰雹」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=1),
  'true_false',
  '「硫磺」是「南一版 6年級上學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 自然科學科 第1課節錄）。「硫磺」出自其他課，非「南一版 6年級上學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=2),
  'single_choice',
  '下列何者是「南一版 6年級上學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "葉緣"}, {"key": "B", "text": "二氧化碳"}, {"key": "C", "text": "熱脹冷縮"}, {"key": "D", "text": "放大鏡"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 自然科學科 第2課節錄）。正確答案「熱脹冷縮」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=2),
  'true_false',
  '「傳導」是「南一版 6年級上學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 自然科學科 第2課節錄）。「傳導」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=3),
  'single_choice',
  '下列何者是「南一版 6年級上學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "眉月"}, {"key": "B", "text": "槓桿"}, {"key": "C", "text": "活塞"}, {"key": "D", "text": "石灰岩"}]'::jsonb,
  'D',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 自然科學科 第3課節錄）。正確答案「石灰岩」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=3),
  'true_false',
  '「槓桿」是「南一版 6年級上學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 自然科學科 第3課節錄）。「槓桿」出自其他課，非「南一版 6年級上學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=4),
  'single_choice',
  '下列何者是「南一版 6年級上學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "初級消費者"}, {"key": "B", "text": "電磁波"}, {"key": "C", "text": "凝固"}, {"key": "D", "text": "沖刷"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 自然科學科 第4課節錄）。正確答案「電磁波」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='南一' and lesson_number=4),
  'true_false',
  '「線圈」是「南一版 6年級上學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（南一版 6年級上學期 自然科學科 第4課節錄）。「線圈」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 6年級下學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "支點"}, {"key": "B", "text": "作用點"}, {"key": "C", "text": "洪水"}, {"key": "D", "text": "溶劑"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 自然科學科 第1課節錄）。正確答案「支點」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「溶劑」是「康軒版 6年級下學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 自然科學科 第1課節錄）。「溶劑」出自其他課，非「康軒版 6年級下學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 6年級下學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "隔音牆"}, {"key": "B", "text": "反射"}, {"key": "C", "text": "風力發電"}, {"key": "D", "text": "等壓線"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 自然科學科 第2課節錄）。正確答案「風力發電」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「能量」是「康軒版 6年級下學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 自然科學科 第2課節錄）。「能量」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 6年級下學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "日照"}, {"key": "B", "text": "地磁"}, {"key": "C", "text": "石蓴"}, {"key": "D", "text": "完全變態"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 自然科學科 第3課節錄）。正確答案「石蓴」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='下' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「完全變態」是「康軒版 6年級下學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級下學期 自然科學科 第3課節錄）。「完全變態」出自其他課，非「康軒版 6年級下學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=1),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "雄蕊"}, {"key": "B", "text": "點播"}, {"key": "C", "text": "等壓線"}, {"key": "D", "text": "能源"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 自然科學科 第1課節錄）。正確答案「等壓線」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=1),
  'true_false',
  '「點播」是「康軒版 6年級上學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 自然科學科 第1課節錄）。「點播」出自其他課，非「康軒版 6年級上學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=2),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "熱輻射"}, {"key": "B", "text": "水溶液"}, {"key": "C", "text": "沙丘"}, {"key": "D", "text": "構造"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 自然科學科 第2課節錄）。正確答案「水溶液」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=2),
  'true_false',
  '「石蕊試紙」是「康軒版 6年級上學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 自然科學科 第2課節錄）。「石蕊試紙」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=3),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "電鍍"}, {"key": "B", "text": "空氣汙染"}, {"key": "C", "text": "二分法"}, {"key": "D", "text": "水蘊草"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 自然科學科 第3課節錄）。正確答案「二分法」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=3),
  'true_false',
  '「電鍍」是「康軒版 6年級上學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 自然科學科 第3課節錄）。「電鍍」出自其他課，非「康軒版 6年級上學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=4),
  'single_choice',
  '下列何者是「康軒版 6年級上學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "指北針"}, {"key": "B", "text": "礫石"}, {"key": "C", "text": "能源"}, {"key": "D", "text": "鹼性"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 自然科學科 第4課節錄）。正確答案「指北針」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='康軒' and lesson_number=4),
  'true_false',
  '「磁性」是「康軒版 6年級上學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（康軒版 6年級上學期 自然科學科 第4課節錄）。「磁性」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=1),
  'single_choice',
  '下列何者是「翰林版 6年級上學期 自然科學科 第1課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "節約"}, {"key": "B", "text": "縫隙"}, {"key": "C", "text": "粒子"}, {"key": "D", "text": "砝碼"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 自然科學科 第1課節錄）。正確答案「粒子」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=1),
  'true_false',
  '「縫隙」是「翰林版 6年級上學期 自然科學科 第1課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 自然科學科 第1課節錄）。「縫隙」出自其他課，非「翰林版 6年級上學期 自然科學科 第1課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=2),
  'single_choice',
  '下列何者是「翰林版 6年級上學期 自然科學科 第2課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "能源"}, {"key": "B", "text": "彈力"}, {"key": "C", "text": "地下水"}, {"key": "D", "text": "夏至"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 自然科學科 第2課節錄）。正確答案「地下水」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=2),
  'true_false',
  '「冷氣團」是「翰林版 6年級上學期 自然科學科 第2課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 自然科學科 第2課節錄）。「冷氣團」出自該課詞彙節錄清單，故為正確。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=3),
  'single_choice',
  '下列何者是「翰林版 6年級上學期 自然科學科 第3課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "凝結"}, {"key": "B", "text": "板岩"}, {"key": "C", "text": "軀幹"}, {"key": "D", "text": "動能"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 自然科學科 第3課節錄）。正確答案「板岩」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=3),
  'true_false',
  '「動能」是「翰林版 6年級上學期 自然科學科 第3課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'B',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 自然科學科 第3課節錄）。「動能」出自其他課，非「翰林版 6年級上學期 自然科學科 第3課」節錄清單內的字詞，故為錯誤。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=4),
  'single_choice',
  '下列何者是「翰林版 6年級上學期 自然科學科 第4課」列出的生字／詞語之一？',
  '[{"key": "A", "text": "彈性限度"}, {"key": "B", "text": "擴散"}, {"key": "C", "text": "指北針"}, {"key": "D", "text": "種子"}]'::jsonb,
  'C',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 自然科學科 第4課節錄）。正確答案「指北針」出自該課詞彙節錄清單。'
);
insert into questions (curriculum_id, question_type, question_text, options, correct_option, explanation) values (
  (select id from curriculum where subject_id=(select id from subjects where code='science' and school_level_id=1) and grade=6 and semester='上' and publisher='翰林' and lesson_number=4),
  'true_false',
  '「電磁鐵」是「翰林版 6年級上學期 自然科學科 第4課」列出的生字／詞語之一。',
  '[{"key": "A", "text": "正確"}, {"key": "B", "text": "錯誤"}]'::jsonb,
  'A',
  '資料來源：教育部教育百科生字詞彙表（翰林版 6年級上學期 自然科學科 第4課節錄）。「電磁鐵」出自該課詞彙節錄清單，故為正確。'
);
