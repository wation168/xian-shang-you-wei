// 數字炸彈（終極密碼猜數字） 純邏輯回歸測試
//
// 核心邏輯有三塊：① 猜測次數上限是用「二分搜尋」反推的最少次數＋2次緩衝，這個公平性
// （只要每次都猜正中間就一定猜得到）是這款遊戲最重要的正確性保證；② judgeGuess/narrowRange
// 的縮小範圍邏輯必須正確，否則範圍會越縮越大或漏掉答案；③ 分數/評語門檻換算。
// 多語言重構把整段搬到 shared/number-bomb.js，這裡驗證這些純函式沒有被改壞。
const fs = require('fs'), path = require('path'), vm = require('vm');
const code = fs.readFileSync(path.join(__dirname, '..', 'shared', 'number-bomb.js'), 'utf8');
const ctx = { console, Math, Array, Object, String, Number, Infinity, globalThis: null };
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(code + `
globalThis.__exp = { minGuessesForRange, guessesAllowedForRange, computeRoundConfig, generateSecret,
  judgeGuess, narrowRange, isValidGuess, computeRoundScore, computeFusePercent, nbRatingIndex,
  nbComputeRating, nextDuelPlayer, gnumberbombT, NB_CONFIG };`, ctx);
const X = ctx.__exp, C = X.NB_CONFIG;

let pass = 0, fail = 0;
const ok = (n, c, d) => { if (c) pass++; else { fail++; console.log('  ✗ ' + n + (d ? ' — ' + d : '')); } };

// ── minGuessesForRange：二分搜尋所需的最少次數 ──
ok('範圍1(cap=1>=1，0次) minGuessesForRange(1)===0', X.minGuessesForRange(1) === 0);
ok('範圍2 → 1次可定位', X.minGuessesForRange(2) === 1);
ok('範圍50 → 6次（2^6=64>=50，2^5=32<50）', X.minGuessesForRange(50) === 6);
ok('範圍100 → 7次（2^7=128>=100）', X.minGuessesForRange(100) === 7);
ok('範圍1000 → 10次（2^10=1024>=1000，2^9=512<1000）', X.minGuessesForRange(1000) === 10);
(function () {
  // 次數必須隨範圍單調不遞減（範圍越大所需次數不會變少）
  let mono = true, prev = -1;
  for (let r = 1; r <= 1200; r += 7) {
    const g = X.minGuessesForRange(r);
    if (g < prev) mono = false;
    prev = g;
  }
  ok('minGuessesForRange隨範圍單調不遞減', mono);
})();

// ── guessesAllowedForRange：最少次數 + 緩衝 ──
ok('guessesAllowedForRange = minGuesses + buffer(2)', X.guessesAllowedForRange(50) === X.minGuessesForRange(50) + C.guessBuffer);

// ── computeRoundConfig：關卡數→範圍表，超過表長時封頂在最後一個範圍 ──
ok('第1關範圍=50', X.computeRoundConfig(1).range === 50);
ok('第2關範圍=100', X.computeRoundConfig(2).range === 100);
ok('第3關範圍=200', X.computeRoundConfig(3).range === 200);
ok('第4關範圍=500', X.computeRoundConfig(4).range === 500);
ok('第5關範圍=1000', X.computeRoundConfig(5).range === 1000);
ok('第6關封頂仍是1000', X.computeRoundConfig(6).range === 1000);
ok('第99關封頂仍是1000', X.computeRoundConfig(99).range === 1000);
ok('roundInfo包含正確的guessesAllowed', X.computeRoundConfig(1).guessesAllowed === X.guessesAllowedForRange(50));

// ── generateSecret：產生的秘密數字必須落在範圍內 ──
(function () {
  let allInRange = true;
  for (let t = 0; t < 500; t++) {
    const s = X.generateSecret(1, 50);
    if (s < 1 || s > 50 || !Number.isInteger(s)) allInRange = false;
  }
  ok('generateSecret 500次抽樣都落在[1,50]範圍內且為整數', allInRange);
})();

// ── judgeGuess：核心比對邏輯 ──
ok('猜中回傳hit', X.judgeGuess(42, 42) === 'hit');
ok('猜太小回傳higher（意思是答案比猜測大，要往上猜）', X.judgeGuess(42, 10) === 'higher');
ok('猜太大回傳lower（意思是答案比猜測小，要往下猜）', X.judgeGuess(42, 90) === 'lower');

// ── narrowRange：縮小範圍不能有誤，且絕不能把答案排除在外 ──
(function () {
  const r1 = X.narrowRange(1, 100, 50, 'higher'); // 答案比50大
  ok('higher結果：新範圍下界變成guess+1，上界不變', r1.min === 51 && r1.max === 100);
  const r2 = X.narrowRange(1, 100, 50, 'lower'); // 答案比50小
  ok('lower結果：新範圍上界變成guess-1，下界不變', r2.min === 1 && r2.max === 49);
  const r3 = X.narrowRange(1, 100, 50, 'hit');
  ok('hit結果：範圍收斂成單一數字', r3.min === 50 && r3.max === 50);
})();
(function () {
  // 用二分搜尋策略模擬完整猜測流程，驗證narrowRange絕不會不小心把真正的答案排除在新範圍外
  let allSafe = true;
  for (let trial = 0; trial < 200; trial++) {
    let min = 1, max = 1000;
    const secret = X.generateSecret(min, max);
    let guesses = 0;
    while (min < max && guesses < 20) {
      const guess = Math.floor((min + max) / 2);
      const result = X.judgeGuess(secret, guess);
      if (result === 'hit') { min = guess; max = guess; break; }
      const n = X.narrowRange(min, max, guess, result);
      if (secret < n.min || secret > n.max) { allSafe = false; break; }
      min = n.min; max = n.max;
      guesses++;
    }
    if (min !== max || min !== secret) allSafe = false;
  }
  ok('200次二分搜尋模擬，narrowRange從未把秘密數字排除在新範圍外，且最終都能收斂到正確答案', allSafe);
})();

// ── isValidGuess ──
ok('範圍內整數合法', X.isValidGuess(50, 1, 100) === true);
ok('範圍外數字不合法', X.isValidGuess(101, 1, 100) === false);
ok('非整數不合法', X.isValidGuess(50.5, 1, 100) === false);
ok('NaN不合法', X.isValidGuess(NaN, 1, 100) === false);
ok('邊界值(min/max本身)合法', X.isValidGuess(1, 1, 100) === true && X.isValidGuess(100, 1, 100) === true);

// ── computeRoundScore：範圍越大基礎分越高，省下的次數給獎勵分 ──
(function () {
  const allowed = X.guessesAllowedForRange(1000);
  const s1 = X.computeRoundScore(1000, allowed, allowed); // 剛好用完，無效率獎勵
  const s2 = X.computeRoundScore(1000, 1, allowed); // 只用1次，效率獎勵拉滿
  ok('用越少次數分數越高（效率獎勵生效）', s2 > s1);
  const base1000 = X.computeRoundScore(1000, allowed, allowed);
  const base50 = X.computeRoundScore(50, X.guessesAllowedForRange(50), X.guessesAllowedForRange(50));
  ok('範圍越大基礎分越高', base1000 > base50);
})();

// ── computeFusePercent：剩餘次數轉百分比，範圍限制在[0,100] ──
ok('剩餘次數=上限時 = 100%', X.computeFusePercent(8, 8) === 100);
ok('剩餘次數=0時 = 0%', X.computeFusePercent(0, 8) === 0);
ok('剩餘次數=一半時 = 50%', X.computeFusePercent(4, 8) === 50);
ok('allowed<=0時安全回傳0（不除以0）', X.computeFusePercent(5, 0) === 0);

// ── nbRatingIndex / nbComputeRating：評分門檻共5級 ──
ok('評分門檻共5級', C.ratingThresholds.length === 5);
ok('0分 → 第0級', X.nbRatingIndex(0) === 0);
ok('80分邊界含 → 第0級', X.nbRatingIndex(80) === 0);
ok('81分 → 第1級', X.nbRatingIndex(81) === 1);
ok('200分邊界含 → 第1級', X.nbRatingIndex(200) === 1);
ok('400分邊界含 → 第2級', X.nbRatingIndex(400) === 2);
ok('700分邊界含 → 第3級', X.nbRatingIndex(700) === 3);
ok('701分 → 第4級（最高，封頂）', X.nbRatingIndex(701) === 4);
ok('99999分 → 第4級（封頂不越界）', X.nbRatingIndex(99999) === 4);
(function () {
  let mono = true, prev = -1;
  for (let s = 0; s <= 1500; s += 10) {
    const i = X.nbRatingIndex(s);
    if (i < prev) mono = false;
    prev = i;
  }
  ok('評分級數隨分數單調不遞減', mono);
})();
ctx.window = { GAME_I18N: { ratings: ['A', 'B', 'C', 'D', 'E'] } };
ok('依分數取對應評語文字', X.nbComputeRating(0) === 'A' && X.nbComputeRating(99999) === 'E');
ctx.window = {};
ok('字典不存在時評語回傳空字串不拋錯', X.nbComputeRating(0) === '');

// ── nextDuelPlayer：雙人對戰輪替 ──
ok('A的下一位是B', X.nextDuelPlayer('A') === 'B');
ok('B的下一位是A', X.nextDuelPlayer('B') === 'A');

// ── gnumberbombT：i18n取字helper ──
ctx.window = { GAME_I18N: { hello: '哈囉 {n} 次' } };
ok('取字並代換變數', X.gnumberbombT('hello', { n: 3 }) === '哈囉 3 次');
ok('缺key回傳空字串不拋錯', X.gnumberbombT('__nope__') === '');
ctx.window = {};
ok('字典不存在時不拋錯', X.gnumberbombT('hello') === '');

// ── 共用檔不得殘留硬寫死文字 ──
(function () {
  const stripped = code.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/[^\n]*/g, '');
  const cjk = stripped.match(/[一-鿿぀-ヿ가-힯]/g);
  ok('共用邏輯檔（排除註解）不含中日韓文字', cjk === null,
     cjk ? [...new Set(cjk)].join('').slice(0, 40) : '');
})();

console.log(`\n數字炸彈 純邏輯回歸測試：${pass} 通過, ${fail} 失敗`);
process.exit(fail ? 1 : 0);
