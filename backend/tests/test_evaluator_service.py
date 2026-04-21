"""Tests for the Evaluator service."""

from app.services.evaluator import MockEvaluator, mock_evaluator


class TestMockEvaluator:
    def test_returns_float(self):
        result = mock_evaluator.evaluate()
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_uses_score(self):
        result = mock_evaluator.evaluate(score=0.9)
        assert result == 0.9

    def test_clamps_high_score(self):
        result = mock_evaluator.evaluate(score=1.5)
        assert result == 1.0

    def test_clamps_low_score(self):
        result = mock_evaluator.evaluate(score=-0.5)
        assert result == 0.0

    def test_default_confidence(self):
        e = MockEvaluator(default_confidence=0.8)
        assert e.evaluate() == 0.8

    def test_custom_default(self):
        e = MockEvaluator(default_confidence=0.3)
        assert e.evaluate() == 0.3
        assert e.evaluate(score=0.9) == 0.9
