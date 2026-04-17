# Status Page

Last verified: 2026-04-17

## Current State

No public status page is deployed yet. Incidents are communicated via direct email to affected users.

## Planned Setup

**Recommended: Better Stack (betterstack.com)**

- Free tier covers up to 5 monitors
- Connects to `GET /health` endpoint
- Public status page at `status.methean.app`
- Incident management with email notifications

**Alternative: UptimeRobot**

- Free tier covers up to 50 monitors
- Simple health check monitoring
- Public status page included

**Alternative: Self-hosted (Upptime on GitHub Pages)**

- Zero cost, runs on GitHub Actions
- Status page auto-generated from health check results
- Fully controlled, no third-party dependency

## Configuration (once deployed)

Monitors to configure:

| Monitor | URL | Check Interval | Alert After |
|---|---|---|---|
| API Health | https://api.methean.app/health | 60s | 3 failures |
| API Readiness | https://api.methean.app/health/ready | 60s | 3 failures |
| Frontend | https://methean.app/ | 60s | 3 failures |
| Metrics | https://api.methean.app/metrics | 300s | 3 failures |

## Status Page URL

Once deployed: `https://status.methean.app` (or equivalent)

Link from:
- Footer of methean.app
- Privacy policy
- Terms of service
- Incident communication emails

## Action Items

- [ ] Choose provider (Better Stack recommended for free tier + incident management)
- [ ] Configure monitors for /health, /health/ready, and frontend
- [ ] Set up DNS for status.methean.app (CNAME to provider)
- [ ] Add status page link to website footer
- [ ] Test: take the backend down, verify status page shows degraded within 3 minutes
