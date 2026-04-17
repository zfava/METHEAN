# Migration Rollback

Last verified: 2026-04-17 (round-trip tested in CI; production rollback not yet exercised)

## When to Rollback vs. Forward-Fix

**Rollback** when:
- The migration introduced a schema error that breaks queries
- The migration dropped data that should not have been dropped
- The migration cannot be forward-fixed without another schema change

**Forward-fix** when:
- The migration is correct but a bug in application code was exposed
- The migration added a column with a wrong default (fix the default, do not rollback)
- Rolling back would lose data that was written after the migration applied

## Rollback One Migration

```bash
# ALWAYS take a backup first
pg_dump -Fc -h $DB_HOST -U $DB_USER -d methean > pre_rollback_$(date +%Y%m%d_%H%M%S).dump

# Check current revision
cd backend && alembic current

# Rollback one step
alembic downgrade -1

# Verify
alembic current
psql -c "SELECT * FROM alembic_version;"
```

## Rollback to a Specific Revision

```bash
# Rollback to revision 029 (for example)
alembic downgrade 029

# Verify
alembic current
```

## When Rollback is Not Possible

If a migration dropped a column or table and data was lost:

1. **Do not attempt rollback.** The downgrade will recreate the column/table but with empty data.
2. Restore from backup (see database-recovery.md).
3. Then apply migrations up to the version before the bad one.
4. Forward-fix the migration, then apply.

## Production Guards

Before rolling back in production:

1. **Take a backup.** Non-negotiable.
2. **Stop the backend.** Prevent writes during schema change.
3. **Run the rollback.**
4. **Deploy the previous code version** (the code must match the schema).
5. **Start the backend.**
6. **Run smoke tests.**

```bash
# Full sequence
railway service stop backend
pg_dump -Fc -h $DB_HOST -U $DB_USER -d methean > pre_rollback.dump
cd backend && alembic downgrade -1
# Deploy previous git commit
git revert HEAD
git push origin main
railway service start backend
curl http://localhost:8000/health
```

## Idempotency

All migrations in this project use `CREATE INDEX IF NOT EXISTS` and `DROP INDEX IF EXISTS` patterns (see docs/migration-guide.md). This means:

- Rerunning `alembic upgrade head` is safe (no "already exists" errors)
- Partial migration failures can be retried without manual cleanup
- The CI gate (`migration-check` job) tests upgrade, downgrade, re-upgrade on every PR
