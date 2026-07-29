"""NLP pipeline: extract -> classify -> evaluate, per dimension.

Hard privacy rule (PROJECT_CONTEXT.md §25, §46; CLAUDE_CODE_RULES.md
rule 8): no external-API processing of LinkedIn profile text. Local
models only (spaCy, sentence-transformers, HuggingFace run locally or
on approved EEA-resident infrastructure).

Cannot be trained before a human gold standard exists (Phase P6) and
taxonomies are anchored (Phase P3).
"""
