"""Tests for the residential and low-voltage electrical trade content.

Mirrors test_hvac_content.py in structure: parametrize every authored
id through validate_competency, hard-check that every hands-on
technique prereqs the trade safety node, the safety_review block is
reviewed:false by default, and requires_human_safety_review returns
true for the safety node and every supervision_required technique.

Electrical is the highest-hazard trade authored to date. The
apprentice-band gold standard elc-021 (DMM + LOTO live-dead-live on a
residential circuit) carries an ELECTRICAL HAZARD and must be cleared
by a licensed electrician before surfacing. A specific guard test in
this file locks the licensed-electrician-physically-present clause
against future relaxation: the clause names verbatim in
supervision_basis that the AI tutor does NOT stand in at the live
moment, and the test enforces those words remain.
"""

import pytest

from app.content.electrical_content import ELECTRICAL_CONTENT
from app.services.node_content import (
    requires_human_safety_review,
    validate_competency,
)


AUTHORED_NODE_IDS = tuple(sorted(ELECTRICAL_CONTENT.keys()))


class TestAuthoredElectrical:
    def test_authored_ids_match_content(self) -> None:
        assert set(AUTHORED_NODE_IDS) == set(ELECTRICAL_CONTENT.keys())

    @pytest.mark.parametrize("node_id", AUTHORED_NODE_IDS)
    def test_each_node_validates(self, node_id: str) -> None:
        validate_competency(ELECTRICAL_CONTENT[node_id], ELECTRICAL_CONTENT)

    def test_root_node_present_and_well_formed(self) -> None:
        assert "el-root" in ELECTRICAL_CONTENT
        root = ELECTRICAL_CONTENT["el-root"]
        assert root["node_type"] == "root"
        assert root["trade"] == "electrical"
        assert root["safety_node"] == "els-001"

    def test_every_technique_prereqs_safety_node(self) -> None:
        for node_id, node in ELECTRICAL_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            prereqs = node.get("prerequisites") or []
            assert "els-001" in prereqs, f"{node_id} technique does not prereq els-001"

    def test_every_technique_has_safety_basis(self) -> None:
        for node_id, node in ELECTRICAL_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            assert isinstance(node.get("safety_basis"), dict), node_id

    def test_every_technique_has_demonstration_criteria(self) -> None:
        for node_id, node in ELECTRICAL_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            criteria = node.get("demonstration_criteria")
            assert isinstance(criteria, list) and criteria, node_id

    def test_cutting_tool_techniques_require_supervision(self) -> None:
        from app.services.node_content import _technique_uses_cutting_tool

        for node_id, node in ELECTRICAL_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            if _technique_uses_cutting_tool(node.get("tools_required") or []):
                assert (
                    node["safety_basis"]["supervision_required"] is True
                ), f"{node_id} uses a cutting tool but supervision_required is not True"

    def test_all_prerequisites_resolve_to_authored_nodes(self) -> None:
        authored_ids = set(ELECTRICAL_CONTENT.keys())
        for node_id, node in ELECTRICAL_CONTENT.items():
            for prereq in node.get("prerequisites") or []:
                assert prereq in authored_ids, (
                    f"{node_id} prereq {prereq!r} does not resolve to any authored node id"
                )


class TestSafetyReviewMarker:
    def test_every_node_has_safety_review_block_unreviewed(self) -> None:
        for node_id, node in ELECTRICAL_CONTENT.items():
            review = node.get("safety_review")
            assert isinstance(review, dict), f"{node_id} missing safety_review block"
            assert review.get("reviewed") is False, f"{node_id} safety_review.reviewed is not False"
            assert review.get("reviewer") is None, f"{node_id} safety_review.reviewer is not None"
            assert review.get("reviewed_on") is None, f"{node_id} safety_review.reviewed_on is not None"
            assert isinstance(review.get("standard_refs"), list), f"{node_id} safety_review.standard_refs is not a list"


class TestRequiresHumanSafetyReview:
    def test_helper_returns_true_for_safety_node(self) -> None:
        if "els-001" in ELECTRICAL_CONTENT:
            assert requires_human_safety_review(ELECTRICAL_CONTENT["els-001"]) is True

    def test_helper_returns_true_for_every_supervision_required_node(self) -> None:
        for node_id, node in ELECTRICAL_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            supervised = (node.get("safety_basis") or {}).get("supervision_required") is True
            if supervised:
                assert requires_human_safety_review(node) is True, (
                    f"{node_id} is supervised but requires_human_safety_review returned False"
                )


class TestElc021HardLimit:
    """Specific guard locking the licensed-electrician-physically-present
    rule on elc-021 against future relaxation. The clause must say
    verbatim that a licensed electrician is physically present at the
    live moment and that the AI tutor does not stand in.
    """

    def test_elc_021_supervision_required(self) -> None:
        if "elc-021" not in ELECTRICAL_CONTENT:
            return
        node = ELECTRICAL_CONTENT["elc-021"]
        assert node["safety_basis"]["supervision_required"] is True
        assert node["mentor_signoff_required"] is True
        assert requires_human_safety_review(node) is True

    def test_elc_021_supervision_basis_locks_licensed_electrician_present(self) -> None:
        if "elc-021" not in ELECTRICAL_CONTENT:
            return
        sb = ELECTRICAL_CONTENT["elc-021"]["safety_basis"]["supervision_basis"]
        # The phrases below are the lock; the test fails if any future
        # edit removes or relaxes them.
        assert "LICENSED ELECTRICIAN" in sb or "licensed electrician" in sb
        assert "PHYSICALLY PRESENT" in sb or "physically present" in sb
        assert "live-dead-live" in sb
        # The AI-does-not-stand-in clause is the second lock.
        assert "does NOT stand in" in sb or "does not stand in" in sb
        # Failure modes must be named so the rule is anchored to the
        # specific things that can kill the learner.
        assert "wrong meter CAT rating" in sb or "CAT rating" in sb
        assert "backfeed" in sb

    def test_elc_021_failure_modes_named(self) -> None:
        if "elc-021" not in ELECTRICAL_CONTENT:
            return
        sb = ELECTRICAL_CONTENT["elc-021"]["safety_basis"]["supervision_basis"]
        for fm in ("generator", "solar", "MWBC", "neutral"):
            assert fm in sb, f"elc-021 supervision_basis must name failure mode: {fm}"


class TestMasteryLadder:
    def test_mastery_ladder_present_on_root(self) -> None:
        root = ELECTRICAL_CONTENT["el-root"]
        assert "mastery_ladder" in root
        ladder = root["mastery_ladder"]
        assert isinstance(ladder, dict)
        assert "framing" in ladder
        assert "rungs" in ladder

    def test_mastery_ladder_has_four_rungs_in_order(self) -> None:
        rungs = ELECTRICAL_CONTENT["el-root"]["mastery_ladder"]["rungs"]
        names = [r["rung_name"] for r in rungs]
        assert names == ["helper", "apprentice", "journeyman", "qualified"]

    def test_each_rung_has_required_fields(self) -> None:
        required = {
            "rung_name",
            "mastery_level_alias",
            "what_the_learner_does",
            "mentor_models_in_use",
            "knowledge_competencies",
            "safety_competencies",
            "low_hazard_hands_on_competencies",
            "higher_hazard_hands_on_competencies",
            "certifications_appropriate_here",
            "portfolio_artifacts_built_here",
        }
        for rung in ELECTRICAL_CONTENT["el-root"]["mastery_ladder"]["rungs"]:
            missing = required - set(rung.keys())
            assert not missing, f"rung {rung['rung_name']!r} missing fields: {missing}"

    def test_credentials_NOT_substitutable_for_lock(self) -> None:
        ladder = ELECTRICAL_CONTENT["el-root"]["mastery_ladder"]
        assert "credentials_NOT_substitutable_for" in ladder
        clauses = ladder["credentials_NOT_substitutable_for"]
        assert isinstance(clauses, list) and len(clauses) >= 4
        joined = " ".join(clauses).lower()
        # Each major credential category named as non-substitutable
        assert "nec" in joined
        assert "nfpa 70e" in joined
        assert "journeyman" in joined or "master electrician" in joined
        assert "osha" in joined

    def test_mastery_marker_names_all_three_conditions(self) -> None:
        marker = ELECTRICAL_CONTENT["el-root"]["mastery_ladder"]["mastery_marker"]
        assert isinstance(marker, str) and marker.strip()
        m = marker.lower()
        assert "demonstrated" in m or "competency" in m
        assert "credential" in m or "license" in m
        assert "qualified" in m


class TestCertificationPrepSpine:
    EXPECTED_CERT_IDS = ("elcert-nec", "elcert-licensing", "elcert-safety")

    @pytest.mark.parametrize("cert_id", EXPECTED_CERT_IDS)
    def test_certification_prep_node_present(self, cert_id: str) -> None:
        if cert_id not in ELECTRICAL_CONTENT:
            pytest.skip(f"{cert_id} not yet authored")
        assert ELECTRICAL_CONTENT[cert_id]["node_type"] == "certification_prep"

    @pytest.mark.parametrize("cert_id", EXPECTED_CERT_IDS)
    def test_certification_prep_node_validates(self, cert_id: str) -> None:
        if cert_id not in ELECTRICAL_CONTENT:
            pytest.skip(f"{cert_id} not yet authored")
        validate_competency(ELECTRICAL_CONTENT[cert_id], ELECTRICAL_CONTENT)

    @pytest.mark.parametrize("cert_id", EXPECTED_CERT_IDS)
    def test_certification_prep_node_names_credential_body(self, cert_id: str) -> None:
        if cert_id not in ELECTRICAL_CONTENT:
            pytest.skip(f"{cert_id} not yet authored")
        body = ELECTRICAL_CONTENT[cert_id].get("credential_body")
        assert isinstance(body, str) and body.strip(), f"{cert_id} missing credential_body"

    @pytest.mark.parametrize("cert_id", EXPECTED_CERT_IDS)
    def test_certification_prep_node_defers_exam(self, cert_id: str) -> None:
        if cert_id not in ELECTRICAL_CONTENT:
            pytest.skip(f"{cert_id} not yet authored")
        node = ELECTRICAL_CONTENT[cert_id]
        assert node.get("exam_taken_through") or node.get("exam_administration_deferred_to")

    @pytest.mark.parametrize("cert_id", EXPECTED_CERT_IDS)
    def test_certification_prep_node_understanding_only(self, cert_id: str) -> None:
        if cert_id not in ELECTRICAL_CONTENT:
            pytest.skip(f"{cert_id} not yet authored")
        assert ELECTRICAL_CONTENT[cert_id].get("prepares_understanding_only") is True

    @pytest.mark.parametrize("cert_id", EXPECTED_CERT_IDS)
    def test_certification_prep_node_does_not_reproduce_exam(self, cert_id: str) -> None:
        if cert_id not in ELECTRICAL_CONTENT:
            pytest.skip(f"{cert_id} not yet authored")
        prohibited = {
            "exam_questions",
            "exam_content",
            "reproduced_exam",
            "sample_questions",
            "practice_exam_questions",
            "exam_answer_key",
        }
        leaked = set(ELECTRICAL_CONTENT[cert_id].keys()) & prohibited
        assert not leaked, f"{cert_id} contains prohibited reproduced-exam fields: {leaked}"
