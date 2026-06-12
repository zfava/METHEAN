"""Tests for the ephemeral within-session signal model.

Covers the deterministic classifier at its documented boundaries, the
rolling Redis window and its TTL, tutor-only injection gated by policy,
the fail-open attempt hook, the zero-database-writes guard, the parent
live view (parent scope and household isolation), and the rare session
pattern proposal that flows through route_proposal under the parent's
policy.

The signal layer talks to Redis through app.core.cache.get_redis, so
these tests install an in-memory fake with a controllable clock for
deterministic TTL behavior. No real Redis is required.
"""

import json
import uuid
from datetime import UTC, datetime, timedelta
from fnmatch import fnmatch
from pathlib import Path
from unittest.mock import patch

import pytest
import pytest_asyncio
from sqlalchemy import select

from app.core import cache
from app.models.curriculum import LearningMap, LearningNode, Subject
from app.models.enums import ActivityType, NodeType
from app.models.governance import Activity, Plan, PlanWeek
from app.models.intelligence import TutorProfileEntry
from app.services import tutor_session_signals as tss
from app.services.governance import set_ai_role_policy
from app.services.learning_context import build_session_signal_block
from app.services.tutor_session_signals import (
    CRUISING,
    FRUSTRATED,
    SIGNAL_TTL_SECONDS,
    STRETCHING,
    STRUGGLING,
    _pattern_key,
    _window_key,
    classify,
    directives,
    get_live_signal,
    maybe_propose_session_pattern,
    read_signal,
    update_on_attempt,
)

# ── In-memory fake Redis with a controllable clock ──────────────────────


class FakeRedis:
    """Minimal async Redis stand-in honoring TTL via a logical clock.

    Mirrors decode_responses=True: values come back as strings. Only the
    operations the signal layer and the policy cache use are implemented.
    advance() fast-forwards the clock so TTL expiry is deterministic and
    sleep-free.
    """

    def __init__(self) -> None:
        self._data: dict[str, tuple[str, float | None]] = {}
        self._clock = 0.0

    def advance(self, seconds: float) -> None:
        self._clock += seconds

    def _expired(self, key: str) -> bool:
        item = self._data.get(key)
        if item is None:
            return True
        _, exp = item
        if exp is not None and exp <= self._clock:
            del self._data[key]
            return True
        return False

    async def get(self, key):
        if self._expired(key):
            return None
        return self._data[key][0]

    async def set(self, key, value, ex=None):
        exp = self._clock + ex if ex is not None else None
        self._data[key] = (str(value), exp)
        return True

    async def delete(self, *keys):
        removed = 0
        for k in keys:
            if k in self._data:
                del self._data[k]
                removed += 1
        return removed

    async def incr(self, key):
        if self._expired(key):
            current, exp = 0, None
        else:
            current, exp = int(self._data[key][0]), self._data[key][1]
        current += 1
        self._data[key] = (str(current), exp)
        return current

    async def expire(self, key, seconds):
        if self._expired(key):
            return False
        value, _ = self._data[key]
        self._data[key] = (value, self._clock + seconds)
        return True

    async def ttl(self, key):
        if self._expired(key):
            return -2
        _, exp = self._data[key]
        if exp is None:
            return -1
        return int(exp - self._clock)

    async def scan_iter(self, match="*"):
        for key in list(self._data.keys()):
            if not self._expired(key) and fnmatch(key, match):
                yield key


class RaisingRedis:
    """A Redis client whose data ops raise, to simulate Redis down."""

    async def get(self, *_a, **_k):
        raise RuntimeError("redis down")

    async def set(self, *_a, **_k):
        raise RuntimeError("redis down")

    async def delete(self, *_a, **_k):
        raise RuntimeError("redis down")

    async def incr(self, *_a, **_k):
        raise RuntimeError("redis down")

    async def expire(self, *_a, **_k):
        raise RuntimeError("redis down")

    async def ttl(self, *_a, **_k):
        raise RuntimeError("redis down")

    async def scan_iter(self, *_a, **_k):
        raise RuntimeError("redis down")
        yield  # pragma: no cover


@pytest.fixture
def signal_redis():
    """Install an in-memory fake Redis for the duration of one test."""
    fake = FakeRedis()
    prev = cache.get_redis()
    cache.init_cache(fake)
    yield fake
    cache.init_cache(prev)


# ── Window construction helpers ─────────────────────────────────────────


def _att(correct: bool, node_id="n", hints=0):
    return {"c": correct, "h": hints, "d": None, "n": node_id}


# A struggling window: 3 of last 5 incorrect, spread across nodes so the
# same-node consecutive rule (frustrated) does not fire.
STRUGGLING_WINDOW = [
    _att(True, "a"),
    _att(False, "b"),
    _att(True, "c"),
    _att(False, "d"),
    _att(False, "e"),
]


async def _feed(child_id, summaries):
    for s in summaries:
        await update_on_attempt(child_id, s)


async def _age_window_stale(redis, child_id, minutes=31):
    raw = await redis.get(_window_key(child_id))
    blob = json.loads(raw)
    blob["last_seen"] = (datetime.now(UTC) - timedelta(minutes=minutes)).isoformat()
    await redis.set(_window_key(child_id), json.dumps(blob), ex=SIGNAL_TTL_SECONDS)


# ── 1. Classification table (deterministic, at documented boundaries) ───


def test_classify_cruising():
    window = [_att(True, "a"), _att(True, "b"), _att(True, "c"), _att(True, "d")]
    assert classify(window) == CRUISING


def test_classify_cruising_breaks_on_hints():
    window = [_att(True, "a"), _att(True, "b"), _att(True, "c"), _att(True, "d", hints=2)]
    # Four correct but heavy hints on the last: not effortless, so the
    # default productive-challenge state, not cruising.
    assert classify(window) == STRETCHING


def test_classify_stretching_default_mixed():
    window = [_att(True, "a"), _att(False, "b"), _att(True, "c")]
    assert classify(window) == STRETCHING


def test_classify_struggling_by_incorrect():
    assert classify(STRUGGLING_WINDOW) == STRUGGLING


def test_classify_struggling_by_hints():
    # Mostly correct but leaning hard on hints across the last five.
    window = [
        _att(True, "a", hints=1),
        _att(True, "b", hints=1),
        _att(True, "c", hints=1),
        _att(True, "d", hints=1),
        _att(True, "e", hints=1),
    ]
    assert classify(window) == STRUGGLING


def test_classify_frustrated_five_of_six():
    window = [
        _att(False, "a"),
        _att(True, "b"),
        _att(False, "c"),
        _att(False, "d"),
        _att(False, "e"),
        _att(False, "f"),
    ]
    assert classify(window) == FRUSTRATED


def test_classify_frustrated_three_consecutive_same_node():
    window = [_att(True, "a"), _att(False, "x"), _att(False, "x"), _att(False, "x")]
    assert classify(window) == FRUSTRATED


def test_classify_three_consecutive_different_nodes_not_frustrated():
    # Three misses in a row but on different nodes is not the same-node
    # stuck signal; with a full window it lands on struggling (3 of last
    # 5 incorrect), never frustrated.
    window = [_att(True, "a"), _att(True, "b"), _att(False, "x"), _att(False, "y"), _att(False, "z")]
    assert classify(window) == STRUGGLING


def test_classify_empty_returns_none():
    assert classify([]) is None


# ── 2. Directives are pedagogy ──────────────────────────────────────────


def test_frustrated_directives_include_a_break():
    texts = " ".join(directives(FRUSTRATED)).lower()
    assert "break" in texts, "a tutor that only pushes harder is a bad tutor"


def test_cruising_directives_stretch_and_avoid_empty_praise():
    texts = " ".join(directives(CRUISING)).lower()
    assert "empty praise" in texts
    assert "challenge" in texts or "stretch" in texts


def test_directives_none_is_empty():
    assert directives(None) == []


# ── 3. Window plumbing and TTL ──────────────────────────────────────────


@pytest.mark.asyncio
async def test_window_rolls_to_last_ten(signal_redis):
    child = uuid.uuid4()
    for i in range(12):
        await update_on_attempt(child, {"correct": True, "node_id": f"n{i}"})
    blob = json.loads(await signal_redis.get(_window_key(child)))
    assert len(blob["attempts"]) == 10
    assert blob["attempts"][0]["n"] == "n2", "oldest two attempts rolled off"
    assert blob["attempts"][-1]["n"] == "n11"


@pytest.mark.asyncio
async def test_no_redis_degrades_silently():
    # No client installed at all.
    prev = cache.get_redis()
    cache.init_cache(None)
    try:
        result = await update_on_attempt(uuid.uuid4(), {"correct": False, "node_id": "n"})
        assert result == {"signal": None, "session_ended": False, "ended_patterns": [], "stored": False}
        assert await read_signal(uuid.uuid4()) is None
    finally:
        cache.init_cache(prev)


@pytest.mark.asyncio
async def test_ttl_expiry_empties_signal(signal_redis):
    child = uuid.uuid4()
    await _feed(child, STRUGGLING_WINDOW)
    assert await read_signal(child) == STRUGGLING
    # Fast-forward past the window TTL: Redis drops the key.
    signal_redis.advance(SIGNAL_TTL_SECONDS + 1)
    assert await read_signal(child) is None
    assert await get_live_signal(child) is None


# ── 4. Injection (tutor only, policy gated, fail closed) ────────────────


@pytest.mark.asyncio
async def test_injection_present_when_signal_and_policy_standard(signal_redis, db_session, household, child):
    await _feed(child.id, STRUGGLING_WINDOW)
    block = await build_session_signal_block(db_session, household.id, child.id, "tutor")
    assert "LIVE SESSION SIGNAL" in block
    assert f"State: {STRUGGLING}" in block
    # Directives are present so the tutor has something concrete to do.
    assert "Do now:" in block


@pytest.mark.asyncio
async def test_injection_absent_when_no_signal(signal_redis, db_session, household, child):
    block = await build_session_signal_block(db_session, household.id, child.id, "tutor")
    assert block == ""


@pytest.mark.asyncio
async def test_injection_absent_when_policy_off(signal_redis, db_session, household, user, child):
    await _feed(child.id, STRUGGLING_WINDOW)
    await set_ai_role_policy(db_session, household.id, user.id, "tutor", "off")
    block = await build_session_signal_block(db_session, household.id, child.id, "tutor")
    assert block == ""


@pytest.mark.asyncio
async def test_injection_absent_for_non_tutor_role(signal_redis, db_session, household, child):
    await _feed(child.id, STRUGGLING_WINDOW)
    block = await build_session_signal_block(db_session, household.id, child.id, "evaluator")
    assert block == ""


@pytest.mark.asyncio
async def test_assembled_tutor_context_contains_block(signal_redis, db_session, household, child):
    from app.services.context_assembly import assemble_context

    await _feed(child.id, STRUGGLING_WINDOW)
    tutor_ctx = await assemble_context(db_session, "tutor", child.id, household.id)
    assert "LIVE SESSION SIGNAL" in tutor_ctx["context_text"]
    # And it never reaches another role's assembled context.
    eval_ctx = await assemble_context(db_session, "evaluator", child.id, household.id)
    assert "LIVE SESSION SIGNAL" not in eval_ctx["context_text"]


# ── 5. Attempt hook is fail-open ────────────────────────────────────────


@pytest_asyncio.fixture
async def practice_activity(db_session, household, child):
    s = Subject(household_id=household.id, name="Math")
    db_session.add(s)
    await db_session.flush()
    m = LearningMap(household_id=household.id, subject_id=s.id, name="Map")
    db_session.add(m)
    await db_session.flush()
    node = LearningNode(learning_map_id=m.id, household_id=household.id, node_type=NodeType.concept, title="Addition")
    db_session.add(node)
    await db_session.flush()
    plan = Plan(household_id=household.id, child_id=child.id, name="Plan", status="active")
    db_session.add(plan)
    await db_session.flush()
    from datetime import date

    week = PlanWeek(
        plan_id=plan.id,
        household_id=household.id,
        week_number=1,
        start_date=date(2026, 1, 5),
        end_date=date(2026, 1, 11),
    )
    db_session.add(week)
    await db_session.flush()
    activity = Activity(
        plan_week_id=week.id,
        household_id=household.id,
        title="Practice",
        activity_type=ActivityType.practice,
        node_id=node.id,
        estimated_minutes=20,
    )
    db_session.add(activity)
    await db_session.flush()
    return activity


@pytest.mark.asyncio
async def test_attempt_hook_failure_does_not_break_submission(db_session, household, child, practice_activity):
    from app.services import attempt_workflow
    from app.services.attempt_workflow import start_attempt, submit_attempt

    att = await start_attempt(db_session, practice_activity.id, child.id, household.id)

    prev = cache.get_redis()
    cache.init_cache(RaisingRedis())
    try:
        with patch.object(attempt_workflow.logger, "warning") as warn:
            result = await submit_attempt(db_session, att.id, household.id, confidence=0.2, duration_minutes=10)
    finally:
        cache.init_cache(prev)

    # The submission still succeeds despite Redis being down.
    from app.models.enums import AttemptStatus

    assert result["attempt"].status == AttemptStatus.completed
    # And the failure is logged at the sanctioned log-and-continue site.
    assert any(c.args and c.args[0] == "session_signal_update_failed" for c in warn.call_args_list)


# ── 6. Zero database writes guard ───────────────────────────────────────


def test_module_performs_no_database_writes():
    source = Path(tss.__file__).read_text()
    assert "from app.models" not in source, "the ephemeral signal layer imports no ORM models"
    assert "import app.models" not in source
    assert "session.add" not in source, "the ephemeral signal layer never adds rows"
    assert ".add(" not in source, "no db.add/session.add of any kind"


# ── 7. Parent live view ─────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_parent_endpoint_returns_live_signal(signal_redis, auth_client, household, child):
    await _feed(child.id, STRUGGLING_WINDOW)
    resp = await auth_client.get(f"/api/v1/children/{child.id}/session-signal")
    assert resp.status_code == 200
    body = resp.json()
    assert body["signal"] == STRUGGLING
    assert body["as_of"]
    assert body["expires_at"]


@pytest.mark.asyncio
async def test_parent_endpoint_empty_after_ttl(signal_redis, auth_client, household, child):
    await _feed(child.id, STRUGGLING_WINDOW)
    signal_redis.advance(SIGNAL_TTL_SECONDS + 1)
    resp = await auth_client.get(f"/api/v1/children/{child.id}/session-signal")
    assert resp.status_code == 200
    assert resp.json() == {}


@pytest.mark.asyncio
async def test_parent_endpoint_denies_child_scope(signal_redis, client, household, user, child):
    from app.core.security import create_access_token

    await _feed(child.id, STRUGGLING_WINDOW)
    token = create_access_token(user.id, household.id, "owner", scope="child", child_id=child.id)
    client.cookies.set("access_token", token)
    resp = await client.get(f"/api/v1/children/{child.id}/session-signal")
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_parent_endpoint_household_isolation(signal_redis, client, db_session, household, child):
    from app.core.database import set_tenant
    from app.core.security import create_access_token, hash_password
    from app.models.identity import Household, User

    await _feed(child.id, STRUGGLING_WINDOW)

    # A second household with its own verified parent.
    other = Household(name="Other Family", subscription_status="trialing")
    db_session.add(other)
    await db_session.flush()
    await set_tenant(db_session, other.id)
    other_user = User(
        household_id=other.id,
        email="other@test.com",
        password_hash=hash_password("testpass123"),
        display_name="Other Parent",
        role="owner",
        email_verified=True,
    )
    db_session.add(other_user)
    await db_session.flush()

    token = create_access_token(other_user.id, other.id, "owner")
    client.cookies.set("access_token", token)
    resp = await client.get(f"/api/v1/children/{child.id}/session-signal")
    # The child is invisible across the household boundary: 404, no leak.
    assert resp.status_code == 404


# ── 8. Session pattern proposals (the one durable artifact) ─────────────


@pytest.mark.asyncio
async def test_distinct_session_counter_increments_on_session_end(signal_redis):
    child = uuid.uuid4()
    await _feed(child, STRUGGLING_WINDOW)
    blob = json.loads(await signal_redis.get(_window_key(child)))
    assert STRUGGLING in blob["patterns_seen"]

    await _age_window_stale(signal_redis, child)
    result = await update_on_attempt(child, {"correct": False, "node_id": "detect"})
    assert result["session_ended"] is True
    assert STRUGGLING in result["ended_patterns"]
    assert int(await signal_redis.get(_pattern_key(child, STRUGGLING))) == 1


@pytest.mark.asyncio
async def test_three_sessions_emit_one_proposal_standard(signal_redis, db_session, household, child):
    # Drive three distinct struggling sessions, each ended by a 30-minute
    # idle gap detected on the next attempt.
    for i in range(3):
        await _feed(child.id, STRUGGLING_WINDOW)
        await _age_window_stale(signal_redis, child.id)
        res = await update_on_attempt(child.id, {"correct": False, "node_id": f"detect{i}"})
        assert res["session_ended"] is True

    assert int(await signal_redis.get(_pattern_key(child.id, STRUGGLING))) == 3

    entry = await maybe_propose_session_pattern(db_session, household.id, child.id)
    assert entry is not None
    assert entry.category == "session_pattern"
    assert entry.status == "proposed", "standard policy queues for parent review"

    # Exactly one: a second check is on cooldown.
    second = await maybe_propose_session_pattern(db_session, household.id, child.id)
    assert second is None


@pytest.mark.asyncio
async def test_counters_reset_after_proposal(signal_redis, db_session, household, child):
    await signal_redis.set(_pattern_key(child.id, STRUGGLING), "3")
    entry = await maybe_propose_session_pattern(db_session, household.id, child.id)
    assert entry is not None
    assert await signal_redis.get(_pattern_key(child.id, STRUGGLING)) is None
    assert await signal_redis.get(_pattern_key(child.id, FRUSTRATED)) is None


@pytest.mark.asyncio
async def test_cooldown_blocks_proposal(signal_redis, db_session, household, child):
    await signal_redis.set(_pattern_key(child.id, FRUSTRATED), "5")
    await signal_redis.set(tss._cooldown_key(child.id), "1", ex=tss.PROPOSAL_COOLDOWN_SECONDS)
    entry = await maybe_propose_session_pattern(db_session, household.id, child.id)
    assert entry is None


@pytest.mark.asyncio
async def test_below_threshold_no_proposal(signal_redis, db_session, household, child):
    await signal_redis.set(_pattern_key(child.id, STRUGGLING), "2")
    entry = await maybe_propose_session_pattern(db_session, household.id, child.id)
    assert entry is None


@pytest.mark.asyncio
async def test_autonomous_proposal_applies_with_grant_hash(signal_redis, db_session, household, user, child):
    await set_ai_role_policy(db_session, household.id, user.id, "tutor", "autonomous")
    await signal_redis.set(_pattern_key(child.id, FRUSTRATED), "3")

    entry = await maybe_propose_session_pattern(db_session, household.id, child.id)
    assert entry is not None
    assert entry.category == "session_pattern"
    assert entry.status == "active", "autonomous applies under the standing grant"
    assert entry.grant_event_hash

    rows = (
        (await db_session.execute(select(TutorProfileEntry).where(TutorProfileEntry.child_id == child.id)))
        .scalars()
        .all()
    )
    assert len(rows) == 1
