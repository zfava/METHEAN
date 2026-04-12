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
from enum import StrEnum

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.enums import AIRunStatus
from app.models.operational import AIRun


class AIRole(StrEnum):
    planner = "planner"
    tutor = "tutor"
    evaluator = "evaluator"
    advisor = "advisor"
    cartographer = "cartographer"
    education_architect = "education_architect"
    content_architect = "content_architect"
    curriculum_mapper = "curriculum_mapper"


class AIProvider(StrEnum):
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
    philosophical_profile: dict | None = None,
    assembled_context: str | None = None,
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

    # Budget check before calling any provider
    try:
        from app.services.usage import UsageLimitExceeded, check_budget

        budget = await check_budget(db, household_id)
        if not budget["allowed"]:
            ai_run_stub = AIRun(
                household_id=household_id,
                triggered_by=triggered_by,
                run_type=role.value,
                status=AIRunStatus.failed,
                error_message="Monthly AI usage limit reached",
                started_at=datetime.now(UTC),
                completed_at=datetime.now(UTC),
            )
            db.add(ai_run_stub)
            await db.flush()
            raise UsageLimitExceeded("Monthly AI token budget exhausted. Resets on your next billing period.")
    except UsageLimitExceeded:
        raise
    except Exception:
        pass  # Budget check failure should not block AI calls

    # Inject philosophical constraints into the system prompt
    from app.ai.prompts import build_philosophical_constraints

    constraints = build_philosophical_constraints(philosophical_profile)
    if constraints:
        system_prompt = system_prompt + "\n" + constraints

    # Create AIRun record
    input_log = {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "role": role.value,
        "expected_json": expected_json,
    }
    if assembled_context:
        input_log["assembled_context"] = assembled_context

    ai_run = AIRun(
        household_id=household_id,
        triggered_by=triggered_by,
        run_type=role.value,
        status=AIRunStatus.running,
        input_data=input_log,
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

    # Record usage for billing
    try:
        from app.services.usage import record_usage

        if input_tokens or output_tokens:
            await record_usage(
                db,
                household_id,
                ai_run.id,
                input_tokens,
                output_tokens,
                model_used or "unknown",
                role.value,
            )
    except Exception:
        pass  # Usage recording should not break AI response

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
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
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
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
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
            "content": json.dumps(
                {
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
                }
            )
        },
        AIRole.tutor: {
            "content": json.dumps(
                {
                    "message": "That's a great start! Can you tell me more about how you arrived at that answer? What steps did you take?",
                    "hints": ["Think about the relationship between the parts"],
                    "encouragement": True,
                }
            )
        },
        AIRole.evaluator: {
            "content": json.dumps(
                {
                    "quality_rating": 3,
                    "confidence_score": 0.65,
                    "strengths": ["Shows understanding of core concepts", "Good effort and persistence"],
                    "areas_for_improvement": ["Could show more detailed work", "Review prerequisite concepts"],
                    "evidence_summary": "Student demonstrated developing understanding with room for growth",
                }
            )
        },
        AIRole.advisor: {
            "content": json.dumps(
                {
                    "summary": "This week showed steady progress across enrolled subjects.",
                    "highlights": ["Completed all scheduled activities", "Improved mastery in key areas"],
                    "concerns": ["Some review items are overdue for spaced repetition"],
                    "recommended_focus": ["Prioritize overdue review items", "Continue current pace"],
                }
            )
        },
        AIRole.cartographer: {
            "content": json.dumps(
                {
                    "difficulty_adjustments": [],
                    "suggested_additions": [],
                    "suggested_removals": [],
                    "estimated_weeks": 12,
                    "rationale": "Current map structure is appropriate for the child's level",
                }
            )
        },
        AIRole.education_architect: {
            "content": json.dumps(
                {
                    "plan_name": "Classical Education Plan",
                    "philosophy_alignment": "This plan follows the classical trivium model",
                    "year_plans": {
                        "2026-2027": {
                            "grade": "1st",
                            "developmental_stage": "Grammar Stage",
                            "subjects": [
                                {
                                    "subject": "Phonics & Reading",
                                    "priority": "core",
                                    "hours_per_week": 5,
                                    "description": "Systematic phonics through reading fluency",
                                    "approach": "Explicit phonics instruction with decodable texts",
                                },
                                {
                                    "subject": "Mathematics",
                                    "priority": "core",
                                    "hours_per_week": 4,
                                    "description": "Number sense through single-digit operations",
                                    "approach": "Concrete manipulatives progressing to abstract",
                                },
                                {
                                    "subject": "Handwriting & Copywork",
                                    "priority": "core",
                                    "hours_per_week": 2,
                                    "description": "Letter formation and penmanship",
                                    "approach": "Daily copywork from quality literature",
                                },
                                {
                                    "subject": "History & Bible",
                                    "priority": "core",
                                    "hours_per_week": 3,
                                    "description": "Ancient civilizations and Old Testament narratives",
                                    "approach": "Narration-based with timeline building",
                                },
                                {
                                    "subject": "Nature Study",
                                    "priority": "enrichment",
                                    "hours_per_week": 2,
                                    "description": "Seasonal nature observation and journaling",
                                    "approach": "Weekly nature walks with field guides",
                                },
                                {
                                    "subject": "Music & Art",
                                    "priority": "enrichment",
                                    "hours_per_week": 2,
                                    "description": "Hymn singing, folk songs, and drawing fundamentals",
                                    "approach": "Integration with history period studied",
                                },
                            ],
                            "total_hours_per_week": 18,
                            "milestones": ["Reading chapter books independently", "Addition/subtraction to 20"],
                            "notes": "Focus on building strong reading foundation",
                        },
                        "2027-2028": {
                            "grade": "2nd",
                            "developmental_stage": "Grammar Stage",
                            "subjects": [
                                {
                                    "subject": "Reading & Literature",
                                    "priority": "core",
                                    "hours_per_week": 5,
                                    "description": "Transition from learning to read to reading to learn",
                                    "approach": "Living books with oral narration",
                                },
                                {
                                    "subject": "Mathematics",
                                    "priority": "core",
                                    "hours_per_week": 4,
                                    "description": "Place value, multi-digit addition/subtraction, intro multiplication",
                                    "approach": "Mastery-based with concrete to pictorial to abstract",
                                },
                                {
                                    "subject": "Writing & Grammar",
                                    "priority": "core",
                                    "hours_per_week": 3,
                                    "description": "Sentence construction and basic grammar",
                                    "approach": "Copywork progressing to dictation",
                                },
                                {
                                    "subject": "History",
                                    "priority": "core",
                                    "hours_per_week": 3,
                                    "description": "Ancient Greece and Rome",
                                    "approach": "Story-based with primary source excerpts",
                                },
                                {
                                    "subject": "Science",
                                    "priority": "core",
                                    "hours_per_week": 2,
                                    "description": "Life science: plants, animals, habitats",
                                    "approach": "Observation-based with nature journal",
                                },
                                {
                                    "subject": "Latin Roots",
                                    "priority": "enrichment",
                                    "hours_per_week": 1,
                                    "description": "Introduction to Latin vocabulary roots",
                                    "approach": "Vocabulary building through word origins",
                                },
                            ],
                            "total_hours_per_week": 18,
                            "milestones": ["Fluent oral narration", "Multiplication facts to 5"],
                            "notes": "Continue building fluency while introducing more subjects",
                        },
                        "2028-2029": {
                            "grade": "3rd",
                            "developmental_stage": "Grammar Stage",
                            "subjects": [
                                {
                                    "subject": "Literature",
                                    "priority": "core",
                                    "hours_per_week": 4,
                                    "description": "Classic children's literature and mythology",
                                    "approach": "Independent reading with written narration",
                                },
                                {
                                    "subject": "Mathematics",
                                    "priority": "core",
                                    "hours_per_week": 5,
                                    "description": "Multiplication/division mastery, fractions introduction",
                                    "approach": "Mastery-based with word problem emphasis",
                                },
                                {
                                    "subject": "Writing",
                                    "priority": "core",
                                    "hours_per_week": 3,
                                    "description": "Paragraph construction and creative writing",
                                    "approach": "Dictation, short compositions, journal writing",
                                },
                                {
                                    "subject": "History",
                                    "priority": "core",
                                    "hours_per_week": 3,
                                    "description": "Middle Ages through Renaissance",
                                    "approach": "Living books, timeline, and map work",
                                },
                                {
                                    "subject": "Science",
                                    "priority": "core",
                                    "hours_per_week": 3,
                                    "description": "Earth science and astronomy",
                                    "approach": "Experiments and observation with science notebook",
                                },
                                {
                                    "subject": "Latin",
                                    "priority": "enrichment",
                                    "hours_per_week": 2,
                                    "description": "Formal Latin grammar introduction",
                                    "approach": "Systematic grammar with vocabulary building",
                                },
                            ],
                            "total_hours_per_week": 20,
                            "milestones": ["Written narration fluency", "All multiplication facts memorized"],
                            "notes": "Transition year: increasing independence and written output",
                        },
                    },
                    "transitions": [
                        {
                            "from_year": "2026-2027",
                            "to_year": "2027-2028",
                            "description": "Reading shifts from learning-to-read to reading-to-learn. Writing begins.",
                        },
                        {
                            "from_year": "2027-2028",
                            "to_year": "2028-2029",
                            "description": "Oral narration transitions to written. Latin formalized. More independent work.",
                        },
                    ],
                    "graduation_pathway": "This plan builds toward college-preparatory classical education with strong humanities foundation",
                    "rationale": "Designed for the Grammar Stage of the trivium, emphasizing memorization, narration, and foundational skills",
                }
            )
        },
    }
    mock_responses[AIRole.content_architect] = {
        "content": json.dumps(
            {
                "learning_objectives": [
                    "Identify and produce letter sounds for all 26 letters",
                    "Blend CVC words (consonant-vowel-consonant) independently",
                ],
                "teaching_guidance": {
                    "introduction": "Begin with familiar letter sounds the child already knows, then introduce new ones in groups of 3-4",
                    "practice_activities": ["Sound sorting games", "Blending chains", "Dictation exercises"],
                    "common_misconceptions": ["Confusing similar sounds (b/d, p/q)", "Skipping the blending step"],
                    "scaffolding_sequence": ["Single sounds", "Two-sound blends", "CVC words", "CCVC words"],
                    "socratic_questions": [
                        "What sound does this letter make?",
                        "Can you hear the difference between these two words?",
                    ],
                    "real_world_connections": ["Reading signs on walks", "Sounding out names of family members"],
                },
                "assessment_criteria": {
                    "mastery_indicators": [
                        "Produces all 26 letter sounds without hesitation",
                        "Blends 3-sound words independently",
                    ],
                    "proficiency_indicators": ["Most sounds correct with occasional self-correction"],
                    "developing_indicators": ["Produces sounds with verbal cues"],
                    "assessment_methods": ["oral response", "sound dictation", "reading decodable text"],
                    "sample_assessment_prompts": ["What sound does M make?", "Read these three words: cat, sit, run"],
                },
                "resource_guidance": {
                    "required": ["Letter tiles or cards", "Decodable readers (systematic phonics series)"],
                    "recommended": ["Whiteboard for writing practice", "Sand tray for letter formation"],
                    "philosophy_specific": {"classical": "Use copywork from quality literature alongside phonics"},
                },
                "connections": {
                    "prerequisite_skills_from_other_subjects": [],
                    "feeds_into": ["Sight Words (Reading)", "Spelling (Writing)"],
                    "parallel_topics": ["Handwriting (Letter Formation)"],
                },
                "accommodations": {
                    "dyslexia": "Use multisensory approach: see, say, trace, write. Extra time on blending.",
                    "adhd": "Keep sessions to 10-15 minutes. Use movement between sound groups.",
                    "gifted": "Accelerate to multisyllabic words. Introduce word origins.",
                    "visual_learner": "Color-code vowels and consonants differently.",
                    "kinesthetic_learner": "Form letters in sand, use body movements for sounds.",
                    "auditory_learner": "Emphasize rhyming and sound discrimination games.",
                },
                "time_estimates": {
                    "first_exposure": 20,
                    "practice_session": 15,
                    "review_session": 10,
                    "estimated_sessions_to_mastery": 8,
                },
            }
        )
    }
    mock_responses[AIRole.curriculum_mapper] = {
        "content": json.dumps(
            {
                "source_material": "Example Curriculum",
                "current_position": {"ref": "unit-3", "status": "in_progress"},
                "nodes_already_mastered": ["root", "unit-1", "unit-2"],
                "nodes": [
                    {"ref": "root", "node_type": "root", "title": "Curriculum Root", "sort_order": 0},
                    {
                        "ref": "unit-1",
                        "node_type": "milestone",
                        "title": "Unit 1: Foundations",
                        "sort_order": 1,
                        "description": "Chapters 1-4",
                        "estimated_minutes": 30,
                    },
                    {
                        "ref": "unit-2",
                        "node_type": "milestone",
                        "title": "Unit 2: Building Blocks",
                        "sort_order": 2,
                        "description": "Chapters 5-8",
                        "estimated_minutes": 30,
                    },
                    {
                        "ref": "unit-3",
                        "node_type": "milestone",
                        "title": "Unit 3: Application",
                        "sort_order": 3,
                        "description": "Chapters 9-12",
                        "estimated_minutes": 35,
                    },
                    {
                        "ref": "unit-4",
                        "node_type": "milestone",
                        "title": "Unit 4: Mastery",
                        "sort_order": 4,
                        "description": "Chapters 13-16",
                        "estimated_minutes": 35,
                    },
                ],
                "edges": [
                    {"from_ref": "root", "to_ref": "unit-1"},
                    {"from_ref": "unit-1", "to_ref": "unit-2"},
                    {"from_ref": "unit-2", "to_ref": "unit-3"},
                    {"from_ref": "unit-3", "to_ref": "unit-4"},
                ],
            }
        )
    }
    return mock_responses.get(role, {"content": json.dumps({"message": "Mock response"})})
