# On-Call Policy

Last verified: 2026-04-17

## Current State

METHEAN is operated by a solo founder (Zack Fava). All on-call responsibility falls to one person. This document makes the arrangement explicit and defines the escalation path.

## On-Call Rotation

| Role | Person | Contact | Hours |
|---|---|---|---|
| Primary on-call | Zack Fava | zack@spartansolutions.co | 24/7 (solo founder) |
| Backup | None | n/a | n/a |

When a second engineer joins (employee, contractor, or co-founder), rotate weekly on-call.

## Alert Channels

| Severity | Channel | Response Time |
|---|---|---|
| P0 (outage, data breach) | SMS + email + Sentry alert | Immediate (drop everything) |
| P1 (major degradation) | Email + Sentry alert | Within 1 hour |
| P2 (minor issue) | Email | Within 4 hours (business hours) |
| P3 (cosmetic) | GitHub issue | Next business day |

## Alert Sources

| Source | What It Monitors | Alert Method |
|---|---|---|
| Sentry | Application errors, performance | Email (configure SMS for P0) |
| Uptime monitor (TBD) | /health endpoint availability | SMS + email |
| Hosting provider | Infrastructure health | Provider dashboard alerts |
| Customer email | User-reported issues | zack@spartansolutions.co |

## Quiet Hours

- **Default**: Alerts flow during business hours (8 AM - 10 PM local time)
- **P0 override**: P0 alerts always flow, regardless of time
- **Weekend handling**: P2/P3 deferred to Monday. P0/P1 immediate.

## Alert Fatigue Management

- Alert thresholds tuned to fire only on genuine incidents (not transient errors)
- Circuit breaker open/close transitions are logged, not alerted (they self-resolve)
- AI budget threshold alerts go to the parent's notification feed, not the ops channel
- Weekly review of alert volume: if more than 3 alerts in a week, tune thresholds

## Escalation Path

If the primary on-call is unreachable for 2+ hours during a P0:

1. The `docs/founder-handoff.md` document contains system access information
2. A competent engineer with access to Railway, GitHub, and the 1Password vault can operate the system
3. Contact information for the hosting provider and AI provider support is in `docs/access-inventory.md`

## Pre-Seed Action Items

- [ ] Configure SMS alerts for P0 via Sentry or PagerDuty
- [ ] Set up external uptime monitor (UptimeRobot, Better Stack, or Pingdom)
- [ ] Add a backup on-call contact (advisor, contractor, or co-founder)
- [ ] Test the alert-to-response pipeline: trigger a synthetic P1 and measure time-to-acknowledge
