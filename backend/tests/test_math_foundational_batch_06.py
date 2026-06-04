"""Gold-standard gate for the math foundational batch mf-106..mf-120, plus the
whole-library graph-integrity gate that scans every mf node (mf-01..mf-120).

The per-batch gates assert the 15 new nodes pass the REAL validator
(node_content.py), carry the exact NATIVE_KEYS from test_node_content.py, never
hard-fail the unschooling rule, satisfy the three-file rule, have backward-only
prerequisites, resolve to UUIDs, and meet the depth floor.

The graph-integrity gate scans the entire authored library: contiguous ids with
no gaps or duplicates, cross-file count parity, an acyclic prerequisite DAG with
no dangling references, backward-only (topologically sound) prerequisites (save
the one documented legacy exception), and reachable spiral-review references.
These assertions keep holding as later batches land.
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

NEW_NUMS = list(range(106, 121))
NEW_IDS = [f"mf-{n}" for n in NEW_NUMS]
NEW_REFS = [f"math_f_{n}" for n in NEW_NUMS]

# Authoritative prerequisite map (docs/math_foundational_gap.md, mf-106..mf-120).
EXPECTED_PREREQS: dict[str, list[str]] = {
    "mf-106": ["mf-103", "mf-104", "mf-105"],
    "mf-107": ["mf-103"],
    "mf-108": ["mf-98"],
    "mf-109": ["mf-45"],
    "mf-110": ["mf-13"],
    "mf-111": ["mf-110"],
    "mf-112": ["mf-111", "mf-97"],
    "mf-113": ["mf-45"],
    "mf-114": ["mf-14"],
    "mf-115": ["mf-42"],
    "mf-116": ["mf-111", "mf-90"],
    "mf-117": ["mf-17"],
    "mf-118": ["mf-17"],
    "mf-119": ["mf-118", "mf-117"],
    "mf-120": ["mf-117"],
}

ACCOMMODATION_KEYS = {"dyslexia", "adhd", "gifted", "visual_learner", "kinesthetic_learner", "auditory_learner"}


def _num(node_id: str) -> int:
    """Numeric part of an mf-NN or math_f_NN id."""
    return int(node_id.split("_")[-1] if node_id.startswith("math_f_") else node_id.split("-")[1])


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
    num = _num(node_id)
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


def test_counts_now_one_hundred_twenty():
    assert len(MATH_FOUNDATIONAL_CONTENT) == 120
    assert len(get_scope_sequence("mathematics", "foundational")) == 120
    assert len(MATH_FOUNDATIONAL.nodes) == 120


# ── Prerequisite integrity (three files agree, earlier-only) ─────────────


def test_scope_prereqs_match_expected_and_are_earlier():
    scope = _scope_by_ref()
    for node_id, prereqs in EXPECTED_PREREQS.items():
        ref = f"math_f_{_num(node_id)}"
        got = scope[ref]["prerequisites"]
        expected_refs = [f"math_f_{_num(p)}" for p in prereqs]
        assert got == expected_refs, f"{ref} scope prereqs {got} != {expected_refs}"
        num = _num(node_id)
        for p in prereqs:
            assert p in MATH_FOUNDATIONAL_CONTENT, f"{node_id} prereq {p} not a real node"
            assert _num(p) < num, f"{node_id} prereq {p} is not earlier"


def test_template_edges_match_scope_prereqs():
    incoming: dict[str, set[str]] = {}
    for e in MATH_FOUNDATIONAL.edges:
        incoming.setdefault(e.to_ref, set()).add(e.from_ref)
    for node_id, prereqs in EXPECTED_PREREQS.items():
        edges_in = incoming.get(node_id, set())
        assert edges_in == set(prereqs), f"{node_id} template edges {edges_in} != prereqs {set(prereqs)}"


# ── WHOLE-LIBRARY GRAPH-INTEGRITY GATE (scans mf-01..mf-120) ──────────────
#
# These assertions scan the entire authored library, not just the 15 new nodes,
# so they keep holding (and catch regressions) as later batches land. The
# prerequisite graph is read from scope_sequences and cross-checked against the
# template edges.


def test_library_ids_are_contiguous_no_gaps_no_duplicates():
    keys = list(MATH_FOUNDATIONAL_CONTENT.keys())
    nums = [_num(k) for k in keys]
    duplicates = sorted({n for n in nums if nums.count(n) > 1})
    assert not duplicates, f"duplicate mf ids: {[f'mf-{n:02d}' for n in duplicates]}"
    top = max(nums)
    expected = set(range(1, top + 1))
    missing = sorted(expected - set(nums))
    assert not missing, f"missing mf ids (gaps): {[f'mf-{n:02d}' for n in missing]}"
    assert set(nums) == expected, f"id set is not exactly mf-01..mf-{top:02d}"


def test_cross_file_count_parity():
    content_count = len(MATH_FOUNDATIONAL_CONTENT)
    scope_count = len(
        [t for t in get_scope_sequence("mathematics", "foundational") if str(t["ref"]).startswith("math_f_")]
    )
    template_count = len({tn.ref for tn in MATH_FOUNDATIONAL.nodes if str(tn.ref).startswith("mf-")})
    assert content_count == scope_count == template_count, (
        f"count mismatch: content={content_count}, scope={scope_count}, template={template_count}"
    )


def test_every_prerequisite_references_a_real_node():
    scope = _scope_by_ref()
    dangling: list[str] = []
    for ref, entry in scope.items():
        for p in entry.get("prerequisites", []):
            # Content ids zero-pad to at least two digits (mf-01, mf-10, mf-100).
            content_id = f"mf-{_num(p):02d}"
            if content_id not in MATH_FOUNDATIONAL_CONTENT or p not in scope:
                dangling.append(f"{ref} -> {p}")
    assert not dangling, f"dangling prerequisite references: {dangling}"


# One pre-existing forward-reference pair lives in the ORIGINAL mf-01..mf-30
# spine, which this contract is forbidden to edit: mf-07 (Addition Facts to 20)
# and mf-08 (Subtraction Facts to 20) both list mf-09 (Place Value Tens and
# Ones) as a prerequisite. The dependency is conceptually correct (adding and
# subtracting to twenty rests on tens-and-ones place value); only the original
# id NUMBERING is out of prerequisite order. The graph stays acyclic. Every node
# the authorship contract governs (mf-31 onward, authored in strict prerequisite
# order) is backward-only, and this gate fails loudly on any NEW forward-
# reference beyond these two documented legacy artifacts.
KNOWN_LEGACY_FORWARD_REFS: set[tuple[str, str]] = {
    ("math_f_07", "math_f_09"),
    ("math_f_08", "math_f_09"),
}


def test_prerequisites_are_backward_only_topologically_sound():
    scope = _scope_by_ref()
    forward: set[tuple[str, str]] = set()
    for ref, entry in scope.items():
        n = _num(ref)
        for p in entry.get("prerequisites", []):
            if _num(p) >= n:
                forward.add((ref, p))
    new_forward = forward - KNOWN_LEGACY_FORWARD_REFS
    assert not new_forward, f"new forward references (prerequisite id not strictly earlier): {sorted(new_forward)}"
    assert forward <= KNOWN_LEGACY_FORWARD_REFS, f"unexpected forward-reference set: {sorted(forward)}"


def test_prerequisite_graph_is_acyclic():
    scope = _scope_by_ref()
    graph = {ref: list(entry.get("prerequisites", [])) for ref, entry in scope.items()}

    WHITE, GREY, BLACK = 0, 1, 2
    color = dict.fromkeys(graph, WHITE)
    cycle_path: list[str] = []

    def visit(node: str, stack: list[str]) -> bool:
        color[node] = GREY
        stack.append(node)
        for nxt in graph.get(node, []):
            if nxt not in color:
                continue
            if color[nxt] == GREY:
                cycle_path.extend(stack[stack.index(nxt) :] + [nxt])
                return True
            if color[nxt] == WHITE and visit(nxt, stack):
                return True
        stack.pop()
        color[node] = BLACK
        return False

    for ref in graph:
        if color[ref] == WHITE and visit(ref, []):
            break
    assert not cycle_path, f"prerequisite cycle detected: {' -> '.join(cycle_path)}"


def test_spiral_review_references_resolve_to_real_prior_nodes():
    """Every new node's spiral_review names only real, strictly-earlier mf nodes."""
    unresolved: list[str] = []
    for node_id in NEW_IDS:
        num = _num(node_id)
        spiral = MATH_FOUNDATIONAL_CONTENT[node_id]["philosophy_specific"]["traditional"]["spiral_review"]
        text = " ".join(spiral)
        referenced = [f"mf-{m:02d}" for m in range(1, 121) if f"mf-{m:02d}" in text]
        assert referenced, f"{node_id} spiral_review references no mf node"
        for r in referenced:
            if r not in MATH_FOUNDATIONAL_CONTENT:
                unresolved.append(f"{node_id} -> {r} (missing)")
            elif _num(r) >= num:
                unresolved.append(f"{node_id} -> {r} (not earlier)")
    assert not unresolved, f"unresolvable spiral references: {unresolved}"


# ── Resolver + generator gates (DB) ──────────────────────────────────────


@pytest.mark.parametrize("ref", NEW_REFS)
async def test_resolver_resolves_each_new_ref(db_session, household, ref):
    res = await resolve_ref_to_uuid(db_session, ref, household.id)
    assert res.node_uuid is not None, f"{ref} did not resolve to a UUID"
    assert res.unresolved is None


async def test_generator_plan_all_resolve_zero_needs_content(db_session, household):
    """A foundational plan over the full 120-topic scope resolves every topic:
    zero needs_content weeks (the 15 new nodes are no longer placeholders), with
    120 distinct focus-node UUIDs."""
    out = await generate_for_subject(
        db_session,
        household.id,
        "mathematics",
        "foundational",
        hours_per_week=4.0,
        total_weeks=120,
        start_date=date(2026, 9, 1),
    )
    needs = [w for w in out["weeks"] if w.get("needs_content")]
    assert needs == [], f"unexpected needs_content weeks: {[w['week_number'] for w in needs]}"
    resolved_ids = {fid for w in out["weeks"] for fid in w["focus_nodes"]}
    assert len(resolved_ids) == 120
