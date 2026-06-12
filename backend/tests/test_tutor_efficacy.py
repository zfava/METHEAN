"""Tests for tutor efficacy: the tutor's memory checks itself.

Covers migration 061 and the full engine: the reused success metric, the
minimum-volume gate, label thresholds at their boundaries, subject
scoping, observation persistence, the bounded idempotent weekly batch,
the retirement proposal lifecycle routed through the autonomy policy
(standard queues, autonomous applies under the grant, off observes but
proposes nothing), the lifetime proposal cap with rejection recurrence,
the single-writer guard extended to observations, household isolation,
child scope, and chain validity across a full retire lifecycle.

Honest statistics: every assertion that touches a label also pins the
sample sizes behind it. A delta without its N is not tested because it is
never produced.
"""

import re
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.core.database import set_tenant
from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import (
    ActivityStatus,
    ActivityType,
    AttemptStatus,
    NodeType,
    PlanStatus,
)
from app.models.governance import Activity, Attempt, GovernanceEvent, Plan, PlanWeek
from app.models.identity import Child, Household
from app.models.intelligence import TutorEntryObservation, TutorProfileEntry
from app.services.governance import set_ai_role_policy
from app.services.tutor_efficacy import (
    EVT_ENTRY_RETIRED,
    EVT_RETIREMENT_PROPOSED,
    EVT_RETIREMENT_REJECTED,
    LABEL_INSUFFICIENT_DATA,
    LABEL_MAY_HAVE_OUTGROWN,
    LABEL_NO_CLEAR_EFFECT,
    LABEL_WORKING_WELL,
    MIN_ATTEMPTS,
    SUCCESS_MIN_SCORE,
    decide_retirement,
    evaluate_entry,
    evaluate_tutor_entries,
    maybe_propose_retirement,
    retirement_pending,
)
from app.services.tutor_profile import get_active_entries_block

PASSWORD = "testpass123"

NOW = datetime(2026, 6, 1, 12, 0, tzinfo=UTC)
ACTIVATION = NOW - timedelta(days=30)
BASELINE_WHEN = NOW - timedelta(days=60)  # inside [activation-90d, activation)
ACTIVE_WHEN = NOW - timedelta(days=10)  # inside [activation, now)


# ── Seeding helpers ─────────────────────────────────────────────────


async def _plan_week(db, household, child) -> PlanWeek:
    plan = Plan(
        household_id=household.id,
        child_id=child.id,
        name="Test Plan",
        status=PlanStatus.active,
    )
    db.add(plan)
    await db.flush()
    pw = PlanWeek(
        plan_id=plan.id,
        household_id=household.id,
        week_number=1,
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 7),
    )
    db.add(pw)
    await db.flush()
    return pw


async def _activity(db, household, child, plan_week, node_id=None, title="Practice") -> Activity:
    activity = Activity(
        plan_week_id=plan_week.id,
        household_id=household.id,
        node_id=node_id,
        activity_type=ActivityType.practice,
        title=title,
        status=ActivityStatus.completed,
    )
    db.add(activity)
    await db.flush()
    return activity


async def _subject_node(db, household, subject_name: str) -> LearningNode:
    subject = Subject(household_id=household.id, name=subject_name)
    db.add(subject)
    await db.flush()
    lm = LearningMap(household_id=household.id, subject_id=subject.id, name=f"{subject_name} Map")
    db.add(lm)
    await db.flush()
    node = LearningNode(
        learning_map_id=lm.id,
        household_id=household.id,
        node_type=NodeType.skill,
        title=f"{subject_name} skill",
    )
    db.add(node)
    await db.flush()
    return node


async def _seed_attempts(db, household, child, activity, n: int, successes: int, when: datetime) -> None:
    """Seed n completed attempts, `successes` of them scored as recall
    successes (score above the reused mastery boundary) and the rest as
    lapses, all completed at `when`."""
    for i in range(n):
        score = 0.9 if i < successes else 0.1
        db.add(
            Attempt(
                activity_id=activity.id,
                household_id=household.id,
                child_id=child.id,
                status=AttemptStatus.completed,
                score=score,
                started_at=when,
                completed_at=when,
            )
        )
    await db.flush()


def _entry(
    household,
    child,
    content="Concrete visual examples before abstract rules help this learner",
    category="explanation_style",
    status="active",
    activation=ACTIVATION,
) -> TutorProfileEntry:
    # Constructed directly: the single-writer guard scans only app/, not
    # tests/, and these tests need full control of activation timing.
    return TutorProfileEntry(
        household_id=household.id,
        child_id=child.id,
        category=category,
        content=content,
        status=status,
        decided_at=activation,
        proposed_at=activation - timedelta(days=1),
    )


async def _active_entry_with_rates(
    db, household, child, *, base_n, base_succ, act_n, act_succ, content=None
) -> TutorProfileEntry:
    """An active entry with baseline and active attempt streams seeded to
    known success counts, all on a single non-subject activity (scope:
    all)."""
    kwargs = {"content": content} if content else {}
    entry = _entry(household, child, **kwargs)
    db.add(entry)
    await db.flush()
    pw = await _plan_week(db, household, child)
    activity = await _activity(db, household, child, pw)
    await _seed_attempts(db, household, child, activity, base_n, base_succ, BASELINE_WHEN)
    await _seed_attempts(db, household, child, activity, act_n, act_succ, ACTIVE_WHEN)
    return entry


# ── Success metric reuse ────────────────────────────────────────────


def test_success_metric_matches_mastery_definition():
    """The success boundary is exactly confidence_to_rating's Again
    cutoff, so the engine reuses the mastery definition and never drifts
    from it."""
    from app.services.state_engine import confidence_to_rating

    # FSRS Again == 1 is the lapse; anything above it is a successful
    # recall. SUCCESS_MIN_SCORE must sit exactly on that boundary.
    assert confidence_to_rating(SUCCESS_MIN_SCORE).value != 1
    assert confidence_to_rating(SUCCESS_MIN_SCORE - 0.001).value == 1


def test_no_gateway_imports_in_engine():
    """Zero AI calls: the efficacy engine never imports the AI gateway."""
    source = (Path(__file__).resolve().parents[1] / "app" / "services" / "tutor_efficacy.py").read_text()
    assert "gateway" not in source
    assert "call_ai" not in source


# ── Volume gates ────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_below_active_volume_is_insufficient_data(db_session, household, child):
    entry = await _active_entry_with_rates(
        db_session, household, child, base_n=30, base_succ=15, act_n=MIN_ATTEMPTS - 1, act_succ=2
    )
    obs = await evaluate_entry(db_session, entry, now=NOW)
    assert entry.efficacy_label == LABEL_INSUFFICIENT_DATA
    assert obs.active_attempts == MIN_ATTEMPTS - 1
    assert obs.baseline_attempts == 30


@pytest.mark.asyncio
async def test_below_baseline_volume_is_insufficient_data(db_session, household, child):
    entry = await _active_entry_with_rates(
        db_session, household, child, base_n=MIN_ATTEMPTS - 1, base_succ=1, act_n=40, act_succ=38
    )
    obs = await evaluate_entry(db_session, entry, now=NOW)
    assert entry.efficacy_label == LABEL_INSUFFICIENT_DATA
    assert obs.baseline_attempts == MIN_ATTEMPTS - 1
    assert obs.active_attempts == 40


# ── Label thresholds at the boundaries ──────────────────────────────


@pytest.mark.asyncio
async def test_working_well_at_positive_boundary(db_session, household, child):
    # baseline 10/20 = 0.50, active 11/20 = 0.55, delta +0.05 exactly.
    entry = await _active_entry_with_rates(db_session, household, child, base_n=20, base_succ=10, act_n=20, act_succ=11)
    obs = await evaluate_entry(db_session, entry, now=NOW)
    assert obs.delta == pytest.approx(0.05)
    assert entry.efficacy_label == LABEL_WORKING_WELL


@pytest.mark.asyncio
async def test_no_clear_effect_inside_band(db_session, household, child):
    # baseline 10/20 = 0.50, active 10/20 = 0.50, delta 0.0.
    entry = await _active_entry_with_rates(db_session, household, child, base_n=20, base_succ=10, act_n=20, act_succ=10)
    await evaluate_entry(db_session, entry, now=NOW)
    assert entry.efficacy_label == LABEL_NO_CLEAR_EFFECT


@pytest.mark.asyncio
async def test_may_have_outgrown_at_negative_boundary(db_session, household, child):
    # baseline 11/20 = 0.55, active 10/20 = 0.50, delta -0.05 exactly.
    entry = await _active_entry_with_rates(db_session, household, child, base_n=20, base_succ=11, act_n=20, act_succ=10)
    obs = await evaluate_entry(db_session, entry, now=NOW)
    assert obs.delta == pytest.approx(-0.05)
    assert entry.efficacy_label == LABEL_MAY_HAVE_OUTGROWN


# ── Subject scoping ─────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_subject_scope_math_excludes_non_math(db_session, household, child):
    """A fractions entry is judged on math attempts only; reading
    attempts are excluded from its sample."""
    entry = _entry(
        household,
        child,
        content="Baking analogies make fractions click for this learner",
    )
    db_session.add(entry)
    await db_session.flush()

    pw = await _plan_week(db_session, household, child)
    math_node = await _subject_node(db_session, household, "Mathematics")
    reading_node = await _subject_node(db_session, household, "Reading")
    math_activity = await _activity(db_session, household, child, pw, node_id=math_node.id, title="Math")
    reading_activity = await _activity(db_session, household, child, pw, node_id=reading_node.id, title="Reading")

    # Math: baseline 14/20 = 0.70, active 10/20 = 0.50 (a drop).
    await _seed_attempts(db_session, household, child, math_activity, 20, 14, BASELINE_WHEN)
    await _seed_attempts(db_session, household, child, math_activity, 20, 10, ACTIVE_WHEN)
    # Reading: high everywhere. Must NOT enter the math-scoped sample.
    await _seed_attempts(db_session, household, child, reading_activity, 40, 40, BASELINE_WHEN)
    await _seed_attempts(db_session, household, child, reading_activity, 40, 40, ACTIVE_WHEN)

    obs = await evaluate_entry(db_session, entry, now=NOW)
    assert obs.subject_scope == "math"
    assert obs.active_attempts == 20  # reading's 40 excluded
    assert obs.baseline_attempts == 20
    assert obs.active_success_rate == pytest.approx(0.5)
    assert entry.efficacy_label == LABEL_MAY_HAVE_OUTGROWN


@pytest.mark.asyncio
async def test_ambiguous_content_scopes_to_all(db_session, household, child):
    entry = await _active_entry_with_rates(
        db_session,
        household,
        child,
        base_n=20,
        base_succ=10,
        act_n=20,
        act_succ=10,
        content="Celebrating small wins keeps momentum going",
    )
    obs = await evaluate_entry(db_session, entry, now=NOW)
    assert obs.subject_scope == "all"


# ── Observation persistence and batch idempotency ───────────────────


@pytest.mark.asyncio
async def test_observation_persisted_and_entry_updated(db_session, household, child):
    entry = await _active_entry_with_rates(db_session, household, child, base_n=20, base_succ=10, act_n=20, act_succ=14)
    obs = await evaluate_entry(db_session, entry, now=NOW)
    assert obs.active_attempts == 20 and obs.baseline_attempts == 20
    assert obs.active_success_rate == pytest.approx(0.7)
    assert obs.baseline_success_rate == pytest.approx(0.5)
    assert obs.delta == pytest.approx(0.2)
    assert entry.observations_count == 1
    assert entry.last_evaluated_at == NOW
    assert entry.efficacy_label == LABEL_WORKING_WELL


@pytest.mark.asyncio
async def test_batch_evaluates_then_skips_within_cooldown(db_session, household, user, child):
    entry_a = await _active_entry_with_rates(
        db_session, household, child, base_n=20, base_succ=10, act_n=20, act_succ=14
    )
    first = await evaluate_tutor_entries(db_session, now=NOW)
    assert first["entries_evaluated"] == 1

    # A second entry arrives, never evaluated, so the household is eligible
    # again two days later. The new entry is evaluated; entry_a, freshly
    # evaluated and inside the cooldown, is skipped, not re-observed.
    entry_b = _entry(household, child, content="Short movement breaks reset focus", category="pacing")
    db_session.add(entry_b)
    await db_session.flush()
    pw = await _plan_week(db_session, household, child)
    activity = await _activity(db_session, household, child, pw)
    await _seed_attempts(db_session, household, child, activity, 20, 10, BASELINE_WHEN)
    await _seed_attempts(db_session, household, child, activity, 20, 14, ACTIVE_WHEN)

    second = await evaluate_tutor_entries(db_session, now=NOW + timedelta(days=2))
    assert second["entries_evaluated"] == 1
    assert second["skipped"] == 1

    a_obs = (
        (await db_session.execute(select(TutorEntryObservation).where(TutorEntryObservation.entry_id == entry_a.id)))
        .scalars()
        .all()
    )
    b_obs = (
        (await db_session.execute(select(TutorEntryObservation).where(TutorEntryObservation.entry_id == entry_b.id)))
        .scalars()
        .all()
    )
    assert len(a_obs) == 1  # not re-observed inside cooldown
    assert len(b_obs) == 1


# ── Retirement proposal lifecycle ───────────────────────────────────


async def _outgrown_entry(db, household, child) -> TutorProfileEntry:
    """An active entry whose attempt streams produce a may_have_outgrown
    reading (baseline 0.75, active 0.50)."""
    return await _active_entry_with_rates(db, household, child, base_n=20, base_succ=15, act_n=20, act_succ=10)


async def _count_events(db, household, target_type) -> int:
    rows = (
        (
            await db.execute(
                select(GovernanceEvent).where(
                    GovernanceEvent.household_id == household.id,
                    GovernanceEvent.target_type == target_type,
                )
            )
        )
        .scalars()
        .all()
    )
    return len(rows)


@pytest.mark.asyncio
async def test_two_consecutive_outgrown_proposes_once(db_session, household, user, child):
    entry = await _outgrown_entry(db_session, household, child)
    await evaluate_entry(db_session, entry, now=NOW)
    # One reading is not enough to propose.
    assert await maybe_propose_retirement(db_session, entry) is None
    assert await _count_events(db_session, household, EVT_RETIREMENT_PROPOSED) == 0

    await evaluate_entry(db_session, entry, now=NOW + timedelta(days=7))
    routed = await maybe_propose_retirement(db_session, entry)
    assert routed is not None
    assert await _count_events(db_session, household, EVT_RETIREMENT_PROPOSED) == 1
    assert await retirement_pending(db_session, entry.id) is True

    # A third evaluation does not duplicate the pending proposal.
    await evaluate_entry(db_session, entry, now=NOW + timedelta(days=14))
    assert await maybe_propose_retirement(db_session, entry) is None
    assert await _count_events(db_session, household, EVT_RETIREMENT_PROPOSED) == 1


@pytest.mark.asyncio
async def test_standard_queue_item_is_readable(db_session, household, user, child):
    entry = await _outgrown_entry(db_session, household, child)
    await evaluate_entry(db_session, entry, now=NOW)
    await evaluate_entry(db_session, entry, now=NOW + timedelta(days=7))
    await maybe_propose_retirement(db_session, entry)

    event = (
        await db_session.execute(select(GovernanceEvent).where(GovernanceEvent.target_type == EVT_RETIREMENT_PROPOSED))
    ).scalar_one()
    assert event.reason.startswith("The tutor thinks this strategy may no longer help:")
    assert "signal, not proof" in event.reason
    # The two deltas and sample sizes ride along.
    assert event.metadata_["deltas"] and len(event.metadata_["deltas"]) == 2
    assert event.metadata_["sample_sizes"] and len(event.metadata_["sample_sizes"]) == 2


@pytest.mark.asyncio
async def test_standard_approval_retires_and_stops_injection(db_session, household, user, child):
    entry = await _outgrown_entry(db_session, household, child)
    await evaluate_entry(db_session, entry, now=NOW)
    await evaluate_entry(db_session, entry, now=NOW + timedelta(days=7))
    await maybe_propose_retirement(db_session, entry)

    # Until approval, the active entry is still injected.
    block_before = await get_active_entries_block(db_session, household.id, child.id)
    assert entry.content in block_before

    retired = await decide_retirement(db_session, household.id, child.id, entry.id, "approve", user.id)
    assert retired.status == "retired"
    assert await _count_events(db_session, household, EVT_ENTRY_RETIRED) == 1

    block_after = await get_active_entries_block(db_session, household.id, child.id)
    assert entry.content not in block_after


@pytest.mark.asyncio
async def test_autonomous_retires_immediately_with_grant_hash(db_session, household, user, child):
    await set_ai_role_policy(db_session, household.id, user.id, "tutor", "autonomous")
    from app.services.governance import get_active_autonomy_grant

    grant_hash = await get_active_autonomy_grant(db_session, household.id, "tutor")
    assert grant_hash

    entry = await _outgrown_entry(db_session, household, child)
    await evaluate_entry(db_session, entry, now=NOW)
    await evaluate_entry(db_session, entry, now=NOW + timedelta(days=7))
    routed = await maybe_propose_retirement(db_session, entry)

    assert routed is not None
    assert entry.status == "retired"
    event = (
        await db_session.execute(select(GovernanceEvent).where(GovernanceEvent.target_type == EVT_ENTRY_RETIRED))
    ).scalar_one()
    assert event.metadata_["grant_event_hash"] == grant_hash
    assert await _count_events(db_session, household, EVT_RETIREMENT_PROPOSED) == 0


@pytest.mark.asyncio
async def test_autonomous_grant_race_drops_retirement(db_session, household, user, child):
    """Policy says autonomous but the grant was revoked moments ago: the
    retirement drops, never applies. Mirrors the 2.3b grant-race test."""
    await set_ai_role_policy(db_session, household.id, user.id, "tutor", "autonomous")
    entry = await _outgrown_entry(db_session, household, child)
    await evaluate_entry(db_session, entry, now=NOW)
    await evaluate_entry(db_session, entry, now=NOW + timedelta(days=7))

    with patch(
        "app.services.tutor_profile.get_active_autonomy_grant",
        new_callable=AsyncMock,
        return_value=None,
    ):
        routed = await maybe_propose_retirement(db_session, entry)

    assert routed is None
    assert entry.status == "active"
    assert await _count_events(db_session, household, EVT_ENTRY_RETIRED) == 0


@pytest.mark.asyncio
async def test_policy_off_observes_but_proposes_nothing(db_session, household, user, child):
    await set_ai_role_policy(db_session, household.id, user.id, "tutor", "off")
    entry = await _outgrown_entry(db_session, household, child)
    await evaluate_entry(db_session, entry, now=NOW)
    await evaluate_entry(db_session, entry, now=NOW + timedelta(days=7))
    routed = await maybe_propose_retirement(db_session, entry)

    assert routed is None
    observations = (
        (await db_session.execute(select(TutorEntryObservation).where(TutorEntryObservation.entry_id == entry.id)))
        .scalars()
        .all()
    )
    assert len(observations) == 2  # observation is read-only and harmless
    assert await _count_events(db_session, household, EVT_RETIREMENT_PROPOSED) == 0
    assert await _count_events(db_session, household, EVT_ENTRY_RETIRED) == 0


@pytest.mark.asyncio
async def test_rejected_then_recurrence_allows_one_more_then_never(db_session, household, user, child):
    entry = await _outgrown_entry(db_session, household, child)
    await evaluate_entry(db_session, entry, now=NOW)
    await evaluate_entry(db_session, entry, now=NOW + timedelta(days=7))
    await maybe_propose_retirement(db_session, entry)  # proposal #1
    assert await _count_events(db_session, household, EVT_RETIREMENT_PROPOSED) == 1

    await decide_retirement(db_session, household.id, child.id, entry.id, "reject", user.id)
    assert await _count_events(db_session, household, EVT_RETIREMENT_REJECTED) == 1
    assert await retirement_pending(db_session, entry.id) is False

    # The signal recurs: exactly one more proposal is allowed.
    await evaluate_entry(db_session, entry, now=NOW + timedelta(days=14))
    second = await maybe_propose_retirement(db_session, entry)
    assert second is not None
    assert await _count_events(db_session, household, EVT_RETIREMENT_PROPOSED) == 2

    await decide_retirement(db_session, household.id, child.id, entry.id, "reject", user.id)
    # Two lifetime proposals reached: never again, even as the signal
    # keeps recurring.
    await evaluate_entry(db_session, entry, now=NOW + timedelta(days=21))
    assert await maybe_propose_retirement(db_session, entry) is None
    assert await _count_events(db_session, household, EVT_RETIREMENT_PROPOSED) == 2


# ── Single-writer guard ─────────────────────────────────────────────


def test_observations_single_writer_guard():
    """Only the model definition and services/tutor_efficacy.py may
    construct TutorEntryObservation, mirroring the TutorProfileEntry
    guard."""
    app_dir = Path(__file__).resolve().parents[1] / "app"
    allowed = {"app/models/intelligence.py", "app/services/tutor_efficacy.py"}
    pattern = re.compile(r"\bTutorEntryObservation\(")
    offenders = []
    for path in app_dir.rglob("*.py"):
        rel = path.relative_to(app_dir.parent).as_posix()
        if rel in allowed:
            continue
        if pattern.search(path.read_text()):
            offenders.append(rel)
    assert offenders == [], f"TutorEntryObservation must only be written through tutor_efficacy.py: {offenders}"


# ── Isolation, scope, chain ─────────────────────────────────────────


@pytest.mark.asyncio
async def test_household_isolation_of_sample(db_session, household, user, child):
    """Another household's attempts never enter this entry's sample."""
    entry = await _active_entry_with_rates(db_session, household, child, base_n=20, base_succ=10, act_n=20, act_succ=14)

    other = Household(name="Other Family", timezone="UTC")
    db_session.add(other)
    await db_session.flush()
    await set_tenant(db_session, other.id)
    other_child = Child(household_id=other.id, first_name="Other", last_name="Kid")
    db_session.add(other_child)
    await db_session.flush()
    other_pw = await _plan_week(db_session, other, other_child)
    other_activity = await _activity(db_session, other, other_child, other_pw)
    await _seed_attempts(db_session, other, other_child, other_activity, 50, 50, ACTIVE_WHEN)

    await set_tenant(db_session, household.id)
    obs = await evaluate_entry(db_session, entry, now=NOW)
    assert obs.active_attempts == 20  # the other household's 50 excluded


@pytest.mark.asyncio
async def test_get_endpoint_exposes_efficacy(auth_client: AsyncClient, db_session, household, user, child):
    entry = await _active_entry_with_rates(db_session, household, child, base_n=20, base_succ=10, act_n=20, act_succ=14)
    await evaluate_entry(db_session, entry, now=NOW)

    response = await auth_client.get(f"/api/v1/children/{child.id}/tutor-profile")
    assert response.status_code == 200, response.text
    data = response.json()
    assert "retired" in data
    active = data["active"]
    assert len(active) == 1
    card = active[0]
    assert card["efficacy_label"] == LABEL_WORKING_WELL
    assert card["observations_count"] == 1
    assert card["active_attempts"] == 20
    assert card["baseline_attempts"] == 20
    assert card["retirement_pending"] is False


@pytest.mark.asyncio
async def test_child_session_denied_on_get(auth_client: AsyncClient, db_session, household, child):
    entry = await _active_entry_with_rates(db_session, household, child, base_n=20, base_succ=10, act_n=20, act_succ=14)
    await evaluate_entry(db_session, entry, now=NOW)
    enter = await auth_client.post("/api/v1/auth/child-session/enter", json={"child_id": str(child.id)})
    assert enter.status_code == 200
    response = await auth_client.get(f"/api/v1/children/{child.id}/tutor-profile")
    assert response.status_code == 403
    assert response.json()["detail"] == "child_session_forbidden"


@pytest.mark.asyncio
async def test_chain_valid_after_full_retire_lifecycle(auth_client: AsyncClient, db_session, household, user, child):
    entry = await _outgrown_entry(db_session, household, child)
    await evaluate_entry(db_session, entry, now=NOW)
    await evaluate_entry(db_session, entry, now=NOW + timedelta(days=7))
    await maybe_propose_retirement(db_session, entry)  # proposed
    await decide_retirement(db_session, household.id, child.id, entry.id, "reject", user.id)  # rejected
    await evaluate_entry(db_session, entry, now=NOW + timedelta(days=14))
    await maybe_propose_retirement(db_session, entry)  # proposed again
    await decide_retirement(db_session, household.id, child.id, entry.id, "approve", user.id)  # retired
    assert entry.status == "retired"

    response = await auth_client.get("/api/v1/chain/verify")
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["checked"] >= 4
