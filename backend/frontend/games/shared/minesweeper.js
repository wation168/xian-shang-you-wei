// ══════════════════════════════════════════════════════════
// 踩地雷 — 共用遊戲邏輯（所有語言版本共用這一份，2026/08/18 多語言化時抽出）
//
// 【多語言架構約定】
//   這個檔案裡「不能出現任何給使用者看的文字」。所有文字一律透過 gminesweeperT('key')
//   讀取頁面在載入這支JS之前先定義好的 window.GAME_I18N 字典。
//   → 遊戲邏輯有bug只要改這一個檔案，10種語言同時生效
//   → 翻譯只動各語言HTML裡的字典，不會誤改邏輯
//
// 遵循《新工具規劃守則.md》第七節：
//   7-1 MS_CONFIG集中管理難度表/計分公式等所有數值（文字在GAME_I18N）
//   7-2 純函式（msPlaceMines/msRevealCell/msChordReveal/msCheckWin等）跟DOM渲染分開，方便單元測試
//   7-3 防錯：地雷放置排除第一次點擊安全區並用大量隨機測試驗證、旗子/已翻開格子互斥操作檢查、
//       字典缺key不會讓遊戲崩潰（回傳空字串並警告）
//   7-4 資源清理：格子DOM節點每輪重新建立時先清空容器（innerHTML=''）避免累積，
//       事件用容器層級委派而非每格綁定，計時器切局/結束時清除
// ══════════════════════════════════════════════════════════

const MS_CONFIG = {
  // 三種業界標準難度（初級9x9/10雷、中級16x16/40雷、高級16x30/99雷），
  // 這是所有踩地雷版本的共同標準，數值不得更動；對應的難度名稱文字放在
  // GAME_I18N.difficulties 同樣順序的陣列裡
  difficultyTable: [
    { key: 'beginner',     rows: 9,  cols: 9,  mines: 10 },
    { key: 'intermediate', rows: 16, cols: 16, mines: 40 },
    { key: 'expert',       rows: 16, cols: 30, mines: 99 }
  ],
  scoreBaseByDifficulty: { beginner: 100, intermediate: 400, expert: 900 },
  timeScorePenaltyPerSec: 0.6,
  timeScorePenaltyCap: 300,
  historyLimit: 6,
  copyRevertMs: 1500,
  nextRoundDelayMs: 1800,
  // 只放門檻數字，對應的評語文字放在 GAME_I18N.ratings 同樣順序的陣列裡
  ratingThresholds: [150, 400, 700, 1100, Infinity]
};

// ── i18n 取字helper（7-3 防錯：缺key不崩潰）──
function gminesweeperT(key, vars) {
  const dict = (typeof window !== 'undefined' && window.GAME_I18N) || {};
  let s = dict[key];
  if (typeof s !== 'string') {
    if (typeof console !== 'undefined' && console.warn) console.warn('[minesweeper] missing i18n key: ' + key);
    return '';
  }
  if (vars) {
    Object.keys(vars).forEach(function (k) {
      s = s.split('{' + k + '}').join(String(vars[k]));
    });
  }
  return s;
}

// ══════════════════════════════════════════════════════════
// 純函式：可獨立單元測試，不依賴DOM，也不含任何文字
// ══════════════════════════════════════════════════════════
function msComputeDifficultyForRound(roundNumber) {
  const idx = Math.min(roundNumber - 1, MS_CONFIG.difficultyTable.length - 1);
  const safeIdx = Math.max(0, idx);
  const d = MS_CONFIG.difficultyTable[safeIdx];
  return { key: d.key, rows: d.rows, cols: d.cols, mines: d.mines, index: safeIdx };
}
// 純函式：回傳「第幾個難度」的index，難度名稱文字由呼叫端從GAME_I18N.difficulties取
function msDifficultyLabel(index) {
  const list = (typeof window !== 'undefined' && window.GAME_I18N && window.GAME_I18N.difficulties) || [];
  return list[index] || '';
}
function msCreateEmptyGrid(rows, cols) {
  const grid = [];
  for (let r = 0; r < rows; r++) {
    const row = [];
    for (let c = 0; c < cols; c++) row.push({ mine: false, revealed: false, flagged: false, adjacent: 0 });
    grid.push(row);
  }
  return grid;
}
function msNeighborsOf(rows, cols, row, col) {
  const out = [];
  for (let dr = -1; dr <= 1; dr++) {
    for (let dc = -1; dc <= 1; dc++) {
      if (dr === 0 && dc === 0) continue;
      const nr = row + dr, nc = col + dc;
      if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) out.push([nr, nc]);
    }
  }
  return out;
}
function msPlaceMines(grid, rows, cols, mineCount, safeRow, safeCol) {
  const safeSet = new Set();
  safeSet.add(safeRow + ',' + safeCol);
  msNeighborsOf(rows, cols, safeRow, safeCol).forEach(function (p) { safeSet.add(p[0] + ',' + p[1]); });
  const candidates = [];
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) if (!safeSet.has(r + ',' + c)) candidates.push([r, c]);
  const actualMineCount = Math.min(mineCount, candidates.length);
  for (let i = candidates.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const tmp = candidates[i]; candidates[i] = candidates[j]; candidates[j] = tmp;
  }
  for (let i = 0; i < actualMineCount; i++) { const p = candidates[i]; grid[p[0]][p[1]].mine = true; }
  return actualMineCount;
}
function msComputeAdjacentCounts(grid, rows, cols) {
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (grid[r][c].mine) continue;
      let count = 0;
      msNeighborsOf(rows, cols, r, c).forEach(function (p) { if (grid[p[0]][p[1]].mine) count++; });
      grid[r][c].adjacent = count;
    }
  }
}
function msRevealCell(grid, rows, cols, row, col) {
  const cell = grid[row][col];
  if (cell.revealed || cell.flagged) return [];
  if (cell.mine) { cell.revealed = true; return [[row, col]]; }
  const revealed = [];
  const queue = [[row, col]];
  const seen = new Set([row + ',' + col]);
  while (queue.length) {
    const p0 = queue.shift();
    const r = p0[0], c = p0[1];
    const cur = grid[r][c];
    if (cur.revealed || cur.flagged || cur.mine) continue;
    cur.revealed = true;
    revealed.push([r, c]);
    if (cur.adjacent === 0) {
      msNeighborsOf(rows, cols, r, c).forEach(function (p) {
        const key = p[0] + ',' + p[1];
        if (!seen.has(key) && !grid[p[0]][p[1]].revealed && !grid[p[0]][p[1]].flagged && !grid[p[0]][p[1]].mine) {
          seen.add(key);
          queue.push(p);
        }
      });
    }
  }
  return revealed;
}
function msToggleFlag(grid, row, col) {
  const cell = grid[row][col];
  if (cell.revealed) return false;
  cell.flagged = !cell.flagged;
  return true;
}
function msCountFlaggedNeighbors(grid, rows, cols, row, col) {
  let count = 0;
  msNeighborsOf(rows, cols, row, col).forEach(function (p) { if (grid[p[0]][p[1]].flagged) count++; });
  return count;
}
function msChordReveal(grid, rows, cols, row, col) {
  const cell = grid[row][col];
  if (!cell.revealed || cell.mine) return { revealed: [], hitMine: false };
  const flagCount = msCountFlaggedNeighbors(grid, rows, cols, row, col);
  if (flagCount !== cell.adjacent) return { revealed: [], hitMine: false };
  let allRevealed = [];
  let hitMine = false;
  msNeighborsOf(rows, cols, row, col).forEach(function (p) {
    const ncell = grid[p[0]][p[1]];
    if (ncell.revealed || ncell.flagged) return;
    const result = msRevealCell(grid, rows, cols, p[0], p[1]);
    allRevealed = allRevealed.concat(result);
    if (ncell.mine && ncell.revealed) hitMine = true;
  });
  return { revealed: allRevealed, hitMine: hitMine };
}
function msCountRevealedNonMine(grid, rows, cols) {
  let count = 0;
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) if (grid[r][c].revealed && !grid[r][c].mine) count++;
  return count;
}
function msCheckWin(grid, rows, cols, mineCount) { return msCountRevealedNonMine(grid, rows, cols) === rows * cols - mineCount; }
function msCountFlags(grid, rows, cols) {
  let count = 0;
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) if (grid[r][c].flagged) count++;
  return count;
}
function msComputeRoundScore(difficultyKey, secondsElapsed) {
  const base = MS_CONFIG.scoreBaseByDifficulty[difficultyKey] || 100;
  const penalty = Math.min(MS_CONFIG.timeScorePenaltyCap, secondsElapsed * MS_CONFIG.timeScorePenaltyPerSec);
  return Math.max(10, Math.round(base - penalty));
}
// 純函式：回傳「第幾級評語」的index，文字本身由呼叫端從GAME_I18N.ratings取
function msRatingIndex(score) {
  for (let i = 0; i < MS_CONFIG.ratingThresholds.length; i++) {
    if (score <= MS_CONFIG.ratingThresholds[i]) return i;
  }
  return MS_CONFIG.ratingThresholds.length - 1;
}
function msComputeRating(score) {
  const list = (typeof window !== 'undefined' && window.GAME_I18N && window.GAME_I18N.ratings) || [];
  return list[msRatingIndex(score)] || '';
}

// ══════════════════════════════════════════════════════════
// UI層
// ══════════════════════════════════════════════════════════
(function () {
  if (typeof document === 'undefined') return; // 純邏輯測試環境（無DOM）時安靜跳過UI部分
  const scoreEl = document.getElementById('msScore');
  const diffBadge = document.getElementById('msDiffBadge');
  const minesLeftEl = document.getElementById('msMinesLeft');
  const timerEl = document.getElementById('msTimer');
  const faceBtn = document.getElementById('msFaceBtn');
  const flagModeBtn = document.getElementById('msFlagModeBtn');
  const boardEl = document.getElementById('msBoard');
  const overPanel = document.getElementById('msOverPanel');
  const overTitle = document.getElementById('msOverTitle');
  const overSub = document.getElementById('msOverSub');
  const ratingEl = document.getElementById('msRating');
  const bestEl = document.getElementById('msBest');
  const bestDiffEl = document.getElementById('msBestDiff');
  const historyEl = document.getElementById('msHistory');
  const startBtn = document.getElementById('msStartBtn');
  if (!boardEl || !diffBadge) return; // 7-3 防錯：頁面結構不符時不炸掉整頁

  let grid = null, rows = 0, cols = 0, mineCount = 0, difficultyKey = 'beginner', difficultyIndex = 0;
  let roundNumber = 1, firstClickDone = false, playing = false, flagMode = false;
  let score = 0, bestScore = 0, bestDiffIndex = null, bestDiffKey = null, history = [];
  let secondsElapsed = 0, timerHandle = null;

  function stopTimer() { if (timerHandle) { clearInterval(timerHandle); timerHandle = null; } }
  function startTimer() {
    stopTimer();
    secondsElapsed = 0;
    timerEl.textContent = '000';
    timerHandle = setInterval(function () {
      secondsElapsed++;
      timerEl.textContent = String(Math.min(999, secondsElapsed)).padStart(3, '0');
    }, 1000);
  }

  function cellClassAndContent(cell) {
    if (cell.flagged && !cell.revealed) return { cls: 'ms-flagged', text: '🚩' };
    if (!cell.revealed) return { cls: '', text: '' };
    if (cell.mine) return { cls: 'ms-mine', text: '💣' };
    if (cell.adjacent === 0) return { cls: 'ms-revealed', text: '' };
    return { cls: 'ms-revealed ms-c' + cell.adjacent, text: String(cell.adjacent) };
  }

  function renderBoard() {
    boardEl.style.gridTemplateColumns = 'repeat(' + cols + ', 26px)';
    // 7-4 資源清理：每次重新渲染前先清空容器，格子DOM不會隨局數增加而持續累積
    boardEl.innerHTML = '';
    const frag = document.createDocumentFragment();
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const cell = grid[r][c];
        const info = cellClassAndContent(cell);
        const div = document.createElement('div');
        div.className = 'ms-cell' + (info.cls ? ' ' + info.cls : '');
        div.textContent = info.text;
        div.setAttribute('data-r', String(r));
        div.setAttribute('data-c', String(c));
        frag.appendChild(div);
      }
    }
    boardEl.appendChild(frag);
    minesLeftEl.textContent = String(Math.max(0, mineCount - msCountFlags(grid, rows, cols)));
  }

  function loadRound(n) {
    roundNumber = n;
    const diff = msComputeDifficultyForRound(n);
    rows = diff.rows; cols = diff.cols; mineCount = diff.mines;
    difficultyKey = diff.key; difficultyIndex = diff.index;
    grid = msCreateEmptyGrid(rows, cols);
    firstClickDone = false;
    diffBadge.textContent = msDifficultyLabel(difficultyIndex);
    diffBadge.classList.remove('ms-diff-up');
    void diffBadge.offsetWidth;
    diffBadge.classList.add('ms-diff-up');
    minesLeftEl.textContent = String(mineCount);
    faceBtn.textContent = '🙂';
    renderBoard();
  }

  function endRun(won, title, sub) {
    playing = false;
    stopTimer();
    if (!won) {
      // 7-3 防錯：輸的時候把所有地雷翻開讓玩家看清楚全貌，不影響分數計算（分數只計入已經過關的關卡）
      for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) if (grid[r][c].mine) grid[r][c].revealed = true;
      renderBoard();
      faceBtn.textContent = '💀';
    } else {
      faceBtn.textContent = '😎';
    }
    bestScore = Math.max(bestScore, score);
    bestEl.textContent = String(bestScore);
    const diffOrder = { beginner: 1, intermediate: 2, expert: 3 };
    if (!bestDiffKey || diffOrder[difficultyKey] > diffOrder[bestDiffKey]) {
      bestDiffKey = difficultyKey;
      bestDiffIndex = msComputeDifficultyForRound(roundNumber).index;
    }
    bestDiffEl.textContent = msDifficultyLabel(bestDiffIndex);
    ratingEl.textContent = gminesweeperT('scoreShort', { s: score }) + ' — ' + msComputeRating(score);
    window._msLastScore = score;
    window._msBestScore = bestScore;
    if (typeof gaSubmitScore === 'function') gaSubmitScore('minesweeper', score);
    overTitle.textContent = title;
    overSub.textContent = sub;
    overPanel.classList.add('show');
    startBtn.textContent = gminesweeperT('retryBtn');
  }

  function afterCellAction() {
    if (!playing) return;
    if (msCheckWin(grid, rows, cols, mineCount)) {
      const gained = msComputeRoundScore(difficultyKey, secondsElapsed);
      score += gained;
      scoreEl.textContent = String(score);
      history.unshift(gained);
      history = history.slice(0, MS_CONFIG.historyLimit);
      historyEl.innerHTML = history.map(function (v) { return '<span>' + gminesweeperT('scorePlus', { s: v }) + '</span>'; }).join('');
      stopTimer();
      renderBoard();
      faceBtn.textContent = '😎';
      overTitle.textContent = gminesweeperT('clearTitle', { d: msDifficultyLabel(difficultyIndex) });
      overSub.textContent = gminesweeperT('clearSub', { t: secondsElapsed, g: gained });
      overPanel.classList.add('show');
      // 注意：這裡刻意不呼叫startTimer()——計時器要等玩家在新一關實際點下第一格才會啟動
      // （由handleReveal裡的!firstClickDone分支負責），這樣每一關都是「真正動手才開始計時」，
      // 跟第1關的行為保持一致，不會因為晉級動畫的1.8秒延遲被冤枉算進下一關的時間裡
      setTimeout(function () { overPanel.classList.remove('show'); loadRound(roundNumber + 1); playing = true; }, MS_CONFIG.nextRoundDelayMs);
      return;
    }
    renderBoard();
  }

  function handleReveal(r, c) {
    if (!playing) return;
    if (!firstClickDone) {
      msPlaceMines(grid, rows, cols, mineCount, r, c);
      msComputeAdjacentCounts(grid, rows, cols);
      firstClickDone = true;
      startTimer();
    }
    const cell = grid[r][c];
    if (cell.revealed && cell.adjacent > 0) {
      // 已翻開的數字格子被再次點擊，視同chord嘗試（跟雙擊等效，方便單擊裝置操作）
      const chordResult = msChordReveal(grid, rows, cols, r, c);
      if (chordResult.hitMine) { endRun(false, gminesweeperT('boomTitle'), gminesweeperT('boomChordSub', { s: score })); return; }
      afterCellAction();
      return;
    }
    const revealed = msRevealCell(grid, rows, cols, r, c);
    const hitMine = revealed.some(function (p) { return grid[p[0]][p[1]].mine; });
    if (hitMine) { endRun(false, gminesweeperT('boomTitle'), gminesweeperT('boomSub', { n: roundNumber, s: score })); return; }
    afterCellAction();
  }

  function handleFlag(r, c) {
    if (!playing) return;
    msToggleFlag(grid, r, c);
    renderBoard();
  }

  // 事件委派：整個盤面只掛一組監聽器，不隨格子數量增加而累積事件綁定（7-4）
  boardEl.addEventListener('click', function (e) {
    const target = e.target.closest('.ms-cell');
    if (!target) return;
    const r = parseInt(target.getAttribute('data-r'), 10), c = parseInt(target.getAttribute('data-c'), 10);
    if (flagMode) handleFlag(r, c); else handleReveal(r, c);
  });
  boardEl.addEventListener('contextmenu', function (e) {
    e.preventDefault();
    const target = e.target.closest('.ms-cell');
    if (!target) return;
    const r = parseInt(target.getAttribute('data-r'), 10), c = parseInt(target.getAttribute('data-c'), 10);
    handleFlag(r, c);
  });
  boardEl.addEventListener('dblclick', function (e) {
    const target = e.target.closest('.ms-cell');
    if (!target) return;
    const r = parseInt(target.getAttribute('data-r'), 10), c = parseInt(target.getAttribute('data-c'), 10);
    if (!playing) return;
    const chordResult = msChordReveal(grid, rows, cols, r, c);
    if (chordResult.hitMine) { endRun(false, gminesweeperT('boomTitle'), gminesweeperT('boomChordSub', { s: score })); return; }
    afterCellAction();
  });

  function msToggleFlagModeInternal() {
    flagMode = !flagMode;
    flagModeBtn.classList.toggle('active', flagMode);
    flagModeBtn.textContent = flagMode ? gminesweeperT('flagModeOn') : gminesweeperT('flagModeOff');
  }
  window.msToggleFlagMode = msToggleFlagModeInternal;

  function msStartInternal() {
    playing = true;
    score = 0;
    scoreEl.textContent = '0';
    ratingEl.textContent = '';
    overPanel.classList.remove('show');
    loadRound(1);
  }
  window.msStart = msStartInternal;

  window.addEventListener('beforeunload', stopTimer); // 7-4 資源清理
})();

function msShareResult() {
  const score = window._msLastScore;
  const text = (score != null)
    ? gminesweeperT('shareWithScore', { s: score })
    : gminesweeperT('shareNoScore');
  if (navigator.share) {
    navigator.share({ title: document.title, text: text, url: location.href }).catch(function () {});
  } else {
    navigator.clipboard.writeText(text + ' ' + location.href);
    const b = event.target;
    const old = b.textContent;
    b.textContent = gminesweeperT('copied');
    setTimeout(function () { b.textContent = old; }, MS_CONFIG.copyRevertMs);
  }
}

// FAQ 展開收合（7-3 防錯：純邏輯測試環境沒有 document 時安靜跳過，
// 不能讓這一行在無DOM環境直接拋 ReferenceError 導致整支檔案無法被單元測試載入）
if (typeof document !== 'undefined') {
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.addEventListener('click', function () { this.parentElement.classList.toggle('open'); });
  });
}
