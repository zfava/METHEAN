"use client";

import { useEffect, useState } from "react";
import { governance, type GovernanceEvent } from "@/lib/api";
import LoadingSkeleton from "@/components/LoadingSkeleton";

const dotColor: Record<string, string> = {
  approve: "bg-green-500",
  reject: "bg-red-500",
  modify: "bg-yellow-500",
  defer: "bg-slate-400",
};
const badgeStyle: Record<string, { bg: string; text: string; label: string }> = {
  approve: { bg: "bg-green-100", text: "text-green-800", label: "Approved" },
  reject: { bg: "bg-red-100", text: "text-red-800", label: "Rejected" },
  modify: { bg: "bg-yellow-100", text: "text-yellow-800", label: "Modified" },
  defer: { bg: "bg-slate-100", text: "text-slate-600", label: "Deferred" },
};

function relativeTime(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

export default function TracePage() {
  const [events, setEvents] = useState<GovernanceEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterAction, setFilterAction] = useState("");
  const [expanded, setExpanded] = useState<Set<string>>(new Set());

  useEffect(() => {
    governance.events(200)
      .then((d) => setEvents((d as any).items || d))
      .finally(() => setLoading(false));
  }, []);

  function toggleExpand(id: string) {
    setExpanded((prev) => { const n = new Set(prev); n.has(id) ? n.delete(id) : n.add(id); return n; });
  }

  const filtered = filterAction ? events.filter((e) => e.action === filterAction) : events;
  const actions = [...new Set(events.map((e) => e.action))];

  if (loading) return <div className="max-w-4xl"><LoadingSkeleton variant="list" count={10} /></div>;

  return (
    <div className="max-w-4xl">
      <div className="mb-6">
        <h1 className="text-xl font-semibold text-slate-800">Decision Trace</h1>
        <p className="text-sm text-slate-500">Complete audit trail of every governance decision.</p>
      </div>

      {/* Filter bar */}
      <div className="flex gap-2 mb-5">
        <button onClick={() => setFilterAction("")}
          className={`px-3 py-1 text-xs rounded-full transition-colors ${!filterAction ? "bg-slate-800 text-white" : "bg-slate-100 text-slate-500 hover:bg-slate-200"}`}
        >All ({events.length})</button>
        {actions.map((a) => {
          const badge = badgeStyle[a] || badgeStyle.defer;
          return (
            <button key={a} onClick={() => setFilterAction(a)}
              className={`px-3 py-1 text-xs rounded-full capitalize transition-colors ${
                filterAction === a ? "bg-slate-800 text-white" : `${badge.bg} ${badge.text} hover:opacity-80`
              }`}
            >{a} ({events.filter((e) => e.action === a).length})</button>
          );
        })}
      </div>

      {filtered.length === 0 ? (
        <div className="bg-white rounded-lg border border-slate-200 p-12 text-center text-sm text-slate-400">
          No governance events found.
        </div>
      ) : (
        <div className="relative">
          {/* Vertical timeline line */}
          <div className="absolute left-[11px] top-0 bottom-0 w-px bg-slate-200" />

          <div className="space-y-0">
            {filtered.map((evt) => {
              const dot = dotColor[evt.action] || "bg-slate-400";
              const badge = badgeStyle[evt.action] || badgeStyle.defer;
              const isOpen = expanded.has(evt.id);

              return (
                <div key={evt.id} className="relative pl-8 pb-4">
                  {/* Dot on timeline */}
                  <div className={`absolute left-[7px] top-[6px] w-[10px] h-[10px] rounded-full ${dot} ring-2 ring-white`} />

                  <button onClick={() => toggleExpand(evt.id)} className="w-full text-left">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded ${badge.bg} ${badge.text}`}>
                          {badge.label}
                        </span>
                        <span className="text-sm text-slate-700 capitalize">{evt.target_type.replace(/_/g, " ")}</span>
                      </div>
                      <span className="text-xs text-slate-400">{relativeTime(evt.created_at)}</span>
                    </div>
                  </button>

                  {/* Expanded detail */}
                  {isOpen && (
                    <div className="mt-2 p-3 bg-slate-50 rounded-md text-xs text-slate-600">
                      <div className="grid grid-cols-2 gap-2">
                        <div><span className="text-slate-400">Time:</span> {new Date(evt.created_at).toLocaleString()}</div>
                        <div><span className="text-slate-400">Target ID:</span> <span className="font-mono">{evt.target_id.slice(0, 12)}...</span></div>
                        {evt.user_id && <div><span className="text-slate-400">Actor:</span> <span className="font-mono">{evt.user_id.slice(0, 8)}...</span></div>}
                      </div>
                      {evt.reason && (
                        <div className="mt-2 pt-2 border-t border-slate-200">
                          <span className="text-slate-400">Reason:</span> {evt.reason}
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
