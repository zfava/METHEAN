"""Tests for node content schema and validation.

Covers:
- NODE_CONTENT_SCHEMA documents the full content shape.
- validate_media flags media and passage warnings without raising.
- validate_content keeps its required-field behavior.
"""

from app.services.node_content import (
    NODE_CONTENT_SCHEMA,
    validate_content,
    validate_media,
    validate_widgets,
)


class TestNodeContentSchema:
    def test_schema_documents_new_and_existing_keys(self):
        """The schema is the single source of truth for content keys."""
        for key in ("media", "passages", "practice_items", "assessment_items"):
            assert key in NODE_CONTENT_SCHEMA, f"{key} missing from NODE_CONTENT_SCHEMA"

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
