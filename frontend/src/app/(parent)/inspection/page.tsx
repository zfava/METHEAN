"use client";

import { useEffect, useState } from "react";
import { ai, type AIRun } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import LoadingSkeleton from "@/components/LoadingSkeleton";

export default function InspectionPage() {
  const [runs, setRuns] = useState<AIRun[]>([]);
  const [selected, setSelected] = useState<AIRun | null>(null);
  const [filterRole, setFilterRole] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRuns();
  }, [filterRole]);

  async function loadRuns() {
    setLoading(true);
    const data = await ai.runs(filterRole ? { role: filterRole } : undefined);
    setRuns(data);
    setLoading(false);
  }

  async function selectRun(runId: string) {
    const detail = await ai.run(runId);
    setSelected(detail);
  }

  const roles = ["planner", "tutor", "evaluator", "advisor", "cartographer"];

  return (
    <div className="max-w-6xl">
      <div className="mb-6">
        <h1 className="text-xl font-semibold">AI Inspection</h1>
        <p className="text-sm text-(--color-text-secondary) mt-0.5">
          Every AI decision is transparent. Inspect any call&apos;s full input and output.
        </p>
      </div>

      <div className="flex gap-2 mb-4">
        <button
          onClick={() => setFilterRole("")}
          className={`px-3 py-1 text-xs rounded-full ${!filterRole ? "bg-(--color-accent) text-white" : "bg-gray-100"}`}
        >
          All
        </button>
        {roles.map((r) => (
          <button
            key={r}
            onClick={() => setFilterRole(r)}
            className={`px-3 py-1 text-xs rounded-full capitalize ${filterRole === r ? "bg-(--color-accent) text-white" : "bg-gray-100"}`}
          >
            {r}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-4">
        {/* Run list */}
        <div className="bg-white rounded-lg border border-(--color-border) max-h-[600px] overflow-y-auto">
          {loading ? (
            <div className="p-4"><LoadingSkeleton variant="list" count={5} /></div>
          ) : runs.length === 0 ? (
            <div className="p-8 text-center text-sm text-(--color-text-secondary)">No AI runs found.</div>
          ) : (
            runs.map((run) => (
              <button
                key={run.id}
                onClick={() => selectRun(run.id)}
                className={`w-full text-left px-4 py-3 border-b border-gray-50 hover:bg-gray-50 transition-colors ${
                  selected?.id === run.id ? "bg-blue-50" : ""
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-medium capitalize">{run.run_type}</span>
                  <StatusBadge status={run.status} />
                </div>
                <div className="flex items-center gap-3 mt-1 text-xs text-(--color-text-secondary)">
                  <span>{run.model_used || "—"}</span>
                  {run.input_tokens && <span>{run.input_tokens + (run.output_tokens || 0)} tokens</span>}
                  <span>{new Date(run.created_at).toLocaleString()}</span>
                </div>
              </button>
            ))
          )}
        </div>

        {/* Detail panel */}
        <div className="bg-white rounded-lg border border-(--color-border)">
          {selected ? (
            <div className="p-4">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-semibold capitalize">{selected.run_type} Run</h3>
                <div className="flex items-center gap-2">
                  <StatusBadge status={selected.status} />
                  {selected.model_used === "mock" && (
                    <span className="text-[10px] px-1.5 py-0.5 bg-amber-50 text-amber-700 rounded font-medium">MOCK</span>
                  )}
                </div>
              </div>

              <div className="grid grid-cols-3 gap-2 mb-4 text-xs">
                <div className="bg-gray-50 rounded p-2">
                  <div className="text-(--color-text-secondary)">Model</div>
                  <div className="font-mono mt-0.5">{selected.model_used || "—"}</div>
                </div>
                <div className="bg-gray-50 rounded p-2">
                  <div className="text-(--color-text-secondary)">Tokens</div>
                  <div className="font-mono mt-0.5">
                    {selected.input_tokens || 0} in / {selected.output_tokens || 0} out
                  </div>
                </div>
                <div className="bg-gray-50 rounded p-2">
                  <div className="text-(--color-text-secondary)">Time</div>
                  <div className="font-mono mt-0.5">
                    {selected.started_at && selected.completed_at
                      ? `${Math.round((new Date(selected.completed_at).getTime() - new Date(selected.started_at).getTime()))}ms`
                      : "—"}
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <div>
                  <div className="text-xs font-semibold text-(--color-text-secondary) mb-1">INPUT</div>
                  <pre className="text-[11px] font-mono bg-gray-50 rounded p-3 overflow-auto max-h-48 whitespace-pre-wrap break-words">
                    {JSON.stringify(selected.input_data, null, 2)}
                  </pre>
                </div>
                <div>
                  <div className="text-xs font-semibold text-(--color-text-secondary) mb-1">OUTPUT</div>
                  <pre className="text-[11px] font-mono bg-gray-50 rounded p-3 overflow-auto max-h-48 whitespace-pre-wrap break-words">
                    {JSON.stringify(selected.output_data, null, 2)}
                  </pre>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-8 text-center text-sm text-(--color-text-secondary)">
              Select an AI run to inspect its full input/output.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
