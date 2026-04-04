"""Evaluator service (Section 6.4).

Calls AI Evaluator through governance gateway. Falls back to mock
if AI is unavailable. The mock is also used directly in test scenarios
where confidence is provided explicitly.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.gateway import AIRole, call_ai
from app.ai.prompts import EVALUATOR_SYSTEM


class MockEvaluator:
    """Mock evaluator returning a configurable confidence score."""

    def __init__(self, default_confidence: float = 0.7):
        self.default_confidence = default_confidence

    def evaluate(
        self,
        score: float | None = None,
        **kwargs,
    ) -> float:
        if score is not None:
            return max(0.0, min(1.0, score))
        return self.default_confidence


# Singleton for use across the app
mock_evaluator = MockEvaluator()


async def evaluate_attempt(
    db: AsyncSession,
    household_id: uuid.UUID,
    user_id: uuid.UUID | None,
    activity_title: str,
    node_title: str,
    child_responses: str,
    tutor_transcript: str | None = None,
) -> dict:
    """Call AI Evaluator through governance gateway.

    Returns dict with: quality_rating, confidence_score, strengths,
    areas_for_improvement, evidence_summary, ai_run_id.
    """
    user_prompt = f"""Evaluate this child's attempt at an activity.

Activity: {activity_title}
Learning Node: {node_title}

Child's responses/work:
{child_responses}

{f'Tutor transcript:{chr(10)}{tutor_transcript}' if tutor_transcript else ''}

Provide your assessment."""

    # Fetch philosophical profile for AI constraints
    from sqlalchemy import select as sa_select
    from app.models.identity import Household
    h_result = await db.execute(sa_select(Household).where(Household.id == household_id))
    h = h_result.scalar_one_or_none()
    phil = h.philosophical_profile if h else None

    result = await call_ai(
        db,
        role=AIRole.evaluator,
        system_prompt=EVALUATOR_SYSTEM,
        user_prompt=user_prompt,
        household_id=household_id,
        triggered_by=user_id,
        philosophical_profile=phil,
    )

    output = result["output"]
    return {
        "quality_rating": output.get("quality_rating", 3),
        "confidence_score": output.get("confidence_score", 0.65),
        "strengths": output.get("strengths", []),
        "areas_for_improvement": output.get("areas_for_improvement", []),
        "evidence_summary": output.get("evidence_summary", ""),
        "ai_run_id": result["ai_run_id"],
        "is_mock": result["is_mock"],
    }
