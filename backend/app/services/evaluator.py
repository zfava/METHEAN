"""Mock evaluator for attempt assessment.

This module provides a mock evaluator that returns a confidence score
for a child's attempt at an activity. The real AI evaluator will be
wired in Session 4 — this mock is configurable for testing.
"""

import random


class MockEvaluator:
    """Mock evaluator returning a configurable confidence score."""

    def __init__(self, default_confidence: float = 0.7):
        self.default_confidence = default_confidence

    def evaluate(
        self,
        score: float | None = None,
        **kwargs,
    ) -> float:
        """Return a confidence score (0-1).

        If score is provided directly, use it as confidence.
        Otherwise return the default.
        """
        if score is not None:
            return max(0.0, min(1.0, score))
        return self.default_confidence


# Singleton for use across the app
mock_evaluator = MockEvaluator()
