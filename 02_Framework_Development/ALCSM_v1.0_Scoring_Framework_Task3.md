# ALCSM v1.0 — Scoring Framework
### Scoring Table, Mathematical Formula (Unweighted), Annotation Guidelines, and Illustrative Classification Examples

**Scope confirmation:** This document formalizes the six dimensions and draft criteria from `ALCSM_Dimension_Design_Task2.md` into a single scoring instrument. Per your instruction, **no final dimension weights are assigned**. Where a formula requires weight terms, they are left symbolic (w₁…w₆) with a defined constraint set, not numeric values. Classification bands given here are **illustrative/provisional only**, built on an unweighted baseline purely to demonstrate how the instrument would be read — they are explicitly flagged as not yet valid for reporting real findings.

As before: **[ESTABLISHED]** = drawn from cited published methodology; **[THESIS-SPECIFIC]** = a project decision I am proposing, not a literature mandate.

---

## 1. Consolidated Scoring Table

This restates the six dimensions' 0–5 criteria (unchanged from Task 2) in a single reference table for annotator and pipeline use.

| Score | D1: Formal Education | D2: Certifications | D3: Practical AI Experience | D4: Technical Contributions | D5: Leadership & Strategic Responsibility | D6: Professional Engagement |
|---|---|---|---|---|---|---|
| 0 | No higher education, or unrelated field | None listed | No AI/ML roles | None discoverable | Individual contributor, no leadership language | No visible engagement |
| 1 | Bachelor's, adjacent field, no AI coursework | One expired/low-credibility cert | AI-adjacent role only | Non-technical public content only | Team lead/informal only | Passive engagement (likes/shares) only |
| 2 | Bachelor's CS/quant, no AI specialization | One current recognized-vendor cert | 1–2 yrs explicit AI/ML role, IC scope | One verifiable technical artifact | Manager-level, team-scope | Regular passive engagement, no original content |
| 3 | Bachelor's + AI specialization, or Master's adjacent | 2+ current general certs | 3+ yrs AI/ML, or 1–2 yrs with ownership language | Multiple artifacts, unverified | Director/Head, some strategic language | Occasional original commentary |
| 4 | Master's AI/ML/DS, or PhD adjacent quant | Multiple current AI/ML-specific certs | Multi-yr, multi-role, ownership escalation | Multiple artifacts, ≥1 externally verifiable | VP/senior, explicit enterprise-strategy scope | Regular original commentary + community membership |
| 5 | PhD CS/AI/ML with AI-specific research | Multiple AI/ML certs + actively maintained professional body credential | Sustained multi-yr AI/ML leadership, deployed systems at scale | Sustained, externally verifiable output (pubs/patents/high-engagement OSS) | C-level/CAIO-equivalent, strategic AND augmentation-aware framing | Sustained thought leadership, community leadership role |

**[THESIS-SPECIFIC] Verifiability annotation (carried from Task 2):** D1, D2, D4 = high–medium verifiability; D3 = medium (self-report language); D5, D6 = low (proxy/self-presentation only). This gradient should be visually retained in any coding interface or Streamlit tool build (e.g., a verifiability indicator per dimension), not just mentioned in prose, so annotators and eventual readers of your NLP tool's output are not misled into treating all six scores as equally trustworthy.

---

## 2. Mathematical Formula (Weights Left Open)

### 2.1 Notation

Let a profile *p* receive six raw dimension scores:

D₁(p), D₂(p), …, D₆(p) ∈ {0, 1, 2, 3, 4, 5}

Let w₁, …, w₆ be dimension weights, currently **undefined**, subject only to the constraint:

wᵢ ≥ 0 for all i, and Σᵢ wᵢ = 1

(This constraint set alone is sufficient to define a valid weighted composite once weights are empirically derived later; no numeric values are fixed here.)

### 2.2 Candidate aggregation functions — a decision you still need to make, not just a formula to fill in

**[ESTABLISHED]** How multiple criteria scores are combined into a single index is a substantive methodological choice in multi-criteria measurement, not a mechanical afterthought — compensatory, partially compensatory, and non-compensatory (conjunctive) aggregation rules encode different theoretical assumptions about how criteria trade off against one another (Keeney & Raiffa, 1976, *Decisions with Multiple Objectives: Preferences and Value Tradeoffs*, Wiley — the foundational multi-attribute utility theory reference for this distinction).

You have **not yet decided** which aggregation logic ALCSM should use, and I want to flag that this decision matters more than the eventual weight values themselves:

**(a) Fully compensatory — weighted arithmetic mean**

ALCSM_raw(p) = Σᵢ₌₁⁶ wᵢ · Dᵢ(p)

Range: [0, 5]. A high score on one dimension can fully offset a low score on another (e.g., exceptional Technical Contributions can compensate for zero Leadership score). **Problem for your specific thesis:** this is arguably the *wrong* model for a credential-gap audit. If your RQ cares about people holding a leadership *title* without leadership *substance*, a compensatory model could let a technically strong but leadership-shallow profile score identically to a genuinely well-rounded AI leader — precisely obscuring the gap you're trying to detect.

**(b) Partially compensatory — weighted geometric mean**

ALCSM_raw(p) = ∏ᵢ₌₁⁶ Dᵢ(p)^wᵢ  (undefined/zero if any Dᵢ(p) = 0, unless you rescale to a 1–6 range first)

A near-zero score on any one dimension pulls the whole index sharply down, but does not create an automatic floor. This penalizes lopsided profiles more than (a), which is closer to your thesis's substantive interest, but introduces a technical wrinkle: geometric means are undefined at zero, so you would need to rescale the 0–5 scale (e.g., to 1–6) purely for this computation — a transformation that itself needs to be disclosed and justified, not silently applied.

**(c) Non-compensatory — conjunctive (minimum-threshold) model**

ALCSM_raw(p) = min(D₁(p), …, D₆(p)), reported alongside the weighted mean, not instead of it

This directly encodes the idea that a "true AI leader" must clear some minimum bar on *every* dimension — a single catastrophic dimension (e.g., zero Leadership scope despite a stellar PhD) caps the overall assessment. This is the closest fit to a strict credential-gap detection logic, but is also the most punishing and may compress your entire 500-profile sample toward low scores if even strong profiles have one weak dimension (a realistic risk given D5/D6's low verifiability from Task 2 — profiles may score low on D5/D6 simply because LinkedIn doesn't capture leadership behavior well, not because the person actually lacks it, per the discussion in Task 2 §0 and §5).

**[THESIS-SPECIFIC] Recommendation:** report **all three** in your pilot/exploratory analysis stage rather than committing to one now. This is not indecision — it's a defensible empirical strategy: compute all three aggregate forms across your pilot profiles, see how much they actually diverge in practice, and let that divergence (or lack of it) inform which aggregation logic you adopt for the main 500-profile analysis and justify in your Methods chapter with reference to Keeney & Raiffa's compensatory/non-compensatory distinction. Committing to one aggregation rule today, before you've seen how the six dimensions actually correlate empirically, would be a weights-and-model decision made without evidence — exactly the kind of premature formalization Hinkin's (1998) staged approach is designed to prevent.

### 2.3 Normalization for reporting

**[THESIS-SPECIFIC]** For readability in tables/visualizations (not for statistical analysis, where the raw 0–5 or 0–30 scale should be used), define:

ALCSM_100(p) = 100 · ALCSM_raw(p) / 5

...for whichever aggregation form (a)/(b)/(c) is in use, clearly labeled as to which one, since a "very same-looking" ALCSM_100 = 60 means something different depending on aggregation choice. Never report ALCSM_100 without stating which aggregation function produced it.

### 2.4 Extending the formula to Contribution 2 (Credential Gap Analysis)

**[THESIS-SPECIFIC — this is the piece that actually operationalizes your second contribution, and it isn't in the literature verbatim; it's my proposed extension of the same scoring instrument to a second corpus.**

Your thesis's second contribution compares *required* credentials (200 job postings) against *held* credentials (500 profiles). This requires scoring job-posting text on the **same six-dimension rubric**, producing a parallel set of scores:

D₁ʳᵉᑫ(j), …, D₆ʳᵉᑫ(j) for job posting *j* — interpreted as *required/expected* level, not *possessed* level.

Define, per dimension, a **Credential Gap** at the aggregate level (e.g., comparing mean required level per job-family against mean held level per matched profile subgroup — not a naive per-individual subtraction, since no single profile is "the" candidate for a given posting):

Gapᵢ = mean(Dᵢʳᵉᑫ over relevant job postings) − mean(Dᵢ over relevant profiles)

A positive Gapᵢ indicates job postings demand more of dimension *i* than current AI leaders visibly hold — the credential gap in the direction your thesis title suggests. A negative Gapᵢ would be a genuinely interesting, underexplored finding (over-qualification relative to stated job requirements) and should not be discarded as noise if observed.

**Important construct-validity caution:** scoring job-posting *requirement* language (e.g., "Master's degree required," "5+ years' experience preferred") is a different NLP task than scoring *self-presentation* language on a LinkedIn profile — requirement extraction is closer to structured requirement-mining, while profile scoring is closer to biographical text classification. Do not assume the same classifier/prompt architecture will transfer cleanly between the two corpora without separate validation (a separate, smaller pilot on job-posting text is advisable before treating both scores as comparable).

### 2.5 Missing-dimension handling in aggregation

**[ESTABLISHED, consistent with your Part 1 rulebook's missing-data handling]** When a dimension is scored 0 due to `missing = TRUE` (no evidence found) rather than `missing = FALSE` (evidence of genuine absence), standard practice in composite-index construction is to distinguish structural/informative zeros from missing-data zeros, since blending the two silently biases the aggregate downward for profiles that simply provide less text overall (a *platform-usage* confound, not a *credential* difference) — this connects directly to the D6 caution already logged in Task 2.

**[THESIS-SPECIFIC] recommendation:** report, alongside every profile's ALCSM_raw score, a **completeness index** = (number of dimensions with `missing = FALSE`) / 6, and treat low-completeness profiles as a separate analytic category (or exclude them from primary analysis, reporting exclusion criteria transparently) rather than silently averaging them in on equal footing with fully-documented profiles.

---

## 3. Annotation Guidelines for Manual Labelling (v1.0-specific)

These extend, rather than replace, the general rulebook already established (`ALCSM_Coding_Rulebook_and_Pilot_Design.md`). The additions here are specific to filling out the v1.0 six-dimension score sheet as a complete instrument.

1. **Score sheet structure per profile:** one row per profile with columns D1–D6 (integer 0–5), `missing_D1`…`missing_D6` (Boolean), `completeness_index` (computed), and `notes`. This is a profile-level rollup of the six per-dimension coding-log entries defined in the rulebook — the coding log is the working file; the score sheet is the analysis-ready output.
2. **Order of coding:** annotators should score all six dimensions for one profile before moving to the next profile (not one dimension across all profiles at a time), to reduce the risk of a "dimension-specific mindset" anchoring scores across unrelated profiles — a standard precaution against sequential-context bias in manual coding.
3. **No aggregate-score calculation by hand:** annotators record only the six raw D1–D6 scores. **Do not** have annotators compute ALCSM_raw themselves during coding — aggregation happens downstream, after all three candidate aggregation functions (§2.2) have been decided against pilot evidence. This prevents annotators from being implicitly influenced by a running composite score while scoring individual dimensions.
4. **Re-use of the tie-breaking, missing-data, and verification rules is mandatory** — this document does not introduce new rules for these; refer to the rulebook.
5. **Every score sheet entry must be traceable** to the corresponding coding-log row via `profile_id` — do not allow the score sheet to exist as a "clean" artifact disconnected from its underlying evidence trail; an examiner or replication attempt should be able to go from any score sheet cell back to the exact text span that justified it.

---

## 4. Illustrative Profile Classification Examples

**Important disclaimer, stated explicitly because it matters for academic integrity:** the four "profiles" below are **entirely constructed composites** for illustration only. They are not real LinkedIn profiles, not drawn from your eventual 500-profile dataset, and not based on any specific real individual. Do not cite these as findings or examples of real data in your thesis — they exist solely to demonstrate how the scoring table and (illustrative, unweighted) aggregation would be applied.

For illustration only, I use the simple unweighted mean (equivalent to setting all wᵢ = 1/6) — this is *not* a recommendation for the final weighting scheme, only a neutral baseline to make the examples legible.

| Composite | D1 | D2 | D3 | D4 | D5 | D6 | Unweighted mean | Illustrative reading |
|---|---|---|---|---|---|---|---|---|
| **A — "Substantiated AI Leader"** | 4 (MSc AI) | 3 (2 current certs) | 4 (5+ yrs, ownership language) | 4 (linked GitHub, 1 co-authored paper) | 4 (VP AI, enterprise strategy language) | 3 (occasional original posts) | 3.67 | Credentials, experience, and leadership language are broadly consistent — no strong contradiction flags expected. |
| **B — "Titleholder Without Substantiated Leadership"** | 2 (BSc CS, no AI specialization) | 1 (one expired cert) | 1 (AI-adjacent role only) | 0 (no discoverable output) | 5 (Chief AI Officer title, but bio is generic project-management language) | 1 (passive engagement only) | 1.67 | This is close to the canonical credential-gap case: an elevated title (D5 scored partly on title-seniority sub-criterion) sitting atop weak scores everywhere else. **Under the compensatory mean, this profile scores low overall** — but note the D5=5 is itself questionable per the "title vs. substance" contradiction rule in the rulebook; a careful annotator should flag `contradiction = TRUE` here and this profile is a strong candidate for the conjunctive model (§2.2c) precisely because a compensatory mean risks under-representing how misleading the D5 score alone would look in isolation. |
| **C — "Under-Signaled Practitioner"** | 3 (BSc + AI specialization) | 0 (no certs listed) | 4 (strong ownership language, 4 yrs) | 3 (active GitHub, unverified beyond that) | 1 (Data Scientist title, no strategic language) | 0 (no visible posting activity) | 1.83 | Genuinely competent-looking practitioner who is simply not LinkedIn-active or certificate-collecting. Numerically similar total to Profile B, but for a completely different substantive reason — this is exactly why a single pooled score without the underlying dimension breakdown would be analytically misleading, and why your thesis should always report dimension-level profiles alongside any composite. |
| **D — "Sparse/Low-Completeness Profile"** | 0 (missing) | 0 (missing) | 1 | 0 (missing) | 2 | 0 (missing) | 0.5 (completeness_index = 2/6) | Should likely be flagged for exclusion or separate reporting rather than treated as equivalent to a genuinely low-credentialed but fully-documented profile (contrast with hypothetical profile scoring 0.5 with completeness_index = 6/6). |

**Key takeaway to carry into your Results/Discussion chapters:** Profiles B and C produce nearly identical unweighted composite scores (1.67 vs. 1.83) for substantively opposite reasons (inflated title vs. under-signaled substance). This is not a flaw in the illustration — it's a genuine finding-in-waiting: **a single ALCSM composite number, on its own, cannot distinguish "credential inflation" from "under-signaling,"** and your thesis should treat the *pattern* of dimension-level scores (not just the total) as the primary analytic unit for the credential-gap narrative, with the composite reserved for higher-level comparative statistics (e.g., against job-posting requirements in Contribution 2, or against professional-impact indicators in RQ4).

---

## 5. Provisional Classification Bands (explicitly draft, not for reporting)

**[THESIS-SPECIFIC — provisional only, using the unweighted mean purely as a placeholder; do not adopt these bands for real analysis until aggregation function and weights are empirically settled.**

| Unweighted mean range | Provisional label |
|---|---|
| 0.0 – 1.0 | Minimal substantiated credential |
| 1.01 – 2.0 | Partial/emerging credential |
| 2.01 – 3.0 | Moderate substantiated credential |
| 3.01 – 4.0 | Strong substantiated credential |
| 4.01 – 5.0 | Comprehensive substantiated credential |

These band boundaries are round-number placeholders, not derived from any distributional or theoretical analysis — do not present them in your thesis as if they were empirically calibrated. Once pilot data exist, revisit banding using the actual score distribution (e.g., quartiles or a cluster analysis) rather than evenly spaced arbitrary cutoffs.

---

## What remains open after this document

- Aggregation function choice among (a)/(b)/(c) in §2.2 — pending pilot evidence
- Dimension weights w₁–w₆ — pending either (i) empirical derivation from job-posting requirement frequency/emphasis (a natural, thesis-native weighting source given Contribution 2), (ii) expert-panel elicitation, or (iii) a data-driven approach (e.g., regression weights against professional-impact indicators for RQ4) — these three weighting strategies are not mutually exclusive and could be reported comparatively
- Real classification bands, derived from actual pilot/main-study score distributions, not the placeholder bands in §5
- Job-posting-side scoring pipeline validation (§2.4), which has not been piloted at all yet and should not be assumed to inherit the profile-side pilot's reliability figures

Tell me when you're ready to move to the data schema design (LinkedIn profiles, job postings, survey), or if you'd like to resolve the aggregation-function question empirically first using constructed test data before proceeding.
