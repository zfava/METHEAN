"use client";

import { useEffect, useState } from "react";
import { governance, type GovernanceEvent, type GovernanceRule } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import LoadingSkeleton from "@/components/LoadingSkeleton";

export default function GovernancePage() {
  const [events, setEvents] = useState<GovernanceEvent[]>([]);
  const [rules, setRules] = useState<GovernanceRule[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterAction, setFilterAction] = useState("");
  const [tab, setTab] = useState<"log" | "rules">("log");

  useEffect(() => {
    Promise.all([
      governance.events(200).then((d) => setEvents((d as any).items || d)),
      governance.rules().then((d) => setRules((d as any).items || d)),
    ]).finally(() => setLoading(false));
  }, []);

  const filtered = filterAction ? events.filter((e) => e.action === filterAction) : events;
  const actions = [...new Set(events.map((e) => e.action))];

  function handleExport() {
    const csv = [
      "timestamp,action,target_type,target_id,reason",
      ...filtered.map((e) =>
        `"${e.created_at}","${e.action}","${e.target_type}","${e.target_id}","${e.reason || ""}"`
      ),
    ].join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "governance-log.csv";
    a.click();
  }

  if (loading) return <div className="max-w-6xl space-y-4"><LoadingSkeleton variant="text" count={1} /><LoadingSkeleton variant="table" count={8} /></div>;

  return (
    <div className="max-w-6xl">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-xl font-semibold">Governance</h1>
        <div className="flex gap-2">
          <button onClick={() => setTab("log")} className={`px-3 py-1.5 text-xs rounded-md ${tab === "log" ? "bg-(--color-accent) text-white" : "bg-gray-100"}`}>Event Log</button>
          <button onClick={() => setTab("rules")} className={`px-3 py-1.5 text-xs rounded-md ${tab === "rules" ? "bg-(--color-accent) text-white" : "bg-gray-100"}`}>Rules</button>
          {tab === "log" && (
            <button onClick={handleExport} className="px-3 py-1.5 text-xs font-medium border border-(--color-border) rounded-md hover:bg-gray-50">Export CSV</button>
          )}
        </div>
      </div>

      {tab === "rules" ? (
        <div className="bg-white rounded-lg border border-(--color-border)">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-(--color-border) text-xs text-(--color-text-secondary)">
                <th className="text-left px-4 py-3 font-medium">Rule</th>
                <th className="text-left px-4 py-3 font-medium">Type</th>
                <th className="text-left px-4 py-3 font-medium">Scope</th>
                <th className="text-left px-4 py-3 font-medium">Priority</th>
                <th className="text-left px-4 py-3 font-medium">Active</th>
              </tr>
            </thead>
            <tbody>
              {rules.map((r) => (
                <tr key={r.id} className="border-b border-gray-50 hover:bg-gray-50">
                  <td className="px-4 py-3">
                    <div className="text-sm font-medium">{r.name}</div>
                    {r.description && <div className="text-xs text-(--color-text-secondary)">{r.description}</div>}
                  </td>
                  <td className="px-4 py-3"><StatusBadge status={r.rule_type} /></td>
                  <td className="px-4 py-3 text-xs">{r.scope}</td>
                  <td className="px-4 py-3 text-xs font-mono">{r.priority}</td>
                  <td className="px-4 py-3">{r.is_active ? <span className="text-emerald-600 text-xs">Active</span> : <span className="text-gray-400 text-xs">Disabled</span>}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {rules.length === 0 && <div className="p-8 text-center text-sm text-(--color-text-secondary)">No rules configured.</div>}
        </div>
      ) : (
        <>
          <div className="flex gap-2 mb-4">
            <button onClick={() => setFilterAction("")} className={`px-3 py-1 text-xs rounded-full ${!filterAction ? "bg-(--color-accent) text-white" : "bg-gray-100 text-(--color-text-secondary)"}`}>All ({events.length})</button>
            {actions.map((a) => (
              <button key={a} onClick={() => setFilterAction(a)} className={`px-3 py-1 text-xs rounded-full capitalize ${filterAction === a ? "bg-(--color-accent) text-white" : "bg-gray-100 text-(--color-text-secondary)"}`}>{a} ({events.filter((e) => e.action === a).length})</button>
            ))}
          </div>

          <div className="bg-white rounded-lg border border-(--color-border)">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-(--color-border) text-xs text-(--color-text-secondary)">
                  <th className="text-left px-4 py-3 font-medium">Time</th>
                  <th className="text-left px-4 py-3 font-medium">Action</th>
                  <th className="text-left px-4 py-3 font-medium">Target</th>
                  <th className="text-left px-4 py-3 font-medium">Reason</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((evt) => (
                  <tr key={evt.id} className="border-b border-gray-50 last:border-0 hover:bg-gray-50">
                    <td className="px-4 py-3 text-xs font-mono text-(--color-text-secondary)">{new Date(evt.created_at).toLocaleString()}</td>
                    <td className="px-4 py-3"><StatusBadge status={evt.action} /></td>
                    <td className="px-4 py-3 text-xs"><span className="font-mono text-(--color-text-secondary)">{evt.target_type}</span></td>
                    <td className="px-4 py-3 text-xs text-(--color-text-secondary) max-w-xs truncate">{evt.reason || "\u2014"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {filtered.length === 0 && <div className="p-8 text-center text-sm text-(--color-text-secondary)">No governance events found.</div>}
          </div>
        </>
      )}
    </div>
  );
}
