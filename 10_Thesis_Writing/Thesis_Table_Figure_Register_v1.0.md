# Thesis Table/Figure Register v1.0

**Purpose:** one row per thesis table/figure, with an editorial essential/optional judgment to help keep the final thesis concise. 9 tables + 6 figures currently exist (`13_Tables/`, `12_Figures/`); this register recommends 10 as essential and 5 as optional (cuttable if space-constrained) — not a mandate, a recommendation you can override.
**Author:** Samiksha Dhere (researcher) — prepared with Claude Code assistance

---

## Tables

| # | Title | RQ | Source | Chapter placement | Essential/Optional |
|---|---|---|---|---|---|
| Tbl 4.1 | Dimension Score Distribution | RQ1 | `RQ1_Final_Results_v1.0.md` §1 | 4.2 | **Essential** — core RQ1 finding, cited throughout Results and Discussion. |
| Tbl 4.2 | Missingness by Dimension | RQ1 | `RQ1_Final_Results_v1.0.md` §2 | 4.2 | **Essential** — needed to correctly interpret every other dimension-level result (n varies by dimension because of this). |
| Tbl 4.3 | Mean Score by Title Category | RQ1 | `RQ1_Final_Results_v1.0.md` §3 | 4.2 | Optional — supporting cross-tabulation, not cited by any headline finding in Results/Discussion source packs. |
| Tbl 4.4 | Requirement Counts by Dimension | RQ2 | `RQ2_Final_Results_v1.0.md` §1 | 4.3 | **Essential** — establishes the 51.3% NOT_DIRECTLY_MAPPED headline figure. |
| Tbl 4.5 | Supply vs. Demand Frequency | RQ2 | `RQ2_Final_Results_v1.0.md` §3 | 4.3 | Optional — same underlying numbers as Tbl 4.1 (held level) + Tbl 4.4 (demand) combined; Fig 4.4 already visualizes the same comparison. |
| Tbl 4.6 | D6 Profile-vs-Posting Asymmetry | RQ2 | `RQ2_Final_Results_v1.0.md` §4 | 4.3 | **Essential** — the single most-cited RQ2 finding in the Discussion chapter (99.4% vs. 0.06%). |
| Tbl 4.7 | Reliability (all six dimensions) | RQ3 | `RQ3_Final_Results_Package_v1.0.md` §C | 4.4 | **Essential** — the thesis's central methodological result. |
| Tbl 4.8 | Expert Survey Summary | RQ3 | `RQ3_Final_Results_Package_v1.0.md` §B | 4.4 | **Essential** — the only table carrying the survey's relevance/appropriateness/most-important-dimension figures; no figure covers this content. |
| Tbl 4.9 | NLP Performance (all six dimensions) | RQ5 | `RQ5_NLP_Final_Results_v1.0.md` | 4.6 | **Essential** — core RQ5 result, every NLP figure cited in Discussion traces here. |

## Figures

| # | Title | RQ | Source | Chapter placement | Essential/Optional |
|---|---|---|---|---|---|
| Fig 4.1 | Dimension Score Distributions (small multiples) | RQ1 | `RQ1_Final_Results_v1.0.md` §1 | 4.2 | **Essential** — visual complement to Tbl 4.1, makes the range-restriction pattern (D2/D4/D5 vs. D1/D3/D6) immediately visible in a way the table alone does not. |
| Fig 4.2 | Missingness by Dimension (stacked bar) | RQ1 | `RQ1_Final_Results_v1.0.md` §2 | 4.2 | Optional — Tbl 4.2 already conveys the same six numbers adequately in a compact form. |
| Fig 4.3 | Requirement Volume by Dimension | RQ2 | `RQ2_Final_Results_v1.0.md` §1 | 4.3 | Optional — redundant with Tbl 4.4's data. |
| Fig 4.4 | Demand Volume vs. Held Level (dual-axis) | RQ2 | `RQ2_Final_Results_v1.0.md` §3 | 4.3 | **Essential** — the dual-axis view is the clearest way to show the D5/D3-aligned vs. D6-asymmetric pattern in one image; supports the Discussion's demand/supply asymmetry section directly. |
| Fig 4.5 | D3 Confusion Matrix | RQ5 | `RQ5_NLP_Final_Results_v1.0.md` | 4.6 | **Essential** — visualizes the thesis's most-discussed NLP finding (strongest signal, weakest human reliability); the concentration pattern at scores 3/4 is only visible in the matrix, not the summary table. |
| Fig 4.6 | D6 Confusion Matrix | RQ5 | `RQ5_NLP_Final_Results_v1.0.md` | 4.6 | Optional — the underperformance itself is already fully stated in Tbl 4.9; keep only if you want the visual contrast with Fig 4.5 (best case vs. weak case) for narrative symmetry. |

## Summary

| | Essential | Optional | Total |
|---|---|---|---|
| Tables | 6 | 3 | 9 |
| Figures | 3 | 3 | 6 |
| **All outputs** | **9** | **6** | **15** |

**If you need to cut for length or a stricter thesis table/figure budget, cut from the Optional column first** (Tbl 4.3, Tbl 4.5, Fig 4.2, Fig 4.3, Fig 4.6) — none of the Results/Discussion source-pack prose depends on them by name. **RQ4 correctly has zero tables/figures** (no results exist to display).

---

*No table or figure content was changed by this register — it is a placement/priority index only, referencing the already-produced files in `13_Tables/`/`12_Figures/`.*
