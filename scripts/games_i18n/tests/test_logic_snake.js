// 貪食蛇 純邏輯回歸測試 —— 對抽出後的 shared/snake.js 重跑，確認多語言化重構沒動到規則
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const code = fs.readFileSync(path.join(__dirname, '..', 'out', 'games', 'shared', 'snake.js'), 'utf8');
const ctx = { console, Math, Array, Object, String, Number, Infinity, globalThis: null };
ctx.globalThis = ctx;
vm.createContext(ctx);
// vm 裡宣告的 const 不會外洩到呼叫端，要在同一次執行裡掛到 globalThis 才能引用
vm.runInContext(code + `
globalThis.__exp = { snNextHead, snIsOutOfBounds, snIsSelfCollision, snRatingIndex,
  snComputeRating, snComputeLevel, gsnakeT, SNAKE_CONFIG };
`, ctx);
const X = ctx.__exp;
const C = X.SNAKE_CONFIG;

let pass = 0, fail = 0;
const ok = (n, c) => { if (c) pass++; else { fail++; console.log('  ✗ ' + n); } };
const eq = (n, a, b) => ok(n, JSON.stringify(a) === JSON.stringify(b));

// ── 移動方向 ──
eq('往上 y-1', X.snNextHead({ x: 5, y: 5 }, 'up'), { x: 5, y: 4 });
eq('往下 y+1', X.snNextHead({ x: 5, y: 5 }, 'down'), { x: 5, y: 6 });
eq('往左 x-1', X.snNextHead({ x: 5, y: 5 }, 'left'), { x: 4, y: 5 });
eq('往右 x+1', X.snNextHead({ x: 5, y: 5 }, 'right'), { x: 6, y: 5 });

// ── 撞牆判定（四個邊界都要測，含剛好在界內的邊緣格）──
const n = C.gridSize;
ok('左出界', X.snIsOutOfBounds({ x: -1, y: 5 }) === true);
ok('上出界', X.snIsOutOfBounds({ x: 5, y: -1 }) === true);
ok('右出界', X.snIsOutOfBounds({ x: n, y: 5 }) === true);
ok('下出界', X.snIsOutOfBounds({ x: 5, y: n }) === true);
ok('左上角在界內', X.snIsOutOfBounds({ x: 0, y: 0 }) === false);
ok('右下角在界內', X.snIsOutOfBounds({ x: n - 1, y: n - 1 }) === false);

// ── 咬到自己判定 ──
const body = [{ x: 3, y: 3 }, { x: 3, y: 4 }, { x: 3, y: 5 }];
ok('撞到蛇身 → true', X.snIsSelfCollision({ x: 3, y: 4 }, body) === true);
ok('沒撞到 → false', X.snIsSelfCollision({ x: 9, y: 9 }, body) === false);
ok('空身體不會誤判', X.snIsSelfCollision({ x: 1, y: 1 }, []) === false);

// ── 反方向對照表：這是「不能180度掉頭」規則的資料來源，必須四個方向都正確互為反向 ──
ok('up 的反向是 down', C.opposite.up === 'down');
ok('down 的反向是 up', C.opposite.down === 'up');
ok('left 的反向是 right', C.opposite.left === 'right');
ok('right 的反向是 left', C.opposite.right === 'left');
ok('反向表互為對稱（套兩次回到自己）',
   ['up', 'down', 'left', 'right'].every(d => C.opposite[C.opposite[d]] === d));

// ── 速度遞增：吃越多越快，但有下限不會快到無法操作 ──
(function () {
  const tickAt = s => Math.max(C.minTickMs, C.initialTickMs - s * C.tickDecreasePerFood);
  ok('起始速度等於設定值', tickAt(0) === C.initialTickMs);
  ok('吃到食物後間隔變短（變快）', tickAt(1) < tickAt(0));
  let monotonic = true;
  for (let s = 1; s <= 100; s++) if (tickAt(s) > tickAt(s - 1)) monotonic = false;
  ok('速度隨分數單調遞增，不會忽快忽慢', monotonic);
  ok('速度有下限封頂，不會無限加速', tickAt(9999) === C.minTickMs);
})();

// ── 等級計算 ──
ok('0分是第1級', X.snComputeLevel(0) === 1);
ok('每 scorePerLevel 分升一級', X.snComputeLevel(C.scorePerLevel) === 2);
(function () {
  let monotonic = true;
  for (let s = 1; s <= 200; s++) if (X.snComputeLevel(s) < X.snComputeLevel(s - 1)) monotonic = false;
  ok('等級隨分數單調不遞減', monotonic);
})();

// ── 評語分級：門檻對應必須跟重構前一致 ──
ok('0分 → 第0級', X.snRatingIndex(0) === 0);
ok('5分（邊界含）→ 第0級', X.snRatingIndex(5) === 0);
ok('6分 → 第1級', X.snRatingIndex(6) === 1);
ok('12分 → 第1級', X.snRatingIndex(12) === 1);
ok('20分 → 第2級', X.snRatingIndex(20) === 2);
ok('30分 → 第3級', X.snRatingIndex(30) === 3);
ok('999分 → 第4級（封頂）', X.snRatingIndex(999) === 4);
ok('門檻數量為5', C.ratingThresholds.length === 5);

// ── i18n 取字 ──
ctx.window = { GAME_I18N: { levelBadge: 'Lv.{n}', ratings: ['A', 'B', 'C', 'D', 'E'] } };
ok('變數代入正確', X.gsnakeT('levelBadge', { n: 7 }) === 'Lv.7');
ok('缺key回傳空字串不拋錯', X.gsnakeT('__nope__') === '');
ok('評語依index取對應語言文字', X.snComputeRating(0) === 'A' && X.snComputeRating(999) === 'E');
ctx.window = {};
ok('字典不存在時不拋錯', X.snComputeRating(10) === '');

// ── 共用檔不得殘留硬寫死的使用者可見文字 ──
(function () {
  const stripped = code.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/[^\n]*/g, '');
  const cjk = stripped.match(/[一-鿿぀-ヿ가-힯]/g);
  ok('共用邏輯檔（排除註解）不含中日韓文字', cjk === null);
})();

console.log(`\n貪食蛇 純邏輯回歸測試：${pass} 通過, ${fail} 失敗`);
process.exit(fail ? 1 : 0);
