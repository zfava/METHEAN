"""Text-to-speech prep.

Sanitizes raw tutor text before it reaches a TTS provider:

1. Strip control characters.
2. Reject SSML-looking tags (callers shouldn't send them; TTS providers
   would honor angle-bracket SSML and we don't want that surface).
3. Truncate to 1-2 sentences if ``voice_mode=True`` (server-enforced).
4. Apply a small pronunciation lexicon (METHEAN -> "meh-thee-an",
   common math symbols).
5. Estimate duration for the cap-arithmetic pre-debit.
6. Decide cache eligibility against the phrase allowlist.
"""

import re
from dataclasses import dataclass

from app.content.personalization_library import VoicePersona
from app.services.tts.phrase_allowlist import cache_key, is_cacheable

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_TAG_LIKE = re.compile(r"<[a-zA-Z/][^>]*>")
_SENTENCE = re.compile(r"[\.\?\!]\s+")

# Lexicon: applied as case-insensitive whole-word substitutions.
# Phonetic spellings target the OpenAI tts-1 voices, which respond
# better to hyphenated forms than to IPA.
_LEXICON: dict[str, str] = {
    "METHEAN": "Meth-ee-an",
    "FSRS": "F S R S",
    "STT": "S T T",
    "TTS": "T T S",
    " / ": " divided by ",
    " * ": " times ",
}


class TTSPrepError(Exception):
    """Caller sent text we won't pass to a TTS provider."""

    def __init__(self, message: str, *, kind: str) -> None:
        super().__init__(message)
        self.kind = kind


@dataclass(frozen=True)
class PreppedSpeech:
    text: str
    estimated_seconds: float
    is_cacheable: bool
    cache_key_value: str | None
    voice_mode: bool


def prep_for_tts(
    raw_text: str,
    persona: VoicePersona,
    *,
    voice_mode: bool = False,
) -> PreppedSpeech:
    if raw_text is None:
        raise TTSPrepError("empty text", kind="text_empty")
    text = _CONTROL_CHARS.sub("", raw_text).strip()
    if not text:
        raise TTSPrepError("empty text", kind="text_empty")
    if len(text) > 4000:
        raise TTSPrepError("text over 4000 chars", kind="text_too_long")
    if _TAG_LIKE.search(text):
        raise TTSPrepError("tag-like content rejected", kind="text_has_tags")

    if voice_mode:
        # Keep at most 2 sentences. The split is best-effort; if the
        # text has no terminator we keep the first 200 chars.
        sentences = _SENTENCE.split(text)
        if len(sentences) > 2:
            text = ". ".join(sentences[:2]).rstrip(".") + "."
        if len(text) > 240:
            text = text[:240].rsplit(" ", 1)[0]

    for key, replacement in _LEXICON.items():
        text = re.sub(re.escape(key), replacement, text, flags=re.IGNORECASE)

    # Duration heuristic: ~3 chars/sec at speech_rate 1.0; persona
    # speech_rate scales inversely (faster rate, fewer seconds).
    chars_per_sec = 3.0 * max(0.5, persona.speech_rate)
    estimated = len(text) / chars_per_sec

    cacheable = is_cacheable(raw_text)
    key = cache_key(raw_text, persona.tts_voice_id, persona.tts_provider) if cacheable else None

    return PreppedSpeech(
        text=text,
        estimated_seconds=estimated,
        is_cacheable=cacheable,
        cache_key_value=key,
        voice_mode=voice_mode,
    )
