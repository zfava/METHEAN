"""The context matrix: for every golden scenario, assemble the tutor context
through the real learning_context path and assert structural truth.

Each scenario is run through context_assembly.assemble_context with role
"tutor" (the exact text the model would receive), and the matrix asserts,
per block:

  * Register: present with the correct tier's guidance (override respected
    for the teenager, protective foundational fallback when no tier
    resolves).
  * Profile: contains exactly the ACTIVE entries, and never a proposed,
    rejected, retired, or revoked one (the teenager and the revoked grant
    are the sharp tests).
  * Signal: present iff a live signal exists (the struggling reader and the
    cruising mathematician), absent otherwise.
  * Milestones: present iff relationship memory is on (the cruising
    mathematician and the teenager), absent otherwise, capped at three and
    preceded by the use naturally preface.
  * Locked down: the off policy is detected and every layer is suppressed
    before assembly produces a block.
  * Ordering: the assembled block order is stable and matches the
    implementation's documented order (see DOCUMENTED_BLOCK_ORDER below).

Zero AI calls: the assertions are on the assembled context, the contract
METHEAN controls.
"""

import pytest

from app.core.database import set_tenant
from app.core.learning_levels import LEARNING_LEVELS
from app.services.context_assembly import assemble_context
from app.services.governance import AI_AUTONOMY_OFF, get_ai_role_policy
from app.services.learning_context import (
    build_milestone_block,
    build_register_block,
    build_session_signal_block,
)
from app.services.tutor_milestones import MAX_MILESTONES
from app.services.tutor_profile import get_active_entries_block
from app.services.tutor_register import REGISTER_GUIDANCE
from tests.tutor_harness.scenarios import SCENARIO_NAMES, seeded_world  # noqa: F401

pytestmark = pytest.mark.asyncio(loop_scope="module")

# Block preface fragments, the stable signature of each layer in the text.
REGISTER_HEADER = "TUTOR VOICE REGISTER"
MILESTONE_HEADER = "TUTOR RELATIONSHIP MEMORY"
MILESTONE_PREFACE = "naturally and sparingly"
PROFILE_HEADER = "WHAT WORKS FOR THIS LEARNER"
SIGNAL_HEADER = "LIVE SESSION SIGNAL"

# The documented runtime order of the four governed blocks in the assembled
# tutor context. assemble_context emits required sources first, in the order
# they are declared on TUTOR_PROFILE.sources, then optional sources by
# descending relevance. Register, relationship milestones, and session
# signal are required (declared in that relative order); the tutor profile is
# optional, so it lands AFTER the required signal block. The order is
# therefore register, milestones, signal, profile, NOT the intuitive
# register/milestones/profile/signal. See docs/architecture/tutor-system.md.
DOCUMENTED_BLOCK_ORDER = [REGISTER_HEADER, MILESTONE_HEADER, SIGNAL_HEADER, PROFILE_HEADER]


async def _assemble(world, scenario):
    await set_tenant(world.session, scenario.household_id)
    result = await assemble_context(
        world.session,
        "tutor",
        scenario.child_id,
        scenario.household_id,
        node_id=scenario.node_id,
    )
    return result["context_text"]


# ── Register ─────────────────────────────────────────────────────────────


@pytest.mark.parametrize("name", SCENARIO_NAMES)
async def test_register_block(name, seeded_world):  # noqa: F811
    scenario = seeded_world.scenarios[name]
    context = await _assemble(seeded_world, scenario)

    if scenario.role_off:
        # Off suppresses the register: it is presentation, but the role is off.
        assert REGISTER_HEADER not in context
        return

    assert REGISTER_HEADER in context, "the register frames every live tutor context"
    label = LEARNING_LEVELS[scenario.expected_tier]["label"]
    assert f"Stage: {label}" in context
    assert REGISTER_GUIDANCE[scenario.expected_tier] in context

    # The override scenario must read the parent's voice provenance; derived
    # scenarios must read the curriculum provenance.
    if scenario.expected_register_source == "override":
        assert "you set this voice" in context
    else:
        assert "from this learner's curriculum stage" in context


async def test_register_override_respected_for_teenager(seeded_world):  # noqa: F811
    scenario = seeded_world.scenarios["teenager"]
    context = await _assemble(seeded_world, scenario)
    # Mastery child, override one tier down: the register speaks advanced,
    # never mastery, and never the protective foundational fallback.
    assert "Stage: Advanced" in context
    assert REGISTER_GUIDANCE["advanced"] in context
    assert "Stage: Mastery" not in context


async def test_register_fallback_is_protective_for_fresh_start(seeded_world):  # noqa: F811
    scenario = seeded_world.scenarios["fresh_start"]
    context = await _assemble(seeded_world, scenario)
    # No tier data anywhere: the register fails closed to the youngest voice.
    assert "Stage: Foundational" in context
    assert REGISTER_GUIDANCE["foundational"] in context


# ── Profile (active only) ────────────────────────────────────────────────


@pytest.mark.parametrize("name", SCENARIO_NAMES)
async def test_profile_block_active_only(name, seeded_world):  # noqa: F811
    scenario = seeded_world.scenarios[name]
    context = await _assemble(seeded_world, scenario)

    if scenario.active_contents:
        assert PROFILE_HEADER in context
        for content in scenario.active_contents:
            assert content in context, f"active entry missing from {name} context"
    else:
        assert PROFILE_HEADER not in context, f"{name} has no active entries; the profile block must be absent"

    # Never a non active entry, whatever its status.
    for content in scenario.forbidden_contents:
        assert content not in context, f"a non active entry leaked into {name} context"


async def test_teenager_profile_excludes_retired_and_rejected(seeded_world):  # noqa: F811
    scenario = seeded_world.scenarios["teenager"]
    context = await _assemble(seeded_world, scenario)
    assert PROFILE_HEADER in context
    assert scenario.active_contents[0] in context
    # The outgrown (retired) and the declined (rejected) strategies are gone.
    for forbidden in scenario.forbidden_contents:
        assert forbidden not in context


async def test_revoked_grant_profile_keeps_active_drops_revoked_and_pending(seeded_world):  # noqa: F811
    scenario = seeded_world.scenarios["revoked_grant"]
    context = await _assemble(seeded_world, scenario)
    assert PROFILE_HEADER in context
    # The entry applied under the (now revoked) grant is still active and
    # still injects; the revoked entry and the pending proposal do not.
    assert scenario.active_contents[0] in context
    for forbidden in scenario.forbidden_contents:
        assert forbidden not in context


# ── Signal (present iff live) ────────────────────────────────────────────


@pytest.mark.parametrize("name", SCENARIO_NAMES)
async def test_signal_block_presence(name, seeded_world):  # noqa: F811
    scenario = seeded_world.scenarios[name]
    context = await _assemble(seeded_world, scenario)

    if scenario.expected_signal is not None:
        assert SIGNAL_HEADER in context
        assert f"State: {scenario.expected_signal}" in context
    else:
        assert SIGNAL_HEADER not in context, f"{name} has no live signal; the signal block must be absent"


# ── Milestones (present iff relationship on, capped, prefaced) ────────────


@pytest.mark.parametrize("name", SCENARIO_NAMES)
async def test_milestone_block_presence_and_cap(name, seeded_world):  # noqa: F811
    scenario = seeded_world.scenarios[name]
    context = await _assemble(seeded_world, scenario)

    if scenario.expect_milestones:
        assert MILESTONE_HEADER in context
        assert MILESTONE_PREFACE in context
        # The block runs from its header to the next blank line separator.
        block = context.split(MILESTONE_HEADER, 1)[1].split("\n\n", 1)[0]
        milestone_lines = [ln for ln in block.splitlines() if ln.startswith("- ")]
        assert 1 <= len(milestone_lines) <= MAX_MILESTONES
    else:
        assert MILESTONE_HEADER not in context, f"{name} has relationship memory off; milestones must be absent"


# ── Locked down: off suppresses every layer before assembly ──────────────


async def test_locked_down_role_off_suppresses_all_blocks(seeded_world):  # noqa: F811
    scenario = seeded_world.scenarios["locked_down"]
    await set_tenant(seeded_world.session, scenario.household_id)

    # The off policy is the single gate, read the same way the gateway reads
    # it before any provider work. It fires before context assembly.
    policy = await get_ai_role_policy(seeded_world.session, scenario.household_id, "tutor")
    assert policy == AI_AUTONOMY_OFF

    # Every individual layer builder short circuits to empty at off, even
    # though the underlying records (active entry, streak, live signal) all
    # exist.
    hh, child = scenario.household_id, scenario.child_id
    assert await build_register_block(seeded_world.session, hh, child, "tutor", node_id=scenario.node_id) == ""
    assert await build_milestone_block(seeded_world.session, hh, child, "tutor") == ""
    assert await build_session_signal_block(seeded_world.session, hh, child, "tutor") == ""
    assert await get_active_entries_block(seeded_world.session, hh, child) == ""

    # And the assembled context carries none of the four governed blocks.
    context = await _assemble(seeded_world, scenario)
    for header in (REGISTER_HEADER, MILESTONE_HEADER, SIGNAL_HEADER, PROFILE_HEADER):
        assert header not in context


# ── Block ordering (stable and documented) ───────────────────────────────


async def test_block_order_is_stable_and_documented(seeded_world):  # noqa: F811
    # The cruising mathematician is the only scenario with all four governed
    # blocks live, so it is the ordering proof.
    scenario = seeded_world.scenarios["cruising_mathematician"]
    context = await _assemble(seeded_world, scenario)

    positions = {header: context.find(header) for header in DOCUMENTED_BLOCK_ORDER}
    assert all(pos >= 0 for pos in positions.values()), f"a governed block is missing: {positions}"

    ordered = sorted(DOCUMENTED_BLOCK_ORDER, key=lambda h: positions[h])
    assert ordered == DOCUMENTED_BLOCK_ORDER, (
        f"assembled block order {ordered} does not match the documented order {DOCUMENTED_BLOCK_ORDER}"
    )


async def test_partial_block_order_respected_for_struggling_reader(seeded_world):  # noqa: F811
    # Register, then profile, then signal are all present here (no milestones).
    # Whatever subset is live must still follow the documented relative order.
    scenario = seeded_world.scenarios["struggling_reader"]
    context = await _assemble(seeded_world, scenario)
    present = [h for h in DOCUMENTED_BLOCK_ORDER if h in context]
    positions = [context.find(h) for h in present]
    assert positions == sorted(positions), f"block order broke for the struggling reader: {present}"
