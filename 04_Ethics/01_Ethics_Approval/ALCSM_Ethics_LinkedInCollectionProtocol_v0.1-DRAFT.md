# ALCSM LinkedIn Profile Collection Protocol (Draft)
### Annex A to the Ethics Application

**Version:** 0.1-DRAFT
**Status:** Draft — not yet approved. Collection may not begin under this protocol until ethics approval, GDPR/DPIA sign-off, and supervisor sign-off on method are all obtained (see `Implementation_Phase_Roadmap.md` §7, Phase P2 exit criteria).
**Purpose:** specify exactly how LinkedIn profile data is collected, so the ethics committee and DPO can assess the method itself, not just its outcome.
**Last Updated:** 2026-07-30
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance
**Related documents:** `ALCSM_Ethics_ApplicationDraft_v0.1-DRAFT.md`, `ALCSM_Ethics_LIA_v0.1-DRAFT.md`, `ALCSM_Ethics_DataManagementPlan_v0.1-DRAFT.md`, `05_Data_Collection/Documentation/Task5_LinkedIn_Collection_Workflow.md` (the operational, step-by-step SOP this protocol summarises for committee review)

---

## 1. Collection method — and why

**Method: manual, human-driven collection. No scraping, no browser automation, no automated retrieval of any kind.**

This is not a default or a convenience choice. Automated collection of LinkedIn data breaches LinkedIn's User Agreement — a real, adjudicated legal exposure (the *hiQ Labs v. LinkedIn* litigation ultimately found in LinkedIn's favour on the breach-of-contract claim, notwithstanding the earlier, narrower ruling on public-data access under US computer-misuse law). A human reading each public profile and transcribing the relevant fields by hand avoids the "automated means" exposure entirely, and keeps the collected volume proportionate to what a single researcher can review and validate. The 500-profile sample size is set at a level that is manually tractable within a defined collection window — it is a consequence of the method, not a compromise imposed on it.

## 2. Scope: public data only

Collection accesses only what a member of the public can see without any special access, and uses no technical means beyond a standard web browser operated by a human. This section states each boundary explicitly, since a protocol a DPO cannot verify point-by-point is a weaker protocol.

- **Public-profile-only collection.** Only content visible on a profile's public-facing page is transcribed. If a field, section, or detail is not shown on that public page, it is not collected — not approximated, not inferred, not obtained by any other means.
- **Logged-in vs. logged-out browsing policy.** The default and preferred mode is **logged-out browsing** — viewing profiles with no LinkedIn account session active, so that what the collector sees is, by construction, exactly what LinkedIn itself classifies as publicly visible. Where LinkedIn's own access limits make sustained logged-out browsing impractical (e.g. rate-limiting or a sign-in prompt after a small number of anonymous views — a real, foreseeable operational constraint, not a hypothetical one), browsing may fall back to a **personal, logged-in account**, but only under two further restrictions that are followed even then: (a) the collector transcribes only what that same public-facing page layout displays — never a connection-, network-, or premium-tier view that reveals more than a logged-out visitor would see; (b) no LinkedIn feature that depends on being logged in (e.g. "who's viewed your profile," extended network visibility, InMail, connection requests) is used to locate, access, or corroborate any profile content. **[INSERT: confirm this fallback position with the DPO/supervisor before collection begins — if the institution prefers logged-out-only with no fallback, that stricter position should be adopted instead, at the cost of a slower collection rate.]**
- **No scraping.** No automated extraction of page content (e.g. parsing HTML/DOM programmatically) is performed at any point.
- **No browser automation.** No headless browser, scripted navigation, or tool that drives a browser programmatically (e.g. Selenium, Playwright, or similar) is used. Every page view and every transcription is a human action.
- **No automated retrieval of any kind.** No scheduled jobs, bots, or bulk-download mechanisms are used to fetch profile pages.
- **No API usage.** LinkedIn's official APIs (or any third-party API purporting to provide LinkedIn data) are not used to obtain profile content. All content is read by a human directly from the standard public web page.
- **No circumvention of privacy settings.** No technique is used to access content a profile owner has restricted from public view — this includes not attempting to view connection-only content via a second-degree connection, not using a fake or pretextual connection request to gain access, and not using any browser extension or tool designed to reveal hidden/restricted profile fields.
- **No collection of non-public profile information.** Only the seven fixed sections defined in §5 are transcribed, and only their publicly visible content; no attempt is made to derive, guess, or reconstruct information the profile owner has not made public.
- **No screenshots or identifying artefacts retained.** No screenshots, page saves, cached copies, or copies of any identifying element (photo, profile URL) are retained at any point — only the text content of the defined profile sections is transcribed by hand into the research database.

These are documentation clarifications of the collection method already approved in principle (manual, human-driven, public-only); none of them changes what that method is.

## 3. Sampling frame and inclusion/exclusion criteria

- **Target population:** individuals who *publicly present* a qualifying AI-leadership title on LinkedIn (e.g. "Chief AI Officer," "Head of AI," "VP of AI/ML," "Director of AI," "AI Lead" — exact pre-registered title list: **[INSERT: final title list]**). This is explicitly narrower than "all AI leaders"; the gap between the two is a disclosed limitation, not a hidden one.
- **Include:** profile publicly presents a qualifying title from the pre-registered list; publicly viewable; within the fixed language scope (**[INSERT: language scope, e.g. English-language profiles]**).
- **Exclude (logged with reason):** duplicate of an already-captured individual; not publicly viewable; title outside the pre-registered list; language out of scope; a company or non-person page.
- **Query design:** exact query strings, platform surface, filters, and per-query quotas are fixed and pre-registered before collection begins, and held constant across the collection window (**[INSERT: collection window dates]**). Search-result order is worked through as returned — results are not re-ordered or cherry-picked, since the algorithmic-ranking bias this introduces is a disclosed limitation, not something to "correct" by hand-picking.

## 4. Pseudonymisation at the point of capture

Every included profile is assigned a pseudonymous identifier (`PRF-#####`) at the moment of capture. From that point forward, the record is referred to only by that identifier. **The collection tooling technically rejects any record carrying a name, profile URL, photograph, email address, or phone number** — this is enforced in software, not left to transcription discipline alone.

## 5. What is transcribed

For each of seven fixed profile sections (headline, about, experience, education, certifications, contributions, activity), two things are recorded: whether the section was retrievable at all, and — only if it was — its verbatim text. A section that was not retrievable is recorded as such and carries no text; this distinction (empty/absent vs. not retrieved) is preserved explicitly rather than being collapsed into an ambiguous blank, because the scoring framework treats "the person states they have none" and "no information was available" as different, non-interchangeable findings.

Post-level activity content is transcribed only where the study's activity-collection flag is explicitly set for that record, because ongoing-activity data carries its own, separate ethics consideration beyond static profile content. Where RQ4 impact indicators (reach, engagement, recognition, career-progression signal) are captured, they are recorded into a physically separate part of the research database from the credential scores, and are never shown to the human coders who later score the profile.

**Incidental special-category content** (e.g. a profile that happens to reveal a political affiliation or a health-related advocacy role) is never transcribed, regardless of context — this content is not needed by the scoring framework and is excluded outright.

## 6. Deduplication

Before a candidate profile is captured, the collector confirms the individual is not already represented in the sample, using a transient, session-local check that is discarded at the end of the session and never persisted into the research database (since the database itself stores no name or other discriminator that would make a persistent duplicate-check index possible or desirable).

## 7. Collection window and audit log

Collection runs within a fixed window (**[INSERT: dates]**), with query definitions held constant throughout. A running collection log — held in the secure store, never in the code repository and never in the research database — records: session date, queries run, results returned vs. included, every exclusion and its reason, and any anomaly or deviation from this protocol. This log is the audit trail referenced in the Methods chapter and in the Data Management Plan.

## 8. Data storage during and after collection

All data is entered directly into the project's access-controlled, EEA-resident database (see the Data Management Plan for the specific storage arrangement). No profile data is stored on a personal laptop, in consumer cloud storage, or anywhere outside the approved environment, at any point, even temporarily.

## 9. Re-identification mapping

This protocol assumes **no persistent mapping** is kept between a pseudonym and the real individual once capture is complete, consistent with the Data Management Plan's recommended default (§4.1 of that plan). If a temporary mapping is used for within-session deduplication or quality review, it is destroyed before the collection session ends and is never written to the research database. **[INSERT: confirm final decision with DPO before collection begins]**.

## 10. What this protocol does not cover

Scoring/annotation of collected profiles is a separate stage governed by the frozen ALCSM coding rulebook and annotation handbook, not by this protocol. This protocol covers collection only — up to and including validated, atomic insertion of a profile record into the research database.

---

*This protocol summarises, for committee review, the fully detailed operational SOP already written and partially execution-tested against the frozen schema: `05_Data_Collection/Documentation/Task5_LinkedIn_Collection_Workflow.md`. Nothing in this protocol changes the frozen ALCSM methodology or the frozen database schema.*
