"use client";

import { useEffect, useState, useMemo } from "react";
import { ai, type AIRun, type ContextDetailResponse } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import MetricCard from "@/components/ui/MetricCard";
import SectionHeader from "@/components/ui/SectionHeader";
import EmptyState from "@/components/ui/EmptyState";
import { cn } from "@/lib/cn";
import { relativeTime } from "@/lib/format";

// ── Role colors for badges ──
const ROLE_COLORS: Record<string, { bg: string; text: string }> = {
  planner:      { bg: "bg-(--color-accent-light)",         text: "text-(--color-accent)" },
  tutor:        { bg: "bg-(--color-success-light)",        text: "text-(--color-success)" },
  evaluator:    { bg: "bg-(--color-warning-light)",        text: "text-(--color-warning)" },
  advisor:      { bg: "bg-(--color-constitutional-light)", text: "text-(--color-constitutional)" },
  cartographer: { bg: "bg-(--color-danger-light)",         text: "text-(--color-danger)" },
  enricher:     { bg: "bg-(--color-accent-light)",         text: "text-(--color-accent)" },
  reflector:    { bg: "bg-(--color-success-light)",        text: "text-(--color-success)" },
  assessor:     { bg: "bg-(--color-warning-light)",        text: "text-(--color-warning)" },
};
const DEFAULT_ROLE_COLOR = { bg: "bg-(--color-page)", text: "text-(--color-text-secondary)" };

function RoleBadge({ role }: { role: string }) {
  const c = ROLE_COLORS[role] || DEFAULT_ROLE_COLOR;
  return (
    <span className={cn("px-2 py-0.5 rounded-[6px] text-[11px] font-semibold capitalize", c.bg, c.text)}>
      {role}
    </span>
  );
}

// ── Helpers ──
function durationMs(run: AIRun): number | null {
  if (!run.started_at || !run.completed_at) return null;
  return new Date(run.completed_at).getTime() - new Date(run.started_at).getTime();
}

function formatDuration(ms: number | null): string {
  if (ms === null) return "—";
  if (ms < 1000) return `${ms}ms`;
  return `${(ms / 1000).toFixed(1)}s`;
}

function formatTokens(input: number | null, output: number | null): string {
  return `${(input || 0).toLocaleString()} in / ${(output || 0).toLocaleString()} out`;
}

function estimateCost(input: number | null, output: number | null): string {
  const cost = ((input || 0) * 3 + (output || 0) * 15) / 1_000_000;
  if (cost < 0.01) return "< $0.01";
  return `$${cost.toFixed(2)}`;
}

function hasPhilosophicalConstraints(run: AIRun): boolean {
  const input = run.input_data as any;
  if (!input) return false;
  const prompt = input.system_prompt || input.system || "";
  return typeof prompt === "string" && prompt.includes("PHILOSOPHICAL CONSTRAINTS");
}

function extractConstraintsBlock(systemPrompt: string): { constraints: string[]; rest: string } {
  // Try to find the philosophical constraints section
  const markers = [
    /PHILOSOPHICAL CONSTRAINTS[:\s]*\n([\s\S]*?)(?:\n\n[A-Z]|\n---|\n##|$)/i,
    /={2,}\s*PHILOSOPHICAL CONSTRAINTS\s*={2,}\n([\s\S]*?)(?:\n={2,}|\n\n[A-Z]|\n---|\n##|$)/i,
  ];

  for (const re of markers) {
    const match = systemPrompt.match(re);
    if (match) {
      const block = match[0];
      const body = match[1].trim();
      const constraints = body
        .split("\n")
        .map((line) => line.replace(/^[-*•]\s*/, "").trim())
        .filter(Boolean);
      const rest = systemPrompt.replace(block, "").trim();
      return { constraints, rest };
    }
  }

  // Fallback: grab everything between the marker and next double-newline
  const idx = systemPrompt.indexOf("PHILOSOPHICAL CONSTRAINTS");
  if (idx !== -1) {
    const after = systemPrompt.substring(idx);
    const end = after.indexOf("\n\n", 30);
    const block = end > 0 ? after.substring(0, end) : after;
    const body = block.replace(/^.*PHILOSOPHICAL CONSTRAINTS[:\s]*/i, "").trim();
    const constraints = body.split("\n").map((l) => l.replace(/^[-*•]\s*/, "").trim()).filter(Boolean);
    const rest = systemPrompt.substring(0, idx).trim() + (end > 0 ? "\n" + systemPrompt.substring(idx + end).trim() : "");
    return { constraints, rest };
  }

  // Last resort: split everything after "PHILOSOPHICAL CONSTRAINTS" by newlines
  const lastIdx = systemPrompt.toUpperCase().indexOf("PHILOSOPHICAL CONSTRAINTS");
  if (lastIdx !== -1) {
    const afterMarker = systemPrompt.substring(lastIdx);
    const firstNewline = afterMarker.indexOf("\n");
    if (firstNewline > 0) {
      const body = afterMarker.substring(firstNewline).trim();
      const endIdx = body.indexOf("\n\n");
      const section = endIdx > 0 ? body.substring(0, endIdx) : body;
      const lines = section.split("\n")
        .map((l) => l.replace(/^[-*•]\s*/, "").trim())
        .filter((l) => l.length > 0 && l.length < 300);
      if (lines.length > 0) {
        const block = afterMarker.substring(0, firstNewline + (endIdx > 0 ? endIdx : section.length) + 1);
        return { constraints: lines.slice(0, 20), rest: systemPrompt.replace(block, "").trim() };
      }
    }
  }

  return { constraints: [], rest: systemPrompt };
}

// ── Smart output rendering ──
function RenderEvaluatorOutput({ data }: { data: any }) {
  const rating = data.quality_rating ?? data.rating ?? data.score;
  const confidence = data.confidence_score ?? data.confidence;
  return (
    <div className="space-y-3">
      {rating != null && (
        <div>
          <div className="text-[11px] font-medium text-(--color-text-tertiary) uppercase mb-1">Quality Rating</div>
          <div className="flex items-center gap-1">
            {[1, 2, 3, 4, 5].map((i) => (
              <span key={i} className={cn("w-5 h-5 rounded-full border-2 flex items-center justify-center text-[10px]",
                i <= rating
                  ? "bg-(--color-success) border-(--color-success) text-white"
                  : "border-(--color-border-strong) text-(--color-text-tertiary)"
              )}>{i <= rating ? "●" : "○"}</span>
            ))}
            <span className="ml-2 text-xs text-(--color-text-secondary)">{rating} / 5</span>
          </div>
        </div>
      )}
      {confidence != null && (
        <div>
          <div className="text-[11px] font-medium text-(--color-text-tertiary) uppercase mb-1">Confidence</div>
          <div className="flex items-center gap-2">
            <div className="flex-1 h-2 rounded-full bg-(--color-border)">
              <div className="h-full rounded-full bg-(--color-accent) transition-all" style={{ width: `${Math.round(confidence * 100)}%` }} />
            </div>
            <span className="text-xs font-mono text-(--color-text-secondary)">{Math.round(confidence * 100)}%</span>
          </div>
        </div>
      )}
      {data.feedback && (
        <div>
          <div className="text-[11px] font-medium text-(--color-text-tertiary) uppercase mb-1">Feedback</div>
          <p className="text-xs text-(--color-text-secondary)">{data.feedback}</p>
        </div>
      )}
      <RenderGenericOutput data={data} exclude={["quality_rating", "rating", "score", "confidence_score", "confidence", "feedback"]} />
    </div>
  );
}

function RenderPlannerOutput({ data }: { data: any }) {
  const activities = data.activities || data.plan || data.schedule;
  if (!Array.isArray(activities)) return <RenderGenericOutput data={data} />;
  return (
    <div className="space-y-2">
      {activities.map((act: any, i: number) => (
        <div key={i} className="flex items-start gap-3 bg-(--color-page) rounded-[10px] p-3">
          <div className="w-6 h-6 rounded-full bg-(--color-accent-light) flex items-center justify-center text-[10px] font-bold text-(--color-accent) shrink-0 mt-0.5">
            {i + 1}
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-0.5">
              <span className="text-xs font-medium text-(--color-text)">{act.title || act.name || `Activity ${i + 1}`}</span>
              {act.activity_type && (
                <span className="px-1.5 py-0.5 text-[10px] rounded-[4px] bg-(--color-accent-light) text-(--color-accent) font-medium capitalize">
                  {act.activity_type}
                </span>
              )}
              {act.estimated_minutes && (
                <span className="text-[10px] text-(--color-text-tertiary)">{act.estimated_minutes} min</span>
              )}
            </div>
            {act.rationale && <p className="text-[11px] text-(--color-text-secondary) leading-relaxed">{act.rationale}</p>}
            {act.description && !act.rationale && <p className="text-[11px] text-(--color-text-secondary) leading-relaxed">{act.description}</p>}
          </div>
        </div>
      ))}
      <RenderGenericOutput data={data} exclude={["activities", "plan", "schedule"]} />
    </div>
  );
}

function RenderGenericOutput({ data, exclude = [] }: { data: any; exclude?: string[] }) {
  if (!data || typeof data !== "object") return null;
  const entries = Object.entries(data).filter(([k]) => !exclude.includes(k));
  if (entries.length === 0) return null;
  return (
    <div className="space-y-1.5">
      {entries.map(([key, val]) => (
        <div key={key} className="flex gap-2 text-xs">
          <span className="text-(--color-text-tertiary) font-mono shrink-0 w-28 truncate">{key}</span>
          <span className="text-(--color-text-secondary) break-words min-w-0">
            {typeof val === "string" ? val : JSON.stringify(val, null, 2)}
          </span>
        </div>
      ))}
    </div>
  );
}

// ── Context Breakdown Panel ──

function ContextBreakdown({ runId }: { runId: string }) {
  const [detail, setDetail] = useState<ContextDetailResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [expandedSource, setExpandedSource] = useState<string | null>(null);

  useEffect(() => {
    ai.contextDetail(runId).then(setDetail).catch(() => setDetail(null)).finally(() => setLoading(false));
  }, [runId]);

  if (loading) return <div className="py-3 text-center"><div className="w-4 h-4 border-2 border-(--color-accent) border-t-transparent rounded-full animate-spin mx-auto" /></div>;
  if (!detail || detail.legacy) return null;
  if (!detail.sources.length && !detail.sources_excluded.length) return null;

  const pct = detail.token_budget > 0 ? (detail.tokens_used / detail.token_budget) * 100 : 0;
  const hasAllRequired = detail.sources.every(s => !s.required || s.tokens > 0);
  const hasTruncation = detail.sources.some(s => s.truncated);
  const quality = pct >= 80 && !hasTruncation && hasAllRequired ? "green"
    : pct >= 50 ? "yellow"
    : "red";
  const qualityColor = quality === "green" ? "var(--color-success)" : quality === "yellow" ? "var(--color-warning)" : "var(--color-danger)";
  const qualityLabel = quality === "green" ? "Excellent" : quality === "yellow" ? "Moderate" : "Limited";

  return (
    <div className="space-y-3">
      {/* Quality + budget bar */}
      <div className="flex items-center justify-between mb-1">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full" style={{ background: qualityColor }} />
          <span className="text-[11px] font-medium" style={{ color: qualityColor }}>{qualityLabel} context</span>
        </div>
        <span className="text-[10px] text-(--color-text-tertiary)">{detail.tokens_used} / {detail.token_budget} tokens ({pct.toFixed(0)}%)</span>
      </div>

      {/* Token budget bar */}
      <div className="h-3 rounded-full bg-(--color-page) overflow-hidden flex">
        {detail.sources.map((s, i) => {
          const segPct = detail.token_budget > 0 ? (s.tokens / detail.token_budget) * 100 : 0;
          if (segPct < 0.5) return null;
          const colors = ["var(--color-accent)", "var(--color-success)", "var(--color-warning)", "#8B5CF6", "#0D9488", "var(--color-constitutional)"];
          return (
            <div key={s.name} className="h-full transition-all" title={`${s.name}: ${s.tokens} tokens`}
              style={{ width: `${segPct}%`, background: colors[i % colors.length], opacity: s.required ? 1 : 0.6 }} />
          );
        })}
      </div>

      {/* Source list */}
      <div className="space-y-1">
        {detail.sources.map(s => (
          <div key={s.name}>
            <button onClick={() => setExpandedSource(expandedSource === s.name ? null : s.name)}
              className="w-full flex items-center justify-between py-1 text-left hover:bg-(--color-page) rounded px-1 -mx-1">
              <div className="flex items-center gap-1.5">
                <span className="text-[11px] text-(--color-text)">{s.name.replace(/_/g, " ")}</span>
                {s.required && <span className="text-[9px] px-1 py-0 rounded bg-(--color-accent)/10 text-(--color-accent)">required</span>}
                {s.truncated && <span className="text-[9px] px-1 py-0 rounded bg-(--color-warning)/10 text-(--color-warning)">truncated</span>}
              </div>
              <span className="text-[10px] text-(--color-text-tertiary)">{s.tokens} tok</span>
            </button>
            {expandedSource === s.name && detail.context_text && (
              <pre className="text-[10px] font-mono bg-(--color-page) rounded-[8px] p-2 mt-1 mb-2 max-h-32 overflow-auto whitespace-pre-wrap text-(--color-text-secondary)">
                {detail.context_text.split("\n\n")[detail.sources.indexOf(s)] || "(source text)"}
              </pre>
            )}
          </div>
        ))}
        {detail.sources_excluded.map(name => (
          <div key={name} className="flex items-center justify-between py-1 px-1 opacity-50">
            <span className="text-[11px] text-(--color-text-tertiary)">{name.replace(/_/g, " ")}</span>
            <span className="text-[9px] text-(--color-text-tertiary)">excluded (budget)</span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Main page ──
export default function InspectionPage() {
  useEffect(() => { document.title = "AI Inspection | METHEAN"; }, []);

  const [runs, setRuns] = useState<AIRun[]>([]);
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [expandedDetail, setExpandedDetail] = useState<AIRun | null>(null);
  const [filterRole, setFilterRole] = useState("");
  const [filterStatus, setFilterStatus] = useState<"" | "completed" | "failed">("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => { loadRuns(); }, [filterRole]);

  async function loadRuns() {
    setLoading(true);
    setError("");
    try {
      const data = await ai.runs(filterRole ? { role: filterRole } : undefined);
      setRuns(data);
    } catch (err: any) {
      setError(err?.message || "Failed to load AI runs.");
    } finally {
      setLoading(false);
    }
  }

  async function toggleExpand(run: AIRun) {
    if (expandedId === run.id) {
      setExpandedId(null);
      setExpandedDetail(null);
      return;
    }
    setExpandedId(run.id);
    try {
      const detail = await ai.run(run.id);
      setExpandedDetail(detail);
    } catch {
      setExpandedDetail(run);
    }
  }

  // ── Computed metrics ──
  const metrics = useMemo(() => {
    const total = runs.length;
    const succeeded = runs.filter((r) => r.status === "completed").length;
    const successRate = total > 0 ? Math.round((succeeded / total) * 100) : 0;

    const durations = runs.map(durationMs).filter((d): d is number => d !== null);
    const avgMs = durations.length > 0 ? durations.reduce((a, b) => a + b, 0) / durations.length : 0;

    const hasConstraints = runs.some(hasPhilosophicalConstraints);

    return { total, successRate, avgDuration: formatDuration(avgMs), hasConstraints };
  }, [runs]);

  // ── Filtered runs ──
  const filtered = useMemo(() => {
    if (!filterStatus) return runs;
    return runs.filter((r) => r.status === filterStatus);
  }, [runs, filterStatus]);

  const roles = ["planner", "tutor", "evaluator", "advisor", "cartographer", "enricher", "reflector", "assessor"];

  if (loading) {
    return (
      <div className="max-w-4xl">
        <PageHeader title="AI Inspection" subtitle="Every AI interaction, fully transparent." />
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
          {[1, 2, 3, 4].map((i) => <LoadingSkeleton key={i} variant="card" count={1} />)}
        </div>
        <LoadingSkeleton variant="card" count={4} />
      </div>
    );
  }

  return (
    <div className="max-w-4xl">
      <PageHeader title="AI Inspection" subtitle="Every AI interaction, fully transparent." />

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <button onClick={loadRuns} className="text-xs text-(--color-accent) hover:underline">Retry</button>
          </div>
        </Card>
      )}

      {/* ── Metrics ── */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        <MetricCard label="Total AI Calls" value={metrics.total} />
        <MetricCard label="Success Rate" value={`${metrics.successRate}%`} color={metrics.successRate >= 90 ? "text-(--color-success)" : "text-(--color-warning)"} />
        <MetricCard label="Avg Response Time" value={metrics.avgDuration} />
        <MetricCard
          label="Philosophical Constraints"
          value={metrics.hasConstraints ? "Active" : "None"}
          color={metrics.hasConstraints ? "text-(--color-success)" : "text-(--color-text-tertiary)"}
          subtitle={metrics.hasConstraints ? "Injected into AI calls" : "No constraints detected"}
        />
      </div>

      {/* ── Filters ── */}
      <div className="flex flex-col sm:flex-row sm:items-center gap-3 mb-5">
        {/* Role pills */}
        <div className="flex gap-1.5 overflow-x-auto pb-1 -mb-1">
          <button
            onClick={() => setFilterRole("")}
            className={cn(
              "px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap transition-colors",
              !filterRole ? "bg-(--color-text) text-white" : "bg-(--color-page) text-(--color-text-secondary) hover:bg-(--color-border)"
            )}
          >All Roles</button>
          {roles.map((r) => (
            <button key={r} onClick={() => setFilterRole(filterRole === r ? "" : r)}
              className={cn(
                "px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap capitalize transition-colors",
                filterRole === r ? "bg-(--color-text) text-white" : "bg-(--color-page) text-(--color-text-secondary) hover:bg-(--color-border)"
              )}
            >{r}</button>
          ))}
        </div>

        {/* Status filter */}
        <div className="flex gap-1.5 sm:ml-auto shrink-0">
          {([["", "All"], ["completed", "Completed"], ["failed", "Failed"]] as const).map(([val, label]) => (
            <button key={val} onClick={() => setFilterStatus(filterStatus === val ? "" : val as any)}
              className={cn(
                "px-3 py-1 rounded-full text-xs font-medium transition-colors",
                filterStatus === val ? "bg-(--color-text) text-white" : "bg-(--color-page) text-(--color-text-secondary) hover:bg-(--color-border)"
              )}
            >{label}</button>
          ))}
        </div>
      </div>

      {/* ── Run list ── */}
      {filtered.length === 0 && !loading ? (
        <EmptyState
          icon="empty"
          title="No AI interactions yet"
          description="Generate a plan or start a learning activity. Every AI call will be logged here with full input and output for your review."
        />
      ) : (
        <div className="space-y-2">
          {filtered.map((run) => {
            const isExpanded = expandedId === run.id;
            const detail = isExpanded ? expandedDetail : null;
            const ms = durationMs(run);

            return (
              <Card key={run.id} padding="p-0">
                {/* ── Collapsed row ── */}
                <button
                  onClick={() => toggleExpand(run)}
                  className="w-full text-left px-4 py-3.5 transition-colors hover:bg-(--color-page)/50"
                >
                  <div className="flex items-center gap-2 flex-wrap">
                    <RoleBadge role={run.run_type} />
                    <StatusBadge status={run.status} />
                    {run.model_used && (
                      <span className="text-[11px] font-mono text-(--color-text-tertiary)">{run.model_used}</span>
                    )}
                    <span className="text-[11px] text-(--color-text-tertiary) ml-auto">{relativeTime(run.created_at)}</span>
                    <svg className={cn("w-4 h-4 text-(--color-text-tertiary) transition-transform", isExpanded && "rotate-180")}
                      fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                  <div className="flex items-center gap-4 mt-1.5 text-[11px] text-(--color-text-tertiary)">
                    {ms !== null && <span>{formatDuration(ms)}</span>}
                    {(run.input_tokens || run.output_tokens) && (
                      <span>{formatTokens(run.input_tokens, run.output_tokens)}</span>
                    )}
                    {(run.input_tokens || run.output_tokens) && (
                      <span>{estimateCost(run.input_tokens, run.output_tokens)}</span>
                    )}
                    {hasPhilosophicalConstraints(run) && (
                      <span className="flex items-center gap-1 text-(--color-constitutional) font-medium">
                        <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clipRule="evenodd" />
                        </svg>
                        Constraints active
                      </span>
                    )}
                  </div>
                </button>

                {/* ── Expanded detail ── */}
                {isExpanded && (
                  <div className="border-t border-(--color-border) px-4 py-5 space-y-6">
                    {!detail ? (
                      <div className="py-6 flex justify-center">
                        <div className="w-5 h-5 border-2 border-(--color-accent) border-t-transparent rounded-full animate-spin" />
                      </div>
                    ) : (
                      <>
                        {/* ── Section A: What We Asked the AI ── */}
                        <div>
                          <SectionHeader title="What We Asked the AI" />
                          <PromptSection inputData={detail.input_data} />
                        </div>

                        {/* ── Section A.5: Context Breakdown ── */}
                        <div>
                          <SectionHeader title="Context Provided" />
                          <ContextBreakdown runId={detail.id} />
                        </div>

                        {/* ── Section B: What the AI Returned ── */}
                        <div>
                          <SectionHeader title="What the AI Returned" />
                          <OutputSection run={detail} />
                        </div>

                        {/* ── Section C: Governance Decision ── */}
                        <div>
                          <SectionHeader title="Governance Decision" />
                          <div className="bg-(--color-page) rounded-[10px] p-3 text-xs text-(--color-text-secondary)">
                            Every AI output passes through your family&apos;s governance rules before reaching your child.
                            <a href="/governance/trace" className="text-(--color-accent) hover:underline ml-1">
                              View governance trail &rarr;
                            </a>
                          </div>
                        </div>
                      </>
                    )}
                  </div>
                )}
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}

// ── Prompt section with philosophical constraints highlight ──
function PromptSection({ inputData }: { inputData: object | null }) {
  if (!inputData) return <p className="text-xs text-(--color-text-tertiary)">No input data recorded.</p>;

  const input = inputData as any;
  const systemPrompt: string = input.system_prompt || input.system || "";
  const userPrompt: string = input.user_prompt || input.prompt || input.message || "";

  if (!systemPrompt && !userPrompt) {
    return (
      <pre className="text-[11px] font-mono bg-(--color-page) rounded-[10px] p-3 overflow-auto max-h-[200px] whitespace-pre-wrap break-words text-(--color-text-secondary)">
        {JSON.stringify(inputData, null, 2)}
      </pre>
    );
  }

  const { constraints, rest } = systemPrompt ? extractConstraintsBlock(systemPrompt) : { constraints: [], rest: "" };
  const hasPhilo = systemPrompt ? hasPhilosophicalConstraints({ input_data: inputData } as any) : false;

  return (
    <div className="space-y-3">
      {/* ★ PHILOSOPHICAL CONSTRAINTS — the star feature ★ */}
      {constraints.length > 0 && (
        <div className="bg-(--color-constitutional-light) border-l-4 border-(--color-constitutional) rounded-r-[10px] p-4">
          <div className="flex items-center gap-2 mb-2.5">
            <svg className="w-5 h-5 text-(--color-constitutional)" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 2.18l7 3.12v4.7c0 4.83-3.4 9.36-7 10.5-3.6-1.14-7-5.67-7-10.5V6.3l7-3.12z" />
              <path d="M12 6.5L9.5 9 11 10.5 9.5 12l2.5 2.5L14.5 12 13 10.5 14.5 9z" opacity="0.3" />
            </svg>
            <h4 className="text-sm font-semibold text-(--color-constitutional)">
              Your Philosophical Constraints
            </h4>
            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-(--color-constitutional)/10 text-(--color-constitutional) font-medium">
              injected into this call
            </span>
          </div>
          <ul className="space-y-1.5">
            {constraints.map((c, i) => (
              <li key={i} className="flex gap-2 text-xs text-(--color-text)">
                <span className="text-(--color-constitutional) shrink-0 mt-0.5">
                  <svg className="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </span>
                <span>{c}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Fallback: constraints detected but regex couldn't extract cleanly */}
      {hasPhilo && constraints.length === 0 && (
        <div className="bg-(--color-constitutional-light) border-l-4 border-(--color-constitutional) rounded-r-[10px] p-4">
          <div className="flex items-center gap-2 mb-2">
            <svg className="w-4 h-4 text-(--color-constitutional)" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 2.18l7 3.12v4.7c0 4.83-3.4 9.36-7 10.5-3.6-1.14-7-5.67-7-10.5V6.3l7-3.12z" />
            </svg>
            <span className="text-xs font-semibold text-(--color-constitutional)">Philosophical Constraints Detected</span>
          </div>
          <p className="text-xs text-(--color-text-secondary)">
            Your family's philosophical constraints were injected into this AI call. View the full system prompt below to see them in context.
          </p>
        </div>
      )}

      {/* System prompt (remainder) */}
      {rest && (
        <div>
          <div className="text-[11px] font-medium text-(--color-text-tertiary) uppercase mb-1">System Prompt</div>
          <pre className="text-[11px] font-mono bg-(--color-page) rounded-[10px] p-3 overflow-y-auto max-h-[200px] whitespace-pre-wrap break-words text-(--color-text-secondary)">
            {rest}
          </pre>
        </div>
      )}

      {/* User prompt */}
      {userPrompt && (
        <div>
          <div className="text-[11px] font-medium text-(--color-text-tertiary) uppercase mb-1">User Prompt</div>
          <pre className="text-[11px] font-mono bg-(--color-page) rounded-[10px] p-3 overflow-y-auto max-h-[200px] whitespace-pre-wrap break-words text-(--color-text-secondary)">
            {userPrompt}
          </pre>
        </div>
      )}
    </div>
  );
}

// ── Output section with smart role-specific rendering ──
function OutputSection({ run }: { run: AIRun }) {
  // Failed runs
  if (run.status === "failed") {
    return (
      <div className="bg-(--color-danger-light) rounded-[10px] p-3">
        <div className="flex items-center gap-2 mb-1">
          <svg className="w-4 h-4 text-(--color-danger)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <span className="text-xs font-semibold text-(--color-danger)">AI Call Failed</span>
        </div>
        <p className="text-xs text-(--color-danger)">{run.error_message || "Unknown error occurred."}</p>
      </div>
    );
  }

  if (!run.output_data) {
    return <p className="text-xs text-(--color-text-tertiary)">No output data recorded.</p>;
  }

  const data = run.output_data as any;
  const role = run.run_type;

  // Role-specific rendering
  if (role === "evaluator" || role === "assessor" || role === "reflector") {
    return <RenderEvaluatorOutput data={data} />;
  }
  if (role === "planner") {
    return <RenderPlannerOutput data={data} />;
  }

  // Generic: formatted key-value
  return <RenderGenericOutput data={data} />;
}
