/* SoftGlow Cookie Manager v1.0
 * 功能：1.GDPR同意橫幅 2.語言偏好記憶 3.最近使用工具
 * 所有資料存在使用者瀏覽器 localStorage，不傳伺服器
 */
(function(){
"use strict";

// ── 1. Cookie 同意橫幅（GDPR）──────────────────────
var CONSENT_KEY = "sg_cookie_consent";
var CONSENT_TEXTS = {
  "zh-TW":{msg:"本站使用 Cookie 來提供更好的瀏覽體驗和個人化廣告。",yes:"同意",no:"拒絕",more:"了解更多"},
  "zh-CN":{msg:"本站使用 Cookie 来提供更好的浏览体验和个性化广告。",yes:"同意",no:"拒绝",more:"了解更多"},
  "en":{msg:"We use cookies to improve your experience and show personalized ads.",yes:"Accept",no:"Decline",more:"Learn more"},
  "ja":{msg:"より良い体験とパーソナライズ広告のためCookieを使用します。",yes:"同意",no:"拒否",more:"詳細"},
  "ko":{msg:"더 나은 경험과 맞춤 광고를 위해 쿠키를 사용합니다.",yes:"동의",no:"거부",more:"자세히"},
  "de":{msg:"Wir verwenden Cookies für ein besseres Erlebnis und personalisierte Werbung.",yes:"Akzeptieren",no:"Ablehnen",more:"Mehr erfahren"},
  "fr":{msg:"Nous utilisons des cookies pour améliorer votre expérience et afficher des publicités personnalisées.",yes:"Accepter",no:"Refuser",more:"En savoir plus"},
  "es":{msg:"Usamos cookies para mejorar tu experiencia y mostrar anuncios personalizados.",yes:"Aceptar",no:"Rechazar",more:"Más información"},
  "pt":{msg:"Usamos cookies para melhorar sua experiência e exibir anúncios personalizados.",yes:"Aceitar",no:"Recusar",more:"Saiba mais"},
  "id":{msg:"Kami menggunakan cookie untuk pengalaman lebih baik dan iklan yang dipersonalisasi.",yes:"Terima",no:"Tolak",more:"Pelajari"}
};

function getLang(){
  var html = document.documentElement;
  return (html.getAttribute("lang")||"en").replace(/_.*/,"");
}

function showConsentBanner(){
  if(localStorage.getItem(CONSENT_KEY)) return;
  var lang = getLang();
  var t = CONSENT_TEXTS[lang] || CONSENT_TEXTS["en"];

  var banner = document.createElement("div");
  banner.id = "sg-consent";
  banner.innerHTML = '<div class="sg-consent-inner">' +
    '<p>' + t.msg + ' <a href="/privacy.html">' + t.more + '</a></p>' +
    '<div class="sg-consent-btns">' +
    '<button class="sg-btn-yes" onclick="sgAcceptCookies()">' + t.yes + '</button>' +
    '<button class="sg-btn-no" onclick="sgDeclineCookies()">' + t.no + '</button>' +
    '</div></div>';
  document.body.appendChild(banner);
}

window.sgAcceptCookies = function(){
  localStorage.setItem(CONSENT_KEY, "accepted");
  var el = document.getElementById("sg-consent");
  if(el) el.remove();
  // 同意後載入 AdSense（如果還沒載入）
  if(!document.querySelector('script[src*="googlesyndication"]')){
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1768270548115739";
    s.crossOrigin = "anonymous";
    document.head.appendChild(s);
  }
};

window.sgDeclineCookies = function(){
  localStorage.setItem(CONSENT_KEY, "declined");
  var el = document.getElementById("sg-consent");
  if(el) el.remove();
};

// ── 2. 語言偏好記憶 ──────────────────────────
var LANG_KEY = "sg_preferred_lang";

function detectCurrentLang(){
  var path = window.location.pathname;
  // /tools/en/xxx.html → en
  var m = path.match(/\/tools\/([a-z]{2}(?:-[A-Z]{2})?)\//);
  if(m) return m[1];
  // /tools/xxx.html → zh-TW
  if(path.match(/^\/tools\/[^/]+\.html$/) || path === "/tools/") return "zh-TW";
  return null;
}

function saveLangPreference(){
  var lang = detectCurrentLang();
  if(lang) localStorage.setItem(LANG_KEY, lang);
}

function checkLangRedirect(){
  var saved = localStorage.getItem(LANG_KEY);
  if(!saved) return;
  var current = detectCurrentLang();
  if(!current || current === saved) return;

  // 只在索引頁自動跳轉（工具頁不跳，避免干擾 SEO）
  var path = window.location.pathname;
  var isIndex = (path === "/tools/" || path.match(/^\/tools\/[a-z]{2}(-[A-Z]{2})?\/?$/));
  if(!isIndex) return;

  var target;
  if(saved === "zh-TW"){
    target = "/tools/";
  } else {
    target = "/tools/" + saved + "/";
  }
  if(path !== target){
    window.location.replace(target);
  }
}

// 攔截語言切換點擊，儲存偏好
function hookLangLinks(){
  document.addEventListener("click", function(e){
    var a = e.target.closest("a.lang-btn");
    if(!a) return;
    var href = a.getAttribute("href") || "";
    var m = href.match(/\/tools\/([a-z]{2}(?:-[A-Z]{2})?)\//);
    if(m){
      localStorage.setItem(LANG_KEY, m[1]);
    } else if(href === "/tools/" || href.match(/^\/tools\/[^/]+\.html$/)){
      localStorage.setItem(LANG_KEY, "zh-TW");
    }
  });
}

// ── 3. 最近使用工具 ──────────────────────────
var RECENT_KEY = "sg_recent_tools";
var MAX_RECENT = 5;

function saveRecentTool(){
  var path = window.location.pathname;
  // 只在工具頁觸發（排除索引頁）
  var m = path.match(/\/tools\/(?:([a-z]{2}(?:-[A-Z]{2})?)\/)?([^/]+)\.html$/);
  if(!m) return;

  var lang = m[1] || "zh-TW";
  var slug = m[2];
  var h1 = document.querySelector("h1");
  var name = h1 ? h1.textContent.trim() : slug;

  var recent = [];
  try{ recent = JSON.parse(localStorage.getItem(RECENT_KEY)) || []; } catch(e){}

  // 移除重複
  recent = recent.filter(function(r){ return r.slug !== slug || r.lang !== lang; });
  // 加到最前面
  recent.unshift({slug: slug, name: name, lang: lang, time: Date.now()});
  // 限制數量
  if(recent.length > MAX_RECENT) recent = recent.slice(0, MAX_RECENT);

  localStorage.setItem(RECENT_KEY, JSON.stringify(recent));
}

function renderRecentTools(){
  var path = window.location.pathname;
  // 只在索引頁顯示
  var isIndex = (path === "/tools/" || path.match(/^\/tools\/[a-z]{2}(-[A-Z]{2})?\/?$/));
  if(!isIndex) return;

  var recent = [];
  try{ recent = JSON.parse(localStorage.getItem(RECENT_KEY)) || []; } catch(e){}
  if(recent.length === 0) return;

  var lang = detectCurrentLang() || "zh-TW";
  var titles = {
    "zh-TW":"🕐 最近使用","en":"🕐 Recently Used","ja":"🕐 最近使用",
    "ko":"🕐 최근 사용","de":"🕐 Zuletzt verwendet","fr":"🕐 Récemment utilisé",
    "es":"🕐 Usado recientemente","pt":"🕐 Usado recentemente",
    "id":"🕐 Baru digunakan","zh-CN":"🕐 最近使用"
  };

  var html = '<section class="tool-category" id="sg-recent" style="margin-bottom:32px">';
  html += '<h2 class="cat-title" style="color:#2563EB">' + (titles[lang]||titles["en"]) + '</h2>';
  html += '<div class="tool-grid">';

  for(var i = 0; i < recent.length; i++){
    var r = recent[i];
    var href;
    if(r.lang === "zh-TW"){
      href = "/tools/" + r.slug + ".html";
    } else {
      href = "/tools/" + r.lang + "/" + r.slug + ".html";
    }
    html += '<a href="' + href + '" class="tool-card" style="border-color:#BEE3F8;background:#EBF5FF">' + r.name + '</a>';
  }
  html += '</div></section>';

  // 插入到 .container 的最前面
  var container = document.querySelector(".container");
  if(container){
    var div = document.createElement("div");
    div.innerHTML = html;
    container.insertBefore(div.firstChild, container.firstChild);
  }
}

// ── 初始化 ──────────────────────────────
function init(){
  // Cookie 同意（GDPR）
  var consent = localStorage.getItem(CONSENT_KEY);
  if(!consent){
    showConsentBanner();
  } else if(consent === "accepted"){
    // 已同意，確保 AdSense 載入
    // （AdSense script 已在 HTML 中，不需額外處理）
  }
  // 如果拒絕，AdSense 不會被延遲載入腳本觸發

  // 語言偏好
  checkLangRedirect();
  saveLangPreference();
  hookLangLinks();

  // 最近使用工具
  saveRecentTool();
  renderRecentTools();
}

// DOM ready
if(document.readyState === "loading"){
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}

})();
