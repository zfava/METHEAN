"""Prometheus metrics for METHEAN.

The voice-input pipeline (Sprint v2 Prompt 1) is the first user of
this module; future features add their own counters and histograms
here so all metric names live in one place.

The metrics are no-op safe: if ``prometheus_client`` is not
installed, the helpers degrade to in-memory counters that tests can
inspect via :func:`get_metric_snapshot`.
"""

import logging
import threading
from collections import defaultdict
from typing import Any

logger = logging.getLogger("methean.observability")

try:
    from prometheus_client import Counter, Histogram  # type: ignore[import-untyped]

    _PROM_AVAILABLE = True
except ImportError:  # pragma: no cover - tested in non-prom envs
    _PROM_AVAILABLE = False

    class Counter:  # type: ignore[no-redef]
        def __init__(self, *_a: Any, **_k: Any) -> None:
            pass

        def labels(self, **_k: Any) -> Counter:
            return self

        def inc(self, _v: float = 1) -> None:
            pass

    class Histogram:  # type: ignore[no-redef]
        def __init__(self, *_a: Any, **_k: Any) -> None:
            pass

        def labels(self, **_k: Any) -> Histogram:
            return self

        def observe(self, _v: float) -> None:
            pass


# In-memory mirror so tests can assert metric emission without
# scraping Prometheus.
_lock = threading.Lock()
_counters: dict[tuple[str, tuple[tuple[str, str], ...]], float] = defaultdict(float)
_histograms: dict[tuple[str, tuple[tuple[str, str], ...]], list[float]] = defaultdict(list)


def _record_counter(name: str, labels: dict[str, str], inc: float = 1) -> None:
    with _lock:
        _counters[(name, tuple(sorted(labels.items())))] += inc


def _record_histogram(name: str, labels: dict[str, str], value: float) -> None:
    with _lock:
        _histograms[(name, tuple(sorted(labels.items())))].append(value)


def get_metric_snapshot() -> dict[str, Any]:
    """Test helper: return a deep copy of the in-memory mirror."""
    with _lock:
        return {
            "counters": {k: v for k, v in _counters.items()},
            "histograms": {k: list(v) for k, v in _histograms.items()},
        }


def reset_metrics_for_tests() -> None:
    """Clear the in-memory mirror. Tests call this in fixtures."""
    with _lock:
        _counters.clear()
        _histograms.clear()


# ── Voice metrics ────────────────────────────────────────────────

voice_transcription_total = Counter(
    "voice_transcription_total",
    "Transcription requests by provider and outcome",
    ["provider", "outcome"],
)
voice_transcription_duration_seconds = Histogram(
    "voice_transcription_duration_seconds",
    "End-to-end transcription latency",
    ["provider"],
    buckets=(0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0),
)
voice_audio_duration_seconds = Histogram(
    "voice_audio_duration_seconds",
    "Submitted audio clip durations",
    ["provider"],
    buckets=(0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 60.0),
)
voice_safety_intervention_total = Counter(
    "voice_safety_intervention_total",
    "Transcripts that triggered a safety intervention",
    ["intervention_kind"],
)
voice_provider_retry_total = Counter(
    "voice_provider_retry_total",
    "Whisper provider retry attempts",
    ["provider", "outcome"],
)


def observe_transcription(
    *,
    provider: str,
    outcome: str,
    duration_seconds: float,
    latency_ms: float,
) -> None:
    """Bump the counters + histograms for one transcription event."""
    labels = {"provider": provider, "outcome": outcome}
    voice_transcription_total.labels(**labels).inc()
    voice_transcription_duration_seconds.labels(provider=provider).observe(latency_ms / 1000.0)
    voice_audio_duration_seconds.labels(provider=provider).observe(duration_seconds)
    _record_counter("voice_transcription_total", labels)
    _record_histogram("voice_transcription_duration_seconds", {"provider": provider}, latency_ms / 1000.0)
    _record_histogram("voice_audio_duration_seconds", {"provider": provider}, duration_seconds)


def observe_safety_intervention(*, intervention_kind: str) -> None:
    voice_safety_intervention_total.labels(intervention_kind=intervention_kind).inc()
    _record_counter("voice_safety_intervention_total", {"intervention_kind": intervention_kind})


def observe_provider_retry(*, provider: str, outcome: str) -> None:
    voice_provider_retry_total.labels(provider=provider, outcome=outcome).inc()
    _record_counter("voice_provider_retry_total", {"provider": provider, "outcome": outcome})


# ── TTS metrics (Sprint v2 Prompt 2) ──────────────────────────────


tts_request_total = Counter(
    "tts_request_total",
    "TTS requests by provider, persona, and outcome",
    ["provider", "persona_id", "outcome"],
)
tts_first_chunk_latency_ms = Histogram(
    "tts_first_chunk_latency_ms",
    "Server-side latency from request to first audio chunk yielded",
    ["provider", "persona_id"],
    buckets=(50, 100, 200, 400, 800, 1500, 3000, 6000),
)
tts_total_duration_seconds = Histogram(
    "tts_total_duration_seconds",
    "Total audio duration generated per request",
    ["provider", "persona_id"],
    buckets=(0.25, 0.5, 1.0, 2.0, 5.0, 10.0),
)
tts_cache_hit_total = Counter(
    "tts_cache_hit_total",
    "Cache hits by phrase key",
    ["phrase_key"],
)


def observe_tts_request(
    *,
    provider: str,
    persona_id: str,
    outcome: str,
    first_chunk_latency_ms: float | None,
    duration_seconds: float,
) -> None:
    labels = {"provider": provider, "persona_id": persona_id, "outcome": outcome}
    tts_request_total.labels(**labels).inc()
    if first_chunk_latency_ms is not None:
        tts_first_chunk_latency_ms.labels(provider=provider, persona_id=persona_id).observe(first_chunk_latency_ms)
    tts_total_duration_seconds.labels(provider=provider, persona_id=persona_id).observe(duration_seconds)
    _record_counter("tts_request_total", labels)
    if first_chunk_latency_ms is not None:
        _record_histogram(
            "tts_first_chunk_latency_ms",
            {"provider": provider, "persona_id": persona_id},
            first_chunk_latency_ms,
        )
    _record_histogram(
        "tts_total_duration_seconds",
        {"provider": provider, "persona_id": persona_id},
        duration_seconds,
    )


def observe_tts_cache_hit(*, phrase_key: str) -> None:
    tts_cache_hit_total.labels(phrase_key=phrase_key).inc()
    _record_counter("tts_cache_hit_total", {"phrase_key": phrase_key})
