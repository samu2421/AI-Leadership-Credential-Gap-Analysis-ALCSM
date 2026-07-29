# ALCSM Design Decisions and Methodological Justification (Version 1.0)
### Definitive Reference for the AI Leadership Credential Signal Measurement Framework

**Thesis:** *The AI Leadership Credential Gap: An NLP Audit of 500 LinkedIn Profiles*
**Document role:** Final methodological justification and decision register for ALCSM v1.0. After this document, no further conceptual modifications are to be made unless pilot testing or empirical validation explicitly requires a versioned update.
**Scope constraint honoured:** This is a *justification and standardization* pass only. No dimension, scoring criterion, or annotation rule is redesigned.

**Consolidates:** `Literature_Remapping_and_Annotations_v1.md`, `ALCSM_Dimension_Design_Task2.md`, `ALCSM_Coding_Rulebook_and_Pilot_Design.md`, `ALCSM_v1.0_Scoring_Framework_Task3.md`, `ALCSM_Measurement_Specification_v1.0.md`.

**Convention:** *Literature-derived* = the decision follows from cited published methodology. *Thesis-specific* = a defensible project decision you must own personally at the viva; it is not mandated by any source.

---

## 0. Terminological Standardization (applies to the entire framework)

**Decision:** ALCSM is, throughout the thesis and all artefacts, described as measuring **observable AI leadership credential *signals* as presented on LinkedIn** — never as directly measuring leadership competence, capability, or "true" qualification.

Standard phrasings to use consistently:
- ✅ "ALCSM scores the credential signal a profile presents."
- ✅ "The observable credential signal on LinkedIn."
- ✅ "ALCSM measures what is signalled, not what is possessed."
- ❌ Avoid: "ALCSM measures whether someone is a qualified AI leader."
- ❌ Avoid: "ALCSM measures leadership competence / ability / true capability."

**Why:** This is the single most consequential framing decision in the thesis. Three of six dimensions (D3, D5, D6) can only observe self-presentation on a self-promotion platform. Claiming to measure competence directly would overreach the data and hand an examiner an easy, fatal objection. Framing ALCSM as a *signal audit* is not a hedge — it is theoretically precise (Spence, 1973: education/credentials are *signals* inferred to correlate with unobservable quality) and it makes the credential *gap* — the divergence between signal and substance — the legitimate object of study rather than a measurement failure.

**Literature-derived or thesis-specific:** Literature-derived (signalling theory), operationalized as a thesis-specific writing standard.

**This reframing is applied retroactively to all prior documents by reference** — wherever earlier drafts implied ALCSM measures competence, this standardization governs.

---

## 1. Master Design-Decision Register

Each decision below carries: the decision, rationale, provenance, supporting references, anticipated examiner criticism, viva defence, and limitation to acknowledge.

---

### DECISION 1 — Ground the entire model in signalling theory

- **Decision:** Use Spence's (1973) signalling theory as the master theoretical frame; treat all credentials as signals of unobservable quality.
- **Why:** Provides a coherent, canonical rationale for inferring competence-relevant information from observable credentials, and for conceptualizing the "gap" as a signalling-market phenomenon.
- **Provenance:** Literature-derived.
- **References:** Spence (1973), *Job Market Signaling*, QJE 87(3).
- **Examiner criticism:** "Signalling theory is a labour-economics abstraction; it doesn't validate a scoring rubric." / "Spence never addressed digital/social-media signalling."
- **Viva defence:** Spence is invoked as the *conceptual* justification for why credential auditing is meaningful at all, not as a psychometric warrant; the thesis extends signalling theory into an empirically novel substrate (LinkedIn) — that extension is a stated contribution, not an unexamined assumption.
- **Limitation to acknowledge:** Signalling theory motivates the approach but does not itself supply measurement validity; that must come from the pilot reliability work (Hinkin-based).

---

### DECISION 2 — Six dimensions, fixed and non-overlapping

- **Decision:** Adopt six credential dimensions (D1 Formal Education, D2 Certifications, D3 Practical Experience, D4 Technical Contributions, D5 Leadership & Strategic Responsibility, D6 Professional Engagement).
- **Why:** Covers the principal observable credential categories in AI leadership profiles while keeping the model tractable and interpretable at MSc scope.
- **Provenance:** Thesis-specific (the *set* is the researcher's construction), each dimension individually literature-anchored.
- **References:** D1 Spence (1973), Ng et al. (2021); D2 Spence (1973), Tadelis (2002); D3 Spence (1973), Cappelli, Tambe & Yakubovich (2018/19); D4 Tadelis (2002), Stark & Pais (2021); D5 Boyatzis (1982), Steinbach et al. (2019), Raisch & Krakowski (2021); D6 Tadelis (2002), Ng et al. (2021).
- **Examiner criticism:** "Why these six and not five or eight?" / "Are the dimensions truly independent, or do D3 and D4 overlap?"
- **Viva defence:** The six were derived to map onto distinct, separately observable LinkedIn credential categories; the coding rules (P-12) explicitly prevent double-counting when one artefact touches two dimensions. Dimensional independence is an *empirical question the pilot tests* (inter-dimension correlation), not an assumption asserted.
- **Limitation to acknowledge:** The dimension set is not derived from factor analysis of an existing item pool (the ideal Hinkin route); it is a rational/theoretical construction to be *empirically checked*, not a statistically discovered structure.

---

### DECISION 3 — Keep Boyatzis as D5 anchor despite it being a late substitution

- **Decision:** Anchor D5 in Boyatzis (1982) competency theory, supplemented by Steinbach et al. (2019) and Raisch & Krakowski (2021).
- **Why:** Boyatzis provides the only genuine competency-modeling lineage in the source set; the original plan's competency anchor was absent from the provided papers and this was sourced and verified to fill the gap.
- **Provenance:** Literature-derived (verified real citation), with a thesis-specific disclosure that it was a substitution.
- **References:** Boyatzis (1982); Steinbach, Gamache & Johnson (2019); Raisch & Krakowski (2021).
- **Examiner criticism:** "Your D5 anchors theorise *unobservable* facets (behavioural competencies, construal flexibility) that LinkedIn text cannot capture — this is a grounding mismatch."
- **Viva defence:** Correct — and deliberately so. The anchors are cited to explain *why the observable proxy is weak*, i.e., why demonstrated leadership competence exceeds what any title-based signal can capture. D5 is explicitly framed as measuring only the positional/rhetorical facet; the cited theory bounds the claim rather than inflating it.
- **Limitation to acknowledge:** D5 has the weakest construct validity of the six; the full text of Boyatzis (1982) must be obtained and read before citing specific competency clusters (currently the citation is verified but the primary text not yet consulted in full).

---

### DECISION 4 — Establish an explicit verifiability gradient across dimensions

- **Decision:** Formally rank the dimensions by how verifiable they are from LinkedIn text (D1/D2 high; D4 medium–high; D3 medium; D5/D6 low) and require per-dimension (never pooled) reliability reporting.
- **Why:** The dimensions are not equally measurable; treating them as if they were would misrepresent the instrument's precision.
- **Provenance:** Thesis-specific (the gradient), built on established reliability-reporting practice.
- **References:** Krippendorff (2004); Hinkin (1998).
- **Examiner criticism:** "If half your dimensions are 'low verifiability', why include them?"
- **Viva defence:** Because low-verifiability dimensions are precisely where credential *gaps* hide; excluding them would blind the audit to the phenomenon of interest. The gradient is disclosed, and reliability is reported per dimension so readers can weight the evidence appropriately.
- **Limitation to acknowledge:** D5/D6 reliability is expected to be lower; this is pre-declared (not discovered post hoc) so it reads as an anticipated property, not a failure.

---

### DECISION 5 — Conservative "default-low under uncertainty" scoring rule

- **Decision:** When evidence plausibly supports two adjacent scores, annotators assign the lower.
- **Why:** For a credential-*gap* audit, a generous default would let the instrument itself inflate apparent credentials — biasing against the thesis's own hypothesis is the safer, more defensible error direction.
- **Provenance:** Thesis-specific.
- **References:** Consistent with conservative-coding conventions in content analysis (Krippendorff, 2004), though the specific rule is the researcher's.
- **Examiner criticism:** "A systematic downward bias is still a bias; it could manufacture the 'gap' you claim to find."
- **Viva defence:** The direction is disclosed and applied uniformly to *both* corpora (profiles and job postings), so relative comparisons are not distorted; and it biases *against* finding people well-credentialed, i.e., against inflating the leaders' scores — it does not manufacture a gap in the hypothesized direction, it makes any observed gap conservative. This is a deliberately declared, symmetric conservatism.
- **Limitation to acknowledge:** Absolute score levels are conservative and should not be interpreted as precise point estimates; the analysis should emphasize relative/comparative patterns.

---

### DECISION 6 — External verification permitted for D4 only, and never score-inflating

- **Decision:** Annotators may verify only Technical Contributions (D4), only via profile-provided links or standard public indices, and verification may confirm or lower a score but never raise it above what profile text supports.
- **Why:** The automated NLP pipeline can only see profile text; if human coders verify facts the pipeline cannot, the human "gold standard" and machine scores would measure different constructs, invalidating RQ5.
- **Provenance:** Thesis-specific.
- **References:** Rationale aligns with construct-comparability requirements in Hinkin (1998).
- **Examiner criticism:** "Why cripple your human coders' accuracy to match a weaker machine?"
- **Viva defence:** Because RQ5 asks whether NLP can *replicate* human scoring; the comparison is only valid if both operate on the same information base. Verification is allowed for D4 specifically because that dimension's design already names external verifiability as a validity enhancement, and the rule is asymmetric (can lower, not raise) to prevent introducing information the pipeline lacks.
- **Limitation to acknowledge:** D4 human scores may slightly understate verifiable achievement for privacy-restricted profiles; documented per case.

---

### DECISION 7 — Keyword ontology locates evidence but never scores

- **Decision:** The AI keyword ontology and automation/augmentation lists are extraction aids only; keyword presence/frequency never directly sets or raises any dimension score.
- **Why:** Keyword-counting rewards buzzword-stuffing — itself a credential-inflation vector the thesis is designed to detect, not reward (see worked Example 14).
- **Provenance:** Thesis-specific.
- **References:** —
- **Examiner criticism:** "Then why maintain an ontology at all?"
- **Viva defence:** To make evidence *location* reproducible and auditable while keeping *judgement* with the rubric; this cleanly separates retrieval from scoring and is an explicit anti-gaming safeguard.
- **Limitation to acknowledge:** Ontology must be version-dated; AI vocabulary drifts and a stale list will under-locate newer terminology.

---

### DECISION 8 — Three candidate aggregation functions, none yet chosen

- **Decision:** Define compensatory (weighted mean), partially compensatory (geometric mean), and non-compensatory (conjunctive/minimum) aggregation as candidates; report all three in pilot analysis; commit to none pre-empirically.
- **Why:** How dimensions combine encodes a substantive theoretical assumption about trade-offs; a compensatory model in particular can mask exactly the title-without-substance pattern the thesis targets. The choice should follow evidence, not precede it.
- **Provenance:** Literature-derived (the compensatory/non-compensatory distinction), thesis-specific in leaving it open.
- **References:** Keeney & Raiffa (1976), *Decisions with Multiple Objectives*.
- **Examiner criticism:** "An incomplete model — you haven't decided how it aggregates."
- **Viva defence:** Deliberate and principled: committing to an aggregation rule before observing how the six dimensions actually co-vary would be premature formalization. Reporting all three and justifying the final choice against pilot evidence is more rigorous than an a priori guess.
- **Limitation to acknowledge:** Until resolved, no single ALCSM composite is authoritative; dimension-level reporting is primary.

---

### DECISION 9 — Weights left symbolic and open

- **Decision:** Dimension weights (w₁–w₆) are constrained (non-negative, sum to 1) but assigned no numeric values; to be derived empirically later.
- **Why:** Arbitrary weights would embed unexamined value judgements about which credentials "matter most"; empirical derivation (job-posting emphasis, expert elicitation, and/or impact-regression) is defensible where a priori guessing is not.
- **Provenance:** Thesis-specific.
- **References:** —
- **Examiner criticism:** "Without weights the model is unfinished." / "Impact-regression weighting risks circularity with RQ4."
- **Viva defence:** Weights are deferred precisely to avoid unjustified assumptions; the circularity risk is pre-empted by separating weight-derivation data from validation data (held-out/cross-validation).
- **Limitation to acknowledge:** Weighting method must be fixed and disclosed before final analysis; comparative reporting of multiple weighting schemes is recommended.

---

### DECISION 10 — Classification bands are placeholders only

- **Decision:** The evenly-spaced 0–5 → label bands are explicitly provisional and not for reporting; real bands to come from the actual pilot/main score distribution.
- **Why:** Round-number cutoffs are not empirically calibrated and could misrepresent the distribution.
- **Provenance:** Thesis-specific.
- **References:** —
- **Examiner criticism:** "Your classification thresholds are arbitrary."
- **Viva defence:** Acknowledged and by design — they are placeholders pending distribution-based calibration (quartiles/clustering); this is stated wherever they appear.
- **Limitation to acknowledge:** No classification claims should be made until bands are empirically set.

---

### DECISION 11 — Krippendorff's α, per dimension, with disclosed benchmark caveat

- **Decision:** Use Krippendorff's α (ordinal) computed separately per dimension; interpret against Landis & Koch (1977) / Krippendorff (2004) benchmarks while explicitly noting those benchmarks are conventional, not uncontested.
- **Why:** α handles ordinal 0–5 data, small pilot samples, and missing cells; per-dimension reporting respects the verifiability gradient.
- **Provenance:** Literature-derived.
- **References:** Krippendorff (2004); Hayes & Krippendorff (2007); Landis & Koch (1977); Cohen (1960) for supplementary weighted κ.
- **Examiner criticism:** "Landis & Koch labels are arbitrary and α is prevalence-sensitive."
- **Viva defence:** Explicitly conceded in-text; benchmarks are used as conventional reference points, not gold standards, and the α ≥ .667 (tentative) / ≥ .80 (confident) thresholds are stated as project decisions, not external law.
- **Limitation to acknowledge:** Reliability coefficients are sensitive to trait prevalence in the pilot sample; boundary-case agreement is reported separately.

---

### DECISION 12 — Purposive (not random) pilot sampling

- **Decision:** The 10–20 pilot profiles are selected purposively to stress-test the rubric (clear, borderline, sparse, contradictory cases), not as a miniature random sample.
- **Why:** A pilot's job is to break the rubric, not to estimate population parameters.
- **Provenance:** Literature-derived (pilot-testing rationale), thesis-specific in composition.
- **References:** Hinkin (1998); Krippendorff (2004).
- **Examiner criticism:** "Purposive sampling isn't representative."
- **Viva defence:** Correct and intentional — representativeness is the *main study's* job (Task 4); the pilot deliberately over-samples difficulty to expose rubric weaknesses. The two sampling logics are distinct and both disclosed.
- **Limitation to acknowledge:** Pilot reliability figures may be *conservative* (harder cases) relative to the main sample — a defensible direction of bias.

---

### DECISION 13 — Preserve, never resolve, title–substance contradictions

- **Decision:** Contradictions between claimed seniority and substantiating evidence are flagged (`title_substance_contradiction_flag`) and preserved as data, not smoothed away during coding.
- **Why:** These contradictions *are* the credential-gap phenomenon; resolving them during coding would destroy the primary evidence.
- **Provenance:** Thesis-specific.
- **References:** Conceptually Spence (1973) (signal–quality divergence).
- **Examiner criticism:** "Isn't a contradiction just a coding error?"
- **Viva defence:** No — it is the unit of analysis. Precedents P-03/P-04/P-05 distinguish genuine inflation from under-signalling and from substantiated-but-narrow leaders, so contradictions are classified, not discarded.
- **Limitation to acknowledge:** Contradiction detection depends on annotator judgement; inter-rater agreement on the flag itself should be reported.

---

## 2. Empirically Anchoring the Taxonomies via the 200 Job Postings

**Standing principle:** The role, certification, education, leadership, and technical-contribution taxonomies are **researcher-constructed design artefacts, not externally validated standards.** To reduce the "arbitrary taxonomy" exposure (Examiner point 7.3 in the Specification), anchor them empirically in the vocabulary of the 200 AI-leadership job postings before freezing their concrete term lists.

**Procedure (recommended, thesis-specific):**
1. **Extract** the raw vocabulary from the 200 postings: required/preferred degrees and fields, named certifications, role titles, seniority terms, and technical-contribution expectations (publications, patents, open-source, tooling).
2. **Rank by frequency** within each category, so the taxonomy's concrete terms reflect what the AI-leadership labour market actually asks for, not the researcher's assumptions.
3. **Seed the taxonomies** with these observed terms: e.g., the D2 certification list is populated from certifications *named in postings* (plus those observed in the profile pilot); the D3 role taxonomy's title bands are calibrated against the seniority language postings actually use.
4. **Document** the extraction date, the posting corpus version, and the frequency thresholds used for inclusion. Publish the resulting term lists in an appendix/repository.
5. **Retain researcher judgement** for classification structure (tiers/bands) — frequency anchors the *terms*, theory anchors the *structure*.

**Why this matters beyond reproducibility:** it converts the taxonomies from a priori constructions into *market-grounded* instruments, and it directly strengthens Contribution 2 — because the same vocabulary basis underlies both the "required" (job-posting) and "held" (profile) scoring, making the credential-gap comparison an apples-to-apples one rather than a comparison across two differently-constructed measurement bases.

**Explicit boundary:** empirical anchoring makes the taxonomies *defensible and current*, not *externally validated*. The thesis must still describe them as researcher-constructed, market-seeded instruments — never as recognized industry standards.

---

## 3. Frozen vs. Open Declaration

### 3.1 FROZEN at v1.0 (no change without a versioned update justified by pilot/empirical evidence)
- Signalling-theory framing and the signal-not-competence terminology standard (§0).
- The six dimensions, their definitions, theoretical anchors, and 0–5 scoring criteria.
- The verifiability gradient and per-dimension reliability-reporting requirement.
- All eight taxonomies' *structure* (tiers/bands) — their concrete term lists are frozen once job-posting anchoring (§2) is complete and logged.
- Annotation rules: default-low; halo prohibition; missing vs. stated-absence distinction; D4-only, non-inflating verification; ontology-locates-but-never-scores; contradiction preservation.
- The 15-entry precedent library and the 18 worked training examples.
- Exclusion of institution prestige from scoring.
- Krippendorff's α (per dimension) as the reliability method, with disclosed benchmark caveats.

### 3.2 INTENTIONALLY OPEN until empirical validation
- **Aggregation function** (compensatory / partially compensatory / conjunctive) — chosen after pilot.
- **Dimension weights (w₁–w₆)** — empirically derived, method to be fixed and disclosed; circularity safeguard required.
- **Classification thresholds/bands** — distribution-calibrated after pilot/main data.
- **Consequences of a dimension failing reliability after one revision cycle** — decided only if it occurs.
- **Language/localization scope** — English-only vs. translation protocol, fixed before main collection.
- **Job-posting-side scoring validation** — the Contribution-2 requirement-mining pipeline requires its own pilot; does not inherit profile-side reliability.

**Declaration:** ALCSM v1.0 is hereby frozen as the definitive measurement framework. Frozen components are settled for implementation. Open components are deliberately deferred to empirical stages and are not conceptual gaps but sequenced decisions. Any future change to a frozen component requires an explicit version increment (v1.1, v2.0) with documented empirical justification.

---

## 4. Readiness Checklist

### 4.1 Tasks 1–3 — completion status
- ✅ **Task 1 — Literature review:** 7 provided papers annotated; literature mismatch honestly reconciled; 2 gaps (competency theory, scale-validation) filled with verified sources (Boyatzis 1982, Hinkin 1998). *Outstanding:* obtain and read full texts of Boyatzis (1982) and confirm final publication details of the Cappelli/Tambe/Yakubovich paper before the reference list is finalized.
- ✅ **Task 2 — Dimension design:** six dimensions defined, theoretically anchored, with NLP extraction plans and the verifiability gradient.
- ✅ **Task 3 — Scoring framework:** consolidated scoring table; unweighted formula with three candidate aggregation functions; Contribution-2 gap extension; rulebook; pilot design; precedent library; worked examples; this justification register.
- ✅ **Measurement Specification v1.0** consolidated and frozen.

### 4.2 Prerequisites required *before* beginning Task 4 (data schema design)
1. **Adopt the §0 terminology standard** across all thesis text — because it changes how dataset variables are *named and interpreted* (signal variables, not competence variables).
2. **Confirm the sampling-frame problem is carried into Task 4** — a LinkedIn-title-based sample structurally excludes competent-but-untitled leaders; the profile dataset schema must capture selection/provenance so this bias is analyzable, not hidden (Specification §7.6).
3. **Decide the job-posting-anchoring workflow (§2) will run before taxonomy term-lists are hard-frozen** — Task 4's job-posting schema should be designed to *support* vocabulary extraction (i.e., store raw required-credential text fields, not only parsed summaries).
4. **Fix language/localization scope** — determines whether the schema needs original-language and translated fields.
5. **Note Task 5 (ethics/GDPR) is a blocking prerequisite for data *collection*** — not for schema *design*, so Task 4 may proceed, but the schema should already anticipate pseudonymization, lawful-basis, and post-level-activity flags so ethics compliance is designed in, not retrofitted.

### 4.3 Not required before Task 4 (correctly deferred)
- Aggregation function, weights, and classification thresholds remain open by design and do not block schema work.
- Pilot execution and reliability results are downstream of schema design.

---

## 5. Closing Statement

This document completes the methodological justification for ALCSM v1.0. The framework is theoretically grounded, transparently reasoned, honest about the substitutions and gaps in its literature base, and consistently framed as an audit of **observable LinkedIn credential signals** rather than of leadership competence. Every major design decision is recorded with its rationale, provenance, anticipated criticism, viva defence, and limitation.

No conceptual modifications remain to be made. The framework is frozen. Subsequent stages (Tasks 4–6) operate on this fixed measurement foundation, and any change to a frozen component requires a justified version increment.
