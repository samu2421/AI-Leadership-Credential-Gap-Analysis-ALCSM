import psycopg2
conn = psycopg2.connect(host="/tmp/pgrun", port=5433, dbname="alcsm_test", user="postgres")
gaps = []

def probe(pid, desc, sql, should_be_blocked):
    cur = conn.cursor()
    try:
        cur.execute(sql); conn.commit(); accepted = True
    except Exception:
        conn.rollback(); accepted = False
    cur.close()
    leaked = accepted and should_be_blocked
    gaps.append((pid, desc, 'ACCEPTED' if accepted else 'blocked', 'GAP' if leaked else 'ok'))

probe('G-01', 'absent_stated with NO evidence_text (positive claim unevidenced)', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id,dimension_number,rater_id,score,missing_status,rulebook_version,coding_ts)
VALUES ('PRF-00009',4,'RATER-A',1,'absent_stated','1.0',now());""", True)

probe('G-02', 'unavailable WITH evidence_text (internally contradictory)', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,rulebook_version,coding_ts)
VALUES ('PRF-00009',5,'RATER-A',0,'some evidence','unavailable','1.0',now());""", True)

probe('G-03', 'Primary rater row flagged is_adjudication=TRUE (silently drops from reliability)', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,rulebook_version,coding_ts,is_adjudication)
VALUES ('PRF-00009',6,'RATER-A',3,'x','present','1.0',now(),TRUE);""", True)

probe('G-04', 'ADJUDICATOR row with is_adjudication=FALSE (would enter reliability if role filter absent)', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,rulebook_version,coding_ts,is_adjudication)
VALUES ('PRF-00007',6,'ADJUDICATOR',3,'x','present','1.0',now(),FALSE);""", True)

probe('G-05', 'Ambiguity candidates that do NOT bracket the assigned score', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,
  ambiguity_flag,ambiguity_candidate_low,ambiguity_candidate_high,rulebook_version,coding_ts)
VALUES ('PRF-00007',1,'RATER-A',5,'x','present',TRUE,1,2,'1.0',now());""", True)

probe('G-06', 'Score row with NULL taxonomy_version_id (unversioned coding)', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,rulebook_version,coding_ts)
VALUES ('PRF-00007',2,'RATER-A',3,'x','present','1.0',now());""", True)

probe('G-07', 'Adjudication row with NO prior disagreement on record', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,rulebook_version,coding_ts,is_adjudication)
VALUES ('PRF-00004',6,'ADJUDICATOR',3,'x','present','1.0',now(),TRUE);""", True)

probe('G-08', 'adjudication_record final_score differing from stored adjudicated score row', """
INSERT INTO alcsm.adjudication_record
 (profile_id,dimension_number,score_rater_a,score_rater_b,resolution_route,
  final_score,adjudicator_id,adjudication_reason)
VALUES ('PRF-00004',5,3,4,'consensus',5,'ADJUDICATOR','inconsistent with score table');""", True)

probe('G-09', 'resolution_route=consensus despite magnitude>=2 (violates frozen tie-break)', """
INSERT INTO alcsm.adjudication_record
 (profile_id,dimension_number,score_rater_a,score_rater_b,resolution_route,
  final_score,adjudicator_id,adjudication_reason)
VALUES ('PRF-00005',1,0,5,'consensus',3,'ADJUDICATOR','magnitude 5 should escalate');""", True)

probe('G-10', 'collection_ts in the future', """
INSERT INTO alcsm.profile (profile_id,sampling_batch_id,search_query,inclusion_reason,collection_ts)
VALUES ('PRF-00011','BATCH-001','q','title_match', now() + interval '5 years');""", True)

probe('G-11', 'coding_ts BEFORE the profile collection_ts (coded before collected)', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,rulebook_version,coding_ts)
VALUES ('PRF-00007',3,'RATER-A',3,'x','present','1.0', now() - interval '10 years');""", True)

probe('G-12', 'Invalid ISO language code', """
INSERT INTO alcsm.profile (profile_id,sampling_batch_id,search_query,inclusion_reason,collection_ts,profile_language)
VALUES ('PRF-00012','BATCH-001','q','title_match', now(), 'ENGLISH');""", True)

probe('G-13', 'Invalid ISO country code', """
INSERT INTO alcsm.profile (profile_id,sampling_batch_id,search_query,inclusion_reason,collection_ts,profile_geography)
VALUES ('PRF-00013','BATCH-001','q','title_match', now(), 'Germany');""", True)

probe('G-14', 'Profile scored on only 3 of 6 dimensions (incomplete coding set)', """
INSERT INTO alcsm.alcsm_dimension_score
 (profile_id,dimension_number,rater_id,score,evidence_text,missing_status,rulebook_version,coding_ts)
VALUES ('PRF-00006',1,'RATER-A',3,'x','present','1.0',now());""", True)

probe('G-15', 'activity_data_collected=FALSE yet engagement criterion populated', """
INSERT INTO alcsm.rq4_impact_indicator
 (profile_id,rq4_content_engagement,rq4_content_post_count,rq4_observation_window_days,
  extraction_method,extraction_ts)
VALUES ('PRF-00004',12.5,10,365,'manual',now());""", True)

print(f"{'ID':<7}{'OUTCOME':<11}{'VERDICT':<7}DESCRIPTION")
print("-"*110)
n_gaps=0
for pid,desc,outcome,verdict in gaps:
    if verdict=='GAP': n_gaps+=1
    print(f"{pid:<7}{outcome:<11}{verdict:<7}{desc[:72]}")
print("-"*110)
print(f"{len(gaps)} probes | {n_gaps} unenforced rules found")
conn.close()
