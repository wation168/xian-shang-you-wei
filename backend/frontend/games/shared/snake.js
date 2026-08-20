// ══════════════════════════════════════════════════════════
// 貪食蛇 — 共用遊戲邏輯（所有語言版本共用這一份，2026/08/18 多語言化時抽出）
//
// 【多語言架構約定】
//   這個檔案裡「不能出現任何給使用者看的文字」。所有文字一律透過 gsnakeT('key') 讀取
//   頁面在載入這支JS之前先定義好的 window.GAME_I18N 字典。
//   → 遊戲邏輯有bug只要改這一個檔案，10種語言同時生效
//   → 翻譯只動各語言HTML裡的字典，不會誤改邏輯
//
// 遵循《新工具規劃守則.md》第七節：
//   7-1 SNAKE_CONFIG集中管理格數/初始速度/加速幅度/初始蛇長等所有可調數值
//       （評語門檻只留數字，文字放在 GAME_I18N.ratings 同順序的陣列）
//   7-2 純函式（snNextHead/snIsOutOfBounds/snIsSelfCollision/snComputeLevel）不碰DOM，
//       跟遊戲迴圈與畫面渲染完全分開，方便單元測試
//   7-3 防錯：禁止直接180度反向、遊戲結束後方向鍵與按鈕都失效、字典缺key不崩潰
//   7-4 資源清理：setInterval統一在clearAll()處理，離開頁面前清除並移除keydown監聽
// ══════════════════════════════════════════════════════════

const SNAKE_CONFIG = {
  gridSize: 15,
  initialLength: 3,
  initialTickMs: 220,
  minTickMs: 80,
  tickDecreasePerFood: 6,
  historyLimit: 5,
  copyRevertMs: 1500,
  scorePerLevel: 5,
  swipeMinPx: 20,
  opposite: { up: 'down', down: 'up', left: 'right', right: 'left' },
  headRotation: { up: 0, right: 90, down: 180, left: 270 },
  foodEmoji: '🍎',
  // 只放門檻數字，對應的評語文字放在 GAME_I18N.ratings 同樣順序的陣列裡
  ratingThresholds: [5, 12, 20, 30, Infinity]
};

// ── i18n 取字helper（7-3 防錯：缺key不崩潰）──
function gsnakeT(key, vars) {
  const dict = (typeof window !== 'undefined' && window.GAME_I18N) || {};
  let s = dict[key];
  if (typeof s !== 'string') {
    if (typeof console !== 'undefined' && console.warn) console.warn('[snake] missing i18n key: ' + key);
    return '';
  }
  if (vars) {
    Object.keys(vars).forEach(function (k) {
      s = s.split('{' + k + '}').join(String(vars[k]));
    });
  }
  return s;
}

// ── 純函式：不碰DOM，只操作資料，也不含任何文字 ──
function snNextHead(head, dir) {
  const d = { up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] }[dir];
  return { x: head.x + d[0], y: head.y + d[1] };
}
function snIsOutOfBounds(pos) {
  return pos.x < 0 || pos.x >= SNAKE_CONFIG.gridSize || pos.y < 0 || pos.y >= SNAKE_CONFIG.gridSize;
}
function snIsSelfCollision(pos, body) {
  return body.some(function (s) { return s.x === pos.x && s.y === pos.y; });
}
// 純函式：回傳「第幾級評語」的index，文字本身由呼叫端從GAME_I18N.ratings取
function snRatingIndex(score) {
  for (let i = 0; i < SNAKE_CONFIG.ratingThresholds.length; i++) {
    if (score <= SNAKE_CONFIG.ratingThresholds[i]) return i;
  }
  return SNAKE_CONFIG.ratingThresholds.length - 1;
}
function snComputeRating(score) {
  const list = (typeof window !== 'undefined' && window.GAME_I18N && window.GAME_I18N.ratings) || [];
  return list[snRatingIndex(score)] || '';
}
function snComputeLevel(score) {
  return 1 + Math.floor(score / SNAKE_CONFIG.scorePerLevel);
}

(function () {
  if (typeof document === 'undefined') return; // 純邏輯測試環境（無DOM）時安靜跳過UI部分
  const boardEl  = document.getElementById('snBoard');
  const scoreEl  = document.getElementById('snScore');
  const ratingEl = document.getElementById('snRating');
  const bestEl   = document.getElementById('snBest');
  const historyEl= document.getElementById('snHistory');
  const startBtn = document.getElementById('snStartBtn');
  const levelEl  = document.getElementById('snLevelBadge');
  if (!boardEl || !scoreEl) return; // 7-3 防錯：頁面結構不符時不炸掉整頁

  boardEl.style.gridTemplateColumns = 'repeat(' + SNAKE_CONFIG.gridSize + ', 1fr)';
  boardEl.style.gridTemplateRows = 'repeat(' + SNAKE_CONFIG.gridSize + ', 1fr)';

  let cellEls = [];
  for (let y = 0; y < SNAKE_CONFIG.gridSize; y++) {
    const row = [];
    for (let x = 0; x < SNAKE_CONFIG.gridSize; x++) {
      const el = document.createElement('div');
      el.className = 'sn-cell' + ((x + y) % 2 === 0 ? ' alt' : '');
      boardEl.appendChild(el);
      row.push(el);
    }
    cellEls.push(row);
  }

  let snake = [];
  let dir = 'right';
  let pendingDir = 'right';
  let food = { x: 0, y: 0 };
  let score = 0;
  let playing = false;
  let tickMs = SNAKE_CONFIG.initialTickMs;
  let tickTimerId = null;
  let history = [];
  let level = 1;

  function clearAll() {
    if (tickTimerId) { clearInterval(tickTimerId); tickTimerId = null; }
  }

  function randomEmptyCell() {
    let pos;
    do {
      pos = { x: Math.floor(Math.random() * SNAKE_CONFIG.gridSize), y: Math.floor(Math.random() * SNAKE_CONFIG.gridSize) };
    } while (snIsSelfCollision(pos, snake));
    return pos;
  }

  function render() {
    for (let y = 0; y < SNAKE_CONFIG.gridSize; y++) {
      for (let x = 0; x < SNAKE_CONFIG.gridSize; x++) {
        const cell = cellEls[y][x];
        cell.className = 'sn-cell' + ((x + y) % 2 === 0 ? ' alt' : '');
        if (cell.textContent) cell.textContent = '';
        cell.style.transform = '';
      }
    }
    snake.forEach(function (s, i) {
      const cell = cellEls[s.y][s.x];
      cell.className += ' ' + (i === 0 ? 'head' : 'body');
      if (i === 0) cell.style.transform = 'rotate(' + SNAKE_CONFIG.headRotation[dir] + 'deg)';
    });
    const foodCell = cellEls[food.y][food.x];
    foodCell.className += ' food';
    foodCell.textContent = SNAKE_CONFIG.foodEmoji;
  }

  function onKeyDown(e) {
    const map = { ArrowUp: 'up', ArrowDown: 'down', ArrowLeft: 'left', ArrowRight: 'right' };
    if (map[e.key]) { e.preventDefault(); trySetDir(map[e.key]); }
  }

  function trySetDir(newDir) {
    if (!playing) return;
    if (SNAKE_CONFIG.opposite[newDir] === dir) return; // 7-3 防錯：禁止直接反向
    pendingDir = newDir;
  }
  window.snSetDir = trySetDir;

  function tick() {
    dir = pendingDir;
    const head = snNextHead(snake[0], dir);
    if (snIsOutOfBounds(head) || snIsSelfCollision(head, snake)) { endGame(); return; }

    snake.unshift(head);
    if (head.x === food.x && head.y === food.y) {
      score++;
      scoreEl.textContent = String(score);
      const newLevel = snComputeLevel(score);
      if (newLevel !== level) {
        level = newLevel;
        levelEl.textContent = gsnakeT('levelBadge', { n: level });
        levelEl.classList.remove('sn-level-up');
        void levelEl.offsetWidth; // 重新觸發動畫
        levelEl.classList.add('sn-level-up');
      }
      food = randomEmptyCell();
      tickMs = Math.max(SNAKE_CONFIG.minTickMs, tickMs - SNAKE_CONFIG.tickDecreasePerFood);
      clearAll();
      tickTimerId = setInterval(tick, tickMs);
    } else {
      snake.pop();
    }
    render();
  }

  function endGame() {
    playing = false;
    clearAll();
    startBtn.disabled = false;
    startBtn.textContent = gsnakeT('playAgainBtn');
    ratingEl.textContent = gsnakeT('scoreShort', { s: score }) + ' — ' + snComputeRating(score);

    history.unshift(score);
    history = history.slice(0, SNAKE_CONFIG.historyLimit);
    const best = Math.max(...history);
    bestEl.textContent = gsnakeT('scoreShort', { s: best });
    historyEl.innerHTML = history.map(function (v) {
      return '<span>' + gsnakeT('scoreShort', { s: v }) + '</span>';
    }).join('');
    window._snLastScore = score;
    window._snBestScore = best;
    if (typeof gaSubmitScore === 'function') gaSubmitScore('snake', score);
  }

  function snStartInternal() {
    clearAll();
    const mid = Math.floor(SNAKE_CONFIG.gridSize / 2);
    snake = [];
    for (let i = 0; i < SNAKE_CONFIG.initialLength; i++) snake.push({ x: mid - i, y: mid });
    dir = 'right';
    pendingDir = 'right';
    score = 0;
    level = 1;
    tickMs = SNAKE_CONFIG.initialTickMs;
    playing = true;
    scoreEl.textContent = '0';
    levelEl.textContent = gsnakeT('levelBadge', { n: 1 });
    ratingEl.textContent = '';
    startBtn.disabled = true;
    startBtn.textContent = gsnakeT('playingBtn');
    food = randomEmptyCell();
    render();
    tickTimerId = setInterval(tick, tickMs);
  }

  window.snStart = snStartInternal;

  // 2026/08/16新增：手機希望能直接滑畫面控制方向，不只靠下方十字按鈕。
  // 用滑動手勢（swipe）判斷方向比「點畫面四個象限」更符合手機貪食蛇的操作直覺、
  // 誤觸機率也更低——記錄手指按下與放開的座標差，取位移較大的軸當作方向。
  let touchStartX = 0, touchStartY = 0;
  boardEl.addEventListener('touchstart', function (e) {
    if (!e.touches || !e.touches.length) return;
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
  }, { passive: true });
  boardEl.addEventListener('touchend', function (e) {
    if (!e.changedTouches || !e.changedTouches.length) return;
    const dx = e.changedTouches[0].clientX - touchStartX;
    const dy = e.changedTouches[0].clientY - touchStartY;
    if (Math.max(Math.abs(dx), Math.abs(dy)) < SNAKE_CONFIG.swipeMinPx) return; // 太小的滑動視為誤觸
    if (Math.abs(dx) > Math.abs(dy)) {
      trySetDir(dx > 0 ? 'right' : 'left');
    } else {
      trySetDir(dy > 0 ? 'down' : 'up');
    }
  }, { passive: true });

  document.addEventListener('keydown', onKeyDown);
  // 7-4 資源清理：離開頁面前清掉計時器與鍵盤事件監聽
  if (typeof window !== 'undefined') {
    window.addEventListener('beforeunload', function () {
      clearAll();
      document.removeEventListener('keydown', onKeyDown);
    });
  }

  render();
})();

function snShareResult() {
  const score = window._snLastScore;
  const text = (score != null)
    ? gsnakeT('shareWithScore', { s: score })
    : gsnakeT('shareNoScore');
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
  b.textContent = gsnakeT('copied');
  setTimeout(function () { b.textContent = old; }, SNAKE_CONFIG.copyRevertMs);
}
// FAQ 展開收合（7-3 防錯：純邏輯測試環境沒有 document 時安靜跳過，
// 不能讓這一行在無DOM環境直接拋 ReferenceError 導致整支檔案無法被單元測試載入）
if (typeof document !== 'undefined') {
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.addEventListener('click', function () { this.parentElement.classList.toggle('open'); });
  });
}
