# Customer Data Request

Last verified: 2026-04-17 (export path tested; deletion path documented but not yet exercised end-to-end)

## Data Export Request (COPPA / FERPA "right to inspect")

### Self-Service

Parents can export their data directly:

1. Log in to METHEAN
2. Navigate to Settings
3. Click "Export Data"
4. Receive a ZIP file containing all household data in JSON format

API: `POST /api/v1/household/export`

### Manual Fulfillment

If a parent cannot access their account:

```bash
# 1. Identify the household
psql -c "SELECT h.id, h.name, u.email FROM households h JOIN users u ON u.household_id = h.id WHERE u.email = 'parent@example.com';"

# 2. Generate the export
cd backend
python -c "
import asyncio
from app.core.database import async_session_factory, set_tenant
from app.services.data_export import export_family_data

async def export():
    async with async_session_factory() as db:
        await set_tenant(db, '<household_uuid>')
        data = await export_family_data(db, '<household_uuid>')
        with open('export.zip', 'wb') as f:
            f.write(data)
        print('Export written to export.zip')

asyncio.run(export())
"

# 3. Send the ZIP to the parent via encrypted email or secure file transfer
# Do NOT send via plain email; the export contains educational records
```

### What the Export Contains

- `family_profile.json`: household name, philosophical profile, settings
- Per-child directories with:
  - `profile.json`: name, DOB, grade level, preferences
  - `mastery_states.json`: per-node mastery levels
  - `weekly_snapshots.json`: weekly activity summaries
  - `curricula.json`: annual curriculum plans
  - `reading_log.json`: reading entries
  - `compliance_hours.json`: hours by subject
- `governance_rules.json`: household governance rules
- `governance_events.json`: governance decision history
- `metadata.json`: export date, version

### Response Time

Self-service: immediate (ZIP generated on demand).
Manual: within 48 hours of request receipt.

## Data Deletion Request (COPPA "right to delete")

### Current State

There is no self-service deletion endpoint yet. Deletion requires database-level operation.

### Manual Fulfillment

```bash
# 1. Confirm the request is from the account owner
# Verify via email match, or require the parent to confirm from their registered email

# 2. Take a backup FIRST
pg_dump -Fc -h $DB_HOST -U $DB_USER -d methean > pre_deletion_$(date +%Y%m%d).dump

# 3. Export data for the parent (in case they want a copy)
# Follow the export procedure above

# 4. Delete the household
# CASCADE foreign keys will propagate to all 49 child tables
psql -c "DELETE FROM households WHERE id = '<household_uuid>';"

# 5. Verify deletion
psql -c "SELECT COUNT(*) FROM users WHERE household_id = '<household_uuid>';"  # should be 0
psql -c "SELECT COUNT(*) FROM children WHERE household_id = '<household_uuid>';"  # should be 0
psql -c "SELECT COUNT(*) FROM ai_runs WHERE household_id = '<household_uuid>';"  # should be 0

# 6. Anonymize audit logs (preserve the event record, remove the household link)
psql -c "UPDATE audit_logs SET household_id = '00000000-0000-0000-0000-000000000000' WHERE household_id = '<household_uuid>';"

# 7. Confirm to the parent
# Send a confirmation email that their data has been deleted
```

### What is Deleted

All data in all 49 household-scoped tables, including:
- All child identifying information
- All educational records (attempts, assessments, portfolios)
- All computed analytics (intelligence, calibration, style vectors)
- All wellbeing and family insight records
- All governance rules and events
- All notification logs and device tokens

### What is Retained

- Anonymized audit logs (household_id replaced with a null UUID)
- Stripe payment records (retained by Stripe per their policy; METHEAN's reference is deleted)

### Response Time

Manual deletion: within 72 hours of confirmed request.
Data removed from backups: within 90 days (backup rotation).

### Follow-Up Item

A self-service `DELETE /api/v1/household` endpoint is needed before beta launch. See docs/compliance/coppa.md "What Is Not Yet Implemented."
