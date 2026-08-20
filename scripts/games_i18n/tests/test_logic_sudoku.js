// 數獨 純邏輯回歸測試
//
// 這款的黃金標準是「每一題都必須唯一解」——用產生器自己的求解器反向驗證。
// 唯一解是數獨題目的基本品質要求：多解代表題目出錯（玩家填對卻被判錯），
// 無解則直接無法完成。多語言重構把產生器整段搬到 shared/sudoku.js，
// 必須證明四個難度產出的題目都還是唯一解。
const fs = require('fs'), path = require('path'), vm = require('vm');
const code = fs.readFileSync(path.join(__dirname, '..', 'shared', 'sudoku.js'), 'utf8');
const ctx = { console, Math, Array, Object, String, Number, Infinity, Date, globalThis: null };
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(code + `
globalThis.__exp = { skGeneratePuzzle, skCountSolutions, skGenerateFullSolution, skIsValidPlacement,
  skMakeGrid9, skCloneGrid9, skIsGridComplete, skComputeConflictCells, skDifficultyLabel,
  skRatingIndex, skComputeRating, skComputeDifficultyIndex, gsudokuT, SUDOKU_CONFIG };`, ctx);
const X = ctx.__exp, C = X.SUDOKU_CONFIG;

let pass = 0, fail = 0;
const ok = (n, c, d) => { if (c) pass++; else { fail++; console.log('  ✗ ' + n + (d ? ' — ' + d : '')); } };

// ── 完整解本身必須合法（每列每行每宮1-9不重複）──
function isValidFullGrid(g) {
  for (let r = 0; r < 9; r++) {
    const row = new Set(g[r]);
    if (row.size !== 9 || g[r].some(v => v < 1 || v > 9)) return false;
  }
  for (let c = 0; c < 9; c++) {
    const col = new Set();
    for (let r = 0; r < 9; r++) col.add(g[r][c]);
    if (col.size !== 9) return false;
  }
  for (let br = 0; br < 3; br++) for (let bc = 0; bc < 3; bc++) {
    const box = new Set();
    for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) box.add(g[br * 3 + r][bc * 3 + c]);
    if (box.size !== 9) return false;
  }
  return true;
}

(function () {
  let allValid = true;
  for (let i = 0; i < 20; i++) if (!isValidFullGrid(X.skGenerateFullSolution())) allValid = false;
  ok('隨機產生20個完整解，每列/行/宮都是1-9不重複', allValid);
})();

// ── 核心：四個難度各產多題，每一題都必須「恰好一組解」──
const t0 = Date.now();
const GEN_TIMES = [];
C.difficulties.forEach(function (d, idx) {
  let uniqueAll = true, cluesOk = true, slowest = 0, worstClues = null;
  const ROUNDS = 6;
  for (let i = 0; i < ROUNDS; i++) {
    const st = Date.now();
    const p = X.skGeneratePuzzle(d.clues);
    const grid = p.puzzle || p.grid || p;
    const elapsed = Date.now() - st;
    if (elapsed > slowest) slowest = elapsed;
    // cap 設 2：只要找得到第2組解就代表不是唯一解
    if (X.skCountSolutions(grid, 2) !== 1) uniqueAll = false;
    const clues = grid.flat().filter(v => v !== 0).length;
    if (clues < d.clues) { cluesOk = false; worstClues = clues; }
  }
  ok(`難度 ${d.key}：${ROUNDS}題全部唯一解`, uniqueAll);
  ok(`難度 ${d.key}：提示數不少於設定值(${d.clues})`, cluesOk,
     worstClues === null ? '' : '出現只有' + worstClues + '個提示');
  // 產生時間只做「不會誇張到卡死」的上限把關（雲端沙盒CPU比一般桌機慢，
  // 這裡放寬到8秒只為了抓住「演算法被改壞導致爆炸性回溯」這種等級的問題）
  ok(`難度 ${d.key}：單題產生時間未失控(<8秒)`, slowest < 8000, slowest + 'ms');
  GEN_TIMES.push(d.key + '=' + slowest + 'ms');
});
console.log(`  （四個難度共 ${C.difficulties.length * 6} 題已逐題用求解器驗證唯一解，總耗時 ${Date.now() - t0}ms）`);
console.log(`  （各難度單題最慢產生時間：${GEN_TIMES.join(', ')}）`);

// ── 求解器本身要先被證明是對的，否則上面的唯一解驗證沒有意義 ──
(function () {
  const full = X.skGenerateFullSolution();
  ok('完整盤面求解器回報恰好1解', X.skCountSolutions(full, 2) === 1);
  const empty = X.skMakeGrid9(0);
  ok('全空盤面有多解（求解器抓得到>1）', X.skCountSolutions(empty, 2) >= 2);
  // 從完整解挖掉夠多格之後，解數必然不再唯一——用這個驗求解器真的會「往下找第2組解」，
  // 而不是永遠回傳1（若求解器壞掉只會回1，上面的唯一解驗證就全部失去意義）
  const holed = X.skCloneGrid9(full);
  for (let i = 0; i < 60; i++) holed[Math.floor(i / 9)][i % 9] = 0;
  ok('挖掉大量格子後解數>1（證明求解器真的會找第2組解）', X.skCountSolutions(holed, 2) >= 2);
})();

// ── 合法性判定 ──
(function () {
  const g = X.skMakeGrid9(0);
  g[0][0] = 5;
  ok('同列重複 → 不合法', X.skIsValidPlacement(g, 0, 3, 5) === false);
  ok('同行重複 → 不合法', X.skIsValidPlacement(g, 4, 0, 5) === false);
  ok('同宮重複 → 不合法', X.skIsValidPlacement(g, 1, 1, 5) === false);
  ok('無衝突 → 合法', X.skIsValidPlacement(g, 4, 4, 5) === true);
  ok('自己那一格不算跟自己衝突', X.skIsValidPlacement(g, 0, 0, 5) === true);
})();

// ── 完成判定 ──
(function () {
  // skIsGridComplete(grid, solution)：比對玩家盤面是否已經跟解答完全一致
  const sol = X.skGenerateFullSolution();
  ok('全空盤面不算完成', X.skIsGridComplete(X.skMakeGrid9(0), sol) === false);
  ok('與解答完全相同才算完成', X.skIsGridComplete(X.skCloneGrid9(sol), sol) === true);
  const almost = X.skCloneGrid9(sol);
  almost[4][4] = almost[4][4] === 1 ? 2 : 1;
  ok('只差一格也不算完成', X.skIsGridComplete(almost, sol) === false);
})();

// ── 難度階梯：解完自動升級，升到最高後維持最高（不會越界） ──
(function () {
  const n = C.difficulties.length;
  ok('第1題是最簡單難度', X.skComputeDifficultyIndex(1) === 0);
  ok('第2題難度提升', X.skComputeDifficultyIndex(2) === 1);
  ok('第4題到達最高難度', X.skComputeDifficultyIndex(4) === n - 1);
  ok('超過難度數量後封頂在最高難度（不會越界取到undefined）', X.skComputeDifficultyIndex(999) === n - 1);
  let mono = true;
  for (let r = 2; r <= 100; r++) if (X.skComputeDifficultyIndex(r) < X.skComputeDifficultyIndex(r - 1)) mono = false;
  ok('難度單調不遞減', mono);
})();

// ── i18n ──
ctx.window = { GAME_I18N: { difficulties: ['A', 'B', 'C', 'D'] } };
ok('難度名稱依index取對應語言文字', X.skDifficultyLabel(0) === 'A' && X.skDifficultyLabel(3) === 'D');
ok('缺key回傳空字串不拋錯', X.gsudokuT('__nope__') === '');
ctx.window = {};
ok('字典不存在時難度名稱不拋錯', X.skDifficultyLabel(0) === '');

// ── 共用檔不得殘留硬寫死文字 ──
(function () {
  const stripped = code.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/[^\n]*/g, '');
  const cjk = stripped.match(/[一-鿿぀-ヿ가-힯]/g);
  ok('共用邏輯檔（排除註解）不含中日韓文字', cjk === null,
     cjk ? [...new Set(cjk)].join('').slice(0, 40) : '');
})();

console.log(`\n數獨 純邏輯回歸測試：${pass} 通過, ${fail} 失敗`);
process.exit(fail ? 1 : 0);
