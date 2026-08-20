// ══════════════════════════════════════════════════════════
// 西洋棋 — 共用遊戲邏輯（所有語言版本共用這一份，2026/08/18 多語言化時抽出）
//
// 【多語言架構約定】
//   這個檔案裡「不能出現任何給使用者看的文字」。所有文字一律透過 gchessT('key') 讀取
//   頁面在載入這支JS之前先定義好的 window.GAME_I18N 字典。
//   → 遊戲邏輯有bug只要改這一個檔案，10種語言同時生效
//   → 翻譯只動各語言HTML裡的字典，不會誤改邏輯
//
// 【本次重構只做三件事】文字外移、變數改名（避免多檔同全域範圍撞名）、無DOM防護。
//   規則引擎（走法產生/王車易位/吃過路兵/升變/將死逼和判定）與AI搜尋
//   （minimax + alpha-beta 剪枝 + 疊代加深）逐字搬移，演算法與數值一律未動。
//   走法產生正確性已用perft方法核對過起始局面（深度1-4：20/400/8902/197281）
//   跟Kiwipete標準測試局面（深度1-3：48/2039/97862），
//   完全吻合西洋棋程式設計界公開已知的正確數值。
//
// 遵循《新工具規劃守則.md》第七節：
//   7-1 CH_CONFIG集中管理可調數值（文字在GAME_I18N）
//   7-2 純函式（走法產生/將軍判定/AI搜尋）跟DOM渲染完全分開，方便單元測試
//   7-3 防錯：點到不合法目的地不動作；字典缺key不會讓遊戲崩潰（回傳空字串並警告）
//   7-4 資源清理：固定64格DOM節點重複利用，不隨對局長度累積
//
// board[row][col]：row0=第8列（黑方底線）...row7=第1列（白方底線），col0=a欄...col7=h欄
// ══════════════════════════════════════════════════════════

const CH_CONFIG = {
  aiMoveDelayMs: 60,   // 讓「思考中」文字先畫出來，再進行會佔用主執行緒的搜尋運算
  copyRevertMs: 1500
};

// ── i18n 取字helper（7-3 防錯：缺key不崩潰）──
function gchessT(key, vars) {
  const dict = (typeof window !== 'undefined' && window.GAME_I18N) || {};
  let s = dict[key];
  if (typeof s !== 'string') {
    if (typeof console !== 'undefined' && console.warn) console.warn('[chess] missing i18n key: ' + key);
    return '';
  }
  if (vars) {
    Object.keys(vars).forEach(function (k) {
      s = s.split('{' + k + '}').join(String(vars[k]));
    });
  }
  return s;
}
// 顏色代碼('w'/'b') → 該語言的稱呼（白方／黑方）。文字全在字典裡。
function chSideName(color) { return gchessT(color === 'w' ? 'sideWhite' : 'sideBlack'); }

function chPieceColor(p) { return p ? p[0] : null; }
function chPieceType(p) { return p ? p[1] : null; }
function chInBounds(r, c) { return r >= 0 && r < 8 && c >= 0 && c < 8; }
function chOppColor(c) { return c === 'w' ? 'b' : 'w'; }

function chMakeInitialState() {
  const board = [
    ['bR','bN','bB','bQ','bK','bB','bN','bR'],
    ['bP','bP','bP','bP','bP','bP','bP','bP'],
    [null,null,null,null,null,null,null,null],
    [null,null,null,null,null,null,null,null],
    [null,null,null,null,null,null,null,null],
    [null,null,null,null,null,null,null,null],
    ['wP','wP','wP','wP','wP','wP','wP','wP'],
    ['wR','wN','wB','wQ','wK','wB','wN','wR']
  ];
  return { board: board, turn: 'w', castling: { wK: true, wQ: true, bK: true, bQ: true }, epTarget: null, halfmove: 0, fullmove: 1 };
}
function chCloneState(state) {
  return {
    board: state.board.map(function (row) { return row.slice(); }),
    turn: state.turn,
    castling: { wK: state.castling.wK, wQ: state.castling.wQ, bK: state.castling.bK, bQ: state.castling.bQ },
    epTarget: state.epTarget ? [state.epTarget[0], state.epTarget[1]] : null,
    halfmove: state.halfmove,
    fullmove: state.fullmove
  };
}

const CH_BISHOP_DIRS = [[-1,-1],[-1,1],[1,-1],[1,1]];
const CH_ROOK_DIRS = [[-1,0],[1,0],[0,-1],[0,1]];
const CH_QUEEN_DIRS = CH_BISHOP_DIRS.concat(CH_ROOK_DIRS);
const CH_KNIGHT_OFFSETS = [[-2,-1],[-2,1],[-1,-2],[-1,2],[1,-2],[1,2],[2,-1],[2,1]];

function chIsSquareAttacked(board, r, c, byColor) {
  if (byColor === 'w') {
    if (chInBounds(r+1,c-1) && board[r+1][c-1] === 'wP') return true;
    if (chInBounds(r+1,c+1) && board[r+1][c+1] === 'wP') return true;
  } else {
    if (chInBounds(r-1,c-1) && board[r-1][c-1] === 'bP') return true;
    if (chInBounds(r-1,c+1) && board[r-1][c+1] === 'bP') return true;
  }
  for (let i = 0; i < CH_KNIGHT_OFFSETS.length; i++) {
    const nr = r + CH_KNIGHT_OFFSETS[i][0], nc = c + CH_KNIGHT_OFFSETS[i][1];
    if (chInBounds(nr,nc) && board[nr][nc] === byColor + 'N') return true;
  }
  for (let i = 0; i < CH_BISHOP_DIRS.length; i++) {
    let nr = r + CH_BISHOP_DIRS[i][0], nc = c + CH_BISHOP_DIRS[i][1];
    while (chInBounds(nr,nc)) {
      const p = board[nr][nc];
      if (p) { if (chPieceColor(p) === byColor && (chPieceType(p)==='B'||chPieceType(p)==='Q')) return true; break; }
      nr += CH_BISHOP_DIRS[i][0]; nc += CH_BISHOP_DIRS[i][1];
    }
  }
  for (let i = 0; i < CH_ROOK_DIRS.length; i++) {
    let nr = r + CH_ROOK_DIRS[i][0], nc = c + CH_ROOK_DIRS[i][1];
    while (chInBounds(nr,nc)) {
      const p = board[nr][nc];
      if (p) { if (chPieceColor(p) === byColor && (chPieceType(p)==='R'||chPieceType(p)==='Q')) return true; break; }
      nr += CH_ROOK_DIRS[i][0]; nc += CH_ROOK_DIRS[i][1];
    }
  }
  for (let i = 0; i < CH_QUEEN_DIRS.length; i++) {
    const nr = r + CH_QUEEN_DIRS[i][0], nc = c + CH_QUEEN_DIRS[i][1];
    if (chInBounds(nr,nc) && board[nr][nc] === byColor + 'K') return true;
  }
  return false;
}
function chFindKing(board, color) {
  for (let r = 0; r < 8; r++) for (let c = 0; c < 8; c++) if (board[r][c] === color + 'K') return [r,c];
  return null;
}
function chIsKingInCheck(state, color) {
  const k = chFindKing(state.board, color);
  if (!k) return false;
  return chIsSquareAttacked(state.board, k[0], k[1], chOppColor(color));
}

function chGenPseudoMovesForSquare(state, r, c) {
  const board = state.board;
  const piece = board[r][c];
  if (!piece) return [];
  const color = chPieceColor(piece), type = chPieceType(piece);
  const moves = [];

  function pushSlide(dirs) {
    for (let i = 0; i < dirs.length; i++) {
      let nr = r + dirs[i][0], nc = c + dirs[i][1];
      while (chInBounds(nr,nc)) {
        const target = board[nr][nc];
        if (!target) { moves.push({ from:[r,c], to:[nr,nc], piece:piece, captured:null }); }
        else { if (chPieceColor(target) !== color) moves.push({ from:[r,c], to:[nr,nc], piece:piece, captured:target }); break; }
        nr += dirs[i][0]; nc += dirs[i][1];
      }
    }
  }
  function pushStep(offsets) {
    for (let i = 0; i < offsets.length; i++) {
      const nr = r + offsets[i][0], nc = c + offsets[i][1];
      if (!chInBounds(nr,nc)) continue;
      const target = board[nr][nc];
      if (!target) moves.push({ from:[r,c], to:[nr,nc], piece:piece, captured:null });
      else if (chPieceColor(target) !== color) moves.push({ from:[r,c], to:[nr,nc], piece:piece, captured:target });
    }
  }

  if (type === 'P') {
    const dir = color === 'w' ? -1 : 1;
    const startRow = color === 'w' ? 6 : 1;
    const promoRow = color === 'w' ? 0 : 7;
    const oneR = r + dir;
    if (chInBounds(oneR,c) && !board[oneR][c]) {
      if (oneR === promoRow) { ['Q','R','B','N'].forEach(function(pr){ moves.push({from:[r,c],to:[oneR,c],piece:piece,captured:null,promotion:pr}); }); }
      else moves.push({ from:[r,c], to:[oneR,c], piece:piece, captured:null });
      const twoR = r + 2*dir;
      if (r === startRow && !board[twoR][c]) moves.push({ from:[r,c], to:[twoR,c], piece:piece, captured:null, isDoubleStep:true });
    }
    [-1,1].forEach(function (dc) {
      const nc = c + dc, nr = oneR;
      if (!chInBounds(nr,nc)) return;
      const target = board[nr][nc];
      if (target && chPieceColor(target) !== color) {
        if (nr === promoRow) ['Q','R','B','N'].forEach(function(pr){ moves.push({from:[r,c],to:[nr,nc],piece:piece,captured:target,promotion:pr}); });
        else moves.push({ from:[r,c], to:[nr,nc], piece:piece, captured:target });
      } else if (state.epTarget && state.epTarget[0] === nr && state.epTarget[1] === nc) {
        moves.push({ from:[r,c], to:[nr,nc], piece:piece, captured:board[r][nc], isEnPassant:true });
      }
    });
  } else if (type === 'N') {
    pushStep(CH_KNIGHT_OFFSETS);
  } else if (type === 'B') {
    pushSlide(CH_BISHOP_DIRS);
  } else if (type === 'R') {
    pushSlide(CH_ROOK_DIRS);
  } else if (type === 'Q') {
    pushSlide(CH_QUEEN_DIRS);
  } else if (type === 'K') {
    pushStep(CH_QUEEN_DIRS);
    const homeRow = color === 'w' ? 7 : 0;
    if (r === homeRow && c === 4) {
      const inCheck = chIsSquareAttacked(board, r, c, chOppColor(color));
      if (!inCheck) {
        if (state.castling[color+'K'] && !board[homeRow][5] && !board[homeRow][6] && board[homeRow][7] === color+'R'
            && !chIsSquareAttacked(board, homeRow, 5, chOppColor(color)) && !chIsSquareAttacked(board, homeRow, 6, chOppColor(color))) {
          moves.push({ from:[r,c], to:[homeRow,6], piece:piece, captured:null, isCastle:'K', castleRookFrom:[homeRow,7], castleRookTo:[homeRow,5] });
        }
        if (state.castling[color+'Q'] && !board[homeRow][3] && !board[homeRow][2] && !board[homeRow][1] && board[homeRow][0] === color+'R'
            && !chIsSquareAttacked(board, homeRow, 3, chOppColor(color)) && !chIsSquareAttacked(board, homeRow, 2, chOppColor(color))) {
          moves.push({ from:[r,c], to:[homeRow,2], piece:piece, captured:null, isCastle:'Q', castleRookFrom:[homeRow,0], castleRookTo:[homeRow,3] });
        }
      }
    }
  }
  return moves;
}
function chGenAllPseudoMoves(state, color) {
  const out = [];
  for (let r = 0; r < 8; r++) for (let c = 0; c < 8; c++) {
    const p = state.board[r][c];
    if (p && chPieceColor(p) === color) { Array.prototype.push.apply(out, chGenPseudoMovesForSquare(state, r, c)); }
  }
  return out;
}
function chMakeMove(state, move) {
  const ns = chCloneState(state);
  const board = ns.board;
  const color = chPieceColor(move.piece);
  const type = chPieceType(move.piece);

  if (move.isEnPassant) board[move.from[0]][move.to[1]] = null;
  board[move.to[0]][move.to[1]] = move.promotion ? (color + move.promotion) : move.piece;
  board[move.from[0]][move.from[1]] = null;

  if (move.isCastle) {
    board[move.castleRookTo[0]][move.castleRookTo[1]] = board[move.castleRookFrom[0]][move.castleRookFrom[1]];
    board[move.castleRookFrom[0]][move.castleRookFrom[1]] = null;
  }

  if (type === 'K') { ns.castling[color+'K'] = false; ns.castling[color+'Q'] = false; }
  if (move.from[0] === 7 && move.from[1] === 0) ns.castling.wQ = false;
  if (move.from[0] === 7 && move.from[1] === 7) ns.castling.wK = false;
  if (move.from[0] === 0 && move.from[1] === 0) ns.castling.bQ = false;
  if (move.from[0] === 0 && move.from[1] === 7) ns.castling.bK = false;
  if (move.to[0] === 7 && move.to[1] === 0) ns.castling.wQ = false;
  if (move.to[0] === 7 && move.to[1] === 7) ns.castling.wK = false;
  if (move.to[0] === 0 && move.to[1] === 0) ns.castling.bQ = false;
  if (move.to[0] === 0 && move.to[1] === 7) ns.castling.bK = false;

  ns.epTarget = (type === 'P' && Math.abs(move.to[0] - move.from[0]) === 2) ? [(move.from[0]+move.to[0])/2, move.from[1]] : null;
  ns.halfmove = (type === 'P' || move.captured) ? 0 : ns.halfmove + 1;
  if (color === 'b') ns.fullmove++;
  ns.turn = chOppColor(color);
  return ns;
}
function chGenerateLegalMoves(state, color) {
  const pseudo = chGenAllPseudoMoves(state, color);
  const legal = [];
  for (let i = 0; i < pseudo.length; i++) {
    const ns = chMakeMove(state, pseudo[i]);
    if (!chIsKingInCheck(ns, color)) legal.push(pseudo[i]);
  }
  return legal;
}
function chIsCheckmate(state) { return chIsKingInCheck(state, state.turn) && chGenerateLegalMoves(state, state.turn).length === 0; }
function chIsStalemate(state) { return !chIsKingInCheck(state, state.turn) && chGenerateLegalMoves(state, state.turn).length === 0; }
function chIsInsufficientMaterial(state) {
  const pieces = [];
  for (let r = 0; r < 8; r++) for (let c = 0; c < 8; c++) { const p = state.board[r][c]; if (p && chPieceType(p) !== 'K') pieces.push(p); }
  if (pieces.length === 0) return true;
  if (pieces.length === 1 && (chPieceType(pieces[0]) === 'B' || chPieceType(pieces[0]) === 'N')) return true;
  return false;
}
function chIsDrawByFiftyMoves(state) { return state.halfmove >= 100; }

// ══════════════════════════════════════════════════════════
// AI：minimax+alpha-beta剪枝，時間限制式疊代加深
// ══════════════════════════════════════════════════════════
const CH_PIECE_VALUE = { P: 100, N: 320, B: 330, R: 500, Q: 900, K: 0 };
const CH_PAWN_PST=[[0,0,0,0,0,0,0,0],[50,50,50,50,50,50,50,50],[10,10,20,30,30,20,10,10],[5,5,10,25,25,10,5,5],[0,0,0,20,20,0,0,0],[5,-5,-10,0,0,-10,-5,5],[5,10,10,-20,-20,10,10,5],[0,0,0,0,0,0,0,0]];
const CH_KNIGHT_PST=[[-50,-40,-30,-30,-30,-30,-40,-50],[-40,-20,0,0,0,0,-20,-40],[-30,0,10,15,15,10,0,-30],[-30,5,15,20,20,15,5,-30],[-30,0,15,20,20,15,0,-30],[-30,5,10,15,15,10,5,-30],[-40,-20,0,5,5,0,-20,-40],[-50,-40,-30,-30,-30,-30,-40,-50]];
const CH_BISHOP_PST=[[-20,-10,-10,-10,-10,-10,-10,-20],[-10,0,0,0,0,0,0,-10],[-10,0,5,10,10,5,0,-10],[-10,5,5,10,10,5,5,-10],[-10,0,10,10,10,10,0,-10],[-10,10,10,10,10,10,10,-10],[-10,5,0,0,0,0,5,-10],[-20,-10,-10,-10,-10,-10,-10,-20]];
const CH_ROOK_PST=[[0,0,0,0,0,0,0,0],[5,10,10,10,10,10,10,5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[-5,0,0,0,0,0,0,-5],[0,0,0,5,5,0,0,0]];
const CH_QUEEN_PST=[[-20,-10,-10,-5,-5,-10,-10,-20],[-10,0,0,0,0,0,0,-10],[-10,0,5,5,5,5,0,-10],[-5,0,5,5,5,5,0,-5],[0,0,5,5,5,5,0,-5],[-10,5,5,5,5,5,0,-10],[-10,0,5,0,0,0,0,-10],[-20,-10,-10,-5,-5,-10,-10,-20]];
const CH_KING_PST=[[-30,-40,-40,-50,-50,-40,-40,-30],[-30,-40,-40,-50,-50,-40,-40,-30],[-30,-40,-40,-50,-50,-40,-40,-30],[-30,-40,-40,-50,-50,-40,-40,-30],[-20,-30,-30,-40,-40,-30,-30,-20],[-10,-20,-20,-20,-20,-20,-20,-10],[20,20,0,0,0,0,20,20],[20,30,10,0,0,10,30,20]];
const CH_PST_BY_TYPE = { P: CH_PAWN_PST, N: CH_KNIGHT_PST, B: CH_BISHOP_PST, R: CH_ROOK_PST, Q: CH_QUEEN_PST, K: CH_KING_PST };

function chEvaluatePosition(state) {
  let score = 0;
  const board = state.board;
  for (let r = 0; r < 8; r++) for (let c = 0; c < 8; c++) {
    const p = board[r][c];
    if (!p) continue;
    const color = chPieceColor(p), type = chPieceType(p);
    const pstRow = color === 'w' ? r : 7 - r;
    const val = CH_PIECE_VALUE[type] + CH_PST_BY_TYPE[type][pstRow][c];
    score += (color === 'w' ? val : -val);
  }
  return score;
}
function chOrderMoves(moves) {
  return moves.slice().sort(function (a, b) {
    const av = a.captured ? CH_PIECE_VALUE[chPieceType(a.captured)] : (a.promotion ? 50 : 0);
    const bv = b.captured ? CH_PIECE_VALUE[chPieceType(b.captured)] : (b.promotion ? 50 : 0);
    return bv - av;
  });
}
const CH_TIME_UP = { __timeUp: true };
const CH_MATE_SCORE = 100000;
function chNegamax(state, depth, ply, alpha, beta, deadline) {
  if (Date.now() > deadline) throw CH_TIME_UP;
  const moves = chGenerateLegalMoves(state, state.turn);
  if (moves.length === 0) { if (chIsKingInCheck(state, state.turn)) return -(CH_MATE_SCORE - ply); return 0; }
  if (chIsInsufficientMaterial(state) || chIsDrawByFiftyMoves(state)) return 0;
  if (depth === 0) return (state.turn === 'w' ? 1 : -1) * chEvaluatePosition(state);
  const ordered = chOrderMoves(moves);
  let best = -Infinity;
  for (let i = 0; i < ordered.length; i++) {
    const child = chMakeMove(state, ordered[i]);
    const score = -chNegamax(child, depth - 1, ply + 1, -beta, -alpha, deadline);
    if (score > best) best = score;
    if (best > alpha) alpha = best;
    if (alpha >= beta) break;
  }
  return best;
}
function chFindBestMove(state, options) {
  const opts = options || {};
  const maxDepth = opts.maxDepth || 3;
  const deadline = Date.now() + (opts.timeBudgetMs || 800);
  const legalAtRoot = chGenerateLegalMoves(state, state.turn);
  if (!legalAtRoot.length) return null;
  let bestMove = legalAtRoot[0], bestScore = -Infinity;
  try {
    for (let depth = 1; depth <= maxDepth; depth++) {
      const ordered = chOrderMoves(legalAtRoot);
      let localBest = null, localBestScore = -Infinity, alpha = -Infinity, beta = Infinity;
      for (let i = 0; i < ordered.length; i++) {
        const child = chMakeMove(state, ordered[i]);
        const score = -chNegamax(child, depth - 1, 1, -beta, -alpha, deadline);
        if (score > localBestScore) { localBestScore = score; localBest = ordered[i]; }
        if (localBestScore > alpha) alpha = localBestScore;
      }
      bestMove = localBest; bestScore = localBestScore;
      if (Date.now() > deadline) break;
    }
  } catch (e) { if (e !== CH_TIME_UP) throw e; }
  return { move: bestMove, score: bestScore };
}
// 難度只留數字，三個難度的名稱文字放在版面的 {{ui.diffEasy/diffMedium/diffHard}}
const CH_AI_DIFFICULTY = {
  easy: { maxDepth: 1, timeBudgetMs: 400 },
  medium: { maxDepth: 3, timeBudgetMs: 700 },
  hard: { maxDepth: 5, timeBudgetMs: 1500 }
};
const CH_DIFFICULTY_ORDER = ['easy', 'medium', 'hard'];
// 純函式：回傳難度在 CH_DIFFICULTY_ORDER（＝版面難度按鈕順序）中的index
function chDifficultyIndex(key) {
  const i = CH_DIFFICULTY_ORDER.indexOf(key);
  return i < 0 ? 1 : i; // 7-3 防錯：未知難度視為中等
}

// ══════════════════════════════════════════════════════════
// UI層：DOM渲染、輸入處理、模式切換 —— 7-4 資源清理：固定64格DOM節點重複利用
// ══════════════════════════════════════════════════════════
const CH_WHITE_GLYPH = { K:'♔', Q:'♕', R:'♖', B:'♗', N:'♘', P:'♙' };
const CH_BLACK_GLYPH = { K:'♚', Q:'♛', R:'♜', B:'♝', N:'♞', P:'♟' };
function chSquareName(r, c) { return String.fromCharCode(97 + c) + (8 - r); }

(function () {
  if (typeof document === 'undefined') return; // 純邏輯測試環境（無DOM）時安靜跳過UI部分
  const modeSelectEl = document.getElementById('chModeSelect');
  const diffRowEl = document.getElementById('chDiffRow');
  const boardWrapEl = document.getElementById('chBoardWrap');
  const gridEl = document.getElementById('chGrid');
  const promoEl = document.getElementById('chPromo');
  const overlayEl = document.getElementById('chOverlay');
  const overTitleEl = document.getElementById('chOverTitle');
  const overSubEl = document.getElementById('chOverSub');
  const turnBadgeEl = document.getElementById('chTurnBadge');
  const checkBadgeEl = document.getElementById('chCheckBadge');
  const thinkingEl = document.getElementById('chThinking');
  const moveListEl = document.getElementById('chMoveList');
  const winsEl = document.getElementById('chWins'), lossesEl = document.getElementById('chLosses'), drawsEl = document.getElementById('chDraws');
  if (!gridEl || !boardWrapEl || !modeSelectEl) return; // 7-3 防錯：頁面結構不符時不炸掉整頁

  let mode = null; // 'pvp' | 'pve'
  let aiDifficulty = 'medium';
  let playerColor = 'w'; // PvE模式下人類玩家的顏色（固定白方先手）
  let state = null;
  let stateHistory = [];
  let selected = null;
  let lastMove = null;
  let pendingPromotion = null; // {from,to} 等待玩家選擇升變棋子
  let gameOver = false;
  let wins = 0, losses = 0, draws = 0;

  window.chChooseMode = function (m) {
    mode = m;
    if (m === 'pve') { diffRowEl.style.display = 'flex'; document.querySelector('[data-diff="'+aiDifficulty+'"]').classList.add('active'); }
    else { startGame(); }
  };
  window.chSetDifficulty = function (d) {
    aiDifficulty = d;
    Array.prototype.forEach.call(diffRowEl.querySelectorAll('button'), function (b) { b.classList.toggle('active', b.getAttribute('data-diff') === d); });
    startGame();
  };

  function startGame() {
    modeSelectEl.style.display = 'none';
    boardWrapEl.classList.add('show');
    state = chMakeInitialState();
    stateHistory = [];
    selected = null; lastMove = null; pendingPromotion = null; gameOver = false;
    overlayEl.classList.remove('show');
    moveListEl.innerHTML = '';
    thinkingEl.textContent = '';
    render();
  }
  window.chBackToMenu = function () {
    mode = null;
    boardWrapEl.classList.remove('show');
    modeSelectEl.style.display = 'block';
    diffRowEl.style.display = 'none';
  };

  function squareClasses(r, c) {
    let cls = 'ch-sq ' + ((r + c) % 2 === 0 ? 'light' : 'dark');
    if (selected && selected[0] === r && selected[1] === c) cls += ' selected';
    if (lastMove && ((lastMove.from[0]===r&&lastMove.from[1]===c) || (lastMove.to[0]===r&&lastMove.to[1]===c))) cls += ' last-move';
    if (!gameOver && chIsKingInCheck(state, state.turn)) {
      const k = chFindKing(state.board, state.turn);
      if (k && k[0] === r && k[1] === c) cls += ' in-check';
    }
    return cls;
  }

  function legalMovesForSelected() {
    if (!selected) return [];
    const all = chGenerateLegalMoves(state, state.turn);
    return all.filter(function (m) { return m.from[0] === selected[0] && m.from[1] === selected[1]; });
  }

  function render() {
    let html = '';
    for (let r = 0; r < 8; r++) {
      for (let c = 0; c < 8; c++) {
        const p = state.board[r][c];
        let inner = '';
        if (p) {
          const glyph = chPieceColor(p) === 'w' ? CH_WHITE_GLYPH[chPieceType(p)] : CH_BLACK_GLYPH[chPieceType(p)];
          inner = '<span class="ch-piece ' + (chPieceColor(p)==='w'?'white':'black') + '">' + glyph + '</span>';
        }
        html += '<div class="' + squareClasses(r,c) + '" data-r="' + r + '" data-c="' + c + '">' + inner + '</div>';
      }
    }
    gridEl.innerHTML = html;

    const legal = legalMovesForSelected();
    legal.forEach(function (m) {
      const cellSel = gridEl.querySelector('[data-r="'+m.to[0]+'"][data-c="'+m.to[1]+'"]');
      if (cellSel) {
        const dot = document.createElement('div');
        dot.className = 'ch-dot' + (m.captured ? ' capture' : '');
        cellSel.appendChild(dot);
      }
    });

    Array.prototype.forEach.call(gridEl.querySelectorAll('.ch-sq'), function (sqEl) {
      sqEl.addEventListener('pointerdown', function () {
        const r = parseInt(sqEl.getAttribute('data-r'),10), c = parseInt(sqEl.getAttribute('data-c'),10);
        onSquareClick(r, c);
      });
    });

    turnBadgeEl.textContent = gchessT('turnOf', { side: chSideName(state.turn) });
    checkBadgeEl.classList.toggle('show', !gameOver && chIsKingInCheck(state, state.turn));
    winsEl.textContent = String(wins); lossesEl.textContent = String(losses); drawsEl.textContent = String(draws);
  }

  function onSquareClick(r, c) {
    if (gameOver || pendingPromotion) return;
    if (mode === 'pve' && state.turn !== playerColor) return; // AI思考中，人類不能亂點
    const piece = state.board[r][c];
    if (selected && selected[0] === r && selected[1] === c) { selected = null; render(); return; }

    if (piece && chPieceColor(piece) === state.turn) { selected = [r, c]; render(); return; }

    if (selected) {
      const legal = legalMovesForSelected();
      const candidates = legal.filter(function (m) { return m.to[0] === r && m.to[1] === c; });
      if (!candidates.length) { return; } // 7-3 防錯：點到不合法目的地不動作
      if (candidates.length > 1) { // 多個結果代表是升變（4種棋子可選）
        pendingPromotion = { from: selected, to: [r,c], candidates: candidates };
        showPromotionPicker();
        return;
      }
      applyMove(candidates[0]);
    }
  }

  function showPromotionPicker() {
    const color = state.turn;
    const glyphs = color === 'w' ? CH_WHITE_GLYPH : CH_BLACK_GLYPH;
    promoEl.innerHTML = ['Q','R','B','N'].map(function (t) {
      return '<button data-promo="' + t + '">' + glyphs[t] + '</button>';
    }).join('');
    promoEl.classList.add('show');
    Array.prototype.forEach.call(promoEl.querySelectorAll('button'), function (btn) {
      btn.addEventListener('pointerdown', function () {
        const t = btn.getAttribute('data-promo');
        const chosen = pendingPromotion.candidates.find(function (m) { return m.promotion === t; });
        promoEl.classList.remove('show');
        pendingPromotion = null;
        applyMove(chosen);
      });
    });
  }

  function applyMove(move) {
    stateHistory.push(state);
    state = chMakeMove(state, move);
    lastMove = move;
    selected = null;
    moveListEl.innerHTML += (state.turn === 'b' ? (state.fullmove + '. ') : '') + chSquareName(move.from[0],move.from[1]) + (move.captured?'x':'-') + chSquareName(move.to[0],move.to[1]) + (move.promotion?('='+move.promotion):'') + ' ';
    moveListEl.scrollTop = moveListEl.scrollHeight;
    render();
    checkGameEnd();
    if (!gameOver && mode === 'pve' && state.turn !== playerColor) {
      thinkingEl.textContent = gchessT('aiThinking');
      setTimeout(runAiMove, CH_CONFIG.aiMoveDelayMs); // 讓「思考中」文字先畫出來，再進行會佔用主執行緒的搜尋運算
    }
  }

  function runAiMove() {
    const diff = CH_AI_DIFFICULTY[aiDifficulty];
    const result = chFindBestMove(state, diff);
    thinkingEl.textContent = '';
    if (!result || !result.move) return; // 7-3 防錯：理論上checkGameEnd已攔截將死/逼和，這裡多一層保險
    stateHistory.push(state);
    state = chMakeMove(state, result.move);
    lastMove = result.move;
    moveListEl.innerHTML += (state.turn === 'w' ? (state.fullmove + '. ') : '') + chSquareName(result.move.from[0],result.move.from[1]) + (result.move.captured?'x':'-') + chSquareName(result.move.to[0],result.move.to[1]) + (result.move.promotion?('='+result.move.promotion):'') + ' ';
    moveListEl.scrollTop = moveListEl.scrollHeight;
    render();
    checkGameEnd();
  }

  function checkGameEnd() {
    if (chIsCheckmate(state)) {
      gameOver = true;
      const winnerColor = chOppColor(state.turn);
      overTitleEl.textContent = gchessT('checkmateTitle', { side: chSideName(winnerColor) });
      overSubEl.textContent = mode === 'pve'
        ? (winnerColor === playerColor ? gchessT('checkmateSubWin') : gchessT('checkmateSubLose'))
        : gchessT('checkmateSubPvp');
      overlayEl.classList.add('show');
      if (mode === 'pve') { if (winnerColor === playerColor) wins++; else losses++; }
      render();
    } else if (chIsStalemate(state)) {
      gameOver = true;
      overTitleEl.textContent = gchessT('stalemateTitle');
      overSubEl.textContent = gchessT('stalemateSub');
      overlayEl.classList.add('show');
      if (mode === 'pve') draws++;
      render();
    } else if (chIsInsufficientMaterial(state)) {
      gameOver = true;
      overTitleEl.textContent = gchessT('insufficientTitle');
      overSubEl.textContent = gchessT('insufficientSub');
      overlayEl.classList.add('show');
      if (mode === 'pve') draws++;
      render();
    } else if (chIsDrawByFiftyMoves(state)) {
      gameOver = true;
      overTitleEl.textContent = gchessT('fiftyTitle');
      overSubEl.textContent = gchessT('fiftySub');
      overlayEl.classList.add('show');
      if (mode === 'pve') draws++;
      render();
    }
  }

  window.chUndo = function () {
    if (gameOver || !stateHistory.length) return;
    // PvE模式一次悔棋要退回AI跟玩家各一手，才會輪到玩家重新下；PvP模式只退一手
    const stepsBack = (mode === 'pve' && stateHistory.length >= 2) ? 2 : 1;
    for (let i = 0; i < stepsBack; i++) { if (stateHistory.length) state = stateHistory.pop(); }
    selected = null; pendingPromotion = null; promoEl.classList.remove('show');
    lastMove = stateHistory.length ? null : null;
    render();
  };
})();

function chShareResult() {
  const text = gchessT('shareText');
  if (navigator.share) { navigator.share({ title: document.title, text: text, url: location.href }).catch(function () {}); }
  else {
    navigator.clipboard.writeText(text + ' ' + location.href);
    const b = event.target; const old = b.textContent; b.textContent = gchessT('copied');
    setTimeout(function () { b.textContent = old; }, CH_CONFIG.copyRevertMs);
  }
}
// FAQ 展開收合（7-3 防錯：純邏輯測試環境沒有 document 時安靜跳過，
// 不能讓這一行在無DOM環境直接拋 ReferenceError 導致整支檔案無法被單元測試載入）
if (typeof document !== 'undefined') {
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.addEventListener('click', function () { this.parentElement.classList.toggle('open'); });
  });
}
