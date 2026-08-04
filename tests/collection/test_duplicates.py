"""Pure-logic tests for deterministic, session-local duplicate detection.

No database required. No NLP: matching is exact/normalised-string
only — these tests explicitly confirm semantically-similar-but-
differently-worded titles are NOT flagged as duplicates (Task 3's
"do not infer semantic duplicates" boundary).
"""

from __future__ import annotations

from alcsm.collection.duplicates import (
    DuplicateCandidate,
    DuplicateRegistry,
    normalize_title,
)


class TestNormalizeTitle:
    def test_casefolds(self) -> None:
        assert normalize_title("Chief AI Officer") == normalize_title(
            "CHIEF ai officer"
        )

    def test_collapses_whitespace(self) -> None:
        assert normalize_title("Head   of\tAI") == normalize_title("Head of AI")

    def test_strips_punctuation(self) -> None:
        assert normalize_title("Head of AI!") == normalize_title("Head of AI")

    def test_decorative_punctuation_and_emoji_are_folded_to_whitespace(self) -> None:
        assert normalize_title("Jane | Chief AI Officer 🚀") == "jane chief ai officer"


class TestDuplicateRegistryExternalId:
    def test_first_registration_is_not_a_duplicate(self) -> None:
        registry = DuplicateRegistry()
        candidate = DuplicateCandidate(source="board_a", external_id="12345")
        result = registry.check(candidate)
        assert result.is_duplicate is False

    def test_same_source_and_external_id_is_a_duplicate(self) -> None:
        registry = DuplicateRegistry()
        candidate = DuplicateCandidate(source="board_a", external_id="12345")
        registry.register(candidate)
        result = registry.check(candidate)
        assert result.is_duplicate is True
        assert result.matched_on == "source_external_id"

    def test_same_external_id_different_source_is_not_a_duplicate(self) -> None:
        registry = DuplicateRegistry()
        registry.register(DuplicateCandidate(source="board_a", external_id="12345"))
        result = registry.check(
            DuplicateCandidate(source="board_b", external_id="12345")
        )
        assert result.is_duplicate is False


class TestDuplicateRegistryUrl:
    def test_same_url_is_a_duplicate(self) -> None:
        registry = DuplicateRegistry()
        url = "https://example-board.test/jobs/98765"
        registry.register(DuplicateCandidate(url=url))
        result = registry.check(DuplicateCandidate(url=url))
        assert result.is_duplicate is True
        assert result.matched_on == "url"

    def test_different_url_is_not_a_duplicate(self) -> None:
        registry = DuplicateRegistry()
        registry.register(DuplicateCandidate(url="https://example.test/1"))
        result = registry.check(DuplicateCandidate(url="https://example.test/2"))
        assert result.is_duplicate is False


class TestDuplicateRegistryNormalizedTitle:
    def test_same_title_different_case_is_a_duplicate(self) -> None:
        registry = DuplicateRegistry()
        registry.register(DuplicateCandidate(title="Head of AI"))
        result = registry.check(DuplicateCandidate(title="HEAD OF AI"))
        assert result.is_duplicate is True
        assert result.matched_on == "normalized_title"

    def test_semantically_similar_but_different_title_is_not_a_duplicate(
        self,
    ) -> None:
        """Explicit boundary check: 'Head of AI' and 'Head of Artificial
        Intelligence' are conceptually the same role but are NOT
        string-identical after normalisation — this function must not
        infer that equivalence (that is a pre-registered human variant
        mapping, not something this deterministic utility decides)."""
        registry = DuplicateRegistry()
        registry.register(DuplicateCandidate(title="Head of AI"))
        result = registry.check(
            DuplicateCandidate(title="Head of Artificial Intelligence")
        )
        assert result.is_duplicate is False


class TestDuplicateRegistryNoSignals:
    def test_candidate_with_no_signals_is_never_a_duplicate(self) -> None:
        registry = DuplicateRegistry()
        registry.register(DuplicateCandidate())
        result = registry.check(DuplicateCandidate())
        assert result.is_duplicate is False


class TestDuplicateRegistryCheckDoesNotMutate:
    def test_check_alone_does_not_register(self) -> None:
        registry = DuplicateRegistry()
        candidate = DuplicateCandidate(title="Director of AI")
        registry.check(candidate)  # not registered
        result = registry.check(candidate)
        assert result.is_duplicate is False

    def test_len_reflects_registered_signals_not_checks(self) -> None:
        registry = DuplicateRegistry()
        candidate = DuplicateCandidate(
            source="board_a", external_id="1", url="https://x.test/1", title="AI Lead"
        )
        registry.check(candidate)
        assert len(registry) == 0
        registry.register(candidate)
        assert len(registry) == 3
