"""repair enum type drift on family_insights and wellbeing tables

Migrations 024 and 025 created these columns as plain String while the
models map native Python enums, so SQLAlchemy binds parameters as
::familypatterntype, ::insightstatus, ::anomalytype, ::anomalystatus,
and ::sensitivitylevel. Those Postgres types exist only on databases
born from Base.metadata.create_all (the test harness); on a
migration-born database every query touching these columns raises
UndefinedObjectError and the aborted transaction poisons the whole
request. The verification harness (PR 58) hit this live: POST
/children/{id}/plans/generate 500s through the planner's family
intelligence context. Same defect class as the fsrsrating repair in
migration 055.

Repair direction per the parity policy: the database becomes what the
model maps. The DDL is idempotent across both database lineages:
create each enum type only if absent, alter each column only when its
current type differs, and fail loudly listing offending values if any
row holds a string outside the enum's members (data is never coerced
or nulled). Columns with varchar server defaults have them dropped and
restored as enum-typed defaults around the ALTER.

The permanent guard for this class lives in
backend/tests/test_schema_parity.py.

Revision ID: 060
Revises: 059
Create Date: 2026-06-11
"""

from collections.abc import Sequence

from alembic import op
from sqlalchemy import text

revision: str = "060"
down_revision: str | None = "059"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# (type_name, members) for every Postgres enum involved. Members are
# the Python enum member NAMES, which is what SQLAlchemy's Enum type
# persists and what create_all-born databases carry as labels.
ENUM_TYPES: list[tuple[str, tuple[str, ...]]] = [
    (
        "familypatterntype",
        (
            "shared_struggle",
            "curriculum_gap",
            "pacing_divergence",
            "environmental_correlation",
            "material_effectiveness",
        ),
    ),
    ("insightstatus", ("detected", "notified", "acknowledged", "acted_on", "dismissed")),
    (
        "anomalytype",
        ("broad_disengagement", "frustration_spike", "performance_cliff", "session_avoidance"),
    ),
    ("anomalystatus", ("detected", "notified", "acknowledged", "dismissed", "resolved")),
    ("sensitivitylevel", ("conservative", "balanced", "sensitive")),
]

# (table, column, type_name, default_label or None)
COLUMN_REPAIRS: list[tuple[str, str, str, str | None]] = [
    ("family_insights", "pattern_type", "familypatterntype", None),
    ("family_insights", "status", "insightstatus", "detected"),
    ("wellbeing_anomalies", "anomaly_type", "anomalytype", None),
    ("wellbeing_anomalies", "status", "anomalystatus", "detected"),
    ("wellbeing_anomalies", "sensitivity_level", "sensitivitylevel", None),
    ("wellbeing_configs", "sensitivity_level", "sensitivitylevel", "balanced"),
]


def _current_udt(bind, table: str, column: str) -> str | None:
    return bind.execute(
        text("SELECT udt_name FROM information_schema.columns WHERE table_name = :t AND column_name = :c"),
        {"t": table, "c": column},
    ).scalar()


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return

    members_by_type = dict(ENUM_TYPES)

    for type_name, members in ENUM_TYPES:
        labels = ", ".join(f"'{m}'" for m in members)
        op.execute(
            f"DO $$ BEGIN CREATE TYPE {type_name} AS ENUM ({labels}); EXCEPTION WHEN duplicate_object THEN NULL; END $$"
        )

    for table, column, type_name, default_label in COLUMN_REPAIRS:
        if _current_udt(bind, table, column) == type_name:
            continue

        # Loud data check: a stored value outside the enum's members is
        # a data problem the migration must surface, never coerce.
        members = members_by_type[type_name]
        placeholders = ", ".join(f"'{m}'" for m in members)
        bad = bind.execute(
            text(
                f"SELECT DISTINCT {column} FROM {table} WHERE {column} IS NOT NULL AND {column} NOT IN ({placeholders})"
            )
        ).all()
        if bad:
            offending = sorted(row[0] for row in bad)
            raise RuntimeError(
                f"Cannot repair {table}.{column} to enum {type_name}: rows hold "
                f"values outside the enum members: {offending}. Resolve the data "
                "first; this migration never coerces or nulls."
            )

        if default_label is not None:
            op.execute(f"ALTER TABLE {table} ALTER COLUMN {column} DROP DEFAULT")
        op.execute(f"ALTER TABLE {table} ALTER COLUMN {column} TYPE {type_name} USING {column}::{type_name}")
        if default_label is not None:
            op.execute(f"ALTER TABLE {table} ALTER COLUMN {column} SET DEFAULT '{default_label}'::{type_name}")


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return

    # Restore the String shapes migrations 024 and 025 created. The
    # enum types themselves are left in place: create_all-born
    # databases legitimately own them for other reasons, and an unused
    # type is harmless while a missing one is not.
    widths = {
        ("family_insights", "pattern_type"): 50,
        ("family_insights", "status"): 20,
        ("wellbeing_anomalies", "anomaly_type"): 30,
        ("wellbeing_anomalies", "status"): 20,
        ("wellbeing_anomalies", "sensitivity_level"): 20,
        ("wellbeing_configs", "sensitivity_level"): 20,
    }
    for table, column, type_name, default_label in COLUMN_REPAIRS:
        if _current_udt(bind, table, column) != type_name:
            continue
        width = widths[(table, column)]
        if default_label is not None:
            op.execute(f"ALTER TABLE {table} ALTER COLUMN {column} DROP DEFAULT")
        op.execute(f"ALTER TABLE {table} ALTER COLUMN {column} TYPE VARCHAR({width}) USING {column}::text")
        if default_label is not None:
            op.execute(f"ALTER TABLE {table} ALTER COLUMN {column} SET DEFAULT '{default_label}'")
