"""Gold-standard gate for the NINTH and FINAL reading-foundational batch rf-146..rf-155.

This batch CLOSES the Reading Foundational tier at 155/155/155.

Strand-boundary + terminal-scope report (in the deliverable):
- rf-146..rf-147 complete S15 (Foundational Comprehension): distinguishing
  fiction from informational text (rf-146) and comparing two texts (rf-147).
- rf-148..rf-152 are S16 (Daily Spiral-Review Structure, explicit-phonics
  routines): a daily phonics review (rf-148), a blending/word-ladder drill
  (rf-149), a daily dictation review (rf-150), cumulative review checkpoints
  (rf-151), and an error-analysis/corrections routine (rf-152). NOTE: per the gap
  doc, rf-146..rf-152 is NOT a single strand; it is the S15 comprehension tail
  plus the distinct S16 spiral-review-structure strand. This batch follows the
  gap doc.
- rf-153..rf-155 are S17 (Cumulative Assessments, terminal): the end-of-grade
  reading READINESS gates, the reading analogue of math mf-155/156/157.
  rf-153 = end-of-Kindergarten, rf-154 = end-of-Grade-1, rf-155 = end-of-Grade-2
  (the tier capstone). rf-155 is the final node; the tier closes at rf-155.

Terminal cross-strand standards enforced by this escalated gate (modeled on the
math tier's cross-band gate):
- Each terminal node (rf-153/154/155) has prerequisites spanning >=3 DISTINCT
  prior strands; the end-of-G2 capstone (rf-155) spans >=4 distinct strands (the
  widest set).
- Each terminal node's assessment items are INTEGRATIVE (decoding + fluency +
  comprehension together on grade-appropriate text), not single-skill drills, and
  honor the grade-appropriate fluency targets (K accuracy-based / no CWPM; G1
  ~50-60 CWPM; G2 ~90-100 CWPM, accuracy-gated, norms vary by source).

Carries forward the prior gates: validator, NATIVE_KEYS, depth floor,
parent-directed (no choice_space), three-file integrity, and the WHOLE-LIBRARY
graph-integrity gate scanning rf-01..rf-155 (CLOSING the tier), INCLUDING the
documented legacy carve-out read_f_15 -> read_f_21/22. Everything this batch
authors (rf-146+) is strictly backward-only.
"""

from datetime import date

import pytest

from app.content.reading_foundational_content import READING_FOUNDATIONAL_CONTENT
from app.content.scope_sequences import get_scope_sequence
from app.services.native_curriculum_generator import generate_for_subject
from app.services.node_content import validate_content, validate_philosophy
from app.services.node_resolver import resolve_ref_to_uuid
from app.services.templates import READING_FOUNDATIONAL

# Canonical requirement sets, imported (not copied) from the schema test.
from tests.test_node_content import NATIVE_KEYS, PHILOSOPHIES, UNSCHOOLING_FORBIDDEN

NEW_NUMS = list(range(146, 156))
NEW_IDS = [f"rf-{n}" for n in NEW_NUMS]
NEW_REFS = [f"read_f_{n}" for n in NEW_NUMS]

# Authoritative prerequisite map (docs/reading_foundational_gap.md, rf-146..rf-155).
EXPECTED_PREREQS: dict[str, list[str]] = {
    "rf-146": ["rf-141"],
    "rf-147": ["rf-146", "rf-142"],
    "rf-148": ["rf-64", "rf-71"],
    "rf-149": ["rf-148", "rf-47"],
    "rf-150": ["rf-134", "rf-148"],
    "rf-151": ["rf-149", "rf-126"],
    "rf-152": ["rf-151", "rf-138"],
    "rf-153": ["rf-49", "rf-64", "rf-71", "rf-131", "rf-22"],
    "rf-154": ["rf-92", "rf-121", "rf-132", "rf-139", "rf-135"],
    "rf-155": ["rf-114", "rf-133", "rf-143", "rf-138", "rf-125"],
}

# Terminal cumulative-assessment nodes (S17).
TERMINAL_NODES = ["rf-153", "rf-154", "rf-155"]
CAPSTONE_NODE = "rf-155"

# Strand classification for the terminal prerequisites (coarse, defensible bands).
STRAND_OF: dict[str, str] = {
    "rf-49": "phonemic_awareness",
    "rf-64": "phonics_decoding",
    "rf-71": "phonics_decoding",
    "rf-92": "phonics_decoding",
    "rf-114": "phonics_decoding",
    "rf-131": "fluency",
    "rf-132": "fluency",
    "rf-133": "fluency",
    "rf-22": "comprehension",
    "rf-139": "comprehension",
    "rf-143": "comprehension",
    "rf-121": "high_frequency_words",
    "rf-135": "encoding",
    "rf-138": "encoding",
    "rf-125": "connected_text",
}

# Terminal grade-fluency targets.
TERMINAL_GRADE_BAND = {
    "rf-153": ["kindergarten"],
    "rf-154": ["grade 1", "grade-1"],
    "rf-155": ["grade 2", "grade-2"],
}
TERMINAL_RATE_NUMBERS = {
    "rf-153": [],  # K accuracy-based / no CWPM
    "rf-154": ["50", "60"],
    "rf-155": ["90", "100"],
}

ACCOMMODATION_KEYS = {"dyslexia", "adhd", "gifted", "visual_learner", "kinesthetic_learner", "auditory_learner"}

# The single legacy forward-reference pair in the un-editable original spine.
KNOWN_LEGACY_FORWARD_REFS: set[tuple[str, str]] = {
    ("read_f_15", "read_f_21"),
    ("read_f_15", "read_f_22"),
}


def _num(node_id: str) -> int:
    return int(node_id.split("_")[-1] if node_id.startswith("read_f_") else node_id.split("-")[1])


def _ref_for(num: int) -> str:
    return f"read_f_{num}"


def _scope_by_ref() -> dict[str, dict]:
    return {t["ref"]: t for t in get_scope_sequence("phonics_reading", "foundational")}


def _template_nodes() -> dict[str, object]:
    return {tn.ref: tn for tn in READING_FOUNDATIONAL.nodes}


def _node_text(node_id: str) -> str:
    import json

    return json.dumps(READING_FOUNDATIONAL_CONTENT[node_id]).lower()


def _spiral(node_id: str) -> str:
    return " ".join(READING_FOUNDATIONAL_CONTENT[node_id]["philosophy_specific"]["traditional"]["spiral_review"])


def _strands_of_refs(refs) -> set[str]:
    return {STRAND_OF[r] for r in refs if r in STRAND_OF}


# ── Validator gate (real validator) ──────────────────────────────────────


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_validate_content_passes(node_id):
    assert validate_content(READING_FOUNDATIONAL_CONTENT[node_id]) == []


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_validate_philosophy_no_hard_fail(node_id):
    errors = [i for i in validate_philosophy(READING_FOUNDATIONAL_CONTENT[node_id]) if i.startswith("error:")]
    assert errors == []


# ── NATIVE_KEYS gate ─────────────────────────────────────────────────────


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_five_native_philosophy_variants(node_id):
    ps = READING_FOUNDATIONAL_CONTENT[node_id]["philosophy_specific"]
    for philosophy in PHILOSOPHIES:
        assert philosophy in ps, f"{node_id} missing {philosophy}"
        variant = ps[philosophy]
        assert isinstance(variant, dict)
        missing = NATIVE_KEYS[philosophy] - set(variant.keys())
        assert not missing, f"{node_id}/{philosophy} missing native keys: {sorted(missing)}"


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_unschooling_carries_no_forbidden_key(node_id):
    unschooling = READING_FOUNDATIONAL_CONTENT[node_id]["philosophy_specific"]["unschooling"]
    forbidden = UNSCHOOLING_FORBIDDEN.intersection(unschooling.keys())
    assert not forbidden, f"{node_id} unschooling has forbidden keys: {sorted(forbidden)}"


# ── Depth floor (mf-01 standard) ─────────────────────────────────────────


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_depth_floor(node_id):
    c = READING_FOUNDATIONAL_CONTENT[node_id]
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


# ── Parent-directed: NO choice_space this batch ──────────────────────────


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_no_choice_space_parent_directed(node_id):
    assert "choice_space" not in READING_FOUNDATIONAL_CONTENT[node_id]


@pytest.mark.parametrize("node_id", NEW_IDS)
def test_traditional_spiral_references_a_prior_node(node_id):
    spiral = _spiral(node_id)
    num = _num(node_id)
    referenced = [f"rf-{m}" for m in range(1, num) if f"rf-{m}" in spiral] + [
        f"rf-{m:02d}" for m in range(1, num) if f"rf-{m:02d}" in spiral
    ]
    assert referenced, f"{node_id} spiral_review references no prior rf node: {spiral}"


# ── TERMINAL CROSS-STRAND GATE (escalated, mirrors math cross-band gate) ──


@pytest.mark.parametrize("node_id", TERMINAL_NODES)
def test_terminal_prereqs_span_at_least_three_strands(node_id):
    """Each terminal node's prerequisites span >= 3 distinct prior strands."""
    prereqs = EXPECTED_PREREQS[node_id]
    strands = _strands_of_refs(prereqs)
    assert len(strands) >= 3, f"{node_id} prereqs span only {sorted(strands)} (need >= 3 distinct strands)"


def test_capstone_spans_widest_set_of_strands():
    """The end-of-Grade-2 capstone (rf-155) spans >= 4 distinct strands, the
    widest set."""
    strands = _strands_of_refs(EXPECTED_PREREQS[CAPSTONE_NODE])
    assert len(strands) >= 4, f"rf-155 capstone spans only {sorted(strands)} (need >= 4 distinct strands)"


@pytest.mark.parametrize("node_id", TERMINAL_NODES)
def test_terminal_spiral_review_spans_multiple_strands(node_id):
    """Each terminal node's spiral_review references nodes spanning >= 3 distinct
    prior strands, mirroring the cross-band review of the math terminal gates."""
    spiral = _spiral(node_id)
    referenced = {r for r in STRAND_OF if r in spiral}
    strands = _strands_of_refs(referenced)
    assert len(strands) >= 3, f"{node_id} spiral_review spans only {sorted(strands)} (need >= 3 distinct strands)"


# ── TERMINAL-INTEGRATIVE: cross-skill, grade-appropriate fluency targets ─


@pytest.mark.parametrize("node_id", TERMINAL_NODES)
def test_terminal_assessment_is_integrative(node_id):
    """Each terminal node integrates decoding + fluency + comprehension together,
    not single-skill drills."""
    text = _node_text(node_id)
    has_decoding = "decod" in text
    has_fluency = "fluen" in text or "accuracy" in text or "rate" in text
    has_comprehension = "comprehen" in text or "retell" in text or "understand" in text or "inference" in text
    assert has_decoding and has_fluency and has_comprehension, (
        f"{node_id} is not integrative (decoding+fluency+comprehension): "
        f"decoding={has_decoding}, fluency={has_fluency}, comprehension={has_comprehension}"
    )
    # An integrative passage-reading assessment item must exist.
    big_items = [
        ai
        for ai in READING_FOUNDATIONAL_CONTENT[node_id]["assessment_items"]
        if "rubric" in ai and ("read" in ai["prompt"].lower())
    ]
    assert big_items, f"{node_id} has no integrative passage-reading assessment item"


@pytest.mark.parametrize("node_id", TERMINAL_NODES)
def test_terminal_honors_grade_fluency_target(node_id):
    text = _node_text(node_id)
    assert any(b in text for b in TERMINAL_GRADE_BAND[node_id]), f"{node_id} not anchored to its grade band"
    if node_id == "rf-153":
        # End-of-K is accuracy-based, NOT a timed CWPM milestone.
        assert "accuracy" in text
        assert "not a timed" in text or "not a words-per-minute" in text or "not a cwpm" in text
    else:
        nums = TERMINAL_RATE_NUMBERS[node_id]
        assert all(n in text for n in nums), f"{node_id} missing its rate range {nums}"
        assert "correct words per minute" in text
        assert "95 percent" in text, f"{node_id} must hold accuracy first (95 percent)"
        assert "varies by source" in text, f"{node_id} must note that norms vary by source"


# ── Three-file integrity ─────────────────────────────────────────────────


def test_all_three_files_have_every_new_node():
    scope = _scope_by_ref()
    tnodes = _template_nodes()
    for n in NEW_NUMS:
        assert f"rf-{n}" in READING_FOUNDATIONAL_CONTENT, f"rf-{n} missing from content"
        assert f"read_f_{n}" in scope, f"read_f_{n} missing from scope_sequences"
        assert f"rf-{n}" in tnodes, f"rf-{n} missing from READING_FOUNDATIONAL template"


def test_counts_now_one_hundred_fifty_five_tier_complete():
    """TIER-COMPLETE: Reading Foundational closes at exactly 155/155/155."""
    assert len(READING_FOUNDATIONAL_CONTENT) == 155
    assert len([t for t in get_scope_sequence("phonics_reading", "foundational")]) == 155
    assert len(READING_FOUNDATIONAL.nodes) == 155


# ── Prerequisite integrity (three files agree, earlier-only) ─────────────


def test_scope_prereqs_match_expected_and_are_earlier():
    scope = _scope_by_ref()
    for node_id, prereqs in EXPECTED_PREREQS.items():
        ref = _ref_for(_num(node_id))
        got = scope[ref]["prerequisites"]
        expected_refs = [_ref_for(_num(p)) for p in prereqs]
        assert got == expected_refs, f"{ref} scope prereqs {got} != {expected_refs}"
        num = _num(node_id)
        for p in prereqs:
            pid = f"rf-{_num(p)}"
            pid_padded = f"rf-{_num(p):02d}"
            assert pid in READING_FOUNDATIONAL_CONTENT or pid_padded in READING_FOUNDATIONAL_CONTENT, (
                f"{node_id} prereq {p} not a real node"
            )
            assert _num(p) < num, f"{node_id} prereq {p} is not earlier"


def test_template_edges_match_scope_prereqs_for_new_nodes():
    incoming: dict[str, set[str]] = {}
    for e in READING_FOUNDATIONAL.edges:
        incoming.setdefault(e.to_ref, set()).add(e.from_ref)
    for node_id, prereqs in EXPECTED_PREREQS.items():
        edges_in = incoming.get(node_id, set())
        assert edges_in == set(prereqs), f"{node_id} template edges {edges_in} != prereqs {set(prereqs)}"


# ── WHOLE-LIBRARY GRAPH-INTEGRITY GATE (scans rf-01..rf-155, tier closed) ─


def test_library_ids_are_contiguous_no_gaps_no_duplicates_closing_at_155():
    keys = list(READING_FOUNDATIONAL_CONTENT.keys())
    nums = [_num(k) for k in keys]
    duplicates = sorted({n for n in nums if nums.count(n) > 1})
    assert not duplicates, f"duplicate rf ids: {sorted(duplicates)}"
    top = max(nums)
    expected = set(range(1, top + 1))
    missing = sorted(expected - set(nums))
    assert not missing, f"missing rf ids (gaps): {missing}"
    assert top == 155, f"library should close at rf-155, got rf-{top}"
    assert set(nums) == expected, "id set is not exactly rf-01..rf-155"


def test_cross_file_count_parity_155():
    content_count = len(READING_FOUNDATIONAL_CONTENT)
    scope_count = len(
        [t for t in get_scope_sequence("phonics_reading", "foundational") if str(t["ref"]).startswith("read_f_")]
    )
    template_count = len({tn.ref for tn in READING_FOUNDATIONAL.nodes if str(tn.ref).startswith("rf-")})
    assert content_count == scope_count == template_count == 155, (
        f"count mismatch: content={content_count}, scope={scope_count}, template={template_count}"
    )


def test_every_prerequisite_references_a_real_node():
    scope = _scope_by_ref()
    dangling: list[str] = []
    for ref, entry in scope.items():
        for p in entry.get("prerequisites", []):
            content_id = f"rf-{_num(p)}"
            content_id_padded = f"rf-{_num(p):02d}"
            if (
                content_id not in READING_FOUNDATIONAL_CONTENT and content_id_padded not in READING_FOUNDATIONAL_CONTENT
            ) or p not in scope:
                dangling.append(f"{ref} -> {p}")
    assert not dangling, f"dangling prerequisite references: {dangling}"


def test_prerequisites_are_backward_only_except_known_legacy():
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
    new_forward_in_batch = {(r, p) for (r, p) in forward if _num(r) in NEW_NUMS}
    assert not new_forward_in_batch, f"authored batch introduced a forward reference: {sorted(new_forward_in_batch)}"


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
    unresolved: list[str] = []
    for node_id in NEW_IDS:
        num = _num(node_id)
        spiral = _spiral(node_id)
        referenced = {f"rf-{m}" for m in range(1, 156) if f"rf-{m}" in spiral}
        referenced |= {f"rf-{m:02d}" for m in range(1, 156) if f"rf-{m:02d}" in spiral}
        assert referenced, f"{node_id} spiral_review references no rf node"
        for rref in referenced:
            rn = _num(rref)
            if f"rf-{rn}" not in READING_FOUNDATIONAL_CONTENT and f"rf-{rn:02d}" not in READING_FOUNDATIONAL_CONTENT:
                unresolved.append(f"{node_id} -> {rref} (missing)")
            elif rn >= num:
                unresolved.append(f"{node_id} -> {rref} (not earlier)")
    assert not unresolved, f"unresolvable spiral references: {unresolved}"


# ── Resolver + generator gates (DB) ──────────────────────────────────────


@pytest.mark.parametrize("ref", NEW_REFS)
async def test_resolver_resolves_each_new_ref(db_session, household, ref):
    res = await resolve_ref_to_uuid(db_session, ref, household.id)
    assert res.node_uuid is not None, f"{ref} did not resolve to a UUID"
    assert res.unresolved is None


async def test_generator_plan_reading_tier_zero_needs_content_tier_complete(db_session, household):
    """TIER-COMPLETE generator gate: needs_content drops by exactly 10 (before this
    batch 145 of 155 resolved; now all 155 resolve), so the full 155-topic reading
    plan has ZERO needs_content weeks and 155 distinct focus-node UUIDs."""
    scope = get_scope_sequence("phonics_reading", "foundational")
    out = await generate_for_subject(
        db_session,
        household.id,
        "phonics_reading",
        "foundational",
        hours_per_week=4.0,
        total_weeks=len(scope),
        start_date=date(2026, 9, 1),
    )
    needs = [w for w in out["weeks"] if w.get("needs_content")]
    assert needs == [], f"unexpected needs_content weeks: {[w['week_number'] for w in needs]}"
    resolved_ids = {fid for w in out["weeks"] for fid in w["focus_nodes"]}
    assert len(resolved_ids) == 155

    newly = 0
    for ref in NEW_REFS:
        res = await resolve_ref_to_uuid(db_session, ref, household.id)
        assert res.node_uuid is not None and res.unresolved is None, f"{ref} unresolved"
        newly += 1
    assert newly == 10
