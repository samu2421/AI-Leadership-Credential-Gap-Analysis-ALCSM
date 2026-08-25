# ALCSM v1.1 — Scoring Framework

### Companion to `ALCSM_v1.0_Scoring_Framework_Task3.md`, restating D1–D5 unchanged and replacing D6 only

**Version:** 1.1
**Status:** D1–D5 sections are restated **[UNCHANGED FROM v1.0]**, carrying that document's own frozen status forward unmodified. The D6 sections are **[v1.1 REPLACEMENT]** — proposed, pending the pilot in `D6_v1.1_Implementation_Assessment.md` §Pilot Design and formal author freeze (`DECISION_LOG.md` D-0038).
**Relationship to v1.0:** `ALCSM_v1.0_Scoring_Framework_Task3.md` is not modified, deleted, or superseded as a historical record. This document is the one to use going forward once D6 v1.1 is frozen; until then, `ALCSM_v1.0_Scoring_Framework_Task3.md` remains the operative reference for any work not specifically about D6.
**No new weights, aggregation function, or classification bands are assigned here** — all three remain exactly as open as they were in v1.0, per explicit instruction.
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance
**Date:** 2026-08-17

---

## 1. Consolidated Scoring Table

D1–D5 are restated verbatim from `ALCSM_v1.0_Scoring_Framework_Task3.md` §1 — **[UNCHANGED FROM v1.0]**. Only the D6 column is new.

| Score | D1: Formal Education | D2: Certifications | D3: Practical AI Experience | D4: Technical Contributions | D5: Leadership & Strategic Responsibility | D6: AI Industry/Application Breadth *(v1.1)* |
|---|---|---|---|---|---|---|
| 0 | No higher education, or unrelated field | None listed | No AI/ML roles | None discoverable | Individual contributor, no leadership language | No AI-related experience with identifiable industry context |
| 1 | Bachelor's, adjacent field, no AI coursework | One expired/low-credibility cert | AI-adjacent role only | Non-technical public content only | Team lead/informal only | Exactly one distinct industry/application domain |
| 2 | Bachelor's CS/quant, no AI specialization | One current recognized-vendor cert | 1–2 yrs explicit AI/ML role, IC scope | One verifiable technical artifact | Manager-level, team-scope | Exactly two distinct industries/application domains |
| 3 | Bachelor's + AI specialization, or Master's adjacent | 2+ current general certs | 3+ yrs AI/ML, or 1–2 yrs with ownership language | Multiple artifacts, unverified | Director/Head, some strategic language | Exactly three distinct industries/application domains |
| 4 | Master's AI/ML/DS, or PhD adjacent quant | Multiple current AI/ML-specific certs | Multi-yr, multi-role, ownership escalation | Multiple artifacts, ≥1 externally verifiable | VP/senior, explicit enterprise-strategy scope | Exactly four distinct industries/application domains |
| 5 | PhD CS/AI/ML with AI-specific research | Multiple AI/ML certs + actively maintained professional body credential | Sustained multi-yr AI/ML leadership, deployed systems at scale | Sustained, externally verifiable output (pubs/patents/high-engagement OSS) | C-level/CAIO-equivalent, strategic AND augmentation-aware framing | Five or more distinct industries/application domains |

D6's criteria are drawn from `ALCSM_D6_Industry_Breadth_v1.1.md` §7, which derives them from the recomputed real-data distribution (494/500 profiles have usable evidence; see that document §5) rather than an a priori guess. **Candidate rubric, pending pilot confirmation — not yet frozen.**

**Verifiability annotation, updated for v1.1:** D1, D2, D4 = high–medium verifiability (structured/partly-external-verifiable fields); D3 = medium (self-report language); D5 = low (title/scope proxy). **D6 moves out of the low-verifiability cluster it occupied in v1.0.** The original D6 (Professional Engagement) was low–medium verifiability, proxy/self-presentation-based; the new D6 (Industry Breadth) is derived from the same structured `Professional_Experience.Industry` field used elsewhere in the dataset, placing it closer to D1/D2/D4's tier — subject to the employer-labeling-consistency caveat in `ALCSM_D6_Industry_Breadth_v1.1.md` §12. This gradient must still be visually retained in any coding interface, exactly as required in v1.0.

---

## 2. Mathematical Formula (Weights Left Open) — [UNCHANGED FROM v1.0]

Sections 2.1–2.5 of `ALCSM_v1.0_Scoring_Framework_Task3.md` are restated in full below with no substantive change. D6 is simply one of the six Dᵢ(p) terms, exactly as before — the formula does not need to know what D6 measures, only that it is a 0–5 ordinal score.

### 2.1 Notation

Let a profile *p* receive six raw dimension scores:

D₁(p), D₂(p), …, D₆(p) ∈ {0, 1, 2, 3, 4, 5}

Let w₁, …, w₆ be dimension weights, currently **undefined**, subject only to the constraint:

wᵢ ≥ 0 for all i, and Σᵢ wᵢ = 1

### 2.2 Candidate aggregation functions — still undecided

**(a) Fully compensatory — weighted arithmetic mean:** ALCSM_raw(p) = Σᵢ₌₁⁶ wᵢ · Dᵢ(p)

**(b) Partially compensatory — weighted geometric mean:** ALCSM_raw(p) = ∏ᵢ₌₁⁶ Dᵢ(p)^wᵢ (undefined/zero at Dᵢ(p)=0 unless rescaled to 1–6)

**(c) Non-compensatory — conjunctive (minimum-threshold):** ALCSM_raw(p) = min(D₁(p), …, D₆(p)), reported alongside the weighted mean

**Recommendation, unchanged:** report all three during pilot/exploratory analysis rather than committing to one now. Nothing about the D6 replacement changes this recommendation or favors one aggregation form over another — D6 v1.1 is no more or less likely to produce a "catastrophic minimum" than the original D6 was.

### 2.3 Normalization for reporting — unchanged

ALCSM_100(p) = 100 · ALCSM_raw(p) / 5, clearly labeled as to which aggregation form produced it.

### 2.4 Extending the formula to Contribution 2 (Credential Gap Analysis) — unchanged in form, with a new operational note for D6

Gapᵢ = mean(Dᵢʳᵉᑫ over relevant job postings) − mean(Dᵢ over relevant profiles)

**New operational note for i=6, arising directly from Task 6 of the D6 v1.1 verification (`ALCSM_D6_Industry_Breadth_v1.1.md` §10):** of 1,558 job-requirement records, only 1 (0.06%) contains language that plausibly maps to industry-breadth as a requirement. This means Gap₆ will be computed from an extremely sparse job-side sample under v1.1 — structurally different from Gap₁–Gap₅, which each have tens to hundreds of mapped requirement records (`D6_v1.1_Implementation_Assessment.md` §Job Requirement Mapping Impact). This is not a formula defect; it is a substantive finding (employers rarely state an explicit multi-industry AI-experience requirement) that must be reported alongside Gap₆, not smoothed over. Under the original D6, the job-side sample was smaller still (7 requirements, §10 of the same document) and none of those 7 requirements would remain D6-relevant under the new definition, so this sparsity is not new — it is now correctly attributed to the right cause (a genuine absence of employer-stated breadth requirements) rather than to platform-usage confound.

### 2.5 Missing-dimension handling in aggregation — unchanged, with a D6-specific note

The `missing = TRUE` / `missing = FALSE` distinction and the completeness_index = (dimensions with `missing = FALSE`) / 6 are unchanged. **Note specific to D6 v1.1:** unlike the original D6 (where "no evidence found" was the dominant real-world case, since activity data was never collected at all), the new D6 has usable evidence for 494/500 profiles (98.8%) — missingness is now the exception rather than the rule for this dimension, which changes its practical contribution to completeness_index in a way the original construct never could have achieved given this dataset (`ALCSM_D6_Industry_Breadth_v1.1.md` §5).

---

## 3. Annotation Guidelines for Manual Labelling — [UNCHANGED FROM v1.0]

All five guidelines in `ALCSM_v1.0_Scoring_Framework_Task3.md` §3 apply identically under v1.1: score all six dimensions per profile before moving to the next; no hand-calculated aggregates by annotators; re-use of tie-breaking/missing-data/verification rules is mandatory (see `ALCSM_Coding_Rulebook_v1.1_Addendum.md` for the D6-specific additions to those rules); every score-sheet entry traceable to its coding-log row via `profile_id`.

---

## 4. Illustrative Profile Classification Examples

**Same disclaimer as v1.0, restated:** the four "profiles" below are entirely constructed composites for illustration only — not real LinkedIn profiles, not drawn from the actual 500-profile dataset. D1–D5 values are carried forward **unchanged** from `ALCSM_v1.0_Scoring_Framework_Task3.md` §4; only the D6 value and its illustrative reading are updated to reflect the new construct.

| Composite | D1 | D2 | D3 | D4 | D5 | D6 *(v1.1)* | Unweighted mean | Illustrative reading |
|---|---|---|---|---|---|---|---|---|
| **A — "Substantiated AI Leader"** | 4 | 3 | 4 | 4 | 4 | 3 (three industries — plausible for a senior VP-level career) | 3.67 | Unchanged from v1.0's reading: credentials, experience, and leadership language are broadly consistent. |
| **B — "Titleholder Without Substantiated Leadership"** | 2 | 1 | 1 (AI-adjacent role only) | 0 | 5 | 1 (single AI-adjacent role → single industry, consistent with the thin D3 evidence) | 1.67 | Unchanged reading from v1.0: elevated title sitting atop weak scores everywhere else, including breadth — the D6 v1.1 score is *consistent with*, not independent evidence against, the shallow D3 profile, illustrating the moderate D3–D6 correlation discussed in `ALCSM_D6_Industry_Breadth_v1.1.md` §8. |
| **C — "Under-Signaled Practitioner"** | 3 | 0 | 4 (strong ownership language, 4 yrs) | 3 | 1 | 2 (two industries, inferred from a 4-year AI/ML tenure with ownership language) | 2.17 | **This is the case where the D6 replacement changes the illustrative outcome, and the change is the point.** Under the original v1.0 D6, this practitioner scored 0 (no visible posting activity) despite genuinely strong D3 experience — the textbook platform-usage confound the original design flagged as a risk (`ALCSM_Dimension_Design_Task2.md` §6). Under v1.1, D6 is derived from the same structured employment evidence that produced the strong D3 score, so a competent non-poster is no longer penalized on D6 for the same reason they were never penalized on D1–D4. The composite mean shifts from 1.83 (v1.0) to 2.17 (v1.1) — not because this constructed practitioner became more credentialed, but because the instrument stopped conflating "doesn't post" with "lacks breadth." |
| **D — "Sparse/Low-Completeness Profile"** | 0 (missing) | 0 (missing) | 1 | 0 (missing) | 2 | 0 (missing — Professional_Experience itself is thin for this composite, consistent with its other missing fields) | 0.5 (completeness_index = 2/6) | Unchanged from v1.0's reading: should likely be flagged for exclusion or separate reporting rather than treated as equivalent to a fully-documented low-scoring profile. |

**Key takeaway, extended from v1.0:** the B/C contrast (near-identical v1.0 totals for opposite substantive reasons) still holds — a single composite cannot distinguish credential inflation from under-signaling. The v1.1 D6 replacement additionally demonstrates, even in illustration, why construct choice matters independently of scoring mechanics: Profile C's mean moved not because any underlying fact about the constructed composite changed, but because the dimension measuring "breadth" started drawing on evidence that actually exists for this composite instead of evidence (posting activity) it never had reason to produce.

---

## 5. Provisional Classification Bands — [UNCHANGED FROM v1.0]

Restated verbatim; still explicitly draft, not for reporting, and not re-derived here since no weighting or aggregation decision has been made:

| Unweighted mean range | Provisional label |
|---|---|
| 0.0 – 1.0 | Minimal substantiated credential |
| 1.01 – 2.0 | Partial/emerging credential |
| 2.01 – 3.0 | Moderate substantiated credential |
| 3.01 – 4.0 | Strong substantiated credential |
| 4.01 – 5.0 | Comprehensive substantiated credential |

These remain round-number placeholders. The D6 replacement does not justify revisiting them pre-emptively — they should be replaced by empirically-derived bands from the actual pilot/main-study distribution regardless of which dimension prompted the most recent revision.

---

## What remains open after this document

Everything that was open after v1.0 remains open, plus one new item:

- Aggregation function choice among (a)/(b)/(c) — pending pilot evidence, unaffected by the D6 change.
- Dimension weights w₁–w₆ — pending empirical derivation; note that D6's job-posting-requirement-frequency weighting source (§2.4) will be materially thinner than D1–D5's under v1.1, which may itself be relevant input to how w₆ is eventually derived.
- Real classification bands — pending actual score distributions.
- Job-posting-side scoring pipeline validation — unpiloted, and now additionally constrained by the near-absence of D6-relevant job-posting language documented in §2.4.
- **New:** the D6 v1.1 candidate rubric itself (§1) is not frozen — it requires the pilot specified in `D6_v1.1_Implementation_Assessment.md` §Pilot Design before it can be treated as equivalent in status to D1–D5's rubrics, which were fixed at v1.0 freeze and are not being reopened here.

---

*This document restates D1–D5 without alteration and proposes the D6 v1.1 replacement for scoring purposes only. It does not assign weights, select an aggregation function, or finalize classification bands — those remain open exactly as in v1.0.*
