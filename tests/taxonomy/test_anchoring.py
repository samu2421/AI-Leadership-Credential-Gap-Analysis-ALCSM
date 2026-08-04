"""Tests for the taxonomy-anchoring infrastructure (Phase P3 Session 2).

Two layers, tested separately (mirrors the module's own split):

- Pure-logic validation tests for `TaxonomyVersionRecord`/
  `TaxonomyTermRecord` — no database required.
- DB-integration tests for `create_taxonomy_version`,
  `insert_taxonomy_terms`, `freeze_taxonomy_version` against the
  shared throwaway PostgreSQL 16 cluster (tests/conftest.py) — never
  against `alcsm_dev`, never with real posting text
  (CLAUDE_CODE_RULES.md rule 6).

`anchor_taxonomy_from_postings` (the generation layer) remains
unimplemented this session — its one test confirms the interface
exists and correctly refuses to run, not that it produces any term.
"""

from __future__ import annotations

from datetime import UTC, datetime

import psycopg2
import pytest

from alcsm.taxonomy.anchoring import (
    AnchoringConfig,
    TaxonomyTermRecord,
    TaxonomyValidationError,
    TaxonomyVersionRecord,
    anchor_taxonomy_from_postings,
    create_taxonomy_version,
    freeze_taxonomy_version,
    insert_taxonomy_terms,
    validate_taxonomy_term,
    validate_taxonomy_version,
)


def _valid_version(**overrides: object) -> TaxonomyVersionRecord:
    # `version_label` defaults to the (unique-per-test) taxonomy_version_id
    # itself: the schema enforces UNIQUE(taxonomy_name, version_label), and
    # every test in this module uses `taxonomy_name="ai_role"` by default,
    # so a fixed literal like "1.0" would collide across tests sharing the
    # session-scoped throwaway database.
    taxonomy_version_id = overrides.get("taxonomy_version_id", "TAX-0001")
    defaults: dict[str, object] = dict(
        taxonomy_version_id=taxonomy_version_id,
        taxonomy_name="ai_role",
        version_label=str(taxonomy_version_id),
        constructed_ts=datetime.now(UTC),
    )
    defaults.update(overrides)
    return TaxonomyVersionRecord(**defaults)  # type: ignore[arg-type]


def _valid_term(**overrides: object) -> TaxonomyTermRecord:
    defaults: dict[str, object] = dict(
        taxonomy_version_id="TAX-0001",
        term="machine learning engineer",
        tier_or_band=None,
        source_frequency=3,
    )
    defaults.update(overrides)
    return TaxonomyTermRecord(**defaults)  # type: ignore[arg-type]


class TestValidateTaxonomyVersion:
    def test_valid_version_has_no_problems(self) -> None:
        assert validate_taxonomy_version(_valid_version()) == []

    def test_missing_taxonomy_version_id_is_reported(self) -> None:
        errs = validate_taxonomy_version(_valid_version(taxonomy_version_id=""))
        assert any("taxonomy_version_id" in e for e in errs)

    def test_missing_version_label_is_reported(self) -> None:
        errs = validate_taxonomy_version(_valid_version(version_label=""))
        assert any("version_label" in e for e in errs)

    @pytest.mark.parametrize(
        "valid_name",
        [
            "degree",
            "certification",
            "ai_role",
            "leadership_level",
            "technical_contribution",
            "professional_engagement",
            "ai_keyword_ontology",
            "automation_augmentation",
        ],
    )
    def test_all_eight_frozen_taxonomy_names_are_accepted(
        self, valid_name: str
    ) -> None:
        errs = validate_taxonomy_version(_valid_version(taxonomy_name=valid_name))
        assert errs == []

    def test_invented_taxonomy_name_is_rejected(self) -> None:
        """PROJECT_CONTEXT.md §27: the eight taxonomies are frozen — no
        ninth one may be invented, not even as a typo."""
        errs = validate_taxonomy_version(
            _valid_version(taxonomy_name="soft_skills")  # type: ignore[arg-type]
        )
        assert any("frozen taxonomies" in e for e in errs)


class TestValidateTaxonomyTerm:
    def test_valid_term_has_no_problems(self) -> None:
        assert validate_taxonomy_term(_valid_term()) == []

    @pytest.mark.parametrize("empty_term", ["", "   "])
    def test_empty_term_is_rejected(self, empty_term: str) -> None:
        errs = validate_taxonomy_term(_valid_term(term=empty_term))
        assert any("term must be non-empty" in e for e in errs)

    def test_negative_source_frequency_is_rejected(self) -> None:
        errs = validate_taxonomy_term(_valid_term(source_frequency=-1))
        assert any("source_frequency" in e for e in errs)

    def test_none_source_frequency_is_accepted(self) -> None:
        """A term added a priori (not from anchoring) carries no
        frequency (schema column comment) — this must not be an error."""
        assert validate_taxonomy_term(_valid_term(source_frequency=None)) == []


class TestAnchoringConfig:
    def test_default_minimum_source_frequency_is_one(self) -> None:
        assert AnchoringConfig().minimum_source_frequency == 1

    def test_minimum_source_frequency_is_configurable(self) -> None:
        assert AnchoringConfig(minimum_source_frequency=5).minimum_source_frequency == 5


class TestAnchorTaxonomyFromPostingsIsNotImplemented:
    def test_anchor_taxonomy_from_postings_raises_not_implemented(self) -> None:
        with pytest.raises(NotImplementedError):
            anchor_taxonomy_from_postings(postings=[], taxonomy_name="ai_role")

    def test_signature_accepts_an_explicit_config(self) -> None:
        """The interface accepts a config object without needing it to
        do anything yet — confirms the signature Task 6 asked for
        exists, independent of the (deliberately unimplemented) body."""
        with pytest.raises(NotImplementedError):
            anchor_taxonomy_from_postings(
                postings=[],
                taxonomy_name="certification",
                config=AnchoringConfig(minimum_source_frequency=2),
            )


class TestCreateTaxonomyVersion:
    def test_create_taxonomy_version_inserts_a_new_row(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_taxonomy_version_id: str,
    ) -> None:
        record = _valid_version(taxonomy_version_id=unique_taxonomy_version_id)
        cur = db_connection.cursor()
        inserted = create_taxonomy_version(cur, record)
        db_connection.commit()
        cur.close()
        assert inserted is True

    def test_create_taxonomy_version_is_idempotent(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_taxonomy_version_id: str,
    ) -> None:
        record = _valid_version(taxonomy_version_id=unique_taxonomy_version_id)
        cur = db_connection.cursor()
        first = create_taxonomy_version(cur, record)
        db_connection.commit()
        second = create_taxonomy_version(cur, record)
        db_connection.commit()
        cur.close()
        assert first is True
        assert second is False

    def test_new_version_defaults_to_unfrozen(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_taxonomy_version_id: str,
    ) -> None:
        record = _valid_version(taxonomy_version_id=unique_taxonomy_version_id)
        cur = db_connection.cursor()
        create_taxonomy_version(cur, record)
        db_connection.commit()
        cur.execute(
            "SELECT frozen FROM alcsm.taxonomy_version WHERE taxonomy_version_id=%s",
            (unique_taxonomy_version_id,),
        )
        (frozen,) = cur.fetchone()
        cur.close()
        assert frozen is False

    def test_invalid_version_is_rejected_before_touching_the_database(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        record = _valid_version(taxonomy_version_id="")
        cur = db_connection.cursor()
        with pytest.raises(TaxonomyValidationError):
            create_taxonomy_version(cur, record)
        cur.close()


class TestInsertTaxonomyTerms:
    def test_insert_terms_returns_count_inserted(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_taxonomy_version_id: str,
    ) -> None:
        cur = db_connection.cursor()
        create_taxonomy_version(
            cur, _valid_version(taxonomy_version_id=unique_taxonomy_version_id)
        )
        db_connection.commit()
        cur.close()

        terms = [
            _valid_term(
                taxonomy_version_id=unique_taxonomy_version_id, term="term one"
            ),
            _valid_term(
                taxonomy_version_id=unique_taxonomy_version_id, term="term two"
            ),
        ]
        count = insert_taxonomy_terms(db_connection, terms)
        assert count == 2

    def test_empty_term_list_is_a_no_op(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        assert insert_taxonomy_terms(db_connection, []) == 0

    def test_duplicate_term_in_same_version_is_rejected_by_the_database(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_taxonomy_version_id: str,
    ) -> None:
        cur = db_connection.cursor()
        create_taxonomy_version(
            cur, _valid_version(taxonomy_version_id=unique_taxonomy_version_id)
        )
        db_connection.commit()
        cur.close()

        insert_taxonomy_terms(
            db_connection,
            [_valid_term(taxonomy_version_id=unique_taxonomy_version_id)],
        )
        with pytest.raises(psycopg2.errors.UniqueViolation):
            insert_taxonomy_terms(
                db_connection,
                [_valid_term(taxonomy_version_id=unique_taxonomy_version_id)],
            )

    def test_invalid_term_never_reaches_the_database(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_taxonomy_version_id: str,
    ) -> None:
        cur = db_connection.cursor()
        create_taxonomy_version(
            cur, _valid_version(taxonomy_version_id=unique_taxonomy_version_id)
        )
        db_connection.commit()
        cur.close()

        with pytest.raises(TaxonomyValidationError):
            insert_taxonomy_terms(
                db_connection,
                [_valid_term(taxonomy_version_id=unique_taxonomy_version_id, term="")],
            )
        cur = db_connection.cursor()
        cur.execute(
            "SELECT count(*) FROM alcsm.taxonomy_term WHERE taxonomy_version_id=%s",
            (unique_taxonomy_version_id,),
        )
        (count,) = cur.fetchone()
        cur.close()
        assert count == 0

    def test_terms_for_nonexistent_version_are_rejected(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        with pytest.raises(TaxonomyValidationError):
            insert_taxonomy_terms(
                db_connection,
                [_valid_term(taxonomy_version_id="TAX-DOES-NOT-EXIST")],
            )


class TestFrozenVersionNeverEdited:
    """PROJECT_CONTEXT.md §27, §37: "never invent unevidenced terms;
    edit a frozen version" — the single highest-value test in this
    module (P3_Session1_Test_Strategy.md §2), since the schema itself
    cannot express this cross-table rule as a CHECK constraint. This
    is purely an application-layer guarantee.
    """

    def test_freeze_taxonomy_version_returns_true_on_first_freeze(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_taxonomy_version_id: str,
    ) -> None:
        cur = db_connection.cursor()
        create_taxonomy_version(
            cur, _valid_version(taxonomy_version_id=unique_taxonomy_version_id)
        )
        db_connection.commit()
        cur.close()

        assert (
            freeze_taxonomy_version(db_connection, unique_taxonomy_version_id) is True
        )

    def test_freeze_taxonomy_version_returns_false_on_second_freeze(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_taxonomy_version_id: str,
    ) -> None:
        cur = db_connection.cursor()
        create_taxonomy_version(
            cur, _valid_version(taxonomy_version_id=unique_taxonomy_version_id)
        )
        db_connection.commit()
        cur.close()

        freeze_taxonomy_version(db_connection, unique_taxonomy_version_id)
        assert (
            freeze_taxonomy_version(db_connection, unique_taxonomy_version_id) is False
        )

    def test_freeze_nonexistent_version_raises(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        with pytest.raises(TaxonomyValidationError):
            freeze_taxonomy_version(db_connection, "TAX-DOES-NOT-EXIST")

    def test_inserting_a_term_into_a_frozen_version_is_rejected(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_taxonomy_version_id: str,
    ) -> None:
        cur = db_connection.cursor()
        create_taxonomy_version(
            cur, _valid_version(taxonomy_version_id=unique_taxonomy_version_id)
        )
        db_connection.commit()
        cur.close()

        freeze_taxonomy_version(db_connection, unique_taxonomy_version_id)

        with pytest.raises(TaxonomyValidationError) as exc_info:
            insert_taxonomy_terms(
                db_connection,
                [_valid_term(taxonomy_version_id=unique_taxonomy_version_id)],
            )
        assert any("frozen" in p for p in exc_info.value.problems)

    def test_rejected_insert_into_frozen_version_leaves_no_partial_rows(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_taxonomy_version_id: str,
    ) -> None:
        cur = db_connection.cursor()
        create_taxonomy_version(
            cur, _valid_version(taxonomy_version_id=unique_taxonomy_version_id)
        )
        db_connection.commit()
        cur.close()
        freeze_taxonomy_version(db_connection, unique_taxonomy_version_id)

        with pytest.raises(TaxonomyValidationError):
            insert_taxonomy_terms(
                db_connection,
                [
                    _valid_term(
                        taxonomy_version_id=unique_taxonomy_version_id, term="a"
                    ),
                    _valid_term(
                        taxonomy_version_id=unique_taxonomy_version_id, term="b"
                    ),
                ],
            )
        cur = db_connection.cursor()
        cur.execute(
            "SELECT count(*) FROM alcsm.taxonomy_term WHERE taxonomy_version_id=%s",
            (unique_taxonomy_version_id,),
        )
        (count,) = cur.fetchone()
        cur.close()
        assert count == 0
