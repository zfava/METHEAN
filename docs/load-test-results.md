# Load Test Baseline

## Configuration
- Tool: Locust
- Target: Local Docker Compose (single backend instance)
- Users: 100 concurrent
- Ramp: 10 users/second
- Duration: 60 seconds

## How to Run

```bash
cd backend
pip install locust
locust -f scripts/load_test.py --host http://localhost:8000

# Headless mode (CI-friendly):
locust -f scripts/load_test.py --host http://localhost:8000 --headless -u 100 -r 10 --run-time 60s
```

## Endpoints Under Test

| Endpoint | Weight | Auth Required |
|----------|--------|--------------|
| GET /health | 3 | No |
| GET /api/v1/children | 2 | Yes |
| GET /api/v1/governance/rules | 2 | Yes |
| GET /api/v1/governance/queue | 1 | Yes |
| GET /api/v1/subjects | 1 | Yes |
| GET /api/v1/notifications | 1 | Yes |

## Baseline Results

(Run the test and paste results here)

## Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| p50 latency | < 100ms | Median response time |
| p95 latency | < 500ms | 95th percentile |
| p99 latency | < 1000ms | 99th percentile |
| Error rate | < 1% | Non-5xx responses |
| Throughput | > 200 req/s | Sustained for 60s |
