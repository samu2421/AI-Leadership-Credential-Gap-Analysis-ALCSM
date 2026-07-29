# ALCSM Annotation Handbook
### Training and Reference Manual for Human Coders

**Thesis:** *The AI Leadership Credential Gap: An NLP Audit of 500 LinkedIn Profiles*
**Framework:** ALCSM v1.0 (frozen). Schema v1.0.1 (frozen).
**Audience:** independent annotators coding LinkedIn profiles on the six ALCSM dimensions.
**Status:** this handbook *operationalises* the frozen rulebook and precedent library. It changes no dimension, criterion, taxonomy, or rule. Where it says "the rule is," that rule is frozen.

> **The one idea to hold above all others.** ALCSM scores the **credential signal a profile presents on LinkedIn** — not the person's real competence. You are auditing what is *shown*, not judging who is *good*. The gap between the signal and the substance is the object of study, not a mistake to correct. Never "give someone the benefit of the doubt" by importing knowledge the profile does not contain.

---

## Part A — Orientation

### A.1 What you are coding
Each profile receives **six independent scores**, one per dimension, each an integer **0–5**:

| Code | Dimension | What the signal is | How verifiable from text |
|---|---|---|---|
| D1 | Formal Education | Credentialed AI/quantitative education | **High** |
| D2 | Professional Certifications | Renewable competence signals | **High** |
| D3 | Practical AI Experience | Self-described applied AI/ML role history | Medium |
| D4 | Technical Contributions | Visible, partly verifiable output | Medium–High |
| D5 | Leadership & Strategic Responsibility | Positional + strategic-framing signal | **Low** |
| D6 | Professional Engagement | Ongoing reputational/engagement activity | **Low–Medium** |

**Why the verifiability column matters to you.** D1, D2, D4 rest on structured, checkable evidence. D3, D5, D6 rest on self-presentation. You will feel *less certain* coding D5 and D6 — that is correct and expected, not a sign you are doing it wrong. The framework anticipates lower agreement there.

### A.2 The three rules that prevent the most common errors
1. **Score the profile, not the person.** If the text does not say it, it does not count — even if you happen to know otherwise.
2. **No halo.** A brilliant PhD (D1) does not raise Leadership (D5). Score each dimension only on its own evidence.
3. **When genuinely torn between two adjacent scores, take the lower.** This *default-low* rule is deliberate: the study audits credential *gaps*, so the safer error is to under-credit, not over-credit. Apply it consistently.

### A.3 The four evidence states (memorise these)
Every dimension score carries exactly one **missing-status**:

| State | Meaning | Typical score | Counts as "informative"? |
|---|---|---|---|
| `present` | Evidence exists; you scored it on its merits | 0–5 | Yes |
| `absent_stated` | The profile **positively states** the credential is absent (e.g. "no formal AI education, self-taught") | usually low | **Yes** — it is a claim, not a gap |
| `unavailable` | No evidence found: section empty, absent, or not retrieved | 0 | No |
| `not_applicable` | (job postings only — you will not use this on profiles) | — | No |

The distinction between `absent_stated` and `unavailable` is one of the most important in the whole scheme. *"I have no certifications, I'm self-taught"* is **`absent_stated`** and informative. A blank certifications section is **`unavailable`** and missing. They are never treated the same.

---

## Part B — The Annotation Sequence

Follow this order for **every profile**. Do not shortcut it, and do not re-order it.

1. **Open one profile.** You see the six dimensions together. You do **not** see the other rater's scores. You do **not** see any RQ4 impact values (follower counts, engagement). If you can see those, stop and report an interface fault — they must be hidden during coding.
2. **Read the whole profile once** before scoring anything, to get context and spot contradictions between sections.
3. **Score all six dimensions for this profile** before moving to the next profile. (Do not code "all D1s across profiles" — that induces bias.)
4. **For each dimension, run the decision tree in Part C.**
5. **Record, per dimension:** the score; the verbatim evidence span(s); the missing-status; any ambiguity or contradiction flag (with candidates/spans); the precedent applied (if any); and, for D4 only, verification metadata.
6. **Set the profile-level contradiction flag** if a title-vs-substance contradiction was found (see P-03).
7. **Submit** only when all six dimensions are complete. Submission is final for the independence step — you cannot revise after seeing another rater's scores.

---

## Part C — The Decision Tree (run per dimension)

```
START — dimension D_i on this profile
│
├─ Q1. Is there ANY evidence for D_i anywhere in the profile?
│      │
│      ├─ NO evidence at all
│      │     │
│      │     ├─ Does the profile POSITIVELY STATE the credential is absent?
│      │     │      (e.g. "self-taught, no degree in the field")
│      │     │     ├─ YES → missing_status = absent_stated
│      │     │     │         score on the stated content (usually low, per the
│      │     │     │         dimension's 0–5 table). NOT missing. → go to Q5
│      │     │     └─ NO  → missing_status = unavailable
│      │     │               score = 0, mark missing. → END (record)
│      │     │
│      └─ YES, evidence exists → missing_status = present → go to Q2
│
├─ Q2. Locate the evidence span(s).
│      Use the AI keyword ontology ONLY to FIND relevant text.
│      Keywords never set or raise a score (see P-09). Copy the exact span.
│
├─ Q3. Apply the dimension's 0–5 criteria (Part E) to the evidence.
│      Reach a provisional score.
│
├─ Q4. Does the evidence plausibly support TWO ADJACENT scores?
│      ├─ YES → ambiguity_flag = TRUE; record candidate_low & candidate_high;
│      │         assign the LOWER (default-low). The assigned score MUST be one
│      │         of the two candidates. → go to Q5
│      └─ NO  → assign the single score → go to Q5
│
├─ Q5. Does this evidence CONTRADICT another part of the profile?
│      (e.g. C-level title vs. an About section describing only junior tasks)
│      ├─ YES → contradiction_flag = TRUE; quote BOTH conflicting spans.
│      │         Score on the MOST SPECIFIC, MOST CONCRETE evidence.
│      │         Do NOT let an unsupported senior title inflate the score (P-03).
│      │         If it is a title-vs-substance case, also set the PROFILE-LEVEL
│      │         title_substance_contradiction_flag. → go to Q6
│      └─ NO  → go to Q6
│
├─ Q6. Is this D4 (Technical Contributions) AND do you need to verify a claim?
│      ├─ D4 only: you MAY follow a link the profile itself provides, or check a
│      │           standard public index (Scholar/arXiv/patent office). Verification
│      │           may CONFIRM or LOWER a score; it may NEVER raise it above what the
│      │           profile text alone supports (P-14, P-15). Record verification
│      │           source, timestamp, outcome.
│      └─ Any other dimension: NO external verification. Score on profile text only.
│
├─ Q7. Does a PRECEDENT (P-01…P-15) match this situation?
│      ├─ YES → apply the binding ruling; record the precedent ID.
│      └─ NO  → proceed.
│
└─ Q8. RECORD: score, evidence span, missing_status, flags (+candidates/spans),
        precedent_applied, and (D4 only) verification metadata. → END
```

**A note on Q1's branch.** The `absent_stated` vs `unavailable` split is the single most error-prone decision. When in doubt about whether silence is a *claim of absence* or merely *no data*, it is `unavailable` — a positive claim requires actual words on the profile asserting the absence.

---

## Part D — Evidence Requirements

- **Every `present` score must cite a verbatim span.** No span, no score. A score sheet cell must always be traceable back to text you can point to. The interface enforces this; do not try to work around it.
- **Keep spans short.** Capture the few words that justify the score, not whole paragraphs.
- **Quote, don't paraphrase, in the evidence field.** Your interpretation goes into the score; the raw words go into the evidence.
- **One artifact can support two dimensions, but does not maximise either** (P-12). A paper on "deploying ML in production" is evidence for both D3 (experience) and D4 (contribution); score each on its own criterion, do not let a single item inflate both.
- **The ontology locates, it never scores** (P-09). Forty AI buzzwords in an About section do not raise any dimension; if keyword density contradicts an absence of real credentials, that is a contradiction to flag, not a score to award.
- **Follow the money on links** (P-14). A GitHub link the profile *itself provides* is within-profile evidence and may inform any dimension. *Searching the web* for corroboration is the restricted external-verification pathway — D4 only.

---

## Part E — The 0–5 Criteria (reference)

Frozen. Apply as written.

| Score | D1 Education | D2 Certifications | D3 Experience | D4 Contributions | D5 Leadership | D6 Engagement |
|---|---|---|---|---|---|---|
| 0 | None / unrelated | None | No AI/ML roles | None discoverable | IC, no leadership language | No visible engagement |
| 1 | Bachelor's, adjacent, no AI coursework | 1 expired/low-credibility | AI-adjacent role only | Non-technical public content | Team lead/informal only | Passive (likes/shares) |
| 2 | Bachelor's CS/quant, no AI spec. | 1 current recognised-vendor | 1–2 yrs explicit AI role, IC | 1 verifiable artifact | Manager, team scope | Regular passive, no original |
| 3 | Bachelor's + AI spec., or Master's adjacent | 2+ current general | 3+ yrs AI, or ownership language | Multiple, unverified | Director/Head, some strategy | Occasional original commentary |
| 4 | Master's AI/ML/DS, or PhD adjacent | Multiple current AI-specific | Multi-yr, multi-role, ownership | Multiple, ≥1 externally verifiable | VP/senior, explicit enterprise strategy | Regular original + community |
| 5 | PhD CS/AI with AI research | Multiple AI certs + maintained pro body | Sustained AI leadership, deployed at scale | Sustained, externally verifiable | C-level, strategic + augmentation-aware | Sustained thought leadership + community role |

---

## Part F — Ambiguity Handling

1. **Recognise it.** Ambiguity = the evidence could reasonably justify **two adjacent** scores (e.g. a 3 or a 4). Non-adjacent uncertainty (a 2 or a 5) is not ambiguity — it means you have not finished reading the evidence.
2. **Record both candidates**, `candidate_low` ≤ `candidate_high`, and they must be adjacent.
3. **Assign the lower** (default-low). The assigned score must equal one of the two candidates — the interface enforces this.
4. **Do not average, do not split.** There are no half-scores.
5. **Flag it.** `ambiguity_flag = TRUE`. A dimension that produces frequent ambiguity flags across many profiles is a signal the *rulebook wording* may need refinement — that is handled by the research lead through the revision log, never by you inventing a local rule.

---

## Part G — Contradiction Handling

1. **The contradiction is data, not noise.** Title-vs-substance mismatches are the central phenomenon this study exists to measure. Never "resolve" them by quietly picking the flattering reading.
2. **Quote both spans.** Record the conflicting evidence verbatim.
3. **Score on the most specific, most concrete evidence** — not on the most impressive-sounding.
4. **A senior title alone never drives D5 above 2** when nothing substantiates it (P-03).
5. **Set the profile-level `title_substance_contradiction_flag`** for title-vs-substance cases.
6. **Distinguish P-03 from P-05.** A "Chief AI Officer" whose profile shows only generic language is *inflation* (P-03). A VP whose profile substantiates real scope and strategy but shows thin technical output is a *legitimately narrow leader* (P-05) — high D5, low D4, and **not** a contradiction. The presence or absence of *substantiating scope evidence* is what separates them. This distinction is the core annotator skill; the examples in Part J drill it.

---

## Part H — Precedent Usage

The precedent library is **binding**. When a live case matches a precedent, apply the ruling rather than re-deciding, and record the precedent ID. You do not create new precedents; only the research lead does, via the revision log.

| ID | Situation | Binding ruling |
|---|---|---|
| P-01 | Field on a taxonomy tier boundary | Default-low; flag `A`; escalate only if raters differ ≥1 |
| P-02 | "Head of X" with no scope/budget language | Score positional Tier 3 (Director-equiv.), not Tier 4; flag `A` |
| P-03 | Senior/C-level title, no substantiating evidence | Title alone must not drive D5 above 2; set contradiction flag |
| P-04 | Strong verifiable tech, low D2/D5/D6 | Score each honestly; **no positive halo**; keep the low scores |
| P-05 | Substantiated leader, thin technical depth | If scope substantiates leadership, D5 legitimately high even with low D4 — **not** a contradiction |
| P-06 | Certification from unrecognised issuer | Low-credibility tier (max 1 for a single such cert); flag `A` |
| P-07 | Long career, short AI-specific tenure | Score D3 on AI-relevant experience only; flag `A` |
| P-08 | Adjacent-field expert (data eng., general SWE) | Adjacent band for D3; resist competence halo |
| P-09 | Keyword-stuffed profile, no substance | Ontology locates but never scores; flag `C` if density contradicts substance |
| P-10 | Headline claim contradicts dated experience | Prefer structured/dated evidence; flag `C`; log both spans |
| P-11 | Non-English / untranslatable credential | Map to a defensible equivalent, else default-low, flag `A`, log verbatim |
| P-12 | One artifact evidences two dimensions | Each dimension on its own criterion; no double-inflation |
| P-13 | Stated absence vs. missing data | `absent_stated` (score on it) vs `unavailable` (score 0, missing) |
| P-14 | Profile-provided link | Within-profile evidence (any dimension); web search is D4-only external verification |
| P-15 | Verification reveals an overstated claim | May lower a score (D4 only); may never raise above profile text |

---

## Part I — Adjudication Workflow

Adjudication resolves disagreements *after* both raters have coded independently. As a coder you do not adjudicate your own disagreements; you supply the independent judgements that feed it.

- **Magnitude 1** (scores differ by 1): a brief consensus discussion is permitted. If consensus is reached, it is recorded with the reason for the initial discrepancy.
- **Magnitude ≥ 2**: **no informal consensus.** Escalate directly to the adjudicator — a two-point gap usually signals rubric ambiguity, not a judgement call.
- **The adjudicated score is stored as a NEW record**, never overwriting your original. Your independent scores are preserved permanently, because reliability is computed on them.
- **A systematic disagreement pattern** (the same kind of case splitting repeatedly) is escalated to the research lead as possible evidence the rulebook wording needs revision — not re-litigated case by case.

---

## Part J — Coding Examples (constructed for training)

> These profiles are **constructed composites for training only.** They are not real people and not from the dataset. Scores use the frozen criteria; aggregation is not shown (it is not your job).

**Example 1 — Substantiated senior leader (the "clean" case).**
*"PhD Machine Learning; VP of AI leading enterprise strategy across 4 units, $12M budget; AWS ML Specialty (2025); 12 publications (Scholar linked); monthly governance posts."*
D1=5, D2=4, D3=4, D4=5, D5=4, D6=4. No flags. Everything is consistent and substantiated.

**Example 2 — Credential inflation (P-03).**
*"Chief AI Officer"; About = "passionate about digital transformation and synergy," no AI/technical/strategic specifics; "BA Communications"; no certs; no output.*
D1=0, D2=0 (`unavailable`), D3=0 (`unavailable`), D4=0 (`unavailable`), **D5=2** (Tier-5 title, but scored **down hard** — nothing substantiates it), D6=1.
Flags: **C** on D5; profile `title_substance_contradiction_flag = TRUE`. **The title does not buy a high D5.**

**Example 3 — Under-signalled expert (P-04).**
*"BSc CS (AI spec.); ML Engineer 4 yrs — architected recommendation pipeline serving 5M users; GitHub linked, actively maintained 300-star library; Data Scientist title, no strategic language; no posting activity."*
D1=3, D2=0 (`unavailable`), D3=4, D4=4 (verified via profile-provided GitHub link), D5=1, D6=0 (`unavailable`). No flags.
**Contrast with Example 2.** Both have several low dimensions — but here the low scores are honest (this person simply does not certify, lead, or post), while Example 2's are hollow. **Distinguishing these two is the whole job.** Do not rescue Example 3's D5/D6 with a halo from its strong D3/D4 (P-04).

**Example 4 — Legitimately narrow leader (P-05).**
*"MBA + BSc Information Systems; VP AI Transformation, leads 40-person org, owns enterprise AI roadmap and governance; PMP; no publications or code; frequent original strategy/ethics posts; augmentation-aware language."*
D1=3, D2=3, D3=3, D4=1, D5=4, D6=4. **No contradiction flag** — the leadership claim is *substantiated by scope language*, so high D5 with low D4 is legitimate, unlike Example 2.

**Example 5 — Stated absence vs. missing (P-13).**
*"Self-taught, no formal AI education — proudly practitioner-first; strong verifiable GitHub; ML Engineer 5 yrs."*
D1 = 1 with `missing_status = absent_stated` (a positive claim, **not** missing), D3=4, D4=4. The certifications section is simply blank → D2=0, `unavailable`.

**Example 6 — Boundary ambiguity (P-02).**
*"Head of Data & AI"* — no budget, scope, or level stated.
D5: candidates 3 and 4; assign **3** (default-low); `ambiguity_flag = TRUE`; precedent P-02.

---

## Part K — Quality Assurance

**Per-profile self-check (run before submitting each profile):**
- [ ] All six dimensions scored.
- [ ] Every `present` score has a verbatim evidence span.
- [ ] Each dimension's missing-status is correct; `absent_stated` and `unavailable` not confused.
- [ ] No halo: check that a strong dimension did not inflate a weak one.
- [ ] Ambiguity candidates are adjacent and bracket the assigned score; default-low applied.
- [ ] Contradictions flagged, both spans quoted, title-substance flag set where relevant.
- [ ] Verification used only on D4, only via allowed sources, never score-raising.
- [ ] Precedent IDs recorded where a precedent was applied.
- [ ] No RQ4 impact values were consulted (they must not even be visible).

**Interface guarantees you can rely on (schema-enforced):**
- You cannot save a `present` score without evidence.
- You cannot record verification on any dimension but D4.
- You cannot set an ambiguity flag without bracketing candidates.
- You cannot see the other rater's scores before submitting.
- Your original score is never overwritten by adjudication.

**Ongoing QA by the research lead:** periodic spot-checks of coded profiles against their evidence spans; monitoring of flag rates per dimension (a dimension with >~30% ambiguity/contradiction flags is reviewed for rubric clarity even if agreement looks fine).

---

## Part L — Inter-Rater Reliability Procedure

Reliability is how the study demonstrates that the coding is reproducible, not idiosyncratic to one person.

1. **Pilot first.** Before main coding, both raters independently code a small purposive pilot (10–20 profiles deliberately including clear, borderline, sparse, contradictory, under-signalled, and inflation cases).
2. **Compute per dimension, never pooled.** Krippendorff's α is calculated **separately for each of the six dimensions**, on the raters' **independent, pre-adjudication** scores only. Adjudicated and adjudicator rows are excluded automatically.
3. **Report with diagnostics.** Each α is accompanied by a bootstrap confidence interval, raw percentage agreement, the number of units, and the score variance — because on low-variance dimensions (often D5/D6) α can look low even when raw agreement is high.
4. **Expect D5/D6 to be lower**, and know this in advance. A modest α on Leadership is an anticipated property of a low-verifiability dimension, not a failure of your coding.
5. **Decision thresholds (frozen):**
   - α ≥ .80 → the dimension proceeds as coded.
   - .667 ≤ α < .80 → acceptable, but disagreement cases are reviewed and rulebook *wording* may be clarified.
   - α < .667 → the rulebook wording is revised (never the frozen criteria) and the dimension is re-piloted.
6. **Sustained reliability.** A pre-registered random subset (or 100%) of the *main* sample is also double-coded, and reliability reported on it — reliability is not a one-time gate; drift over hundreds of profiles is real.
7. **Your part in all this:** code independently, cite evidence, apply precedents, and never discuss specific profiles with the other rater before both of you submit. The statistics are only meaningful if your judgements are genuinely independent.

---

## Part M — Annotator Training Path (certification before real data)

A new annotator is *certified* before coding any real profile:

1. **Read** this handbook, the frozen rulebook, and the precedent library end to end.
2. **Study** the worked examples in Part J until the P-03 vs P-04 vs P-05 distinctions are second nature.
3. **Practice-code** 2–3 constructed (non-sample) profiles jointly with the trainer; discuss every discrepancy openly. These are excluded from all reliability figures.
4. **Certification check:** independently code a small held-out set of constructed profiles with known reference scores. Meet the agreement threshold set by the research lead before proceeding. If not met, repeat training on the dimensions where you diverged.
5. **Begin real coding**, starting with the reliability pilot.

Re-certify if the rulebook is revised (a new rulebook version) or after any extended break in coding.

---

*This handbook operationalises frozen ALCSM v1.0 and Schema v1.0.1. It introduces no new dimension, criterion, taxonomy, precedent, or rule. Any apparent need to change a frozen element is escalated to the research lead as a possible framework-version decision — it is never made at the desk.*
