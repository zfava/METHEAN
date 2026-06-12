# On-screen "0 nodes" investigation (Part B)

Date: 2026-06-12
Symptom: a parent (household "Fava Family", child "Greyson Fava") used
"Build from Philosophy" with `educational_philosophy=classical` and the screen
read "Mathematics with 0 nodes", although Phase 0
(`docs/philosophy_resolution_audit.md`) proved the generator returns 157
Mathematics nodes for classical.

## TL;DR

The on-screen "0 nodes" is a **frontend display defect**, not an empty plan and
not a generator/persistence fault. It is produced at a single line:

- `frontend/src/app/(parent)/curriculum/page.tsx:441`

```tsx
{proposal?.material_name || selectedSubject?.s || "Your curriculum"} with{" "}
{proposal?.nodes?.length || 0} nodes is now active for {selectedChild.first_name}.
```

For the "Build from Philosophy" path, `proposal` is the annual-curriculum
generate response, whose shape is `{id, status, subject}` with **no `nodes`
field** (`backend/app/api/annual_curriculum.py:152`). So
`proposal?.nodes?.length` is `undefined`, the `|| 0` renders **0**, and
`selectedSubject?.s` renders "Mathematics". The card therefore reads
"Mathematics with 0 nodes" for **every** philosophy and **every** subject on
this path, including traditional. The number is hardcoded-to-zero by the
missing field; it never reflects what was actually generated or materialized.

The actual year plan is correct. The same curriculum, opened at
`/curriculum/year?id=...`, reads `curriculum.scope_sequence.weeks` and renders
its full set of weeks (`frontend/src/app/(parent)/curriculum/year/page.tsx:150,
189, 196`). Nothing downstream is empty.

This is fully consistent with Phase 0: philosophy is innocent, the generator is
innocent, the empty is downstream, and it is a presentation artifact.

## 1. The real "Build from Philosophy" path, end to end

1. UI action: `generateFromPhilosophy()`
   (`frontend/src/app/(parent)/curriculum/page.tsx:117-139`) calls
   `annualCurriculum.generate(childId, { subject_name, academic_year,
   hours_per_week, total_weeks, scope_notes, content_tier? })`.
2. API client: `frontend/src/lib/api.ts:1306-1307`
   `POST /children/{childId}/curricula/generate`.
3. Route: `backend/app/api/annual_curriculum.py:120-152` `generate_curriculum`
   -> `generate_annual_curriculum(...)`.
4. Service: `backend/app/services/annual_curriculum.py:114-329`
   `generate_annual_curriculum` builds the prompt and calls `call_ai`
   (`annual_curriculum.py:284-293`).
5. Gateway: `backend/app/ai/gateway.py:236+` `call_ai` runs the provider chain
   Claude -> OpenAI -> Native -> Mock. With AI keys blank the **native**
   provider answers (`gateway.py:416-428` -> `build_native_response`). This is
   exactly the path Phase 0 measured at 157 nodes for classical.
6. The route returns `{"id", "status", "subject"}`
   (`annual_curriculum.py:152`). The frontend stores it as `proposal`
   (`page.tsx:134`).
7. Approve: `approveProposal()` (`page.tsx:153-162`) calls
   `annualCurriculum.approve(proposal.id)` -> materialize. Then the
   confirmation card (`page.tsx:434-454`) renders, and line 441 prints the
   "0 nodes" string.

The proposal-review card just above (`page.tsx:404-406`) already branches on
shape: when `proposal.id` is present (the annual path) it shows
`Status: ... Approving will create a full year of activities.` and does **not**
show a node count. Only the post-approval confirmation card (line 441) forgets
to branch and reaches for `proposal.nodes`, a field that only the learning-map
proposal shape carries (the map shape is rendered at `page.tsx:406, 410-419`,
where `proposal.nodes` is a real array).

## 2. Where the count becomes 0 (and where it does not)

- It becomes 0 at `frontend/src/app/(parent)/curriculum/page.tsx:441`, because
  the annual generate response has no `nodes` field and `|| 0` supplies the
  zero. This is the on-screen number.
- It does NOT become 0 in the generator: Phase 0 measured 157 (math) and 155
  (reading) for classical and every other philosophy.
- It does NOT become 0 in materialization: `materialize_full_year`
  (`annual_curriculum.py:387-547`) writes the full weeks and activities; the
  year-plan view renders them.
- The backend generate response simply does not carry any count to display
  (`annual_curriculum.py:152`), so even a shape-aware frontend currently has no
  node or week number to show on this path without an extra read.

Ruling on the candidate downstream causes the brief listed:

- (a) different generator/service than Phase 0 tested - RULED OUT. The path is
  `generate_annual_curriculum` -> `call_ai` -> native, the same one Phase 0
  drove.
- (b) focus_nodes fail to resolve to UUIDs at persist time - NOT the on-screen
  cause. For `foundational`, math resolves all 157 to real UUIDs (Phase 0). See
  section 4 for the one case where focus_nodes are legitimately empty (a
  separate tier/template gap), which still does not change the line-441 text.
- (c) read-back endpoint filters by grade/level/age - RULED OUT for the
  symptom. The confirmation card does not read back; it prints from the stale
  `proposal` object. The year-plan read-back renders all weeks.
- (d) plan created against stale/pre-entitlement DB state - RULED OUT. Phase 0
  generated cleanly against a fresh DB; the route is entitlement-gated
  (`annual_curriculum.py:127`) and returns a normal draft.
- (e) the annual (AI-keyed) service returns empty when keys are blank - RULED
  OUT. With keys blank the native provider answers and returns a full plan
  (Phase 0). The service is not a separate empty-returning path.

## 3. Does Build-from-Philosophy use the native generator or an AI-keyed path?

It uses `generate_annual_curriculum`, which delegates to the gateway provider
chain. With AI keys blank, the deterministic **native** generator answers
(`gateway.py:416-428`). With keys present, Claude or OpenAI answers and may
return a different JSON shape, but that is a separate provider-shape concern and
is not what produces this symptom: line 441 prints 0 regardless of which
provider filled the plan, because the count it reads was never in the response.
Confirmed: the generation service is innocent; the symptom is in the
confirmation render.

## 4. Greyson's profile and the tier gap (separate, latent, still not the
on-screen cause)

Greyson's specific DB row is not queryable from this environment, but the path
is deterministic enough to reason about. The frontend sends `content_tier` only
when the tier picker has a value for the subject
(`page.tsx:125, 132`: `content_tier = subjectLevels[selectedSubject.id]`). When
it is omitted, the backend resolves the level from the child's preferences and
**defaults to `developing`** (`backend/app/core/learning_levels.py:230-241`,
`backend/app/services/annual_curriculum.py:169-175`).

Only `foundational` math (and `foundational` reading) resolve to real node
UUIDs today; `developing` math maps to `md-NN` content ids that have no wired
template, so `resolve_ref_to_uuid` returns `needs_content` and the plan's
`focus_nodes` are genuinely empty for every week (the 36 weeks still
materialize with consolidation activities). This is the same template-wiring
gap catalogued in the Phase 0 audit, and it is philosophy-independent.

Two important clarifications:

- This tier gap can make `focus_nodes` legitimately empty for a non-foundational
  tier, but it does **not** produce the literal "0 nodes" confirmation string.
  That string is hardcoded-to-zero by the missing `nodes` field at line 441 and
  shows 0 even when `foundational` generated 157 real nodes.
- So even if Greyson generated at `foundational` (157 real nodes) the screen
  still reads "0 nodes". The tier gap is a real but separate concern; it is not
  the explanation for the reported text.

## Minimal fix (proposed, not implemented this run)

Primary (frontend, the on-screen text):
`frontend/src/app/(parent)/curriculum/page.tsx:441`. Make the confirmation card
branch on proposal shape exactly as the review card at lines 404-406 already
does. For the annual path (`proposal.id` present), stop reading
`proposal.nodes?.length`; show a meaningful annual message (for example
"... is now active" or a week count) rather than a node count that does not
exist on this shape. Leave the node-count rendering for the map-proposal shape
(`proposal.nodes` present) unchanged.

Optional supporting backend change so the confirmation can show a real number:
have `generate_curriculum` (`backend/app/api/annual_curriculum.py:152`) and/or
the approve response include `total_weeks` (and, if desired, a count of
resolved focus nodes / activities created by `materialize_full_year`, which
already computes `weeks_created` and `activities_created` at
`annual_curriculum.py:543-547`). Then line 441 can display "N weeks" /
"N activities" instead of a node count.

Out of scope here (separate task): wiring templates for non-foundational tiers
and for science / history / writing so those subjects/tiers resolve to real
node UUIDs. Already flagged in the Phase 0 audit.

## Conclusion

The exact file:line where the displayed node count becomes 0 on the real UI
path is `frontend/src/app/(parent)/curriculum/page.tsx:441`, driven by the
annual-curriculum generate response shape
(`backend/app/api/annual_curriculum.py:152`) carrying no `nodes` field. The
generator and materialization are proven correct and are not involved. The
minimal fix is a shape-aware confirmation card (frontend), optionally backed by
a count field added to the generate/approve response (backend). Per the Part B
instruction, the fix is reported, not implemented, in this run.
