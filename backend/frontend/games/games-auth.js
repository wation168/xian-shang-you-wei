// ══════════════════════════════════════════════════════════
// 遊戲排行榜共用模組（2026/08/15 新增）
// 帥哥鴻反饋「沒有比賽機制，可以設定登入加入比賽排名」——
// 沿用網站既有的會員登入系統（跟股票App共用同一個localStorage token），
// 不做另一套帳號系統。玩家用Google或LINE登入後，遊戲分數會記在他的
// 帳號名下，排行榜任何人都能看，不用登入也能玩遊戲（只是分數不會上榜）。
//
// 【2026/08/17 多語言化】所有給使用者看的文字改走 gaT() 取字：
//   * 預設值 GA_TEXT_DEFAULT 就是繁中版原文 → 繁中頁面不需要帶任何語言包，
//     行為與文字跟多語言化之前100%相同（避免既有13個繁中頁面產生回歸風險）
//   * 其餘9語言的頁面在載入本檔之前先定義 window.GA_LANG_PACK 覆蓋
//   * 排行榜本身「不分語言共用同一份資料」（game_slug 與語言無關），
//     所以英文頁玩出的分數會跟繁中頁的玩家排在同一張榜上，這是刻意的設計
//
// 遵循《新工具規劃守則.md》第七節：
//   7-1 GA_CONFIG集中管理API位置/儲存key/顯示筆數等所有可調數值
//   7-2 純函式（gaFormatScore/gaMedal/gaT）跟DOM/fetch邏輯分開
//   7-3 防錯：未登入送分直接跳過並提示、API失敗不擋遊戲本身進行、語言包缺key退回預設
//   7-4 資源清理：toast的setTimeout存id並可重複觸發不堆疊
// ══════════════════════════════════════════════════════════
const GA_CONFIG = {
  googleClientId: '584257110691-jtn1tf282q4vsfn7c7vhp9c12m6ino1n.apps.googleusercontent.com',
  tokenStorageKey: 'auth_token', // 跟 frontend/index.html 共用同一把 key，兩邊登入狀態互通
  leaderboardLimit: 20,
  toastMs: 2600,
  loginReminderDismissKey: 'ga_login_reminder_dismissed', // sessionStorage key，關掉進場彈窗後本次瀏覽不再彈
  // 繁中預設遊戲名稱（2026/08/17 補齊到13款；原本只登記5款，其餘會顯示「這個遊戲」）
  gameNames: {
    'reaction-time-test': '反應力測試',
    'memory-match': '記憶翻牌',
    'whack-a-mole': '打地鼠',
    'piano-tiles': '鋼琴塊',
    'snake': '貪食蛇',
    'gomoku': '五子棋',
    'halloween-spell-draw': '萬聖節塗鴉法術',
    '2048': '2048',
    'sudoku': '數獨',
    'sliding-puzzle': '數字推盤',
    'chess': '西洋棋',
    'number-bomb': '數字炸彈',
    'minesweeper': '踩地雷'
  },
  // 繁中預設分數單位（2026/08/17 補齊到13款；原本只有5款，其餘排行榜會顯示裸數字）
  scoreUnit: {
    'reaction-time-test': 'ms',
    'memory-match': '步',
    'sliding-puzzle': '步',
    'whack-a-mole': '分',
    'piano-tiles': '分',
    'snake': '分',
    'halloween-spell-draw': '分',
    '2048': '分',
    'sudoku': '分',
    'number-bomb': '分',
    'minesweeper': '分'
  }
};

// ── 文字預設值（＝繁中原文）。其他語言由頁面的 window.GA_LANG_PACK 覆蓋 ──
const GA_TEXT_DEFAULT = {
  loginToRank: '登入才能把成績送上排行榜 🏆',
  newRecord: '🎉 新紀錄！目前排名第 {r} 名',
  submitted: '已送上排行榜，目前排名第 {r} 名',
  emptyBoard: '還沒有人上榜，登入後第一個玩就能拿下第一名！',
  loadingBoard: '載入排行榜中…',
  googleFail: 'Google 登入失敗',
  connFail: '連線失敗，請稍後再試',
  loginOk: '登入成功！',
  logoutOk: '已登出',
  lineLoginOk: 'LINE登入成功！',
  lineLoginFail: 'LINE登入失敗，請再試一次',
  logoutBtn: '登出',
  loadingName: '載入中…',
  player: '玩家',
  loginTip: '登入才能把成績存上排行榜，跟朋友比分數！',
  lineBtn: '💬 用LINE登入',
  fsEnter: '⛶ 全螢幕',
  fsExit: '✕ 離開全螢幕',
  fsAria: '全螢幕放大遊戲',
  fsUnsupported: '這個瀏覽器不支援全螢幕',
  reminderTitle: '登入才能把{game}成績存上排行榜',
  reminderSub: '不登入也能繼續玩，只是分數不會被記錄下來',
  reminderSkip: '先不用，直接玩',
  reminderClose: '關閉',
  badge: '🔒 登入才能上榜',
  thisGame: '這個遊戲'
};

// ── 純函式：取字（7-3 防錯：語言包沒有這個key就退回繁中預設，缺到底才回空字串）──
function gaT(key, vars) {
  const pack = (typeof window !== 'undefined' && window.GA_LANG_PACK) || {};
  let s = (typeof pack[key] === 'string') ? pack[key] : GA_TEXT_DEFAULT[key];
  if (typeof s !== 'string') {
    if (typeof console !== 'undefined' && console.warn) console.warn('[games-auth] missing text key: ' + key);
    return '';
  }
  if (vars) {
    Object.keys(vars).forEach(function (k) {
      s = s.split('{' + k + '}').join(String(vars[k]));
    });
  }
  return s;
}
function gaGameName(gameSlug) {
  const pack = (typeof window !== 'undefined' && window.GA_LANG_PACK) || {};
  if (pack.gameNames && typeof pack.gameNames[gameSlug] === 'string') return pack.gameNames[gameSlug];
  return GA_CONFIG.gameNames[gameSlug] || gaT('thisGame');
}
function gaScoreUnit(gameSlug) {
  const pack = (typeof window !== 'undefined' && window.GA_LANG_PACK) || {};
  if (pack.scoreUnit && typeof pack.scoreUnit[gameSlug] === 'string') return pack.scoreUnit[gameSlug];
  return GA_CONFIG.scoreUnit[gameSlug] || '';
}

function gaGetAPI() {
  const isLocal = location.hostname === 'localhost' || location.hostname === '127.0.0.1' || location.hostname.startsWith('192.168');
  return isLocal ? 'http://localhost:8000' : 'https://api.softglow-ai.com';
}

// ── 純函式：不碰DOM ──
function gaFormatScore(gameSlug, score) {
  return score + gaScoreUnit(gameSlug);
}
function gaMedal(rank) {
  if (rank === 1) return '🥇';
  if (rank === 2) return '🥈';
  if (rank === 3) return '🥉';
  return '#' + rank;
}

// ── Token 存取（跟 index.html 共用同一個 localStorage key）──
function gaGetToken() { return localStorage.getItem(GA_CONFIG.tokenStorageKey); }
function gaSetToken(t) { localStorage.setItem(GA_CONFIG.tokenStorageKey, t); }
function gaClearToken() { localStorage.removeItem(GA_CONFIG.tokenStorageKey); }
function gaIsLoggedIn() { return !!gaGetToken(); }
function gaAuthHeaders() {
  const t = gaGetToken();
  return t ? { 'Authorization': 'Bearer ' + t, 'Content-Type': 'application/json' } : { 'Content-Type': 'application/json' };
}

let _gaToastTimerId = null;
function gaToast(msg) {
  let el = document.getElementById('gaToast');
  if (!el) {
    el = document.createElement('div');
    el.id = 'gaToast';
    el.style.cssText = 'position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:#1e293b;color:#fff;padding:10px 18px;border-radius:20px;font-size:13px;font-weight:600;z-index:9999;opacity:0;transition:opacity .25s;pointer-events:none;box-shadow:0 4px 12px rgba(0,0,0,.25)';
    document.body.appendChild(el);
  }
  el.textContent = msg;
  el.style.opacity = '1';
  if (_gaToastTimerId) clearTimeout(_gaToastTimerId);
  _gaToastTimerId = setTimeout(function () { el.style.opacity = '0'; }, GA_CONFIG.toastMs);
}

// ── 送分（需要登入；未登入時不報錯，只提示一次，不影響遊戲本身）──
async function gaSubmitScore(gameSlug, score) {
  if (!gaIsLoggedIn()) {
    gaToast(gaT('loginToRank'));
    return null;
  }
  try {
    const res = await fetch(gaGetAPI() + '/api/games/score', {
      method: 'POST',
      headers: gaAuthHeaders(),
      body: JSON.stringify({ game_slug: gameSlug, score: score }),
      signal: AbortSignal.timeout(8000)
    });
    if (!res.ok) {
      if (res.status === 401) { gaClearToken(); gaRenderAllWidgets(); }
      return null; // 7-3 防錯：送分失敗不影響玩家看到的遊戲結果
    }
    const data = await res.json();
    if (data.is_new_best) {
      gaToast(gaT('newRecord', { r: data.rank }));
    } else if (data.rank) {
      gaToast(gaT('submitted', { r: data.rank }));
    }
    gaRefreshLeaderboards(gameSlug);
    return data;
  } catch (e) {
    return null; // 網路失敗一律安靜失敗，遊戲本身不受影響
  }
}

// ── 排行榜載入與渲染 ──
async function gaLoadLeaderboard(gameSlug) {
  try {
    const res = await fetch(gaGetAPI() + '/api/games/leaderboard/' + encodeURIComponent(gameSlug) + '?limit=' + GA_CONFIG.leaderboardLimit, {
      signal: AbortSignal.timeout(8000)
    });
    if (!res.ok) return null;
    return await res.json();
  } catch (e) {
    return null;
  }
}

function gaRenderLeaderboardList(container, gameSlug, data) {
  if (!container) return;
  if (!data || !data.leaderboard || !data.leaderboard.length) {
    container.innerHTML = '<div class="ga-empty">' + _gaEscape(gaT('emptyBoard')) + '</div>';
    return;
  }
  container.innerHTML = data.leaderboard.map(function (row) {
    return '<div class="ga-row' + (row.rank <= 3 ? ' ga-top3' : '') + '">' +
      '<span class="ga-rank">' + gaMedal(row.rank) + '</span>' +
      '<span class="ga-name">' + _gaEscape(row.name) + '</span>' +
      '<span class="ga-score">' + gaFormatScore(gameSlug, row.score) + '</span>' +
      '</div>';
  }).join('');
}
function _gaEscape(s) {
  return String(s).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}

const _gaLeaderboardContainers = {}; // gameSlug -> containerEl，供送分後即時重新整理用
async function gaRefreshLeaderboards(gameSlug) {
  const container = _gaLeaderboardContainers[gameSlug];
  if (!container) return;
  const data = await gaLoadLeaderboard(gameSlug);
  gaRenderLeaderboardList(container, gameSlug, data);
}

function gaMountLeaderboard(containerId, gameSlug) {
  const container = document.getElementById(containerId);
  if (!container) return;
  _gaLeaderboardContainers[gameSlug] = container;
  container.innerHTML = '<div class="ga-empty">' + _gaEscape(gaT('loadingBoard')) + '</div>';
  gaLoadLeaderboard(gameSlug).then(function (data) {
    gaRenderLeaderboardList(container, gameSlug, data);
  });
}

// ── 登入狀態小工具（Google + LINE）──
let _gaGoogleReady = false;
function _gaInitGoogleButton(btnEl) {
  if (typeof google === 'undefined' || !google.accounts || !btnEl) return;
  if (!_gaGoogleReady) {
    _gaGoogleReady = true;
    google.accounts.id.initialize({
      client_id: GA_CONFIG.googleClientId,
      callback: _gaHandleGoogleLogin
    });
  }
  if (!btnEl.hasChildNodes()) {
    google.accounts.id.renderButton(btnEl, { theme: 'outline', size: 'medium', text: 'signin_with', width: 220 });
  }
}
async function _gaHandleGoogleLogin(response) {
  try {
    const res = await fetch(gaGetAPI() + '/auth/google', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ google_token: response.credential }),
      signal: AbortSignal.timeout(10000)
    });
    const data = await res.json();
    if (!res.ok) { gaToast(data.detail || gaT('googleFail')); return; }
    gaSetToken(data.token);
    gaToast(gaT('loginOk'));
    gaRenderAllWidgets();
  } catch (e) {
    gaToast(gaT('connFail'));
  }
}
function gaLineLoginUrl() {
  const returnUrl = location.pathname; // 登入完成後導回目前這個遊戲頁面（含語言路徑，不會跳掉語言）
  return gaGetAPI() + '/auth/line?return_url=' + encodeURIComponent(returnUrl);
}
function gaLogout() {
  gaClearToken();
  gaToast(gaT('logoutOk'));
  gaRenderAllWidgets();
}
window.gaLogout = gaLogout;

async function _gaFetchNickname() {
  try {
    const res = await fetch(gaGetAPI() + '/auth/me', { headers: gaAuthHeaders(), signal: AbortSignal.timeout(8000) });
    if (!res.ok) return null;
    const data = await res.json();
    return (data.nickname && data.nickname.trim()) || (data.email ? data.email.split('@')[0] : gaT('player'));
  } catch (e) {
    return null;
  }
}

const _gaWidgetContainers = []; // 記錄所有已掛載的登入widget容器id，登入狀態變化時統一重繪
function gaRenderAllWidgets() {
  _gaWidgetContainers.forEach(function (id) { gaMountAuthWidget(id); });
  // 2026/08/17新增：登入/登出時同步處理進場彈窗跟盤面常駐提示——
  // 登入成功就整個拿掉（不需要再提醒）；登出的話重新掛回盤面提示（彈窗不重複打擾，只留常駐提示）
  if (gaIsLoggedIn()) {
    _gaRemoveLoginReminders();
  } else if (_gaReminderGameSlug) {
    _gaMountBoardBadge();
  }
}

async function gaMountAuthWidget(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  if (_gaWidgetContainers.indexOf(containerId) === -1) _gaWidgetContainers.push(containerId);

  if (gaIsLoggedIn()) {
    container.innerHTML = '<div class="ga-logged-in">👤 <span id="' + containerId + 'Name">' + _gaEscape(gaT('loadingName')) + '</span> <button class="ga-logout-btn" onclick="gaLogout()">' + _gaEscape(gaT('logoutBtn')) + '</button></div>';
    const name = await _gaFetchNickname();
    const nameEl = document.getElementById(containerId + 'Name');
    if (nameEl) nameEl.textContent = name || gaT('player');
    if (!name) { gaClearToken(); gaMountAuthWidget(containerId); } // token失效，視同未登入重繪
    return;
  }

  container.innerHTML =
    '<div class="ga-login-prompt">' +
    '<span class="ga-login-icon">🏆</span>' +
    '<span class="ga-login-tip">' + _gaEscape(gaT('loginTip')) + '</span>' +
    '<span class="ga-login-actions">' +
    '<span id="' + containerId + 'Google" class="ga-google-btn"></span>' +
    '<a class="ga-line-btn" href="' + gaLineLoginUrl() + '">' + _gaEscape(gaT('lineBtn')) + '</a>' +
    '</span>' +
    '</div>';
  const googleBtn = document.getElementById(containerId + 'Google');
  if (typeof google !== 'undefined' && google.accounts) {
    _gaInitGoogleButton(googleBtn);
  } else {
    // Google SDK可能還沒載入完成，稍後再試一次
    window.addEventListener('load', function () { _gaInitGoogleButton(googleBtn); }, { once: true });
    setTimeout(function () { _gaInitGoogleButton(googleBtn); }, 1200);
  }
}

// ── 處理LINE登入導回：網址帶著 ?line_token=xxx 或 ?line_login=fail ──
function gaHandleLineCallbackToken() {
  const params = new URLSearchParams(location.search);
  const token = params.get('line_token');
  const fail = params.get('line_login');
  if (token) {
    gaSetToken(token);
    gaToast(gaT('lineLoginOk'));
    gaRenderAllWidgets(); // 2026/08/17補上：原本LINE登入導回沒重繪widget，登入卡片/提醒要等重新整理頁面才會消失
  } else if (fail === 'fail') {
    gaToast(gaT('lineLoginFail'));
  }
  if (token || fail) {
    params.delete('line_token');
    params.delete('line_login');
    const qs = params.toString();
    history.replaceState(null, '', location.pathname + (qs ? '?' + qs : ''));
  }
}

document.addEventListener('DOMContentLoaded', function () {
  gaHandleLineCallbackToken();
});

// ── 全螢幕放大遊戲區（2026/08/16 新增，帥哥鴻反饋想要玩遊戲時畫面能放大）──
// 找頁面上唯一的 .game-card，插入一顆全螢幕按鈕，點擊後用瀏覽器原生 Fullscreen API
// 把整張卡片（標題+盤面+分數+排行榜）放大到全螢幕，離開時自動還原。
// 7-3 防錯精神延伸：偵測不到 .game-card 或瀏覽器不支援 Fullscreen API 時安靜跳過，不影響遊戲本身。
function gaInitFullscreenToggle() {
  const card = document.querySelector('.game-card');
  if (!card) return;

  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'ga-fullscreen-btn';
  btn.setAttribute('aria-label', gaT('fsAria'));
  btn.innerHTML = _gaEscape(gaT('fsEnter'));
  card.insertBefore(btn, card.firstChild);

  function isFs() {
    const fsEl = document.fullscreenElement || document.webkitFullscreenElement;
    return fsEl === card;
  }
  function updateBtn() {
    btn.innerHTML = _gaEscape(isFs() ? gaT('fsExit') : gaT('fsEnter'));
  }
  function enter() {
    const req = card.requestFullscreen || card.webkitRequestFullscreen;
    if (!req) { gaToast(gaT('fsUnsupported')); return; }
    Promise.resolve(req.call(card)).catch(function () { gaToast(gaT('fsUnsupported')); });
  }
  function exit() {
    const ext = document.exitFullscreen || document.webkitExitFullscreen;
    if (ext) ext.call(document);
  }

  btn.addEventListener('click', function () { isFs() ? exit() : enter(); });
  document.addEventListener('fullscreenchange', updateBtn);
  document.addEventListener('webkitfullscreenchange', updateBtn);
}
window.gaInitFullscreenToggle = gaInitFullscreenToggle;

// ── 登入提醒：進場彈窗＋盤面常駐小提示（2026/08/17新增）──
// 帥哥鴻反饋：原本的登入提示卡片放在遊戲盤面「下方」，玩家常常沒捲頁面就開始玩，容易完全沒注意到。
// 新增兩層提醒，遵循既有「未登入完全不影響遊玩」原則（7-3防錯精神延伸），且不重寫送分/登入邏輯：
//   1. 進場彈窗：未登入時，一進頁面彈出一次，關掉（含點背景、按X、按「先不用」）後這次瀏覽
//      （sessionStorage，分頁關掉或跳出瀏覽器就重置）不會再彈，不會每次玩都打斷
//   2. 盤面常駐小提示：疊在遊戲盤面本身左上角（用跟全螢幕按鈕同一套 [id$="Board"]/.game-stage
//      屬性選擇器涵蓋全部有排行榜的遊戲），半透明徽章、pointer-events:none 完全不擋任何遊戲點擊，
//      登入前持續顯示、登入後（含LINE登入導回重繪）自動消失
let _gaReminderGameSlug = null; // 記住這次呼叫的遊戲slug，供登出後重新掛回盤面提示使用
function gaInitLoginReminder(gameSlug) {
  _gaReminderGameSlug = gameSlug;
  if (gaIsLoggedIn()) return; // 已登入什麼都不用做
  _gaShowEntryReminder(gameSlug);
  _gaMountBoardBadge();
}

function _gaShowEntryReminder(gameSlug) {
  if (gaIsLoggedIn() || document.getElementById('gaReminderOverlay')) return;
  let dismissed = false;
  try { dismissed = sessionStorage.getItem(GA_CONFIG.loginReminderDismissKey) === '1'; } catch (e) { /* 無痕模式等sessionStorage不可用時，直接視為沒關過，仍會彈一次 */ }
  if (dismissed) return;

  const gameName = gaGameName(gameSlug);
  const overlay = document.createElement('div');
  overlay.id = 'gaReminderOverlay';
  overlay.className = 'ga-reminder-overlay';
  overlay.innerHTML =
    '<div class="ga-reminder-modal">' +
    '<button type="button" class="ga-reminder-close" aria-label="' + _gaEscape(gaT('reminderClose')) + '">✕</button>' +
    '<div class="ga-reminder-icon">🏆</div>' +
    '<div class="ga-reminder-title">' + _gaEscape(gaT('reminderTitle', { game: gameName })) + '</div>' +
    '<div class="ga-reminder-sub">' + _gaEscape(gaT('reminderSub')) + '</div>' +
    '<div class="ga-reminder-actions">' +
    '<span id="gaReminderGoogle" class="ga-google-btn"></span>' +
    '<a class="ga-line-btn" href="' + gaLineLoginUrl() + '">' + _gaEscape(gaT('lineBtn')) + '</a>' +
    '</div>' +
    '<button type="button" class="ga-reminder-skip">' + _gaEscape(gaT('reminderSkip')) + '</button>' +
    '</div>';
  document.body.appendChild(overlay);

  function dismiss() {
    try { sessionStorage.setItem(GA_CONFIG.loginReminderDismissKey, '1'); } catch (e) {}
    overlay.remove();
  }
  overlay.querySelector('.ga-reminder-close').addEventListener('click', dismiss);
  overlay.querySelector('.ga-reminder-skip').addEventListener('click', dismiss);
  overlay.addEventListener('click', function (e) { if (e.target === overlay) dismiss(); }); // 點背景空白處也視為關閉

  const googleBtn = document.getElementById('gaReminderGoogle');
  if (typeof google !== 'undefined' && google.accounts) {
    _gaInitGoogleButton(googleBtn);
  } else {
    window.addEventListener('load', function () { _gaInitGoogleButton(googleBtn); }, { once: true });
    setTimeout(function () { _gaInitGoogleButton(googleBtn); }, 1200);
  }
}

function _gaMountBoardBadge() {
  if (gaIsLoggedIn() || document.getElementById('gaBoardBadge')) return;
  const board = document.querySelector('[id$="Board"], .game-stage');
  const host = board || document.querySelector('.game-card'); // 找不到盤面時退回整張卡片，不會整個掛載失敗
  if (!host) return;
  const badge = document.createElement('div');
  badge.id = 'gaBoardBadge';
  badge.className = 'ga-board-badge';
  badge.textContent = gaT('badge');
  host.appendChild(badge);
}

function _gaRemoveLoginReminders() {
  const overlay = document.getElementById('gaReminderOverlay');
  if (overlay) overlay.remove();
  const badge = document.getElementById('gaBoardBadge');
  if (badge) badge.remove();
}
window.gaInitLoginReminder = gaInitLoginReminder;
