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


# The three gold-standard exemplars set the in-code bar for the
# strand and must always be present. Authored nodes grow as the
# strand is built out; every id added to AUTHORED_NODE_IDS is
# parametrized through validate_literature below.

GOLD_EXEMPLAR_IDS = ("lit-craft-031", "lit-work-001", "lit-work-inh-004")

AUTHORED_NODE_IDS = (
    *GOLD_EXEMPLAR_IDS,
    "lit-craft-001",
    "lit-craft-002",
    "lit-craft-003",
    "lit-craft-004",
    "lit-craft-006",
    "lit-craft-007",
    "lit-craft-008",
    "lit-craft-010",
    "lit-craft-011",
    "lit-craft-012",
    "lit-craft-013",
    "lit-craft-014",
    "lit-craft-020",
    "lit-craft-021",
    "lit-craft-022",
    "lit-craft-023",
    "lit-craft-040",
    "lit-craft-041",
    "lit-craft-042",
    "lit-craft-043",
    "lit-craft-050",
    "lit-craft-051",
    "lit-craft-052",
    "lit-craft-053",
    "lit-work-002",
    "lit-work-003",
    "lit-work-004",
    "lit-work-005",
    "lit-work-006",
    "lit-work-007",
    "lit-work-008",
    "lit-work-009",
    "lit-work-010",
    "lit-work-011",
    "lit-work-012",
    "lit-work-013",
    "lit-work-014",
    "lit-work-015",
    "lit-work-016",
    "lit-work-017",
    "lit-work-018",
    "lit-work-019",
    "lit-work-020",
    "lit-work-021",
    "lit-work-022",
    "lit-work-023",
    "lit-work-024",
    "lit-work-025",
    "lit-work-026",
    "lit-work-027",
    "lit-work-028",
)


class TestAuthoredExemplars:
    def test_gold_exemplars_present(self) -> None:
        assert set(GOLD_EXEMPLAR_IDS).issubset(LITERATURE_MASTERY_CONTENT.keys())

    def test_authored_ids_match_content(self) -> None:
        assert set(AUTHORED_NODE_IDS) == set(LITERATURE_MASTERY_CONTENT.keys())

    @pytest.mark.parametrize("node_id", AUTHORED_NODE_IDS)
    def test_each_node_validates(self, node_id: str) -> None:
        validate_literature(LITERATURE_MASTERY_CONTENT[node_id])

    def test_work_nodes_have_minimum_band(self) -> None:
        for node_id, node in LITERATURE_MASTERY_CONTENT.items():
            if node.get("node_type") == "work":
                assert node.get("minimum_band") in LITERARY_BANDS, node_id

    def test_inheritance_node_has_lineage_and_comparative_threads(self) -> None:
        node = LITERATURE_MASTERY_CONTENT["lit-work-inh-004"]
        assert node.get("track") == "inheritance"
        assert node.get("lineage"), "inheritance node must carry lineage"
        threads = node.get("comparative_threads") or []
        assert threads, "inheritance node must carry non-empty comparative_threads"

    def test_every_node_has_classical_and_charlotte_mason(self) -> None:
        for node_id, node in LITERATURE_MASTERY_CONTENT.items():
            philosophy = node["philosophy"]
            assert "classical" in philosophy, node_id
            assert "charlotte_mason" in philosophy, node_id
            assert isinstance(philosophy["classical"], dict), node_id
            assert isinstance(philosophy["charlotte_mason"], dict), node_id

    def test_no_unschooling_lesson_keys(self) -> None:
        for node_id, node in LITERATURE_MASTERY_CONTENT.items():
            unschooling = node["philosophy"].get("unschooling")
            if isinstance(unschooling, dict):
                forbidden = _UNSCHOOLING_FORBIDDEN_KEYS.intersection(unschooling.keys())
                assert not forbidden, f"{node_id} unschooling has forbidden keys: {sorted(forbidden)}"

    def test_no_node_reproduces_long_in_copyright_passages(self) -> None:
        for node_id, node in LITERATURE_MASTERY_CONTENT.items():
            warnings = validate_literature(node)
            copyright_flags = [w for w in warnings if "in-copyright" in w]
            assert not copyright_flags, f"{node_id} reproduced flagged passage(s): {copyright_flags}"

    def test_montessori_neutralized_with_reason(self) -> None:
        # All three exemplars explicitly mark montessori as neutral
        # rather than authoring a stretched native variant.
        for node_id, node in LITERATURE_MASTERY_CONTENT.items():
            neutral = node.get("philosophy_neutral", {})
            assert "montessori" in neutral, node_id
            assert neutral["montessori"], f"{node_id} montessori neutral lacks a reason"

    def test_lit_craft_031_band_and_prerequisites(self) -> None:
        node = LITERATURE_MASTERY_CONTENT["lit-craft-031"]
        assert node["node_type"] == "craft"
        assert node["band"] == "advanced"
        assert node["prerequisites"] == [
            "lit-craft-008",
            "close reading: proficient",
        ]
        assert node["strand"] == "narrative craft"

    def test_all_prerequisites_resolve_to_authored_nodes(self) -> None:
        # Every craft-node prerequisite must resolve against authored
        # content: either as an explicit node id, or as a
        # "{strand}: {band}" pair that matches exactly one authored
        # craft node. Bands with more than one authored node (e.g.
        # character: developing has both lit-craft-010 and lit-craft-011)
        # are ambiguous and must be disambiguated to a node id.
        authored_ids = set(LITERATURE_MASTERY_CONTENT.keys())
        pair_to_ids: dict[str, set[str]] = {}
        for nid, node in LITERATURE_MASTERY_CONTENT.items():
            if node.get("node_type") != "craft":
                continue
            strand = node.get("strand")
            band = node.get("band")
            if isinstance(strand, str) and isinstance(band, str):
                pair_to_ids.setdefault(f"{strand}: {band}", set()).add(nid)
        for nid, node in LITERATURE_MASTERY_CONTENT.items():
            for prereq in node.get("prerequisites") or []:
                if prereq in authored_ids:
                    continue
                if prereq in pair_to_ids:
                    resolving = pair_to_ids[prereq]
                    assert len(resolving) == 1, (
                        f"{nid} prereq {prereq!r} is ambiguous; resolves to "
                        f"{sorted(resolving)}; use a node id"
                    )
                    continue
                raise AssertionError(
                    f"{nid} prereq {prereq!r} does not resolve to any "
                    "authored node id or strand:band"
                )

    def test_validate_literature_with_registry_emits_no_prereq_warnings(self) -> None:
        for nid, node in LITERATURE_MASTERY_CONTENT.items():
            warnings = validate_literature(node, LITERATURE_MASTERY_CONTENT)
            prereq_warnings = [w for w in warnings if "prerequisite" in w]
            assert not prereq_warnings, f"{nid} produced: {prereq_warnings}"

    def test_lit_work_001_is_public_domain_classics(self) -> None:
        node = LITERATURE_MASTERY_CONTENT["lit-work-001"]
        assert node["track"] == "classics"
        assert node["work"]["author"] == "Homer"
        assert node["minimum_band"] == "developing"

    def test_lit_work_inh_004_is_inheritance(self) -> None:
        node = LITERATURE_MASTERY_CONTENT["lit-work-inh-004"]
        assert node["track"] == "inheritance"
        assert node["work"]["author"] == "J.R.R. Tolkien"
        assert node["minimum_band"] == "proficient"
        assert "Beowulf" in node["lineage"]
