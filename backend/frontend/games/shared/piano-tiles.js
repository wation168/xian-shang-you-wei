// ══════════════════════════════════════════════════════════
// 鋼琴塊 — 共用遊戲邏輯（所有語言版本共用這一份，多語言化時抽出）
//
// 【多語言架構約定】
//   這個檔案裡「不能出現任何給使用者看的文字」。所有文字一律透過 gpianotilesT('key') 讀取
//   頁面在載入這支JS之前先定義好的 window.GAME_I18N 字典。
//   曲名同理：JS只留 PT_CONFIG.songNames 這組內部代號（跟音符資料一一對應排序），
//   實際顯示的曲名文字從 window.GAME_I18N.songNames 同順序陣列取出。
//
// 遵循《新工具規劃守則.md》第七節：
//   7-1 PT_CONFIG集中管理欄數/初始速度/加速幅度/出現頻率等所有可調數值
//   7-2 純函式（ptComputeRating/ptComputeLevel）跟 requestAnimationFrame遊戲迴圈/DOM分開
//   7-3 防錯：遊戲結束後點擊不再計分、避免重複觸發game over
//   7-4 資源清理：rAF與spawn interval統一在clearAll()處理，離開頁面前清除
// ══════════════════════════════════════════════════════════
const PT_CONFIG = {
  columns: 5,
  initialSpeedPxPerSec: 160,
  maxSpeedPxPerSec: 620,
  speedIncreasePerHit: 10,
  initialBeatMs: 850,
  minBeatMs: 340,
  beatMsDecreasePerSpawn: 14,
  tileHeightPx: 90,
  historyLimit: 5,
  copyRevertMs: 1500,
  adLoadDelayMs: 2000,
  scorePerLevel: 10,
  sound: {
    enabled: true,
    volume: 0.16,
    noteDurationSec: 0.15,
    missFreqStart: 300,
    missFreqEnd: 70,
    missDurationSec: 0.35
  },
  // 只放門檻數字，對應的評語文字放在 GAME_I18N.ratings 同樣順序的陣列裡
  ratingThresholds: [8, 18, 30, 45, Infinity],
  // 4首曲子的內部代號，順序跟 SONGS 一一對應；顯示用的曲名文字從
  // window.GAME_I18N.songNames 同順序陣列取（陣列長度必須跟這裡一致，4個）
  songNames: ['twinkle', 'marylamb', 'furelise', 'canon']
};

// ── i18n 取字helper（7-3 防錯：缺key不崩潰）──
function gpianotilesT(key, vars) {
  const dict = (typeof window !== 'undefined' && window.GAME_I18N) || {};
  let s = dict[key];
  if (typeof s !== 'string') {
    if (typeof console !== 'undefined' && console.warn) console.warn('[piano-tiles] missing i18n key: ' + key);
    return '';
  }
  if (vars) {
    Object.keys(vars).forEach(function (k) {
      s = s.split('{' + k + '}').join(String(vars[k]));
    });
  }
  return s;
}
// 純函式：依index取曲名文字（防錯：字典缺陣列或索引越界回傳空字串）
function ptSongName(idx) {
  const list = (typeof window !== 'undefined' && window.GAME_I18N && window.GAME_I18N.songNames) || [];
  return list[idx] || '';
}

// ── 純函式：不碰DOM，只操作資料，也不含任何文字 ──
function ptRatingIndex(score) {
  const th = PT_CONFIG.ratingThresholds;
  for (let i = 0; i < th.length; i++) if (score <= th[i]) return i;
  return th.length - 1;
}
function ptComputeRating(score) {
  const list = (typeof window !== 'undefined' && window.GAME_I18N && window.GAME_I18N.ratings) || [];
  return list[ptRatingIndex(score)] || '';
}
function ptComputeLevel(score) {
  return 1 + Math.floor(score / PT_CONFIG.scorePerLevel);
}

// 2026/08/16新增：黑塊依照真實世界名曲的音符順序掉落，玩家依序點對就會彈出正確旋律。
// 四首曲子輪流播放，皆為公版民謠或古典名曲（貝多芬、帕海貝爾），沒有版權疑慮。
// NOTE_FREQ：十二平均律音名對應頻率（A4=440Hz為基準，公式 440*2^(n/12)）
const NOTE_FREQ = {
  C3: 130.81, D3: 146.83, E3: 164.81, 'F#3': 185.00, G3: 196.00, A3: 220.00, B3: 246.94,
  C4: 261.63, 'C#4': 277.18, D4: 293.66, 'D#4': 311.13, E4: 329.63, F4: 349.23, 'F#4': 369.99,
  G4: 392.00, 'G#4': 415.30, A4: 440.00, 'A#4': 466.16, B4: 493.88,
  C5: 523.25, 'C#5': 554.37, D5: 587.33, 'D#5': 622.25, E5: 659.25, F5: 698.46, 'F#5': 739.99,
  G5: 783.99, 'G#5': 830.61, A5: 880.00
};
// 每個音符的相對拍長（1=一拍，2=兩拍...），掉落間隔跟音效播放長度都依照這個比例調整，
// 節奏感才會接近真正的旋律。順序跟 PT_CONFIG.songNames 一一對應。
const SONGS = [
  { notes: ['C4','C4','G4','G4','A4','A4','G4','F4','F4','E4','E4','D4','D4','C4','G4','G4','F4','F4','E4','E4','D4','G4','G4','F4','F4','E4','E4','D4','C4','C4','G4','G4','A4','A4','G4','F4','F4','E4','E4','D4','D4','C4'],
    durs:  [1,1,1,1,1,1,2, 1,1,1,1,1,1,2, 1,1,1,1,1,1,2, 1,1,1,1,1,1,2, 1,1,1,1,1,1,2, 1,1,1,1,1,1,2] },
  { notes: ['E4','D4','C4','D4','E4','E4','E4','D4','D4','D4','E4','G4','G4','E4','D4','C4','D4','E4','E4','E4','E4','D4','D4','E4','D4','C4'],
    durs:  [1,1,1,1, 1,1,2, 1,1,2, 1,1,2, 1,1,1,1, 1,1,1,1, 1,1,1,1, 4] },
  { notes: ['E5','D#5','E5','D#5','E5','B4','D5','C5','A4','C4','E4','A4','B4','E4','G#4','B4','C5'],
    durs:  [1,1,1,1,1,1,1,1, 2, 1,1,1, 2, 1,1,1, 2] },
  { notes: ['D3','A3','B3','F#3','G3','D3','G3','A3','D3','A3','B3','F#3','G3','D3','G3','A3'],
    durs:  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] }
];
// 把每首歌的音符轉成「音名固定對應欄位」（同一音永遠掉同一欄，像真的琴鍵位置），
// 依照該曲用到的音高由低到高排序後，用 %欄數 分配，讓琴鍵感覺合理不會太集中在單欄。
// dur（相對拍長）原樣帶進tile資料，供掉落間隔跟播放長度使用。
function ptBuildSongTiles(song) {
  const distinct = Array.from(new Set(song.notes)).sort(function (a, b) { return NOTE_FREQ[a] - NOTE_FREQ[b]; });
  const colOf = {};
  distinct.forEach(function (n, i) { colOf[n] = i % PT_CONFIG.columns; });
  return song.notes.map(function (n, i) { return { freq: NOTE_FREQ[n], col: colOf[n], dur: song.durs[i] }; });
}
const SONG_TILES = SONGS.map(ptBuildSongTiles);

// ── 音效：Web Audio API 合成音，不需外部音檔（7-3 防錯：播放失敗不影響遊戲本身） ──
let ptAudioCtx = null;
let ptSoundOn = true;
function ptGetAudioCtx() {
  if (!PT_CONFIG.sound.enabled) return null;
  if (!ptAudioCtx) {
    try { ptAudioCtx = new (window.AudioContext || window.webkitAudioContext)(); }
    catch (e) { ptAudioCtx = null; }
  }
  if (ptAudioCtx && ptAudioCtx.state === 'suspended') { ptAudioCtx.resume().catch(function () {}); }
  return ptAudioCtx;
}
function ptPlayTone(freq, durationSec) {
  if (!ptSoundOn) return;
  const ctx = ptGetAudioCtx();
  if (!ctx) return;
  try {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.value = freq;
    gain.gain.setValueAtTime(PT_CONFIG.sound.volume, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + durationSec);
    osc.connect(gain).connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + durationSec);
  } catch (e) { /* 音效失敗不應中斷遊戲 */ }
}
function ptPlayMissSound() {
  if (!ptSoundOn) return;
  const ctx = ptGetAudioCtx();
  if (!ctx) return;
  try {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(PT_CONFIG.sound.missFreqStart, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(PT_CONFIG.sound.missFreqEnd, ctx.currentTime + PT_CONFIG.sound.missDurationSec);
    gain.gain.setValueAtTime(PT_CONFIG.sound.volume, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + PT_CONFIG.sound.missDurationSec);
    osc.connect(gain).connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + PT_CONFIG.sound.missDurationSec);
  } catch (e) { /* 音效失敗不應中斷遊戲 */ }
}
if (typeof window !== 'undefined') {
  window.ptToggleSound = function () {
    ptSoundOn = !ptSoundOn;
    const btn = document.getElementById('ptSoundBtn');
    if (btn) btn.textContent = ptSoundOn ? gpianotilesT('soundOnBtn') : gpianotilesT('soundOffBtn');
    if (ptSoundOn) ptGetAudioCtx();
  };
}

(function () {
  if (typeof document === 'undefined') return; // 純邏輯測試環境（無DOM）時安靜跳過UI部分

  const board     = document.getElementById('ptBoard');
  if (!board) return; // 7-3 防錯：頁面結構不符時不炸掉整頁
  const cols      = Array.from(board.querySelectorAll('.pt-col'));
  const overlay   = document.getElementById('ptOverlay');
  const overTitle = document.getElementById('ptOverTitle');
  const overSub   = document.getElementById('ptOverSub');
  const scoreEl   = document.getElementById('ptScore');
  const ratingEl  = document.getElementById('ptRating');
  const bestEl    = document.getElementById('ptBest');
  const historyEl = document.getElementById('ptHistory');
  const startBtn  = document.getElementById('ptStartBtn');
  const levelEl   = document.getElementById('ptLevelBadge');
  const songNameEl = document.getElementById('ptSongName');

  let playing = false;
  let score = 0;
  let level = 1;
  let speedPxPerSec = PT_CONFIG.initialSpeedPxPerSec;
  let beatMs = PT_CONFIG.initialBeatMs; // 一拍（dur=1音符）的間隔，實際掉落間隔＝beatMs×該音符的dur
  let tiles = [];
  let tileSeq = 0;
  let rafId = null;
  let spawnTimerId = null;
  let lastTs = 0;
  let history = [];
  // 目前演奏到第幾首曲子、曲子裡第幾個音符（曲子放完自動接下一首，循環播放）
  let songIndex = 0;
  let noteIndex = 0;

  function clearAll() {
    if (rafId) { cancelAnimationFrame(rafId); rafId = null; }
    if (spawnTimerId) { clearTimeout(spawnTimerId); spawnTimerId = null; }
    tiles.forEach(function (t) { if (t.el && t.el.parentNode) t.el.parentNode.removeChild(t.el); });
    tiles = [];
  }

  function nextSongNote() {
    const tilesForSong = SONG_TILES[songIndex];
    const note = tilesForSong[noteIndex];
    noteIndex++;
    if (noteIndex >= tilesForSong.length) {
      noteIndex = 0;
      songIndex = (songIndex + 1) % SONGS.length;
      if (songNameEl) songNameEl.textContent = ptSongName(songIndex);
    }
    return note;
  }

  function spawnTile() {
    if (!playing) return;
    const note = nextSongNote();
    const col = note.col;
    const el = document.createElement('div');
    el.className = 'pt-tile';
    el.style.height = PT_CONFIG.tileHeightPx + 'px';
    el.style.top = (-PT_CONFIG.tileHeightPx) + 'px';
    const id = tileSeq++;
    cols[col].appendChild(el);
    tiles.push({ id: id, col: col, el: el, topPx: -PT_CONFIG.tileHeightPx, freq: note.freq, dur: note.dur });

    beatMs = Math.max(PT_CONFIG.minBeatMs, beatMs - PT_CONFIG.beatMsDecreasePerSpawn);
    // 下一顆塊出現的間隔，依這顆音符的拍長（dur）等比例延長/縮短，而不是每顆塊都固定同一個
    // 間隔，這樣掉落節奏才會貼近真實曲子的長短音，旋律才聽得出來。
    spawnTimerId = setTimeout(spawnTile, beatMs * note.dur);
  }

  function removeTile(t) {
    const idx = tiles.indexOf(t);
    if (idx !== -1) tiles.splice(idx, 1);
    if (t.el && t.el.parentNode) t.el.parentNode.removeChild(t.el);
  }

  // 靈敏度修正：整個直排都是感應區，不再要求點在小方塊的精確像素範圍內。
  // 一欄內若同時有多顆方塊，優先消掉最接近底部（最緊急）的那顆，符合玩家直覺。
  function onColumnHit(col) {
    if (!playing) return;
    const candidates = tiles.filter(function (t) { return t.col === col; });
    if (!candidates.length) return; // 7-3 防錯：該欄目前沒有方塊，點擊不計分也不報錯
    candidates.sort(function (a, b) { return b.topPx - a.topPx; });
    const t = candidates[0];
    removeTile(t);
    score++;
    scoreEl.textContent = String(score);
    const newLevel = ptComputeLevel(score);
    if (newLevel !== level) {
      level = newLevel;
      levelEl.textContent = 'Lv.' + level;
      levelEl.classList.remove('pt-level-up');
      void levelEl.offsetWidth;
      levelEl.classList.add('pt-level-up');
    }
    speedPxPerSec = Math.min(PT_CONFIG.maxSpeedPxPerSec, speedPxPerSec + PT_CONFIG.speedIncreasePerHit);
    ptPlayTone(t.freq, PT_CONFIG.sound.noteDurationSec * t.dur);
  }

  cols.forEach(function (colEl, colIndex) {
    colEl.addEventListener('pointerdown', function (e) {
      e.preventDefault();
      onColumnHit(colIndex);
    });
  });

  function loop(ts) {
    if (!playing) return;
    if (!lastTs) lastTs = ts;
    const dtSec = (ts - lastTs) / 1000;
    lastTs = ts;
    const boardHeight = board.clientHeight;

    for (let i = tiles.length - 1; i >= 0; i--) {
      const t = tiles[i];
      t.topPx += speedPxPerSec * dtSec;
      t.el.style.top = t.topPx + 'px';
      if (t.topPx >= boardHeight) {
        endGame();
        return;
      }
    }
    rafId = requestAnimationFrame(loop);
  }

  function endGame() {
    playing = false;
    clearAll();
    ptPlayMissSound();
    startBtn.disabled = false;
    startBtn.textContent = gpianotilesT('playAgainBtn');
    overTitle.textContent = gpianotilesT('missTitle');
    overSub.textContent = gpianotilesT('scoreLine', { s: score });
    overlay.classList.add('show');
    ratingEl.textContent = gpianotilesT('scoreShort', { s: score }) + ' — ' + ptComputeRating(score);

    history.unshift(score);
    history = history.slice(0, PT_CONFIG.historyLimit);
    const best = Math.max(...history);
    bestEl.textContent = gpianotilesT('scoreShort', { s: best });
    historyEl.innerHTML = history.map(function (v) { return '<span>' + gpianotilesT('scoreShort', { s: v }) + '</span>'; }).join('');
    window._ptLastScore = score;
    window._ptBestScore = best;
    if (typeof gaSubmitScore === 'function') gaSubmitScore('piano-tiles', score);
  }

  function ptStartInternal() {
    clearAll();
    ptGetAudioCtx(); // 在使用者手勢（點擊開始）當下解鎖/建立AudioContext，符合瀏覽器自動播放政策
    overlay.classList.remove('show');
    playing = true;
    score = 0;
    level = 1;
    speedPxPerSec = PT_CONFIG.initialSpeedPxPerSec;
    beatMs = PT_CONFIG.initialBeatMs;
    lastTs = 0;
    // 每局隨機挑一首曲子開始演奏（從頭彈起），彈完自動接下一首並循環
    songIndex = Math.floor(Math.random() * SONGS.length);
    noteIndex = 0;
    if (songNameEl) songNameEl.textContent = ptSongName(songIndex);
    scoreEl.textContent = '0';
    levelEl.textContent = 'Lv.1';
    ratingEl.textContent = '';
    startBtn.disabled = true;
    startBtn.textContent = gpianotilesT('playingBtn');

    spawnTimerId = setTimeout(spawnTile, beatMs);
    rafId = requestAnimationFrame(loop);
  }

  window.ptStart = ptStartInternal;

  // 7-4 資源清理：離開頁面前清掉 rAF 與計時器
  window.addEventListener('beforeunload', clearAll);
})();

function ptShareResult() {
  const score = window._ptLastScore;
  const text = (score != null)
    ? gpianotilesT('shareWithScore', { s: score })
    : gpianotilesT('shareNoScore');
  if (navigator.share) {
    navigator.share({ title: document.title, text: text, url: location.href }).catch(function () {});
  } else {
    if (!navigator.clipboard || !navigator.clipboard.writeText) return;
    navigator.clipboard.writeText(text + ' ' + location.href);
    const b = event.target;
    const old = b.textContent;
    b.textContent = gpianotilesT('copied');
    setTimeout(function () { b.textContent = old; }, PT_CONFIG.copyRevertMs);
  }
}
// FAQ 展開收合（7-3 防錯：純邏輯測試環境沒有 document 時安靜跳過）
if (typeof document !== 'undefined') {
  document.querySelectorAll('.faq-q').forEach(function (q) {
    q.addEventListener('click', function () { this.parentElement.classList.toggle('open'); });
  });
}
