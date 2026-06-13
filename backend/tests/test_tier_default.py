"""Tests for the tier-default / fallback-safety behavior.

Covers the developing-tier default trap fix: a parent must never silently
generate an empty plan because of an unchosen or non-generatable content tier.
The system either defaults to the populated foundational tier or falls back to
it, transparently. See docs/philosophy_empty_plan_investigation.md.
"""

import structlog
from sqlalchemy import func, select

from app.core.config import settings
from app.core.learning_levels import DEFAULT_LEVEL
from app.models.governance import Activity, Plan, PlanWeek
from app.services.annual_curriculum import (
    _level_is_generatable,
    _resolve_generatable_level,
    _resolve_subject_id,
    approve_annual_curriculum,
    generate_annual_curriculum,
)


def _focus_node_count(curriculum) -> int:
    """Total resolved focus_nodes across all weeks of a generated curriculum."""
    weeks = (curriculum.scope_sequence or {}).get("weeks", [])
    return sum(len(w.get("focus_nodes", [])) for w in weeks)


def _native_only(monkeypatch) -> None:
    """Force the deterministic native provider (no AI keys, mock disabled)."""
    monkeypatch.setattr(settings, "AI_API_KEY", "")
    monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
    monkeypatch.setattr(settings, "AI_MOCK_ENABLED", False)


# ── Pure helpers ─────────────────────────────────────────────────────────


def test_default_level_is_foundational():
    assert DEFAULT_LEVEL == "foundational"


def test_level_is_generatable_matrix():
    # Only foundational math and reading are wired today.
    assert _level_is_generatable("mathematics", "foundational") is True
    assert _level_is_generatable("phonics_reading", "foundational") is True
    # Non-foundational math/reading tiers have scope but no wired templates.
    assert _level_is_generatable("mathematics", "developing") is False
    assert _level_is_generatable("phonics_reading", "developing") is False
    # Science is unauthored at every tier (the separate, out-of-scope gap).
    assert _level_is_generatable("science", "foundational") is False
    assert _level_is_generatable("science", "developing") is False


def test_resolve_generatable_level_passthrough_for_foundational():
    # A generatable tier is returned unchanged (no fallback).
    assert _resolve_generatable_level("Mathematics", "mathematics", "foundational") == "foundational"


def test_resolve_generatable_level_falls_back_to_foundational():
    # developing math has no wired content -> fall back to foundational, logged.
    with structlog.testing.capture_logs() as logs:
        result = _resolve_generatable_level("Mathematics", "mathematics", "developing")
    assert result == "foundational"
    events = [e for e in logs if e.get("event") == "annual_curriculum.tier_fallback"]
    assert len(events) == 1
    ev = events[0]
    assert ev["subject"] == "Mathematics"
    assert ev["requested_level"] == "developing"
    assert ev["fallback_level"] == "foundational"


def test_resolve_generatable_level_no_false_fallback_for_unauthored_subject():
    # Science has no wired tier at all: leave the requested level untouched and
    # do NOT fabricate a foundational fallback (which would also be empty). No
    # fallback event is emitted; the materialize guard handles the empty shell.
    with structlog.testing.capture_logs() as logs:
        result = _resolve_generatable_level("Science", "science", "developing")
    assert result == "developing"
    assert not [e for e in logs if e.get("event") == "annual_curriculum.tier_fallback"]


def test_resolve_subject_id_maps_display_names():
    assert _resolve_subject_id("Mathematics") == "mathematics"
    assert _resolve_subject_id("Phonics & Reading") == "phonics_reading"


# ── Integration: default (no tier) lands on a populated plan ──────────────


async def test_no_tier_defaults_to_foundational_math_populated(db_session, household, child, user, monkeypatch):
    """No content_tier and no saved level -> foundational -> >0 focus_nodes."""
    _native_only(monkeypatch)
    curriculum = await generate_annual_curriculum(
        db_session,
        household.id,
        child.id,
        user.id,
        subject_name="Mathematics",
        academic_year="2026-2027",
        total_weeks=12,
        content_tier=None,
    )
    assert _focus_node_count(curriculum) > 0


async def test_no_tier_defaults_to_foundational_reading_populated(db_session, household, child, user, monkeypatch):
    _native_only(monkeypatch)
    curriculum = await generate_annual_curriculum(
        db_session,
        household.id,
        child.id,
        user.id,
        subject_name="Phonics & Reading",
        academic_year="2026-2027",
        total_weeks=12,
        content_tier=None,
    )
    assert _focus_node_count(curriculum) > 0


# ── Integration: explicit developing falls back, with log + populated plan ─


async def test_developing_request_falls_back_and_is_populated(db_session, household, child, user, monkeypatch):
    """An explicit developing tier (no wired content) falls back to foundational,
    logs the fallback, and produces a populated plan instead of an empty one."""
    _native_only(monkeypatch)
    with structlog.testing.capture_logs() as logs:
        curriculum = await generate_annual_curriculum(
            db_session,
            household.id,
            child.id,
            user.id,
            subject_name="Mathematics",
            academic_year="2026-2027",
            total_weeks=12,
            content_tier="developing",
        )
    assert _focus_node_count(curriculum) > 0
    fallback = [e for e in logs if e.get("event") == "annual_curriculum.tier_fallback"]
    assert len(fallback) == 1
    assert fallback[0]["requested_level"] == "developing"
    assert fallback[0]["fallback_level"] == "foundational"


# ── Regression: explicit foundational unchanged; equals the default path ───


async def test_explicit_foundational_equals_default(db_session, household, child, user, monkeypatch):
    """The working path is unchanged: an explicit foundational request yields
    the same focus-node count as the (now-foundational) default."""
    _native_only(monkeypatch)
    explicit = await generate_annual_curriculum(
        db_session,
        household.id,
        child.id,
        user.id,
        subject_name="Mathematics",
        academic_year="2026-2027",
        total_weeks=12,
        content_tier="foundational",
    )
    default = await generate_annual_curriculum(
        db_session,
        household.id,
        child.id,
        user.id,
        subject_name="Mathematics",
        academic_year="2026-2027",
        total_weeks=12,
        content_tier=None,
    )
    assert _focus_node_count(explicit) == _focus_node_count(default) > 0


# ── No-silent-empty invariant + end-to-end materialization ────────────────


async def test_no_tier_materializes_real_focus_nodes_end_to_end(db_session, household, child, user, monkeypatch):
    """With AI keys blank and no tier chosen, math materializes >0 weeks with
    real mf- focus_nodes (the no-silent-empty invariant)."""
    _native_only(monkeypatch)
    curriculum = await generate_annual_curriculum(
        db_session,
        household.id,
        child.id,
        user.id,
        subject_name="Mathematics",
        academic_year="2026-2027",
        total_weeks=6,
        content_tier=None,
    )
    assert _focus_node_count(curriculum) > 0

    await approve_annual_curriculum(db_session, curriculum.id, user.id, household.id)

    plan = (await db_session.execute(select(Plan).where(Plan.annual_curriculum_id == curriculum.id))).scalar_one()
    week_count = await db_session.scalar(select(func.count()).select_from(PlanWeek).where(PlanWeek.plan_id == plan.id))
    activity_count = await db_session.scalar(
        select(func.count())
        .select_from(Activity)
        .join(PlanWeek, Activity.plan_week_id == PlanWeek.id)
        .where(PlanWeek.plan_id == plan.id)
    )
    assert week_count == 6
    assert activity_count > 0

    # The resolved focus nodes are real persisted LearningNodes from the
    # math-foundational template (source_ref mf-NN), not empty placeholders.
    from app.models.curriculum import LearningNode

    focus_ids = [fid for w in curriculum.scope_sequence["weeks"] for fid in w.get("focus_nodes", [])]
    assert focus_ids
    rows = (
        (await db_session.execute(select(LearningNode.source_ref).where(LearningNode.id.in_(focus_ids))))
        .scalars()
        .all()
    )
    assert rows and all((ref or "").startswith("mf-") for ref in rows)
