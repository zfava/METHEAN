"""Gold-standard gate for the SEVENTH reading-foundational batch rf-116..rf-130.

Strand-boundary report (in the deliverable):
- rf-116..rf-121 complete S11 (High-Frequency / Irregular Sight Words): the four
  high-frequency word sets taught with the HEART-WORD METHOD (rf-116..rf-119), a
  high-frequency word SPELL (encode) node (rf-120), and a sight-word reading
  automaticity FLUENCY checkpoint (rf-121). S11 ends at rf-121.
- rf-122..rf-126 are S12 (Decodable Connected-Text Reading): decodable phrases
  and sentences (rf-122), sentences with blends/digraphs (rf-123), passages with
  long vowels and vowel teams (rf-124), advanced passages with r-controlled,
  diphthongs, and multisyllabic words (rf-125), and self-monitoring/self-correction
  (rf-126). S12 ends at rf-126.
- rf-127..rf-130 open S13 (Fluency: Accuracy, Rate, Prosody): high accuracy
  (95 percent, rf-127), meaningful phrasing (rf-128), prosody/expression (rf-129),
  and a repeated-reading rate routine (rf-130). The discrete connected-text
  words-per-minute rate-target [F] checkpoints (rf-131..rf-133) fall in the NEXT
  batch; this batch's discrete [F] automaticity checkpoint is rf-121, and rf-127
  carries a concrete connected-text accuracy target.

THE PIVOT FROM DECODING TO FLUENCY AND MEANING, enforced by this gate:
- HEART-WORD-METHOD honesty (asserted): every S11 high-frequency-word node
  (rf-116..rf-121) reflects the heart-word method (decode the regular parts, mark
  only the irregular heart part) and names the whole-word-memorization
  misconception. S11 builds on the existing heart-word-method node (rf-115).
- FLUENCY-MEASURABLE (asserted): the fluency nodes carry observable targets
  (rf-121 instant-on-sight automaticity; rf-127 95 percent accuracy; rf-128
  three-to-five-word phrases; rf-129 punctuation/expression; rf-130 repeated
  reading with held accuracy), not a vague "reads smoothly".
- FLUENCY bridge (asserted): the first connected-text/fluency node (rf-122) lists
  a decoding-automaticity node (rf-71) as a prerequisite; rf-125 also bridges to
  multisyllabic automaticity (rf-114). Fluency is built ON automatic decoding.
- DECODING/FLUENCY IN SERVICE OF MEANING (asserted): the connected-text and
  fluency nodes tie reading to meaning, not decoding for its own sake.

Carries forward the prior gates: validator, NATIVE_KEYS, depth floor,
parent-directed (no choice_space), three-file integrity, and the WHOLE-LIBRARY
graph-integrity gate scanning rf-01..rf-130, INCLUDING the documented legacy
carve-out read_f_15 -> read_f_21/22. Everything this batch authors (rf-116+) is
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

NEW_NUMS = list(range(116, 131))
NEW_IDS = [f"rf-{n}" for n in NEW_NUMS]
NEW_REFS = [f"read_f_{n}" for n in NEW_NUMS]

# Authoritative prerequisite map (docs/reading_foundational_gap.md, rf-116..rf-130).
# rf-116 is augmented with rf-115 (the heart-word-method node it extends) alongside
# rf-10 (the existing sight-words node).
EXPECTED_PREREQS: dict[str, list[str]] = {
    "rf-116": ["rf-10", "rf-115"],
    "rf-117": ["rf-116"],
    "rf-118": ["rf-117"],
    "rf-119": ["rf-118"],
    "rf-120": ["rf-119", "rf-113"],
    "rf-121": ["rf-119"],
    "rf-122": ["rf-71", "rf-116"],
    "rf-123": ["rf-80", "rf-122"],
    "rf-124": ["rf-92", "rf-123"],
    "rf-125": ["rf-114", "rf-11"],
    "rf-126": ["rf-125"],
    "rf-127": ["rf-126"],
    "rf-128": ["rf-127"],
    "rf-129": ["rf-128"],
    "rf-130": ["rf-127"],
}

# S11 high-frequency-word nodes (the heart-word method).
S11_HEART_WORD_NODES = ["rf-116", "rf-117", "rf-118", "rf-119", "rf-120", "rf-121"]
HEART_WORD_METHOD_PARENT = "rf-115"

# Fluency nodes and the observable target keyword(s) each must carry.
FLUENCY_TARGET_KEYWORDS: dict[str, list[str]] = {
    "rf-121": ["about a second", "instant", "automatic"],
    "rf-127": ["95 percent", "per 20", "accuracy"],
    "rf-128": ["three to five", "phrase"],
    "rf-129": ["punctuation", "expression", "prosody"],
    "rf-130": ["repeated", "rate", "accuracy"],
}

# The discrete [F] automaticity checkpoint in this range, with a concrete target.
DISCRETE_FLUENCY_CHECKPOINT = "rf-121"

# First connected-text / fluency node bridges to decoding automaticity.
FIRST_FLUENCY_NODE = "rf-122"
DECODING_AUTOMATICITY = {"rf-71", "rf-114"}

# Connected-text and fluency nodes that must tie reading to meaning.
MEANING_NODES = ["rf-122", "rf-124", "rf-125", "rf-126", "rf-127", "rf-130"]

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


# ── HEART-WORD-METHOD honesty (S11) ──────────────────────────────────────


@pytest.mark.parametrize("node_id", S11_HEART_WORD_NODES)
def test_s11_node_reflects_heart_word_method(node_id):
    """Every S11 high-frequency-word node reflects the heart-word method: decode
    the regular parts and mark/recall ONLY the irregular heart part."""
    text = _node_text(node_id)
    assert "heart" in text, f"{node_id} never mentions the heart-word method"
    assert "regular" in text, f"{node_id} never names the regular (decodable) parts"
    assert any(k in text for k in ("mark", "recall", "remember")), (
        f"{node_id} never says to mark/recall only the heart part"
    )


@pytest.mark.parametrize("node_id", S11_HEART_WORD_NODES)
def test_s11_node_names_whole_word_memorization_misconception(node_id):
    """Every S11 node names the wrong approach (whole-word memorization) as a
    misconception, with the heart-word correction."""
    misc = " ".join(_misconceptions(node_id)).lower()
    names_whole = "whole" in misc and ("memoriz" in misc or "shape" in misc)
    assert names_whole, f"{node_id} does not name the whole-word-memorization misconception: {_misconceptions(node_id)}"


def test_s11_builds_on_heart_word_method_node():
    """The first S11 word-set node (rf-116) lists the existing heart-word-method
    node (rf-115) as a prerequisite, building on it rather than re-teaching it."""
    assert HEART_WORD_METHOD_PARENT in EXPECTED_PREREQS["rf-116"]


# ── FLUENCY-MEASURABLE: observable targets, not "reads smoothly" ─────────


@pytest.mark.parametrize("node_id", list(FLUENCY_TARGET_KEYWORDS.keys()))
def test_fluency_node_has_observable_target(node_id):
    """Each fluency node addresses accuracy, rate, and/or prosody with an
    OBSERVABLE/measurable target, not a vague 'reads smoothly'."""
    text = _node_text(node_id)
    hits = [kw for kw in FLUENCY_TARGET_KEYWORDS[node_id] if kw in text]
    assert hits, f"{node_id} carries no observable fluency target from {FLUENCY_TARGET_KEYWORDS[node_id]}"


def test_discrete_fluency_checkpoint_has_concrete_target():
    """The discrete [F] automaticity checkpoint (rf-121) gives a concrete,
    observable target (instant on sight, within about a second)."""
    text = _node_text(DISCRETE_FLUENCY_CHECKPOINT)
    assert "about a second" in text or "one second" in text, "rf-121 lacks a concrete instant-recognition target"
    assert "automatic" in text


def test_accuracy_node_has_95_percent_target():
    """rf-127 carries the concrete connected-text accuracy target (95 percent)."""
    text = _node_text("rf-127")
    assert "95 percent" in text, "rf-127 lacks the 95 percent accuracy target"


def test_first_fluency_node_bridges_decoding_automaticity():
    """The first connected-text/fluency node (rf-122) lists a decoding-automaticity
    node (rf-71) as a prerequisite; fluency is built on automatic decoding."""
    prereqs = set(EXPECTED_PREREQS[FIRST_FLUENCY_NODE])
    bridge = prereqs & DECODING_AUTOMATICITY
    assert bridge, f"{FIRST_FLUENCY_NODE} reaches no decoding-automaticity prerequisite: {sorted(prereqs)}"
    assert "rf-71" in prereqs
    # rf-125 also bridges to multisyllabic automaticity (rf-114).
    assert "rf-114" in set(EXPECTED_PREREQS["rf-125"])


# ── DECODING/FLUENCY IN SERVICE OF MEANING ───────────────────────────────


@pytest.mark.parametrize("node_id", MEANING_NODES)
def test_node_ties_reading_to_meaning(node_id):
    text = _node_text(node_id)
    assert "meaning" in text or "makes sense" in text or "understand" in text, (
        f"{node_id} does not tie reading to meaning"
    )


# ── Three-file integrity ─────────────────────────────────────────────────


def test_all_three_files_have_every_new_node():
    scope = _scope_by_ref()
    tnodes = _template_nodes()
    for n in NEW_NUMS:
        assert f"rf-{n}" in READING_FOUNDATIONAL_CONTENT, f"rf-{n} missing from content"
        assert f"read_f_{n}" in scope, f"read_f_{n} missing from scope_sequences"
        assert f"rf-{n}" in tnodes, f"rf-{n} missing from READING_FOUNDATIONAL template"


def test_counts_now_one_hundred_thirty():
    assert len(READING_FOUNDATIONAL_CONTENT) == 130
    assert len([t for t in get_scope_sequence("phonics_reading", "foundational")]) == 130
    assert len(READING_FOUNDATIONAL.nodes) == 130


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
            assert p in READING_FOUNDATIONAL_CONTENT, f"{node_id} prereq {p} not a real node"
            assert _num(p) < num, f"{node_id} prereq {p} is not earlier"


def test_template_edges_match_scope_prereqs_for_new_nodes():
    incoming: dict[str, set[str]] = {}
    for e in READING_FOUNDATIONAL.edges:
        incoming.setdefault(e.to_ref, set()).add(e.from_ref)
    for node_id, prereqs in EXPECTED_PREREQS.items():
        edges_in = incoming.get(node_id, set())
        assert edges_in == set(prereqs), f"{node_id} template edges {edges_in} != prereqs {set(prereqs)}"


# ── WHOLE-LIBRARY GRAPH-INTEGRITY GATE (scans rf-01..rf-130) ─────────────


def test_library_ids_are_contiguous_no_gaps_no_duplicates():
    keys = list(READING_FOUNDATIONAL_CONTENT.keys())
    nums = [_num(k) for k in keys]
    duplicates = sorted({n for n in nums if nums.count(n) > 1})
    assert not duplicates, f"duplicate rf ids: {sorted(duplicates)}"
    top = max(nums)
    expected = set(range(1, top + 1))
    missing = sorted(expected - set(nums))
    assert not missing, f"missing rf ids (gaps): {missing}"
    assert top == 130, f"library top should be rf-130, got rf-{top}"
    assert set(nums) == expected, f"id set is not exactly rf-01..rf-{top}"


def test_cross_file_count_parity():
    content_count = len(READING_FOUNDATIONAL_CONTENT)
    scope_count = len(
        [t for t in get_scope_sequence("phonics_reading", "foundational") if str(t["ref"]).startswith("read_f_")]
    )
    template_count = len({tn.ref for tn in READING_FOUNDATIONAL.nodes if str(tn.ref).startswith("rf-")})
    assert content_count == scope_count == template_count == 130, (
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
        referenced = {f"rf-{m}" for m in range(1, 131) if f"rf-{m}" in text}
        referenced |= {f"rf-{m:02d}" for m in range(1, 131) if f"rf-{m:02d}" in text}
        assert referenced, f"{node_id} spiral_review references no rf node"
        for r in referenced:
            rn = _num(r)
            if f"rf-{rn}" not in READING_FOUNDATIONAL_CONTENT and f"rf-{rn:02d}" not in READING_FOUNDATIONAL_CONTENT:
                unresolved.append(f"{node_id} -> {r} (missing)")
            elif rn >= num:
                unresolved.append(f"{node_id} -> {r} (not earlier)")
    assert not unresolved, f"unresolvable spiral references: {unresolved}"


# ── Resolver + generator gates (DB) ──────────────────────────────────────


@pytest.mark.parametrize("ref", NEW_REFS)
async def test_resolver_resolves_each_new_ref(db_session, household, ref):
    res = await resolve_ref_to_uuid(db_session, ref, household.id)
    assert res.node_uuid is not None, f"{ref} did not resolve to a UUID"
    assert res.unresolved is None


async def test_generator_plan_reading_tier_zero_needs_content(db_session, household):
    """needs_content drops by exactly 15: before this batch, 115 of the 130 reading
    refs resolved (rf-01..rf-115) and 15 were needs_content (rf-116..rf-130); now all
    130 resolve, so the full 130-topic plan has zero needs_content weeks and 130
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
    assert len(resolved_ids) == 130

    newly = 0
    for ref in NEW_REFS:
        res = await resolve_ref_to_uuid(db_session, ref, household.id)
        assert res.node_uuid is not None and res.unresolved is None, f"{ref} unresolved"
        newly += 1
    assert newly == 15
