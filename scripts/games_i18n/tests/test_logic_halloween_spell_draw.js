// 萬聖節塗鴉法術 純邏輯回歸測試
//
// 這款遊戲最核心、最容易被多語言重構改壞的是 $1 Unistroke Recognizer 手勢辨識演算法
// （閃電/星星/圓圈三種手繪形狀要能正確互相區分，原本程式註解宣稱「加了反方向範本之後
// 三種形狀互相誤判的機率依然是0%」——這個保證必須驗證還在），其次是波次/難度曲線的
// 純函式數學，以及「內部代號→翻譯後文字」查表（怪物名稱/法術形狀名稱）不能查錯位置。
const fs = require('fs'), path = require('path'), vm = require('vm');
const code = fs.readFileSync(path.join(__dirname, '..', 'shared', 'halloween-spell-draw.js'), 'utf8');
const ctx = {
  console, Math, Array, Object, String, Number, Infinity, JSON,
  performance: { now: () => 0 },
  window: undefined,
  document: undefined,
  navigator: undefined,
  globalThis: null,
};
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(code + `
globalThis.__exp = {
  hwPtDist, hwPathLen, hwResamplePoints, hwCentroidOf, hwIndicativeAngle, hwRotateByAngle,
  hwBoundingBoxOf, hwScaleToSquare, hwTranslateToOrigin, hwNormalizeGesture, hwPathDistance,
  hwDistanceAtAngle, hwDistanceAtBestAngle, hwMakeStarPoints, hwMakeLightningPoints, hwMakeCirclePoints,
  hwRecognizeGesture, hwMonsterName, hwShapeLabel, hwRatingIndex, hwComputeRating, hwComputeWave,
  hwComputeSpawnIntervalMs, hwComputeMonsterSpeed, hwComputeConcurrentCap, ghalloweenspelldrawT,
  HW_CONFIG, HW_RECOG, HW_RAW_TEMPLATES, HW_TEMPLATES, HW_MONSTER_TYPES, HW_SHAPE_META
};`, ctx);
const X = ctx.__exp, C = X.HW_CONFIG;

let pass = 0, fail = 0;
const ok = (n, c, d) => { if (c) pass++; else { fail++; console.log('  ✗ ' + n + (d ? ' — ' + d : '')); } };

// ── 小工具：模擬手繪 — 沿著理想範本點位加上隨機抖動與些微縮放/平移，
//    近似真人用手指/滑鼠畫出的不完美筆畫 ──
function jitterStroke(basePoints, opts) {
  opts = opts || {};
  const noise = opts.noise != null ? opts.noise : 4;
  const scale = opts.scale != null ? opts.scale : 1;
  const dx = opts.dx || 0, dy = opts.dy || 0;
  // 先用線性插值把範本的少數控制點加密成較多點，模擬滑鼠移動軌跡的取樣密度
  const dense = [];
  for (let i = 0; i < basePoints.length - 1; i++) {
    const a = basePoints[i], b = basePoints[i + 1];
    const steps = 8;
    for (let s = 0; s < steps; s++) {
      const t = s / steps;
      dense.push({ x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t });
    }
  }
  dense.push(basePoints[basePoints.length - 1]);
  return dense.map(p => ({
    x: p.x * scale + dx + (Math.random() - 0.5) * noise,
    y: p.y * scale + dy + (Math.random() - 0.5) * noise
  }));
}

// ── hwPtDist / hwPathLen：基本幾何 ──
ok('hwPtDist 兩點距離(3-4-5直角三角形)', X.hwPtDist({ x: 0, y: 0 }, { x: 3, y: 4 }) === 5);
ok('hwPathLen 單點路徑長度為0', X.hwPathLen([{ x: 0, y: 0 }]) === 0);
(function () {
  const square = [{ x: 0, y: 0 }, { x: 10, y: 0 }, { x: 10, y: 10 }, { x: 0, y: 10 }];
  ok('hwPathLen 正方形三邊路徑長度=30', Math.abs(X.hwPathLen(square) - 30) < 1e-9);
})();

// ── hwResamplePoints：重取樣後點數必須剛好等於指定的n ──
(function () {
  const raw = X.hwMakeCirclePoints();
  const resampled = X.hwResamplePoints(raw, 64);
  ok('hwResamplePoints 輸出點數等於指定的n', resampled.length === 64);
})();

// ── hwNormalizeGesture：正規化後應該置中在原點附近、且落在參考正方形尺度內 ──
(function () {
  const norm = X.hwNormalizeGesture(X.hwMakeLightningPoints());
  const c = X.hwCentroidOf(norm);
  ok('正規化後形心接近原點(0,0)', Math.abs(c.x) < 1e-6 && Math.abs(c.y) < 1e-6);
  const bb = X.hwBoundingBoxOf(norm);
  ok('正規化後寬或高其中一邊等於參考尺寸(SIZE=200)', Math.abs(bb.width - 200) < 1e-6 || Math.abs(bb.height - 200) < 1e-6);
})();

// ── HW_TEMPLATES：每個形狀存了「原始+反方向」共2份範本，3形狀=6份 ──
ok('HW_RAW_TEMPLATES 有3種形狀(閃電/星星/圓圈)', X.HW_RAW_TEMPLATES.length === 3);
ok('HW_TEMPLATES 每形狀存正反2份，共6份範本', X.HW_TEMPLATES.length === 6);
ok('HW_RAW_TEMPLATES 不含label欄位（文字已抽離到i18n）', X.HW_RAW_TEMPLATES.every(t => !('label' in t)));

// ── hwRecognizeGesture：核心正確性 — 大量隨機模擬「手繪抖動版」的三種形狀，
//    驗證原程式註解宣稱的「三種形狀互相誤判機率是0%」這個保證在重構後依然成立 ──
(function () {
  const shapeMakers = {
    lightning: X.hwMakeLightningPoints,
    star: X.hwMakeStarPoints,
    circle: X.hwMakeCirclePoints
  };
  const TRIALS_PER_SHAPE = 60;
  let correct = 0, total = 0, misclassified = [];
  Object.keys(shapeMakers).forEach(shapeName => {
    for (let t = 0; t < TRIALS_PER_SHAPE; t++) {
      const base = shapeMakers[shapeName]();
      // 一半模擬正方向畫，一半模擬反方向畫（原始論文提到方向敏感性問題）
      const pts = (t % 2 === 0) ? base : base.slice().reverse();
      const stroke = jitterStroke(pts, { noise: 3, scale: 0.9 + Math.random() * 0.3, dx: Math.random() * 20, dy: Math.random() * 20 });
      const result = X.hwRecognizeGesture(stroke, ['lightning', 'star', 'circle']);
      total++;
      if (result && result.name === shapeName) correct++;
      else misclassified.push(shapeName + '→' + (result ? result.name : 'null'));
    }
  });
  ok('模擬' + total + '次手繪抖動辨識，正確率100%（0%互相誤判）', correct === total,
     misclassified.slice(0, 5).join(', '));
})();

// ── hwRecognizeGesture：防錯 — 點數太少 / 幾乎沒移動時安全回傳null，不拋錯 ──
ok('點數低於strokeMinPoints時回傳null', X.hwRecognizeGesture([{ x: 0, y: 0 }, { x: 1, y: 1 }], ['lightning']) === null);
ok('幾乎沒有移動的點擊回傳null(路徑長度<20)', X.hwRecognizeGesture([{ x: 0, y: 0 }, { x: 1, y: 0 }, { x: 2, y: 0 }, { x: 3, y: 0 }], ['lightning']) === null);
ok('空/undefined筆畫回傳null不拋錯', X.hwRecognizeGesture(null, ['lightning']) === null);
(function () {
  // allowedNames 限縮辨識範圍：即使畫的是圓圈，若圓圈被鎖住(不在allowedNames)，也絕不會回傳circle
  const stroke = jitterStroke(X.hwMakeCirclePoints(), { noise: 2 });
  const result = X.hwRecognizeGesture(stroke, ['lightning', 'star']); // circle 被排除在允許清單外
  ok('allowedNames限制生效：圓圈被鎖時絕不會辨識成circle', !result || result.name !== 'circle');
})();

// ── hwMonsterName / hwShapeLabel：內部代號→翻譯文字查表，缺字典/查無索引時安全回傳空字串 ──
ctx.window = { GAME_I18N: { monsterNames: ['南瓜怪', '幽靈', '蝙蝠', '女巫幽魂'], shapeNames: ['閃電', '星星', '圓圈'] } };
ok('hwMonsterName 依內部代號取正確翻譯(pumpkin)', X.hwMonsterName('pumpkin') === '南瓜怪');
ok('hwMonsterName 依內部代號取正確翻譯(witch，最後一個)', X.hwMonsterName('witch') === '女巫幽魂');
ok('hwShapeLabel 依內部代號取正確翻譯(circle，最後一個)', X.hwShapeLabel('circle') === '圓圈');
ok('hwMonsterName 查無此代號時回傳空字串不拋錯', X.hwMonsterName('__nope__') === '');
ctx.window = {};
ok('hwMonsterName 字典不存在時回傳空字串不拋錯', X.hwMonsterName('pumpkin') === '');
ok('hwShapeLabel 字典不存在時回傳空字串不拋錯', X.hwShapeLabel('circle') === '');
(function () {
  // HW_CONFIG.monsterNames / shapeNames 內部代號順序，必須跟 HW_MONSTER_TYPES / HW_RAW_TEMPLATES 資料順序一一對應
  const cfgKeys = C.monsterNames;
  const dataKeys = X.HW_MONSTER_TYPES.map(t => t.key);
  ok('HW_CONFIG.monsterNames 順序跟 HW_MONSTER_TYPES 資料順序一致', JSON.stringify(cfgKeys) === JSON.stringify(dataKeys));
  const shapeCfgKeys = C.shapeNames;
  const shapeDataKeys = X.HW_RAW_TEMPLATES.map(t => t.name);
  ok('HW_CONFIG.shapeNames 順序跟 HW_RAW_TEMPLATES 資料順序一致', JSON.stringify(shapeCfgKeys) === JSON.stringify(shapeDataKeys));
})();

// ── hwComputeWave：每消滅 waveThreshold(6) 隻怪物升一波 ──
ok('第0隻擊殺時是第1波', X.hwComputeWave(0) === 1);
ok('第5隻擊殺時仍是第1波(未滿6)', X.hwComputeWave(5) === 1);
ok('第6隻擊殺時升到第2波', X.hwComputeWave(6) === 2);
ok('第11隻擊殺時仍是第2波', X.hwComputeWave(11) === 2);
ok('第12隻擊殺時升到第3波', X.hwComputeWave(12) === 3);

// ── hwComputeSpawnIntervalMs：波數越高間隔越短，且不會低於下限 ──
ok('第1波間隔=起始值', X.hwComputeSpawnIntervalMs(1) === C.spawnIntervalStartMs);
ok('波數越高間隔越短', X.hwComputeSpawnIntervalMs(5) < X.hwComputeSpawnIntervalMs(1));
ok('間隔永遠不低於下限spawnIntervalMinMs', X.hwComputeSpawnIntervalMs(999) === C.spawnIntervalMinMs);

// ── hwComputeMonsterSpeed：波數越高速度越快，且不會超過上限 ──
ok('第1波速度=起始值', X.hwComputeMonsterSpeed(1) === C.monsterSpeedStartPxPerSec);
ok('波數越高速度越快', X.hwComputeMonsterSpeed(5) > X.hwComputeMonsterSpeed(1));
ok('速度永遠不超過上限monsterSpeedMaxPxPerSec', X.hwComputeMonsterSpeed(999) === C.monsterSpeedMaxPxPerSec);

// ── hwComputeConcurrentCap：每隔concurrentCapStepEveryWaves(2)波上限+1，封頂在concurrentCapMax ──
ok('第1波同時存在上限=起始值', X.hwComputeConcurrentCap(1) === C.concurrentCapStart);
ok('第2波仍是起始值(還沒滿2波間隔)', X.hwComputeConcurrentCap(2) === C.concurrentCapStart);
ok('第3波上限+1', X.hwComputeConcurrentCap(3) === C.concurrentCapStart + 1);
ok('上限永遠不超過concurrentCapMax', X.hwComputeConcurrentCap(999) === C.concurrentCapMax);

// ── hwRatingIndex / hwComputeRating：評分門檻共5級 ──
ok('評分門檻共5級', C.ratingThresholds.length === 5);
ok('0分 → 第0級', X.hwRatingIndex(0) === 0);
ok('40分邊界含 → 第0級', X.hwRatingIndex(40) === 0);
ok('41分 → 第1級', X.hwRatingIndex(41) === 1);
ok('100分邊界含 → 第1級', X.hwRatingIndex(100) === 1);
ok('200分邊界含 → 第2級', X.hwRatingIndex(200) === 2);
ok('350分邊界含 → 第3級', X.hwRatingIndex(350) === 3);
ok('351分 → 第4級(最高，封頂)', X.hwRatingIndex(351) === 4);
ok('99999分 → 第4級(封頂不越界)', X.hwRatingIndex(99999) === 4);
(function () {
  let mono = true, prev = -1;
  for (let s = 0; s <= 600; s += 5) {
    const i = X.hwRatingIndex(s);
    if (i < prev) mono = false;
    prev = i;
  }
  ok('評分級數隨分數單調不遞減', mono);
})();
ctx.window = { GAME_I18N: { ratings: ['A', 'B', 'C', 'D', 'E'] } };
ok('依分數取對應評語文字', X.hwComputeRating(0) === 'A' && X.hwComputeRating(99999) === 'E');
ctx.window = {};
ok('字典不存在時評語回傳空字串不拋錯', X.hwComputeRating(0) === '');

// ── ghalloweenspelldrawT：i18n取字helper ──
ctx.window = { GAME_I18N: { hello: '哈囉 {n} 次' } };
ok('取字並代換變數', X.ghalloweenspelldrawT('hello', { n: 3 }) === '哈囉 3 次');
ok('缺key回傳空字串不拋錯', X.ghalloweenspelldrawT('__nope__') === '');
ctx.window = {};
ok('字典不存在時不拋錯', X.ghalloweenspelldrawT('hello') === '');

// ── 共用檔不得殘留硬寫死文字 ──
(function () {
  const stripped = code.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/[^\n]*/g, '');
  const cjk = stripped.match(/[一-鿿぀-ヿ가-힯]/g);
  ok('共用邏輯檔（排除註解）不含中日韓文字', cjk === null,
     cjk ? [...new Set(cjk)].join('').slice(0, 40) : '');
})();

console.log(`\n萬聖節塗鴉法術 純邏輯回歸測試：${pass} 通過, ${fail} 失敗`);
process.exit(fail ? 1 : 0);
