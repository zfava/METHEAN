# METHEAN Node Authorship Contract

The canonical, file-grounded standard every new content node must satisfy.
Derived directly from the gold-standard node (`mf-01`), the real validator
(`node_content.py`), and the test that defines "valid" (`test_node_content.py`).
Transcribed from the files, not paraphrased.

Sources:
- `backend/app/content/math_foundational_content.py` — `mf-01` (the structural exemplar, lines 4–292)
- `backend/app/services/node_content.py` — `NODE_CONTENT_SCHEMA`, `validate_content`, `validate_philosophy`, `validate_media`, `validate_widgets`
- `backend/tests/test_node_content.py` — `NATIVE_KEYS`, `UNSCHOOLING_FORBIDDEN`, the authored-node assertions
- `backend/app/content/scope_sequences.py` — `math_f_01` (the scope-entry exemplar)
- `backend/app/services/templates.py` — `MATH_FOUNDATIONAL` `TemplateNode` / `TemplateEdge`

---

## 0. The hard gates (what the validator actually enforces)

Two functions in `node_content.py` are the only code that *rejects* content.
Everything else (`validate_media`, `validate_widgets`, and the `warning:` lines
of `validate_philosophy`) returns advisory warnings and **never raises / never
rejects**.

`validate_content(content) -> list[str]` flags exactly three missing fields:
```python
if not content.get("learning_objectives"): issues.append("learning_objectives missing")
if not content.get("teaching_guidance"):   issues.append("teaching_guidance missing")
if not content.get("assessment_criteria"): issues.append("assessment_criteria missing")
```
So **`learning_objectives`, `teaching_guidance`, `assessment_criteria` are the
machine-required minimum.** `is_enriched()` additionally treats a node as
"enriched" only when both `learning_objectives` and `teaching_guidance` are
truthy.

`validate_philosophy(content) -> list[str]` returns `warning:`-prefixed advisories
and `error:`-prefixed **hard failures**. The one hard failure for foundational
nodes is the unschooling forbidden-key rule (§2).

Everything beyond the three required fields is **not** machine-enforced but **is**
review-enforced against the exemplar (§6 depth floor, §7 traditional spine). A
node that passes `validate_content` but is materially thinner than `mf-01` fails
human review.

---

## 1. CONTENT NODE shape (`*_content.py`)

The dict keyed by `mf-NN` in the content module. Transcribed from `mf-01`. Every
key `mf-01` carries is listed; "required" = enforced by `validate_content`;
"exemplar / depth-floor" = not machine-checked but expected at `mf-01` depth and
checked at review.

```python
"mf-01": {
    "enriched": True,                       # exemplar: bool marker; is_enriched() keys off objectives+guidance
    "learning_objectives": [ ... ],         # REQUIRED (non-empty list of measurable objectives; mf-01 carries 4)

    "teaching_guidance": {                  # REQUIRED (non-empty)
        "introduction": "...",              # exemplar
        "scaffolding_sequence": [ ... ],    # exemplar (simple -> complex)
        "socratic_questions": [ ... ],      # exemplar (ask, don't tell)
        "practice_activities": [ ... ],     # exemplar
        "real_world_connections": [ ... ],  # exemplar
        "common_misconceptions": [ ... ],   # exemplar
    },

    "assessment_criteria": {                # REQUIRED (non-empty)
        "mastery_indicators": [ ... ],          # exemplar (observable mastery behaviors)
        "assessment_methods": [ ... ],          # exemplar (e.g. oral counting, object counting, numeral writing)
        "sample_assessment_prompts": [ ... ],   # exemplar
        # schema also documents optional proficiency_indicators / developing_indicators
    },

    "practice_items": [                     # exemplar / depth-floor (mf-01 carries 7, difficulty ramp 1 -> 3)
        {
            "type": "problem",              # problem-type label
            "difficulty": 1,                # int 1..3, ramped across the list
            "prompt": "...",                # the question
            "expected_type": "number",      # number | text | multiple_choice | true_false
            "correct_answer": "7",          # OPTIONAL — omitted on open/text items (see note)
            "hints": [ ... ],               # optional progressive hints
            "explanation": "...",           # optional worked explanation
            # "options": [ ... ]            # optional, only for multiple_choice
        },
        # ...
    ],
    # NOTE (transcribed from mf-01): difficulty ramps 1,1,2,2,2,3,3. Some items are
    # expected_type "text" with NO correct_answer (e.g. "Count backward from 12 to 7.
    # What numbers did you say?" and "Write the even numbers from 2 to 20.") — open
    # items carry hints + explanation but no machine-checkable answer. This is correct,
    # not an omission.

    "assessment_items": [                   # exemplar / depth-floor (mf-01 carries 5)
        {
            "prompt": "...",                # the assessment question
            "type": "number",              # number | multiple_choice | true_false | open_response (mf-01 uses number | text | open_response)
            "correct_answer": "15",         # answer-keyed items, OR ->
            "rubric": "Mastery: ... Proficient: ... Developing: ...",  # rubric-scored items (mutually used with type open_response/text)
            "target_concept": "counting_to_20",  # the concept the item assesses
        },
        # ...
    ],

    "resource_guidance": {                  # exemplar
        "required": [ ... ],                # never brand names, always types
        "recommended": [ ... ],
    },

    "time_estimates": {                     # exemplar (mf-01 uses these 3 keys)
        "first_exposure": 20,
        "practice_session": 15,
        "assessment": 10,
        # schema documents the wider set: first_exposure, practice_session,
        # review_session, estimated_sessions_to_mastery
    },

    "accommodations": {                     # exemplar — ALL SIX keys present, each a non-empty string
        "dyslexia": "...",
        "adhd": "...",
        "gifted": "...",
        "visual_learner": "...",
        "kinesthetic_learner": "...",
        "auditory_learner": "...",
    },

    "philosophy_specific": {                # see §2 — all five native variants required at review
        "traditional": { ... },
        "classical": { ... },
        "charlotte_mason": { ... },
        "montessori": { ... },
        "unschooling": { ... },
    },

    "connections": {                        # exemplar
        "reading": "...",
        "science": "...",
        "history": "...",
        # schema's generic connections shape also documents:
        # prerequisite_skills_from_other_subjects, feeds_into, parallel_topics
    },
}
```

Optional blocks the schema supports (use when the node needs them; flagged only
by advisory validators, never required): `media[]` (`alt` required per item, ids
unique), `passages[]` (`text` required per item, ids unique), `widgets[]` (`id`
+ `widget` required per item, ids unique, `params` must be a dict).

---

## 2. `philosophy_specific` — native-key requirements

`test_node_content.py::test_node_has_all_five_native_variants` asserts that every
authored reference node carries a `dict` variant for **all five** philosophies,
and that each variant contains **at least** its philosophy's `NATIVE_KEYS`. A
plain-string variant is legacy/valid-but-flagged (`warning:`), not acceptable for
new authoring. Transcribed EXACTLY from `NATIVE_KEYS` in the test:

### traditional (the spine — every key required)
```
introduction, gradual_release, guided_practice, independent_practice, mastery_check, spiral_review
```
`gradual_release` is itself `{ "i_do", "we_do", "you_do" }` (teacher models →
together → independent), per the schema and `mf-01`.

### classical (`copywork` is optional — omitted for oral / pre-print skills)
```
narrative_introduction, memory_work, recitation_routine, history_integration, read_aloud_suggestions
```
`memory_work` is `{ "chants", "recitations" }`.

### charlotte_mason (all seven required)
```
lesson_length_minutes, living_book_suggestions, short_lesson_flow, narration_prompt, real_world_objects, nature_connection, habit_focus
```

### montessori (all six required)
```
prepared_materials, presentation, control_of_error, abstraction_pathway, extensions, observation_focus
```
`presentation` is `{ "three_period_lesson", "steps" }`.

### unschooling (all six required)
```
invitations, real_world_contexts, conversation_starters, resource_bank, parent_role, observation_documentation
```

### THE UNSCHOOLING HARD-FAIL RULE

`validate_philosophy` **hard-fails** (returns an `error:` line) an unschooling
variant that carries ANY lesson / sequence / assessment key. Unschooling is
invitation and observation only — never a lesson, never a fixed sequence, never a
test. The forbidden set (`_UNSCHOOLING_FORBIDDEN_KEYS` in `node_content.py`,
mirrored by `UNSCHOOLING_FORBIDDEN` in the test) is exactly:
```
gradual_release, i_do, we_do, you_do, guided_practice, independent_practice,
mastery_check, spiral_review, scaffolding, assessment, lesson, sequence
```
If an unschooling variant's keys intersect that set, the node is rejected:
```
error: unschooling variant must not contain lesson, sequence, or assessment keys (found: ...)
```
`test_unschooling_variant_has_no_lesson_keys` asserts every authored node passes
this. Author unschooling variants from the native keys above and nothing from the
forbidden set.

---

## 3. SCOPE_SEQUENCES entry shape (`scope_sequences.py`)

The second file. One dict per topic inside
`SCOPE_SEQUENCES["mathematics"]["foundational"]`, in authored prerequisite order.
Transcribed verbatim from `math_f_01`:

```python
{
    "ref": "math_f_01",
    "title": "Counting to 20",
    "description": "Count objects to 20 with one-to-one correspondence. Recognize and write numerals 0 through 20, counting forward and backward from any number within 20.",
    "prerequisites": [],                    # list of other refs (e.g. ["math_f_01"]); empty only for the root
    "estimated_weeks": 2,
    "key_concepts": ["one-to-one correspondence", "numeral recognition", "counting sequence", "cardinality"],
    "assessment_indicators": ["Counts 20 objects accurately", "Writes numerals 0-20", "Counts backward from 20"],
    "classical_alignment": "Grammar stage: memorization of number sequence",
    "charlotte_mason_alignment": "Living math: counting real objects in nature and daily life",
    "standard_alignment": "K.CC.1-5",
}
```

The `ref` (`math_f_NN`) is the namespace twin of the content id (`mf-NN`); the
resolver maps them mechanically. `prerequisites` here is what the native generator
reads to order weeks. `key_concepts` and `estimated_weeks` feed the prompt/scope
block.

---

## 4. TEMPLATE NODE shape (`templates.py`)

The third file. Each node is a `TemplateNode`; prerequisites are expressed as
`TemplateEdge`s on the template. The dataclasses (transcribed):

```python
@dataclass
class TemplateNode:
    ref: str                          # the content/scope id, e.g. "mf-01" — this is how content + edges are wired
    node_type: str                    # e.g. "milestone" | "concept" | "skill"
    title: str
    description: str = ""
    estimated_minutes: int | None = None
    sort_order: int = 0
    content: dict | None = None        # inline content; usually None (content comes from *_content.py by ref)

@dataclass
class TemplateEdge:
    from_ref: str
    to_ref: str
    relation: str = "prerequisite"
```

`MATH_FOUNDATIONAL` node (positional args = `ref, node_type, title, description, estimated_minutes, sort_order`):
```python
TemplateNode("mf-01", "milestone", "Counting to 20",
             "Count objects to 20 with one-to-one correspondence. Recognize and write numerals 0-20.",
             20, 0),
```

Edge-wiring pattern — `prerequisite` edges run **from the prerequisite to the
dependent** (`from_ref` is taught before `to_ref`):
```python
edges=[
    TemplateEdge("mf-01", "mf-02"),                 # mf-01 is a prerequisite of mf-02
    TemplateEdge("mf-01", "mf-03"),
    TemplateEdge("mf-01", "mf-04", "prerequisite"),
    TemplateEdge("mf-02", "mf-04"),
    ...
]
```
The from-template persistence path deep-copies each `TemplateNode` into a
`LearningNode` (new UUID, `source_ref = tnode.ref`) and each `TemplateEdge` into a
`LearningEdge(from_node_id, to_node_id, relation)`. So a node's `scope_sequences`
`prerequisites` and its template `edges` must agree: every prerequisite `math_f_X`
of `math_f_Y` has a corresponding `TemplateEdge("X-ref", "Y-ref")`.

---

## 5. THE THREE-FILE RULE

Every authored node touches **three files**, and a node missing any one is
incomplete — it will not generate, resolve, or persist correctly:

1. **`*_content.py`** — the node dict (§1), keyed `mf-NN`. The teaching/assessment
   payload. Without it the resolver finds no content to inject.
2. **`scope_sequences.py`** — the `math_f_NN` entry (§3) with `prerequisites`.
   Without it the native generator cannot place the node in the week order (the
   ref never appears in the scope block, so it is never scheduled).
3. **`templates.py`** — the `TemplateNode` + its `TemplateEdge`s (§4). Without it
   `resolve_content_id_to_uuid` finds no owning template, returns an `Unresolved`
   record (`reason="no_template"`), and the generator emits the ref as a
   `needs_content` placeholder (no UUID, no persisted node).

Author all three together, in prerequisite order, with the ref/`mf-NN` consistent
across all three and the prerequisites consistent between (2) and (3).

---

## 6. DEPTH FLOOR

`mf-01` spans **~289 lines** (lines 4–292 of `math_foundational_content.py`). That
is the depth expectation for a foundational node. Concretely, `mf-01` carries:
**4 learning objectives; 6 teaching_guidance sub-blocks; 3 assessment_criteria
sub-blocks; 7 practice_items ramped difficulty 1→3 (with open `text` items);
5 assessment_items (answer-keyed and rubric-scored); all 6 accommodations; all 5
philosophy variants in full native shape; reading/science/history connections.**

A node materially thinner than the exemplar — a stub philosophy variant, two
practice items instead of a ramped set, missing assessment_items, only some
accommodations — **fails review**, even though it may pass `validate_content`
(which only checks the three required fields). The validator is the floor of
machine-checkable structure; the exemplar is the floor of authored depth.

---

## 7. TRADITIONAL SPINE NON-NEGOTIABLES

Traditional is the spine (it is the only philosophy whose every native key is
required, and it is the default tier the native generator uses). Its variant must
embody **explicit, direct instruction**, not discovery:

1. **Direct instruction, not discovery.** `gradual_release` runs `i_do` (teacher
   models the skill explicitly) → `we_do` (teacher and child together) → `you_do`
   (child independent). The skill is taught and modeled, never left to be
   discovered. (Contrast: montessori `control_of_error`, unschooling `invitations`
   — those belong to *their* variants, never the traditional one.)
2. **Mastery threshold stated before advancement.** `mastery_check` must list the
   observable checks that gate moving on (e.g. mf-01: "Count 18 objects with
   one-to-one correspondence", "Write 0 to 20 from memory", "Count backward from
   14"). State the bar; do not advance until it is met.
3. **Daily `spiral_review` referencing prior work.** `spiral_review` must revisit
   at least one earlier skill to confirm retention, and for any non-root node it
   should reference a prior `mf-NN` by its skill so the spiral is concrete. (`mf-01`
   is the root and has no prior node, so its `spiral_review` references the
   precursor sub-skill — "Re-count within 10 to confirm retention before extending
   to 20." Every later node should name a real prior node's skill.)
4. **Accurate, sequenced prerequisites.** The `scope_sequences` `prerequisites`
   and the template `edges` must reflect the true teaching order (e.g. subtraction
   facts after the addition facts they invert; place value before two-digit
   computation). Prerequisites are load-bearing — the generator orders the year by
   them and the resolver wires them into the DAG.

---

## 8. OPTIONAL `choice_space` — governed agency (PARENT-FINAL child choice)

`choice_space` is an **optional** node block that bounds what a child may
**propose**. It is the schema half of "governed agency": child choice
mirrors the existing parent-adjustable AI input/oversight dial, the same
governance primitive with a different actor. Three roles:

- **CHILD PROPOSES** within a bounded set of all-acceptable options
  (`proposable[]`), never an open field.
- **SYSTEM INFORMS**: each proposal and its resolution is captured as an
  immutable governance event (event type `child_choice_proposal`) carrying
  child / node / option / outcome / timestamp. A future readiness service
  will derive a per-child, per-class signal from that history. The
  inference is a later phase; only the event hooks are laid now.
- **PARENT APPROVES**: final authority always, via the existing governance
  queue. The parent can grant standing approval for a choice class (`auto`)
  or require per-instance review (`review`), and can `disable` a class
  entirely.

### The absent-means-parent-directed default (why existing nodes stay valid)

When `choice_space` is **absent**, the node is **fully parent-directed**: the
child proposes nothing and the node behaves exactly as before. This is the
safe default. `validate_choice_space(content)` returns `[]` for any content
without a `choice_space`, so all 182 existing foundational nodes (157 `mf` +
25 `rf`) stay valid unchanged. `validate_content` and `validate_philosophy`
are not touched by this feature.

### Shape (when present)

```python
"choice_space": {
    "proposable": [                       # the bounded, all-acceptable options
        {
            "class": "order",             # one of: order | practice_path |
                                          #   practice_variant | pacing_within_bounds
            "option": "addition_first",   # stable id/label of this option
            "label": "Do addition before subtraction",  # optional, human-readable
        },
        # ... every option here must be acceptable REGARDLESS of which the child picks
    ],
    "excluded_note": (                    # REQUIRED explicit statement
        "Consequential decisions (prerequisite-skip, mastery-declaration, "
        "subject-exit) are not in scope and never child-proposable."
    ),
    "author_default_latitude": "auto",    # 'auto' (low-stakes) or 'review' (higher-stakes);
                                          # may be a per-class dict; the parent can override per class
}
```

### The two hard rules the validator enforces (`validate_choice_space`)

1. **Every option in `proposable[]` must be an acceptable outcome.** The
   author asserts that whichever the child picks is fine. Bounded set, never
   an open field.
2. **No consequential decision is ever proposable.** Skipping a
   prerequisite, declaring mastery, and leaving a subject are NEVER in a
   `choice_space`. The validator **rejects** (an `error:` line) any
   `proposable` entry that names one of these by class or by option, and
   `excluded_note` must be present to state the exclusion explicitly.

Like the other validators, `validate_choice_space` never raises: `error:`
lines are hard failures the pipeline must not ship; `warning:` lines (an
unknown class, an out-of-range `author_default_latitude`, an empty
`proposable`) are advisory. `choice_space_is_valid(content)` is the boolean
the runtime path consults before honoring a proposal.

### Parent latitude (mirrors the AI oversight dial) and routing

The parent tunes child-choice latitude **per child** via a JSONB key,
`ChildPreferences.personalization['child_choice_latitude']`, a dict mapping
choice class to `auto` | `review` | `disabled`. This reuses the same
mechanism as the AI dial (which lives in
`Household.philosophical_profile['ai_autonomy_level']`); no parallel
mechanism is introduced. Resolution (`app/services/child_choice.py`):

- parent value for the class WINS (WIDEN -> `auto`, TIGHTEN -> `review`,
  DISABLE -> `disabled`);
- unset -> the node's `author_default_latitude`;
- otherwise -> the safe default `review`.

A child proposal routes through `propose_child_choice`, which writes one
immutable `child_choice_proposal` governance event:

- `auto` -> applied immediately (action `approve`);
- `review` -> queued for the parent (action `defer`); the child sees
  "waiting for approval" and **no learning state changes** until approved;
- `disabled` -> rejected (action `reject`); proposability removed for that
  class regardless of the author default.

The parent's decision on a queued proposal is recorded by
`resolve_pending_choice` as a second immutable event (`approve` / `reject`),
linked to the proposal. The governance core and its existing event types are
unchanged; this is additive (a new `target_type` string only).

## Authoring checklist

- [ ] `*_content.py` node dict added, keyed `mf-NN`, at `mf-01` depth (§1, §6).
- [ ] `learning_objectives`, `teaching_guidance`, `assessment_criteria` all present and non-empty (passes `validate_content`).
- [ ] All five `philosophy_specific` variants present as dicts, each carrying its full `NATIVE_KEYS` (§2).
- [ ] unschooling variant carries **none** of the forbidden lesson/sequence/assessment keys (§2).
- [ ] All six `accommodations` filled.
- [ ] `practice_items` ramped 1→3; open `text` items may omit `correct_answer`.
- [ ] `assessment_items` present, answer-keyed and/or rubric-scored, with `target_concept`.
- [ ] `scope_sequences.py` `math_f_NN` entry added with accurate `prerequisites` (§3).
- [ ] `templates.py` `TemplateNode` + `TemplateEdge`s added, edges agreeing with scope prerequisites (§4).
- [ ] Traditional variant is direct-instruction, states a mastery threshold, and spirals to prior work (§7).
- [ ] (Optional) If the node offers child choice, `choice_space` lists only all-acceptable options, names no consequential decision, and carries `excluded_note` (§8). Absent is fine: the node is then fully parent-directed.
