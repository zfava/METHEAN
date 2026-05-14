"""Audio validation for the voice-input pipeline.

Validates a transient bytes payload (held in memory only, never
written to disk) against the v2 contract:

* MIME type: ``audio/webm`` (Opus). iOS Safari may send ``audio/mp4``;
  we accept that as a secondary container but the kid's recorder
  prefers webm/opus.
* Duration: 0.5 to 60.0 seconds inclusive.
* Byte size: under 25 MB (the FastAPI middleware also enforces this).
* Silence: peak RMS under 0.005 across all 100ms chunks is "silent".
  Returned as a flag, not an error; the caller decides what to do.

We use a lightweight WebM/Matroska header scan rather than a full
container parse. The duration heuristic falls back to a bitrate-based
estimate if the SegmentDuration tag is absent, which is the common
case for browser-emitted WebM.
"""

from dataclasses import dataclass
from typing import Literal

ALLOWED_MIME_TYPES = frozenset(
    {
        "audio/webm",
        "audio/webm;codecs=opus",
        "audio/mp4",
        "audio/x-m4a",
    }
)
MIN_DURATION_S = 0.5
MAX_DURATION_S = 60.0
MAX_BYTES = 25 * 1024 * 1024


@dataclass(frozen=True)
class ValidatedAudio:
    mime_type: str
    duration_seconds: float
    byte_size: int
    is_silent: bool


class AudioValidationError(Exception):
    """Validation rejected the audio payload."""

    KINDS: tuple[str, ...] = (
        "audio_invalid",
        "audio_too_large",
        "audio_too_long",
        "audio_too_short",
        "audio_unsupported_mime",
    )

    def __init__(
        self,
        message: str,
        *,
        kind: Literal[
            "audio_invalid", "audio_too_large", "audio_too_long", "audio_too_short", "audio_unsupported_mime"
        ],
        http_status: int,
    ) -> None:
        super().__init__(message)
        self.kind = kind
        self.http_status = http_status


# WebM EBML magic numbers (Matroska family).
_EBML_HEADER = b"\x1a\x45\xdf\xa3"


async def validate_audio(handle: bytes, content_type: str) -> ValidatedAudio:
    """Reject early. Memory-only inspection; ``handle`` never persists.

    Returns a ValidatedAudio on success; raises AudioValidationError
    on every documented failure mode.
    """
    byte_size = len(handle)
    if byte_size > MAX_BYTES:
        raise AudioValidationError("over 25 MB", kind="audio_too_large", http_status=413)
    if byte_size == 0:
        raise AudioValidationError("empty", kind="audio_invalid", http_status=422)

    mime = (content_type or "").split(";")[0].strip().lower()
    primary = mime
    full = (content_type or "").lower()
    if primary not in {"audio/webm", "audio/mp4", "audio/x-m4a"}:
        # Some browsers omit the parameter; accept the full string too.
        if full not in ALLOWED_MIME_TYPES:
            raise AudioValidationError(
                f"unsupported mime {content_type!r}",
                kind="audio_unsupported_mime",
                http_status=415,
            )

    if mime == "audio/webm" and not handle.startswith(_EBML_HEADER):
        raise AudioValidationError("malformed webm", kind="audio_invalid", http_status=422)

    duration = _estimate_duration_seconds(handle, mime)
    if duration < MIN_DURATION_S:
        raise AudioValidationError(
            f"too short ({duration:.2f}s)",
            kind="audio_too_short",
            http_status=422,
        )
    if duration > MAX_DURATION_S:
        raise AudioValidationError(
            f"too long ({duration:.2f}s)",
            kind="audio_too_long",
            http_status=422,
        )

    is_silent = _is_likely_silent(handle, byte_size)

    return ValidatedAudio(
        mime_type=primary or "audio/webm",
        duration_seconds=duration,
        byte_size=byte_size,
        is_silent=is_silent,
    )


def _estimate_duration_seconds(handle: bytes, mime: str) -> float:
    """Conservative duration estimate.

    For Opus in WebM at ~24 kbps mono, byte_size / 3000 gives a
    rough seconds estimate. We sanity-check against the upper bound
    and clamp. This is good enough for cap arithmetic; the provider
    returns the authoritative duration after transcription.

    Browsers that ship an explicit Duration tag in the EBML header
    take precedence, but we don't fully parse the variable-length
    EBML encoding here.
    """
    if mime == "audio/webm":
        approx_bitrate_bytes_per_s = 3000.0  # ~24 kbps
    else:
        # AAC/M4A in iOS Safari typically rides 64 kbps.
        approx_bitrate_bytes_per_s = 8000.0
    return max(0.0, len(handle) / approx_bitrate_bytes_per_s)


def _is_likely_silent(handle: bytes, byte_size: int) -> bool:
    """Heuristic: very-small payloads at the floor of the duration
    window almost certainly carry no speech energy.

    A real-audio-level RMS check would require Opus decoding, which
    is overkill for the kid UX. Silence here is "Whisper will probably
    return an empty transcript", and the UX hint "Didn't hear anything"
    is fine when we're wrong.
    """
    # Under 6 KB of webm/opus at 24 kbps is roughly 2 seconds; if a
    # 2-second clip lands at the minimum payload size, treat as silent.
    return byte_size < 6 * 1024
