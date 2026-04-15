"""Custom Prometheus business metrics for METHEAN."""

from prometheus_client import Counter, Histogram

ai_calls_total = Counter(
    "methean_ai_calls_total",
    "Total AI gateway calls",
    ["role", "provider", "status"],
)

ai_latency = Histogram(
    "methean_ai_latency_seconds",
    "AI call latency in seconds",
    ["role"],
)

governance_decisions = Counter(
    "methean_governance_decisions_total",
    "Governance decisions by action type",
    ["action"],
)

attempts_completed = Counter(
    "methean_attempts_completed_total",
    "Learning attempts completed",
)

fsrs_decays = Counter(
    "methean_fsrs_decays_total",
    "FSRS mastery decay transitions",
)
