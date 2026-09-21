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
      who: {
        diySummary: "站長可先補主要頁的 title／description／canonical。",
        diySteps: [
        "打開首頁與 2–3 個主要分類頁的編輯畫面或 CMS。",
        "為每頁填寫一句清楚的 Meta description（約 70–155 字）。",
        "確認 canonical 指向正式網址，且每頁只有一個。",
        "標題與 H1 對齊主題後存檔並抽查原始碼。"
      ],
        teamHandoff: "請內容／前端依「缺 description／canonical／標題」清單，於本週補齊首頁與轉換頁；完成後回報 URL 清單供再測。",
        conciergeCta: "由我們代為盤點、撰寫草稿並提交修改建議（付費服務・示範）。",
      },
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
      who: {
        diySummary: "站長可先挑最相似的一組頁面，拉開獨特段落。",
        diySteps: [
        "並列開啟相似度最高的兩頁，標出重複段落。",
        "決定保留／合併／刪除，並為保留頁補獨特案例或 FAQ。",
        "調整標題與內連，讓每頁意圖更清楚。"
      ],
        teamHandoff: "請內容團隊依相似群組清單差異化正文；優先高流量頁，完成後標記可再測。",
        conciergeCta: "由我們代寫差異化大綱與改寫草稿（付費服務・示範）。",
      },
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
      who: {
        diySummary: "站長可先匯出連結清單，確認狀態碼再決定修法。",
        diySteps: [
        "匯出受影響連結（來源頁 → 目標 URL）。",
        "用瀏覽器或工具確認 200／301／404。",
        "404 改連或移除；301 更新為最終網址。"
      ],
        teamHandoff: "請工程／維運依連結清單做狀態碼確認與重導向修正；完成後回報修復範圍。",
        conciergeCta: "由我們代查失效連結並產出修補優先序（付費服務・示範）。",
      },
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
      who: {
        diySummary: "先確認是否真的多語；單語通常不必硬加 hreflang。",
        diySteps: [
        "確認站點是單語還是多語。",
        "多語：列出語言代碼與對應 URL。",
        "補齊互指 hreflang（含 x-default 若適用）。"
      ],
        teamHandoff: "請前端／SEO 依語言對照表補 hreflang；單語則註記略過原因。",
        conciergeCta: "由我們代建語言對照與標籤草稿（付費服務・示範）。",
      },
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
      who: {
        diySummary: "站長可在主題相關頁的正文加 1–2 條自然內連。",
        diySteps: [
        "挑主題真的相關的頁面對（略過歸檔噪音）。",
        "在正文自然段落加入說明性內連。",
        "錨點寫清楚主題，少用「點這裡」。"
      ],
        teamHandoff: "請內容依建議內連對照表於正文補連結；優先轉換路徑頁面。",
        conciergeCta: "由我們代擬內連對照與錨點文案（付費服務・示範）。",
      },
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
      who: {
        diySummary: "先讀證據，分辨急件與需再確認，再決定誰動手。",
        diySteps: [
        "閱讀詳細證據與 disposition。",
        "依流量／轉換排出優先順序。",
        "對急件寫出最小可行修復步驟。"
      ],
        teamHandoff: "請負責人本週處理 true_issue；needs_review 先補證據再排程。",
        conciergeCta: "由我們代排優先序並產出修復草案（付費服務・示範）。",
      },
    },
  };

  const state = { data: null, view: "landing", detail: null, mode: null, member: false, paid: false, adUnlocks: {}, pendingAnalyze: null };
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

  function planLabel() {
    if (state.paid) return { chip: "付費（完整解法）", cls: "paid", short: "paid" };
    if (state.member) return { chip: "會員（免費檢測）", cls: "member", short: "member" };
    return { chip: "未登入／非會員", cls: "guest", short: "guest" };
  }

  function planHintLine() {
    return "會員可免費測；付費看完整解法；看廣告可解鎖一小部份";
  }

  function renderPlanChipsHtml(opts) {
    const o = opts || {};
    const p = planLabel();
    let html =
      '<div class="plan-bar" id="' + (o.id || "plan-bar") + '">' +
      '<span class="plan-chip ' + p.cls + '">' + escapeHtml(p.chip) + "</span>";
    if (state.member && !state.paid) {
      html += '<button type="button" class="btn ghost btn-sm" data-demo-upgrade-paid>示範升級付費</button>';
    } else if (!state.member) {
      html += '<button type="button" class="btn ghost btn-sm" data-demo-become-member>以會員身分繼續（示範）</button>';
    } else if (state.paid) {
      html += '<span class="plan-chip free">本工作階段已付費示範</span>';
    }
    html += '<span class="plan-hint muted">' + escapeHtml(planHintLine()) + "</span></div>";
    return html;
  }

  function ensurePlanBarLanding() {
    const panel = document.querySelector("#view-landing .hero-panel");
    if (!panel) return;
    let bar = document.getElementById("landing-plan-bar");
    if (!bar) {
      bar = document.createElement("div");
      bar.id = "landing-plan-bar-wrap";
      panel.insertBefore(bar, panel.firstChild);
    }
    const wrap = document.getElementById("landing-plan-bar-wrap");
    wrap.innerHTML = renderPlanChipsHtml({ id: "landing-plan-bar" });
    bindPlanActions(wrap);
  }

  function ensurePlanBarDash() {
    const topbar = document.querySelector("#view-dash .topbar");
    if (!topbar) return;
    let slot = document.getElementById("dash-plan-slot");
    if (!slot) {
      slot = document.createElement("div");
      slot.id = "dash-plan-slot";
      slot.style.cssText = "flex:1 1 100%; margin-top:8px";
      topbar.appendChild(slot);
    }
    slot.innerHTML = renderPlanChipsHtml({ id: "dash-plan-bar" });
    bindPlanActions(slot);
  }

  function refreshPlanBars() {
    ensurePlanBarLanding();
    if (state.view === "dash" && state.data) ensurePlanBarDash();
  }

  function bindPlanActions(root) {
    root.querySelectorAll("[data-demo-upgrade-paid]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        state.paid = true;
        refreshPlanBars();
        if (state.data) {
          if (state.detail) openDetail(state.detail);
          else {
            renderResultHero();
            renderPillars();
            renderTopIssues();
          }
        }
      });
    });
    root.querySelectorAll("[data-demo-become-member]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        state.member = true;
        refreshPlanBars();
      });
    });
  }

  function ensureGateModal() {
    let overlay = document.getElementById("gate-modal-overlay");
    if (overlay) return overlay;
    overlay = document.createElement("div");
    overlay.id = "gate-modal-overlay";
    overlay.className = "gate-modal-overlay hidden";
    overlay.innerHTML =
      '<div class="glass gate-modal" role="dialog" aria-modal="true" aria-labelledby="gate-modal-title">' +
      '<h3 id="gate-modal-title">免費檢測需先成為會員</h3>' +
      '<p class="muted">本產品示範：成為會員後才能執行免費掃描／檢測。付費可看完整解法；看廣告僅能解鎖一小部份（例如 1 步）。</p>' +
      '<div class="gate-actions">' +
      '<button type="button" class="btn" id="gate-become-member">以會員身分繼續（示範）</button>' +
      '<button type="button" class="btn ghost" id="gate-dismiss">先看看介紹</button>' +
      "</div>" +
      '<p class="muted" style="margin-top:12px;font-size:.82rem">示範狀態僅存於本工作階段，無真實登入／金流／廣告網路。</p>' +
      "</div>";
    document.body.appendChild(overlay);
    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) hideGateModal(false);
    });
    document.getElementById("gate-dismiss").addEventListener("click", function () {
      hideGateModal(false);
    });
    document.getElementById("gate-become-member").addEventListener("click", function () {
      state.member = true;
      hideGateModal(true);
      refreshPlanBars();
      const pending = state.pendingAnalyze;
      state.pendingAnalyze = null;
      if (pending) analyze(pending.url, pending.opts);
    });
    return overlay;
  }

  function showGateModal(pending) {
    state.pendingAnalyze = pending || null;
    const overlay = ensureGateModal();
    overlay.classList.remove("hidden");
  }

  function hideGateModal(proceeded) {
    const overlay = document.getElementById("gate-modal-overlay");
    if (overlay) overlay.classList.add("hidden");
    if (!proceeded) state.pendingAnalyze = null;
  }

  function requireMemberThen(url, opts) {
    if (state.member) {
      analyze(url, opts);
      return;
    }
    showGateModal({ url: url, opts: opts || {} });
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
      '<p class="muted freemium-line">會員可免費測；付費看完整解法（怎麼做＋誰來解決）；看廣告可解鎖一小部份（例如 1 步）。AI 真實觀測屬付費。</p>' +
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
      { id: "ai", icon: "🤖", kicker: "AI", name: "AI 提得到你嗎？", blurb: "AI 真實觀測屬付費；會員免費版不測、不造假分，誠實標「尚未測量」。", metric: st.ai.text, metricIcon: st.ai.icon, tier: "unmeasured", tone: "pending", planBadge: "付費可測" },
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

  function whoSummaryHtml(pb) {
    const who = pb.who || {};
    return (
      '<div class="who-section who-summary">' +
      "<h5>誰來解決</h5>" +
      '<div class="who-roles">' +
      '<div class="who-role"><span class="who-label">1. 我自己做（DIY）</span>' +
      '<p class="muted">' + escapeHtml(who.diySummary || "站長可先從影響最大的頁面動手。") + "</p></div>" +
      '<div class="who-role"><span class="who-label">2. 交給我的團隊</span>' +
      '<p class="muted">付費完整版可匯出交接說明給團隊。</p></div>' +
      '<div class="who-role"><span class="who-label">3. 請你們代做</span>' +
      '<p class="muted">付費服務：由我們代為處理（示範 CTA）。</p></div>' +
      "</div></div>"
    );
  }

  function whoDetailHtml(pb, unlockId, mode) {
    // mode: 'paid' | 'ad' | 'locked'
    const who = pb.who || {};
    const diySteps = who.diySteps || [];
    let diyBody = "";
    if (mode === "paid") {
      diyBody =
        '<ol class="paywall-steps">' +
        diySteps.map(function (s) { return "<li>" + escapeHtml(s) + "</li>"; }).join("") +
        "</ol>";
    } else if (mode === "ad" && diySteps.length) {
      diyBody =
        '<div class="ad-unlock-partial">' +
        '<span class="plan-chip ad">廣告解鎖・僅 1 步</span>' +
        '<ol class="paywall-steps"><li>' + escapeHtml(diySteps[0]) + "</li></ol>" +
        '<p class="muted" style="font-size:.82rem">其餘 DIY 步驟需付費完整解法。</p></div>';
    } else {
      diyBody =
        '<ol class="paywall-steps locked-preview">' +
        (diySteps[0] ? '<li class="blurred">' + escapeHtml(diySteps[0]) + "</li>" : "") +
        '<li class="blurred">……</li></ol>' +
        '<p class="muted" style="font-size:.82rem">詳細 DIY 清單屬付費；看廣告可解鎖第 1 步。</p>';
    }

    let teamBody = "";
    if (mode === "paid") {
      teamBody =
        '<div class="who-handoff">' +
        '<p class="why">' + escapeHtml(who.teamHandoff || "") + "</p>" +
        '<button type="button" class="btn ghost btn-sm" data-copy-handoff="' + unlockId + '">複製交接說明（示範）</button>' +
        '<pre class="handoff-export hidden" id="handoff-' + unlockId + '">' + escapeHtml(who.teamHandoff || "") + "</pre>" +
        "</div>";
    } else {
      teamBody = '<p class="muted">升級付費後可匯出可交接的團隊說明。</p>';
    }

    let conciergeBody = "";
    if (mode === "paid") {
      conciergeBody =
        '<p class="why">' + escapeHtml(who.conciergeCta || "") + "</p>" +
        '<button type="button" class="btn btn-sm" data-concierge-demo="' + unlockId + '">請你們代做（示範・無金流）</button>' +
        '<p class="muted concierge-note hidden" id="concierge-note-' + unlockId + '" style="margin-top:8px;font-size:.82rem">已記錄示範意向（本工作階段），無真實下單。</p>';
    } else {
      conciergeBody = '<p class="muted">付費服務 CTA：升級後可提出代做意向（示範）。</p>';
    }

    return (
      '<div class="who-section who-detail">' +
      "<h5>誰來解決（詳細）</h5>" +
      '<div class="who-role paid-block"><span class="who-label">1. 我自己做（DIY）</span>' + diyBody + "</div>" +
      '<div class="who-role paid-block"><span class="who-label">2. 交給我的團隊</span>' + teamBody + "</div>" +
      '<div class="who-role paid-block"><span class="who-label">3. 請你們代做</span>' + conciergeBody + "</div>" +
      "</div>"
    );
  }

  function howHtml(pb, unlockId, mode) {
    const steps = pb.paidSteps || [];
    if (mode === "paid") {
      return (
        "<h5>怎麼做｜完整解決方案</h5>" +
        '<ol class="paywall-steps">' +
        steps.map(function (s) { return "<li>" + escapeHtml(s) + "</li>"; }).join("") +
        "</ol>" +
        '<p class="why"><strong>文案／草稿：</strong>' + escapeHtml(pb.paidDraftHint || "") + "</p>" +
        '<p class="why"><strong>修復後再測：</strong>' + escapeHtml(pb.verifyHint || "") + "</p>"
      );
    }
    if (mode === "ad" && steps.length) {
      return (
        "<h5>怎麼做｜解法</h5>" +
        '<div class="ad-unlock-partial">' +
        '<span class="plan-chip ad">廣告解鎖・僅 1 步</span>' +
        '<ol class="paywall-steps"><li>' + escapeHtml(steps[0]) + "</li></ol>" +
        '<p class="muted" style="font-size:.82rem">完整步驟、草稿與再測屬付費。</p></div>'
      );
    }
    const preview = steps.slice(0, 2);
    return (
      "<h5>怎麼做｜完整解決方案（付費）</h5>" +
      '<ol class="paywall-steps locked-preview">' +
      preview.map(function (s) { return '<li class="blurred">' + escapeHtml(s) + "</li>"; }).join("") +
      (steps.length > 2 ? '<li class="blurred">……</li>' : "") +
      "</ol>" +
      '<p class="paywall-teaser">付費解鎖：逐步做法、文案草稿、修復後再測；看廣告僅解鎖一小部份（1 步）</p>'
    );
  }

  function paywallHtml(g, unlockId) {
    const pb = playbookFor(g.key);
    const adN = (state.adUnlocks && state.adUnlocks[unlockId]) || 0;
    const mode = state.paid ? "paid" : adN >= 1 ? "ad" : "locked";
    const head =
      state.paid
        ? '<div class="paywall-head"><span class="lock-badge">已解鎖</span><span class="plan-chip paid">付費（完整解法）</span></div>'
        : mode === "ad"
          ? '<div class="paywall-head"><span class="lock-badge">部份解鎖</span><span class="plan-chip ad">廣告・僅 1 步</span></div>'
          : '<div class="paywall-head"><span class="lock-badge">🔒 鎖定</span><span class="plan-chip paid">付費功能</span></div>';

    let actions = "";
    if (!state.paid) {
      actions =
        '<div class="paywall-actions">' +
        '<button type="button" class="btn ghost" data-ad-unlock="' + unlockId + '"' +
        (adN >= 1 ? " disabled" : "") +
        ">" +
        (adN >= 1 ? "已用廣告解鎖一小部份" : "看廣告解鎖一小部份（示範）") +
        "</button>" +
        '<button type="button" class="btn" data-upgrade-paid="' + unlockId + '">升級付費看完整解法（示範）</button>' +
        '<p class="muted" style="margin-top:8px;font-size:.82rem">示範狀態僅本工作階段；無真實廣告網路／金流；不會呼叫外部 AI。</p>' +
        "</div>";
    }

    return (
      '<div class="paywall' + (state.paid ? " unlocked" : "") + (mode === "ad" ? " ad-partial" : "") +
      '" data-paywall-id="' + unlockId + '">' +
      head +
      whoSummaryHtml(pb) +
      howHtml(pb, unlockId, mode) +
      whoDetailHtml(pb, unlockId, mode) +
      actions +
      "</div>"
    );
  }

  function reRenderPaywalls() {
    refreshPlanBars();
    if (state.detail) openDetail(state.detail);
    else if (state.data) {
      renderResultHero();
      renderPillars();
      renderTopIssues();
    }
  }

  function bindPaywallActions(root) {
    root.querySelectorAll("[data-ad-unlock]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        const id = btn.getAttribute("data-ad-unlock");
        if (!id || (state.adUnlocks[id] || 0) >= 1) return;
        btn.disabled = true;
        btn.textContent = "播放廣告中…";
        setTimeout(function () {
          state.adUnlocks[id] = 1;
          reRenderPaywalls();
        }, 1200);
      });
    });
    root.querySelectorAll("[data-upgrade-paid]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        state.paid = true;
        reRenderPaywalls();
      });
    });
    root.querySelectorAll("[data-copy-handoff]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        const id = btn.getAttribute("data-copy-handoff");
        const pre = document.getElementById("handoff-" + id);
        if (pre) {
          pre.classList.remove("hidden");
          const t = pre.textContent || "";
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(t).catch(function () {});
          }
          btn.textContent = "已顯示／已複製（示範）";
        }
      });
    });
    root.querySelectorAll("[data-concierge-demo]").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        const id = btn.getAttribute("data-concierge-demo");
        const note = document.getElementById("concierge-note-" + id);
        if (note) note.classList.remove("hidden");
        btn.textContent = "已送出示範意向";
        btn.disabled = true;
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
    if (sub) sub.textContent = "先看群組。會員可見問題、影響與「誰來解決」角色摘要；付費解鎖完整怎麼做＋DIY 清單／團隊交接／代做；看廣告僅解鎖一小部份。";

    const groups = buildGroups(state.data.issues || [])
      .filter(function (g) { return g.level !== "ok"; })
      .slice(0, 5);
    if (!groups.length) {
      box.innerHTML = '<p class="muted">目前沒有特別需要先看的項目。你可以點上面四張卡片隨意逛逛。</p>';
      return;
    }
    box.innerHTML = groups.map(renderGroupCard).join("");
    bindEvidenceToggles(box);
    bindPaywallActions(box);
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
      const adN = (state.adUnlocks && state.adUnlocks[aiUnlock]) || 0;
      const mode = state.paid ? "paid" : adN >= 1 ? "ad" : "locked";
      const aiSteps = [
        "設定品牌／產品關鍵問句，對真實 ChatGPT 等模型做提及觀測（付費能力）。",
        "收集可核對的 mention、citation、source 片段作為證據層。",
        "對照網站內容缺口，產出可執行的可見度改善步驟與草稿。",
        "修復後再測：重跑同一觀測組，比較提及是否出現或品質提升。",
      ];
      const aiWho = {
        diySummary: "站長可先整理品牌問句清單，但真實觀測需付費接線。",
        diySteps: [
          "列出 5–10 個顧客會問 AI 的品牌／產品問題。",
          "記錄目前公開內容中可被引用的來源頁。",
          "付費方案再跑真實模型觀測與再測。",
        ],
        teamHandoff: "請成長／內容團隊準備品牌問句與來源頁清單；付費開通後交觀測組執行。",
        conciergeCta: "由我們代跑 AI 提及觀測並交付證據摘要（付費服務・示範）。",
      };
      const pbAi = {
        paidSteps: aiSteps,
        paidDraftHint: "升級後可取得針對你網站的提問組與內容補強草稿（仍需真實模型證據，不會造假）。",
        verifyHint: "付費方案可重跑 AI 觀測迴圈驗證改善。",
        who: aiWho,
      };
      // reuse helpers with synthetic playbook
      const head =
        state.paid
          ? '<div class="paywall-head"><span class="lock-badge">已解鎖</span><span class="plan-chip paid">付費（完整解法）</span></div>'
          : mode === "ad"
            ? '<div class="paywall-head"><span class="lock-badge">部份解鎖</span><span class="plan-chip ad">廣告・僅 1 步</span></div>'
            : '<div class="paywall-head"><span class="lock-badge">🔒 鎖定</span><span class="plan-chip paid">付費功能</span></div>';
      let actions = "";
      if (!state.paid) {
        actions =
          '<div class="paywall-actions">' +
          '<button type="button" class="btn ghost" data-ad-unlock="' + aiUnlock + '"' +
          (adN >= 1 ? " disabled" : "") +
          ">" +
          (adN >= 1 ? "已用廣告解鎖一小部份" : "看廣告解鎖一小部份（示範）") +
          "</button>" +
          '<button type="button" class="btn" data-upgrade-paid="' + aiUnlock + '">升級付費看完整解法（示範）</button>' +
          '<p class="muted" style="margin-top:8px;font-size:.82rem">示範狀態僅本工作階段；不會呼叫 OpenAI。</p></div>';
      }
      const aiPaywall =
        '<div class="paywall' + (state.paid ? " unlocked" : "") + (mode === "ad" ? " ad-partial" : "") +
        '" data-paywall-id="' + aiUnlock + '">' +
        head +
        whoSummaryHtml(pbAi) +
        howHtml(pbAi, aiUnlock, mode) +
        whoDetailHtml(pbAi, aiUnlock, mode) +
        actions +
        "</div>";
      body.innerHTML =
        '<div class="glass panel"><h3>AI｜AI 提得到你嗎？</h3>' +
        '<div style="display:flex;gap:8px;flex-wrap:wrap;margin:12px 0">' +
        '<span class="tier unmeasured">尚未測量</span>' +
        '<span class="plan-chip paid">付費可測</span>' +
        '<span class="plan-chip member">會員免費版不測</span></div>' +
        "<p><strong>會員免費版：</strong>清楚標示「尚未測量」。AI 真實觀測屬付費；我們<strong>不測、不造假分</strong>，也<strong>絕對不會</strong>發明 GEO／AEO 分數。</p>" +
        '<p class="muted">付費接上真實提及／引用證據迴圈後，才會標成「已測量」。廣告僅能解鎖解法／DIY 的一小部份，不會讓狀態變成已測量。</p>' +
        aiPaywall +
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
    bindPaywallActions(body);
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
    ensurePlanBarDash();
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
        requireMemberThen(u, { demo: true, demoKey: btn.getAttribute("data-demo-key") });
      });
    });
  }

  $("btn-analyze").addEventListener("click", function () {
    const url = ($("url-input").value || "").trim() || "https://example.com";
    requireMemberThen(url);
  });
  $("url-input").addEventListener("keydown", function (e) {
    if (e.key === "Enter") $("btn-analyze").click();
  });
  $("btn-home").addEventListener("click", function () { show("landing"); ensurePlanBarLanding(); });
  $("btn-rescan").addEventListener("click", function () {
    requireMemberThen((state.data && state.data.sample_url) || $("url-input").value, { demo: state.mode === "demo" });
  });
  $("btn-back-pillars").addEventListener("click", closeDetail);

  initChips();
  show("landing");
  ensurePlanBarLanding();
  ensureGateModal();
  checkLiveHealth().then(function (ok) {
    if (!ok) ensureLiveNote();
  });
})();
