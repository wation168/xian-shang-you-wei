// 鋼琴塊 純邏輯回歸測試
//
// 核心邏輯有三塊：① 依旋律音符建出掉落磚塊資料（音名→固定欄位、拍長帶入）；
// ② 分數→評語等級、分數→Lv徽章數字的換算；③ 曲名改用 PT_CONFIG.songNames 內部代號
// 對應 window.GAME_I18N.songNames 同順序陣列取字（而不是直接把曲名寫死在SONGS資料裡）。
// 多語言重構把整段搬到 shared/piano-tiles.js，這裡驗證這些純函式沒有被改壞。
const fs = require('fs'), path = require('path'), vm = require('vm');
const code = fs.readFileSync(path.join(__dirname, '..', 'shared', 'piano-tiles.js'), 'utf8');
const ctx = { console, Math, Array, Object, String, Number, Infinity, Set, JSON, globalThis: null };
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(code + `
globalThis.__exp = { gpianotilesT, ptSongName, ptRatingIndex, ptComputeRating, ptComputeLevel,
  ptBuildSongTiles, PT_CONFIG, NOTE_FREQ, SONGS, SONG_TILES };`, ctx);
const X = ctx.__exp, C = X.PT_CONFIG;

let pass = 0, fail = 0;
const ok = (n, c, d) => { if (c) pass++; else { fail++; console.log('  ✗ ' + n + (d ? ' — ' + d : '')); } };

// ── PT_CONFIG.songNames 跟 SONGS 的曲目數必須一致（陣列長度必須對得上）──
ok('songNames 內部代號共4首，跟 SONGS 陣列長度一致', C.songNames.length === X.SONGS.length && C.songNames.length === 4);
ok('SONG_TILES 也是4首（跟 SONGS 一一對應）', X.SONG_TILES.length === 4);

// ── ptBuildSongTiles：每個音符轉出 {freq, col, dur}，欄位跟拍長要對得上原始資料 ──
(function () {
  const song = X.SONGS[0];
  const tiles = X.ptBuildSongTiles(song);
  ok('磚塊數跟音符數一致', tiles.length === song.notes.length);
  let durOk = true, freqOk = true;
  for (let i = 0; i < tiles.length; i++) {
    if (tiles[i].dur !== song.durs[i]) durOk = false;
    if (tiles[i].freq !== X.NOTE_FREQ[song.notes[i]]) freqOk = false;
  }
  ok('每個磚塊的拍長(dur)跟原始資料一一對應，順序未被打亂', durOk);
  ok('每個磚塊的頻率(freq)跟音名對應的NOTE_FREQ一致', freqOk);

  // 同一個音名永遠掉在同一欄（固定對應，不會同一首歌裡C4一下掉第0欄一下掉第3欄）
  const colOfNote = {};
  let stableCol = true;
  song.notes.forEach(function (n, i) {
    if (colOfNote[n] === undefined) colOfNote[n] = tiles[i].col;
    else if (colOfNote[n] !== tiles[i].col) stableCol = false;
  });
  ok('同一音名在整首歌裡固定掉同一欄', stableCol);

  // 欄位必須落在 [0, columns) 範圍內
  const colInRange = tiles.every(function (t) { return t.col >= 0 && t.col < C.columns; });
  ok('所有欄位都落在 [0, columns) 範圍內', colInRange);
})();

// 對4首歌都跑一次同樣的完整性檢查
(function () {
  let allOk = true;
  X.SONGS.forEach(function (song, idx) {
    const tiles = X.SONG_TILES[idx];
    if (tiles.length !== song.notes.length) allOk = false;
    tiles.forEach(function (t) {
      if (t.col < 0 || t.col >= C.columns) allOk = false;
      if (typeof t.freq !== 'number' || !(t.freq > 0)) allOk = false;
      if (typeof t.dur !== 'number' || !(t.dur > 0)) allOk = false;
    });
  });
  ok('4首歌的 SONG_TILES 皆完整（磚塊數對、欄位跟頻率都合法）', allOk);
})();

// ── ptSongName：讀 window.GAME_I18N.songNames[idx]，不是直接讀 SONGS 資料 ──
ctx.window = { GAME_I18N: { songNames: ['小星星', '瑪莉有隻小羊', '給愛麗絲', '卡農'] } };
ok('依index取翻譯後曲名', X.ptSongName(0) === '小星星' && X.ptSongName(3) === '卡農');
ok('索引越界回傳空字串不拋錯', X.ptSongName(99) === '');
ctx.window = {};
ok('字典不存在時曲名回傳空字串不拋錯', X.ptSongName(0) === '');
ok('SONGS 資料本身不含 name 欄位（曲名已改由 i18n 陣列提供）',
   X.SONGS.every(function (s) { return !('name' in s); }));

// ── ptRatingIndex / ptComputeRating：分數→評語等級（5級門檻） ──
ok('評分門檻共5級', C.ratingThresholds.length === 5);
ok('0分 → 第0級', X.ptRatingIndex(0) === 0);
ok('8分邊界含 → 第0級', X.ptRatingIndex(8) === 0);
ok('9分 → 第1級', X.ptRatingIndex(9) === 1);
ok('18分邊界含 → 第1級', X.ptRatingIndex(18) === 1);
ok('30分邊界含 → 第2級', X.ptRatingIndex(30) === 2);
ok('45分邊界含 → 第3級', X.ptRatingIndex(45) === 3);
ok('46分 → 第4級（最高，封頂）', X.ptRatingIndex(46) === 4);
ok('9999分 → 第4級（封頂不越界）', X.ptRatingIndex(9999) === 4);
(function () {
  let mono = true, prev = -1;
  for (let s = 0; s <= 100; s++) {
    const i = X.ptRatingIndex(s);
    if (i < prev) mono = false;
    prev = i;
  }
  ok('評分級數隨分數單調不遞減', mono);
})();
ctx.window = { GAME_I18N: { ratings: ['A', 'B', 'C', 'D', 'E'] } };
ok('依分數取對應評語文字', X.ptComputeRating(0) === 'A' && X.ptComputeRating(9999) === 'E');
ctx.window = {};
ok('字典不存在時評語回傳空字串不拋錯', X.ptComputeRating(0) === '');

// ── ptComputeLevel：分數→Lv徽章數字（每 scorePerLevel 分升一級，Lv從1起跳） ──
ok('scorePerLevel 設定為10', C.scorePerLevel === 10);
ok('0分 → Lv.1', X.ptComputeLevel(0) === 1);
ok('9分 → 仍是 Lv.1', X.ptComputeLevel(9) === 1);
ok('10分 → Lv.2', X.ptComputeLevel(10) === 2);
ok('25分 → Lv.3', X.ptComputeLevel(25) === 3);
(function () {
  let mono = true, prev = 0;
  for (let s = 0; s <= 200; s++) {
    const lv = X.ptComputeLevel(s);
    if (lv < prev) mono = false;
    prev = lv;
  }
  ok('等級隨分數單調不遞減', mono);
})();

// ── gpianotilesT：i18n取字helper ──
ctx.window = { GAME_I18N: { hello: '哈囉 {n} 次' } };
ok('取字並代換變數', X.gpianotilesT('hello', { n: 3 }) === '哈囉 3 次');
ok('缺key回傳空字串不拋錯', X.gpianotilesT('__nope__') === '');
ctx.window = {};
ok('字典不存在時不拋錯', X.gpianotilesT('hello') === '');

// ── 共用檔不得殘留硬寫死文字（排除註解），曲名等文字必須整段搬到i18n ──
(function () {
  const stripped = code.replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/[^\n]*/g, '');
  const cjk = stripped.match(/[一-鿿぀-ヿ가-힯]/g);
  ok('共用邏輯檔（排除註解）不含中日韓文字', cjk === null,
     cjk ? [...new Set(cjk)].join('').slice(0, 40) : '');
})();

console.log(`\n鋼琴塊 純邏輯回歸測試：${pass} 通過, ${fail} 失敗`);
process.exit(fail ? 1 : 0);
