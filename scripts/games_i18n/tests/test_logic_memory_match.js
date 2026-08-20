// 記憶翻牌 純邏輯回歸測試
//
// 這款遊戲的核心正確性在於「牌堆一定要是8組完整配對、洗牌後仍然如此」。
// 多語言重構把 mmBuildDeck/mmShuffle 搬到 shared/memory-match.js，這裡驗證
// 產牌邏輯沒有被改到：牌數、配對完整性、洗牌演算法的正確性都要核對。
const fs = require('fs'), path = require('path'), vm = require('vm');
const code = fs.readFileSync(path.join(__dirname, '..', 'shared', 'memory-match.js'), 'utf8');
const ctx = { console, Math, Array, Object, String, Number, Infinity, globalThis: null };
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(code + `
globalThis.__exp = { mmShuffle, mmBuildDeck, gmemorymatchT, MM_CONFIG };`, ctx);
const X = ctx.__exp, C = X.MM_CONFIG;

let pass = 0, fail = 0;
const ok = (n, c, d) => { if (c) pass++; else { fail++; console.log('  ✗ ' + n + (d ? ' — ' + d : '')); } };

// ── CONFIG 基本設定 ──
ok('8組配對設定', C.pairCount === 8);
ok('提供至少8種圖案', C.symbols.length >= C.pairCount);
ok('圖案不重複', new Set(C.symbols).size === C.symbols.length);

// ── mmBuildDeck：牌堆正確性（這是這款遊戲最核心的規則）──
(function () {
  let allOk = true;
  for (let trial = 0; trial < 50; trial++) {
    const deck = X.mmBuildDeck();
    if (deck.length !== C.pairCount * 2) { allOk = false; break; }
    // 每張牌一開始都要是蓋著、未配對的狀態
    if (!deck.every(c => c.flipped === false && c.matched === false)) { allOk = false; break; }
    // id必須是0..15不重複（畫面渲染跟點擊事件靠id對應）
    const ids = deck.map(c => c.id).sort((a, b) => a - b);
    for (let i = 0; i < ids.length; i++) if (ids[i] !== i) { allOk = false; break; }
    // 每種圖案恰好出現2次（配對遊戲的核心：不能有落單或超過2張的圖案）
    const counts = {};
    deck.forEach(c => { counts[c.symbol] = (counts[c.symbol] || 0) + 1; });
    const symbolKeys = Object.keys(counts);
    if (symbolKeys.length !== C.pairCount) { allOk = false; break; }
    if (!symbolKeys.every(k => counts[k] === 2)) { allOk = false; break; }
  }
  ok('產50副牌，每副都恰好16張、8種圖案各出現2次、id為0-15不重複', allOk);
})();

// ── mmShuffle：洗牌後仍是同一組元素（只是順序變了），且不修改原陣列 ──
(function () {
  const original = [1, 2, 3, 4, 5, 6, 7, 8];
  const shuffled = X.mmShuffle(original);
  ok('洗牌後長度不變', shuffled.length === original.length);
  ok('洗牌後元素集合不變（只是順序打亂）',
     JSON.stringify(shuffled.slice().sort()) === JSON.stringify(original.slice().sort()));
  ok('不修改原陣列（回傳新陣列，避免呼叫端資料被意外改動）',
     JSON.stringify(original) === JSON.stringify([1, 2, 3, 4, 5, 6, 7, 8]));
})();

// ── mmShuffle：真的有打亂（不是每次都回傳原順序）──
(function () {
  const original = Array.from({ length: 20 }, (_, i) => i);
  let anyDifferent = false;
  for (let i = 0; i < 20; i++) {
    const shuffled = X.mmShuffle(original);
    if (JSON.stringify(shuffled) !== JSON.stringify(original)) { anyDifferent = true; break; }
  }
  ok('20次洗牌至少有一次順序真的改變了（不是恆等函式）', anyDifferent);
})();

// ── i18n ──
ok('缺key回傳空字串不拋錯', X.gmemorymatchT('__nope__') === '');
ctx.window = { GAME_I18N: { movesShort: '{m}手' } };
ok('變數代入正確', X.gmemorymatchT('movesShort', { m: 12 }) === '12手');

// ── 共用檔不得殘留硬寫死文字 ──
(function () {
  const stripped = code.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/[^\n]*/g, '');
  const cjk = stripped.match(/[一-鿿぀-ヿ가-힯]/g);
  ok('共用邏輯檔（排除註解）不含中日韓文字', cjk === null,
     cjk ? [...new Set(cjk)].join('').slice(0, 40) : '');
})();

console.log(`\n記憶翻牌 純邏輯回歸測試：${pass} 通過, ${fail} 失敗`);
process.exit(fail ? 1 : 0);
