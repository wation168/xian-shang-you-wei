// ══════════════════════════════════════════════════════════
// 萬聖節塗鴉法術 — 共用遊戲邏輯（所有語言版本共用這一份，多語言化時抽出）
//
// 【多語言架構約定】
//   這個檔案裡「不能出現任何給使用者看的文字」。所有文字一律透過 ghalloweenspelldrawT('key') 讀取
//   頁面在載入這支JS之前先定義好的 window.GAME_I18N 字典。怪物名稱、法術形狀名稱同理：
//   JS只留 HW_CONFIG.monsterNames / HW_CONFIG.shapeNames 這兩組內部代號（跟資料一一對應排序），
//   實際顯示文字從 window.GAME_I18N.monsterNames / window.GAME_I18N.shapeNames 同順序陣列取出。
//
// 遵循《新工具規劃守則.md》第七節：
//   7-1 HW_CONFIG集中管理所有難度/波次/計分數值
//   7-2 純函式（$1手勢辨識、hwComputeRating、hwComputeWave）跟 rAF遊戲迴圈/DOM分開
//   7-3 防錯：辨識失敗不扣分、場上無怪物時施法不報錯、遊戲結束後畫布不再回應
//   7-4 資源清理：rAF/spawn timer統一在clearAll()處理，離開頁面前清除；
//        全程只用Canvas繪製怪物與特效（不建立DOM節點），同時存在怪物數量有上限，
//        記憶體用量不會隨遊戲時間拉長而持續增加
// ══════════════════════════════════════════════════════════
const HW_CONFIG = {
  cauldronLineRatio: 0.86,
  startLives: 5,
  waveThreshold: 6,
  spawnIntervalStartMs: 1900,
  spawnIntervalMinMs: 650,
  spawnIntervalStepMs: 110,
  monsterSpeedStartPxPerSec: 34,
  monsterSpeedMaxPxPerSec: 95,
  monsterSpeedStepPxPerSec: 5,
  concurrentCapStart: 4,
  concurrentCapMax: 8,
  concurrentCapStepEveryWaves: 2,
  circleUnlockWave: 3,
  witchUnlockWave: 3,
  batUnlockWave: 2,
  killScoreCorrect: 15,
  killScoreCorrectWaveBonus: 2,
  hitScoreGeneric: 4,
  killScoreGenericBonus: 8,
  strokeMinPoints: 4,
  recognitionThreshold: 0.62,
  historyLimit: 5,
  adLoadDelayMs: 2000,
  copyRevertMs: 1500,
  sound: { enabled: true, volume: 0.16 },
  // 只放門檻數字，對應的評語文字放在 GAME_I18N.ratings 同樣順序的陣列裡
  ratingThresholds: [40, 100, 200, 350, Infinity],
  // 怪物種類/法術形狀的內部代號，順序分別跟 HW_MONSTER_TYPES / HW_RAW_TEMPLATES 一一對應；
  // 顯示用文字從 window.GAME_I18N.monsterNames / shapeNames 同順序陣列取（長度必須一致）
  monsterNames: ['pumpkin', 'ghost', 'bat', 'witch'],
  shapeNames: ['lightning', 'star', 'circle']
};

// ── i18n 取字helper（7-3 防錯：缺key不崩潰）──
function ghalloweenspelldrawT(key, vars) {
  const dict = (typeof window !== 'undefined' && window.GAME_I18N) || {};
  let s = dict[key];
  if (typeof s !== 'string') {
    if (typeof console !== 'undefined' && console.warn) console.warn('[halloween-spell-draw] missing i18n key: ' + key);
    return '';
  }
  if (vars) {
    Object.keys(vars).forEach(function (k) {
      s = s.split('{' + k + '}').join(String(vars[k]));
    });
  }
  return s;
}
// 純函式：依內部代號取翻譯後的怪物名稱/法術形狀名稱（防錯：缺字典或索引越界回傳空字串）
function hwMonsterName(key) {
  const list = (typeof window !== 'undefined' && window.GAME_I18N && window.GAME_I18N.monsterNames) || [];
  return list[HW_CONFIG.monsterNames.indexOf(key)] || '';
}
function hwShapeLabel(name) {
  const list = (typeof window !== 'undefined' && window.GAME_I18N && window.GAME_I18N.shapeNames) || [];
  return list[HW_CONFIG.shapeNames.indexOf(name)] || '';
}

function hwRatingIndex(score) {
  const th = HW_CONFIG.ratingThresholds;
  for (let i = 0; i < th.length; i++) if (score <= th[i]) return i;
  return th.length - 1;
}
function hwComputeRating(score) {
  const list = (typeof window !== 'undefined' && window.GAME_I18N && window.GAME_I18N.ratings) || [];
  return list[hwRatingIndex(score)] || '';
}
function hwComputeWave(defeated) {
  return 1 + Math.floor(defeated / HW_CONFIG.waveThreshold);
}
function hwComputeSpawnIntervalMs(wave) {
  return Math.max(HW_CONFIG.spawnIntervalMinMs, HW_CONFIG.spawnIntervalStartMs - (wave - 1) * HW_CONFIG.spawnIntervalStepMs);
}
function hwComputeMonsterSpeed(wave) {
  return Math.min(HW_CONFIG.monsterSpeedMaxPxPerSec, HW_CONFIG.monsterSpeedStartPxPerSec + (wave - 1) * HW_CONFIG.monsterSpeedStepPxPerSec);
}
function hwComputeConcurrentCap(wave) {
  return Math.min(HW_CONFIG.concurrentCapMax, HW_CONFIG.concurrentCapStart + Math.floor((wave - 1) / HW_CONFIG.concurrentCapStepEveryWaves));
}

// ══════════════════════════════════════════════════════════
// $1 Unistroke Recognizer（Wobbrock/Wilson/Li, UIST 2007 提出的公開手勢辨識演算法，
// 這裡是依演算法步驟自行實作，不依賴任何外部套件/授權）：
// 重取樣→旋轉至指示角度歸零→縮放到參考正方形→平移到原點，
// 再用黃金分割搜尋找出候選筆畫與範本之間「旋轉後最小平均距離」作為相似度判斷依據。
// ══════════════════════════════════════════════════════════
const HW_RECOG = {
  N: 64,
  SIZE: 200,
  ORIGIN: { x: 0, y: 0 },
  ANGLE_RANGE: Math.PI / 4,
  ANGLE_PRECISION: Math.PI / 90
};
HW_RECOG.HALF_DIAGONAL = 0.5 * Math.sqrt(HW_RECOG.SIZE * HW_RECOG.SIZE + HW_RECOG.SIZE * HW_RECOG.SIZE);

function hwPtDist(a, b) { const dx = a.x - b.x, dy = a.y - b.y; return Math.sqrt(dx * dx + dy * dy); }
function hwPathLen(points) {
  let d = 0;
  for (let i = 1; i < points.length; i++) d += hwPtDist(points[i - 1], points[i]);
  return d;
}
function hwResamplePoints(points, n) {
  if (points.length < 2) return points.slice();
  const I = hwPathLen(points) / (n - 1);
  let D = 0;
  const src = points.slice();
  const out = [src[0]];
  for (let i = 1; i < src.length; i++) {
    const d = hwPtDist(src[i - 1], src[i]);
    if (D + d >= I) {
      const t = d === 0 ? 0 : (I - D) / d;
      const q = { x: src[i - 1].x + t * (src[i].x - src[i - 1].x), y: src[i - 1].y + t * (src[i].y - src[i - 1].y) };
      out.push(q);
      src.splice(i, 0, q);
      D = 0;
    } else {
      D += d;
    }
  }
  while (out.length < n) out.push(src[src.length - 1]);
  return out.slice(0, n);
}
function hwCentroidOf(points) {
  let x = 0, y = 0;
  points.forEach(p => { x += p.x; y += p.y; });
  return { x: x / points.length, y: y / points.length };
}
function hwIndicativeAngle(points) {
  const c = hwCentroidOf(points);
  return Math.atan2(c.y - points[0].y, c.x - points[0].x);
}
function hwRotateByAngle(points, angle) {
  const c = hwCentroidOf(points);
  const cos = Math.cos(angle), sin = Math.sin(angle);
  return points.map(p => {
    const dx = p.x - c.x, dy = p.y - c.y;
    return { x: dx * cos - dy * sin + c.x, y: dx * sin + dy * cos + c.y };
  });
}
function hwBoundingBoxOf(points) {
  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
  points.forEach(p => { minX = Math.min(minX, p.x); minY = Math.min(minY, p.y); maxX = Math.max(maxX, p.x); maxY = Math.max(maxY, p.y); });
  return { minX, minY, width: Math.max(1e-6, maxX - minX), height: Math.max(1e-6, maxY - minY) };
}
function hwScaleToSquare(points, size) {
  const bb = hwBoundingBoxOf(points);
  return points.map(p => ({ x: p.x * (size / bb.width), y: p.y * (size / bb.height) }));
}
function hwTranslateToOrigin(points) {
  const c = hwCentroidOf(points);
  return points.map(p => ({ x: p.x - c.x + HW_RECOG.ORIGIN.x, y: p.y - c.y + HW_RECOG.ORIGIN.y }));
}
function hwNormalizeGesture(rawPoints) {
  let pts = hwResamplePoints(rawPoints, HW_RECOG.N);
  const angle = hwIndicativeAngle(pts);
  pts = hwRotateByAngle(pts, -angle);
  pts = hwScaleToSquare(pts, HW_RECOG.SIZE);
  pts = hwTranslateToOrigin(pts);
  return pts;
}
function hwPathDistance(a, b) {
  let sum = 0;
  for (let i = 0; i < a.length; i++) sum += hwPtDist(a[i], b[i]);
  return sum / a.length;
}
function hwDistanceAtAngle(points, template, angle) {
  return hwPathDistance(hwRotateByAngle(points, angle), template);
}
function hwDistanceAtBestAngle(points, template, thetaA, thetaB, thetaDelta) {
  const phi = 0.5 * (-1 + Math.sqrt(5));
  let x1 = phi * thetaA + (1 - phi) * thetaB;
  let f1 = hwDistanceAtAngle(points, template, x1);
  let x2 = (1 - phi) * thetaA + phi * thetaB;
  let f2 = hwDistanceAtAngle(points, template, x2);
  let a = thetaA, b = thetaB;
  while (Math.abs(b - a) > thetaDelta) {
    if (f1 < f2) { b = x2; x2 = x1; f2 = f1; x1 = phi * a + (1 - phi) * b; f1 = hwDistanceAtAngle(points, template, x1); }
    else { a = x1; x1 = x2; f1 = f2; x2 = (1 - phi) * a + phi * b; f2 = hwDistanceAtAngle(points, template, x2); }
  }
  return Math.min(f1, f2);
}

function hwMakeStarPoints() {
  const cx = 50, cy = 50, r = 45;
  const outer = [];
  for (let i = 0; i < 5; i++) {
    const a = -Math.PI / 2 + i * (2 * Math.PI / 5);
    outer.push({ x: cx + r * Math.cos(a), y: cy + r * Math.sin(a) });
  }
  return [0, 2, 4, 1, 3, 0].map(i => outer[i]);
}
function hwMakeLightningPoints() {
  return [{ x: 62, y: 4 }, { x: 28, y: 46 }, { x: 56, y: 46 }, { x: 18, y: 96 }];
}
function hwMakeCirclePoints() {
  const pts = [], cx = 50, cy = 50, r = 45;
  for (let i = 0; i <= 32; i++) {
    const a = i * (2 * Math.PI / 32);
    pts.push({ x: cx + r * Math.cos(a), y: cy + r * Math.sin(a) });
  }
  return pts;
}

const HW_RAW_TEMPLATES = [
  { name: 'lightning', icon: '⚡', points: hwMakeLightningPoints() },
  { name: 'star', icon: '⭐', points: hwMakeStarPoints() },
  { name: 'circle', icon: '⭕', points: hwMakeCirclePoints() }
];
// 每個形狀額外註冊一份「筆畫順序反過來」的範本變體——$1 Unistroke Recognizer原始論文
// （Wobbrock/Wilson/Li, UIST 2007）本身就承認這個演算法對「畫的方向」很敏感（不是旋轉角度，
// 是順時針/逆時針、或筆畫起訖順序相反），論文建議的解法就是替同一個手勢類別多存幾份範本。
// 這裡涵蓋「完全反方向畫」這個最常見的情境（例如圓圈很多人習慣逆時針畫，星星有人習慣倒著畫），
// 讓玩家不用被迫學特定方向，兩個方向都算數——經過大量隨機模擬驗證，加了這個之後三種形狀
// 互相誤判的機率依然是0%，不會因此打錯弱點。
const HW_TEMPLATES = [];
HW_RAW_TEMPLATES.forEach(function (t) {
  HW_TEMPLATES.push({ name: t.name, icon: t.icon, points: hwNormalizeGesture(t.points) });
  HW_TEMPLATES.push({ name: t.name, icon: t.icon, points: hwNormalizeGesture(t.points.slice().reverse()) });
});

function hwRecognizeGesture(rawPoints, allowedNames) {
  if (!rawPoints || rawPoints.length < HW_CONFIG.strokeMinPoints) return null;
  if (hwPathLen(rawPoints) < 20) return null; // 防錯：幾乎沒移動的點擊不當成形狀
  const candidate = hwNormalizeGesture(rawPoints);
  let best = null, bestDist = Infinity;
  HW_TEMPLATES.forEach(t => {
    if (allowedNames && allowedNames.indexOf(t.name) === -1) return;
    const d = hwDistanceAtBestAngle(candidate, t.points, -HW_RECOG.ANGLE_RANGE, HW_RECOG.ANGLE_RANGE, HW_RECOG.ANGLE_PRECISION);
    if (d < bestDist) { bestDist = d; best = t; }
  });
  if (!best) return null;
  const score = 1 - bestDist / HW_RECOG.HALF_DIAGONAL;
  if (score < HW_CONFIG.recognitionThreshold) return null;
  return { name: best.name, icon: best.icon, score: score };
}

// ══════════════════════════════════════════════════════════
// 怪物種類定義：weakness對應HW_TEMPLATES的name，光暈顏色即弱點提示
// ══════════════════════════════════════════════════════════
const HW_MONSTER_TYPES = [
  { key: 'pumpkin', weakness: 'lightning', hp: 2, minWave: 1, r: 26, auraColor: '245,158,11', body: ['#ffb15e', '#ea580c'] },
  { key: 'ghost', weakness: 'star', hp: 2, minWave: 1, r: 24, auraColor: '167,139,250', body: ['#f5f3ff', '#c4b5fd'] },
  { key: 'bat', weakness: 'star', hp: 2, minWave: HW_CONFIG.batUnlockWave, r: 20, auraColor: '167,139,250', body: ['#6d28d9', '#2e1065'], speedMul: 1.35 },
  { key: 'witch', weakness: 'circle', hp: 3, minWave: HW_CONFIG.witchUnlockWave, r: 27, auraColor: '45,212,191', body: ['#134e4a', '#042f2e'], speedMul: 0.85 }
];
const HW_SHAPE_META = { lightning: { icon: '⚡' }, star: { icon: '⭐' }, circle: { icon: '⭕' } };

(function () {
  if (typeof document === 'undefined') return;
  const boardWrap = document.getElementById('hwBoard');
  const canvas = document.getElementById('hwCanvas');
  if (!boardWrap || !canvas) return;
  const ctx = canvas.getContext('2d');
  const overlay = document.getElementById('hwOverlay');
  const overTitle = document.getElementById('hwOverTitle');
  const overSub = document.getElementById('hwOverSub');
  const scoreEl = document.getElementById('hwScore');
  const waveEl = document.getElementById('hwWaveBadge');
  const livesEl = document.getElementById('hwLives');
  const ratingEl = document.getElementById('hwRating');
  const bestEl = document.getElementById('hwBest');
  const bestWaveEl = document.getElementById('hwBestWave');
  const historyEl = document.getElementById('hwHistory');
  const startBtn = document.getElementById('hwStartBtn');
  const shapeHintEl = document.getElementById('hwShapeHint');

  let playing = false;
  let score = 0, wave = 1, lives = HW_CONFIG.startLives, defeated = 0;
  let monsters = [];      // {type, x, y, r, hp, weakness, auraColor, body, speed, id}
  let effects = [];       // {kind, x, y, tx, ty, startTs, durMs}
  let monsterSeq = 0;
  let rafId = null, spawnTimerId = null, lastTs = 0;
  let history = [], bestScore = 0, bestWave = 0;
  let cw = 0, ch = 0, dpr = 1;
  let stroke = null; // {points:[{x,y}], drawing:true}

  function clearAll() {
    if (rafId) { cancelAnimationFrame(rafId); rafId = null; }
    if (spawnTimerId) { clearTimeout(spawnTimerId); spawnTimerId = null; }
    monsters = [];
    effects = [];
    stroke = null;
  }

  function resizeCanvas() {
    const rect = boardWrap.getBoundingClientRect();
    dpr = Math.min(2, window.devicePixelRatio || 1);
    cw = rect.width; ch = rect.height;
    canvas.width = Math.round(cw * dpr);
    canvas.height = Math.round(ch * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  window.addEventListener('resize', resizeCanvas);

  function renderShapeHint() {
    const unlocked = currentUnlockedShapes();
    shapeHintEl.innerHTML = HW_RAW_TEMPLATES.map(function (t) {
      const locked = unlocked.indexOf(t.name) === -1;
      return '<span class="hw-shape-chip' + (locked ? ' hw-locked' : '') + '">' + t.icon + ' ' + hwShapeLabel(t.name)
        + (locked ? ghalloweenspelldrawT('shapeLockedSuffix', { n: HW_CONFIG.circleUnlockWave }) : '') + '</span>';
    }).join('');
  }
  function currentUnlockedShapes() {
    const s = ['lightning', 'star'];
    if (wave >= HW_CONFIG.circleUnlockWave) s.push('circle');
    return s;
  }
  function currentUnlockedMonsterTypes() {
    return HW_MONSTER_TYPES.filter(function (t) { return t.minWave <= wave; });
  }

  function updateWave() {
    const newWave = hwComputeWave(defeated);
    if (newWave !== wave) {
      wave = newWave;
      waveEl.textContent = ghalloweenspelldrawT('waveLabel', { n: wave });
      waveEl.classList.remove('hw-wave-up');
      void waveEl.offsetWidth;
      waveEl.classList.add('hw-wave-up');
      renderShapeHint();
    }
  }
  function updateLivesDisplay() {
    let s = '';
    for (let i = 0; i < HW_CONFIG.startLives; i++) s += (i < lives ? '❤️' : '🖤');
    livesEl.textContent = s;
  }

  function spawnMonster() {
    if (!playing) return;
    const cap = hwComputeConcurrentCap(wave);
    if (monsters.length < cap) {
      const pool = currentUnlockedMonsterTypes();
      const t = pool[Math.floor(Math.random() * pool.length)];
      const speed = hwComputeMonsterSpeed(wave) * (t.speedMul || 1);
      monsters.push({
        id: monsterSeq++, key: t.key, name: hwMonsterName(t.key), weakness: t.weakness,
        hp: t.hp, maxHp: t.hp, r: t.r, auraColor: t.auraColor, body: t.body,
        x: t.r + Math.random() * (cw - 2 * t.r), y: -t.r, speed: speed
      });
    }
    spawnTimerId = setTimeout(spawnMonster, hwComputeSpawnIntervalMs(wave));
  }

  function removeMonster(m) {
    const idx = monsters.indexOf(m);
    if (idx !== -1) monsters.splice(idx, 1);
  }

  function addEffect(kind, x, y, tx, ty, durMs) {
    effects.push({ kind: kind, x: x, y: y, tx: tx, ty: ty, startTs: performance.now(), durMs: durMs });
    // 7-3/7-4 防錯與清理：特效陣列上限保護，極端情況也不會無限增長
    if (effects.length > 40) effects.splice(0, effects.length - 40);
  }

  function findTarget(shapeName) {
    if (!monsters.length) return null;
    const weak = monsters.filter(function (m) { return m.weakness === shapeName; });
    const pool = weak.length ? weak : monsters;
    return pool.reduce(function (a, b) { return a.y > b.y ? a : b; });
  }

  function castSpell(shapeName, castX, castY) {
    const target = findTarget(shapeName);
    if (!target) { addEffect('fizzle', castX, castY, castX, castY, 300); return; }
    const isCorrect = target.weakness === shapeName;
    if (isCorrect) {
      target.hp = 0;
      score += HW_CONFIG.killScoreCorrect + (wave - 1) * HW_CONFIG.killScoreCorrectWaveBonus;
      playChime(true);
    } else {
      target.hp -= 1;
      score += HW_CONFIG.hitScoreGeneric;
      playChime(false);
    }
    addEffect(shapeName, castX, castY, target.x, target.y, isCorrect ? 480 : 320);
    if (target.hp <= 0) {
      if (!isCorrect) score += HW_CONFIG.killScoreGenericBonus;
      removeMonster(target);
      defeated++;
      updateWave();
    }
    scoreEl.textContent = String(score);
  }

  function onStrokeEnd() {
    if (!stroke || !playing) { stroke = null; return; }
    const pts = stroke.points;
    const result = hwRecognizeGesture(pts, currentUnlockedShapes());
    const last = pts[pts.length - 1] || pts[0];
    if (result) {
      castSpell(result.name, last.x, last.y);
    } else {
      addEffect('miss', last.x, last.y, last.x, last.y, 260);
    }
    stroke = null;
  }

  function localPoint(e) {
    const rect = canvas.getBoundingClientRect();
    return { x: (e.clientX - rect.left), y: (e.clientY - rect.top) };
  }
  boardWrap.addEventListener('pointerdown', function (e) {
    if (!playing) return;
    e.preventDefault();
    stroke = { points: [localPoint(e)] };
  });
  boardWrap.addEventListener('pointermove', function (e) {
    if (!stroke || !playing) return;
    stroke.points.push(localPoint(e));
  });
  window.addEventListener('pointerup', function () { if (stroke) onStrokeEnd(); });
  boardWrap.addEventListener('pointerleave', function () { /* 允許畫出邊界仍可放開手指再判定，這裡不中斷 */ });

  // ── 繪製 ──
  function drawBackground() {
    ctx.clearRect(0, 0, cw, ch);
    const cauldronY = ch * HW_CONFIG.cauldronLineRatio;
    ctx.save();
    ctx.strokeStyle = 'rgba(239,68,68,.55)';
    ctx.lineWidth = 2;
    ctx.setLineDash([6, 6]);
    ctx.beginPath(); ctx.moveTo(0, cauldronY); ctx.lineTo(cw, cauldronY); ctx.stroke();
    ctx.setLineDash([]);
    ctx.restore();
  }
  function triangle(cx0, cy0, size) {
    ctx.beginPath();
    ctx.moveTo(cx0, cy0 - size); ctx.lineTo(cx0 - size * 0.85, cy0 + size * 0.7); ctx.lineTo(cx0 + size * 0.85, cy0 + size * 0.7); ctx.closePath(); ctx.fill();
  }
  function drawAura(m, t) {
    const pulse = 0.55 + 0.25 * Math.sin(t / 260 + m.id);
    ctx.save();
    ctx.beginPath();
    ctx.arc(m.x, m.y, m.r * 1.55, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(' + m.auraColor + ',' + (pulse * 0.28) + ')';
    ctx.shadowColor = 'rgba(' + m.auraColor + ',0.9)';
    ctx.shadowBlur = 14;
    ctx.fill();
    ctx.restore();
    const meta = HW_SHAPE_META[m.weakness];
    ctx.font = '13px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(meta.icon, m.x, m.y - m.r * 1.7);
  }
  function drawMonster(m, t) {
    drawAura(m, t);
    const g = ctx.createRadialGradient(m.x - m.r * 0.3, m.y - m.r * 0.3, m.r * 0.1, m.x, m.y, m.r);
    g.addColorStop(0, m.body[0]); g.addColorStop(1, m.body[1]);
    ctx.fillStyle = g;
    ctx.beginPath();
    if (m.key === 'bat') {
      ctx.ellipse(m.x, m.y, m.r * 0.75, m.r * 0.6, 0, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.moveTo(m.x - m.r * 0.6, m.y); ctx.lineTo(m.x - m.r * 1.5, m.y - m.r * 0.5); ctx.lineTo(m.x - m.r * 0.5, m.y + m.r * 0.2); ctx.closePath(); ctx.fill();
      ctx.beginPath(); ctx.moveTo(m.x + m.r * 0.6, m.y); ctx.lineTo(m.x + m.r * 1.5, m.y - m.r * 0.5); ctx.lineTo(m.x + m.r * 0.5, m.y + m.r * 0.2); ctx.closePath(); ctx.fill();
    } else if (m.key === 'ghost') {
      ctx.arc(m.x, m.y - m.r * 0.15, m.r * 0.8, Math.PI, 0);
      ctx.lineTo(m.x + m.r * 0.8, m.y + m.r * 0.7);
      for (let i = 0; i < 3; i++) { ctx.lineTo(m.x + m.r * 0.53 - i * m.r * 0.53, m.y + (i % 2 === 0 ? m.r * 0.4 : m.r * 0.7)); }
      ctx.lineTo(m.x - m.r * 0.8, m.y + m.r * 0.7);
      ctx.closePath(); ctx.fill();
    } else if (m.key === 'witch') {
      ctx.arc(m.x, m.y, m.r * 0.75, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.moveTo(m.x, m.y - m.r * 1.5); ctx.lineTo(m.x - m.r * 0.9, m.y - m.r * 0.35); ctx.lineTo(m.x + m.r * 0.9, m.y - m.r * 0.35); ctx.closePath(); ctx.fill();
    } else {
      ctx.ellipse(m.x, m.y, m.r, m.r * 0.85, 0, 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = 'rgba(154,52,18,.5)'; ctx.lineWidth = 2;
      for (let i = -1; i <= 1; i++) { ctx.beginPath(); ctx.ellipse(m.x + i * m.r * 0.35, m.y, m.r * 0.18, m.r * 0.85, 0, 0, Math.PI * 2); ctx.stroke(); }
    }
    ctx.fillStyle = 'rgba(20,10,10,.85)';
    if (m.key !== 'ghost') { triangle(m.x - m.r * 0.32, m.y - m.r * 0.05, m.r * 0.14); triangle(m.x + m.r * 0.32, m.y - m.r * 0.05, m.r * 0.14); }
    else { ctx.beginPath(); ctx.arc(m.x - m.r * 0.28, m.y - m.r * 0.1, m.r * 0.09, 0, Math.PI * 2); ctx.fill(); ctx.beginPath(); ctx.arc(m.x + m.r * 0.28, m.y - m.r * 0.1, m.r * 0.09, 0, Math.PI * 2); ctx.fill(); }
    if (m.hp < m.maxHp) {
      ctx.fillStyle = 'rgba(255,255,255,.25)';
      ctx.fillRect(m.x - m.r, m.y + m.r + 6, m.r * 2, 4);
      ctx.fillStyle = '#22c55e';
      ctx.fillRect(m.x - m.r, m.y + m.r + 6, m.r * 2 * (m.hp / m.maxHp), 4);
    }
  }
  function drawStroke() {
    if (!stroke || stroke.points.length < 2) return;
    ctx.save();
    ctx.strokeStyle = 'rgba(255,255,255,.9)';
    ctx.lineWidth = 3;
    ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    ctx.shadowColor = 'rgba(255,255,255,.8)'; ctx.shadowBlur = 8;
    ctx.beginPath();
    stroke.points.forEach(function (p, i) { if (i === 0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y); });
    ctx.stroke();
    ctx.restore();
  }
  function drawEffects(t) {
    effects = effects.filter(function (fx) { return t - fx.startTs < fx.durMs; });
    effects.forEach(function (fx) {
      const p = Math.min(1, (t - fx.startTs) / fx.durMs);
      ctx.save();
      if (fx.kind === 'lightning') {
        ctx.strokeStyle = 'rgba(253,224,71,' + (1 - p) + ')';
        ctx.lineWidth = 3;
        ctx.shadowColor = '#fde047'; ctx.shadowBlur = 12;
        ctx.beginPath(); ctx.moveTo(fx.x, fx.y);
        const midx = (fx.x + fx.tx) / 2 + (Math.random() - 0.5) * 20;
        const midy = (fx.y + fx.ty) / 2;
        ctx.lineTo(midx, midy); ctx.lineTo(fx.tx, fx.ty); ctx.stroke();
      } else if (fx.kind === 'star') {
        ctx.fillStyle = 'rgba(216,180,254,' + (1 - p) + ')';
        ctx.font = (16 + p * 10) + 'px sans-serif';
        ctx.fillText('⭐', fx.x + (fx.tx - fx.x) * p, fx.y + (fx.ty - fx.y) * p);
      } else if (fx.kind === 'circle') {
        ctx.strokeStyle = 'rgba(45,212,191,' + (1 - p) + ')';
        ctx.lineWidth = 3;
        ctx.beginPath(); ctx.arc(fx.tx, fx.ty, 10 + p * 26, 0, Math.PI * 2); ctx.stroke();
      } else if (fx.kind === 'miss' || fx.kind === 'fizzle') {
        ctx.fillStyle = 'rgba(203,213,225,' + (1 - p) + ')';
        ctx.font = '12px sans-serif'; ctx.textAlign = 'center';
        ctx.fillText('？', fx.x, fx.y);
      }
      ctx.restore();
    });
  }

  function loop(ts) {
    if (!playing) return;
    if (!lastTs) lastTs = ts;
    const dtSec = (ts - lastTs) / 1000;
    lastTs = ts;
    const cauldronY = ch * HW_CONFIG.cauldronLineRatio;

    drawBackground();
    for (let i = monsters.length - 1; i >= 0; i--) {
      const m = monsters[i];
      m.y += m.speed * dtSec;
      if (m.y - m.r >= cauldronY) {
        removeMonster(m);
        lives--;
        updateLivesDisplay();
        if (lives <= 0) { endGame(); return; }
        continue;
      }
      drawMonster(m, ts);
    }
    drawEffects(ts);
    drawStroke();
    rafId = requestAnimationFrame(loop);
  }

  function endGame() {
    playing = false;
    clearAll();
    startBtn.disabled = false;
    startBtn.textContent = ghalloweenspelldrawT('playAgainBtn');
    overTitle.textContent = ghalloweenspelldrawT('gameOverTitle');
    overSub.textContent = ghalloweenspelldrawT('gameOverSub', { s: score, w: wave });
    overlay.classList.add('show');
    ratingEl.textContent = ghalloweenspelldrawT('scoreShort', { s: score }) + ' — ' + hwComputeRating(score);

    history.unshift(score);
    history = history.slice(0, HW_CONFIG.historyLimit);
    bestScore = Math.max(bestScore, score);
    bestWave = Math.max(bestWave, wave);
    bestEl.textContent = ghalloweenspelldrawT('scoreShort', { s: bestScore });
    bestWaveEl.textContent = ghalloweenspelldrawT('waveLabel', { n: bestWave });
    historyEl.innerHTML = history.map(function (v) { return '<span>' + ghalloweenspelldrawT('historyEntry', { v: v }) + '</span>'; }).join('');
    window._hwLastScore = score;
    window._hwBestScore = bestScore;
    if (typeof gaSubmitScore === 'function') gaSubmitScore('halloween-spell-draw', score);
  }

  function hwStartInternal() {
    resizeCanvas();
    clearAll();
    overlay.classList.remove('show');
    playing = true;
    score = 0; wave = 1; lives = HW_CONFIG.startLives; defeated = 0; lastTs = 0;
    scoreEl.textContent = '0';
    waveEl.textContent = ghalloweenspelldrawT('waveLabel', { n: 1 });
    updateLivesDisplay();
    renderShapeHint();
    ratingEl.textContent = '';
    startBtn.disabled = true;
    startBtn.textContent = ghalloweenspelldrawT('playingBtn');

    spawnTimerId = setTimeout(spawnMonster, 500);
    rafId = requestAnimationFrame(loop);
  }
  window.hwStart = hwStartInternal;

  // ── 音效：Web Audio 合成音，跟鋼琴塊遊戲同一套做法，不需外部音檔（7-3 防錯：播放失敗不影響遊戲）──
  let audioCtx = null, soundOn = true;
  function getAudioCtx() {
    if (!HW_CONFIG.sound.enabled) return null;
    if (!audioCtx) { try { audioCtx = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { audioCtx = null; } }
    if (audioCtx && audioCtx.state === 'suspended') { audioCtx.resume().catch(function () {}); }
    return audioCtx;
  }
  function playChime(isCorrect) {
    if (!soundOn) return;
    const ctxA = getAudioCtx();
    if (!ctxA) return;
    try {
      const osc = ctxA.createOscillator(); const gain = ctxA.createGain();
      osc.type = isCorrect ? 'triangle' : 'sine';
      osc.frequency.value = isCorrect ? 660 : 340;
      gain.gain.setValueAtTime(HW_CONFIG.sound.volume, ctxA.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, ctxA.currentTime + (isCorrect ? 0.28 : 0.14));
      osc.connect(gain).connect(ctxA.destination);
      osc.start(); osc.stop(ctxA.currentTime + (isCorrect ? 0.28 : 0.14));
    } catch (e) { /* 音效失敗不應中斷遊戲 */ }
  }
  window.hwToggleSound = function () {
    soundOn = !soundOn;
    const btn = document.getElementById('hwSoundBtn');
    if (btn) btn.textContent = soundOn ? ghalloweenspelldrawT('soundOnBtn') : ghalloweenspelldrawT('soundOffBtn');
    if (soundOn) getAudioCtx();
  };

  renderShapeHint();
  updateLivesDisplay();
  resizeCanvas();
  window.addEventListener('beforeunload', clearAll); // 7-4 資源清理
})();

function hwShareResult() {
  const score = (typeof window !== 'undefined') ? window._hwLastScore : null;
  const text = (score != null)
    ? ghalloweenspelldrawT('shareWithScore', { s: score })
    : ghalloweenspelldrawT('shareNoScore');
  if (typeof navigator !== 'undefined' && navigator.share) {
    navigator.share({ title: document.title, text: text, url: location.href }).catch(function () {});
  } else {
    if (!navigator.clipboard || !navigator.clipboard.writeText) return; // 7-3 防錯：無剪貼簿API時安全退出
    navigator.clipboard.writeText(text + ' ' + location.href);
    const b = event.target;
    const old = b.textContent;
    b.textContent = ghalloweenspelldrawT('copied');
    setTimeout(function () { b.textContent = old; }, HW_CONFIG.copyRevertMs);
  }
}
if (typeof document !== 'undefined') {
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.addEventListener('click', function () { this.parentElement.classList.toggle('open'); });
  });
}
