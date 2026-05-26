"""Tests for the reading_developing content.

Gates every authored rd-NN node through the five-philosophy native
variants check, validates that every prerequisite resolves to an
authored node id (in either reading_foundational or reading_developing),
and asserts the developing-level full apparatus: enriched flag,
learning_objectives, teaching_guidance with the foundational sub-keys,
assessment_criteria, practice_items, assessment_items, philosophy_specific
with all five philosophies' native shapes.
"""

import pytest

from app.content.reading_developing_content import READING_DEVELOPING_CONTENT
from app.content.reading_foundational_content import READING_FOUNDATIONAL_CONTENT
from app.content.scope_sequences import SCOPE_SEQUENCES


PHILOSOPHIES = ("traditional", "classical", "charlotte_mason", "montessori", "unschooling")

# The distinctive native top-level keys each philosophy variant carries,
# mirroring the central test_node_content.py contract.
NATIVE_KEYS: dict[str, set[str]] = {
    "traditional": {
        "introduction",
        "gradual_release",
        "guided_practice",
        "independent_practice",
        "mastery_check",
        "spiral_review",
    },
    # copywork is optional; classical variants may carry it for topics
    # that invite copying language (poetry, fluency passages, narration)
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

# Lesson / sequence / graded-assessment keys an unschooling variant must
# never carry.
UNSCHOOLING_FORBIDDEN_KEYS = {
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


AUTHORED_NODE_IDS = tuple(sorted(READING_DEVELOPING_CONTENT.keys()))


class TestAuthoredReadingDeveloping:
    def test_authored_ids_match_content(self) -> None:
        assert set(AUTHORED_NODE_IDS) == set(READING_DEVELOPING_CONTENT.keys())

    @pytest.mark.parametrize("node_id", AUTHORED_NODE_IDS)
    def test_each_node_is_enriched(self, node_id: str) -> None:
        node = READING_DEVELOPING_CONTENT[node_id]
        assert node.get("enriched") is True, f"{node_id} missing enriched=True"

    @pytest.mark.parametrize("node_id", AUTHORED_NODE_IDS)
    def test_each_node_has_required_top_level_keys(self, node_id: str) -> None:
        node = READING_DEVELOPING_CONTENT[node_id]
        required = {
            "learning_objectives",
            "teaching_guidance",
            "assessment_criteria",
            "practice_items",
            "assessment_items",
            "resource_guidance",
            "time_estimates",
            "accommodations",
            "philosophy_specific",
            "connections",
        }
        missing = required - set(node.keys())
        assert not missing, f"{node_id} missing required top-level keys: {sorted(missing)}"

    @pytest.mark.parametrize("node_id", AUTHORED_NODE_IDS)
    def test_each_node_teaching_guidance_has_sub_keys(self, node_id: str) -> None:
        tg = READING_DEVELOPING_CONTENT[node_id].get("teaching_guidance", {})
        required_sub_keys = {
            "introduction",
            "scaffolding_sequence",
            "socratic_questions",
            "practice_activities",
            "real_world_connections",
            "common_misconceptions",
        }
        missing = required_sub_keys - set(tg.keys())
        assert not missing, f"{node_id} teaching_guidance missing sub-keys: {sorted(missing)}"

    @pytest.mark.parametrize("node_id", AUTHORED_NODE_IDS)
    def test_each_node_assessment_criteria_has_mastery_indicators(self, node_id: str) -> None:
        ac = READING_DEVELOPING_CONTENT[node_id].get("assessment_criteria", {})
        assert ac.get("mastery_indicators"), f"{node_id} assessment_criteria missing mastery_indicators"
        assert ac.get("assessment_methods"), f"{node_id} assessment_criteria missing assessment_methods"

    @pytest.mark.parametrize("node_id", AUTHORED_NODE_IDS)
    def test_each_node_has_practice_items(self, node_id: str) -> None:
        items = READING_DEVELOPING_CONTENT[node_id].get("practice_items", [])
        assert isinstance(items, list) and items, f"{node_id} missing practice_items"

    @pytest.mark.parametrize("node_id", AUTHORED_NODE_IDS)
    def test_each_node_has_assessment_items(self, node_id: str) -> None:
        items = READING_DEVELOPING_CONTENT[node_id].get("assessment_items", [])
        assert isinstance(items, list) and items, f"{node_id} missing assessment_items"

    @pytest.mark.parametrize("node_id", AUTHORED_NODE_IDS)
    def test_each_node_has_all_five_native_philosophy_variants(self, node_id: str) -> None:
        ps = READING_DEVELOPING_CONTENT[node_id].get("philosophy_specific", {})
        for philosophy in PHILOSOPHIES:
            assert philosophy in ps, f"{node_id} missing {philosophy} variant"
            variant = ps[philosophy]
            assert isinstance(variant, dict), f"{node_id}/{philosophy} is not a native dict"
            missing = NATIVE_KEYS[philosophy] - set(variant.keys())
            assert not missing, f"{node_id}/{philosophy} missing native keys: {sorted(missing)}"

    @pytest.mark.parametrize("node_id", AUTHORED_NODE_IDS)
    def test_unschooling_variant_carries_no_lesson_or_sequence_keys(self, node_id: str) -> None:
        unschooling = READING_DEVELOPING_CONTENT[node_id]["philosophy_specific"]["unschooling"]
        leaked = set(unschooling.keys()) & UNSCHOOLING_FORBIDDEN_KEYS
        assert not leaked, f"{node_id}/unschooling carries forbidden lesson/sequence/assessment keys: {sorted(leaked)}"


class TestPrerequisiteResolution:
    """Every prerequisite in a developing-reading node must resolve to an
    authored node id, either in reading_foundational (rf-NN) or in
    reading_developing (rd-NN).
    """

    def _expected_node_id_for_topic_ref(self, topic_ref: str) -> str:
        """Map a scope_sequences topic ref like 'read_f_11' or 'read_d_03' to
        the authored node id 'rf-11' or 'rd-03'.
        """
        if topic_ref.startswith("read_f_"):
            return f"rf-{topic_ref.removeprefix('read_f_')}"
        if topic_ref.startswith("read_d_"):
            return f"rd-{topic_ref.removeprefix('read_d_')}"
        raise AssertionError(f"unknown reading topic ref convention: {topic_ref!r}")

    def test_every_authored_node_has_matching_scope_topic(self) -> None:
        """Every rd-NN node must correspond to a read_d_NN scope topic by
        position.
        """
        scope_refs = {t["ref"] for t in SCOPE_SEQUENCES["phonics_reading"]["developing"]}
        for node_id in AUTHORED_NODE_IDS:
            num = node_id.removeprefix("rd-")
            expected_ref = f"read_d_{num}"
            assert expected_ref in scope_refs, (
                f"{node_id} has no matching scope topic {expected_ref!r}"
            )

    @pytest.mark.parametrize("node_id", AUTHORED_NODE_IDS)
    def test_authored_node_prerequisites_resolve(self, node_id: str) -> None:
        """For each authored rd-NN, look up its scope-topic prereqs and
        assert each maps to an authored node id (rf-NN or rd-NN).
        """
        num = node_id.removeprefix("rd-")
        topic_ref = f"read_d_{num}"
        scope_topic = next(
            (t for t in SCOPE_SEQUENCES["phonics_reading"]["developing"] if t["ref"] == topic_ref),
            None,
        )
        assert scope_topic is not None, f"{node_id} has no matching scope topic"
        for prereq_ref in scope_topic.get("prerequisites", []):
            expected_id = self._expected_node_id_for_topic_ref(prereq_ref)
            if expected_id.startswith("rf-"):
                assert expected_id in READING_FOUNDATIONAL_CONTENT, (
                    f"{node_id} prereq {prereq_ref!r} -> {expected_id!r} does not resolve "
                    f"to any authored reading_foundational node"
                )
            elif expected_id.startswith("rd-"):
                # Earlier batches of reading_developing must already be authored.
                # This will fail if a node is authored out of topological order
                # (which is by design: keeps the DAG valid at every commit).
                assert expected_id in READING_DEVELOPING_CONTENT, (
                    f"{node_id} prereq {prereq_ref!r} -> {expected_id!r} does not resolve "
                    f"to any authored reading_developing node; author it first"
                )
