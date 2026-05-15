"""Sentence-boundary truncator for voice-mode responses.

The voice-mode contract caps the tutor's reply at one or two
sentences regardless of what the model produced. This module is the
belt-and-suspenders enforcement: the prompt asks for brevity AND the
server clamps the output before it streams back.

Edge cases the splitter handles:

- Trailing punctuation: "Hi." vs "Hi" both count as a sentence.
- Abbreviations: "Mr. Smith said hi." is one sentence, not two.
- Question / exclamation / semicolon boundaries.
- Empty / whitespace-only input: returns "" without raising.

Limitations (documented):

- Multi-character abbreviations like "U.S.A." are conservatively
  treated as part of the surrounding sentence; the splitter does not
  attempt full NLP. A future iteration can replace this with a real
  sentence segmenter.
"""

import re

# Abbreviations that look like sentence boundaries but aren't. The
# splitter rejoins on these when the preceding token matches.
_ABBREVIATIONS = frozenset(
    {
        "mr",
        "mrs",
        "ms",
        "dr",
        "st",
        "sr",
        "jr",
        "vs",
        "etc",
        "e.g",
        "i.e",
        "u.s",
        "a.m",
        "p.m",
        "no",
        "fig",
        "vol",
        "approx",
    }
)

# Splits on terminator-then-space. The lookahead keeps the terminator
# attached to the preceding token so we can rejoin without loss.
_BOUNDARY = re.compile(r"([\.!\?;])\s+")


def truncate_to_sentences(text: str, max_sentences: int = 2) -> str:
    """Return at most ``max_sentences`` sentences from ``text``.

    The function never raises and is safe to call on any string. If
    no sentence boundary is found, the input is returned as-is.
    """
    if not text or max_sentences < 1:
        return ""

    cleaned = text.strip()
    if not cleaned:
        return ""

    parts = _split_sentences(cleaned)
    if not parts:
        return cleaned

    kept = parts[: max(1, max_sentences)]
    return " ".join(kept).strip()


def _split_sentences(text: str) -> list[str]:
    """Split with abbreviation handling.

    Strategy: split on the terminator-then-space regex, then walk the
    resulting tokens and rejoin pairs where the left side ends with a
    known abbreviation (e.g., "Mr." should not start a new sentence).
    """
    # ``re.split`` with a capture group returns interleaved
    # ``[chunk, sep, chunk, sep, ..., chunk]``. We zip pairs back into
    # ``"chunk + sep"`` tokens and then post-process for abbreviations.
    pieces = _BOUNDARY.split(text)
    if len(pieces) <= 1:
        return [pieces[0]] if pieces and pieces[0] else []

    raw: list[str] = []
    i = 0
    while i < len(pieces):
        chunk = pieces[i]
        sep = pieces[i + 1] if i + 1 < len(pieces) else ""
        if sep:
            raw.append(chunk + sep)
        elif chunk:
            raw.append(chunk)
        i += 2

    # Merge abbreviation false-positives back into the prior sentence.
    merged: list[str] = []
    for tok in raw:
        if merged and _ends_with_abbreviation(merged[-1]):
            merged[-1] = merged[-1] + " " + tok
        else:
            merged.append(tok)
    return [t.strip() for t in merged if t.strip()]


def _ends_with_abbreviation(token: str) -> bool:
    """True if ``token`` ends with a known abbreviation followed by '.'."""
    if not token.endswith("."):
        return False
    # Strip the trailing period and grab the last whitespace-delimited
    # word, lowercased.
    stripped = token[:-1].rstrip()
    last = stripped.rsplit(" ", 1)[-1] if " " in stripped else stripped
    return last.lower() in _ABBREVIATIONS
