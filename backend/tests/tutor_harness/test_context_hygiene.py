"""Context hygiene and bounds: cleanliness rules run against every golden
scenario's assembled tutor context.

These are the promises that protect a family's trust regardless of which
policies and states are in play:

  * No quoted child speech and no clinical or diagnostic language. The
    assertion reuses the 2.3b tutor profile validator's own denylist and
    quote pattern as its source, so the harness and the validator can never
    drift apart.
  * No raw failure or attempt counts surfaced by milestone derivation: the
    dignity rule speaks struggle in weeks and in showing up, never in how
    many times something went wrong.
  * No secrets or internal identifiers beyond what the context legitimately
    needs. Node titles are legitimate references; household, child, and user
    UUIDs, grant hashes, and the JWT secret are not, and must never appear.
  * A documented size bound (a character proxy for a token budget), so the
    context handed to the model is always cheap and bounded.
  * Determinism: assembling twice with no intervening events yields an
    identical context (the tutor context carries no timestamps to exclude).

Zero AI calls: every assertion is on the assembled context string.
"""

import pytest

from app.core.config import settings
from app.core.database import set_tenant
from app.services.context_assembly import assemble_context

# Reuse the 2.3b validator's own lists as the single source of truth, so the
# hygiene assertions track the production validator exactly.
from app.services.tutor_profile import (  # noqa: F401  (denylist re-exported for visibility)
    _DENYLIST_PATTERN,
    _QUOTE_PATTERN,
    CLINICAL_DENYLIST,
)
from tests.tutor_harness.scenarios import SCENARIO_NAMES, seeded_world  # noqa: F401

pytestmark = pytest.mark.asyncio(loop_scope="module")

MILESTONE_HEADER = "TUTOR RELATIONSHIP MEMORY"

# Documented size bound: a character proxy for the tutor's roughly 2,000
# token budget (the assembly engine estimates four characters per token, so
# the hard ceiling is about 8,000 characters; 12,000 is a comfortable,
# documented guard that still catches a runaway context). If a real context
# ever exceeds this, the failure reports the actual size rather than the
# bound quietly rising.
SIZE_BUDGET_CHARS = 12_000


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


def _milestone_block(context: str) -> str | None:
    if MILESTONE_HEADER not in context:
        return None
    return context.split(MILESTONE_HEADER, 1)[1].split("\n\n", 1)[0]


# ── 1. No quoted speech, no clinical language ────────────────────────────


@pytest.mark.parametrize("name", SCENARIO_NAMES)
async def test_no_quoted_child_speech(name, seeded_world):  # noqa: F811
    scenario = seeded_world.scenarios[name]
    context = await _assemble(seeded_world, scenario)
    match = _QUOTE_PATTERN.search(context)
    assert match is None, f"{name} context contains a quotation mark ({match.group(0)!r}); speech must never be quoted"


@pytest.mark.parametrize("name", SCENARIO_NAMES)
async def test_no_clinical_denylist_terms(name, seeded_world):  # noqa: F811
    scenario = seeded_world.scenarios[name]
    context = await _assemble(seeded_world, scenario)
    match = _DENYLIST_PATTERN.search(context)
    assert match is None, f"{name} context contains clinical/diagnostic language ({match.group(0)!r})"


# ── 2. No raw failure counts from milestone derivation ───────────────────


@pytest.mark.parametrize("name", SCENARIO_NAMES)
async def test_no_failure_counts_in_milestones(name, seeded_world):  # noqa: F811
    scenario = seeded_world.scenarios[name]
    context = await _assemble(seeded_world, scenario)
    block = _milestone_block(context)
    if block is None:
        return
    lowered = block.lower()
    # The dignity rule: struggle is never spoken as failure or as a count of
    # attempts. Weeks and streak days are allowed; the words below are not.
    assert "fail" not in lowered, f"{name} milestone block surfaced failure language: {block!r}"
    assert "attempt" not in lowered, f"{name} milestone block surfaced an attempt count: {block!r}"
    assert "wrong" not in lowered, f"{name} milestone block surfaced wrongness: {block!r}"


# ── 3. No secrets or internal identifiers ────────────────────────────────


@pytest.mark.parametrize("name", SCENARIO_NAMES)
async def test_no_internal_identifiers_or_secrets(name, seeded_world):  # noqa: F811
    scenario = seeded_world.scenarios[name]
    context = await _assemble(seeded_world, scenario)

    # Internal UUIDs are never part of a legitimate tutor context: the model
    # is taught about the learner, not about METHEAN's row identifiers.
    for forbidden_id in (scenario.household_id, scenario.child_id, scenario.user_id):
        assert str(forbidden_id) not in context, f"{name} context leaked an internal UUID"

    # Grant hashes are audit references, never tutor context.
    for secret in scenario.secret_strings:
        assert secret not in context, f"{name} context leaked a grant hash"

    # And never any key material.
    assert settings.JWT_SECRET not in context


# ── 4. Size bound ────────────────────────────────────────────────────────


@pytest.mark.parametrize("name", SCENARIO_NAMES)
async def test_context_within_size_budget(name, seeded_world):  # noqa: F811
    scenario = seeded_world.scenarios[name]
    context = await _assemble(seeded_world, scenario)
    size = len(context)
    assert size < SIZE_BUDGET_CHARS, (
        f"{name} assembled context is {size} chars, over the {SIZE_BUDGET_CHARS} char budget"
    )


async def test_report_context_sizes(seeded_world):  # noqa: F811
    # Not a guard: a single, readable line per scenario so the actual sizes
    # are visible in the run output for the deliverable report.
    for name in SCENARIO_NAMES:
        scenario = seeded_world.scenarios[name]
        context = await _assemble(seeded_world, scenario)
        print(f"[context-size] {name}: {len(context)} chars")


# ── 5. Determinism ───────────────────────────────────────────────────────


@pytest.mark.parametrize("name", SCENARIO_NAMES)
async def test_assembly_is_deterministic(name, seeded_world):  # noqa: F811
    scenario = seeded_world.scenarios[name]
    first = await _assemble(seeded_world, scenario)
    second = await _assemble(seeded_world, scenario)
    # The tutor context carries no timestamps in its text, so two assemblies
    # with no intervening events must be byte for byte identical.
    assert first == second, f"{name} assembled context is not deterministic"
