"""add source_ref to learning_nodes

Records the template / content-module ref a learning node was materialized
from (e.g. "mf-01"). The from-template persistence path (copy_template)
previously kept its ref -> uuid map only in memory and discarded it, so a
persisted node carried no link back to the content id it came from.

The native-namespace resolver needs that link to be idempotent: it must be
able to find an already-persisted node by its content id rather than
creating a duplicate node/map on every resolve. A single nullable, indexed
column on the existing learning_nodes table is the minimal change and reuses
the same table the from-template path already writes; no parallel lookup
table is introduced.

The column is nullable: nodes created outside the from-template path (hand
built maps, AI-enriched maps) simply have NULL and are ignored by the
resolver's lookup.

Revision ID: 050
Revises: 049
Create Date: 2026-05-30
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "050"
down_revision: str | None = "049"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "learning_nodes",
        sa.Column("source_ref", sa.String(length=64), nullable=True),
    )
    op.create_index(
        "ix_learning_nodes_source_ref",
        "learning_nodes",
        ["source_ref"],
    )


def downgrade() -> None:
    op.drop_index("ix_learning_nodes_source_ref", table_name="learning_nodes")
    op.drop_column("learning_nodes", "source_ref")
