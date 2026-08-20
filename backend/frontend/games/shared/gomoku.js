// ══════════════════════════════════════════════════════════
// 五子棋 — 共用遊戲邏輯（所有語言版本共用這一份，多語言化時抽出）
//
// 【多語言架構約定】
//   這個檔案裡「不能出現任何給使用者看的文字」。所有文字一律透過 ggomokuT('key') 讀取
//   頁面在載入這支JS之前先定義好的 window.GAME_I18N 字典。
//
// 遵循《新工具規劃守則.md》第七節：
//   7-1 GK_CONFIG集中管理棋盤大小/連線長度/棋子顏色/AI思考延遲等所有可調數值
//   7-2 純函式（checkWin/cellThreatScore/pickAiMove等）完全不碰DOM，
//        AI邏輯可以獨立測試、重用
//   7-3 防錯：格子已有棋子、遊戲已結束、電腦思考中點擊一律無效
//   7-4 資源清理：電腦「思考中」的setTimeout存id，重新開始/切換模式/
//        離開頁面前統一清除
//
//   2026/08/15 全部重寫：帥哥鴻反饋「四子棋是錯的，我要的是五子棋，
//   而且點擊時放不到對應的位置，每次都出現在最低的位置」——
//   原本的四子棋（Connect Four，7x6棋盤、棋子會因重力落到欄位最底端）
//   從一開始就不是使用者要的遊戲。這裡改成正確的五子棋：15x15棋盤、
//   點哪裡棋子就精確出現在那裡（不受重力影響）、連成5顆才獲勝。
//   AI改用即時威脅評分（活三/衝四等棋型分數）+ 立即獲勝/立即防守
//   的判斷邏輯（不是搬用四子棋的minimax，因為15x15棋盤搜尋空間太大
//   不適合深度搜尋），已用Node.js單元測試驗證：橫/直/斜恰好5連線才
//   判定獲勝（4連線不算）、點擊位置與棋子落點完全一致、AI會正確
//   把握自己的獲勝機會、擋下對手的獲勝威脅、開局佔中央、並會處理
//   對手的「活三」局面。
// ══════════════════════════════════════════════════════════
const GK_CONFIG = {
  boardSize: 15,
  winLength: 5,
  playerClass: { 1: 'p1', 2: 'p2' },
  playerColor: { 1: '#0f172a', 2: '#ffffff' },
  aiThinkMsMin: 350,
  aiThinkMsMax: 650,
  copyRevertMs: 1500,
  adLoadDelayMs: 2000
};
const GK_DIRS = [[1, 0], [0, 1], [1, 1], [1, -1]];

// ── i18n 取字helper（7-3 防錯：缺key不崩潰）──
function ggomokuT(key, vars) {
  const dict = (typeof window !== 'undefined' && window.GAME_I18N) || {};
  let s = dict[key];
  if (typeof s !== 'string') {
    if (typeof console !== 'undefined' && console.warn) console.warn('[gomoku] missing i18n key: ' + key);
    return '';
  }
  if (vars) {
    Object.keys(vars).forEach(function (k) {
      s = s.split('{' + k + '}').join(String(vars[k]));
    });
  }
  return s;
}
// 純函式：依模式('ai'/'2p')與玩家編號(1/2)取顯示名稱
// （逐一用字面量 key 呼叫 ggomokuT，這樣驗證器的自動掃描才抓得到這幾個key）
function gkPlayerName(mode, player) {
  if (mode === 'ai') return player === 1 ? ggomokuT('nameYou') : ggomokuT('nameComputer');
  return player === 1 ? ggomokuT('namePlayer1') : ggomokuT('namePlayer2');
}

// ── 純函式：不碰DOM，只操作資料 ──
function createEmptyBoard(size) {
  return Array.from({ length: size }, function () { return Array(size).fill(0); });
}
function inBounds(x, y, size) { return x >= 0 && x < size && y >= 0 && y < size; }

function checkWin(board, x, y, player, size, winLen) {
  for (const [dx, dy] of GK_DIRS) {
    const cells = [[x, y]];
    for (const sign of [1, -1]) {
      let cx = x + dx * sign, cy = y + dy * sign;
      while (inBounds(cx, cy, size) && board[cy][cx] === player) {
        cells.push([cx, cy]);
        cx += dx * sign; cy += dy * sign;
      }
    }
    if (cells.length >= winLen) return cells;
  }
  return null;
}
function isBoardFull(board) {
  return board.every(function (row) { return row.every(function (v) { return v !== 0; }); });
}
function countDirection(board, x, y, dx, dy, player, size) {
  let n = 0, cx = x + dx, cy = y + dy;
  while (inBounds(cx, cy, size) && board[cy][cx] === player) { n++; cx += dx; cy += dy; }
  return n;
}
function patternScore(count, openEnds, winLen) {
  if (count >= winLen) return 100000;
  if (count === winLen - 1 && openEnds === 2) return 10000;
  if (count === winLen - 1 && openEnds === 1) return 1000;
  if (count === winLen - 2 && openEnds === 2) return 800;
  if (count === winLen - 2 && openEnds === 1) return 150;
  if (count === winLen - 3 && openEnds === 2) return 100;
  if (count === winLen - 3 && openEnds === 1) return 20;
  if (openEnds === 2) return 10;
  return 1;
}
function lineScoreAt(board, size, x, y, dx, dy, player, winLen) {
  const fwd = countDirection(board, x, y, dx, dy, player, size);
  const bwd = countDirection(board, x, y, -dx, -dy, player, size);
  const count = 1 + fwd + bwd;
  const posEndX = x + dx * (fwd + 1), posEndY = y + dy * (fwd + 1);
  const negEndX = x - dx * (bwd + 1), negEndY = y - dy * (bwd + 1);
  let openEnds = 0;
  if (inBounds(posEndX, posEndY, size) && board[posEndY][posEndX] === 0) openEnds++;
  if (inBounds(negEndX, negEndY, size) && board[negEndY][negEndX] === 0) openEnds++;
  return patternScore(count, openEnds, winLen);
}
function cellThreatScore(board, size, x, y, player, winLen) {
  let total = 0;
  for (const [dx, dy] of GK_DIRS) total += lineScoreAt(board, size, x, y, dx, dy, player, winLen);
  return total;
}
function placeStoneImmutable(board, x, y, player) {
  const nb = board.map(function (row) { return row.slice(); });
  nb[y][x] = player;
  return nb;
}
function candidateCells(board, size) {
  const has = board.some(function (row) { return row.some(function (v) { return v !== 0; }); });
  if (!has) return [{ x: Math.floor(size / 2), y: Math.floor(size / 2) }];
  const seen = new Set();
  const out = [];
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      if (board[y][x] !== 0) continue;
      let near = false;
      for (let dy = -2; dy <= 2 && !near; dy++) {
        for (let dx = -2; dx <= 2 && !near; dx++) {
          const nx = x + dx, ny = y + dy;
          if (inBounds(nx, ny, size) && board[ny][nx] !== 0) near = true;
        }
      }
      if (near) { const k = x + ',' + y; if (!seen.has(k)) { seen.add(k); out.push({ x: x, y: y }); } }
    }
  }
  return out;
}
// AI：立即獲勝優先 → 立即防守優先 → 威脅評分（攻擊分+防守分*1.1）挑最高分的格子
function pickAiMove(board, size, aiPlayer, humanPlayer, winLen) {
  const candidates = candidateCells(board, size);

  for (const c of candidates) {
    if (checkWin(placeStoneImmutable(board, c.x, c.y, aiPlayer), c.x, c.y, aiPlayer, size, winLen)) return c;
  }
  const blockers = [];
  for (const c of candidates) {
    if (checkWin(placeStoneImmutable(board, c.x, c.y, humanPlayer), c.x, c.y, humanPlayer, size, winLen)) blockers.push(c);
  }
  if (blockers.length) {
    blockers.sort(function (a, b) {
      return cellThreatScore(board, size, b.x, b.y, aiPlayer, winLen) - cellThreatScore(board, size, a.x, a.y, aiPlayer, winLen);
    });
    return blockers[0];
  }
  let best = candidates[0], bestScore = -Infinity;
  for (const c of candidates) {
    const off = cellThreatScore(board, size, c.x, c.y, aiPlayer, winLen);
    const def = cellThreatScore(board, size, c.x, c.y, humanPlayer, winLen);
    const score = off + def * 1.1;
    if (score > bestScore) { bestScore = score; best = c; }
  }
  return best;
}

(function () {
  if (typeof document === 'undefined') return;
  const boardEl    = document.getElementById('gkBoard');
  const turnText   = document.getElementById('gkTurnText');
  const turnDot    = document.getElementById('gkTurnDot');
  const ratingEl   = document.getElementById('gkRating');
  const p1WinsEl   = document.getElementById('gkP1Wins');
  const p2WinsEl   = document.getElementById('gkP2Wins');
  const p1LabelEl  = document.getElementById('gkP1Label');
  const p2LabelEl  = document.getElementById('gkP2Label');
  const modeAiBtn  = document.getElementById('gkModeAiBtn');
  const mode2pBtn  = document.getElementById('gkMode2pBtn');
  if (!boardEl || !turnText) return;

  boardEl.style.gridTemplateColumns = 'repeat(' + GK_CONFIG.boardSize + ', 1fr)';
  boardEl.style.gridTemplateRows = 'repeat(' + GK_CONFIG.boardSize + ', 1fr)';

  let board = createEmptyBoard(GK_CONFIG.boardSize);
  let current = 1;
  let gameOver = false;
  let wins = { ai: { 1: 0, 2: 0 }, '2p': { 1: 0, 2: 0 } };
  let cellEls = [];
  let mode = 'ai'; // 'ai' | '2p'
  let aiTimerId = null;

  function names() { return { 1: gkPlayerName(mode, 1), 2: gkPlayerName(mode, 2) }; }

  function clearAiTimer() {
    if (aiTimerId) { clearTimeout(aiTimerId); aiTimerId = null; }
    boardEl.classList.remove('thinking');
  }

  function render() {
    boardEl.innerHTML = '';
    cellEls = [];
    for (let y = 0; y < GK_CONFIG.boardSize; y++) {
      const rowEls = [];
      for (let x = 0; x < GK_CONFIG.boardSize; x++) {
        const cell = document.createElement('div');
        cell.className = 'gk-cell';
        const stone = document.createElement('div');
        stone.className = 'gk-stone';
        cell.appendChild(stone);
        // 直接綁定該格自己的(x,y)，點擊時棋子就精確落在這一格，不做任何重力/位移計算
        cell.addEventListener('click', function () { onCellClick(x, y); });
        boardEl.appendChild(cell);
        rowEls.push({ cell: cell, stone: stone });
      }
      cellEls.push(rowEls);
    }
    syncBoardUI();
  }

  function syncBoardUI(winCells) {
    for (let y = 0; y < GK_CONFIG.boardSize; y++) {
      for (let x = 0; x < GK_CONFIG.boardSize; x++) {
        const v = board[y][x];
        const stone = cellEls[y][x].stone;
        stone.className = 'gk-stone' + (v ? ' ' + GK_CONFIG.playerClass[v] : '');
      }
    }
    if (winCells) {
      winCells.forEach(function ([x, y]) { cellEls[y][x].stone.classList.add('win'); });
    }
  }

  function updateTurnUI() {
    if (mode === 'ai' && current === 2) {
      turnText.textContent = ggomokuT('aiThinking');
    } else if (mode === 'ai' && current === 1) {
      // 「你」是代名詞，跟「{名字}的回合」這種通用模板套在一起會有文法問題
      // （英文變成"You's turn"、德文動詞變化錯誤），所以人類對電腦時單獨用一句
      // 專門翻好的完整句子，不透過 {name} 套版
      turnText.textContent = ggomokuT('turnOfYou');
    } else {
      turnText.textContent = ggomokuT('turnOf', { name: names()[current] });
    }
    turnDot.style.background = GK_CONFIG.playerColor[current];
  }

  function updateLabels() {
    // 同樣道理：「你」的勝場標籤不套 {name} 模板，改用整句翻譯避免代名詞文法問題
    p1LabelEl.textContent = mode === 'ai' ? ggomokuT('winsYouLabel') : ggomokuT('winsLabel', { name: names()[1] });
    p2LabelEl.textContent = ggomokuT('winsLabel', { name: names()[2] });
    p1WinsEl.textContent = String(wins[mode][1]);
    p2WinsEl.textContent = String(wins[mode][2]);
  }

  function finishMove(x, y) {
    const winCells = checkWin(board, x, y, current, GK_CONFIG.boardSize, GK_CONFIG.winLength);
    if (winCells) {
      gameOver = true;
      clearAiTimer();
      wins[mode][current]++;
      updateLabels();
      ratingEl.textContent = ggomokuT('winMessage', { name: names()[current] });
      syncBoardUI(winCells);
      window._gkLastResult = ggomokuT('shareWinResult', { name: names()[current] });
      return true;
    }
    if (isBoardFull(board)) {
      gameOver = true;
      clearAiTimer();
      ratingEl.textContent = ggomokuT('drawMessage');
      window._gkLastResult = ggomokuT('shareDrawResult');
      return true;
    }
    return false;
  }

  function onCellClick(x, y) {
    if (gameOver) return; // 7-3 防錯：遊戲已結束
    if (mode === 'ai' && current === 2) return; // 7-3 防錯：電腦思考中禁止玩家插手
    if (board[y][x] !== 0) return; // 7-3 防錯：這格已經有棋子，不能重複下
    board[y][x] = current;
    syncBoardUI();
    if (finishMove(x, y)) return;
    current = current === 1 ? 2 : 1;
    updateTurnUI();
    if (mode === 'ai' && current === 2) scheduleAiMove();
  }

  function scheduleAiMove() {
    boardEl.classList.add('thinking');
    const delay = GK_CONFIG.aiThinkMsMin + Math.random() * (GK_CONFIG.aiThinkMsMax - GK_CONFIG.aiThinkMsMin);
    aiTimerId = setTimeout(function () {
      aiTimerId = null;
      boardEl.classList.remove('thinking');
      if (gameOver) return;
      const move = pickAiMove(board, GK_CONFIG.boardSize, 2, 1, GK_CONFIG.winLength);
      board[move.y][move.x] = 2;
      syncBoardUI();
      if (finishMove(move.x, move.y)) return;
      current = 1;
      updateTurnUI();
    }, delay);
  }

  function restartInternal() {
    clearAiTimer();
    board = createEmptyBoard(GK_CONFIG.boardSize);
    current = 1;
    gameOver = false;
    ratingEl.textContent = '';
    updateLabels();
    render();
    updateTurnUI();
  }

  function setModeInternal(m) {
    if (mode === m) return;
    mode = m;
    modeAiBtn.classList.toggle('active', m === 'ai');
    mode2pBtn.classList.toggle('active', m === '2p');
    restartInternal();
  }

  window.gkRestart = restartInternal;
  window.gkSetMode = setModeInternal;
  restartInternal();

  // 7-4 資源清理：離開頁面前清掉電腦「思考中」的計時器
  window.addEventListener('beforeunload', clearAiTimer);
})();

function gkShareResult() {
  const text = (typeof window !== 'undefined' && window._gkLastResult)
    ? ggomokuT('shareWithResult', { r: window._gkLastResult })
    : ggomokuT('shareNoResult');
  if (typeof navigator !== 'undefined' && navigator.share) {
    navigator.share({ title: document.title, text: text, url: location.href }).catch(function () {});
  } else {
    if (!navigator.clipboard || !navigator.clipboard.writeText) return; // 7-3 防錯：無剪貼簿API時安全退出
    navigator.clipboard.writeText(text + ' ' + location.href);
    const b = event.target;
    const old = b.textContent;
    b.textContent = ggomokuT('copied');
    setTimeout(function () { b.textContent = old; }, GK_CONFIG.copyRevertMs);
  }
}
if (typeof document !== 'undefined') {
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.addEventListener('click', function () { this.parentElement.classList.toggle('open'); });
  });
}
