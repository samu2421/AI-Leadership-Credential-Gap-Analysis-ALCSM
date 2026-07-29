# ALCSM v1.0 Implementation Readiness Specification

### Definitive Implementation Bridge Between the Frozen Conceptual Framework (Tasks 1–3) and Data Schema Design (Task 4)

**Thesis:** *The AI Leadership Credential Gap: An NLP Audit of 500 LinkedIn Profiles*
**Status of ALCSM v1.0:** Conceptually frozen. This document introduces **no new dimensions, scoring criteria, taxonomies, annotation rules, validation logic, or measurement-model changes.** Its sole function is to fix canonical names, encodings, types, and conventions so that the database schema, annotation interface, NLP pipeline, statistical analysis, and thesis text all refer to identical constructs in identical terms.

**Standardisation-only guarantee.** Every element below is traceable to an already-frozen decision. Where an existing conceptual rule required a concrete storage encoding (most notably the missing-data rule in §2), the encoding is presented as an *implementation of* the frozen rule, with the source rule cited. No rule is altered, extended, or reinterpreted.

**Convention markers:** *[Frozen]* = restates an existing framework decision. *[Encoding]* = an implementation-level representation of a frozen decision. *[Convention]* = an arbitrary-but-fixed engineering choice with no conceptual content.

**Stack assumptions.** PostgreSQL for structured storage; Python for pipeline and analysis; `snake_case` throughout; UTC timestamps. *[Convention]*

---

## 1. Canonical Variable Dictionary

Naming rule: `snake_case`, no abbreviations except the fixed set `alcsm`, `nlp`, `rq4`, `id`, `ts`, `src`. Dimension variables are numbered `d1`–`d6` in the frozen order. *[Convention]*

### 1.1 Profile entity — identity and provenance

| Variable | Description | Type | Allowed values | Null convention | Example |
|---|---|---|---|---|---|
| `profile_id` | Pseudonymous primary identifier for a sampled profile. Never stores a real name or profile URL. | `TEXT` (PK) | `PRF-` + 5-digit zero-padded integer | Not nullable | `PRF-00137` |
| `profile_source` | Platform from which the record was collected. | `TEXT` | `linkedin` | Not nullable | `linkedin` |
| `search_query` | Verbatim query string used to locate the record. *[Frozen: provenance requirement]* | `TEXT` | Free text | Not nullable | `"Chief AI Officer"` |
| `search_rank_position` | Position of the record within the result set, where observable. | `INTEGER` | ≥ 1 | `NULL` if platform did not expose ordering | `14` |
| `collection_ts` | Timestamp of collection. | `TIMESTAMPTZ` | ISO 8601, UTC | Not nullable | `2026-08-03T09:41:00Z` |
| `inclusion_reason` | Coded reason the record met inclusion criteria. | `TEXT` | `title_match`, `title_variant_match`, `manual_review_included` | Not nullable | `title_match` |
| `profile_language` | Primary language of the profile text. | `TEXT` | ISO 639-1 two-letter code | `und` if undetermined | `en` |
| `profile_geography` | Self-declared location. | `TEXT` | ISO 3166-1 alpha-2 country code | `NULL` if not declared | `DE` |
| `sampling_batch_id` | Identifier for the collection batch. | `TEXT` | `BATCH-` + 3-digit integer | Not nullable | `BATCH-002` |

### 1.2 Profile entity — raw captured text

Raw text fields are retained verbatim to permit re-coding, taxonomy anchoring, and NLP re-runs without re-collection. *[Frozen: raw-text retention requirement]*

| Variable | Description | Type | Null convention | Example |
|---|---|---|---|---|
| `raw_headline` | Profile headline text. | `TEXT` | `NULL` if section absent | `Chief AI Officer at [redacted]` |
| `raw_about` | "About"/summary section text. | `TEXT` | `NULL` if section absent | *(long text)* |
| `raw_experience` | Employment history block, verbatim. | `TEXT` | `NULL` if section absent | *(long text)* |
| `raw_education` | Education block, verbatim. | `TEXT` | `NULL` if section absent | `MSc Artificial Intelligence, ...` |
| `raw_certifications` | Licences & certifications block, verbatim. | `TEXT` | `NULL` if section absent | `AWS Certified ML – Specialty, 2025` |
| `raw_contributions` | Publications/projects/featured block, verbatim. | `TEXT` | `NULL` if section absent | *(long text)* |
| `raw_activity` | Engagement/activity block, verbatim. Subject to the frozen ethics flag on post-level data. | `TEXT` | `NULL` if not collected or unavailable | *(long text)* |

### 1.3 ALCSM dimension scores (human-coded)

One row per `profile_id` × `dimension_number` × `rater_id`. *[Frozen: per-dimension coding log structure]*

| Variable | Description | Type | Allowed values | Null convention | Example |
|---|---|---|---|---|---|
| `score_record_id` | Surrogate primary key. | `BIGSERIAL` (PK) | ≥ 1 | Not nullable | `4821` |
| `profile_id` | FK → profile entity. | `TEXT` (FK) | Existing `profile_id` | Not nullable | `PRF-00137` |
| `dimension_number` | ALCSM dimension index, frozen order. | `SMALLINT` | `1`–`6` | Not nullable | `5` |
| `dimension_code` | Fixed short code for the dimension. | `TEXT` | `d1_education`, `d2_certifications`, `d3_experience`, `d4_contributions`, `d5_leadership`, `d6_engagement` | Not nullable | `d5_leadership` |
| `rater_id` | Annotator identifier. | `TEXT` | `RATER-A`, `RATER-B`, `ADJUDICATOR` | Not nullable | `RATER-B` |
| `score` | Assigned 0–5 ordinal score. *[Frozen: 0–5 criteria]* | `SMALLINT` | `0`–`5` | Not nullable | `3` |
| `evidence_text` | Short verbatim span(s) justifying the score. | `TEXT` | Free text, brief | `NULL` only when `missing_status <> 'present'` | `"leading enterprise AI strategy"` |
| `missing_status` | Three-state missing-data code. See §2. | `TEXT` | `present`, `absent_stated`, `unavailable`, `not_applicable` | Not nullable | `present` |
| `ambiguity_flag` | Ambiguous evidence flag. *[Frozen: `A` flag]* | `BOOLEAN` | `TRUE`/`FALSE` | Not nullable, default `FALSE` | `TRUE` |
| `ambiguity_candidate_low` | Lower candidate score when ambiguous. | `SMALLINT` | `0`–`5` | `NULL` when `ambiguity_flag = FALSE` | `2` |
| `ambiguity_candidate_high` | Upper candidate score when ambiguous. | `SMALLINT` | `0`–`5` | `NULL` when `ambiguity_flag = FALSE` | `3` |
| `contradiction_flag` | Contradictory evidence flag. *[Frozen: `C` flag]* | `BOOLEAN` | `TRUE`/`FALSE` | Not nullable, default `FALSE` | `TRUE` |
| `contradiction_text` | Conflicting spans, both quoted briefly. | `TEXT` | Free text | `NULL` when `contradiction_flag = FALSE` | *(two short spans)* |
| `verification_used` | External verification applied. Permitted for `d4_contributions` only. *[Frozen: D4-only rule]* | `BOOLEAN` | `TRUE`/`FALSE` | Not nullable, default `FALSE` | `TRUE` |
| `verification_source` | Source consulted. | `TEXT` | Free text / URL | `NULL` when `verification_used = FALSE` | `github.com/[redacted]` |
| `verification_ts` | Date of verification. | `TIMESTAMPTZ` | ISO 8601, UTC | `NULL` when `verification_used = FALSE` | `2026-08-04T11:02:00Z` |
| `verification_outcome` | Result of verification. | `TEXT` | `confirmed`, `contradicted`, `not_confirmable` | `NULL` when `verification_used = FALSE` | `confirmed` |
| `precedent_applied` | Precedent-library entry applied, if any. *[Frozen: P-01…P-15]* | `TEXT` | `P-01`–`P-15` | `NULL` if none applied | `P-03` |
| `rulebook_version` | Rulebook version under which the score was assigned. | `TEXT` | Semantic version string | Not nullable | `1.0` |
| `alcsm_version` | ALCSM framework version. | `TEXT` | Semantic version string | Not nullable | `1.0` |
| `coding_ts` | Timestamp of coding. | `TIMESTAMPTZ` | ISO 8601, UTC | Not nullable | `2026-08-05T14:20:00Z` |
| `notes` | Free-text annotator note. | `TEXT` | Free text | `NULL` if none | — |

### 1.4 Profile-level derived variables

Computed, never hand-entered. *[Frozen: derived from existing rules; no new constructs]*

| Variable | Description | Type | Allowed values | Example |
|---|---|---|---|---|
| `completeness_index` | Proportion of dimensions with `missing_status = 'present'` or `'absent_stated'`. *[Frozen: completeness index]* | `NUMERIC(3,2)` | `0.00`–`1.00` | `0.83` |
| `title_substance_contradiction_flag` | Profile-level contradiction indicator. *[Frozen: P-03]* | `BOOLEAN` | `TRUE`/`FALSE` | `TRUE` |
| `adjudicated` | Whether any dimension required adjudication. | `BOOLEAN` | `TRUE`/`FALSE` | `FALSE` |
| `double_coded` | Whether the profile was independently coded by two raters. | `BOOLEAN` | `TRUE`/`FALSE` | `TRUE` |

**Deliberately absent:** no `alcsm_total`, `alcsm_composite`, or `alcsm_band` variable is defined. Aggregation function, weights, and classification thresholds remain **open** by frozen declaration; composites are computed at analysis time, versioned by method, never stored as a canonical column. *[Frozen: open-items declaration]*

### 1.5 Job posting entity

| Variable | Description | Type | Allowed values | Null convention | Example |
|---|---|---|---|---|---|
| `posting_id` | Primary identifier. | `TEXT` (PK) | `JOB-` + 5-digit integer | Not nullable | `JOB-00042` |
| `posting_source` | Board/platform of origin. | `TEXT` | Free text, controlled at collection | Not nullable | `linkedin_jobs` |
| `search_query` | Verbatim query used. | `TEXT` | Free text | Not nullable | `"Head of AI" job` |
| `search_rank_position` | Result-set position. | `INTEGER` | ≥ 1 | `NULL` if unavailable | `7` |
| `collection_ts` | Collection timestamp. | `TIMESTAMPTZ` | ISO 8601, UTC | Not nullable | `2026-08-03T10:15:00Z` |
| `inclusion_reason` | Coded inclusion rationale. | `TEXT` | `title_match`, `title_variant_match`, `manual_review_included` | Not nullable | `title_match` |
| `posting_language` | Language of posting. | `TEXT` | ISO 639-1 | `und` if undetermined | `en` |
| `posting_geography` | Advertised location. | `TEXT` | ISO 3166-1 alpha-2 | `NULL` if not stated | `DE` |
| `raw_posting_text` | Full posting text, verbatim. Required for taxonomy anchoring. *[Frozen: raw-text retention]* | `TEXT` | Free text | Not nullable | *(long text)* |
| `raw_requirements_text` | Requirements/qualifications section, verbatim. | `TEXT` | Free text | `NULL` if section absent | *(long text)* |
| `sampling_batch_id` | Collection batch. | `TEXT` | `BATCH-` + 3-digit integer | Not nullable | `BATCH-005` |

### 1.6 Job posting requirement scores

Structurally parallel to §1.3, storing *required* rather than *held* levels. Table separated because, per the frozen commensurability caveat, the two score sets are not interchangeable and require independent validation. *[Frozen: Contribution-2 caveat]*

| Variable | Description | Type | Allowed values | Example |
|---|---|---|---|---|
| `requirement_record_id` | Surrogate PK. | `BIGSERIAL` (PK) | ≥ 1 | `912` |
| `posting_id` | FK → job posting entity. | `TEXT` (FK) | Existing `posting_id` | `JOB-00042` |
| `dimension_number` | Dimension index. | `SMALLINT` | `1`–`6` | `1` |
| `dimension_code` | Dimension short code. | `TEXT` | As §1.3 | `d1_education` |
| `required_score` | Required level on the frozen 0–5 criteria. | `SMALLINT` | `0`–`5` | `4` |
| `requirement_modality` | Whether stated as mandatory or preferred. | `TEXT` | `required`, `preferred`, `unspecified` | `required` |
| `evidence_text` | Verbatim span stating the requirement. | `TEXT` | Free text, brief | `"MSc in AI or related field required"` |
| `missing_status` | Three-state code per §2. | `TEXT` | As §2 | `present` |
| `rater_id` | Annotator. | `TEXT` | `RATER-A`, `RATER-B`, `ADJUDICATOR` | `RATER-A` |
| `rulebook_version` / `alcsm_version` / `coding_ts` | As §1.3. | — | — | — |

### 1.7 Survey entity

Structure kept minimal here; full instrument design belongs to Task 4 and the ethics documentation. *[No new constructs introduced.]*

| Variable | Description | Type | Allowed values | Null convention | Example |
|---|---|---|---|---|---|
| `respondent_id` | Pseudonymous respondent key. | `TEXT` (PK) | `RSP-` + 4-digit integer | Not nullable | `RSP-0031` |
| `consent_confirmed` | Informed consent recorded prior to any item. | `BOOLEAN` | `TRUE` only; `FALSE` records are not retained | Not nullable | `TRUE` |
| `consent_ts` | Consent timestamp. | `TIMESTAMPTZ` | ISO 8601, UTC | Not nullable | `2026-09-01T08:00:00Z` |
| `response_ts` | Submission timestamp. | `TIMESTAMPTZ` | ISO 8601, UTC | Not nullable | `2026-09-01T08:12:00Z` |
| `survey_version` | Instrument version. | `TEXT` | Semantic version string | Not nullable | `1.0` |
| `withdrawal_flag` | Participant withdrawal recorded. | `BOOLEAN` | `TRUE`/`FALSE` | Not nullable, default `FALSE` | `FALSE` |

### 1.8 NLP prediction entity

| Variable | Description | Type | Allowed values | Example |
|---|---|---|---|---|
| `prediction_id` | Surrogate PK. | `BIGSERIAL` (PK) | ≥ 1 | `20114` |
| `profile_id` | FK → profile entity. | `TEXT` (FK) | Existing `profile_id` | `PRF-00137` |
| `dimension_code` | Dimension predicted. | `TEXT` | As §1.3 | `d2_certifications` |
| `predicted_score` | Model-predicted 0–5 score. | `SMALLINT` | `0`–`5` | `3` |
| `prediction_confidence` | Model confidence, where the method exposes one. | `NUMERIC(4,3)` | `0.000`–`1.000`; `NULL` if not exposed | `0.812` |
| `model_name` | Model/pipeline identifier. | `TEXT` | Free text | `clf_d2_v1` |
| `model_version` | Model version. | `TEXT` | Semantic version string | `1.0` |
| `pipeline_run_id` | Batch run identifier. | `TEXT` | `RUN-` + 4-digit integer | `RUN-0007` |
| `prediction_ts` | Timestamp of prediction. | `TIMESTAMPTZ` | ISO 8601, UTC | `2026-10-02T16:40:00Z` |

---

## 2. Standard Missing-Data Policy

The frozen rulebook establishes one conceptual distinction: **stated absence** (the profile positively asserts that a credential is not held) versus **no evidence found** (the profile is silent). *[Frozen]* Implementation requires one further operational separation — silence caused by the profile itself versus silence caused by collection limits — because the two have different analytic consequences and must not be pooled. The four-value encoding below is the storage representation of these distinctions; it adds no scoring rule and changes no score.

| Code | Meaning | Scoring consequence | Analytic treatment |
|---|---|---|---|
| `present` | Evidence for the dimension exists in the profile and was scored on its merits. | Score assigned per frozen 0–5 criteria. | Included in all analyses. |
| `absent_stated` | The profile explicitly asserts the credential is not held (e.g., self-declared absence of formal education). | Scored low **on the basis of stated content**; this is informative, not missing. *[Frozen: Example 18, P-13]* | Treated as observed data, **not** as missingness. Counts toward `completeness_index`. |
| `unavailable` | No evidence found: the section is empty, absent, or was not retrievable at collection. | Score `0` per frozen convention, flagged as missing. *[Frozen: `missing = TRUE`]* | Analysed separately; excluded from claims about credential absence. Does **not** count toward `completeness_index`. |
| `not_applicable` | The dimension is structurally inapplicable to the record type (principally job-posting records that specify no expectation on a given dimension). | No score interpretation; `required_score` recorded as `0` with modality `unspecified`. | Excluded from `Gap_i` computation for that dimension rather than treated as a required level of zero. |

**Binding implementation rules.**
1. `missing_status` is **not nullable** on every scored record; every score carries an explicit state. *[Encoding]*
2. `unavailable` and `absent_stated` must never be collapsed in analysis or reporting. Conflating them would convert a data-collection artefact into a substantive claim about credentials — the exact error the frozen distinction exists to prevent. *[Frozen rationale]*
3. `completeness_index` counts `present` and `absent_stated` as informative; `unavailable` and `not_applicable` are excluded from the numerator. *[Encoding of the frozen completeness index]*
4. Low-completeness records are reported as a separate analytic category and are not silently pooled with fully documented records. *[Frozen]*
5. Missingness is reported descriptively per dimension (rate of `unavailable`) as a data-quality result in its own right, since differential missingness across dimensions is itself interpretable given the frozen verifiability gradient. *[Frozen: verifiability gradient]*
6. No imputation of dimension scores is performed. Imputing a credential signal would fabricate evidence of a signal that was never presented. *[Encoding consistent with the frozen conservative-scoring principle]*

---

## 3. RQ4 Criterion-Variable Specification

Per the frozen terminology standard, the RQ4 criterion construct is **observable professional impact indicators** — publicly observable signals of professional visibility, recognition, or reach, external to the credential signals ALCSM measures. The term "leadership effectiveness" is not used. *[Frozen]*

### 3.1 Final criterion variables

| Variable | Operational definition | Type | Allowed values | Null convention | Example |
|---|---|---|---|---|---|
| `rq4_network_reach` | Count of connections or followers displayed on the profile at collection time. Recorded as displayed, including platform-capped values. | `INTEGER` | ≥ 0 | `NULL` if not displayed | `4820` |
| `rq4_network_reach_capped` | Whether the displayed figure was a platform cap rather than an exact count. | `BOOLEAN` | `TRUE`/`FALSE` | Not nullable where reach is present | `TRUE` |
| `rq4_content_engagement` | Mean reactions plus comments received per public post across the observation window defined at collection. | `NUMERIC(10,2)` | ≥ 0 | `NULL` if activity not collected or no posts exist | `37.50` |
| `rq4_content_post_count` | Number of public posts in the observation window, denominator for the above. | `INTEGER` | ≥ 0 | `NULL` if activity not collected | `12` |
| `rq4_recognition_count` | Count of distinct third-party recognition events stated on the profile: awards, named invited speaking engagements at recognised venues, editorial or advisory board appointments. Counts recognition **conferred by others**, not outputs produced. | `INTEGER` | ≥ 0 | `NULL` if section unavailable | `3` |
| `rq4_seniority_progression_rate` | Number of upward seniority transitions in the employment history divided by total years of professional tenure. Transitions are identified from dated role changes; the measure is a rate of positional advancement over time. | `NUMERIC(5,3)` | ≥ 0 | `NULL` if dates insufficient to compute | `0.214` |
| `rq4_observation_window_days` | Length of the activity observation window, for comparability of engagement measures. | `INTEGER` | ≥ 1 | `NULL` if activity not collected | `365` |

Storage: all criterion variables live in a **separate table** keyed on `profile_id`, never in the dimension-score table, so that predictor and criterion remain physically as well as conceptually distinct. *[Convention enforcing a frozen requirement]*

### 3.2 Independence from ALCSM dimensions

Each variable is external to the six dimensions by construction:

- **`rq4_network_reach`** measures audience size. No ALCSM dimension scores audience size; D6 scores *engagement behaviour and continuing development*, not the number of people connected. Reach is a property of the network, not of the credential.
- **`rq4_content_engagement`** measures the response *received* from others. D6 scores the *originality and evaluative depth of what the individual produces*. The distinction is authored output (D6) versus audience reaction (criterion) — a boundary that must be preserved in the annotation interface so raters never consult engagement counts when scoring D6.
- **`rq4_recognition_count`** counts recognition conferred by third parties. D4 counts technical artefacts the individual produced. Awards and board appointments are not technical outputs; publications, patents, and repositories are, and are therefore **excluded** from this variable.
- **`rq4_seniority_progression_rate`** measures rate of positional change over time. D5 scores *current* positional seniority and strategic-scope language. The criterion is a trajectory derived from dated transitions; the dimension is a static level. The two must be computed from the same employment data without reusing the D5 score itself as an input.

**Circularity safeguards (binding).** *[Frozen: circularity caveat]*
1. Externally verifiable technical outputs — citations, patents, repository metrics — inform **D4 only** and are prohibited as criterion variables.
2. No criterion variable may be derived from any ALCSM dimension score.
3. Should weights ever be derived empirically against these criteria, weight-derivation and criterion-validation must use disjoint data (held-out split or cross-validation), and the split must be recorded.
4. The annotation interface must not display criterion variables to raters during dimension coding, preventing criterion knowledge from contaminating predictor scores.

---

## 4. Database Implementation Conventions

### 4.1 Primary keys
- Natural, human-readable keys for the three sampled entities: `profile_id`, `posting_id`, `respondent_id`, using the fixed prefix-plus-zero-padded-integer patterns in §1. *[Convention]*
- Surrogate `BIGSERIAL` keys for high-volume child tables: `score_record_id`, `requirement_record_id`, `prediction_id`. *[Convention]*
- Uniqueness constraint on the natural coding grain: `(profile_id, dimension_number, rater_id, rulebook_version)` must be unique, preventing silent duplicate coding of the same dimension by the same rater under the same rulebook version.

### 4.2 Foreign keys
- `alcsm_dimension_score.profile_id` → `profile.profile_id`
- `rq4_impact_indicator.profile_id` → `profile.profile_id`
- `nlp_prediction.profile_id` → `profile.profile_id`
- `job_requirement_score.posting_id` → `job_posting.posting_id`
- Referential actions: `ON DELETE RESTRICT`. Sampled records are research data; cascading deletion must never be possible. *[Convention, protective]*

### 4.3 Naming conventions
- Tables: singular `snake_case` nouns — `profile`, `job_posting`, `alcsm_dimension_score`, `job_requirement_score`, `rq4_impact_indicator`, `nlp_prediction`, `survey_response`, `annotation_revision_log`.
- Columns: `snake_case`; booleans end in `_flag` or read as predicates (`verification_used`, `double_coded`); timestamps end in `_ts`; identifiers end in `_id`; counts end in `_count`; rates end in `_rate`.
- Dimension references always use the canonical `dimension_code` values in §1.3; ad-hoc labels such as `education_score` are prohibited across schema, code, and thesis text.
- Controlled vocabularies are stored as `TEXT` with `CHECK` constraints rather than integer codes, so exported data is self-describing. *[Convention]*

### 4.4 Timestamp standards
- All timestamps `TIMESTAMPTZ`, stored in **UTC**, formatted ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`). *[Convention]*
- Every table carries `created_ts` and `updated_ts`, set by trigger, distinct from the domain timestamps (`collection_ts`, `coding_ts`, `prediction_ts`).
- Collection timestamps are mandatory on both corpora; they establish the temporal validity boundary of every finding, given that taxonomies and platform content both drift.

### 4.5 Version tracking
Every scored, predicted, or collected record carries the versions under which it was produced, so that any result can be reconstructed exactly. *[Frozen: reproducibility and versioning requirements]*

| Field | Applies to | Purpose |
|---|---|---|
| `alcsm_version` | All scored records | Framework version (`1.0`) |
| `rulebook_version` | All scored records | Coding rulebook version in force |
| `taxonomy_version` | All scored records | Version of the frozen taxonomies' term lists, post job-posting anchoring |
| `model_version`, `pipeline_run_id` | NLP predictions | Model and batch reproducibility |
| `survey_version` | Survey responses | Instrument version |
| `schema_version` | Database | Migration state |

A dedicated `annotation_revision_log` table implements the frozen revision-log template (revision id, date, dimension affected, version before/after, trigger, change description, rationale, re-pilot required, approved by). Historical rulebook versions are retained; superseded versions are never overwritten. *[Frozen]*

### 4.6 Annotation metadata
Required on every human-coded record, per §1.3: `rater_id`, `coding_ts`, `missing_status`, `ambiguity_flag` (+ candidate scores), `contradiction_flag` (+ text), `verification_used` (+ source, timestamp, outcome), `precedent_applied`, `rulebook_version`, `alcsm_version`, `taxonomy_version`, `evidence_text`.

Additional integrity requirements:
- **Independence preservation:** the interface must prevent a rater from viewing the other rater's scores before both have submitted, implementing the frozen blind cross-check.
- **Adjudication is additive:** adjudicated scores are stored as new rows with `rater_id = 'ADJUDICATOR'`; original rater rows are never overwritten. Reliability is computed on pre-adjudication rows only. *[Frozen]*
- **Verification constraint:** a `CHECK` constraint must enforce `verification_used = TRUE` only where `dimension_code = 'd4_contributions'`, encoding the frozen D4-only rule in the database rather than relying on annotator discipline.
- **Evidence traceability:** every score row must be traceable to its evidence span; score sheets may not exist detached from the coding log. *[Frozen]*

---

## 5. Conceptual Framework Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  THEORETICAL FOUNDATION                                                      │
│  Spence (1973) signalling · Tadelis (2002) reputation · Boyatzis (1982)      │
│  competency · Steinbach et al. (2019) · Raisch & Krakowski (2021)            │
│  Ng et al. (2021) · Cappelli, Tambe & Yakubovich · Stark & Pais (2021)       │
└───────────────────────────────────┬──────────────────────────────────────────┘
                                    │  derives
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  ALCSM v1.0  —  FORMATIVE COMPOSITE INDEX (FROZEN)                           │
│  D1 Education │ D2 Certifications │ D3 Experience                            │
│  D4 Contributions │ D5 Leadership │ D6 Engagement          each scored 0–5   │
│  Verifiability gradient:  D1,D2 high → D4 med-high → D3 med → D5,D6 low      │
│  Frozen taxonomies · precedent library P-01…P-15 · coding rulebook           │
└───────────────┬──────────────────────────────────────┬───────────────────────┘
                │ applied to                           │ applied to
                ▼                                      ▼
┌───────────────────────────────┐      ┌───────────────────────────────────────┐
│  PROFILE CORPUS (n ≈ 500)     │      │  JOB POSTING CORPUS (n ≈ 200)         │
│  purposive, title-based       │      │  purposive, query-defined             │
│  provenance captured          │      │  raw requirement text retained        │
└───────────────┬───────────────┘      └───────────────────┬───────────────────┘
                │                                          │
                ▼                                          ▼
┌───────────────────────────────┐      ┌───────────────────────────────────────┐
│  HUMAN ANNOTATION             │      │  REQUIREMENT SCORING                  │
│  2 independent raters         │      │  same 0–5 criteria, separate          │
│  blind → adjudication         │      │  validation (commensurability caveat) │
│  flags: missing/ambiguity/    │      │  modality: required vs preferred      │
│  contradiction · precedents   │      │                                       │
└───────────────┬───────────────┘      └───────────────────┬───────────────────┘
                │ produces gold standard                   │
                ▼                                          │
┌───────────────────────────────┐                          │
│  RELIABILITY EVIDENCE         │                          │
│  Krippendorff's α PER         │                          │
│  DIMENSION (never pooled)     │                          │
│  bootstrap CIs · % agreement  │                          │
│  ✗ internal consistency is    │                          │
│    NOT an evaluation criterion│                          │
└───────────────┬───────────────┘                          │
                │ gates                                    │
                ▼                                          │
┌───────────────────────────────┐                          │
│  NLP PIPELINE  (RQ5)          │                          │
│  extraction → dimension       │                          │
│  classifiers → predicted 0–5  │                          │
│  same information base as     │                          │
│  human coders (comparability) │                          │
└───────────────┬───────────────┘                          │
                │ evaluated against gold standard          │
                ▼                                          │
┌──────────────────────────────────────────────────────────┴───────────────────┐
│  VALIDATION LAYER                                                            │
│  content validity (expert review) · reproducibility (rulebook, precedents,   │
│  versioning) · inter-rater reliability · criterion validity (RQ4) ·          │
│  NLP replication accuracy                                                    │
│                                                                              │
│  RQ4 criterion set — held physically separate, no overlap with D1–D6:        │
│  network reach · content engagement · recognition count · progression rate   │
└───────────────┬──────────────────────────────────────────────────────────────┘
                │ supports
                ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│  CREDENTIAL GAP ANALYSIS                                                      │
│  Gap_i = mean(required_i | postings) − mean(held_i | profiles)               │
│  reported PER DIMENSION; composite only for aggregate comparison             │
│  aggregation function · weights · classification bands  →  OPEN, empirical    │
│                                                                              │
│  Interpretive layer: dimension-level patterns + contradiction flags          │
│  distinguish credential inflation from under-signalling                      │
│  (a single composite cannot)                                                 │
└──────────────────────────────────────────────────────────────────────────────┘

Scope boundary: all measurement pertains to OBSERVABLE CREDENTIAL SIGNALS
presented on LinkedIn — not to leadership competence or true capability.
```

---

## 6. Implementation Checklist

### 6.1 Conceptual framework — complete, frozen

- [x] Literature base reconciled; substitutions and gaps disclosed
- [x] Six dimensions defined, theoretically anchored, 0–5 criteria fixed
- [x] Verifiability gradient established and reporting requirement fixed
- [x] Eight taxonomies frozen in structure
- [x] Coding rulebook, precedent library (P-01–P-15), 18 worked examples
- [x] Pilot design and per-dimension reliability method fixed
- [x] Design-decision register with viva defences
- [x] Measurement model specified as formative; Hinkin re-scoped; validation pathway fixed
- [x] RQ4 terminology corrected to observable professional impact indicators
- [x] Sampling frame characterised; provenance requirements stated

### 6.2 Standardised by this document

- [x] Canonical variable names, types, allowed values, null conventions
- [x] Four-state missing-data encoding implementing the frozen distinctions
- [x] RQ4 criterion variables operationalised, with independence rationale and circularity safeguards
- [x] Primary/foreign keys, naming, timestamps, version tracking, annotation metadata
- [x] Conceptual framework diagram
- [x] No composite/band variable defined, preserving the frozen open items

### 6.3 Outstanding before data **collection** (not blocking Task 4 schema design)

- [ ] Obtain full texts: Boyatzis (1982); confirm final publication details for Cappelli, Tambe & Yakubovich; obtain Bollen & Lennox (1991), Diamantopoulos & Winklhofer (2001), Jarvis et al. (2003)
- [ ] Run job-posting vocabulary anchoring, then stamp `taxonomy_version`
- [ ] Fix language/localisation scope (English-only vs. translation protocol)
- [ ] Confirm rater identities and independence arrangement
- [ ] Fix the activity observation window used by `rq4_content_engagement`
- [ ] Complete Task 5 ethics documentation — **blocking for collection**, including the separate justification for post-level activity data
- [ ] Execute pilot; compute per-dimension α with bootstrap CIs; log any revisions

### 6.4 Deliberately open — do not close before empirical evidence

- [ ] Aggregation function (compensatory / partially compensatory / conjunctive)
- [ ] Dimension weights w₁–w₆
- [ ] Classification thresholds and bands
- [ ] Consequences of a dimension failing reliability after one revision cycle
- [ ] Job-posting-side scoring validation (own pilot; does not inherit profile-side reliability)

### 6.5 Readiness

All prerequisites for **Task 4 (data schema design)** are met. The variable dictionary, missing-data encoding, criterion specification, and database conventions above are sufficient to construct the three schemas without further conceptual input.

ALCSM v1.0 remains **conceptually frozen**. This document introduced no dimension, scoring criterion, taxonomy, annotation rule, validation-strategy, or measurement-model change; it fixed names, types, encodings, and conventions only. Remaining work is implementation, data collection, reliability testing, and validation.
