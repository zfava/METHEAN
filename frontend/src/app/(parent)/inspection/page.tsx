"use client";

import { useEffect, useState } from "react";
import { ai, type AIRun } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import { cn } from "@/lib/cn";
import EmptyState from "@/components/ui/EmptyState";

export default function InspectionPage() {
  useEffect(() => { document.title = "AI Inspection | METHEAN"; }, []);

  const [runs, setRuns] = useState<AIRun[]>([]);
  const [selected, setSelected] = useState<AIRun | null>(null);
  const [filterRole, setFilterRole] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => { loadRuns(); }, [filterRole]);

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
      <PageHeader title="AI Inspection" subtitle="Every AI decision is transparent. Inspect any call's full input and output." />

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between">
            <p className="text-sm text-(--color-danger)">{error}</p>
          </div>
        </Card>
      )}

      <div className="flex gap-2 mb-4">
        <Button variant={!filterRole ? "primary" : "secondary"} size="sm" onClick={() => setFilterRole("")}>All</Button>
        {roles.map((r) => (
          <Button key={r} variant={filterRole === r ? "primary" : "secondary"} size="sm"
            onClick={() => setFilterRole(r)} className="capitalize">{r}</Button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card padding="p-0" className="max-h-[600px] overflow-y-auto">
          {loading ? (
            <div className="p-4"><LoadingSkeleton variant="list" count={5} /></div>
          ) : runs.length === 0 ? (
            <div className="p-6"><EmptyState icon="empty" title="No AI activity recorded" description="When the planner, tutor, evaluator, or advisor runs, every call is logged here with full input and output for your inspection." /></div>
          ) : runs.map((run) => (
            <button key={run.id} onClick={() => selectRun(run.id)}
              className={cn(
                "w-full text-left px-4 py-3 border-b border-(--color-border)/30 hover:bg-(--color-page) transition-colors duration-150",
                selected?.id === run.id && "bg-(--color-accent-light)",
              )}>
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium capitalize text-(--color-text)">{run.run_type}</span>
                <StatusBadge status={run.status} />
              </div>
              <div className="flex items-center gap-3 mt-1 text-xs text-(--color-text-secondary)">
                <span>{run.model_used || "\u2014"}</span>
                {run.input_tokens && <span>{run.input_tokens + (run.output_tokens || 0)} tokens</span>}
                <span>{new Date(run.created_at).toLocaleString()}</span>
              </div>
            </button>
          ))}
        </Card>

        <Card padding="p-0">
          {selected ? (
            <div className="p-5">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium capitalize text-(--color-text)">{selected.run_type} Run</h3>
                <div className="flex items-center gap-2">
                  <StatusBadge status={selected.status} />
                  {selected.model_used === "mock" && (
                    <span className="text-[10px] px-1.5 py-0.5 bg-(--color-warning-light) text-(--color-warning) rounded-[4px] font-medium">MOCK</span>
                  )}
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 mb-4 text-xs">
                {[
                  { label: "Model", value: selected.model_used || "\u2014" },
                  { label: "Tokens", value: `${selected.input_tokens || 0} in / ${selected.output_tokens || 0} out` },
                  { label: "Time", value: selected.started_at && selected.completed_at ? `${Math.round((new Date(selected.completed_at).getTime() - new Date(selected.started_at).getTime()))}ms` : "\u2014" },
                ].map((m) => (
                  <div key={m.label} className="bg-(--color-page) rounded-[6px] p-2">
                    <div className="text-(--color-text-tertiary)">{m.label}</div>
                    <div className="font-mono mt-0.5 text-(--color-text)">{m.value}</div>
                  </div>
                ))}
              </div>
              <div className="space-y-3">
                <div>
                  <div className="text-xs font-medium text-(--color-text-secondary) mb-1">INPUT</div>
                  <pre className="text-[11px] font-mono bg-(--color-page) rounded-[6px] p-3 overflow-auto max-h-48 whitespace-pre-wrap break-words text-(--color-text-secondary)">
                    {JSON.stringify(selected.input_data, null, 2)}
                  </pre>
                </div>
                <div>
                  <div className="text-xs font-medium text-(--color-text-secondary) mb-1">OUTPUT</div>
                  <pre className="text-[11px] font-mono bg-(--color-page) rounded-[6px] p-3 overflow-auto max-h-48 whitespace-pre-wrap break-words text-(--color-text-secondary)">
                    {JSON.stringify(selected.output_data, null, 2)}
                  </pre>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-8 text-center text-sm text-(--color-text-tertiary)">
              Select an AI run to inspect its full input/output.
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
