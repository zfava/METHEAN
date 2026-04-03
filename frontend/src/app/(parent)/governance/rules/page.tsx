"use client";

import { useEffect, useState } from "react";
import { governance, type GovernanceRule } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";

const ruleDescriptions: Record<string, (params: Record<string, unknown>) => string> = {
  pace_limit: (p) => `No more than ${p.max_daily_minutes || 240} minutes of scheduled learning per day`,
  content_filter: () => "Filters content based on parent-defined criteria",
  schedule_constraint: () => "Constrains when learning activities can be scheduled",
  ai_boundary: () => "Limits AI behavior within parent-defined boundaries",
  approval_required: (p) => {
    if (p.action === "auto_approve" && p.max_difficulty)
      return `Activities with difficulty below ${p.max_difficulty} are auto-approved`;
    if (p.action === "require_review" && p.min_difficulty)
      return `Activities with difficulty ${p.min_difficulty} or above require parent review`;
    if (p.action === "block" && p.min_difficulty)
      return `Activities with difficulty ${p.min_difficulty} or above are blocked`;
    return "Requires parent approval for activities";
  },
};

export default function RulesPage() {
  const [rules, setRules] = useState<GovernanceRule[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    governance.rules()
      .then((d) => setRules((d as any).items || d))
      .finally(() => setLoading(false));
  }, []);

  // Group by type
  const byType: Record<string, GovernanceRule[]> = {};
  rules.forEach((r) => {
    if (!byType[r.rule_type]) byType[r.rule_type] = [];
    byType[r.rule_type].push(r);
  });

  const typeLabels: Record<string, string> = {
    pace_limit: "Pace Limits",
    content_filter: "Content Filters",
    schedule_constraint: "Schedule Constraints",
    ai_boundary: "AI Boundaries",
    approval_required: "Approval Requirements",
  };

  if (loading) return <div className="text-sm text-(--color-text-secondary)">Loading rules...</div>;

  return (
    <div className="max-w-4xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold">Governance Rules</h1>
          <p className="text-sm text-(--color-text-secondary)">Define how AI recommendations are filtered before reaching your children</p>
        </div>
      </div>

      {Object.entries(byType).length === 0 ? (
        <div className="bg-white rounded-lg border border-(--color-border) p-8 text-center">
          <p className="text-sm text-(--color-text-secondary)">No rules configured. Initialize defaults from the governance overview.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {Object.entries(byType).map(([type, typeRules]) => (
            <div key={type}>
              <h3 className="text-xs font-semibold text-(--color-text-secondary) uppercase tracking-wider mb-2">
                {typeLabels[type] || type}
              </h3>
              <div className="space-y-2">
                {typeRules.map((r) => {
                  const desc = ruleDescriptions[r.rule_type];
                  const explanation = desc ? desc(r.parameters as Record<string, unknown>) : "";
                  return (
                    <div key={r.id} className={`bg-white rounded-lg border p-4 ${r.is_active ? "border-(--color-border)" : "border-gray-200 opacity-60"}`}>
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center gap-2">
                          <span className="text-sm font-medium">{r.name}</span>
                          <StatusBadge status={r.scope} />
                          <span className="text-xs font-mono text-(--color-text-secondary)">P{r.priority}</span>
                        </div>
                        <span className={`text-xs font-medium ${r.is_active ? "text-emerald-600" : "text-gray-400"}`}>
                          {r.is_active ? "Active" : "Disabled"}
                        </span>
                      </div>
                      {r.description && <p className="text-xs text-(--color-text-secondary) mb-1">{r.description}</p>}
                      {explanation && (
                        <div className="text-xs bg-amber-50 border border-amber-100 text-amber-800 rounded px-2 py-1.5 mt-2">
                          What this means: {explanation}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
