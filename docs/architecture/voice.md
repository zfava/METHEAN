# Voice (Sprint v2)

## Overview

The voice subsystem covers two streams:

- **Voice input (Prompt 1, this document's primary focus).** Kids
  speak instead of typing. Audio is captured by the browser
  (MediaRecorder, Opus/WebM), uploaded as multipart form data, and
  transcribed server-side via OpenAI Whisper or a self-hosted
  faster-whisper service. The transcript is debited against a daily
  cap, run through a safety check, and returned to the kid.
- **Voice output** lands in Prompt 2 (companion speaks the tutor's
  reply). This document gets a TTS section in that wave.

## Data flow

```
Kid device                                        Backend
─────────────                                     ────────────────────────────────
MediaRecorder ──┐
  audio/webm    │
  opus 24 kbps  │
                ▼
        fetch POST /api/v1/children/{id}/transcribe (multipart)
                                                  │
                                                  ▼
                                          require_child_access("write")
                                                  │
                                                  ▼
                                          PersonalizationPolicy load
                                                  │
                                          (voice_input_enabled?)
                                                  │
                                                  ▼
                                          audio_validation (size, mime, duration)
                                                  │
                                                  ▼
                                          voice_usage.get_remaining_seconds
                                                  │
                                                  ▼
                                          whisper.factory.get_whisper_client
                                                  │
                                                  ▼
                                          provider.transcribe(audio_handle)
                                                  │
                                  (audio_handle = None HERE)
                                                  │
                                                  ▼
                                          voice_usage.debit_seconds (atomic)
                                                  │
                                                  ▼
                                          voice_safety.evaluate_transcript_safety
                                                  │
                                                  ▼
                                          metrics + INFO log (no audio, no transcript)
                                                  │
                                                  ▼
                                          TranscribeResponse JSON
```

## Privacy guarantees

- Audio bytes pass through memory only. The handle variable is
  named ``audio_handle`` and is explicitly dropped after the
  provider call returns. There is no DB column, no log line, and no
  audit trail that contains audio bytes.
- The integration test
  ``test_transcribe_audio_handle_not_persisted`` enforces that no
  column on ``voice_usage_daily`` (or any voice-related table) is
  bytea/text/jsonb-typed.
- Transcripts are returned to the kid, not stored server-side. The
  caller (lesson reflection, practice answer, tutor prompt) is the
  one who persists them if at all.
- Safety check operates on the in-memory transcript and emits only
  the intervention kind enum to metrics; the transcript text never
  reaches a log line at INFO level.

## Provider abstraction

```
WhisperClient (Protocol)
├── OpenAIWhisperProvider     # model="whisper-1", 10s timeout, 1 retry
└── LocalWhisperProvider      # httpx POST to LOCAL_WHISPER_URL/transcribe
```

The factory selects by ``PersonalizationPolicy.whisper_provider``;
``local`` falls back to ``openai`` on a failed cheap liveness probe.

## Cost model (OpenAI tier)

OpenAI Whisper API: $0.006/min (as of v2 launch).

| daily cap (min) | per-child monthly worst case |
|---|---|
| 30 | $5.40 |
| 60 (default) | $10.80 |
| 120 | $21.60 |

A household of 4 kids at the default cap costs ~$43/mo if every cap
is exhausted every day. Most families will use well under the cap;
operational cost is the cap-shaped ceiling, not a flat per-family
fee.

## Failure modes

See ``docs/runbooks/voice-input.md`` for the cap-and-error table.
The transcribe endpoint maps:

| failure | HTTP | kid sees |
|---|---|---|
| disabled policy | 403 | "Voice is off right now." |
| cap reached | 429 | "Voice time is up for today." |
| oversized | 413 | (client-side catches first) |
| over 60s | 422 | "Try a shorter clip." |
| under 0.5s | 422 | "Didn't catch that. Tap again?" |
| silence | 200 + is_silent | "Didn't hear anything." |
| malformed | 422 | "Tap again to retry." |
| provider 5xx (after retry) | 503 | "Voice service is having a moment." |
| safety flag | 200 + safety_intervention | wellbeing UI |

## Voice output (Sprint v2 Prompt 2)

```
Backend
─────────────
TutorChat finishes streaming text
       │
       ▼
useTutorVoice.speak(messageId, text)
       │  POST /children/{id}/tts/stream (JSON body)
       ▼
FastAPI tts.tts_stream
       │
       ▼
 policy check (voice_output_enabled?)
       │
       ▼
 persona lookup (get_voice_persona)
       │
       ▼
 prep_for_tts (sanitize, voice-mode truncate, lexicon)
       │
       ▼
 cap check (voice_output_minutes_daily_cap)
       │
       ▼
 phrase allowlist check ──── HIT ────┐
       │                              │
      MISS                            ▼
       │                       cache.lookup
       │                              │
       ▼                              ▼
 get_tts_client (factory)       stream cached bytes
       │
       ▼
 client.stream_speech (OpenAI tts-1)
       │
       ▼
 SSE chunks (base64 MP3) to client
       │
       ▼
 cache.insert if eligible
       │
       ▼
 voice_usage.debit_tts_seconds (atomic)
```

### Cache model

- Global, NOT household-scoped.
- Gated by ``phrase_allowlist.CACHEABLE_PHRASES`` (50+ generic
  phrases).
- Personalized content (kid names, problem text) NEVER reaches the
  cache; the allowlist match is the gate.
- Hit rate target: over 30% across the first 1000 requests in
  production.

### Persona mapping (OpenAI tts-1)

| persona | voice_id | speech_rate | prosody |
|---|---|---|---|
| default_warm (Sage) | nova | 0.95 | warm and unhurried |
| default_bright (Nova) | shimmer | 1.05 | bright and energetic |
| default_steady (Atlas) | onyx | 0.92 | measured and clear |
| default_playful (Pip) | fable | 1.05 | light and playful |
| default_gentle (Wren) | alloy | 0.90 | soft and patient |

### Failure modes (output)

| failure | HTTP | kid sees |
|---|---|---|
| voice_output_enabled=false | 403 | (silent; mic in chat header is visible but TTS doesn't fire) |
| cap reached | 429 | text still readable, no audio |
| unknown persona | 422 | (silent; client logs) |
| text over 4000 chars | 422 | (silent; caller should split) |
| provider 5xx after retry | 503 / SSE error event | tap-to-hear affordance |
| autoplay blocked | client-side | tap-to-hear affordance |
| client disconnect mid-stream | partial debit | next message plays normally |
