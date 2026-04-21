# Database Recovery

Last verified: UNTESTED. This runbook has not been exercised against a production database. Verify before relying on it.

## Backup Configuration

Backups depend on the hosting provider:

- **Railway**: automatic daily snapshots, 7-day retention
- **AWS RDS**: automated backups configurable to 35-day retention, point-in-time recovery
- **Self-hosted**: must configure pg_dump cron or WAL archiving manually

Check the current backup schedule:

```bash
# Railway
railway database snapshots list

# AWS RDS
aws rds describe-db-instances --db-instance-identifier methean-prod --query 'DBInstances[0].BackupRetentionPeriod'
```

## Point-in-Time Recovery (PITR)

If available (AWS RDS, some managed Postgres providers):

```bash
# Create a new instance restored to a specific time
aws rds restore-db-instance-to-point-in-time \
  --source-db-instance-identifier methean-prod \
  --target-db-instance-identifier methean-recovery \
  --restore-time "2026-04-17T10:30:00Z"

# Wait for the new instance to be available
aws rds wait db-instance-available --db-instance-identifier methean-recovery

# Update the backend's DATABASE_URL to point to the recovery instance
# Test before switching production traffic
```

## Full Restore from Snapshot

```bash
# 1. Stop the backend to prevent writes during restore
railway service stop backend

# 2. Restore the snapshot (provider-specific)
# Railway:
railway database restore --snapshot-id <snapshot_id>
# AWS:
aws rds restore-db-instance-from-db-snapshot --db-instance-identifier methean-recovery --db-snapshot-identifier <snapshot_id>

# 3. Run any missing migrations
cd backend && alembic upgrade head

# 4. Verify data integrity
psql -c "SELECT COUNT(*) FROM households;"
psql -c "SELECT COUNT(*) FROM children;"
psql -c "SELECT MAX(created_at) FROM ai_runs;"  # check freshness

# 5. Restart the backend
railway service start backend

# 6. Run smoke tests
curl http://localhost:8000/health
curl -H "Authorization: Bearer $TOK" http://localhost:8000/api/v1/children
```

## Manual pg_dump Restore

If using manual backups:

```bash
# Create a backup
pg_dump -Fc -h $DB_HOST -U $DB_USER -d methean > methean_$(date +%Y%m%d_%H%M%S).dump

# Restore to a new database
createdb methean_recovery
pg_restore -d methean_recovery methean_20260417_103000.dump

# Verify
psql -d methean_recovery -c "SELECT COUNT(*) FROM households;"
```

## Estimated Recovery Times

| Scenario | Estimated Time | Notes |
|---|---|---|
| Railway snapshot restore | 5-15 minutes | Depends on database size |
| AWS PITR | 10-30 minutes | Instance creation + WAL replay |
| pg_dump restore (1GB) | 5-10 minutes | Depends on network and disk |
| pg_dump restore (10GB) | 30-60 minutes | Consider parallel restore |

These are estimates. Measure actual recovery time during a scheduled drill.

## Data Loss Window

- Railway daily snapshots: up to 24 hours of data loss
- AWS RDS continuous backup: up to 5 minutes of data loss (WAL-based)
- Manual pg_dump: depends on cron frequency

## Post-Recovery Checklist

- [ ] Health endpoint returns 200
- [ ] Can log in as a test user
- [ ] Children and learning data visible
- [ ] AI calls succeed (test via tutor)
- [ ] Celery tasks running (check flower or redis queue)
- [ ] No migration errors in logs
- [ ] RLS still enforced (check pg_policies)
