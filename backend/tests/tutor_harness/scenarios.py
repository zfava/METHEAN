"""Golden scenario definitions for the tutor context quality harness.

Six fully seeded households, each a named child with a story, that together
exercise every gate the assembled tutor context depends on: the four
context layers (developmental register, relationship milestones, parent
governed profile memory, live session signal), the autonomy spectrum (off,
standard, autonomous with a standing grant, and a revoked grant), and the
full profile entry lifecycle (proposed, active, rejected, retired, revoked).

Every scenario is seeded through the REAL services that own each write
path, the same fixture style the existing suite uses, so the harness
exercises the true contracts rather than fabricating rows:

  * tutor profile entries flow through tutor_profile.route_proposal,
    decide_entry, and revoke_entry, and tutor_efficacy.decide_retirement;
  * autonomy policy and standing grants flow through
    governance.set_ai_role_policy;
  * live session signals flow through tutor_session_signals.update_on_attempt;
  * relationship milestones are DERIVED from seeded mastery, attempt, and
    streak rows exactly as production derives them (never written directly).

The households are seeded once per test module (module scoped fixture) and
shared read only by the matrix and hygiene suites, which keeps the whole
package fast.
"""

import uuid
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta

import pytest_asyncio

import app.core.cache as cache_module
from app.core.database import Base, set_tenant
from app.core.security import hash_password
from app.models.achievements import Streak
from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import (
    ActivityType,
    AttemptStatus,
    MasteryLevel,
    NodeType,
    StateEventType,
)
from app.models.governance import Activity, Attempt, Plan, PlanWeek
from app.models.identity import Child, ChildPreferences, Household, User
from app.models.intelligence import ChildTutorPreferences, TutorProfileEntry
from app.models.state import ChildNodeState, StateEvent
from app.services.governance import (
    get_active_autonomy_grant,
    set_ai_role_policy,
)
from app.services.tutor_efficacy import (
    decide_retirement,
    maybe_propose_tier_lag_retirement,
)
from app.services.tutor_profile import decide_entry, revoke_entry, route_proposal
from app.services.tutor_session_signals import update_on_attempt
from tests.conftest import _apply_rls_policies, test_engine, test_session_factory

# ────────────────────────────────────────────────────────────────────────
# In memory Redis so the real signal write path and the milestone cache run
# ────────────────────────────────────────────────────────────────────────
#
# In the test process app.core.cache._redis is never initialized, so signals
# (a Redis only layer) cannot be seeded and read back. We install a small
# async, in process stand in for the duration of the harness module and
# restore the prior value on teardown. It supports exactly the operations the
# signal window plumbing and the cache helpers use.


class InMemoryRedis:
    """A minimal async Redis stand in: string get/set with TTL, delete,
    counters, and TTL inspection. Enough for the session signal window and
    the milestone/policy caches; never a full Redis."""

    def __init__(self) -> None:
        self._store: dict[str, str] = {}
        self._expiry: dict[str, datetime] = {}

    def _expired(self, key: str) -> bool:
        exp = self._expiry.get(key)
        if exp is not None and exp <= datetime.now(UTC):
            self._store.pop(key, None)
            self._expiry.pop(key, None)
            return True
        return False

    async def get(self, key: str):
        if self._expired(key):
            return None
        return self._store.get(key)

    async def set(self, key: str, value, ex: int | None = None):
        self._store[key] = value
        if ex is not None:
            self._expiry[key] = datetime.now(UTC) + timedelta(seconds=ex)
        else:
            self._expiry.pop(key, None)
        return True

    async def delete(self, *keys: str):
        removed = 0
        for key in keys:
            if self._store.pop(key, None) is not None:
                removed += 1
            self._expiry.pop(key, None)
        return removed

    async def incr(self, key: str):
        current = 0 if self._expired(key) else int(self._store.get(key, 0))
        current += 1
        self._store[key] = str(current)
        return current

    async def expire(self, key: str, seconds: int):
        if key in self._store:
            self._expiry[key] = datetime.now(UTC) + timedelta(seconds=seconds)
            return True
        return False

    async def ttl(self, key: str):
        exp = self._expiry.get(key)
        if exp is None:
            return -1
        return max(0, int((exp - datetime.now(UTC)).total_seconds()))

    async def scan_iter(self, match: str | None = None):
        for key in list(self._store.keys()):
            yield key


# ────────────────────────────────────────────────────────────────────────
# Scenario record: identity plus the expectations the matrix asserts on
# ────────────────────────────────────────────────────────────────────────


@dataclass
class Scenario:
    """One seeded household and the structural truths the harness asserts.

    The expectation fields are the contract: a scenario declares which tier
    the register must speak in, which live signal (if any) must be present,
    whether milestones must appear, which profile contents must be injected
    (active only), which must never appear (proposed/rejected/retired/
    revoked), and which strings (UUIDs, grant hashes) must never leak.
    """

    name: str
    story: str
    household_id: uuid.UUID
    child_id: uuid.UUID
    user_id: uuid.UUID
    node_id: uuid.UUID | None
    policy: str
    role_off: bool
    expected_tier: str
    expected_register_source: str
    expected_signal: str | None
    expect_milestones: bool
    active_contents: list[str] = field(default_factory=list)
    forbidden_contents: list[str] = field(default_factory=list)
    secret_strings: list[str] = field(default_factory=list)


@dataclass
class SeededWorld:
    session: object
    scenarios: dict[str, Scenario]


# ────────────────────────────────────────────────────────────────────────
# Seeding helpers (thin wrappers over real models and services)
# ────────────────────────────────────────────────────────────────────────


async def _household(session, name: str, email: str) -> tuple[Household, User]:
    household = Household(
        name=name,
        timezone="America/New_York",
        subscription_status="trialing",
        trial_ends_at=datetime.now(UTC) + timedelta(days=14),
    )
    session.add(household)
    await session.flush()
    await set_tenant(session, household.id)
    user = User(
        household_id=household.id,
        email=email,
        password_hash=hash_password("testpass123"),
        display_name="Parent",
        role="owner",
        email_verified=True,
    )
    session.add(user)
    await session.flush()
    return household, user


async def _child(session, household: Household, first_name: str) -> Child:
    child = Child(household_id=household.id, first_name=first_name, last_name="Learner")
    session.add(child)
    await session.flush()
    return child


async def _prefs(session, household: Household, child: Child, levels: dict) -> ChildPreferences:
    prefs = ChildPreferences(child_id=child.id, household_id=household.id, subject_levels=levels)
    session.add(prefs)
    await session.flush()
    return prefs


async def _subject_node(session, household: Household, subject_name: str, map_name: str, title: str) -> LearningNode:
    subject = Subject(household_id=household.id, name=subject_name)
    session.add(subject)
    await session.flush()
    lmap = LearningMap(household_id=household.id, subject_id=subject.id, name=map_name)
    session.add(lmap)
    await session.flush()
    node = LearningNode(
        learning_map_id=lmap.id,
        household_id=household.id,
        node_type=NodeType.concept,
        title=title,
    )
    session.add(node)
    await session.flush()
    return node


async def _plan_week(session, household: Household, child: Child) -> PlanWeek:
    plan = Plan(household_id=household.id, child_id=child.id, name="Plan", status="active")
    session.add(plan)
    await session.flush()
    week = PlanWeek(
        plan_id=plan.id,
        household_id=household.id,
        week_number=1,
        start_date=date(2026, 6, 8),
        end_date=date(2026, 6, 14),
    )
    session.add(week)
    await session.flush()
    return week


async def _seed_breakthrough(
    session,
    household: Household,
    child: Child,
    week: PlanWeek,
    subject_name: str,
    map_name: str,
    title: str,
    *,
    attempts: int,
    span_days: int,
) -> None:
    """A reached node whose pre mastery attempt history is long enough or
    persistent enough to derive as a breakthrough milestone. Mirrors the
    seeding shape the milestone tests use, so derivation sees real rows."""
    node = await _subject_node(session, household, subject_name, map_name, title)
    activity = Activity(
        plan_week_id=week.id,
        household_id=household.id,
        title=f"Practice {title}",
        activity_type=ActivityType.practice,
        node_id=node.id,
    )
    session.add(activity)
    await session.flush()

    now = datetime.now(UTC)
    for i in range(attempts):
        offset = span_days - (span_days * i // (attempts - 1)) if attempts > 1 else 0
        ts = now - timedelta(days=offset)
        session.add(
            Attempt(
                activity_id=activity.id,
                household_id=household.id,
                child_id=child.id,
                status=AttemptStatus.completed,
                score=0.8,
                duration_minutes=20,
                started_at=ts,
                completed_at=ts,
            )
        )
    session.add(
        ChildNodeState(
            child_id=child.id,
            household_id=household.id,
            node_id=node.id,
            mastery_level=MasteryLevel.mastered,
            attempts_count=attempts,
            last_activity_at=now,
        )
    )
    session.add(
        StateEvent(
            child_id=child.id,
            household_id=household.id,
            node_id=node.id,
            event_type=StateEventType.mastery_change,
            from_state="developing",
            to_state=MasteryLevel.mastered.value,
        )
    )
    await session.flush()


async def _streak(session, household: Household, child: Child, longest: int) -> None:
    session.add(
        Streak(
            child_id=child.id,
            household_id=household.id,
            current_streak=min(longest, 7),
            longest_streak=longest,
            last_activity_date=date(2026, 6, 12),
        )
    )
    await session.flush()


async def _active_by_approval(session, household, child, user, content: str, category: str) -> TutorProfileEntry:
    """The standard path to an active entry: the tutor proposes, the parent
    approves. Exercises route_proposal then decide_entry."""
    entry = await route_proposal(session, household.id, child.id, {"category": category, "content": content})
    assert entry is not None and entry.status == "proposed"
    decided = await decide_entry(session, household.id, child.id, entry.id, "approve", user.id)
    assert decided.status == "active"
    return decided


async def _proposed(session, household, child, content: str, category: str) -> TutorProfileEntry:
    entry = await route_proposal(session, household.id, child.id, {"category": category, "content": content})
    assert entry is not None and entry.status == "proposed"
    return entry


async def _rejected(session, household, child, user, content: str, category: str) -> TutorProfileEntry:
    entry = await route_proposal(session, household.id, child.id, {"category": category, "content": content})
    assert entry is not None and entry.status == "proposed"
    decided = await decide_entry(session, household.id, child.id, entry.id, "reject", user.id)
    assert decided.status == "rejected"
    return decided


async def _feed_signal(child: Child, outcomes: list[dict]) -> str | None:
    """Drive the real session signal window with a sequence of attempt
    outcomes and return the live signal it classifies to."""
    result = {"signal": None}
    for outcome in outcomes:
        result = await update_on_attempt(child.id, outcome)
    return result["signal"]


# ────────────────────────────────────────────────────────────────────────
# The six golden scenarios
# ────────────────────────────────────────────────────────────────────────


async def build_fresh_start(session) -> Scenario:
    """a. Fresh start: a brand new child, no history, all defaults (policy
    standard, memory empty, relationship off). The register still speaks,
    falling back to the most protective tier; nothing else appears."""
    household, user = await _household(session, "Fresh Family", "fresh@harness.test")
    child = await _child(session, household, "Robin")
    # No prefs, no node, no entries, no signal, default standard policy.
    return Scenario(
        name="fresh_start",
        story="A new child with no history at all. Defaults everywhere.",
        household_id=household.id,
        child_id=child.id,
        user_id=user.id,
        node_id=None,
        policy="standard",
        role_off=False,
        expected_tier="foundational",
        expected_register_source="derived",
        expected_signal=None,
        expect_milestones=False,
        active_contents=[],
        forbidden_contents=[],
        secret_strings=[],
    )


async def build_struggling_reader(session) -> Scenario:
    """b. The struggling reader: foundational tier, active profile entries
    about multisensory strategies, a mid session frustrated signal,
    relationship off."""
    household, user = await _household(session, "Reader Family", "reader@harness.test")
    child = await _child(session, household, "Sam")
    await _prefs(session, household, child, {"reading": "foundational"})
    node = await _subject_node(session, household, "Reading", "Early Reading", "Letter Sounds")

    multisensory = "Multisensory letter work with sand trays and tactile tiles helps this learner anchor new sounds."
    pacing = "Short reading bursts with a concrete win up front keep this learner moving through the tricky stretches."
    await _active_by_approval(session, household, child, user, multisensory, "explanation_style")
    await _active_by_approval(session, household, child, user, pacing, "pacing")

    # Mid session frustration: three wrong in a row on the same node.
    signal = await _feed_signal(
        child,
        [{"correct": False, "hints_used": 1, "node_id": str(node.id)} for _ in range(3)],
    )
    assert signal == "frustrated"

    return Scenario(
        name="struggling_reader",
        story="A foundational reader, multisensory strategies remembered, frustrated right now.",
        household_id=household.id,
        child_id=child.id,
        user_id=user.id,
        node_id=node.id,
        policy="standard",
        role_off=False,
        expected_tier="foundational",
        expected_register_source="derived",
        expected_signal="frustrated",
        expect_milestones=False,
        active_contents=[multisensory, pacing],
        forbidden_contents=[],
        secret_strings=[],
    )


async def build_cruising_mathematician(session) -> Scenario:
    """c. The cruising mathematician: intermediate tier, autonomous policy
    with an active standing grant, entries applied autonomously, a cruising
    signal, relationship on with a breakthrough milestone. Every one of the
    four layers is present, so this is the block ordering proof."""
    household, user = await _household(session, "Math Family", "math@harness.test")
    child = await _child(session, household, "Avery")
    await _prefs(session, household, child, {"mathematics": "intermediate"})
    node = await _subject_node(session, household, "Mathematics", "Math Core", "Ratios")

    # Autonomous: the standing grant is created here and every autonomous
    # entry cites its hash.
    await set_ai_role_policy(session, household.id, user.id, "tutor", "autonomous")
    grant_hash = await get_active_autonomy_grant(session, household.id, "tutor")
    assert grant_hash is not None

    applied = "Tying each new idea to a concrete real world ratio lets this learner reason it through independently."
    entry = await route_proposal(session, household.id, child.id, {"category": "explanation_style", "content": applied})
    assert entry is not None and entry.status == "active"
    assert entry.grant_event_hash == grant_hash

    # Relationship memory on, with a derivable breakthrough (many attempts).
    session.add(ChildTutorPreferences(household_id=household.id, child_id=child.id, relationship_memory="on"))
    await session.flush()
    week = await _plan_week(session, household, child)
    await _seed_breakthrough(
        session,
        household,
        child,
        week,
        "Mathematics",
        "Long Division Unit",
        "Long Division",
        attempts=6,
        span_days=3,
    )

    # Cruising right now: four clean correct attempts.
    signal = await _feed_signal(
        child,
        [{"correct": True, "hints_used": 0, "node_id": str(node.id)} for _ in range(4)],
    )
    assert signal == "cruising"

    return Scenario(
        name="cruising_mathematician",
        story="An intermediate mathematician under a standing grant, cruising, with a breakthrough remembered.",
        household_id=household.id,
        child_id=child.id,
        user_id=user.id,
        node_id=node.id,
        policy="autonomous",
        role_off=False,
        expected_tier="intermediate",
        expected_register_source="derived",
        expected_signal="cruising",
        expect_milestones=True,
        active_contents=[applied],
        forbidden_contents=[],
        secret_strings=[grant_hash],
    )


async def build_teenager(session) -> Scenario:
    """d. The teenager: mastery tier with a parent register override set one
    tier down (advanced), mixed entry statuses (active, retired, rejected),
    relationship on. The retired and rejected entries must never reach the
    tutor; only the active one does."""
    household, user = await _household(session, "Teen Family", "teen@harness.test")
    child = await _child(session, household, "Quinn")
    node = await _subject_node(session, household, "Mathematics", "Algebra", "Quadratics")

    # The to be retired strategy was learned at a much younger stage. Seed
    # the child low first so route_proposal stamps a foundational tier_band,
    # then advance the child to mastery so the tier lag retirement fires.
    early_prefs = await _prefs(session, household, child, {"mathematics": "foundational"})
    outgrown = "Counting blocks and drawing the problem out helped this learner picture early number work."
    retired_entry = await _active_by_approval(session, household, child, user, outgrown, "explanation_style")
    assert retired_entry.tier_band == "foundational"

    early_prefs.subject_levels = {"mathematics": "mastery"}
    await session.flush()
    routed = await maybe_propose_tier_lag_retirement(session, retired_entry)
    assert routed is not None
    retired = await decide_retirement(session, household.id, child.id, retired_entry.id, "approve", user.id)
    assert retired.status == "retired"

    # An active strategy that fits the teenager now, and a rejected proposal.
    active = "Giving this learner the goal and room to choose their own method keeps them invested in hard problems."
    await _active_by_approval(session, household, child, user, active, "motivation")
    rejected = "Frequent praise for small steps reassures this learner when a topic feels overwhelming."
    await _rejected(session, household, child, user, rejected, "motivation")

    # Parent voice: override one tier down from mastery, and relationship on.
    session.add(
        ChildTutorPreferences(
            household_id=household.id,
            child_id=child.id,
            register_override="advanced",
            relationship_memory="on",
        )
    )
    await session.flush()
    await _streak(session, household, child, longest=12)

    return Scenario(
        name="teenager",
        story="A mastery teen whose parent set the voice one notch down; mixed entry history, relationship on.",
        household_id=household.id,
        child_id=child.id,
        user_id=user.id,
        node_id=node.id,
        policy="standard",
        role_off=False,
        expected_tier="advanced",
        expected_register_source="override",
        expected_signal=None,
        expect_milestones=True,
        active_contents=[active],
        forbidden_contents=[outgrown, rejected],
        secret_strings=[],
    )


async def build_locked_down(session) -> Scenario:
    """e. Locked down: tutor policy off entirely. Memory, relationship, and
    signal data all exist, seeded while the role was on, but the off gate
    short circuits every layer before assembly, so none of the four blocks
    appear."""
    household, user = await _household(session, "Quiet Family", "quiet@harness.test")
    child = await _child(session, household, "Jordan")
    await _prefs(session, household, child, {"mathematics": "intermediate"})
    node = await _subject_node(session, household, "Mathematics", "Math Core", "Decimals")

    # Seed real content while the role is still standard.
    suppressed = "Working through one example aloud before independent practice settles this learner into a problem."
    await _active_by_approval(session, household, child, user, suppressed, "explanation_style")
    session.add(ChildTutorPreferences(household_id=household.id, child_id=child.id, relationship_memory="on"))
    await session.flush()
    await _streak(session, household, child, longest=15)
    await _feed_signal(child, [{"correct": True, "hints_used": 0, "node_id": str(node.id)} for _ in range(4)])

    # Now turn the tutor fully off.
    await set_ai_role_policy(session, household.id, user.id, "tutor", "off")

    return Scenario(
        name="locked_down",
        story="A family that turned the tutor off. Everything it would have said is suppressed.",
        household_id=household.id,
        child_id=child.id,
        user_id=user.id,
        node_id=node.id,
        policy="off",
        role_off=True,
        expected_tier="intermediate",
        expected_register_source="derived",
        expected_signal=None,
        expect_milestones=False,
        active_contents=[],
        forbidden_contents=[suppressed],
        secret_strings=[],
    )


async def build_revoked_grant(session) -> Scenario:
    """f. The revoked grant: previously autonomous (entries carrying grant
    hashes), now back to standard, with a revoked entry and a pending
    proposal in the queue. The active grant carrying entries still inject;
    the revoked and the pending proposal must not."""
    household, user = await _household(session, "Trust Family", "trust@harness.test")
    child = await _child(session, household, "Riley")
    await _prefs(session, household, child, {"mathematics": "advanced"})
    node = await _subject_node(session, household, "Mathematics", "Math Core", "Functions")

    # Grant, then two autonomous entries that cite the grant hash.
    await set_ai_role_policy(session, household.id, user.id, "tutor", "autonomous")
    grant_hash = await get_active_autonomy_grant(session, household.id, "tutor")
    assert grant_hash is not None
    kept = "Pausing to ask this learner what they expect before they start sharpens their estimates over time."
    to_revoke = "Letting this learner teach the step back to you confirms they have really understood it."
    kept_entry = await route_proposal(
        session, household.id, child.id, {"category": "explanation_style", "content": kept}
    )
    revoke_target = await route_proposal(
        session, household.id, child.id, {"category": "motivation", "content": to_revoke}
    )
    assert kept_entry is not None and kept_entry.status == "active" and kept_entry.grant_event_hash == grant_hash
    assert revoke_target is not None and revoke_target.status == "active"

    # Revoke the standing grant by returning to standard.
    await set_ai_role_policy(session, household.id, user.id, "tutor", "standard")
    assert await get_active_autonomy_grant(session, household.id, "tutor") is None

    # A parent removes one of the formerly autonomous entries, and a fresh
    # proposal now waits in the queue under standard.
    revoked = await revoke_entry(session, household.id, child.id, revoke_target.id, user.id)
    assert revoked.status == "revoked"
    pending = "Short timed drills with an immediate check keep this learner engaged on routine fluency work."
    await _proposed(session, household, child, pending, "pacing")

    return Scenario(
        name="revoked_grant",
        story="Autonomy was granted, used, then revoked; one entry removed, one proposal pending.",
        household_id=household.id,
        child_id=child.id,
        user_id=user.id,
        node_id=node.id,
        policy="standard",
        role_off=False,
        expected_tier="advanced",
        expected_register_source="derived",
        expected_signal=None,
        expect_milestones=False,
        active_contents=[kept],
        forbidden_contents=[to_revoke, pending],
        secret_strings=[grant_hash],
    )


BUILDERS = (
    build_fresh_start,
    build_struggling_reader,
    build_cruising_mathematician,
    build_teenager,
    build_locked_down,
    build_revoked_grant,
)

SCENARIO_NAMES = [
    "fresh_start",
    "struggling_reader",
    "cruising_mathematician",
    "teenager",
    "locked_down",
    "revoked_grant",
]


# ────────────────────────────────────────────────────────────────────────
# Module scoped seeded world
# ────────────────────────────────────────────────────────────────────────


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def seeded_world():
    """Seed all six households once per test module and yield them read only.

    Creates the schema and the row level security policies the same way the
    suite's db_session fixture does, installs an in process Redis so the
    signal and cache layers are live, seeds every scenario through real
    services, and tears the schema down at the end. The Redis stand in is
    restored to its prior value (None in the test process) on teardown so no
    other module inherits it.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await _apply_rls_policies(conn)

    prior_redis = cache_module._redis
    cache_module.init_cache(InMemoryRedis())

    try:
        async with test_session_factory() as session:
            scenarios: dict[str, Scenario] = {}
            for builder in BUILDERS:
                scenario = await builder(session)
                scenarios[scenario.name] = scenario
            await session.flush()
            yield SeededWorld(session=session, scenarios=scenarios)
    finally:
        cache_module._redis = prior_redis
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
