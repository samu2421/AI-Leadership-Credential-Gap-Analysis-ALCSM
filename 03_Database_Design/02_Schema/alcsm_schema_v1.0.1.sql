-- =====================================================================
-- ALCSM Schema v1.0.1 — Data Architecture (PostgreSQL DDL)
-- Thesis: The AI Leadership Credential Gap: An NLP Audit of 500 LinkedIn Profiles
--
-- Implementation layer of the FROZEN ALCSM v1.0 framework.
-- No conceptual construct is introduced by this file.
--
-- v1.0.1 (implementation freeze) applies corrections F-01..F-05.
-- Changes vs v1.0.0 are marked [v1.0.1]. No conceptual rule altered.
--
-- Marker legend used in comments:
--   [F] Frozen    — fixed in ALCSM v1.0
--   [E] Encoding  — implementation of an existing frozen decision
--   [C] Convention— database/engineering convention, no conceptual content
--   [!] Flagged   — may influence statistical analysis or validity
-- =====================================================================

BEGIN;

CREATE SCHEMA IF NOT EXISTS alcsm;
SET search_path TO alcsm, public;


-- =====================================================================
-- 1. REFERENCE / CONTROLLED VOCABULARY TABLES
--    [C] Controlled vocabularies as TEXT + FK to reference tables, so
--        exports are self-describing rather than integer-coded.
-- =====================================================================

-- [F] The six dimensions, frozen order and codes.
CREATE TABLE dimension_ref (
    dimension_number    SMALLINT    PRIMARY KEY
                        CHECK (dimension_number BETWEEN 1 AND 6),
    dimension_code      TEXT        NOT NULL UNIQUE,
    dimension_label     TEXT        NOT NULL,
    verifiability_tier  TEXT        NOT NULL
                        CHECK (verifiability_tier IN ('high','medium_high','medium','low_medium','low')),
    external_verification_permitted BOOLEAN NOT NULL DEFAULT FALSE
);

COMMENT ON TABLE dimension_ref IS
  '[F] Six ALCSM dimensions. Frozen order, codes and verifiability tiers.';
COMMENT ON COLUMN dimension_ref.external_verification_permitted IS
  '[F] TRUE for d4_contributions only; enforced downstream by CHECK on scores.';

INSERT INTO dimension_ref VALUES
 (1,'d1_education',      'Formal Education',                            'high',        FALSE),
 (2,'d2_certifications', 'Professional Certifications',                 'high',        FALSE),
 (3,'d3_experience',     'Practical AI Experience',                     'medium',      FALSE),
 (4,'d4_contributions',  'Technical Contributions',                     'medium_high', TRUE),
 (5,'d5_leadership',     'Leadership and Strategic Responsibility',     'low',         FALSE),
 (6,'d6_engagement',     'Professional Engagement and Continuous Development','low_medium', FALSE);


-- [E] Four-state missing-data encoding of the frozen missing-data rules.
CREATE TABLE missing_status_ref (
    missing_status      TEXT        PRIMARY KEY,
    description         TEXT        NOT NULL,
    counts_as_informative BOOLEAN   NOT NULL,   -- feeds completeness_index numerator
    include_in_gap      BOOLEAN     NOT NULL    -- eligible for Gap_i computation
);

INSERT INTO missing_status_ref VALUES
 ('present',        'Evidence exists in the record and was scored on its merits.',                 TRUE,  TRUE),
 ('absent_stated',  'Record explicitly asserts the credential is not held. Informative, not missing.', TRUE, TRUE),
 ('unavailable',    'No evidence found: section empty, absent, or not retrievable at collection.',  FALSE, FALSE),
 ('not_applicable', 'Dimension structurally inapplicable to this record (chiefly postings).',       FALSE, FALSE);


-- [F] Precedent library P-01 .. P-15.
CREATE TABLE precedent_ref (
    precedent_id        TEXT        PRIMARY KEY CHECK (precedent_id ~ '^P-[0-9]{2}$'),
    situation           TEXT        NOT NULL,
    binding_ruling      TEXT        NOT NULL,
    introduced_in_version TEXT      NOT NULL DEFAULT '1.0'
);


-- [C] Annotators, including the adjudicator role.
CREATE TABLE rater_ref (
    rater_id            TEXT        PRIMARY KEY,
    rater_role          TEXT        NOT NULL CHECK (rater_role IN ('primary','secondary','adjudicator')),
    blind_to_hypotheses BOOLEAN,                       -- [!] bias-control disclosure
    notes               TEXT
);

COMMENT ON COLUMN rater_ref.blind_to_hypotheses IS
  '[!] Recorded for transparency: expectancy bias is a live concern on low-verifiability dimensions.';


-- [F] Frozen taxonomies. Structure frozen; term lists versioned after
--     job-posting vocabulary anchoring.
CREATE TABLE taxonomy_version (
    taxonomy_version_id TEXT        PRIMARY KEY,       -- e.g. 'TAX-1.0'
    taxonomy_name       TEXT        NOT NULL CHECK (taxonomy_name IN
                        ('degree','certification','ai_role','leadership_level',
                         'technical_contribution','professional_engagement',
                         'ai_keyword_ontology','automation_augmentation')),
    version_label       TEXT        NOT NULL,
    constructed_ts      TIMESTAMPTZ NOT NULL,
    anchored_to_batch   TEXT,                          -- posting batch used for anchoring
    frozen              BOOLEAN     NOT NULL DEFAULT FALSE,
    UNIQUE (taxonomy_name, version_label)
);

CREATE TABLE taxonomy_term (
    term_id             BIGSERIAL   PRIMARY KEY,
    taxonomy_version_id TEXT        NOT NULL REFERENCES taxonomy_version(taxonomy_version_id)
                                    ON DELETE RESTRICT,
    term                TEXT        NOT NULL,
    tier_or_band        TEXT,                          -- e.g. 'tier_a', 'seniority_tier_4'
    source_frequency    INTEGER,                       -- [!] frequency in anchoring corpus
    UNIQUE (taxonomy_version_id, term)
);

COMMENT ON COLUMN taxonomy_term.source_frequency IS
  '[!] Observed frequency in the job-posting corpus used for anchoring; NULL if term added a priori.';


-- =====================================================================
-- 2. SAMPLING / PROVENANCE
--    [F] Provenance capture is a frozen requirement: selection effects
--        must remain analysable, not hidden.
-- =====================================================================

CREATE TABLE sampling_batch (
    sampling_batch_id   TEXT        PRIMARY KEY CHECK (sampling_batch_id ~ '^BATCH-[0-9]{3}$'),
    corpus              TEXT        NOT NULL CHECK (corpus IN ('profile','job_posting')),
    search_query        TEXT        NOT NULL,
    platform            TEXT        NOT NULL,
    collection_started_ts TIMESTAMPTZ NOT NULL,
    collection_ended_ts   TIMESTAMPTZ,
    result_set_size     INTEGER,                       -- [!] denominator for selection rate
    records_included    INTEGER,
    inclusion_protocol_version TEXT NOT NULL,
    notes               TEXT,
    CHECK (collection_ended_ts IS NULL OR collection_ended_ts >= collection_started_ts)
);

COMMENT ON TABLE sampling_batch IS
  '[F] One row per documented, reproducible search. Purposive/title-based sampling, not probability sampling.';
COMMENT ON COLUMN sampling_batch.result_set_size IS
  '[!] Enables reporting of what fraction of an algorithmically ranked result set entered the sample.';


-- =====================================================================
-- 3. CORPUS 1 — LINKEDIN PROFILES (n ~ 500)
-- =====================================================================

CREATE TABLE profile (
    profile_id          TEXT        PRIMARY KEY CHECK (profile_id ~ '^PRF-[0-9]{5}$'),
    sampling_batch_id   TEXT        NOT NULL REFERENCES sampling_batch(sampling_batch_id)
                                    ON DELETE RESTRICT,
    profile_source      TEXT        NOT NULL DEFAULT 'linkedin',
    search_query        TEXT        NOT NULL,
    search_rank_position INTEGER    CHECK (search_rank_position IS NULL OR search_rank_position >= 1),
    inclusion_reason    TEXT        NOT NULL CHECK (inclusion_reason IN
                        ('title_match','title_variant_match','manual_review_included')),
    collection_ts       TIMESTAMPTZ NOT NULL,
    profile_language    TEXT        NOT NULL DEFAULT 'und',   -- ISO 639-1 or 'und'
    profile_geography   TEXT,                                  -- ISO 3166-1 alpha-2
    observation_window_days INTEGER CHECK (observation_window_days IS NULL OR observation_window_days >= 1),
    activity_data_collected BOOLEAN NOT NULL DEFAULT FALSE,    -- [F] separate ethics justification
    created_ts          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_ts          TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE profile IS
  '[F] Pseudonymous. No name, URL, photo or direct identifier is stored in this database.';
COMMENT ON COLUMN profile.activity_data_collected IS
  '[F] Post-level activity requires its own ethics/GDPR justification; flag records where collected.';
COMMENT ON COLUMN profile.observation_window_days IS
  '[!] Denominator context for engagement-based criterion variables; must be fixed and constant across records.';


-- [!] FLAGGED DESIGN CHOICE: raw text stored as one row per section
--     (long format) rather than wide columns. Long format supports
--     section-level NLP provenance and per-section availability, and
--     records absence explicitly rather than as ambiguous NULL.
CREATE TABLE profile_raw_section (
    raw_section_id      BIGSERIAL   PRIMARY KEY,
    profile_id          TEXT        NOT NULL REFERENCES profile(profile_id) ON DELETE RESTRICT,
    section_name        TEXT        NOT NULL CHECK (section_name IN
                        ('headline','about','experience','education',
                         'certifications','contributions','activity')),
    section_text        TEXT,
    section_available   BOOLEAN     NOT NULL,          -- [E] distinguishes empty from not-retrieved
    captured_ts         TIMESTAMPTZ NOT NULL,
    UNIQUE (profile_id, section_name)
);

COMMENT ON COLUMN profile_raw_section.section_available IS
  '[E] FALSE => not retrievable at collection. Feeds the ''unavailable'' missing-status distinction.';


-- =====================================================================
-- 4. CORPUS 2 — JOB POSTINGS (n ~ 200)
-- =====================================================================

CREATE TABLE job_posting (
    posting_id          TEXT        PRIMARY KEY CHECK (posting_id ~ '^JOB-[0-9]{5}$'),
    sampling_batch_id   TEXT        NOT NULL REFERENCES sampling_batch(sampling_batch_id)
                                    ON DELETE RESTRICT,
    posting_source      TEXT        NOT NULL,
    search_query        TEXT        NOT NULL,
    search_rank_position INTEGER    CHECK (search_rank_position IS NULL OR search_rank_position >= 1),
    inclusion_reason    TEXT        NOT NULL CHECK (inclusion_reason IN
                        ('title_match','title_variant_match','manual_review_included')),
    collection_ts       TIMESTAMPTZ NOT NULL,
    posting_language    TEXT        NOT NULL DEFAULT 'und',
    posting_geography   TEXT,
    posted_date         DATE,                          -- [!] enables recency control
    seniority_label_raw TEXT,
    raw_posting_text    TEXT        NOT NULL,          -- [F] raw retention for taxonomy anchoring
    raw_requirements_text TEXT,
    created_ts          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_ts          TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON COLUMN job_posting.raw_posting_text IS
  '[F] Verbatim retention is required: taxonomy anchoring cannot be performed on parsed summaries.';


-- =====================================================================
-- 5. HUMAN ANNOTATION — PROFILE DIMENSION SCORES
--    [F] One row per profile x dimension x rater.
--    [F] Adjudication is ADDITIVE: adjudicated scores are new rows;
--        original rater rows are never overwritten.
-- =====================================================================

CREATE TABLE alcsm_dimension_score (
    score_record_id     BIGSERIAL   PRIMARY KEY,
    profile_id          TEXT        NOT NULL REFERENCES profile(profile_id) ON DELETE RESTRICT,
    dimension_number    SMALLINT    NOT NULL REFERENCES dimension_ref(dimension_number)
                                    ON DELETE RESTRICT,
    rater_id            TEXT        NOT NULL REFERENCES rater_ref(rater_id) ON DELETE RESTRICT,

    score               SMALLINT    NOT NULL CHECK (score BETWEEN 0 AND 5),   -- [F] 0-5 ordinal
    evidence_text       TEXT,
    missing_status      TEXT        NOT NULL REFERENCES missing_status_ref(missing_status)
                                    ON DELETE RESTRICT,

    ambiguity_flag      BOOLEAN     NOT NULL DEFAULT FALSE,                   -- [F] 'A' flag
    ambiguity_candidate_low  SMALLINT CHECK (ambiguity_candidate_low  BETWEEN 0 AND 5),
    ambiguity_candidate_high SMALLINT CHECK (ambiguity_candidate_high BETWEEN 0 AND 5),

    contradiction_flag  BOOLEAN     NOT NULL DEFAULT FALSE,                   -- [F] 'C' flag
    contradiction_text  TEXT,

    verification_used   BOOLEAN     NOT NULL DEFAULT FALSE,                   -- [F] D4 only
    verification_source TEXT,
    verification_ts     TIMESTAMPTZ,
    verification_outcome TEXT       CHECK (verification_outcome IN
                        ('confirmed','contradicted','not_confirmable')),

    precedent_applied   TEXT        REFERENCES precedent_ref(precedent_id) ON DELETE RESTRICT,

    alcsm_version       TEXT        NOT NULL DEFAULT '1.0',
    rulebook_version    TEXT        NOT NULL,
    taxonomy_version_id TEXT        REFERENCES taxonomy_version(taxonomy_version_id) ON DELETE RESTRICT,
    coding_ts           TIMESTAMPTZ NOT NULL,
    is_adjudication     BOOLEAN     NOT NULL DEFAULT FALSE,                   -- [E] excludes row from reliability
    notes               TEXT,
    created_ts          TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- [F] One score per rater per dimension per profile per rulebook version.
    UNIQUE (profile_id, dimension_number, rater_id, rulebook_version),

    -- [F] External verification is permitted for d4_contributions only.
    CONSTRAINT ck_verification_d4_only
        CHECK (verification_used = FALSE OR dimension_number = 4),

    -- [E] Verification metadata is required when, and only when, used.
    CONSTRAINT ck_verification_metadata
        CHECK ((verification_used = FALSE
                AND verification_source IS NULL
                AND verification_ts IS NULL
                AND verification_outcome IS NULL)
            OR (verification_used = TRUE
                AND verification_source IS NOT NULL
                AND verification_ts IS NOT NULL
                AND verification_outcome IS NOT NULL)),

    -- [E] Ambiguity candidates required when, and only when, flagged; low <= high.
    CONSTRAINT ck_ambiguity_metadata
        CHECK ((ambiguity_flag = FALSE
                AND ambiguity_candidate_low IS NULL
                AND ambiguity_candidate_high IS NULL)
            OR (ambiguity_flag = TRUE
                AND ambiguity_candidate_low IS NOT NULL
                AND ambiguity_candidate_high IS NOT NULL
                AND ambiguity_candidate_low <= ambiguity_candidate_high)),

    -- [E] Contradiction text required when flagged.
    CONSTRAINT ck_contradiction_metadata
        CHECK (contradiction_flag = FALSE OR contradiction_text IS NOT NULL),

    -- [E] Evidence required whenever the record was actually scored on content.
    CONSTRAINT ck_evidence_when_present
        CHECK (missing_status <> 'present' OR evidence_text IS NOT NULL),

    -- [E] 'unavailable' implies score 0 per the frozen convention.
    CONSTRAINT ck_unavailable_scores_zero
        CHECK (missing_status <> 'unavailable' OR score = 0),

    -- [E] 'not_applicable' is a posting-side state; never valid for profiles.
    CONSTRAINT ck_profile_not_applicable
        CHECK (missing_status <> 'not_applicable'),

    -- [v1.0.1][F-02] Adjudication flag must agree with rater role, else a
    -- primary rater's row is silently dropped from reliability input.
    CONSTRAINT ck_adjudication_role_alignment
        CHECK ((is_adjudication = TRUE  AND rater_id  = 'ADJUDICATOR')
            OR (is_adjudication = FALSE AND rater_id <> 'ADJUDICATOR')),

    -- [v1.0.1][F-04] 'absent_stated' is a positive textual claim: evidenced.
    CONSTRAINT ck_absent_stated_needs_evidence
        CHECK (missing_status <> 'absent_stated' OR evidence_text IS NOT NULL),

    -- [v1.0.1][F-04] 'unavailable' means no evidence found: none may be stored.
    CONSTRAINT ck_unavailable_has_no_evidence
        CHECK (missing_status <> 'unavailable' OR evidence_text IS NULL),

    -- [v1.0.1][F-05] Assigned score must lie within the ambiguity candidates.
    CONSTRAINT ck_ambiguity_brackets_score
        CHECK (ambiguity_flag = FALSE
            OR (score >= ambiguity_candidate_low AND score <= ambiguity_candidate_high))
);

CREATE INDEX ix_score_profile      ON alcsm_dimension_score (profile_id);
CREATE INDEX ix_score_dimension    ON alcsm_dimension_score (dimension_number);
CREATE INDEX ix_score_rater        ON alcsm_dimension_score (rater_id);
CREATE INDEX ix_score_reliability  ON alcsm_dimension_score (dimension_number, is_adjudication);

COMMENT ON COLUMN alcsm_dimension_score.is_adjudication IS
  '[F] Reliability is computed on independent pre-adjudication rows only; this flag excludes adjudicated rows.';
COMMENT ON COLUMN alcsm_dimension_score.score IS
  '[!] ORDINAL, not interval. Analyses must use ordinal-appropriate methods; means are descriptive only.';


-- [F] Profile-level derived flags. Computed, never hand-entered.
CREATE TABLE profile_derived (
    profile_id          TEXT        PRIMARY KEY REFERENCES profile(profile_id) ON DELETE RESTRICT,
    completeness_index  NUMERIC(3,2) CHECK (completeness_index BETWEEN 0 AND 1),
    title_substance_contradiction_flag BOOLEAN NOT NULL DEFAULT FALSE,   -- [F] P-03
    adjudicated         BOOLEAN     NOT NULL DEFAULT FALSE,
    double_coded        BOOLEAN     NOT NULL DEFAULT FALSE,
    derived_from_rulebook_version TEXT NOT NULL,
    computed_ts         TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE profile_derived IS
  '[F] No composite/band column exists: aggregation function, weights and thresholds remain OPEN by declaration.';


-- =====================================================================
-- 6. HUMAN ANNOTATION — JOB POSTING REQUIREMENT SCORES
--    [F] Separate table: required vs held levels are NOT interchangeable
--        (commensurability caveat) and require independent validation.
-- =====================================================================

CREATE TABLE job_requirement_score (
    requirement_record_id BIGSERIAL PRIMARY KEY,
    posting_id          TEXT        NOT NULL REFERENCES job_posting(posting_id) ON DELETE RESTRICT,
    dimension_number    SMALLINT    NOT NULL REFERENCES dimension_ref(dimension_number) ON DELETE RESTRICT,
    rater_id            TEXT        NOT NULL REFERENCES rater_ref(rater_id) ON DELETE RESTRICT,

    required_score      SMALLINT    NOT NULL CHECK (required_score BETWEEN 0 AND 5),
    requirement_modality TEXT       NOT NULL CHECK (requirement_modality IN
                        ('required','preferred','unspecified')),
    evidence_text       TEXT,
    missing_status      TEXT        NOT NULL REFERENCES missing_status_ref(missing_status) ON DELETE RESTRICT,

    ambiguity_flag      BOOLEAN     NOT NULL DEFAULT FALSE,
    contradiction_flag  BOOLEAN     NOT NULL DEFAULT FALSE,
    precedent_applied   TEXT        REFERENCES precedent_ref(precedent_id) ON DELETE RESTRICT,

    alcsm_version       TEXT        NOT NULL DEFAULT '1.0',
    rulebook_version    TEXT        NOT NULL,
    taxonomy_version_id TEXT        REFERENCES taxonomy_version(taxonomy_version_id) ON DELETE RESTRICT,
    coding_ts           TIMESTAMPTZ NOT NULL,
    is_adjudication     BOOLEAN     NOT NULL DEFAULT FALSE,
    notes               TEXT,
    created_ts          TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE (posting_id, dimension_number, rater_id, rulebook_version),

    CONSTRAINT ck_req_evidence_when_present
        CHECK (missing_status <> 'present' OR evidence_text IS NOT NULL),

    -- [E] 'not_applicable' => posting states no expectation; excluded from Gap_i.
    CONSTRAINT ck_req_not_applicable_modality
        CHECK (missing_status <> 'not_applicable' OR requirement_modality = 'unspecified'),

    -- [v1.0.1][F-02] Adjudication flag must agree with rater role.
    CONSTRAINT ck_req_adjudication_role_alignment
        CHECK ((is_adjudication = TRUE  AND rater_id  = 'ADJUDICATOR')
            OR (is_adjudication = FALSE AND rater_id <> 'ADJUDICATOR')),

    -- [v1.0.1][F-04] Missing-status / evidence coherence, posting side.
    CONSTRAINT ck_req_absent_stated_needs_evidence
        CHECK (missing_status <> 'absent_stated' OR evidence_text IS NOT NULL),
    CONSTRAINT ck_req_unavailable_has_no_evidence
        CHECK (missing_status <> 'unavailable' OR evidence_text IS NULL)
);

CREATE INDEX ix_req_posting   ON job_requirement_score (posting_id);
CREATE INDEX ix_req_dimension ON job_requirement_score (dimension_number, is_adjudication);

COMMENT ON CONSTRAINT ck_req_not_applicable_modality ON job_requirement_score IS
  '[!] A posting silent on a dimension is NOT a requirement of level 0; it is excluded from Gap_i.';


-- =====================================================================
-- 7. RQ4 CRITERION VARIABLES
--    [F] Physically separate from dimension scores; must never be
--        visible to raters during dimension coding.
-- =====================================================================

CREATE TABLE rq4_impact_indicator (
    profile_id          TEXT        PRIMARY KEY REFERENCES profile(profile_id) ON DELETE RESTRICT,

    rq4_network_reach            INTEGER  CHECK (rq4_network_reach IS NULL OR rq4_network_reach >= 0),
    rq4_network_reach_capped     BOOLEAN,
    rq4_content_engagement       NUMERIC(10,2) CHECK (rq4_content_engagement IS NULL OR rq4_content_engagement >= 0),
    rq4_content_post_count       INTEGER  CHECK (rq4_content_post_count IS NULL OR rq4_content_post_count >= 0),
    rq4_recognition_count        INTEGER  CHECK (rq4_recognition_count IS NULL OR rq4_recognition_count >= 0),
    rq4_seniority_progression_rate NUMERIC(5,3) CHECK (rq4_seniority_progression_rate IS NULL
                                                    OR rq4_seniority_progression_rate >= 0),
    rq4_observation_window_days  INTEGER  CHECK (rq4_observation_window_days IS NULL
                                                    OR rq4_observation_window_days >= 1),

    extraction_method   TEXT        NOT NULL CHECK (extraction_method IN ('manual','automated','mixed')),
    extracted_by        TEXT        REFERENCES rater_ref(rater_id) ON DELETE RESTRICT,
    extraction_ts       TIMESTAMPTZ NOT NULL,
    created_ts          TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- [E] Engagement mean requires its denominator to be meaningful.
    CONSTRAINT ck_engagement_denominator
        CHECK (rq4_content_engagement IS NULL
            OR (rq4_content_post_count IS NOT NULL AND rq4_observation_window_days IS NOT NULL))
);

COMMENT ON TABLE rq4_impact_indicator IS
  '[F] Observable professional impact indicators. NOT leadership effectiveness. Predictor/criterion independence is structural.';
COMMENT ON COLUMN rq4_impact_indicator.rq4_recognition_count IS
  '[F] Recognition CONFERRED BY OTHERS only. Publications/patents/repositories inform D4 and are excluded here (circularity).';
COMMENT ON COLUMN rq4_impact_indicator.rq4_seniority_progression_rate IS
  '[!] Shares source data with D5 (employment history). Distinct construct (trajectory vs static level); D5 score must never be an input. Weakest independence claim of the four.';


-- =====================================================================
-- 8. CORPUS 3 — EXPERT SURVEY / VALIDATION DATA
--    [F] Supports content validity (formative index) — not a source of
--        ALCSM scores.
-- =====================================================================

CREATE TABLE survey_instrument (
    survey_version      TEXT        PRIMARY KEY,
    instrument_title    TEXT        NOT NULL,
    purpose             TEXT        NOT NULL CHECK (purpose IN
                        ('content_validity','expert_weighting_elicitation','other')),
    ethics_approval_ref TEXT,
    created_ts          TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON COLUMN survey_instrument.purpose IS
  '[!] If used for weight elicitation, resulting weights must not later be validated on the same data (circularity).';

CREATE TABLE survey_respondent (
    respondent_id       TEXT        PRIMARY KEY CHECK (respondent_id ~ '^RSP-[0-9]{4}$'),
    survey_version      TEXT        NOT NULL REFERENCES survey_instrument(survey_version) ON DELETE RESTRICT,
    consent_confirmed   BOOLEAN     NOT NULL CHECK (consent_confirmed = TRUE),  -- [F] no consent => not retained
    consent_ts          TIMESTAMPTZ NOT NULL,
    response_ts         TIMESTAMPTZ,
    withdrawal_flag     BOOLEAN     NOT NULL DEFAULT FALSE,
    withdrawal_ts       TIMESTAMPTZ,
    expertise_domain    TEXT,                          -- coarse, non-identifying
    expertise_years_band TEXT       CHECK (expertise_years_band IN ('0-4','5-9','10-14','15+')),
    created_ts          TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT ck_withdrawal_ts CHECK (withdrawal_flag = FALSE OR withdrawal_ts IS NOT NULL)
);

COMMENT ON TABLE survey_respondent IS
  '[F] Consent precedes any item. Only consented records are retained. Expertise stored in bands to limit re-identification.';

CREATE TABLE survey_response_item (
    response_item_id    BIGSERIAL   PRIMARY KEY,
    respondent_id       TEXT        NOT NULL REFERENCES survey_respondent(respondent_id) ON DELETE RESTRICT,
    item_code           TEXT        NOT NULL,
    dimension_number    SMALLINT    REFERENCES dimension_ref(dimension_number) ON DELETE RESTRICT,
    response_value      TEXT,
    response_numeric    NUMERIC(6,3),
    item_ts             TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (respondent_id, item_code)
);

COMMENT ON COLUMN survey_response_item.dimension_number IS
  '[E] Populated where an item concerns a specific dimension (e.g. coverage adequacy); NULL for general items.';


-- =====================================================================
-- 9. NLP PIPELINE (RQ5)
-- =====================================================================

CREATE TABLE nlp_model_run (
    pipeline_run_id     TEXT        PRIMARY KEY CHECK (pipeline_run_id ~ '^RUN-[0-9]{4}$'),
    model_name          TEXT        NOT NULL,
    model_version       TEXT        NOT NULL,
    dimension_number    SMALLINT    REFERENCES dimension_ref(dimension_number) ON DELETE RESTRICT,
    training_set_definition TEXT,
    random_seed         INTEGER,                       -- [C] reproducibility
    code_commit_hash    TEXT,                          -- [C] reproducibility
    information_base    TEXT        NOT NULL CHECK (information_base IN ('profile_text_only','profile_text_plus_links')),
    run_ts              TIMESTAMPTZ NOT NULL,
    notes               TEXT
);

COMMENT ON COLUMN nlp_model_run.information_base IS
  '[F] Human and machine coders must operate on the same information base for RQ5 comparability.';

CREATE TABLE nlp_prediction (
    prediction_id       BIGSERIAL   PRIMARY KEY,
    profile_id          TEXT        NOT NULL REFERENCES profile(profile_id) ON DELETE RESTRICT,
    dimension_number    SMALLINT    NOT NULL REFERENCES dimension_ref(dimension_number) ON DELETE RESTRICT,
    pipeline_run_id     TEXT        NOT NULL REFERENCES nlp_model_run(pipeline_run_id) ON DELETE RESTRICT,
    predicted_score     SMALLINT    NOT NULL CHECK (predicted_score BETWEEN 0 AND 5),
    prediction_confidence NUMERIC(4,3) CHECK (prediction_confidence IS NULL
                                            OR prediction_confidence BETWEEN 0 AND 1),
    predicted_missing_status TEXT   REFERENCES missing_status_ref(missing_status) ON DELETE RESTRICT,
    prediction_ts       TIMESTAMPTZ NOT NULL,
    UNIQUE (profile_id, dimension_number, pipeline_run_id)
);

CREATE INDEX ix_pred_run ON nlp_prediction (pipeline_run_id, dimension_number);


-- =====================================================================
-- 10. RELIABILITY, ADJUDICATION AND REVISION AUDIT
-- =====================================================================

-- [F] Implements the frozen revision-log template.
CREATE TABLE annotation_revision_log (
    revision_id         BIGSERIAL   PRIMARY KEY,
    revision_ts         TIMESTAMPTZ NOT NULL DEFAULT now(),
    dimension_number    SMALLINT    REFERENCES dimension_ref(dimension_number) ON DELETE RESTRICT,
    rulebook_version_before TEXT    NOT NULL,
    rulebook_version_after  TEXT    NOT NULL,
    trigger_finding     TEXT        NOT NULL,
    change_description  TEXT        NOT NULL,
    rationale           TEXT        NOT NULL,
    re_pilot_required   BOOLEAN     NOT NULL,
    approved_by         TEXT
);

-- [F] Adjudication trail: which disagreement was resolved, how and why.
CREATE TABLE adjudication_record (
    adjudication_id     BIGSERIAL   PRIMARY KEY,
    profile_id          TEXT        REFERENCES profile(profile_id) ON DELETE RESTRICT,
    posting_id          TEXT        REFERENCES job_posting(posting_id) ON DELETE RESTRICT,
    dimension_number    SMALLINT    NOT NULL REFERENCES dimension_ref(dimension_number) ON DELETE RESTRICT,
    score_rater_a       SMALLINT    NOT NULL CHECK (score_rater_a BETWEEN 0 AND 5),
    score_rater_b       SMALLINT    NOT NULL CHECK (score_rater_b BETWEEN 0 AND 5),
    disagreement_magnitude SMALLINT GENERATED ALWAYS AS (abs(score_rater_a - score_rater_b)) STORED,
    resolution_route    TEXT        NOT NULL CHECK (resolution_route IN ('consensus','escalated')),
    final_score         SMALLINT    NOT NULL CHECK (final_score BETWEEN 0 AND 5),
    adjudicator_id      TEXT        REFERENCES rater_ref(rater_id) ON DELETE RESTRICT,
    adjudication_reason TEXT        NOT NULL,
    adjudication_ts     TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- [E] Exactly one corpus referenced per adjudication row.
    CONSTRAINT ck_adjudication_one_corpus
        CHECK ((profile_id IS NOT NULL AND posting_id IS NULL)
            OR (profile_id IS NULL AND posting_id IS NOT NULL)),

    -- [v1.0.1][F-03] Frozen tie-break: magnitude >= 2 must escalate.
    CONSTRAINT ck_tiebreak_route
        CHECK (abs(score_rater_a - score_rater_b) < 2
            OR resolution_route = 'escalated')
);

COMMENT ON COLUMN adjudication_record.resolution_route IS
  '[F] Magnitude 1 => consensus attempt permitted; magnitude >= 2 => direct escalation.';

-- [F] Reliability results stored, not merely reported, for reproducibility.
CREATE TABLE reliability_result (
    reliability_id      BIGSERIAL   PRIMARY KEY,
    analysis_stage      TEXT        NOT NULL CHECK (analysis_stage IN ('pilot','main_double_coded')),
    corpus              TEXT        NOT NULL CHECK (corpus IN ('profile','job_posting')),
    dimension_number    SMALLINT    NOT NULL REFERENCES dimension_ref(dimension_number) ON DELETE RESTRICT,
    n_units             INTEGER     NOT NULL CHECK (n_units > 0),
    krippendorff_alpha  NUMERIC(5,4),
    alpha_ci_lower      NUMERIC(5,4),
    alpha_ci_upper      NUMERIC(5,4),
    percent_agreement   NUMERIC(5,4) CHECK (percent_agreement IS NULL OR percent_agreement BETWEEN 0 AND 1),
    score_variance      NUMERIC(8,4),                  -- [!] low variance can deflate alpha
    rulebook_version    TEXT        NOT NULL,
    computed_ts         TIMESTAMPTZ NOT NULL DEFAULT now(),
    notes               TEXT
);

COMMENT ON COLUMN reliability_result.score_variance IS
  '[!] Reported alongside alpha: prevalence/low-variance effects can deflate alpha despite high raw agreement.';


-- =====================================================================
-- 11. ANALYSIS VIEWS
--    [E] Encode frozen rules as queryable objects so analysis code
--        cannot silently violate them.
-- =====================================================================

-- [F] Reliability must use INDEPENDENT, PRE-ADJUDICATION rows only.
CREATE VIEW v_reliability_input AS
SELECT s.profile_id       AS unit_id,
       'profile'::TEXT    AS corpus,
       s.dimension_number,
       s.rater_id,
       s.score,
       s.rulebook_version
FROM   alcsm_dimension_score s
JOIN   rater_ref r ON r.rater_id = s.rater_id
WHERE  s.is_adjudication = FALSE
  AND  r.rater_role IN ('primary','secondary')
UNION ALL
SELECT q.posting_id, 'job_posting', q.dimension_number, q.rater_id, q.required_score, q.rulebook_version
FROM   job_requirement_score q
JOIN   rater_ref r2 ON r2.rater_id = q.rater_id
WHERE  q.is_adjudication = FALSE
  AND  r2.rater_role IN ('primary','secondary');

COMMENT ON VIEW v_reliability_input IS
  '[F] Adjudicated and adjudicator rows are excluded: including them would inflate agreement artificially.';


-- [F] Analysis-ready score per profile x dimension: adjudicated value wins.
CREATE VIEW v_final_profile_score AS
SELECT DISTINCT ON (s.profile_id, s.dimension_number)
       s.profile_id,
       s.dimension_number,
       s.score,
       s.missing_status,
       s.ambiguity_flag,
       s.contradiction_flag,
       s.is_adjudication AS from_adjudication,
       s.rulebook_version,
       s.alcsm_version
FROM   alcsm_dimension_score s
ORDER  BY s.profile_id, s.dimension_number, s.is_adjudication DESC, s.coding_ts DESC;

COMMENT ON VIEW v_final_profile_score IS
  '[E] One analysis-ready row per profile x dimension. No composite is produced: aggregation remains OPEN.';


-- [E] Completeness index per the frozen definition.
-- [v1.0.1][F-01 CORRECTION] Frozen definition divides by SIX, not by the
-- number of dimensions actually scored. v1.0.0 reported 1.00 for a profile
-- coded on 2 of 6 dimensions. coding_complete separates a sparse profile
-- from an incompletely coded one.
CREATE VIEW v_profile_completeness AS
SELECT p.profile_id,
       round(COALESCE(SUM(CASE WHEN m.counts_as_informative THEN 1 ELSE 0 END), 0)::NUMERIC / 6, 2)
           AS completeness_index,
       COUNT(f.dimension_number)       AS dimensions_scored,
       (COUNT(f.dimension_number) = 6) AS coding_complete
FROM       profile p
LEFT JOIN  v_final_profile_score f ON f.profile_id     = p.profile_id
LEFT JOIN  missing_status_ref    m ON m.missing_status = f.missing_status
GROUP BY   p.profile_id;


-- [F] Gap_i: 'not_applicable' / 'unavailable' rows are EXCLUDED, not read as zero.
CREATE VIEW v_credential_gap_by_dimension AS
WITH held AS (
    SELECT f.dimension_number, avg(f.score::NUMERIC) AS mean_held, count(*) AS n_profiles
    FROM   v_final_profile_score f
    JOIN   missing_status_ref m ON m.missing_status = f.missing_status
    WHERE  m.include_in_gap
    GROUP  BY f.dimension_number
),
required AS (
    SELECT q.dimension_number, avg(q.required_score::NUMERIC) AS mean_required, count(*) AS n_postings
    FROM   job_requirement_score q
    JOIN   missing_status_ref m2 ON m2.missing_status = q.missing_status
    WHERE  m2.include_in_gap
      AND  q.is_adjudication = FALSE
    GROUP  BY q.dimension_number
)
SELECT d.dimension_number,
       d.dimension_code,
       r.mean_required,
       h.mean_held,
       (r.mean_required - h.mean_held) AS gap_value,
       r.n_postings,
       h.n_profiles
FROM   dimension_ref d
LEFT JOIN held     h ON h.dimension_number = d.dimension_number
LEFT JOIN required r ON r.dimension_number = d.dimension_number
ORDER  BY d.dimension_number;

COMMENT ON VIEW v_credential_gap_by_dimension IS
  '[!] Means of ORDINAL scores are descriptive only. Inferential comparison requires ordinal-appropriate tests.';


-- [F] NLP evaluation against the human gold standard, same information base.
CREATE VIEW v_nlp_evaluation AS
SELECT p.pipeline_run_id,
       p.dimension_number,
       p.profile_id,
       p.predicted_score,
       g.score AS gold_score,
       (p.predicted_score - g.score) AS signed_error,
       abs(p.predicted_score - g.score) AS absolute_error,
       (p.predicted_score = g.score) AS exact_match
FROM   nlp_prediction p
JOIN   v_final_profile_score g
       ON g.profile_id = p.profile_id
      AND g.dimension_number = p.dimension_number;


-- =====================================================================
-- 12. UPDATED-TIMESTAMP TRIGGERS  [C]
-- =====================================================================

CREATE OR REPLACE FUNCTION set_updated_ts() RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_ts = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_profile_updated
    BEFORE UPDATE ON profile
    FOR EACH ROW EXECUTE FUNCTION set_updated_ts();

CREATE TRIGGER trg_job_posting_updated
    BEFORE UPDATE ON job_posting
    FOR EACH ROW EXECUTE FUNCTION set_updated_ts();

COMMIT;

-- =====================================================================
-- END OF SCHEMA v1.0.1
-- No conceptual construct was introduced by this file.
-- Aggregation function, dimension weights and classification thresholds
-- are deliberately ABSENT: they remain OPEN pending empirical validation.
-- =====================================================================
