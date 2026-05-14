"""TTS provider abstraction + cache + phrase allowlist.

Voice output (Sprint v2 Prompt 2). The companion speaks tutor text
aloud in the kid's chosen persona voice. The cache is global (no
RLS) and stores only phrases on the explicit allowlist; everything
personalized is streamed direct to the client.
"""

from app.services.tts.base import TTSClient, TTSError
from app.services.tts.factory import get_tts_client
from app.services.tts.phrase_allowlist import cache_key, is_cacheable, normalize_phrase

__all__ = [
    "TTSClient",
    "TTSError",
    "cache_key",
    "get_tts_client",
    "is_cacheable",
    "normalize_phrase",
]
