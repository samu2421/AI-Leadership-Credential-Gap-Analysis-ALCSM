# ALCSM Legitimate Interests Assessment (Draft)
### Legal basis for the LinkedIn profile-audit strand (Art 6(1)(f) GDPR)

**Version:** 0.1-DRAFT
**Status:** Draft — the researcher's own reasoning, prepared for supervisor/DPO review. Not yet confirmed as an adequate basis by the DPO.
**Purpose:** work through the purpose, necessity, and balancing tests that justify relying on legitimate interests, rather than consent, for the LinkedIn profile-audit strand.
**Last Updated:** 2026-07-30
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance
**Applies to:** the LinkedIn profile-audit strand only. The expert-survey strand relies on consent (Art 6(1)(a)) instead — see `05_Consent_Materials/`.

---

## 1. Purpose test — is there a legitimate interest?

**Question:** does the processing pursue a real, specific, present, and lawful interest?

Yes. The interest is a scientific-research interest recognised under Art 89 GDPR and the corresponding German BDSG research provisions: producing reproducible, population-level evidence about the relationship between publicly presented AI-leadership credentials and stated job requirements. This is a real academic interest (an MSc thesis with defined research questions, RQ1–RQ5), specific (not a vague "improve our understanding" interest), present (the research is actively underway), and lawful (auditing publicly presented information is not itself prohibited; the method chosen specifically avoids the ToS/legal exposure that automated collection would create — see the LinkedIn Collection Protocol).

**Conclusion:** the purpose test is satisfied.

## 2. Necessity test — is the processing necessary for that purpose?

**Question:** is this processing, at this scale, actually needed to achieve the purpose, or would a less-intrusive approach do?

- The research question is specifically about *what people publicly present*, not what they privately believe or would self-report — so processing publicly presented profile content is intrinsic to the question, not an incidental convenience.
- A smaller sample would reduce statistical power for the population-level and RQ4 correlation analyses; ~500 is a bounded, pragmatic target chosen for manual tractability, not the maximum the researcher could gather.
- Alternative approaches (e.g. surveying self-identified AI leaders about their own credentials) would not answer the *presented-signal* question and would introduce the exact self-report inflation risk the study exists to detect.
- Data minimisation is actively practised: no direct identifier is collected; no special-category data is collected; only ALCSM-relevant fields and a small set of independently justified RQ4 indicators are recorded.

**Conclusion:** the necessity test is satisfied — the processing, at approximately this scale and scope, is required to answer the research question; broader collection (e.g. private/connection-gated content, or automated scraping for a much larger sample) is neither used nor necessary.

## 3. Balancing test — do the data subjects' interests override the legitimate interest?

**Question:** does the impact on the individuals whose data is processed outweigh the researcher's legitimate interest?

**Factors favouring the research interest:**
- The data is already public, presented by the individual specifically for professional/public visibility (a LinkedIn profile is, by its nature, intended to be seen by third parties evaluating professional credentials — which is close to, though not identical to, the purpose of this study).
- No individual-level output is ever published; only aggregate, population-level findings.
- Direct identifiers are excluded by design and enforced technically.
- The study explicitly frames its measurement as *signal*, never *competence*, precisely to avoid overstating what is being claimed about any individual.
- A public privacy notice provides transparency in place of infeasible individual notification (the "make the information publicly available" Art 14(5)(b) safeguard).

**Factors favouring the data subjects' interests:**
- Individuals have not been asked and have not had the opportunity to object before processing begins (mitigated, not eliminated, by the public notice and the ability to object under Art 21 after the fact).
- A "credential-gap" finding, if ever mistakenly attributed to a named individual, could cause professional reputational harm — this is the study's principal risk (see the DPIA).
- Some profile subjects may reasonably expect their content to be seen by recruiters and peers, but may not expect systematic, structured *scoring* of their credentials for a research study — this is a real gap between ordinary expectation and this specific use, and is not fully resolved by "the data was already public."

**Balancing conclusion (researcher's provisional view, for DPO confirmation):** the legitimate interest in producing transparent, reproducible research evidence — combined with pseudonymisation, aggregate-only reporting, technical exclusion of direct identifiers, and public transparency via the privacy notice — outweighs the residual impact on data subjects, **provided** the mitigations in the DPIA (Part D) are actually implemented and the public notice is genuinely published before or at the start of collection. This conclusion is not final until the DPO has reviewed and, if necessary, revised it.

## 4. Data-subject rights under this legal basis

Under Art 6(1)(f) processing, data subjects retain the rights of access, rectification, erasure, restriction, and — significantly — the **right to object (Art 21)** at any time, on grounds relating to their particular situation, without needing to justify the objection further. The privacy notice states how to exercise these rights and whom to contact. Because profiles are pseudonymised at capture, locating one specific person's record to honour a request may be genuinely difficult; this is disclosed honestly in the Data Management Plan rather than treated as a solved problem.

## 5. Outcome

| Field | Value |
|---|---|
| Purpose test | Satisfied |
| Necessity test | Satisfied |
| Balancing test | Favours the legitimate interest, subject to DPIA mitigations being implemented — **pending DPO confirmation** |
| DPO reviewed | `[INSERT: yes/no, date]` |
| DPO conclusion | `[INSERT]` |

---

*This LIA operationalises `05_Data_Collection/Documentation/Task5_PreCollection_Roadmap.md` §3.3. No frozen ALCSM methodology or database element is altered by this document.*
