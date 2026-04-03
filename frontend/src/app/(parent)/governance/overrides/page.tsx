"use client";

import { useEffect, useState } from "react";
import { governance, type GovernanceEvent } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import LoadingSkeleton from "@/components/LoadingSkeleton";

export default function OverridesPage() {
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
      <div className="mb-6">
        <h1 className="text-xl font-semibold">Override Log</h1>
        <p className="text-sm text-(--color-text-secondary)">
          Prerequisite bypasses, manual mastery changes, and blocked node unlocks.
          This is the audit trail that proves parental sovereignty.
        </p>
      </div>

      {overrides.length === 0 ? (
        <div className="bg-white rounded-lg border border-(--color-border) p-8 text-center">
          <p className="text-sm text-(--color-text-secondary)">No overrides recorded yet.</p>
          <p className="text-xs text-(--color-text-secondary) mt-1">
            Overrides appear here when you unlock a blocked node or bypass a prerequisite.
          </p>
        </div>
      ) : (
        <div className="space-y-2">
          {overrides.map((evt) => (
            <div key={evt.id} className="bg-white rounded-lg border border-(--color-border) border-l-4 border-l-amber-400 p-4">
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  <StatusBadge status={evt.action} />
                  <span className="text-sm font-medium">Override</span>
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
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
