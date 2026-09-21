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


  const SOLUTION_PLAYBOOKS = {
    meta_bundle: {
      freeImpact: "可能讓搜尋引擎較難判斷頁面主題與主要網址，進而影響點擊與收錄品質。",
      paidSteps: [
        "盤點首頁、主要分類與轉換頁，列出缺 description／canonical／標題的頁面。",
        "為每一頁寫一句「這頁在講什麼＋給誰看」的摘要（建議 70–155 字）。",
        "確認每頁只有一個 canonical，且指向你希望被索引的正式網址。",
        "標題（title）與 H1 對齊主題，避免多頁共用同一組文案。",
        "改完後用預覽／檢視原始碼抽查 3–5 個代表性頁面。",
        "付費方案可再測一次，確認問題群是否消失或降級。",
      ],
      paidDraftHint: "升級後可取得：各頁 Meta description 草稿範例、canonical 設定檢查清單、標題對照表。",
      verifyHint: "修復後再測（付費）：重新掃描同一批 URL，比對 meta_bundle 群組是否仍出現。",
    },
    content_similar: {
      freeImpact: "頁面過度相似時，搜尋與使用者較難分辨差異，可能稀釋曝光。",
      paidSteps: [
        "先挑相似度最高的一組，並列開啟兩頁比較「獨特段落」。",
        "標出可合併、可刪、或必須保留的頁面角色（入口／細節／轉換）。",
        "為保留頁補上獨特案例、表格、FAQ 或步驟說明，拉開差異。",
        "調整內部連結與標題，讓每頁意圖更清楚。",
        "若是樣板殼層過重，優先改正文區而非全站導覽。",
        "付費可再測，確認相似群組縮小或消失。",
      ],
      paidDraftHint: "升級後可取得：差異化大綱草稿、可合併頁建議、獨特段落改寫提示。",
      verifyHint: "修復後再測（付費）：重跑掃描，看 content_similar 群組數量與嚴重度是否下降。",
    },
    url_uncertain: {
      freeImpact: "連結目標證據不足時，不應直接當 404；但未確認前可能影響體驗與信任。",
      paidSteps: [
        "匯出受影響連結清單，標註來源頁與目標 URL。",
        "先做連線／狀態碼確認（200／301／404），再決定修法。",
        "404：改連到正確頁或移除失效錨點；301：更新為最終網址。",
        "相對路徑與尾斜線規則統一，避免同頁多種寫法。",
        "抽查導覽、頁尾、正文內連三處高流量來源。",
        "付費可再測，確認 url_uncertain 是否清掉。",
      ],
      paidDraftHint: "升級後可取得：失效連結修補優先序、建議替換目標、重導向對照草稿。",
      verifyHint: "修復後再測（付費）：開啟連線檢查模式重掃，確認證據鏈與狀態。",
    },
    i18n: {
      freeImpact: "若你確實有多語版本，hreflang／語系標示不完整可能讓搜尋選錯語言版本。",
      paidSteps: [
        "先確認站點是單語還是多語；單語通常不必硬加 hreflang。",
        "多語：列出語言代碼與對應首頁／關鍵頁 URL 對照表。",
        "每頁補齊互指的 hreflang，並包含 x-default（若適用）。",
        "檢查語言版本內容是否真的不同，避免只換殼。",
        "用 Search Console／網址檢查抽樣驗證（若有）。",
        "付費可再測，確認 i18n 群組是否仍需處理。",
      ],
      paidDraftHint: "升級後可取得：hreflang 標籤草稿、語言對照表範本、單語／多語決策說明。",
      verifyHint: "修復後再測（付費）：重掃後看 i18n 問題是否降為可略過或消失。",
    },
    links_opportunity: {
      freeImpact: "相關頁缺少自然內連不一定是錯誤，但可能錯過主題權重流動的機會。",
      paidSteps: [
        "只挑「主題真的相關」的頁面對，略過年表／歸檔噪音。",
        "在正文自然段落加入 1–2 條說明性內連，避免硬塞。",
        "錨點文字寫清楚主題，少用「點這裡」。",
        "檢查是否已有導覽／側欄連到同一目標，避免重複堆疊。",
        "優先處理高流量或轉換路徑上的頁面。",
        "付費可再測，看內連機會是否被消化。",
      ],
      paidDraftHint: "升級後可取得：建議內連對照表、錨點文案草稿、優先處理清單。",
      verifyHint: "修復後再測（付費）：重掃後 links_opportunity 是否減少或改為可略過。",
    },
    other: {
      freeImpact: "其他項目建議先看證據再決定；不一定都要立刻改。",
      paidSteps: [
        "閱讀詳細證據與 disposition，分辨 true_issue 與 needs_review。",
        "依影響面（流量／轉換／信任）排出優先順序。",
        "對 true_issue 寫出最小可行修復步驟。",
        "needs_review 先補證據，再決定是否動手。",
        "改完記錄變更範圍，方便對照。",
        "付費可再測，驗證修復是否生效。",
      ],
      paidDraftHint: "升級後可取得：依群組客製的修復步驟與文案／設定草稿。",
      verifyHint: "修復後再測（付費）：同一 URL 再掃一次，比對該群組是否改善。",
    },
  };

  const state = { data: null, view: "landing", detail: null, mode: null, demoUnlock: {} };
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

  async function postLiveScan(url) {
    let res;
    try {
      res = await fetch("/api/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url, max_pages: 40 }),
      });
    } catch (e) {
      throw new Error(
        "連不上即時掃描伺服器。請在 product 目錄執行：python server.py，然後開啟 http://127.0.0.1:8765/"
      );
    }
    let payload = null;
    try {
      payload = await res.json();
    } catch (e) {
      payload = null;
    }
    if (!res.ok) {
      const msg =
        (payload && payload.error) ||
        ("伺服器回應 " + res.status + (res.statusText ? " " + res.statusText : ""));
      throw new Error(msg);
    }
    if (!payload || typeof payload !== "object" || !("pages" in payload)) {
      throw new Error("伺服器未回傳有效的掃描結果 JSON。");
    }
    return payload;
  }

  async function checkLiveHealth() {
    try {
      const res = await fetch("/api/health", { cache: "no-store" });
      if (!res.ok) return false;
      const j = await res.json();
      return !!(j && j.ok);
    } catch (e) {
      return false;
    }
  }

  function ensureLiveNote() {
    if (document.getElementById("live-server-note")) return;
    const panel = document.querySelector("#view-landing .hero-panel");
    if (!panel) return;
    const note = document.createElement("p");
    note.id = "live-server-note";
    note.className = "muted";
    note.style.margin = "12px 0 0";
    note.textContent =
      "即時掃描需要本機伺服器。請在 product 目錄執行 python server.py，再開啟 http://127.0.0.1:8765/（示範按鈕不受影響）。";
    panel.appendChild(note);
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
    let tone = "ok";
    let badge = "目前沒有急件";
    if (urgentN === 0 && watchN === 0) {
      verdict = "目前沒有需要立即處理的重大問題，也沒有特別需要留意的項目。";
      badge = "整體看起來穩定";
    } else if (urgentN === 0) {
      verdict = "目前沒有需要立即處理的重大問題。不過有幾個地方的基本資訊與內容結構值得先整理。";
      tone = "watch";
      badge = "有幾項值得先看";
    } else {
      verdict = "有 " + urgentN + " 類問題建議優先處理；其餘可稍後再看。";
      tone = "urgent";
      badge = "建議優先處理";
    }
    el.className = "glass panel result-hero tone-" + tone;
    const offlineNote =
      c.httpMode === "offline"
        ? '<div class="note-card">補充：這次沒有連線檢查網址是否真的打不開，所以「找不到頁面」先當成「證據還不夠」，不是直接宣判 404。</div>'
        : "";
    el.innerHTML =
      '<div class="hero-badge ' + tone + '">' + escapeHtml(badge) + "</div>" +
      "<h3>一句話看懂</h3>" +
      '<p class="big">' +
      escapeHtml(verdict) +
      "</p>" +
      '<p class="muted">這是網站「可見度健檢」：搜尋看不看得到、AI 提不提得到、網站與內容有沒有明顯問題。你不需要先懂 SEO。</p>' +
      '<p class="muted freemium-line">免費：看懂問題與影響。付費：完整解法、草稿、AI 真實觀測、修復後再測。</p>' +
      offlineNote;
  }

  function pillarTone(icon) {
    if (icon === "⚠️") return "watch";
    if (icon === "⏳") return "pending";
    return "ok";
  }

  function pillarCards(c) {
    const st = pillarStatus(c, buildGroups(state.data.issues || []));
    return [
      { id: "search", icon: "🔎", kicker: "搜尋", name: "別人搜得到嗎？", blurb: "Google 這類搜尋，能不能正確讀懂你的網站。", metric: st.search.text, metricIcon: st.search.icon, tone: pillarTone(st.search.icon) },
      { id: "ai", icon: "🤖", kicker: "AI", name: "AI 提得到你嗎？", blurb: "測量 ChatGPT 等是否提到你是付費功能。免費版誠實標「尚未測量」、不造假分數；尚未接上真實證據前不會顯示「已測量」。", metric: st.ai.text, metricIcon: st.ai.icon, tier: "unmeasured", tone: "pending", planBadge: "付費可測" },
      { id: "website", icon: "🌐", kicker: "網站", name: "網站健不健康？", blurb: "結構、連結、技術基礎有沒有明顯問題。", metric: st.website.text, metricIcon: st.website.icon, tone: pillarTone(st.website.icon) },
      { id: "content", icon: "📝", kicker: "內容", name: "內容清不清楚？", blurb: "頁面是不是講清楚、會不會彼此太像。", metric: st.content.text, metricIcon: st.content.icon, tone: pillarTone(st.content.icon) },
    ];
  }

  function renderPillars() {
    const c = counts(state.data);
    const box = $("pillars");
    box.innerHTML = pillarCards(c)
      .map(function (p) {
        return (
          '<article class="glass pillar tone-' +
          (p.tone || "ok") +
          '" data-pillar="' +
          p.id +
          '"><div class="pillar-icon">' +
          (p.icon || "") +
          '</div><div class="kicker">' +
          escapeHtml(p.kicker) +
          '</div><div class="name">' +
          escapeHtml(p.name) +
          '</div><p class="blurb">' +
          escapeHtml(p.blurb) +
          '</p><div class="metric"><span class="status-ico">' +
          (p.metricIcon || "") +
          "</span><span>" +
          escapeHtml(p.metric) +
          "</span></div>" +
          (p.tier === "unmeasured" ? '<div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap;align-items:center"><span class="tier unmeasured">尚未測量</span>' + (p.planBadge ? '<span class="plan-chip paid">' + escapeHtml(p.planBadge) + '</span>' : '') + '</div>' : "") +
          '<div class="pillar-cta">點進去看細節 →</div></article>'
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


  function playbookFor(key) {
    return SOLUTION_PLAYBOOKS[key] || SOLUTION_PLAYBOOKS.other;
  }

  function freeImpactText(g) {
    const pb = playbookFor(g.key);
    const base = (g.impact || "").trim();
    const free = (pb.freeImpact || "").trim();
    if (!free) return base;
    if (!base) return free;
    if (base === free || free.indexOf(base) >= 0 || base.indexOf(free) >= 0) return base;
    return base;
  }

  function paywallHtml(g, unlockId) {
    const pb = playbookFor(g.key);
    const unlocked = !!(state.demoUnlock && state.demoUnlock[unlockId]);
    const steps = pb.paidSteps || [];
    const preview = steps.slice(0, 2);
    if (unlocked) {
      return (
        '<div class="paywall unlocked" data-paywall-id="' + unlockId + '">' +
        '<div class="paywall-head"><span class="lock-badge">付費功能預覽</span>' +
        '<span class="plan-chip paid">付費方案</span></div>' +
        '<h5>完整解決方案（付費）</h5>' +
        '<ol class="paywall-steps">' +
        steps.map(function (s) { return "<li>" + escapeHtml(s) + "</li>"; }).join("") +
        "</ol>" +
        '<p class="why"><strong>文案／草稿：</strong>' + escapeHtml(pb.paidDraftHint || "") + "</p>" +
        '<p class="why"><strong>修復後再測：</strong>' + escapeHtml(pb.verifyHint || "") + "</p>" +
        '<button type="button" class="btn ghost" data-demo-unlock="' + unlockId + '">收起預覽</button>' +
        "</div>"
      );
    }
    return (
      '<div class="paywall" data-paywall-id="' + unlockId + '">' +
      '<div class="paywall-head"><span class="lock-badge">🔒 鎖定</span>' +
      '<span class="plan-chip paid">付費功能</span></div>' +
      "<h5>完整解決方案（付費）</h5>" +
      '<ol class="paywall-steps locked-preview">' +
      preview.map(function (s) { return '<li class="blurred">' + escapeHtml(s) + "</li>"; }).join("") +
      (steps.length > 2 ? '<li class="blurred">……</li>' : "") +
      "</ol>" +
      '<p class="paywall-teaser">升級後解鎖：逐步做法、文案草稿、修復後再測</p>' +
      '<button type="button" class="btn ghost" data-demo-unlock="' + unlockId + '">預覽解法（產品示範）</button>' +
      '<p class="muted" style="margin-top:8px;font-size:.82rem">示範解鎖僅供產品預覽，非真實付費；不會呼叫外部 AI。</p>' +
      "</div>"
    );
  }

  function bindDemoUnlock(root) {
    root.querySelectorAll("[data-demo-unlock]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        const id = btn.getAttribute("data-demo-unlock");
        if (!id) return;
        state.demoUnlock[id] = !state.demoUnlock[id];
        // re-render current view pieces that contain paywalls
        if (state.detail) openDetail(state.detail);
        else {
          renderTopIssues();
        }
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

    const impactText = freeImpactText(g);
    const unlockId = "grp-" + g.key + "-" + idx;
    return (
      '<article class="issue group-card level-' +
      g.level +
      '"><div class="group-meta"><span class="tag ' +
      g.level +
      '">' +
      escapeHtml(g.label) +
      '</span><span class="plan-chip free">免費</span><span class="tag">' +
      g.count +
      " 項</span>" +
      (g.pages && g.pages.length ? '<span class="tag">' + g.pages.length + " 頁</span>" : "") +
      "</div><h4>" +
      (idx + 1) +
      "｜" +
      escapeHtml(g.title) +
      '</h4><p class="why">' +
      escapeHtml(g.summary) +
      "</p>" +
      kinds +
      (impactText ? '<p class="why"><strong>影響（免費）：</strong>' + escapeHtml(impactText) + "</p>" : "") +
      (g.advice ? '<p class="why"><strong>建議：</strong>' + escapeHtml(g.advice) + "</p>" : "") +
      '<div class="actions">' +
      (pages.length ? '<button class="btn ghost" data-toggle="' + gid + '-pages">查看受影響頁面 →</button>' : "") +
      '<button class="btn ghost" data-toggle="' +
      gid +
      '-ev">查看詳細證據</button></div>' +
      pageBlock +
      evidBlock +
      paywallHtml(g, unlockId) +
      "</article>"
    );
  }

  function renderTopIssues() {
    const box = $("top-issues");
    const heading = document.querySelector("#overview-extras h3");
    if (heading) heading.textContent = "現在最值得先看的地方";
    const sub = document.querySelector("#overview-extras .muted");
    if (sub) sub.textContent = "先看群組。專業詞（P1、needs_review、meta、canonical）都藏在「查看詳細證據」。免費：看懂問題與影響。付費：完整解法、草稿、AI 真實觀測、修復後再測。";

    const groups = buildGroups(state.data.issues || [])
      .filter(function (g) { return g.level !== "ok"; })
      .slice(0, 5);
    if (!groups.length) {
      box.innerHTML = '<p class="muted">目前沒有特別需要先看的項目。你可以點上面四張卡片隨意逛逛。</p>';
      return;
    }
    box.innerHTML = groups.map(renderGroupCard).join("");
    bindEvidenceToggles(box);
    bindDemoUnlock(box);
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
      const aiUnlock = "pillar-ai";
      const aiUnlocked = !!(state.demoUnlock && state.demoUnlock[aiUnlock]);
      const aiPaywallLocked =
        '<div class="paywall" data-paywall-id="' + aiUnlock + '">' +
        '<div class="paywall-head"><span class="lock-badge">🔒 鎖定</span><span class="plan-chip paid">付費功能</span></div>' +
        "<h5>完整解決方案（付費）</h5>" +
        '<ol class="paywall-steps locked-preview">' +
        '<li class="blurred">對真實 ChatGPT（或其他指定模型）跑提及／引用觀測迴圈</li>' +
        '<li class="blurred">彙整可核對的 mention／citation／source 證據</li>' +
        '<li class="blurred">……</li></ol>' +
        '<p class="paywall-teaser">升級後解鎖：逐步做法、文案草稿、修復後再測</p>' +
        '<button type="button" class="btn ghost" data-demo-unlock="' + aiUnlock + '">預覽解法（產品示範）</button>' +
        '<p class="muted" style="margin-top:8px;font-size:.82rem">示範解鎖僅供產品預覽，非真實付費；不會呼叫 OpenAI。</p></div>';
      const aiPaywallOpen =
        '<div class="paywall unlocked" data-paywall-id="' + aiUnlock + '">' +
        '<div class="paywall-head"><span class="lock-badge">付費功能預覽</span><span class="plan-chip paid">付費方案</span></div>' +
        "<h5>完整解決方案（付費）</h5>" +
        '<ol class="paywall-steps">' +
        "<li>設定品牌／產品關鍵問句，對真實 ChatGPT 等模型做提及觀測（付費能力）。</li>" +
        "<li>收集可核對的 mention、citation、source 片段作為證據層。</li>" +
        "<li>對照網站內容缺口，產出可執行的可見度改善步驟與草稿。</li>" +
        "<li>修復後再測：重跑同一觀測組，比較提及是否出現或品質提升。</li>" +
        "</ol>" +
        '<p class="why"><strong>文案／草稿：</strong>升級後可取得針對你網站的提問組與內容補強草稿（仍需真實模型證據，不會造假）。</p>' +
        '<p class="why"><strong>修復後再測：</strong>付費方案可重跑 AI 觀測迴圈驗證改善。</p>' +
        '<button type="button" class="btn ghost" data-demo-unlock="' + aiUnlock + '">收起預覽</button></div>';
      body.innerHTML =
        '<div class="glass panel"><h3>AI｜AI 提得到你嗎？</h3>' +
        '<div style="display:flex;gap:8px;flex-wrap:wrap;margin:12px 0">' +
        '<span class="tier unmeasured">尚未測量</span>' +
        '<span class="plan-chip paid">付費可測</span>' +
        '<span class="plan-chip free">免費誠實標示</span></div>' +
        "<p><strong>免費：</strong>清楚告訴你「尚未測量」。我們<strong>不會</strong>用助手自己的回答冒充已測量，也<strong>絕對不會</strong>發明 GEO／AEO 分數。</p>" +
        '<p class="muted">付費解鎖：接上真實 ChatGPT 提及／引用證據迴圈後，才會標成「已測量」。在那之前即使預覽付費解法，狀態仍是尚未測量。</p>' +
        (aiUnlocked ? aiPaywallOpen : aiPaywallLocked) +
        "</div>";
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
    bindDemoUnlock(body);
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
    const base = state.data.site_label || state.data.sample_url || "";
    const tag = state.mode === "demo" ? "示範資料" : "真實掃描";
    $("dash-site-label").textContent = base + " · " + tag;
    renderResultHero();
    renderPillars();
    renderTopIssues();
  }

  async function analyze(url, opts) {
    const options = opts || {};
    const asDemo = !!options.demo;
    try {
      const anim = runScanAnimation(url);
      let data;
      if (asDemo) {
        const key = options.demoKey || pickDemoKey(url);
        const loaded = await loadDemo(key);
        await anim;
        data = loaded;
        state.mode = "demo";
      } else {
        let live;
        let liveErr = null;
        try {
          live = await postLiveScan(url);
        } catch (e) {
          liveErr = e;
        }
        await anim;
        if (liveErr) throw liveErr;
        data = live;
        state.mode = "live";
      }
      state.data = data;
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
      return (
        '<button type="button" class="chip" data-demo-key="' +
        d.key +
        '" data-url="' +
        d.url +
        '">示範：' +
        d.label +
        "</button>"
      );
    }).join("");
    box.querySelectorAll(".chip").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const u = btn.getAttribute("data-url");
        $("url-input").value = u;
        analyze(u, { demo: true, demoKey: btn.getAttribute("data-demo-key") });
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
  checkLiveHealth().then(function (ok) {
    if (!ok) ensureLiveNote();
  });
})();
