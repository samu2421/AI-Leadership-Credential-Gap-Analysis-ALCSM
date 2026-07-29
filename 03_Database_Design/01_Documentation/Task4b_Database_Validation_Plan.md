# Pilot Database Validation Plan
### Implementation Validation of the ALCSM v1.0 Schema Prior to Real Data Collection

**Objective:** stress-test every database constraint and implementation rule using ten manually entered test profiles. This is **not** an evaluation of ALCSM scores; all score values are arbitrary placeholders chosen solely to trigger specific rules. The schema was **not modified**.

**Execution status — this plan has been run, not merely designed.** A PostgreSQL 16.14 instance was provisioned, the schema loaded, and the full suite executed:

| Result | Count |
|---|---|
| Schema statements loaded without error | 70 |
| Validation tests executed | 56 |
| Tests behaving exactly as specified | **56 / 56** |
| Must-fail statements correctly rejected | **18 / 18** |
| Distinct constraints empirically exercised | 15 |
| Additional gap probes run | 15 |
| Unenforced rules discovered | **15** |
| Genuine implementation defects found | **1** (see F-01) |

---

## 1. Test Profile Design

Ten profiles, each constructed to exercise a distinct class of rule. Score values are placeholders and carry no substantive meaning.

### PRF-00001 — Baseline / happy path
- **Purpose:** establish that a fully valid, completely coded profile is accepted.
- **Rules tested:** FK integrity (profile → batch, score → profile/dimension/rater), `UNIQUE` coding grain, evidence requirement, complete six-dimension set.
- **Expected DB behaviour:** all six score rows accepted; `completeness_index` = 1.00.
- **CHECK constraints:** `ck_evidence_when_present` satisfied on all six rows.
- **FK behaviour:** all four FKs resolve.
- **Missing-data encoding:** `present` ×6.
- **Verification:** none (`verification_used = FALSE`).
- **Adjudication:** none.
- **Outcome:** **SUCCEED** ✅ observed.

### PRF-00002 — Unavailable data
- **Purpose:** confirm the `unavailable` state is stored correctly and forces score 0.
- **Rules tested:** `ck_unavailable_scores_zero`; `profile_raw_section.section_available = FALSE`.
- **Expected DB behaviour:** score row and raw-section row both accepted.
- **CHECK constraints:** `ck_unavailable_scores_zero`; `ck_evidence_when_present` not triggered (only applies to `present`).
- **Missing-data encoding:** `unavailable`, score 0, no evidence.
- **Outcome:** **SUCCEED** ✅ observed.

### PRF-00003 — Stated absence
- **Purpose:** verify the frozen distinction between *stated absence* (informative) and *missing data*.
- **Rules tested:** `absent_stated` handling; precedent FK (`P-13`); completeness treatment.
- **Expected DB behaviour:** accepted; `absent_stated` must count as **informative** toward completeness.
- **Missing-data encoding:** `absent_stated` with evidence text.
- **Outcome:** **SUCCEED** ✅ observed — but exposed defect **F-01** in the completeness view.

### PRF-00004 — Ambiguity / boundary case
- **Purpose:** exercise ambiguity metadata (precedent P-02, "Head of X").
- **Rules tested:** `ck_ambiguity_metadata` (both candidates required, low ≤ high).
- **Missing-data encoding:** `present`.
- **Outcome:** **SUCCEED** ✅ observed.

### PRF-00005 — Contradiction (canonical credential inflation)
- **Purpose:** confirm contradictions are *preserved as data*, per the frozen rule.
- **Rules tested:** `ck_contradiction_metadata`; precedent `P-03`.
- **Outcome:** **SUCCEED** ✅ observed.

### PRF-00006 — D4 external verification
- **Purpose:** confirm verification is permitted on D4 and requires full metadata.
- **Rules tested:** `ck_verification_d4_only` (positive case); `ck_verification_metadata`.
- **Verification behaviour:** `verification_used = TRUE`, source + timestamp + outcome all populated, outcome `confirmed`.
- **Outcome:** **SUCCEED** ✅ observed.

### PRF-00007 — Constraint-violation vehicle
- **Purpose:** target for must-fail tests N-01 to N-06; no valid rows inserted.
- **Outcome:** all attempted inserts **FAIL** ✅ observed.

### PRF-00008 — Double coding and adjudication
- **Purpose:** the most consequential test — verify reliability integrity.
- **Rules tested:** independent coding by two raters; additive adjudication; generated `disagreement_magnitude`; exclusion of adjudicated rows from `v_reliability_input`.
- **Adjudication behaviour:** RATER-A = 2, RATER-B = 4 (magnitude 2 → `escalated` per frozen tie-break); ADJUDICATOR row inserted **additively** with `is_adjudication = TRUE`; original rows untouched.
- **Expected view behaviour:** `v_reliability_input` returns **2** rows (not 3); `v_final_profile_score` returns the adjudicated **3**.
- **Outcome:** **SUCCEED** ✅ observed; both view assertions correct.

### PRF-00009 — Negative-test vehicle
- **Purpose:** target for N-07, N-08, N-11, N-13.
- **Outcome:** all attempted inserts **FAIL** ✅ observed.

### PRF-00010 — Sparse profile (fully coded, mostly unavailable)
- **Purpose:** distinguish a *sparse profile* (6 dimensions coded, few informative) from an *incompletely coded profile*.
- **Rules tested:** completeness computation across mixed missing states.
- **Missing-data encoding:** 2 × `present`, 4 × `unavailable`.
- **Expected:** `completeness_index` = 0.33.
- **Outcome:** **SUCCEED** ✅ observed, 0.33 correct.

### Supporting records
`JOB-00002` exercises posting-side insertion with raw text retained, a `not_applicable` requirement (D6) and a `present` requirement (D1). `RUN-0001` plus one prediction exercises the NLP tables and `v_nlp_evaluation`.

---

## 2. Must-Fail Test Matrix

All 18 were rejected by the database. Fifteen distinct named constraints were exercised.

| ID | Violation attempted | Constraint that fired |
|---|---|---|
| N-01 | Score = 6 | `alcsm_dimension_score_score_check` |
| N-02 | `unavailable` with score 3 | `ck_unavailable_scores_zero` |
| N-03 | `present` without evidence | `ck_evidence_when_present` |
| N-04 | **Verification on D5** | `ck_verification_d4_only` |
| N-05 | Verification without metadata | `ck_verification_metadata` |
| N-06 | Ambiguity flag, no candidates | `ck_ambiguity_metadata` |
| N-07 | Ambiguity low > high | `ck_ambiguity_metadata` |
| N-08 | Contradiction flag, no text | `ck_contradiction_metadata` |
| N-09 | Duplicate coding grain | `UNIQUE` on (profile, dim, rater, rulebook) |
| N-10 | Nonexistent profile | `..._profile_id_fkey` |
| N-11 | `not_applicable` on a profile | `ck_profile_not_applicable` |
| N-12 | Malformed `profile_id` | `profile_profile_id_check` |
| N-13 | `dimension_number` = 7 | `..._dimension_number_fkey` |
| N-14 | DELETE profile holding scores | FK `ON DELETE RESTRICT` |
| N-15 | Adjudication citing both corpora | `ck_adjudication_one_corpus` |
| N-16 | Engagement mean without denominator | `ck_engagement_denominator` |
| N-17 | Survey record without consent | `survey_respondent_consent_confirmed_check` |
| N-18 | `not_applicable` with modality `required` | `ck_req_not_applicable_modality` |

---

## 3. Findings

### F-01 — [DEFECT, correction recommended] `v_profile_completeness` contradicts the frozen definition

**The frozen definition** of `completeness_index` is *(dimensions with `present` or `absent_stated`) ÷ 6*.
**The shipped view** divides by the number of dimensions **actually scored**, not by 6.

**Empirically demonstrated:** PRF-00006, coded on 2 of 6 dimensions (both informative), reports **1.00**. The frozen definition gives **0.33**.

This is not a stylistic difference. It means a partially coded profile is indistinguishable from a fully documented one, and the "low-completeness records reported as a separate analytic category" rule — a frozen requirement — cannot be applied reliably. Since the implementation contradicts a frozen definition, correcting it restores the framework rather than modifying it.

A corrected view is supplied in `alcsm_integrity_patch_OPTIONAL.sql` (item C-1) and was verified to produce 1.00 / 0.33 / 0.33 / 0.17 correctly across the test profiles. It also adds a `coding_complete` boolean, separating *sparse profile* from *incomplete coding* — analytically different situations that currently look identical.

*Note on the test suite itself:* my original assertion V-04 expected 1.00 for PRF-00003 and therefore **encoded the bug**. Under the corrected view it returns 0.17, which is right. Treat this as a caution about test suites written against the implementation rather than the specification.

### F-02 — [Reliability integrity] Adjudication flag not tied to rater role

`is_adjudication` and `rater_id` can disagree. A primary rater's row flagged `TRUE` is silently dropped from `v_reliability_input`; an ADJUDICATOR row flagged `FALSE` is currently caught only by the view's role filter. Both corrupt α without raising any error. **Highest-priority gap after F-01.** Patch item C-2.

### F-03 — [Frozen rule unenforced] Tie-break routing

`resolution_route = 'consensus'` is accepted with a disagreement magnitude of 5, violating the frozen rule that magnitude ≥ 2 must escalate. Patch item C-3.

### F-04 — [Coherence] Missing-status / evidence combinations

`absent_stated` without evidence is accepted (a positive textual claim with nothing to support it), and `unavailable` **with** evidence is accepted (self-contradictory). Patch item C-4.

### F-05 — [Coherence] Ambiguity candidates need not bracket the score

A score of 5 with candidates (1, 2) is accepted. The frozen rule is that the assigned score is one of the candidates. Patch item C-5.

### F-06 — [Reproducibility] `taxonomy_version_id` nullable

Scores can be recorded without a taxonomy version, making them unreproducible. Patch item C-6 is supplied **commented out**, since it can only be enabled after taxonomy anchoring is complete.

### F-07 — [Hygiene] Uncontrolled values

Future `collection_ts`; `coding_ts` predating collection; free-text language/country values such as `'ENGLISH'`, `'Germany'`. Patch items C-7, C-8. Note C-8 validates *shape only* (two letters), not membership of the real ISO list.

### F-08 — [Ethics linkage] Engagement without collected activity data

`rq4_content_engagement` can be populated for a profile whose `activity_data_collected` is FALSE — i.e. impact data recorded where the corresponding collection was not flagged as performed and ethically justified. Patch item C-9 (trigger).

### Deliberately not patched
Three rules are left to process control rather than constraints, because enforcing them at row level would block legitimate incremental work: complete six-dimension coverage, agreement between `adjudication_record.final_score` and the adjudicated score row, and adjudication only where real disagreement exists. Checklist queries Q-06, Q-08 and Q-09 detect all three.

**Patch verification:** applying `alcsm_integrity_patch_OPTIONAL.sql` to a fresh schema closed 10 of the 15 probed gaps; the remaining 5 are the deliberately-deferred items above plus C-6, which is intentionally disabled. The full 56-test suite still passes afterwards, with the single expected change to V-04 described in F-01.

---

## 4. Pre-Load Validation Checklist

Execute before loading the real 500-profile dataset. Every query should return **zero rows** unless stated otherwise.

**Stage A — Environment**
- [ ] A-1 Schema deployed to a clean database; all 70 statements succeed.
- [ ] A-2 Decision recorded on `alcsm_integrity_patch_OPTIONAL.sql`: applied in full, applied selectively (which items), or declined with reasons.
- [ ] A-3 **F-01 correction applied** regardless of the rest of the patch, or a written justification for retaining the current behaviour.
- [ ] A-4 Full validation suite run on a throwaway database: 56/56 as specified.
- [ ] A-5 Backup and restore tested; restored copy passes A-4.

**Stage B — Reference data**
- [ ] B-1 `dimension_ref` contains exactly 6 rows with frozen codes; D4 alone has `external_verification_permitted = TRUE`.
- [ ] B-2 `missing_status_ref` contains exactly 4 rows.
- [ ] B-3 `precedent_ref` contains all 15 rulings with real text (not placeholders).
- [ ] B-4 `rater_ref` populated; `blind_to_hypotheses` recorded for each rater (bias-control disclosure).
- [ ] B-5 `taxonomy_version` stamped **after** job-posting anchoring; `frozen = TRUE`.
- [ ] B-6 `sampling_batch` rows created *before* collection, with `result_set_size` recorded.

**Stage C — Outstanding decisions (from Task 4 §9)**
- [ ] C-1 Double-coding subset defined (which ~10–15%, chosen how). Non-random selection must be justified — α will not generalise otherwise.
- [ ] C-2 Re-identification mapping decision made and, if retained, stored **outside** this database under separate access control with a retention/destruction schedule.
- [ ] C-3 Activity observation window fixed and identical across all profiles.
- [ ] C-4 Language/localisation scope fixed.

**Stage D — Integrity queries (expect 0 rows)**

```sql
-- Q-01 verification outside D4
SELECT * FROM alcsm_dimension_score WHERE verification_used AND dimension_number <> 4;

-- Q-02 adjudication flag disagrees with rater role
SELECT * FROM alcsm_dimension_score
WHERE (is_adjudication AND rater_id <> 'ADJUDICATOR')
   OR (NOT is_adjudication AND rater_id = 'ADJUDICATOR');

-- Q-03 unavailable with a non-zero score, or with evidence
SELECT * FROM alcsm_dimension_score
WHERE missing_status='unavailable' AND (score <> 0 OR evidence_text IS NOT NULL);

-- Q-04 absent_stated without evidence
SELECT * FROM alcsm_dimension_score WHERE missing_status='absent_stated' AND evidence_text IS NULL;

-- Q-05 ambiguity candidates that do not bracket the score
SELECT * FROM alcsm_dimension_score
WHERE ambiguity_flag AND (score < ambiguity_candidate_low OR score > ambiguity_candidate_high);

-- Q-06 profiles not coded on all six dimensions
SELECT profile_id, count(*) FROM v_final_profile_score
GROUP BY profile_id HAVING count(*) <> 6;

-- Q-07 scores lacking a taxonomy version
SELECT * FROM alcsm_dimension_score WHERE taxonomy_version_id IS NULL;

-- Q-08 adjudication_record final_score inconsistent with the stored adjudicated row
SELECT a.* FROM adjudication_record a
JOIN alcsm_dimension_score s
  ON s.profile_id = a.profile_id AND s.dimension_number = a.dimension_number
 AND s.is_adjudication
WHERE s.score <> a.final_score;

-- Q-09 adjudication recorded where raters did not actually disagree
SELECT * FROM adjudication_record WHERE score_rater_a = score_rater_b;

-- Q-10 consensus route used despite magnitude >= 2
SELECT * FROM adjudication_record
WHERE abs(score_rater_a - score_rater_b) >= 2 AND resolution_route <> 'escalated';

-- Q-11 engagement criterion without collected activity data
SELECT r.profile_id FROM rq4_impact_indicator r JOIN profile p USING (profile_id)
WHERE r.rq4_content_engagement IS NOT NULL AND NOT p.activity_data_collected;

-- Q-12 provenance completeness
SELECT * FROM profile
WHERE search_query IS NULL OR inclusion_reason IS NULL OR collection_ts IS NULL;

-- Q-13 postings missing raw text (blocks taxonomy anchoring)
SELECT * FROM job_posting WHERE raw_posting_text IS NULL OR length(raw_posting_text) < 50;

-- Q-14 NLP predictions on a different information base than human coding
SELECT * FROM nlp_model_run WHERE information_base <> 'profile_text_only';
```

**Stage E — Expected-value checks (verify manually)**
- [ ] E-1 `v_reliability_input` excludes every adjudicated row (`SELECT count(*) FROM v_reliability_input WHERE ...` matches independent rows only).
- [ ] E-2 `v_final_profile_score` returns exactly one row per profile × dimension.
- [ ] E-3 `v_profile_completeness` denominator is 6 (post-F-01 correction).
- [ ] E-4 `v_credential_gap_by_dimension` excludes `not_applicable` and `unavailable` rows.
- [ ] E-5 Trigger `updated_ts` fires on UPDATE of `profile` and `job_posting`.

**Stage F — Sign-off**
- [ ] F-1 All Stage D queries return zero rows on the pilot data.
- [ ] F-2 Findings F-01 to F-08 each have a recorded disposition (patched / accepted with justification).
- [ ] F-3 Supervisor sign-off on the patch decision.
- [ ] F-4 Task 5 ethics documentation complete — **blocking for collection**.

---

## 5. Deliverables

| File | Purpose |
|---|---|
| `alcsm_validation_tests.sql` | Annotated test suite; 18 must-fail statements, view assertions. Executed: 18/18 rejected, 15 constraints exercised. |
| `alcsm_validation_harness.py` | Automated runner producing a pass/fail table (56 tests). |
| `alcsm_gap_probes.py` | The 15 probes that discovered F-01 to F-08. |
| `alcsm_integrity_patch_OPTIONAL.sql` | **Not applied.** Proposed remediation, verified to apply cleanly and close 10/15 gaps. Your decision. |

**The schema was not modified.** The patch file is a proposal requiring your decision; only the F-01 correction is recommended unconditionally, because there the implementation contradicts a frozen definition.
