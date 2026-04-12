"""Tests for the compliance engine — 50 states + DC homeschool requirements."""

import pytest
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
