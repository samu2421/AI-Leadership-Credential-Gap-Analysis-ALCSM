# P3 Test Strategy

**Version:** 0.1-DRAFT
**Status:** Design document only — defines how future P3 code (job-posting write path, `taxonomy/anchoring.py`) will be tested. No P3 implementation code has been written this session; no real data is used anywhere in this strategy.
**Purpose:** define, before any P3 code is written, the testing approach for the job-posting collection tooling and taxonomy anchoring, extending the existing pattern already proven in P1 (`tests/collection/`) rather than inventing a new one.
**Last Updated:** 2026-08-02
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance, Phase P3 Session 1
**Related documents:** `PROJECT_CONTEXT.md` §33 (Testing Strategy), `tests/collection/conftest.py` (the pattern this strategy extends), `Task5_P3_JobPosting_Collection_Plan.md`, `src/alcsm/taxonomy/anchoring.py`

---

## 1. Governing principle (unchanged from P1)

*"Test against the specification, not the implementation"* (`PROJECT_CONTEXT.md` §33) — a documented past failure mode on this project was a test that encoded the *buggy* behaviour of the completeness view and therefore passed while the code was wrong. Every P3 test must be written from the frozen rules (`PROJECT_CONTEXT.md`, the schema's own CHECK constraints, `Task5_P3_JobPosting_Collection_Plan.md`) — never from "whatever the code currently does." No real personal data, and no real job-posting text scraped from an actual source, is ever used in a test — only constructed, synthetic fixtures, matching `CLAUDE_CODE_RULES.md` rule 6.

## 2. Unit tests (pure logic, no database)

Mirrors `tests/collection/test_validation.py`'s existing pattern for the profile side. For the future job-posting validator (§10.1 of the Job Posting Collection Plan):
- `posting_id` format acceptance/rejection (`^JOB-[0-9]{5}$` — valid, too-short, wrong-prefix, lowercase-letters cases).
- Provenance completeness: each of `sampling_batch_id`, `search_query`, `inclusion_reason`, `collection_ts` individually missing produces a readable, combined error listing every problem at once (not just the first) — matching `ProfileValidationError`'s existing contract.
- `inclusion_reason` controlled-vocabulary check (accepts `title_match`/`title_variant_match`/`manual_review_included`; rejects anything else).
- ISO-code shape checks for `posting_language`/`posting_geography`, reusing the same regex patterns already defined for profiles (`_LANGUAGE_PATTERN`, `_GEOGRAPHY_PATTERN` in `collection/helper.py`) rather than redefining them.
- `raw_posting_text` non-empty check (a posting with only whitespace or an empty string is rejected before it reaches the database).
- Recruiter-redaction check, once built (§10.2 of the Job Posting Collection Plan): a constructed posting text containing an obviously-named contact pattern is rejected/flagged; a posting with no such pattern passes untouched.

For `taxonomy/anchoring.py` once implemented:
- Term extraction from a small, constructed corpus of synthetic posting texts (never real postings) produces the expected candidate terms and frequencies for a hand-verifiable case (e.g. three synthetic postings mentioning "TensorFlow" twice and "PyTorch" once should yield exactly those counts).
- A term with zero evidence in the constructed corpus is never invented into the output — this is the single highest-value test in the whole P3 suite, since it directly guards the frozen "never invent unevidenced terms" rule.
- `taxonomy_version_id` stamping produces the correct `taxonomy_name` (one of the eight fixed values) and a version label that does not collide with an existing one in the fixture.
- Attempting to write a term against an already-`frozen=TRUE` taxonomy version is rejected (mirrors the "frozen version, never edited" rule) — this test should fail loudly if anchoring code ever allows it, since a silent success here would be a real methodology violation, not just a code bug.

## 3. Integration tests (real throwaway PostgreSQL, real schema)

Extends the exact pattern already proven in `tests/collection/conftest.py` — a disposable PostgreSQL 16 cluster (never `alcsm_dev`) provisioned per test session with `alcsm_schema_v1.0.1.sql` deployed, torn down afterward, and skipped (not failed) if local PostgreSQL 16 binaries are absent. A new `tests/taxonomy/conftest.py` (and, once the job-posting helper functions exist, a shared or sibling fixture for them) should reuse `tests/collection/conftest.py`'s `pg_binaries`/cluster-lifecycle fixtures rather than re-implementing cluster bring-up — proposed as a small shared fixture module under `tests/conftest.py` if duplication would otherwise occur between `tests/collection/` and `tests/taxonomy/`.

Cases to cover once the job-posting write path exists:
- `create_job_posting_batch()` is idempotent (a duplicate `sampling_batch_id` with `corpus='job_posting'` is a no-op, mirroring `create_sampling_batch()`'s existing `ON CONFLICT DO NOTHING` behaviour).
- `insert_job_posting()` is atomic: a deliberately invalid second write (e.g. violating a schema CHECK constraint the pure-logic validator wouldn't catch, such as a foreign-key reference to a non-existent `sampling_batch_id`) leaves **no** partial row — assert the posting table is empty afterward, exactly mirroring the existing profile-side atomicity test.
- `verify_posting()` correctly reports on a constructed record with `raw_posting_text` present vs. (deliberately, for the test only) absent.
- Real constraint rejections from the schema itself (e.g. `job_posting.raw_posting_text NOT NULL`) surface as a clear, caught error — proving the schema's own protection still holds even if application-level validation were bypassed.

Cases to cover once `taxonomy/anchoring.py` writes to the database:
- A stamped `taxonomy_version` row round-trips correctly (write, then read back, matches).
- `taxonomy_term` rows are correctly linked via `taxonomy_version_id` foreign key; attempting a term insert against a non-existent version is rejected by the schema (`ON DELETE RESTRICT` / FK constraint), proving the real constraint fires.
- The `UNIQUE (taxonomy_version_id, term)` constraint is exercised directly: inserting the same term twice against one version is rejected, not silently duplicated.

## 4. Validation tests (schema-level, environment smoke test)

Unchanged from the existing P0/P1 pattern — no new work needed here, only confirmation it still applies: deploying `alcsm_schema_v1.0.1.sql` to a throwaway database and running the 67-test validation harness (`03_Database_Design/03_Validation/alcsm_validation_harness_v1.0.1.py`) remains the required check for any new environment touching P3 code. This session's audit (Task 1) did not re-run the harness, since no schema change occurred; it should be re-run once real P3 collection infrastructure is deployed to a new environment (e.g. before the secure store goes live).

## 5. Constructed-fixture tests (the only kind used before ethics approval)

Every fixture used in P3 tests — synthetic postings, synthetic profile records already used in P1 — is invented text resembling the shape of real data, never derived from an actual scraped or manually-viewed real posting or profile. This is not merely a style preference: `CLAUDE_CODE_RULES.md` rule 6/8 and `PROJECT_CONTEXT.md` §46 make using real data in a test before ethics approval a compliance violation, not a quality issue. Concretely: a synthetic posting fixture like *"Seeking a Head of AI to lead a 12-person applied-ML team... TensorFlow, PyTorch, and Kubernetes experience preferred..."* is fine; copying real text observed on an actual live job board, even fragmentarily, is not.

## 6. Future real-data validation (explicitly out of scope for any test written this session)

Once P2 clears and real postings/profiles exist, a **separate**, later validation activity (not a unit or integration test in the pytest sense) checks real collected data against this plan's rules — e.g. sampling a handful of real inserted postings and confirming `raw_posting_text` genuinely came from a permitted source. This is operational QA (already specified in §6/§9 of the two Task 3/4 design documents), not part of the automated test suite, and is explicitly **not** built or run in this session.

## 7. Boundary cases to exercise (once code exists)

- Posting with `raw_requirements_text` present but structurally identical to `raw_posting_text` (a posting with no separately-delineated requirements section) — should not error, just capture the same text in both if that is genuinely all that exists.
- Posting with an extremely short (but non-empty) `raw_posting_text` — passes structural validation (it is not literally empty) but should be flagged by the QA spot-check (§6 of the Job Posting Collection Plan) as a candidate for exclusion under the "content-free listing" rule, since that judgement is a human QA call, not something the structural validator can or should reject automatically.
- Taxonomy anchoring on a corpus where one category (e.g. `automation_augmentation`) has zero evidenced terms — the anchoring code must produce an empty term list for that taxonomy version, never fabricate placeholder terms to avoid an empty result.
- Duplicate-posting detection at the boundary: two constructed postings differing only in whitespace/punctuation but otherwise identical — the QA/dedup logic's behaviour on this near-duplicate case should be an explicit, tested decision (documented in the Job Posting Collection Plan once built), not an accident of string equality.

## 8. Error handling verification

- Every new validation function follows the existing `ProfileValidationError` contract: collect all problems, raise once, never fail on the first issue only (`collection/helper.py`'s existing pattern, to be mirrored exactly for postings).
- Every new database write function follows the existing atomic, fail-loud, roll-back-whole-transaction pattern (`PROJECT_CONTEXT.md` §32) — tested by deliberately forcing a failure partway through a multi-statement insert and asserting zero partial rows remain, exactly as the existing profile-insert atomicity test already does.
- No new code swallows an exception to "keep going" — a test asserting an exception propagates (rather than being caught and logged only) is required wherever the existing profile-side code has that shape.

## 9. Logging verification

- Mirrors the existing pattern: log messages reference only pseudonymous IDs (`PRF-#####`, and the future `JOB-#####`) and batch IDs — never raw posting/profile text. A test should assert that a captured log record from an insert function contains the record's ID and does **not** contain any fixture text substring, catching an accidental personal/content leak into logs at the test level rather than relying on manual review alone.
- Recruiter-redaction events (§6 of the Job Posting Collection Plan) log that a redaction occurred, never the redacted content itself — tested the same way.

## 10. What this strategy does not do

- It does not write any test file yet — `tests/taxonomy/test_anchoring.py`'s current single skeleton test (`NotImplementedError` on the stub) remains the only P3-adjacent test in the repository after this session, unchanged.
- It does not implement the job-posting write path or `taxonomy/anchoring.py` — those are Session 2+ implementation tasks this strategy prepares for.
- It does not relax or add to any frozen rule — every case above tests an existing frozen constraint or an already-designed (Task 3/4 documents) rule, never a new one invented here.

---

*This strategy extends the existing, already-proven P1 testing pattern (`tests/collection/`) to P3's two implementation surfaces. No frozen ALCSM methodology, database schema, or existing test is altered by this document.*
