"use client";

import { useEffect, useState } from "react";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import StatusBadge from "@/components/StatusBadge";
import MetricCard from "@/components/ui/MetricCard";
import SectionHeader from "@/components/ui/SectionHeader";
import EmptyState from "@/components/ui/EmptyState";
import { ShieldIcon } from "@/components/ConstitutionalCeremony";
import { cn } from "@/lib/cn";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

function getCsrf(): string | undefined {
  if (typeof document === "undefined") return undefined;
  const m = document.cookie.match(/(?:^|; )csrf_token=([^;]*)/);
  return m ? decodeURIComponent(m[1]) : undefined;
}

// CSS bar chart component (no external deps)
function BarChart({ data, maxValue }: { data: Array<{ label: string; value: number; color: string }>; maxValue?: number }) {
  const max = maxValue || Math.max(...data.map((d) => d.value), 1);
  return (
    <div className="space-y-2">
      {data.map((d) => (
        <div key={d.label} className="flex items-center gap-3">
          <span className="text-xs text-(--color-text-secondary) w-24 text-right truncate">{d.label}</span>
          <div className="flex-1 h-5 bg-(--color-page) rounded-[6px] overflow-hidden">
            <div className="h-full rounded-[6px] transition-all duration-500" style={{ width: `${(d.value / max) * 100}%`, background: d.color }} />
          </div>
          <span className="text-xs font-mono text-(--color-text) w-8 text-right">{d.value}</span>
        </div>
      ))}
    </div>
  );
}

export default function ReportsPage() {
  useEffect(() => { document.title = "Reports | METHEAN"; }, []);

  const [startDate, setStartDate] = useState(() => {
    const d = new Date(); d.setDate(d.getDate() - 30);
    return d.toISOString().split("T")[0];
  });
  const [endDate, setEndDate] = useState(() => new Date().toISOString().split("T")[0]);
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [attestText, setAttestText] = useState("");
  const [attested, setAttested] = useState(false);

  function setPreset(days: number) {
    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - days);
    setStartDate(start.toISOString().split("T")[0]);
    setEndDate(end.toISOString().split("T")[0]);
  }

  async function generate() {
    setLoading(true);
    setReport(null);
    setAttested(false);
    setError("");
    try {
      const csrf = getCsrf();
      const resp = await fetch(`${API}/governance/report`, {
        method: "POST", credentials: "include",
        headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
        body: JSON.stringify({ period_start: startDate, period_end: endDate }),
      });
      if (resp.ok) setReport(await resp.json());
      else setError("Failed to generate report.");
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't generate report.");
    } finally { setLoading(false); }
  }

  async function attest() {
    if (!attestText.trim() || attestText.length < 10) return;
    const csrf = getCsrf();
    const resp = await fetch(`${API}/governance/report/attest`, {
      method: "POST", credentials: "include",
      headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
      body: JSON.stringify({ report_id: report?.generated_at || "report", attestation_text: attestText }),
    });
    if (resp.ok) setAttested(true);
  }

  const s = report?.executive_summary;
  const decisions = report?.governance_decisions || [];
  const aiRoles = Object.entries(report?.ai_oversight?.runs_by_role || {}) as Array<[string, number]>;
  const ruleEnforcement = report?.rule_enforcement || {};
  const constitutionalActions = report?.constitutional_actions || [];

  // Compute decision breakdown for bar chart
  const decisionCounts = {
    approved: decisions.filter((d: any) => d.action === "approve").length,
    rejected: decisions.filter((d: any) => d.action === "reject").length,
    modified: decisions.filter((d: any) => d.action === "modify").length,
    deferred: decisions.filter((d: any) => d.action === "defer").length,
  };

  // Compute auto vs manual for review rate
  const autoApproved = decisions.filter((d: any) => d.action === "approve" && (d.reason || "").toLowerCase().includes("auto")).length;
  const manualDecisions = decisions.length - autoApproved;
  const reviewRate = decisions.length > 0 ? Math.round((manualDecisions / decisions.length) * 100) : 100;

  return (
    <div className="max-w-5xl">
      <PageHeader
        title="Governance Analytics"
        subtitle="Visualize your family's educational oversight."
        actions={
          <button onClick={() => window.print()} className="text-xs text-(--color-text-tertiary) hover:text-(--color-text-secondary) print:hidden">
            Print Report
          </button>
        }
      />

      {/* Print header */}
      <div className="governance-report-print-header hidden print:block mb-6">
        <h1 className="text-lg font-bold">METHEAN Governance Report</h1>
        <p className="text-sm text-(--color-text-secondary)">{report?.household?.name} · {startDate} to {endDate} · Generated {new Date().toLocaleDateString()}</p>
      </div>

      {/* ── Period Selector ── */}
      <div className="print:hidden">
        <div className="flex flex-col sm:flex-row items-start sm:items-end gap-3 mb-6">
          <div className="flex gap-3">
            <div>
              <label className="block text-xs text-(--color-text-secondary) mb-1">From</label>
              <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)}
                className="px-3 py-1.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)" />
            </div>
            <div>
              <label className="block text-xs text-(--color-text-secondary) mb-1">To</label>
              <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)}
                className="px-3 py-1.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)" />
            </div>
          </div>
          <div className="flex gap-1.5 flex-wrap">
            {[["7d", 7], ["30d", 30], ["90d", 90], ["1y", 365]] .map(([label, days]) => (
              <button key={label as string} onClick={() => setPreset(days as number)}
                className="px-2.5 py-1 text-[10px] font-medium rounded-[10px] border border-(--color-border) text-(--color-text-secondary) hover:bg-(--color-page)">
                {label}
              </button>
            ))}
          </div>
          <Button variant="primary" size="md" onClick={generate} disabled={loading}>
            {loading ? "Generating..." : "Generate Report"}
          </Button>
        </div>
      </div>

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button variant="ghost" size="sm" onClick={() => { setError(""); generate(); }}>Retry</Button>
          </div>
        </Card>
      )}

      {loading && <LoadingSkeleton variant="card" count={4} />}

      {!loading && !report && !error && (
        <EmptyState icon="empty" title="No report generated yet"
          description="Select a date range and click Generate Report to see governance analytics." />
      )}

      {report && (
        <div className="space-y-6 print:space-y-4">
          {/* ── Section 2: Executive Summary ── */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
            <MetricCard label="Total Decisions" value={s?.total_governance_events || 0} />
            <MetricCard label="Parent Review Rate" value={`${reviewRate}%`} color={reviewRate > 50 ? "success" : reviewRate > 20 ? "warning" : "danger"} />
            <MetricCard label="AI Calls" value={s?.ai_runs_count || 0} />
            <MetricCard label="Constitutional Changes" value={s?.constitutional_changes_count || 0} />
          </div>

          {/* ── Section 3: Decision Breakdown ── */}
          <Card>
            <SectionHeader title="Decision Breakdown" />
            <div className="mt-3">
              <BarChart data={[
                { label: "Approved", value: decisionCounts.approved, color: "#2D6A4F" },
                { label: "Rejected", value: decisionCounts.rejected, color: "#A63D40" },
                { label: "Modified", value: decisionCounts.modified, color: "#B8860B" },
                { label: "Deferred", value: decisionCounts.deferred, color: "#4A6FA5" },
              ]} />
            </div>
          </Card>

          {/* ── Section 4: AI Oversight ── */}
          {aiRoles.length > 0 && (
            <Card>
              <SectionHeader title="AI Usage by Role" />
              <div className="mt-3">
                <BarChart data={aiRoles.map(([role, count]) => ({
                  label: role.charAt(0).toUpperCase() + role.slice(1).replace(/_/g, " "),
                  value: count,
                  color: "#4A6FA5",
                }))} />
              </div>
              <p className="text-[10px] text-(--color-text-tertiary) mt-2">
                {s?.ai_runs_count || 0} total AI calls · Acceptance rate: {s?.ai_acceptance_rate_pct ?? "N/A"}%
              </p>
            </Card>
          )}

          {/* ── Section 5: Rule Enforcement ── */}
          {Object.keys(ruleEnforcement).length > 0 && (
            <Card padding="p-0">
              <div className="px-5 py-3 border-b border-(--color-border)">
                <SectionHeader title="Rule Enforcement Summary" />
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-xs">
                  <thead>
                    <tr className="border-b border-(--color-border)">
                      <th className="text-left px-5 py-2 text-(--color-text-secondary) font-medium">Rule</th>
                      <th className="text-left px-3 py-2 text-(--color-text-secondary) font-medium">Type</th>
                      <th className="text-right px-3 py-2 text-(--color-text-secondary) font-medium">Evaluated</th>
                      <th className="text-right px-3 py-2 text-(--color-text-secondary) font-medium">Triggered</th>
                      <th className="text-right px-5 py-2 text-(--color-text-secondary) font-medium">Trigger Rate</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(ruleEnforcement).map(([name, data]: [string, any]) => (
                      <tr key={name} className="border-b border-(--color-border)/30">
                        <td className="px-5 py-2 text-(--color-text) font-medium">{name}</td>
                        <td className="px-3 py-2 text-(--color-text-secondary) capitalize">{data.type?.replace(/_/g, " ")}</td>
                        <td className="px-3 py-2 text-right text-(--color-text)">{data.evaluated}</td>
                        <td className="px-3 py-2 text-right">
                          <span className={data.triggered > 0 ? "text-(--color-warning) font-medium" : "text-(--color-text-tertiary)"}>{data.triggered}</span>
                        </td>
                        <td className="px-5 py-2 text-right text-(--color-text-secondary)">
                          {data.evaluated > 0 ? `${Math.round((data.triggered / data.evaluated) * 100)}%` : "—"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          )}

          {/* ── Section 6: Per-Child Governance ── */}
          {(report.learning_progress || []).length > 0 && (
            <Card>
              <SectionHeader title="Per-Child Governance Profile" />
              <div className="mt-3 space-y-3">
                {(report.learning_progress || []).map((cp: any) => (
                  <div key={cp.child_id} className="flex items-center justify-between py-2 px-3 rounded-[10px] bg-(--color-page)">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-(--color-accent) text-white flex items-center justify-center text-xs font-bold">
                        {cp.child_name?.charAt(0)}
                      </div>
                      <div>
                        <span className="text-xs font-medium text-(--color-text)">{cp.child_name}</span>
                        {cp.grade_level && <span className="text-[10px] text-(--color-text-tertiary) ml-1">{cp.grade_level}</span>}
                      </div>
                    </div>
                    <div className="flex gap-4 text-xs text-(--color-text-secondary)">
                      <span>{cp.nodes_mastered}/{cp.nodes_total} mastered</span>
                      <span>{cp.total_hours}h logged</span>
                      <span>{cp.total_attempts} attempts</span>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* ── Section 7: Constitutional History ── */}
          <Card>
            <SectionHeader title="Constitutional Rule History" />
            {constitutionalActions.length === 0 ? (
              <p className="text-xs text-(--color-text-secondary) mt-2 italic">
                No constitutional changes during this period. Your foundational principles remained stable.
              </p>
            ) : (
              <div className="mt-3 space-y-2">
                {constitutionalActions.map((ca: any, i: number) => (
                  <div key={i} className="flex items-start gap-2 px-3 py-2 rounded-[10px] bg-(--color-constitutional-light) border-l-2 border-(--color-constitutional)">
                    <ShieldIcon size={14} className="text-(--color-constitutional) shrink-0 mt-0.5" />
                    <div>
                      <span className="text-xs text-(--color-text-secondary)">{ca.timestamp?.split("T")[0]}</span>
                      {ca.reason && <p className="text-xs text-(--color-constitutional) italic mt-0.5">"{ca.reason}"</p>}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>

          {/* ── Section 8: Attestation ── */}
          <Card className="print:break-before-page">
            <SectionHeader title="Parent Attestation" />
            {!attested ? (
              <div className="mt-3 print:hidden">
                <p className="text-xs text-(--color-text-secondary) mb-3">
                  By signing below, I attest that this report accurately reflects the governance
                  decisions made during this period, and that I was in control of my children's
                  educational program at all times.
                </p>
                <textarea
                  value={attestText}
                  onChange={(e) => setAttestText(e.target.value)}
                  placeholder="I confirm that this report is accurate and complete..."
                  className="w-full h-24 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] resize-none mb-3 bg-(--color-surface) text-(--color-text)"
                />
                <Button variant="primary" size="md" onClick={attest} disabled={attestText.length < 10}>
                  Attest &amp; Sign Report
                </Button>
              </div>
            ) : (
              <div className="mt-3 bg-(--color-success-light) border border-(--color-success)/30 rounded-[10px] p-4">
                <p className="text-sm text-(--color-success) font-medium mb-1">Report attested.</p>
                <p className="text-xs text-(--color-success)">"{attestText}"</p>
                <p className="text-xs text-(--color-success) mt-2">Attested on {new Date().toLocaleDateString()}. Permanently recorded.</p>
              </div>
            )}
          </Card>
        </div>
      )}
    </div>
  );
}
