// ══════════════════════════════════════════════════════════
// 打地鼠 — 共用遊戲邏輯（所有語言版本共用這一份，多語言化時抽出）
//
// 【多語言架構約定】
//   這個檔案裡「不能出現任何給使用者看的文字」。所有文字一律透過 gwhackamoleT('key') 讀取
//   頁面在載入這支JS之前先定義好的 window.GAME_I18N 字典。
//   → 遊戲邏輯有bug只要改這一個檔案，10種語言同時生效
//   → 翻譯只動各語言HTML裡的字典，不會誤改邏輯
//
// 遵循《新工具規劃守則.md》第七節：
//   7-1 WAM_CONFIG集中管理格數/時限/地鼠出現節奏等所有可調數值
//   7-2 純函式（wamComputeRating/wamLevelIndexForScore）跟 UI/計時器邏輯分開
//   7-3 防錯：地鼠已縮回時點擊不計分、遊戲未開始時點擊無效
//   7-4 資源清理：所有 setTimeout/setInterval 都存id，遊戲結束、
//        重新開始、離開頁面前統一 clearAll()
// ══════════════════════════════════════════════════════════
const WAM_CONFIG = {
  holesCount: 9,
  gameDurationSec: 30,
  historyLimit: 5,
  moleEmoji: '🐹',
  copyRevertMs: 1500,
  adLoadDelayMs: 2000,
  // scoreThreshold累積分數達標時，套用該級距的難度設定（地鼠停留變短、出現變密集、
  // 可同時出現隻數增加），並加上bonusSeconds秒的時間獎勵，讓玩家能持續挑戰更高分。
  difficultyLevels: [
    { scoreThreshold: 0,  moleUpMsMin: 650, moleUpMsMax: 1300, spawnIntervalMsMin: 500, spawnIntervalMsMax: 900, maxActiveMoles: 2, bonusSeconds: 0 },
    { scoreThreshold: 10, moleUpMsMin: 560, moleUpMsMax: 1100, spawnIntervalMsMin: 430, spawnIntervalMsMax: 780, maxActiveMoles: 2, bonusSeconds: 5 },
    { scoreThreshold: 20, moleUpMsMin: 470, moleUpMsMax: 900,  spawnIntervalMsMin: 360, spawnIntervalMsMax: 660, maxActiveMoles: 3, bonusSeconds: 5 },
    { scoreThreshold: 32, moleUpMsMin: 390, moleUpMsMax: 740,  spawnIntervalMsMin: 300, spawnIntervalMsMax: 560, maxActiveMoles: 3, bonusSeconds: 5 },
    { scoreThreshold: 46, moleUpMsMin: 330, moleUpMsMax: 620,  spawnIntervalMsMin: 250, spawnIntervalMsMax: 470, maxActiveMoles: 4, bonusSeconds: 6 }
  ],
  // 只放門檻數字，對應的評語文字放在 GAME_I18N.ratings 同樣順序的陣列裡
  ratingThresholds: [10, 18, 26, 34, Infinity]
};

// ── i18n 取字helper（7-3 防錯：缺key不崩潰）──
function gwhackamoleT(key, vars) {
  const dict = (typeof window !== 'undefined' && window.GAME_I18N) || {};
  let s = dict[key];
  if (typeof s !== 'string') {
    if (typeof console !== 'undefined' && console.warn) console.warn('[whack-a-mole] missing i18n key: ' + key);
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
function wamRatingIndex(score) {
  const th = WAM_CONFIG.ratingThresholds;
  for (let i = 0; i < th.length; i++) if (score <= th[i]) return i;
  return th.length - 1;
}
function wamComputeRating(score) {
  const list = (typeof window !== 'undefined' && window.GAME_I18N && window.GAME_I18N.ratings) || [];
  return list[wamRatingIndex(score)] || '';
}
function wamRandBetween(min, max) { return min + Math.random() * (max - min); }
// 純函式：依目前分數找出應套用的難度級距索引（levels依scoreThreshold遞增排序）
function wamLevelIndexForScore(score, levels) {
  let idx = 0;
  for (let i = 0; i < levels.length; i++) {
    if (score >= levels[i].scoreThreshold) idx = i;
  }
  return idx;
}

(function () {
  if (typeof document === 'undefined') return; // 純邏輯測試環境（無DOM）時安靜跳過UI部分

  const board    = document.getElementById('wamBoard');
  const scoreEl  = document.getElementById('wamScore');
  const timeEl   = document.getElementById('wamTime');
  const ratingEl = document.getElementById('wamRating');
  const bestEl   = document.getElementById('wamBest');
  const historyEl= document.getElementById('wamHistory');
  const startBtn = document.getElementById('wamStartBtn');
  const timeWrap = document.getElementById('wamTimeWrap');
  const levelEl  = document.getElementById('wamLevelBadge');
  const toastEl  = document.getElementById('wamToast');
  if (!board || !scoreEl) return; // 7-3 防錯：頁面結構不符時不炸掉整頁

  let holes = [];
  let score = 0;
  let timeLeft = WAM_CONFIG.gameDurationSec;
  let playing = false;
  let activeCount = 0;
  let timers = { gameInterval: null, spawnTimeout: null, moleTimeouts: [], toastTimeout: null };
  let history = [];
  let levelIdx = 0;
  let curLevel = WAM_CONFIG.difficultyLevels[0];

  // 初始化九宮格
  for (let i = 0; i < WAM_CONFIG.holesCount; i++) {
    const hole = document.createElement('div');
    hole.className = 'wam-hole';
    const mole = document.createElement('div');
    mole.className = 'wam-mole';
    mole.textContent = WAM_CONFIG.moleEmoji;
    hole.appendChild(mole);
    hole.addEventListener('click', function () { onHoleClick(i); });
    board.appendChild(hole);
    holes.push({ el: hole, up: false });
  }

  function clearAll() {
    if (timers.gameInterval) { clearInterval(timers.gameInterval); timers.gameInterval = null; }
    if (timers.spawnTimeout) { clearTimeout(timers.spawnTimeout); timers.spawnTimeout = null; }
    if (timers.toastTimeout) { clearTimeout(timers.toastTimeout); timers.toastTimeout = null; }
    timers.moleTimeouts.forEach(clearTimeout);
    timers.moleTimeouts = [];
  }

  function setHoleUp(i, up) {
    holes[i].up = up;
    holes[i].el.classList.toggle('up', up);
  }

  function scheduleSpawn() {
    const delay = wamRandBetween(curLevel.spawnIntervalMsMin, curLevel.spawnIntervalMsMax);
    timers.spawnTimeout = setTimeout(trySpawn, delay);
  }

  function trySpawn() {
    if (!playing) return;
    if (activeCount < curLevel.maxActiveMoles) {
      const emptyIdx = holes.map((h, i) => h.up ? -1 : i).filter(i => i >= 0);
      if (emptyIdx.length) {
        const idx = emptyIdx[Math.floor(Math.random() * emptyIdx.length)];
        setHoleUp(idx, true);
        activeCount++;
        const upMs = wamRandBetween(curLevel.moleUpMsMin, curLevel.moleUpMsMax);
        const tid = setTimeout(function () {
          if (holes[idx].up) { setHoleUp(idx, false); activeCount--; }
        }, upMs);
        timers.moleTimeouts.push(tid);
      }
    }
    scheduleSpawn();
  }

  function showToast(text) {
    toastEl.textContent = text;
    toastEl.classList.remove('show');
    void toastEl.offsetWidth;
    toastEl.classList.add('show');
    if (timers.toastTimeout) clearTimeout(timers.toastTimeout);
    timers.toastTimeout = setTimeout(function () { toastEl.classList.remove('show'); }, 1400);
  }

  function applyLevelUp() {
    curLevel = WAM_CONFIG.difficultyLevels[levelIdx];
    levelEl.textContent = 'Lv.' + (levelIdx + 1);
    levelEl.classList.remove('wam-level-up');
    void levelEl.offsetWidth;
    levelEl.classList.add('wam-level-up');

    if (curLevel.bonusSeconds > 0) {
      timeLeft += curLevel.bonusSeconds;
      timeEl.textContent = String(timeLeft);
      timeWrap.classList.remove('wam-bonus');
      void timeWrap.offsetWidth;
      timeWrap.classList.add('wam-bonus');
      showToast(gwhackamoleT('levelUpBonus', { n: curLevel.bonusSeconds }));
    } else {
      showToast(gwhackamoleT('levelUp'));
    }
  }

  function onHoleClick(i) {
    if (!playing) return;
    if (holes[i].up) {
      setHoleUp(i, false);
      activeCount--;
      score++;
      scoreEl.textContent = score;

      const newLevelIdx = wamLevelIndexForScore(score, WAM_CONFIG.difficultyLevels);
      if (newLevelIdx !== levelIdx) {
        levelIdx = newLevelIdx;
        applyLevelUp();
      }
    }
  }

  function wamStartInternal() {
    clearAll();
    holes.forEach((h, i) => setHoleUp(i, false));
    score = 0;
    activeCount = 0;
    levelIdx = 0;
    curLevel = WAM_CONFIG.difficultyLevels[0];
    timeLeft = WAM_CONFIG.gameDurationSec;
    scoreEl.textContent = '0';
    timeEl.textContent = String(timeLeft);
    levelEl.textContent = 'Lv.1';
    toastEl.classList.remove('show');
    ratingEl.textContent = '';
    playing = true;
    startBtn.disabled = true;
    startBtn.textContent = gwhackamoleT('playingBtn');

    timers.gameInterval = setInterval(function () {
      timeLeft--;
      timeEl.textContent = String(Math.max(timeLeft, 0));
      if (timeLeft <= 0) endGame();
    }, 1000);

    scheduleSpawn();
  }

  function endGame() {
    playing = false;
    clearAll();
    holes.forEach((h, i) => setHoleUp(i, false));
    startBtn.disabled = false;
    startBtn.textContent = gwhackamoleT('playAgainBtn');
    ratingEl.textContent = gwhackamoleT('scoreShort', { s: score }) + ' — ' + wamComputeRating(score);

    history.unshift(score);
    history = history.slice(0, WAM_CONFIG.historyLimit);
    const best = Math.max(...history);
    bestEl.textContent = gwhackamoleT('scoreShort', { s: best });
    historyEl.innerHTML = history.map(function (v) { return '<span>' + gwhackamoleT('scoreShort', { s: v }) + '</span>'; }).join('');

    window._wamLastScore = score;
    window._wamBestScore = best;
    if (typeof gaSubmitScore === 'function') gaSubmitScore('whack-a-mole', score);
  }

  window.wamStart = wamStartInternal;

  // 7-4 資源清理：離開頁面前清掉所有計時器
  window.addEventListener('beforeunload', clearAll);
})();

function wamShareResult() {
  const score = window._wamLastScore;
  const text = (score != null)
    ? gwhackamoleT('shareWithScore', { s: score })
    : gwhackamoleT('shareNoScore');
  if (navigator.share) {
    navigator.share({ title: document.title, text: text, url: location.href }).catch(function () {});
  } else {
    if (!navigator.clipboard || !navigator.clipboard.writeText) return;
    navigator.clipboard.writeText(text + ' ' + location.href);
    const b = event.target;
    const old = b.textContent;
    b.textContent = gwhackamoleT('copied');
    setTimeout(function () { b.textContent = old; }, WAM_CONFIG.copyRevertMs);
  }
}
// FAQ 展開收合（7-3 防錯：純邏輯測試環境沒有 document 時安靜跳過，
// 不能讓這一行在無DOM環境直接拋 ReferenceError 導致整支檔案無法被單元測試載入）
if (typeof document !== 'undefined') {
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.addEventListener('click', function () { this.parentElement.classList.toggle('open'); });
  });
}
