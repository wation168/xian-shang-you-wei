# -*- coding: utf-8 -*-
"""產出單一自包含深色 HTML dashboard（資料內嵌，file:// 可開）。"""

from __future__ import annotations

import html
import json
from datetime import datetime, timezone, timedelta
from typing import Any

from .models import Page, Issue
from .similarity import SimPair

TZ_TW = timezone(timedelta(hours=8))


def _esc(s: Any) -> str:
    return html.escape("" if s is None else str(s), quote=True)


def render_dashboard(
    pages: list[Page],
    issues: list[Issue],
    sim_pairs: list[SimPair],
    summary: dict,
    site_name: str = "SEO Scanner",
) -> str:
    generated = datetime.now(TZ_TW).strftime("%Y-%m-%d %H:%M:%S TW")

    pages_json = json.dumps([p.to_dict() for p in pages], ensure_ascii=False)
    issues_json = json.dumps([i.to_dict() for i in issues], ensure_ascii=False)
    pairs_json = json.dumps([p.to_dict() for p in sim_pairs], ensure_ascii=False)
    summary_json = json.dumps(summary, ensure_ascii=False)

    pc = summary.get("priority_counts", {})
    cs = summary.get("cluster_summary") or {}
    ls = summary.get("link_opportunity_summary") or {}

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{_esc(site_name)} — SEO Scanner v2</title>
<style>
:root {{
  --bg:#0f1419; --panel:#1a2332; --border:#2d3a4d; --text:#e7ecf3; --muted:#8b9bb4;
  --p0:#ff5c5c; --p1:#ff9f43; --p2:#f6c945; --p3:#5dade2; --ok:#2ecc71; --accent:#6c8cff;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:"Segoe UI", "Noto Sans TC", "Microsoft JhengHei", sans-serif;
  background:var(--bg); color:var(--text); line-height:1.5; }}
header {{ padding:1.25rem 1.5rem; border-bottom:1px solid var(--border);
  background:linear-gradient(180deg,#1a2332,#0f1419); position:sticky; top:0; z-index:10; }}
header h1 {{ margin:0 0 .25rem; font-size:1.35rem; }}
header .meta {{ color:var(--muted); font-size:.85rem; }}
nav.tabs {{ display:flex; gap:.5rem; padding:.75rem 1.5rem; flex-wrap:wrap;
  border-bottom:1px solid var(--border); background:var(--panel); }}
nav.tabs button {{ background:#243044; color:var(--text); border:1px solid var(--border);
  border-radius:6px; padding:.4rem .9rem; cursor:pointer; font-size:.9rem; }}
nav.tabs button.active {{ background:var(--accent); border-color:var(--accent); color:#fff; }}
main {{ padding:1.25rem 1.5rem 3rem; max-width:1400px; margin:0 auto; }}
.cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(110px,1fr)); gap:.75rem; margin-bottom:1.25rem; }}
.card {{ background:var(--panel); border:1px solid var(--border); border-radius:10px; padding:1rem; }}
.card .n {{ font-size:1.7rem; font-weight:700; }}
.card .l {{ color:var(--muted); font-size:.78rem; }}
.card.p0 .n {{ color:var(--p0); }} .card.p1 .n {{ color:var(--p1); }}
.card.p2 .n {{ color:var(--p2); }} .card.p3 .n {{ color:var(--p3); }}
.card.ok .n {{ color:var(--ok); }}
.filters {{ display:flex; gap:.75rem; flex-wrap:wrap; margin-bottom:1rem; align-items:center; }}
.filters select, .filters input {{ background:#243044; color:var(--text); border:1px solid var(--border);
  border-radius:6px; padding:.4rem .6rem; }}
table {{ width:100%; border-collapse:collapse; font-size:.88rem; }}
th, td {{ border-bottom:1px solid var(--border); padding:.55rem .6rem; text-align:left; vertical-align:top; }}
th {{ color:var(--muted); font-weight:600; position:sticky; top:60px; background:var(--panel); }}
tr:hover td {{ background:#1f2a3d; }}
.badge {{ display:inline-block; padding:.1rem .45rem; border-radius:4px; font-size:.75rem; font-weight:600; }}
.badge.P0 {{ background:var(--p0); color:#1a0000; }}
.badge.P1 {{ background:var(--p1); color:#1a0a00; }}
.badge.P2 {{ background:var(--p2); color:#1a1500; }}
.badge.P3 {{ background:var(--p3); color:#001018; }}
.badge.cat {{ background:#2a3a55; color:#c5d0e0; }}
.badge.fold {{ background:#3a4558; color:#c5d0e0; }}
.badge.hv {{ background:#2ecc71; color:#06210f; }}
.badge.disp-true_issue {{ background:#ff5c5c; color:#1a0000; }}
.badge.disp-needs_review {{ background:#f6c945; color:#1a1500; }}
.badge.disp-likely_exception {{ background:#3a4558; color:#c5d0e0; }}
.badge.disp-insufficient_evidence {{ background:#2a3a55; color:#c5d0e0; }}
.badge.conf-high {{ background:#2ecc71; color:#06210f; }}
.badge.conf-medium {{ background:#5dade2; color:#001018; }}
.badge.conf-low {{ background:#3a4558; color:#c5d0e0; }}
.understand-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:.75rem; }}
.understand-block {{ background:#0d1218; border:1px solid var(--border); border-radius:8px; padding:.75rem; }}
.understand-block h4 {{ margin:0 0 .4rem; font-size:.9rem; color:var(--accent); }}
.notes li {{ margin:.2rem 0; color:var(--muted); font-size:.85rem; }}
.mono {{ font-family:ui-monospace, Consolas, monospace; font-size:.8rem; color:#b8c5d9; }}
.panel {{ background:var(--panel); border:1px solid var(--border); border-radius:10px; padding:1rem; overflow:auto; }}
.section {{ display:none; }}
.section.active {{ display:block; }}
details {{ margin:.4rem 0; }}
summary {{ cursor:pointer; color:var(--accent); }}
pre.ev {{ white-space:pre-wrap; word-break:break-word; background:#0d1218; padding:.6rem;
  border-radius:6px; font-size:.75rem; color:#a8b8cc; max-height:200px; overflow:auto; }}
.fix {{ color:#a8e6a3; }}
.cause {{ color:#f0d9a8; }}
.cluster-grid {{ display:grid; gap:.85rem; }}
.cluster-card {{ background:var(--panel); border:1px solid var(--border); border-radius:10px; padding:1rem 1.1rem; }}
.cluster-card.folded {{ opacity:.85; border-style:dashed; }}
.cluster-card h3 {{ margin:0 0 .4rem; font-size:1.02rem; }}
.cluster-meta {{ color:var(--muted); font-size:.82rem; margin-bottom:.5rem; }}
.cluster-card ul.slugs {{ margin:.35rem 0; padding-left:1.1rem; font-size:.82rem; color:#b8c5d9; }}
.hint {{ color:var(--muted); font-size:.85rem; }}
.h-section {{ margin-top:1.25rem; }}
</style>
</head>
<body>
<header>
  <h1>{_esc(site_name)} — 本機 SEO Scanner v2</h1>
  <div class="meta">產生時間：{_esc(generated)} · 頁數：{summary.get("page_count", 0)} ·
    相似待處理：{cs.get("actionable_cluster_count", 0)} ·
    內連高價值機會：{ls.get("high_value_count", 0)} ·
    內連 pairwise：{summary.get("link_pair_count", 0)} · 可離線開啟（file://）</div>
</header>
<nav class="tabs" id="tabs">
  <button type="button" data-tab="overview" class="active">總覽</button>
  <button type="button" data-tab="issues">診斷清單</button>
  <button type="button" data-tab="similarity">相似內容</button>
  <button type="button" data-tab="links">Link Opportunities</button>
  <button type="button" data-tab="meta">Meta / i18n</button>
</nav>
<main>
  <section id="overview" class="section active">
    <div class="cards">
      <div class="card"><div class="n" id="n-pages">0</div><div class="l">掃描頁數</div></div>
      <div class="card p0"><div class="n">{pc.get("P0",0)}</div><div class="l">P0</div></div>
      <div class="card p1"><div class="n">{pc.get("P1",0)}</div><div class="l">P1</div></div>
      <div class="card p2"><div class="n">{pc.get("P2",0)}</div><div class="l">P2</div></div>
      <div class="card p3"><div class="n">{pc.get("P3",0)}</div><div class="l">P3</div></div>
      <div class="card"><div class="n">{cs.get("actionable_cluster_count",0)}</div><div class="l">相似待處理</div></div>
      <div class="card"><div class="n" id="n-link-hv">{ls.get("high_value_count",0)}</div><div class="l">內連高價值機會</div></div>
      <div class="card ok"><div class="n" id="n-link-fold">{ls.get("folded_count",0)}</div><div class="l">內連已摺疊</div></div>
    </div>

    <div class="cards" style="margin-bottom:1rem">
      <div class="card p0"><div class="n" id="n-critical">0</div><div class="l">Critical（true_issue P0/P1）</div></div>
      <div class="card p2"><div class="n" id="n-needs-review">0</div><div class="l">Needs Review</div></div>
      <div class="card ok"><div class="n" id="n-likely-exc">0</div><div class="l">Likely Exception</div></div>
      <div class="card"><div class="n" id="n-unique-ratio">—</div><div class="l">Mean unique ratio</div></div>
    </div>
    <p class="hint" style="margin:-0.4rem 0 1rem">原始偵測 ≠ 必改：上方 P0–P3 為 raw detections；請先依 disposition（true_issue）行動，likely_exception／insufficient_evidence 勿當必改清單。</p>

    <div class="panel" style="margin-bottom:1rem">
      <h3 style="margin-top:0">Website Understanding</h3>
      <p class="hint">站級結構摘要（非 Google spam 判定）。供產品判斷 Critical vs Needs Review。</p>
      <div id="site-understanding" class="understand-grid"></div>
      <ul id="understand-notes" class="notes"></ul>
    </div>

    <div class="panel" style="margin-bottom:1rem">
      <h3 style="margin-top:0">Link Opportunities（優先高價值）</h3>
      <p class="hint">嚴重度以機會／模板計，不是 pairwise 筆數。原始內連配對完整保留，可展開查看。</p>
      <div id="link-hv" class="cluster-grid"></div>
      <details class="h-section" id="link-fold-wrap">
        <summary>一般／低價值內連（已摺疊）— <span id="n-link-fold-label">0</span></summary>
        <div id="link-fold" class="cluster-grid" style="margin-top:.75rem"></div>
      </details>
    </div>

    <div class="panel" style="margin-bottom:1rem">
      <h3 style="margin-top:0">相似內容問題（模板級）</h3>
      <p class="hint">嚴重度以集群／模板計。下方「已摺疊」含合理共用／鏡像／同遊戲家族。</p>
      <div id="cluster-actionable" class="cluster-grid"></div>
      <details id="cluster-folded-wrap" style="margin-top:1rem">
        <summary>已摺疊相似 — <span id="n-fold-label">0</span> 項</summary>
        <div id="cluster-folded" class="cluster-grid" style="margin-top:.75rem"></div>
      </details>
    </div>

    <div class="panel">
      <h3 style="margin-top:0">分類計數</h3>
      <div id="cat-summary" class="mono"></div>
      <h3>相似／內連摘要（工程對照）</h3>
      <div id="sim-summary" class="mono"></div>
      <p class="hint" style="margin-bottom:0">
        修復建議中的數字／獎金／賠率一律需人工審核，勿直接上線。
      </p>
    </div>
  </section>

  <section id="issues" class="section">
    <div class="filters">
      <label>Priority <select id="f-pri"><option value="">全部</option>
        <option>P0</option><option>P1</option><option>P2</option><option>P3</option></select></label>
      <label>Category <select id="f-cat"><option value="">全部</option>
        <option>similarity</option><option>links</option><option>meta</option>
        <option>i18n</option><option>thin</option></select></label>
      <label><input type="checkbox" id="f-hide-fold" checked/> 隱藏已摺疊</label>
      <label>Disposition <select id="f-disp">
          <option value="true_issue_med" selected>Critical: true_issue + confidence≥medium</option>
          <option value="credible">Credible: true_issue + needs_review</option>
          <option value="">All dispositions</option>
          <option value="true_issue">True issue only</option>
          <option value="needs_review">Needs review</option>
          <option value="likely_exception">Likely exception</option>
          <option value="insufficient_evidence">Insufficient evidence</option>
        </select></label>
      <label>搜尋 <input id="f-q" type="search" placeholder="problem / slug…"/></label>
</div>
    <div class="panel"><table>
      <thead><tr><th>Pri</th><th>Disp</th><th>Cat</th><th>問題／原因／修復</th><th>Pages</th></tr></thead>
      <tbody id="issues-body"></tbody>
    </table></div>
  </section>

  <section id="similarity" class="section">
    <div class="panel" style="margin-bottom:1rem">
      <h3 style="margin-top:0">模板／集群視圖</h3>
      <div id="sim-clusters" class="cluster-grid"></div>
    </div>
    <div class="panel">
      <h3 style="margin-top:0">相似度 pairwise 明細（保留）</h3>
      <table>
        <thead><tr>
          <th>Pri</th><th>分類</th><th>raw</th><th>norm</th><th>drop</th><th>Lang</th><th>A</th><th>B</th>
        </tr></thead>
        <tbody id="sim-body"></tbody>
      </table>
    </div>
  </section>

  <section id="links" class="section">
    <div class="panel" style="margin-bottom:1rem">
      <h3 style="margin-top:0">Link Opportunities</h3>
      <p class="hint">template／topic／strong_pair／hub 優先；folded 預設摺疊。展開可見原始 pairwise。</p>
      <div id="link-opps-all" class="cluster-grid"></div>
    </div>
    <div class="panel">
      <h3 style="margin-top:0">內連 pairwise 明細（完整保留）</h3>
      <table>
        <thead><tr><th>Pri</th><th>sim</th><th>Lang</th><th>A</th><th>B</th></tr></thead>
        <tbody id="link-pairs-body"></tbody>
      </table>
    </div>
  </section>

  <section id="meta" class="section">
    <div class="panel"><table>
      <thead><tr><th>Pri</th><th>Cat</th><th>問題</th><th>Pages</th><th>證據</th></tr></thead>
      <tbody id="meta-body"></tbody>
    </table></div>
  </section>
</main>

<script type="application/json" id="data-pages">{pages_json}</script>
<script type="application/json" id="data-issues">{issues_json}</script>
<script type="application/json" id="data-pairs">{pairs_json}</script>
<script type="application/json" id="data-summary">{summary_json}</script>
<script>
(function() {{
  const pages = JSON.parse(document.getElementById('data-pages').textContent);
  const issues = JSON.parse(document.getElementById('data-issues').textContent);
  const pairs = JSON.parse(document.getElementById('data-pairs').textContent);
  const summary = JSON.parse(document.getElementById('data-summary').textContent);
  const clusters = summary.clusters || [];
  const linkOpps = summary.link_opportunities || [];
  const linkPairs = summary.link_pairs || [];

  document.getElementById('n-pages').textContent = summary.page_count || pages.length;
  document.getElementById('cat-summary').textContent = JSON.stringify(summary.category_counts || {{}}, null, 2);
  document.getElementById('sim-summary').textContent = JSON.stringify({{
    similarity: {{
      pairwise: summary.similarity_classifications || {{}},
      pair_count: summary.similarity_pair_count || pairs.length,
      clusters: summary.cluster_summary || {{}}
    }},
    links: {{
      pairwise: summary.link_pair_count || linkPairs.length,
      opportunities: summary.link_opportunity_summary || {{}}
    }}
  }}, null, 2);

  document.querySelectorAll('#tabs button').forEach(btn => {{
    btn.addEventListener('click', () => {{
      document.querySelectorAll('#tabs button').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(btn.dataset.tab).classList.add('active');
    }});
  }});

  function esc(s) {{
    return String(s ?? '').replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}})[c]);
  }}

  const und = summary.site_understanding || {{}};
  const rb = summary.review_buckets || {{}};
  const dc = summary.disposition_counts || {{}};
  document.getElementById('n-critical').textContent = rb.critical_true_issue ?? 0;
  document.getElementById('n-needs-review').textContent = rb.needs_review ?? dc.needs_review ?? 0;
  document.getElementById('n-likely-exc').textContent = rb.likely_exception ?? dc.likely_exception ?? 0;
  const mur = (und.template_shell_sketch || {{}}).mean_unique_ratio;
  document.getElementById('n-unique-ratio').textContent =
    (mur === null || mur === undefined) ? '—' : mur;
  (function renderUnderstanding() {{
    const box = document.getElementById('site-understanding');
    if (!box) return;
    const lang = und.languages || {{}};
    const shell = und.template_shell_sketch || {{}};
    const hubs = (und.top_hubs_by_inbound || []).slice(0, 6)
      .map(h => esc(h.slug) + ' (' + h.inbound_degree + ')')
      .join(', ') || '—';
    const typeHist = JSON.stringify(und.page_type_histogram || {{}}, null, 0);
    const csum = und.similarity_clusters || {{}};
    box.innerHTML = `
      <div class="understand-block"><h4>Languages</h4>
        <div class="mono">monolingual=${{!!lang.monolingual}} · primary=${{esc(lang.primary_lang)}} · distinct=${{lang.distinct_langs ?? 0}}</div>
        <pre class="ev">${{esc(JSON.stringify(lang.lang_counts || {{}}, null, 2))}}</pre>
      </div>
      <div class="understand-block"><h4>Page types</h4>
        <pre class="ev">${{esc(typeHist)}}</pre>
        <p class="hint" style="margin:.35rem 0 0">page_type 為結構啟發式，非正式標註／ground truth。</p>
      </div>
      <div class="understand-block"><h4>Template shell sketch</h4>
        <div class="mono">unique≈${{shell.mean_unique_ratio ?? '—'}} · shell_types=${{shell.shell_token_types ?? '—'}} · mean_tokens=${{shell.mean_body_tokens ?? '—'}} · sampled=${{shell.sampled_pages ?? 0}}</div>
        <p class="hint" style="margin:.4rem 0 0">Structural estimate only — not a spam verdict.</p>
      </div>
      <div class="understand-block"><h4>Similarity / hubs</h4>
        <div class="mono">pairs=${{und.similarity_pair_count ?? 0}} · clusters=${{csum.cluster_count ?? 0}} · actionable=${{csum.actionable_cluster_count ?? 0}}</div>
        <div class="mono" style="margin-top:.35rem">top hubs: ${{hubs}}</div>
      </div>`;
    const notes = document.getElementById('understand-notes');
    notes.innerHTML = (und.notes || []).map(n => '<li>' + esc(n) + '</li>').join('');
  }})();


  function renderSimCard(c) {{
    const slugPreview = (c.slugs || []).slice(0, 12).map(s => '<li class="mono">' + esc(s) + '</li>').join('');
    const more = (c.slugs || []).length > 12 ? '<li>…共 ' + c.slugs.length + ' 個 slug</li>' : '';
    const pairsHtml = (c.pair_refs || []).slice(0, 40).map(p =>
      '<tr><td>' + esc(p.lang) + '</td><td class="mono">' + esc(p.slug_a) + '</td><td class="mono">' +
      esc(p.slug_b) + '</td><td>' + p.raw_sim + '</td><td>' + p.norm_sim + '</td><td>' +
      esc(p.classification) + '</td></tr>'
    ).join('');
    const foldBadge = c.folded ? ' <span class="badge fold">folded</span>' : '';
    return `
      <div class="cluster-card ${{c.folded ? 'folded' : ''}}">
        <h3><span class="badge ${{esc(c.priority)}}">${{esc(c.priority)}}</span>
          ${{esc(c.title)}}${{foldBadge}}</h3>
        <div class="cluster-meta">
          頁 ${{c.page_count}} · 語系 ${{c.lang_count}}（${{esc((c.langs||[]).join(', '))}}）·
          pairwise ${{c.pair_count}} · norm ${{c.norm_min}}–${{c.norm_max}} ·
          bucket ${{esc(c.bucket)}} / ${{esc(c.kind)}}
        </div>
        <div class="cause">原因：${{esc(c.why)}}</div>
        <div class="fix">修復：${{esc(c.fix)}}</div>
        <details>
          <summary>展開 slug／語系／配對明細</summary>
          <ul class="slugs">${{slugPreview}}${{more}}</ul>
          <table><thead><tr><th>Lang</th><th>A</th><th>B</th><th>raw</th><th>norm</th><th>class</th></tr></thead>
          <tbody>${{pairsHtml || '<tr><td colspan="6">無</td></tr>'}}</tbody></table>
        </details>
      </div>`;
  }}

  function renderLinkCard(o) {{
    const slugPreview = (o.slugs || []).slice(0, 12).map(s => '<li class="mono">' + esc(s) + '</li>').join('');
    const more = (o.slugs || []).length > 12 ? '<li>…共 ' + o.slugs.length + ' 個 slug</li>' : '';
    const pairsHtml = (o.pair_refs || []).slice(0, 60).map(p =>
      '<tr><td><span class="badge ' + esc(p.priority) + '">' + esc(p.priority) + '</span></td><td>' +
      esc(p.lang) + '</td><td class="mono">' + esc(p.slug_a) + '</td><td class="mono">' +
      esc(p.slug_b) + '</td><td>' + p.link_sim + '</td></tr>'
    ).join('');
    const foldBadge = o.folded ? ' <span class="badge fold">folded</span>' : '';
    const hvBadge = o.high_value ? ' <span class="badge hv">high value</span>' : '';
    return `
      <div class="cluster-card ${{o.folded ? 'folded' : ''}}">
        <h3><span class="badge ${{esc(o.priority)}}">${{esc(o.priority)}}</span>
          ${{esc(o.title)}}${{hvBadge}}${{foldBadge}}</h3>
        <div class="cluster-meta">
          bucket ${{esc(o.bucket)}} / ${{esc(o.kind)}} ·
          頁 ${{o.page_count}} · 語系 ${{o.lang_count}}（${{esc((o.langs||[]).join(', '))}}）·
          pairwise ${{o.pair_count}} · sim ${{o.sim_min}}–${{o.sim_max}}
        </div>
        <div class="cause">原因：${{esc(o.why)}}</div>
        <div class="fix">修復：${{esc(o.fix)}}</div>
        <details>
          <summary>展開原始 pairwise（${{o.pair_count}}）</summary>
          <ul class="slugs">${{slugPreview}}${{more}}</ul>
          <table><thead><tr><th>Pri</th><th>Lang</th><th>A</th><th>B</th><th>sim</th></tr></thead>
          <tbody>${{pairsHtml || '<tr><td colspan="5">無</td></tr>'}}</tbody></table>
        </details>
      </div>`;
  }}

  const act = clusters.filter(c => !c.folded);
  const fold = clusters.filter(c => c.folded);
  document.getElementById('cluster-actionable').innerHTML =
    act.length ? act.map(renderSimCard).join('') :
    '<p class="hint">沒有待處理的相似模板集群。</p>';
  document.getElementById('cluster-folded').innerHTML =
    fold.length ? fold.map(renderSimCard).join('') : '<p class="hint">無</p>';
  document.getElementById('n-fold-label').textContent = String(fold.length);
  document.getElementById('sim-clusters').innerHTML =
    clusters.map(renderSimCard).join('') || '<p class="hint">無相似集群</p>';

  const linkHv = linkOpps.filter(o => o.high_value && !o.folded);
  const linkFold = linkOpps.filter(o => o.folded || !o.high_value);
  document.getElementById('link-hv').innerHTML =
    linkHv.length ? linkHv.map(renderLinkCard).join('') :
    '<p class="hint">沒有高價值內連機會。</p>';
  document.getElementById('link-fold').innerHTML =
    linkFold.length ? linkFold.map(renderLinkCard).join('') : '<p class="hint">無</p>';
  document.getElementById('n-link-fold-label').textContent = String(linkFold.length);
  document.getElementById('link-opps-all').innerHTML =
    linkOpps.map(renderLinkCard).join('') || '<p class="hint">無內連機會</p>';

  function renderIssues() {{
    const pri = document.getElementById('f-pri').value;
    const cat = document.getElementById('f-cat').value;
    const disp = document.getElementById('f-disp').value;
    const hideFold = document.getElementById('f-hide-fold').checked;
    const q = (document.getElementById('f-q').value || '').toLowerCase();
    const tb = document.getElementById('issues-body');
    tb.innerHTML = '';
    issues.forEach(it => {{
      if (pri && it.priority !== pri) return;
      if (cat && it.category !== cat) return;
      const ev = it.evidence || {{}};
      const d0 = ev.disposition || 'needs_review';
      const c0 = (ev.confidence || 'medium').toLowerCase();
      const confRank = {{low: 0, medium: 1, med: 1, high: 2}};
      if (disp === 'true_issue_med') {{
        if (d0 !== 'true_issue') return;
        if ((confRank[c0] ?? 1) < 1) return; // require medium+
      }} else if (disp === 'credible') {{
        if (d0 !== 'true_issue' && d0 !== 'needs_review') return;
      }} else if (disp && d0 !== disp) return;
      if (hideFold && ev.folded) return;
      const blob = (it.problem + ' ' + it.cause + ' ' + (it.pages||[]).join(' ') + ' ' + (ev.disposition||'') + ' ' + (ev.confidence||'') + ' ' + (ev.kind||'') + ' ' + (ev.archive_date_demoted ? 'archive_date_demoted' : '') + ' ' + (ev.demotion_reason||'')).toLowerCase();
      if (q && !blob.includes(q)) return;
      const foldMark = ev.folded ? ' <span class="badge fold">folded</span>' : '';
      const d = ev.disposition || 'needs_review';
      const c = ev.confidence || 'medium';
      const dnf = ev.do_not_fix_if ? ('<br/><span class="hint">do_not_fix_if：' + esc(ev.do_not_fix_if) + '</span>') : '';
      const tsm = ev.template_shell_metrics || null;
      const shellNote = tsm ? ('<br/><span class="hint">shell unique — cluster: ' + esc(tsm.cluster_mean_unique_ratio) + ' · site: ' + esc(tsm.site_mean_unique_ratio) + '</span>') : '';
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><span class="badge ${{esc(it.priority)}}">${{esc(it.priority)}}</span></td>
        <td><span class="badge disp-${{esc(d)}}">${{esc(d)}}</span><br/>
            <span class="badge conf-${{esc(c)}}">${{esc(c)}}</span></td>
        <td><span class="badge cat">${{esc(it.category)}}</span></td>
        <td>
          <strong>${{esc(it.problem)}}</strong>${{foldMark}}<br/>
          <span class="cause">原因：${{esc(it.cause)}}</span><br/>
          <span class="fix">修復：${{esc(it.fix)}}</span>${{dnf}}${{shellNote}}
          <details><summary>evidence</summary><pre class="ev">${{esc(JSON.stringify(it.evidence, null, 2))}}</pre></details>
        </td>
        <td class="mono">${{esc((it.pages||[]).slice(0,20).join(', '))}}${{(it.pages||[]).length>20?'…':''}}</td>`;
      tb.appendChild(tr);
    }});
  }}

  ['f-pri','f-cat','f-disp','f-q','f-hide-fold'].forEach(id => {{
    const el = document.getElementById(id);
    el.addEventListener('input', renderIssues);
    el.addEventListener('change', renderIssues);
  }});
  renderIssues();

  const simBody = document.getElementById('sim-body');
  pairs.forEach(p => {{
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><span class="badge ${{esc(p.priority)}}">${{esc(p.priority)}}</span></td>
      <td>${{esc(p.classification)}}</td>
      <td>${{p.raw_sim}}</td><td>${{p.norm_sim}}</td><td>${{p.drop}}</td>
      <td>${{esc(p.lang)}}</td>
      <td class="mono">${{esc(p.slug_a)}}</td>
      <td class="mono">${{esc(p.slug_b)}}</td>`;
    simBody.appendChild(tr);
  }});

  const lpBody = document.getElementById('link-pairs-body');
  linkPairs.forEach(p => {{
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><span class="badge ${{esc(p.priority)}}">${{esc(p.priority)}}</span></td>
      <td>${{p.link_sim ?? ''}}</td>
      <td>${{esc(p.lang)}}</td>
      <td class="mono">${{esc(p.slug_a)}}</td>
      <td class="mono">${{esc(p.slug_b)}}</td>`;
    lpBody.appendChild(tr);
  }});

  const metaBody = document.getElementById('meta-body');
  issues.filter(i => i.category === 'meta' || i.category === 'i18n' || i.category === 'thin').forEach(it => {{
    const ev = it.evidence || {{}};
    const d = ev.disposition || '';
    const c = ev.confidence || '';
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><span class="badge ${{esc(it.priority)}}">${{esc(it.priority)}}</span></td>
      <td><span class="badge cat">${{esc(it.category)}}</span>
        ${{d ? ' <span class="badge disp-' + esc(d) + '">' + esc(d) + '</span>' : ''}}
        ${{c ? ' <span class="badge conf-' + esc(c) + '">' + esc(c) + '</span>' : ''}}</td>
      <td><strong>${{esc(it.problem)}}</strong><br/><span class="cause">${{esc(it.cause)}}</span>
        ${{ev.do_not_fix_if ? '<br/><span class="hint">do_not_fix_if：' + esc(ev.do_not_fix_if) + '</span>' : ''}}</td>
      <td class="mono">${{esc((it.pages||[]).join(', '))}}</td>
      <td><pre class="ev">${{esc(JSON.stringify(it.evidence, null, 2))}}</pre></td>`;
    metaBody.appendChild(tr);
  }});
}})();
</script>
</body>
</html>
"""
