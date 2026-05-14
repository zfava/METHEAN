"""Phrase allowlist for the TTS cache.

Only phrases on this list are eligible for cache insertion. The
allowlist intentionally excludes anything personalized (no kid
names, no subject names, no math problem text) so the cache never
holds PII-bearing audio.

Adding a phrase requires a PR; the file is the governance gate.
"""

import hashlib
import re

CACHEABLE_PHRASES: frozenset[str] = frozenset(
    {
        "let me check what you wrote",
        "good thinking",
        "try that again",
        "you're getting closer",
        "tell me more about that",
        "what made you pick that answer",
        "i'm here when you're ready",
        "take your time",
        "great work",
        "let's try a different angle",
        "i can see this is tricky",
        "let's work through it together",
        "what part is confusing you",
        "nice try",
        "almost there",
        "one more try",
        "you've got this",
        "that's a great start",
        "tell me how you got that answer",
        "what step would you do first",
        "can you say more about that",
        "what do you notice",
        "what's the same",
        "what's different",
        "show me how",
        "explain that to me",
        "walk me through your thinking",
        "let's slow down for a minute",
        "what's the first thing",
        "what would you try next",
        "i like how you thought about that",
        "good question",
        "let's think about it together",
        "what does that remind you of",
        "great question",
        "you're on the right track",
        "keep going",
        "let me hear your thinking",
        "what's your guess",
        "what do you think",
        "that's interesting",
        "tell me what you tried",
        "let's check that",
        "let's read it again",
        "what makes you sure",
        "okay let's review",
        "how did you figure that out",
        "what's your next step",
        "let's pause here",
        "want a hint",
        "ready for the next one",
    }
)


_WHITESPACE = re.compile(r"\s+")
_PUNCT_TRAIL = re.compile(r"[\.\?\!,;:]+$")


def normalize_phrase(text: str) -> str:
    """Lower, single-space, strip trailing punctuation.

    Two phrases that differ only in capitalization, spacing, or a
    closing period must hash identically so cache hit rate isn't
    fragmented by typography.
    """
    cleaned = _PUNCT_TRAIL.sub("", text.strip().lower())
    return _WHITESPACE.sub(" ", cleaned)


def is_cacheable(text: str) -> bool:
    return normalize_phrase(text) in CACHEABLE_PHRASES


def cache_key(text: str, voice_id: str, provider: str) -> str:
    """SHA-256 of ``normalize_phrase(text) || voice_id || provider``."""
    payload = f"{normalize_phrase(text)}|{voice_id}|{provider}".encode()
    return hashlib.sha256(payload).hexdigest()
