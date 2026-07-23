/**
 * lottery-live.js — 動態載入最新開獎號碼
 * 從 /lottery/data/{slug}.json 讀取，更新頁面上的開獎結果
 * 放在 frontend/js/lottery-live.js
 */
(function(){
  'use strict';

  // Detect lottery slug from URL or page
  var path = window.location.pathname;
  var match = path.match(/\/lottery\/(?:[a-z]{2}(?:-[A-Z]{2})?\/)?([a-z0-9-]+?)(?:-(results|history|statistics))?\.html/);
  if (!match) return;

  var slug = match[1];
  var pageType = match[2] || 'intro';

  // Skip tool pages
  var tools = ['ai-pick','bazi-pick','birthday-pick','chinese-zodiac-pick','cold-pick',
    'divination-pick','dream-pick','hot-pick','life-event-pick','lucky-number',
    'number-generator','random-pick','zodiac-pick'];
  if (tools.indexOf(slug) !== -1) return;

  // Fetch JSON data
  var jsonUrl = '/lottery/data/' + slug + '.json';
  fetch(jsonUrl)
    .then(function(r){ return r.ok ? r.json() : Promise.reject('not found'); })
    .then(function(draws){
      if (!draws || !draws.length) return;

      // Update latest draws on intro and results pages
      if (pageType === 'intro' || pageType === 'results') {
        updateDrawCards(draws, pageType);
      }
      
      // Update lottery card dates on index pages
      updateIndexDates(slug, draws[0]);
    })
    .catch(function(e){
      // Silently fail — page keeps static content
    });

  function ballHTML(num, isBonus) {
    var cls = isBonus ? 'ball ball-bonus' : 'ball ball-main';
    return '<span class="' + cls + '">' + num + '</span>';
  }

  function drawHTML(draw, isLatest, labels) {
    var cls = isLatest ? 'draw-card latest' : 'draw-card';
    var label = isLatest ? '<span class="draw-label">' + (labels.latest || 'Latest') + '</span>' : '';
    
    var balls = '';
    var nums = draw.numbers || draw.n || [];
    var bonus = draw.bonus || draw.b || [];
    
    for (var i = 0; i < nums.length; i++) {
      balls += ballHTML(nums[i], false);
    }
    if (bonus.length > 0) {
      balls += '<span class="draw-plus">+</span>';
      for (var j = 0; j < bonus.length; j++) {
        balls += ballHTML(bonus[j], true);
      }
    }

    var date = draw.date || draw.d || '';
    return '<div class="' + cls + '">' + label +
      '<div class="draw-date">' + date + '</div>' +
      '<div class="draw-nums">' + balls + '</div></div>';
  }

  function updateDrawCards(draws, type) {
    // Find the card containing draw-card elements
    var cards = document.querySelectorAll('.draw-card');
    if (!cards.length) return;

    // Get the parent container
    var container = cards[0].parentElement;
    if (!container) return;

    // Detect language for labels
    var html = document.documentElement.lang || 'en';
    var labels = { latest: 'Latest Winning Numbers' };
    if (html.indexOf('zh') === 0) labels.latest = '最新開獎號碼';
    if (html === 'ja') labels.latest = '最新当選番号';
    if (html === 'ko') labels.latest = '최신 당첨번호';
    if (html === 'de') labels.latest = 'Neueste Ziehung';
    if (html === 'fr') labels.latest = 'Derniers résultats';
    if (html === 'es') labels.latest = 'Últimos resultados';
    if (html === 'pt') labels.latest = 'Últimos resultados';
    if (html === 'id') labels.latest = 'Hasil terbaru';

    // Remove existing draw cards
    var existing = container.querySelectorAll('.draw-card');
    for (var i = existing.length - 1; i >= 0; i--) {
      existing[i].remove();
    }
    // Also remove "no data" message
    var nodata = container.querySelector('p[style*="A0AEC0"]');
    if (nodata) nodata.remove();

    // Insert new draws
    var count = type === 'results' ? Math.min(draws.length, 20) : Math.min(draws.length, 3);
    var firstChild = container.querySelector('.draw-label, div[style*="margin-top"]');
    var insertBefore = container.querySelector('div[style*="margin-top:16px"]');
    
    var fragment = document.createDocumentFragment();
    var tempDiv = document.createElement('div');
    
    for (var k = 0; k < count; k++) {
      tempDiv.innerHTML = drawHTML(draws[k], k === 0, labels);
      fragment.appendChild(tempDiv.firstChild);
    }
    
    if (insertBefore) {
      container.insertBefore(fragment, insertBefore);
    } else {
      container.appendChild(fragment);
    }
  }

  function updateIndexDates(slug, latestDraw) {
    // Update date on index page lottery cards
    var cards = document.querySelectorAll('.lottery-card');
    for (var i = 0; i < cards.length; i++) {
      var href = cards[i].getAttribute('href') || '';
      if (href.indexOf(slug + '.html') !== -1) {
        var meta = cards[i].querySelector('.lc-meta');
        if (meta && latestDraw.date) {
          var text = meta.textContent;
          // Replace date portion (after last · )
          var dotIdx = text.lastIndexOf('·');
          if (dotIdx !== -1) {
            meta.textContent = text.substring(0, dotIdx + 1) + ' ' + latestDraw.date;
          }
        }
      }
    }
  }
})();
