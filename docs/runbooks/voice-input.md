# Voice Input Runbook

Operational notes for the kid-facing voice transcription pipeline.

## Diagnose "voice not working"

1. **Parent policy off?** Check ``personalization_policy`` for the
   household; ``voice_input_enabled`` may be false.
2. **Cap reached?** Query:
   ```sql
   SELECT * FROM voice_usage_daily
   WHERE child_id = '<uuid>' AND usage_date = CURRENT_DATE;
   ```
   If ``stt_seconds_used / 60 >= voice_minutes_daily_cap`` from the
   policy, the kid sees a 429 and the CapReachedNotice replaces the
   mic in the textarea.
3. **Mic permission denied?** Browser-side; check the kid device's
   permission settings. The frontend renders PermissionDeniedNotice
   in this case.
4. **Provider down?** Hit ``OPENAI_API_KEY`` health or
   ``GET ${LOCAL_WHISPER_URL}/health``. Cloud fallback engages
   automatically when ``local`` is selected but unreachable.
5. **Metrics:** scrape ``/metrics`` and look for the
   ``voice_transcription_total{outcome="error"}`` counter; high
   error-rate triggers the operator-facing alert.

## Inspect usage per child

```sql
SELECT c.first_name,
       u.usage_date,
       u.stt_seconds_used,
       (p.voice_minutes_daily_cap * 60) AS cap_seconds
FROM voice_usage_daily u
JOIN children c ON c.id = u.child_id
LEFT JOIN personalization_policy p ON p.household_id = u.household_id
WHERE u.household_id = '<uuid>'
ORDER BY u.usage_date DESC
LIMIT 14;
```

## Common errors

| Symptom | Likely cause | Fix |
|---|---|---|
| 403 `voice_input_disabled` | parent toggled off in /governance/personalization | parent re-enables |
| 429 `voice_cap_reached` | child hit daily cap | wait until midnight or raise cap |
| 422 `audio_invalid` | corrupted/incomplete upload | retry; check WebM container |
| 503 `provider_unavailable` | OpenAI 5xx after retry | wait, dashboard alert covers persistent |
| Mic LED stays on | tab kept stream open | reload the tab; the recorder calls track.stop() on close |

## Alert thresholds

- Error rate > 2% over 5 minutes ➜ page operator.
- P95 transcription latency > 2s for 5 minutes ➜ page operator.
- Provider retry rate > 10% over 15 minutes ➜ page operator.

## Rollback

Immediate kill-switch (no deploy):
```sql
UPDATE personalization_policy SET voice_input_enabled = false;
```
The frontend hides the mic on next policy refresh (≤ 60s). For a
full rollback, revert the commit; migration 044 downgrade is safe
because ``voice_usage_daily`` is a counter, not user-authored
content.

## Incident log

(empty; new incidents go here with date, summary, mitigation)
