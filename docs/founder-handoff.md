# Founder Handoff Document

**CONFIDENTIAL. Update weekly. This is the document that answers "what if Zack is unavailable."**

Last updated: 2026-04-17

## System Map

| Component | What It Does | Where It Runs | Critical? |
|---|---|---|---|
| Backend API | FastAPI, 216 endpoints, all business logic | Railway (Python 3.12) | Yes |
| Celery Worker | 12 scheduled tasks + on-demand enrichment | Railway (same codebase) | Yes (data integrity) |
| PostgreSQL | 51 tables, RLS on 49, all user data | Railway managed | Yes |
| Redis | Celery broker, rate limiting, cache | Railway managed | Yes (for background tasks) |
| Frontend | Next.js 15, 38 pages, PWA | Railway or Vercel | Yes (user-facing) |
| Nginx | Reverse proxy, TLS, rate limiting | Production only | Yes (production) |

## Repo Structure

- `backend/app/`: 59,200 LOC Python. Services, API, models, AI gateway, tasks.
- `backend/tests/`: 19,992 LOC. 936 parametrized test cases across 62 files.
- `frontend/src/`: 20,144 LOC TypeScript. Next.js App Router with Tailwind CSS 4.
- `docs/`: Architecture decisions, runbooks, compliance, deployment.
- `.github/workflows/`: 5 CI jobs, native builds, staging deploy.

## Who to Call

| Role | Contact | Notes |
|---|---|---|
| Founder/CTO | Zack Fava, zack@methean.io | Primary for everything |
| Legal | (TBD, engage before seed) | COPPA/FERPA review needed |
| Accountant | (TBD) | METHEAN, Inc. LLC books |
| AI Provider (Anthropic) | Enterprise support (when DPA signed) | Primary AI provider |
| Hosting (Railway) | support@railway.app | Infra issues |

## Where Things Are

- **Source code**: github.com/zfava/METHEAN (private)
- **Infrastructure**: Railway dashboard (see access-inventory.md)
- **DNS**: Domain registrar (see access-inventory.md)
- **Credentials**: 1Password vault (see access-inventory.md)
- **Legal docs**: (TBD, not yet centralized)
- **Financial**: Stripe dashboard for billing, bank account for METHEAN, Inc. LLC

## What Is Weird (Non-Obvious Decisions)

1. **The governance gateway is the core product, not the AI.** AI is an instrument; governance is the value proposition. Do not optimize AI quality at the expense of governance completeness.

2. **RLS is enforced at the database level, not the application level.** Every query goes through PostgreSQL RLS. If RLS is disabled, ALL data leaks. The `set_tenant()` call in `app/core/database.py` is the single most critical line of code.

3. **The mock AI provider is not a test double.** It is a production fallback. When Claude and OpenAI are both down, mock keeps the platform functional. Mock responses are designed to be useful, not just placeholder.

4. **Pre-enriched content files are not AI-generated at runtime.** The 115 nodes in `app/content/` are hand-crafted curriculum content. They are applied at template instantiation time, not through the AI pipeline.

5. **Wellbeing data is parent-only by design.** No child-facing API endpoint returns wellbeing anomalies. This is a COPPA-adjacent safety decision, not just a UI choice.

6. **The 51-state compliance engine contains legal-adjacent data.** The STATE_REQUIREMENTS dict was verified against HSLDA and state DOE sources in April 2026. Laws change. Re-verify annually.

## What Is In Flight

| Item | Status | Notes |
|---|---|---|
| Pre-enriched content (5 subjects, 115 nodes) | Complete | Math (30), Reading (25), History (20), Writing (20), Science (20) |
| AI cost controls | Complete | Per-household daily budget, loop guard, cost tracking |
| RLS coverage | Complete | 49 tables, migration 031 added audit_logs |
| COPPA/FERPA documentation | Draft complete | Needs legal review before public |
| Self-service account deletion | NOT BUILT | P0 gap for COPPA compliance |
| Stripe billing hardening | Partial | Checkout + portal + webhooks work; dunning not built |
| E2E tests | 2 Playwright tests | Need expansion for golden paths |
| Uptime monitoring | NOT SET UP | Need external pinger before beta |
| DPAs with AI providers | NOT SIGNED | P1 for school-district customers |

## Customer Context

Currently pre-beta. 6-8 families signed letters of intent at $99/month. No live customers yet. Beta launch target: (founder sets date).

## The Beta Onboarding Flow

1. Parent signs up at methean.app
2. Completes onboarding: household name, children, philosophical profile, home state
3. System generates education plans per child
4. Parent reviews and approves governance rules
5. Children begin daily learning activities
6. Parent reviews AI recommendations in governance queue
7. Weekly snapshots and monthly compliance reports generated automatically
