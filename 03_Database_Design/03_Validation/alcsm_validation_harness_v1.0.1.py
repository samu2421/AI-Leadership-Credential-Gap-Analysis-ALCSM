import psycopg2, sys

conn = psycopg2.connect(host="/tmp/pgrun", port=5433, dbname="alcsm_101", user="postgres")
conn.autocommit = False
results = []

def run(test_id, desc, sql, expect):
    """expect: 'success' or 'fail'"""
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
        actual = 'success'
        detail = ''
    except Exception as e:
        conn.rollback()
        actual = 'fail'
        detail = type(e).__name__ + ': ' + str(e).strip().split('\n')[0][:110]
    ok = (actual == expect)
    results.append((test_id, desc, expect, actual, 'PASS' if ok else 'MISMATCH', detail))
    cur.close()

def query(test_id, desc, sql, check_fn):
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        ok, detail = check_fn(rows)
        results.append((test_id, desc, 'query', 'ok', 'PASS' if ok else 'MISMATCH', detail))
    except Exception as e:
        conn.rollback()
        results.append((test_id, desc, 'query', 'error', 'MISMATCH', str(e)[:110]))
    cur.close()

# ---------- SETUP: reference data ----------
run('S-01', 'Seed raters', """
INSERT INTO alcsm.rater_ref VALUES
 ('RATER-A','primary',TRUE,NULL),
 ('RATER-B','secondary',TRUE,NULL),
 ('ADJUDICATOR','adjudicator',FALSE,'supervisor');""", 'success')

run('S-02', 'Seed precedents P-01..P-15', """
INSERT INTO alcsm.precedent_ref (precedent_id, situation, binding_ruling)
SELECT 'P-' || lpad(g::text,2,'0'), 'situation '||g, 'ruling '||g
FROM generate_series(1,15) g;""", 'success')

run('S-03', 'Seed taxonomy version', """
INSERT INTO alcsm.taxonomy_version VALUES
 ('TAX-1.0','degree','1.0', now(), 'BATCH-005', TRUE);""", 'success')

run('S-04', 'Seed sampling batches', """
INSERT INTO alcsm.sampling_batch VALUES
 ('BATCH-001','profile','"Chief AI Officer"','linkedin', now(), now(), 300, 10, 'IP-1.0', NULL),
 ('BATCH-005','job_posting','"Head of AI"','linkedin_jobs', now(), now(), 120, 5, 'IP-1.0', NULL);""", 'success')

# ---------- 10 TEST PROFILES ----------
for pid, lang, geo, act in [
    ('PRF-00001','en','DE',False), ('PRF-00002','en','US',False),
    ('PRF-00003','en','GB',False), ('PRF-00004','en','DE',False),
    ('PRF-00005','en','NL',False), ('PRF-00006','en','US',True),
    ('PRF-00007','en','DE',False), ('PRF-00008','en','FR',False),
    ('PRF-00009','en','DE',False), ('PRF-00010','de','AT',False)]:
    run(f'P-{pid[-2:]}', f'Insert profile {pid}', f"""
    INSERT INTO alcsm.profile (profile_id, sampling_batch_id, profile_source, search_query,
      search_rank_position, inclusion_reason, collection_ts, profile_language,
      profile_geography, observation_window_days, activity_data_collected)
    VALUES ('{pid}','BATCH-001','linkedin','"Chief AI Officer"', 1,'title_match', now(),
      '{lang}','{geo}', 365, {act});""", 'success')

# P01 baseline: all six dimensions, present, evidence
run('T-01', 'P01 baseline: 6 dims present with evidence (happy path)', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  rulebook_version, taxonomy_version_id, coding_ts)
SELECT 'PRF-00001', d, 'RATER-A', 3, 'evidence span for dim '||d, 'present',
       '1.0','TAX-1.0', now()
FROM generate_series(1,6) d;""", 'success')

# P02 unavailable -> score must be 0
run('T-02', 'P02 unavailable with score 0 (correct encoding)', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, missing_status, rulebook_version, coding_ts)
VALUES ('PRF-00002', 2, 'RATER-A', 0, 'unavailable', '1.0', now());""", 'success')

run('T-03', 'P02 raw section marked not available', """
INSERT INTO alcsm.profile_raw_section
 (profile_id, section_name, section_text, section_available, captured_ts)
VALUES ('PRF-00002','certifications', NULL, FALSE, now());""", 'success')

# P03 stated absence
run('T-04', 'P03 absent_stated with evidence (informative, not missing)', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  rulebook_version, coding_ts, precedent_applied)
VALUES ('PRF-00003', 1, 'RATER-A', 1, 'self-taught, no formal AI education',
        'absent_stated','1.0', now(), 'P-13');""", 'success')

# P04 ambiguity
run('T-05', 'P04 ambiguity flag with both candidates, low<=high', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  ambiguity_flag, ambiguity_candidate_low, ambiguity_candidate_high,
  rulebook_version, coding_ts, precedent_applied)
VALUES ('PRF-00004', 5, 'RATER-A', 3, 'Head of Data & AI', 'present',
        TRUE, 3, 4, '1.0', now(), 'P-02');""", 'success')

# P05 contradiction
run('T-06', 'P05 contradiction flag with text (P-03 canonical inflation)', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  contradiction_flag, contradiction_text, rulebook_version, coding_ts, precedent_applied)
VALUES ('PRF-00005', 5, 'RATER-A', 2, 'Chief AI Officer', 'present',
        TRUE, 'title=CAIO vs about section = generic PM language', '1.0', now(), 'P-03');""", 'success')

# P06 D4 verification permitted
run('T-07', 'P06 verification on D4 with full metadata (permitted)', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  verification_used, verification_source, verification_ts, verification_outcome,
  rulebook_version, coding_ts, precedent_applied)
VALUES ('PRF-00006', 4, 'RATER-A', 4, 'linked repository', 'present',
        TRUE, 'github.com/example', now(), 'confirmed', '1.0', now(), 'P-14');""", 'success')

# P08 double coding + adjudication
run('T-08', 'P08 rater A scores D5', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status, rulebook_version, coding_ts)
VALUES ('PRF-00008', 5, 'RATER-A', 2, 'director level', 'present','1.0', now());""", 'success')

run('T-09', 'P08 rater B scores D5 differently (independent)', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status, rulebook_version, coding_ts)
VALUES ('PRF-00008', 5, 'RATER-B', 4, 'director level', 'present','1.0', now());""", 'success')

run('T-10', 'P08 adjudication stored as ADDITIVE row', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  rulebook_version, coding_ts, is_adjudication)
VALUES ('PRF-00008', 5, 'ADJUDICATOR', 3, 'adjudicated', 'present','1.0', now(), TRUE);""", 'success')

run('T-11', 'P08 adjudication_record with generated magnitude', """
INSERT INTO alcsm.adjudication_record
 (profile_id, dimension_number, score_rater_a, score_rater_b, resolution_route,
  final_score, adjudicator_id, adjudication_reason)
VALUES ('PRF-00008', 5, 2, 4, 'escalated', 3, 'ADJUDICATOR', 'gap>=2 escalated per frozen rule');""", 'success')

# P10 sparse
run('T-12', 'P10 sparse profile: 4 unavailable + 2 present', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status, rulebook_version, coding_ts)
VALUES
 ('PRF-00010',1,'RATER-A',3,'MSc CS','present','1.0',now()),
 ('PRF-00010',5,'RATER-A',1,'AI Engineer','present','1.0',now()),
 ('PRF-00010',2,'RATER-A',0,NULL,'unavailable','1.0',now()),
 ('PRF-00010',3,'RATER-A',0,NULL,'unavailable','1.0',now()),
 ('PRF-00010',4,'RATER-A',0,NULL,'unavailable','1.0',now()),
 ('PRF-00010',6,'RATER-A',0,NULL,'unavailable','1.0',now());""", 'success')

# ---------- NEGATIVE TESTS: must FAIL ----------
run('N-01', 'Score out of range (6) must fail', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status, rulebook_version, coding_ts)
VALUES ('PRF-00007', 1, 'RATER-A', 6, 'x', 'present','1.0', now());""", 'fail')

run('N-02', 'unavailable with non-zero score must fail', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, missing_status, rulebook_version, coding_ts)
VALUES ('PRF-00007', 2, 'RATER-A', 3, 'unavailable','1.0', now());""", 'fail')

run('N-03', 'present without evidence_text must fail', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, missing_status, rulebook_version, coding_ts)
VALUES ('PRF-00007', 3, 'RATER-A', 3, 'present','1.0', now());""", 'fail')

run('N-04', 'Verification on D5 must fail (D4-only rule)', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  verification_used, verification_source, verification_ts, verification_outcome,
  rulebook_version, coding_ts)
VALUES ('PRF-00007', 5, 'RATER-A', 3, 'x', 'present',
        TRUE, 'src', now(), 'confirmed','1.0', now());""", 'fail')

run('N-05', 'Verification used without metadata must fail', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  verification_used, rulebook_version, coding_ts)
VALUES ('PRF-00007', 4, 'RATER-A', 3, 'x', 'present', TRUE, '1.0', now());""", 'fail')

run('N-06', 'Ambiguity flag without candidates must fail', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  ambiguity_flag, rulebook_version, coding_ts)
VALUES ('PRF-00007', 6, 'RATER-A', 3, 'x', 'present', TRUE, '1.0', now());""", 'fail')

run('N-07', 'Ambiguity candidates low > high must fail', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  ambiguity_flag, ambiguity_candidate_low, ambiguity_candidate_high, rulebook_version, coding_ts)
VALUES ('PRF-00009', 1, 'RATER-A', 3, 'x', 'present', TRUE, 4, 2, '1.0', now());""", 'fail')

run('N-08', 'Contradiction flag without text must fail', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status,
  contradiction_flag, rulebook_version, coding_ts)
VALUES ('PRF-00009', 2, 'RATER-A', 3, 'x', 'present', TRUE, '1.0', now());""", 'fail')

run('N-09', 'Duplicate (profile,dim,rater,rulebook) must fail', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status, rulebook_version, coding_ts)
VALUES ('PRF-00001', 1, 'RATER-A', 4, 'duplicate attempt', 'present','1.0', now());""", 'fail')

run('N-10', 'FK violation: nonexistent profile must fail', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status, rulebook_version, coding_ts)
VALUES ('PRF-99999', 1, 'RATER-A', 3, 'x', 'present','1.0', now());""", 'fail')

run('N-11', 'not_applicable on a PROFILE must fail (posting-only state)', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status, rulebook_version, coding_ts)
VALUES ('PRF-00009', 3, 'RATER-A', 0, 'x', 'not_applicable','1.0', now());""", 'fail')

run('N-12', 'Malformed profile_id must fail', """
INSERT INTO alcsm.profile (profile_id, sampling_batch_id, search_query, inclusion_reason, collection_ts)
VALUES ('PROFILE-1','BATCH-001','q','title_match', now());""", 'fail')

run('N-13', 'Invalid dimension_number (7) FK must fail', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id, dimension_number, rater_id, score, evidence_text, missing_status, rulebook_version, coding_ts)
VALUES ('PRF-00009', 7, 'RATER-A', 3, 'x', 'present','1.0', now());""", 'fail')

run('N-14', 'DELETE profile with child scores must be RESTRICTed', """
DELETE FROM alcsm.profile WHERE profile_id = 'PRF-00001';""", 'fail')

run('N-15', 'Adjudication referencing BOTH corpora must fail', """
INSERT INTO alcsm.job_posting (posting_id, sampling_batch_id, posting_source, search_query,
  inclusion_reason, collection_ts, raw_posting_text)
VALUES ('JOB-00001','BATCH-005','linkedin_jobs','q','title_match', now(), 'text');
INSERT INTO alcsm.adjudication_record
 (profile_id, posting_id, dimension_number, score_rater_a, score_rater_b,
  resolution_route, final_score, adjudication_reason)
VALUES ('PRF-00002','JOB-00001', 1, 2, 3, 'consensus', 3, 'invalid dual reference');""", 'fail')

run('N-16', 'Engagement mean without denominator must fail', """
INSERT INTO alcsm.rq4_impact_indicator
 (profile_id, rq4_content_engagement, extraction_method, extraction_ts)
VALUES ('PRF-00003', 45.5, 'manual', now());""", 'fail')

run('N-17', 'Survey record without consent must fail', """
INSERT INTO alcsm.survey_instrument VALUES ('SV-1.0','Expert review','content_validity',NULL, now());
INSERT INTO alcsm.survey_respondent (respondent_id, survey_version, consent_confirmed, consent_ts)
VALUES ('RSP-0001','SV-1.0', FALSE, now());""", 'fail')

# ---------- POSTING-SIDE ----------
run('T-13', 'Job posting insert (raw text retained)', """
INSERT INTO alcsm.job_posting (posting_id, sampling_batch_id, posting_source, search_query,
  inclusion_reason, collection_ts, posting_language, raw_posting_text, raw_requirements_text)
VALUES ('JOB-00002','BATCH-005','linkedin_jobs','"Head of AI"','title_match', now(), 'en',
        'full posting text','MSc in AI required');""", 'success')

run('T-14', 'Posting requirement: not_applicable requires unspecified modality', """
INSERT INTO alcsm.job_requirement_score
 (posting_id, dimension_number, rater_id, required_score, requirement_modality,
  missing_status, rulebook_version, coding_ts)
VALUES ('JOB-00002', 6, 'RATER-A', 0, 'unspecified', 'not_applicable','1.0', now());""", 'success')

run('N-18', 'not_applicable with modality=required must fail', """
INSERT INTO alcsm.job_requirement_score
 (posting_id, dimension_number, rater_id, required_score, requirement_modality,
  missing_status, rulebook_version, coding_ts)
VALUES ('JOB-00002', 5, 'RATER-A', 0, 'required', 'not_applicable','1.0', now());""", 'fail')

run('T-15', 'Posting requirement present with evidence', """
INSERT INTO alcsm.job_requirement_score
 (posting_id, dimension_number, rater_id, required_score, requirement_modality,
  evidence_text, missing_status, rulebook_version, coding_ts)
VALUES ('JOB-00002', 1, 'RATER-A', 4, 'required', 'MSc in AI required','present','1.0', now());""", 'success')

# ---------- NLP ----------
run('T-16', 'NLP model run + prediction', """
INSERT INTO alcsm.nlp_model_run (pipeline_run_id, model_name, model_version, dimension_number,
  random_seed, information_base, run_ts)
VALUES ('RUN-0001','clf_d1','1.0', 1, 42, 'profile_text_only', now());
INSERT INTO alcsm.nlp_prediction (profile_id, dimension_number, pipeline_run_id,
  predicted_score, prediction_confidence, prediction_ts)
VALUES ('PRF-00001', 1, 'RUN-0001', 4, 0.812, now());""", 'success')

# ---------- VIEW TESTS ----------
query('V-01', 'v_reliability_input EXCLUDES adjudicated rows',
 "SELECT count(*) FROM alcsm.v_reliability_input WHERE unit_id='PRF-00008' AND dimension_number=5;",
 lambda r: (r[0][0] == 2, f"expected 2 independent rows, got {r[0][0]}"))

query('V-02', 'v_final_profile_score PREFERS adjudicated score (=3)',
 "SELECT score, from_adjudication FROM alcsm.v_final_profile_score WHERE profile_id='PRF-00008' AND dimension_number=5;",
 lambda r: (r[0][0] == 3 and r[0][1] is True, f"got score={r[0][0]}, from_adjudication={r[0][1]}"))

query('V-03', 'v_profile_completeness: sparse profile = 2/6 informative',
 "SELECT completeness_index FROM alcsm.v_profile_completeness WHERE profile_id='PRF-00010';",
 lambda r: (float(r[0][0]) == 0.33, f"expected 0.33, got {r[0][0]}"))

query('V-04', 'v_profile_completeness: absent_stated informative, denominator=6 (F-01)',
 "SELECT completeness_index FROM alcsm.v_profile_completeness WHERE profile_id='PRF-00003';",
 lambda r: (float(r[0][0]) == 0.17, f"expected 0.17 (1 informative of 6), got {r[0][0]}"))

query('V-05', 'v_credential_gap excludes not_applicable rows from D6',
 "SELECT dimension_number, mean_required, n_postings FROM alcsm.v_credential_gap_by_dimension WHERE dimension_number=6;",
 lambda r: (r[0][1] is None and r[0][2] is None, f"expected NULL (excluded), got {r[0][1]}, n={r[0][2]}"))

query('V-06', 'v_nlp_evaluation computes error vs gold standard',
 "SELECT gold_score, predicted_score, absolute_error, exact_match FROM alcsm.v_nlp_evaluation WHERE profile_id='PRF-00001';",
 lambda r: (r[0][2] == 1 and r[0][3] is False, f"gold={r[0][0]}, pred={r[0][1]}, abs_err={r[0][2]}"))

query('V-07', 'adjudication_record generated magnitude column = 2',
 "SELECT disagreement_magnitude, resolution_route FROM alcsm.adjudication_record WHERE profile_id='PRF-00008';",
 lambda r: (r[0][0] == 2 and r[0][1]=='escalated', f"got magnitude={r[0][0]}, route={r[0][1]}"))

query('V-08', 'updated_ts trigger fires on profile UPDATE',
 "UPDATE alcsm.profile SET profile_geography='CH' WHERE profile_id='PRF-00009' RETURNING (updated_ts >= created_ts);",
 lambda r: (r[0][0] is True, f"trigger result {r[0][0]}"))


# ---------- v1.0.1 REGRESSION TESTS (F-01 .. F-05) ----------

query('V-09', 'F-01 coding_complete distinguishes sparse from incomplete',
 "SELECT profile_id, completeness_index, dimensions_scored, coding_complete "
 "FROM alcsm.v_profile_completeness WHERE profile_id IN ('PRF-00010','PRF-00006') ORDER BY 1;",
 lambda r: (dict((x[0], (float(x[1]), x[2], x[3])) for x in r) ==
            {'PRF-00006': (0.17, 1, False), 'PRF-00010': (0.33, 6, True)},
            f"got {r}"))

query('V-10', 'F-01 fully coded profile = 1.00',
 "SELECT completeness_index, coding_complete FROM alcsm.v_profile_completeness WHERE profile_id='PRF-00001';",
 lambda r: (float(r[0][0]) == 1.00 and r[0][1] is True, f"got {r[0]}"))

run('N-19', 'F-02 primary rater flagged is_adjudication=TRUE must fail', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,rulebook_version,coding_ts,is_adjudication)
VALUES ('PRF-00009',6,'RATER-A',3,'x','present','1.0',now(),TRUE);""", 'fail')

run('N-20', 'F-02 ADJUDICATOR row with is_adjudication=FALSE must fail', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,rulebook_version,coding_ts,is_adjudication)
VALUES ('PRF-00007',6,'ADJUDICATOR',3,'x','present','1.0',now(),FALSE);""", 'fail')

run('N-21', 'F-03 consensus route at magnitude>=2 must fail', """
INSERT INTO alcsm.adjudication_record
 (profile_id,dimension_number,score_rater_a,score_rater_b,resolution_route,
  final_score,adjudicator_id,adjudication_reason)
VALUES ('PRF-00005',1,0,5,'consensus',3,'ADJUDICATOR','magnitude 5 must escalate');""", 'fail')

run('T-17', 'F-03 consensus route at magnitude 1 still permitted', """
INSERT INTO alcsm.adjudication_record
 (profile_id,dimension_number,score_rater_a,score_rater_b,resolution_route,
  final_score,adjudicator_id,adjudication_reason)
VALUES ('PRF-00005',2,2,3,'consensus',2,'ADJUDICATOR','magnitude 1 consensus permitted');""", 'success')

run('N-22', 'F-04 absent_stated without evidence must fail', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id,dimension_number,rater_id,score,missing_status,rulebook_version,coding_ts)
VALUES ('PRF-00009',4,'RATER-A',1,'absent_stated','1.0',now());""", 'fail')

run('N-23', 'F-04 unavailable WITH evidence must fail', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,rulebook_version,coding_ts)
VALUES ('PRF-00009',5,'RATER-A',0,'some evidence','unavailable','1.0',now());""", 'fail')

run('N-24', 'F-05 ambiguity candidates not bracketing score must fail', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,
  ambiguity_flag,ambiguity_candidate_low,ambiguity_candidate_high,rulebook_version,coding_ts)
VALUES ('PRF-00007',1,'RATER-A',5,'x','present',TRUE,1,2,'1.0',now());""", 'fail')

run('N-25', 'F-04 posting-side unavailable WITH evidence must fail', """
INSERT INTO alcsm.job_requirement_score
 (posting_id,dimension_number,rater_id,required_score,requirement_modality,
  evidence_text,missing_status,rulebook_version,coding_ts)
VALUES ('JOB-00002',3,'RATER-A',0,'unspecified','ev','unavailable','1.0',now());""", 'fail')

run('T-18', 'F-05 ambiguity candidates correctly bracketing score still permitted', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,
  ambiguity_flag,ambiguity_candidate_low,ambiguity_candidate_high,rulebook_version,coding_ts)
VALUES ('PRF-00007',2,'RATER-A',2,'x','present',TRUE,2,3,'1.0',now());""", 'success')

# ---------- REPORT ----------
print(f"{'ID':<7}{'EXPECT':<9}{'ACTUAL':<9}{'RESULT':<11}DESCRIPTION")
print("-"*118)
mismatches = 0
for tid, desc, exp, act, res, det in results:
    if res != 'PASS': mismatches += 1
    print(f"{tid:<7}{exp:<9}{act:<9}{res:<11}{desc[:60]}")
    if res != 'PASS' and det:
        print(f"       └─ {det}")
print("-"*118)
print(f"TOTAL: {len(results)} tests | PASS: {len(results)-mismatches} | MISMATCH: {mismatches}")
conn.close()
sys.exit(0 if mismatches == 0 else 1)
