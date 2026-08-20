// 打地鼠 純邏輯回歸測試
//
// 這款遊戲的核心邏輯是「難度階梯」跟「評分分級」：分數達標時要正確切換到對應難度級距
// （地鼠停留時間變短、出現變密集），且不能跳級或退級判斷錯誤。多語言重構把整段搬到
// shared/whack-a-mole.js，這裡驗證這兩組純函式沒有被改到。
const fs = require('fs'), path = require('path'), vm = require('vm');
const code = fs.readFileSync(path.join(__dirname, '..', 'shared', 'whack-a-mole.js'), 'utf8');
const ctx = { console, Math, Array, Object, String, Number, Infinity, globalThis: null };
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(code + `
globalThis.__exp = { wamRatingIndex, wamComputeRating, wamRandBetween, wamLevelIndexForScore, gwhackamoleT, WAM_CONFIG };`, ctx);
const X = ctx.__exp, C = X.WAM_CONFIG;

let pass = 0, fail = 0;
const ok = (n, c, d) => { if (c) pass++; else { fail++; console.log('  ✗ ' + n + (d ? ' — ' + d : '')); } };

// ── 難度階梯：依分數找出正確的難度級距索引 ──
(function () {
  const levels = C.difficultyLevels;
  ok('分數0 → 第0級（初始難度）', X.wamLevelIndexForScore(0, levels) === 0);
  ok('分數9 → 仍是第0級（未達第1級門檻10）', X.wamLevelIndexForScore(9, levels) === 0);
  ok('分數10 → 第1級', X.wamLevelIndexForScore(10, levels) === 1);
  ok('分數19 → 仍是第1級', X.wamLevelIndexForScore(19, levels) === 1);
  ok('分數20 → 第2級', X.wamLevelIndexForScore(20, levels) === 2);
  ok('分數32 → 第3級', X.wamLevelIndexForScore(32, levels) === 3);
  ok('分數46 → 第4級（最高難度）', X.wamLevelIndexForScore(46, levels) === 4);
  ok('分數9999 → 封頂在最高難度（不會越界）', X.wamLevelIndexForScore(9999, levels) === levels.length - 1);
  let mono = true, prev = -1;
  for (let s = 0; s <= 100; s++) {
    const i = X.wamLevelIndexForScore(s, levels);
    if (i < prev) mono = false;
    prev = i;
  }
  ok('難度級距隨分數單調不遞減', mono);
})();

// ── 難度曲線本身：等級越高，地鼠停留時間應越短、出現越密集、同時出現數越多 ──
(function () {
  const levels = C.difficultyLevels;
  let stayShrinks = true, spawnTightens = true, activeGrows = true;
  for (let i = 1; i < levels.length; i++) {
    if (!(levels[i].moleUpMsMax <= levels[i - 1].moleUpMsMax)) stayShrinks = false;
    if (!(levels[i].spawnIntervalMsMax <= levels[i - 1].spawnIntervalMsMax)) spawnTightens = false;
    if (!(levels[i].maxActiveMoles >= levels[i - 1].maxActiveMoles)) activeGrows = false;
  }
  ok('等級越高地鼠停留時間上限越短（或持平）', stayShrinks);
  ok('等級越高出現間隔上限越短（或持平，出現更密集）', spawnTightens);
  ok('等級越高同時出現地鼠數上限越多（或持平）', activeGrows);
  ok('難度級距是依scoreThreshold遞增排序', levels.every((l, i) => i === 0 || l.scoreThreshold >= levels[i - 1].scoreThreshold));
})();

// ── randBetween 範圍正確性 ──
(function () {
  let allInRange = true;
  for (let i = 0; i < 500; i++) {
    const v = X.wamRandBetween(100, 200);
    if (v < 100 || v > 200) allInRange = false;
  }
  ok('wamRandBetween 500次抽樣都落在[min,max]範圍內', allInRange);
  ok('min等於max時回傳固定值', X.wamRandBetween(50, 50) === 50);
})();

// ── 評分分級：門檻共5級，索引正確 ──
ok('評分門檻共5級', C.ratingThresholds.length === 5);
ok('0分 → 第0級', X.wamRatingIndex(0) === 0);
ok('10分邊界含 → 第0級', X.wamRatingIndex(10) === 0);
ok('11分 → 第1級', X.wamRatingIndex(11) === 1);
ok('18分邊界含 → 第1級', X.wamRatingIndex(18) === 1);
ok('26分邊界含 → 第2級', X.wamRatingIndex(26) === 2);
ok('34分邊界含 → 第3級', X.wamRatingIndex(34) === 3);
ok('9999分 → 第4級（最高，封頂）', X.wamRatingIndex(9999) === 4);
(function () {
  let mono = true, prev = -1;
  for (let s = 0; s <= 100; s++) {
    const i = X.wamRatingIndex(s);
    if (i < prev) mono = false;
    prev = i;
  }
  ok('評分級數隨分數單調不遞減', mono);
})();

// ── i18n ──
ctx.window = { GAME_I18N: { ratings: ['A', 'B', 'C', 'D', 'E'] } };
ok('依分數取對應評語文字', X.wamComputeRating(0) === 'A' && X.wamComputeRating(9999) === 'E');
ok('缺key回傳空字串不拋錯', X.gwhackamoleT('__nope__') === '');
ctx.window = {};
ok('字典不存在時評語不拋錯', X.wamComputeRating(0) === '');

// ── 共用檔不得殘留硬寫死文字 ──
(function () {
  const stripped = code.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/[^\n]*/g, '');
  const cjk = stripped.match(/[一-鿿぀-ヿ가-힯]/g);
  ok('共用邏輯檔（排除註解）不含中日韓文字', cjk === null,
     cjk ? [...new Set(cjk)].join('').slice(0, 40) : '');
})();

console.log(`\n打地鼠 純邏輯回歸測試：${pass} 通過, ${fail} 失敗`);
process.exit(fail ? 1 : 0);
