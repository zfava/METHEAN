# Incident Response

Last verified: 2026-04-17 (process documented, not yet exercised in production)

## Detection

Incidents are detected through:

1. **Sentry alerts**: error rate spike, new error type, performance degradation
2. **Prometheus/Grafana**: custom metrics (ai_calls_total, governance_decisions, fsrs_decays) and request latency
3. **Health endpoint**: `GET /health` returns non-200 (monitored by hosting provider)
4. **Customer report**: email to zack@spartansolutions.co or in-app feedback

## Severity Levels

| Level | Definition | Response Time | Example |
|---|---|---|---|
| P0 | Complete service outage or data breach | Immediate (drop everything) | Database unreachable, RLS bypass, credential leak |
| P1 | Major feature broken, affecting all users | Within 1 hour | AI gateway down (no fallback), auth broken, data export failing |
| P2 | Feature degraded, workaround exists | Within 4 hours | AI degraded to mock only, one state's compliance check wrong, slow queries |
| P3 | Minor issue, cosmetic or edge case | Next business day | Typo in email template, minor UI glitch, non-critical test failure |

## Triage Process

1. Check `/health` and `/health/ready` endpoints
2. Check Sentry for error spike (last 15 minutes)
3. Check Railway dashboard for deploy status
4. Check PostgreSQL connection (can the app reach the DB?)
5. Check Redis connection (can Celery tasks run?)
6. Check AI provider status pages (status.anthropic.com, status.openai.com)

## Communication

### Status Page

Post to the status page (when one exists; until then, direct email):

```
Subject: [METHEAN] Service Issue - {brief description}

We are aware of {issue description}.
Impact: {what users experience}
Current status: {investigating / identified / fixing / resolved}
ETA: {honest estimate or "investigating"}
```

### Customer Email (P0/P1 only)

```
Subject: METHEAN service disruption - {date}

Hi {name},

We experienced {brief description} starting at {time UTC}.
Impact: {what you could not do}
Resolution: {what we did}
Duration: {how long it lasted}
Prevention: {what we changed so it does not recur}

-- Zack
```

## War Room Log

During an active incident, write a running log:

```
# Incident: {title}
# Opened: {time UTC}
# Severity: P{n}

HH:MM - Detected: {what triggered the alert}
HH:MM - Investigating: {first finding}
HH:MM - Root cause: {identified cause}
HH:MM - Mitigation: {what was done}
HH:MM - Resolved: {confirmation}
HH:MM - Closed
```

Write this in a scratch file or Notion page. Copy to `docs/incidents/YYYY-MM-DD-title.md` after resolution.

## Post-Incident Review

Within 48 hours of resolution:

1. What happened? (timeline)
2. What was the impact? (users affected, duration, data loss)
3. What was the root cause?
4. What did we do to fix it?
5. What will we do to prevent recurrence? (with owner and deadline)
6. Was the detection adequate? (how long before we noticed)
7. Was the response adequate? (could we have been faster)

No blame. Focus on systems, not people.
