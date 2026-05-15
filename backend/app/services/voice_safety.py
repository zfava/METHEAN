"""Voice-input safety check.

Runs over the transcript AFTER transcription but BEFORE returning
text to the kid. If a risk signal fires, the transcribe endpoint
flags ``safety_intervention=true`` and the frontend routes to the
wellbeing UI instead of writing the transcript into the textarea.

The transcript text is never logged in this path; only the
intervention kind enum value leaves the function via metrics.

v2 scope: a curated keyword list seeded by a small set of distress
phrases. A future iteration replaces this with the wellbeing
detection engine's free-text channel once that channel exists; the
existing engine (``app.services.wellbeing_detection``) operates on
engagement signals, not transcript content.
"""

import re
import uuid
from dataclasses import dataclass
from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession

InterventionKind = Literal["distress_signal", "self_harm_keyword", "unsafe_disclosure"]


@dataclass(frozen=True)
class SafetyVerdict:
    safe: bool
    intervention_kind: InterventionKind | None
    suggested_response: str | None


# Curated keyword patterns. The lists are intentionally short for v2;
# false positives are preferable to false negatives here (a parent-
# notified wellbeing intervention is always recoverable, an unsurfaced
# distress signal is not).
_DISTRESS_PHRASES: tuple[str, ...] = (
    "i hate everything",
    "i hate myself",
    "i want to die",
    "nobody likes me",
    "nobody loves me",
    "everyone hates me",
    "i give up",
)
_SELF_HARM_KEYWORDS: tuple[str, ...] = (
    "kill myself",
    "kill me",
    "hurt myself",
    "end it all",
    "cut myself",
)
_UNSAFE_DISCLOSURE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bmy address is\b", re.IGNORECASE),
    re.compile(r"\bmy phone number is\b", re.IGNORECASE),
    re.compile(r"\bmy school is\b", re.IGNORECASE),
    re.compile(r"\bi live (at|on)\b", re.IGNORECASE),
)


async def evaluate_transcript_safety(
    db: AsyncSession,
    *,
    child_id: uuid.UUID,
    transcript: str,
) -> SafetyVerdict:
    """Classify a transcript without ever logging it.

    The ``db`` and ``child_id`` parameters are present so future
    iterations can read child-specific risk thresholds without
    breaking the API surface.
    """
    if not transcript:
        return SafetyVerdict(safe=True, intervention_kind=None, suggested_response=None)

    lowered = transcript.lower()

    for phrase in _SELF_HARM_KEYWORDS:
        if phrase in lowered:
            return SafetyVerdict(
                safe=False,
                intervention_kind="self_harm_keyword",
                suggested_response=(
                    "What you said matters. I'm telling a grown-up who cares about you, and they'll come check in."
                ),
            )

    for phrase in _DISTRESS_PHRASES:
        if phrase in lowered:
            return SafetyVerdict(
                safe=False,
                intervention_kind="distress_signal",
                suggested_response=(
                    "That sounds really hard. Let's take a break together, and your parent will be here in a minute."
                ),
            )

    for pat in _UNSAFE_DISCLOSURE_PATTERNS:
        if pat.search(transcript):
            return SafetyVerdict(
                safe=False,
                intervention_kind="unsafe_disclosure",
                suggested_response=(
                    "Let's keep things like addresses and phone numbers offline. "
                    "Want to tell me about the lesson instead?"
                ),
            )

    return SafetyVerdict(safe=True, intervention_kind=None, suggested_response=None)
