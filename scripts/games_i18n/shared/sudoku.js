// ══════════════════════════════════════════════════════════
// 數獨 — 共用遊戲邏輯（所有語言版本共用這一份，2026/08/18 多語言化時抽出）
//
// 【多語言架構約定】
//   這個檔案裡「不能出現任何給使用者看的文字」。所有文字一律透過 gsudokuT('key') 讀取
//   頁面在載入這支JS之前先定義好的 window.GAME_I18N 字典。
//   → 遊戲邏輯有bug只要改這一個檔案，10種語言同時生效
//   → 翻譯只動各語言HTML裡的字典，不會誤改邏輯
//
// 本次多語言化只做三件事：文字外移、變數改名、無DOM防護。
// 產生器（generateFullSolution / generatePuzzle）與回溯求解器（countSolutions）
// 的演算法本體逐字搬移，數值（提示數、節點上限、計分係數）一律原封不動。
//
// 遵循《新工具規劃守則.md》第七節：
//   7-1 SUDOKU_CONFIG集中管理難度級距/計分/安全上限等數值（文字在GAME_I18N）
//   7-2 純函式（產生器/求解器/衝突偵測）跟DOM渲染完全分開，方便單元測試
//   7-3 防錯：求解器有節點數安全上限避免卡死；挖空找不到可移除格就提前結束，不強求剛好命中目標提示數
//   7-4 資源清理：固定81格DOM節點重複利用，計時器在切題/結束時清除
// ══════════════════════════════════════════════════════════

const SUDOKU_CONFIG = {
  // 難度只留 key 與提示數（clues），對應的名稱文字放在 GAME_I18N.difficulties 同樣順序的陣列裡
  difficulties: [
    { key: 'easy', clues: 38 },
    { key: 'medium', clues: 32 },
    { key: 'hard', clues: 27 },
    { key: 'expert', clues: 24 }
  ],
  solverNodeCap: 60000,
  historyLimit: 5,
  copyRevertMs: 1500,
  scorePerPuzzleBase: 100,
  scoreDifficultyMultiplier: { easy: 1, medium: 1.4, hard: 1.9, expert: 2.5 },
  scoreTimePenaltyPerSec: 0.25,
  scoreTimePenaltyCap: 60,
  hintPenalty: 15,
  // 只放門檻數字，對應的評語文字放在 GAME_I18N.ratings 同樣順序的陣列裡
  ratingThresholds: [100, 300, 600, 1000, Infinity]
};

// ── i18n 取字helper（7-3 防錯：缺key不崩潰）──
function gsudokuT(key, vars) {
  const dict = (typeof window !== 'undefined' && window.GAME_I18N) || {};
  let s = dict[key];
  if (typeof s !== 'string') {
    if (typeof console !== 'undefined' && console.warn) console.warn('[sudoku] missing i18n key: ' + key);
    return '';
  }
  if (vars) {
    Object.keys(vars).forEach(function (k) {
      s = s.split('{' + k + '}').join(String(vars[k]));
    });
  }
  return s;
}
// 難度名稱：JS只留索引，文字由 GAME_I18N.difficulties 依同樣順序提供
function skDifficultyLabel(idx) {
  const list = (typeof window !== 'undefined' && window.GAME_I18N && window.GAME_I18N.difficulties) || [];
  return list[idx] || '';
}

// ══════════════════════════════════════════════════════════
// 純函式：數獨產生器/求解器/衝突偵測，不依賴DOM，可獨立單元測試
// ══════════════════════════════════════════════════════════
function skMakeGrid9(fillVal) {
  return Array.from({ length: 9 }, function () { return Array.from({ length: 9 }, function () { return fillVal; }); });
}
function skCloneGrid9(g) { return g.map(function (r) { return r.slice(); }); }
function skShuffleArr(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const t = a[i]; a[i] = a[j]; a[j] = t;
  }
  return a;
}
function skIsValidPlacement(grid, row, col, val) {
  for (let i = 0; i < 9; i++) {
    if (i !== col && grid[row][i] === val) return false;
    if (i !== row && grid[i][col] === val) return false;
  }
  const br = Math.floor(row / 3) * 3, bc = Math.floor(col / 3) * 3;
  for (let r = br; r < br + 3; r++) for (let c = bc; c < bc + 3; c++) { if ((r !== row || c !== col) && grid[r][c] === val) return false; }
  return true;
}
function skFindEmptyCell(grid) {
  for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++) if (grid[r][c] === 0) return [r, c];
  return null;
}
function skFillDiagonalBoxes(grid) {
  for (let b = 0; b < 9; b += 3) {
    const nums = skShuffleArr([1, 2, 3, 4, 5, 6, 7, 8, 9]);
    let idx = 0;
    for (let r = b; r < b + 3; r++) for (let c = b; c < b + 3; c++) grid[r][c] = nums[idx++];
  }
}
function skFillGridBacktrack(grid) {
  const pos = skFindEmptyCell(grid);
  if (!pos) return true;
  const r = pos[0], c = pos[1];
  const nums = skShuffleArr([1, 2, 3, 4, 5, 6, 7, 8, 9]);
  for (let i = 0; i < nums.length; i++) {
    const v = nums[i];
    if (skIsValidPlacement(grid, r, c, v)) {
      grid[r][c] = v;
      if (skFillGridBacktrack(grid)) return true;
      grid[r][c] = 0;
    }
  }
  return false;
}
function skGenerateFullSolution() {
  const g = skMakeGrid9(0);
  skFillDiagonalBoxes(g);
  skFillGridBacktrack(g);
  return g;
}
function skCountSolutions(grid, cap) {
  let count = 0, nodes = 0;
  const g = skCloneGrid9(grid);
  function helper() {
    if (count >= cap) return;
    nodes++;
    if (nodes > SUDOKU_CONFIG.solverNodeCap) { count = cap; return; } // 7-3 防錯：超過安全上限視為不安全（保守判定非唯一解）
    const pos = skFindEmptyCell(g);
    if (!pos) { count++; return; }
    const r = pos[0], c = pos[1];
    for (let v = 1; v <= 9; v++) {
      if (count >= cap) return;
      if (skIsValidPlacement(g, r, c, v)) {
        g[r][c] = v;
        helper();
        g[r][c] = 0;
        if (count >= cap) return;
      }
    }
  }
  helper();
  return count;
}
function skGeneratePuzzle(targetClues) {
  const solution = skGenerateFullSolution();
  const puzzle = skCloneGrid9(solution);
  const positions = skShuffleArr(Array.from({ length: 81 }, function (_, i) { return i; }));
  let clueCount = 81;
  for (let i = 0; i < positions.length; i++) {
    if (clueCount <= targetClues) break;
    const r = Math.floor(positions[i] / 9), c = positions[i] % 9;
    if (puzzle[r][c] === 0) continue;
    const backup = puzzle[r][c];
    puzzle[r][c] = 0;
    const solCount = skCountSolutions(puzzle, 2);
    if (solCount !== 1) { puzzle[r][c] = backup; } // 唯一解才允許挖空，否則還原（7-3 防錯：不產生無解/多解題目）
    else { clueCount--; }
  }
  return { puzzle: puzzle, solution: solution, clueCount: clueCount };
}
function skComputeConflictCells(grid) {
  const conflicts = {};
  function mark(keys) { if (keys.length > 1) keys.forEach(function (k) { conflicts[k] = true; }); }
  for (let r = 0; r < 9; r++) {
    const seen = {};
    for (let c = 0; c < 9; c++) { const v = grid[r][c]; if (!v) continue; (seen[v] = seen[v] || []).push(r + ',' + c); }
    Object.keys(seen).forEach(function (k) { mark(seen[k]); });
  }
  for (let c = 0; c < 9; c++) {
    const seen = {};
    for (let r = 0; r < 9; r++) { const v = grid[r][c]; if (!v) continue; (seen[v] = seen[v] || []).push(r + ',' + c); }
    Object.keys(seen).forEach(function (k) { mark(seen[k]); });
  }
  for (let br = 0; br < 9; br += 3) {
    for (let bc = 0; bc < 9; bc += 3) {
      const seen = {};
      for (let r = br; r < br + 3; r++) for (let c = bc; c < bc + 3; c++) { const v = grid[r][c]; if (!v) continue; (seen[v] = seen[v] || []).push(r + ',' + c); }
      Object.keys(seen).forEach(function (k) { mark(seen[k]); });
    }
  }
  return conflicts;
}
function skIsGridComplete(grid, solution) {
  for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++) if (grid[r][c] !== solution[r][c]) return false;
  return true;
}
function skComputeDifficultyIndex(puzzleNumber) {
  return Math.min(SUDOKU_CONFIG.difficulties.length - 1, puzzleNumber - 1);
}
function skComputePuzzleScore(diffKey, seconds) {
  const mult = SUDOKU_CONFIG.scoreDifficultyMultiplier[diffKey] || 1;
  const penalty = Math.min(SUDOKU_CONFIG.scoreTimePenaltyCap, seconds * SUDOKU_CONFIG.scoreTimePenaltyPerSec);
  return Math.max(20, Math.round(SUDOKU_CONFIG.scorePerPuzzleBase * mult - penalty));
}
// 純函式：回傳「第幾級評語」的index，文字本身由呼叫端從GAME_I18N.ratings取
function skRatingIndex(score) {
  for (let i = 0; i < SUDOKU_CONFIG.ratingThresholds.length; i++) {
    if (score <= SUDOKU_CONFIG.ratingThresholds[i]) return i;
  }
  return SUDOKU_CONFIG.ratingThresholds.length - 1;
}
function skComputeRating(score) {
  const list = (typeof window !== 'undefined' && window.GAME_I18N && window.GAME_I18N.ratings) || [];
  return list[skRatingIndex(score)] || '';
}

(function () {
  if (typeof document === 'undefined') return; // 純邏輯測試環境（無DOM）時安靜跳過UI部分
  const gridEl = document.getElementById('skGrid');
  const numpadEl = document.getElementById('skNumpad');
  const overlay = document.getElementById('skOverlay');
  const overTitle = document.getElementById('skOverTitle');
  const overSub = document.getElementById('skOverSub');
  const scoreEl = document.getElementById('skScore');
  const diffBadge = document.getElementById('skDiffBadge');
  const puzzleNumEl = document.getElementById('skPuzzleNum');
  const timerEl = document.getElementById('skTimer');
  const ratingEl = document.getElementById('skRating');
  const bestEl = document.getElementById('skBest');
  const bestDiffEl = document.getElementById('skBestDiff');
  const historyEl = document.getElementById('skHistory');
  const startBtn = document.getElementById('skStartBtn');
  if (!gridEl || !numpadEl) return; // 7-3 防錯：頁面結構不符時不炸掉整頁

  let puzzle = null, solution = null, given = null, hinted = null;
  let selected = null;
  let playing = false;
  let score = 0, bestScore = 0, bestDiffIdx = -1, history = [];
  let puzzleNumber = 0, timerId = null, secondsElapsed = 0;

  function buildNumpad() {
    let html = '';
    for (let n = 1; n <= 9; n++) html += '<button onclick="skInputDigit(' + n + ')">' + n + '</button>';
    html += '<button class="sk-clear" onclick="skInputDigit(0)">' + gsudokuT('clearCell') + '</button>';
    numpadEl.innerHTML = html;
  }

  function render() {
    const conflicts = skComputeConflictCells(puzzle);
    const selVal = selected && puzzle[selected[0]][selected[1]] ? puzzle[selected[0]][selected[1]] : null;
    let html = '';
    for (let r = 0; r < 9; r++) {
      for (let c = 0; c < 9; c++) {
        const v = puzzle[r][c];
        const key = r + ',' + c;
        const isGiven = given[r][c] !== 0;
        const isSel = selected && selected[0] === r && selected[1] === c;
        const isPeer = selected && !isSel && (selected[0] === r || selected[1] === c || (Math.floor(selected[0] / 3) === Math.floor(r / 3) && Math.floor(selected[1] / 3) === Math.floor(c / 3)));
        const isSameVal = selVal && v === selVal && !isSel;
        let cls = 'sk-cell';
        if (isGiven) cls += ' sk-given';
        if (isPeer) cls += ' sk-peer';
        if (isSameVal) cls += ' sk-same-value';
        if (isSel) cls += ' sk-selected';
        if (conflicts[key]) cls += ' sk-conflict';
        if (hinted[r][c]) cls += ' sk-hinted';
        html += '<div class="' + cls + '" data-r="' + r + '" data-c="' + c + '">' + (v || '') + '</div>';
      }
    }
    gridEl.innerHTML = html;
    Array.prototype.forEach.call(gridEl.querySelectorAll('.sk-cell'), function (cell) {
      cell.addEventListener('pointerdown', function () {
        const r = parseInt(cell.getAttribute('data-r'), 10), c = parseInt(cell.getAttribute('data-c'), 10);
        if (given[r][c] !== 0) return; // 7-3 防錯：給定格不可選取修改
        selected = [r, c];
        render();
      });
    });
  }

  function formatTime(sec) {
    const m = Math.floor(sec / 60), s = sec % 60;
    return (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
  }
  function startTimer() {
    stopTimer();
    secondsElapsed = 0;
    timerEl.textContent = formatTime(0);
    timerId = setInterval(function () { secondsElapsed++; timerEl.textContent = formatTime(secondsElapsed); }, 1000);
  }
  function stopTimer() { if (timerId) { clearInterval(timerId); timerId = null; } } // 7-4 資源清理

  function loadPuzzle(number) {
    puzzleNumber = number;
    const diffIdx = skComputeDifficultyIndex(puzzleNumber);
    const diff = SUDOKU_CONFIG.difficulties[diffIdx];
    diffBadge.textContent = skDifficultyLabel(diffIdx);
    diffBadge.classList.remove('sk-diff-up');
    void diffBadge.offsetWidth;
    diffBadge.classList.add('sk-diff-up');
    puzzleNumEl.textContent = String(puzzleNumber);

    const gen = skGeneratePuzzle(diff.clues);
    puzzle = gen.puzzle;
    solution = gen.solution;
    given = skCloneGrid9(gen.puzzle);
    hinted = skMakeGrid9(0);
    selected = null;
    startTimer();
    render();
  }

  window.skInputDigit = function (n) {
    if (!playing || !selected) return;
    const r = selected[0], c = selected[1];
    if (given[r][c] !== 0) return; // 7-3 防錯：不可覆蓋給定格
    puzzle[r][c] = n;
    hinted[r][c] = 0; // 玩家自己改動這格就不再算提示格
    render();
    checkWin();
  };
  window.addEventListener('keydown', function (e) {
    if (!playing || !selected) return;
    if (e.key >= '1' && e.key <= '9') { window.skInputDigit(parseInt(e.key, 10)); }
    else if (e.key === 'Backspace' || e.key === 'Delete' || e.key === '0') { window.skInputDigit(0); }
    else if (e.key === 'ArrowUp' || e.key === 'ArrowDown' || e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
      e.preventDefault();
      let [r, c] = selected;
      if (e.key === 'ArrowUp') r = Math.max(0, r - 1);
      if (e.key === 'ArrowDown') r = Math.min(8, r + 1);
      if (e.key === 'ArrowLeft') c = Math.max(0, c - 1);
      if (e.key === 'ArrowRight') c = Math.min(8, c + 1);
      selected = [r, c];
      render();
    }
  });

  window.skHint = function () {
    if (!playing) return;
    const emptyOrWrong = [];
    for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++) { if (given[r][c] === 0 && puzzle[r][c] !== solution[r][c]) emptyOrWrong.push([r, c]); }
    if (!emptyOrWrong.length) return; // 7-3 防錯：沒有可提示的格子就不動作
    const pick = emptyOrWrong[Math.floor(Math.random() * emptyOrWrong.length)];
    puzzle[pick[0]][pick[1]] = solution[pick[0]][pick[1]];
    hinted[pick[0]][pick[1]] = 1;
    score = Math.max(0, score - SUDOKU_CONFIG.hintPenalty);
    scoreEl.textContent = String(score);
    render();
    checkWin();
  };
  window.skClearEntries = function () {
    if (!playing) return;
    for (let r = 0; r < 9; r++) for (let c = 0; c < 9; c++) { if (given[r][c] === 0) { puzzle[r][c] = 0; hinted[r][c] = 0; } }
    render();
  };

  function checkWin() {
    if (!skIsGridComplete(puzzle, solution)) return;
    stopTimer();
    const diffIdx = skComputeDifficultyIndex(puzzleNumber);
    const diff = SUDOKU_CONFIG.difficulties[diffIdx];
    const gained = skComputePuzzleScore(diff.key, secondsElapsed);
    score += gained;
    scoreEl.textContent = String(score);

    // 每一題的得分（不是累積總分）記錄進歷史列表，方便看最近幾題手感
    history.unshift(gained);
    history = history.slice(0, SUDOKU_CONFIG.historyLimit);
    historyEl.innerHTML = history.map(function (v) { return '<span>' + gsudokuT('scoreShort', { s: v }) + '</span>'; }).join('');

    // 最佳成績＝這個瀏覽階段裡任一輪跑出來的最高累積分數；最高難度＝曾經到達過的最高難度層級
    bestScore = Math.max(bestScore, score);
    bestEl.textContent = String(bestScore);
    if (bestDiffIdx < 0 || diffIdx >= bestDiffIdx) {
      bestDiffIdx = diffIdx;
    }
    bestDiffEl.textContent = skDifficultyLabel(bestDiffIdx);
    ratingEl.textContent = gsudokuT('scoreShort', { s: score }) + ' — ' + skComputeRating(score);
    window._skLastScore = score;
    window._skBestScore = bestScore;
    if (typeof gaSubmitScore === 'function') gaSubmitScore('sudoku', score);

    overTitle.textContent = gsudokuT('puzzleDone', { n: puzzleNumber });
    overSub.textContent = gsudokuT('nextUp', {
      t: formatTime(secondsElapsed),
      g: gained,
      d: skDifficultyLabel(skComputeDifficultyIndex(puzzleNumber + 1))
    });
    overlay.classList.add('show');
    setTimeout(function () {
      overlay.classList.remove('show');
      loadPuzzle(puzzleNumber + 1);
    }, 1800);
  }

  function skStartInternal() {
    playing = true;
    score = 0;
    scoreEl.textContent = '0';
    ratingEl.textContent = '';
    overlay.classList.remove('show');
    startBtn.textContent = gsudokuT('restartRound');
    loadPuzzle(1);
  }
  window.skStart = skStartInternal;

  window.addEventListener('beforeunload', stopTimer); // 7-4 資源清理

  buildNumpad();
})();

function skShareResult() {
  const score = window._skLastScore;
  const text = (score != null)
    ? gsudokuT('shareWithScore', { s: score })
    : gsudokuT('shareNoScore');
  if (navigator.share) {
    navigator.share({ title: document.title, text: text, url: location.href }).catch(function () {});
  } else {
    navigator.clipboard.writeText(text + ' ' + location.href);
    const b = event.target;
    const old = b.textContent;
    b.textContent = gsudokuT('copied');
    setTimeout(function () { b.textContent = old; }, SUDOKU_CONFIG.copyRevertMs);
  }
}
// FAQ 展開收合（7-3 防錯：純邏輯測試環境沒有 document 時安靜跳過，
// 不能讓這一行在無DOM環境直接拋 ReferenceError 導致整支檔案無法被單元測試載入）
if (typeof document !== 'undefined') {
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.addEventListener('click', function () { this.parentElement.classList.toggle('open'); });
  });
}
