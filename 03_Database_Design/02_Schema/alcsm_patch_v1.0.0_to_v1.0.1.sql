-- =====================================================================
-- ALCSM Schema — Implementation Patch  v1.0.0 → v1.0.1
--
-- SCOPE: implementation corrections ONLY. Every change below restores
--        consistency between the database and the FROZEN ALCSM v1.0
--        conceptual framework. NO conceptual rule is introduced,
--        removed, or altered.
--
-- APPLIES: F-01 (unconditional), F-02, F-03, F-04, F-05.
-- DEFERS:  F-06, F-07, F-08 (see alcsm_optional_recommendations.sql).
--
-- Idempotent: safe to re-run. Uses IF NOT EXISTS / OR REPLACE.
-- =====================================================================

BEGIN;
SET search_path TO alcsm, public;


-- ---------------------------------------------------------------------
-- F-01 [CORRECTION — UNCONDITIONAL]
-- v_profile_completeness contradicted the frozen definition.
--
-- Frozen definition (Implementation Readiness Spec §1.4):
--     completeness_index = (dimensions with present|absent_stated) / 6
--
-- v1.0.0 divided by dimensions ACTUALLY SCORED, so a profile coded on
-- 2 of 6 dimensions reported 1.00 instead of 0.33 — making a partially
-- coded profile indistinguishable from a fully documented one, and
-- rendering the frozen "report low-completeness records separately"
-- rule unenforceable.
--
-- The added coding_complete column separates "sparse profile"
-- (6 coded, few informative) from "incomplete coding" (<6 coded).
-- These are analytically different and were previously conflated.
-- No conceptual change: the frozen definition is unchanged; only the
-- implementation is brought into agreement with it.
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW v_profile_completeness AS
SELECT p.profile_id,
       round(COALESCE(SUM(CASE WHEN m.counts_as_informative THEN 1 ELSE 0 END), 0)::NUMERIC / 6, 2)
           AS completeness_index,
       COUNT(f.dimension_number)        AS dimensions_scored,
       (COUNT(f.dimension_number) = 6)  AS coding_complete
FROM       profile p
LEFT JOIN  v_final_profile_score f ON f.profile_id     = p.profile_id
LEFT JOIN  missing_status_ref    m ON m.missing_status = f.missing_status
GROUP BY   p.profile_id;

COMMENT ON VIEW v_profile_completeness IS
  '[F] completeness_index = (present|absent_stated) / 6 per the frozen definition. '
  'coding_complete distinguishes a sparse profile from an incompletely coded one.';


-- ---------------------------------------------------------------------
-- F-02 [Encoding] Adjudication flag must agree with rater role.
--
-- v1.0.0 permitted is_adjudication and rater_id to disagree. A primary
-- rater's row flagged TRUE was silently dropped from v_reliability_input
-- with no error raised — corrupting Krippendorff's alpha invisibly.
--
-- The frozen rule ("reliability is computed on independent
-- pre-adjudication rows only") is unchanged; it is now enforced at the
-- row level rather than relying on the view's role filter alone.
-- ---------------------------------------------------------------------
ALTER TABLE alcsm_dimension_score
  ADD CONSTRAINT ck_adjudication_role_alignment CHECK (
      (is_adjudication = TRUE  AND rater_id  = 'ADJUDICATOR')
   OR (is_adjudication = FALSE AND rater_id <> 'ADJUDICATOR'));

ALTER TABLE job_requirement_score
  ADD CONSTRAINT ck_req_adjudication_role_alignment CHECK (
      (is_adjudication = TRUE  AND rater_id  = 'ADJUDICATOR')
   OR (is_adjudication = FALSE AND rater_id <> 'ADJUDICATOR'));


-- ---------------------------------------------------------------------
-- F-03 [Encoding] Frozen tie-breaking rule.
--
-- Frozen rule (Coding Rulebook §1.5): a 1-point disagreement may go to
-- consensus; a disagreement of 2 or more must escalate, because a 2+
-- point gap signals rubric ambiguity rather than a judgement call.
--
-- v1.0.0 accepted resolution_route='consensus' at magnitude 5.
-- ---------------------------------------------------------------------
ALTER TABLE adjudication_record
  ADD CONSTRAINT ck_tiebreak_route CHECK (
      abs(score_rater_a - score_rater_b) < 2
   OR resolution_route = 'escalated');


-- ---------------------------------------------------------------------
-- F-04 [Encoding] Missing-status / evidence coherence.
--
-- Frozen rule (Implementation Readiness Spec §2): 'absent_stated' means
-- the record POSITIVELY asserts the credential is not held — a textual
-- claim, therefore evidenced. 'unavailable' means no evidence was found
-- — therefore there can be no evidence span.
--
-- v1.0.0 accepted absent_stated without evidence, and unavailable WITH
-- evidence (self-contradictory). Both corrupt the informative/missing
-- distinction that completeness_index and all missingness analysis rest on.
-- ---------------------------------------------------------------------
ALTER TABLE alcsm_dimension_score
  ADD CONSTRAINT ck_absent_stated_needs_evidence
    CHECK (missing_status <> 'absent_stated' OR evidence_text IS NOT NULL);

ALTER TABLE alcsm_dimension_score
  ADD CONSTRAINT ck_unavailable_has_no_evidence
    CHECK (missing_status <> 'unavailable' OR evidence_text IS NULL);

ALTER TABLE job_requirement_score
  ADD CONSTRAINT ck_req_absent_stated_needs_evidence
    CHECK (missing_status <> 'absent_stated' OR evidence_text IS NOT NULL);

ALTER TABLE job_requirement_score
  ADD CONSTRAINT ck_req_unavailable_has_no_evidence
    CHECK (missing_status <> 'unavailable' OR evidence_text IS NULL);


-- ---------------------------------------------------------------------
-- F-05 [Encoding] Ambiguity candidates must bracket the assigned score.
--
-- Frozen rule (Coding Rulebook §1.3): where evidence plausibly supports
-- two adjacent scores, the annotator records both candidates and assigns
-- one of them (default-low selects the lower). The assigned score is
-- therefore necessarily within the candidate range.
--
-- v1.0.0 accepted score=5 with candidates (1,2).
-- ---------------------------------------------------------------------
ALTER TABLE alcsm_dimension_score
  ADD CONSTRAINT ck_ambiguity_brackets_score CHECK (
      ambiguity_flag = FALSE
   OR (score >= ambiguity_candidate_low AND score <= ambiguity_candidate_high));


-- ---------------------------------------------------------------------
-- Version stamp
-- ---------------------------------------------------------------------
COMMENT ON SCHEMA alcsm IS
  'ALCSM research database, schema v1.0.1. Implements FROZEN ALCSM v1.0 '
  'conceptual framework. v1.0.1 applies implementation corrections F-01..F-05; '
  'no conceptual rule was changed.';

COMMIT;

-- =====================================================================
-- END OF PATCH
-- Conceptual framework unchanged: six dimensions, 0-5 criteria,
-- taxonomies, annotation rules, measurement model, validation strategy
-- and research questions are all untouched by this patch.
-- =====================================================================
