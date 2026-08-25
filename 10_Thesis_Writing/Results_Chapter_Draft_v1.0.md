# Chapter 4: Results (Draft v1.0)

*Draft prose for the thesis Results chapter. Every statistic below is reproduced from the RQ-specific final-results documents (`09_Statistical_Analysis/RQ{1,2,3,4,5}/`) and the curated tables/figures in `13_Tables/`/`12_Figures/` (numbered `Tbl4.x`/`Fig4.x` throughout, matching the citations below). Nothing in this chapter is a new computation.*

---

## 4.1 Dataset overview

The final dataset comprises 500 LinkedIn profiles of self-identified AI leaders, annotated across six ALCSM dimensions (D1–D6), yielding 3,000 profile × dimension labels. Annotation followed a frozen, researcher-reviewed protocol; the resulting dataset (`ALCSM_Final_Human_Annotation_v1.1.xlsx`) is the single gold standard used throughout this chapter and was not modified at any point during the analyses reported here.

The corpus is complemented by 201 job postings comprising 1,558 individual requirement records (RQ2), 24 consented expert survey respondents providing content-assessment evidence (RQ3), a 75-profile independently double-coded reliability subset (RQ3), and per-dimension NLP baseline predictions evaluated against the same gold standard (RQ5). Table 4.1 and Table 4.2 (below, §4.2) summarize the annotation dataset's own descriptive properties; subsequent sections address each research question in turn.

## 4.2 RQ1 — LinkedIn profile descriptive patterns

Dimension scores show markedly different distributional shapes (Table 4.1; Figure 4.1). D1 (Formal Education), D3 (Practical AI Experience), and D6 (AI Industry/Application Breadth) span the full nominal 0–5 range, while D2 (Professional Certifications) never exceeds a score of 1 and D4 (Technical Contributions) never exceeds 3 — properties of what the underlying LinkedIn data actually contains (no certification issue/expiry metadata; no technical-contribution verification metadata), not artifacts of the scoring procedure. D5 (Leadership & Strategic Responsibility) is heavily concentrated at score 3 (87.0% of all 500 profiles).

Missingness (Table 4.2; Figure 4.2) also varies sharply by dimension: D5 has no unavailable cases at all (0.0%), while D4 (65.0%) and D2 (53.2%) have the highest rates — the majority of profiles simply do not state technical-contribution or certification evidence on LinkedIn. D3 and D6 each have exactly three unavailable profiles, all attributable to the same three profiles lacking any listed professional experience.

Cross-tabulating mean dimension score by title category (Table 4.3) shows senior-sounding but more technically scoped titles ("Lead") associated with the lowest D1 and D5 means among categories with a meaningful sample size, consistent with D5's definition privileging demonstrated strategic scope over title alone.

## 4.3 RQ2 — Job posting requirements vs. profile credential signals

Of the 1,558 requirement records extracted from 201 postings, 51.3% do not map to any ALCSM dimension and are retained as `NOT_DIRECTLY_MAPPED` (Table 4.4) — these are not forced into D1–D6. Among mapped requirements, demand concentrates heavily in D5 (436 requirements, 28.0% of the total) and D3 (185, 11.9%), while D2, D4, and D6 are only sparsely represented (17, 4, and 1 requirements respectively).

Comparing requirement volume (demand-side) against mean held score (supply-side) without computing a numeric gap (Table 4.5; Figure 4.3, Figure 4.4) shows D5 and D3 as cases where demand and supply point the same direction — both heavily requested and comparatively highly held. D6 shows the starkest asymmetry in the dataset (Table 4.6): while 99.4% of profiles carry some observable D6 evidence, only 0.06% of requirement records (a single record, of 1,558) state anything mappable to D6 — job postings essentially never phrase AI industry/application breadth as a discrete stated requirement, even though the profile side shows it almost universally.

## 4.4 RQ3 — ALCSM construction and validation

Two independent lines of evidence are reported, neither treated as sufficient on its own, and both reported per dimension without pooling.

**Inter-rater reliability** (Table 4.7): D1 (α = .944) and D6 (α = 1.000, non-degenerate) show strong reproducibility across a 75-profile independently double-coded subset. D2 and D4 also reach α = 1.000 but on degenerate, near-zero-variance samples (D2's present-only population is uniformly scored 1; D4's usable sample is small, n=26) and are not read as evidence of strong discrimination. D3 (α = .102) shows a systematic, one-directional 3→4 calibration disagreement between the two raters, concentrated at the score boundary where cumulative AI-experience duration and senior-title language must be weighed. D5 (α = .246) shows substantial range restriction (one rater concentrated 68 of 75 ratings at a single score) combined with a narrower, genuine boundary disagreement around seniority-title language versus explicit strategic scope (Director/Head/VP boundary cases).

**Expert content-assessment survey** (N = 24; Table 4.8): all six dimensions were rated moderately-to-highly relevant (means 3.25–4.33 of 5), with D3 rated most relevant and most frequently selected as most important (9 of 24 respondents). Overall framework appropriateness was rated 3.42 of 5. The distinctiveness item received a 0% response rate across all 24 respondents, a stated limitation of the survey instrument rather than a withheld finding.

No composite reliability or validity score is computed anywhere in this section — the six dimensions are reported and read independently, consistent with ALCSM's formative measurement design.

## 4.5 RQ4 — Observable professional impact

The planned criterion-validity analysis could not be conducted. The four defined external criterion variables (network reach, content engagement, recognition count, seniority progression rate) were not collected in any form during this project's data-collection phase — verified against every processed data source and the project database. This is reported as an unresolved empirical question and a concrete direction for future work (§4.5 continues in the Discussion chapter, §5), not as a null result or an estimated effect.

## 4.6 RQ5 — NLP baseline performance

A minimal, local, reproducible TF-IDF + Ridge regression baseline was trained and evaluated independently for each of the six dimensions (Table 4.9), explicitly as a proof-of-concept for RQ5, not a production-ready assessment system.

| Dim | Exact agreement | Weighted κ | Majority baseline | Reading |
|---|---|---|---|---|
| D1 | 29.5% | .283 | 28.4% | Modest signal above baseline. |
| D2 | 100.0% | 1.000 | 100.0% | Degenerate — evaluated data are effectively one-class. |
| D3 | 52.0% | .399 | 35.0% | Strongest genuine NLP signal. |
| D4 | 62.9% | −.022 | 71.4% | Below baseline. |
| D5 | 87.0% | .260 | 87.0% | Ties an 87%-majority-class floor; 87% accuracy is not itself evidence of strong predictive performance. |
| D6 | 44.0% | .238 | 48.0% | Below baseline. |

D3's confusion matrix (Figure 4.5) shows predictions concentrated at the middle-to-high end of the scale, correctly capturing the bulk of gold-standard scores 3 and 4. D6's confusion matrix (Figure 4.6) shows predictions clustering at scores 1–2 even where gold-standard scores of 3–5 occur, consistent with a bag-of-words representation's limited ability to aggregate distinct-industry counts across a profile's full experience history.

Notably, D3 shows the strongest NLP signal of any dimension despite showing the weakest human inter-rater reliability (§4.4) — reported as an interesting asymmetry between two different forms of agreement, not as evidence resolving D3's reliability limitation.

---

*Sources: `RQ1_Final_Results_v1.0.md`, `RQ2_Final_Results_v1.0.md`, `RQ3_Final_Results_Package_v1.0.md`, `RQ4_Final_Status_v1.0.md`, `RQ5_NLP_Final_Results_v1.0.md`. Table/figure numbers match `13_Tables/`/`12_Figures/`. No canonical source file modified; no composite score, weight, or classification band computed anywhere in this chapter.*
