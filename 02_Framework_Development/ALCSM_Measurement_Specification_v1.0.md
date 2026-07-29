# ALCSM Measurement Specification v1.0
### Final Pre-Implementation Blueprint

**Thesis:** *The AI Leadership Credential Gap: An NLP Audit of 500 LinkedIn Profiles*
**Status:** Conceptual model frozen. Implementation parameters (aggregation function, weights, classification thresholds) intentionally open pending empirical validation.
**Purpose:** This document is the definitive, version-controlled reference for all remaining thesis stages (Tasks 4–6 and beyond). It consolidates prior deliverables without introducing new dimensions or altering the conceptual model.

**Prior deliverables consolidated here:**
- `Literature_Remapping_and_Annotations_v1.md`
- `ALCSM_Dimension_Design_Task2.md`
- `ALCSM_Coding_Rulebook_and_Pilot_Design.md`
- `ALCSM_v1.0_Scoring_Framework_Task3.md`

**Notation convention (retained throughout):** **[ESTABLISHED]** = grounded in cited published methodology; **[THESIS-SPECIFIC]** = a project design decision that you must own and defend, not a literature mandate; **[FROZEN]** = fixed before implementation; **[OPEN]** = deliberately unresolved until empirical validation.

**Integrity note on constructed content:** All taxonomies (§2), worked examples (§3), and precedent cases (§4) are *design artifacts*, not empirical findings. The example profiles are fully constructed composites — not real individuals, not drawn from your eventual dataset. None of this content should ever be cited in the thesis as data or as evidence about real AI leaders.

---

## 1. Definitive Six-Dimension Reference Table

The conceptual model is **[FROZEN]**. The six dimensions, their theoretical anchors, and their 0–5 criteria are restated below as the single authoritative reference. (Criteria unchanged from Task 2/Task 3.)

| # | Dimension | Primary theoretical anchor(s) | Verifiability from LinkedIn text | Core construct measured |
|---|---|---|---|---|
| D1 | Formal Education | Spence (1973); Ng et al. (2021) | **High** (structured field) | Credentialed foundational AI/quantitative literacy |
| D2 | Professional Certifications | Spence (1973); Tadelis (2002) | **High** (structured field) | Renewable, lower-cost competence signals |
| D3 | Practical AI Experience | Spence (1973); Cappelli, Tambe & Yakubovich (2018/19) | **Medium** (self-report language) | Self-described applied AI/ML role history |
| D4 | Technical Contributions | Tadelis (2002); Stark & Pais (2021) | **Medium–High** (subset externally verifiable) | Visible, partly verifiable technical output |
| D5 | Leadership & Strategic Responsibility | Boyatzis (1982); Steinbach et al. (2019); Raisch & Krakowski (2021) | **Low** (title/scope proxy only) | Positional + strategic-framing leadership signal |
| D6 | Professional Engagement & Continuous Development | Tadelis (2002); Ng et al. (2021) | **Low–Medium** (platform-usage confound) | Ongoing reputational/engagement activity |

**Full 0–5 scoring criteria:** see the consolidated scoring table in `ALCSM_v1.0_Scoring_Framework_Task3.md` §1. That table is incorporated here by reference and is **[FROZEN]** at v1.0.

**Standing caveat (carried forward, [FROZEN] as a reporting requirement):** the six dimensions do **not** have equal measurement validity. Any composite score, coding interface, or NLP output must preserve the dimension-level breakdown and the verifiability gradient above; per-dimension reliability must be reported separately, never pooled into a single figure.

---

## 2. Frozen Taxonomies (Reproducibility Layer)

**[THESIS-SPECIFIC] — critical framing before you use any of these.** These taxonomies are **your design artifacts**. I have constructed them to be reasonable and internally consistent, but I did *not* derive them from an external authoritative standard, and no such single standard exists for "AI leadership credentials." Therefore:

- Each taxonomy below is **[FROZEN] for v1.0 reproducibility** — meaning: once you begin annotation, you do not silently change it; changes go through the Task 2 revision-log procedure.
- But "frozen" does **not** mean "externally validated." You must state in your Methods chapter that these taxonomies are researcher-constructed, give the construction rationale, and (strongly recommended) triangulate at least the certification and role taxonomies against the actual vocabulary observed in your 200 job postings, so they are not purely a priori. **[THESIS-SPECIFIC recommendation]**
- Every taxonomy carries a **construction date** and a **version number**. Vendor certifications and role titles drift; a taxonomy frozen in month X may misclassify a profile written in month X+12.

### 2.1 Degree taxonomy (D1)

Version 1.0. Classifies the *field* and *level* of the highest relevant degree.

**Field tiers:**
- **Tier A — AI-core:** Artificial Intelligence, Machine Learning, Deep Learning, Computational Linguistics / NLP, Computer Vision, Data Science (where AI/ML is explicit).
- **Tier B — AI-adjacent quantitative:** Computer Science (general), Statistics, Applied Mathematics, Computational/Quantitative fields, Electrical/Computer Engineering, Operations Research, Physics.
- **Tier C — Adjacent professional/analytical:** Information Systems, general Engineering, Economics, Business Analytics, Cognitive Science, Bioinformatics.
- **Tier D — Unrelated:** all other fields (general business/MBA without analytics specialization, humanities, unrelated sciences).

**Level:** Bachelor's < Master's < Doctorate.

**Mapping to D1 score (deterministic where possible):**
| Highest degree | Score |
|---|---|
| No higher education, or Tier D only | 0 |
| Tier C Bachelor's, no AI coursework stated | 1 |
| Tier B Bachelor's, no AI specialization stated | 2 |
| Tier A Bachelor's, OR Tier B/C Master's | 3 |
| Tier A Master's, OR Tier B Doctorate | 4 |
| Tier A Doctorate with AI-specific research/thesis | 5 |

**Frozen decision:** institution prestige is **excluded** from scoring (halo-bias risk, no theoretical grounding in Spence's cost-of-signal logic). It may be retained only as a descriptive control variable. **[FROZEN]**

### 2.2 Certification taxonomy (D2)

Version 1.0, construction date to be stamped at freeze. Certifications are classified by **type**, **AI-specificity**, **issuer credibility**, and **currency**.

- **Issuer credibility — High:** major cloud/tech vendors (AWS, Microsoft Azure, Google Cloud, IBM, NVIDIA), recognized professional bodies (e.g., DAMA/CDMP, PMI/PMP), accredited universities (verified certificate programs).
- **Issuer credibility — Low/Unverified:** unbranded MOOCs, unaccredited online courses, self-issued or platform-completion badges without assessment.
- **AI-specificity — AI/ML-specific:** e.g., AWS Certified Machine Learning – Specialty, TensorFlow Developer Certificate, Azure AI Engineer Associate, NVIDIA Deep Learning Institute certifications.
- **AI-specificity — General/adjacent:** general cloud, general data/analytics, general project management.
- **Currency:** current (issued/renewed within the last 3 years, or no expiry) vs. expired/stale.

**[THESIS-SPECIFIC, strongly recommended]** Seed this taxonomy's concrete certification list from the certifications actually named in your 200 job postings, plus the most common ones appearing in your profile sample during the pilot, rather than from memory. Document the seed list and its date. This makes the taxonomy empirically anchored rather than arbitrary, and directly supports Contribution 2's job-vs-profile comparison.

### 2.3 AI role taxonomy (D3)

Version 1.0. Classifies each employment-history role into one of three bands, plus a responsibility-language layer.

- **AI-core roles:** Machine Learning Engineer, Data Scientist (with ML/AI content), AI/ML Research Scientist, AI Product Manager/Lead, NLP/CV Engineer, MLOps Engineer, AI Engineer.
- **AI-adjacent roles:** Data Analyst, Software Engineer (general), Data Engineer, BI Developer, general Product Manager touching an AI product.
- **Non-AI roles:** everything else.

**Responsibility-language layer [THESIS-SPECIFIC]:** within role descriptions, distinguish:
- **Agentic/ownership verbs:** built, led, designed, architected, deployed, owned, delivered, scaled.
- **Peripheral/passive verbs:** involved in, supported, assisted, participated, contributed to, exposed to.

**[FROZEN] caution:** the responsibility-language layer measures *how experience is described*, not the experience itself. This is a self-presentation signal and must be reported as such. NLP extraction here (dependency parsing for verb–subject relations) must be validated in the pilot before trust.

### 2.4 Leadership-level taxonomy (D5)

Version 1.0. Two components: **positional seniority** and **strategic-scope language**.

**Positional seniority tiers (from title):**
- **Tier 5 — C-suite/executive:** Chief AI Officer, Chief Data Officer, Chief AI/ML Scientist, EVP/SVP of AI.
- **Tier 4 — Senior leadership:** VP of AI/Data/ML, Head of AI (enterprise-level).
- **Tier 3 — Middle leadership:** Director of AI/Data Science, Head of (team-level), Senior Manager.
- **Tier 2 — First-line management:** Manager, Team Lead (formal).
- **Tier 1 — Informal/none:** Lead (IC senior), Principal (IC), no leadership title.

**Strategic-scope language layer:**
- **Strategic:** enterprise AI strategy, org-level roadmap, budget ownership, cross-functional mandate, governance responsibility.
- **Operational only:** team management, project delivery, model development leadership without org-level strategy.
- **Augmentation-aware (thesis-native signal):** explicit language about human–AI collaboration design, automation/augmentation balance (per Raisch & Krakowski, 2021).

**[FROZEN] caution — the single most important construct-validity flag in the whole model:** titles are self-assigned and company-specific; the cognitive/behavioral facet of leadership that Boyatzis and Steinbach et al. actually theorize is **not observable** from static profile text. D5 measures a positional/rhetorical proxy, not demonstrated leadership competence. This must be stated plainly wherever D5 results appear.

### 2.5 Technical contribution taxonomy (D4)

Version 1.0. Classifies technical output by **type** and **verifiability**.

- **Verifiable-external:** peer-reviewed publications (indexable on Scholar/arXiv/DBLP), granted/filed patents (patent-office searchable), public open-source repositories with real commit history (GitHub/GitLab), indexed conference talks.
- **Self-reported-only:** claimed publications/talks/projects with no link or external index; "featured" items without verifiable substance.
- **Non-technical public content:** generic thought-leadership posts, reshared news, opinion pieces without technical substance.

**[FROZEN] verification rule (from rulebook §1.4):** external verification is permitted **only** for D4, and only via links the profile itself provides or standard public indices; verification may confirm or *lower* a score (on discovered contradiction) but must not *inflate* a score beyond what the profile text supports, because the automated pipeline cannot see beyond the profile. This keeps human "gold standard" and machine scores measuring the same construct.

### 2.6 Professional engagement taxonomy (D6)

Version 1.0. Classifies engagement by **modality** and **depth**.

- **Passive:** likes, shares, reshares without commentary.
- **Active-surface:** original posts at the "know/understand" tier (Ng et al., 2021) — news summaries, announcements, generic commentary.
- **Active-evaluative:** original posts at the "evaluate/create" tier — critical analysis, methodological/ethical critique, original technical writing.
- **Community role:** membership vs. leadership/organizing role in recognized professional AI communities/associations.
- **Continuing education:** recent courses/workshops/conference attendance (as attendee — speaking is D4, not D6).

**[FROZEN] caution:** D6 is confounded by platform-usage propensity. Highly competent leaders who don't post will score low; prolific self-promoters will score high. This is a systematic measurement bias favoring visible self-promoters, not a neutral measure of development. Report as a named limitation.

**[FROZEN] ethics flag:** post-level activity data (frequency, history) raises different GDPR/ToS questions than static profile fields and must be justified separately in the ethics documentation (Task 5).

### 2.7 AI keyword ontology (cross-cutting extraction aid)

Version 1.0. A controlled vocabulary used across D1–D6 for NLP extraction. **[THESIS-SPECIFIC]** — this is an extraction aid, not a scoring rule; presence of a keyword never *by itself* sets a score.

- **Core AI/ML:** artificial intelligence, machine learning, deep learning, neural network, transformer, LLM, foundation model, reinforcement learning, supervised/unsupervised learning.
- **Subfields:** NLP, natural language processing, computer vision, speech recognition, recommender systems, generative AI, MLOps.
- **Methods/tools:** TensorFlow, PyTorch, scikit-learn, Hugging Face, XGBoost, model deployment, feature engineering, model training, fine-tuning.
- **Data/infra (adjacent):** data pipeline, ETL, data engineering, cloud ML, model serving, vector database.

**[FROZEN] rule:** the ontology is used to *locate* evidence, after which the scoring criteria (§1) are applied by judgment. Keyword-counting is explicitly **not** a scoring method (it would reward keyword-stuffing — a credential-inflation vector the thesis is trying to detect, not reward).

### 2.8 Automation vs. augmentation keyword lists (D5 strategic-scope, thesis-native)

Version 1.0. Supports the augmentation-aware sub-signal in D5, grounded in Raisch & Krakowski (2021).

- **Automation-leaning language:** automate, replace, eliminate manual work, reduce headcount, straight-through processing, full automation, remove human intervention.
- **Augmentation-leaning language:** augment, assist, human-in-the-loop, decision support, collaboration between humans and AI, empower teams, human oversight, complement human judgment.

**[FROZEN] caution — do not overclaim this signal.** Detecting augmentation-aware language is a novel, thesis-specific NLP task with **no validated classifier behind it yet**. In the pilot it must be manually annotated and reliability-tested before any automated detection is trusted. Presence of augmentation vocabulary indicates *rhetoric*, not demonstrated capability — a CAIO can write "human-in-the-loop" without practising it. Treat as an exploratory secondary signal, not a core scored criterion, until validated.

---

## 3. Expanded Annotation Manual — 18 Worked Example Profiles

**Integrity disclaimer (repeated because it matters):** all 18 profiles below are **fully constructed composites for annotator training only.** They are not real, not from your dataset, and must never appear in the thesis as data. Evidence excerpts are invented illustrative text. Scores use the frozen §1 criteria and §2 taxonomies. Aggregation is deliberately **not** computed here (aggregation function is [OPEN]); only the six raw scores plus flags are given.

Flag legend: `M` = missing (no evidence), `A` = ambiguous, `C` = contradiction. Scores are integers 0–5. "Default-low" refers to rulebook Principle 4.

---

**Example 01 — Clear high (substantiated senior leader)**
Excerpts: *"PhD, Machine Learning, Carnegie Mellon (thesis on graph neural networks)"; "VP of AI, leading enterprise AI strategy across 4 business units, $12M budget"; "AWS ML Specialty (2025), Azure AI Engineer (2024)"; "12 publications (Google Scholar linked)"; "monthly posts analysing AI governance."*
Scores: D1=5, D2=4, D3=4, D4=5, D5=4, D6=4. Flags: none. Handling: straightforward; all dimensions well-evidenced.

**Example 02 — Clear low (minimal credentials)**
Excerpts: *"BA Marketing"; "Social Media Coordinator"; no certifications; no technical output; occasional reshares of AI news."*
Scores: D1=0, D2=0, D3=0, D4=1, D5=0, D6=1. Flags: `M` on D2, D3. Handling: score 0 where no evidence; D4=1 for non-technical reshared content.

**Example 03 — Clear mid (solid IC data scientist)**
Excerpts: *"MSc Data Science"; "Data Scientist, 3 yrs, built and deployed churn model"; "Google Cloud ML Engineer cert (2024)"; "public GitHub with 2 small ML repos"; "Data Scientist title, no management language"; "shares others' articles occasionally."*
Scores: D1=4, D2=2, D3=3, D4=3, D5=0, D6=1. Flags: none. Handling: agentic verbs ("built, deployed") support D3=3; no leadership language → D5=0.

**Example 04 — Borderline D1 (Bachelor's vs Master's field boundary)**
Excerpts: *"BSc Applied Statistics (dissertation: Bayesian methods)"; no mention of AI/ML coursework specifically."*
Scores: D1=3 (default-low: Tier B Bachelor's sits at 2, but dissertation in a quantitative-inferential area nudges toward AI-adjacent; annotators split 2 vs 3). Flags: `A` on D1 (candidates 2/3, default-low would say 2 — see precedent P-01). Handling: **flag, don't average.** Escalate per tie-break if raters disagree.

**Example 05 — Borderline D5 (Director vs VP seniority)**
Excerpts: *"Head of Data & AI"* (no indication whether enterprise-level or team-level; no budget/scope stated).
Scores: D5=3 (default-low between Tier 3 Director-equivalent and Tier 4 Head-enterprise). Flags: `A` on D5 (candidates 3/4). Handling: "Head of" is ambiguous across companies; default-low to 3 absent scope language. See precedent P-02.

**Example 06 — Sparse profile (low completeness)**
Excerpts: *"MSc Computer Science"; "AI Engineer"* — nothing else populated.
Scores: D1=3, D2=0, D3=2, D4=0, D5=1, D6=0. Flags: `M` on D2, D4, D6. Handling: completeness_index = 3/6. Candidate for separate-analysis/exclusion category, not silent averaging.

**Example 07 — Contradiction (title vs substance — canonical inflation)**
Excerpts: *"Chief AI Officer"; About section: "passionate about digital transformation and driving synergy"* — no AI-specific, technical, or strategic detail anywhere; *"BA Communications"; no certs; no technical output.*
Scores: D1=0, D2=0, D3=0 (`M`), D4=0 (`M`), D5=2 (title Tier 5, but scored down hard: no strategic-scope or augmentation language, and About contradicts the title), D6=1. Flags: `C` on D5 (title Tier 5 vs. zero substantiating evidence), `M` on D3/D4. Handling: **the contradiction is the finding.** Set `title_substance_contradiction_flag = TRUE` at profile level. Do NOT let the Tier-5 title alone drive D5 to 4–5. See precedent P-03 (the single most important precedent).

**Example 08 — Under-signaled expert**
Excerpts: *"BSc Computer Science (AI specialization)"; "ML Engineer, 4 yrs — architected recommendation pipeline serving 5M users"; no certs listed; GitHub linked with an actively maintained library (300+ stars); Data Scientist title, no strategic language; no posting activity."*
Scores: D1=3, D2=0 (`M`), D3=4, D4=4 (external verification via provided GitHub link permitted), D5=1, D6=0 (`M`). Flags: `M` on D2, D6. Handling: genuinely strong practitioner scoring low on D2/D5/D6 for reasons unrelated to competence. Contrast deliberately with Example 07 — similar low dimensions, opposite meaning. See precedent P-04.

**Example 09 — Mixed strength (strong tech, weak leadership)**
Excerpts: *"PhD Computer Vision"; "Senior Research Scientist, 6 yrs"; "15 patents (USPTO-searchable)"; "NeurIPS/CVPR talks"; no management role; no certs; active on academic Twitter, minimal LinkedIn."*
Scores: D1=5, D2=0 (`M`), D3=4, D4=5, D5=1, D6=2. Flags: `M` on D2. Handling: illustrates why compensatory aggregation is contentious — huge D1/D4, near-zero D5. Preserve dimension profile; do not let a mean mask the leadership gap.

**Example 10 — Mixed strength (strong leadership, weak technical depth)**
Excerpts: *"MBA + BSc Information Systems"; "VP of AI Transformation, leads 40-person org, owns enterprise AI roadmap and governance"; "PMP (current)"; no publications, no code; frequent original posts on AI strategy and ethics; augmentation-aware language present."*
Scores: D1=3, D2=3, D3=3, D4=1, D5=4, D6=4. Flags: none (no contradiction — the leadership claims are substantiated by scope language even though technical depth is thin). Handling: genuinely strong *leader* who is not a technical contributor — legitimately different from Example 07's inflation. Distinguishing 10 from 07 is the core annotator skill. See precedent P-05.

**Example 11 — Ambiguous certification credibility**
Excerpts: *"Certified AI Professional — [unspecified online academy], 2023"* (issuer not recognizable; no assessment detail).
Scores: D2=1 (low-credibility issuer, but current). Flags: `A` on D2 (is this a recognized cert? default-low to 1). Handling: unknown-issuer certs default to low-credibility tier. See precedent P-06.

**Example 12 — Career pivot (recent AI, long non-AI history)**
Excerpts: *"20 yrs in general management; last 18 months as 'Head of AI Initiatives'"; "completed Google ML crash course (2025)"; no technical output; strategic language present but AI tenure very short."*
Scores: D1=2, D2=2, D3=2 (short explicit AI tenure), D4=0 (`M`), D5=3, D6=2. Flags: `A` on D3 (long career but short AI-specific tenure — score the AI-specific portion only). Handling: score D3 on AI-relevant experience, not total career length. See precedent P-07.

**Example 13 — Adjacent field expert (data engineering, not AI/ML)**
Excerpts: *"MSc Computer Science"; "Principal Data Engineer, 8 yrs — built large-scale data platforms"; "AWS Solutions Architect (current)"; strong GitHub (data infra, not ML); no ML modeling evidence; IC role."*
Scores: D1=3, D2=2 (general cloud, not AI-specific), D3=1 (AI-adjacent role band), D4=3, D5=1, D6=1. Flags: `A` on D3 (data engineering is adjacent, not AI-core). Handling: strong in an adjacent field ≠ AI credentials. Resist halo from obvious technical competence. See precedent P-08.

**Example 14 — Keyword-stuffed profile (inflation via vocabulary)**
Excerpts: *About section lists 40+ AI buzzwords ("AI, ML, deep learning, LLM, generative AI, transformers…"); no degree in field; no certs; no roles with AI-core titles; no technical output; title 'AI Evangelist'."*
Scores: D1=0, D2=0 (`M`), D3=0 (`M`), D4=1, D5=1, D6=2. Flags: `C` (keyword density contradicts absence of substantiating credentials). Handling: **the ontology locates keywords; it never scores them.** Keyword presence does not raise any dimension. This is a designed-in anti-inflation safeguard. See precedent P-09.

**Example 15 — Contradiction across sections (dates/roles inconsistent)**
Excerpts: *Headline: "10 years in AI leadership"; Experience section shows first AI-titled role beginning 3 years ago.*
Scores: score dimensions on the verifiable Experience-section evidence (D3 reflects ~3 yrs), not the headline claim. Flags: `C` on D3 (headline vs. experience dates). Handling: prefer structured/dated evidence over headline self-claims; log both spans. See precedent P-10.

**Example 16 — Non-English / localization ambiguity**
Excerpts: profile mixes English and another language; degree title in original language not clearly mapping to the §2.1 tiers.
Scores: attempt taxonomy mapping via the degree's recognized equivalent; if unresolved, `A` flag and default-low, log the untranslated term verbatim. Handling: do NOT guess a generous equivalence. See precedent P-11. **[THESIS-SPECIFIC]** Decide and document your language-scope policy before main collection (English-only sample? translation protocol?).

**Example 17 — Overlapping evidence across dimensions (double-counting risk)**
Excerpts: *"Published a paper on deploying ML in production"* — relevant to both D3 (experience) and D4 (contribution).
Scores: count the publication as D4 evidence (technical output) and the *deployment role* it describes as D3 evidence — but do not let the single artifact inflate both to their maxima; score each dimension on its own criterion. Flags: none if handled cleanly; note in log. Handling: one artifact may inform two dimensions, but each dimension is judged on its own rubric, not on artifact count. See precedent P-12.

**Example 18 — Deceptive absence (evidence of absence vs missing data)**
Excerpts: *"Self-taught, no formal AI education — proudly practitioner-first"; strong verifiable GitHub; ML Engineer 5 yrs."*
Scores: D1=1 (evidence of genuine absence of formal education — `missing=FALSE`, not `M`), D3=4, D4=4. Flags: none; explicitly `missing=FALSE` on D1. Handling: distinguish stated absence (score on it) from missing data (flag `M`). See rulebook §1.3 and precedent P-13.

---

## 4. Official Precedent Library

**[THESIS-SPECIFIC] — [FROZEN] once annotation begins.** These are binding coding precedents. When a live case matches a precedent, annotators apply the precedent ruling rather than re-deciding. New precedents may be added during the pilot via the revision log, but existing ones are not overturned silently.

| ID | Situation | Binding ruling |
|---|---|---|
| **P-01** | Field sits on a taxonomy tier boundary (e.g., Applied Statistics between Tier A/B) | Default-low; flag `A`; escalate to tie-break only if raters disagree by ≥1. Do not average. |
| **P-02** | "Head of X" title with no scope/budget/level language | Score positional Tier 3 (Director-equivalent), not Tier 4, absent explicit enterprise-scope evidence. Flag `A`. |
| **P-03** | Senior/C-level title with no substantiating AI, technical, or strategic evidence anywhere (canonical inflation) | Do **not** let title alone drive D5 above 2. Set `title_substance_contradiction_flag=TRUE`. This pattern is preserved as data, never resolved away. |
| **P-04** | Strong verifiable technical evidence but low D2/D5/D6 (under-signaling) | Score each dimension honestly on its evidence; do **not** infer higher D5/D6 from technical strength (no positive halo). Preserve the low scores; they are meaningful. |
| **P-05** | Substantiated leader, thin technical depth (opposite of P-03) | If scope/budget/governance language substantiates the leadership claim, D5 is legitimately high even with low D4. This is **not** a contradiction. The distinction from P-03 is the presence vs. absence of substantiating scope evidence. |
| **P-06** | Certification from unrecognized/unknown issuer | Default to low-credibility tier (max D2 contribution = 1 for a single such cert). Flag `A`. |
| **P-07** | Long total career, short AI-specific tenure | Score D3 on AI-relevant experience only, not total years. Flag `A`. |
| **P-08** | Expert in adjacent field (data eng., general SWE) with no ML-core evidence | Adjacent-role band for D3; do not treat adjacent expertise as AI-core. Resist competence halo. |
| **P-09** | Keyword-stuffed profile, no substantiating credentials | Ontology locates keywords but never scores them. Keyword density cannot raise any dimension. Flag `C` if density contradicts substance. |
| **P-10** | Headline self-claim contradicts dated Experience section | Prefer structured/dated evidence over headline claims. Flag `C`. Log both spans. |
| **P-11** | Non-English or untranslatable credential | Map to recognized equivalent if defensible; else default-low, flag `A`, log verbatim. Never guess generously. |
| **P-12** | One artifact is evidence for two dimensions | Each dimension scored on its own criterion; a single artifact may inform two dimensions but does not automatically maximize either. No double-inflation. |
| **P-13** | Stated absence of a credential vs. missing data | Stated absence: score on it, `missing=FALSE`. No evidence at all: score 0, `missing=TRUE`. Analyze the two separately. |
| **P-14** | External link provided by profile (e.g., GitHub) | Following a profile-provided link is within-profile evidence (allowed all dimensions); web-searching for corroboration is restricted external verification (D4 only, per §2.5). |
| **P-15** | Verification reveals claim is false/overstated | Verification may lower a score (D4 only); it may never raise a score above what profile text supports. |

---

## 5. Complete Version History

| Version | Stage | Key decisions / changes | Status |
|---|---|---|---|
| **v0.1** | Initial concept (thesis exposé) | Six-dimension idea proposed; original 8-paper literature plan (Spence, Boyatzis, Tadelis, van Dijk, De Keyser, Tambe, Waller, Haffar) | Superseded |
| **v0.2** | Literature reconciliation | Discovered only 2 of 8 planned papers present; honest remapping to 7 real papers + 2 verified gap-fillers (Boyatzis 1982, Hinkin 1998). Competency-theory and scale-validation gaps disclosed. | Superseded |
| **v0.3** | Dimension design (Task 2) | Six dimensions given theoretical anchors, 0–5 criteria, NLP extraction plans, verifiability gradient established. Institution-prestige excluded from D1. | Superseded |
| **v0.4** | Coding rulebook + pilot design | General scoring principles, missing/ambiguous/contradiction handling, verification rules, tie-breaks, coding log, pilot design, per-dimension Krippendorff's α, revision procedure. | Superseded |
| **v0.5** | Scoring framework (Task 3) | Consolidated scoring table; unweighted formula with three candidate aggregation functions (Keeney & Raiffa); credential-gap extension for Contribution 2; illustrative classification; placeholder bands. | Superseded |
| **v1.0** | **Final pre-implementation blueprint (this document)** | Definitive reference table; all 8 taxonomies frozen; 18 worked examples; 15-entry precedent library; frozen/open decision register; examiner critique. **No new dimensions, no conceptual change.** | **Current — frozen for implementation** |

---

## 6. Frozen vs. Open Decision Register

### 6.1 Permanently frozen before implementation [FROZEN]
- The six dimensions, their definitions, and their theoretical anchors.
- The 0–5 scoring criteria per dimension (Task 3 §1 table).
- The eight taxonomies in §2 (frozen for reproducibility; revisable only via logged revision procedure).
- The verifiability gradient and the requirement to report per-dimension reliability separately.
- Rulebook rules: default-low under uncertainty; halo prohibition; missing vs. stated-absence distinction; verification permitted for D4 only and never score-inflating; keyword ontology never used as a scoring method.
- The 15-entry precedent library.
- Exclusion of institution prestige from scoring.

### 6.2 Intentionally open until empirical validation [OPEN]
- **Aggregation function** — compensatory / partially compensatory / conjunctive (Task 3 §2.2). To be chosen after pilot evidence on how the three diverge in practice.
- **Dimension weights (w₁–w₆)** — to be derived empirically (job-posting emphasis, expert elicitation, and/or regression against impact indicators), reported comparatively. No numeric values fixed.
- **Classification thresholds/bands** — placeholder bands in Task 3 §5 are explicitly not for reporting; real bands to come from the actual score distribution (quartiles/clustering).
- **Minimum reliability thresholds' consequences** — the α≥.667 / ≥.80 targets are set, but what to do if a dimension fails *after one revision cycle* is deferred until/unless it actually occurs.
- **Language/localization scope** (Example 16 / P-11) — English-only vs. translation protocol: decide and document before main collection.
- **Job-posting-side scoring validation** — the Contribution-2 requirement-mining pipeline (Task 3 §2.4) is unpiloted and must not inherit the profile-side pilot's reliability.

---

## 7. External Examiner's Critical Review

Written deliberately in the voice of a skeptical MSc thesis examiner. These are the questions you should expect and pre-empt, not reasons the framework is unsound. I have not softened them.

**7.1 Construct validity — the central vulnerability.**
Half your instrument (D3, D5, D6) measures *self-presentation on a self-promotion platform*, not the underlying constructs it names. An examiner will press: "You claim to audit whether AI leaders *possess* credentials, but for three of six dimensions you can only observe what they *chose to write on LinkedIn*." Your defence must be explicit and up front: ALCSM measures the **credential signal as visible on LinkedIn**, and the gap between signal and substance *is itself the object of study* (Spence). Reframe the thesis claim precisely — you are auditing the *signalling layer*, not certifying actual competence. If you overclaim ("we measure whether they are qualified"), you will lose ground you don't need to cede. This reframing is the most important single edit to make across the whole thesis before Task 4.

**7.2 The D5 title-as-proxy problem will be probed hard.**
Boyatzis and Steinbach et al. are cited as anchors for D5, yet both theorise facets of leadership (behavioural competencies; construal-level flexibility) that your data *cannot observe*. An examiner may call this a citation-grounding mismatch. Pre-empt it: state that D5 measures only the *positional and rhetorical* facet, that the cited theories are invoked to explain *why the unobservable facets matter* (hence why D5 is a weak proxy), and that this limitation is why D5 is a candidate for non-compensatory treatment. Do not imply D5 measures leadership competence.

**7.3 Researcher-constructed taxonomies = reproducibility exposure.**
All eight taxonomies are your own design. Two risks: (a) another researcher applying "the same" taxonomy could classify differently at the boundaries; (b) the taxonomies date quickly. Mitigations to state: empirically seed the certification/role taxonomies from your job-posting corpus; stamp construction dates and versions; report boundary-case inter-rater reliability specifically (not just overall α); publish the taxonomies in full in an appendix/repo so they are auditable. The pilot's boundary-case agreement is your evidence that the taxonomies are operational, not merely plausible.

**7.4 Single-composite ambiguity is a known, unresolved risk.**
Your own Task 3 examples (B vs. C; here 07 vs. 08) show that one composite number cannot distinguish inflation from under-signalling. An examiner will ask what your headline finding actually *is* if the composite is ambiguous. Answer: the *pattern* of dimension scores (and the contradiction flags) is the primary unit of analysis; the composite is reserved for aggregate comparisons (vs. job postings; vs. impact indicators). Make sure your Results chapter is structured around dimension-level and flag-level analysis, not a single ALCSM leaderboard — otherwise the ambiguity becomes a finding *against* you.

**7.5 The automation/augmentation signal (§2.8) is the weakest limb.**
It is a novel, unvalidated NLP task detecting *rhetoric*, resting on a single conceptual paper (Raisch & Krakowski). If you foreground it, an examiner will target it. Recommendation: keep it clearly labelled as *exploratory/secondary* throughout; do not let any headline finding depend on it until (and unless) the pilot shows it can be annotated reliably. Consider whether it earns its place in v1.0 at all, or should be demoted to "future work."

**7.6 Sampling validity of the 500 profiles (foreshadowing Task 4).**
Not in scope for this document, but the examiner's biggest empirical question is looming: how are 500 "AI leaders" *selected*, and does that selection bias the credential picture? A LinkedIn-search-based sample of people *with AI leadership titles* structurally cannot include competent AI leaders who lack the title — which interacts with your under-signalling category (Example 08). Flag now that Task 4 must define the sampling frame precisely and honestly, because a biased frame undermines every downstream ALCSM statistic regardless of how good the instrument is.

**7.7 Circularity risk in weighting (RQ4).**
If you later derive weights by regressing ALCSM dimensions against "professional impact indicators" (RQ4) *and then* report that ALCSM correlates with those same indicators, that is circular. Pre-empt: keep weight-derivation data and validation data separate (e.g., cross-validation / held-out set), and state the safeguard explicitly.

**7.8 Ethics/GDPR is not yet resolved (Task 5).**
D6's post-level activity and any external verification touch personal data under GDPR. The specification is implementation-ready on the *measurement* side but not on the *lawful-basis* side. Task 5 must precede real data collection, not follow it. An examiner (and an ethics board) will treat this as blocking, not optional.

**Overall examiner verdict (simulated):** the conceptual model is coherent, theoretically grounded, and unusually transparent about its own limitations — which is a strength. The instrument is defensible *if and only if* the thesis consistently frames it as an audit of the **LinkedIn credential signal**, reports at dimension level rather than as a single score, treats D3/D5/D6 and the augmentation signal with appropriate epistemic humility, and resolves sampling (Task 4) and ethics (Task 5) rigorously. None of these require redesigning the framework. They require disciplined framing and honest reporting — which the framework is already built to support.

---

## 8. Readiness statement for Task 4

The measurement model is frozen and implementation-ready at the conceptual level. Before or alongside Task 4 (data schema design), the two examiner points that most affect schema design are: (7.1) the signal-vs-substance reframing (affects how variables are *named and interpreted*), and (7.6) the sampling frame (affects the profile dataset schema's provenance/selection fields). I recommend carrying both into Task 4 explicitly.

No new dimensions were introduced and the conceptual model was not altered. Genuine issues were flagged for framing/reporting, not resolved by redesign, per your instruction.
