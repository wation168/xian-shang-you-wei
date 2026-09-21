/* AI Search & Website Intelligence — Phase 3 product shell
   Uses real Scanner export JSON (disposition / understanding / issues).
*/
(function () {
  const DEMOS = [
    { key: "django", label: "示範：部落格網站", url: "https://www.djangoproject.com/weblog/" },
    { key: "tutorial", label: "示範：教學網站", url: "https://docs.python.org/3/tutorial/" },
    { key: "patterns", label: "示範：大型內容站", url: "https://example.com/patterns" },
  ];

  const SCAN_STEPS = [
    "網站解析",
    "Website Understanding",
    "Technical Scan",
    "Content Understanding",
    "Search Analysis",
    "AI Analysis",
  ];

  const state = {
    data: null,
    view: "landing",
    detail: null,
  };

  const $ = (id) => document.getElementById(id);

  function show(view) {
    state.view = view;
    ["landing", "scan", "dash"].forEach((v) => {
      const el = $("view-" + v);
      if (el) el.classList.toggle("hidden", v !== view);
    });
  }

  function plainIssue(issue) {
    const ev = issue.evidence || {};
    const d = ev.disposition || "needs_review";
    const problem = issue.problem || "";
    const cat = issue.category || "";

    // Human titles
    let title = problem;
    let why = issue.cause || "";
    let should = "建議先看證據再決定。不是每個紅燈都要立刻改。";
    let how = issue.fix || "打開詳細證據，對照頁面後再改。";

    if (cat === "similarity" || ev.cluster) {
      title = "有一群頁面長得很像";
      why = "我們發現多個頁面共用類似版型或內容結構，獨特內容可能偏少。";
      should = d === "true_issue" ? "值得優先處理：先確認這群頁面是否該差異化。" : "可先觀察，不一定是錯誤。";
      how = "檢查模板與正文差異；必要時補強每頁獨特說明。";
    } else if (ev.url_evidence || (issue.id || "").startsWith("url-")) {
      title = "有些內部連結目標，目前還不能確認";
      why = "掃描集合裡找不到對應頁面；若尚未做 HTTP 探測，這不代表一定是 404。";
      should = "先不要當搬站錯誤硬改；補 HTTP／sitemap 證據後再判。";
      how = "用 URL Evidence（HTTP／redirect／sitemap）確認後再修連結。";
    } else if (cat === "i18n" || /hreflang|語系|語言/i.test(problem)) {
      title = "多語言頁面可能沒有正確互相連結";
      why = why || "我們發現語系標記或缺漏，可能影響搜尋理解語言版本。";
      should = d === "likely_exception" ? "若網站其實是單語，通常不必硬加全套 hreflang。" : "若你確實有多語版本，建議核對互相連結。";
      how = how || "補齊或修正 hreflang／語系頁對應。";
    } else if (cat === "meta") {
      title = "頁面標題或摘要可能不夠清楚";
      why = why || "標題／描述重複或過短，使用者與搜尋可能較難分辨頁面。";
      should = "若頁面目的不同，建議差異化；若本來就該相同，可略過。";
      how = how || "依頁面目的改寫 title／meta description。";
    } else if (cat === "links" && ev.link_opportunity) {
      title = "可能有值得加強的內連機會";
      why = why || "兩頁內容相關，但彼此可能還沒有自然連結。";
      should = ev.archive_date_demoted ? "年份／目錄頁通常不必互連。" : "有主題關聯再加；沒有就略過。";
      how = how || "在相關區塊加入自然錨點連結。";
    }

    return { title, why, should, how, disposition: d, priority: issue.priority || "P3", raw: issue };
  }

  function counts(data) {
    const s = data.summary || {};
    const dc = s.disposition_counts || {};
    const rb = s.review_buckets || {};
    const und = s.site_understanding || {};
    const shell = und.template_shell_sketch || {};
    const ue = s.url_evidence_summary || {};
    const trueN = rb.critical_true_issue != null ? rb.critical_true_issue : (dc.true_issue || 0);
    return {
      trueN,
      review: dc.needs_review || 0,
      exc: dc.likely_exception || 0,
      insuff: dc.insufficient_evidence || 0,
      pages: s.page_count || (data.pages || []).length,
      unique: shell.mean_unique_ratio,
      urlChains: (ue.url_evidence_chain || {}).chain_count || 0,
      http404: (ue.url_evidence_chain || {}).confirmed_http_404_or_410 || 0,
      httpMode: ue.http_live ? "live" : (ue.http_fixture_loaded ? "fixture" : "offline"),
      langs: ((und.languages || {}).distinct_langs) || Object.keys(((und.languages || {}).lang_counts) || {}).length || 1,
      pageTypes: und.page_type_histogram || {},
    };
  }

  function pickDemoKey(url) {
    const u = (url || "").toLowerCase();
    if (u.includes("django")) return "django";
    if (u.includes("python") || u.includes("docs.python")) return "tutorial";
    if (u.includes("pattern")) return "patterns";
    return "django";
  }

  async function loadDemo(key) {
    const res = await fetch("./data/" + key + ".json", { cache: "no-store" });
    if (!res.ok) throw new Error("無法載入 demo：" + key);
    return res.json();
  }

  function renderScanSteps(activeIdx) {
    const box = $("scan-steps");
    box.innerHTML = SCAN_STEPS.map((label, i) => {
      const cls = i < activeIdx ? "step done" : i === activeIdx ? "step active" : "step";
      const mark = i < activeIdx ? "✓" : i === activeIdx ? "●" : "○";
      // Show friendly labels only
      const friendly = [
        "讀取網站結構",
        "理解網站長什麼樣子",
        "檢查技術健康",
        "理解內容與頁面目的",
        "評估搜尋可見度",
        "評估 AI 可見度（未測量則誠實標示）",
      ][i];
      return `<div class="${cls}"><span class="i">${mark}</span><span>${friendly}</span></div>`;
    }).join("");
  }

  function runScanAnimation(url) {
    return new Promise((resolve) => {
      show("scan");
      $("scan-url-label").textContent = "目標：" + url;
      let i = 0;
      renderScanSteps(0);
      const timer = setInterval(() => {
        i += 1;
        if (i >= SCAN_STEPS.length) {
          clearInterval(timer);
          renderScanSteps(SCAN_STEPS.length);
          setTimeout(resolve, 450);
          return;
        }
        renderScanSteps(i);
      }, 700);
    });
  }

  function pillarCards(c) {
    const aiTier = "unmeasured";
    const searchMetric = c.trueN === 0 ? "目前沒有急件" : "有 " + c.trueN + " 件建議先看";
    const webMetric = "掃了 " + c.pages + " 頁";
    const contentMetric = c.unique != null ? (c.unique >= 0.5 ? "內容差異還可以" : "很多頁長得很像") : "尚無摘要";
    return [
      {
        id: "search",
        kicker: "搜尋",
        name: "別人搜得到嗎？",
        blurb: "Google 這類搜尋，能不能正確讀懂你的網站。",
        metric: searchMetric,
        metricSmall: "點進去看要不要改",
      },
      {
        id: "ai",
        kicker: "AI",
        name: "AI 提得到你嗎？",
        blurb: "ChatGPT 等會不會提到你——這版還沒實測，所以誠實寫「尚未測量」。",
        metric: "尚未測量",
        metricSmall: "不會給假分數",
        tier: aiTier,
      },
      {
        id: "website",
        kicker: "網站",
        name: "網站健不健康？",
        blurb: "結構、連結、技術基礎有沒有明顯問題。",
        metric: webMetric,
        metricSmall: "先看地圖與注意事項",
      },
      {
        id: "content",
        kicker: "內容",
        name: "內容清不清楚？",
        blurb: "頁面是不是講清楚、會不會彼此太像。",
        metric: contentMetric,
        metricSmall: "點進去看像哪幾頁",
      },
    ];
  }

  
  function renderResultHero() {
    const el = document.getElementById("result-hero");
    if (!el) return;
    const c = counts(state.data);
    const top = topPlainIssues(1)[0];
    let verdict;
    if (c.trueN === 0) {
      verdict = "整體看起來沒有「必須立刻處理」的急件。你可以先逛四個區塊，了解網站現況。";
    } else {
      verdict = "目前有 " + c.trueN + " 件比較值得先看的事。先不要被其他數字嚇到——從下面第一件開始即可。";
    }
    const next = top
      ? ("下一步建議：先看「" + top.title + "」。")
      : "下一步建議：點「網站健不健康？」看結構地圖。";
    el.className = "glass panel result-hero";
    const offlineNote = (c.httpMode === "offline")
      ? ('<div class="muted" style="margin-top:8px">補充：這次沒有連線檢查網址是否真的打不開，所以「找不到頁面」先當成「證據還不夠」，不是直接宣判 404。</div>')
      : "";
    el.innerHTML = "<h3>用一句話說明這次結果</h3>" +
      "<p class=\"big\">" + verdict + "</p>" +
      "<p class=\"muted\">這份報告在幫你做網站「可見度健檢」：搜尋看不看得到、AI 提不提得到、網站與內容有沒有明顯問題。</p>" +
      "<div class=\"next-box\"><strong>" + next + "</strong>" +
      "下面四張卡片用白話分類；點進去才看細節。專業術語都藏在「查看詳細證據」。" +
      offlineNote + "</div>";
  }

  function renderPillars() {
    const c = counts(state.data);
    const box = $("pillars");
    box.innerHTML = pillarCards(c)
      .map(
        (p) => `<article class="glass pillar" data-pillar="${p.id}">
        <div class="kicker">${p.kicker}</div>
        <div class="name">${p.name}</div>
        <p class="blurb">${p.blurb}</p>
        <div class="metric">${p.metric}<small>${p.metricSmall || ""}</small></div>
        ${p.tier === "unmeasured" ? '<div style="margin-top:10px"><span class="tier unmeasured">尚未測量</span></div>' : ""}
      </article>`
      )
      .join("");
    box.querySelectorAll(".pillar").forEach((el) => {
      el.addEventListener("click", () => openDetail(el.getAttribute("data-pillar")));
    });
  }

  function topPlainIssues(limit) {
    const issues = (state.data.issues || []).slice();
    const rank = { P0: 0, P1: 1, P2: 2, P3: 3 };
    const dRank = { true_issue: 0, needs_review: 1, insufficient_evidence: 2, likely_exception: 3 };
    issues.sort((a, b) => {
      const ea = a.evidence || {}, eb = b.evidence || {};
      const da = dRank[ea.disposition || "needs_review"] ?? 9;
      const db = dRank[eb.disposition || "needs_review"] ?? 9;
      if (da !== db) return da - db;
      return (rank[a.priority] ?? 9) - (rank[b.priority] ?? 9);
    });
    return issues.slice(0, limit).map(plainIssue);
  }

  function renderIssueCard(p, { openEvidence } = {}) {
    const raw = p.raw;
    const ev = raw.evidence || {};
    const evidId = "ev-" + (raw.id || Math.random().toString(36).slice(2));
    return `<article class="issue">
      <div>
        <span class="tag ${String(p.priority).toLowerCase()}">${p.priority}</span>
        <span class="tag">${p.disposition}</span>
      </div>
      <h4>${escapeHtml(p.title)}</h4>
      <p class="why"><strong>我們發現：</strong>${escapeHtml(p.why)}</p>
      <p class="why"><strong>我要處理嗎？</strong>${escapeHtml(p.should)}</p>
      <p class="why"><strong>怎麼處理？</strong>${escapeHtml(p.how)}</p>
      <div class="actions">
        <button class="btn ghost" data-toggle="${evidId}">查看詳細證據</button>
      </div>
      <div class="evidence hidden" id="${evidId}">${escapeHtml(
        [
          "原始問題：" + (raw.problem || ""),
          "原因：" + (raw.cause || ""),
          "建議：" + (raw.fix || ""),
          "disposition：" + (ev.disposition || ""),
          "confidence：" + (ev.confidence || ""),
          ev.do_not_fix_if ? "do_not_fix_if：" + ev.do_not_fix_if : "",
          ev.http_checked === false ? "HTTP：未探測" : "",
          (ev.url_evidence_chain_sample && ev.url_evidence_chain_sample.evidence_gap) || ev.evidence_gap || "",
        ]
          .filter(Boolean)
          .join("\n")
      )}</div>
    </article>`;
  }

  function escapeHtml(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderTopIssues() {
    const box = $("top-issues");
    const list = topPlainIssues(5);
    const heading = document.querySelector("#overview-extras h3");
    if (heading) heading.textContent = "現在最該先看的一件（或幾件）事";
    const sub = document.querySelector("#overview-extras .muted");
    if (sub) sub.textContent = "不用一次看懂全部。先處理最上面的，看完再決定要不要點四張卡片。";
    box.innerHTML = list.map((p) => renderIssueCard(p)).join("") || '<p class="muted">目前沒有特別急的項目。可以點上面四張卡片隨意逛逛。</p>';
    bindEvidenceToggles(box);
  }

  function bindEvidenceToggles(root) {
    root.querySelectorAll("[data-toggle]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const el = document.getElementById(btn.getAttribute("data-toggle"));
        if (el) el.classList.toggle("hidden");
      });
    });
  }

  function websiteMapHtml(c) {
    const types = c.pageTypes || {};
    const entries = Object.entries(types).slice(0, 6);
    if (!entries.length) {
      return `<div class="map"><div class="map-row"><span class="map-node hub">首頁／入口</span><span class="arrow">→</span><span class="map-node">內容頁 × ${c.pages}</span></div></div>`;
    }
    return `<div class="map">
      <div class="map-row"><span class="map-node hub">網站入口</span></div>
      <div class="map-row">${entries
        .map(([k, v]) => `<span class="map-node">${escapeHtml(k)} · ${v}</span>`)
        .join('<span class="arrow">·</span>')}</div>
      <p class="muted">這是依頁面結構推估的地圖，不是設計稿。page_type 為啟發式。</p>
    </div>`;
  }

  function filterIssues(pred) {
    return (state.data.issues || []).filter(pred).map(plainIssue);
  }

  function openDetail(pillar) {
    state.detail = pillar;
    $("detail-root").classList.remove("hidden");
    $("overview-extras").classList.add("hidden");
    $("pillars").classList.add("hidden");
    const c = counts(state.data);
    const body = $("detail-body");

    if (pillar === "search") {
      const items = filterIssues((i) => {
        const ev = i.evidence || {};
        return (
          ev.disposition === "true_issue" ||
          i.category === "i18n" ||
          i.category === "meta" ||
          (ev.url_evidence && ev.disposition !== "likely_exception")
        );
      }).slice(0, 12);
      body.innerHTML = `<div class="glass panel">
        <h3>Search｜搜尋可見度</h3>
        <p class="muted">搜尋引擎能不能正確理解你的網站？</p>
        <p>優先真問題 <strong>${c.trueN}</strong> · 待審 ${c.review} · HTTP ${c.httpMode === "offline" ? "未探測" : c.httpMode}${c.http404 ? " · 已確認 404：" + c.http404 : ""}</p>
        <details style="margin-top:12px"><summary>專業分類（SEO／Technical）</summary>
          <p class="muted">Indexability、URL、Internal Links、Canonical、Hreflang、Sitemap 等細節在下方證據中。</p>
        </details>
      </div>
      <div class="issues">${items.map((p) => renderIssueCard(p)).join("") || '<p class="muted">這一層暫時沒有優先項目。</p>'}</div>`;
    } else if (pillar === "ai") {
      body.innerHTML = `<div class="glass panel">
        <h3>AI｜AI 可見度</h3>
        <p class="muted">AI 是否看得到、理解並提到你。</p>
        <div style="display:flex; gap:8px; flex-wrap:wrap; margin:12px 0">
          <span class="tier measured">已測量：0（尚未接 AI 平台觀測）</span>
          <span class="tier est">推估：可依內容／結構看 readiness（非正式分數）</span>
          <span class="tier unmeasured">尚未測量：目前沒有 ChatGPT／Gemini／Perplexity 等實測</span>
        </div>
        <p><strong>絕對不會</strong>顯示假的 GEO／AEO 分數。</p>
        <details style="margin-top:12px"><summary>專業分類（AEO／GEO／AI Visibility）</summary>
          <p class="muted">等接上真實 mention／citation／source 資料後，會出現在「已測量」。</p>
        </details>
        <p class="muted" style="margin-top:14px">內容獨特度均值（結構推估）：${c.unique != null ? c.unique : "—"}</p>
      </div>`;
    } else if (pillar === "website") {
      body.innerHTML = `<div class="split">
        <div class="glass panel">
          <h3>Website｜網站健康</h3>
          <p class="muted">用空間化地圖理解網站結構（小白層）。</p>
          ${websiteMapHtml(c)}
        </div>
        <div class="glass panel">
          <h3>Website Understanding</h3>
          <p>頁數 <strong>${c.pages}</strong> · 語系約 <strong>${c.langs}</strong></p>
          <p class="muted">URL Evidence 鏈 ${c.urlChains}；缺目標在未探測 HTTP 時保持「證據不足」，不當 404。</p>
          <details><summary>查看詳細證據（技術）</summary>
            <pre class="evidence" style="display:block">${escapeHtml(JSON.stringify((state.data.summary || {}).site_understanding || {}, null, 2).slice(0, 1800))}</pre>
          </details>
        </div>
      </div>`;
    } else if (pillar === "content") {
      const sims = filterIssues((i) => i.category === "similarity" || (i.evidence || {}).cluster).slice(0, 10);
      body.innerHTML = `<div class="glass panel">
        <h3>Content｜內容品質</h3>
        <p class="muted">先看人話：哪些頁面太像？哪些內容真正不同？哪些需要注意？</p>
        <p>獨特內容均值（推估）：<strong>${c.unique != null ? c.unique : "—"}</strong></p>
      </div>
      <div class="issues">${sims.map((p) => renderIssueCard(p)).join("") || '<p class="muted">沒有明顯的相似內容群。</p>'}</div>`;
    }
    bindEvidenceToggles(body);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function closeDetail() {
    state.detail = null;
    $("detail-root").classList.add("hidden");
    $("overview-extras").classList.remove("hidden");
    $("pillars").classList.remove("hidden");
  }

  function renderDash() {
    show("dash");
    closeDetail();
    const label = (state.data.site_label || state.data.sample_url || "") + " · 來自 Scanner 真實輸出";
    $("dash-site-label").textContent = label;
    renderResultHero();
    renderPillars();
    renderTopIssues();
  }

  async function analyze(url) {
    const key = pickDemoKey(url);
    await runScanAnimation(url);
    state.data = await loadDemo(key);
    state.data.sample_url = url;
    renderDash();
  }

  function initChips() {
    const box = $("demo-chips");
    box.innerHTML = DEMOS.map(
      (d) => `<button type="button" class="chip" data-key="${d.key}" data-url="${d.url}">Demo：${d.label}</button>`
    ).join("");
    box.querySelectorAll(".chip").forEach((btn) => {
      btn.addEventListener("click", () => {
        $("url-input").value = btn.getAttribute("data-url");
        analyze(btn.getAttribute("data-url"));
      });
    });
  }

  $("btn-analyze").addEventListener("click", () => {
    const url = ($("url-input").value || "").trim() || "https://example.com";
    analyze(url);
  });
  $("url-input").addEventListener("keydown", (e) => {
    if (e.key === "Enter") $("btn-analyze").click();
  });
  $("btn-home").addEventListener("click", () => show("landing"));
  $("btn-rescan").addEventListener("click", () => {
    const url = (state.data && state.data.sample_url) || $("url-input").value;
    analyze(url);
  });
  $("btn-back-pillars").addEventListener("click", closeDetail);

  initChips();
  show("landing");
})();
