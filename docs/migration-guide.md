# Migration Guide

Rules for writing Alembic migrations in METHEAN.

## Idempotency Checklist

Every migration must be safe to run on a fresh database AND on a database where it partially succeeded previously.

- [ ] Index creation uses `CREATE INDEX IF NOT EXISTS` via `op.execute()`
- [ ] Index drops use `DROP INDEX IF EXISTS` via `op.execute()`
- [ ] Table creation uses `op.create_table()` (Alembic handles existence)
- [ ] RLS policies use `DROP POLICY IF EXISTS ... ; CREATE POLICY ...`
- [ ] Downgrade is implemented (not just `pass`)
- [ ] Downgrade reverses every operation in upgrade
- [ ] Tested: upgrade, downgrade, upgrade again on fresh DB

## Patterns

### Creating an index

```python
# CORRECT: idempotent
op.execute("CREATE INDEX IF NOT EXISTS ix_foo_bar ON foo (bar, baz)")

# CORRECT: unique index
op.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_foo_bar ON foo (bar)")

# CORRECT: expression index (DESC ordering)
op.execute("CREATE INDEX IF NOT EXISTS ix_foo_bar ON foo (bar, created_at DESC)")

# WRONG: not idempotent, fails if index exists
op.create_index("ix_foo_bar", "foo", ["bar", "baz"])
```

### Dropping an index (in downgrade)

```python
# CORRECT: idempotent
op.execute("DROP INDEX IF EXISTS ix_foo_bar")

# WRONG: fails if index doesn't exist
op.drop_index("ix_foo_bar")
```

### RLS policies

```python
# CORRECT: drop-then-create is idempotent
op.execute("DROP POLICY IF EXISTS my_table_tenant ON my_table")
op.execute("ALTER TABLE my_table ENABLE ROW LEVEL SECURITY")
op.execute("ALTER TABLE my_table FORCE ROW LEVEL SECURITY")
op.execute("""
    CREATE POLICY my_table_tenant ON my_table
    USING (household_id = current_setting('app.current_household_id', true)::uuid)
""")
```

### Adding a column

```python
# CORRECT: add_column is idempotent in Alembic (fails gracefully if exists)
op.add_column("foo", sa.Column("bar", sa.Text, nullable=True))

# Downgrade:
op.drop_column("foo", "bar")
```

## Testing a migration

Before committing:

```bash
cd backend
alembic upgrade head       # apply all migrations
alembic downgrade -1       # rollback yours
alembic upgrade head       # re-apply
alembic downgrade base     # full rollback
alembic upgrade head       # full re-apply from clean
```

CI runs this automatically in the `migration-check` job.

## Naming conventions

- Index: `ix_{table}_{columns}` (e.g., `ix_attempts_activity_child`)
- Unique index: `ix_{table}_{columns}` with UNIQUE keyword
- RLS policy: `{table}_tenant` or `{table}_household_isolation`
- Migration file: `{NNN}_{description}.py` where NNN is zero-padded sequence
