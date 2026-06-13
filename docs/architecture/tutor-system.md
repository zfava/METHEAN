# The METHEAN Tutor System

This is the consolidated design of the parent governed AI tutor: the four
context layers that shape how it speaks, the single writer choke points that
keep its memory honest, the autonomy spectrum that keeps the parent in
control, the privacy rules that are structural rather than aspirational, the
order in which the tutor's context is assembled, and the governance event
that every parent control emits.

It is written to be handed to a technical diligence team. Everything below is
enforced by code and by the permanent quality harness in
`backend/tests/tutor_harness/`.

## 1. The four context layers

The tutor never speaks from a blank prompt. Four layers feed its context,
each one governed, each one able to be off. The harness proves that every
combination of their states produces a correct, complete, bounded, and clean
context.

### 1a. Developmental voice register (`app/services/tutor_register.py`)

What it is: per tier voice guidance (sentence length, abstraction, tone, how
much independence to grant) injected into every live tutor context, telling
the model how to speak to this learner right now.

Reads: the child's content tier for the subject being tutored
(`ChildPreferences.subject_levels`, the canonical
`app.core.learning_levels.LEARNING_LEVELS` ordering: foundational, developing,
intermediate, advanced, mastery), and the absolute per child parent override
(`ChildTutorPreferences.register_override`).

Writes: nothing. The register is presentation, not memory.

Fail closed: an unresolved tier falls back to the most protective (youngest)
register, never a silently richer one. The only gate is the tutor role being
off.

### 1b. Relationship milestones (`app/services/tutor_milestones.py`)

What it is: the journey so far ("long division was hard for weeks, and then it
clicked"), so the tutor speaks like someone who remembers how far the learner
has come.

Reads: existing mastery, attempt, curriculum, and streak records only.
Breakthroughs (a struggle of fourteen or more days, or five or more attempts,
before reaching the bar), curriculum completions, notable streaks, and firsts.

Writes: nothing. Milestones are DERIVED at assembly time, capped at three,
ranked most meaningful first, and cached in Redis for speed (24 hour TTL,
invalidated immediately when the parent toggles the layer). The module
performs zero database writes, enforced by a guard test.

Opt in: strictly off by default. Nothing is derived, queried, or injected
unless `ChildTutorPreferences.relationship_memory` is on.

### 1c. Parent governed profile memory (`app/services/tutor_profile.py`)

What it is: abstracted teaching strategies the tutor has learned work for this
child (how to explain, what motivates, what pace, what interests), injected as
the "what works for this learner" block.

Reads: only `status == "active"` entries (parent approved, or applied under a
standing grant). Proposed, rejected, retired, and revoked entries are never
injected.

Writes: `TutorProfileEntry` rows, through this module only (see the choke
points below).

### 1d. Live session signal (`app/services/tutor_session_signals.py`)

What it is: the learner's right now state in a single sitting (cruising,
stretching, struggling, frustrated) plus concrete pedagogical directives, so
the tutor adapts within a session, not only between sessions.

Reads: a rolling Redis window of recent attempt outcomes. The classifier is
deterministic arithmetic over that window, with zero AI calls.

Writes: nothing durable. The window lives in Redis under a short TTL and is
never persisted. This module imports no ORM models. Its one possible durable
artifact is an ordinary `session_pattern` profile proposal, produced only by
delegating to `tutor_profile.route_proposal`, which routes it under the
parent's policy exactly like every other proposal.

## 2. Single writer choke points

Each kind of durable truth has exactly one writer, mirroring the
`log_governance_event` pattern and covered by guard tests. This is what makes
the tutor auditable.

| Truth | Single writer | Guarantee |
| --- | --- | --- |
| `TutorProfileEntry` rows (entry creation) | `tutor_profile.py` | The tutor reads the profile through context assembly; it can never write it directly. Every write runs the privacy validator and the autonomy routing. |
| `TutorEntryObservation` rows and entry efficacy fields | `tutor_efficacy.py` | The efficacy engine mutates entry status for a retirement it proposed, but never constructs an entry, so the creation writer guard still holds. |
| `GovernanceEvent` hash chain | `governance.log_governance_event` | Every parent control and every autonomous action is a sealed, hash chained event. |
| Session signal window | `tutor_session_signals.py` (Redis only) | Imports no ORM; never adds a row. |
| Milestones | none (derived) | `tutor_milestones.py` performs zero database writes. |

## 3. The autonomy spectrum and standing grants

The parent sets each AI role's autonomy. Only the tutor is autonomy capable
today, because the tutor profile system is the only consumer of a standing
grant (`governance.ALLOWED_AUTONOMY`).

- **off**: the role makes no AI calls at all. The gateway raises
  `AIRoleDisabledError` before any provider work, and every context layer
  short circuits to empty before assembly. The features it powers show a kind
  unavailable state.
- **standard** (the default): the AI advises. Every proposed entry waits for
  the parent's approval before it can influence the tutor.
- **autonomous**: a standing grant. The tutor may apply its specific, named
  adjustments without per item approval. Every autonomous write cites the hash
  of the `ai_autonomy_granted` event in force at application time
  (`TutorProfileEntry.grant_event_hash`), so every action is traceable to the
  exact parent decision that authorized it. One tap revokes the grant.

Fail closed throughout: if the policy cannot be read, or the standing grant
cannot be resolved while autonomous, the proposal is dropped and logged, never
auto applied. Returning a child's policy to standard or off leaves any entries
already applied under the former grant active (the record is the record); it
is the grant that is revoked, not the history.

## 4. Privacy rules (structural, not aspirational)

- **Ephemeral signals are ephemeral by construction.** The session signal
  lives only in Redis under a two hour TTL, is never persisted, is never shown
  to the child, and is read only at context assembly time. The module imports
  no ORM models, so it physically cannot write a row.
- **Milestones are derived, never stored.** They are a computed lens over the
  hash chained record, discarded freely. The dignity rule is absolute:
  milestones celebrate persistence and breakthrough and never recall failure
  as failure. No template prints a raw count of failures or attempts; struggle
  is spoken in weeks of effort and in showing up.
- **Transcript and voice derived memory is forbidden.** Milestones derive only
  from mastery, attempt, curriculum, and streak records.
- **Profile entries are abstracted strategies, never speech.** The validator
  in `tutor_profile.py` rejects, on every write path regardless of autonomy:
  quotation marks (the signature of verbatim child speech), clinical and
  diagnostic vocabulary (a deliberately broad denylist; METHEAN is not
  qualified to keep a medical chart), empty content, content over 300
  characters, and unknown categories.
- **The assembled context carries no internal identifiers or secrets.** Node
  titles are legitimate references; household, child, and user UUIDs, grant
  hashes, and key material are not, and never appear. The hygiene suite
  enforces this against every scenario.

## 5. Context assembly order

The tutor context is assembled by `context_assembly.assemble_context` for the
`tutor` role within a 2,000 token budget. The engine fetches every source,
scores it, then emits **required sources first, in the order they are declared
on `TUTOR_PROFILE.sources`, followed by optional sources in descending
relevance**. A source that produces empty text is skipped.

For the four governed layers this yields a stable, documented order:

1. **Developmental register** (required, declared first)
2. **Relationship milestones** (required, declared second; empty unless opted in)
3. (other required sources: current activity, style vector, governance constraints, each skipped when empty)
4. **Live session signal** (required, declared last among the required sources)
5. **Parent governed profile memory** (optional, so it lands after the required signal block)

The resulting relative order of the four governed blocks is therefore
**register, milestones, signal, profile**. This is deliberately not the
intuitive "register, milestones, profile, signal": the profile is an optional
source and the signal is a required one, so the signal precedes the profile in
the assembled text. The matrix harness asserts exactly this order on the one
scenario where all four blocks are live.

## 6. Parent controls and their governance events

Every parent control over the tutor emits a hash chained governance event.
System emitted events (the tutor proposing, an autonomous application, the
efficacy engine proposing a retirement) are included for completeness and
marked as such.

| Parent control | Surface | Governance event(s) |
| --- | --- | --- |
| Set tutor autonomy to off / standard / autonomous | AI governance role board | `ai_role_policy_changed`; additionally `ai_autonomy_granted` on a change into autonomous, or `ai_autonomy_revoked` on a change out of autonomous |
| Approve a proposed memory entry | Tutor memory, review queue | `tutor_profile_approved` |
| Reject a proposed memory entry | Tutor memory, review queue | `tutor_profile_rejected` |
| Remove (revoke) an active memory entry | Tutor memory, active list | `tutor_profile_entry_revoked` |
| Approve a proposed retirement | Tutor memory, active entry | `tutor_profile_entry_retired` (via `standard_approval`) |
| Reject a proposed retirement | Tutor memory, active entry | `tutor_profile_retirement_rejected` |
| Set the developmental voice override | Tutor voice register row | `tutor_register_override_set` |
| Clear the developmental voice override | Tutor voice register row | `tutor_register_override_cleared` |
| Enable relationship memory | Relationship memory control | `tutor_relationship_memory_enabled` |
| Disable relationship memory | Relationship memory control | `tutor_relationship_memory_disabled` |
| (system) Tutor proposes a memory entry under standard | n/a | `tutor_profile_proposed` |
| (system) Tutor applies a memory entry under a standing grant | n/a | `tutor_profile_applied_autonomously` |
| (system) Tutor applies a retirement under a standing grant | n/a | `tutor_profile_entry_retired` (via `autonomous_grant`) |
| (system) Efficacy engine proposes retiring an entry | n/a | `tutor_profile_retirement_proposed` |

## 7. The quality harness

`backend/tests/tutor_harness/` is the permanent proof that the assembled tutor
context is always correct, complete, bounded, and clean. It asserts on the
assembled context (the exact text handed to the model), never on model output,
and makes zero AI calls.

- `scenarios.py`: six golden households seeded through the real services
  (fresh start, the struggling reader, the cruising mathematician, the
  teenager, locked down, the revoked grant), spanning every policy and every
  entry status.
- `test_context_matrix.py`: per scenario structural truth for each block
  (register tier and override, active only profile filtering, signal presence,
  milestone opt in and cap, the off short circuit, and the documented block
  order).
- `test_context_hygiene.py`: cleanliness and bounds against every scenario (no
  quoted speech and no clinical language, reusing the profile validator's own
  denylist as the source; no failure counts in milestones; no internal
  identifiers or secrets; a documented size budget; and determinism).
