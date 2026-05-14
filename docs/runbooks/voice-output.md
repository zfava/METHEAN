# Voice Output Runbook

Operational notes for the companion-voice (TTS) pipeline.

## Diagnose "companion not speaking"

1. **Parent policy off?** Check
   ``personalization_policy.voice_output_enabled``.
2. **Cap reached?** Query:
   ```sql
   SELECT u.usage_date,
          u.tts_seconds_used,
          (p.voice_output_minutes_daily_cap * 60) AS cap_seconds
   FROM voice_usage_daily u
   LEFT JOIN personalization_policy p ON p.household_id = u.household_id
   WHERE u.child_id = '<uuid>'
   ORDER BY u.usage_date DESC LIMIT 3;
   ```
3. **Session muted?** The kid may have toggled the in-chat
   speaker icon. Stored in ``sessionStorage`` under
   ``tutor_voice_muted``; clears on tab close.
4. **Autoplay blocked?** Many browsers reject programmatic
   ``Audio.play()`` until the first user gesture. The hook surfaces
   ``error`` from ``useTutorVoice``; TutorChat renders a small "tap
   to hear" affordance in a follow-up.
5. **Provider down?** Check ``/metrics``: a high
   ``tts_request_total{outcome="error"}`` rate over 5 minutes is the
   page-operator signal.

## Cache hits

```sql
SELECT text_hash, voice_id, provider, access_count, last_accessed_at
FROM tts_cache ORDER BY access_count DESC LIMIT 20;
```

Eviction is currently manual; the LRU job is wired but not
scheduled. Until automatic eviction lands, run ad-hoc:

```sql
DELETE FROM tts_cache WHERE last_accessed_at < now() - interval '90 days';
```

## Alert thresholds

- TTS error rate over 2% for 5 minutes ➜ page.
- First-chunk P95 latency over 1500ms for 5 minutes ➜ page.
- Cache hit rate under 20% over 1000 requests ➜ review the phrase
  allowlist; common phrases may be missing.

## Rollback

Immediate kill-switch:
```sql
UPDATE personalization_policy SET voice_output_enabled = false;
```

Cache table can be cleared without functional impact (entries
regenerate on demand):
```sql
TRUNCATE TABLE tts_cache;
```
