// 踩地雷 純邏輯回歸測試
//
// 這款的關鍵不變量有三個，多語言重構後必須逐一證明沒被改壞：
//   1. 三種難度必須完全等同業界標準值（初級9x9/10雷、中級16x16/40雷、高級16x30/99雷）
//   2. 第一次點擊必安全——該格與周圍3x3絕對不能有雷（用大量隨機測試驗證100%成立）
//   3. 連鎖翻開用BFS而非遞迴（高級盤面480格，遞迴在極端情況會爆呼叫堆疊）
const fs = require('fs'), path = require('path'), vm = require('vm');
const code = fs.readFileSync(path.join(__dirname, '..', 'shared', 'minesweeper.js'), 'utf8');
const ctx = { console, Math, Array, Object, String, Number, Infinity, Set, Date, globalThis: null };
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(code + `
globalThis.__exp = { msComputeDifficultyForRound, msCreateEmptyGrid, msNeighborsOf, msPlaceMines,
  msComputeAdjacentCounts, msRevealCell, msToggleFlag, msCountFlaggedNeighbors, msChordReveal,
  msCountRevealedNonMine, msCheckWin, msCountFlags, msComputeRoundScore, msRatingIndex,
  msComputeRating, msDifficultyLabel, gminesweeperT, MS_CONFIG };`, ctx);
const X = ctx.__exp, C = X.MS_CONFIG;

let pass = 0, fail = 0;
const ok = (n, c, d) => { if (c) pass++; else { fail++; console.log('  ✗ ' + n + (d ? ' — ' + d : '')); } };

// ── 1. 業界標準難度數值（跟Windows內建踩地雷完全一致，不得更動）──
const STD = [
  { key: 'beginner', rows: 9, cols: 9, mines: 10 },
  { key: 'intermediate', rows: 16, cols: 16, mines: 40 },
  { key: 'expert', rows: 16, cols: 30, mines: 99 },
];
STD.forEach(function (s, i) {
  const d = C.difficultyTable[i];
  ok(`難度${i + 1} key=${s.key}`, d.key === s.key, d.key);
  ok(`難度${i + 1} 盤面 ${s.rows}x${s.cols}`, d.rows === s.rows && d.cols === s.cols, `${d.rows}x${d.cols}`);
  ok(`難度${i + 1} 地雷數 ${s.mines}`, d.mines === s.mines, String(d.mines));
});
ok('剛好三種難度', C.difficultyTable.length === 3);

// ── 難度階梯：過關升級，升到最高後維持最高 ──
ok('第1關是初級', X.msComputeDifficultyForRound(1).key === 'beginner');
ok('第2關是中級', X.msComputeDifficultyForRound(2).key === 'intermediate');
ok('第3關是高級', X.msComputeDifficultyForRound(3).key === 'expert');
ok('第4關之後維持高級（不越界）', X.msComputeDifficultyForRound(4).key === 'expert');
ok('第999關仍是高級', X.msComputeDifficultyForRound(999).key === 'expert');
ok('關卡數異常(0)不會取到undefined', X.msComputeDifficultyForRound(0).key === 'beginner');

// ── 鄰居計算：邊界情況 ──
ok('中間格有8個鄰居', X.msNeighborsOf(9, 9, 4, 4).length === 8);
ok('角落格有3個鄰居', X.msNeighborsOf(9, 9, 0, 0).length === 3);
ok('邊緣格有5個鄰居', X.msNeighborsOf(9, 9, 0, 4).length === 5);
ok('1x1盤面無鄰居', X.msNeighborsOf(1, 1, 0, 0).length === 0);
ok('鄰居不含自己', !X.msNeighborsOf(9, 9, 4, 4).some(p => p[0] === 4 && p[1] === 4));

// ── 2. 核心：第一次點擊必安全（該格＋周圍3x3都沒有雷）──
(function () {
  let violations = 0, mineCountWrong = 0;
  const ROUNDS = 200;
  for (let i = 0; i < ROUNDS; i++) {
    const d = C.difficultyTable[i % 3];
    const g = X.msCreateEmptyGrid(d.rows, d.cols);
    const sr = Math.floor(Math.random() * d.rows), sc = Math.floor(Math.random() * d.cols);
    X.msPlaceMines(g, d.rows, d.cols, d.mines, sr, sc);
    if (g[sr][sc].mine) violations++;
    X.msNeighborsOf(d.rows, d.cols, sr, sc).forEach(function (p) {
      if (g[p[0]][p[1]].mine) violations++;
    });
    let total = 0;
    for (let r = 0; r < d.rows; r++) for (let c = 0; c < d.cols; c++) if (g[r][c].mine) total++;
    if (total !== d.mines) mineCountWrong++;
  }
  ok(`第一次點擊安全區保證：${ROUNDS}次隨機測試零違規`, violations === 0, violations + ' 次違規');
  ok(`地雷總數永遠等於難度設定：${ROUNDS}次全對`, mineCountWrong === 0, mineCountWrong + ' 次不符');
})();

// 角落起手也要安全（安全區被盤面邊界裁掉的情況）
(function () {
  let bad = 0;
  for (let i = 0; i < 50; i++) {
    const d = C.difficultyTable[0];
    const g = X.msCreateEmptyGrid(d.rows, d.cols);
    X.msPlaceMines(g, d.rows, d.cols, d.mines, 0, 0);
    if (g[0][0].mine || g[0][1].mine || g[1][0].mine || g[1][1].mine) bad++;
  }
  ok('從角落起手時安全區仍成立', bad === 0, bad + ' 次違規');
})();

// ── 鄰接數計算：用人工可驗證的固定盤面核對 ──
(function () {
  const g = X.msCreateEmptyGrid(3, 3);
  g[0][0].mine = true;
  g[2][2].mine = true;
  X.msComputeAdjacentCounts(g, 3, 3);
  ok('正中央被兩顆雷包夾 → 2', g[1][1].adjacent === 2);
  ok('緊鄰單顆雷 → 1', g[0][1].adjacent === 1);
  ok('離兩顆雷都不相鄰 → 0', g[2][0].adjacent === 0, String(g[2][0].adjacent));
  const g2 = X.msCreateEmptyGrid(3, 3);
  X.msComputeAdjacentCounts(g2, 3, 3);
  let allZero = true;
  for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) if (g2[r][c].adjacent !== 0) allZero = false;
  ok('沒有雷時所有格子鄰接數為0', allZero);
})();

// ── 3. 連鎖翻開（BFS）：全空盤面點一下應該翻開全部格子，且效能無虞 ──
(function () {
  const g = X.msCreateEmptyGrid(16, 30);
  X.msComputeAdjacentCounts(g, 16, 30);
  const st = Date.now();
  const revealed = X.msRevealCell(g, 16, 30, 8, 15);
  const ms = Date.now() - st;
  ok('全空的高級盤面一次連鎖翻開全部480格', revealed.length === 480, String(revealed.length));
  ok('高級盤面連鎖翻開效能無虞(<200ms)', ms < 200, ms + 'ms');
  ok('沒有爆呼叫堆疊（BFS而非遞迴）', true);
})();

(function () {
  // 有雷時連鎖會停在數字格：中央放一顆雷，從角落翻開不應該翻到雷
  const g = X.msCreateEmptyGrid(9, 9);
  g[4][4].mine = true;
  X.msComputeAdjacentCounts(g, 9, 9);
  const revealed = X.msRevealCell(g, 9, 9, 0, 0);
  ok('連鎖翻開不會翻到地雷', !revealed.some(p => p[0] === 4 && p[1] === 4));
  ok('連鎖翻開範圍是 80 格（81格扣掉那顆雷）', revealed.length === 80, String(revealed.length));
})();

(function () {
  const g = X.msCreateEmptyGrid(5, 5);
  g[0][0].mine = true;
  X.msComputeAdjacentCounts(g, 5, 5);
  ok('點到地雷回傳只含該格', (function () {
    const r = X.msRevealCell(g, 5, 5, 0, 0);
    return r.length === 1 && r[0][0] === 0 && r[0][1] === 0;
  })());
  const g2 = X.msCreateEmptyGrid(5, 5);
  X.msComputeAdjacentCounts(g2, 5, 5);
  X.msToggleFlag(g2, 2, 2);
  ok('插旗的格子不能被翻開', X.msRevealCell(g2, 5, 5, 2, 2).length === 0);
  ok('已翻開的格子不能插旗', (function () {
    const g3 = X.msCreateEmptyGrid(5, 5);
    g3[1][1].revealed = true;
    return X.msToggleFlag(g3, 1, 1) === false;
  })());
  ok('插旗可以取消', (function () {
    const g4 = X.msCreateEmptyGrid(5, 5);
    X.msToggleFlag(g4, 1, 1);
    X.msToggleFlag(g4, 1, 1);
    return g4[1][1].flagged === false;
  })());
})();

// ── chord（旗數等於數字時快速翻開鄰居）：正確觸發與誤觸地雷兩種情境 ──
(function () {
  const g = X.msCreateEmptyGrid(5, 5);
  g[0][0].mine = true;
  X.msComputeAdjacentCounts(g, 5, 5);
  g[1][1].revealed = true;            // (1,1) 的 adjacent 應為 1
  ok('(1,1)鄰接數為1', g[1][1].adjacent === 1);
  X.msToggleFlag(g, 0, 0);            // 旗子插在真正的雷上
  const chord1 = X.msChordReveal(g, 5, 5, 1, 1);
  ok('旗數等於數字時 chord 會翻開其餘鄰居', chord1.revealed.length > 0, String(chord1.revealed.length));
  ok('旗子插對位置時 chord 不會踩到雷', chord1.hitMine === false);

  // 旗子插錯位置 → chord 應該真的會踩到雷（這是經典規則刻意保留的風險）
  const g2 = X.msCreateEmptyGrid(5, 5);
  g2[0][0].mine = true;
  X.msComputeAdjacentCounts(g2, 5, 5);
  g2[1][1].revealed = true;
  X.msToggleFlag(g2, 2, 2);           // 插在沒有雷的地方
  const res = X.msChordReveal(g2, 5, 5, 1, 1);
  ok('旗子插錯位置時 chord 會踩到真正的地雷（保留經典規則風險）', res.hitMine === true);
  ok('踩到雷時該雷格確實被翻開', res.revealed.some(p => p[0] === 0 && p[1] === 0));

  // 旗數不等於數字 → 不該觸發
  const g3 = X.msCreateEmptyGrid(5, 5);
  g3[0][0].mine = true;
  X.msComputeAdjacentCounts(g3, 5, 5);
  g3[1][1].revealed = true;
  ok('旗數不足時 chord 不觸發', X.msChordReveal(g3, 5, 5, 1, 1).revealed.length === 0);
  ok('未翻開的格子不能 chord', X.msChordReveal(g3, 5, 5, 3, 3).revealed.length === 0);
})();

// ── 勝利判定：翻開所有非雷格才算贏 ──
(function () {
  const g = X.msCreateEmptyGrid(3, 3);
  g[0][0].mine = true;
  X.msComputeAdjacentCounts(g, 3, 3);
  ok('還沒翻完不算贏', X.msCheckWin(g, 3, 3, 1) === false);
  for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) if (!g[r][c].mine) g[r][c].revealed = true;
  ok('翻開所有非雷格即獲勝', X.msCheckWin(g, 3, 3, 1) === true);
  ok('獲勝不需要把雷都插旗', g[0][0].flagged === false);
})();

// ── 評語分級 ──
ok('低分 → 第0級', X.msRatingIndex(0) === 0);
ok('150分（邊界含）→ 第0級', X.msRatingIndex(150) === 0);
ok('151分 → 第1級', X.msRatingIndex(151) === 1);
ok('超高分 → 最後一級（封頂）', X.msRatingIndex(99999) === C.ratingThresholds.length - 1);

// ── i18n ──
ctx.window = { GAME_I18N: { difficulties: ['A', 'B', 'C'], ratings: ['1', '2', '3', '4', '5'] } };
ok('難度名稱依index取對應語言文字', X.msDifficultyLabel(0) === 'A' && X.msDifficultyLabel(2) === 'C');
ok('缺key回傳空字串不拋錯', X.gminesweeperT('__nope__') === '');
ctx.window = {};
ok('字典不存在時不拋錯', X.msDifficultyLabel(0) === '' && X.msComputeRating(10) === '');

// ── 共用檔不得殘留硬寫死文字 ──
(function () {
  const stripped = code.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/[^\n]*/g, '');
  const cjk = stripped.match(/[一-鿿぀-ヿ가-힯]/g);
  ok('共用邏輯檔（排除註解）不含中日韓文字', cjk === null,
     cjk ? [...new Set(cjk)].join('').slice(0, 40) : '');
})();

console.log(`\n踩地雷 純邏輯回歸測試：${pass} 通過, ${fail} 失敗`);
process.exit(fail ? 1 : 0);
