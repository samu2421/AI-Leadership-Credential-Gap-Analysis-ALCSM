# LinkedIn Data Collection Workflow (SOP)
### Manual, Human-Driven Collection — Frozen ALCSM v1.0 / Schema v1.0.1

**Thesis:** *The AI Leadership Credential Gap: An NLP Audit of 500 LinkedIn Profiles*
**Method:** manual collection. A human reads each public profile and records the ALCSM-relevant fields by hand into the database. **No scraping, no browser automation, no automated retrieval.** This is the method recommended in the Task 5 roadmap because automated collection breaches LinkedIn's User Agreement (the basis on which hiQ lost) and raises GDPR exposure. Every step below matches the frozen framework and schema; **no schema modification is involved.**

**Verification status.** The database-facing parts of this SOP were executed against a live PostgreSQL 16 instance running Schema v1.0.1: the insertion helper passed 8/8 tests (including atomic rollback), the empty-vs-not-retrieved distinction stored correctly, criterion isolation held, and a `pg_dump`/`pg_restore` round-trip restored all data intact.

**Hard gate.** Do not run any step past §1 until the Task 5 collection-readiness gate (M8) is cleared: ethics approval, GDPR/DPIA sign-off, approved collection method, and pre-registered protocol. This SOP is the *how*; approval is the *whether*.

---

## Step 0 — Preconditions (verify once, before a session)

- Ethics approval reference on file; approved method = manual collection.
- Pre-registered sampling protocol frozen (title list, inclusion/exclusion, query strings, quotas, language scope, collection window).
- Secure store live; database deployed from `alcsm_schema_v1.0.1.sql`; reference data loaded.
- `sampling_batch` row created for this search **before** any profile is captured (it is the provenance root; every profile references it).
- Re-identification-mapping decision made (DMP §4.1). This SOP assumes **no persistent mapping**; if a temporary one is used it lives outside this database.

---

## Step 1 — Browser workflow (manual, public-only)

1. Open a standard browser session. Navigate to LinkedIn.
2. **Collect only what is publicly visible.** Do not use techniques that expose data behind the login/connection wall beyond what an ordinary public viewer sees. The hiQ ruling turned partly on accessing login-gated data via fake accounts — stay strictly on public content.
3. Run one pre-registered search query at a time. Record the **exact query string** and the **result-set ordering** as you go — you will need `search_rank_position`.
4. Work through results in their natural order, applying the selection rules in Step 2. Do not re-order or cherry-pick; the ranking bias is disclosed, not corrected.
5. **Do not** save the page, the URL, screenshots containing identifiers, or the profile photo. You are transcribing field *content*, not archiving the person.

*Reviewer note:* this is deliberately slow and deliberately manual. 500 profiles across a fixed collection window is tractable, and manual transcription is exactly what keeps you clear of the "automated means" prohibition.

---

## Step 2 — Profile selection

Apply the **pre-registered** inclusion/exclusion criteria exactly as written (Task 5 §5.2). For each candidate:

- **Include** if: the profile publicly presents a qualifying AI-leadership title from the frozen title list; it is publicly viewable; its language is within scope.
- **Exclude** (and log the reason) if: it is a duplicate of an already-captured individual; it is not publicly viewable; the title is outside the list; the language is out of scope; it is a company/non-person page.
- **Deduplication:** before capturing, confirm the individual is not already in the sample. Because you store no name, keep a *transient, session-local* check (e.g. a scratch note of a non-stored discriminator) and discard it after the session — do not persist it into the database.

Record `inclusion_reason` as one of `title_match`, `title_variant_match`, `manual_review_included`.

---

## Step 3 — Pseudonymisation (at the moment of capture, not after)

1. Assign the next identifier in sequence: `PRF-00001`, `PRF-00002`, … (format enforced by the schema).
2. From this point on, the record is referred to **only** by its `PRF-#####`.
3. **Never** enter a name, profile URL, photograph, email, or phone number into the database. The insertion helper actively rejects any record carrying such a field, before it reaches the database.

This is data minimisation (GDPR) implemented at the earliest possible point.

---

## Step 4 — Section extraction and evidence capture

For each of the seven canonical sections — `headline`, `about`, `experience`, `education`, `certifications`, `contributions`, `activity` — record two things:

- **`available`** (boolean): was the section retrievable at all?
- **`text`**: the verbatim content, **only if available**.

The critical distinction, which the schema and the framework both depend on:

| Situation | `available` | `text` |
|---|---|---|
| Section present with content | `True` | the verbatim text |
| Section present but genuinely empty | `True` | empty string / minimal |
| Section absent or not retrievable | `False` | `None` |

A `False`/not-retrieved section **must** carry no text — the helper rejects the contradiction. This is what later lets scoring distinguish *`unavailable`* (no evidence found) from *`absent_stated`* (the person positively states absence), which the frozen missing-data policy requires never be conflated.

**Activity section is special:** capture it **only** if `activity_data_collected` is set, because post-level activity carries its own ethics/GDPR justification. The helper blocks activity text when the flag is False.

Transcribe faithfully. Do not summarise, interpret, or score — scoring is a separate stage with its own rulebook. Do not record any incidental special-category content (Article 9): if a section reveals, e.g., political or health information not needed for ALCSM, omit that content.

---

## Step 5 — Criterion capture (RQ4, isolated)

If your protocol captures the RQ4 observable impact indicators at collection time (recommended, since some are time-sensitive), record them into the **separate** `rq4_impact_indicator` table:

- `rq4_network_reach` (+ `rq4_network_reach_capped` if the platform shows a capped figure like "500+")
- `rq4_content_engagement`, `rq4_content_post_count`, `rq4_observation_window_days`
- `rq4_recognition_count` — recognition **conferred by others** only (awards, invited talks, board seats); **not** publications/patents/repositories, which belong to dimension D4 and must not be reused here (circularity).
- `rq4_seniority_progression_rate` — derived from dated role transitions; never uses the D5 score as an input.

These values live in their own table and **must never be visible to raters during scoring** (predictor/criterion contamination). Collection may see them; annotation may not.

---

## Step 6 — Quality checks (before insertion)

The helper runs `validate_profile_record()` before touching the database. It catches, in plain language:

- malformed or missing `PRF-#####`;
- any forbidden identifier field (name/URL/photo/email/phone);
- missing provenance (`sampling_batch_id`, `search_query`, `inclusion_reason`, `collection_ts`);
- `inclusion_reason` outside the controlled vocabulary;
- ISO shape errors on language/geography;
- a section missing its `available` flag;
- the not-retrieved-but-has-text contradiction;
- activity text without the ethics flag.

Only a record that passes all of these proceeds to insertion. This turns silent data-entry mistakes into immediate, readable errors.

---

## Step 7 — Database insertion (atomic)

`insert_profile()` writes the whole profile in **one transaction**:

1. the `profile` row (identity + provenance + collection context);
2. all seven `profile_raw_section` rows (availability explicit);
3. the optional `rq4_impact_indicator` row.

If **any** step fails — including a database-level `CHECK` violation — the entire transaction rolls back. **Tested:** a profile whose criterion violated a `CHECK` left **zero** rows behind. There is no such thing as a half-captured profile.

The insertion honours every frozen v1.0.1 constraint automatically; the helper does not and cannot bypass them.

---

## Step 8 — Audit logging (outside the database)

Maintain a running **collection log** in the secure store (not in Git, not in the research DB):

- session date and collector;
- each query run, result-set size, records included vs. excluded;
- every exclusion with its reason;
- any anomaly, interruption, or deviation from the protocol;
- the `PRF-#####` range assigned in the session.

Also update the `sampling_batch` row's `result_set_size` and `records_included` so the sampling rate (what fraction of an algorithmically ranked result set entered the sample) is recoverable — a real external-validity measure. The log is your Methods-chapter audit trail.

---

## Step 9 — Version tracking

Collection records the *collection* protocol version (`inclusion_protocol_version` on the batch). Scoring — a later stage — stamps `rulebook_version`, `alcsm_version`, and `taxonomy_version_id` on each score. Two consequences for the collector:

- Do not begin **scoring** until the taxonomies are anchored to the job-posting vocabulary and a `taxonomy_version` is stamped (`frozen = TRUE`); only then may the optional F-06 NOT-NULL constraint be enabled.
- Keep the code repository tagged at the frozen states (`schema-v1.0.1`) so any record can be tied to the exact schema and code that produced it.

---

## Step 10 — Backup procedure

Run `backup_alcsm.sh` on a schedule (e.g. daily during active collection, and after each session). It performs a compressed `pg_dump -Fc`, **verifies the dump is readable** (`pg_restore --list`) before trusting it, prunes to a retention window, and supports optional AES-256 encryption at rest.

**Tested:** dump + restore into a fresh database recovered all profiles and sections intact.

**Security rules:** backups contain pseudonymised personal data. Write them only to the approved, EEA-resident, access-controlled store; encrypt at rest; never place them in Git or on a personal device.

Restore is documented in the script header and should be **rehearsed once** before collection begins, so a real recovery is not the first time you run it.

---

## Step 11 — Error handling

| Failure | What happens | Collector action |
|---|---|---|
| Validation error (Step 6) | Insertion aborts before the DB; readable message | Fix the entry; re-submit |
| DB `CHECK`/FK violation | Transaction rolls back; **no partial rows** | Inspect the message; correct; re-submit |
| Duplicate `PRF-#####` | Unique-key error; rollback | Assign the correct next identifier |
| Duplicate individual detected mid-session | Not a DB error | Exclude; log reason; do not capture |
| Section genuinely ambiguous (empty vs. hidden) | Not a DB error | Default to `available=False` and log the ambiguity; conservatism matches the framework |
| Interruption / crash mid-session | Atomicity guarantees no half-profiles | Resume from the last confirmed `PRF-#####`; the log shows where you stopped |
| Suspected data-entry mistake found later | — | Do **not** silently overwrite; correct via a logged, dated amendment, preserving the original for audit |
| Backup dump fails verification | Script exits non-zero | Do not trust it; investigate storage; re-run before continuing |

**Principle:** the system fails loudly and atomically. A failed profile leaves nothing behind, so retrying is always safe; a passed profile is complete and constraint-valid by construction.

---

## Per-profile quick sequence (field card)

1. Search → next result in order.
2. Public-only view. Record query + rank position.
3. Passes inclusion criteria? If not, exclude + log.
4. Not a duplicate? If it is, exclude + log.
5. Assign `PRF-#####`.
6. Transcribe each of 7 sections: set `available`, capture `text` only if available.
7. (If in protocol) record RQ4 criterion values → isolated table.
8. Run validation.
9. Insert (atomic).
10. Update collection log + batch counts.

---

## Deliverables accompanying this SOP

| File | Role | Verified |
|---|---|---|
| `collection_helper.py` | Manual-entry validation + atomic insertion (no scraping) | 8/8 tests pass on live v1.0.1 |
| `backup_alcsm.sh` | Verified `pg_dump`/restore backup with retention | dump+restore round-trip intact |

**No scraping or browser-automation code is provided, by design.** Collection is performed by a human; these tools only validate, store, and protect what the human transcribes. No modification was made to ALCSM v1.0 or Schema v1.0.1.
