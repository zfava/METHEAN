"use client";

import { useEffect, useState } from "react";
import { governance, type GovernanceEvent } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";

export default function GovernancePage() {
  const [events, setEvents] = useState<GovernanceEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterAction, setFilterAction] = useState("");

  useEffect(() => {
    governance.events(200).then(setEvents).finally(() => setLoading(false));
  }, []);

  const filtered = filterAction
    ? events.filter((e) => e.action === filterAction)
    : events;

  const actions = [...new Set(events.map((e) => e.action))];

  function handleExport() {
    const csv = [
      "timestamp,action,target_type,target_id,actor,reason",
      ...filtered.map(
        (e) =>
          `"${e.created_at}","${e.action}","${e.target_type}","${e.target_id}","${e.user_id || "system"}","${e.reason || ""}"`
      ),
    ].join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "governance-log.csv";
    a.click();
  }

  if (loading) return <div className="text-sm text-(--color-text-secondary)">Loading...</div>;

  return (
    <div className="max-w-6xl">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-xl font-semibold">Governance Log</h1>
        <button
          onClick={handleExport}
          className="px-3 py-1.5 text-xs font-medium border border-(--color-border) rounded-md hover:bg-gray-50"
        >
          Export CSV
        </button>
      </div>

      <div className="flex gap-2 mb-4">
        <button
          onClick={() => setFilterAction("")}
          className={`px-3 py-1 text-xs rounded-full ${!filterAction ? "bg-(--color-accent) text-white" : "bg-gray-100 text-(--color-text-secondary)"}`}
        >
          All ({events.length})
        </button>
        {actions.map((a) => (
          <button
            key={a}
            onClick={() => setFilterAction(a)}
            className={`px-3 py-1 text-xs rounded-full capitalize ${filterAction === a ? "bg-(--color-accent) text-white" : "bg-gray-100 text-(--color-text-secondary)"}`}
          >
            {a} ({events.filter((e) => e.action === a).length})
          </button>
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
                <td className="px-4 py-3 text-xs font-mono text-(--color-text-secondary)">
                  {new Date(evt.created_at).toLocaleString()}
                </td>
                <td className="px-4 py-3">
                  <StatusBadge status={evt.action} />
                </td>
                <td className="px-4 py-3 text-xs">
                  <span className="font-mono text-(--color-text-secondary)">{evt.target_type}</span>
                </td>
                <td className="px-4 py-3 text-xs text-(--color-text-secondary) max-w-xs truncate">
                  {evt.reason || "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && (
          <div className="p-8 text-center text-sm text-(--color-text-secondary)">
            No governance events found.
          </div>
        )}
      </div>
    </div>
  );
}
