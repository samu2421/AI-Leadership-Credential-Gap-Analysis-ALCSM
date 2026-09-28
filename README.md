# The AI Leadership Credential Gap

**An NLP Audit of 500 LinkedIn Profiles**

MSc thesis research repository — Applied Data Science and Analytics, SRH Berlin University of Applied Sciences, Hamburg, Germany.

This repository contains the framework specification, analysis code, governance record, and aggregate results for a master's thesis study of the credential signals that self-identified AI leaders display on LinkedIn, and how those signals compare to the credentials that AI leadership job postings actually ask for.

---

## Overview

Organisations hiring for AI leadership roles rely heavily on publicly visible professional credentials, but there is no shared, documented instrument for describing what those credentials consist of. This study builds one — the **AI Leadership Credential Scoring Model (ALCSM)** — applies it to a sample of German-market LinkedIn profiles and job postings, examines how reliably it can be applied, and tests whether a simple NLP model can reproduce human scores.

ALCSM describes **observable credential signals**. It does not measure competence, capability, or leadership effectiveness, and it does not rank or score candidates. This distinction is load-bearing throughout the study and throughout this repository.

## Research aim

To develop and empirically examine a structured, dimension-level model for describing AI leadership credential signals as they appear in public professional profiles, and to compare those signals against employer-stated requirements.

## Research questions

| | Question | Status |
|---|---|---|
| **RQ1** | What credential patterns exist among self-identified AI leaders, as observable on LinkedIn? | Complete |
| **RQ2** | How do stated job-posting requirements compare to the credential signals held by AI leaders on LinkedIn? | Complete |
| **RQ3** | How can ALCSM be constructed and validated as a measurement instrument? | Complete |
| **RQ4** | Do ALCSM credential signals correlate with observable professional impact? | **Planned but not conducted** |
| **RQ5** | Does a human-vs-machine comparison of NLP-predicted ALCSM scores against the human gold standard reveal usable automated-scoring signal? | Complete (proof-of-concept) |

**RQ4 was not conducted.** The external criterion variables it required (network reach, content engagement, recognition count, seniority progression) were never collected, and no proxy variable was substituted for them. RQ4 is reported in the thesis as a documented limitation, not as a finding. No RQ4 result exists anywhere in this repository.

## The ALCSM framework (v1.1)

ALCSM describes a profile across six dimensions. Each dimension is scored as an **integer from 0 to 5** on an **ordinal** scale.

| | Dimension | What it describes |
|---|---|---|
| **D1** | Formal Education | Degree-level educational credentials in relevant fields |
| **D2** | Professional Certifications | Named, verifiable professional certifications |
| **D3** | Practical AI Experience | Observable applied AI work history |
| **D4** | Technical Contributions | Publications, patents, open-source and comparable technical output |
| **D5** | Leadership & Strategic Responsibility | Stated leadership scope and strategic responsibility |
| **D6** | AI Industry/Application Breadth | The number of distinct industries or application domains in which AI-related professional experience is observable |

### Properties of the model

- **Each dimension is scored independently.** There is no cross-dimension inference and no halo effect: evidence supporting one dimension never raises another.
- **Scoring is evidence-based.** A score above zero requires an identified evidence span in the source text. Keyword presence alone never sets a score.
- **There is no composite score.** ALCSM produces six separate dimension scores and nothing else.
- **There is no weighting scheme.** No dimension is weighted relative to another; the question of relative weight is left deliberately open.
- **There are no classification bands.** ALCSM does not sort profiles into tiers, levels, or categories.

ALCSM is treated as a **formative composite index**, not a reflective scale: its dimensions define the construct rather than reflect a single underlying latent trait. This classification follows the formative/reflective distinction in the measurement literature (Bollen & Lennox, 1991; Diamantopoulos & Winklhofer, 2001; Jarvis, MacKenzie & Podsakoff, 2003). It has a direct methodological consequence: **internal-consistency statistics such as Cronbach's alpha are not appropriate across ALCSM dimensions and are never computed in this study.** Agreement is assessed per dimension using Krippendorff's alpha (Krippendorff, 2004), never pooled across dimensions.

### D6 in version 1.1

D6 was revised during the study. The original D6, "Professional Engagement & Continuous Development," was retired because the collected dataset contained no post-level activity evidence for any profile, making the construct unobservable at the population level sampled. It was replaced by **D6 — AI Industry/Application Breadth**, which is answerable from evidence the dataset uniformly contains. This change is recorded in `11_Implementation_Governance/Governance/DECISION_LOG.md` (D-0038) and specified in `02_Framework_Development/ALCSM_D6_Industry_Breadth_v1.1.md`.

Because this repository preserves the full chronological design record, earlier documents under `02_Framework_Development/`, `03_Database_Design/` and `11_Implementation_Governance/` still describe the retired D6. Those documents are retained deliberately as the historical record. **The definition above is the operative one used in the thesis.** The database column code `d6_engagement` was also left unchanged for schema stability; it now carries the v1.1 construct.

### Missing data

ALCSM distinguishes four evidence states: `present`, `absent_stated`, `unavailable`, and `not_applicable`. Only `present` and `unavailable` occur on the profile side of this study. **`unavailable` is never treated as zero** — an absence of observable evidence is recorded as unobserved, not as an absence of the credential.

## Research design

A cross-sectional, mixed-methods observational study in four stages:

1. **Framework development** — dimension specification, scoring rubric, coding rulebook, and taxonomies, frozen before annotation.
2. **Data collection** — LinkedIn profiles and AI leadership job postings from the German market, collected against a documented sampling frame.
3. **Annotation** — rubric-based scoring of every profile on all six dimensions, with a structured human review pass and an audit trail.
4. **Analysis** — descriptive analysis (RQ1), supply-versus-demand comparison (RQ2), reliability and expert content-validity assessment (RQ3), and an NLP baseline (RQ5).

## Dataset

| Quantity | Value |
|---|---|
| LinkedIn profiles collected | 611 |
| Profiles included after exclusion criteria | **500** |
| Profiles excluded | 111 |
| Profile × dimension annotation records | 3,000 |
| Job postings collected | **201** |
| Requirement records extracted from postings | **1,558** |
| Profiles independently double-coded | 75 |
| Expert survey respondents | N = 24 |

**No profile-level, posting-level, or respondent-level data is included in this repository.** See [Data and privacy](#data-and-privacy).

## Annotation and scoring

Every included profile was scored on all six dimensions against the frozen rubric, producing 3,000 profile × dimension records. Cases that were structurally ambiguous under the rubric were routed to a human review queue.

| Review activity | Value |
|---|---|
| Records entering the review queue | 685, across 425 profiles |
| Score changes retained after review | 28 |
| — by dimension | D5: 22, D1: 4, D3: 2; D2, D4, D6: 0 |
| Unresolved cases at freeze | 0 |

Every accept, change, and defer decision in the review process was made by the researcher. The annotation dataset was frozen before any analysis was run, and no score was altered afterwards.

## Research questions and methods

| RQ | Data used | Method |
|---|---|---|
| RQ1 | Frozen annotation (500 profiles × 6 dimensions) | Descriptive statistics: distributions, missingness, cross-tabulations |
| RQ2 | 201 postings / 1,558 requirement records + frozen annotation | Aggregate dimension-level demand-versus-supply comparison |
| RQ3 | 75 double-coded profiles + N=24 expert survey | Krippendorff's alpha (ordinal, per dimension, never pooled) + descriptive survey statistics |
| RQ4 | — | Not conducted; criterion data never collected |
| RQ5 | Frozen annotation (gold standard) + profile text features | TF-IDF + Ridge regression, six independent per-dimension models |

## Key findings

### RQ1 — Credential signal distribution (n = 500)

| Dimension | Mean | Median | SD | `unavailable` |
|---|---|---|---|---|
| D1 Formal Education | 2.28 | 3 | 1.59 | 5.8% |
| D2 Professional Certifications | 0.47 | 0 | 0.50 | 53.2% |
| D3 Practical AI Experience | 2.93 | 3 | 1.14 | 0.6% |
| D4 Technical Contributions | 0.95 | 0 | 1.32 | 65.0% |
| D5 Leadership & Strategic Responsibility | 2.91 | 3 | 0.49 | 0.0% |
| D6 AI Industry/Application Breadth | 1.77 | 2 | 0.96 | 0.6% |

D5 is strikingly concentrated: **435 of 500 profiles (87.0%) scored exactly 3**. D2 and D4 are characterised more by absence of observable evidence than by low scores.

### RQ2 — Requirements versus held signals (1,558 requirement records)

**799 of 1,558 requirement records (51.3%) could not be directly mapped to any ALCSM dimension.** This is a finding about the boundary of the instrument — a majority of what employers write in AI leadership postings sits outside what a credential-signal model captures. It is *not* a measured skills gap, and must not be read as one.

Of the requirements that did map:

| Dimension | Requirement records | Share of all 1,558 |
|---|---|---|
| D5 | 436 | 28.0% |
| D3 | 185 | 11.9% |
| D1 | 116 | 7.4% |
| D2 | 17 | 1.1% |
| D4 | 4 | 0.3% |
| D6 | 1 | 0.06% |

**The D6 asymmetry** is the sharpest structural result: industry/application breadth is observable in **497 of 500 profiles (99.4%)** but appears in **1 of 1,558 requirement records (0.06%)**. The dimension is highly visible on the candidate side and almost entirely unstated on the demand side. This is reported as an asymmetry in what is *written down* in postings. It is not evidence that employers do not value industry breadth — posting text is not a measure of employer preference.

### RQ3 — Reliability and content validity

Krippendorff's alpha (ordinal), computed per dimension on the 75 double-coded profiles:

| Dimension | α | Interpretation |
|---|---|---|
| D1 | .944 | High agreement |
| D2 | 1.000 | **Degenerate** — restricted score range, α not interpretable as agreement |
| D3 | .102 | Low agreement |
| D4 | 1.000 | **Degenerate** — restricted score range, α not interpretable as agreement |
| D5 | .246 | Low agreement |
| D6 | 1.000 | Full agreement on a narrow observed range |

These values must not be summarised as uniformly strong. They range from .102 to 1.000 for different and separately diagnosed reasons. Where the observed score range is restricted, alpha is mathematically degenerate rather than evidence of reliable coding — D2 and D4 are explicitly flagged as such. D3's and D5's low values are reported as genuine reliability limitations of those dimensions as currently specified.

Expert survey (N = 24), dimension relevance on a 1–5 scale:

| D1 | D2 | D3 | D4 | D5 | D6 |
|---|---|---|---|---|---|
| 3.54 | 3.25 | 4.33 | 3.54 | 3.63 | 3.67 |

Overall appropriateness of the framework: **3.42 / 5** (median 3, SD 1.06; 45.8% rated 4–5). D3 was most frequently named the single most important dimension (9 of 24 respondents, 37.5%). **These counts were never converted into dimension weights.**

### RQ4 — Not conducted

No analysis, no result, no proxy. See [Research questions](#research-questions).

## NLP baseline (RQ5)

A deliberately simple, **local-only** proof-of-concept: TF-IDF features (max 2,000 features, 1–2 grams, min_df=2, English stop words) into Ridge regression (α=1.0), trained as six independent per-dimension models, with predictions rounded and clipped to [0, 5]. Random seed 42; 80/20 train-test split. No external API was called on any profile text at any point.

| Dim | Exact match | Baseline | Cohen's κ | MAE | Baseline MAE | Test n |
|---|---|---|---|---|---|---|
| D1 | 29.5% | 28.4% | .283 | 0.99 | 1.23 | 95 |
| D2 | 100.0% | 100.0% | 1.000 | 0.00 | 0.00 | 47 |
| D3 | **52.0%** | 35.0% | **.399** | 0.57 | 1.03 | 100 |
| D4 | 62.9% | 71.4% | −.022 | 0.37 | 0.31 | 35 |
| D5 | 87.0% | 87.0% | .260 | 0.15 | 0.17 | 100 |
| D6 | 44.0% | 48.0% | .238 | 0.64 | 0.80 | 100 |

Read against the majority-class baseline, only **D3 clearly beats it**. D2 is degenerate (a single class). D4 and D6 fall *below* their baselines, and D5 merely matches its own — a model that predicts "3" for everyone achieves 87.0% on D5 because 87.0% of profiles score 3.

**This baseline is a proof-of-concept.** It is not production-ready, not deployable, not validated, and not a screening tool. It exists to answer whether any automated signal is present, and the answer is: for one dimension, weakly.

There is no working screening application in this repository. `src/alcsm/app/streamlit_app.py` is an unimplemented stub from a planned phase that was never built; it raises `NotImplementedError` by design. The Streamlit application that *was* built and used is `src/alcsm/app/annotation_app.py`, the researcher-facing annotation review interface.

## Repository structure

```
00_Project_Management/     Project administration
01_Literature_Review/      Literature mapping and annotations
02_Framework_Development/  ALCSM specification, rubric, coding rulebook (incl. v1.1 D6)
03_Database_Design/        ER design, PostgreSQL schema and patch DDL
04_Ethics/                 Ethics, DPIA, LIA, privacy notice, GDPR documentation (drafts)
05_Data_Collection/        Sampling frame, search library, dictionaries, collection protocol
06_Annotation/             Annotation handbook and procedure
07_Reliability/            Double-coding and expert-survey procedure
08_NLP_Development/        NLP baseline design notes
09_Statistical_Analysis/   RQ1/RQ2/RQ3 analysis outputs (aggregate tables and figures)
11_Implementation_Governance/  Decision log, project context, guides, review reports
12_Figures/                Thesis figures
13_Tables/                 Thesis tables
14_Appendix/               Appendix material
15_Scripts/                Runnable analysis entry points
16_Archive/                Superseded artefacts, retained as historical record
src/alcsm/                 Python package (collection, annotation, reliability, analysis, nlp, db, app)
tests/                     Test suite
```

`10_Thesis_Writing/` exists on the author's machine but is excluded from this repository: it holds superseded manuscript drafts and drafting scaffolding, which should not be mistaken for the final research record.

## Reproducibility

The analysis code, framework specification, and aggregate outputs are complete and inspectable. **The analyses cannot be re-executed end-to-end from this repository**, because the underlying profile, posting, and survey data are withheld for privacy reasons (see below). What is reproducible is the logic: every script, transformation, statistic, and model is present and readable, and the aggregate outputs they produced are committed under `09_Statistical_Analysis/`, `12_Figures/`, and `13_Tables/`.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[nlp,reliability,plotting,dev]"
pytest
```

Requires Python 3.11+. `requirements.txt` is a pinned snapshot of the core environment; the optional extras above add scikit-learn, SciPy, and Matplotlib, which the reliability, NLP, and plotting code need.

Analysis entry points live in `15_Scripts/` (RQ1, RQ2, reliability, survey analysis, NLP baseline, results summary). Each expects the withheld source workbooks at the paths named in its own docstring.

Some modules in `src/alcsm/` are explicit stubs for phases that were never implemented (`nlp/classify.py`, `nlp/extract.py`, `taxonomy/anchoring.py`, parts of `db/queries.py`, and `app/streamlit_app.py`). They raise `NotImplementedError` and are retained, tested, and documented as unbuilt scope rather than removed.

## Data and privacy

This repository is public. It contains **no personal data**.

Specifically excluded, and excluded from the repository's history as well:

- LinkedIn profile records, names, profile URLs, and any direct identifier
- Raw or processed profile collection workbooks
- Job posting text and posting-level records
- Individual survey responses, ratings, or free-text answers
- Screenshots, exports, or any material from which a participant could be re-identified
- Any mapping file linking a research ID to a real person

What *is* included is aggregate only: dimension-level distributions, requirement counts, reliability coefficients, survey means, and model performance metrics. A small number of research IDs (e.g. `LP0041`) appear in methodological documentation purely to illustrate how the missing-data framework was applied; these are internal sequence numbers carrying no identifying information and no lookup table for them exists in this repository.

Profile data was handled under the project's data protection documentation in `04_Ethics/`. **Those documents are drafts (v0.1-DRAFT) and are published as a record of the process followed, not as institutional approvals.** As stated in the thesis, the institutional ethics-approval status was subject to final confirmation at the time of writing; accordingly no approval number, approval date, or Data Protection Officer determination is claimed here.

Any example or demonstration data anywhere in this repository is synthetic and labelled as such. The email addresses appearing in `tests/` are fabricated fixtures used to test contact-detail stripping.

## Limitations

- **Single-market, single-platform sample.** German-market LinkedIn profiles only. Findings do not generalise to other labour markets or to professionals who are not active on LinkedIn.
- **Self-presentation bias.** LinkedIn profiles are self-authored marketing documents. ALCSM measures what people choose to display, not what they have done.
- **Title-based sampling excludes the under-signalled.** Locating profiles by leadership title structurally omits capable practitioners who do not hold or advertise such a title.
- **D3 and D5 reliability is low** (α = .102 and .246). Results for these dimensions should be treated as provisional.
- **D2 and D4 alpha values are degenerate**, driven by restricted score ranges rather than by reliable coding.
- **D5 has almost no variance** — 87.0% of profiles score exactly 3 — which limits what any analysis of that dimension can show.
- **51.3% of requirements are unmapped**, bounding how much of employer demand ALCSM can speak to at all.
- **RQ4 was not conducted**, so no criterion validity of any kind has been established.
- **The NLP baseline is a proof-of-concept** that beats a majority-class baseline on one dimension only.
- **ALCSM is not a validated instrument.** It has been constructed and examined; it has not been validated against any external criterion.
- **Single primary annotator.** The first-pass annotation and all review decisions rest with one researcher, with a 75-profile double-coded subset as the only independent check.

## Future research

- Collect the external criterion variables RQ4 required, and conduct the criterion-validity analysis that was planned.
- Revise D3 and D5 rubrics specifically to address their low inter-rater agreement.
- Extend sampling beyond a single national market and beyond a single platform.
- Investigate the 51.3% unmapped requirement corpus directly — what employers ask for that credential signals do not describe is arguably the more interesting question.
- Test whether the D6 supply/demand asymmetry reflects genuine employer indifference or merely a convention of how postings are written.
- Replace the TF-IDF baseline with contextual language models, given a larger annotated corpus.

## Research boundaries

To state plainly what this work does **not** do:

- It does not measure AI leadership ability, competence, capability, or effectiveness.
- It does not produce a composite ALCSM score, an overall score, or a weighted score.
- It does not rank, rate, screen, shortlist, or assess candidates, and must not be used to.
- It does not provide a validated hiring model or a predictive instrument of any kind.
- It does not quantify a skills gap. The 51.3% figure is the share of requirement records that fall outside the instrument's mapping, not a deficit in any population.
- It does not establish employer preferences. Requirement counts describe posting text, not what employers value.
- It does not claim ALCSM has been externally validated.

## Thesis

*The AI Leadership Credential Gap: An NLP Audit of 500 LinkedIn Profiles.*
MSc Applied Data Science and Analytics, SRH Berlin University of Applied Sciences, Hamburg, Germany, 2026.

The submitted thesis is the authoritative source for all research content. Where any document in this repository disagrees with it — and this repository deliberately preserves superseded design documents as a historical record — the thesis governs.

## Citation

```bibtex
@mastersthesis{dhere2026alcsm,
  author  = {Dhere, Samiksha},
  title   = {The {AI} Leadership Credential Gap: An {NLP} Audit of 500 {LinkedIn} Profiles},
  school  = {SRH Berlin University of Applied Sciences, Hamburg},
  year    = {2026},
  type    = {{MSc} thesis},
  note    = {Applied Data Science and Analytics}
}
```

## License

No license has been assigned to this repository yet. Until one is added, all rights are reserved and no permission to reuse, redistribute, or modify this material is granted. If you wish to build on the ALCSM framework or the code here, please contact the author.
