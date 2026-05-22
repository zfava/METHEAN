"""Tests for node content schema and validation.

Covers:
- NODE_CONTENT_SCHEMA documents the full content shape.
- validate_media flags media and passage warnings without raising.
- validate_content keeps its required-field behavior.
- validate_philosophy warns on legacy strings and hard-fails an
  unschooling variant carrying a lesson/sequence/assessment key.
- The authored reference nodes mf-01 through mf-08 and rf-01 through
  rf-06 carry native variants for all five philosophies.
"""

import pytest

from app.content.history_foundational_content import HISTORY_FOUNDATIONAL_CONTENT
from app.content.math_foundational_content import MATH_FOUNDATIONAL_CONTENT
from app.content.reading_foundational_content import READING_FOUNDATIONAL_CONTENT
from app.content.science_foundational_content import SCIENCE_FOUNDATIONAL_CONTENT
from app.services.node_content import (
    NODE_CONTENT_SCHEMA,
    validate_content,
    validate_media,
    validate_philosophy,
    validate_widgets,
)

PHILOSOPHIES = ("traditional", "classical", "charlotte_mason", "montessori", "unschooling")

# The distinctive native top-level keys each philosophy variant carries.
NATIVE_KEYS: dict[str, set[str]] = {
    "traditional": {
        "introduction",
        "gradual_release",
        "guided_practice",
        "independent_practice",
        "mastery_check",
        "spiral_review",
    },
    # copywork is optional: omitted for oral or pre-print skills that
    # have no authentic copywork, so it is not a required native key.
    "classical": {
        "narrative_introduction",
        "memory_work",
        "recitation_routine",
        "history_integration",
        "read_aloud_suggestions",
    },
    "charlotte_mason": {
        "lesson_length_minutes",
        "living_book_suggestions",
        "short_lesson_flow",
        "narration_prompt",
        "real_world_objects",
        "nature_connection",
        "habit_focus",
    },
    "montessori": {
        "prepared_materials",
        "presentation",
        "control_of_error",
        "abstraction_pathway",
        "extensions",
        "observation_focus",
    },
    "unschooling": {
        "invitations",
        "real_world_contexts",
        "conversation_starters",
        "resource_bank",
        "parent_role",
        "observation_documentation",
    },
}

# Lesson, sequence, and assessment keys an unschooling variant must
# never carry.
UNSCHOOLING_FORBIDDEN: set[str] = {
    "gradual_release",
    "i_do",
    "we_do",
    "you_do",
    "guided_practice",
    "independent_practice",
    "mastery_check",
    "spiral_review",
    "scaffolding",
    "assessment",
    "lesson",
    "sequence",
}


def _node_content(node_key: str) -> dict:
    if node_key in MATH_FOUNDATIONAL_CONTENT:
        return MATH_FOUNDATIONAL_CONTENT[node_key]
    if node_key in READING_FOUNDATIONAL_CONTENT:
        return READING_FOUNDATIONAL_CONTENT[node_key]
    if node_key in SCIENCE_FOUNDATIONAL_CONTENT:
        return SCIENCE_FOUNDATIONAL_CONTENT[node_key]
    return HISTORY_FOUNDATIONAL_CONTENT[node_key]


class TestNodeContentSchema:
    def test_schema_documents_new_and_existing_keys(self):
        """The schema is the single source of truth for content keys."""
        for key in ("media", "passages", "practice_items", "assessment_items", "philosophy_specific"):
            assert key in NODE_CONTENT_SCHEMA, f"{key} missing from NODE_CONTENT_SCHEMA"

    def test_schema_documents_native_philosophy_shapes(self):
        """The schema documents a distinct native shape per philosophy."""
        ps = NODE_CONTENT_SCHEMA["philosophy_specific"]
        for philosophy in PHILOSOPHIES:
            assert philosophy in ps, f"{philosophy} missing from philosophy_specific schema"
        assert "gradual_release" in ps["traditional"]
        assert "memory_work" in ps["classical"]
        assert "short_lesson_flow" in ps["charlotte_mason"]
        assert "presentation" in ps["montessori"]
        assert "invitations" in ps["unschooling"]

    def test_media_schema_entry_has_alt(self):
        media_example = NODE_CONTENT_SCHEMA["media"][0]
        assert "alt" in media_example
        assert "kind" in media_example

    def test_passage_schema_entry_has_text(self):
        passage_example = NODE_CONTENT_SCHEMA["passages"][0]
        assert "text" in passage_example

    def test_schema_documents_widgets_key(self):
        assert "widgets" in NODE_CONTENT_SCHEMA
        widget_example = NODE_CONTENT_SCHEMA["widgets"][0]
        assert "id" in widget_example
        assert "widget" in widget_example
        assert "params" in widget_example


class TestValidateContent:
    def test_legacy_required_fields_unchanged(self):
        """validate_content still flags the three required fields."""
        issues = validate_content({})
        assert "learning_objectives missing" in issues
        assert "teaching_guidance missing" in issues
        assert "assessment_criteria missing" in issues

    def test_complete_content_has_no_issues(self):
        issues = validate_content(
            {
                "learning_objectives": ["x"],
                "teaching_guidance": {"introduction": "y"},
                "assessment_criteria": {"mastery_indicators": ["z"]},
            }
        )
        assert issues == []


class TestValidateMedia:
    def test_legacy_content_yields_no_warnings(self):
        """A node with no media or passages produces no warnings, no raise."""
        assert validate_media({}) == []
        assert validate_media({"learning_objectives": ["x"]}) == []

    def test_flags_media_block_missing_alt(self):
        warnings = validate_media(
            {
                "media": [
                    {"id": "img1", "kind": "image", "src": "/a.png", "alt": "A chart"},
                    {"id": "img2", "kind": "image", "src": "/b.png"},
                ]
            }
        )
        assert any("alt" in w and "media[1]" in w for w in warnings)
        assert not any("media[0]" in w for w in warnings)

    def test_flags_passage_missing_text(self):
        warnings = validate_media(
            {
                "passages": [
                    {"id": "p1", "text": "The cat sat."},
                    {"id": "p2", "title": "Empty"},
                ]
            }
        )
        assert any("text" in w and "passage[1]" in w for w in warnings)

    def test_flags_duplicate_media_ids(self):
        warnings = validate_media(
            {
                "media": [
                    {"id": "dup", "kind": "image", "alt": "first"},
                    {"id": "dup", "kind": "diagram", "alt": "second"},
                ]
            }
        )
        assert any("duplicate media id: dup" in w for w in warnings)

    def test_flags_duplicate_passage_ids(self):
        warnings = validate_media(
            {
                "passages": [
                    {"id": "same", "text": "One."},
                    {"id": "same", "text": "Two."},
                ]
            }
        )
        assert any("duplicate passage id: same" in w for w in warnings)

    def test_clean_media_and_passages_yield_no_warnings(self):
        warnings = validate_media(
            {
                "media": [
                    {"id": "n1", "kind": "number_line", "alt": "0 to 20", "params": {"min": 0, "max": 20}},
                ],
                "passages": [
                    {"id": "r1", "text": "Sam ran.", "decodable_focus": ["short a"]},
                ],
            }
        )
        assert warnings == []


class TestValidateWidgets:
    def test_legacy_content_yields_no_warnings(self):
        """A node with no widgets produces no warnings, no raise."""
        assert validate_widgets({}) == []
        assert validate_widgets({"learning_objectives": ["x"]}) == []

    def test_flags_widget_missing_type(self):
        warnings = validate_widgets(
            {
                "widgets": [
                    {"id": "w1", "widget": "counting_objects", "params": {"count": 7}},
                    {"id": "w2", "params": {}},
                ]
            }
        )
        assert any("widget[1]" in w and "widget type" in w for w in warnings)
        assert not any("widget[0]" in w for w in warnings)

    def test_flags_widget_missing_id(self):
        warnings = validate_widgets({"widgets": [{"widget": "number_line", "params": {"min": 0, "max": 10}}]})
        assert any("widget[0]" in w and "missing id" in w for w in warnings)

    def test_flags_duplicate_widget_ids(self):
        warnings = validate_widgets(
            {
                "widgets": [
                    {"id": "dup", "widget": "counting_objects", "params": {}},
                    {"id": "dup", "widget": "number_line", "params": {}},
                ]
            }
        )
        assert any("duplicate widget id: dup" in w for w in warnings)

    def test_flags_non_dict_params(self):
        warnings = validate_widgets({"widgets": [{"id": "w1", "widget": "counting_objects", "params": "seven"}]})
        assert any("widget[0]" in w and "params is not a dict" in w for w in warnings)

    def test_clean_widgets_yield_no_warnings(self):
        warnings = validate_widgets(
            {
                "widgets": [
                    {"id": "w1", "widget": "counting_objects", "params": {"count": 5}},
                    {"id": "w2", "widget": "number_line", "params": {"min": 0, "max": 20}},
                ]
            }
        )
        assert warnings == []


class TestValidatePhilosophy:
    def test_legacy_content_yields_no_issues(self):
        """Content with no philosophy_specific produces nothing, no raise."""
        assert validate_philosophy({}) == []
        assert validate_philosophy({"learning_objectives": ["x"]}) == []

    def test_legacy_string_variant_warns(self):
        """A plain-string variant is valid but flagged with a warning."""
        issues = validate_philosophy({"philosophy_specific": {"classical": "Chant number sequences daily."}})
        assert any(i.startswith("warning:") and "classical" in i for i in issues)
        assert not any(i.startswith("error:") for i in issues)

    def test_unschooling_with_lesson_key_hard_fails(self):
        """An unschooling variant carrying a lesson/assessment key hard-fails."""
        issues = validate_philosophy(
            {"philosophy_specific": {"unschooling": {"invitations": ["x"], "mastery_check": ["bad"]}}}
        )
        errors = [i for i in issues if i.startswith("error:")]
        assert errors
        assert "mastery_check" in errors[0]

    def test_unschooling_with_gradual_release_hard_fails(self):
        issues = validate_philosophy({"philosophy_specific": {"unschooling": {"gradual_release": {"i_do": "x"}}}})
        assert any(i.startswith("error:") for i in issues)

    def test_clean_unschooling_variant_has_no_error(self):
        """A native unschooling variant raises no hard-fail."""
        issues = validate_philosophy(
            {
                "philosophy_specific": {
                    "unschooling": {
                        "invitations": ["leave objects out"],
                        "parent_role": "follow the child's interests",
                    }
                }
            }
        )
        assert not any(i.startswith("error:") for i in issues)


class TestAuthoredPhilosophyContent:
    @pytest.mark.parametrize(
        "node_key",
        [
            "mf-01",
            "mf-02",
            "mf-03",
            "mf-04",
            "mf-05",
            "mf-06",
            "mf-07",
            "mf-08",
            "mf-09",
            "mf-10",
            "mf-11",
            "mf-12",
            "mf-13",
            "mf-14",
            "mf-15",
            "mf-16",
            "mf-17",
            "mf-18",
            "mf-19",
            "mf-20",
            "mf-21",
            "mf-22",
            "mf-23",
            "mf-24",
            "mf-25",
            "mf-26",
            "mf-27",
            "mf-28",
            "mf-29",
            "mf-30",
            "rf-01",
            "rf-02",
            "rf-03",
            "rf-04",
            "rf-05",
            "rf-06",
            "rf-07",
            "rf-08",
            "rf-09",
            "rf-10",
            "rf-11",
            "rf-12",
            "rf-13",
            "rf-14",
            "rf-15",
            "rf-16",
            "rf-17",
            "rf-18",
            "rf-19",
            "rf-20",
            "rf-21",
            "rf-22",
            "rf-23",
            "rf-24",
            "rf-25",
            "sf-01",
            "sf-02",
            "sf-03",
            "sf-04",
            "sf-05",
            "sf-06",
            "sf-07",
            "sf-08",
            "sf-09",
            "sf-10",
            "sf-11",
            "sf-12",
            "sf-13",
            "sf-14",
            "sf-15",
            "sf-16",
            "sf-17",
            "sf-18",
            "sf-19",
            "sf-20",
            "hf-01",
            "hf-02",
            "hf-03",
            "hf-04",
            "hf-05",
            "hf-06",
            "hf-07",
            "hf-08",
            "hf-09",
            "hf-10",
            "hf-11",
            "hf-12",
            "hf-13",
            "hf-14",
            "hf-15",
            "hf-16",
        ],
    )
    def test_node_has_all_five_native_variants(self, node_key):
        """Each reference node carries a native variant for every philosophy."""
        content = _node_content(node_key)
        ps = content["philosophy_specific"]
        for philosophy in PHILOSOPHIES:
            assert philosophy in ps, f"{node_key} missing {philosophy} variant"
            variant = ps[philosophy]
            assert isinstance(variant, dict), f"{node_key}/{philosophy} is not a native dict"
            missing = NATIVE_KEYS[philosophy] - set(variant.keys())
            assert not missing, f"{node_key}/{philosophy} missing native keys: {sorted(missing)}"

    @pytest.mark.parametrize(
        "node_key",
        [
            "mf-01",
            "mf-02",
            "mf-03",
            "mf-04",
            "mf-05",
            "mf-06",
            "mf-07",
            "mf-08",
            "mf-09",
            "mf-10",
            "mf-11",
            "mf-12",
            "mf-13",
            "mf-14",
            "mf-15",
            "mf-16",
            "mf-17",
            "mf-18",
            "mf-19",
            "mf-20",
            "mf-21",
            "mf-22",
            "mf-23",
            "mf-24",
            "mf-25",
            "mf-26",
            "mf-27",
            "mf-28",
            "mf-29",
            "mf-30",
            "rf-01",
            "rf-02",
            "rf-03",
            "rf-04",
            "rf-05",
            "rf-06",
            "rf-07",
            "rf-08",
            "rf-09",
            "rf-10",
            "rf-11",
            "rf-12",
            "rf-13",
            "rf-14",
            "rf-15",
            "rf-16",
            "rf-17",
            "rf-18",
            "rf-19",
            "rf-20",
            "rf-21",
            "rf-22",
            "rf-23",
            "rf-24",
            "rf-25",
            "sf-01",
            "sf-02",
            "sf-03",
            "sf-04",
            "sf-05",
            "sf-06",
            "sf-07",
            "sf-08",
            "sf-09",
            "sf-10",
            "sf-11",
            "sf-12",
            "sf-13",
            "sf-14",
            "sf-15",
            "sf-16",
            "sf-17",
            "sf-18",
            "sf-19",
            "sf-20",
            "hf-01",
            "hf-02",
            "hf-03",
            "hf-04",
            "hf-05",
            "hf-06",
            "hf-07",
            "hf-08",
            "hf-09",
            "hf-10",
            "hf-11",
            "hf-12",
            "hf-13",
            "hf-14",
            "hf-15",
            "hf-16",
        ],
    )
    def test_unschooling_variant_has_no_lesson_keys(self, node_key):
        """Each unschooling variant carries no lesson/sequence/assessment key."""
        content = _node_content(node_key)
        unschooling = content["philosophy_specific"]["unschooling"]
        forbidden = UNSCHOOLING_FORBIDDEN.intersection(unschooling.keys())
        assert not forbidden, f"{node_key} unschooling has forbidden keys: {sorted(forbidden)}"
        # validate_philosophy must report no hard-fail for the authored node.
        assert not [i for i in validate_philosophy(content) if i.startswith("error:")]
