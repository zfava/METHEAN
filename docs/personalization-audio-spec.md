# Personalization Audio Spec

Twelve cues across two packs. Replace the placeholder silent MP3s in `frontend/public/sounds/<pack>/<event>.mp3` with the final audio. The `off` pack ships no files; the hook short-circuits before lookup.

## Constraints

- Format: MP3, 16-bit, 44.1 kHz, mono
- Volume normalized to -16 LUFS
- No melody, no spoken word, no recognizable instrument samples
- Sources: granular synthesis, soft noise envelopes, gentle pitched tones
- File size budget: under 30 KB per cue at the soft pack, under 50 KB at the full pack

## Cue list

| Event | Soft | Full |
|---|---|---|
| activity_start | barely-there breath, ~300ms | brief pitched tone, ~400ms |
| correct | soft tick, ~150ms | warm two-note rise, ~400ms |
| hint_revealed | gentle chime, ~250ms | brighter chime, ~400ms |
| activity_complete | soft swell, ~500ms | satisfying close, ~700ms |
| mastery_up | rising sparkle, ~600ms | richer rising sparkle, ~800ms |
| day_complete | warm fade-up, ~800ms | longer warm cadence, ~1.0s |

## Naming

File names must match exactly: `activity_start.mp3`, `correct.mp3`, `hint_revealed.mp3`, `activity_complete.mp3`, `mastery_up.mp3`, `day_complete.mp3`.

## Behavioral context

The frontend plays each cue once and only after the first user gesture. Two cues within 200ms of each other collapse into one (the second is dropped). When the user has `prefers-reduced-motion: reduce` set, only `mastery_up` and `day_complete` play; the routine cues are suppressed. Cues are always advisory; a missing file or playback rejection is a silent no-op.

## Quality bar

- The cue should be audible at 50 percent system volume in a quiet room without being startling at 80 percent.
- A child should be able to tell `correct` from `hint_revealed` without seeing the screen.
- No cue should resemble a notification chime from a common messaging app.
- The soft pack should be calm enough for a shared room (sibling sleeping nearby).
- The full pack may be celebratory but never garish.

## Versioning

Producer audio replaces the placeholder files in place; the filenames are the contract. If the cue set ever expands, update both this spec and `frontend/src/lib/useSoundCue.ts` in the same PR.
