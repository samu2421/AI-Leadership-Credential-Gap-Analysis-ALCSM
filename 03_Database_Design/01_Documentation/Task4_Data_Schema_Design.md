# Task 4 — Data Schema Design
### Implementation Layer of the Frozen ALCSM v1.0 Framework

**Thesis:** *The AI Leadership Credential Gap: An NLP Audit of 500 LinkedIn Profiles*
**Status:** ALCSM v1.0 is conceptually frozen. This document and its accompanying DDL (`alcsm_schema_v1.sql`) constitute an *implementation* of that framework. No dimension, scoring criterion, taxonomy, coding rule, precedent, measurement-model or validation decision is altered.

**Marker legend (applied to every design choice):**
- **[Frozen]** — already fixed in ALCSM v1.0; the schema merely gives it a physical form.
- **[Encoding]** — an implementation-level representation of an existing frozen decision.
- **[Convention]** — a database or engineering choice with no conceptual content.
- **[!] Flagged** — a schema decision that could influence future statistical analysis or validity, surfaced here rather than made silently.

**Verification note.** The DDL has been parsed with `pglast`, which wraps the genuine PostgreSQL parser; all 70 statements parse without error. This confirms syntactic validity only — semantic correctness against your eventual data remains to be confirmed on first load.

---

## 1. Architecture Overview

The architecture comprises **twenty-two base tables and five analysis views** across six functional groups. The design principle throughout: *frozen rules are enforced by the database wherever possible, rather than relying on annotator discipline or analyst memory.* A rule encoded as a `CHECK` constraint cannot erode over 500 profiles; a rule written only in a rulebook can.

| Group | Tables | Purpose |
|---|---|---|
| Reference | `dimension_ref`, `missing_status_ref`, `precedent_ref`, `rater_ref`, `taxonomy_version`, `taxonomy_term` | Controlled vocabularies; frozen taxonomies and their versioned term lists |
| Provenance | `sampling_batch` | Documented, reproducible searches for both corpora |
| Corpus 1 | `profile`, `profile_raw_section` | LinkedIn profiles (n ≈ 500) and verbatim section text |
| Corpus 2 | `job_posting` | Job postings (n ≈ 200) with raw text retained |
| Corpus 3 | `survey_instrument`, `survey_respondent`, `survey_response_item` | Expert survey / validation data |
| Annotation | `alcsm_dimension_score`, `job_requirement_score`, `profile_derived` | Human coding, both corpora, plus derived flags |
| Criterion | `rq4_impact_indicator` | RQ4 observable professional impact indicators |
| NLP | `nlp_model_run`, `nlp_prediction` | Pipeline runs and predictions (RQ5) |
| Audit | `annotation_revision_log`, `adjudication_record`, `reliability_result` | Revision trail, adjudication trail, stored reliability results |

### 1.1 Entity-relationship overview

```
                        ┌──────────────────┐
                        │  sampling_batch  │  [Frozen] provenance
                        └────────┬─────────┘
                     ┌───────────┴───────────┐
                     ▼                       ▼
             ┌───────────────┐       ┌────────────────┐
             │    profile    │       │  job_posting   │
             │   (n ≈ 500)   │       │   (n ≈ 200)    │
             └───┬───┬───┬───┘       └────────┬───────┘
                 │   │   │                    │
     ┌───────────┘   │   └──────────┐         │
     ▼               ▼              ▼         ▼
┌──────────────┐ ┌────────────┐ ┌────────┐ ┌──────────────────────┐
│ profile_raw_ │ │   alcsm_   │ │  rq4_  │ │  job_requirement_    │
│   section    │ │ dimension_ │ │ impact_│ │       score          │
│ (long format)│ │   score    │ │indicat.│ │ (required levels)    │
└──────────────┘ └─────┬──────┘ └────────┘ └──────────┬───────────┘
                       │   ▲                          │
                       │   │ dimension_ref            │
                       │   │ missing_status_ref       │
                       │   │ precedent_ref            │
                       │   │ rater_ref                │
                       │   │ taxonomy_version         │
                       ▼   │                          ▼
              ┌──────────────────┐          ┌──────────────────┐
              │ nlp_prediction   │          │ adjudication_    │
              │  ← nlp_model_run │          │    record        │
              └──────────────────┘          └──────────────────┘

              ┌──────────────────────────────────────────────┐
              │ survey_instrument → survey_respondent →      │
              │                     survey_response_item     │
              │ [Frozen] content validity; not a score source│
              └──────────────────────────────────────────────┘

Views: v_reliability_input · v_final_profile_score · v_profile_completeness
       v_credential_gap_by_dimension · v_nlp_evaluation
```

---

## 2. Dataset 1 — LinkedIn Profiles

### 2.1 `profile`
Carries identity (pseudonymous), provenance, and collection context. **[Frozen]** No name, URL, photograph or direct identifier is stored. **[Frozen]** Every record carries `search_query`, `search_rank_position`, `inclusion_reason`, `collection_ts`, `profile_language`, `profile_geography` — the provenance set fixed pre-Task 4, so that title-gating and ranking bias remain analysable rather than invisible.

`activity_data_collected` **[Frozen]** flags records for which post-level activity was gathered, since that data carries its own ethics/GDPR justification separate from static profile fields.

### 2.2 `profile_raw_section` — **[!] flagged design decision**
Raw text is stored in **long format** (one row per profile × section) rather than as wide columns.

*Why this matters for validity:* a wide-column design conflates two distinct states in a single `NULL` — "the section exists but is empty" versus "the section was not retrievable at collection." That conflation would propagate directly into the frozen `unavailable` missing-status determination and corrupt your missingness analysis. The long format carries an explicit `section_available` boolean, keeping the two separable. **[Encoding]** of the frozen missing-data distinction.

*Cost:* queries need a join or pivot to reconstruct a full profile. This is a deliberate trade of query convenience for measurement integrity.

---

## 3. Dataset 2 — Job Postings

`job_posting` mirrors the profile provenance structure. Two decisions carry forward frozen requirements:

- **[Frozen]** `raw_posting_text` is `NOT NULL`. Taxonomy anchoring cannot be performed on parsed summaries; losing raw text would forfeit the anchoring procedure entirely and require re-collection.
- **[!]** `posted_date` is captured to permit recency control. Postings and profiles are collected at one moment but describe different time horizons; without posting dates you cannot check whether requirement levels drift across the collection window.

Requirement scores live in a **separate table** (`job_requirement_score`), not in the profile score table. **[Frozen]** — required and held levels are not interchangeable under the commensurability caveat, and the separation makes it structurally impossible to pool them by accident.

`requirement_modality` (`required` / `preferred` / `unspecified`) **[Encoding]** preserves a distinction the source text makes and the frozen rubric does not erase: "MSc required" and "MSc preferred" are different claims.

---

## 4. Dataset 3 — Expert Survey / Validation Data

Three tables: `survey_instrument`, `survey_respondent`, `survey_response_item`.

- **[Frozen]** Consent precedes any item: `consent_confirmed` carries `CHECK (consent_confirmed = TRUE)`, so a non-consenting record cannot physically exist in the table.
- **[Frozen]** Withdrawal is recordable at any time (`withdrawal_flag`, `withdrawal_ts`).
- **[Convention]** Expertise is stored in coarse bands (`0-4`, `5-9`, `10-14`, `15+`) rather than exact years, limiting re-identification risk in a small expert population.
- **[!]** `survey_instrument.purpose` distinguishes `content_validity` from `expert_weighting_elicitation`. This is flagged because **if the survey is used to elicit weights, those weights must not later be validated against the same respondents' data** — that is the circularity trap already identified in the frozen framework. Recording purpose at the instrument level makes the separation auditable.

The survey supports **content validity** for a formative index. **[Frozen]** It is not a source of ALCSM dimension scores.

---

## 5. Annotation, Adjudication and Reliability

### 5.1 Frozen rules enforced as database constraints

| Frozen rule | Enforcement |
|---|---|
| External verification permitted for D4 only | `CHECK (verification_used = FALSE OR dimension_number = 4)` |
| Verification metadata required when used | Composite `CHECK` on source, timestamp, outcome |
| Ambiguity flag requires both candidate scores, low ≤ high | Composite `CHECK` |
| Contradiction flag requires contradiction text | `CHECK` |
| `unavailable` implies score 0 | `CHECK (missing_status <> 'unavailable' OR score = 0)` |
| `not_applicable` invalid for profiles | `CHECK (missing_status <> 'not_applicable')` |
| Evidence required when a dimension was actually scored on content | `CHECK (missing_status <> 'present' OR evidence_text IS NOT NULL)` |
| One score per rater per dimension per profile per rulebook version | `UNIQUE` constraint |
| Research data never cascades on delete | `ON DELETE RESTRICT` throughout |

### 5.2 Adjudication is additive — **[Frozen]**
Adjudicated scores are inserted as **new rows** with `is_adjudication = TRUE`; original rater rows are never overwritten. `adjudication_record` separately stores both raters' scores, the disagreement magnitude (a generated column), the resolution route, the final score and the documented reason.

**[Frozen]** `resolution_route` encodes the frozen tie-breaking rule: magnitude 1 permits a consensus attempt; magnitude ≥ 2 escalates directly, since a two-point gap signals rubric ambiguity rather than a judgement call.

### 5.3 `v_reliability_input` — **[!] the most consequential view**
Reliability must be computed on **independent, pre-adjudication** scores. **[Frozen]** Including adjudicated rows would inflate agreement artificially and invalidate every α you report. Rather than trusting analysis code to remember this, the view filters to `is_adjudication = FALSE` and to raters with role `primary`/`secondary` only. Analysis should query the view, never the base table.

### 5.4 `reliability_result` — stored, not merely reported
Per-dimension α, bootstrap CI bounds, raw percentage agreement, `n_units`, **and `score_variance`**. **[!]** Variance is stored deliberately: with a small pilot and skewed distributions (likely on D5/D6), low variance can deflate α despite high raw agreement. Storing variance alongside α means a low coefficient can be diagnosed rather than misread as poor coding.

---

## 6. RQ4 Criterion Variables

`rq4_impact_indicator` is a **separate table keyed on `profile_id`**. **[Frozen]** Physical separation backs the conceptual predictor/criterion independence, and the annotation interface must not surface these values to raters during dimension coding.

Two flags carried into the schema as column comments:

- **[Frozen]** `rq4_recognition_count` counts recognition *conferred by others*. Publications, patents and repository metrics inform D4 and are excluded here — reusing them as criterion would be circular.
- **[!]** `rq4_seniority_progression_rate` shares source data with D5 (employment history). The constructs are distinct (trajectory over time vs. current static level) and the D5 score is barred as an input, but this remains the weakest of the four independence claims. It is flagged in the DDL itself so the caveat travels with the data.

**[Encoding]** `ck_engagement_denominator` prevents a mean engagement value from existing without its post count and observation window — a stored mean without its denominator is uninterpretable and would silently distort any correlation with ALCSM scores.

---

## 7. NLP Pipeline

`nlp_model_run` records `model_name`, `model_version`, `random_seed`, `code_commit_hash` **[Convention]** for reproducibility, and — critically — **`information_base`**. **[Frozen]** Human and machine coders must operate on the same information base for RQ5 comparability; recording it per run makes any violation visible rather than assumed away.

`v_nlp_evaluation` joins predictions to the human gold standard and exposes signed error, absolute error and exact match per profile × dimension, supporting the per-dimension evaluation the frozen framework requires.

---

## 8. Version Control and Reproducibility

Every scored, predicted or collected record carries the versions under which it was produced: `alcsm_version`, `rulebook_version`, `taxonomy_version_id`, plus `model_version` / `pipeline_run_id` for predictions and `survey_version` for survey data. **[Frozen]** Any result can therefore be reconstructed exactly, and re-coding under a revised rulebook produces new rows rather than mutating history.

`taxonomy_version` and `taxonomy_term` store the frozen taxonomies' **term lists** with `constructed_ts`, `anchored_to_batch` and a `frozen` boolean. **[!]** `taxonomy_term.source_frequency` records each term's observed frequency in the anchoring corpus, distinguishing empirically anchored terms from a priori ones — directly supporting the examiner defence that the taxonomies are market-grounded rather than arbitrary.

---

## 9. Register of Flagged Decisions

These are surfaced rather than silently made, as instructed.

| # | Decision | Why flagged |
|---|---|---|
| F-1 | Raw text in long format with `section_available` | Prevents `NULL` conflating "empty" with "not retrieved"; protects the frozen missing-data logic |
| F-2 | `score` stored as `SMALLINT` but **ordinal** | Means are descriptive only; inferential analysis requires ordinal-appropriate methods. Noted in DDL comments and in `v_credential_gap_by_dimension` |
| F-3 | `not_applicable` excluded from `Gap_i`, not read as 0 | A posting silent on a dimension is not a requirement of level zero; treating it as such would systematically deflate the gap |
| F-4 | No composite or band column anywhere | Aggregation, weights and thresholds remain **open**; a stored composite would silently commit you to one method |
| F-5 | `v_reliability_input` excludes adjudicated rows | Including them inflates α; enforced structurally rather than by convention |
| F-6 | `score_variance` stored with α | Low variance deflates α independently of coding quality; needed to interpret D5/D6 results |
| F-7 | `rq4_seniority_progression_rate` shares source data with D5 | Weakest independence claim; flagged in DDL so the caveat is inseparable from the data |
| F-8 | `survey_instrument.purpose` distinguishes content validity from weight elicitation | Weights elicited from a sample cannot be validated on that same sample |
| F-9 | `sampling_batch.result_set_size` captured | Enables reporting what fraction of an algorithmically ranked result set entered the sample — a direct external-validity measure |
| F-10 | Double-coding subset selection not fixed in schema | **Requires your decision:** which ~10–15% of the main sample is double-coded. If chosen non-randomly, main-study α will not generalise to the full corpus |
| F-11 | Re-identification mapping deliberately absent from this database | **Requires an ethics decision:** if a pseudonym↔source mapping is retained at all, it must live outside this database under separate access control, and its retention/destruction schedule belongs in Task 5 |

Items **F-10** and **F-11** are the two that need a decision from you before data collection begins; the remaining nine are already resolved in the design.

---

## 10. Readiness

The data architecture implements the frozen framework without extending it. Aggregation function, dimension weights and classification thresholds are **absent by design** — they remain open pending empirical validation, exactly as declared.

**Deliverables:** `alcsm_schema_v1.sql` (PostgreSQL DDL, parser-validated) and this specification.

**Before first data load:** resolve F-10 (double-coding subset) and F-11 (re-identification mapping and its access control), populate `precedent_ref` with the P-01–P-15 rulings, populate `rater_ref`, and stamp `taxonomy_version` once job-posting anchoring is complete.

**Blocking for collection, not for schema work:** Task 5 ethics documentation, including the separate justification for post-level activity data.
