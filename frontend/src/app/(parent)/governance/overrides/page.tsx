"use client";

import { useEffect, useState } from "react";
import { governance, type GovernanceEvent } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import EmptyState from "@/components/ui/EmptyState";

export default function OverridesPage() {
  useEffect(() => { document.title = "Overrides | METHEAN"; }, []);

  const [overrides, setOverrides] = useState<GovernanceEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    governance.events(200)
      .then((d) => {
        const all: GovernanceEvent[] = (d as any).items || d;
        // Overrides are governance events on child_node_state targets
        setOverrides(all.filter((e) => e.target_type === "child_node_state"));
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="max-w-4xl"><LoadingSkeleton variant="list" count={4} /></div>;

  return (
    <div className="max-w-4xl">
      <PageHeader
        title="Override Log"
        subtitle="Prerequisite bypasses, manual mastery changes, and blocked node unlocks. This is the audit trail that proves parental sovereignty."
      />

      {overrides.length === 0 ? (
        <EmptyState
          icon="empty"
          title="No overrides recorded yet"
          description="Overrides appear here when you unlock a blocked node or bypass a prerequisite."
        />
      ) : (
        <div className="space-y-2">
          {overrides.map((evt) => (
            <Card key={evt.id} padding="p-4" borderLeft="border-l-(--color-warning)" className="border-l-4">
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  <StatusBadge status={evt.action} />
                  <span className="text-sm font-medium text-(--color-text)">Override</span>
                </div>
                <span className="text-xs font-mono text-(--color-text-secondary)">
                  {new Date(evt.created_at).toLocaleString()}
                </span>
              </div>
              {evt.reason && (
                <p className="text-sm text-(--color-text) mt-1">&ldquo;{evt.reason}&rdquo;</p>
              )}
              <p className="text-xs text-(--color-text-secondary) mt-1">
                Target: {evt.target_type} &middot; {evt.target_id.slice(0, 8)}...
              </p>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
