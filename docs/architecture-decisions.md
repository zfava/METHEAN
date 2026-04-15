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
