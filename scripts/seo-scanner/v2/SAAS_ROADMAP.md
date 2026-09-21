# SoftGlow SEO Scanner SaaS — Product Roadmap (Scanner-only)

> Scope: `scripts/seo-scanner/v2/` only. SoftGlow website HTML under `backend/frontend/` is out of scope for Scanner work.
> Updated: 2026-09-21 (Asia/Taipei)

## Current architecture (v2)

```
run_scan.py
  → parse.scan_root          # static HTML → Page[]
  → diagnose.run_all_checks
       → similarity + sim_clusters     # pairwise → template clusters
       → checks_meta / checks_links / checks_i18n
       → link_opportunities            # pairwise → opportunity cards
       → understanding.build_site_understanding   # site sketch
       → disposition.apply_disposition_rules      # confidence / disposition
  → report.render_dashboard  # self-contained dark HTML (file://)
```

**Issue model:** `problem / cause / fix / priority / evidence / pages`  
**Phase 2 evidence fields:** `confidence` (`high|medium|low`), `disposition` (`true_issue|needs_review|likely_exception|insufficient_evidence`), optional `do_not_fix_if`.  
**Website Understanding:** page_count, lang profile (monolingual?), page_type_histogram, template_shell_sketch (unique ratio / shell tokens), top hubs, cluster summary notes.

**Design invariants**

- High raw cosine ≠ automatic SEO defect (`shared_template_ok` / folded clusters exist).
- No SoftGlow-specific slug hardcoding for FP suppression.
- Prefer additive judgment layer over deleting detections.
- Do not tune thresholds solely to zero SoftGlow P0/P1/P2.

---

## Phased plan (product)

### Phase 1 — Local diagnostic engine *(partially done)*
- [x] Static HTML parse (multi layout heuristics)
- [x] Similarity classification + cluster aggregation
- [x] Meta / thin / links / i18n checks
- [x] Dashboard HTML + fixtures / similarity tests
- [x] Benchmark cases BC-01..06 + second-site sample
- [ ] Package as installable CLI with stable exit codes / JSON export

### Phase 2 — Judgment layer + generic FP reduction *(in progress — this milestone)*
- [x] Website Understanding object on each scan
- [x] Issue confidence / disposition / do_not_fix_if
- [x] Template shell metrics (structural; not “Google spam”)
- [x] Monolingual i18n soft-disposition (missing en/x-default → likely_exception)
- [x] Small high-unique mono doc trees: encyclopedia mesh → softer disposition
- [ ] Per-cluster unique ratio (beyond site-wide sketch)
- [ ] Dashboard UX polish: Critical vs Needs Review as primary product buckets

### Phase 3 — Multi-site confidence calibration
- Expand benchmark corpus beyond SoftGlow + python-tutorial
- Precision/recall tracking for disposition classes
- Explicit “insufficient_evidence” paths for thin signal

### Phase 4 — Actionability scoring
- Rank by expected SEO impact × fix effort × confidence
- Separate “detect” from “recommend change”
- Safe autofix candidates vs human-only

### Phase 5 — GSC / analytics enrichment
- Optional GSC CSV (already stubbed) → deeper impression/click priors
- Zero-impression boost only for actionable buckets (existing) → refine

### Phase 6 — SaaS surface (read-only first)
- Auth, project, upload zip / connect storage of static export
- Scan history, diff between runs
- No auto-write to customer production HTML in v1 SaaS

### Phase 7 — Collaboration / workflow
- Issue assignment, ignore/snooze with reason codes
- Export Jira/Linear/CSV

### Phase 8 — Continuous monitoring
- Scheduled re-scan of static mirrors / staging
- Regression alerts when new template_shell clusters appear

### Phase 9 — Optional assistive rewrites
- Draft unique-content outlines (human approve)
- Never invent regulated numbers (lottery/odds)

### Phase 10 — Scale & packaging
- Multi-tenant quotas, billing, SLAs
- Horizontal scan workers, incremental parse

---

## Phase 2 acceptance checklist

| Check | Expected |
|-------|----------|
| `SAAS_ROADMAP.md` exists | Yes |
| Dashboard Overview shows Website Understanding | Yes |
| Issues show disposition + confidence | Yes |
| python-tutorial: similarity clusters = 0 | Still |
| python-tutorial: i18n/mesh not Critical spam | Softened to likely_exception / lower P |
| SoftGlow patterns: template_shell still surfaces | Yes |
| Unit tests for unique ratio / monolingual / disposition | Pass |
| No SoftGlow frontend HTML edits | Yes |

---

## How to run (scanner)

```bat
cd /d D:\xian-shang-you-wei\scripts\seo-scanner\v2
.venv\Scripts\activate
python tests\test_similarity.py
python tests\test_phase2_understanding.py
python run_scan.py --root "C:/Users/user/Documents/seo-scanner-handoff/benchmark/second-site/python-tutorial" --site-name "python-tutorial" --out dashboard_second_site_python_tutorial.html
python run_scan.py --root "D:/xian-shang-you-wei/backend/frontend/patterns" --lang en --site-name "patterns-en" --out dashboard_patterns_en_phase2.html
```

## Product wording (Overview)

- **原始偵測 ≠ 必改**：raw priority counts are detections; act on disposition (	rue_issue) first.
- page_type is a structural heuristic for understanding/disposition — not UI ground truth.



## Product positioning (2026-09-21)

See `PRODUCT_POSITIONING.md`. Scanner is the **Website Intelligence Engine** under AI Search & Website Intelligence — not five separate SEO/GEO/AEO products.
