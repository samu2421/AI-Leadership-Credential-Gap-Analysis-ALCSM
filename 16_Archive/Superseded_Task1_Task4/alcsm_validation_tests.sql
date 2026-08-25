-- =====================================================================
-- ALCSM v1.0 — Pilot Database Validation Test Suite
--
-- PURPOSE: stress-test every database constraint and implementation
--          rule. This does NOT evaluate ALCSM scores; score values are
--          arbitrary placeholders chosen to trigger specific rules.
--
-- USAGE:   psql -d <db> -f alcsm_validation_tests.sql
--          Run against a THROWAWAY database, never the real corpus.
--          Sections marked "MUST FAIL" are expected to raise errors;
--          run with ON_ERROR_STOP OFF (the default) so execution
--          continues, or use alcsm_validation_harness.py for automatic
--          pass/fail reporting.
--
-- STATUS:  Executed against PostgreSQL 16.14. 56/56 tests behaved as
--          specified on the unpatched schema.
-- =====================================================================

SET search_path TO alcsm, public;

-- =====================================================================
-- SECTION 0 — REFERENCE SEED DATA (must succeed)
-- =====================================================================
INSERT INTO rater_ref VALUES
 ('RATER-A','primary',TRUE,NULL),
 ('RATER-B','secondary',TRUE,NULL),
 ('ADJUDICATOR','adjudicator',FALSE,'supervisor adjudication');

INSERT INTO precedent_ref (precedent_id, situation, binding_ruling)
SELECT 'P-'||lpad(g::text,2,'0'), 'situation '||g, 'ruling '||g FROM generate_series(1,15) g;

INSERT INTO taxonomy_version VALUES ('TAX-1.0','degree','1.0', now(), 'BATCH-005', TRUE);

INSERT INTO sampling_batch VALUES
 ('BATCH-001','profile','"Chief AI Officer"','linkedin', now(), now(), 300, 10, 'IP-1.0', NULL),
 ('BATCH-005','job_posting','"Head of AI"','linkedin_jobs', now(), now(), 120, 5, 'IP-1.0', NULL);

-- Ten test profiles (provenance fields exercised on every row).
INSERT INTO profile (profile_id, sampling_batch_id, profile_source, search_query,
  search_rank_position, inclusion_reason, collection_ts, profile_language,
  profile_geography, observation_window_days, activity_data_collected) VALUES
 ('PRF-00001','BATCH-001','linkedin','"Chief AI Officer"',1,'title_match',now(),'en','DE',365,FALSE),
 ('PRF-00002','BATCH-001','linkedin','"Chief AI Officer"',2,'title_match',now(),'en','US',365,FALSE),
 ('PRF-00003','BATCH-001','linkedin','"Chief AI Officer"',3,'title_match',now(),'en','GB',365,FALSE),
 ('PRF-00004','BATCH-001','linkedin','"Chief AI Officer"',4,'title_match',now(),'en','DE',365,FALSE),
 ('PRF-00005','BATCH-001','linkedin','"Chief AI Officer"',5,'title_match',now(),'en','NL',365,FALSE),
 ('PRF-00006','BATCH-001','linkedin','"Chief AI Officer"',6,'title_match',now(),'en','US',365,TRUE),
 ('PRF-00007','BATCH-001','linkedin','"Chief AI Officer"',7,'title_match',now(),'en','DE',365,FALSE),
 ('PRF-00008','BATCH-001','linkedin','"Chief AI Officer"',8,'title_match',now(),'en','FR',365,FALSE),
 ('PRF-00009','BATCH-001','linkedin','"Chief AI Officer"',9,'title_match',now(),'en','DE',365,FALSE),
 ('PRF-00010','BATCH-001','linkedin','"Chief AI Officer"',10,'manual_review_included',now(),'de','AT',365,FALSE);


-- =====================================================================
-- PROFILE 01 — BASELINE / HAPPY PATH
-- Tests: FK integrity, UNIQUE grain, evidence requirement, full 6-dim set
-- Expect: SUCCESS
-- =====================================================================
INSERT INTO alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  rulebook_version, taxonomy_version_id, coding_ts)
SELECT 'PRF-00001', d, 'RATER-A', 3, 'evidence span for dim '||d, 'present',
       '1.0','TAX-1.0', now()
FROM generate_series(1,6) d;


-- =====================================================================
-- PROFILE 02 — UNAVAILABLE (data absent at collection)
-- Tests: ck_unavailable_scores_zero; section_available FALSE encoding
-- Expect: SUCCESS
-- =====================================================================
INSERT INTO alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, missing_status, rulebook_version, coding_ts)
VALUES ('PRF-00002', 2, 'RATER-A', 0, 'unavailable', '1.0', now());

INSERT INTO profile_raw_section (profile_id, section_name, section_text, section_available, captured_ts)
VALUES ('PRF-00002','certifications', NULL, FALSE, now());


-- =====================================================================
-- PROFILE 03 — STATED ABSENCE (informative, NOT missing)
-- Tests: absent_stated vs unavailable distinction; precedent P-13 FK
-- Expect: SUCCESS. completeness_index must treat this as informative.
-- =====================================================================
INSERT INTO alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  rulebook_version, coding_ts, precedent_applied)
VALUES ('PRF-00003', 1, 'RATER-A', 1, 'self-taught, no formal AI education',
        'absent_stated','1.0', now(), 'P-13');


-- =====================================================================
-- PROFILE 04 — AMBIGUITY (boundary case)
-- Tests: ck_ambiguity_metadata; precedent P-02 ("Head of X")
-- Expect: SUCCESS
-- =====================================================================
INSERT INTO alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  ambiguity_flag, ambiguity_candidate_low, ambiguity_candidate_high,
  rulebook_version, coding_ts, precedent_applied)
VALUES ('PRF-00004', 5, 'RATER-A', 3, 'Head of Data & AI', 'present',
        TRUE, 3, 4, '1.0', now(), 'P-02');


-- =====================================================================
-- PROFILE 05 — CONTRADICTION (canonical credential inflation, P-03)
-- Tests: ck_contradiction_metadata; contradiction preserved as data
-- Expect: SUCCESS
-- =====================================================================
INSERT INTO alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  contradiction_flag, contradiction_text, rulebook_version, coding_ts, precedent_applied)
VALUES ('PRF-00005', 5, 'RATER-A', 2, 'Chief AI Officer', 'present',
        TRUE, 'title=CAIO vs about section = generic PM language', '1.0', now(), 'P-03');


-- =====================================================================
-- PROFILE 06 — D4 EXTERNAL VERIFICATION (permitted dimension)
-- Tests: ck_verification_d4_only (positive); ck_verification_metadata
-- Expect: SUCCESS
-- =====================================================================
INSERT INTO alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  verification_used, verification_source, verification_ts, verification_outcome,
  rulebook_version, coding_ts, precedent_applied)
VALUES ('PRF-00006', 4, 'RATER-A', 4, 'linked repository', 'present',
        TRUE, 'github.com/example', now(), 'confirmed', '1.0', now(), 'P-14');


-- =====================================================================
-- PROFILE 07 — CONSTRAINT-VIOLATION VEHICLE
-- Used by the MUST-FAIL block below. No valid rows inserted here.
-- =====================================================================


-- =====================================================================
-- PROFILE 08 — DOUBLE CODING + ADJUDICATION
-- Tests: independent coding, additive adjudication, generated magnitude,
--        exclusion of adjudicated rows from v_reliability_input
-- Expect: SUCCESS (all four inserts)
-- =====================================================================
INSERT INTO alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status, rulebook_version, coding_ts)
VALUES ('PRF-00008', 5, 'RATER-A', 2, 'director level', 'present','1.0', now());

INSERT INTO alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status, rulebook_version, coding_ts)
VALUES ('PRF-00008', 5, 'RATER-B', 4, 'director level', 'present','1.0', now());

INSERT INTO alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  rulebook_version, coding_ts, is_adjudication)
VALUES ('PRF-00008', 5, 'ADJUDICATOR', 3, 'adjudicated', 'present','1.0', now(), TRUE);

INSERT INTO adjudication_record
 (profile_id, dimension_number, score_rater_a, score_rater_b, resolution_route,
  final_score, adjudicator_id, adjudication_reason)
VALUES ('PRF-00008', 5, 2, 4, 'escalated', 3, 'ADJUDICATOR',
        'magnitude 2 -> direct escalation per frozen tie-break rule');


-- =====================================================================
-- PROFILE 09 — NEGATIVE-TEST VEHICLE (see MUST-FAIL block)
-- =====================================================================


-- =====================================================================
-- PROFILE 10 — SPARSE PROFILE (low completeness, fully coded)
-- Tests: completeness_index computation; distinguishes sparse profile
--        from incompletely-coded profile
-- Expect: SUCCESS; completeness_index = 0.33 (2 informative of 6)
-- =====================================================================
INSERT INTO alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status, rulebook_version, coding_ts)
VALUES
 ('PRF-00010',1,'RATER-A',3,'MSc CS','present','1.0',now()),
 ('PRF-00010',5,'RATER-A',1,'AI Engineer','present','1.0',now()),
 ('PRF-00010',2,'RATER-A',0,NULL,'unavailable','1.0',now()),
 ('PRF-00010',3,'RATER-A',0,NULL,'unavailable','1.0',now()),
 ('PRF-00010',4,'RATER-A',0,NULL,'unavailable','1.0',now()),
 ('PRF-00010',6,'RATER-A',0,NULL,'unavailable','1.0',now());


-- =====================================================================
-- POSTING-SIDE VALID CASES
-- =====================================================================
INSERT INTO job_posting (posting_id, sampling_batch_id, posting_source, search_query,
  inclusion_reason, collection_ts, posting_language, raw_posting_text, raw_requirements_text)
VALUES ('JOB-00002','BATCH-005','linkedin_jobs','"Head of AI"','title_match', now(), 'en',
        'full posting text','MSc in AI required');

-- not_applicable => posting states no expectation; excluded from Gap_i
INSERT INTO job_requirement_score
 (posting_id, dimension_number, rater_id, required_score, requirement_modality,
  missing_status, rulebook_version, coding_ts)
VALUES ('JOB-00002', 6, 'RATER-A', 0, 'unspecified', 'not_applicable','1.0', now());

INSERT INTO job_requirement_score
 (posting_id, dimension_number, rater_id, required_score, requirement_modality,
  evidence_text, missing_status, rulebook_version, coding_ts)
VALUES ('JOB-00002', 1, 'RATER-A', 4, 'required', 'MSc in AI required','present','1.0', now());


-- =====================================================================
-- NLP PIPELINE
-- =====================================================================
INSERT INTO nlp_model_run (pipeline_run_id, model_name, model_version, dimension_number,
  random_seed, information_base, run_ts)
VALUES ('RUN-0001','clf_d1','1.0', 1, 42, 'profile_text_only', now());

INSERT INTO nlp_prediction (profile_id, dimension_number, pipeline_run_id,
  predicted_score, prediction_confidence, prediction_ts)
VALUES ('PRF-00001', 1, 'RUN-0001', 4, 0.812, now());


-- #####################################################################
-- #  MUST-FAIL BLOCK — every statement below MUST raise an error.     #
-- #  If any succeeds, the corresponding rule is NOT enforced.         #
-- #####################################################################

-- N-01 score out of range
INSERT INTO alcsm_dimension_score (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,rulebook_version,coding_ts)
VALUES ('PRF-00007',1,'RATER-A',6,'x','present','1.0',now());

-- N-02 unavailable must score 0
INSERT INTO alcsm_dimension_score (profile_id,dimension_number,rater_id,score,missing_status,rulebook_version,coding_ts)
VALUES ('PRF-00007',2,'RATER-A',3,'unavailable','1.0',now());

-- N-03 present requires evidence
INSERT INTO alcsm_dimension_score (profile_id,dimension_number,rater_id,score,missing_status,rulebook_version,coding_ts)
VALUES ('PRF-00007',3,'RATER-A',3,'present','1.0',now());

-- N-04 verification outside D4 (FROZEN RULE)
INSERT INTO alcsm_dimension_score (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,
  verification_used,verification_source,verification_ts,verification_outcome,rulebook_version,coding_ts)
VALUES ('PRF-00007',5,'RATER-A',3,'x','present',TRUE,'src',now(),'confirmed','1.0',now());

-- N-05 verification without metadata
INSERT INTO alcsm_dimension_score (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,
  verification_used,rulebook_version,coding_ts)
VALUES ('PRF-00007',4,'RATER-A',3,'x','present',TRUE,'1.0',now());

-- N-06 ambiguity flag without candidates
INSERT INTO alcsm_dimension_score (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,
  ambiguity_flag,rulebook_version,coding_ts)
VALUES ('PRF-00007',6,'RATER-A',3,'x','present',TRUE,'1.0',now());

-- N-07 ambiguity low > high
INSERT INTO alcsm_dimension_score (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,
  ambiguity_flag,ambiguity_candidate_low,ambiguity_candidate_high,rulebook_version,coding_ts)
VALUES ('PRF-00009',1,'RATER-A',3,'x','present',TRUE,4,2,'1.0',now());

-- N-08 contradiction flag without text
INSERT INTO alcsm_dimension_score (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,
  contradiction_flag,rulebook_version,coding_ts)
VALUES ('PRF-00009',2,'RATER-A',3,'x','present',TRUE,'1.0',now());

-- N-09 duplicate coding grain
INSERT INTO alcsm_dimension_score (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,rulebook_version,coding_ts)
VALUES ('PRF-00001',1,'RATER-A',4,'duplicate attempt','present','1.0',now());

-- N-10 FK: nonexistent profile
INSERT INTO alcsm_dimension_score (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,rulebook_version,coding_ts)
VALUES ('PRF-99999',1,'RATER-A',3,'x','present','1.0',now());

-- N-11 not_applicable is posting-only
INSERT INTO alcsm_dimension_score (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,rulebook_version,coding_ts)
VALUES ('PRF-00009',3,'RATER-A',0,'x','not_applicable','1.0',now());

-- N-12 malformed profile_id
INSERT INTO profile (profile_id,sampling_batch_id,search_query,inclusion_reason,collection_ts)
VALUES ('PROFILE-1','BATCH-001','q','title_match',now());

-- N-13 dimension_number out of range
INSERT INTO alcsm_dimension_score (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,rulebook_version,coding_ts)
VALUES ('PRF-00009',7,'RATER-A',3,'x','present','1.0',now());

-- N-14 ON DELETE RESTRICT protects research data
DELETE FROM profile WHERE profile_id = 'PRF-00001';

-- N-15 adjudication may reference exactly one corpus
INSERT INTO job_posting (posting_id,sampling_batch_id,posting_source,search_query,inclusion_reason,collection_ts,raw_posting_text)
VALUES ('JOB-00001','BATCH-005','linkedin_jobs','q','title_match',now(),'text');
INSERT INTO adjudication_record (profile_id,posting_id,dimension_number,score_rater_a,score_rater_b,
  resolution_route,final_score,adjudication_reason)
VALUES ('PRF-00002','JOB-00001',1,2,3,'consensus',3,'invalid dual reference');

-- N-16 engagement mean without denominator
INSERT INTO rq4_impact_indicator (profile_id,rq4_content_engagement,extraction_method,extraction_ts)
VALUES ('PRF-00003',45.5,'manual',now());

-- N-17 survey record without consent
INSERT INTO survey_instrument VALUES ('SV-1.0','Expert review','content_validity',NULL,now());
INSERT INTO survey_respondent (respondent_id,survey_version,consent_confirmed,consent_ts)
VALUES ('RSP-0001','SV-1.0',FALSE,now());

-- N-18 not_applicable with a stated modality
INSERT INTO job_requirement_score (posting_id,dimension_number,rater_id,required_score,
  requirement_modality,missing_status,rulebook_version,coding_ts)
VALUES ('JOB-00002',5,'RATER-A',0,'required','not_applicable','1.0',now());


-- #####################################################################
-- #  VIEW-BEHAVIOUR ASSERTIONS                                        #
-- #####################################################################

-- V-01 reliability input must EXCLUDE the adjudicated row -> expect 2
SELECT 'V-01' AS test, count(*) AS got, 2 AS expected
FROM v_reliability_input WHERE unit_id='PRF-00008' AND dimension_number=5;

-- V-02 final score must PREFER the adjudicated value -> expect 3, TRUE
SELECT 'V-02' AS test, score, from_adjudication
FROM v_final_profile_score WHERE profile_id='PRF-00008' AND dimension_number=5;

-- V-03 sparse profile completeness -> expect 0.33
SELECT 'V-03' AS test, completeness_index FROM v_profile_completeness WHERE profile_id='PRF-00010';

-- V-04 absent_stated counts as informative
--      NOTE: on the UNPATCHED schema this returns 1.00 because the view
--      divides by dimensions scored, not by 6. See finding F-01.
SELECT 'V-04' AS test, completeness_index FROM v_profile_completeness WHERE profile_id='PRF-00003';

-- V-05 not_applicable excluded from Gap_i -> expect NULLs on D6
SELECT 'V-05' AS test, mean_required, n_postings
FROM v_credential_gap_by_dimension WHERE dimension_number=6;

-- V-06 NLP evaluation error computation -> expect abs_err=1, exact_match=false
SELECT 'V-06' AS test, gold_score, predicted_score, absolute_error, exact_match
FROM v_nlp_evaluation WHERE profile_id='PRF-00001';

-- V-07 generated disagreement magnitude -> expect 2, 'escalated'
SELECT 'V-07' AS test, disagreement_magnitude, resolution_route
FROM adjudication_record WHERE profile_id='PRF-00008';

-- V-08 updated_ts trigger
UPDATE profile SET profile_geography='CH' WHERE profile_id='PRF-00009'
RETURNING 'V-08' AS test, (updated_ts >= created_ts) AS trigger_fired;

-- =====================================================================
-- END OF TEST SUITE
-- =====================================================================
