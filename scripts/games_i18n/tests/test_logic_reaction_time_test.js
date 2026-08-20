// 反應力測試 純邏輯回歸測試 —— 對抽出後的 shared/reaction-time-test.js 重跑
const fs = require('fs'), path = require('path'), vm = require('vm');
const code = fs.readFileSync(path.join(__dirname, '..', 'out', 'games', 'shared', 'reaction-time-test.js'), 'utf8');
const ctx = { console, Math, Array, Object, String, Number, Infinity, globalThis: null };
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(code + `
globalThis.__exp = { rtRatingIndex, rtRatingLabel, rtComputeStats, greactiontimetestT, RT_CONFIG };`, ctx);
const X = ctx.__exp, C = X.RT_CONFIG;

let pass = 0, fail = 0;
const ok = (n, c) => { if (c) pass++; else { fail++; console.log('  ✗ ' + n); } };
const eq = (n, a, b) => ok(n, JSON.stringify(a) === JSON.stringify(b));

// ── 評分門檻：越快越好，所以是「毫秒越小級數越前面」，跟一般分數制方向相反，特別驗 ──
ok('150ms → 第0級（最快）', X.rtRatingIndex(150) === 0);
ok('200ms 邊界含 → 第0級', X.rtRatingIndex(200) === 0);
ok('201ms → 第1級', X.rtRatingIndex(201) === 1);
ok('250ms → 第1級', X.rtRatingIndex(250) === 1);
ok('300ms → 第2級', X.rtRatingIndex(300) === 2);
ok('380ms → 第3級', X.rtRatingIndex(380) === 3);
ok('500ms → 第4級', X.rtRatingIndex(500) === 4);
ok('9999ms → 第5級（最慢，封頂）', X.rtRatingIndex(9999) === 5);
ok('門檻共6級', C.ratingThresholds.length === 6);
(function () {
  // 單調性：反應時間越大，級數不可以往回跳
  let mono = true, prev = -1;
  for (let ms = 50; ms <= 1200; ms += 5) {
    const i = X.rtRatingIndex(ms);
    if (i < prev) mono = false;
    prev = i;
  }
  ok('級數隨毫秒數單調不遞減', mono);
})();

// ── 統計：最佳取最小值（不是最大值），平均四捨五入 ──
eq('空紀錄回傳null不回NaN', X.rtComputeStats([]), { best: null, avg: null });
eq('最佳是最小毫秒數', X.rtComputeStats([300, 210, 450]).best, 210);
ok('平均為整數', Number.isInteger(X.rtComputeStats([300, 210, 450]).avg));
ok('平均計算正確', X.rtComputeStats([300, 200, 400]).avg === 300);
ok('平均四捨五入', X.rtComputeStats([100, 101]).avg === 101);
ok('單筆時最佳與平均相同', (function () {
  const s = X.rtComputeStats([234]); return s.best === 234 && s.avg === 234;
})());

// ── 等待延遲區間設定（防止「固定節奏亂猜」的關鍵設計，數值不可被改動）──
ok('最短等待1500ms', C.minDelayMs === 1500);
ok('最長等待5000ms', C.maxDelayMs === 5000);
ok('最短小於最長', C.minDelayMs < C.maxDelayMs);
ok('四種狀態顏色都有定義',
   ['idle', 'waiting', 'ready', 'early'].every(k => typeof C.colors[k] === 'string' && C.colors[k]));

// ── i18n ──
ctx.window = { GAME_I18N: { msValue: '{ms} 毫秒', ratingLabels: ['A', 'B', 'C', 'D', 'E', 'F'] } };
ok('變數代入正確', X.greactiontimetestT('msValue', { ms: 233 }) === '233 毫秒');
ok('缺key回傳空字串不拋錯', X.greactiontimetestT('__nope__') === '');
ok('評語依index取文字', X.rtRatingLabel(150) === 'A' && X.rtRatingLabel(9999) === 'F');
ctx.window = {};
ok('字典不存在時不拋錯', X.rtRatingLabel(250) === '');

// ── 共用檔不得殘留硬寫死文字 ──
(function () {
  const stripped = code.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/[^\n]*/g, '');
  ok('共用邏輯檔（排除註解）不含中日韓文字', stripped.match(/[一-鿿぀-ヿ가-힯]/g) === null);
})();

console.log(`\n反應力測試 純邏輯回歸測試：${pass} 通過, ${fail} 失敗`);
process.exit(fail ? 1 : 0);
