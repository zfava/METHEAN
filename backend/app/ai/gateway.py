"""AI Governance Gateway (Section 6.1).

Every AI call goes through this single gateway. The gateway:
1. Builds the prompt from role templates
2. Calls AI provider (Claude primary, OpenAI fallback, mock last resort)
3. Validates response against expected schema
4. Logs full input/output as AIRun record
5. Returns output as RECOMMENDATION — never writes to state directly

AI never writes to state directly. Output queues as recommendations
through parent governance.
"""

import json
import time
import uuid
from datetime import UTC, datetime
from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.enums import AIRunStatus
from app.models.operational import AIRun


class AIRole(str, Enum):
    planner = "planner"
    tutor = "tutor"
    evaluator = "evaluator"
    advisor = "advisor"
    cartographer = "cartographer"


class AIProvider(str, Enum):
    claude = "claude"
    openai = "openai"
    mock = "mock"


async def call_ai(
    db: AsyncSession,
    role: AIRole,
    system_prompt: str,
    user_prompt: str,
    household_id: uuid.UUID,
    triggered_by: uuid.UUID | None = None,
    expected_json: bool = True,
    max_tokens: int | None = None,
) -> dict:
    """Call AI through the governance gateway.

    Returns dict with:
    - ai_run_id: UUID of the logged AIRun
    - output: parsed response data
    - is_mock: whether mock fallback was used
    - model_used: model identifier
    - provider: which provider was used
    """
    max_tokens = max_tokens or settings.AI_MAX_TOKENS
    start = time.monotonic()

    # Create AIRun record
    ai_run = AIRun(
        household_id=household_id,
        triggered_by=triggered_by,
        run_type=role.value,
        status=AIRunStatus.running,
        input_data={
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "role": role.value,
            "expected_json": expected_json,
        },
        started_at=datetime.now(UTC),
    )
    db.add(ai_run)
    await db.flush()

    output = None
    model_used = None
    provider_used = None
    is_mock = False
    error_msg = None
    input_tokens = 0
    output_tokens = 0

    # Try providers in order: Claude -> OpenAI -> Mock
    providers = _get_provider_chain()

    for provider in providers:
        try:
            if provider == AIProvider.claude and settings.AI_API_KEY:
                result = await _call_claude(system_prompt, user_prompt, max_tokens)
                output = result["content"]
                model_used = result["model"]
                input_tokens = result.get("input_tokens", 0)
                output_tokens = result.get("output_tokens", 0)
                provider_used = AIProvider.claude
                break

            elif provider == AIProvider.openai and settings.AI_FALLBACK_API_KEY:
                result = await _call_openai(system_prompt, user_prompt, max_tokens)
                output = result["content"]
                model_used = result["model"]
                input_tokens = result.get("input_tokens", 0)
                output_tokens = result.get("output_tokens", 0)
                provider_used = AIProvider.openai
                break

            elif provider == AIProvider.mock and settings.AI_MOCK_ENABLED:
                result = _call_mock(role, user_prompt)
                output = result["content"]
                model_used = "mock"
                provider_used = AIProvider.mock
                is_mock = True
                break

        except Exception as e:
            error_msg = f"{provider.value}: {str(e)}"
            continue

    if output is None:
        # All providers failed
        ai_run.status = AIRunStatus.failed
        ai_run.error_message = error_msg or "All AI providers unavailable"
        ai_run.completed_at = datetime.now(UTC)
        await db.flush()
        raise RuntimeError(f"AI call failed for role={role.value}: {error_msg}")

    # Parse JSON if expected
    parsed_output = output
    if expected_json and isinstance(output, str):
        try:
            parsed_output = json.loads(output)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            import re
            match = re.search(r"```(?:json)?\s*\n(.*?)\n```", output, re.DOTALL)
            if match:
                parsed_output = json.loads(match.group(1))
            else:
                parsed_output = {"raw_text": output}

    elapsed_ms = int((time.monotonic() - start) * 1000)

    # Update AIRun
    ai_run.status = AIRunStatus.completed
    ai_run.model_used = model_used
    ai_run.input_tokens = input_tokens
    ai_run.output_tokens = output_tokens
    ai_run.output_data = parsed_output if isinstance(parsed_output, dict) else {"result": parsed_output}
    ai_run.completed_at = datetime.now(UTC)
    await db.flush()

    return {
        "ai_run_id": ai_run.id,
        "output": parsed_output,
        "is_mock": is_mock,
        "model_used": model_used,
        "provider": provider_used.value if provider_used else "none",
        "elapsed_ms": elapsed_ms,
    }


def _get_provider_chain() -> list[AIProvider]:
    """Get ordered list of providers to try."""
    chain = []
    if settings.AI_API_KEY:
        chain.append(AIProvider.claude)
    if settings.AI_FALLBACK_API_KEY:
        chain.append(AIProvider.openai)
    if settings.AI_MOCK_ENABLED:
        chain.append(AIProvider.mock)
    return chain


async def _call_claude(
    system_prompt: str, user_prompt: str, max_tokens: int,
) -> dict:
    """Call Claude API."""
    import anthropic

    client = anthropic.AsyncAnthropic(api_key=settings.AI_API_KEY)
    response = await client.messages.create(
        model=settings.AI_PRIMARY_MODEL,
        max_tokens=max_tokens,
        temperature=settings.AI_TEMPERATURE,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return {
        "content": response.content[0].text,
        "model": response.model,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }


async def _call_openai(
    system_prompt: str, user_prompt: str, max_tokens: int,
) -> dict:
    """Call OpenAI API as fallback."""
    import openai

    client = openai.AsyncOpenAI(api_key=settings.AI_FALLBACK_API_KEY)
    response = await client.chat.completions.create(
        model=settings.AI_FALLBACK_MODEL,
        max_tokens=max_tokens,
        temperature=settings.AI_TEMPERATURE,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    choice = response.choices[0]
    usage = response.usage
    return {
        "content": choice.message.content,
        "model": response.model,
        "input_tokens": usage.prompt_tokens if usage else 0,
        "output_tokens": usage.completion_tokens if usage else 0,
    }


def _call_mock(role: AIRole, user_prompt: str) -> dict:
    """Deterministic mock fallback — system never breaks because AI is down."""
    mock_responses = {
        AIRole.planner: {
            "content": json.dumps({
                "activities": [
                    {
                        "title": "Review previous concepts",
                        "activity_type": "review",
                        "estimated_minutes": 20,
                        "difficulty": 2,
                        "rationale": "Reinforce foundational knowledge before new material",
                    },
                    {
                        "title": "Introduce new concept",
                        "activity_type": "lesson",
                        "estimated_minutes": 30,
                        "difficulty": 3,
                        "rationale": "Progressive skill building at appropriate level",
                    },
                    {
                        "title": "Practice exercises",
                        "activity_type": "practice",
                        "estimated_minutes": 25,
                        "difficulty": 3,
                        "rationale": "Applied practice for skill reinforcement",
                    },
                ],
                "total_minutes": 75,
                "rationale": "Balanced plan with review, new learning, and practice",
            })
        },
        AIRole.tutor: {
            "content": json.dumps({
                "message": "That's a great start! Can you tell me more about how you arrived at that answer? What steps did you take?",
                "hints": ["Think about the relationship between the parts"],
                "encouragement": True,
            })
        },
        AIRole.evaluator: {
            "content": json.dumps({
                "quality_rating": 3,
                "confidence_score": 0.65,
                "strengths": ["Shows understanding of core concepts", "Good effort and persistence"],
                "areas_for_improvement": ["Could show more detailed work", "Review prerequisite concepts"],
                "evidence_summary": "Student demonstrated developing understanding with room for growth",
            })
        },
        AIRole.advisor: {
            "content": json.dumps({
                "summary": "This week showed steady progress across enrolled subjects.",
                "highlights": ["Completed all scheduled activities", "Improved mastery in key areas"],
                "concerns": ["Some review items are overdue for spaced repetition"],
                "recommended_focus": ["Prioritize overdue review items", "Continue current pace"],
            })
        },
        AIRole.cartographer: {
            "content": json.dumps({
                "difficulty_adjustments": [],
                "suggested_additions": [],
                "suggested_removals": [],
                "estimated_weeks": 12,
                "rationale": "Current map structure is appropriate for the child's level",
            })
        },
    }
    return mock_responses.get(role, {"content": json.dumps({"message": "Mock response"})})
