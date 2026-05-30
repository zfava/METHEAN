# Curriculum Generation Pipeline Audit

Read-only audit. No code was changed. All line numbers reference the repository state at audit time.

> Path note: the request specified `/Users/Fava/Desktop/METHEAN/docs/...` (a local Mac path). In this remote container the repository is mounted at `/home/user/METHEAN`, so this report was written to `/home/user/METHEAN/docs/curriculum_pipeline_audit.md`.

## TL;DR (the headline finding)

`AIRole.education_architect` is shared by **two** services that expect **two different output contracts**:

- `education_architect.py` (multi-year education plan) reads `output["year_plans"]`.
- `annual_curriculum.py` → `materialize_full_year` reads `scope_sequence["weeks"]`.

The deterministic mock in `gateway.py` returns the **`year_plans`** shape only. So when the mock provider is used, an annual curriculum materializes **0 weeks and 0 activities** (the `weeks` key is absent). The real-AI path works for annual curriculum because the `ANNUAL_CURRICULUM_SYSTEM` prompt instructs the model to emit `weeks[]`; the mock was written against the *other* consumer's contract.

---

## 1. Exact call site: AnnualCurriculum generation invokes `call_ai` with `AIRole.education_architect`

**`backend/app/services/annual_curriculum.py:235-244`** (role on line **237**):

```python
235  ai_result = await call_ai(
236      db,
237      role=AIRole.education_architect,
238      system_prompt=system_prompt,
239      user_prompt=user_prompt,
240      household_id=household_id,
241      triggered_by=user_id,
242      philosophical_profile=phil,
243      max_tokens=8000,
244  )
```

The returned `ai_result["output"]` is stored verbatim as `curriculum.scope_sequence` (`annual_curriculum.py:246`, `:260`):

```python
246  output = ai_result["output"] if isinstance(ai_result["output"], dict) else {}
260      scope_sequence=output,
```

> Note: there is a **second**, distinct call site with the same role at `backend/app/services/education_architect.py:84` (the multi-year education plan). That one is the contract the mock actually matches — see §4.

---

## 2. Provider chain order, mock selection, and env gating

**Chain construction — `backend/app/ai/gateway.py:550-559`:**

```python
550  def _get_provider_chain() -> list[AIProvider]:
551      """Get ordered list of providers to try."""
552      chain = []
553      if settings.AI_API_KEY:
554          chain.append(AIProvider.claude)
555      if settings.AI_FALLBACK_API_KEY:
556          chain.append(AIProvider.openai)
557      if settings.AI_MOCK_ENABLED:
558          chain.append(AIProvider.mock)
559      return chain
```

Order today: **Claude → OpenAI → Mock** (each appended only if its gate is set).

**Selection loop — `gateway.py:326-374`** tries providers in order; the branch that fires depends on per-provider config:

```python
327  providers = _get_provider_chain()
329  for provider in providers:
331      if provider == AIProvider.claude and settings.AI_API_KEY:      # -> _call_claude
344      elif provider == AIProvider.openai and settings.AI_FALLBACK_API_KEY:  # -> _call_openai
357      elif provider == AIProvider.mock and settings.AI_MOCK_ENABLED:  # -> _call_mock
370          result = _call_mock(role, user_prompt)
374          is_mock = True
```

Mock is selected **only when** (a) it is in the chain (`AI_MOCK_ENABLED=True`) **and** (b) every real provider ahead of it either was absent from the chain or raised (the loop reaches the `mock` branch). The mock branch logs `ai_gateway.mock_fallback_used` (`:362-368`).

**Env flags (`backend/app/core/config.py`):**

| Flag | Default | Gates |
|---|---|---|
| `AI_API_KEY` | `""` (`config.py:37`) | Claude in chain + `_call_claude` |
| `AI_FALLBACK_API_KEY` | `""` (`config.py:38`) | OpenAI in chain + `_call_openai` |
| `AI_MOCK_ENABLED` | `False` (`config.py:49`) | Mock in chain + `_call_mock` |
| `AI_PRIMARY_MODEL` | `claude-opus-4-6` (`config.py:39`) | Claude model id |
| `AI_TEMPERATURE` | `0.7` (`config.py:51`) | both real providers |

If all real providers fail **and** `AI_MOCK_ENABLED=False`, `call_ai` raises `AIProvidersUnavailable` rather than fabricating content (`gateway.py:114-126`, `:401-416`). A production safety validator refuses to boot with `AI_MOCK_ENABLED=True` unless `ALLOW_AI_MOCK_IN_PRODUCTION=true` (`config.py:111-118`).

---

## 3. EXACT shape `materialize_full_year` expects as input

**`backend/app/services/annual_curriculum.py:333-434`.** Input is `curriculum.scope_sequence` (a dict). Field accesses, quoted:

**Top level:**
```python
339  weeks_data = curriculum.scope_sequence.get("weeks", [])      # REQUIRED: weeks[]
353      description=curriculum.scope_sequence.get("overview", ""),  # plan description
```
If `weeks` is missing/empty it short-circuits: `:340-341` `return {"weeks_created": 0, "activities_created": 0}`.

**Per-week (iterating `weeks_data`, `:377`):**
```python
378  week_num = week_data.get("week_number", 1)             # week_number
388      notes=week_data.get("assessment_focus", ""),       # assessment_focus -> PlanWeek.notes
394  activities = week_data.get("suggested_activities", []) # suggested_activities[]
418  focus_nodes = week_data.get("focus_nodes", [])         # focus_nodes[]
```

**Per-activity / per-day (iterating `suggested_activities`, `:396`):**
```python
397  day_name = act_data.get("day", "Monday")        # day (Monday..Friday)
401  act_type_str = act_data.get("type", "lesson")   # type (lesson/practice/assessment/review/project/field_trip)
408      title=act_data.get("title", f"Activity {idx + 1}"),  # title
409      description=act_data.get("description", ""),          # description
410      estimated_minutes=act_data.get("minutes", 30),       # minutes
```
Day → date offset via `day_offsets` (`:373`, Monday=0…Friday=4). Type → enum via `activity_type_map` (`:364-371`).

**Node linking (`:418-423`):**
```python
418  focus_nodes = week_data.get("focus_nodes", [])
421      activity.node_id = uuid.UUID(focus_nodes[min(idx, len(focus_nodes) - 1)])
```
`focus_nodes[i]` must parse as a **UUID**; `ValueError`/`IndexError` are swallowed (`:422-423`). String node ids like `mf-01` or `math_f_01` (see §5/§6) would silently fail to link.

**Important precision:** `materialize_full_year` does **not** read per-week `title` or `objectives`. Those are read only by the reporting function `get_curriculum_history` — `title` at `annual_curriculum.py:625`, `objectives` at `:626`, and `suggested_activities` (for a count) at `:628`. The single-week reporting path also reads `week_number` (`:574`). So the *materialization* contract is narrower than the full documented week shape.

**Documented (intended) week shape** — the system prompt `ANNUAL_CURRICULUM_SYSTEM` (`annual_curriculum.py:46-66`) tells the model to emit exactly: top-level `overview`, `philosophy_alignment`, `materials[]`, `weeks[]`; per week `week_number`, `title`, `focus_nodes[]`, `objectives[]`, `suggested_activities[]` (`title`,`type`,`minutes`,`day`,`description`), `assessment_focus`, `parent_notes_placeholder`.

---

## 4. The shape the mock returns — the `year_plans`-vs-`weeks` divergence

**`backend/app/ai/gateway.py:690-866`**, `mock_responses[AIRole.education_architect]`. The JSON content has these **top-level keys** (`:692-864`):

```python
693  "plan_name": "Classical Education Plan",
694  "philosophy_alignment": "...",
695  "year_plans": {            # <-- dict keyed by academic year, NOT a weeks[] array
696      "2026-2027": { "grade": "1st", "developmental_stage": "...",
700                     "subjects": [ {subject, priority, hours_per_week, description, approach}, ... ],
743                     "total_hours_per_week": 18, "milestones": [...], "notes": "..." },
747      "2027-2028": { ... },
798      "2028-2029": { ... } },
850  "transitions": [ {from_year, to_year, description}, ... ],
862  "graduation_pathway": "...",
863  "rationale": "..."
```

There is **no `weeks` key** anywhere in the mock payload.

**Concrete divergence:**

| Consumer | Reads | Mock provides? | Result with mock |
|---|---|---|---|
| `education_architect.py:91` | `output.get("year_plans", {})` and `output.get("plan_name", …)` | ✅ yes | Education plan populates correctly |
| `annual_curriculum.py` → `materialize_full_year:339` | `scope_sequence.get("weeks", [])` | ❌ no | `weeks_data == []` → early return `{"weeks_created": 0, "activities_created": 0}` (`:340-341`); a Plan with **zero** PlanWeeks/Activities |

Flow that produces the broken state: mock output → stored as `curriculum.scope_sequence` (`annual_curriculum.py:260`) → `approve_annual_curriculum` calls `materialize_full_year` (`:319`) → `.get("weeks", [])` is empty → no PlanWeek/Activity rows created.

Root cause: a **single `AIRole.education_architect` mock** cannot satisfy two services with different contracts. The mock matches `education_architect.py` (`year_plans`); `annual_curriculum.py` needs the `weeks[]` shape its own system prompt (`:46-66`) documents.

---

## 5. `scope_sequences.py` shape

**`backend/app/content/scope_sequences.py`.** Structure: `SCOPE_SEQUENCES[subject_id][level] -> list[topic_dict]`.

Accessors (`:6-27`):
```python
6   def get_scope_sequence(subject_id, level) -> list[dict]:
7       return SCOPE_SEQUENCES.get(subject_id, {}).get(level, [])
11  def get_next_topics(subject_id, level, completed_refs, count=5) -> list[dict]:   # prerequisite-gated
24  def get_all_subject_ids() -> list[str]:
```

One entry (topic), keys quoted from `mathematics → foundational → math_f_01` (`:31-51`):
```python
{
  "ref": "math_f_01",                       # topic reference id
  "title": "Counting to 20",
  "description": "...",
  "prerequisites": [],                      # list[str] of other refs (e.g. ["math_f_01"])
  "estimated_weeks": 2,
  "key_concepts": ["one-to-one correspondence", "numeral recognition", ...],
  "assessment_indicators": ["Counts 20 objects accurately", ...],
  "classical_alignment": "Grammar stage: ...",
  "charlotte_mason_alignment": "...",
  "standard_alignment": "K.CC.1-5",
}
```

- **Ref format:** `<subject>_<level-initial>_<NN>` → `math_f_01`, `math_f_02`, … (`:33`, `:48`).
- **Node reference:** topics reference each other purely by the string `ref` in `prerequisites` (no UUIDs, no cross-file ids).
- **Consumption:** `annual_curriculum.py:177-190` calls `get_scope_sequence(subj_id, level)` and reads `t["ref"]`, `t["title"]`, `t.get("prerequisites")`, `t.get("estimated_weeks")`, `t.get("key_concepts")[:5]` to build a "scope and sequence" block injected into the user prompt. It is prompt context only; it is not persisted structurally.

---

## 6. Content-module node keying and node-id format

**`backend/app/content/math_foundational_content.py`** — top-level dict `MATH_FOUNDATIONAL_CONTENT` (`:3`) keyed by **node-id strings**:

```python
3   MATH_FOUNDATIONAL_CONTENT = {
4       "mf-01": {
5           "enriched": True,
6           "learning_objectives": [ ... ],
12          "teaching_guidance": {
                "introduction": "...",
                "scaffolding_sequence": [ ... ],
                "socratic_questions": [ ... ],
                "practice_activities": [ ... ],
                "real_world_connections": [ ... ],
                "common_misconceptions": [ ... ] },
            "assessment_criteria": {
                "mastery_indicators": [ ... ],
                "assessment_methods": [ ... ],
                "sample_assessment_prompts": [ ... ] },
            "practice_items": [ {type, difficulty, prompt, expected_type, correct_answer, hints[], explanation}, ... ],
        },
        "mf-02": { ... }, ...  "mf-10": { ... }
  }
```

Keys present: `mf-01`, `mf-02`, …, `mf-10` (`grep` hits at lines 4, 293, 533, 760, 989, 1229, 1472, 1702, 1940, 2164).

**Node-id format = `<subject-level-initials>-NN`** (zero-padded). Observed prefixes across `content/*_content.py`:

| Module (var) | Prefix | Example first key |
|---|---|---|
| `MATH_FOUNDATIONAL_CONTENT` | `mf-` | `mf-01` |
| `MATH_DEVELOPING_CONTENT` | `md-` | `md-01` |
| `READING_FOUNDATIONAL_CONTENT` | `rf-` | `rf-01` |
| `READING_DEVELOPING_CONTENT` | `rd-` | `rd-01` |
| `SCIENCE_FOUNDATIONAL_CONTENT` | `sf-` | `sf-01` |
| `HISTORY_FOUNDATIONAL_CONTENT` | `hf-` | `hf-01` |
| `WRITING_FOUNDATIONAL_CONTENT` | `wf-` | `wf-01` |
| `literature_mastery_content` | `lit-` | `lit-craft-001` |
| Vocational (`electrical`, `gardening`, `hvac`, `woodworking`) | `<slug>-` | `el-root`, `gardening-root`, `hvac-root`, `woodworking-root` |

> **Three incompatible node-id namespaces coexist:** content modules (`mf-01`), scope_sequences (`math_f_01`), and DB `LearningNode` rows (UUIDs). `materialize_full_year` only accepts UUIDs for `focus_nodes` (`annual_curriculum.py:421`); the string ids from the content/scope layers do not link there and are silently dropped.

---

## 7. Inputs available at generation time

All flow from `GenerateRequest` (`backend/app/api/annual_curriculum.py:35-48`) through the endpoint (`api/annual_curriculum.py:123-136`) into `generate_annual_curriculum(...)` (`annual_curriculum.py:70-83`).

| Input | Type | Origin / resolution | Citation |
|---|---|---|---|
| **child age** | `float` (years) | Computed: `(date.today() - child.date_of_birth).days / 365.25`, fallback `6`. Child loaded by `child_id`. | `annual_curriculum.py:118`, `:87-88` |
| **learning_level** | `str` (+ `level_info` dict) | `content_tier` if in `VALID_LEVELS`, else `get_level_for_subject(prefs, subject_name)`; `level_info = LEARNING_LEVELS.get(level, …["developing"])` | `annual_curriculum.py:127-131` |
| **hours_per_week** | `float` (default `4.0`) | Request body field | `api:39`, `annual_curriculum.py:78`, used `:225` |
| **total_weeks** | `int` (default `36`) | Request body; if `36`, overridden by `calendar["total_instructional_weeks"]` | `api:40`, `annual_curriculum.py:79`, `:102-103` |
| **start_date** | `date \| None` | Request; else `calendar["start_date"]`; else default `date(year, 9, 1)` | `api:41`, `annual_curriculum.py:80`, `:108-116` |
| **philosophy** | `dict` (`phil`) | `household.philosophical_profile or {}`; expanded via `build_philosophical_constraints(phil)` | `annual_curriculum.py:96`, `:162`, `:206-209` |

Supporting inputs also threaded in:
- `subject_name: str`, `academic_year: str` (e.g. `"2026-2027"`) — `api:36-37`.
- `learning_map_id: uuid.UUID | None` — if present, DB `LearningNode`/`LearningEdge` are loaded in topo order and rendered into the prompt (`annual_curriculum.py:135-159`).
- `prefs` (`ChildPreferences`) — `learning_style`, `interests`, `accommodations` injected into the user prompt (`:90-91`, `:221-223`).
- `scope_notes: str | None`, `content_tier: ContentTier | None` — `api:42`, `:48`.
- Academic calendar drives `instruction_days` / `days_per_week` / `end_date` (`:99-116`).

These are assembled into `system_prompt` + `user_prompt` (`annual_curriculum.py:201-233`) and passed to `call_ai` (§1). The model is asked to return the `weeks[]` contract (§3), which the real providers honor but the shared mock does not (§4).

---

## Cross-cutting observations (no fix applied; audit only)

1. **Shared role, two contracts (highest impact).** `AIRole.education_architect` is consumed by both `annual_curriculum.py` (`weeks[]`) and `education_architect.py` (`year_plans`). The mock can only satisfy one; it satisfies `education_architect.py`. Any mock-backed annual-curriculum approval materializes nothing.
2. **Silent zero-materialization.** `materialize_full_year` returns `{"weeks_created": 0, …}` (`:340-341`) with no error when `weeks` is absent — the failure is invisible to callers/UI unless they inspect counts.
3. **Node-id namespace fragmentation.** `mf-01` (content) vs `math_f_01` (scope_sequences) vs UUID (DB nodes). `focus_nodes` linking only accepts UUIDs (`:421`); the other two formats are accepted by the model prompt but dropped at materialization.
4. **`title`/`objectives` are prompt-documented and report-consumed but not materialized.** They survive only inside `scope_sequence` JSON and surface via `get_curriculum_history`, never as columns on `PlanWeek`/`Activity`.

— End of audit —
