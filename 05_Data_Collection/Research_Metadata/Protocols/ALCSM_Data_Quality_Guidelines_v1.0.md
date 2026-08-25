# ALCSM Data Quality Guidelines

**Version:** 1.0
**Status:** Draft — governance-layer research documentation.
**Document type:** Research protocol (data governance layer, `16_Data/04_Metadata/Protocols/`)
**Last Updated:** 2026-08-02

---

## 1. Purpose

This document defines the data quality principles and rules applied across both ALCSM datasets (LinkedIn profiles and job postings), from collection through to any later correction. It is written as a durable reference for any researcher handling this dataset, present or future.

## 2. Data Accuracy

- Only information that is directly observable in the source (a public LinkedIn profile, a public job posting) may be recorded.
- Transcription is verbatim wherever the dataset structure calls for verbatim text; interpretation and paraphrase are not substituted for source content.
- A field left blank because the information was not observable is recorded as such explicitly, never left ambiguous.

## 3. Consistency Rules

- The same field is recorded the same way across every record — a controlled vocabulary or fixed format is used wherever one is defined, rather than free-text variation.
- A collection decision (e.g. how a borderline case is classified) is applied consistently across the full collection window; a decision is not revisited retroactively for records already collected without a documented, dated reason.
- Units, date formats, and identifier formats are fixed once and used identically throughout the dataset.

## 4. Duplicate Detection

- Before a candidate record is added to the dataset, it is checked against records already collected in the same session, using the identifying signals available (e.g. a source-specific identifier, a source URL, or a normalized title/name comparison where appropriate).
- A confirmed duplicate is excluded, with the exclusion and its reason logged.
- Duplicate-checking signals used only for this purpose are not retained beyond what is necessary to perform the check.

## 5. Missing Values

- A missing value is recorded as missing, never inferred or filled from assumption, context, or a similar record.
- Where the dataset structure distinguishes a stated absence (the source explicitly states the information does not apply or does not exist) from an unretrieved value (the information was not accessible at collection time), that distinction is preserved and never collapsed into a single generic "missing" state.

## 6. Quality Checks

- Every record is checked for structural completeness (required fields present, correct format) before being finalized as part of the dataset.
- A sample of each collection batch is independently re-checked against the original source for transcription fidelity.
- Batch-level counts (records collected vs. records declared) are reconciled at the close of each collection batch.

## 7. Version Control

- Every substantive document and dataset artefact governed by this guideline carries an explicit version number.
- A change to collection criteria, quality rules, or dataset structure is recorded as a new version with a dated revision-history entry; the previous version is retained, not overwritten.

## 8. Audit Trail

- Every data collection session is logged: date, scope, what was collected, and any deviation from the governing protocol.
- Every modification to a previously collected record is logged separately from the original observation.
- The audit trail is retained for the life of the dataset and is not summarized away.

## 9. Example Quality Rules

The following principles apply, without exception, to both datasets:

- Only publicly observable information may be recorded.
- Never infer missing information.
- Use controlled vocabularies whenever available.
- Maintain an audit trail for every modification.
- Never overwrite original observations.
- Record corrections as separate documented updates.
- Every data collection session must be logged.

## 10. Future Expansion

This section is reserved for additional quality rules identified as the dataset grows or as new data types are added.

*[Space reserved for future rules.]*

## 11. Version History

| Version | Date | Summary of Change | Author |
|---|---|---|---|
| 1.0 | 2026-08-02 | Initial draft of the data quality guidelines. | Samiksha Dhere |

---

*This document defines data quality principles only. It does not define or alter any software implementation, database schema, or ALCSM scoring methodology.*
