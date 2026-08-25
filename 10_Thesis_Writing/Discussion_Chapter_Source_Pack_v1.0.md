# Discussion Chapter Source Pack v1.0

**Purpose:** organized, cited raw material for Chapter 5 (Discussion), one section per requested theme. Each bullet is a claim already supported by a specific project document — turn into thesis prose in your own voice. Claims kept at MSc-appropriate scope: read from measured results, never asserted beyond what those results show. Compare against `Discussion_Chapter_Draft_v1.0.md` (prior session's full-prose draft covering the same ground) if a ready-written paragraph is more useful than raw bullets for a given point.
**Author:** Samiksha Dhere (researcher) — prepared with Claude Code assistance

---

## Practical AI Experience (D3) as dominant signal

- D3 was rated the single most relevant dimension by expert survey respondents (mean 4.33/5, highest of all six) and the most frequently chosen "most important" dimension (9 of 24, 37.5%). Source: `RQ3_Final_Results_Package_v1.0.md` §B.
- D3 produced the strongest genuine NLP baseline signal of any dimension (52.0% exact agreement vs. 35.0% majority baseline, weighted κ=.399 — the widest margin over baseline of any dimension). Source: `RQ5_NLP_Final_Results_v1.0.md`.
- D3 simultaneously showed the **weakest** human inter-rater reliability of any dimension (α=.102). Source: `RQ3_Final_Results_Package_v1.0.md` §C.
- The D3 disagreement pattern is not random noise: 100% one-directional (Rater B always scored higher, 34/34 disagreements), concentrated at the 3→4 score boundary (18/34, 52.9%). Source: `RQ3_Reliability_Final_Interpretation_v1.0.md` §3; `D3_D5_Disagreement_Analysis_v1.0.xlsx`.
- **MSc-appropriate framing:** D3 can be discussed as the dimension experts and an automated model both find most tractable to engage with from surface evidence, while the precise scoring threshold (how to count cumulative AI-experience duration across multiple listed roles) remains under-specified enough to produce systematic rater disagreement. This is a claim about *this dataset and this rulebook's current wording*, not a general claim about "practical experience" as a construct.

## Difficulty of coding leadership/strategic scope (D5)

- D5 population is heavily concentrated: 87.0% of all 500 profiles score exactly 3. Source: `RQ1_Final_Results_v1.0.md` §1.
- D5 inter-rater alpha is low (.246) despite high raw agreement (85.3%) — driven by Rater A concentrating 68 of 75 ratings (90.7%) at a single score. Source: `RQ3_Final_Results_Package_v1.0.md` §C; `Reliability_Results_v1.1.xlsx`.
- D5 disagreements (11 of 75 pairs) are bidirectional (6 Rater-A-higher, 5 Rater-B-higher), unlike D3's one-directional pattern — a different disagreement character. Source: `RQ3_Reliability_Final_Interpretation_v1.0.md` §4.
- D5 is the only dimension coded "low" verifiability in the frozen dimension configuration (vs. D1's "high"). Source: `02_Framework_Development/ALCSM_v1.1_Scoring_Framework.md` §1, "Verifiability annotation."
- D5's NLP baseline result (87.0% exact, ties its majority-class baseline exactly) must not be read as strong predictive performance — it is the floor set by the 87% class imbalance. Source: `RQ5_NLP_Final_Results_v1.0.md`.
- **MSc-appropriate framing:** the specific residual disagreement (Director/Head/VP boundary cases, whether a title's own wording counts as sufficient "strategic language") is a narrow, identifiable coding-rulebook ambiguity — appropriate to name as a specific limitation, not to generalize into a claim that "leadership is unmeasurable."

## Industry/Application Breadth (D6)

- D6 shows strong, non-degenerate inter-rater reliability (α=1.000, full range used, 5 categories, identical rater distributions — unlike D2/D4's degenerate perfect scores). Source: `RQ3_Final_Results_Package_v1.0.md` §C.
- D6 spans the full 0–5 range in the population data (mean 1.77, median 2). Source: `RQ1_Final_Results_v1.0.md` §1.
- D6 shows near-universal profile-side observability (99.4%, 497/500) alongside near-total posting-side absence (0.06%, 1/1,558). Source: `RQ2_Final_Results_v1.0.md` §4.
- D6's NLP baseline underperforms its majority baseline (44.0% vs. 48.0%, κ=.238); confusion matrix shows predictions clustering at scores 1–2 even where gold scores of 3–5 occur. Source: `RQ5_NLP_Final_Results_v1.0.md`; `ALCSM_Fig4.6_RQ5_ConfusionMatrix_D6_v1.0.png`.
- **MSc-appropriate framing:** the NLP underperformance can be discussed as *consistent with* a bag-of-words model's inability to aggregate/count distinct values across repeated structured fields — flagged explicitly in the source report as a plausible mechanistic explanation, not a confirmed cause (no ablation study was run).

## Demand/supply asymmetry (RQ2)

- 51.3% of all requirement text does not map to any ALCSM dimension (NOT_DIRECTLY_MAPPED), preserved as its own category, never forced into D1–D6. Source: `RQ2_Final_Results_v1.0.md` §1.
- D5 and D3 show demand (requirement volume) and supply (held level) pointing the same direction — both heavily represented on both sides. Source: `RQ2_Final_Results_v1.0.md` §3.
- D2 shows both sides agreeing it is a minor signal (17 requirements, mean held 0.47). Source: same.
- D6 shows the sharpest asymmetry in the dataset (§ above). Source: same.
- **MSc-appropriate framing:** this is a description of *what this specific corpus of 201 postings states*, not a claim about employer preferences generally — the postings were not sampled to be representative of any defined labor market.

## Expert content-assessment findings

- All six dimensions rated moderately-to-highly relevant (means 3.25–4.33/5) and moderately-to-highly clear (means 3.29–4.00/5, per `Clarity` sheet). Source: `RQ3_Final_Results_Package_v1.0.md` §B.
- Overall framework appropriateness: 3.42/5 (median 3), N=24. Source: same.
- Distinctiveness item: 0% response rate across all 24 respondents and every prior survey snapshot — a stated instrument limitation. Source: same.
- **MSc-appropriate framing, restated for the Discussion (already established in Methods §3.12 and Results §4.4): this is content-assessment evidence only — never described as predictive validation, competence validation, population inference, internal consistency, or factor analysis anywhere in this project.** Source: `Survey_Analysis_Plan_v1.0.md` §1.

## Dimension-specific reliability (synthesis across D1–D6)

- Non-degenerate strong reproducibility: D1 (α=.944), D6 (α=1.000). Source: `RQ3_Final_Results_Package_v1.0.md` §C.
- Degenerate perfect agreement (not read as strong evidence): D2 (α=1.000, present-only population 100% one score), D4 (α=1.000, n=26, small restricted sample). Source: same.
- Limited reliability, two distinct diagnosed causes: D3 (systematic calibration disagreement), D5 (range restriction + narrower boundary ambiguity). Source: same; `RQ3_Reliability_Final_Interpretation_v1.0.md`.
- **MSc-appropriate framing:** present these six results as a genuine finding about which dimensions reproduce well under the specific test conducted (one subset, one second rater) — not as a general, permanent verdict on each dimension's measurability.

## NLP baseline findings

- Two dimensions exceed their majority-class baseline meaningfully: D1 (29.5% vs 28.4%, modest), D3 (52.0% vs 35.0%, clearest signal). Source: `RQ5_NLP_Final_Results_v1.0.md`.
- Two dimensions tie a degenerate or imbalanced floor: D2 (100% vs 100%, degenerate), D5 (87.0% vs 87.0%, imbalanced). Source: same.
- Two dimensions underperform their floor: D4 (62.9% vs 71.4%, κ=−.022), D6 (44.0% vs 48.0%). Source: same.
- Explicitly stated framing already in the source report, to be preserved in the Discussion: **"proof-of-concept baseline for RQ5, not a production-ready AI leadership assessment system."** Source: `RQ5_NLP_Final_Results_v1.0.md` header.
- **MSc-appropriate framing:** the D3 cross-analysis contrast (strongest NLP signal + weakest human reliability) is explicitly flagged in `Final_Thesis_Evidence_Audit_v1.0.md` §8 as an interpretive juxtaposition between two independently computed results, not a jointly computed statistic — word it as an observation, not a resolved finding.

## RQ4 limitation

- The four defined criterion variables (network reach, content engagement, recognition count, seniority progression rate) were not collected in any form. Source: `RQ4_Final_Status_v1.0.md`; `RQ4_Limitation_Report_v1.0.md` §2.
- No proxy was invented; D4/D5 were not retroactively repurposed as RQ4 criteria (would be circular — both are ALCSM dimensions scored from the same evidence RQ4 needs independence from). Source: `RQ4_Final_Status_v1.0.md`.
- **MSc-appropriate framing, as already stated in the source document:** "an unresolved empirical question," not a null result and not an estimated effect.

## Contribution of the study

Candidate framing points, each traceable to a specific delivered artifact (synthesize into your own contribution statement, do not just list):

- A working, fully reproducible six-dimension formative credential-scoring pipeline, applied to 500 real profiles with a documented, auditable annotation trail (28 retained score changes, zero unresolved cases). Source: `Final_Annotation_Audit_v1.1.md`.
- Dimension-level, non-pooled measurement-reproducibility evidence combining two independent methods (inter-rater reliability + expert content-assessment), a design explicitly grounded in formative-index measurement theory (Bollen & Lennox 1991; Diamantopoulos & Winklhofer 2001; Jarvis et al. 2003 — full citations in `Methods_Chapter_Source_Pack_v1.0.md` §3.7). Source: `RQ3_Final_Results_Package_v1.0.md`.
- A demand-vs-supply comparison at the credential-signal level across a real job-posting corpus, with an explicit, disclosed treatment of unmapped requirement text (never forced into the framework). Source: `RQ2_Final_Results_v1.0.md`.
- A minimal, transparent, local-only NLP baseline with honest majority-class-baseline comparison throughout, rather than a bare accuracy claim. Source: `RQ5_NLP_Final_Results_v1.0.md`.

## Limitations

Consolidated list (full detail per item in the cited source; do not re-derive):

- Non-probability, title-gated LinkedIn sampling frame. Source: `Methods_Chapter_Source_Pack_v1.0.md` §3.4.
- One 75-profile reliability subset, one independent second rater. Source: §3.11 same.
- N=24 self-selected survey respondents; 0% response on the distinctiveness item. Source: §3.12 same.
- RQ4 not conducted — data-collection gap. Source: `RQ4_Final_Status_v1.0.md`.
- NLP baseline: linear bag-of-words model, single train/test split per dimension (not cross-validated), small per-dimension training sets for some dimensions (e.g. D4, n=140 train). Source: `RQ5_NLP_Final_Results_v1.0.md`.
- Formal ethics-committee approval status undocumented/unresolved as of the last recorded project state — **flagged in Methods §3.14 as the single item most requiring the researcher's own direct follow-up before submission.**

## Future research

- A rulebook revision specifically targeting D3's cumulative-duration-counting ambiguity and D5's title-language-vs-strategic-scope boundary, followed by a re-run of the same double-coding design to test whether reliability improves. Source: `RQ3_Reliability_Final_Interpretation_v1.0.md` §3–§4 (diagnosis only; no rulebook change made in this project).
- Dedicated data collection for RQ4's external criterion variables. Source: `RQ4_Final_Status_v1.0.md`.
- A more structured NLP feature representation (one that can explicitly aggregate/count across a profile's listed experience entries), targeted at D6's and D4's weaker baseline results. Source: `RQ5_NLP_Final_Results_v1.0.md`.
- A larger, more representative expert-survey sample and a redesigned distinctiveness item. Source: `RQ3_Final_Results_Package_v1.0.md` §D.

---

*No new statistic introduced in this pack; every claim traces to an already-computed result. No canonical source file modified.*
