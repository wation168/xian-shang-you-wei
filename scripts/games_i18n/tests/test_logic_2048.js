// 2048 純邏輯回歸測試 —— 對「抽出後的共用檔 shared/2048.js」重跑，
// 確認多語言化重構沒有動到任何遊戲規則（第三十輪原本15項測試 + 重構後新增的針對性檢查）
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const SRC = path.join(__dirname, '..', 'out', 'games', 'shared', '2048.js');
const code = fs.readFileSync(SRC, 'utf8');

// 【第三十輪已記錄的JS細節】eval/vm 裡宣告的 const 不會外洩到呼叫端，
// 要在同一次執行裡明確掛到 globalThis 上才能從外面引用。
const ctx = { console, Math, Array, Object, String, Number, Infinity, globalThis: null };
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(code + `
globalThis.__exp = { slideLeftLine, moveGrid, hasMovesLeft, makeEmptyGrid,
  maxTileOf, ratingIndex, transpose, emptyCells, computeRating, g2048T, G2048_CONFIG };
`, ctx);
const X = ctx.__exp;

let pass = 0, fail = 0;
function ok(name, cond) {
  if (cond) { pass++; } else { fail++; console.log('  ✗ ' + name); }
}
function eq(name, a, b) { ok(name, JSON.stringify(a) === JSON.stringify(b)); }

// ── 1-6：單行滑動合併邏輯 ──
eq('空行不動', X.slideLeftLine([0,0,0,0]).line, [0,0,0,0]);
ok('空行 moved=false', X.slideLeftLine([0,0,0,0]).moved === false);
eq('靠攏不合併', X.slideLeftLine([0,2,0,4]).line, [2,4,0,0]);
eq('兩個相同合併', X.slideLeftLine([2,2,0,0]).line, [4,0,0,0]);
ok('合併加分正確', X.slideLeftLine([2,2,0,0]).scoreGain === 4);
eq('四個相同合併成兩組（不連鎖）', X.slideLeftLine([2,2,2,2]).line, [4,4,0,0]);

// ── 7-8：防重複合併（同一步內合併過的方塊不能再合併）──
eq('4,2,2 → 4,4 而非 8', X.slideLeftLine([4,2,2,0]).line, [4,4,0,0]);
eq('2,2,4 → 4,4 而非 8', X.slideLeftLine([2,2,4,0]).line, [4,4,0,0]);

// ── 9-12：四方向移動 ──
eq('往左', X.moveGrid([[2,2,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], 'left').grid[0], [4,0,0,0]);
eq('往右', X.moveGrid([[2,2,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]], 'right').grid[0], [0,0,0,4]);
eq('往上', X.moveGrid([[2,0,0,0],[2,0,0,0],[0,0,0,0],[0,0,0,0]], 'up').grid.map(r=>r[0]), [4,0,0,0]);
eq('往下', X.moveGrid([[2,0,0,0],[2,0,0,0],[0,0,0,0],[0,0,0,0]], 'down').grid.map(r=>r[0]), [0,0,0,4]);

// ── 13：總和守恆不變量（合併不會憑空生出或吃掉數值）──
(function () {
  const g = [[2,2,4,4],[8,8,16,16],[2,4,8,16],[0,0,2,2]];
  const sum = a => a.flat().reduce((x,y)=>x+y,0);
  let allOk = true;
  ['left','right','up','down'].forEach(function (d) {
    if (sum(X.moveGrid(g, d).grid) !== sum(g)) allOk = false;
  });
  ok('四方向移動皆保持總和守恆', allOk);
})();

// ── 14：鏡射一致性交叉驗證（左移結果水平翻轉 === 翻轉後右移）──
(function () {
  const g = [[2,0,2,4],[4,4,0,0],[0,2,2,2],[8,0,8,0]];
  const flip = a => a.map(r => r.slice().reverse());
  eq('左移鏡射等於鏡射後右移', flip(X.moveGrid(g,'left').grid), X.moveGrid(flip(g),'right').grid);
})();

// ── 15：遊戲結束判定 ──
ok('滿盤且無可合併 → 結束', X.hasMovesLeft([[2,4,2,4],[4,2,4,2],[2,4,2,4],[4,2,4,2]]) === false);
ok('滿盤但有相鄰相同 → 還能動', X.hasMovesLeft([[2,2,2,4],[4,2,4,2],[2,4,2,4],[4,2,4,2]]) === true);
ok('有空格 → 還能動', X.hasMovesLeft([[2,4,2,4],[4,2,4,2],[2,4,2,4],[4,2,4,0]]) === true);

// ══ 以下為多語言重構後「新增」的針對性測試 ══

// ── 評語分級改成「回傳index」後，門檻對應必須跟原本完全一致 ──
ok('分數0 → 第0級', X.ratingIndex(0) === 0);
ok('分數128（邊界含）→ 第0級', X.ratingIndex(128) === 0);
ok('分數129 → 第1級', X.ratingIndex(129) === 1);
ok('分數512 → 第1級', X.ratingIndex(512) === 1);
ok('分數1024 → 第2級', X.ratingIndex(1024) === 2);
ok('分數2048 → 第3級', X.ratingIndex(2048) === 3);
ok('分數20000 → 第4級（封頂）', X.ratingIndex(20000) === 4);
ok('門檻數量與評語數量一致（5級）', X.G2048_CONFIG.ratingThresholds.length === 5);

// ── i18n 取字：缺key不能崩潰，且要能做變數代入 ──
ctx.window = { GAME_I18N: { hello: '你好 {name}，得分 {s}' } };
ok('變數代入正確', X.g2048T('hello', { name: '鴻哥', s: 100 }) === '你好 鴻哥，得分 100');
ok('缺key回傳空字串不拋錯', X.g2048T('__not_exist__') === '');
ctx.window = { GAME_I18N: { ratings: ['A','B','C','D','E'] } };
ok('computeRating 依index取對應語言文字', X.computeRating(0) === 'A' && X.computeRating(20000) === 'E');
ctx.window = {};
ok('字典整個不存在時 computeRating 不拋錯', X.computeRating(500) === '');

// ── 共用檔裡不得殘留任何硬寫死的使用者可見文字 ──
(function () {
  // 抓中日韓文字（註解除外——先把註解整段移除再檢查）
  // 註解含行首整行註解與程式碼後方的尾隨註解，兩種都要先剝掉才檢查
  const stripped = code
    .replace(/\/\*[\s\S]*?\*\//g, '')
    .replace(/\/\/[^\n]*/g, '');
  const cjk = stripped.match(/[一-鿿぀-ヿ가-힯]/g);
  ok('共用邏輯檔（排除註解）不含任何中日韓文字，確保文字都在字典裡', cjk === null);
})();

console.log(`\n2048 純邏輯回歸測試：${pass} 通過, ${fail} 失敗`);
process.exit(fail ? 1 : 0);
