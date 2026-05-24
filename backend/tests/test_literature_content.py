"""Tests for the literary mastery strand: schema, validation, and
the authored exemplars.

Covers:
- NODE_CONTENT_SCHEMA documents literary_craft_node and literary_work_node.
- validate_literature accepts well-formed craft and work nodes.
- validate_literature raises on the hard violations: a work node
  missing minimum_band, an inheritance work missing lineage or with
  empty comparative_threads, a node whose philosophy lacks classical
  or charlotte_mason, an unschooling variant carrying a lesson,
  sequence, or graded-assessment key.
- validate_literature warns when an in-copyright work carries an
  oversized close_reading_passages entry, and stays silent for public-
  domain works.
"""

import pytest

from app.content.literature_mastery_content import LITERATURE_MASTERY_CONTENT
from app.services.node_content import (
    _UNSCHOOLING_FORBIDDEN_KEYS,
    LITERARY_BANDS,
    LITERARY_TRACKS,
    NODE_CONTENT_SCHEMA,
    validate_literature,
)


def _minimal_craft_node(**overrides: object) -> dict:
    base: dict = {
        "node_type": "craft",
        "strand": "narrative craft",
        "band": "advanced",
        "prerequisites": [],
        "objective": "x",
        "core_understanding": "y",
        "analytical_moves": [],
        "seminar_questions": [],
        "writing_invitations": [],
        "exemplar_texts": [],
        "philosophy": {
            "classical": {"narrative_introduction": "x"},
            "charlotte_mason": {"short_lesson_flow": "x"},
        },
        "philosophy_neutral": {},
    }
    base.update(overrides)
    return base


def _minimal_work_node(**overrides: object) -> dict:
    base: dict = {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "X",
            "author": "Y",
            "date": "c. 800 BCE",
            "genre": "epic",
            "form": "epic poem",
        },
        "minimum_band": "developing",
        "content_notes": "",
        "craft_focus": [],
        "entry": "",
        "close_reading_passages": [],
        "structural_analysis": "",
        "thematic_lines": [],
        "comparative_threads": [],
        "seminar_questions": [],
        "writing_invitations": [],
        "context": "",
        "philosophy": {
            "classical": {"narrative_introduction": "x"},
            "charlotte_mason": {"short_lesson_flow": "x"},
        },
        "philosophy_neutral": {},
    }
    base.update(overrides)
    return base


class TestSchemaDocumentation:
    def test_literary_craft_node_documented(self) -> None:
        assert "literary_craft_node" in NODE_CONTENT_SCHEMA
        assert NODE_CONTENT_SCHEMA["literary_craft_node"]["node_type"] == "craft"

    def test_literary_work_node_documented(self) -> None:
        assert "literary_work_node" in NODE_CONTENT_SCHEMA
        assert NODE_CONTENT_SCHEMA["literary_work_node"]["node_type"] == "work"

    def test_bands_and_tracks_exported(self) -> None:
        assert frozenset({"emerging", "developing", "proficient", "advanced", "mastery"}) == LITERARY_BANDS
        assert frozenset({"classics", "inheritance"}) == LITERARY_TRACKS


class TestValidateLiteratureBasics:
    def test_minimal_craft_node_passes(self) -> None:
        assert validate_literature(_minimal_craft_node()) == []

    def test_minimal_classics_work_node_passes(self) -> None:
        assert validate_literature(_minimal_work_node()) == []

    def test_minimal_inheritance_work_node_passes(self) -> None:
        node = _minimal_work_node(track="inheritance", lineage="x", comparative_threads=["x"])
        assert validate_literature(node) == []

    def test_non_dict_content_raises(self) -> None:
        with pytest.raises(ValueError, match="must be a dict"):
            validate_literature("not a dict")  # type: ignore[arg-type]

    def test_unknown_node_type_raises(self) -> None:
        with pytest.raises(ValueError, match="node_type"):
            validate_literature({"node_type": "mystery", "philosophy": {}})


class TestValidateLiteratureHardChecks:
    def test_work_node_missing_minimum_band_raises(self) -> None:
        node = _minimal_work_node()
        del node["minimum_band"]
        with pytest.raises(ValueError, match="minimum_band"):
            validate_literature(node)

    def test_inheritance_work_missing_lineage_raises(self) -> None:
        node = _minimal_work_node(track="inheritance", comparative_threads=["x"])
        with pytest.raises(ValueError, match="lineage"):
            validate_literature(node)

    def test_inheritance_work_empty_comparative_threads_raises(self) -> None:
        node = _minimal_work_node(track="inheritance", lineage="x")
        with pytest.raises(ValueError, match="comparative_threads"):
            validate_literature(node)

    def test_node_missing_classical_raises(self) -> None:
        node = _minimal_craft_node()
        node["philosophy"] = {"charlotte_mason": {"short_lesson_flow": "x"}}
        with pytest.raises(ValueError, match="classical"):
            validate_literature(node)

    def test_node_missing_charlotte_mason_raises(self) -> None:
        node = _minimal_craft_node()
        node["philosophy"] = {"classical": {"narrative_introduction": "x"}}
        with pytest.raises(ValueError, match="charlotte_mason"):
            validate_literature(node)

    def test_non_dict_philosophy_raises(self) -> None:
        node = _minimal_craft_node()
        node["philosophy"] = ["not a dict"]
        with pytest.raises(ValueError, match="philosophy must be a dict"):
            validate_literature(node)

    def test_unschooling_variant_with_lesson_keys_raises(self) -> None:
        node = _minimal_craft_node()
        node["philosophy"]["unschooling"] = {
            "invitations": [],
            "mastery_check": ["bad"],
        }
        with pytest.raises(ValueError, match="unschooling variant"):
            validate_literature(node)


class TestCopyrightWarnings:
    def test_in_copyright_long_close_reading_passage_warns(self) -> None:
        node = _minimal_work_node(track="inheritance", lineage="x", comparative_threads=["x"])
        node["work"]["date"] = "1954-55"
        node["close_reading_passages"] = ["a" * 500]
        warnings = validate_literature(node)
        assert any("in-copyright" in w for w in warnings)

    def test_public_domain_long_passage_does_not_warn_for_copyright(self) -> None:
        node = _minimal_work_node()
        node["work"]["date"] = "c. 800 BCE"
        node["close_reading_passages"] = ["a" * 2000]
        warnings = validate_literature(node)
        assert not any("in-copyright" in w for w in warnings)

    def test_in_copyright_short_passage_does_not_warn(self) -> None:
        node = _minimal_work_node(track="inheritance", lineage="x", comparative_threads=["x"])
        node["work"]["date"] = "1954-55"
        node["close_reading_passages"] = ["a short referenced passage"]
        warnings = validate_literature(node)
        assert not any("in-copyright" in w for w in warnings)

    def test_unknown_band_warns(self) -> None:
        node = _minimal_craft_node(band="ultraviolet")
        warnings = validate_literature(node)
        assert any("band" in w for w in warnings)

    def test_unknown_track_warns(self) -> None:
        node = _minimal_work_node(track="oddities")
        warnings = validate_literature(node)
        assert any("track" in w for w in warnings)


class TestContentDictExists:
    def test_content_dict_importable(self) -> None:
        assert isinstance(LITERATURE_MASTERY_CONTENT, dict)

    def test_unschooling_forbidden_keys_set_available(self) -> None:
        # Sanity: the same forbidden-keys set used inside the literary
        # validator is the one exported from node_content.
        assert "mastery_check" in _UNSCHOOLING_FORBIDDEN_KEYS
        assert "gradual_release" in _UNSCHOOLING_FORBIDDEN_KEYS
