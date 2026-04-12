"""Initial schema - all tables, enums, indexes, and RLS policies.

Revision ID: 001
Revises: None
Create Date: 2026-04-02
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# All PostgreSQL enum types
ENUM_DEFINITIONS = {
    "userrole": ("owner", "co_parent", "observer"),
    "nodetype": ("root", "milestone", "concept", "skill"),
    "edgerelation": ("prerequisite", "corequisite", "recommended"),
    "masterylevel": ("not_started", "emerging", "developing", "proficient", "mastered"),
    "stateeventtype": ("mastery_change", "review_completed", "node_unlocked", "node_skipped", "override"),
    "fsrsrating": ("1", "2", "3", "4"),
    "ruletype": ("pace_limit", "content_filter", "schedule_constraint", "ai_boundary", "approval_required"),
    "rulescope": ("household", "child", "subject", "map"),
    "governanceaction": ("approve", "reject", "modify", "defer"),
    "planstatus": ("draft", "proposed", "approved", "active", "completed", "archived"),
    "activitytype": ("lesson", "practice", "assessment", "review", "project", "field_trip"),
    "activitystatus": ("scheduled", "in_progress", "completed", "skipped", "cancelled"),
    "attemptstatus": ("started", "completed", "abandoned"),
    "artifacttype": ("photo", "video", "document", "audio", "link"),
    "alertseverity": ("info", "warning", "action_required"),
    "alertstatus": ("unread", "read", "dismissed", "acted_on"),
    "airunstatus": ("pending", "running", "completed", "failed"),
    "auditaction": ("create", "read", "update", "delete", "login", "logout", "export"),
}


def upgrade() -> None:
    # ── Create all PostgreSQL enums (checkfirst for CI idempotency) ──
    bind = op.get_bind()
    for name, values in ENUM_DEFINITIONS.items():
        sa.Enum(*values, name=name).create(bind, checkfirst=True)

    # ── Section 3.1: Identity & Tenancy ──

    op.create_table(
        "households",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("timezone", sa.String(50), server_default="America/New_York"),
        sa.Column("settings", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("email", sa.String(320), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("display_name", sa.String(100), nullable=False),
        sa.Column("role", sa.Enum("owner", "co_parent", "observer", name="userrole", create_type=False), nullable=False),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("last_login_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "children",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100)),
        sa.Column("date_of_birth", sa.Date),
        sa.Column("grade_level", sa.String(20)),
        sa.Column("avatar_url", sa.Text),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "child_preferences",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), unique=True, nullable=False),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("learning_style", JSONB, server_default="{}"),
        sa.Column("interests", JSONB, server_default="[]"),
        sa.Column("accommodations", JSONB, server_default="{}"),
        sa.Column("daily_duration_minutes", sa.Integer),
        sa.Column("preferred_schedule", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Section 3.2: Curriculum Architecture ──

    op.create_table(
        "subjects",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("color", sa.String(7)),
        sa.Column("icon", sa.String(50)),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("sort_order", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "learning_maps",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subject_id", UUID(as_uuid=True), sa.ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("version", sa.Integer, server_default="1"),
        sa.Column("is_published", sa.Boolean, server_default="false"),
        sa.Column("metadata", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "learning_nodes",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("learning_map_id", UUID(as_uuid=True), sa.ForeignKey("learning_maps.id", ondelete="CASCADE"), nullable=False),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("node_type", sa.Enum("root", "milestone", "concept", "skill", name="nodetype", create_type=False), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("content", JSONB, server_default="{}"),
        sa.Column("estimated_minutes", sa.Integer),
        sa.Column("sort_order", sa.Integer, server_default="0"),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "learning_edges",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("learning_map_id", UUID(as_uuid=True), sa.ForeignKey("learning_maps.id", ondelete="CASCADE"), nullable=False),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("from_node_id", UUID(as_uuid=True), sa.ForeignKey("learning_nodes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("to_node_id", UUID(as_uuid=True), sa.ForeignKey("learning_nodes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("relation", sa.Enum("prerequisite", "corequisite", "recommended", name="edgerelation", create_type=False), nullable=False),
        sa.Column("weight", sa.Float, server_default="1.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("learning_map_id", "from_node_id", "to_node_id", name="uq_edge"),
    )

    op.create_table(
        "learning_map_closure",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("learning_map_id", UUID(as_uuid=True), sa.ForeignKey("learning_maps.id", ondelete="CASCADE"), nullable=False),
        sa.Column("ancestor_id", UUID(as_uuid=True), sa.ForeignKey("learning_nodes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("descendant_id", UUID(as_uuid=True), sa.ForeignKey("learning_nodes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("depth", sa.Integer, nullable=False),
        sa.UniqueConstraint("learning_map_id", "ancestor_id", "descendant_id", name="uq_closure"),
    )

    op.create_table(
        "child_map_enrollments",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("learning_map_id", UUID(as_uuid=True), sa.ForeignKey("learning_maps.id", ondelete="CASCADE"), nullable=False),
        sa.Column("enrolled_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("progress_pct", sa.Float, server_default="0.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("child_id", "learning_map_id", name="uq_child_map"),
    )

    # ── Section 3.3: Learner State Engine ──

    op.create_table(
        "child_node_states",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("node_id", UUID(as_uuid=True), sa.ForeignKey("learning_nodes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("mastery_level", sa.Enum("not_started", "emerging", "developing", "proficient", "mastered", name="masterylevel", create_type=False), nullable=False, server_default="not_started"),
        sa.Column("is_unlocked", sa.Boolean, server_default="false"),
        sa.Column("attempts_count", sa.Integer, server_default="0"),
        sa.Column("time_spent_minutes", sa.Integer, server_default="0"),
        sa.Column("last_activity_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "state_events",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("node_id", UUID(as_uuid=True), sa.ForeignKey("learning_nodes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("event_type", sa.Enum("mastery_change", "review_completed", "node_unlocked", "node_skipped", "override", name="stateeventtype", create_type=False), nullable=False),
        sa.Column("from_state", sa.Text),
        sa.Column("to_state", sa.Text),
        sa.Column("trigger", sa.Text),
        sa.Column("metadata", JSONB, server_default="{}"),
        sa.Column("created_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "fsrs_cards",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("node_id", UUID(as_uuid=True), sa.ForeignKey("learning_nodes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("stability", sa.Float, server_default="0.0"),
        sa.Column("difficulty", sa.Float, server_default="0.0"),
        sa.Column("elapsed_days", sa.Integer, server_default="0"),
        sa.Column("scheduled_days", sa.Integer, server_default="0"),
        sa.Column("reps", sa.Integer, server_default="0"),
        sa.Column("lapses", sa.Integer, server_default="0"),
        sa.Column("state", sa.Integer, server_default="0"),
        sa.Column("due", sa.DateTime(timezone=True)),
        sa.Column("last_review", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "review_logs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("card_id", UUID(as_uuid=True), sa.ForeignKey("fsrs_cards.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rating", sa.Enum("1", "2", "3", "4", name="fsrsrating", create_type=False), nullable=False),
        sa.Column("scheduled_days", sa.Integer, nullable=False),
        sa.Column("elapsed_days", sa.Integer, nullable=False),
        sa.Column("review_duration_ms", sa.Integer),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Section 3.4: Parent Governance ──

    op.create_table(
        "governance_rules",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("rule_type", sa.Enum("pace_limit", "content_filter", "schedule_constraint", "ai_boundary", "approval_required", name="ruletype", create_type=False), nullable=False),
        sa.Column("scope", sa.Enum("household", "child", "subject", "map", name="rulescope", create_type=False), nullable=False),
        sa.Column("scope_id", UUID(as_uuid=True)),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("parameters", JSONB, nullable=False, server_default="{}"),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("priority", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "governance_events",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("action", sa.Enum("approve", "reject", "modify", "defer", name="governanceaction", create_type=False), nullable=False),
        sa.Column("target_type", sa.String(100), nullable=False),
        sa.Column("target_id", UUID(as_uuid=True), nullable=False),
        sa.Column("reason", sa.Text),
        sa.Column("metadata", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "plans",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("status", sa.Enum("draft", "proposed", "approved", "active", "completed", "archived", name="planstatus", create_type=False), nullable=False, server_default="draft"),
        sa.Column("start_date", sa.Date),
        sa.Column("end_date", sa.Date),
        sa.Column("ai_generated", sa.Boolean, server_default="false"),
        sa.Column("ai_run_id", UUID(as_uuid=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "plan_weeks",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("plan_id", UUID(as_uuid=True), sa.ForeignKey("plans.id", ondelete="CASCADE"), nullable=False),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("week_number", sa.Integer, nullable=False),
        sa.Column("start_date", sa.Date, nullable=False),
        sa.Column("end_date", sa.Date, nullable=False),
        sa.Column("notes", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "activities",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("plan_week_id", UUID(as_uuid=True), sa.ForeignKey("plan_weeks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("node_id", UUID(as_uuid=True), sa.ForeignKey("learning_nodes.id", ondelete="SET NULL")),
        sa.Column("activity_type", sa.Enum("lesson", "practice", "assessment", "review", "project", "field_trip", name="activitytype", create_type=False), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("instructions", JSONB, server_default="{}"),
        sa.Column("estimated_minutes", sa.Integer),
        sa.Column("status", sa.Enum("scheduled", "in_progress", "completed", "skipped", "cancelled", name="activitystatus", create_type=False), nullable=False, server_default="scheduled"),
        sa.Column("scheduled_date", sa.Date),
        sa.Column("sort_order", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "attempts",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("activity_id", UUID(as_uuid=True), sa.ForeignKey("activities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.Enum("started", "completed", "abandoned", name="attemptstatus", create_type=False), nullable=False, server_default="started"),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("duration_minutes", sa.Integer),
        sa.Column("score", sa.Float),
        sa.Column("feedback", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Section 3.5: Evidence & Feedback ──

    op.create_table(
        "artifacts",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("attempt_id", UUID(as_uuid=True), sa.ForeignKey("attempts.id", ondelete="SET NULL")),
        sa.Column("artifact_type", sa.Enum("photo", "video", "document", "audio", "link", name="artifacttype", create_type=False), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("s3_key", sa.Text),
        sa.Column("url", sa.Text),
        sa.Column("file_size_bytes", sa.Integer),
        sa.Column("mime_type", sa.String(100)),
        sa.Column("metadata", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "alerts",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="SET NULL")),
        sa.Column("severity", sa.Enum("info", "warning", "action_required", name="alertseverity", create_type=False), nullable=False),
        sa.Column("status", sa.Enum("unread", "read", "dismissed", "acted_on", name="alertstatus", create_type=False), nullable=False, server_default="unread"),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("message", sa.Text, nullable=False),
        sa.Column("source", sa.String(100), nullable=False),
        sa.Column("action_url", sa.Text),
        sa.Column("metadata", JSONB, server_default="{}"),
        sa.Column("read_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "weekly_snapshots",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("week_start", sa.Date, nullable=False),
        sa.Column("week_end", sa.Date, nullable=False),
        sa.Column("total_minutes", sa.Integer, server_default="0"),
        sa.Column("activities_completed", sa.Integer, server_default="0"),
        sa.Column("activities_scheduled", sa.Integer, server_default="0"),
        sa.Column("nodes_mastered", sa.Integer, server_default="0"),
        sa.Column("nodes_progressed", sa.Integer, server_default="0"),
        sa.Column("reviews_completed", sa.Integer, server_default="0"),
        sa.Column("average_rating", sa.Float),
        sa.Column("summary", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Section 3.6: Operational ──

    op.create_table(
        "ai_runs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("triggered_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("run_type", sa.String(100), nullable=False),
        sa.Column("status", sa.Enum("pending", "running", "completed", "failed", name="airunstatus", create_type=False), nullable=False, server_default="pending"),
        sa.Column("model_used", sa.String(100)),
        sa.Column("input_tokens", sa.Integer),
        sa.Column("output_tokens", sa.Integer),
        sa.Column("cost_usd", sa.Float),
        sa.Column("input_data", JSONB, server_default="{}"),
        sa.Column("output_data", JSONB, server_default="{}"),
        sa.Column("error_message", sa.Text),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "advisor_reports",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("child_id", UUID(as_uuid=True), sa.ForeignKey("children.id", ondelete="CASCADE"), nullable=False),
        sa.Column("ai_run_id", UUID(as_uuid=True), sa.ForeignKey("ai_runs.id", ondelete="SET NULL")),
        sa.Column("report_type", sa.String(100), nullable=False),
        sa.Column("period_start", sa.Date, nullable=False),
        sa.Column("period_end", sa.Date, nullable=False),
        sa.Column("content", JSONB, nullable=False),
        sa.Column("recommendations", JSONB, server_default="[]"),
        sa.Column("parent_reviewed", sa.Boolean, server_default="false"),
        sa.Column("reviewed_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="SET NULL")),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("action", sa.Enum("create", "read", "update", "delete", "login", "logout", "export", name="auditaction", create_type=False), nullable=False),
        sa.Column("resource_type", sa.String(100), nullable=False),
        sa.Column("resource_id", UUID(as_uuid=True)),
        sa.Column("details", JSONB, server_default="{}"),
        sa.Column("ip_address", sa.String(45)),
        sa.Column("user_agent", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "refresh_tokens",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.String(255), nullable=False),
        sa.Column("device_info", sa.Text),
        sa.Column("is_revoked", sa.Boolean, server_default="false"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "device_tokens",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("device_type", sa.String(50), nullable=False),
        sa.Column("token", sa.Text, nullable=False),
        sa.Column("is_active", sa.Boolean, server_default="true"),
        sa.Column("last_used_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "notification_logs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("household_id", UUID(as_uuid=True), sa.ForeignKey("households.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("channel", sa.String(50), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("body", sa.Text, nullable=False),
        sa.Column("sent", sa.Boolean, server_default="false"),
        sa.Column("sent_at", sa.DateTime(timezone=True)),
        sa.Column("error", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Section 4.1: Indexes (25 indexes) ──

    # 1. Users by household
    op.create_index("ix_users_household_id", "users", ["household_id"])
    # 2. Users by email (already unique, but explicit)
    op.create_index("ix_users_email", "users", ["email"])
    # 3. Children by household
    op.create_index("ix_children_household_id", "children", ["household_id"])
    # 4. Subjects by household
    op.create_index("ix_subjects_household_id", "subjects", ["household_id"])
    # 5. Learning maps by household
    op.create_index("ix_learning_maps_household_id", "learning_maps", ["household_id"])
    # 6. Learning maps by subject
    op.create_index("ix_learning_maps_subject_id", "learning_maps", ["subject_id"])
    # 7. Learning nodes by map
    op.create_index("ix_learning_nodes_map_id", "learning_nodes", ["learning_map_id"])
    # 8. Learning nodes by household
    op.create_index("ix_learning_nodes_household_id", "learning_nodes", ["household_id"])
    # 9. Learning edges by map
    op.create_index("ix_learning_edges_map_id", "learning_edges", ["learning_map_id"])
    # 10. Closure table by map + ancestor
    op.create_index("ix_closure_map_ancestor", "learning_map_closure", ["learning_map_id", "ancestor_id"])
    # 11. Child map enrollments by child
    op.create_index("ix_enrollments_child_id", "child_map_enrollments", ["child_id"])
    # 12. Child node states: child + node (for fast lookup)
    op.create_index("ix_child_node_states_child_node", "child_node_states", ["child_id", "node_id"])
    # 13. Child node states by household
    op.create_index("ix_child_node_states_household", "child_node_states", ["household_id"])
    # 14. State events by child + node + created_at (event stream queries)
    op.create_index("ix_state_events_child_node_time", "state_events", ["child_id", "node_id", "created_at"])
    # 15. State events by household
    op.create_index("ix_state_events_household", "state_events", ["household_id"])
    # 16. FSRS cards by child + due (scheduling queries)
    op.create_index("ix_fsrs_cards_child_due", "fsrs_cards", ["child_id", "due"])
    # 17. Review logs by card
    op.create_index("ix_review_logs_card_id", "review_logs", ["card_id"])
    # 18. Governance rules by household + active
    op.create_index("ix_governance_rules_household_active", "governance_rules", ["household_id", "is_active"])
    # 19. Plans by household + child
    op.create_index("ix_plans_household_child", "plans", ["household_id", "child_id"])
    # 20. Activities by plan_week
    op.create_index("ix_activities_plan_week", "activities", ["plan_week_id"])
    # 21. Activities by scheduled_date (daily view)
    op.create_index("ix_activities_scheduled_date", "activities", ["household_id", "scheduled_date"])
    # 22. Attempts by activity
    op.create_index("ix_attempts_activity_id", "attempts", ["activity_id"])
    # 23. Alerts by household + status (unread alerts)
    op.create_index("ix_alerts_household_status", "alerts", ["household_id", "status"])
    # 24. Audit logs by household + created_at
    op.create_index("ix_audit_logs_household_time", "audit_logs", ["household_id", "created_at"])
    # 25. Refresh tokens by user + revoked (active token lookup)
    op.create_index("ix_refresh_tokens_user_active", "refresh_tokens", ["user_id", "is_revoked"])

    # ── Section 4.2: Row-Level Security Policies ──

    conn = op.get_bind()

    # Enable RLS on all household-scoped tables
    household_tables = [
        "users", "children", "child_preferences", "subjects", "learning_maps",
        "learning_nodes", "learning_edges", "learning_map_closure",
        "child_map_enrollments", "child_node_states", "state_events",
        "fsrs_cards", "review_logs", "governance_rules", "governance_events",
        "plans", "plan_weeks", "activities", "attempts", "artifacts",
        "alerts", "weekly_snapshots", "advisor_reports", "ai_runs",
        "refresh_tokens", "device_tokens", "notification_logs",
    ]

    for table in household_tables:
        conn.execute(sa.text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY"))
        conn.execute(sa.text(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY"))

        # Policy: users can only see rows from their household
        conn.execute(sa.text(
            f"CREATE POLICY {table}_household_isolation ON {table} "
            f"USING (household_id = current_setting('app.current_household_id')::uuid)"
        ))

    # Audit logs get a separate policy (household_id can be null)
    conn.execute(sa.text("ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY"))
    conn.execute(sa.text("ALTER TABLE audit_logs FORCE ROW LEVEL SECURITY"))
    conn.execute(sa.text(
        "CREATE POLICY audit_logs_household_isolation ON audit_logs "
        "USING (household_id = current_setting('app.current_household_id')::uuid "
        "OR household_id IS NULL)"
    ))


def downgrade() -> None:
    # Drop all tables in reverse order
    tables = [
        "notification_logs", "device_tokens", "refresh_tokens",
        "audit_logs", "advisor_reports", "ai_runs",
        "weekly_snapshots", "alerts", "artifacts",
        "attempts", "activities", "plan_weeks", "plans",
        "governance_events", "governance_rules",
        "review_logs", "fsrs_cards", "state_events", "child_node_states",
        "child_map_enrollments", "learning_map_closure", "learning_edges",
        "learning_nodes", "learning_maps", "subjects",
        "child_preferences", "children", "users", "households",
    ]
    for table in tables:
        op.drop_table(table)

    # Drop all enums (checkfirst for safety)
    bind = op.get_bind()
    for name in ENUM_DEFINITIONS:
        sa.Enum(name=name).drop(bind, checkfirst=True)
