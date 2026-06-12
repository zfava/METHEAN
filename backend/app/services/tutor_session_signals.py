"""Ephemeral within-session signal model for the tutor.

This layer reads the live attempt stream during a single sitting and
classifies the learner's right-now state (cruising, stretching,
struggling, frustrated), handing the tutor that state plus concrete
pedagogical directives so the tutor adapts WITHIN a session, not only
between sessions through the durable profile.

EPHEMERAL IS STRUCTURAL. Everything here lives in Redis under a short
TTL and is never persisted. This module imports no ORM models and never
adds rows to a database session; a guard test enforces that. The single
durable artifact this system may ever produce is an ordinary tutor
profile proposal (category session_pattern), and it is produced only by
delegating to services.tutor_profile.route_proposal, which routes it
under the parent's policy exactly like every other proposal.

The classifier is deterministic arithmetic over the recent attempt
stream. There are zero AI calls in this file.
"""

import json
import uuid
from datetime import UTC, datetime, timedelta

import structlog

from app.core.cache import get_redis

logger = structlog.get_logger()


# ── Signal names ──

CRUISING = "cruising"
STRETCHING = "stretching"
STRUGGLING = "struggling"
FRUSTRATED = "frustrated"

# Patterns worth remembering across sessions. Only the harder states
# recur into a durable strategy proposal; cruising/stretching are good
# days and never need a parent decision.
_DURABLE_PATTERNS = (STRUGGLING, FRUSTRATED)


# ── Tunable scope constants ──
#
# A "session" here is not a database row (there is no session table by
# design). It is the span of activity that shares one Redis window: the
# window lives for SIGNAL_TTL_SECONDS and is refreshed on every attempt,
# so a quiet gap longer than SESSION_IDLE_GAP_SECONDS is treated as the
# previous session ending and a new one beginning. Tests may monkeypatch
# these to shorten them.

SIGNAL_TTL_SECONDS = 2 * 60 * 60  # 2 hours, refreshed on activity
SESSION_IDLE_GAP_SECONDS = 30 * 60  # 30 min quiet => prior session ended
WINDOW_SIZE = 10  # rolling window of recent attempts

# Session pattern proposals are rare by design.
PATTERN_COUNTER_TTL_SECONDS = 14 * 24 * 60 * 60  # distinct-session tally window
PROPOSAL_COOLDOWN_SECONDS = 7 * 24 * 60 * 60  # at most one proposal per 7 days
PATTERN_MIN_SESSIONS = 3  # recurred across at least 3 distinct sessions

# Correctness boundary. The attempt-recording path derives a boolean
# `correct` from the FSRS rating (Good or Easy = correct), which is the
# same confidence >= 0.5 boundary state_engine.confidence_to_rating
# already uses. This module just consumes that boolean.


def _now() -> datetime:
    return datetime.now(UTC)


def _window_key(child_id: uuid.UUID | str) -> str:
    return f"tutor_signal:{child_id}:window"


def _pattern_key(child_id: uuid.UUID | str, pattern: str) -> str:
    return f"tutor_signal:{child_id}:pattern:{pattern}"


def _cooldown_key(child_id: uuid.UUID | str) -> str:
    return f"tutor_signal:{child_id}:cooldown"


# ── Classification (deterministic, documented rules) ──


def _tail_consecutive_incorrect_same_node(attempts: list[dict]) -> int:
    """Count incorrect attempts in an unbroken run at the tail of the
    window that share one real node id.

    A run of wrong answers on the SAME node is the clearest signal that
    a learner is stuck on one idea, distinct from a scattering of misses
    across different topics. Attempts with no node id cannot establish
    sameness, so they end the run rather than silently extend it.
    """
    node: str | None = None
    count = 0
    for a in reversed(attempts):
        if a.get("c"):
            break
        an = a.get("n")
        if an is None:
            break
        if node is None:
            node = an
        elif an != node:
            break
        count += 1
    return count


def classify(attempts: list[dict]) -> str | None:
    """Map a rolling attempt window to a right-now signal, or None.

    Each attempt dict carries: c (correct, bool), h (hints used, int),
    d (duration minutes, int or None), n (node id, str or None).

    Rules, evaluated worst-state-first so the most protective directive
    wins, with the rationale for each constant:

    FRUSTRATED: 5 of the last 6 incorrect, OR 3 consecutive incorrect on
        the same node. Either is a sustained failure run, not a single
        bad answer; both are the threshold at which pushing harder stops
        helping and a break belongs on the table.

    STRUGGLING: 3 of the last 5 incorrect, OR heavy hint leaning (4+
        hints across the last 5). A minority-but-real miss rate, or
        leaning on hints to get through, means step down and scaffold.

    CRUISING: the last 4 attempts all correct with at most one hint
        across the last 5. Consistent unaided success is room to stretch
        upward.

    STRETCHING (default): mixed and productively challenged. The healthy
        middle, where the tutor holds difficulty and lets the struggle
        stay the learner's own.

    Hint counts come from the attempt feedback only when the surface
    records them; when it does not they are 0, so the incorrect-count
    rules are the primary driver and hints only ever amplify. A window
    with no attempts yields None (the tutor falls back to its default
    behavior, fail closed).
    """
    if not attempts:
        return None

    last6 = attempts[-6:]
    last5 = attempts[-5:]
    last4 = attempts[-4:]

    inc6 = sum(1 for a in last6 if not a.get("c"))
    inc5 = sum(1 for a in last5 if not a.get("c"))
    cor4 = sum(1 for a in last4 if a.get("c"))
    hints5 = sum(int(a.get("h") or 0) for a in last5)
    consec_same_node = _tail_consecutive_incorrect_same_node(attempts)

    if (len(last6) >= 6 and inc6 >= 5) or consec_same_node >= 3:
        return FRUSTRATED

    if (len(last5) >= 5 and inc5 >= 3) or (len(last5) >= 3 and hints5 >= 4):
        return STRUGGLING

    if len(last4) >= 4 and cor4 >= 4 and hints5 <= 1:
        return CRUISING

    return STRETCHING


# ── Directives (pedagogy, written with care) ──

_DIRECTIVES: dict[str, list[str]] = {
    CRUISING: [
        "Raise the challenge a notch: offer a harder variation or a why question that extends the idea.",
        "Skip empty praise; name the specific thing they did well, then point at the next stretch.",
    ],
    STRETCHING: [
        "Hold the current difficulty; they are productively challenged right where they are.",
        "Offer a hint only after they have genuinely tried, so the thinking stays theirs.",
    ],
    STRUGGLING: [
        "Step down one level of difficulty and rebuild from the last idea they had solid.",
        "Offer a worked example, then ask them to try a near-identical problem alongside it.",
        "Slow the pace and check one small step at a time rather than the whole problem.",
    ],
    FRUSTRATED: [
        "Step the difficulty down clearly and take the pressure to perform right now off the table.",
        "Name the struggle kindly: this is genuinely tricky right now, and finding it hard is normal.",
        "Suggest a short break before trying again; a reset helps more than one more attempt.",
        "Celebrate any partial progress to rebuild momentum before adding any challenge back.",
    ],
}


def directives(signal: str | None) -> list[str]:
    """Short imperative guidance for the tutor for one signal.

    The frustrated list always includes a break suggestion: a tutor that
    only ever pushes harder is a bad tutor.
    """
    if signal is None:
        return []
    return list(_DIRECTIVES.get(signal, []))


# ── Window plumbing (Redis only, cheap) ──


async def update_on_attempt(child_id: uuid.UUID | str, attempt_outcome_summary: dict) -> dict:
    """Fold one attempt outcome into the rolling Redis window.

    `attempt_outcome_summary` carries the fields the attempt path
    actually has: correct (bool), hints_used (int), duration_minutes
    (int or None), node_id (str or None). Pure data plumbing: read the
    window, append, trim to WINDOW_SIZE, reclassify, write back with a
    refreshed TTL. No database, no AI.

    Returns a small dict: {"signal", "session_ended", "ended_patterns",
    "stored"}. When a quiet gap longer than SESSION_IDLE_GAP_SECONDS is
    detected, the prior session is treated as ended: any durable pattern
    it exhibited is tallied (one distinct session) and session_ended is
    True so the caller can run the post-session proposal check lazily.

    Fail open: a missing or erroring Redis client returns a neutral
    result and never raises.
    """
    redis = get_redis()
    if redis is None:
        return {"signal": None, "session_ended": False, "ended_patterns": [], "stored": False}

    now = _now()
    attempt = {
        "c": bool(attempt_outcome_summary.get("correct")),
        "h": int(attempt_outcome_summary.get("hints_used") or 0),
        "d": attempt_outcome_summary.get("duration_minutes"),
        "n": attempt_outcome_summary.get("node_id"),
        "t": now.isoformat(),
    }

    key = _window_key(child_id)
    raw = await redis.get(key)
    blob = json.loads(raw) if raw else None

    session_ended = False
    ended_patterns: list[str] = []

    if blob is None:
        blob = {
            "session_id": str(uuid.uuid4()),
            "started_at": now.isoformat(),
            "attempts": [],
            "patterns_seen": [],
        }
    else:
        last_seen = _parse_iso(blob.get("last_seen"))
        if last_seen is not None and (now - last_seen).total_seconds() > SESSION_IDLE_GAP_SECONDS:
            # Lazy session-end detection: the previous window went quiet
            # past the idle gap. Tally each durable pattern it showed as
            # one distinct session, then start a fresh session.
            session_ended = True
            ended_patterns = [p for p in blob.get("patterns_seen", []) if p in _DURABLE_PATTERNS]
            for pattern in ended_patterns:
                await _increment_pattern(redis, child_id, pattern)
            blob = {
                "session_id": str(uuid.uuid4()),
                "started_at": now.isoformat(),
                "attempts": [],
                "patterns_seen": [],
            }

    attempts = blob.get("attempts", [])
    attempts.append(attempt)
    attempts = attempts[-WINDOW_SIZE:]
    blob["attempts"] = attempts
    blob["last_seen"] = now.isoformat()

    signal = classify(attempts)
    if signal in _DURABLE_PATTERNS and signal not in blob["patterns_seen"]:
        blob["patterns_seen"].append(signal)

    await redis.set(key, json.dumps(blob, default=str), ex=SIGNAL_TTL_SECONDS)

    return {
        "signal": signal,
        "session_ended": session_ended,
        "ended_patterns": ended_patterns,
        "stored": True,
    }


async def _increment_pattern(redis, child_id: uuid.UUID | str, pattern: str) -> None:
    key = _pattern_key(child_id, pattern)
    await redis.incr(key)
    await redis.expire(key, PATTERN_COUNTER_TTL_SECONDS)


def _parse_iso(value) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt


# ── Reads (signal + directives for the tutor; live view for the parent) ──


async def read_signal(child_id: uuid.UUID | str) -> str | None:
    """The current signal for a child, or None when nothing is live.

    Fail open: any Redis problem reads as no signal so the tutor keeps
    its default behavior.
    """
    redis = get_redis()
    if redis is None:
        return None
    try:
        raw = await redis.get(_window_key(child_id))
        if not raw:
            return None
        blob = json.loads(raw)
        return classify(blob.get("attempts", []))
    except Exception as exc:
        logger.warning("session_signal_read_failed", child_id=str(child_id), error=str(exc))
        return None


async def get_live_signal(child_id: uuid.UUID | str) -> dict | None:
    """The parent live view payload: {signal, as_of, expires_at} or None.

    Read only. The signal is framed for the parent as right-now
    information that disappears; expires_at comes straight from the Redis
    TTL so the chip can clear itself when the window lapses.
    """
    redis = get_redis()
    if redis is None:
        return None
    try:
        key = _window_key(child_id)
        raw = await redis.get(key)
        if not raw:
            return None
        blob = json.loads(raw)
        signal = classify(blob.get("attempts", []))
        if signal is None:
            return None
        ttl = await redis.ttl(key)
        expires_at = None
        if isinstance(ttl, int) and ttl > 0:
            expires_at = (_now() + timedelta(seconds=ttl)).isoformat()
        return {
            "signal": signal,
            "as_of": blob.get("last_seen"),
            "expires_at": expires_at,
        }
    except Exception as exc:
        logger.warning("session_signal_live_view_failed", child_id=str(child_id), error=str(exc))
        return None


# ── Session pattern proposals (the one durable artifact, routed normally) ──

# Strategy phrasing per durable pattern. Abstracted strategy, never a
# fact about the child and never clinical language, so it passes the
# tutor_profile validator unchanged. No quotation marks, no em dashes.
_PATTERN_PROPOSAL_CONTENT: dict[str, str] = {
    FRUSTRATED: (
        "Short sessions with an early easy win, plus a brief break when a topic gets hard, "
        "help this learner stay engaged through the tricky parts."
    ),
    STRUGGLING: (
        "Stepping back to an easier related skill and rebuilding before retrying "
        "helps this learner when a new topic is not landing yet."
    ),
}


async def maybe_propose_session_pattern(db, household_id: uuid.UUID, child_id: uuid.UUID):
    """Post-session check: emit at most one durable strategy proposal.

    Run lazily by the attempt hook whenever update_on_attempt reports a
    session just ended (there is no clean session-end seam in the schema,
    so the 30-minute idle gap stands in for one). When the same durable
    pattern recurred across at least PATTERN_MIN_SESSIONS distinct
    sessions inside the 14-day counter window and no proposal is on
    cooldown, route one proposal (category session_pattern) through the
    ordinary tutor_profile.route_proposal gate, then reset the counter
    and stamp the 7-day cooldown.

    Fail open and side-effect minimal: a Redis problem yields no proposal
    and never raises. The only durable write is route_proposal's, under
    the parent's policy.
    """
    redis = get_redis()
    if redis is None:
        return None
    try:
        if await redis.get(_cooldown_key(child_id)):
            return None

        # Frustrated outranks struggling when both qualify: it is the
        # state whose strategy most needs remembering.
        for pattern in (FRUSTRATED, STRUGGLING):
            raw = await redis.get(_pattern_key(child_id, pattern))
            count = int(raw) if raw else 0
            if count >= PATTERN_MIN_SESSIONS:
                from app.services.tutor_profile import route_proposal

                entry = await route_proposal(
                    db,
                    household_id,
                    child_id,
                    {"category": "session_pattern", "content": _PATTERN_PROPOSAL_CONTENT[pattern]},
                )
                # Reset both tallies and start the cooldown regardless of
                # how route_proposal chose to route (queue, auto-apply, or
                # drop): the recurrence has been acted on.
                await redis.delete(_pattern_key(child_id, FRUSTRATED))
                await redis.delete(_pattern_key(child_id, STRUGGLING))
                await redis.set(_cooldown_key(child_id), "1", ex=PROPOSAL_COOLDOWN_SECONDS)
                logger.info(
                    "session_pattern_proposed",
                    household_id=str(household_id),
                    child_id=str(child_id),
                    pattern=pattern,
                    routed=entry is not None,
                )
                return entry
        return None
    except Exception as exc:
        logger.warning(
            "session_pattern_proposal_failed",
            household_id=str(household_id),
            child_id=str(child_id),
            error=str(exc),
        )
        return None
