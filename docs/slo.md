# Service Level Objectives

Internal reliability targets for METHEAN. These are goals, not customer-facing SLAs. Updated as monitoring capabilities improve.

Last verified: 2026-04-17

## SLO-1: API Availability

**Target:** 99.5% monthly (~3.6 hours downtime allowed per month)

**Measurement:** External uptime checker pinging `GET /health` every 60 seconds. Availability = (successful checks / total checks) * 100.

**Alert threshold:** 3 consecutive failed health checks (3 minutes) triggers a P1 alert.

**Breach response:** Post-incident review within 48 hours. Identify root cause. Add monitoring if detection was slow. See `docs/runbooks/incident-response.md`.

**Status:** Target set. Measurement pending (external uptime monitor not yet configured).

## SLO-2: API Latency

**Target:** p95 under 500ms for authenticated API endpoints; p95 under 3s for AI-augmented endpoints.

**Measurement:** Prometheus `http_request_duration_seconds` histogram, exposed at `/metrics`. Filter by handler to separate AI vs non-AI endpoints.

**Alert threshold:** p95 exceeds 1s for 5 consecutive minutes on non-AI endpoints.

**Breach response:** Profile slow endpoints. Check for N+1 queries, missing indexes, connection pool exhaustion. See `docs/runbooks/database-recovery.md` for DB-related latency.

**Status:** Prometheus instrumented via `prometheus-fastapi-instrumentator`. Dashboard not yet deployed.

## SLO-3: Error Rate

**Target:** Under 1% of authenticated requests return 5xx.

**Measurement:** Sentry error rate dashboard. Alternatively, Prometheus `http_requests_total` counter filtered by status code >= 500 divided by total.

**Alert threshold:** Error rate exceeds 2% over a 5-minute window.

**Breach response:** Sentry triage for the top error class. Deploy hotfix if customer-facing. See `docs/runbooks/incident-response.md`.

**Status:** Sentry configured. Error rate alerting not yet configured in Sentry.

## SLO-4: Scheduled Task Freshness

**Target:** Weekly digest fires within 24 hours of its scheduled time, 99% of weeks.

**Measurement:** Query `notification_logs` for the most recent weekly digest send. Compare to the Celery beat schedule (Sunday 18:00 UTC).

**Alert threshold:** No digest send recorded by Monday 18:00 UTC (24h late).

**Breach response:** Check Celery beat status. Check Redis queue depth. See `docs/runbooks/celery-queue-issues.md`.

**Status:** Measurable via DB query. No automated alert yet.

## SLO-5: Data Durability

**Target:** Backups every 24 hours, 7-day retention minimum. Monthly restore drill.

**Measurement:** Hosting provider backup dashboard (Railway snapshots, AWS RDS automated backups).

**Alert threshold:** No backup completed in the last 25 hours.

**Breach response:** Manual `pg_dump` immediately. Investigate backup provider. See `docs/runbooks/database-recovery.md`.

**Status:** Provider-dependent. Restore drill: UNTESTED (marked in database-recovery.md).

## SLO-6: Migration Safety

**Target:** Zero failed migrations in production.

**Measurement:** CI `migration-check` job: upgrade head, downgrade base, re-upgrade head. Gate blocks merge on failure.

**Alert threshold:** Any migration failure in CI.

**Breach response:** Fix the migration before merging. See `docs/runbooks/migration-rollback.md`.

**Status:** Fully measured. CI gate active on every PR.

## SLO-7: AI Cost Ceiling

**Target:** No household exceeds $3/day in AI costs (daily budget).

**Measurement:** `ai_runs` table aggregated by household_id and day. Cost computed via `app/ai/cost_controls.py`.

**Alert threshold:** Household crosses 80% of daily budget.

**Breach response:** Automatic: degrade to mock provider. Governance alert sent to parent. See `app/ai/cost_controls.py`.

**Status:** Fully implemented and tested. 20 tests in `test_ai_budget.py`.

## Measurement Infrastructure

| Component | Status | Source |
|---|---|---|
| Prometheus metrics | Configured, exposed at /metrics | `prometheus-fastapi-instrumentator` in main.py |
| Custom business metrics | 5 counters/histograms | `app/core/metrics.py`: ai_calls, ai_latency, governance_decisions, attempts, fsrs_decays |
| Structured logging | Configured (JSON, ISO timestamps) | `app/core/logging.py`: structlog with request_id |
| Sentry error tracking | Configured | `app/main.py`: sentry_sdk init |
| Health endpoint | Active | `GET /health` returns `{"status": "ok"}` |
| Readiness endpoint | Active | `GET /health/ready` checks DB + Redis |
| External uptime monitor | Not configured | Needed before beta |
| Grafana dashboards | Not deployed | Prometheus data available but no visualization |
