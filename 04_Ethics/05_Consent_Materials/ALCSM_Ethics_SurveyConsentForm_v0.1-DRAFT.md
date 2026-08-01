# Informed Consent Form — Expert Validation Survey (Draft)
### The AI Leadership Credential Gap Study

**Version:** 0.1-DRAFT — must match the version/date referenced in `ALCSM_Ethics_SurveyInfoSheet_v0.1-DRAFT.md`.
**Status:** Draft — not yet used with any real respondent.
**Purpose:** record a survey respondent's informed consent before any of their responses are entered into the research database.
**Last Updated:** 2026-07-30
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance

---

Please confirm each statement before proceeding. *(The research database records consent as a single confirmed state; a respondent who does not confirm every statement cannot enter the dataset — this is enforced by the frozen schema's `survey_respondent` table, which requires `consent_confirmed = TRUE`.)*

- [ ] I have read and understood the Participant Information Sheet (version 0.1-DRAFT, dated `[INSERT]`).
- [ ] I understand my participation is voluntary and I may stop at any time before submitting.
- [ ] I understand my responses are pseudonymous and will be reported only in aggregate.
- [ ] I understand that withdrawal after submission may not be possible once my responses have been aggregated with others.
- [ ] I consent to my pseudonymous responses being used for this research, the resulting thesis, and any subsequent academic publication.

**[ ] I consent and wish to proceed.**

*Date and time of consent are recorded automatically by the survey system at the moment of confirmation (`consent_ts`); no further signature is required for the digital version of this form. If a paper version is ever used instead, a handwritten signature and date should be added here: `[INSERT: signature line, if applicable]`.*

---

## Schema alignment note (for the research team, not the respondent)

This form's five confirmations map directly onto the frozen `survey_respondent` table's `consent_confirmed`, `consent_ts`, and `withdrawal_flag` fields, with no schema change required. A respondent's `withdrawal_flag` is set if they later exercise the right to object described in the information sheet, to the extent withdrawal remains possible post-aggregation.

---

*Source: this document formalises the ready-to-adapt draft in `05_Data_Collection/Documentation/Task5_PreCollection_Roadmap.md` §2.3.*
