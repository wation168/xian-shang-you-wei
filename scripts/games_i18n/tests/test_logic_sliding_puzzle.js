// 數字推盤 純邏輯回歸測試
//
// 核心邏輯有兩塊：① 可解性驗證（isSolvable用逆序數奇偶性公式）必須跟「用合法滑動從解答狀態
// 洗牌」（shuffleViaRandomMoves）產生的盤面永遠一致為「可解」，這是這款遊戲最重要的正確性保證，
// 一旦壞掉玩家就可能拿到解不開的盤面；② 分數/評語的門檻換算。多語言重構把整段搬到
// shared/sliding-puzzle.js，這裡驗證這些純函式沒有被改壞。
const fs = require('fs'), path = require('path'), vm = require('vm');
const code = fs.readFileSync(path.join(__dirname, '..', 'shared', 'sliding-puzzle.js'), 'utf8');
const ctx = { console, Math, Array, Object, String, Number, Infinity, Set, globalThis: null };
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(code + `
globalThis.__exp = { makeSolvedBoard, cloneBoard, findBlank, isSolved, canMove, moveBlank, moveTileAt,
  shuffleViaRandomMoves, countInversions, isSolvable, computeBoardSize, computePuzzleScore,
  spRatingIndex, spComputeRating, gslidingpuzzleT, SP_CONFIG };`, ctx);
const X = ctx.__exp, C = X.SP_CONFIG;

let pass = 0, fail = 0;
const ok = (n, c, d) => { if (c) pass++; else { fail++; console.log('  ✗ ' + n + (d ? ' — ' + d : '')); } };

// ── makeSolvedBoard / isSolved：解答狀態本身必須被判定為已解 ──
[3, 4, 5, 6].forEach(function (size) {
  const b = X.makeSolvedBoard(size);
  ok('size=' + size + ' 的解答狀態 isSolved()===true', X.isSolved(b));
  ok('size=' + size + ' 解答狀態的空格在右下角', b[size - 1][size - 1] === 0);
});

// ── findBlank / cloneBoard ──
(function () {
  const b = X.makeSolvedBoard(4);
  const blank = X.findBlank(b);
  ok('findBlank找到正確位置(3,3)', blank[0] === 3 && blank[1] === 3);
  const c = X.cloneBoard(b);
  c[0][0] = 999;
  ok('cloneBoard是深拷貝，不會互相影響', b[0][0] !== 999);
})();

// ── moveBlank / canMove：邊界不能移出盤面 ──
(function () {
  const b = X.makeSolvedBoard(3); // 空格在(2,2)，右下角
  ok('空格在右下角時 down 不合法', X.canMove(b, 'down') === false);
  ok('空格在右下角時 right 不合法', X.canMove(b, 'right') === false);
  ok('空格在右下角時 up 合法', X.canMove(b, 'up') === true);
  ok('空格在右下角時 left 合法', X.canMove(b, 'left') === true);
  const res = X.moveBlank(b, 'down');
  ok('不合法方向 moveBlank 回傳 moved:false 且盤面不變', res.moved === false && res.board === b);
  const res2 = X.moveBlank(b, 'up');
  ok('合法方向 moveBlank 回傳 moved:true', res2.moved === true);
  ok('合法移動後空格位置改變', X.findBlank(res2.board)[0] === 1 && X.findBlank(res2.board)[1] === 2);
})();

// ── moveTileAt：只有跟空格相鄰的方塊才能點擊移動 ──
(function () {
  const b = X.makeSolvedBoard(3); // 空格(2,2)
  const notAdjacent = X.moveTileAt(b, 0, 0);
  ok('點擊不相鄰方塊不會移動', notAdjacent.moved === false);
  const adjacent = X.moveTileAt(b, 2, 1); // 跟空格(2,2)相鄰
  ok('點擊相鄰方塊會移動', adjacent.moved === true);
  ok('點擊相鄰方塊後該方塊被交換到原空格位置', adjacent.board[2][2] === b[2][1]);
})();

// ── isSolvable：解答狀態本身、以及所有透過合法滑動洗出來的盤面，永遠可解 ──
(function () {
  [3, 4, 5, 6].forEach(function (size) {
    ok('size=' + size + ' 解答狀態 isSolvable===true', X.isSolvable(X.makeSolvedBoard(size)));
  });
})();
(function () {
  let allSolvable = true, trials = 0;
  [3, 4, 5, 6].forEach(function (size) {
    for (let t = 0; t < 30; t++) {
      trials++;
      const shuffleMoves = Math.max(C.minShuffleMoves, size * size * C.shuffleMovesPerCell);
      const board = X.shuffleViaRandomMoves(size, shuffleMoves);
      if (!X.isSolvable(board)) allSolvable = false;
    }
  });
  ok('shuffleViaRandomMoves洗出的' + trials + '個盤面(size 3~6)全部isSolvable===true', allSolvable);
})();
(function () {
  // 反向驗證：isSolvable公式本身要正確，不能永遠回傳true——構造一個已知無解的3x3盤面
  // （只交換兩個非空格方塊，其餘不動＝一次對換＝逆序數變化奇數＝理論上無解）
  const solved = X.makeSolvedBoard(3);
  const unsolvable = X.cloneBoard(solved);
  const tmp = unsolvable[0][0]; unsolvable[0][0] = unsolvable[0][1]; unsolvable[0][1] = tmp;
  ok('人為對換兩個方塊（保持空格位置不變）產生的盤面 isSolvable===false', X.isSolvable(unsolvable) === false);
})();

// ── countInversions ──
ok('已排序陣列逆序數為0', X.countInversions([1, 2, 3, 4]) === 0);
ok('完全反轉陣列的逆序數為 n(n-1)/2', X.countInversions([4, 3, 2, 1]) === 6);
ok('[2,1,3]的逆序數為1', X.countInversions([2, 1, 3]) === 1);

// ── computeBoardSize：關卡數→盤面大小，min3~max6遞增後封頂 ──
ok('第1關 → 3x3', X.computeBoardSize(1) === 3);
ok('第2關 → 4x4', X.computeBoardSize(2) === 4);
ok('第3關 → 5x5', X.computeBoardSize(3) === 5);
ok('第4關 → 6x6', X.computeBoardSize(4) === 6);
ok('第5關 → 封頂在6x6', X.computeBoardSize(5) === 6);
ok('第99關 → 仍封頂在6x6', X.computeBoardSize(99) === 6);

// ── computePuzzleScore：步數/時間增加會扣分，且有下限20分 ──
(function () {
  const base3 = C.scoreBaseBySize[3];
  ok('0步0秒時分數等於該盤面基礎分', X.computePuzzleScore(3, 0, 0) === base3);
  const s1 = X.computePuzzleScore(3, 10, 0);
  const s2 = X.computePuzzleScore(3, 50, 0);
  ok('步數越多分數越低', s2 < s1 && s1 < base3);
  const t1 = X.computePuzzleScore(3, 0, 10);
  const t2 = X.computePuzzleScore(3, 0, 60);
  ok('花費時間越久分數越低', t2 < t1 && t1 <= base3);
  ok('分數有下限20分，不會扣成負數', X.computePuzzleScore(3, 9999, 9999) === 20);
  ok('盤面越大基礎分越高', C.scoreBaseBySize[6] > C.scoreBaseBySize[5] &&
     C.scoreBaseBySize[5] > C.scoreBaseBySize[4] && C.scoreBaseBySize[4] > C.scoreBaseBySize[3]);
})();

// ── spRatingIndex / spComputeRating：評分門檻共5級 ──
ok('評分門檻共5級', C.ratingThresholds.length === 5);
ok('0分 → 第0級', X.spRatingIndex(0) === 0);
ok('100分邊界含 → 第0級', X.spRatingIndex(100) === 0);
ok('101分 → 第1級', X.spRatingIndex(101) === 1);
ok('300分邊界含 → 第1級', X.spRatingIndex(300) === 1);
ok('600分邊界含 → 第2級', X.spRatingIndex(600) === 2);
ok('1000分邊界含 → 第3級', X.spRatingIndex(1000) === 3);
ok('1001分 → 第4級（最高，封頂）', X.spRatingIndex(1001) === 4);
ok('99999分 → 第4級（封頂不越界）', X.spRatingIndex(99999) === 4);
(function () {
  let mono = true, prev = -1;
  for (let s = 0; s <= 2000; s += 10) {
    const i = X.spRatingIndex(s);
    if (i < prev) mono = false;
    prev = i;
  }
  ok('評分級數隨分數單調不遞減', mono);
})();
ctx.window = { GAME_I18N: { ratings: ['A', 'B', 'C', 'D', 'E'] } };
ok('依分數取對應評語文字', X.spComputeRating(0) === 'A' && X.spComputeRating(99999) === 'E');
ctx.window = {};
ok('字典不存在時評語回傳空字串不拋錯', X.spComputeRating(0) === '');

// ── gslidingpuzzleT：i18n取字helper ──
ctx.window = { GAME_I18N: { hello: '哈囉 {n} 次' } };
ok('取字並代換變數', X.gslidingpuzzleT('hello', { n: 3 }) === '哈囉 3 次');
ok('缺key回傳空字串不拋錯', X.gslidingpuzzleT('__nope__') === '');
ctx.window = {};
ok('字典不存在時不拋錯', X.gslidingpuzzleT('hello') === '');

// ── 共用檔不得殘留硬寫死文字 ──
(function () {
  const stripped = code.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/[^\n]*/g, '');
  const cjk = stripped.match(/[一-鿿぀-ヿ가-힯]/g);
  ok('共用邏輯檔（排除註解）不含中日韓文字', cjk === null,
     cjk ? [...new Set(cjk)].join('').slice(0, 40) : '');
})();

console.log(`\n數字推盤 純邏輯回歸測試：${pass} 通過, ${fail} 失敗`);
process.exit(fail ? 1 : 0);
