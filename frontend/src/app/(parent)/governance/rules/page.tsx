"use client";

import { useEffect, useState } from "react";
import { governance, type GovernanceRule } from "@/lib/api";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import EmptyState from "@/components/ui/EmptyState";
import StatusBadge from "@/components/StatusBadge";

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
      <PageHeader title="Governance Rules" subtitle="You set these. You can change them anytime." />

      {rules.length === 0 ? (
        <EmptyState icon="empty" title="No rules configured" description="Initialize defaults from the governance overview or create a new rule." />
      ) : (
        <div className="space-y-8">
          {/* Constitutional rules first */}
          {(() => {
            const constitutional = rules.filter((r) => (r as any).tier === "constitutional");
            const policy = rules.filter((r) => (r as any).tier !== "constitutional");

            // Group policy by type
            const policyByType: Record<string, GovernanceRule[]> = {};
            policy.forEach((r) => { (policyByType[r.rule_type] ||= []).push(r); });

            return (
              <>
                {constitutional.length > 0 && (
                  <div>
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-lg">&#x1F6E1;</span>
                      <h3 className="text-sm font-semibold text-(--color-constitutional)">Constitutional Rules</h3>
                      <StatusBadge status="constitutional" className="text-[10px] font-semibold" />
                    </div>
                    <div className="space-y-2">
                      {constitutional.map((r) => (
                        <Card key={r.id} padding="p-4" borderLeft="border-l-(--color-warning)" className={`border-l-4 ${r.is_active ? "border-(--color-warning)/40" : "border-(--color-border) opacity-50"}`}>
                          <div className="flex items-center justify-between mb-1">
                            <div className="flex items-center gap-2">
                              <span className="text-sm font-semibold text-(--color-text)">{r.name}</span>
                              <StatusBadge status="constitutional" />
                            </div>
                            <span className={`text-xs font-medium ${r.is_active ? "text-(--color-success)" : "text-(--color-text-tertiary)"}`}>
                              {r.is_active ? "Active" : "Deactivated"}
                            </span>
                          </div>
                          {r.description && <p className="text-xs text-(--color-text-secondary) mb-2">{r.description}</p>}
                          <div className="text-xs bg-(--color-constitutional-light) border border-(--color-constitutional)/20 text-(--color-constitutional) rounded px-3 py-2">
                            <span className="font-medium">What this means:</span> {humanize(r)}
                          </div>
                          <p className="text-[10px] text-(--color-text-tertiary) mt-2 italic">Changes require written confirmation and are permanently logged.</p>
                        </Card>
                      ))}
                    </div>
                    {policy.length > 0 && <div className="border-t border-(--color-border) mt-6 pt-2" />}
                  </div>
                )}

                {Object.entries(policyByType).map(([type, typeRules]) => {
                  const info = typeLabels[type] || { label: type, icon: "?" };
                  return (
                    <div key={type}>
                      <div className="flex items-center gap-2 mb-3">
                        <span className="text-lg">{info.icon}</span>
                        <h3 className="text-sm font-semibold text-(--color-text)">{info.label}</h3>
                        <span className="text-xs text-(--color-text-tertiary)">({typeRules.length})</span>
                      </div>
                      <div className="space-y-2">
                        {typeRules.map((r) => (
                          <Card key={r.id} padding="p-4" className={!r.is_active ? "opacity-50" : ""}>
                            <div className="flex items-center justify-between mb-1">
                              <div className="flex items-center gap-2">
                                <span className="text-sm font-semibold text-(--color-text)">{r.name}</span>
                                <span className="text-[10px] px-1.5 py-0.5 bg-(--color-page) text-(--color-text-secondary) rounded font-medium">{r.scope}</span>
                                <span className="text-[10px] font-mono text-(--color-text-tertiary)">P{r.priority}</span>
                              </div>
                              <span className={`text-xs font-medium ${r.is_active ? "text-(--color-success)" : "text-(--color-text-tertiary)"}`}>
                                {r.is_active ? "Active" : "Disabled"}
                              </span>
                            </div>
                            {r.description && <p className="text-xs text-(--color-text-secondary) mb-2">{r.description}</p>}
                            <div className="text-xs bg-(--color-constitutional-light) border border-(--color-constitutional)/20 text-(--color-constitutional) rounded px-3 py-2">
                              <span className="font-medium">What this means:</span> {humanize(r)}
                            </div>
                          </Card>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </>
            );
          })()}
        </div>
      )}
    </div>
  );
}
