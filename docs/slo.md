# Service Level Objectives

Targets for METHEAN service reliability. These are internal goals, not customer-facing SLAs. Updated as monitoring capabilities improve.

Last verified: 2026-04-17 (objectives set; measurement infrastructure partially in place)

## Objectives

| Metric | Target | Measurement | Status |
|---|---|---|---|
| API availability | 99.5% monthly (~3.6h downtime allowed) | Health endpoint uptime check | Not yet measured (no uptime monitor configured) |
| API latency (p95) | Under 500ms for authenticated endpoints | Prometheus request duration histogram | Prometheus configured but no dashboard |
| AI gateway latency (p95) | Under 3s for AI-augmented calls | ai_call_duration metric in gateway | Metric exists in code |
| Error rate | Under 1% of authenticated requests return 5xx | Sentry error rate | Sentry configured |
| Weekly digest delivery | Fires within 24h of scheduled time, 99% of weeks | Beat schedule + notification_logs | Testable via DB query |
| Data durability | Backups every 24h, 7-day retention minimum | Hosting provider backup policy | Provider-dependent |
| Migration safety | Zero failed migrations in production | CI migration-check gate | Gate active in CI |

## What Happens When We Miss

| Objective | Response |
|---|---|
| Availability below 99.5% | Post-incident review within 48h. Identify root cause. Add monitoring if detection was slow. |
| Latency above p95 target | Profile slow endpoints. Add database indexes or caching. Check for N+1 queries. |
| Error rate above 1% | Sentry triage. Fix or suppress the error class. Deploy hotfix if customer-facing. |
| Digest not sent | Check Celery beat status (see celery-queue-issues.md). Manually trigger if stuck. |
| Backup missed | Alert immediately. Check provider dashboard. Manual pg_dump as fallback. |

## Not Yet Measurable

The following objectives require infrastructure not yet deployed:

- **Real uptime monitoring**: Need an external uptime checker (UptimeRobot, Pingdom, or similar) pinging /health every 60 seconds
- **Latency dashboards**: Prometheus metrics exist but no Grafana dashboard is deployed
- **Customer-facing status page**: No status page exists; incidents are communicated via email

These should be resolved before public beta.
