# Philosophy resolution audit (Phase 0)

Date: 2026-06-12
Scope: confirm the root cause of the reported defect "generating a curriculum
for a household whose `educational_philosophy` is anything other than
`traditional` yields an empty plan (Mathematics with 0 nodes)" before writing
any fix.

## TL;DR (STOP-gate result)

The reported defect **does not reproduce**. Philosophy has **zero** effect on
which nodes a plan contains. Measured directly against a live database, every
philosophy value (including `custom` and a nonsense string) produces the
**identical** node set and count as `traditional`, for every generatable
subject:

| subject (foundational) | traditional | classical | charlotte_mason | montessori | unschooling | eclectic | custom | nonsense_xyz |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Mathematics | 157 | 157 | 157 | 157 | 157 | 157 | 157 | 157 |
| Phonics & Reading | 155 | 155 | 155 | 155 | 155 | 155 | 155 | 155 |

The core invariant the Phase 1 design asks us to establish ("a plan generated
for any philosophy contains the same node count and id set as the same
subject+tier generated for traditional") is **already true in the current
code**. None of the candidate causes (a), (b), (c), (d) is occurring.

Per the Phase 0 STOP gate ("If the confirmed cause differs materially from
candidates (a)-(d), STOP and report rather than forcing the Phase 1 design"),
no fix is written. The remainder of this document is the evidence.

## How this was measured

A throwaway parametrized test drove the real generation path
(`generate_annual_curriculum` -> `call_ai` -> native provider) against a live
Postgres test database with `AI_API_KEY=""`, `AI_FALLBACK_API_KEY=""`,
`AI_MOCK_ENABLED=False` (so only the deterministic native generator can
answer), setting `household.philosophical_profile = {"educational_philosophy":
<value>}` for each of eight philosophy values and counting the distinct
`focus_nodes` UUIDs in the resulting `scope_sequence["weeks"]`. The numbers in
the table above are that count. The throwaway test was removed after
measurement.

## 1. Where `educational_philosophy` enters generation, and where it stops

Trace from the household profile to node selection:

1. `backend/app/services/annual_curriculum.py:140`
   `phil = household.philosophical_profile or {}` reads the profile.
2. `backend/app/services/annual_curriculum.py:206`
   `phil_constraints = build_philosophical_constraints(phil)`. This text is
   injected into the **system** prompt only
   (`annual_curriculum.py:255-258`), and again appended to the system prompt
   in `backend/app/ai/gateway.py:344-346`.
3. The **user** prompt (`annual_curriculum.py:260-282`) carries the subject,
   level, time budget, and the scope-and-sequence block
   (`annual_curriculum.py:208-234`). It contains **no philosophy token**.
4. `backend/app/ai/gateway.py:422`
   `build_native_response(db, household_id, role, user_prompt, philosophical_profile)`.
5. `backend/app/services/native_curriculum_generator.py:320`
   `philosophy=philosophy_key(philosophical_profile)`.
6. `native_curriculum_generator.py:74-79` `philosophy_key` returns the key if
   it is in `PHILOSOPHY_BLOCKS`, else `DEFAULT_PHILOSOPHY` ("traditional").
   This is already a **total fallback**: any unknown value becomes traditional.
7. `native_curriculum_generator.py:183`
   `block = PHILOSOPHY_BLOCKS.get(philosophy, PHILOSOPHY_BLOCKS[DEFAULT_PHILOSOPHY])`.
   Philosophy selects only a `{framing, verb}` text block used to phrase
   activity titles/descriptions (`_build_activities`, lines 126-154).

Where philosophy **stops**: `focus_nodes` are built at
`native_curriculum_generator.py:193-200` purely from
`resolve_ref_to_uuid(db, topic.ref, household_id)`. The `topic` list comes
from `topics_for_subject` (lines 82-102) which reads
`get_scope_sequence(subject_id, level)`. Philosophy is never consulted in node
selection. This is why the counts are identical above.

## 2. Is SCOPE_SEQUENCES keyed by philosophy? No, subject+level only

`backend/app/content/scope_sequences.py:6-7`:

```python
def get_scope_sequence(subject_id: str, level: str) -> list[dict]:
    return SCOPE_SEQUENCES.get(subject_id, {}).get(level, [])
```

The key structure is `SCOPE_SEQUENCES[subject_id][level] -> list[topic dict]`
(for example `SCOPE_SEQUENCES["mathematics"]["foundational"]` at
`scope_sequences.py:28-29`). Philosophy is not part of the key at any level.

CRUX confirmed: scope selection is subject+level only, so philosophy
**cannot** zero out the node set. Any empty result must originate elsewhere,
and as section 6 shows, the only empties are subject-driven (template/content
gaps) and identical across all philosophies including traditional.

## 3. Actual cause of "0 nodes" for classical: none; all candidates ruled out

There is no classical-specific empty. Classical Mathematics resolves 157
nodes, identical to traditional. Each candidate, ruled out with evidence:

- **(a) generation keys the scope lookup on philosophy** - RULED OUT. The only
  scope lookup is `get_scope_sequence(subject_id, level)`
  (`scope_sequences.py:7`, called from `native_curriculum_generator.py:89`).
  No philosophy argument exists. Measured: classical math = 157 = traditional.

- **(b) a philosophy-variant lookup returns empty and is treated as
  empty-node** - RULED OUT. The native generator performs no per-node
  `philosophy_specific` lookup at all (see section 4). The only such lookup is
  at the kid surface, `backend/app/services/learning_context.py:387-393`, and
  it already retains the node when the variant is absent (it sets
  `content: variant or None`, it does not drop the activity).

- **(c) the API/service empties or rejects the plan when philosophy !=
  traditional** - RULED OUT. The route
  `backend/app/api/annual_curriculum.py:120-152` (`generate_curriculum`) passes
  no philosophy filter and applies no philosophy gate; it forwards to
  `generate_annual_curriculum`. Measured: classical generates a full plan.

- **(d) materialization drops nodes whose `philosophy_specific[philosophy]`
  block is absent** - RULED OUT. `materialize_full_year`
  (`annual_curriculum.py:387-547`) reads only `weeks[].focus_nodes`,
  `weeks[].suggested_activities`, and `weeks[].assessment_focus`. It never
  inspects `philosophy_specific`. Its `MaterializationError` guard
  (`annual_curriculum.py:396-419, 446-454`) fires only on a zero-weeks or
  zero-activities shape, which is shape-driven, not philosophy-driven.

The only "0 nodes" outcomes observed are **subject-driven and identical across
all philosophies including traditional** (section 6).

## 4. Current per-node philosophy fallback in the generator

The transcript's description ("philosophy selects the `philosophy_specific`
block, falls back to traditional when absent") is **not** what the native
generator does. The generator carries a hardcoded framing table:

`native_curriculum_generator.py:63-71`:

```python
PHILOSOPHY_BLOCKS: dict[str, dict[str, str]] = {
    "classical": {"framing": "...", "verb": "Recite and master"},
    ...
    "eclectic": {"framing": "mixed methods", "verb": "Practice"},
    "traditional": {"framing": "structured textbook lessons", "verb": "Study"},
}
DEFAULT_PHILOSOPHY = "traditional"
```

All six keys are present, and selection is a total `.get(philosophy, default)`
at line 183. There is no `philosophy_specific` content read here.

The real per-node `philosophy_specific` selection lives at the kid surface,
`learning_context.py:387-393`:

```python
phil_specific = content.get("philosophy_specific", {})
variant = phil_specific.get(chosen) if isinstance(phil_specific, dict) else None
context["philosophy"] = {
    "approach": chosen,
    "content": variant or None,
    "is_native": variant is not None,
}
```

When the requested philosophy's variant is absent, `content` is `None` and the
child keeps the neutral teaching content; the node/activity is **not dropped**.
This is the existing unschooling-safe behavior: an unschooling plan still
materializes every node, and where an unschooling variant is absent the child
simply sees neutral content. Nothing synthesizes a lesson into an unschooling
variant, so `validate_philosophy` (`node_content.py:520-558`) is never put at
risk by this path.

## 5. eclectic and custom

- `eclectic` IS a known key in `PHILOSOPHY_BLOCKS`
  (`native_curriculum_generator.py:68`), so it gets its own framing and
  resolves cleanly. At the kid surface it maps to traditional content with an
  optional per-subject override (`learning_context.py:130, 371-385`). Measured:
  eclectic math = 157 = traditional.
- `custom` is NOT in `PHILOSOPHY_BLOCKS`, so `philosophy_key`
  (`native_curriculum_generator.py:79`) returns `DEFAULT_PHILOSOPHY`. Measured:
  custom math = 157 = traditional.
- A nonsense value behaves identically (falls back to traditional). Measured:
  nonsense_xyz math = 157 = traditional.

The total fallback the Phase 1 design asks for ("any philosophy value not
explicitly handled resolves to traditional, never to empty") is already in
place at both the generator (`:79`, `:183`) and the surface
(`learning_context.py:130, 372-373`).

## 6. Subject enumeration (what is generatable today)

Measured for the foundational tier with the native provider:

GENERATABLE (refs resolve to real persisted UUIDs for traditional, and
identically for every other philosophy):

- `mathematics` / `foundational`: 157 nodes (template `math-foundational`,
  refs `math_f_NN` -> content `mf-NN`).
- `phonics_reading` / `foundational` (subject name "Phonics & Reading"): 155
  nodes (refs `read_f_NN` -> content `rf-NN`).

NOT generatable for anyone (authored scope but no wired template; resolver
returns `needs_content` for all philosophies including traditional). These are
template-wiring gaps, explicitly out of scope for the philosophy task and
flagged here as a separate task:

- `science` / `foundational`: 0 nodes, 12 needs_content weeks (refs
  `sci_f_NN` -> `sf-NN`, no template owns `sf-NN`).
- `history` / `foundational`: 0 nodes, 12 needs_content weeks.
- `writing_grammar` / `foundational` (name "Writing & Grammar"): 0 nodes, 12
  needs_content weeks (refs `writ_f_NN` -> `wf-NN`, no template).
- `literature` / `foundational`: no foundational level exists at all
  (`SCOPE_SEQUENCES["literature"]` has only intermediate/advanced/mastery), so
  the scope block is empty, `parse_prompt` returns `None`, the native provider
  declines, and the call raises `AIProviderUnavailableError`. The literature
  strand also uses the non-mechanical `lit-craft-NNN` namespace the resolver
  deliberately returns `None` for (`node_resolver.py:88-99`). Out of scope.

All of the empties above are identical across all eight philosophies, which is
the proof that philosophy is not the variable.

## Conclusion and fix location

The defect as described (classical/non-traditional yields 0 nodes) is not
present. Philosophy never participates in node selection; the node set is
already identical across all philosophies for every generatable subject, and
the unmapped-philosophy total fallback already resolves to traditional. There
is no node-selection code to sever and no empty result to fall back from.

If the symptom is ever observed in production, the only places that could
introduce a philosophy-driven divergence are:

- node selection: `native_curriculum_generator.py:193-200` (currently
  philosophy-free; would be the fix site if a filter were ever added);
- variant surfacing: `learning_context.py:387-393` (currently node-retaining;
  would be the fix site if a future change started dropping nodes on a missing
  variant).

Optional, non-defect hardening that aligns with the Phase 1 intent without
changing any node-selection behavior:

- a regression test (`backend/tests/test_philosophy_resolution.py`) that
  asserts the identical-node-set invariant across the six UI philosophies for
  each generatable subject, locking the current correct behavior against future
  regression;
- a structured info/governance log when the surface falls back from a
  requested philosophy variant to neutral/traditional content, for
  transparency.

These are proposed, not implemented, pending direction, because the Phase 0
STOP gate forbids forcing the Phase 1 design when the confirmed cause differs
from the candidates.
