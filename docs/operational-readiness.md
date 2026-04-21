# Operational Readiness Checklist

Assessment of METHEAN's operational posture for investor and acquirer diligence. Every item is honest about its current state; partial and not-started items are documented, not hidden.

Last updated: 2026-04-17

## Checklist

### Reliability

| Item | Status | Evidence |
|---|---|---|
| SLOs defined | Done | docs/slo.md: 7 objectives with targets, measurement methods, and breach responses |
| SLOs measured | Partial | Prometheus instrumented (5 custom metrics + request histogram). External uptime monitor not yet configured. |
| Health endpoint | Done | `GET /health` returns `{"status": "ok"}`. Tested in CI. |
| Readiness endpoint | Done | `GET /health/ready` checks DB and Redis connectivity. |
| Metrics endpoint | Done | `GET /metrics` returns Prometheus-format metrics (request duration, custom business counters). |

### Observability

| Item | Status | Evidence |
|---|---|---|
| Structured logging | Done | `app/core/logging.py`: structlog with JSON output, ISO timestamps, log levels. |
| Request tracing | Done | `app/core/middleware.py`: request_id on every request, logged with response. |
| Error tracking | Done | Sentry SDK configured in `app/main.py` with FastAPI integration. |
| Custom business metrics | Done | `app/core/metrics.py`: ai_calls_total, ai_latency, governance_decisions, attempts_completed, fsrs_decays. |
| Metrics dashboard | Not started | Prometheus data is available at /metrics but no Grafana or dashboard is deployed. |
| External uptime monitor | Not started | Needed before beta. See docs/status-page.md. |

### Incident Management

| Item | Status | Evidence |
|---|---|---|
| Incident response policy | Done | docs/runbooks/incident-response.md: severity definitions, triage, communication templates, post-mortem template. |
| Severity definitions | Done | P0 (outage/breach), P1 (degraded), P2 (single-customer), P3 (cosmetic). |
| Communication templates | Done | Email templates for customers and status updates in incident-response.md. |
| Post-incident review | Done | Template and 7-day timeline defined. |
| Status page | Not started | Provider selected (Better Stack recommended). See docs/status-page.md. |

### On-Call

| Item | Status | Evidence |
|---|---|---|
| On-call rotation | Done (solo) | docs/on-call.md: solo founder, all severity levels. |
| Alert channels | Partial | Sentry email alerts configured. SMS for P0 not yet set up. |
| Escalation path | Done | docs/founder-handoff.md: system access documented for backup engineer. |
| Alert fatigue management | Done | Thresholds documented; circuit breaker transitions not alerted (self-resolve). |

### Data Protection

| Item | Status | Evidence |
|---|---|---|
| Backup configuration | Partial | Provider-dependent. Manual pg_dump procedure documented. |
| Restore procedure | Documented | docs/runbooks/database-recovery.md. Marked UNTESTED. |
| Restore drill | Not done | Must test before production launch. |
| Row-Level Security | Done | 49 tables with RLS policies. docs/rls-coverage.md. Migration 031. |
| Data export | Done | POST /api/v1/household/export. 7 tests in test_data_export.py. |
| Data deletion | Documented | CASCADE deletion via foreign keys. Self-service endpoint not yet built. |

### Deployment

| Item | Status | Evidence |
|---|---|---|
| CI pipeline | Done | 5 CI jobs: tests, lint, frontend, migrations, E2E. |
| Deploy procedure | Done | docs/runbooks/deploy-rollback.md. |
| Rollback procedure | Done | Railway rollback + git revert documented. |
| Migration safety | Done | CI gate: upgrade, downgrade base, re-upgrade. All migrations idempotent. |

### Compliance

| Item | Status | Evidence |
|---|---|---|
| COPPA posture | Draft | docs/compliance/coppa.md. Needs legal review. |
| FERPA posture | Draft | docs/compliance/ferpa.md. Needs legal review. |
| Data inventory | Done | docs/compliance/data-inventory.md. Field-level PII inventory. |
| Third-party processor list | Done | docs/compliance/processors.md. DPA status tracked. |
| State privacy law posture | Draft | docs/compliance/state-privacy.md. 9 states covered. |

### AI Operations

| Item | Status | Evidence |
|---|---|---|
| Circuit breaker | Done | 3-failure threshold, 60s recovery. 9 tests. |
| Provider failover | Done | Claude -> OpenAI -> mock. Automatic. |
| Cost controls | Done | Per-household daily budget, loop guard. 20 tests. |
| Cost tracking | Done | Per-AIRun cost estimation in integer cents. |

### Documentation

| Item | Status | Evidence |
|---|---|---|
| Architecture decisions | Done | 10 ADRs in docs/architecture-decisions.md. |
| Operational runbooks | Done | 8 runbooks in docs/runbooks/. |
| Founder handoff | Done | docs/founder-handoff.md. System map, contacts, non-obvious decisions. |
| Access inventory | Done | docs/access-inventory.md (gitignored). 9 service accounts. |

## Summary

| Category | Done | Partial | Not Started |
|---|---|---|---|
| Reliability | 4 | 1 | 0 |
| Observability | 4 | 0 | 2 |
| Incident Management | 4 | 0 | 1 |
| On-Call | 3 | 1 | 0 |
| Data Protection | 3 | 1 | 2 |
| Deployment | 4 | 0 | 0 |
| Compliance | 2 | 3 | 0 |
| AI Operations | 4 | 0 | 0 |
| Documentation | 4 | 0 | 0 |
| **Total** | **32** | **6** | **5** |

32 of 43 items complete. 6 partial. 5 not started. The not-started items (metrics dashboard, uptime monitor, status page, restore drill, business continuity plan) are pre-beta tasks, not blockers for the current stage.
