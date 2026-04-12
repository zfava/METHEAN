"use client";

import { useEffect, useState } from "react";
import { governance, type GovernanceEvent } from "@/lib/api";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import EmptyState from "@/components/ui/EmptyState";
import StatusBadge from "@/components/StatusBadge";
import { cn } from "@/lib/cn";
import { relativeTime } from "@/lib/format";
import EvaluationChain from "@/components/EvaluationChain";
import { ShieldIcon } from "@/components/ConstitutionalCeremony";

const dotColor: Record<string, string> = {
  approve: "bg-(--color-success)",
  reject: "bg-(--color-danger)",
  modify: "bg-(--color-warning)",
  defer: "bg-(--color-text-tertiary)",
};

export default function TracePage() {
  useEffect(() => { document.title = "Decision Trace | METHEAN"; }, []);

  const [events, setEvents] = useState<GovernanceEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filterAction, setFilterAction] = useState("");
  const [filterCalibration, setFilterCalibration] = useState(false);
  const [expanded, setExpanded] = useState<Set<string>>(new Set());

  useEffect(() => {
    governance.events(200)
      .then((d) => setEvents((d as any).items || d))
      .finally(() => setLoading(false));
  }, []);

  function toggleExpand(id: string) {
    setExpanded((prev) => { const n = new Set(prev); n.has(id) ? n.delete(id) : n.add(id); return n; });
  }

  const calibrationEvents = events.filter((e) => e.target_type === "calibration_profile");
  const filtered = filterCalibration
    ? calibrationEvents
    : filterAction
      ? events.filter((e) => e.action === filterAction)
      : events;
  const actions = [...new Set(events.map((e) => e.action))];

  if (loading) return <div className="max-w-4xl"><LoadingSkeleton variant="list" count={10} /></div>;

  return (
    <div className="max-w-4xl">
      <PageHeader title="Decision Trace" subtitle="Complete audit trail of every governance decision." />

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between">
            <p className="text-sm text-(--color-danger)">{error}</p>
          </div>
        </Card>
      )}

      {/* Filter bar */}
      <div className="flex flex-wrap gap-2 mb-5">
        <button onClick={() => { setFilterAction(""); setFilterCalibration(false); }}
          className={cn(
            "px-3 py-1 text-xs rounded-full transition-colors",
            !filterAction && !filterCalibration ? "bg-(--color-text) text-white" : "bg-(--color-page) text-(--color-text-secondary) hover:bg-(--color-border)"
          )}
        >All ({events.length})</button>
        {actions.map((a) => (
          <button key={a} onClick={() => { setFilterAction(a); setFilterCalibration(false); }}
            className={cn(
              "px-3 py-1 text-xs rounded-full capitalize transition-colors",
              filterAction === a && !filterCalibration
                ? "bg-(--color-text) text-white"
                : ""
            )}
          >
            {filterAction !== a ? (
              <StatusBadge status={a} className="bg-transparent p-0 text-[11px]" />
            ) : (
              a
            )}
            {" "}({events.filter((e) => e.action === a).length})
          </button>
        ))}
        {calibrationEvents.length > 0 && (
          <button onClick={() => { setFilterCalibration(true); setFilterAction(""); }}
            className={cn(
              "px-3 py-1 text-xs rounded-full transition-colors",
              filterCalibration ? "bg-(--color-accent) text-white" : "bg-(--color-page) text-(--color-text-secondary) hover:bg-(--color-border)"
            )}
          >Calibration ({calibrationEvents.length})</button>
        )}
      </div>

      {filtered.length === 0 ? (
        <EmptyState icon="empty" title="No governance events found" />
      ) : (
        <div className="relative">
          {/* Vertical timeline line */}
          <div className="absolute left-[11px] top-0 bottom-0 w-px bg-(--color-border)" />

          <div className="space-y-0">
            {filtered.map((evt) => {
              const isConstitutional = evt.target_type.includes("constitutional");
              const dot = isConstitutional ? "bg-(--color-constitutional)" : (dotColor[evt.action] || "bg-(--color-text-tertiary)");
              const isOpen = expanded.has(evt.id);

              return (
                <div key={evt.id} className="relative pl-8 pb-4">
                  {/* Dot on timeline */}
                  <div className={cn("absolute left-[7px] top-[6px] w-[10px] h-[10px] rounded-full ring-2 ring-(--color-surface)", dot)} />

                  <button onClick={() => toggleExpand(evt.id)} className="w-full text-left">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        {isConstitutional && <ShieldIcon size={12} className="text-(--color-constitutional)" />}
                        <StatusBadge status={evt.action} />
                        {isConstitutional && <StatusBadge status="constitutional" />}
                        <span className="text-sm text-(--color-text) capitalize">{evt.target_type.replace(/_/g, " ")}</span>
                      </div>
                      <span className="text-xs text-(--color-text-tertiary)">{relativeTime(evt.created_at)}</span>
                    </div>
                  </button>

                  {/* Expanded detail */}
                  {isOpen && (
                    <div className="mt-2 p-3 bg-(--color-page) rounded-[10px] text-xs text-(--color-text-secondary)">
                      <div className="grid grid-cols-2 gap-2">
                        <div><span className="text-(--color-text-tertiary)">Time:</span> {new Date(evt.created_at).toLocaleString()}</div>
                        <div><span className="text-(--color-text-tertiary)">Target ID:</span> <span className="font-mono">{evt.target_id.slice(0, 12)}...</span></div>
                        {evt.user_id && <div><span className="text-(--color-text-tertiary)">Actor:</span> <span className="font-mono">{evt.user_id.slice(0, 8)}...</span></div>}
                      </div>
                      {evt.reason && (
                        <div className={cn("mt-2 pt-2 border-t border-(--color-border)", isConstitutional && "bg-(--color-constitutional-light) -mx-3 px-3 py-2 rounded-[10px] border-t-0 mt-3")}>
                          <span className="text-(--color-text-tertiary)">{isConstitutional ? "Stated reason:" : "Reason:"}</span>
                          {isConstitutional ? <p className="italic text-(--color-constitutional) mt-0.5">"{evt.reason}"</p> : <span> {evt.reason}</span>}
                        </div>
                      )}
                      {evt.metadata_?.evaluations && evt.metadata_.evaluations.length > 0 && (
                        <div className="mt-2 pt-2 border-t border-(--color-border)">
                          <div className="text-(--color-text-tertiary) mb-1.5">Rule evaluations:</div>
                          <EvaluationChain
                            evaluations={evt.metadata_.evaluations}
                            blockingRules={evt.metadata_.blocking_rules || []}
                          />
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
