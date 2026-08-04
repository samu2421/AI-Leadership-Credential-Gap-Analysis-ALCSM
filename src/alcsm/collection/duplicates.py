"""Deterministic, in-memory, session-local duplicate-detection utilities.

Implements the transient duplicate check already specified in
Task5_P3_Sampling_Framework_Design.md §8 and §6 of the job-posting
counterpart: before a candidate profile or posting is captured, the
collector confirms it is not already represented in the sample, using
a working set discarded at the end of the session — never persisted
into the research database (the schema itself stores no name, URL, or
other discriminator that would make a persistent duplicate-check index
possible or desirable, PROJECT_CONTEXT.md §45).

Deliberately NOT semantic: matching is exact-string or normalised-
string only (case/whitespace/punctuation folding). No fuzzy matching,
no embeddings, no NLP of any kind — Task 3's explicit boundary. A
title normalisation function is included because "normalised titles
where appropriate" was asked for, but it is pure string
transformation, not language understanding.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_WHITESPACE_PATTERN = re.compile(r"\s+")
_PUNCTUATION_PATTERN = re.compile(r"[^\w\s]")


def normalize_title(raw: str) -> str:
    """Fold a title to a comparable canonical form.

    Deterministic string transformation only: casefold, strip
    punctuation, collapse whitespace. Does not attempt to resolve
    synonyms or paraphrases (e.g. "Head of AI" vs "Head of Artificial
    Intelligence") — that mapping, where it exists, is a pre-registered
    variant list applied by a human collector
    (Task5_P3_Sampling_Framework_Design.md §3), not something this
    function infers.
    """
    folded = raw.casefold()
    folded = _PUNCTUATION_PATTERN.sub(" ", folded)
    folded = _WHITESPACE_PATTERN.sub(" ", folded).strip()
    return folded


@dataclass(frozen=True)
class DuplicateCandidate:
    """The signals available to check one candidate record for
    duplication before it is captured. Every field is optional since
    profiles carry none of the posting-specific identifiers (no URL,
    no external listing id — forbidden by the frozen privacy design),
    while postings may carry some or all of them depending on what the
    source exposes.
    """

    source: str | None = None
    external_id: str | None = None
    url: str | None = None
    title: str | None = None


@dataclass(frozen=True)
class DuplicateCheckResult:
    """Outcome of checking one candidate against the session registry."""

    is_duplicate: bool
    matched_on: str | None = None
    matched_key: str | None = None


class DuplicateRegistry:
    """A session-local, in-memory registry of already-seen candidates.

    Never persisted to the database or to disk by this class itself —
    a caller who needs an audit trail of exclusions logs that
    separately (see ``collection.audit``); this registry's state is
    discarded when the process/session ends, matching the frozen
    design's "transient, session-local" requirement exactly.

    Checks, in order, the most specific available signal first:
    ``(source, external_id)``, then ``url``, then normalised
    ``title``. The first match found is reported; a candidate with no
    signals at all is never flagged as a duplicate (nothing to compare).
    """

    def __init__(self) -> None:
        self._external_ids: set[tuple[str, str]] = set()
        self._urls: set[str] = set()
        self._normalized_titles: set[str] = set()

    def check(self, candidate: DuplicateCandidate) -> DuplicateCheckResult:
        """Return whether ``candidate`` matches anything already registered.

        Does not modify the registry — call :meth:`register` separately
        once the candidate is actually included, so a rejected/excluded
        candidate never pollutes future checks.
        """
        if candidate.source and candidate.external_id:
            key = (candidate.source, candidate.external_id)
            if key in self._external_ids:
                return DuplicateCheckResult(
                    is_duplicate=True,
                    matched_on="source_external_id",
                    matched_key=f"{candidate.source}:{candidate.external_id}",
                )

        if candidate.url and candidate.url in self._urls:
            return DuplicateCheckResult(
                is_duplicate=True, matched_on="url", matched_key=candidate.url
            )

        if candidate.title:
            normalized = normalize_title(candidate.title)
            if normalized and normalized in self._normalized_titles:
                return DuplicateCheckResult(
                    is_duplicate=True,
                    matched_on="normalized_title",
                    matched_key=normalized,
                )

        return DuplicateCheckResult(is_duplicate=False)

    def register(self, candidate: DuplicateCandidate) -> None:
        """Record ``candidate`` as seen, for future :meth:`check` calls."""
        if candidate.source and candidate.external_id:
            self._external_ids.add((candidate.source, candidate.external_id))
        if candidate.url:
            self._urls.add(candidate.url)
        if candidate.title:
            normalized = normalize_title(candidate.title)
            if normalized:
                self._normalized_titles.add(normalized)

    def __len__(self) -> int:
        """Number of distinct signals registered (not distinct
        candidates — a candidate can register up to three signals)."""
        return len(self._external_ids) + len(self._urls) + len(self._normalized_titles)
