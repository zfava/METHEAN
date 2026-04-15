"""Tests for the AI gateway circuit breaker."""

import time

from app.ai.gateway import CircuitBreaker


class TestCircuitBreaker:
    def test_circuit_starts_closed(self):
        cb = CircuitBreaker()
        assert cb.state == "closed"
        assert cb.should_allow() is True

    def test_circuit_opens_after_threshold(self):
        cb = CircuitBreaker(failure_threshold=3)
        cb.record_failure()
        cb.record_failure()
        assert cb.state == "closed"
        cb.record_failure()
        assert cb.state == "open"

    def test_open_circuit_blocks_requests(self):
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=60)
        cb.record_failure()
        cb.record_failure()
        assert cb.state == "open"
        assert cb.should_allow() is False

    def test_circuit_transitions_to_half_open(self):
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0)
        cb.record_failure()
        cb.record_failure()
        assert cb.state == "open"
        # Recovery timeout is 0, so immediately transitions
        assert cb.should_allow() is True
        assert cb.state == "half_open"

    def test_half_open_closes_on_success(self):
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0)
        cb.record_failure()
        cb.record_failure()
        cb.should_allow()  # transitions to half_open
        assert cb.state == "half_open"
        cb.record_success()
        assert cb.state == "closed"
        assert len(cb.failures) == 0

    def test_half_open_reopens_on_failure(self):
        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0)
        cb.record_failure()
        cb.record_failure()
        cb.should_allow()  # half_open
        assert cb.state == "half_open"
        cb.record_failure()
        assert cb.state == "open"

    def test_old_failures_outside_window_ignored(self):
        cb = CircuitBreaker(failure_threshold=3, window=1)
        cb.failures = [time.monotonic() - 10, time.monotonic() - 10]  # old failures
        cb.record_failure()  # only 1 recent failure
        assert cb.state == "closed"

    def test_success_in_closed_state_prunes(self):
        cb = CircuitBreaker(failure_threshold=5, window=1)
        cb.failures = [time.monotonic() - 10, time.monotonic() - 10]  # old
        cb.record_success()
        assert len(cb.failures) == 0  # pruned

    def test_status_property(self):
        cb = CircuitBreaker()
        s = cb.status
        assert s["state"] == "closed"
        assert s["failures_in_window"] == 0
