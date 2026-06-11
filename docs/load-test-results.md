# Load Test Baseline

> Last verified: 2026-06-11 against this build. Single-instance local baseline; not a production capacity claim.

## Configuration

- Tool: Locust (install with `pip install locust`; not a project dependency)
- Locustfile: `backend/scripts/load_test.py` (the single canonical path)
- Target: local stack, one uvicorn worker, local PostgreSQL 16 and Redis, `APP_ENV=test`
- Users: 100 concurrent, ramp 10 users/second, duration 60 seconds
- Each simulated user registers a fresh household and seeds one child plus one approved activity through the public API, then loops the weighted read surface

## How to Run

```bash
cd backend
pip install locust
locust -f scripts/load_test.py --host http://localhost:8000 --headless -u 100 -r 10 --run-time 60s
```

## Endpoints Under Test

| Endpoint | Weight | Why |
|----------|--------|-----|
| GET /activities/{id}/learn | 5 | The hottest path: every child activity open |
| GET /children/{id}/dashboard | 4 | Kid surface aggregate |
| GET /children + GET /children/{id}/today | 3 | Parent dashboard aggregate reads |
| GET /governance/queue | 2 | Parent review loop |
| GET /children/{id}/curricula | 2 | Annual curriculum read |
| GET /children/{id}/family-record | 1 | Record read (heavier query, lighter traffic) |
| GET /health | 1 | Probe baseline |
| POST /auth/register | once per user | Cookie login flow in on_start |

## Baseline Results (2026-06-11, this build)

2,069 requests in 60s, 0 failures (0.00%), 35.0 req/s aggregate sustained.

| Endpoint | Requests | RPS | p50 ms | p95 ms | p99 ms | Failures |
|----------|---------:|----:|-------:|-------:|-------:|---------:|
| GET /activities/{id}/learn | 354 | 6.0 | 21 | 1000 | 1400 | 0 |
| GET /children/{id}/dashboard | 276 | 4.7 | 35 | 820 | 1600 | 0 |
| GET /children | 216 | 3.7 | 16 | 910 | 1700 | 0 |
| GET /children/{id}/today | 216 | 3.7 | 17 | 330 | 990 | 0 |
| GET /governance/queue | 133 | 2.3 | 18 | 890 | 1300 | 0 |
| GET /children/{id}/curricula | 129 | 2.2 | 16 | 1100 | 2000 | 0 |
| GET /children/{id}/family-record | 74 | 1.3 | 29 | 98 | 1500 | 0 |
| GET /health | 71 | 1.2 | 5 | 20 | 170 | 0 |
| POST /auth/register (login) | 100 | 1.7 | 18000 | 23000 | 25000 | 0 |
| Seed writes (children/subjects/maps/nodes/activities) | 500 | 8.5 | 760 to 7800 | 1500 to 17000 | 2300 to 23000 | 0 |

## Comparison to the April 15 baseline

Not possible: the April document referenced two different locustfile paths (`scripts/locustfile.py` and `scripts/load_test.py`, now reconciled to `backend/scripts/load_test.py`) and its results section contained only the placeholder "Run the test and paste results here". This run is the first recorded baseline. The April performance targets are retained below and evaluated against it.

## Performance Targets

| Metric | Target | This run | Verdict |
|--------|--------|----------|---------|
| p50 latency (read surface) | < 100ms | 5 to 35ms | Pass |
| p95 latency (read surface) | < 500ms | 20 to 1100ms | Mixed, see below |
| p99 latency (read surface) | < 1000ms | 170 to 2000ms | Mixed, see below |
| Error rate | < 1% | 0.00% | Pass |
| Throughput | > 200 req/s | 35 req/s offered | Not exercised: the workload waits 1 to 3s per user, so 100 users offer about 35 req/s by design |

## Interpretation

Steady-state reads are comfortable: every endpoint's median sits between 5ms and 35ms on a single uvicorn worker, with zero failures. The p95/p99 tails (0.8 to 2.0s) are not steady-state behavior; they coincide with the ramp window, when all 100 users register simultaneously and bcrypt password hashing saturates the CPU. Registration itself shows this clearly (p50 18s under the burst): bcrypt is intentionally expensive, and 10 registrations per second on one worker is far beyond any realistic signup rate. At 10x read traffic the things to watch are, in order: bcrypt contention if signups spike (isolate auth workers or queue registrations), the learn-context and child-dashboard tails (both aggregate multiple queries; the today-performance indexes from migration 041 hold up at this level but deserve re-measurement), and the governance queue's per-activity governance-event lookups, which are linear in queue depth. The family record read (the heaviest single query surface) held a 98ms p95 at this traffic, which leaves clear headroom.
