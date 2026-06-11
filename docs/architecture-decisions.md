# Architecture Decision Records

## ADR-001: Governance-First AI Pattern
**Decision:** All AI output queues as recommendations. AI never writes to learner state directly.
**Context:** EdTech competitors use AI as a direct decision-maker. Parents have no visibility or control.
**Rationale:** Homeschool parents chose to leave institutional education to maintain authority. The governance gateway enforces this architecturally, not as a feature toggle.
**Consequences:** Higher latency on AI actions (governance evaluation required). Stronger parent trust. Regulatory advantage.

## ADR-002: FSRS v6 Over SM-2
**Decision:** Use Free Spaced Repetition Scheduler v6 for retention modeling.
**Context:** SM-2 (Anki's algorithm) is widely used but less accurate.
**Rationale:** FSRS v6 achieves 20-30% fewer reviews for equivalent retention. Per-child weight optimization (21 parameters) adapts to individual memory patterns. Power-law forgetting curve models human memory more accurately.
**Consequences:** Dependency on py-fsrs. More complex state model. Superior learning outcomes.

## ADR-003: DAG with Transitive Closure
**Decision:** Store curriculum as a directed acyclic graph with materialized transitive closure table.
**Context:** Prerequisite enforcement requires knowing all ancestors of a node.
**Rationale:** O(1) ancestor/descendant lookups. Rebuilds only on edge mutations (rare). Reads (frequent) are instant.
**Consequences:** Additional storage. Rebuild cost on structure changes. Dramatically faster prerequisite checks.

## ADR-004: PostgreSQL RLS Over Application-Level Tenancy
**Decision:** Enforce tenant isolation at the database level using Row-Level Security.
**Context:** Application-level filtering relies entirely on application correctness.
**Rationale:** Defense-in-depth. Even with application vulnerabilities, the database prevents cross-household data access. Critical for children's data.
**Consequences:** More complex migrations. Stronger data protection guarantees.

## ADR-005: Event-Sourced Learning State
**Decision:** All learning state changes recorded as immutable StateEvents. Current state is a materialized projection.
**Context:** Most EdTech platforms overwrite state in place, losing history.
**Rationale:** Enables time-travel queries, regression detection, and complete audit trails.
**Consequences:** Higher storage. More complex current-state queries. Complete learning history.

## ADR-006: AI Cost Controls
**Decision:** Per-household daily token and cost budgets with degrade-to-mock as the default enforcement.
**Context:** At $99/month pricing, a single household running the tutor agent continuously, or an agent loop that calls itself without termination, could consume more than $99 in Claude tokens in a day. The circuit breaker guards provider health, not cost.
**Rationale:** Degrade is preferred over block because the educational experience must not stop. A child mid-lesson should still get a tutor response (from mock), even if the household has hit its daily AI budget. Block mode is available for adversarial detection (loop runaways). Per-household budgeting (not per-user) matches the subscription model: one subscription covers the whole family. Budget defaults: 200k tokens/day, $3/day cost ceiling, alert at 80%, degrade at 100%.
**Consequences:** Households exceeding budgets get mock AI responses for the remainder of the day. Parents receive a governance alert at 80%. Cost is tracked per AIRun in integer cents. Tutor sessions have a 50-call loop guard to catch runaway agent loops.

## ADR-007: Claude Primary, OpenAI Fallback, Mock Always-Available
**Decision:** Three-tier AI provider chain with automatic failover.
**Context:** EdTech platforms that depend on a single AI provider have a single point of failure.
**Rationale:** Claude is primary (best instruction-following for educational context). OpenAI is fallback (different infrastructure, different failure modes). Mock is the safety net: deterministic, zero-cost, always available. Circuit breakers (3-failure threshold, 60s recovery) manage transitions automatically.
**Consequences:** More complex gateway code. Higher reliability. Zero-downtime AI, even during provider outages.

## ADR-008: Philosophical Profile Injection
**Decision:** Every AI prompt includes the household's educational philosophy (classical, Charlotte Mason, Montessori, traditional) as a constraint.
**Context:** Homeschool families choose their approach deliberately. AI recommendations that conflict with the family's philosophy erode trust.
**Rationale:** Pre-enriched content nodes have philosophy-specific teaching guidance, resources, and assessment methods. The AI respects these as constraints, not suggestions. This is a product differentiator: no other EdTech platform adapts to educational philosophy.
**Consequences:** Larger prompts (more tokens per call). Philosophy-aware AI output. Content authoring requires 4x effort (one approach per philosophy). Stronger product-market fit.

## ADR-009: Constitutional vs. Policy Rule Tiers
**Decision:** Governance rules are organized in two tiers: constitutional (cannot be overridden by AI) and policy (can be adjusted within bounds).
**Context:** Parents need both hard limits ("never more than 3 hours of screen time") and soft preferences ("prefer morning sessions").
**Rationale:** Constitutional rules are enforced pre-AI (the planner never sees options that violate them). Policy rules are enforced post-AI (the planner may suggest something that a policy rule modifies). This prevents the AI from being creative about circumventing hard limits while allowing flexibility on preferences.
**Consequences:** Two-pass governance evaluation. More complex rule engine. Clearer parent control semantics.

## ADR-010: Append-Only Parent Observations
**Decision:** Parent observations in LearnerIntelligence are stored as an append-only JSONB array.
**Context:** Parents notice things about their children's learning that no algorithm can detect ("she reads better after playing outside").
**Rationale:** These observations are primary source material for the AI advisor and wellbeing detection. Append-only prevents accidental overwrites. The array grows over time, building a richer picture.
**Consequences:** JSONB arrays grow unbounded (mitigated by context assembly truncation). Parent voice is preserved in the data model.

## ADR-011: Database-enforced append-only audit with per-household hash chain
**Decision:** governance_events and state_events are protected by BEFORE UPDATE OR DELETE triggers that raise at the Postgres level, and every governance event carries a SHA-256 event_hash chained to the previous event in its household (prev_event_hash), with a pure verification function and a parent-facing GET /chain/verify endpoint.
**Context:** The append-only guarantee was an application convention: no code path mutated these tables, but nothing stopped a future bug, a migration, or a compromised connection with table grants from rewriting audit history. For a parent-governed system, the audit trail is the trust anchor; it must be tamper-evident, not just tamper-discouraged.
**Rationale:** Triggers, not application discipline: discipline does not survive refactors, new contributors, or raw SQL, while a trigger raises for every client on every path, including ones that bypass the ORM. Advisory locks (pg_advisory_xact_lock keyed on the household id) serialize concurrent appends per household so two transactions can never read the same chain head and fork the chain; the lock is transaction-scoped, self-releasing, and scopes contention to a single household rather than the whole table. A genesis sentinel ("GENESIS" in place of a previous hash) makes the first event in each household hash over a fixed, non-null value, so an attacker cannot truncate the head of a chain and present the remainder as complete: removing the first event breaks the second event's recomputation. Hashes are computed client-side before insert because the triggers forbid a second-pass UPDATE to write them.
**Consequences:** Backfilled hashes for existing rows are computed in migration 052 (idempotent, per household, RLS-scoped via set_config). Downgrade drops the triggers, the trigger function, and both hash columns: the cryptographic history is destroyed on downgrade and cannot be reconstructed with the same timestamps, so downgrading in production is an audit-affecting operation that should itself be logged and justified. Rows can never be corrected in place; corrections are new compensating events. Verification is O(n) per household and runs in a single query under RLS.

## ADR-012: Failure handling policy: loud by default, silent never
**Decision:** No broad exception handler in backend/app may swallow a failure invisibly. Every `except Exception` (or bare `except`) handler must do at least one of: (a) emit a structured log with enough context to act on (structlog key-value style, never prose f-strings), (b) narrow to the real exception types the protected code raises, keeping a final broad catch only for genuinely unknowable third-party surfaces, or (c) re-raise or convert to a domain error. The rule is enforced permanently by `backend/tests/test_no_silent_swallows.py`, which walks the application AST and fails on any broad handler whose body is a bare `pass` or contains neither a logging call nor a raise.
**Context:** The June audit found 53 `except Exception` blocks swallowing errors, many with a bare `pass`: failed verification emails, dead enrichment queues, broken usage recording, and silently degraded dashboards all looked identical to healthy operation. Phase 0c established loud failure over silent degradation as the platform's failure philosophy; this ADR applies it repo-wide and makes regression structurally impossible rather than a review convention.
**Rationale:** Most of the audited swallows were intentionally non-blocking (advisory calibration, achievements, notification delivery, metrics, context assembly) and that design is correct: a child mid-lesson must not crash because an advisory subsystem hiccuped. The defect was never the continue, it was the invisibility. Logging with context preserves every behavioral contract while making the failure rate observable; narrowing documents what the code actually expects; re-raising is reserved for cases where call-site analysis proves no caller depends on the swallow. Behavior preservation is the default because a warning we can see beats a crash we did not design. Privacy bounds the logs: secrets, tokens, transcript text, PINs, and child free-text never appear in log values; where an exception message could echo such content (token URLs, notification bodies, tutor streams), only the exception class name is logged.
**Consequences:** Failure visibility becomes a build-time property: a new silent swallow fails CI. Justified permanent exemptions exist but carry a structured `# swallow-exempt: <reason>` comment on the except line; the guard test surfaces every exemption, fails any without a reason, and pins the current exemption count (zero) so additions are deliberate, reviewed events. Log volume rises on genuinely failing subsystems, which is the point; routine churn paths (invalid tokens at logout, scope-token decode) log at debug to stay quiet in healthy operation.
