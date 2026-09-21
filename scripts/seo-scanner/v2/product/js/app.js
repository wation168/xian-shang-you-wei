/* AI Search & Website Intelligence — Phase 3 result UX */
(function () {
  const DEMOS = [
    { key: "django", label: "示範：部落格網站", url: "https://www.djangoproject.com/weblog/" },
    { key: "tutorial", label: "示範：教學網站", url: "https://docs.python.org/3/tutorial/" },
    { key: "patterns", label: "示範：大型內容站", url: "https://example.com/patterns" },
  ];

  const SCAN_STEPS = [
    "讀取網站結構",
    "理解網站長什麼樣子",
    "檢查技術健康",
    "理解內容與頁面目的",
    "評估搜尋可見度",
    "評估 AI 可見度（未測量則誠實標示）",
  ];

  const state = { data: null, view: "landing", detail: null };
  const $ = (id) => document.getElementById(id);

  function show(view) {
    state.view = view;
    ["landing", "scan", "dash"].forEach((v) => {
      const el = $("view-" + v);
      if (el) el.classList.toggle("hidden", v !== view);
    });
  }

  function escapeHtml(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
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
      trueN: trueN,
      review: dc.needs_review || 0,
      pages: s.page_count || (data.pages || []).length,
      unique: shell.mean_unique_ratio,
      urlChains: (ue.url_evidence_chain || {}).chain_count || 0,
      httpMode: ue.http_live ? "live" : (ue.http_fixture_loaded ? "fixture" : "offline"),
      pageTypes: und.page_type_histogram || {},
    };
  }

  function userSeverity(issue) {
    const d = (issue.evidence || {}).disposition || "needs_review";
    if (d === "true_issue") return "urgent";
    if (d === "needs_review" || d === "insufficient_evidence") return "watch";
    return "ok";
  }

  function techKey(issue) {
    const ev = issue.evidence || {};
    const cat = issue.category || "";
    const blob = (issue.problem || "") + " " + (issue.cause || "");
    if (cat === "similarity" || ev.cluster) return "content_similar";
    if (ev.url_evidence || String(issue.id || "").indexOf("url-") === 0) return "url_uncertain";
    if (cat === "i18n" || /hreflang|語系|語言/i.test(blob)) return "i18n";
    if (cat === "meta") {
      if (/canonical/i.test(blob)) return "meta_canonical";
      if (/description|摘要|描述/i.test(blob)) return "meta_description";
      return "meta_basic";
    }
    if (cat === "links" && ev.link_opportunity) {
      if (ev.archive_date_demoted) return "links_archive";
      return "links_opportunity";
    }
    return "other";
  }

  function productGroupKey(issue) {
    const k = techKey(issue);
    if (k === "meta_description" || k === "meta_canonical" || k === "meta_basic") return "meta_bundle";
    return k;
  }

  function buildGroups(issues) {
    const buckets = {};
    (issues || []).forEach(function (issue) {
      const key = productGroupKey(issue);
      if (key === "links_archive") return;
      if (!buckets[key]) buckets[key] = { key: key, issues: [], severities: [] };
      buckets[key].issues.push(issue);
      buckets[key].severities.push(userSeverity(issue));
    });

    const groups = [];
    Object.keys(buckets).forEach(function (key) {
      const b = buckets[key];
      const hasUrgent = b.severities.indexOf("urgent") >= 0;
      const hasWatch = b.severities.indexOf("watch") >= 0;
      const pageSet = {};
      const pages = [];
      b.issues.forEach(function (it) {
        (it.pages || []).forEach(function (pg) {
          if (pg && !pageSet[pg]) {
            pageSet[pg] = true;
            pages.push(pg);
          }
        });
      });

      let title = "其他值得一看的項目";
      let summary = "有一些項目建議再確認一次。";
      let impact = "";
      let advice = "點進去看證據後再決定。";
      let kinds = [];

      if (key === "meta_bundle") {
        title = "頁面基本資訊需要補強";
        summary = "有 " + b.issues.length + " 個檢查項目顯示：部分頁面缺少搜尋引擎常用資訊。";
        const kindSet = {};
        b.issues.forEach(function (it) {
          const k = techKey(it);
          if (k === "meta_description") kindSet["頁面描述（Meta description）"] = true;
          else if (k === "meta_canonical") kindSet["網址規範（Canonical）"] = true;
          else kindSet["標題／摘要"] = true;
        });
        kinds = Object.keys(kindSet);
        impact = "可能讓搜尋引擎較難判斷頁面內容與主要網址。";
        advice = "建議先從主要頁面開始補齊。";
      } else if (key === "content_similar") {
        title = "有些頁面的內容可能太相似";
        summary = "我們找到 " + b.issues.length + " 組值得進一步比較的頁面。";
        impact = "過於相似時，搜尋與使用者可能較難分辨差異。";
        advice = "先看差異最大的那一組，再決定要不要改。";
      } else if (key === "url_uncertain") {
        title = "有些連結目標還不能確認";
        summary = "掃描時找不到對應頁面；若尚未連線檢查，這不代表一定打不開。";
        impact = "在補證據前，不應直接當 404 處理。";
        advice = "先查看受影響連結；必要時再做連線確認。";
      } else if (key === "i18n") {
        title = "多語言設定可能需要核對";
        summary = "語系頁面之間的互相標示可能不完整。";
        impact = "若你確實有多語版本，可能影響搜尋理解語言。";
        advice = "單語網站通常不必硬加；多語再核對。";
      } else if (key === "links_opportunity") {
        title = "可能有值得加強的內連";
        summary = "有些相關頁面彼此可能還沒有自然連結。";
        impact = "不一定是錯誤，只是成長機會。";
        advice = "有主題關聯再加；沒有就略過。";
      }

      groups.push({
        key: key,
        title: title,
        summary: summary,
        kinds: kinds,
        impact: impact,
        advice: advice,
        label: hasUrgent ? "建議優先處理" : hasWatch ? "需要留意" : "可略過",
        level: hasUrgent ? "urgent" : hasWatch ? "watch" : "ok",
        count: b.issues.length,
        pages: pages,
        issues: b.issues,
      });
    });

    groups.sort(function (a, b) {
      const order = { urgent: 0, watch: 1, ok: 2 };
      return order[a.level] - order[b.level] || b.count - a.count;
    });
    return groups;
  }

  function pillarStatus(c, groups) {
    const watchSearch = groups.filter(function (g) {
      return ["meta_bundle", "i18n", "url_uncertain"].indexOf(g.key) >= 0 && g.level !== "ok";
    }).length;
    const contentN = groups
      .filter(function (g) { return g.key === "content_similar"; })
      .reduce(function (s, g) { return s + g.count; }, 0);
    return {
      search:
        c.trueN > 0
          ? { icon: "⚠️", text: "有 " + c.trueN + " 項建議優先處理" }
          : watchSearch > 0
            ? { icon: "⚠️", text: "有 " + watchSearch + " 項需要留意" }
            : { icon: "✓", text: "目前沒有急件" },
      ai: { icon: "⏳", text: "尚未測量" },
      website: { icon: "✓", text: c.pages + " 頁已完成掃描" },
      content:
        contentN > 0
          ? { icon: "⚠️", text: "有 " + contentN + " 組頁面值得比較" }
          : { icon: "✓", text: "沒有明顯相似群" },
    };
  }

  function pickDemoKey(url) {
    const u = (url || "").toLowerCase();
    if (u.indexOf("django") >= 0) return "django";
    if (u.indexOf("python") >= 0 || u.indexOf("docs.python") >= 0) return "tutorial";
    if (u.indexOf("pattern") >= 0) return "patterns";
    return "django";
  }

  async function loadDemo(key) {
    const res = await fetch("./data/" + key + ".json", { cache: "no-store" });
    if (!res.ok) throw new Error("無法載入 demo：" + key);
    return res.json();
  }

  function renderScanSteps(activeIdx) {
    $("scan-steps").innerHTML = SCAN_STEPS.map(function (label, i) {
      const cls = i < activeIdx ? "step done" : i === activeIdx ? "step active" : "step";
      const mark = i < activeIdx ? "✓" : i === activeIdx ? "●" : "○";
      return '<div class="' + cls + '"><span class="i">' + mark + "</span><span>" + label + "</span></div>";
    }).join("");
  }

  function runScanAnimation(url) {
    return new Promise(function (resolve) {
      show("scan");
      $("scan-url-label").textContent = "目標：" + url;
      let i = 0;
      renderScanSteps(0);
      const timer = setInterval(function () {
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

  function renderResultHero() {
    const el = $("result-hero");
    if (!el) return;
    const c = counts(state.data);
    const groups = buildGroups(state.data.issues || []);
    const watchN = groups.filter(function (g) { return g.level === "watch"; }).length;
    const urgentN = groups.filter(function (g) { return g.level === "urgent"; }).length;
    let verdict;
    if (urgentN === 0 && watchN === 0) {
      verdict = "目前沒有需要立即處理的重大問題，也沒有特別需要留意的項目。";
    } else if (urgentN === 0) {
      verdict = "目前沒有需要立即處理的重大問題。不過有幾個地方的基本資訊與內容結構值得先整理。";
    } else {
      verdict = "有 " + urgentN + " 類問題建議優先處理；其餘可稍後再看。";
    }
    el.className = "glass panel result-hero";
    const offlineNote =
      c.httpMode === "offline"
        ? '<div class="muted" style="margin-top:8px">補充：這次沒有連線檢查網址是否真的打不開，所以「找不到頁面」先當成「證據還不夠」，不是直接宣判 404。</div>'
        : "";
    el.innerHTML =
      "<h3>一句話看懂</h3>" +
      '<p class="big">' +
      escapeHtml(verdict) +
      "</p>" +
      '<p class="muted">這是網站「可見度健檢」：搜尋看不看得到、AI 提不提得到、網站與內容有沒有明顯問題。你不需要先懂 SEO。</p>' +
      offlineNote;
  }

  function pillarCards(c) {
    const st = pillarStatus(c, buildGroups(state.data.issues || []));
    return [
      { id: "search", kicker: "搜尋", name: "別人搜得到嗎？", blurb: "Google 這類搜尋，能不能正確讀懂你的網站。", metric: st.search.text, metricIcon: st.search.icon },
      { id: "ai", kicker: "AI", name: "AI 提得到你嗎？", blurb: "這版還沒接真實 AI 觀測，所以誠實寫尚未測量——不會給假分數。", metric: st.ai.text, metricIcon: st.ai.icon, tier: "unmeasured" },
      { id: "website", kicker: "網站", name: "網站健不健康？", blurb: "結構、連結、技術基礎有沒有明顯問題。", metric: st.website.text, metricIcon: st.website.icon },
      { id: "content", kicker: "內容", name: "內容清不清楚？", blurb: "頁面是不是講清楚、會不會彼此太像。", metric: st.content.text, metricIcon: st.content.icon },
    ];
  }

  function renderPillars() {
    const c = counts(state.data);
    const box = $("pillars");
    box.innerHTML = pillarCards(c)
      .map(function (p) {
        return (
          '<article class="glass pillar" data-pillar="' +
          p.id +
          '"><div class="kicker">' +
          escapeHtml(p.kicker) +
          '</div><div class="name">' +
          escapeHtml(p.name) +
          '</div><p class="blurb">' +
          escapeHtml(p.blurb) +
          '</p><div class="metric"><span class="status-ico">' +
          (p.metricIcon || "") +
          "</span> " +
          escapeHtml(p.metric) +
          "</div>" +
          (p.tier === "unmeasured" ? '<div style="margin-top:10px"><span class="tier unmeasured">尚未測量</span></div>' : "") +
          "</article>"
        );
      })
      .join("");
    box.querySelectorAll(".pillar").forEach(function (el) {
      el.addEventListener("click", function () {
        openDetail(el.getAttribute("data-pillar"));
      });
    });
  }

  function bindEvidenceToggles(root) {
    root.querySelectorAll("[data-toggle]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const el = document.getElementById(btn.getAttribute("data-toggle"));
        if (el) el.classList.toggle("hidden");
      });
    });
  }

  function renderGroupCard(g, idx) {
    const gid = "grp-" + idx;
    const kinds = (g.kinds || []).length
      ? '<ul class="kind-list">' + g.kinds.map(function (k) { return "<li>" + escapeHtml(k) + "</li>"; }).join("") + "</ul>"
      : "";
    const pages = (g.pages || []).slice(0, 16);
    const pageBlock = pages.length
      ? '<div class="evidence hidden" id="' +
        gid +
        '-pages"><strong>受影響頁面</strong><br/>' +
        pages.map(escapeHtml).join("<br/>") +
        ((g.pages || []).length > 16 ? "<br/>…共 " + g.pages.length + " 頁" : "") +
        "</div>"
      : "";
    const evidBlock =
      '<div class="evidence hidden" id="' +
      gid +
      '-ev">' +
      g.issues
        .slice(0, 10)
        .map(function (it) {
          const ev = it.evidence || {};
          return escapeHtml(
            [
              "・" + (it.problem || ""),
              "  頁面：" + ((it.pages || []).slice(0, 6).join(", ") || "—"),
              "  內部判斷：" + (ev.disposition || "—") + (it.priority ? " / " + it.priority : ""),
              ev.do_not_fix_if ? "  注意：" + ev.do_not_fix_if : "",
            ]
              .filter(Boolean)
              .join("\n")
          );
        })
        .join("\n\n") +
      (g.issues.length > 10 ? "\n…還有 " + (g.issues.length - 10) + " 筆原始項目" : "") +
      "</div>";

    return (
      '<article class="issue group-card"><div><span class="tag ' +
      g.level +
      '">' +
      escapeHtml(g.label) +
      '</span><span class="tag">' +
      g.count +
      " 項</span></div><h4>" +
      (idx + 1) +
      "｜" +
      escapeHtml(g.title) +
      '</h4><p class="why">' +
      escapeHtml(g.summary) +
      "</p>" +
      kinds +
      (g.impact ? '<p class="why"><strong>影響：</strong>' + escapeHtml(g.impact) + "</p>" : "") +
      (g.advice ? '<p class="why"><strong>建議：</strong>' + escapeHtml(g.advice) + "</p>" : "") +
      '<div class="actions">' +
      (pages.length ? '<button class="btn ghost" data-toggle="' + gid + '-pages">查看受影響頁面</button>' : "") +
      '<button class="btn ghost" data-toggle="' +
      gid +
      '-ev">查看詳細證據</button></div>' +
      pageBlock +
      evidBlock +
      "</article>"
    );
  }

  function renderTopIssues() {
    const box = $("top-issues");
    const heading = document.querySelector("#overview-extras h3");
    if (heading) heading.textContent = "現在最值得先看的地方";
    const sub = document.querySelector("#overview-extras .muted");
    if (sub) sub.textContent = "先看群組。專業詞（P1、needs_review、meta、canonical）都藏在「查看詳細證據」。";

    const groups = buildGroups(state.data.issues || [])
      .filter(function (g) { return g.level !== "ok"; })
      .slice(0, 5);
    if (!groups.length) {
      box.innerHTML = '<p class="muted">目前沒有特別需要先看的項目。你可以點上面四張卡片隨意逛逛。</p>';
      return;
    }
    box.innerHTML = groups.map(renderGroupCard).join("");
    bindEvidenceToggles(box);
  }

  function websiteMapHtml(c) {
    const types = c.pageTypes || {};
    const keys = Object.keys(types).slice(0, 6);
    if (!keys.length) {
      return (
        '<div class="map"><div class="map-row"><span class="map-node hub">首頁／入口</span><span class="arrow">→</span><span class="map-node">內容頁 × ' +
        c.pages +
        "</span></div></div>"
      );
    }
    return (
      '<div class="map"><div class="map-row"><span class="map-node hub">網站入口</span></div><div class="map-row">' +
      keys
        .map(function (k) {
          return '<span class="map-node">' + escapeHtml(k) + " · " + types[k] + "</span>";
        })
        .join('<span class="arrow">·</span>') +
      '</div><p class="muted">這是依頁面結構推估的地圖，不是設計稿。</p></div>'
    );
  }

  function openDetail(pillar) {
    state.detail = pillar;
    $("detail-root").classList.remove("hidden");
    $("overview-extras").classList.add("hidden");
    $("pillars").classList.add("hidden");
    const c = counts(state.data);
    const body = $("detail-body");
    const groups = buildGroups(state.data.issues || []);

    if (pillar === "search") {
      const g = groups.filter(function (x) {
        return ["meta_bundle", "i18n", "url_uncertain"].indexOf(x.key) >= 0 && x.level !== "ok";
      });
      body.innerHTML =
        '<div class="glass panel"><h3>搜尋｜別人搜得到嗎？</h3><p class="muted">搜尋引擎能不能正確理解你的網站？</p></div><div class="issues">' +
        (g.map(renderGroupCard).join("") || '<p class="muted">這一層暫時沒有需要留意的項目。</p>') +
        "</div>";
    } else if (pillar === "ai") {
      body.innerHTML =
        '<div class="glass panel"><h3>AI｜AI 提得到你嗎？</h3><div style="display:flex;gap:8px;flex-wrap:wrap;margin:12px 0">' +
        '<span class="tier measured">已測量：0</span><span class="tier est">推估：可依內容結構看 readiness（非正式分數）</span><span class="tier unmeasured">尚未測量</span></div>' +
        "<p><strong>絕對不會</strong>顯示假的 GEO／AEO 分數。</p>" +
        '<p class="muted">等接上真實 mention／citation／source 後，會出現在「已測量」。</p></div>';
    } else if (pillar === "website") {
      body.innerHTML =
        '<div class="split"><div class="glass panel"><h3>網站｜健不健康？</h3>' +
        websiteMapHtml(c) +
        '</div><div class="glass panel"><h3>掃描摘要</h3><p>頁數 <strong>' +
        c.pages +
        "</strong></p>" +
        '<p class="muted">URL 證據鏈 ' +
        c.urlChains +
        "；缺目標在未探測 HTTP 時保持「證據還不夠」。</p></div></div>";
    } else if (pillar === "content") {
      const g = groups.filter(function (x) { return x.key === "content_similar"; });
      body.innerHTML =
        '<div class="glass panel"><h3>內容｜清不清楚？</h3><p class="muted">哪些頁面太像？哪些真正不同？</p><p>獨特內容均值（推估）：<strong>' +
        (c.unique != null ? c.unique : "—") +
        '</strong></p></div><div class="issues">' +
        (g.map(renderGroupCard).join("") || '<p class="muted">沒有明顯的相似內容群。</p>') +
        "</div>";
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
    $("dash-site-label").textContent = (state.data.site_label || state.data.sample_url || "") + " · Scanner 真實輸出";
    renderResultHero();
    renderPillars();
    renderTopIssues();
  }

  async function analyze(url) {
    const key = pickDemoKey(url);
    try {
      await runScanAnimation(url);
      state.data = await loadDemo(key);
      state.data.sample_url = url;
      renderDash();
    } catch (err) {
      alert("分析失敗：" + (err && err.message ? err.message : err));
      show("landing");
    }
  }

  function initChips() {
    const box = $("demo-chips");
    box.innerHTML = DEMOS.map(function (d) {
      return '<button type="button" class="chip" data-url="' + d.url + '">Demo：' + d.label + "</button>";
    }).join("");
    box.querySelectorAll(".chip").forEach(function (btn) {
      btn.addEventListener("click", function () {
        $("url-input").value = btn.getAttribute("data-url");
        analyze(btn.getAttribute("data-url"));
      });
    });
  }

  $("btn-analyze").addEventListener("click", function () {
    const url = ($("url-input").value || "").trim() || "https://example.com";
    analyze(url);
  });
  $("url-input").addEventListener("keydown", function (e) {
    if (e.key === "Enter") $("btn-analyze").click();
  });
  $("btn-home").addEventListener("click", function () { show("landing"); });
  $("btn-rescan").addEventListener("click", function () {
    analyze((state.data && state.data.sample_url) || $("url-input").value);
  });
  $("btn-back-pillars").addEventListener("click", closeDetail);

  initChips();
  show("landing");
})();
