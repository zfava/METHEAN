# Celery Queue Issues

Last verified: 2026-04-17 (beat schedule verified in test_task_coverage.py; production queue monitoring not yet exercised)

## Beat Schedule

12 scheduled tasks run via Celery Beat (see `app/tasks/worker.py`):

| Schedule | Task | Safe to Replay |
|---|---|---|
| Nightly (configurable) | nightly_decay_task | Yes (idempotent) |
| Sunday 00:00 | weekly_snapshot_task | Yes (idempotent, dedup by week) |
| Sunday 02:00 | fsrs_optimize_task | Yes (recompute is idempotent) |
| Daily 03:00 | temporal_triggers_task | Yes (triggered_at prevents re-fire) |
| Monday 05:00 | curriculum_eval_task | Yes (week completion is idempotent) |
| Daily 07:00 | check_alerts_task | Yes (alert dedup in place) |
| Daily 07:15 | daily_summary_task | NO (sends duplicate emails) |
| Sunday 18:00 | weekly_digest_task | NO (sends duplicate emails) |
| Nightly 03:30 | calibration_nightly_task | Yes (recompute is idempotent) |
| Nightly 04:00 | style_vector_nightly_task | Yes (recompute is idempotent) |
| Nightly 04:30 | family_intelligence_nightly_task | Yes (dedup by pattern + window) |
| Daily 05:00 | wellbeing_detection_task | Yes (dedup by anomaly type + 14-day window) |

## Detection

### Stuck Queue

```bash
# Check Redis queue lengths
redis-cli LLEN celery

# Check active/reserved/scheduled tasks
celery -A app.tasks.worker inspect active
celery -A app.tasks.worker inspect reserved
celery -A app.tasks.worker inspect scheduled
```

### Worker Down

```bash
# Check if any workers are connected
celery -A app.tasks.worker inspect ping

# Check worker status
celery -A app.tasks.worker status
```

### Beat Not Running

```bash
# Check if beat has sent recent tasks
redis-cli KEYS "celery-task-meta-*" | head -5

# Check beat's last heartbeat
# (If using flower: http://localhost:5555/dashboard)
```

## Draining a Stuck Queue

```bash
# Purge all pending tasks (CAUTION: tasks are lost)
celery -A app.tasks.worker purge

# Purge only a specific queue
celery -A app.tasks.worker purge -Q celery
```

Only purge if:
- The tasks are all retryable (check the "Safe to Replay" column above)
- The queue is growing faster than workers can consume
- A bad deploy sent thousands of invalid tasks

## Replaying Failed Tasks

```bash
# Check for failed tasks in the result backend
redis-cli KEYS "celery-task-meta-*" | while read key; do
  status=$(redis-cli HGET "$key" status)
  [ "$status" = "FAILURE" ] && echo "$key: $status"
done

# Manually trigger a specific task
celery -A app.tasks.worker call app.tasks.worker.nightly_decay_task

# Trigger with arguments (for tasks that take args)
celery -A app.tasks.worker call app.tasks.worker.enrich_map_task --args='["<map_id>","<household_id>"]'
```

## Safe vs. Unsafe Replay

**Safe to replay** (idempotent): decay, snapshots, optimizer, temporal triggers, curriculum eval, alerts, calibration, style vectors, family intelligence, wellbeing

**NOT safe to replay** (side effects): daily_summary (sends emails), weekly_digest (sends emails), enrich_map (may duplicate AI calls and cost)

For email tasks, check if the email was already sent before replaying:
```bash
psql -c "SELECT * FROM notification_logs WHERE created_at > NOW() - INTERVAL '1 hour' ORDER BY created_at DESC LIMIT 10;"
```

## Restarting Workers

```bash
# Graceful restart (finishes current tasks)
celery -A app.tasks.worker control shutdown

# Hard restart via hosting provider
railway service restart worker

# Verify workers are back
celery -A app.tasks.worker status
```
