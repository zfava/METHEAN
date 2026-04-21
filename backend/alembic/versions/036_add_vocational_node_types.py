"""add_vocational_node_types

Backfill the 5 vocational NodeType values that are present in the
Python enum (app.models.enums.NodeType) but were never added to the
Postgres nodetype enum. Migration 001 created the enum with only the
4 academic labels, and no later migration added the vocational set,
so any attempt to persist a vocational node fails at the DB layer.

This is additive only. Autogenerate cannot detect Postgres enum
additions. Each ALTER TYPE uses ADD VALUE IF NOT EXISTS for
idempotency across environments.

Revision ID: 036
Revises: 035
Create Date: 2026-04-19
"""

from typing import Sequence, Union

from alembic import op

revision: str = "036"
down_revision: Union[str, None] = "035"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

VOCATIONAL_VALUES = [
    "safety",
    "knowledge",
    "technique",
    "project",
    "certification_prep",
]


def upgrade() -> None:
    for val in VOCATIONAL_VALUES:
        op.execute(f"ALTER TYPE nodetype ADD VALUE IF NOT EXISTS '{val}'")


def downgrade() -> None:
    # PostgreSQL does not support removing values from an enum type.
    # The added values are harmless to leave in place.
    pass
