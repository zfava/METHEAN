"""Gold-standard gate for the EIGHTH reading-foundational batch rf-131..rf-145.

Strand-boundary report (in the deliverable):
- rf-131..rf-133 close S13 (Fluency): the deferred connected-text words-per-minute
  rate checkpoints. rf-131 is the honest end-of-Kindergarten target (accuracy on
  short text, NOT a timed CWPM milestone), rf-132 the end-of-Grade-1 rate
  (roughly 50 to 60 CWPM), and rf-133 the end-of-Grade-2 fluency capstone
  (accuracy + rate + prosody, roughly 90 to 100 CWPM). All rate nodes are
  accuracy-gated and use research-based ranges, not fabricated single numbers.
- rf-134..rf-138 are S14 (Spelling / Encoding strand, the inverse of decoding):
  a dictation routine (rf-134), spell-from-dictation with blends/digraphs/silent-e
  (rf-135) and vowel-teams/r-controlled (rf-136), applying spelling rules
  (rf-137), and an encoding automaticity checkpoint (rf-138). NOTE: the gap doc
  places S14 in the numeric range BETWEEN the CWPM close and the comprehension
  opening; this batch follows the gap doc.
- rf-139..rf-145 open S15 (Foundational Comprehension): retell in order (rf-139),
  setting (rf-140), story-elements review (rf-141), key details (rf-142),
  inference (rf-143), ask/answer questions (rf-144), and word meaning from
  context and word parts (rf-145). S17 terminal cumulative assessments
  (rf-153/rf-154) are far outside this range, reserved for a later batch.

Domain standards enforced by this gate:
- CWPM-GROUNDED (asserted): each rate node carries a grade-anchored target
  consistent with standard ORF norms (K is accuracy-based/pre-CWPM; G1 ~50-60;
  G2 ~90-100) stated as a range with a norms-vary note, NOT a fabricated single
  universal number.
- ACCURACY-GATED (asserted): each rate node states accuracy (95 percent) is held
  first and names the speed-without-accuracy (fast-but-inaccurate) misconception.
- COMPREHENSION dual-bridge (asserted): the first comprehension node (rf-139)
  lists BOTH a fluency node (rf-130) AND rf-21 (listening comprehension) as
  prerequisites, and frames comprehension as listening-comprehension applied to
  self-decoded text.
- WORD-CALLING (asserted): every comprehension node (rf-139..rf-145) names the
  decode-without-meaning (word-calling) misconception with the
  understanding-is-the-goal correction.

Carries forward the prior gates: validator, NATIVE_KEYS, depth floor,
parent-directed (no choice_space), three-file integrity, and the WHOLE-LIBRARY
graph-integrity gate scanning rf-01..rf-145, INCLUDING the documented legacy
carve-out read_f_15 -> read_f_21/22. Everything this batch authors (rf-131+) is
strictly backward-only.
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

NEW_NUMS = list(range(131, 146))
NEW_IDS = [f"rf-{n}" for n in NEW_NUMS]
NEW_REFS = [f"read_f_{n}" for n in NEW_NUMS]

# Authoritative prerequisite map (docs/reading_foundational_gap.md, rf-131..rf-145).
# rf-139 is augmented with rf-21 (listening comprehension) and rf-130 (fluency)
# to make the comprehension dual bridge explicit, alongside the gap-doc parents
# rf-22 (story retelling) and rf-122 (first connected-text node).
EXPECTED_PREREQS: dict[str, list[str]] = {
    "rf-131": ["rf-127"],
    "rf-132": ["rf-129", "rf-131", "rf-130"],
    "rf-133": ["rf-132"],
    "rf-134": ["rf-69"],
    "rf-135": ["rf-134", "rf-84"],
    "rf-136": ["rf-135", "rf-100"],
    "rf-137": ["rf-136", "rf-113"],
    "rf-138": ["rf-137", "rf-120"],
    "rf-139": ["rf-22", "rf-122", "rf-21", "rf-130"],
    "rf-140": ["rf-14"],
    "rf-141": ["rf-140", "rf-13"],
    "rf-142": ["rf-12"],
    "rf-143": ["rf-23", "rf-142"],
    "rf-144": ["rf-143"],
    "rf-145": ["rf-19", "rf-111"],
}

# CWPM rate nodes and the grade band + numeric range each must carry.
RATE_NODES = ["rf-131", "rf-132", "rf-133"]
RATE_GRADE_BAND = {
    "rf-131": ["kindergarten"],
    "rf-132": ["grade 1", "grade-1"],
    "rf-133": ["grade 2", "grade-2"],
}
RATE_RANGE_NUMBERS = {
    "rf-131": [],  # K is accuracy-based / pre-CWPM, no fabricated number
    "rf-132": ["50", "60"],
    "rf-133": ["90", "100"],
}

# Comprehension nodes (S15) that must name the word-calling misconception.
COMPREHENSION_NODES = ["rf-139", "rf-140", "rf-141", "rf-142", "rf-143", "rf-144", "rf-145"]

# Comprehension dual bridge: first comprehension node lists a fluency node AND rf-21.
FIRST_COMPREHENSION_NODE = "rf-139"
FLUENCY_NODES = {"rf-130", "rf-133"}
LISTENING_COMPREHENSION_NODE = "rf-21"

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


def _misconceptions(node_id: str) -> list[str]:
    return READING_FOUNDATIONAL_CONTENT[node_id]["teaching_guidance"]["common_misconceptions"]


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
    spiral = READING_FOUNDATIONAL_CONTENT[node_id]["philosophy_specific"]["traditional"]["spiral_review"]
    text = " ".join(spiral)
    num = _num(node_id)
    referenced = [f"rf-{m}" for m in range(1, num) if f"rf-{m}" in text] + [
        f"rf-{m:02d}" for m in range(1, num) if f"rf-{m:02d}" in text
    ]
    assert referenced, f"{node_id} spiral_review references no prior rf node: {spiral}"


# ── CWPM-GROUNDED: grade-anchored, research-based ranges ─────────────────


@pytest.mark.parametrize("node_id", RATE_NODES)
def test_rate_node_is_grade_anchored(node_id):
    text = _node_text(node_id)
    bands = RATE_GRADE_BAND[node_id]
    assert any(b in text for b in bands), f"{node_id} is not anchored to its grade band {bands}"


@pytest.mark.parametrize("node_id", RATE_NODES)
def test_rate_node_uses_research_based_range_not_fabricated_number(node_id):
    """G1 and G2 nodes state a numeric range with a norms-vary note; K is honestly
    pre-CWPM / accuracy-based (no fabricated universal number)."""
    text = _node_text(node_id)
    if node_id == "rf-131":
        assert "not yet a words-per-minute" in text or "not a timed" in text, (
            "rf-131 must state Kindergarten is not a timed CWPM milestone"
        )
        assert "accuracy" in text
    else:
        nums = RATE_RANGE_NUMBERS[node_id]
        assert all(n in text for n in nums), f"{node_id} missing its range numbers {nums}"
        assert "norms vary" in text, f"{node_id} must note that norms vary by source"
        assert "correct words per minute" in text, f"{node_id} must use correct-words-per-minute"


@pytest.mark.parametrize("node_id", RATE_NODES)
def test_rate_node_is_accuracy_gated(node_id):
    """Each rate node states accuracy (95 percent) is held first and names the
    speed-without-accuracy misconception."""
    text = _node_text(node_id)
    assert "95 percent" in text, f"{node_id} does not state the 95 percent accuracy gate"
    misc = " ".join(_misconceptions(node_id)).lower()
    speed_misc = ("fast" in misc and ("inaccurate" in misc or "not fluent" in misc)) or (
        "speed" in misc and ("not the goal" in misc or "meaningless" in misc)
    )
    assert speed_misc, f"{node_id} does not name the speed-without-accuracy misconception: {_misconceptions(node_id)}"


# ── COMPREHENSION dual bridge + word-calling ─────────────────────────────


def test_first_comprehension_node_dual_bridge():
    """The first comprehension node (rf-139) lists BOTH a fluency node (rf-130) AND
    rf-21 (listening comprehension), and frames comprehension as listening
    comprehension applied to self-decoded text."""
    prereqs = set(EXPECTED_PREREQS[FIRST_COMPREHENSION_NODE])
    assert prereqs & FLUENCY_NODES, f"rf-139 reaches no fluency node: {sorted(prereqs)}"
    assert LISTENING_COMPREHENSION_NODE in prereqs, "rf-139 must list rf-21 (listening comprehension)"
    text = _node_text(FIRST_COMPREHENSION_NODE)
    assert "read aloud" in text or "listening comprehension" in text, (
        "rf-139 must frame comprehension as listening comprehension applied to self-decoded text"
    )
    assert "decode" in text and ("independently" in text or "self" in text)


@pytest.mark.parametrize("node_id", COMPREHENSION_NODES)
def test_comprehension_node_names_word_calling_misconception(node_id):
    """Every comprehension node names the decode-without-meaning (word-calling)
    misconception, with the understanding-is-the-goal correction."""
    misc = " ".join(_misconceptions(node_id)).lower()
    names_word_calling = "word-calling" in misc or (("decod" in misc) and ("meaning" in misc or "understand" in misc))
    assert names_word_calling, f"{node_id} does not name the word-calling misconception: {_misconceptions(node_id)}"


# ── Three-file integrity ─────────────────────────────────────────────────


def test_all_three_files_have_every_new_node():
    scope = _scope_by_ref()
    tnodes = _template_nodes()
    for n in NEW_NUMS:
        assert f"rf-{n}" in READING_FOUNDATIONAL_CONTENT, f"rf-{n} missing from content"
        assert f"read_f_{n}" in scope, f"read_f_{n} missing from scope_sequences"
        assert f"rf-{n}" in tnodes, f"rf-{n} missing from READING_FOUNDATIONAL template"


def test_counts_now_one_hundred_forty_five():
    # Lower bound: rf-145 landed in this batch; the final batch (rf-146..155) raises these.
    assert len(READING_FOUNDATIONAL_CONTENT) >= 145
    assert len([t for t in get_scope_sequence("phonics_reading", "foundational")]) >= 145
    assert len(READING_FOUNDATIONAL.nodes) >= 145


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


# ── WHOLE-LIBRARY GRAPH-INTEGRITY GATE (scans rf-01..rf-145) ─────────────


def test_library_ids_are_contiguous_no_gaps_no_duplicates():
    keys = list(READING_FOUNDATIONAL_CONTENT.keys())
    nums = [_num(k) for k in keys]
    duplicates = sorted({n for n in nums if nums.count(n) > 1})
    assert not duplicates, f"duplicate rf ids: {sorted(duplicates)}"
    top = max(nums)
    expected = set(range(1, top + 1))
    missing = sorted(expected - set(nums))
    assert not missing, f"missing rf ids (gaps): {missing}"
    assert top >= 145, f"library top should be at least rf-145, got rf-{top}"
    assert set(nums) == expected, f"id set is not exactly rf-01..rf-{top}"


def test_cross_file_count_parity():
    content_count = len(READING_FOUNDATIONAL_CONTENT)
    scope_count = len(
        [t for t in get_scope_sequence("phonics_reading", "foundational") if str(t["ref"]).startswith("read_f_")]
    )
    template_count = len({tn.ref for tn in READING_FOUNDATIONAL.nodes if str(tn.ref).startswith("rf-")})
    assert content_count == scope_count == template_count >= 145, (
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
        spiral = READING_FOUNDATIONAL_CONTENT[node_id]["philosophy_specific"]["traditional"]["spiral_review"]
        text = " ".join(spiral)
        referenced = {f"rf-{m}" for m in range(1, 146) if f"rf-{m}" in text}
        referenced |= {f"rf-{m:02d}" for m in range(1, 146) if f"rf-{m:02d}" in text}
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


async def test_generator_plan_reading_tier_zero_needs_content(db_session, household):
    """needs_content drops by exactly 15: before this batch, 130 of the 145 reading
    refs resolved (rf-01..rf-130) and 15 were needs_content (rf-131..rf-145); now all
    145 resolve, so the full 145-topic plan has zero needs_content weeks and 145
    distinct focus-node UUIDs."""
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
    # Lower bound: rf-01..rf-145 all resolve; the final batch adds more resolvable refs.
    assert len(resolved_ids) >= 145

    newly = 0
    for ref in NEW_REFS:
        res = await resolve_ref_to_uuid(db_session, ref, household.id)
        assert res.node_uuid is not None and res.unresolved is None, f"{ref} unresolved"
        newly += 1
    assert newly == 15
