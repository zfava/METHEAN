"""Gold-standard gate for the FINAL math foundational batch mf-151..mf-157, which
closes the complete 157-node K-2 tier. Carries the per-batch gold-standard gates,
the whole-library graph-integrity gate scanning every mf node (mf-01..mf-157),
and an ESCALATED cross-band gate for the spiral-review (section 15) and
cumulative-assessment (section 16) capstone nodes.

The escalated cross-band minimums (prerequisites must span at least this many
DISTINCT prior concept bands) are:
    mf-151..mf-154 (section 15): >= 2 bands
    mf-155 (end of Kindergarten): >= 3 bands
    mf-156 (end of Grade 1):      >= 4 bands
    mf-157 (end of Grade 2):      >= 5 bands (terminal tier capstone)

Per the gap doc, mf-152/153/154 carry single-prereq chains that span only one
band; those three keep their gap-doc prerequisite and add cross-band
prerequisites reflecting the bands the review node genuinely spans, so they meet
the section 15 minimum. mf-151 and mf-155/156/157 meet their minimums with the
exact gap-doc prerequisites.
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

NEW_NUMS = list(range(151, 158))
NEW_IDS = [f"mf-{n}" for n in NEW_NUMS]
NEW_REFS = [f"math_f_{n}" for n in NEW_NUMS]

# Authoritative prerequisite map (docs/math_foundational_gap.md, mf-151..mf-157).
# mf-152/153/154 augment their gap-doc prerequisite with cross-band prerequisites
# to meet the escalated section 15 minimum (see module docstring).
EXPECTED_PREREQS: dict[str, list[str]] = {
    "mf-151": ["mf-73", "mf-82"],
    "mf-152": ["mf-148", "mf-56", "mf-111", "mf-138", "mf-143"],
    "mf-153": ["mf-152", "mf-96", "mf-119", "mf-128"],
    "mf-154": ["mf-153", "mf-92", "mf-82", "mf-102"],
    "mf-155": ["mf-63", "mf-78", "mf-17", "mf-15", "mf-16"],
    "mf-156": ["mf-73", "mf-82", "mf-88", "mf-90", "mf-126"],
    "mf-157": ["mf-94", "mf-96", "mf-106", "mf-147", "mf-132", "mf-138"],
}

# Escalated cross-band minimums for the section 15 / 16 capstone nodes.
CROSS_BAND_MINIMUMS: dict[str, int] = {
    "mf-151": 2,
    "mf-152": 2,
    "mf-153": 2,
    "mf-154": 2,
    "mf-155": 3,
    "mf-156": 4,
    "mf-157": 5,
}

ACCOMMODATION_KEYS = {"dyslexia", "adhd", "gifted", "visual_learner", "kinesthetic_learner", "auditory_learner"}


def _num(node_id: str) -> int:
    """Numeric part of an mf-NN or math_f_NN id."""
    return int(node_id.split("_")[-1] if node_id.startswith("math_f_") else node_id.split("-")[1])


# Concept band for each authored node, following the gap doc's section grouping.
_COVERED_BANDS: dict[int, str] = {
    1: "counting",
    2: "counting",
    3: "counting",
    4: "counting",
    5: "addition",
    6: "subtraction",
    7: "addition",
    8: "subtraction",
    9: "place_value",
    10: "patterns",
    11: "patterns",
    12: "patterns",
    13: "measurement",
    14: "measurement",
    15: "time",
    16: "money",
    17: "geometry",
    18: "patterns",
    19: "place_value",
    20: "patterns",
    21: "fractions",
    22: "data",
    23: "word_problems",
    24: "word_problems",
    25: "addition",
    26: "subtraction",
    27: "multidigit",
    28: "addition",
    29: "geometry",
    30: "cumulative",
}
_GAP_BAND_RANGES: list[tuple[int, int, str]] = [
    (31, 44, "counting"),
    (45, 51, "patterns"),
    (52, 59, "place_value"),
    (60, 74, "addition"),
    (75, 85, "subtraction"),
    (86, 97, "multidigit"),
    (98, 108, "multiplication"),
    (109, 116, "measurement"),
    (117, 124, "geometry"),
    (125, 128, "fractions"),
    (129, 133, "time"),
    (134, 139, "money"),
    (140, 143, "data"),
    (144, 149, "word_problems"),
    (150, 154, "spiral"),
    (155, 157, "cumulative"),
]


def _band_of(num: int) -> str:
    if num in _COVERED_BANDS:
        return _COVERED_BANDS[num]
    for lo, hi, band in _GAP_BAND_RANGES:
        if lo <= num <= hi:
            return band
    return "unknown"


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


def test_counts_now_one_hundred_fifty_seven():
    assert len(MATH_FOUNDATIONAL_CONTENT) == 157
    assert len(get_scope_sequence("mathematics", "foundational")) == 157
    assert len(MATH_FOUNDATIONAL.nodes) == 157


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


# ── ESCALATED section 15 / 16 cross-band check ───────────────────────────


def test_capstone_nodes_meet_escalated_cross_band_minimums():
    """Each spiral-review (section 15) and cumulative-assessment (section 16)
    node must list prerequisites spanning at least its escalated minimum number
    of DISTINCT prior concept bands: section 15 >= 2, end-of-K >= 3,
    end-of-Grade-1 >= 4, end-of-Grade-2 >= 5 (the terminal tier capstone)."""
    for node_id, minimum in CROSS_BAND_MINIMUMS.items():
        prereqs = EXPECTED_PREREQS[node_id]
        bands = {_band_of(_num(p)) for p in prereqs}
        assert "unknown" not in bands, f"{node_id} has a prereq with an unknown band: {prereqs}"
        assert len(bands) >= minimum, (
            f"{node_id} prerequisites span only {len(bands)} bands {sorted(bands)}; escalated minimum is {minimum}"
        )


# ── WHOLE-LIBRARY GRAPH-INTEGRITY GATE (scans mf-01..mf-157) ──────────────


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
            content_id = f"mf-{_num(p):02d}"
            if content_id not in MATH_FOUNDATIONAL_CONTENT or p not in scope:
                dangling.append(f"{ref} -> {p}")
    assert not dangling, f"dangling prerequisite references: {dangling}"


# One pre-existing forward-reference pair lives in the ORIGINAL mf-01..mf-30
# spine, which this contract is forbidden to edit: mf-07 and mf-08 both list
# mf-09 (Place Value Tens and Ones) as a prerequisite. The dependency is
# conceptually correct; only the original id NUMBERING is out of order. The graph
# stays acyclic. Every node the authorship contract governs (mf-31 onward) is
# backward-only, and this gate fails on any NEW forward-reference beyond these two.
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
        referenced = [f"mf-{m:02d}" for m in range(1, 158) if f"mf-{m:02d}" in text]
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


async def test_generator_plan_full_tier_zero_needs_content(db_session, household):
    """The terminal check for the whole tier: a foundational plan over the full
    157-topic scope resolves every topic, with EXACTLY zero needs_content weeks
    and 157 distinct focus-node UUIDs. This batch brings needs_content to zero
    for the complete math-foundational scope."""
    out = await generate_for_subject(
        db_session,
        household.id,
        "mathematics",
        "foundational",
        hours_per_week=4.0,
        total_weeks=157,
        start_date=date(2026, 9, 1),
    )
    needs = [w for w in out["weeks"] if w.get("needs_content")]
    assert needs == [], f"unexpected needs_content weeks: {[w['week_number'] for w in needs]}"
    resolved_ids = {fid for w in out["weeks"] for fid in w["focus_nodes"]}
    assert len(resolved_ids) == 157
