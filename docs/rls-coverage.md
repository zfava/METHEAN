# RLS Coverage Matrix

Every table with a `household_id` column has a PostgreSQL Row-Level Security policy that restricts visibility to the current tenant. The tenant is set via `SET LOCAL app.current_household_id` on every authenticated request.

Last verified: 2026-04-17

## Coverage

| Table | Has household_id | RLS enabled | Policy name | Migration |
|---|---|---|---|---|
| users | yes | yes | users_household_isolation | 027 |
| children | yes | yes | children_household_isolation | 027 |
| child_preferences | yes | yes | child_preferences_household_isolation | 027 |
| subjects | yes | yes | subjects_household_isolation | 027 |
| learning_maps | yes | yes | learning_maps_household_isolation | 027 |
| learning_nodes | yes | yes | learning_nodes_household_isolation | 027 |
| learning_edges | yes | yes | learning_edges_household_isolation | 027 |
| child_map_enrollments | yes | yes | child_map_enrollments_household_isolation | 027 |
| child_node_states | yes | yes | child_node_states_household_isolation | 027 |
| state_events | yes | yes | state_events_household_isolation | 027 |
| fsrs_cards | yes | yes | fsrs_cards_household_isolation | 027 |
| review_logs | yes | yes | review_logs_household_isolation | 027 |
| governance_rules | yes | yes | governance_rules_household_isolation | 027 |
| governance_events | yes | yes | governance_events_household_isolation | 027 |
| plans | yes | yes | plans_household_isolation | 027 |
| plan_weeks | yes | yes | plan_weeks_household_isolation | 027 |
| activities | yes | yes | activities_household_isolation | 027 |
| attempts | yes | yes | attempts_household_isolation | 027 |
| alerts | yes | yes | alerts_household_isolation | 027 |
| weekly_snapshots | yes | yes | weekly_snapshots_household_isolation | 027 |
| advisor_reports | yes | yes | advisor_reports_household_isolation | 027 |
| artifacts | yes | yes | artifacts_household_isolation | 027 |
| assessments | yes | yes | assessments_household_isolation | 027 |
| portfolio_entries | yes | yes | portfolio_entries_household_isolation | 027 |
| annual_curricula | yes | yes | annual_curricula_household_isolation | 027 |
| activity_feedback | yes | yes | activity_feedback_household_isolation | 027 |
| reading_log_entries | yes | yes | reading_log_entries_household_isolation | 027 |
| family_resources | yes | yes | family_resources_household_isolation | 027 |
| education_plans | yes | yes | education_plans_household_isolation | 027 |
| achievements | yes | yes | achievements_household_isolation | 027 |
| streaks | yes | yes | streaks_household_isolation | 027 |
| usage_ledger | yes | yes | usage_ledger_household_isolation | 027 |
| usage_events | yes | yes | usage_events_household_isolation | 027 |
| ai_runs | yes | yes | ai_runs_household_isolation | 027 |
| audit_logs | yes | yes | audit_logs_household_isolation | 031 |
| refresh_tokens | yes | yes | refresh_tokens_household_isolation | 027 |
| device_tokens | yes | yes | device_tokens_household_isolation | 027 |
| notification_logs | yes | yes | notification_logs_household_isolation | 027 |
| user_permissions | yes | yes | user_permissions_household_isolation | 027 |
| family_invites | yes | yes | family_invites_household_isolation | 027 |
| learner_intelligence | yes | yes | learner_intelligence_household_isolation | 027 |
| evaluator_predictions | yes | yes | evaluator_predictions_household_isolation | 027 |
| calibration_profiles | yes | yes | calibration_profiles_household_isolation | 027 |
| calibration_snapshots | yes | yes | calibration_snapshots_household_isolation | 027 |
| learner_style_vectors | yes | yes | learner_style_vectors_household_isolation | 027 |
| family_insights | yes | yes | family_insights_household_isolation | 027 |
| family_insight_configs | yes | yes | family_insight_configs_household_isolation | 027 |
| wellbeing_anomalies | yes | yes | wellbeing_anomalies_household_isolation | 027 |
| wellbeing_configs | yes | yes | wellbeing_configs_household_isolation | 027 |

## Tables WITHOUT household_id (no RLS needed)

| Table | Reason |
|---|---|
| households | IS the tenant; no cross-tenant scoping needed |
| learning_map_closure | Scoped via learning_map_id, not household_id (closure table) |

## How to verify

```bash
# Check which tables have RLS enabled (requires running postgres)
psql -U methean -d methean -c "
  SELECT tablename, rowsecurity
  FROM pg_tables
  WHERE schemaname = 'public'
  ORDER BY tablename;
"

# Check policy details
psql -U methean -d methean -c "
  SELECT tablename, policyname, cmd, qual
  FROM pg_policies
  WHERE schemaname = 'public'
  ORDER BY tablename;
"

# Automated test
cd backend && pytest tests/test_security.py -k "rls" -v
```

## Policy pattern

All policies use the same USING clause:

```sql
CREATE POLICY {table}_household_isolation ON {table}
USING (household_id = current_setting('app.current_household_id', true)::uuid)
```

The `true` parameter to `current_setting` makes it return NULL (not error) when the setting is unset, which means: if `app.current_household_id` is not set, NO rows are visible. This is fail-closed by design.
