"""Tests for the gardening / horticulture trade content.

Mirrors test_woodworking_content.py's structure: parametrize every
authored id through validate_competency, hard checks for safety gating
(every hands-on technique prereqs the trade safety node, carries
safety_basis, sharp-tool techniques set supervision_required True),
and the safety_review block is at reviewed=False by default. A separate
guard test resolves every prerequisite against the authored set.
"""

import pytest

from app.content.gardening_content import GARDENING_CONTENT
from app.services.node_content import (
    requires_human_safety_review,
    validate_competency,
)


AUTHORED_NODE_IDS = tuple(sorted(GARDENING_CONTENT.keys()))


class TestAuthoredGardening:
    def test_authored_ids_match_content(self) -> None:
        assert set(AUTHORED_NODE_IDS) == set(GARDENING_CONTENT.keys())

    @pytest.mark.parametrize("node_id", AUTHORED_NODE_IDS)
    def test_each_node_validates(self, node_id: str) -> None:
        validate_competency(GARDENING_CONTENT[node_id], GARDENING_CONTENT)

    def test_root_node_present_and_well_formed(self) -> None:
        assert "gardening-root" in GARDENING_CONTENT
        root = GARDENING_CONTENT["gardening-root"]
        assert root["node_type"] == "root"
        assert root["trade"] == "agriculture"
        assert root["safety_node"] == "gs-001"

    def test_every_technique_prereqs_safety_node(self) -> None:
        for node_id, node in GARDENING_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            prereqs = node.get("prerequisites") or []
            assert "gs-001" in prereqs, f"{node_id} technique does not prereq gs-001"

    def test_every_technique_has_safety_basis(self) -> None:
        for node_id, node in GARDENING_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            assert isinstance(node.get("safety_basis"), dict), node_id

    def test_every_technique_has_demonstration_criteria(self) -> None:
        for node_id, node in GARDENING_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            criteria = node.get("demonstration_criteria")
            assert isinstance(criteria, list) and criteria, node_id

    def test_cutting_tool_techniques_require_supervision(self) -> None:
        from app.services.node_content import _technique_uses_cutting_tool

        for node_id, node in GARDENING_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            if _technique_uses_cutting_tool(node.get("tools_required") or []):
                assert (
                    node["safety_basis"]["supervision_required"] is True
                ), f"{node_id} uses a cutting tool but supervision_required is not True"

    def test_all_prerequisites_resolve_to_authored_nodes(self) -> None:
        authored_ids = set(GARDENING_CONTENT.keys())
        for node_id, node in GARDENING_CONTENT.items():
            for prereq in node.get("prerequisites") or []:
                assert prereq in authored_ids, (
                    f"{node_id} prereq {prereq!r} does not resolve to any authored node id"
                )


class TestSafetyReviewMarker:
    def test_every_node_has_safety_review_block_unreviewed(self) -> None:
        for node_id, node in GARDENING_CONTENT.items():
            review = node.get("safety_review")
            assert isinstance(review, dict), f"{node_id} missing safety_review block"
            assert review.get("reviewed") is False, f"{node_id} safety_review.reviewed is not False"
            assert review.get("reviewer") is None, f"{node_id} safety_review.reviewer is not None"
            assert review.get("reviewed_on") is None, f"{node_id} safety_review.reviewed_on is not None"
            assert isinstance(review.get("standard_refs"), list), f"{node_id} safety_review.standard_refs is not a list"


class TestRequiresHumanSafetyReview:
    def test_helper_returns_true_for_safety_node(self) -> None:
        if "gs-001" in GARDENING_CONTENT:
            assert requires_human_safety_review(GARDENING_CONTENT["gs-001"]) is True

    def test_helper_returns_true_for_every_supervision_required_node(self) -> None:
        for node_id, node in GARDENING_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            supervised = (node.get("safety_basis") or {}).get("supervision_required") is True
            if supervised:
                assert requires_human_safety_review(node) is True, (
                    f"{node_id} is supervised but requires_human_safety_review returned False"
                )
