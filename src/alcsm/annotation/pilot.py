"""Pilot / double-coding subset selection mechanism.

This module provides the SELECTION MECHANISM only. It never chooses,
hardcodes, or suggests which real profiles constitute the actual P4
pilot or the P6 double-coding subset -- that is the researcher's
decision, made later, once P2/P3 clear (this task's explicit "DO NOT
choose the final pilot sample automatically" instruction). Every
function here takes the candidate profile IDs as an argument; none of
them read the real dataset themselves.

Implements the frozen double-coding policy verbatim (CLAUDE_CODE_
IMPLEMENTATION_GUIDE.md §15): "100% double coding if feasible;
otherwise a pre-registered random subset of at least 15%." A sampled
subset must be random and pre-registered (method + seed recorded) --
this module makes that recording structural (the seed and method are
fields on the returned object, not side information the caller must
remember to write down).
"""

from __future__ import annotations

import random
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime

_MINIMUM_SUBSET_FRACTION = 0.15  # CLAUDE_CODE_IMPLEMENTATION_GUIDE.md §15, frozen


class PilotSelectionError(ValueError):
    """Raised when a requested selection would violate the frozen
    double-coding policy."""


@dataclass(frozen=True)
class PilotSelection:
    """A reproducible record of one pilot/subset selection.

    Every field here is exactly what a pre-registration needs to
    reproduce the same selection later: ``method`` and ``seed`` are
    sufficient to regenerate ``selected_profile_ids`` deterministically
    from the same ``candidate_pool`` (see :func:`select_pilot_subset`'s
    docstring for the reproduction recipe).
    """

    method: str  # "full" or "random_subset"
    seed: int | None
    fraction: float | None
    candidate_pool_size: int
    selected_profile_ids: tuple[str, ...]
    selected_at: datetime

    @property
    def actual_fraction(self) -> float:
        if self.candidate_pool_size == 0:
            return 0.0
        return len(self.selected_profile_ids) / self.candidate_pool_size


def select_pilot_subset(
    candidate_profile_ids: Sequence[str],
    method: str,
    seed: int | None = None,
    fraction: float = _MINIMUM_SUBSET_FRACTION,
) -> PilotSelection:
    """Select a double-coding subset per the frozen policy.

    ``method``:
        - ``"full"`` -- every candidate profile is selected (100%
          double coding). ``seed``/``fraction`` are ignored.
        - ``"random_subset"`` -- a reproducible random sample of
          ``fraction`` of ``candidate_profile_ids`` (must be >= 0.15,
          the frozen minimum), using Python's ``random.Random(seed)``
          so the exact same ``seed`` against the exact same
          ``candidate_profile_ids`` (in the same order) always
          reproduces the same selection -- this is the whole point of
          "pre-registered": the method and seed, recorded once, are
          sufficient for anyone to verify the selection later.

    Raises :class:`PilotSelectionError` for an unknown method, a
    ``fraction`` below the frozen 15% minimum, a missing ``seed`` for
    ``"random_subset"``, or an empty candidate pool.
    """
    if not candidate_profile_ids:
        raise PilotSelectionError("candidate_profile_ids must not be empty")

    if method == "full":
        return PilotSelection(
            method="full",
            seed=None,
            fraction=1.0,
            candidate_pool_size=len(candidate_profile_ids),
            selected_profile_ids=tuple(candidate_profile_ids),
            selected_at=datetime.now(),
        )

    if method == "random_subset":
        if fraction < _MINIMUM_SUBSET_FRACTION:
            raise PilotSelectionError(
                f"fraction={fraction} is below the frozen minimum "
                f"{_MINIMUM_SUBSET_FRACTION} (CLAUDE_CODE_IMPLEMENTATION_"
                "GUIDE.md §15: 'a pre-registered random subset of at "
                "least 15%')"
            )
        if seed is None:
            raise PilotSelectionError(
                "seed is required for method='random_subset' -- a "
                "pre-registered subset must be reproducible"
            )
        pool = list(candidate_profile_ids)
        n = max(1, round(len(pool) * fraction))
        rng = random.Random(seed)
        selected = rng.sample(pool, k=n)
        return PilotSelection(
            method="random_subset",
            seed=seed,
            fraction=fraction,
            candidate_pool_size=len(pool),
            selected_profile_ids=tuple(selected),
            selected_at=datetime.now(),
        )

    raise PilotSelectionError(
        f"unknown method {method!r}; must be 'full' or 'random_subset'"
    )
