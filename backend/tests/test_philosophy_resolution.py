"""Philosophy resolution invariant tests.

Locks in the property proven by docs/philosophy_resolution_audit.md: the
educational philosophy is a presentation layer, never a node-selection filter.
For a given subject and tier, the set of authored nodes a plan materializes is
identical across every philosophy the UI offers, and any unmapped philosophy
value (eclectic, custom, or a nonsense string) resolves to the same full
traditional node set rather than to an empty plan.

These tests drive the real generation path (generate_annual_curriculum ->
call_ai -> native provider) with the AI providers disabled, so only the
deterministic native generator answers. They assert PER-SUBJECT parity (each
philosophy matches that subject's own traditional baseline), not a pooled
count, so a divergence in any single subject fails loudly.

No production code is exercised here beyond what the UI's
"Build from Philosophy" generation already runs; the suite is a regression
guard, not a fix.
"""

import pytest
from sqlalchemy import select

from app.core.config import settings
from app.models.identity import Household
from app.services.annual_curriculum import generate_annual_curriculum
from app.services.node_content import validate_philosophy

# The six philosophies the UI offers in the Build-from-Philosophy picker.
UI_PHILOSOPHIES = [
    "traditional",
    "classical",
    "charlotte_mason",
    "montessori",
    "unschooling",
    "eclectic",
]

# Values that are NOT explicit keys in the generator's philosophy table and
# must therefore fall back to the full traditional node set, never to empty.
# "custom" is offered by the UI; the nonsense value stands in for any stale or
# malformed client input.
UNMAPPED_PHILOSOPHIES = ["custom", "totally_made_up_value"]

# Generatable subjects: those whose foundational scope resolves to real
# persisted node UUIDs today (per the Phase 0 audit). The expected count is the
# current authored total for the tier; it is asserted exactly so this test
# documents the known-good baseline and a future content change updates it
# deliberately. Subjects that are needs_content-for-everyone (science, history,
# writing) or have no foundational level (literature) are out of scope: they
# are empty for traditional too, so they are a template-wiring concern, not a
# philosophy concern.
GENERATABLE_SUBJECTS = [
    ("Mathematics", 157),
    ("Phonics & Reading", 155),
]


@pytest.fixture(autouse=True)
def _native_only(monkeypatch):
    """Force the deterministic native provider: no AI keys, no mock."""
    monkeypatch.setattr(settings, "AI_API_KEY", "")
    monkeypatch.setattr(settings, "AI_FALLBACK_API_KEY", "")
    monkeypatch.setattr(settings, "AI_MOCK_ENABLED", False)


async def _set_philosophy(db_session, household_id, philosophy):
    household = (await db_session.execute(select(Household).where(Household.id == household_id))).scalar_one()
    household.philosophical_profile = {"educational_philosophy": philosophy}
    await db_session.flush()


async def _focus_node_set(db_session, household, child, user, subject_name, philosophy):
    """Generate one curriculum and return the set of distinct focus-node UUIDs.

    The resolver is idempotent per household, so the same authored node yields
    the same UUID across repeated calls for one household; that is what lets the
    per-philosophy id sets be compared by equality below.
    """
    await _set_philosophy(db_session, household.id, philosophy)
    curriculum = await generate_annual_curriculum(
        db_session,
        household.id,
        child.id,
        user.id,
        subject_name=subject_name,
        academic_year="2026-2027",
        total_weeks=12,
        content_tier="foundational",
    )
    weeks = (curriculum.scope_sequence or {}).get("weeks", [])
    node_ids: set[str] = set()
    for week in weeks:
        node_ids.update(week.get("focus_nodes", []))
    return node_ids


# ── Core invariant: per-subject node-set parity across UI philosophies ──────


@pytest.mark.parametrize("subject_name,expected_count", GENERATABLE_SUBJECTS)
async def test_node_set_identical_across_ui_philosophies(
    db_session, household, child, user, subject_name, expected_count
):
    """Every UI philosophy yields the IDENTICAL node id set and count as that
    subject's own traditional baseline. Parity is asserted per subject."""
    baseline = await _focus_node_set(db_session, household, child, user, subject_name, "traditional")
    assert len(baseline) == expected_count, (
        f"{subject_name} traditional baseline changed: expected {expected_count}, got {len(baseline)}"
    )

    for philosophy in UI_PHILOSOPHIES:
        node_ids = await _focus_node_set(db_session, household, child, user, subject_name, philosophy)
        assert node_ids == baseline, (
            f"{subject_name}: philosophy {philosophy!r} produced a different node set "
            f"than traditional ({len(node_ids)} vs {len(baseline)} nodes)"
        )
        assert len(node_ids) == expected_count


@pytest.mark.parametrize("subject_name,expected_count", GENERATABLE_SUBJECTS)
async def test_no_philosophy_yields_zero_nodes(db_session, household, child, user, subject_name, expected_count):
    """No (subject, philosophy) pair produces a 0-node plan. This is the direct
    negation of the reported defect."""
    for philosophy in UI_PHILOSOPHIES:
        node_ids = await _focus_node_set(db_session, household, child, user, subject_name, philosophy)
        assert len(node_ids) > 0, f"{subject_name} + {philosophy} materialized 0 nodes"


# ── Total fallback: unmapped / eclectic / custom resolve to traditional ─────


@pytest.mark.parametrize("subject_name,expected_count", GENERATABLE_SUBJECTS)
async def test_unmapped_philosophy_falls_back_to_traditional_node_set(
    db_session, household, child, user, subject_name, expected_count
):
    """eclectic, custom, and a nonsense value all resolve to the full
    traditional node set, never to empty."""
    baseline = await _focus_node_set(db_session, household, child, user, subject_name, "traditional")
    for philosophy in ["eclectic", *UNMAPPED_PHILOSOPHIES]:
        node_ids = await _focus_node_set(db_session, household, child, user, subject_name, philosophy)
        assert node_ids == baseline, (
            f"{subject_name}: unmapped philosophy {philosophy!r} did not fall back to the "
            f"full traditional node set ({len(node_ids)} vs {len(baseline)} nodes)"
        )


# ── Unschooling integrity: full node set, validator never violated ──────────


async def test_unschooling_materializes_full_node_set(db_session, household, child, user):
    """An unschooling plan carries the same full node set as traditional."""
    baseline = await _focus_node_set(db_session, household, child, user, "Mathematics", "traditional")
    unschooling = await _focus_node_set(db_session, household, child, user, "Mathematics", "unschooling")
    assert unschooling == baseline
    assert len(unschooling) > 0


def test_unschooling_variants_pass_validator():
    """The authored unschooling variants must not carry lesson/sequence/
    assessment keys: validate_philosophy hard-fails them if they do. This
    guards the fallback design's premise that surfacing the unschooling variant
    where present is safe, and that materialization never synthesizes a lesson
    into one."""
    from app.content.math_foundational_content import MATH_FOUNDATIONAL_CONTENT

    offenders = []
    for node_id, content in MATH_FOUNDATIONAL_CONTENT.items():
        errors = [i for i in validate_philosophy(content) if i.startswith("error:")]
        if errors:
            offenders.append((node_id, errors))
    assert not offenders, f"unschooling validator violations: {offenders[:5]}"
