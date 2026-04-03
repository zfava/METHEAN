"use client";

import { useEffect, useState } from "react";
import { governance, type GovernanceRule } from "@/lib/api";
import LoadingSkeleton from "@/components/LoadingSkeleton";

function humanize(rule: GovernanceRule): string {
  const p = rule.parameters as Record<string, unknown>;
  switch (rule.rule_type) {
    case "pace_limit": {
      const mins = Number(p.max_daily_minutes || 240);
      const hrs = mins / 60;
      return hrs === Math.floor(hrs)
        ? `No more than ${hrs} hours of learning per day`
        : `No more than ${mins} minutes of learning per day`;
    }
    case "approval_required":
      if (p.action === "auto_approve" && p.max_difficulty)
        return `Activities under difficulty ${p.max_difficulty} are auto-approved`;
      if (p.action === "require_review" && p.min_difficulty)
        return `Activities at difficulty ${p.min_difficulty} or above require your review`;
      if (p.action === "block" && p.min_difficulty)
        return `Activities at difficulty ${p.min_difficulty} or above are blocked entirely`;
      return "Requires your approval for activities";
    case "schedule_constraint":
      return p.allowed_days ? `Learning scheduled on ${p.allowed_days} only` : "Schedule constraints active";
    case "content_filter":
      return p.blocked_topics ? `Topics blocked: ${p.blocked_topics}` : "Content filtering active";
    case "ai_boundary":
      return "AI behavior restricted within your defined boundaries";
    default:
      return rule.description || "Rule active";
  }
}

const typeLabels: Record<string, { label: string; icon: string }> = {
  approval_required: { label: "Approval Requirements", icon: "\u26E8" },
  pace_limit: { label: "Pace Limits", icon: "\u23F1" },
  schedule_constraint: { label: "Schedule Constraints", icon: "\u2637" },
  content_filter: { label: "Content Filters", icon: "\u2616" },
  ai_boundary: { label: "AI Boundaries", icon: "\u2B21" },
};

export default function RulesPage() {
  const [rules, setRules] = useState<GovernanceRule[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    governance.rules()
      .then((d) => setRules((d as any).items || d))
      .finally(() => setLoading(false));
  }, []);

  const byType: Record<string, GovernanceRule[]> = {};
  rules.forEach((r) => { (byType[r.rule_type] ||= []).push(r); });

  if (loading) return <div className="max-w-4xl"><LoadingSkeleton variant="list" count={5} /></div>;

  return (
    <div className="max-w-4xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold text-slate-800">Governance Rules</h1>
          <p className="text-sm text-slate-500">You set these. You can change them anytime.</p>
        </div>
      </div>

      {Object.keys(byType).length === 0 ? (
        <div className="bg-white rounded-lg border border-slate-200 p-12 text-center">
          <p className="text-sm text-slate-500">No rules configured.</p>
          <p className="text-xs text-slate-400 mt-1">Initialize defaults from the governance overview or create a new rule.</p>
        </div>
      ) : (
        <div className="space-y-8">
          {Object.entries(byType).map(([type, typeRules]) => {
            const info = typeLabels[type] || { label: type, icon: "?" };
            return (
              <div key={type}>
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-lg">{info.icon}</span>
                  <h3 className="text-sm font-semibold text-slate-700">{info.label}</h3>
                  <span className="text-xs text-slate-400">({typeRules.length})</span>
                </div>
                <div className="space-y-2">
                  {typeRules.map((r) => (
                    <div key={r.id} className={`bg-white rounded-lg border p-4 ${r.is_active ? "border-slate-200" : "border-slate-100 opacity-50"}`}>
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center gap-2">
                          <span className="text-sm font-semibold text-slate-800">{r.name}</span>
                          <span className="text-[10px] px-1.5 py-0.5 bg-slate-100 text-slate-500 rounded font-medium">{r.scope}</span>
                          <span className="text-[10px] font-mono text-slate-400">P{r.priority}</span>
                        </div>
                        <span className={`text-xs font-medium ${r.is_active ? "text-green-600" : "text-slate-400"}`}>
                          {r.is_active ? "Active" : "Disabled"}
                        </span>
                      </div>
                      {r.description && <p className="text-xs text-slate-500 mb-2">{r.description}</p>}
                      <div className="text-xs bg-amber-50 border border-amber-100 text-amber-800 rounded px-3 py-2">
                        <span className="font-medium">What this means:</span> {humanize(r)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
