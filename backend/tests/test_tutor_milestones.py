"""Tests for tutor relationship memory: milestones derived, never stored.

Covers breakthrough detection on a seeded struggle then mastery history
(and exclusion of quick masteries), streak and completion and first
detection per the reused definitions, ranking and the cap of three, the
dignity rule (no failure counts in any rendered line), the opt in gate at
context assembly (off by default, no derivation runs; on injects the
block; disabling invalidates and injects nothing), the enable/disable
governance events with a valid hash chain, the parent preview equalling
the tutor injection (same source proof), the zero database writes guard,
the no migration guard, and access control.
"""

import subprocess
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select

import app.services.tutor_milestones as tm
from app.models.achievements import Streak
from app.models.curriculum import ChildMapEnrollment, LearningMap, LearningNode, Subject
from app.models.enums import ActivityType, AttemptStatus, MasteryLevel, NodeType, StateEventType
from app.models.governance import Activity, Attempt, GovernanceEvent, Plan, PlanWeek
from app.models.intelligence import ChildTutorPreferences
from app.models.state import ChildNodeState, StateEvent
from app.services.learning_context import build_milestone_block
from app.services.tutor_milestones import derive_milestones, get_milestones

# ── Seeding helpers ─────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def plan_week(db_session, household, child) -> PlanWeek:
    plan = Plan(household_id=household.id, child_id=child.id, name="Plan", status="active")
    db_session.add(plan)
    await db_session.flush()
    week = PlanWeek(
        plan_id=plan.id,
        household_id=household.id,
        week_number=1,
        start_date=date(2026, 6, 8),
        end_date=date(2026, 6, 14),
    )
    db_session.add(week)
    await db_session.flush()
    return week


async def _subject_map(db, household, subject_name: str, map_name: str) -> LearningMap:
    s = Subject(household_id=household.id, name=subject_name)
    db.add(s)
    await db.flush()
    m = LearningMap(household_id=household.id, subject_id=s.id, name=map_name)
    db.add(m)
    await db.flush()
    return m


async def _seed_node(
    db,
    household,
    child,
    lmap: LearningMap,
    week: PlanWeek,
    title: str,
    mastery: MasteryLevel,
    *,
    attempts: int = 2,
    span_days: int = 0,
    score: float = 0.8,
) -> LearningNode:
    """A reached node with an attempt history spread across span_days."""
    node = LearningNode(
        learning_map_id=lmap.id,
        household_id=household.id,
        node_type=NodeType.concept,
        title=title,
    )
    db.add(node)
    await db.flush()
    activity = Activity(
        plan_week_id=week.id,
        household_id=household.id,
        title=f"Practice {title}",
        activity_type=ActivityType.practice,
        node_id=node.id,
    )
    db.add(activity)
    await db.flush()

    now = datetime.now(UTC)
    for i in range(attempts):
        # i=0 is the oldest (now - span_days), the last is now.
        offset = span_days - (span_days * i // (attempts - 1)) if attempts > 1 else 0
        ts = now - timedelta(days=offset)
        db.add(
            Attempt(
                activity_id=activity.id,
                household_id=household.id,
                child_id=child.id,
                status=AttemptStatus.completed,
                score=score,
                duration_minutes=20,
                started_at=ts,
                completed_at=ts,
            )
        )
    db.add(
        ChildNodeState(
            child_id=child.id,
            household_id=household.id,
            node_id=node.id,
            mastery_level=mastery,
            attempts_count=attempts,
            last_activity_at=now,
        )
    )
    db.add(
        StateEvent(
            child_id=child.id,
            household_id=household.id,
            node_id=node.id,
            event_type=StateEventType.mastery_change,
            from_state="developing",
            to_state=mastery.value,
        )
    )
    await db.flush()
    return node


async def _enable_memory(db, household, child) -> ChildTutorPreferences:
    ctp = ChildTutorPreferences(household_id=household.id, child_id=child.id, relationship_memory="on")
    db.add(ctp)
    await db.flush()
    return ctp


# ── 1. Breakthrough detection ───────────────────────────────────────────


@pytest.mark.asyncio
async def test_breakthrough_detected_on_long_struggle(db_session, household, child, plan_week):
    lmap = await _subject_map(db_session, household, "Mathematics", "Math Unit")
    await _seed_node(
        db_session, household, child, lmap, plan_week, "Long Division", MasteryLevel.mastered, attempts=4, span_days=42
    )
    milestones = await derive_milestones(db_session, child.id)
    breaks = [m for m in milestones if m.kind == "breakthrough"]
    assert len(breaks) == 1
    assert breaks[0].title == "Long Division"
    assert "Long Division" in breaks[0].line
    assert "weeks" in breaks[0].line  # measured in weeks of effort


@pytest.mark.asyncio
async def test_breakthrough_detected_on_many_attempts(db_session, household, child, plan_week):
    # Short span (under 14 days) but many attempts: still a breakthrough,
    # rendered as persistence with no number.
    lmap = await _subject_map(db_session, household, "Mathematics", "Math Unit")
    await _seed_node(
        db_session, household, child, lmap, plan_week, "Fractions", MasteryLevel.proficient, attempts=6, span_days=3
    )
    milestones = await derive_milestones(db_session, child.id)
    breaks = [m for m in milestones if m.kind == "breakthrough"]
    assert len(breaks) == 1
    assert breaks[0].title == "Fractions"
    assert "Fractions" in breaks[0].line


@pytest.mark.asyncio
async def test_quick_mastery_excluded_from_breakthroughs(db_session, household, child, plan_week):
    # Reached fast (two attempts, same day): not a breakthrough. It may
    # still be a gentle "first", but never a struggle-then-click arc.
    lmap = await _subject_map(db_session, household, "Mathematics", "Math Unit")
    await _seed_node(
        db_session, household, child, lmap, plan_week, "Counting", MasteryLevel.mastered, attempts=2, span_days=0
    )
    milestones = await derive_milestones(db_session, child.id)
    assert [m for m in milestones if m.kind == "breakthrough"] == []


# ── 2. Completion, first, streak detection ──────────────────────────────


@pytest.mark.asyncio
async def test_completion_detected_when_unit_fully_reached(db_session, household, child, plan_week):
    lmap = await _subject_map(db_session, household, "Science", "Science Unit")
    await _seed_node(db_session, household, child, lmap, plan_week, "Cells", MasteryLevel.mastered, attempts=2)
    await _seed_node(db_session, household, child, lmap, plan_week, "Atoms", MasteryLevel.proficient, attempts=2)
    db_session.add(ChildMapEnrollment(child_id=child.id, household_id=household.id, learning_map_id=lmap.id))
    await db_session.flush()

    milestones = await derive_milestones(db_session, child.id)
    completions = [m for m in milestones if m.kind == "completion"]
    assert len(completions) == 1
    assert completions[0].title == "Science Unit"
    assert "Science" in completions[0].line


@pytest.mark.asyncio
async def test_completion_not_detected_when_unit_partial(db_session, household, child, plan_week):
    lmap = await _subject_map(db_session, household, "Science", "Science Unit")
    await _seed_node(db_session, household, child, lmap, plan_week, "Cells", MasteryLevel.mastered, attempts=2)
    # A second active node the child has NOT reached lives in the map but
    # gets no ChildNodeState, so the unit is not complete.
    unreached = LearningNode(
        learning_map_id=lmap.id, household_id=household.id, node_type=NodeType.concept, title="Atoms"
    )
    db_session.add(unreached)
    db_session.add(ChildMapEnrollment(child_id=child.id, household_id=household.id, learning_map_id=lmap.id))
    await db_session.flush()

    milestones = await derive_milestones(db_session, child.id)
    assert [m for m in milestones if m.kind == "completion"] == []


@pytest.mark.asyncio
async def test_first_detected_for_a_subject(db_session, household, child, plan_week):
    lmap = await _subject_map(db_session, household, "Latin", "Latin Unit")
    await _seed_node(
        db_session, household, child, lmap, plan_week, "First Declension", MasteryLevel.mastered, attempts=2
    )
    milestones = await derive_milestones(db_session, child.id)
    firsts = [m for m in milestones if m.kind == "first"]
    assert len(firsts) == 1
    assert firsts[0].subject == "Latin"
    assert "Latin" in firsts[0].line
    assert "First Declension" in firsts[0].line


@pytest.mark.asyncio
async def test_streak_detected_above_threshold(db_session, household, child):
    db_session.add(
        Streak(
            child_id=child.id,
            household_id=household.id,
            current_streak=7,
            longest_streak=20,
            last_activity_date=date(2026, 6, 12),
        )
    )
    await db_session.flush()
    milestones = await derive_milestones(db_session, child.id)
    streaks = [m for m in milestones if m.kind == "streak"]
    assert len(streaks) == 1
    assert "20 days" in streaks[0].line


@pytest.mark.asyncio
async def test_streak_below_threshold_excluded(db_session, household, child):
    db_session.add(Streak(child_id=child.id, household_id=household.id, current_streak=2, longest_streak=3))
    await db_session.flush()
    milestones = await derive_milestones(db_session, child.id)
    assert [m for m in milestones if m.kind == "streak"] == []


# ── 3. Ranking and the cap of three ─────────────────────────────────────


@pytest.mark.asyncio
async def test_ranking_and_cap_of_three(db_session, household, child, plan_week):
    # A breakthrough (math, not enrolled so no completion), a completed
    # unit (science, enrolled), a notable streak, and a first (the science
    # nodes also yield a first). Four candidate kinds, capped at three,
    # ordered breakthrough > completion > streak; the first is dropped.
    math = await _subject_map(db_session, household, "Mathematics", "Math Unit")
    await _seed_node(
        db_session, household, child, math, plan_week, "Long Division", MasteryLevel.mastered, attempts=4, span_days=42
    )
    sci = await _subject_map(db_session, household, "Science", "Science Unit")
    await _seed_node(db_session, household, child, sci, plan_week, "Cells", MasteryLevel.mastered, attempts=2)
    db_session.add(ChildMapEnrollment(child_id=child.id, household_id=household.id, learning_map_id=sci.id))
    db_session.add(Streak(child_id=child.id, household_id=household.id, current_streak=10, longest_streak=10))
    await db_session.flush()

    milestones = await derive_milestones(db_session, child.id)
    assert len(milestones) == 3
    assert [m.kind for m in milestones] == ["breakthrough", "completion", "streak"]


# ── 4. Dignity rule: no failure counts ──────────────────────────────────


@pytest.mark.asyncio
async def test_templates_never_print_failure_counts(db_session, household, child, plan_week):
    # Fourteen attempts all scoring zero over six weeks: a hard, drawn out
    # struggle. The rendered line must never surface "14" (the attempt or
    # failure count) and must never use the word "fail".
    lmap = await _subject_map(db_session, household, "Mathematics", "Math Unit")
    await _seed_node(
        db_session,
        household,
        child,
        lmap,
        plan_week,
        "Long Division",
        MasteryLevel.mastered,
        attempts=14,
        span_days=42,
        score=0.0,
    )
    milestones = await derive_milestones(db_session, child.id)
    assert milestones
    for m in milestones:
        assert "14" not in m.line, f"raw count leaked into: {m.line}"
        assert "fail" not in m.line.lower(), f"failure language leaked into: {m.line}"


# ── 5. Opt in gate at context assembly ──────────────────────────────────


@pytest.mark.asyncio
async def test_off_by_default_no_derivation_runs(db_session, household, child, plan_week, monkeypatch):
    # Default off: build_milestone_block must inject nothing AND never call
    # the (potentially expensive) milestone derivation.
    lmap = await _subject_map(db_session, household, "Mathematics", "Math Unit")
    await _seed_node(
        db_session, household, child, lmap, plan_week, "Long Division", MasteryLevel.mastered, attempts=4, span_days=42
    )

    calls = {"n": 0}

    async def _spy(db, child_id):
        calls["n"] += 1
        return []

    monkeypatch.setattr(tm, "get_milestones", _spy)
    block = await build_milestone_block(db_session, household.id, child.id, "tutor")
    assert block == ""
    assert calls["n"] == 0


@pytest.mark.asyncio
async def test_non_tutor_role_injects_nothing(db_session, household, child):
    await _enable_memory(db_session, household, child)
    block = await build_milestone_block(db_session, household.id, child.id, "evaluator")
    assert block == ""


@pytest.mark.asyncio
async def test_on_injects_block_with_milestones(db_session, household, child, plan_week):
    lmap = await _subject_map(db_session, household, "Mathematics", "Math Unit")
    await _seed_node(
        db_session, household, child, lmap, plan_week, "Long Division", MasteryLevel.mastered, attempts=4, span_days=42
    )
    await _enable_memory(db_session, household, child)

    block = await build_milestone_block(db_session, household.id, child.id, "tutor")
    assert "TUTOR RELATIONSHIP MEMORY" in block
    assert "naturally and sparingly" in block
    assert "Long Division" in block
    assert block.count("\n- ") >= 1  # at least one delimited milestone line


@pytest.mark.asyncio
async def test_disable_then_assemble_injects_nothing(auth_client: AsyncClient, db_session, household, child, plan_week):
    lmap = await _subject_map(db_session, household, "Mathematics", "Math Unit")
    await _seed_node(
        db_session, household, child, lmap, plan_week, "Long Division", MasteryLevel.mastered, attempts=4, span_days=42
    )
    on = await auth_client.put(f"/api/v1/children/{child.id}/tutor-register", json={"relationship_memory": "on"})
    assert on.status_code == 200, on.text
    assert "TUTOR RELATIONSHIP MEMORY" in await build_milestone_block(db_session, household.id, child.id, "tutor")

    # Disabling logs the counterpart, invalidates the cache, and takes
    # effect on the next assembly: nothing is injected.
    off = await auth_client.put(f"/api/v1/children/{child.id}/tutor-register", json={"relationship_memory": "off"})
    assert off.status_code == 200, off.text
    assert await build_milestone_block(db_session, household.id, child.id, "tutor") == ""


# ── 6. Governance events and chain integrity ────────────────────────────


@pytest.mark.asyncio
async def test_enable_disable_log_events_and_chain_valid(auth_client: AsyncClient, db_session, household, child):
    enable = await auth_client.put(f"/api/v1/children/{child.id}/tutor-register", json={"relationship_memory": "on"})
    assert enable.status_code == 200, enable.text
    assert enable.json()["relationship_memory"] == "on"
    disable = await auth_client.put(f"/api/v1/children/{child.id}/tutor-register", json={"relationship_memory": "off"})
    assert disable.status_code == 200
    assert disable.json()["relationship_memory"] == "off"

    types = {
        row[0]
        for row in (
            await db_session.execute(
                select(GovernanceEvent.target_type).where(GovernanceEvent.household_id == household.id)
            )
        ).all()
    }
    assert "tutor_relationship_memory_enabled" in types
    assert "tutor_relationship_memory_disabled" in types

    verify = await auth_client.get("/api/v1/chain/verify")
    assert verify.status_code == 200
    assert verify.json()["valid"] is True


@pytest.mark.asyncio
async def test_register_override_write_leaves_memory_untouched(auth_client: AsyncClient, db_session, child):
    # A write to one field never disturbs the other.
    await auth_client.put(f"/api/v1/children/{child.id}/tutor-register", json={"relationship_memory": "on"})
    resp = await auth_client.put(
        f"/api/v1/children/{child.id}/tutor-register", json={"register_override": "intermediate"}
    )
    assert resp.status_code == 200
    assert resp.json()["relationship_memory"] == "on"
    assert resp.json()["register_override"] == "intermediate"


@pytest.mark.asyncio
async def test_invalid_relationship_memory_rejected(auth_client: AsyncClient, child):
    resp = await auth_client.put(f"/api/v1/children/{child.id}/tutor-register", json={"relationship_memory": "maybe"})
    assert resp.status_code == 422


# ── 7. Preview equals injection (same source proof) ─────────────────────


@pytest.mark.asyncio
async def test_preview_equals_injected_milestones(auth_client: AsyncClient, db_session, household, child, plan_week):
    math = await _subject_map(db_session, household, "Mathematics", "Math Unit")
    await _seed_node(
        db_session, household, child, math, plan_week, "Long Division", MasteryLevel.mastered, attempts=4, span_days=42
    )
    db_session.add(Streak(child_id=child.id, household_id=household.id, current_streak=8, longest_streak=8))
    await _enable_memory(db_session, household, child)

    preview = await auth_client.get(f"/api/v1/children/{child.id}/tutor-register/milestones")
    assert preview.status_code == 200, preview.text
    preview_lines = [m["line"] for m in preview.json()["milestones"]]
    assert preview_lines  # there is something to remember

    block = await build_milestone_block(db_session, household.id, child.id, "tutor")
    injected_lines = [ln[len("- ") :] for ln in block.splitlines() if ln.startswith("- ")]

    assert preview_lines == injected_lines


# ── 8. Zero database writes and no migration guards ─────────────────────


@pytest.mark.asyncio
async def test_module_performs_no_database_writes(db_session, household, child, plan_week):
    # Source guard: no ORM write idioms anywhere in the module.
    source = Path(tm.__file__).read_text()
    assert "db.add" not in source, "the derived layer never adds rows"
    assert "session.add" not in source
    assert ".commit(" not in source, "the derived layer never commits"

    # Runtime guard: derivation and the cached read leave the session with
    # no pending new or dirty objects (mirrors test_family_record's guard).
    lmap = await _subject_map(db_session, household, "Mathematics", "Math Unit")
    await _seed_node(
        db_session, household, child, lmap, plan_week, "Long Division", MasteryLevel.mastered, attempts=4, span_days=42
    )
    await db_session.flush()
    await derive_milestones(db_session, child.id)
    assert not db_session.new and not db_session.dirty
    await get_milestones(db_session, child.id)
    assert not db_session.new and not db_session.dirty


def test_no_migration_added_to_diff():
    # Relationship memory is a computed view; the diff must contain no
    # Alembic migration. Same git assertion as the prior derived layer.
    repo_root = Path(__file__).resolve().parents[2]
    base = None
    for ref in ("origin/main", "main"):
        probe = subprocess.run(["git", "rev-parse", "--verify", ref], cwd=repo_root, capture_output=True, text=True)
        if probe.returncode == 0:
            base = ref
            break
    if base is None:
        pytest.skip("no main ref available to diff against")
    diff = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"], cwd=repo_root, capture_output=True, text=True
    )
    if diff.returncode != 0:
        pytest.skip("git diff unavailable")
    migrations = [f for f in diff.stdout.splitlines() if "alembic/versions/" in f]
    assert migrations == [], f"relationship memory must add no migration; found {migrations}"


# ── 9. Access control ───────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_preview_child_scope_denied(client: AsyncClient, household, user, child):
    from app.core.security import create_access_token

    token = create_access_token(user.id, household.id, "owner", scope="child", child_id=child.id)
    client.cookies.set("access_token", token)
    resp = await client.get(f"/api/v1/children/{child.id}/tutor-register/milestones")
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_preview_household_isolation(client: AsyncClient, db_session, household, child):
    from app.core.database import set_tenant
    from app.core.security import create_access_token, hash_password
    from app.models.identity import Household, User

    other = Household(name="Other Family", subscription_status="trialing")
    db_session.add(other)
    await db_session.flush()
    await set_tenant(db_session, other.id)
    other_user = User(
        household_id=other.id,
        email="other-milestones@test.com",
        password_hash=hash_password("testpass123"),
        display_name="Other Parent",
        role="owner",
        email_verified=True,
    )
    db_session.add(other_user)
    await db_session.flush()

    token = create_access_token(other_user.id, other.id, "owner")
    client.cookies.set("access_token", token)
    resp = await client.get(f"/api/v1/children/{child.id}/tutor-register/milestones")
    assert resp.status_code == 404
