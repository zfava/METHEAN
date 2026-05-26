"""Tests for the HVAC trade content.

Mirrors test_woodworking_content.py and test_gardening_content.py in
structure: parametrize every authored id through validate_competency,
hard-check that every hands-on technique prereqs the trade safety node,
the safety_review block is reviewed:false by default, and
requires_human_safety_review returns true for the safety node and every
supervision_required technique.

HVAC is a higher-hazard trade. The gold-standard apprentice node carries
an electrical hazard and must be cleared by a licensed HVAC technician
or licensed electrician before surfacing (this is a content-review
contract, not a test-enforceable one; the test verifies the
safety_review block is unreviewed, which is the integration gate).
"""

import pytest

from app.content.hvac_content import HVAC_CONTENT
from app.services.node_content import (
    requires_human_safety_review,
    validate_competency,
)


AUTHORED_NODE_IDS = tuple(sorted(HVAC_CONTENT.keys()))


class TestAuthoredHVAC:
    def test_authored_ids_match_content(self) -> None:
        assert set(AUTHORED_NODE_IDS) == set(HVAC_CONTENT.keys())

    @pytest.mark.parametrize("node_id", AUTHORED_NODE_IDS)
    def test_each_node_validates(self, node_id: str) -> None:
        validate_competency(HVAC_CONTENT[node_id], HVAC_CONTENT)

    def test_root_node_present_and_well_formed(self) -> None:
        assert "hvac-root" in HVAC_CONTENT
        root = HVAC_CONTENT["hvac-root"]
        assert root["node_type"] == "root"
        assert root["trade"] == "hvac"
        assert root["safety_node"] == "hs-001"

    def test_every_technique_prereqs_safety_node(self) -> None:
        for node_id, node in HVAC_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            prereqs = node.get("prerequisites") or []
            assert "hs-001" in prereqs, f"{node_id} technique does not prereq hs-001"

    def test_every_technique_has_safety_basis(self) -> None:
        for node_id, node in HVAC_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            assert isinstance(node.get("safety_basis"), dict), node_id

    def test_every_technique_has_demonstration_criteria(self) -> None:
        for node_id, node in HVAC_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            criteria = node.get("demonstration_criteria")
            assert isinstance(criteria, list) and criteria, node_id

    def test_cutting_tool_techniques_require_supervision(self) -> None:
        from app.services.node_content import _technique_uses_cutting_tool

        for node_id, node in HVAC_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            if _technique_uses_cutting_tool(node.get("tools_required") or []):
                assert (
                    node["safety_basis"]["supervision_required"] is True
                ), f"{node_id} uses a cutting tool but supervision_required is not True"

    def test_all_prerequisites_resolve_to_authored_nodes(self) -> None:
        authored_ids = set(HVAC_CONTENT.keys())
        for node_id, node in HVAC_CONTENT.items():
            for prereq in node.get("prerequisites") or []:
                assert prereq in authored_ids, (
                    f"{node_id} prereq {prereq!r} does not resolve to any authored node id"
                )


class TestSafetyReviewMarker:
    def test_every_node_has_safety_review_block_unreviewed(self) -> None:
        for node_id, node in HVAC_CONTENT.items():
            review = node.get("safety_review")
            assert isinstance(review, dict), f"{node_id} missing safety_review block"
            assert review.get("reviewed") is False, f"{node_id} safety_review.reviewed is not False"
            assert review.get("reviewer") is None, f"{node_id} safety_review.reviewer is not None"
            assert review.get("reviewed_on") is None, f"{node_id} safety_review.reviewed_on is not None"
            assert isinstance(review.get("standard_refs"), list), f"{node_id} safety_review.standard_refs is not a list"


class TestRequiresHumanSafetyReview:
    def test_helper_returns_true_for_safety_node(self) -> None:
        if "hs-001" in HVAC_CONTENT:
            assert requires_human_safety_review(HVAC_CONTENT["hs-001"]) is True

    def test_helper_returns_true_for_every_supervision_required_node(self) -> None:
        for node_id, node in HVAC_CONTENT.items():
            if node.get("node_type") != "technique":
                continue
            supervised = (node.get("safety_basis") or {}).get("supervision_required") is True
            if supervised:
                assert requires_human_safety_review(node) is True, (
                    f"{node_id} is supervised but requires_human_safety_review returned False"
                )

    def test_gold_standard_hc_021_requires_human_review_if_authored(self) -> None:
        # hc-021 is the apprentice-band gold standard. It must always require
        # human safety review per its electrical hazard. This test is a
        # specific guard that the live-dead-live verification node is never
        # downgraded to AI-mentor-only in any future edit.
        if "hc-021" in HVAC_CONTENT:
            assert requires_human_safety_review(HVAC_CONTENT["hc-021"]) is True, (
                "hc-021 (DMM + LOTO live-dead-live) must require human safety review"
            )
            assert HVAC_CONTENT["hc-021"]["safety_basis"]["supervision_required"] is True
            assert HVAC_CONTENT["hc-021"]["mentor_signoff_required"] is True


class TestExistingSafetyContentUnchangedByCertificationRetrofit:
    """Guards that the certification-spine retrofit did NOT modify the
    safety_basis or supervision_basis of any pre-existing competency. The
    retrofit may add metadata (e.g. certification_alignment), but it must
    not touch the safety content.
    """

    def test_hs_001_safety_basis_intact(self) -> None:
        sb = HVAC_CONTENT["hs-001"]["safety_basis"]
        assert sb["supervision_required"] is True
        assert isinstance(sb["hazards"], list) and len(sb["hazards"]) >= 10
        assert isinstance(sb["ppe_required"], list) and len(sb["ppe_required"]) >= 5
        # The supervision_basis text still names the adult-on-premises and AI-may-guide model
        assert "adult on premises" in sb["supervision_basis"]
        assert "AI tutor" in sb["supervision_basis"]
        assert "self-attestation" in sb["supervision_basis"]

    def test_hc_001_supervision_unchanged(self) -> None:
        sb = HVAC_CONTENT["hc-001"]["safety_basis"]
        assert sb["supervision_required"] is False
        assert "AI tutor mentors this competency end-to-end" in sb["supervision_basis"]

    def test_hc_002_supervision_unchanged(self) -> None:
        sb = HVAC_CONTENT["hc-002"]["safety_basis"]
        assert sb["supervision_required"] is False
        assert "AI tutor mentors this competency end-to-end" in sb["supervision_basis"]

    def test_hc_021_qualified_human_rule_intact(self) -> None:
        sb = HVAC_CONTENT["hc-021"]["safety_basis"]
        assert sb["supervision_required"] is True
        # The qualified-human-physically-present rule must still be present verbatim
        assert "PHYSICALLY PRESENT" in sb["supervision_basis"]
        assert "licensed HVAC technician" in sb["supervision_basis"]
        assert "licensed electrician" in sb["supervision_basis"]
        # The AI-does-not-stand-in rule must still be present
        assert "AI tutor does not stand in" in sb["supervision_basis"] or (
            "does NOT stand in" in sb["supervision_basis"]
        )

    def test_hvac_root_safety_review_intact(self) -> None:
        review = HVAC_CONTENT["hvac-root"]["safety_review"]
        assert review["reviewed"] is False
        assert review["reviewer"] is None
        assert review["reviewed_on"] is None


class TestCertificationPrepSpine:
    EXPECTED_CERT_IDS = ("hcert-epa608", "hcert-licensing", "hcert-nate", "hcert-osha")

    @pytest.mark.parametrize("cert_id", EXPECTED_CERT_IDS)
    def test_certification_prep_node_present(self, cert_id: str) -> None:
        assert cert_id in HVAC_CONTENT, f"missing certification_prep node {cert_id}"
        assert HVAC_CONTENT[cert_id]["node_type"] == "certification_prep"

    @pytest.mark.parametrize("cert_id", EXPECTED_CERT_IDS)
    def test_certification_prep_node_validates(self, cert_id: str) -> None:
        # Hard-validation pass under the new certification_prep rules in
        # validate_competency: credential_body named, deferral statement
        # present, prepares_understanding_only True, no reproduced exam
        # fields.
        validate_competency(HVAC_CONTENT[cert_id], HVAC_CONTENT)

    @pytest.mark.parametrize("cert_id", EXPECTED_CERT_IDS)
    def test_certification_prep_node_names_credential_body(self, cert_id: str) -> None:
        body = HVAC_CONTENT[cert_id].get("credential_body")
        assert isinstance(body, str) and body.strip(), f"{cert_id} missing credential_body"

    @pytest.mark.parametrize("cert_id", EXPECTED_CERT_IDS)
    def test_certification_prep_node_defers_exam(self, cert_id: str) -> None:
        node = HVAC_CONTENT[cert_id]
        assert node.get("exam_taken_through") or node.get("exam_administration_deferred_to"), (
            f"{cert_id} must defer exam administration to an external body"
        )

    @pytest.mark.parametrize("cert_id", EXPECTED_CERT_IDS)
    def test_certification_prep_node_understanding_only(self, cert_id: str) -> None:
        assert HVAC_CONTENT[cert_id].get("prepares_understanding_only") is True

    @pytest.mark.parametrize("cert_id", EXPECTED_CERT_IDS)
    def test_certification_prep_node_does_not_reproduce_exam(self, cert_id: str) -> None:
        prohibited = {
            "exam_questions",
            "exam_content",
            "reproduced_exam",
            "sample_questions",
            "practice_exam_questions",
            "exam_answer_key",
        }
        node_keys = set(HVAC_CONTENT[cert_id].keys())
        leaked = node_keys & prohibited
        assert not leaked, f"{cert_id} contains prohibited reproduced-exam fields: {leaked}"

    @pytest.mark.parametrize("cert_id", EXPECTED_CERT_IDS)
    def test_certification_prep_node_safety_review_unreviewed(self, cert_id: str) -> None:
        review = HVAC_CONTENT[cert_id].get("safety_review")
        assert isinstance(review, dict)
        assert review["reviewed"] is False
        assert review["reviewer"] is None
        assert review["reviewed_on"] is None
        assert isinstance(review.get("standard_refs"), list) and review["standard_refs"]

    def test_epa608_marked_legally_required(self) -> None:
        # EPA Section 608 is legally required for refrigerant handling per
        # the Clean Air Act. This must be explicit in the node so the
        # mastery-path and any downstream surfacing cannot treat it as
        # optional.
        assert HVAC_CONTENT["hcert-epa608"]["legal_status"] == "legally_required"

    def test_licensing_marked_jurisdiction_specific(self) -> None:
        assert HVAC_CONTENT["hcert-licensing"]["legal_status"] == "jurisdiction_specific"

    def test_nate_and_osha_marked_optional(self) -> None:
        assert HVAC_CONTENT["hcert-nate"]["legal_status"] == "optional"
        assert HVAC_CONTENT["hcert-osha"]["legal_status"] == "optional"


class TestCertificationPrepValidator:
    """Tests the new validate_competency rules for certification_prep nodes
    using minimal fixture nodes."""

    def _minimal_cert_node(self, **overrides) -> dict:
        base = {
            "node_type": "certification_prep",
            "trade": "hvac",
            "credential_name": "Some Credential",
            "credential_body": "Some Body",
            "authorizing_scope": "what it lets you do",
            "exam_taken_through": "the body",
        }
        base.update(overrides)
        return base

    def test_minimal_certification_prep_validates(self) -> None:
        validate_competency(self._minimal_cert_node())

    def test_missing_credential_body_raises(self) -> None:
        node = self._minimal_cert_node()
        del node["credential_body"]
        with pytest.raises(ValueError, match="credential_body"):
            validate_competency(node)

    def test_empty_credential_body_raises(self) -> None:
        node = self._minimal_cert_node(credential_body="")
        with pytest.raises(ValueError, match="credential_body"):
            validate_competency(node)

    def test_missing_credential_name_raises(self) -> None:
        node = self._minimal_cert_node()
        del node["credential_name"]
        with pytest.raises(ValueError, match="credential_name"):
            validate_competency(node)

    def test_missing_authorizing_scope_raises(self) -> None:
        node = self._minimal_cert_node()
        del node["authorizing_scope"]
        with pytest.raises(ValueError, match="authorizing_scope"):
            validate_competency(node)

    def test_missing_exam_deferral_raises(self) -> None:
        node = self._minimal_cert_node()
        del node["exam_taken_through"]
        with pytest.raises(ValueError, match="defer exam administration"):
            validate_competency(node)

    def test_alternate_deferral_field_accepted(self) -> None:
        node = self._minimal_cert_node()
        del node["exam_taken_through"]
        node["exam_administration_deferred_to"] = "the official body"
        validate_competency(node)

    def test_understanding_only_false_raises(self) -> None:
        node = self._minimal_cert_node(prepares_understanding_only=False)
        with pytest.raises(ValueError, match="prepares_understanding_only"):
            validate_competency(node)

    def test_understanding_only_true_accepted(self) -> None:
        node = self._minimal_cert_node(prepares_understanding_only=True)
        validate_competency(node)

    def test_understanding_only_absent_accepted(self) -> None:
        node = self._minimal_cert_node()
        validate_competency(node)

    @pytest.mark.parametrize(
        "field",
        [
            "exam_questions",
            "exam_content",
            "reproduced_exam",
            "sample_questions",
            "practice_exam_questions",
            "exam_answer_key",
        ],
    )
    def test_prohibited_reproduced_exam_field_raises(self, field: str) -> None:
        node = self._minimal_cert_node(**{field: ["any value"]})
        with pytest.raises(ValueError, match="reproduce or administer exam content"):
            validate_competency(node)
