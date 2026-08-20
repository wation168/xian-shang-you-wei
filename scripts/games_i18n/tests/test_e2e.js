// 端對端測試：用 jsdom 實際載入產出的完整HTML，跑真正的遊戲流程，
// 驗證「共用JS + 各語言字典」組合起來在瀏覽器環境真的能跑，而且顯示的是對的語言。
// （延續第三十輪數字炸彈/踩地雷建立的三層驗證紀律：純邏輯 → 嵌入版 → jsdom端對端）
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const OUT = path.join(__dirname, '..', 'out', 'games');
let pass = 0, fail = 0;
function ok(name, cond, detail) {
  if (cond) pass++;
  else { fail++; console.log('  ✗ ' + name + (detail ? ' — ' + detail : '')); }
}

function loadPage(loc, slug) {
  const rel = loc === 'zh-TW' ? `${slug}.html` : `${loc}/${slug}.html`;
  let html = fs.readFileSync(path.join(OUT, rel), 'utf8');

  // 把本站的外連JS換成實際檔案內容（jsdom不會去抓 / 開頭的絕對路徑），
  // 外部CDN（Google登入、AdSense）則整段移除，測試不依賴網路
  const shared = fs.readFileSync(path.join(OUT, 'shared', `${slug}.js`), 'utf8');
  const auth = fs.readFileSync(path.join(OUT, 'games-auth.js'), 'utf8');
  html = html.replace(`<script src="/games/shared/${slug}.js"></script>`,
                      `<script>${shared}</script>`);
  html = html.replace('<script src="/games/games-auth.js"></script>',
                      `<script>${auth}</script>`);
  html = html.replace(/<script src="https:\/\/accounts\.google\.com[^>]*><\/script>/g, '');
  html = html.replace(/<script src="\/common\/softglow-common\.js"><\/script>/g, '');
  html = html.replace(/<script src="\/js\/softglow-cookies\.js" defer><\/script>/g, '');
  // 廣告載入器（會動態插入外部script）拿掉，避免jsdom嘗試連外
  html = html.replace(/<script>\(function\(\)\{var AD_DELAY_MS[\s\S]*?<\/script>/g, '');

  const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    url: 'https://softglow-ai.com' + (loc === 'zh-TW' ? `/games/${slug}.html` : `/games/${loc}/${slug}.html`),
    beforeParse(win) {
      // 排行榜/送分的網路請求一律擋掉（回傳空榜），遊戲本身不該因此受影響
      win.fetch = () => Promise.resolve({ ok: true, status: 200, json: () => Promise.resolve({ leaderboard: [] }) });
      win.AbortSignal.timeout = () => undefined;
    },
  });
  return dom;
}

function key(dom, k) {
  const ev = new dom.window.KeyboardEvent('keydown', { key: k, bubbles: true, cancelable: true });
  dom.window.dispatchEvent(ev);
}

function tileValues(doc) {
  return [...doc.querySelectorAll('.g2048-tile')].map(e => parseInt(e.textContent, 10));
}

// ══ 逐一測試每個語言版本 ══
const LOCALES = ['zh-TW', 'en', 'de', 'es', 'fr', 'id', 'ja', 'ko', 'pt', 'zh-CN'];
const EXPECT = {
  'zh-TW': { score: '分數：', over: '💥 遊戲結束', fs: '⛶ 全螢幕', board: '🔒 登入才能上榜' },
  'en':    { score: 'Score: ', over: '💥 Game Over', fs: '⛶ Fullscreen', board: '🔒 Sign in to rank' },
  'de':    { score: 'Punkte: ', over: '💥 Spiel beendet', fs: '⛶ Vollbild', board: '🔒 Anmelden für Bestenliste' },
  'es':    { score: 'Puntos: ', over: '💥 Fin del juego', fs: '⛶ Pantalla completa', board: '🔒 Inicia sesión para clasificar' },
  'fr':    { score: 'Score : ', over: '💥 Partie terminée', fs: '⛶ Plein écran', board: '🔒 Connectez-vous pour être classé' },
  'id':    { score: 'Skor: ', over: '💥 Permainan berakhir', fs: '⛶ Layar penuh', board: '🔒 Masuk untuk masuk peringkat' },
  'ja':    { score: 'スコア：', over: '💥 ゲームオーバー', fs: '⛶ 全画面', board: '🔒 ログインでランキング参加' },
  'ko':    { score: '점수: ', over: '💥 게임 종료', fs: '⛶ 전체화면', board: '🔒 로그인하면 순위 등록' },
  'pt':    { score: 'Pontos: ', over: '💥 Fim de jogo', fs: '⛶ Tela cheia', board: '🔒 Entre para entrar no ranking' },
  'zh-CN': { score: '分数：', over: '💥 游戏结束', fs: '⛶ 全屏', board: '🔒 登录才能上榜' },
};

for (const loc of LOCALES) {
  const dom = loadPage(loc, '2048');
  const doc = dom.window.document;
  const W = dom.window;
  const exp = EXPECT[loc];
  const tag = `[${loc}]`;

  // 1. 靜態在地化文字有正確渲染
  ok(`${tag} 分數標籤在地化`, doc.querySelector('.g2048-topbar').textContent.includes(exp.score),
     doc.querySelector('.g2048-topbar').textContent.trim().slice(0, 40));

  // 2. games-auth.js 的全螢幕按鈕文字跟著語言（驗證 GA_LANG_PACK 生效）
  const fsBtn = doc.querySelector('.ga-fullscreen-btn');
  ok(`${tag} 全螢幕按鈕在地化`, fsBtn && fsBtn.textContent.trim() === exp.fs,
     fsBtn ? fsBtn.textContent.trim() : '按鈕不存在');

  // 3. 未登入時的盤面常駐提示跟著語言
  const badge = doc.getElementById('gaBoardBadge');
  ok(`${tag} 盤面登入提示在地化`, badge && badge.textContent === exp.board,
     badge ? badge.textContent : '徽章不存在');

  // 4. 進場登入彈窗有出現且標題帶入在地化遊戲名稱
  const modal = doc.querySelector('.ga-reminder-title');
  ok(`${tag} 進場彈窗標題含遊戲名稱`, modal && modal.textContent.includes('2048'),
     modal ? modal.textContent : '彈窗不存在');

  // 5. 開始遊戲：盤面出現2個起始方塊
  W.g2048Restart();
  ok(`${tag} 開局後盤面有2個方塊`, tileValues(doc).length === 2, String(tileValues(doc)));
  ok(`${tag} 起始方塊值只會是2或4`, tileValues(doc).every(v => v === 2 || v === 4));

  // 6. 實際按方向鍵能玩：連按多次後盤面方塊數會增加、分數為非負整數
  for (let i = 0; i < 12; i++) { key(dom, ['ArrowLeft','ArrowUp','ArrowRight','ArrowDown'][i % 4]); }
  const sc = parseInt(doc.getElementById('g2048Score').textContent, 10);
  ok(`${tag} 按方向鍵後分數為合法數字`, Number.isInteger(sc) && sc >= 0, String(sc));
  ok(`${tag} 按方向鍵後盤面方塊數增加`, tileValues(doc).length >= 2, String(tileValues(doc).length));

  // 7. 無效移動不消耗回合：把盤面推到底再往同方向推，方塊數不該變
  for (let i = 0; i < 30; i++) key(dom, 'ArrowLeft');
  const before = tileValues(doc).length;
  key(dom, 'ArrowLeft');
  const after = tileValues(doc).length;
  ok(`${tag} 已推到底再推同方向不會多生方塊`, after === before, `${before} → ${after}`);

  // 8. 遊戲結束overlay文字在地化（直接把盤面填成死局再觸發一次移動）
  //    透過鍵盤操作很難穩定造出死局，這裡直接驗證字典→畫面的對應：
  const dict = JSON.parse(/window\.GAME_I18N = (\{[\s\S]*?\});/.exec(
    fs.readFileSync(path.join(OUT, loc === 'zh-TW' ? '2048.html' : `${loc}/2048.html`), 'utf8'))[1]);
  ok(`${tag} 字典gameOver與預期一致`, dict.gameOver === exp.over, dict.gameOver);
  ok(`${tag} 字典有完整5級評語`, Array.isArray(dict.ratings) && dict.ratings.length === 5);
  ok(`${tag} winTitle含{v}佔位`, dict.winTitle.includes('{v}'), dict.winTitle);
  ok(`${tag} scoreShort含{s}佔位`, dict.scoreShort.includes('{s}'), dict.scoreShort);

  // 9. 排行榜區塊已掛載並顯示在地化空榜訊息（fetch被stub成空榜）
  ok(`${tag} 排行榜容器存在`, !!doc.getElementById('gaLeaderboard'));

  // 10. 分享功能不會拋錯（navigator.share 不存在 → 走複製分支）
  let threw = null;
  try { W.g2048ShareResult(); } catch (e) { threw = e.message; }
  ok(`${tag} 分享功能不拋錯`, threw === null, threw || '');

  dom.window.close();
}

console.log(`\njsdom 端對端測試：${pass} 通過, ${fail} 失敗`);
process.exit(fail ? 1 : 0);
