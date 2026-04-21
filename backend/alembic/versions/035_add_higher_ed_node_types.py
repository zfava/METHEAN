"""add_higher_ed_node_types

Adds 8 higher-education values to the existing nodetype Postgres enum.
Autogenerate cannot detect Postgres enum value additions, so this is
written manually. Each ALTER TYPE uses ADD VALUE IF NOT EXISTS so the
migration is idempotent across environments.

Revision ID: 035
Revises: 034
Create Date: 2026-04-19
"""

from typing import Sequence, Union

from alembic import op

revision: str = "035"
down_revision: Union[str, None] = "034"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

NEW_VALUES = [
    "lecture",
    "reading",
    "research",
    "lab",
    "thesis_component",
    "exam_prep",
    "peer_review",
    "practicum",
]


def upgrade() -> None:
    # ALTER TYPE ... ADD VALUE cannot run inside a transaction block
    # in older Postgres releases, but PG12+ allows it. Alembic's online
    # mode wraps DDL in a transaction by default; this works on PG16
    # which is the supported version.
    for val in NEW_VALUES:
        op.execute(f"ALTER TYPE nodetype ADD VALUE IF NOT EXISTS '{val}'")


def downgrade() -> None:
    # PostgreSQL does not support removing values from an enum type.
    # The added values are harmless to leave in place and do not break
    # downgrade integrity for any other revision.
    pass
