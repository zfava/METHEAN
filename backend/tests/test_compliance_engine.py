"""Tests for the compliance engine — 50 states + DC homeschool requirements."""

import uuid
from datetime import date

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import set_tenant
from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import MasteryLevel, NodeType
from app.models.identity import Child, Household
from app.models.state import ChildNodeState
from app.services.compliance_engine import STATE_REQUIREMENTS


class TestStateRequirements:
    def test_all_50_states_plus_dc(self):
        """Every US state and DC should have an entry."""
        expected_count = 51  # 50 states + DC
        assert len(STATE_REQUIREMENTS) >= expected_count

    def test_required_fields_present(self):
        """Each state must have core requirement fields."""
        required_keys = {"notification", "required_subjects", "annual_assessment"}
        for state, reqs in STATE_REQUIREMENTS.items():
            for key in required_keys:
                assert key in reqs, f"State {state} missing '{key}'"

    def test_virginia_has_requirements(self):
        assert "VA" in STATE_REQUIREMENTS
        va = STATE_REQUIREMENTS["VA"]
        assert va["notification"]["required"] is True

    def test_texas_minimal_requirements(self):
        assert "TX" in STATE_REQUIREMENTS
        tx = STATE_REQUIREMENTS["TX"]
        # Texas is famously minimal
        assert isinstance(tx.get("required_subjects", {}), dict)

    def test_new_york_strict(self):
        assert "NY" in STATE_REQUIREMENTS
        ny = STATE_REQUIREMENTS["NY"]
        assert ny["notification"]["required"] is True

    def test_unknown_state_not_present(self):
        assert "XX" not in STATE_REQUIREMENTS
        assert STATE_REQUIREMENTS.get("XX") is None

    def test_subjects_are_dicts(self):
        for state, reqs in STATE_REQUIREMENTS.items():
            subjects = reqs.get("required_subjects", {})
            assert isinstance(subjects, dict), f"State {state} required_subjects is not a dict"

    def test_dc_included(self):
        assert "DC" in STATE_REQUIREMENTS

    def test_all_entries_are_dicts(self):
        for state, reqs in STATE_REQUIREMENTS.items():
            assert isinstance(reqs, dict), f"State {state} entry is not a dict"

    def test_no_empty_states(self):
        for state, reqs in STATE_REQUIREMENTS.items():
            assert len(reqs) > 0, f"State {state} has empty requirements"


class TestStateRequirementsDataIntegrity:
    """Data integrity checks across the entire STATE_REQUIREMENTS dict."""

    def test_all_50_states_plus_dc_present(self):
        """STATE_REQUIREMENTS has entries for all 50 states + DC."""
        expected_codes = {
            "AL",
            "AK",
            "AZ",
            "AR",
            "CA",
            "CO",
            "CT",
            "DE",
            "FL",
            "GA",
            "HI",
            "ID",
            "IL",
            "IN",
            "IA",
            "KS",
            "KY",
            "LA",
            "ME",
            "MD",
            "MA",
            "MI",
            "MN",
            "MS",
            "MO",
            "MT",
            "NE",
            "NV",
            "NH",
            "NJ",
            "NM",
            "NY",
            "NC",
            "ND",
            "OH",
            "OK",
            "OR",
            "PA",
            "RI",
            "SC",
            "SD",
            "TN",
            "TX",
            "UT",
            "VT",
            "VA",
            "WA",
            "WV",
            "WI",
            "WY",
            "DC",
        }
        present = set(STATE_REQUIREMENTS.keys())
        missing = expected_codes - present
        assert not missing, f"Missing state codes: {missing}"

    def test_every_state_has_core_fields(self):
        """Every state entry has name, strictness, notification, required_subjects, annual_assessment."""
        required_fields = {"name", "strictness", "notification", "required_subjects", "annual_assessment"}
        for code, data in STATE_REQUIREMENTS.items():
            for field in required_fields:
                assert field in data, f"{code} missing field: {field}"
            assert isinstance(data["name"], str) and len(data["name"]) > 0, f"{code} has empty name"

    def test_strictness_values_are_valid(self):
        """Every state's strictness is one of the expected categories."""
        valid = {"none", "low", "moderate", "high"}
        for code, data in STATE_REQUIREMENTS.items():
            assert data.get("strictness") in valid, f"{code} has invalid strictness: {data.get('strictness')}"

    def test_notification_structure_is_dict(self):
        """Every state's notification field is a dict with 'required' key."""
        for code, data in STATE_REQUIREMENTS.items():
            notif = data.get("notification")
            assert isinstance(notif, dict), f"{code} notification is not a dict"
            assert "required" in notif, f"{code} notification missing 'required'"
            assert isinstance(notif["required"], bool), f"{code} notification.required not a bool"

    def test_annual_assessment_structure(self):
        """Every state's annual_assessment is a dict with 'required' key."""
        for code, data in STATE_REQUIREMENTS.items():
            aa = data.get("annual_assessment")
            assert isinstance(aa, dict), f"{code} annual_assessment is not a dict"
            assert "required" in aa, f"{code} annual_assessment missing 'required'"
            assert isinstance(aa["required"], bool), f"{code} annual_assessment.required not a bool"

    def test_state_requirements_no_duplicate_subjects(self):
        """No state lists the same subject twice in required_subjects for a given grade range."""
        for code, data in STATE_REQUIREMENTS.items():
            subjects = data.get("required_subjects", {})
            for grade_range, subj_list in subjects.items():
                if isinstance(subj_list, list):
                    normalized = [s.lower() if isinstance(s, str) else s for s in subj_list]
                    assert len(normalized) == len(set(normalized)), f"{code}:{grade_range} has duplicate subjects"

    def test_every_state_has_special_notes(self):
        """Every state has a special_notes field explaining nuances."""
        for code, data in STATE_REQUIREMENTS.items():
            assert "special_notes" in data, f"{code} missing special_notes"
            assert isinstance(data["special_notes"], str), f"{code} special_notes not a string"

    def test_state_code_matches_key(self):
        """If a state has a 'code' field, it matches the dict key."""
        for code, data in STATE_REQUIREMENTS.items():
            if "code" in data:
                assert data["code"] == code, f"{code} has mismatched code field: {data['code']}"

    def test_strictness_distribution_reasonable(self):
        """Expect at least a few states in each strictness category (sanity check)."""
        counts = {"none": 0, "low": 0, "moderate": 0, "high": 0}
        for data in STATE_REQUIREMENTS.values():
            s = data.get("strictness")
            if s in counts:
                counts[s] += 1
        # Each category should have at least 1 state
        for category, count in counts.items():
            assert count >= 1, f"No states in strictness category '{category}'"


# ---------------------------------------------------------------------------
# DB-backed compliance check tests
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def hh(db_session: AsyncSession) -> Household:
    h = Household(name="Compliance Test", timezone="America/New_York")
    db_session.add(h)
    await db_session.flush()
    await set_tenant(db_session, h.id)
    return h


@pytest_asyncio.fixture
async def kid(db_session: AsyncSession, hh: Household) -> Child:
    c = Child(household_id=hh.id, first_name="ComplianceKid", last_name="Test")
    db_session.add(c)
    await db_session.flush()
    return c


@pytest_asyncio.fixture
async def math_subject(db_session: AsyncSession, hh: Household) -> Subject:
    s = Subject(household_id=hh.id, name="Mathematics")
    db_session.add(s)
    await db_session.flush()
    return s


@pytest_asyncio.fixture
async def math_map(db_session: AsyncSession, hh: Household, math_subject: Subject) -> LearningMap:
    m = LearningMap(household_id=hh.id, subject_id=math_subject.id, name="Math Map")
    db_session.add(m)
    await db_session.flush()
    return m


@pytest_asyncio.fixture
async def math_node(db_session: AsyncSession, hh: Household, math_map: LearningMap) -> LearningNode:
    n = LearningNode(
        learning_map_id=math_map.id,
        household_id=hh.id,
        node_type=NodeType.concept,
        title="Counting",
    )
    db_session.add(n)
    await db_session.flush()
    return n


class TestComplianceCheckLogic:
    @pytest.mark.asyncio
    async def test_check_compliance_unknown_state_returns_error(self, db_session, hh, kid):
        """Unknown state code returns graceful error, not crash."""
        from app.services.compliance_engine import check_compliance

        result = await check_compliance(db_session, hh.id, kid.id, "XX")
        assert "error" in result
        assert "XX" in result["error"] or "not found" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_check_compliance_unknown_child_returns_error(self, db_session, hh):
        """Unknown child ID returns graceful error."""
        from app.services.compliance_engine import check_compliance

        result = await check_compliance(db_session, hh.id, uuid.uuid4(), "TX")
        assert "error" in result

    @pytest.mark.asyncio
    async def test_check_compliance_returns_structured_result(self, db_session, hh, kid):
        """Compliance check returns a dict with expected structure for a valid state."""
        from app.services.compliance_engine import check_compliance

        result = await check_compliance(db_session, hh.id, kid.id, "TX")

        assert "state" in result
        assert "state_code" in result
        assert result["state_code"] == "TX"
        assert "strictness" in result
        assert "compliant" in result
        assert "score" in result
        assert "checks" in result
        assert isinstance(result["checks"], list)
        assert "total_hours" in result
        assert "hours_by_subject" in result

    @pytest.mark.asyncio
    async def test_check_compliance_notification_only_state(self, db_session, hh, kid):
        """Notification-only states like AK (strictness=none) require minimal compliance."""
        from app.services.compliance_engine import check_compliance

        # Alaska has strictness "none" — no notification, no subjects, no hours, no assessment
        result = await check_compliance(db_session, hh.id, kid.id, "AK")
        assert result["state_code"] == "AK"
        assert result["strictness"] == "none"
        # With no requirements, score should be 100 (nothing to check fails)
        assert result["score"] == 100
        assert result["compliant"] is True

    @pytest.mark.asyncio
    async def test_check_compliance_strict_state_flags_missing_subjects(self, db_session, hh, kid):
        """Strict states flag missing required subjects."""
        from app.services.compliance_engine import check_compliance

        # NY has required subjects across grade ranges. With no enrollments, subjects should be not_met.
        result = await check_compliance(db_session, hh.id, kid.id, "NY")

        # NY requires specific subjects — with no enrollments, some should be not_met
        ny_reqs = STATE_REQUIREMENTS["NY"]
        if ny_reqs.get("required_subjects"):
            not_met_count = sum(1 for c in result["checks"] if c.get("status") == "not_met")
            assert not_met_count > 0, "Expected some requirements to be not met for empty NY household"

    @pytest.mark.asyncio
    async def test_check_compliance_with_zero_hours_at_risk(self, db_session, hh, kid):
        """States with hour requirements flag hours as at_risk or on_track when zero logged."""
        from app.services.compliance_engine import check_compliance

        # Find a state with instruction_hours defined
        state_with_hours = None
        for code, data in STATE_REQUIREMENTS.items():
            if data.get("instruction_hours"):
                state_with_hours = code
                break

        if state_with_hours is None:
            pytest.skip("No state with instruction_hours found")

        result = await check_compliance(db_session, hh.id, kid.id, state_with_hours)
        assert result["total_hours"] == 0
        # An hours check should appear
        hour_checks = [c for c in result["checks"] if "hours" in c.get("requirement", "").lower()]
        assert len(hour_checks) > 0, f"Expected hour requirements for {state_with_hours}"

    @pytest.mark.asyncio
    async def test_check_compliance_notification_check_present_when_required(self, db_session, hh, kid):
        """When state requires notification, a notification check appears."""
        from app.services.compliance_engine import check_compliance

        # VA requires notification
        result = await check_compliance(db_session, hh.id, kid.id, "VA")

        notif_checks = [c for c in result["checks"] if "notification" in c.get("requirement", "").lower()]
        assert len(notif_checks) >= 1, "VA should have a notification check"

    @pytest.mark.asyncio
    async def test_check_compliance_logged_subjects_credited(self, db_session, hh, kid, math_map, math_node):
        """Subjects with logged time are credited in the compliance check."""
        from app.services.compliance_engine import check_compliance

        # Add a ChildNodeState with time logged for math
        state = ChildNodeState(
            child_id=kid.id,
            household_id=hh.id,
            node_id=math_node.id,
            mastery_level=MasteryLevel.proficient,
            attempts_count=5,
            time_spent_minutes=300,  # 5 hours
        )
        db_session.add(state)
        await db_session.flush()

        # Use a state that requires math (most do)
        # AZ requires reading, grammar, mathematics, social studies, science
        result = await check_compliance(db_session, hh.id, kid.id, "AZ")

        assert result["total_hours"] > 0
        assert "Mathematics" in result["hours_by_subject"] or any(
            "math" in k.lower() for k in result["hours_by_subject"]
        )


class TestHoursBreakdown:
    @pytest.mark.asyncio
    async def test_hours_breakdown_empty(self, db_session, hh, kid):
        """Hours breakdown returns zeros for a child with no states."""
        from app.services.compliance_engine import get_hours_breakdown

        result = await get_hours_breakdown(db_session, hh.id, kid.id)

        assert result["total_hours"] == 0
        assert result["by_subject"] == {}

    @pytest.mark.asyncio
    async def test_hours_breakdown_aggregates_by_subject(self, db_session, hh, kid, math_map, math_node):
        """Hours are correctly aggregated by subject."""
        from app.services.compliance_engine import get_hours_breakdown

        state = ChildNodeState(
            child_id=kid.id,
            household_id=hh.id,
            node_id=math_node.id,
            mastery_level=MasteryLevel.proficient,
            attempts_count=3,
            time_spent_minutes=120,  # 2 hours
        )
        db_session.add(state)
        await db_session.flush()

        result = await get_hours_breakdown(db_session, hh.id, kid.id)

        assert result["total_hours"] == 2.0
        assert "Mathematics" in result["by_subject"]
        assert result["by_subject"]["Mathematics"] == 2.0

    @pytest.mark.asyncio
    async def test_hours_breakdown_multiple_sessions(self, db_session, hh, kid, math_map, math_node):
        """Multiple states/sessions sum correctly."""
        from app.services.compliance_engine import get_hours_breakdown

        # Create a second node in same map
        node2 = LearningNode(
            learning_map_id=math_map.id,
            household_id=hh.id,
            node_type=NodeType.concept,
            title="Addition",
        )
        db_session.add(node2)
        await db_session.flush()

        for n, mins in [(math_node, 60), (node2, 90)]:
            s = ChildNodeState(
                child_id=kid.id,
                household_id=hh.id,
                node_id=n.id,
                mastery_level=MasteryLevel.proficient,
                time_spent_minutes=mins,
            )
            db_session.add(s)
        await db_session.flush()

        result = await get_hours_breakdown(db_session, hh.id, kid.id)

        assert result["total_hours"] == 2.5  # 150 minutes
        assert result["by_subject"]["Mathematics"] == 2.5


class TestDocumentGeneration:
    @pytest.mark.asyncio
    async def test_generate_ihip_returns_pdf_bytes(self, db_session, hh, kid):
        """IHIP generation returns non-empty PDF bytes."""
        from app.services.document_generator import generate_ihip

        result = await generate_ihip(db_session, hh.id, kid.id, "NY", "2025-2026")

        assert isinstance(result, bytes)
        assert len(result) > 100  # non-trivial PDF content
        # PDFs start with %PDF-
        assert result[:5] == b"%PDF-"

    @pytest.mark.asyncio
    async def test_generate_quarterly_report_returns_pdf(self, db_session, hh, kid):
        """Quarterly report generation returns PDF bytes."""
        from app.services.document_generator import generate_quarterly_report

        result = await generate_quarterly_report(db_session, hh.id, kid.id, 1, "2025-2026")

        assert isinstance(result, bytes)
        assert len(result) > 100
        assert result[:5] == b"%PDF-"

    @pytest.mark.asyncio
    async def test_generate_transcript_returns_pdf(self, db_session, hh, kid):
        """Transcript generation returns PDF bytes even with no curricula."""
        from app.services.document_generator import generate_transcript

        result = await generate_transcript(db_session, hh.id, kid.id)

        assert isinstance(result, bytes)
        assert len(result) > 100
        assert result[:5] == b"%PDF-"

    @pytest.mark.asyncio
    async def test_generate_attendance_record_returns_pdf(self, db_session, hh, kid):
        """Attendance record generation returns PDF bytes."""
        from app.services.document_generator import generate_attendance_record

        start = date(2026, 1, 1)
        end = date(2026, 3, 31)
        result = await generate_attendance_record(db_session, hh.id, kid.id, start, end)

        assert isinstance(result, bytes)
        assert len(result) > 100
        assert result[:5] == b"%PDF-"


class TestComplianceEdgeCases:
    @pytest.mark.asyncio
    async def test_compliance_handles_child_with_no_enrollments(self, db_session, hh, kid):
        """Child with no learning maps still produces a valid compliance result."""
        from app.services.compliance_engine import check_compliance

        result = await check_compliance(db_session, hh.id, kid.id, "CA")

        # Should return a valid structured result, not an error
        assert "error" not in result
        assert "state_code" in result
        assert result["total_hours"] == 0
        assert result["hours_by_subject"] == {}

    @pytest.mark.asyncio
    async def test_compliance_case_insensitive_state_code(self, db_session, hh, kid):
        """State codes are handled case-insensitively."""
        from app.services.compliance_engine import check_compliance

        result_upper = await check_compliance(db_session, hh.id, kid.id, "CA")
        result_lower = await check_compliance(db_session, hh.id, kid.id, "ca")

        assert result_upper["state_code"] == "CA"
        assert result_lower["state_code"] == "CA"
        assert result_upper["state"] == result_lower["state"]

    @pytest.mark.asyncio
    async def test_compliance_score_is_percentage(self, db_session, hh, kid):
        """Compliance score is an integer 0-100."""
        from app.services.compliance_engine import check_compliance

        result = await check_compliance(db_session, hh.id, kid.id, "NY")
        assert isinstance(result["score"], int)
        assert 0 <= result["score"] <= 100

    @pytest.mark.asyncio
    async def test_compliance_checks_have_required_fields(self, db_session, hh, kid):
        """Every check in the results list has requirement and status."""
        from app.services.compliance_engine import check_compliance

        result = await check_compliance(db_session, hh.id, kid.id, "PA")
        for check in result["checks"]:
            assert "requirement" in check, f"Check missing requirement: {check}"
            assert "status" in check, f"Check missing status: {check}"
            assert check["status"] in ("met", "not_met", "unknown", "at_risk", "on_track"), (
                f"Invalid status: {check['status']}"
            )


# ══════════════════════════════════════════════════
# Multi-domain compliance framework
# ══════════════════════════════════════════════════


class TestComplianceDomains:
    def test_all_domains_are_valid_strings(self):
        from app.services.compliance_engine import COMPLIANCE_DOMAINS

        expected = {
            "k12_homeschool",
            "undergraduate",
            "graduate",
            "professional_cert",
            "trade_apprentice",
            "corporate",
        }
        assert set(COMPLIANCE_DOMAINS.keys()) == expected
        for name, cfg in COMPLIANCE_DOMAINS.items():
            assert isinstance(name, str) and name
            assert "description" in cfg and isinstance(cfg["description"], str)

    def test_graduate_domain_has_thesis_requirement(self):
        from app.services.compliance_engine import COMPLIANCE_DOMAINS

        grad = COMPLIANCE_DOMAINS["graduate"]
        assert grad["thesis_required"] is True
        assert grad["comprehensive_exam"] is True
        assert grad["credit_hours_required"] == 36
        assert grad["gpa_minimum"] == 3.0

    @pytest.mark.asyncio
    async def test_unknown_domain_returns_error(self, db_session, household, child):
        from app.services.compliance_engine import check_domain_compliance

        result = await check_domain_compliance(household.id, child.id, "nonexistent", db_session)
        assert result["status"] == "error"
        assert "nonexistent" in result["message"]

    @pytest.mark.asyncio
    async def test_undergraduate_domain_returns_structure(self, db_session, household, child):
        from app.services.compliance_engine import check_domain_compliance

        result = await check_domain_compliance(household.id, child.id, "undergraduate", db_session)
        assert result["domain"] == "undergraduate"
        reqs = result["requirements"]
        assert "credit_hours" in reqs
        assert "gpa" in reqs
        assert reqs["credit_hours"]["required"] == 120.0
        assert reqs["gpa"]["required"] == 2.0
        # Empty child has earned 0 and no GPA
        assert reqs["credit_hours"]["earned"] == 0.0
        assert reqs["credit_hours"]["met"] is False
        assert reqs["gpa"]["met"] is False

    @pytest.mark.asyncio
    async def test_k12_domain_delegates_to_existing(self, db_session, household, child):
        from app.services.compliance_engine import check_compliance, check_domain_compliance

        household.home_state = "TX"
        await db_session.flush()

        direct = await check_compliance(db_session, household.id, child.id, "TX")
        via_domain = await check_domain_compliance(household.id, child.id, "k12_homeschool", db_session)

        # Both paths must produce the same core shape
        assert "checks" in via_domain
        assert "score" in via_domain
        assert via_domain.get("state") == direct.get("state")
        assert via_domain.get("score") == direct.get("score")
        assert len(via_domain.get("checks", [])) == len(direct.get("checks", []))
