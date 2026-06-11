"""add supervision_attestations for the qualified-human runtime presence gate

A node whose safety_basis names a qualified human who must be
physically present at the work (requires_qualified_human_present_at_runtime
in services/node_content.py) is not surfaced to the learner until a
parent attests, today, that the named qualified human is present for
this child and this node. Attestations are per child, per node, per
day: expires_at is the household-local end of day, so there are no
standing waivers. Every attestation is hash-chained as a governance
event (migration 052).

The composite index (child_id, node_id, expires_at) serves the hot
path: "is there an unexpired attestation for this child and node",
checked on every learning-context build for a hazardous node.

RLS mirrors migration 027's policy pattern exactly.

Revision ID: 058
Revises: 057
Create Date: 2026-06-11
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: str = "058"
down_revision: str | None = "057"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "supervision_attestations"


def upgrade() -> None:
    op.create_table(
        TABLE,
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "household_id",
            UUID(as_uuid=True),
            sa.ForeignKey("households.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "child_id",
            UUID(as_uuid=True),
            sa.ForeignKey("children.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "node_id",
            UUID(as_uuid=True),
            sa.ForeignKey("learning_nodes.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "attested_by",
            UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("role_claimed", sa.String(100), nullable=False),
        sa.Column("attested_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("note", sa.String(500), nullable=True),
    )
    op.create_index(f"ix_{TABLE}_household_id", TABLE, ["household_id"])
    op.create_index(
        "ix_supervision_attestation_lookup",
        TABLE,
        ["child_id", "node_id", "expires_at"],
    )

    if op.get_bind().dialect.name == "postgresql":
        policy = f"{TABLE}_household_isolation"
        op.execute(f"ALTER TABLE {TABLE} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {TABLE} FORCE ROW LEVEL SECURITY")
        op.execute(
            f"CREATE POLICY {policy} ON {TABLE} "
            "USING (household_id = current_setting('app.current_household_id', true)::uuid)"
        )


def downgrade() -> None:
    if op.get_bind().dialect.name == "postgresql":
        op.execute(f"DROP POLICY IF EXISTS {TABLE}_household_isolation ON {TABLE}")
    op.drop_index("ix_supervision_attestation_lookup", table_name=TABLE)
    op.drop_index(f"ix_{TABLE}_household_id", table_name=TABLE)
    op.drop_table(TABLE)
