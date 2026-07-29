"""
ALCSM Manual Collection Helper  —  collection_helper.py
=======================================================
Writes ONE manually-collected LinkedIn profile into the frozen ALCSM
Schema v1.0.1.

WHAT THIS IS
  A structured DATA-ENTRY tool. A human reads a public profile by eye and
  types the field values in. This module pseudonymises, validates, and
  inserts them transactionally, honouring every frozen constraint.

WHAT THIS IS NOT
  It performs NO browsing, NO scraping, NO automated retrieval of LinkedIn.
  There is deliberately no HTTP client here. Automated collection is a
  breach-of-ToS / GDPR exposure (see Task 5 roadmap) and is out of scope.

It does NOT score dimensions. Scoring is the separate annotation stage.
It does NOT store names, URLs, photographs, or contact details.
"""

import psycopg2, re, datetime, sys

SECTIONS = ('headline','about','experience','education',
            'certifications','contributions','activity')


# ---------------------------------------------------------------------
# Pre-insertion validation — runs BEFORE the database is touched.
# Catches human data-entry mistakes early, in plain language, rather
# than as raw constraint errors mid-transaction.
# ---------------------------------------------------------------------
def validate_profile_record(rec):
    errs = []

    # Identity / privacy: nothing that could be a direct identifier.
    if not re.fullmatch(r'PRF-\d{5}', rec.get('profile_id','')):
        errs.append("profile_id must match PRF-##### (assign at capture)")
    for forbidden in ('name','full_name','profile_url','url','photo','email','phone'):
        if rec.get(forbidden):
            errs.append(f"forbidden identifier field present: {forbidden!r} "
                        f"(never store direct identifiers)")

    # Provenance: mandatory, per the frozen requirement.
    for f in ('sampling_batch_id','search_query','inclusion_reason','collection_ts'):
        if not rec.get(f):
            errs.append(f"missing provenance field: {f}")
    if rec.get('inclusion_reason') not in ('title_match','title_variant_match','manual_review_included'):
        errs.append("inclusion_reason not in the controlled vocabulary")

    # ISO shape (advisory; DB may or may not enforce depending on optional patch).
    lang = rec.get('profile_language','und')
    if lang != 'und' and not re.fullmatch(r'[a-z]{2}', lang):
        errs.append("profile_language must be ISO 639-1 (2 lowercase letters) or 'und'")
    geo = rec.get('profile_geography')
    if geo is not None and not re.fullmatch(r'[A-Z]{2}', geo):
        errs.append("profile_geography must be ISO 3166-1 alpha-2 or None")

    # Sections: each must declare availability explicitly.
    secs = rec.get('sections', {})
    for name, s in secs.items():
        if name not in SECTIONS:
            errs.append(f"unknown section name: {name!r}")
        if 'available' not in s:
            errs.append(f"section {name!r} missing 'available' flag "
                        f"(empty vs not-retrieved must be explicit)")
        # Coherence: not-available implies no captured text.
        if s.get('available') is False and s.get('text'):
            errs.append(f"section {name!r}: available=False but text present "
                        f"(a not-retrieved section cannot have text)")

    # Activity ethics gate: activity text implies the ethics-flagged collection.
    act = secs.get('activity', {})
    if act.get('available') and act.get('text') and not rec.get('activity_data_collected'):
        errs.append("activity section captured but activity_data_collected is False "
                    "(post-level activity needs its own ethics justification)")

    return errs


# ---------------------------------------------------------------------
# One-time per search: register the batch (provenance root).
# ---------------------------------------------------------------------
def create_sampling_batch(cur, batch):
    cur.execute("""
        INSERT INTO alcsm.sampling_batch
          (sampling_batch_id, corpus, search_query, platform,
           collection_started_ts, collection_ended_ts,
           result_set_size, records_included, inclusion_protocol_version, notes)
        VALUES (%(sampling_batch_id)s,'profile',%(search_query)s,%(platform)s,
                %(started_ts)s,%(ended_ts)s,%(result_set_size)s,
                %(records_included)s,%(inclusion_protocol_version)s,%(notes)s)
        ON CONFLICT (sampling_batch_id) DO NOTHING;""", batch)


# ---------------------------------------------------------------------
# Insert ONE profile: identity+provenance, raw sections, optional
# RQ4 criterion values — all in a single transaction. Any failure
# rolls the whole profile back, so no half-captured records exist.
# ---------------------------------------------------------------------
def insert_profile(conn, rec, criterion=None):
    problems = validate_profile_record(rec)
    if problems:
        raise ValueError("Validation failed:\n  - " + "\n  - ".join(problems))

    cur = conn.cursor()
    try:
        # 1. profile (identity + provenance + collection context)
        cur.execute("""
            INSERT INTO alcsm.profile
              (profile_id, sampling_batch_id, profile_source, search_query,
               search_rank_position, inclusion_reason, collection_ts,
               profile_language, profile_geography, observation_window_days,
               activity_data_collected)
            VALUES (%(profile_id)s,%(sampling_batch_id)s,'linkedin',%(search_query)s,
                    %(search_rank_position)s,%(inclusion_reason)s,%(collection_ts)s,
                    %(profile_language)s,%(profile_geography)s,%(observation_window_days)s,
                    %(activity_data_collected)s);""",
            {**{'search_rank_position':None,'profile_language':'und',
                'profile_geography':None,'observation_window_days':None,
                'activity_data_collected':False}, **rec})

        # 2. raw sections (long format; availability explicit)
        for name in SECTIONS:
            s = rec['sections'].get(name, {'available': False, 'text': None})
            cur.execute("""
                INSERT INTO alcsm.profile_raw_section
                  (profile_id, section_name, section_text, section_available, captured_ts)
                VALUES (%s,%s,%s,%s,%s);""",
                (rec['profile_id'], name,
                 s.get('text') if s.get('available') else None,
                 bool(s.get('available')),
                 rec['collection_ts']))

        # 3. RQ4 criterion values (optional, ISOLATED table — never shown to raters)
        if criterion:
            cur.execute("""
                INSERT INTO alcsm.rq4_impact_indicator
                  (profile_id, rq4_network_reach, rq4_network_reach_capped,
                   rq4_content_engagement, rq4_content_post_count,
                   rq4_recognition_count, rq4_seniority_progression_rate,
                   rq4_observation_window_days, extraction_method, extracted_by, extraction_ts)
                VALUES (%(profile_id)s,%(rq4_network_reach)s,%(rq4_network_reach_capped)s,
                        %(rq4_content_engagement)s,%(rq4_content_post_count)s,
                        %(rq4_recognition_count)s,%(rq4_seniority_progression_rate)s,
                        %(rq4_observation_window_days)s,%(extraction_method)s,
                        %(extracted_by)s,%(extraction_ts)s);""",
                {**{'rq4_network_reach':None,'rq4_network_reach_capped':None,
                    'rq4_content_engagement':None,'rq4_content_post_count':None,
                    'rq4_recognition_count':None,'rq4_seniority_progression_rate':None,
                    'rq4_observation_window_days':None,'extracted_by':None},
                 **{'profile_id':rec['profile_id']}, **criterion})

        conn.commit()
        return rec['profile_id']
    except Exception:
        conn.rollback()   # atomic: a failed profile leaves NO partial rows
        raise
    finally:
        cur.close()


# ---------------------------------------------------------------------
# Post-insertion verification for one profile.
# ---------------------------------------------------------------------
def verify_profile(conn, profile_id):
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM alcsm.profile_raw_section WHERE profile_id=%s", (profile_id,))
    n_sections = cur.fetchone()[0]
    cur.execute("""SELECT bool_or(section_text IS NOT NULL AND section_available=FALSE)
                   FROM alcsm.profile_raw_section WHERE profile_id=%s""", (profile_id,))
    incoherent = cur.fetchone()[0]
    cur.close()
    return {'sections': n_sections, 'coherent': not bool(incoherent)}
