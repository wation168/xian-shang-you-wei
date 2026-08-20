// ══════════════════════════════════════════════════════════
// 2048 — 共用遊戲邏輯（所有語言版本共用這一份，2026/08/17 多語言化時抽出）
//
// 【多語言架構約定】
//   這個檔案裡「不能出現任何給使用者看的文字」。所有文字一律透過 t('key') 讀取
//   頁面在載入這支JS之前先定義好的 window.GAME_I18N 字典。
//   → 遊戲邏輯有bug只要改這一個檔案，10種語言同時生效
//   → 翻譯只動各語言HTML裡的字典，不會誤改邏輯
//   驗證方式：tests/validate_i18n_keys.py 會自動掃出本檔所有 t('...') 用到的key，
//   逐一比對每個語言的字典是否都有，缺一個就讓建置失敗。
//
// 遵循《新工具規劃守則.md》第七節：
//   7-1 G2048_CONFIG集中管理盤面大小/出現機率/分數門檻等所有數值（文字在GAME_I18N）
//   7-2 純函式（slideLeftLine/moveGrid/hasMovesLeft）跟DOM渲染完全分開，方便單元測試
//   7-3 防錯：無效移動不消耗回合；字典缺key不會讓遊戲崩潰（回傳空字串並警告）
//   7-4 資源清理：固定16格DOM節點重複利用，不隨遊戲時間增加而累積
// ══════════════════════════════════════════════════════════

const G2048_CONFIG = {
  size: 4,
  startTiles: 2,
  prob4: 0.1,
  winValue: 2048,
  historyLimit: 5,
  copyRevertMs: 1500,
  swipeMinPx: 24,
  // 只放門檻數字，對應的評語文字放在 GAME_I18N.ratings 同樣順序的陣列裡
  ratingThresholds: [128, 512, 1024, 2048, Infinity]
};

// ── i18n 取字helper（7-3 防錯：缺key不崩潰）──
function g2048T(key, vars) {
  const dict = (typeof window !== 'undefined' && window.GAME_I18N) || {};
  let s = dict[key];
  if (typeof s !== 'string') {
    if (typeof console !== 'undefined' && console.warn) console.warn('[2048] missing i18n key: ' + key);
    return '';
  }
  if (vars) {
    Object.keys(vars).forEach(function (k) {
      s = s.split('{' + k + '}').join(String(vars[k]));
    });
  }
  return s;
}

// ── 純函式：可獨立單元測試，不依賴DOM，也不含任何文字 ──
function makeEmptyGrid(size) {
  return Array.from({ length: size }, () => Array.from({ length: size }, () => 0));
}
function cloneGrid(g) { return g.map(r => r.slice()); }
function transpose(g) {
  const n = g.length;
  const out = makeEmptyGrid(n);
  for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) out[c][r] = g[r][c];
  return out;
}
function slideLeftLine(line) {
  const vals = line.filter(function (v) { return v !== 0; });
  const result = [];
  let scoreGain = 0;
  let i = 0;
  while (i < vals.length) {
    if (i + 1 < vals.length && vals[i] === vals[i + 1]) {
      const merged = vals[i] * 2;
      result.push(merged);
      scoreGain += merged;
      i += 2;
    } else {
      result.push(vals[i]);
      i += 1;
    }
  }
  while (result.length < line.length) result.push(0);
  let moved = false;
  for (let k = 0; k < line.length; k++) { if (line[k] !== result[k]) { moved = true; break; } }
  return { line: result, scoreGain: scoreGain, moved: moved };
}
function moveGrid(grid, direction) {
  let g = cloneGrid(grid);
  if (direction === 'right') g = g.map(function (r) { return r.slice().reverse(); });
  else if (direction === 'up') g = transpose(g);
  else if (direction === 'down') { g = transpose(g); g = g.map(function (r) { return r.slice().reverse(); }); }

  let totalScoreGain = 0, anyMoved = false;
  const slid = g.map(function (row) {
    const res = slideLeftLine(row);
    totalScoreGain += res.scoreGain;
    if (res.moved) anyMoved = true;
    return res.line;
  });

  let finalG = slid;
  if (direction === 'right') finalG = slid.map(function (r) { return r.slice().reverse(); });
  else if (direction === 'up') finalG = transpose(slid);
  else if (direction === 'down') { finalG = slid.map(function (r) { return r.slice().reverse(); }); finalG = transpose(finalG); }

  return { grid: finalG, scoreGain: totalScoreGain, moved: anyMoved };
}
function emptyCells(grid) {
  const out = [];
  for (let r = 0; r < grid.length; r++) for (let c = 0; c < grid[r].length; c++) if (grid[r][c] === 0) out.push({ r: r, c: c });
  return out;
}
function hasMovesLeft(grid) {
  if (emptyCells(grid).length > 0) return true;
  const n = grid.length;
  for (let r = 0; r < n; r++) {
    for (let c = 0; c < n; c++) {
      const v = grid[r][c];
      if (c + 1 < n && grid[r][c + 1] === v) return true;
      if (r + 1 < n && grid[r + 1][c] === v) return true;
    }
  }
  return false;
}
// 純函式：回傳「第幾級評語」的index，文字本身由呼叫端從GAME_I18N.ratings取
function ratingIndex(score) {
  for (let i = 0; i < G2048_CONFIG.ratingThresholds.length; i++) {
    if (score <= G2048_CONFIG.ratingThresholds[i]) return i;
  }
  return G2048_CONFIG.ratingThresholds.length - 1;
}
function computeRating(score) {
  const list = (typeof window !== 'undefined' && window.GAME_I18N && window.GAME_I18N.ratings) || [];
  const idx = ratingIndex(score);
  return list[idx] || '';
}
function maxTileOf(grid) {
  let m = 0;
  grid.forEach(function (row) { row.forEach(function (v) { if (v > m) m = v; }); });
  return m;
}

(function () {
  if (typeof document === 'undefined') return; // 純邏輯測試環境（無DOM）時安靜跳過UI部分
  const gridEl = document.getElementById('g2048Grid');
  const boardEl = document.getElementById('g2048Board');
  const overlay = document.getElementById('g2048Overlay');
  const overTitle = document.getElementById('g2048OverTitle');
  const overSub = document.getElementById('g2048OverSub');
  const continueBtn = document.getElementById('g2048ContinueBtn');
  const scoreEl = document.getElementById('g2048Score');
  const bestEl = document.getElementById('g2048Best');
  const bestInlineEl = document.getElementById('g2048BestInline');
  const bestTileEl = document.getElementById('g2048BestTile');
  const ratingEl = document.getElementById('g2048Rating');
  const historyEl = document.getElementById('g2048History');
  const startBtn = document.getElementById('g2048StartBtn');
  if (!gridEl || !boardEl) return; // 7-3 防錯：頁面結構不符時不炸掉整頁

  let grid = makeEmptyGrid(G2048_CONFIG.size);
  let score = 0, bestScore = 0, bestTile = 0, history = [];
  let playing = false, wonAnnounced = false;

  function randomTileValue() { return Math.random() < G2048_CONFIG.prob4 ? 4 : 2; }
  function spawnRandomTile() {
    const cells = emptyCells(grid);
    if (!cells.length) return false; // 7-3 防錯：沒有空格就不放
    const pick = cells[Math.floor(Math.random() * cells.length)];
    grid[pick.r][pick.c] = randomTileValue();
    return true;
  }

  function tileStyle(v) {
    const exp = Math.max(1, Math.log2(v));
    const hue = Math.max(10, 260 - Math.min(220, exp * 20));
    const light = Math.max(38, 60 - exp * 2);
    const fontSize = v >= 1000 ? 22 : v >= 100 ? 26 : 32;
    return 'background:hsl(' + hue + ',68%,' + light + '%);color:' + (exp >= 6 ? '#fff' : '#1e293b') + ';font-size:' + fontSize + 'px';
  }

  function render() {
    // 固定size*size個格底 + 逐一畫出非0方塊，格數固定不隨時間增加，符合7-4資源清理精神
    const n = G2048_CONFIG.size;
    const cellPct = 100 / n;
    let html = '';
    for (let i = 0; i < n * n; i++) html += '<div class="g2048-cellbg"></div>';
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n; c++) {
        const v = grid[r][c];
        if (!v) continue;
        html += '<div class="g2048-tile" style="left:' + (c * cellPct) + '%;top:' + (r * cellPct) + '%;width:' + cellPct + '%;height:' + cellPct + '%;' + tileStyle(v) + '">' + v + '</div>';
      }
    }
    gridEl.innerHTML = html;
  }

  function updateScoreDisplay() {
    scoreEl.textContent = String(score);
    bestInlineEl.textContent = String(bestScore);
  }

  function checkGameOver() {
    if (!hasMovesLeft(grid)) {
      playing = false;
      overTitle.textContent = g2048T('gameOver');
      overSub.textContent = g2048T('scoreLine', { s: score });
      continueBtn.style.display = 'none';
      overlay.classList.add('show');
      finalizeRound();
    }
  }

  function finalizeRound() {
    bestScore = Math.max(bestScore, score);
    bestTile = Math.max(bestTile, maxTileOf(grid));
    bestEl.textContent = String(bestScore);
    bestTileEl.textContent = String(bestTile);
    updateScoreDisplay();
    history.unshift(score);
    history = history.slice(0, G2048_CONFIG.historyLimit);
    historyEl.innerHTML = history.map(function (v) { return '<span>' + g2048T('scoreShort', { s: v }) + '</span>'; }).join('');
    ratingEl.textContent = g2048T('scoreShort', { s: score }) + ' — ' + computeRating(score);
    window._g2048LastScore = score;
    window._g2048BestScore = bestScore;
    if (typeof gaSubmitScore === 'function') gaSubmitScore('2048', score);
  }

  function tryMove(direction) {
    if (!playing) return;
    const result = moveGrid(grid, direction);
    if (!result.moved) return; // 7-3 防錯：無效移動不消耗回合
    grid = result.grid;
    score += result.scoreGain;
    spawnRandomTile();
    render();
    updateScoreDisplay();
    if (!wonAnnounced && maxTileOf(grid) >= G2048_CONFIG.winValue) {
      wonAnnounced = true;
      playing = false;
      overTitle.textContent = g2048T('winTitle', { v: G2048_CONFIG.winValue });
      overSub.textContent = g2048T('scoreLine', { s: score });
      continueBtn.style.display = 'inline-block';
      overlay.classList.add('show');
      finalizeRound();
      return;
    }
    checkGameOver();
  }
  window.g2048Continue = function () {
    overlay.classList.remove('show');
    playing = true;
  };

  const KEY_DIR = { ArrowLeft: 'left', ArrowRight: 'right', ArrowUp: 'up', ArrowDown: 'down' };
  window.addEventListener('keydown', function (e) {
    const dir = KEY_DIR[e.key];
    if (!dir) return;
    e.preventDefault();
    tryMove(dir);
  });

  let touchStartX = 0, touchStartY = 0;
  boardEl.addEventListener('pointerdown', function (e) { touchStartX = e.clientX; touchStartY = e.clientY; });
  boardEl.addEventListener('pointerup', function (e) {
    const dx = e.clientX - touchStartX, dy = e.clientY - touchStartY;
    if (Math.abs(dx) < G2048_CONFIG.swipeMinPx && Math.abs(dy) < G2048_CONFIG.swipeMinPx) return; // 太短不算滑動
    if (Math.abs(dx) > Math.abs(dy)) tryMove(dx > 0 ? 'right' : 'left');
    else tryMove(dy > 0 ? 'down' : 'up');
  });

  function g2048RestartInternal() {
    grid = makeEmptyGrid(G2048_CONFIG.size);
    score = 0; playing = true; wonAnnounced = false;
    overlay.classList.remove('show');
    continueBtn.style.display = 'none';
    for (let i = 0; i < G2048_CONFIG.startTiles; i++) spawnRandomTile();
    render();
    updateScoreDisplay();
    ratingEl.textContent = '';
    startBtn.textContent = g2048T('restartBtn');
  }
  window.g2048Restart = g2048RestartInternal;

  render();
})();

function g2048ShareResult() {
  const score = window._g2048LastScore;
  const text = (score != null)
    ? g2048T('shareWithScore', { s: score })
    : g2048T('shareNoScore');
  if (navigator.share) {
    navigator.share({ title: document.title, text: text, url: location.href }).catch(function () {});
    return;
  }
  // 7-3 防錯：navigator.clipboard 在非HTTPS環境或部分舊瀏覽器不存在，
  // 原本直接呼叫 writeText 會拋 TypeError 讓按鈕整個失效，這裡先確認能力再用。
  if (!navigator.clipboard || !navigator.clipboard.writeText) return;
  Promise.resolve(navigator.clipboard.writeText(text + ' ' + location.href)).catch(function () {});
  const b = (typeof event !== 'undefined' && event && event.target) ? event.target : null;
  if (!b) return; // 拿不到按鈕元素就只複製、不改文字
  const old = b.textContent;
  b.textContent = g2048T('copied');
  setTimeout(function () { b.textContent = old; }, G2048_CONFIG.copyRevertMs);
}
// FAQ 展開收合（7-3 防錯：純邏輯測試環境沒有 document 時安靜跳過，
// 不能讓這一行在無DOM環境直接拋 ReferenceError 導致整支檔案無法被單元測試載入）
if (typeof document !== 'undefined') {
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.addEventListener('click', function () { this.parentElement.classList.toggle('open'); });
  });
}
