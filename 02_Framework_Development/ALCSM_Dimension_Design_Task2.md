# ALCSM Dimension Design (Task 2)
### AI Leadership Credential Scoring Model — Critical Evaluation of the Six Dimensions

Built on the 9-source literature base established in `Literature_Remapping_and_Annotations_v1.md`. No weights are assigned here (that's Task 3's job, and weighting *before* validation would itself be a methodological error — see the pushback in §0).

---

## 0. A structural objection before the dimensions

You've proposed six dimensions. Before I justify each one individually, I want to flag a conceptual risk in the set as a whole: **Dimensions 1 and 2 (Formal Education, Certifications) and Dimension 4 (Technical Contributions) are all still fundamentally *signals* in Spence's sense — proxies for unobservable competence.** Dimension 5 (Leadership) is a *different kind of construct* — it's closer to what Boyatzis and Steinbach et al. call demonstrated behavioral competency, which LinkedIn text can only capture indirectly (via titles, self-description, endorsements) rather than through direct observation of behavior. This means:

- Dimensions 1, 2, 4 can be scored with reasonably high construct validity from LinkedIn text (they are literally credentials/artifacts).
- Dimensions 5 and 6 are scoring *inferences about behavior* from *self-reported text*, which is a much weaker validity claim — LinkedIn is a self-presentation platform (impression management), not a performance record.

**Recommendation:** explicitly report this asymmetry in your validity discussion — don't let ALCSM imply all six dimensions have equal measurement validity, because they don't, and a psychometrically literate examiner (especially if they've seen Hinkin) will ask about this.

---

## 1. Dimension 1 — Formal Education

**Theoretical justification:** Spence (1973) treats formal education as the canonical costly signal — degree attainment separates types because it's differentially costly for low- vs. high-ability individuals to acquire. Ng et al. (2021) supplements this by giving formal AI/data-science education internal structure via the "know & understand" tier of their AI-literacy framework — i.e., a computer science or data science degree indicates foundational conceptual literacy, not necessarily applied or evaluative literacy.

**Supporting literature:** Spence (1973) [signal cost/separation]; Ng et al. (2021) [tiered literacy framework].

**Measurable indicators:**
- Degree type (CS/Data Science/AI/Statistics vs. adjacent vs. unrelated field)
- Degree level (Bachelor's/Master's/PhD)
- Institution tier (optional — methodologically fraught, see caution below)
- Explicit AI/ML coursework or specialization mentioned in profile "Education" section

**NLP extraction possibilities:**
- Named entity recognition (NER) on the LinkedIn "Education" block to extract degree, field, institution
- Keyword/ontology matching against a controlled vocabulary of AI-relevant degree titles (e.g., "Machine Learning," "Artificial Intelligence," "Data Science," "Computer Science," "Statistics," "Computational Linguistics")
- Fuzzy string matching to handle naming variance across universities/countries

**Scoring criteria (0–5, draft — not final weights):**
| Score | Criterion |
|---|---|
| 0 | No formal higher education listed, or field entirely unrelated to computing/data/AI |
| 1 | Bachelor's in an adjacent field (e.g., general business, engineering) with no AI/data coursework mentioned |
| 2 | Bachelor's in CS/quantitative field, no AI-specific specialization stated |
| 3 | Bachelor's with AI/ML specialization, OR Master's in adjacent field |
| 4 | Master's in AI/ML/Data Science, OR PhD in adjacent quantitative field |
| 5 | PhD in AI/ML/Computer Science with thesis/research explicitly in AI |

**Strong evidence example:** "M.Sc. Artificial Intelligence, University of Edinburgh" with thesis title mentioning a specific ML subfield.
**Weak evidence example:** "MBA, General Management" with a self-appointed "Chief AI Officer" title elsewhere in the profile — this is precisely the credential gap your thesis investigates.

**Caution (methodological, not just descriptive):** Scoring "institution tier" invites prestige bias and is not something signaling theory requires — Spence's argument is about the cost of the credential, not the school's ranking. I'd advise *against* including institution prestige as a scored indicator; it adds a validity threat (halo effect) without theoretical grounding in your own source base. Mention it only as a descriptive/control variable, not a scored ALCSM component.

---

## 2. Dimension 2 — Professional Certifications

**Theoretical justification:** Certifications are a *faster-cycle, lower-cost signal* than formal degrees (Spence's logic still applies, but with a shorter differential-cost horizon) — this makes them theoretically weaker signals individually, but Tadelis (2002) is relevant here too: certifications, especially recent and renewed ones, function like reputation-market entries that must be periodically "re-earned," giving them a dynamic-incentive quality static degrees lack.

**Supporting literature:** Spence (1973) [signal, weaker cost-differential]; Tadelis (2002) [dynamic/renewable reputational signal].

**Measurable indicators:**
- Presence/absence of vendor certifications (AWS/Azure/GCP ML certifications, TensorFlow Developer Certificate, etc.)
- Presence of applied professional certifications (PMP for AI project leadership, CDMP for data management)
- Recency (issued/renewed within last 2–3 years vs. expired or stale)
- Certifying body credibility (major cloud/tech vendor vs. unaccredited online course)

**NLP extraction possibilities:**
- Parse LinkedIn "Licenses & Certifications" section directly (structured field, high extraction reliability)
- Named entity matching against a curated certification taxonomy (build this list explicitly and cite your inclusion criteria — this taxonomy itself needs a documented, defensible construction method, e.g., drawing from your 200 job postings' most-requested certifications)
- Date-field parsing for recency scoring

**Scoring criteria (0–5, draft):**
| Score | Criterion |
|---|---|
| 0 | No certifications listed |
| 1 | One certification, expired or from unverified/low-credibility source |
| 2 | One current certification from a recognized vendor |
| 3 | Two+ current certifications from recognized vendors, general (not AI-specific) |
| 4 | Multiple current AI/ML-specific certifications from major vendors |
| 5 | Multiple current AI/ML-specific certifications plus a professional body credential (e.g., CDMP) actively maintained |

**Strong evidence example:** "AWS Certified Machine Learning – Specialty (issued 2025)" alongside "TensorFlow Developer Certificate (2024)."
**Weak evidence example:** A single "Introduction to AI" certificate from an unspecified MOOC listed without a completion date.

**Caution:** Certification taxonomies age quickly (vendor programs are renamed/retired constantly) — document your taxonomy's construction date and plan for revision; don't let this become a silent validity threat over your data-collection period.

---

## 3. Dimension 3 — Practical AI Experience

**Theoretical justification:** This dimension sits closest to revealed/demonstrated competence rather than credentialed signal — it's the dimension signaling theory says should matter most if markets were fully efficient (Spence's model predicts signal-value erodes when directly observable performance data exists). Cappelli, Tambe & Yakubovich (2018/19) is relevant here for a different reason: they warn that HR/AI data on "practical experience" is exactly the kind of complex, hard-to-verify phenomenon prone to noisy, non-causal proxies — a caution about over-trusting self-reported experience descriptions.

**Supporting literature:** Spence (1973) [signal vs. observable performance]; Cappelli, Tambe & Yakubovich (2018/19) [caution on complexity/verifiability of HR-relevant experience data].

**Measurable indicators:**
- Years in explicitly AI/ML-titled roles (Data Scientist, ML Engineer, AI Product Lead, etc.) vs. years in adjacent roles later re-labeled with AI titles
- Described project scope/ownership language (e.g., "led," "built," "deployed" vs. "involved in," "supported")
- Industry sector of AI application
- Team size/scope managed (if stated)

**NLP extraction possibilities:**
- Job title history parsing with role-title taxonomy classification (AI-core vs. AI-adjacent vs. non-AI)
- Verb-based responsibility extraction from role descriptions (dependency parsing to distinguish agentic verbs like "built/led/deployed" from passive/peripheral verbs like "assisted/participated")
- Duration calculation from date ranges in Experience entries
- **Important limitation to flag explicitly in your methodology:** self-reported responsibility language is a *stylistic/impression-management signal*, not verified performance data — NLP here measures how someone describes their experience, not their experience itself. This is a construct-validity limitation you should name, not hide.

**Scoring criteria (0–5, draft):**
| Score | Criterion |
|---|---|
| 0 | No AI/ML-related roles in employment history |
| 1 | AI-adjacent role only (e.g., general software engineer touching an ML product) |
| 2 | 1–2 years in an explicitly AI/ML-titled role, individual-contributor scope |
| 3 | 3+ years in AI/ML roles, or 1–2 years with clear ownership language |
| 4 | Multiple years across multiple AI/ML roles with demonstrated ownership/scope escalation |
| 5 | Sustained multi-year AI/ML leadership track record with explicit deployed-system ownership at scale |

**Strong evidence example:** "Led end-to-end deployment of a fraud-detection ML pipeline serving 2M+ daily transactions" (specific, agentic, scoped).
**Weak evidence example:** "Involved in various AI initiatives across the organization" (vague, passive, unscoped) — a textbook case of possible credential-gap language your thesis is designed to detect.

---

## 4. Dimension 4 — Technical Contributions

**Theoretical justification:** Tadelis (2002) is again directly relevant — visible technical output (publications, patents, open-source contributions, conference talks) functions as a continuously renewable reputational signal, distinct from a one-time credential. This dimension is your strongest *objectively verifiable* dimension because much of it can be cross-referenced against external records (GitHub, arXiv, patent databases) rather than relying solely on self-report.

**Supporting literature:** Tadelis (2002) [reputation as ongoing market signal]; secondarily Stark & Pais (2021) [algorithmic visibility/rankings as a form of reputational currency — relevant if you incorporate platform-based metrics like GitHub stars or citation counts].

**Measurable indicators:**
- Peer-reviewed publications in AI/ML venues
- Patents filed/granted in AI-related domains
- Open-source contributions (repositories, commit history, maintainer status)
- Conference speaking engagements (technical, not motivational/keynote-only)
- Technical blog posts/whitepapers with substantive content

**NLP extraction possibilities:**
- Named entity extraction for publication/patent mentions in "Featured" or "Publications" LinkedIn sections
- Optional external verification layer: cross-reference extracted names against Google Scholar/arXiv/USPTO APIs for corroboration (this would meaningfully strengthen construct validity — flag as a stretch goal for your Streamlit tool, not a v1.0 requirement given your timeline)
- GitHub username extraction (if linked) with API-based repo/contribution metadata pull

**Scoring criteria (0–5, draft):**
| Score | Criterion |
|---|---|
| 0 | No technical contributions of any kind mentioned or discoverable |
| 1 | Non-technical public content only (e.g., generic LinkedIn posts about AI trends) |
| 2 | One verifiable technical artifact (e.g., a single conference talk or blog post) |
| 3 | Multiple technical artifacts, unverified/self-reported only |
| 4 | Multiple technical artifacts with at least one externally verifiable (linked GitHub, indexed publication) |
| 5 | Sustained, externally verifiable technical output (multiple publications/patents/high-engagement open-source work) |

**Strong evidence example:** Linked GitHub profile with an actively maintained ML library (verifiable commit history) plus a co-authored paper indexed on arXiv.
**Weak evidence example:** "Thought leader in AI" self-description with no linked artifacts, publications, or repositories — unverifiable and exactly the pattern the credential-gap literature (Spence; Cappelli et al.) predicts markets will fail to sanction.

---

## 5. Dimension 5 — Leadership and Strategic Responsibility

**Theoretical justification:** This is the dimension I pushed back on in §0. Boyatzis (1982) gives you an empirically-derived competency-cluster model (linking observable managerial behaviors to effectiveness) — use this for *what kinds of behavioral indicators count as leadership competence*. Steinbach, Gamache & Johnson (2019) adds an important qualifier: executive effectiveness depends partly on cognitive flexibility (construal-level shifts) that is essentially invisible in LinkedIn text — meaning this dimension can only ever capture the *structural/positional* facet of leadership (title, scope, span of control), not the cognitive/behavioral facet Boyatzis and Steinbach et al. both center. Raisch & Krakowski (2021) adds the substantive content of *what* AI leaders should be strategically responsible for: navigating the automation-augmentation paradox rather than defaulting to one pole.

**Supporting literature:** Boyatzis (1982) [competency clusters]; Steinbach et al. (2019) [cognitive/behavioral facet, largely unobservable via text]; Raisch & Krakowski (2021) [substantive strategic content — automation/augmentation balance].

**Measurable indicators:**
- Title seniority (Head of/VP/Chief AI Officer/Director vs. Lead/Manager vs. individual contributor)
- Span of control (team size, budget, cross-functional scope, if stated)
- Explicit mention of strategic responsibilities (e.g., "responsible for enterprise AI strategy" vs. "responsible for model development")
- Language indicating balance of automation/augmentation framing (does the person's self-description show awareness of human-AI collaboration design, or purely technical/automation framing?)

**NLP extraction possibilities:**
- Title classification against a seniority taxonomy (rule-based or fine-tuned classifier)
- Dependency/keyword extraction for scope indicators ("team of X," "budget of $Y," "across N countries")
- Topic modeling or keyword-based framing detection distinguishing automation-only language from augmentation-aware language (this is a genuinely novel, thesis-specific NLP task — flag it as a contribution, but also flag it as unvalidated; you'd need manual annotation and inter-rater reliability testing before trusting classifier output here, per Hinkin's stages)

**Scoring criteria (0–5, draft):**
| Score | Criterion |
|---|---|
| 0 | Individual contributor, no leadership language |
| 1 | Team lead / informal leadership only, no strategic language |
| 2 | Manager-level title, team-scope leadership only |
| 3 | Director/Head-level title with some strategic-scope language |
| 4 | VP/senior leadership title with explicit enterprise-strategy responsibility |
| 5 | C-level/Chief AI Officer-equivalent title with explicit strategic AND augmentation-aware framing |

**Strong evidence example:** "As Chief AI Officer, I lead a cross-functional strategy balancing automation of routine claims processing with augmented decision support for senior underwriters" (title + scope + augmentation-aware framing).
**Weak evidence example:** "Chief AI Officer" title with a bio describing only personal coding projects and no strategic or organizational scope language — a canonical title-without-substance credential-gap case.

**Explicit limitation to disclose:** This dimension has the weakest construct validity of the six, because (a) titles are self-selected/company-specific and not standardized across organizations, and (b) the cognitive facet of leadership competence that Boyatzis and Steinbach et al. actually theorize about is not observable from static profile text at all. Say this directly in your thesis rather than let ALCSM imply Dimension 5 measures leadership competence with the same rigor as Dimension 2 measures certification possession.

---

## 6. Dimension 6 — Professional Engagement and Continuous Development

**Theoretical justification:** Tadelis (2002) is your primary anchor — this dimension operationalizes his "ageless incentive" logic: continuous, updated professional activity as an ongoing reputational signal rather than a one-off credential. Ng et al. (2021)'s "use & apply" and "evaluate & create" literacy tiers also map here, distinguishing passive AI awareness from active, evaluative engagement (e.g., critically discussing AI ethics/limitations vs. just sharing news links).

**Supporting literature:** Tadelis (2002) [dynamic reputational signal]; Ng et al. (2021) [active/evaluative literacy tiers].

**Measurable indicators:**
- Recency and frequency of AI-related posts/articles
- Participation in professional AI communities/associations
- Continuing education (recent courses, workshops, conference attendance as *attendee*, not just speaker — that's Dimension 4)
- Engagement quality (original analysis/critique vs. passive resharing)

**NLP extraction possibilities:**
- Post-frequency and recency analysis (if post history is accessible/scraped within LinkedIn's terms of use — **flag now for your ethics chapter**: scraping post-level activity data raises different GDPR/ToS questions than scraping static profile fields, and needs its own justification)
- Sentiment/stance classification distinguishing original commentary from passive shares
- Topic modeling to assess whether engagement content demonstrates evaluative depth (Ng et al.'s "evaluate & create" tier) vs. surface-level awareness ("know & understand" tier only)

**Scoring criteria (0–5, draft):**
| Score | Criterion |
|---|---|
| 0 | No visible AI-related professional engagement |
| 1 | Occasional passive engagement (likes/shares only) |
| 2 | Regular passive engagement, no original content |
| 3 | Occasional original commentary/posts on AI topics |
| 4 | Regular original, substantive commentary; community/association membership |
| 5 | Sustained thought leadership: regular original critical commentary, active community leadership role, demonstrable continuing education |

**Strong evidence example:** Monthly original posts critically analyzing AI governance developments, plus active membership/leadership in a recognized professional AI association.
**Weak evidence example:** Profile shows zero activity beyond the static profile fields — common, and not in itself damning, but scored low per the rubric's logic.

**Caution:** This is the dimension most vulnerable to **platform-usage confounds** unrelated to actual competence — some highly competent AI leaders simply don't post on LinkedIn, while some less-credentialed people post prolifically. Flag this explicitly as a threat to validity (systematic measurement bias favoring extroverted self-promoters), not just a footnote.

---

## 7. Summary table (no weights — Task 3 will formalize scoring math)

| Dimension | Primary theory | Data verifiability | Key named limitation |
|---|---|---|---|
| 1. Formal Education | Spence (1973); Ng et al. (2021) | High (structured field) | Institution-prestige bias risk if scored |
| 2. Certifications | Spence (1973); Tadelis (2002) | High (structured field) | Taxonomy decays quickly, needs versioning |
| 3. Practical AI Experience | Spence (1973); Cappelli et al. | Medium (self-report language) | Measures self-presentation, not verified performance |
| 4. Technical Contributions | Tadelis (2002); Stark & Pais (2021) | Medium–High (externally verifiable subset exists) | Full verification (GitHub/Scholar API) is a stretch goal, not v1.0 baseline |
| 5. Leadership & Strategic Responsibility | Boyatzis (1982); Steinbach et al. (2019); Raisch & Krakowski (2021) | Low (title/scope proxies only) | Cannot capture the cognitive/behavioral facet theory says matters most |
| 6. Professional Engagement | Tadelis (2002); Ng et al. (2021) | Low–Medium (platform-usage confound) | Penalizes low-visibility competence, rewards self-promotion |

This verifiability gradient (High → Low) is itself a finding worth stating up front in your Methodology: **ALCSM's six dimensions are not equally measurable from LinkedIn text, and your validation strategy (Task 3/Hinkin-based) should report separate reliability statistics per dimension rather than one pooled inter-rater reliability figure**, since pooling would mask the fact that Dimensions 1–2 will likely show much higher inter-rater agreement than Dimensions 5–6.

---

## Next step

Ready for **Task 3** (ALCSM v1.0 scoring framework: scoring table, mathematical formula without final weights, annotation guidelines, profile classification examples) whenever you want to proceed — say the word and I'll build it directly from the six dimension definitions above.
