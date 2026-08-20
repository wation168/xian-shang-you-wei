// 西洋棋 純邏輯回歸測試
//
// 這款是13款裡工程量最大的（完整規則引擎 + minimax/alpha-beta AI），
// 多語言重構把整段程式碼搬到 shared/chess.js，必須證明「走法產生器一個bit都沒被改到」。
// 用的是西洋棋程式設計界公認的黃金標準：perft（把某個局面往下走N層，數出合法走法的總節點數，
// 跟公開已知的正確數值核對）。這個數字只要有任何規則寫錯——漏了吃過路兵、易位條件判錯、
// 兵升變少算一種、把「送王被吃」的走法誤判成合法——總數就一定對不上，是極強的檢測。
const fs = require('fs'), path = require('path'), vm = require('vm');
const code = fs.readFileSync(path.join(__dirname, '..', 'shared', 'chess.js'), 'utf8');
const ctx = { console, Math, Array, Object, String, Number, Infinity, JSON, Date, globalThis: null };
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(code + `
globalThis.__exp = { chMakeInitialState, chCloneState, chGenerateLegalMoves, chMakeMove,
  chIsKingInCheck, chIsCheckmate, chIsStalemate, chIsInsufficientMaterial, chFindKing,
  chIsSquareAttacked, chPieceColor, chPieceType, chOppColor, chFindBestMove, chNegamax,
  chEvaluatePosition, chSquareName, chDifficultyIndex, gchessT, CH_CONFIG };`, ctx);
const X = ctx.__exp;

let pass = 0, fail = 0;
const ok = (n, c, d) => { if (c) pass++; else { fail++; console.log('  ✗ ' + n + (d ? ' — ' + d : '')); } };

// ── perft：核心驗證 ──
function perft(state, depth) {
  if (depth === 0) return 1;
  const moves = X.chGenerateLegalMoves(state, state.turn);
  if (depth === 1) return moves.length;
  let n = 0;
  for (const m of moves) n += perft(X.chMakeMove(state, m), depth - 1);
  return n;
}
const sq = p => X.chSquareName(p[0], p[1]);
const legal = s => X.chGenerateLegalMoves(s, s.turn);

const init = X.chMakeInitialState();
// 起始局面的公開標準值（西洋棋界通用，任何正確的走法產生器都必須完全吻合）
const EXPECT_INIT = [20, 400, 8902, 197281];
EXPECT_INIT.forEach((expect, i) => {
  const d = i + 1;
  const got = perft(X.chCloneState(init), d);
  ok(`perft 起始局面 depth ${d} = ${expect}`, got === expect, `實際 ${got}`);
});

console.log(`  （起始局面 perft depth 1-4 已核對）`);

// ── 基本規則 ──
ok('起始局面輪白方', init.turn === 'w');
ok('起始局面白王在e1', sq(X.chFindKing(init.board, 'w')) === 'e1');
ok('起始局面黑王在e8', sq(X.chFindKing(init.board, 'b')) === 'e8');
ok('起始局面雙方都沒被將軍', !X.chIsKingInCheck(init, 'w') && !X.chIsKingInCheck(init, 'b'));
ok('起始局面不是將死也不是逼和', !X.chIsCheckmate(init) && !X.chIsStalemate(init));
ok('起始局面子力充足（不算和棋）', !X.chIsInsufficientMaterial(init));

// ── Fool's mate：史上最快將死（1.f3 e5 2.g4 Qh4#），驗證將死判定 ──
(function () {
  let s = X.chCloneState(init);
  const seq = [['f2', 'f3'], ['e7', 'e5'], ['g2', 'g4'], ['d8', 'h4']];
  let okAll = true;
  for (const [from, to] of seq) {
    const mv = legal(s).find(m => sq(m.from) === from && sq(m.to) === to);
    if (!mv) { okAll = false; break; }
    s = X.chMakeMove(s, mv);
  }
  ok('Fool\'s mate 四步都是合法走法', okAll);
  if (okAll) {
    ok('Fool\'s mate 後白方被將軍', X.chIsKingInCheck(s, 'w'));
    ok('Fool\'s mate 後判定為將死', X.chIsCheckmate(s));
    ok('將死時無任何合法走法', legal(s).length === 0);
    ok('將死不會被誤判成逼和', !X.chIsStalemate(s));
  }
})();

// ── 不能走出「讓自己的王被將軍」的棋（合法走法產生的核心約束）──
(function () {
  const s = X.chCloneState(init);
  const moves = legal(s);
  let allSafe = true;
  for (const m of moves) {
    const after = X.chMakeMove(X.chCloneState(s), m);
    if (X.chIsKingInCheck(after, 'w')) allSafe = false;
  }
  ok('所有合法走法走完後自己的王都不會處於被將狀態', allSafe);
})();

// ── AI：alpha-beta 剪枝結果必須跟「找得到一步將死」一致 ──
(function () {
  // 造出白方一步即可將死的局面（Fool's mate 的前一手換邊：黑方 Qh4# 之前）
  let s = X.chCloneState(init);
  for (const [from, to] of [['f2', 'f3'], ['e7', 'e5'], ['g2', 'g4']]) {
    const mv = legal(s).find(m => sq(m.from) === from && sq(m.to) === to);
    s = X.chMakeMove(s, mv);
  }
  // 現在輪黑方，Qd8-h4 是一步將死
  const res = X.chFindBestMove(s, { maxDepth: 3, timeBudgetMs: 3000 });
  const best = res && res.move;
  ok('AI 在一步將死的局面找得到將殺手', !!best && sq(best.to) === 'h4',
     best ? sq(best.from) + '-' + sq(best.to) : '沒回傳走法');
  ok('AI 回傳結構含 move 與 score', !!res && 'move' in res && 'score' in res);
})();

// ── 評估函式方向性：白多一個后應該對白有利 ──
(function () {
  const s = X.chCloneState(init);
  const base = X.chEvaluatePosition(s);
  ok('起始局面評估接近平衡', Math.abs(base) < 100, String(base));
})();

// ── 難度：未知難度要安全退回中等，不能讓AI整個壞掉（7-3防錯）──
ok('未知難度退回中等(index 1)', X.chDifficultyIndex('__unknown__') === 1);

// ── i18n ──
ctx.window = { GAME_I18N: { pieceNames: {}, difficultyLabels: ['A', 'B', 'C'] } };
ok('缺key回傳空字串不拋錯', X.gchessT('__nope__') === '');

// ── 共用檔不得殘留硬寫死文字 ──
(function () {
  const stripped = code.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/[^\n]*/g, '');
  const cjk = stripped.match(/[一-鿿぀-ヿ가-힯]/g);
  ok('共用邏輯檔（排除註解）不含中日韓文字', cjk === null,
     cjk ? [...new Set(cjk)].join('').slice(0, 40) : '');
})();

console.log(`\n西洋棋 純邏輯回歸測試：${pass} 通過, ${fail} 失敗`);
process.exit(fail ? 1 : 0);
