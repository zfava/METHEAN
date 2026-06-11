# METHEAN Grafana Dashboards

## Import

1. Grafana: Dashboards, then New, then Import.
2. Upload `methean-overview.json` (or paste its contents).
3. When prompted, map the `DS_PROMETHEUS` input to the Prometheus
   datasource that scrapes the backend's `/metrics` endpoint
   (exposed by prometheus-fastapi-instrumentator on the API service).
   Any datasource name works; the dashboard binds it at import time.

## Rows

- **Traffic**: request rate by handler, 5xx error share, and p50/p95
  latency from the instrumentator's `http_requests_total` and
  `http_request_duration_seconds` series.
- **AI**: gateway calls by role, calls by provider and status (the
  provider split is the failover chain made visible), and per-role
  latency p95 from `methean_ai_calls_total` and
  `methean_ai_latency_seconds`.
- **Learning**: attempts completed, governance decisions by action,
  and FSRS decay transitions from the `methean_*` business counters.
- **Voice and TTS**: transcription volume and latency, TTS first-chunk
  latency, and safety interventions from the `voice_*` and `tts_*`
  families.
- **System**: process memory, CPU, and file descriptors from the
  default process collector.

Every panel queries only metric names the application actually emits
(enumerated from `backend/app/core/metrics.py`,
`backend/app/core/observability.py`, the instrumentator defaults, and
a live `/metrics` scrape). Panels the original sketch wanted but whose
metrics do not exist yet are omitted rather than invented: estimated
AI spend, curricula-generated counts, dunning-state gauges, DB pool,
Redis, and Celery queue depth. Add the metric first, then the panel.
