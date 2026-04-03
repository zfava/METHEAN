"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { governance, type GovernanceEvent } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import LoadingSkeleton from "@/components/LoadingSkeleton";

const actionColors: Record<string, string> = {
  approve: "border-l-emerald-500",
  reject: "border-l-red-500",
  modify: "border-l-amber-500",
  defer: "border-l-gray-400",
};

export default function TracePage() {
  const [events, setEvents] = useState<GovernanceEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterAction, setFilterAction] = useState("");

  useEffect(() => {
    governance.events(200)
      .then((d) => setEvents((d as any).items || d))
      .finally(() => setLoading(false));
  }, []);

  const filtered = filterAction ? events.filter((e) => e.action === filterAction) : events;
  const actions = [...new Set(events.map((e) => e.action))];

  if (loading) return <div className="max-w-4xl"><LoadingSkeleton variant="list" count={8} /></div>;

  return (
    <div className="max-w-4xl">
      <div className="mb-6">
        <h1 className="text-xl font-semibold">Decision Trace</h1>
        <p className="text-sm text-(--color-text-secondary)">Every governance decision, in chronological order</p>
      </div>

      <div className="flex gap-2 mb-4">
        <button onClick={() => setFilterAction("")}
          className={`px-3 py-1 text-xs rounded-full ${!filterAction ? "bg-(--color-accent) text-white" : "bg-gray-100 text-(--color-text-secondary)"}`}
        >All ({events.length})</button>
        {actions.map((a) => (
          <button key={a} onClick={() => setFilterAction(a)}
            className={`px-3 py-1 text-xs rounded-full capitalize ${filterAction === a ? "bg-(--color-accent) text-white" : "bg-gray-100 text-(--color-text-secondary)"}`}
          >{a} ({events.filter((e) => e.action === a).length})</button>
        ))}
      </div>

      {filtered.length === 0 ? (
        <div className="bg-white rounded-lg border border-(--color-border) p-8 text-center text-sm text-(--color-text-secondary)">
          No governance events found.
        </div>
      ) : (
        <div className="space-y-1">
          {filtered.map((evt) => (
            <div key={evt.id} className={`bg-white border border-(--color-border) border-l-4 ${actionColors[evt.action] || "border-l-gray-300"} rounded-r-lg px-4 py-3`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <StatusBadge status={evt.action} />
                  <span className="text-sm font-medium capitalize">{evt.target_type.replace(/_/g, " ")}</span>
                </div>
                <span className="text-xs font-mono text-(--color-text-secondary)">
                  {new Date(evt.created_at).toLocaleString()}
                </span>
              </div>
              {evt.reason && (
                <p className="text-xs text-(--color-text-secondary) mt-1 ml-[68px]">{evt.reason}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
