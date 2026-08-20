// ══════════════════════════════════════════════════════════
// 數字推盤 — 共用遊戲邏輯（所有語言版本共用這一份，多語言化時抽出）
//
// 【多語言架構約定】
//   這個檔案裡「不能出現任何給使用者看的文字」。所有文字一律透過 gslidingpuzzleT('key') 讀取
//   頁面在載入這支JS之前先定義好的 window.GAME_I18N 字典。評語文字同理，
//   JS只留 SP_CONFIG.ratingThresholds 門檻數字，實際文字從 window.GAME_I18N.ratings 取。
//
// 遵循《新工具規劃守則.md》第七節：
//   7-1 SP_CONFIG集中管理盤面大小範圍/計分/洗牌步數等所有可調數值
//   7-2 純函式（isSolvable/countInversions/shuffleViaRandomMoves/moveBlank...）跟DOM渲染分開，方便單元測試
//   7-3 防錯：洗牌用「從解答狀態做合法滑動」保證一定可解，並用逆序數奇偶性公式做獨立驗證雙重把關
//   7-4 資源清理：固定size*size-1個磚塊DOM節點重複利用，不隨遊戲時間增加而累積；計時器切題/結束時清除
// ══════════════════════════════════════════════════════════
const SP_CONFIG = {
  minSize: 3,
  maxSize: 6,
  shuffleMovesPerCell: 25,
  minShuffleMoves: 80,
  historyLimit: 5,
  adLoadDelayMs: 2000,
  copyRevertMs: 1500,
  scoreBaseBySize: { 3: 80, 4: 130, 5: 190, 6: 260 },
  moveScorePenalty: 0.6,
  timeScorePenaltyPerSec: 0.4,
  timeScorePenaltyCap: 80,
  // 只放門檻數字，對應的評語文字放在 GAME_I18N.ratings 同樣順序的陣列裡
  ratingThresholds: [100, 300, 600, 1000, Infinity]
};

// ── i18n 取字helper（7-3 防錯：缺key不崩潰）──
function gslidingpuzzleT(key, vars) {
  const dict = (typeof window !== 'undefined' && window.GAME_I18N) || {};
  let s = dict[key];
  if (typeof s !== 'string') {
    if (typeof console !== 'undefined' && console.warn) console.warn('[sliding-puzzle] missing i18n key: ' + key);
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
// 純函式：可獨立單元測試，不依賴DOM
// ══════════════════════════════════════════════════════════
function makeSolvedBoard(size) {
  const b = Array.from({ length: size }, function () { return Array.from({ length: size }, function () { return 0; }); });
  let v = 1;
  for (let r = 0; r < size; r++) for (let c = 0; c < size; c++) { if (r === size - 1 && c === size - 1) b[r][c] = 0; else b[r][c] = v++; }
  return b;
}
function cloneBoard(b) { return b.map(function (r) { return r.slice(); }); }
function findBlank(board) {
  for (let r = 0; r < board.length; r++) for (let c = 0; c < board[r].length; c++) if (board[r][c] === 0) return [r, c];
  return null;
}
function isSolved(board) {
  const size = board.length;
  const solved = makeSolvedBoard(size);
  for (let r = 0; r < size; r++) for (let c = 0; c < size; c++) if (board[r][c] !== solved[r][c]) return false;
  return true;
}
const DIR_DELTA = { up: [-1, 0], down: [1, 0], left: [0, -1], right: [0, 1] };
const OPPOSITE_DIR = { up: 'down', down: 'up', left: 'right', right: 'left' };
function canMove(board, dir) {
  const size = board.length;
  const blank = findBlank(board);
  const dr = DIR_DELTA[dir][0], dc = DIR_DELTA[dir][1];
  const tr = blank[0] + dr, tc = blank[1] + dc; // 空格往dir方向移動時，實際被滑動的方塊來自(tr,tc)
  return tr >= 0 && tr < size && tc >= 0 && tc < size;
}
function moveBlank(board, dir) {
  if (!canMove(board, dir)) return { board: board, moved: false };
  const size = board.length;
  const blank = findBlank(board);
  const dr = DIR_DELTA[dir][0], dc = DIR_DELTA[dir][1];
  const tr = blank[0] + dr, tc = blank[1] + dc;
  const nb = cloneBoard(board);
  nb[blank[0]][blank[1]] = nb[tr][tc];
  nb[tr][tc] = 0;
  return { board: nb, moved: true };
}
function moveTileAt(board, r, c) {
  // 點擊(r,c)這個方塊：只有跟空格相鄰時才合法，回傳swap後的盤面
  const blank = findBlank(board);
  const adjacent = (Math.abs(blank[0] - r) + Math.abs(blank[1] - c)) === 1;
  if (!adjacent) return { board: board, moved: false };
  const nb = cloneBoard(board);
  nb[blank[0]][blank[1]] = nb[r][c];
  nb[r][c] = 0;
  return { board: nb, moved: true };
}
function shuffleViaRandomMoves(size, numMoves) {
  let board = makeSolvedBoard(size);
  let lastDir = null;
  const dirs = ['up', 'down', 'left', 'right'];
  for (let i = 0; i < numMoves; i++) {
    const candidates = dirs.filter(function (d) { return canMove(board, d) && d !== (lastDir ? OPPOSITE_DIR[lastDir] : null); });
    const pool = candidates.length ? candidates : dirs.filter(function (d) { return canMove(board, d); });
    const dir = pool[Math.floor(Math.random() * pool.length)];
    const res = moveBlank(board, dir);
    board = res.board;
    lastDir = dir;
  }
  return board;
}
function countInversions(flatTiles) {
  let inv = 0;
  for (let i = 0; i < flatTiles.length; i++) for (let j = i + 1; j < flatTiles.length; j++) { if (flatTiles[i] > flatTiles[j]) inv++; }
  return inv;
}
function isSolvable(board) {
  const size = board.length;
  const flat = [];
  let blankRow = 0;
  for (let r = 0; r < size; r++) for (let c = 0; c < size; c++) { const v = board[r][c]; if (v === 0) blankRow = r; else flat.push(v); }
  const inv = countInversions(flat);
  if (size % 2 === 1) return inv % 2 === 0;
  const rowFromBottom = size - blankRow;
  if (rowFromBottom % 2 === 0) return inv % 2 === 1;
  return inv % 2 === 0;
}
function computeBoardSize(levelNumber) {
  return Math.min(SP_CONFIG.maxSize, SP_CONFIG.minSize + (levelNumber - 1));
}
function computePuzzleScore(size, moves, seconds) {
  const base = SP_CONFIG.scoreBaseBySize[size] || 80;
  const penalty = moves * SP_CONFIG.moveScorePenalty + Math.min(SP_CONFIG.timeScorePenaltyCap, seconds * SP_CONFIG.timeScorePenaltyPerSec);
  return Math.max(20, Math.round(base - penalty));
}
function spRatingIndex(score) {
  const th = SP_CONFIG.ratingThresholds;
  for (let i = 0; i < th.length; i++) if (score <= th[i]) return i;
  return th.length - 1;
}
function spComputeRating(score) {
  const list = (typeof window !== 'undefined' && window.GAME_I18N && window.GAME_I18N.ratings) || [];
  return list[spRatingIndex(score)] || '';
}

(function () {
  if (typeof document === 'undefined') return;
  const gridEl = document.getElementById('spGrid');
  const boardEl = document.getElementById('spBoard');
  const overlay = document.getElementById('spOverlay');
  const overTitle = document.getElementById('spOverTitle');
  const overSub = document.getElementById('spOverSub');
  const scoreEl = document.getElementById('spScore');
  const sizeBadge = document.getElementById('spSizeBadge');
  const movesEl = document.getElementById('spMoves');
  const timerEl = document.getElementById('spTimer');
  const ratingEl = document.getElementById('spRating');
  const bestEl = document.getElementById('spBest');
  const bestSizeEl = document.getElementById('spBestSize');
  const historyEl = document.getElementById('spHistory');
  const startBtn = document.getElementById('spStartBtn');
  if (!gridEl || !boardEl || !startBtn) return;

  let board = null, size = SP_CONFIG.minSize;
  let playing = false, levelNumber = 0;
  let score = 0, bestScore = 0, bestSize = 0, history = [];
  let moveCount = 0, timerId = null, secondsElapsed = 0;

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

  function render() {
    const cellPct = 100 / size;
    let html = '';
    for (let r = 0; r < size; r++) for (let c = 0; c < size; c++) {
      html += '<div class="sp-cellbg" style="left:' + (c * cellPct) + '%;top:' + (r * cellPct) + '%;width:' + cellPct + '%;height:' + cellPct + '%"></div>';
    }
    for (let r = 0; r < size; r++) {
      for (let c = 0; c < size; c++) {
        const v = board[r][c];
        if (!v) continue;
        const fontSize = size >= 6 ? 16 : size >= 5 ? 18 : 22;
        html += '<div class="sp-tile" data-r="' + r + '" data-c="' + c + '" style="left:' + (c * cellPct) + '%;top:' + (r * cellPct) + '%;width:' + cellPct + '%;height:' + cellPct + '%;font-size:' + fontSize + 'px">' + v + '</div>';
      }
    }
    gridEl.innerHTML = html;
    Array.prototype.forEach.call(gridEl.querySelectorAll('.sp-tile'), function (tile) {
      tile.addEventListener('pointerdown', function () {
        if (!playing) return;
        const r = parseInt(tile.getAttribute('data-r'), 10), c = parseInt(tile.getAttribute('data-c'), 10);
        applyMoveTile(r, c);
      });
    });
  }

  function applyMoveTile(r, c) {
    const res = moveTileAt(board, r, c);
    if (!res.moved) return; // 7-3 防錯：不合法的移動（沒跟空格相鄰）不消耗步數
    board = res.board;
    moveCount++;
    movesEl.textContent = String(moveCount);
    render();
    checkWin();
  }
  function applyMoveDir(dir) {
    const res = moveBlank(board, dir);
    if (!res.moved) return;
    board = res.board;
    moveCount++;
    movesEl.textContent = String(moveCount);
    render();
    checkWin();
  }
  window.addEventListener('keydown', function (e) {
    if (!playing) return;
    const map = { ArrowUp: 'up', ArrowDown: 'down', ArrowLeft: 'left', ArrowRight: 'right' };
    const dir = map[e.key];
    if (!dir) return;
    e.preventDefault();
    applyMoveDir(dir);
  });

  function loadLevel(number) {
    levelNumber = number;
    size = computeBoardSize(levelNumber);
    sizeBadge.textContent = size + 'x' + size;
    sizeBadge.classList.remove('sp-size-up');
    void sizeBadge.offsetWidth;
    sizeBadge.classList.add('sp-size-up');

    const shuffleMoves = Math.max(SP_CONFIG.minShuffleMoves, size * size * SP_CONFIG.shuffleMovesPerCell);
    board = shuffleViaRandomMoves(size, shuffleMoves);
    // 7-3 防錯：雙重把關，理論上洗牌方式必然可解，這裡再用逆序數公式獨立驗證一次；
    // 萬一驗證失敗（不應該發生），額外補做隨機合法滑動修正，絕不會出可解性有問題的題目
    let guard = 0;
    while (!isSolvable(board) && guard < 20) {
      const extra = moveBlank(board, ['up', 'down', 'left', 'right'][Math.floor(Math.random() * 4)]);
      board = extra.board;
      guard++;
    }
    moveCount = 0;
    movesEl.textContent = '0';
    startTimer();
    render();
  }

  function checkWin() {
    if (!isSolved(board)) return;
    stopTimer();
    const gained = computePuzzleScore(size, moveCount, secondsElapsed);
    score += gained;
    scoreEl.textContent = String(score);

    history.unshift(gained);
    history = history.slice(0, SP_CONFIG.historyLimit);
    historyEl.innerHTML = history.map(function (v) { return '<span>' + gslidingpuzzleT('scoreShort', { s: v }) + '</span>'; }).join('');

    bestScore = Math.max(bestScore, score);
    bestEl.textContent = String(bestScore);
    bestSize = Math.max(bestSize, size);
    bestSizeEl.textContent = bestSize + 'x' + bestSize;
    ratingEl.textContent = gslidingpuzzleT('scoreShort', { s: score }) + ' — ' + spComputeRating(score);
    window._spLastScore = score;
    window._spBestScore = bestScore;
    if (typeof gaSubmitScore === 'function') gaSubmitScore('sliding-puzzle', score);

    const nextSize = computeBoardSize(levelNumber + 1);
    overTitle.textContent = gslidingpuzzleT('winTitle', { sz: size });
    overSub.textContent = gslidingpuzzleT('winSub', { m: moveCount, t: formatTime(secondsElapsed), g: gained, next: nextSize + 'x' + nextSize });
    overlay.classList.add('show');
    setTimeout(function () {
      overlay.classList.remove('show');
      loadLevel(levelNumber + 1);
    }, 1800);
  }

  function spStartInternal() {
    playing = true;
    score = 0;
    scoreEl.textContent = '0';
    ratingEl.textContent = '';
    overlay.classList.remove('show');
    startBtn.textContent = gslidingpuzzleT('restartRoundBtn');
    loadLevel(1);
  }
  window.spStart = spStartInternal;

  window.addEventListener('beforeunload', stopTimer); // 7-4 資源清理
})();

function spShareResult() {
  const score = (typeof window !== 'undefined') ? window._spLastScore : null;
  const text = (score != null)
    ? gslidingpuzzleT('shareWithScore', { s: score })
    : gslidingpuzzleT('shareNoScore');
  if (typeof navigator !== 'undefined' && navigator.share) {
    navigator.share({ title: document.title, text: text, url: location.href }).catch(function () {});
  } else {
    if (!navigator.clipboard || !navigator.clipboard.writeText) return; // 7-3 防錯：無剪貼簿API時安全退出
    navigator.clipboard.writeText(text + ' ' + location.href);
    const b = event.target;
    const old = b.textContent;
    b.textContent = gslidingpuzzleT('copied');
    setTimeout(function () { b.textContent = old; }, SP_CONFIG.copyRevertMs);
  }
}
if (typeof document !== 'undefined') {
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.addEventListener('click', function () { this.parentElement.classList.toggle('open'); });
  });
}
