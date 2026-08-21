// ══════════════════════════════════════════════════════════
// 反應力測試 — 共用遊戲邏輯（所有語言版本共用這一份，2026/08/18 多語言化時抽出）
//
// 【多語言架構約定】
//   這個檔案裡「不能出現任何給使用者看的文字」。所有文字一律透過
//   greactiontimetestT('key') 讀取頁面在載入這支JS之前先定義好的 window.GAME_I18N 字典。
//   → 遊戲邏輯有bug只要改這一個檔案，10種語言同時生效
//   → 翻譯只動各語言HTML裡的字典，不會誤改邏輯
//
// 遵循《新工具規劃守則.md》第七節（原始檔既有精神，重構後原樣保留）：
//   7-1 RT_CONFIG集中管理等待秒數/歷史筆數/分級門檻等所有數值（文字在GAME_I18N）
//   7-2 純函式（rtRatingIndex/rtComputeStats）跟DOM事件處理完全分開，方便單元測試
//   7-3 防錯：太早點擊（false start）明確處理，不會讓畫面卡住或顯示NaN；字典缺key不崩潰
//   7-4 資源清理：setTimeout 一律存 id，重新開始或離開頁面前 clearTimeout
//
// 【重構備註】原始檔的分級是 6 級（含 Infinity 封頂），這裡只把門檻數字留在
//   RT_CONFIG.ratingThresholds，對應的 6 段評語文字放在各語言字典的 ratingLabels 陣列，
//   順序與門檻一一對應。門檻值與判定方式與原始碼完全相同。
// ══════════════════════════════════════════════════════════

const RT_CONFIG = {
  minDelayMs: 1500,
  maxDelayMs: 5000,
  historyLimit: 5,
  copyRevertMs: 1500,
  colors: { idle: '#3b82f6', waiting: '#ef4444', ready: '#22c55e', early: '#f59e0b' },
  // 只放門檻數字，對應的評語文字放在 GAME_I18N.ratingLabels 同樣順序的陣列裡
  ratingThresholds: [200, 250, 300, 380, 500, Infinity]
};

// ── i18n 取字helper（7-3 防錯：缺key不崩潰）──
function greactiontimetestT(key, vars) {
  const dict = (typeof window !== 'undefined' && window.GAME_I18N) || {};
  let s = dict[key];
  if (typeof s !== 'string') {
    if (typeof console !== 'undefined' && console.warn) console.warn('[reaction-time-test] missing i18n key: ' + key);
    return '';
  }
  if (vars) {
    Object.keys(vars).forEach(function (k) {
      s = s.split('{' + k + '}').join(String(vars[k]));
    });
  }
  return s;
}

// ── 純函式：不碰DOM，也不含任何文字，方便單元測試/重用 ──
// 回傳「第幾級評語」的index，文字本身由呼叫端從 GAME_I18N.ratingLabels 取
function rtRatingIndex(ms) {
  for (let i = 0; i < RT_CONFIG.ratingThresholds.length; i++) {
    if (ms <= RT_CONFIG.ratingThresholds[i]) return i;
  }
  return RT_CONFIG.ratingThresholds.length - 1;
}
function rtRatingLabel(ms) {
  const list = (typeof window !== 'undefined' && window.GAME_I18N && window.GAME_I18N.ratingLabels) || [];
  return list[rtRatingIndex(ms)] || '';
}
function rtComputeStats(history) {
  if (!history.length) return { best: null, avg: null };
  const best = Math.min.apply(null, history);
  const avg = Math.round(history.reduce(function (a, b) { return a + b; }, 0) / history.length);
  return { best: best, avg: avg };
}

(function () {
  if (typeof document === 'undefined') return; // 純邏輯測試環境（無DOM）時安靜跳過UI部分
  const stage     = document.getElementById('rtStage');
  const stageText = document.getElementById('rtStageText');
  const stageSub  = document.getElementById('rtStageSub');
  const ratingEl  = document.getElementById('rtRating');
  const bestEl    = document.getElementById('rtBest');
  const avgEl     = document.getElementById('rtAvg');
  const historyEl = document.getElementById('rtHistory');
  if (!stage || !stageText) return; // 7-3 防錯：頁面結構不符時不炸掉整頁

  let rtState = 'idle';   // idle | waiting | ready | early
  let timerId = null;
  let readyAt = 0;
  let history = [];

  // 四種狀態的主/副標題文字。這裡刻意逐個寫成字面key，
  // 讓驗證器能掃出全部key並確認10個語言的字典都有定義。
  function stageMainText(s) {
    if (s === 'waiting') return greactiontimetestT('waitingMain');
    if (s === 'ready') return greactiontimetestT('readyMain');
    if (s === 'early') return greactiontimetestT('earlyMain');
    return greactiontimetestT('idleMain');
  }
  function stageSubText(s) {
    if (s === 'waiting') return greactiontimetestT('waitingSub');
    if (s === 'ready') return greactiontimetestT('readySub');
    if (s === 'early') return greactiontimetestT('earlySub');
    return greactiontimetestT('idleSub');
  }

  function setStageUI(s) {
    stageText.textContent = stageMainText(s);
    stageSub.textContent = stageSubText(s);
    stage.style.background = RT_CONFIG.colors[s] || RT_CONFIG.colors.idle;
  }

  function clearTimer() {
    if (timerId) { clearTimeout(timerId); timerId = null; }
  }

  function startRound() {
    clearTimer();
    rtState = 'waiting';
    setStageUI('waiting');
    const delay = RT_CONFIG.minDelayMs + Math.random() * (RT_CONFIG.maxDelayMs - RT_CONFIG.minDelayMs);
    timerId = setTimeout(function () {
      rtState = 'ready';
      readyAt = performance.now();
      setStageUI('ready');
    }, delay);
  }

  function handleStageClick() {
    if (rtState === 'idle' || rtState === 'early') { startRound(); return; }
    if (rtState === 'waiting') { clearTimer(); rtState = 'early'; setStageUI('early'); return; }
    if (rtState === 'ready') {
      const ms = Math.round(performance.now() - readyAt);
      recordResult(ms);
      rtState = 'idle';
      setStageUI('idle');
    }
  }

  function recordResult(ms) {
    history.unshift(ms);
    history = history.slice(0, RT_CONFIG.historyLimit);
    ratingEl.textContent = greactiontimetestT('msValue', { ms: ms }) + ' — ' + rtRatingLabel(ms);
    const stats = rtComputeStats(history);
    bestEl.textContent = stats.best != null ? greactiontimetestT('msShort', { ms: stats.best }) : '—';
    avgEl.textContent  = stats.avg  != null ? greactiontimetestT('msShort', { ms: stats.avg })  : '—';
    historyEl.innerHTML = history.map(function (v) {
      return '<span>' + greactiontimetestT('msShort', { ms: v }) + '</span>';
    }).join('');
    if (typeof gaSubmitScore === 'function') gaSubmitScore('reaction-time-test', ms);
  }

  stage.addEventListener('click', handleStageClick);
  setStageUI('idle');

  // 7-4 資源清理：離開頁面前清掉尚未觸發的計時器
  if (typeof window !== 'undefined') window.addEventListener('beforeunload', clearTimer);

  window._rtShareText = function () {
    const stats = rtComputeStats(history);
    return stats.best != null
      ? greactiontimetestT('shareWithScore', { ms: stats.best })
      : greactiontimetestT('shareNoScore');
  };
})();

function rtShareResult() {
  const text = (typeof window !== 'undefined' && window._rtShareText)
    ? window._rtShareText()
    : document.title;
  if (navigator.share) {
    navigator.share({ title: document.title, text: text, url: location.href }).catch(function () {});
  } else {
    navigator.clipboard.writeText(text + ' ' + location.href);
    const b = event.target;
    const old = b.textContent;
    b.textContent = greactiontimetestT('copied');
    setTimeout(function () { b.textContent = old; }, RT_CONFIG.copyRevertMs);
  }
}
// FAQ 展開收合（7-3 防錯：純邏輯測試環境沒有 document 時安靜跳過，
// 不能讓這一行在無DOM環境直接拋 ReferenceError 導致整支檔案無法被單元測試載入）
if (typeof document !== 'undefined') {
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.addEventListener('click', function () { this.parentElement.classList.toggle('open'); });
  });
}
