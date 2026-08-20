// 五子棋 純邏輯回歸測試
//
// 核心邏輯有兩塊：① 連線判定（checkWin，必須恰好5連線才算贏，4連線不算）跟落子位置的精確性
// （不像四子棋有重力，點哪裡就該落在哪裡）；② AI邏輯（立即獲勝優先→立即防守優先→威脅評分挑最高分）。
// 這是2026/08/15從錯誤的四子棋重寫成正確五子棋後留下的測試重點，多語言重構把整段搬到
// shared/gomoku.js，這裡驗證這些純函式沒有被改壞。
const fs = require('fs'), path = require('path'), vm = require('vm');
const code = fs.readFileSync(path.join(__dirname, '..', 'shared', 'gomoku.js'), 'utf8');
const ctx = { console, Math, Array, Object, String, Number, Infinity, Set, globalThis: null };
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(code + `
globalThis.__exp = { createEmptyBoard, inBounds, checkWin, isBoardFull, countDirection, patternScore,
  lineScoreAt, cellThreatScore, placeStoneImmutable, candidateCells, pickAiMove, ggomokuT, gkPlayerName,
  GK_CONFIG };`, ctx);
const X = ctx.__exp, C = X.GK_CONFIG;

let pass = 0, fail = 0;
const ok = (n, c, d) => { if (c) pass++; else { fail++; console.log('  ✗ ' + n + (d ? ' — ' + d : '')); } };

function emptyBoard() { return X.createEmptyBoard(C.boardSize); }
function place(board, cells, player) { cells.forEach(function ([x, y]) { board[y][x] = player; }); return board; }

// ── createEmptyBoard / inBounds ──
(function () {
  const b = emptyBoard();
  ok('盤面大小為15x15', b.length === 15 && b[0].length === 15);
  ok('初始盤面全部是0（空格）', b.every(function (row) { return row.every(function (v) { return v === 0; }); }));
  ok('inBounds邊界判斷正確', X.inBounds(0, 0, 15) && X.inBounds(14, 14, 15) && !X.inBounds(-1, 0, 15) && !X.inBounds(0, 15, 15));
})();

// ── checkWin：恰好5連線才算贏，4連線不算，橫直斜都要能判斷 ──
(function () {
  let b = emptyBoard();
  place(b, [[0, 0], [1, 0], [2, 0], [3, 0]], 1); // 橫向4連線
  ok('橫向4連線不算獲勝', X.checkWin(b, 3, 0, 1, 15, 5) === null);
  place(b, [[4, 0]], 1); // 補到5連線
  const win = X.checkWin(b, 4, 0, 1, 15, 5);
  ok('橫向恰好5連線判定獲勝', win !== null && win.length === 5);
})();
(function () {
  let b = emptyBoard();
  place(b, [[3, 0], [3, 1], [3, 2], [3, 3], [3, 4]], 1);
  ok('直向5連線判定獲勝', X.checkWin(b, 3, 4, 1, 15, 5) !== null);
})();
(function () {
  let b = emptyBoard();
  place(b, [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]], 1);
  ok('主對角線5連線判定獲勝', X.checkWin(b, 4, 4, 1, 15, 5) !== null);
})();
(function () {
  let b = emptyBoard();
  place(b, [[4, 0], [3, 1], [2, 2], [1, 3], [0, 4]], 1);
  ok('反對角線5連線判定獲勝', X.checkWin(b, 0, 4, 1, 15, 5) !== null);
})();
(function () {
  let b = emptyBoard();
  place(b, [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0]], 1);
  ok('對手棋子不會被誤判為己方連線', X.checkWin(b, 4, 0, 2, 15, 5) === null);
})();
(function () {
  // 6連線（超過5）仍然算獲勝，不會因為「剛好」判斷失準
  let b = emptyBoard();
  place(b, [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0]], 1);
  ok('超過5連線（6顆）仍判定獲勝', X.checkWin(b, 5, 0, 1, 15, 5) !== null);
})();

// ── isBoardFull ──
ok('全空盤面 isBoardFull===false', X.isBoardFull(emptyBoard()) === false);
(function () {
  const full = Array.from({ length: 15 }, function () { return Array(15).fill(1); });
  ok('全滿盤面 isBoardFull===true', X.isBoardFull(full) === true);
})();

// ── placeStoneImmutable：不修改原盤面 ──
(function () {
  const b = emptyBoard();
  const nb = X.placeStoneImmutable(b, 5, 5, 1);
  ok('placeStoneImmutable不修改原盤面', b[5][5] === 0);
  ok('placeStoneImmutable回傳的新盤面有正確落子', nb[5][5] === 1);
})();

// ── candidateCells：空盤面只回傳正中央一格，非空盤面回傳鄰近空格候選 ──
(function () {
  const b = emptyBoard();
  const cands = X.candidateCells(b, 15);
  ok('空盤面候選只有1格，且是正中央', cands.length === 1 && cands[0].x === 7 && cands[0].y === 7);
})();
(function () {
  const b = emptyBoard();
  b[7][7] = 1;
  const cands = X.candidateCells(b, 15);
  ok('落一子後候選格不為空', cands.length > 0);
  ok('候選格都在該子附近(曼哈頓/棋盤距離2以內)且本身是空格', cands.every(function (c) {
    return b[c.y][c.x] === 0 && Math.abs(c.x - 7) <= 2 && Math.abs(c.y - 7) <= 2;
  }));
  ok('已落子的格子本身不會出現在候選清單', !cands.some(function (c) { return c.x === 7 && c.y === 7; }));
})();

// ── pickAiMove：AI能把握自己的獲勝機會 ──
(function () {
  const b = emptyBoard();
  place(b, [[0, 0], [1, 0], [2, 0], [3, 0]], 2); // AI(2)已有4連線，下一步就贏
  const move = X.pickAiMove(b, 15, 2, 1, 5);
  ok('AI能一步獲勝時，優先選擇獲勝手（4,0）', move.x === 4 && move.y === 0);
})();

// ── pickAiMove：AI會擋下對手即將獲勝的威脅 ──
(function () {
  const b = emptyBoard();
  place(b, [[0, 5], [1, 5], [2, 5], [3, 5]], 1); // 人類(1)4連線，AI必須擋
  const move = X.pickAiMove(b, 15, 2, 1, 5);
  const blocked = (move.x === 4 && move.y === 5) || (move.x === -1 && move.y === 5);
  // 邊界只有一端能擋（-1不合法），確認AI擋的是合法的那一端
  ok('AI會擋下對手即將完成的5連線', move.x === 4 && move.y === 5);
})();

// ── pickAiMove：獲勝優先於防守（自己能贏就不需要擋對手）──
(function () {
  const b = emptyBoard();
  place(b, [[0, 0], [1, 0], [2, 0], [3, 0]], 2); // AI能一步獲勝
  place(b, [[0, 5], [1, 5], [2, 5], [3, 5]], 1); // 人類也快贏了
  const move = X.pickAiMove(b, 15, 2, 1, 5);
  ok('自己能獲勝時優先取勝，不理會對手的威脅', move.x === 4 && move.y === 0);
})();

// ── pickAiMove：開局第一手佔正中央 ──
(function () {
  const b = emptyBoard();
  const move = X.pickAiMove(b, 15, 2, 1, 5);
  ok('空盤面時AI第一手下在正中央(7,7)', move.x === 7 && move.y === 7);
})();

// ── patternScore：連線數越多、開放端越多，威脅分數越高 ──
(function () {
  ok('達到winLen視為必勝分數', X.patternScore(5, 2, 5) === 100000);
  ok('活四(count=4,openEnds=2)分數最高（僅次於直接獲勝）', X.patternScore(4, 2, 5) === 10000);
  ok('衝四(count=4,openEnds=1)分數低於活四', X.patternScore(4, 1, 5) < X.patternScore(4, 2, 5));
  ok('活三(count=3,openEnds=2)分數低於衝四但仍具威脅', X.patternScore(3, 2, 5) < X.patternScore(4, 1, 5) && X.patternScore(3, 2, 5) > 0);
  ok('兩端都被封死的連線威脅分數最低(=1)', X.patternScore(2, 0, 5) === 1);
})();

// ── gkPlayerName：依模式與玩家編號取正確key ──
ctx.window = { GAME_I18N: { nameYou: 'YOU', nameComputer: 'CPU', namePlayer1: 'P1', namePlayer2: 'P2' } };
ok('ai模式玩家1 → 你', X.gkPlayerName('ai', 1) === 'YOU');
ok('ai模式玩家2 → 電腦', X.gkPlayerName('ai', 2) === 'CPU');
ok('2p模式玩家1 → 玩家1', X.gkPlayerName('2p', 1) === 'P1');
ok('2p模式玩家2 → 玩家2', X.gkPlayerName('2p', 2) === 'P2');
ctx.window = {};
ok('字典不存在時不拋錯，回傳空字串', X.gkPlayerName('ai', 1) === '');

// ── ggomokuT：i18n取字helper ──
ctx.window = { GAME_I18N: { hello: '哈囉 {n} 次' } };
ok('取字並代換變數', X.ggomokuT('hello', { n: 3 }) === '哈囉 3 次');
ok('缺key回傳空字串不拋錯', X.ggomokuT('__nope__') === '');
ctx.window = {};
ok('字典不存在時不拋錯', X.ggomokuT('hello') === '');

// ── 共用檔不得殘留硬寫死文字 ──
(function () {
  const stripped = code.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/[^\n]*/g, '');
  const cjk = stripped.match(/[一-鿿぀-ヿ가-힯]/g);
  ok('共用邏輯檔（排除註解）不含中日韓文字', cjk === null,
     cjk ? [...new Set(cjk)].join('').slice(0, 40) : '');
})();

console.log(`\n五子棋 純邏輯回歸測試：${pass} 通過, ${fail} 失敗`);
process.exit(fail ? 1 : 0);
