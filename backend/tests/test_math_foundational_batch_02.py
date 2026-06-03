"""Gold-standard gate for the math foundational batch mf-46..mf-60.

Asserts the 15 new nodes pass the REAL validator (node_content.py), carry the
exact NATIVE_KEYS from test_node_content.py, never hard-fail the unschooling
rule, satisfy the three-file rule (content + scope + template), have mutually
consistent prerequisites referencing only earlier real nodes, resolve to UUIDs
through node_resolver, and meet the depth floor. The real validator functions
are imported and called, not reimplemented.
"""

from datetime import date

import pytest

from app.content.math_foundational_content import MATH_FOUNDATIONAL_CONTENT
from app.content.scope_sequences import get_scope_sequence
from app.services.native_curriculum_generator import generate_for_subject
from app.services.node_content import validate_content, validate_philosophy
from app.services.node_resolver import resolve_ref_to_uuid
from app.services.templates import MATH_FOUNDATIONAL

# Canonical requirement sets, imported (not copied) from the schema test.
from tests.test_node_content import NATIVE_KEYS, PHILOSOPHIES, UNSCHOOLING_FORBIDDEN

NEW_NUMS = list(range(46, 61))
NEW_IDS = [f"mf-{n}" for n in NEW_NUMS]
NEW_REFS = [f"math_f_{n}" for n in NEW_NUMS]

# Authoritative prerequisite map (docs/math_foundational_gap.md, mf-46..mf-60).
EXPECTED_PREREQS: dict[str, list[str]] = {
    "mf-46": ["mf-11"],
    "mf-47": ["mf-11"],
    "mf-48": ["mf-11"],
    "mf-49": ["mf-42", "mf-11"],
    "mf-50": ["mf-18"],
    "mf-51": ["mf-10"],
    "mf-52": ["mf-34", "mf-09"],
    "mf-53": ["mf-09"],
    "mf-54": ["mf-09"],
    "mf-55": ["mf-54"],
    "mf-56": ["mf-55"],
    "mf-57": ["mf-56"],
    "mf-58": ["mf-56", "mf-46"],
    "mf-59": ["mf-19"],
    "mf-60": ["mf-34", "mf-35"],
}

ACCOMMODATION_KEYS = {"dyslexia", "adhd", "gifted", "visual_learner", "kinesthetic_learner", "auditory_learner"}


def _scope_by_ref() -> dict[str, dict]:
    return {t["ref"]: t for t in get_scope_sequence("mathematics", "foundational")}


def _template_nodes() -> dict[str, object]:
    return {tn.ref: tn for tn in MATH_FOUNDATIONAL.nodes}


# ── Validator gate (real validator) ──────────────────────────────────────


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_validate_content_passes(node_id):
    assert validate_content(MATH_FOUNDATIONAL_CONTENT[node_id]) == []


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_validate_philosophy_no_hard_fail(node_id):
    errors = [i for i in validate_philosophy(MATH_FOUNDATIONAL_CONTENT[node_id]) if i.startswith("error:")]
    assert errors == []


# ── NATIVE_KEYS gate ─────────────────────────────────────────────────────


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_five_native_philosophy_variants(node_id):
    ps = MATH_FOUNDATIONAL_CONTENT[node_id]["philosophy_specific"]
    for philosophy in PHILOSOPHIES:
        assert philosophy in ps, f"{node_id} missing {philosophy}"
        variant = ps[philosophy]
        assert isinstance(variant, dict)
        missing = NATIVE_KEYS[philosophy] - set(variant.keys())
        assert not missing, f"{node_id}/{philosophy} missing native keys: {sorted(missing)}"


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_unschooling_carries_no_forbidden_key(node_id):
    unschooling = MATH_FOUNDATIONAL_CONTENT[node_id]["philosophy_specific"]["unschooling"]
    forbidden = UNSCHOOLING_FORBIDDEN.intersection(unschooling.keys())
    assert not forbidden, f"{node_id} unschooling has forbidden keys: {sorted(forbidden)}"


# ── Depth floor ──────────────────────────────────────────────────────────


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_depth_floor(node_id):
    c = MATH_FOUNDATIONAL_CONTENT[node_id]
    assert len(c["practice_items"]) >= 8, f"{node_id} has < 8 practice_items"
    assert len(c["assessment_items"]) >= 5, f"{node_id} has < 5 assessment_items"
    assert set(c["accommodations"].keys()) == ACCOMMODATION_KEYS
    assert set(c["philosophy_specific"].keys()) >= set(PHILOSOPHIES)
    diffs = [pi["difficulty"] for pi in c["practice_items"]]
    assert min(diffs) == 1 and max(diffs) == 3
    assert any("correct_answer" not in pi for pi in c["practice_items"])
    assert any("correct_answer" in ai for ai in c["assessment_items"])
    assert any("rubric" in ai for ai in c["assessment_items"])
    assert all(ai.get("target_concept") for ai in c["assessment_items"])


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_traditional_spiral_references_a_prior_node(node_id):
    spiral = MATH_FOUNDATIONAL_CONTENT[node_id]["philosophy_specific"]["traditional"]["spiral_review"]
    text = " ".join(spiral)
    num = int(node_id.split("-")[1])
    referenced = [f"mf-{m:02d}" for m in range(1, num) if f"mf-{m:02d}" in text]
    assert referenced, f"{node_id} spiral_review references no prior mf node: {spiral}"


# ── Three-file integrity ─────────────────────────────────────────────────


def test_all_three_files_have_every_new_node():
    scope = _scope_by_ref()
    tnodes = _template_nodes()
    for n in NEW_NUMS:
        assert f"mf-{n}" in MATH_FOUNDATIONAL_CONTENT, f"mf-{n} missing from content"
        assert f"math_f_{n}" in scope, f"math_f_{n} missing from scope_sequences"
        assert f"mf-{n}" in tnodes, f"mf-{n} missing from MATH_FOUNDATIONAL template"


def test_counts_now_sixty():
    assert len(MATH_FOUNDATIONAL_CONTENT) == 60
    assert len(get_scope_sequence("mathematics", "foundational")) == 60
    assert len(MATH_FOUNDATIONAL.nodes) == 60


# ── Prerequisite integrity (three files agree, earlier-only) ─────────────


def test_scope_prereqs_match_expected_and_are_earlier():
    scope = _scope_by_ref()
    for node_id, prereqs in EXPECTED_PREREQS.items():
        ref = f"math_f_{node_id.split('-')[1]}"
        got = scope[ref]["prerequisites"]
        expected_refs = [f"math_f_{p.split('-')[1]}" for p in prereqs]
        assert got == expected_refs, f"{ref} scope prereqs {got} != {expected_refs}"
        num = int(node_id.split("-")[1])
        for p in prereqs:
            assert p in MATH_FOUNDATIONAL_CONTENT, f"{node_id} prereq {p} not a real node"
            assert int(p.split("-")[1]) < num, f"{node_id} prereq {p} is not earlier"


def test_template_edges_match_scope_prereqs():
    incoming: dict[str, set[str]] = {}
    for e in MATH_FOUNDATIONAL.edges:
        incoming.setdefault(e.to_ref, set()).add(e.from_ref)
    for node_id, prereqs in EXPECTED_PREREQS.items():
        edges_in = incoming.get(node_id, set())
        assert edges_in == set(prereqs), f"{node_id} template edges {edges_in} != prereqs {set(prereqs)}"


# ── Resolver + generator gates (DB) ──────────────────────────────────────


@pytest.mark.parametrize("ref", NEW_REFS)
async def test_resolver_resolves_each_new_ref(db_session, household, ref):
    res = await resolve_ref_to_uuid(db_session, ref, household.id)
    assert res.node_uuid is not None, f"{ref} did not resolve to a UUID"
    assert res.unresolved is None


async def test_generator_plan_all_sixty_resolve_zero_needs_content(db_session, household):
    """A foundational plan over the full 60-topic scope resolves every topic:
    zero needs_content weeks (60 of 60 resolved, the 15 new nodes no longer
    placeholders), with 60 distinct focus-node UUIDs."""
    out = await generate_for_subject(
        db_session,
        household.id,
        "mathematics",
        "foundational",
        hours_per_week=4.0,
        total_weeks=60,
        start_date=date(2026, 9, 1),
    )
    needs = [w for w in out["weeks"] if w.get("needs_content")]
    assert needs == [], f"unexpected needs_content weeks: {[w['week_number'] for w in needs]}"
    resolved_ids = {fid for w in out["weeks"] for fid in w["focus_nodes"]}
    assert len(resolved_ids) == 60
