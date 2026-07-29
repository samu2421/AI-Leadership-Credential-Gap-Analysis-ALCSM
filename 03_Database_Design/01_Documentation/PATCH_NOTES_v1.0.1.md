# ALCSM PostgreSQL Schema v1.0.1 — Patch Notes
### Final Implementation Freeze for Task 4

**Release:** v1.0.0 → v1.0.1
**Type:** implementation hardening. **No conceptual change.**
**Verification:** executed against live PostgreSQL 16.14, not reasoned about on paper.

---

## 1. Executive Summary

| Metric | Result |
|---|---|
| Corrections applied | **F-01 – F-05** |
| Corrections deferred | F-06, F-07, F-08 (documented, supplied separately) |
| Validation tests | **67 / 67 pass** |
| Gap probes closed by patch | **7 of 15** (F-01–F-05 fully closed) |
| Consolidated schema vs. patch path | **catalogue-identical** (129 constraints, view definitions byte-identical by MD5) |
| Final schema | 22 tables · 5 views · 66 CHECK constraints · 33 foreign keys |
| ER structure change | **none** — 22 entities, 33 relationships, verified against catalogue |
| Conceptual rules altered | **zero** |

---

## 2. Changes Applied

### F-01 — `v_profile_completeness` corrected *(unconditional)*

**Defect.** The frozen definition is `completeness_index = (dimensions with present|absent_stated) ÷ 6`. The v1.0.0 view divided by the number of dimensions *actually scored*.

**Impact.** A profile coded on 2 of 6 dimensions reported **1.00** instead of **0.33**, making a partially coded profile indistinguishable from a fully documented one and rendering the frozen rule "report low-completeness records as a separate analytic category" unenforceable.

**Fix.** Denominator fixed at 6; `LEFT JOIN` from `profile` so uncoded profiles appear with 0.00 rather than vanishing; added `coding_complete` boolean.

**Why `coding_complete` is not a new construct.** It exposes a distinction the frozen framework already makes — a *sparse profile* (6 dimensions coded, few informative) versus *incomplete coding* (fewer than 6 coded) — which v1.0.0 silently conflated. Verified: PRF-00010 = 0.33 / 6 coded / complete; PRF-00006 = 0.17 / 1 coded / incomplete. Same index value would previously have hidden two different situations.

### F-02 — Adjudication flag aligned to rater role

**Defect.** `is_adjudication` and `rater_id` could disagree. A primary rater's row flagged `TRUE` was silently dropped from `v_reliability_input` with **no error raised**, corrupting Krippendorff's α invisibly.

**Fix.** `ck_adjudication_role_alignment` on `alcsm_dimension_score` and `job_requirement_score`.

**Conceptual status.** The frozen rule ("reliability is computed on independent, pre-adjudication rows only") is unchanged; it is now enforced at row level rather than depending on the view's role filter alone. This was the highest-risk gap in v1.0.0 because its failure mode is silent.

### F-03 — Tie-break routing enforced

**Defect.** `resolution_route = 'consensus'` was accepted at a disagreement magnitude of 5, violating the frozen rulebook (§1.5): magnitude 1 may go to consensus; magnitude ≥ 2 must escalate.

**Fix.** `ck_tiebreak_route` on `adjudication_record`.

**Verified both directions.** Magnitude 5 + consensus → rejected (N-21). Magnitude 1 + consensus → still permitted (T-17).

### F-04 — Missing-status / evidence coherence

**Defect.** `absent_stated` without evidence was accepted (a positive textual claim with nothing supporting it), and `unavailable` **with** evidence was accepted (self-contradictory).

**Fix.** Four constraints across both scoring tables.

**Conceptual status.** Enforces the existing frozen distinction — `absent_stated` is informative and evidenced; `unavailable` means no evidence exists. Both feed `completeness_index` and every missingness analysis, so incoherent rows would have propagated into results.

### F-05 — Ambiguity candidates must bracket the score

**Defect.** A score of 5 with candidates (1, 2) was accepted.

**Fix.** `ck_ambiguity_brackets_score`.

**Conceptual status.** The frozen rulebook states that where evidence supports two adjacent scores the annotator records both and assigns one of them (default-low picks the lower). The assigned score is therefore necessarily within range. Verified: (5; 1–2) rejected, (2; 2–3) accepted.

---

## 3. Changes Deferred

Assessed against your stated criterion — defer only if the item depends on a later implementation stage. **One assessment does not support deferral, and I am flagging it rather than quietly accepting the grouping.**

| Item | Depends on a later stage? | Disposition |
|---|---|---|
| **F-06** taxonomy_version_id NOT NULL | **Yes, unambiguously.** Taxonomy term lists are to be anchored to the 200 job postings and only then version-stamped. Enforcing NOT NULL first would make pilot coding impossible. | Deferred; supplied commented-out |
| **F-07** temporal + ISO hygiene | **No.** This does not depend on any later stage. It was grouped with F-06/F-08 in the earlier triage, but on the stated criterion it could be applied now. | Supplied **active** (ISO shape checks) with the future-timestamp check left commented and its caveat explained |
| **F-08** engagement requires activity data | **Yes.** Depends on the Task 5 ethics decision for post-level activity data and on collection workflow ordering; `activity_data_collected` may legitimately be set after criterion extraction. | Deferred; supplied commented-out |

**F-07 technical caveat, stated so the decision is informed.** The future-timestamp check uses `now()`, which is not `IMMUTABLE`. PostgreSQL permits it in a `CHECK` and the predicate is monotone-safe here (a row valid at insert stays valid as time advances), but non-immutable CHECK constraints are poor practice generally and can behave unexpectedly under dump/restore. An application-level guard at collection time is cleaner. The ISO *shape* checks carry no such caveat and are supplied active — note they validate shape only (two letters), not membership of the real ISO register.

**F-07(d) is not implementable as a constraint.** "`coding_ts` must not precede the profile's `collection_ts`" is a cross-table predicate requiring a trigger. A checklist detection query is supplied instead.

### Permanently unpatched, by design
Three rules stay under process control because a row-level constraint would block legitimate incremental work: complete six-dimension coverage; `adjudication_record.final_score` matching the adjudicated score row; adjudication only where a genuine disagreement exists. Covered by checklist queries Q-06, Q-08, Q-09.

---

## 4. Verification Record

### 4.1 Validation suite — 67/67

Original 56 tests **plus** 11 new v1.0.1 regression tests (N-19 – N-25, T-17, T-18, V-09, V-10). All pass against both deployment paths.

### 4.2 Two test-assertion corrections — disclosed, not hidden

Two of my own assertions were wrong and were corrected. Both matter methodologically:

- **V-04** expected `completeness_index = 1.00` for PRF-00003. That expectation *encoded the F-01 bug*: the test was written against the implementation rather than the specification, so it validated the defect. Corrected to 0.17 (1 informative ÷ 6).
- **V-09** expected PRF-00006 to have 2 scored dimensions; it has 1. My expectation was carried over from a gap-probe run where an extra row existed.

In both cases the database was right and the test was wrong. Recorded because "our tests all passed" is worth much less when the tests were derived from the code under test.

### 4.3 Gap probes re-run — and one false positive caught

Post-patch: 7 of 15 probes now blocked. G-06 initially reported "blocked", which would have wrongly implied F-06 was applied. On investigation this was a **unique-key collision** with test T-18, not a constraint firing. Retested on a clean key slot: the row inserted with `taxonomy_version_id = NULL`, confirming **F-06 is genuinely still open**, as intended.

| Probe | Pre-patch | Post-patch |
|---|---|---|
| G-01, G-02 (F-04) | accepted | **blocked** |
| G-03, G-04 (F-02) | accepted | **blocked** |
| G-05 (F-05) | accepted | **blocked** |
| G-09 (F-03) | accepted | **blocked** |
| G-06 (F-06) | accepted | accepted — deferred as intended |
| G-10 – G-13 (F-07) | accepted | accepted — deferred |
| G-15 (F-08) | accepted | accepted — deferred |
| G-07, G-08, G-14 | accepted | accepted — process control by design |

### 4.4 Deployment-path equivalence

Two paths were compared at catalogue level:
1. v1.0.0 schema + `alcsm_patch_v1.0.0_to_v1.0.1.sql`
2. consolidated `alcsm_schema_v1.0.1.sql` on a clean database

`diff` of all constraint definitions: **identical**, 129 constraints each. View definitions compared by MD5: **identical**. This guarantees no drift between the upgrade path and a fresh install — a real risk in hand-maintained schema files.

### 4.5 ER diagram regenerated from the catalogue

Relationships were extracted programmatically from `pg_constraint` on the patched database and compared to the documented diagram: **33 in the catalogue, 33 in the diagram, zero discrepancies in either direction.** The diagram is version-stamped v1.0.1.

**Structurally unchanged, as expected.** F-01 modified a view; F-02–F-05 added CHECK constraints. Neither alters entities, keys or cardinality. The regeneration confirms synchronisation rather than producing a different picture.

---

## 5. Confirmation of Conceptual Non-Interference

Explicitly confirmed unchanged by this patch:

| Frozen element | Status |
|---|---|
| Six ALCSM dimensions, definitions, theoretical anchors | **Unchanged** |
| 0–5 scoring criteria, all dimensions | **Unchanged** |
| Eight taxonomies (structure and term lists) | **Unchanged** |
| Coding rulebook, precedent library P-01–P-15 | **Unchanged** |
| Measurement model (formative composite index) | **Unchanged** |
| Validation strategy | **Unchanged** |
| Research questions and sub-questions | **Unchanged** |
| Terminology standard (credential *signals*, not competence) | **Unchanged** |
| Open items (aggregation, weights, thresholds) | **Still open** — no composite or band column exists in v1.0.1 |

Every applied change is either a **correction** restoring agreement with a frozen definition (F-01) or an **encoding** enforcing an existing frozen rule at row level (F-02–F-05). None introduces, removes or reinterprets a methodological rule.

**One-line justification for the thesis:** *v1.0.1 corrected a completeness-index computation that contradicted the frozen definition, and moved four existing coding rules from documentary to database-level enforcement; no conceptual element of ALCSM v1.0 was modified.*

---

## 6. Deliverables

| File | Role |
|---|---|
| `alcsm_schema_v1.0.1.sql` | **Consolidated schema — single source of truth.** Fresh installs use this. |
| `alcsm_patch_v1.0.0_to_v1.0.1.sql` | Upgrade path for an existing v1.0.0 deployment. Idempotent. |
| `alcsm_optional_recommendations.sql` | F-06/F-07/F-08 menu with honest per-item stage-dependency assessment. |
| `alcsm_er_diagram.mermaid` | ER diagram, v1.0.1-stamped, catalogue-verified. |
| `alcsm_validation_harness_v1.0.1.py` | 67-test suite. |
| `alcsm_gap_probes_v1.0.1.py` | 15 probes for residual unenforced rules. |
| `Task4c_ER_Design_Documentation.md` | Design documentation — see §7 for the amendments this release requires. |

---

## 7. Documentation Amendments Required

`Task4c_ER_Design_Documentation.md` remains accurate on entities, keys, cardinality, normalisation and rationale. Three amendments bring it to v1.0.1:

1. **§11 (reliability protection)** — the stated limitation, that `is_adjudication` and `rater_id` can be set inconsistently, is **now resolved** by F-02. Reliability protection is now *five* mechanisms, with row-level role alignment added.
2. **§14 (weakness table)** — W-3 (adjudication flag) and W-4 (completeness view) are **resolved in v1.0.1**. W-1 (3NF `search_query` denormalisation), W-2 (`anchored_to_batch` without FK) and W-5 (`rq4_seniority_progression_rate` sharing source data with D5) **remain open and should still be disclosed in the thesis.**
3. **Version references** — v1.0.0 → v1.0.1; constraint count 66 CHECK constraints.

The Chapter 3 draft text in §13 needs one sentence updated: the validation account should read *sixty-seven cases* rather than fifty-six, and may note that two test assertions were themselves found defective and corrected — a point that strengthens rather than weakens the account.

---

## 8. Implementation Freeze Declaration

**Schema v1.0.1 is the final implementation freeze for Task 4.**

The database implements the frozen ALCSM v1.0 conceptual framework and is verified consistent with it. Remaining work is data collection, annotation, reliability testing, NLP development and analysis — not further schema design.

Any future schema change requires a version increment (v1.0.2 / v1.1.0) with documented justification. Changes that would alter a conceptual rule require a change to the **framework** version first, not the schema.

**Outstanding before first real data load** (unchanged by this release):
- Double-coding subset defined and its selection method justified
- Re-identification mapping decision, stored outside this database if retained
- Activity observation window fixed
- Language/localisation scope fixed
- Taxonomy anchoring complete, then F-06 enabled
- **Task 5 ethics documentation — blocking for collection**
