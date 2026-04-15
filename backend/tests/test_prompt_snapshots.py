"""Snapshot tests for AI system prompts.

If a prompt changes, update the snapshot file to acknowledge the change.
This prevents accidental prompt drift.
"""

import hashlib
import json
from pathlib import Path

import pytest

from app.ai.prompts import (
    ADVISOR_SYSTEM,
    CARTOGRAPHER_SYSTEM,
    CONTENT_ARCHITECT_SYSTEM,
    CURRICULUM_MAPPER_SYSTEM,
    EDUCATION_ARCHITECT_SYSTEM,
    EVALUATOR_SYSTEM,
    PLANNER_SYSTEM,
    TUTOR_SYSTEM,
    VOCATIONAL_CURRICULUM_SYSTEM,
    VOCATIONAL_TUTOR_SYSTEM,
    build_philosophical_constraints,
)

SNAPSHOT_FILE = Path(__file__).parent / "prompt_snapshots.json"

PROMPTS = {
    "planner": PLANNER_SYSTEM,
    "tutor": TUTOR_SYSTEM,
    "evaluator": EVALUATOR_SYSTEM,
    "advisor": ADVISOR_SYSTEM,
    "cartographer": CARTOGRAPHER_SYSTEM,
    "curriculum_mapper": CURRICULUM_MAPPER_SYSTEM,
    "content_architect": CONTENT_ARCHITECT_SYSTEM,
    "education_architect": EDUCATION_ARCHITECT_SYSTEM,
    "vocational_curriculum": VOCATIONAL_CURRICULUM_SYSTEM,
    "vocational_tutor": VOCATIONAL_TUTOR_SYSTEM,
}


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _load_snapshots() -> dict:
    if SNAPSHOT_FILE.exists():
        return json.loads(SNAPSHOT_FILE.read_text())
    return {}


def _save_snapshots(data: dict):
    SNAPSHOT_FILE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


class TestPromptSnapshots:
    """Ensure AI prompts don't change without deliberate review."""

    def test_snapshot_file_exists_or_create(self):
        """On first run, create the snapshot file."""
        if not SNAPSHOT_FILE.exists():
            snapshots = {name: _hash(text) for name, text in PROMPTS.items()}
            _save_snapshots(snapshots)

    @pytest.mark.parametrize("role", list(PROMPTS.keys()))
    def test_prompt_unchanged(self, role: str):
        """Verify each prompt matches its snapshot hash."""
        snapshots = _load_snapshots()
        if role not in snapshots:
            snapshots[role] = _hash(PROMPTS[role])
            _save_snapshots(snapshots)
            return

        current_hash = _hash(PROMPTS[role])
        assert current_hash == snapshots[role], (
            f"Prompt for '{role}' has changed! "
            f"Expected hash {snapshots[role]}, got {current_hash}. "
            f"If this change is intentional, delete backend/tests/prompt_snapshots.json "
            f"and re-run tests to regenerate snapshots."
        )

    def test_no_empty_prompts(self):
        """Every AI role must have a non-empty system prompt."""
        for role, text in PROMPTS.items():
            assert len(text.strip()) > 100, f"Prompt for '{role}' is suspiciously short ({len(text)} chars)"

    def test_prompts_contain_role_identity(self):
        """Each prompt should identify its role to the AI."""
        role_keywords = {
            "planner": ["plan", "week", "schedule"],
            "tutor": ["tutor", "socratic", "question"],
            "evaluator": ["evaluat", "assess", "confidence"],
            "advisor": ["advisor", "report", "parent"],
            "cartographer": ["map", "calibrat", "cartograph"],
            "curriculum_mapper": ["map", "curriculum", "materials"],
            "content_architect": ["content", "teaching", "guidance"],
            "education_architect": ["education", "blueprint", "architect"],
            "vocational_curriculum": ["trade", "curriculum", "vocational"],
            "vocational_tutor": ["trade", "student", "learn"],
        }
        for role, keywords in role_keywords.items():
            prompt_lower = PROMPTS[role].lower()
            assert any(kw in prompt_lower for kw in keywords), (
                f"Prompt for '{role}' doesn't contain any expected keywords: {keywords}"
            )

    def test_philosophical_constraint_builder(self):
        """The philosophical constraint builder should produce non-empty output."""
        result = build_philosophical_constraints({"philosophy": "classical", "ai_autonomy": "preview_all"})
        assert len(result) > 0

        result_none = build_philosophical_constraints(None)
        assert isinstance(result_none, str)
