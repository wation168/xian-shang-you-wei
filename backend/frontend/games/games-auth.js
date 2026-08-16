// ══════════════════════════════════════════════════════════
// 遊戲排行榜共用模組（2026/08/15 新增）
// 帥哥鴻反饋「沒有比賽機制，可以設定登入加入比賽排名」——
// 沿用網站既有的會員登入系統（跟股票App共用同一個localStorage token），
// 不做另一套帳號系統。玩家用Google或LINE登入後，遊戲分數會記在他的
// 帳號名下，排行榜任何人都能看，不用登入也能玩遊戲（只是分數不會上榜）。
//
// 遵循《新工具規劃守則.md》第七節：
//   7-1 GA_CONFIG集中管理API位置/儲存key/顯示筆數等所有可調數值
//   7-2 純函式（gaFormatScore/gaMedal）跟DOM/fetch邏輯分開
//   7-3 防錯：未登入送分直接跳過並提示、API失敗不擋遊戲本身進行
//   7-4 資源清理：toast的setTimeout存id並可重複觸發不堆疊
// ══════════════════════════════════════════════════════════
const GA_CONFIG = {
  googleClientId: '584257110691-jtn1tf282q4vsfn7c7vhp9c12m6ino1n.apps.googleusercontent.com',
  tokenStorageKey: 'auth_token', // 跟 frontend/index.html 共用同一把 key，兩邊登入狀態互通
  leaderboardLimit: 20,
  toastMs: 2600,
  gameNames: {
    'reaction-time-test': '反應力測試',
    'memory-match': '記憶翻牌',
    'whack-a-mole': '打地鼠',
    'piano-tiles': '鋼琴塊',
    'snake': '貪食蛇'
  },
  scoreUnit: {
    'reaction-time-test': 'ms',
    'memory-match': '步',
    'whack-a-mole': '分',
    'piano-tiles': '分',
    'snake': '分'
  }
};

function gaGetAPI() {
  const isLocal = location.hostname === 'localhost' || location.hostname === '127.0.0.1' || location.hostname.startsWith('192.168');
  return isLocal ? 'http://localhost:8000' : 'https://api.softglow-ai.com';
}

// ── 純函式：不碰DOM ──
function gaFormatScore(gameSlug, score) {
  const unit = GA_CONFIG.scoreUnit[gameSlug] || '';
  return score + unit;
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
    gaToast('登入才能把成績送上排行榜 🏆');
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
      gaToast('🎉 新紀錄！目前排名第 ' + data.rank + ' 名');
    } else if (data.rank) {
      gaToast('已送上排行榜，目前排名第 ' + data.rank + ' 名');
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
    container.innerHTML = '<div class="ga-empty">還沒有人上榜，登入後第一個玩就能拿下第一名！</div>';
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
  container.innerHTML = '<div class="ga-empty">載入排行榜中…</div>';
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
    if (!res.ok) { gaToast(data.detail || 'Google 登入失敗'); return; }
    gaSetToken(data.token);
    gaToast('登入成功！');
    gaRenderAllWidgets();
  } catch (e) {
    gaToast('連線失敗，請稍後再試');
  }
}
function gaLineLoginUrl() {
  const returnUrl = location.pathname; // 登入完成後導回目前這個遊戲頁面
  return gaGetAPI() + '/auth/line?return_url=' + encodeURIComponent(returnUrl);
}
function gaLogout() {
  gaClearToken();
  gaToast('已登出');
  gaRenderAllWidgets();
}
window.gaLogout = gaLogout;

async function _gaFetchNickname() {
  try {
    const res = await fetch(gaGetAPI() + '/auth/me', { headers: gaAuthHeaders(), signal: AbortSignal.timeout(8000) });
    if (!res.ok) return null;
    const data = await res.json();
    return (data.nickname && data.nickname.trim()) || (data.email ? data.email.split('@')[0] : '玩家');
  } catch (e) {
    return null;
  }
}

const _gaWidgetContainers = []; // 記錄所有已掛載的登入widget容器id，登入狀態變化時統一重繪
function gaRenderAllWidgets() {
  _gaWidgetContainers.forEach(function (id) { gaMountAuthWidget(id); });
}

async function gaMountAuthWidget(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;
  if (_gaWidgetContainers.indexOf(containerId) === -1) _gaWidgetContainers.push(containerId);

  if (gaIsLoggedIn()) {
    container.innerHTML = '<div class="ga-logged-in">👤 <span id="' + containerId + 'Name">載入中…</span> <button class="ga-logout-btn" onclick="gaLogout()">登出</button></div>';
    const name = await _gaFetchNickname();
    const nameEl = document.getElementById(containerId + 'Name');
    if (nameEl) nameEl.textContent = name || '玩家';
    if (!name) { gaClearToken(); gaMountAuthWidget(containerId); } // token失效，視同未登入重繪
    return;
  }

  container.innerHTML =
    '<div class="ga-login-prompt">' +
    '<span class="ga-login-icon">🏆</span>' +
    '<span class="ga-login-tip">登入才能把成績存上排行榜，跟朋友比分數！</span>' +
    '<span class="ga-login-actions">' +
    '<span id="' + containerId + 'Google" class="ga-google-btn"></span>' +
    '<a class="ga-line-btn" href="' + gaLineLoginUrl() + '">💬 用LINE登入</a>' +
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
    gaToast('LINE登入成功！');
  } else if (fail === 'fail') {
    gaToast('LINE登入失敗，請再試一次');
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
// 把整張卡片（標題+盤面+分數+排行榜）放大到全螢幕，離開時自動還原，不用使用者自己按ESC以外的操作。
// 7-3 防錯精神延伸：偵測不到 .game-card 或瀏覽器不支援 Fullscreen API 時安靜跳過，不影響遊戲本身。
function gaInitFullscreenToggle() {
  const card = document.querySelector('.game-card');
  if (!card) return;

  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'ga-fullscreen-btn';
  btn.setAttribute('aria-label', '全螢幕放大遊戲');
  btn.innerHTML = '⛶ 全螢幕';
  card.insertBefore(btn, card.firstChild);

  function isFs() {
    const fsEl = document.fullscreenElement || document.webkitFullscreenElement;
    return fsEl === card;
  }
  function updateBtn() {
    btn.innerHTML = isFs() ? '✕ 離開全螢幕' : '⛶ 全螢幕';
  }
  function enter() {
    const req = card.requestFullscreen || card.webkitRequestFullscreen;
    if (!req) { gaToast('這個瀏覽器不支援全螢幕'); return; }
    Promise.resolve(req.call(card)).catch(function () { gaToast('這個瀏覽器不支援全螢幕'); });
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
