# Operational Runbooks

Step-by-step procedures for common operational scenarios. Each runbook includes a "Last verified" date; procedures marked UNTESTED have not been exercised against production.

## Index

| Runbook | Scenario | Verified |
|---|---|---|
| [incident-response.md](incident-response.md) | How to detect, triage, communicate, and review incidents | 2026-04-17 (documented) |
| [ai-provider-outage.md](ai-provider-outage.md) | Detect and handle Claude/OpenAI outages; force mock mode | 2026-04-17 (circuit breaker tested) |
| [database-recovery.md](database-recovery.md) | Backup, restore, PITR, and post-recovery validation | UNTESTED |
| [migration-rollback.md](migration-rollback.md) | When and how to roll back a database migration | 2026-04-17 (CI round-trip tested) |
| [auth-token-rotation.md](auth-token-rotation.md) | JWT secret rotation, bulk password reset, session invalidation | 2026-04-17 (dual-key code verified) |
| [celery-queue-issues.md](celery-queue-issues.md) | Detect stuck queues, drain safely, replay tasks | 2026-04-17 (beat schedule tested) |
| [deploy-rollback.md](deploy-rollback.md) | Roll back a Railway deploy or git revert | 2026-04-17 (documented) |
| [customer-data-request.md](customer-data-request.md) | Fulfill COPPA/FERPA data export and deletion requests | 2026-04-17 (export tested) |
| [dev-environment.md](dev-environment.md) | Local developer setup: ruff, pre-commit hooks, backend env | 2026-05-15 (documented) |

## How to Use

1. During an incident, identify the scenario from the table above
2. Open the corresponding runbook
3. Follow the steps in order
4. Record actions in the war room log (see incident-response.md)
5. After resolution, update the runbook if steps were wrong or missing

## Maintenance

- Review all runbooks quarterly
- After every incident, update the relevant runbook with lessons learned
- Test database recovery at least once before production launch
- Every new operational scenario gets a new runbook
