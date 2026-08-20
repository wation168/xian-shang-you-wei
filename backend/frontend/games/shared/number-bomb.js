// ══════════════════════════════════════════════════════════
// 數字炸彈（終極密碼猜數字）— 共用遊戲邏輯（所有語言版本共用這一份，多語言化時抽出）
//
// 【多語言架構約定】
//   這個檔案裡「不能出現任何給使用者看的文字」。所有文字一律透過 gnumberbombT('key') 讀取
//   頁面在載入這支JS之前先定義好的 window.GAME_I18N 字典。評語文字同理，
//   JS只留 NB_CONFIG.ratingThresholds 門檻數字，實際文字從 window.GAME_I18N.ratings 取。
//
// 遵循《新工具規劃守則.md》第七節：
//   7-1 NB_CONFIG集中管理範圍表/猜測次數緩衝/計分公式等數值
//   7-2 純函式（minGuessesForRange/judgeGuess/narrowRange/computeRoundScore等）跟DOM渲染分開，方便單元測試
//   7-3 防錯：猜測次數上限用「二分搜尋最佳策略反推」並用大量隨機模擬驗證公平性，輸入邊界檢查（isValidGuess）
//   7-4 資源清理：猜測紀錄DOM有上限（historyLimit），單/雙人模式各自獨立不互相污染狀態
// ══════════════════════════════════════════════════════════
const NB_CONFIG = {
  guessBuffer: 2,
  roundRanges: [50, 100, 200, 500, 1000],
  scoreBaseDivisor: 10,
  scoreEfficiencyBonus: 15,
  historyLimit: 6,
  adLoadDelayMs: 2000,
  copyRevertMs: 1500,
  duelRangeOptions: [50, 100, 200],
  duelDefaultRange: 100,
  // 只放門檻數字，對應的評語文字放在 GAME_I18N.ratings 同樣順序的陣列裡
  ratingThresholds: [80, 200, 400, 700, Infinity]
};

// ── i18n 取字helper（7-3 防錯：缺key不崩潰）──
function gnumberbombT(key, vars) {
  const dict = (typeof window !== 'undefined' && window.GAME_I18N) || {};
  let s = dict[key];
  if (typeof s !== 'string') {
    if (typeof console !== 'undefined' && console.warn) console.warn('[number-bomb] missing i18n key: ' + key);
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
function minGuessesForRange(range) {
  let guesses = 0, cap = 1;
  while (cap < range) { cap *= 2; guesses++; }
  return guesses;
}
function guessesAllowedForRange(range) { return minGuessesForRange(range) + NB_CONFIG.guessBuffer; }
function computeRoundConfig(roundNumber) {
  const idx = Math.min(roundNumber - 1, NB_CONFIG.roundRanges.length - 1);
  const range = NB_CONFIG.roundRanges[Math.max(0, idx)];
  return { round: roundNumber, range: range, min: 1, max: range, guessesAllowed: guessesAllowedForRange(range) };
}
function generateSecret(min, max) { return min + Math.floor(Math.random() * (max - min + 1)); }
function judgeGuess(secret, guess) { if (guess === secret) return 'hit'; return guess < secret ? 'higher' : 'lower'; }
function narrowRange(min, max, guess, result) {
  if (result === 'hit') return { min: guess, max: guess };
  if (result === 'higher') return { min: guess + 1, max: max };
  return { min: min, max: guess - 1 };
}
function isValidGuess(guess, min, max) { return Number.isInteger(guess) && guess >= min && guess <= max; }
function computeRoundScore(range, guessesUsed, guessesAllowed) {
  const base = Math.round(range / NB_CONFIG.scoreBaseDivisor);
  const efficiency = Math.max(0, guessesAllowed - guessesUsed) * NB_CONFIG.scoreEfficiencyBonus;
  return base + efficiency;
}
function computeFusePercent(guessesLeft, guessesAllowed) {
  if (guessesAllowed <= 0) return 0;
  return Math.max(0, Math.min(100, Math.round((guessesLeft / guessesAllowed) * 100)));
}
function nbRatingIndex(score) {
  const th = NB_CONFIG.ratingThresholds;
  for (let i = 0; i < th.length; i++) if (score <= th[i]) return i;
  return th.length - 1;
}
function nbComputeRating(score) {
  const list = (typeof window !== 'undefined' && window.GAME_I18N && window.GAME_I18N.ratings) || [];
  return list[nbRatingIndex(score)] || '';
}
function nextDuelPlayer(current) { return current === 'A' ? 'B' : 'A'; }

// ══════════════════════════════════════════════════════════
// UI層
// ══════════════════════════════════════════════════════════
function nbSwitchTab(tab) {
  if (typeof document === 'undefined') return;
  const tabSoloBtn = document.getElementById('nbTabSoloBtn');
  const tabDuelBtn = document.getElementById('nbTabDuelBtn');
  const soloPanel = document.getElementById('nbSoloPanel');
  const duelPanel = document.getElementById('nbDuelPanel');
  if (!tabSoloBtn || !tabDuelBtn || !soloPanel || !duelPanel) return;
  tabSoloBtn.classList.toggle('active', tab === 'solo');
  tabDuelBtn.classList.toggle('active', tab === 'duel');
  soloPanel.classList.toggle('active', tab === 'solo');
  duelPanel.classList.toggle('active', tab === 'duel');
}
if (typeof window !== 'undefined') window.nbSwitchTab = nbSwitchTab;

// ── 單人拆彈模式 ──
(function () {
  if (typeof document === 'undefined') return;
  const scoreEl = document.getElementById('nbScore');
  const roundBadge = document.getElementById('nbRoundBadge');
  const minEl = document.getElementById('nbRangeMin');
  const maxEl = document.getElementById('nbRangeMax');
  const fuseFill = document.getElementById('nbFuseFill');
  const fuseText = document.getElementById('nbFuseText');
  const feedbackEl = document.getElementById('nbFeedback');
  const inputEl = document.getElementById('nbGuessInput');
  const guessBtn = document.getElementById('nbGuessBtn');
  const logEl = document.getElementById('nbGuessLog');
  const overlay = document.getElementById('nbOverlay');
  const overTitle = document.getElementById('nbOverTitle');
  const overSub = document.getElementById('nbOverSub');
  const ratingEl = document.getElementById('nbRating');
  const bestEl = document.getElementById('nbBest');
  const bestRoundEl = document.getElementById('nbBestRound');
  const historyEl = document.getElementById('nbHistory');
  const startBtn = document.getElementById('nbStartBtn');
  if (!scoreEl || !roundBadge || !startBtn) return;

  let playing = false;
  let roundNumber = 1, roundInfo = null, secret = 0, min = 1, max = 50, guessesUsed = 0;
  let score = 0, bestScore = 0, bestRound = 0;
  let history = [];

  function renderStage() {
    minEl.textContent = String(min);
    maxEl.textContent = String(max);
    const left = roundInfo.guessesAllowed - guessesUsed;
    fuseFill.style.width = computeFusePercent(left, roundInfo.guessesAllowed) + '%';
    fuseText.textContent = gnumberbombT('fuseText', { left: left, allowed: roundInfo.guessesAllowed });
  }

  function loadRound(n) {
    roundNumber = n;
    roundInfo = computeRoundConfig(n);
    min = roundInfo.min; max = roundInfo.max;
    secret = generateSecret(min, max);
    guessesUsed = 0;
    logEl.innerHTML = '';
    feedbackEl.textContent = gnumberbombT('rangeReady', { min: min, max: max });
    roundBadge.textContent = gnumberbombT('roundLabel', { n: n });
    roundBadge.classList.remove('nb-round-up');
    void roundBadge.offsetWidth;
    roundBadge.classList.add('nb-round-up');
    inputEl.min = String(min); inputEl.max = String(max);
    inputEl.value = '';
    inputEl.disabled = false; guessBtn.disabled = false;
    renderStage();
  }

  function explode() {
    stopGame(gnumberbombT('explodeTitle'), gnumberbombT('explodeSub', { n: roundNumber, s: secret, sc: score }));
  }

  function stopGame(title, sub) {
    playing = false;
    inputEl.disabled = true; guessBtn.disabled = true;
    bestScore = Math.max(bestScore, score);
    bestEl.textContent = String(bestScore);
    bestRound = Math.max(bestRound, roundNumber);
    bestRoundEl.textContent = gnumberbombT('roundLabel', { n: bestRound });
    ratingEl.textContent = gnumberbombT('scoreShort', { v: score }) + ' — ' + nbComputeRating(score);
    window._nbLastScore = score;
    if (typeof gaSubmitScore === 'function') gaSubmitScore('number-bomb', score);
    overTitle.textContent = title;
    overSub.textContent = sub;
    overlay.classList.add('show');
    startBtn.textContent = gnumberbombT('restartChallengeBtn');
  }

  function nbSubmitGuessInternal() {
    if (!playing) return;
    const raw = inputEl.value;
    const guess = parseInt(raw, 10);
    if (!isValidGuess(guess, min, max)) {
      feedbackEl.textContent = gnumberbombT('invalidGuess', { min: min, max: max });
      return;
    }
    guessesUsed++;
    const result = judgeGuess(secret, guess);
    const tag = document.createElement('span');
    tag.className = 'nb-log-item' + (result === 'hit' ? ' nb-log-hit' : '');
    tag.textContent = result === 'hit' ? gnumberbombT('logHit', { g: guess })
      : (result === 'higher' ? gnumberbombT('logHigher', { g: guess }) : gnumberbombT('logLower', { g: guess }));
    logEl.appendChild(tag);

    if (result === 'hit') {
      const gained = computeRoundScore(roundInfo.range, guessesUsed, roundInfo.guessesAllowed);
      score += gained;
      scoreEl.textContent = String(score);
      history.unshift(gained);
      history = history.slice(0, NB_CONFIG.historyLimit);
      historyEl.innerHTML = history.map(function (v) { return '<span>' + gnumberbombT('scoreGainShort', { v: v }) + '</span>'; }).join('');
      feedbackEl.textContent = gnumberbombT('hitFeedback', { s: secret, g: gained });
      inputEl.disabled = true; guessBtn.disabled = true;
      setTimeout(function () { loadRound(roundNumber + 1); }, 1400);
      return;
    }

    const narrowed = narrowRange(min, max, guess, result);
    min = narrowed.min; max = narrowed.max;
    feedbackEl.textContent = result === 'higher' ? gnumberbombT('feedbackHigher') : gnumberbombT('feedbackLower');
    renderStage();

    if (guessesUsed >= roundInfo.guessesAllowed) {
      explode();
    }
  }
  window.nbSubmitGuess = nbSubmitGuessInternal;

  inputEl.addEventListener('keydown', function (e) { if (e.key === 'Enter') nbSubmitGuessInternal(); });

  function nbStartInternal() {
    playing = true;
    score = 0;
    scoreEl.textContent = '0';
    ratingEl.textContent = '';
    overlay.classList.remove('show');
    loadRound(1);
  }
  window.nbStart = nbStartInternal;
})();

function nbShareResult() {
  const score = (typeof window !== 'undefined') ? window._nbLastScore : null;
  const text = (score != null)
    ? gnumberbombT('shareWithScore', { s: score })
    : gnumberbombT('shareNoScore');
  if (typeof navigator !== 'undefined' && navigator.share) {
    navigator.share({ title: document.title, text: text, url: location.href }).catch(function () {});
  } else {
    if (!navigator.clipboard || !navigator.clipboard.writeText) return; // 7-3 防錯：無剪貼簿API時安全退出
    navigator.clipboard.writeText(text + ' ' + location.href);
    const b = event.target;
    const old = b.textContent;
    b.textContent = gnumberbombT('copied');
    setTimeout(function () { b.textContent = old; }, NB_CONFIG.copyRevertMs);
  }
}
if (typeof window !== 'undefined') window.nbShareResult = nbShareResult;

// ── 雙人對戰模式 ──
(function () {
  if (typeof document === 'undefined') return;
  const optsWrap = document.getElementById('nbDuelRangeOpts');
  const setupEl = document.getElementById('nbDuelSetup');
  const stageEl = document.getElementById('nbDuelStage');
  const turnBadge = document.getElementById('nbTurnBadge');
  const minEl = document.getElementById('nbDuelMin');
  const maxEl = document.getElementById('nbDuelMax');
  const feedbackEl = document.getElementById('nbDuelFeedback');
  const inputEl = document.getElementById('nbDuelInput');
  const guessBtn = document.getElementById('nbDuelGuessBtn');
  const logEl = document.getElementById('nbDuelLog');
  const overlay = document.getElementById('nbDuelOverlay');
  const overTitle = document.getElementById('nbDuelOverTitle');
  const overSub = document.getElementById('nbDuelOverSub');
  if (!optsWrap || !setupEl || !stageEl) return;

  let chosenRange = NB_CONFIG.duelDefaultRange;
  let secret = 0, min = 1, max = chosenRange, currentPlayer = 'A', active = false;

  optsWrap.innerHTML = NB_CONFIG.duelRangeOptions.map(function (r) {
    return '<button class="nb-range-opt' + (r === chosenRange ? ' active' : '') + '" data-range="' + r + '">' + gnumberbombT('duelRangeLabel', { r: r }) + '</button>';
  }).join('');
  optsWrap.querySelectorAll('.nb-range-opt').forEach(function (btn) {
    btn.addEventListener('click', function () {
      chosenRange = parseInt(btn.getAttribute('data-range'), 10);
      optsWrap.querySelectorAll('.nb-range-opt').forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
    });
  });

  function playerLabel(p) { return p === 'A' ? gnumberbombT('namePlayerA') : gnumberbombT('namePlayerB'); }

  function renderTurn() {
    turnBadge.textContent = (currentPlayer === 'A' ? '🔴 ' : '🔵 ') + gnumberbombT('turnOf', { name: playerLabel(currentPlayer) });
    turnBadge.className = 'nb-turn-badge ' + (currentPlayer === 'A' ? 'nb-turn-a' : 'nb-turn-b');
    minEl.textContent = String(min); maxEl.textContent = String(max);
    inputEl.min = String(min); inputEl.max = String(max);
    inputEl.value = '';
  }

  function nbDuelStartInternal() {
    secret = generateSecret(1, chosenRange);
    min = 1; max = chosenRange; currentPlayer = 'A'; active = true;
    logEl.innerHTML = '';
    feedbackEl.textContent = gnumberbombT('duelSecretReady', { r: chosenRange });
    setupEl.style.display = 'none';
    stageEl.style.display = 'block';
    overlay.classList.remove('show');
    guessBtn.disabled = false; inputEl.disabled = false;
    renderTurn();
  }
  window.nbDuelStart = nbDuelStartInternal;

  function nbDuelSubmitGuessInternal() {
    if (!active) return;
    const guess = parseInt(inputEl.value, 10);
    if (!isValidGuess(guess, min, max)) {
      feedbackEl.textContent = gnumberbombT('invalidGuess', { min: min, max: max });
      return;
    }
    const result = judgeGuess(secret, guess);
    const tag = document.createElement('span');
    tag.className = 'nb-log-item' + (result === 'hit' ? ' nb-log-hit' : '');
    tag.textContent = gnumberbombT('duelLogEntry', { name: playerLabel(currentPlayer), g: guess })
      + (result === 'hit' ? ' 💥' : (result === 'higher' ? ' ⬆️' : ' ⬇️'));
    logEl.appendChild(tag);

    if (result === 'hit') {
      active = false;
      inputEl.disabled = true; guessBtn.disabled = true;
      const loser = playerLabel(currentPlayer);
      const winner = playerLabel(nextDuelPlayer(currentPlayer));
      overTitle.textContent = gnumberbombT('duelLoseTitle', { name: loser });
      overSub.textContent = gnumberbombT('duelWinSub', { name: winner, s: secret });
      overlay.classList.add('show');
      return;
    }

    const narrowed = narrowRange(min, max, guess, result);
    min = narrowed.min; max = narrowed.max;
    currentPlayer = nextDuelPlayer(currentPlayer);
    feedbackEl.textContent = result === 'higher' ? gnumberbombT('duelFeedbackHigher') : gnumberbombT('duelFeedbackLower');
    renderTurn();
  }
  window.nbDuelSubmitGuess = nbDuelSubmitGuessInternal;

  inputEl.addEventListener('keydown', function (e) { if (e.key === 'Enter') nbDuelSubmitGuessInternal(); });

  function nbDuelResetInternal() {
    active = false;
    setupEl.style.display = 'block';
    stageEl.style.display = 'none';
    overlay.classList.remove('show');
  }
  window.nbDuelReset = nbDuelResetInternal;
})();

if (typeof document !== 'undefined') {
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.addEventListener('click', function () { this.parentElement.classList.toggle('open'); });
  });
}
