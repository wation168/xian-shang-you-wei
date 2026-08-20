// ══════════════════════════════════════════════════════════
// 記憶翻牌 — 共用遊戲邏輯（所有語言版本共用這一份，多語言化時抽出）
//
// 【多語言架構約定】
//   這個檔案裡「不能出現任何給使用者看的文字」。所有文字一律透過 gmemorymatchT('key') 讀取
//   頁面在載入這支JS之前先定義好的 window.GAME_I18N 字典。
//
// 遵循《新工具規劃守則.md》第七節：
//   7-1 MM_CONFIG集中管理格數/圖案組/計時間隔等所有可調數值
//   7-2 純函式（mmShuffle/mmBuildDeck）跟 UI/計時器邏輯分開
//   7-3 防錯：翻牌動畫中或已配對的卡片點擊無效、避免同張卡連點兩次
//   7-4 資源清理：flip-back的setTimeout與計時interval統一在clearAll()處理
// ══════════════════════════════════════════════════════════
const MM_CONFIG = {
  pairCount: 8,
  symbols: ['🍎','🍌','🍇','🍒','🍉','🍓','🥝','🍑'],
  flipBackDelayMs: 800,
  historyLimit: 5,
  copyRevertMs: 1500,
  adLoadDelayMs: 2000
};

// ── i18n 取字helper（7-3 防錯：缺key不崩潰）──
function gmemorymatchT(key, vars) {
  const dict = (typeof window !== 'undefined' && window.GAME_I18N) || {};
  let s = dict[key];
  if (typeof s !== 'string') {
    if (typeof console !== 'undefined' && console.warn) console.warn('[memory-match] missing i18n key: ' + key);
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
function mmShuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
function mmBuildDeck() {
  const pairs = MM_CONFIG.symbols.slice(0, MM_CONFIG.pairCount);
  return mmShuffle(pairs.concat(pairs)).map(function (sym, i) {
    return { id: i, symbol: sym, flipped: false, matched: false };
  });
}

(function () {
  if (typeof document === 'undefined') return; // 純邏輯測試環境（無DOM）時安靜跳過UI部分

  const board    = document.getElementById('mmBoard');
  const movesEl  = document.getElementById('mmMoves');
  const timeEl   = document.getElementById('mmTime');
  const pairsEl  = document.getElementById('mmPairs');
  const ratingEl = document.getElementById('mmRating');
  const bestEl   = document.getElementById('mmBest');
  const historyEl= document.getElementById('mmHistory');
  if (!board || !movesEl) return; // 7-3 防錯：頁面結構不符時不炸掉整頁

  let deck = [];
  let cardEls = [];
  let openIds = [];
  let moves = 0;
  let matchedCount = 0;
  let elapsedSec = 0;
  let locked = false;
  let timers = { tickInterval: null, flipBackTimeout: null };
  let history = [];

  function clearAll() {
    if (timers.tickInterval) { clearInterval(timers.tickInterval); timers.tickInterval = null; }
    if (timers.flipBackTimeout) { clearTimeout(timers.flipBackTimeout); timers.flipBackTimeout = null; }
  }

  function render() {
    board.innerHTML = '';
    cardEls = deck.map(function (card) {
      const el = document.createElement('div');
      el.className = 'mm-card';
      el.innerHTML =
        '<div class="mm-card-inner">' +
          '<div class="mm-face mm-face-back">?</div>' +
          '<div class="mm-face mm-face-front">' + card.symbol + '</div>' +
        '</div>';
      el.addEventListener('click', function () { onCardClick(card.id); });
      board.appendChild(el);
      return el;
    });
  }

  function updateCardUI(id) {
    const card = deck[id];
    const el = cardEls[id];
    el.classList.toggle('flipped', card.flipped);
    el.classList.toggle('matched', card.matched);
  }

  function onCardClick(id) {
    if (locked) return;
    const card = deck[id];
    if (card.flipped || card.matched) return;
    if (openIds.length >= 2) return;

    card.flipped = true;
    updateCardUI(id);
    openIds.push(id);

    if (openIds.length === 2) {
      moves++;
      movesEl.textContent = String(moves);
      const [a, b] = openIds;
      if (deck[a].symbol === deck[b].symbol) {
        deck[a].matched = true;
        deck[b].matched = true;
        updateCardUI(a);
        updateCardUI(b);
        openIds = [];
        matchedCount++;
        pairsEl.textContent = String(matchedCount);
        if (matchedCount === MM_CONFIG.pairCount) endGame();
      } else {
        locked = true;
        timers.flipBackTimeout = setTimeout(function () {
          deck[a].flipped = false;
          deck[b].flipped = false;
          updateCardUI(a);
          updateCardUI(b);
          openIds = [];
          locked = false;
        }, MM_CONFIG.flipBackDelayMs);
      }
    }
  }

  function endGame() {
    clearAll();
    ratingEl.textContent = gmemorymatchT('doneMsg', { m: moves, t: elapsedSec });
    history.unshift(moves);
    history = history.slice(0, MM_CONFIG.historyLimit);
    const best = Math.min(...history);
    bestEl.textContent = gmemorymatchT('movesShort', { m: best });
    historyEl.innerHTML = history.map(function (v) { return '<span>' + gmemorymatchT('movesShort', { m: v }) + '</span>'; }).join('');
    window._mmLastMoves = moves;
    window._mmBestMoves = best;
    if (typeof gaSubmitScore === 'function') gaSubmitScore('memory-match', moves);
  }

  function mmStartInternal() {
    clearAll();
    deck = mmBuildDeck();
    openIds = [];
    moves = 0;
    matchedCount = 0;
    elapsedSec = 0;
    locked = false;
    movesEl.textContent = '0';
    timeEl.textContent = '0';
    pairsEl.textContent = '0';
    ratingEl.textContent = '';
    render();
    timers.tickInterval = setInterval(function () {
      elapsedSec++;
      timeEl.textContent = String(elapsedSec);
    }, 1000);
  }

  window.mmStart = mmStartInternal;
  mmStartInternal();

  // 7-4 資源清理：離開頁面前清掉所有計時器
  window.addEventListener('beforeunload', clearAll);
})();

function mmShareResult() {
  const moves = window._mmLastMoves;
  const text = (moves != null)
    ? gmemorymatchT('shareWithMoves', { m: moves })
    : gmemorymatchT('shareNoScore');
  if (navigator.share) {
    navigator.share({ title: document.title, text: text, url: location.href }).catch(function () {});
  } else {
    if (!navigator.clipboard || !navigator.clipboard.writeText) return;
    navigator.clipboard.writeText(text + ' ' + location.href);
    const b = event.target;
    const old = b.textContent;
    b.textContent = gmemorymatchT('copied');
    setTimeout(function () { b.textContent = old; }, MM_CONFIG.copyRevertMs);
  }
}
// FAQ 展開收合（7-3 防錯：純邏輯測試環境沒有 document 時安靜跳過）
if (typeof document !== 'undefined') {
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.addEventListener('click', function () { this.parentElement.classList.toggle('open'); });
  });
}
