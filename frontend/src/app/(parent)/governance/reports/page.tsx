"use client";

import { useEffect, useState } from "react";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import StatusBadge from "@/components/StatusBadge";
import MetricCard from "@/components/ui/MetricCard";
import EmptyState from "@/components/ui/EmptyState";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

function getCsrf(): string | undefined {
  if (typeof document === "undefined") return undefined;
  const m = document.cookie.match(/(?:^|; )csrf_token=([^;]*)/);
  return m ? decodeURIComponent(m[1]) : undefined;
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
  const [attestText, setAttestText] = useState("");
  const [attested, setAttested] = useState(false);

  async function generate() {
    setLoading(true);
    setReport(null);
    setAttested(false);
    try {
      const csrf = getCsrf();
      const resp = await fetch(`${API}/governance/report`, {
        method: "POST", credentials: "include",
        headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
        body: JSON.stringify({ period_start: startDate, period_end: endDate }),
      });
      if (resp.ok) setReport(await resp.json());
    } catch {} finally { setLoading(false); }
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

  return (
    <div className="max-w-4xl">
      <PageHeader
        title="Governance Report"
        subtitle="Board meeting minutes for your homeschool."
        actions={
          <button onClick={() => window.print()} className="text-xs text-(--color-text-tertiary) hover:text-(--color-text-secondary) print:hidden">
            Print
          </button>
        }
      />

      {/* Date range */}
      <div className="flex items-end gap-3 mb-6 print:hidden">
        <div>
          <label className="block text-xs text-(--color-text-secondary) mb-1">From</label>
          <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)}
            className="px-3 py-1.5 text-sm border border-(--color-border) rounded-[6px] bg-(--color-surface) text-(--color-text)" />
        </div>
        <div>
          <label className="block text-xs text-(--color-text-secondary) mb-1">To</label>
          <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)}
            className="px-3 py-1.5 text-sm border border-(--color-border) rounded-[6px] bg-(--color-surface) text-(--color-text)" />
        </div>
        <Button variant="primary" size="md" onClick={generate} disabled={loading}
          className="bg-(--color-text) hover:opacity-90">
          {loading ? "Generating..." : "Generate Report"}
        </Button>
      </div>

      {loading && <LoadingSkeleton variant="text" count={5} />}

      {!loading && !report && (
        <EmptyState icon="empty" title="No reports generated yet" description="Select a date range above and click Generate Report to see a summary of AI oversight and family progress." />
      )}

      {report && (
        <div className="space-y-6 print:space-y-4">
          {/* Header */}
          <div className="border-b-2 border-(--color-text) pb-4">
            <h2 className="text-lg font-bold text-(--color-text) uppercase tracking-wide">
              Governance Report
            </h2>
            <p className="text-sm text-(--color-text-secondary)">{report.household?.name}</p>
            <p className="text-xs text-(--color-text-secondary)">
              Period: {report.period?.start} to {report.period?.end} ({report.period?.days} days)
            </p>
            <p className="text-xs text-(--color-text-tertiary)">Generated: {new Date(report.generated_at).toLocaleString()}</p>
          </div>

          {/* Executive Summary */}
          <section>
            <h3 className="text-sm font-bold text-(--color-text) uppercase tracking-wider mb-2 border-b border-(--color-border) pb-1">
              1. Executive Summary
            </h3>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {[
                { label: "Activities Approved", value: s?.activities_approved },
                { label: "Activities Rejected", value: s?.activities_rejected },
                { label: "Parent Overrides", value: s?.overrides_count },
                { label: "AI Acceptance Rate", value: s?.ai_acceptance_rate_pct != null ? `${s.ai_acceptance_rate_pct}%` : "N/A" },
              ].map((m) => (
                <MetricCard key={m.label} label={m.label} value={m.value ?? 0} />
              ))}
            </div>
          </section>

          {/* AI Oversight */}
          <section>
            <h3 className="text-sm font-bold text-(--color-text) uppercase tracking-wider mb-2 border-b border-(--color-border) pb-1">
              2. AI Oversight
            </h3>
            <p className="text-xs text-(--color-text-secondary) mb-2">
              {report.ai_oversight?.total_ai_runs || 0} AI calls made. Acceptance rate: {report.ai_oversight?.acceptance_rate_pct ?? "N/A"}%.
            </p>
            {report.ai_oversight?.runs_by_role && (
              <div className="flex gap-3 text-xs text-(--color-text-secondary)">
                {Object.entries(report.ai_oversight.runs_by_role).map(([role, count]) => (
                  <span key={role} className="capitalize">{role}: {count as number}</span>
                ))}
              </div>
            )}
          </section>

          {/* Governance Decisions */}
          <section>
            <h3 className="text-sm font-bold text-(--color-text) uppercase tracking-wider mb-2 border-b border-(--color-border) pb-1">
              3. Governance Decisions ({report.governance_decisions?.length || 0})
            </h3>
            <div className="text-xs space-y-1 max-h-60 overflow-y-auto print:max-h-none">
              {(report.governance_decisions || []).slice(0, 20).map((d: any, i: number) => (
                <div key={i} className="flex justify-between py-1 border-b border-(--color-border)/30">
                  <div className="flex items-center gap-2">
                    <StatusBadge status={d.action} />
                    <span className="text-(--color-text-secondary)">{d.target_type}</span>
                    {d.reason && <span className="text-(--color-text-tertiary) truncate max-w-xs">{d.reason}</span>}
                  </div>
                  <span className="text-(--color-text-tertiary) shrink-0">{d.timestamp?.split("T")[0]}</span>
                </div>
              ))}
            </div>
          </section>

          {/* Learning Progress */}
          <section>
            <h3 className="text-sm font-bold text-(--color-text) uppercase tracking-wider mb-2 border-b border-(--color-border) pb-1">
              4. Learning Progress
            </h3>
            <div className="space-y-2">
              {(report.learning_progress || []).map((cp: any) => (
                <Card key={cp.child_id} padding="p-3" className="flex items-center justify-between">
                  <div>
                    <span className="text-sm font-medium text-(--color-text)">{cp.child_name}</span>
                    <span className="text-xs text-(--color-text-secondary) ml-2">{cp.grade_level || ""}</span>
                  </div>
                  <div className="flex gap-4 text-xs text-(--color-text-secondary)">
                    <span>{cp.nodes_mastered}/{cp.nodes_total} mastered</span>
                    <span>{cp.total_hours}h logged</span>
                    <span>{cp.total_attempts} attempts</span>
                  </div>
                </Card>
              ))}
            </div>
          </section>

          {/* Overrides */}
          {(report.overrides?.length || 0) > 0 && (
            <section>
              <h3 className="text-sm font-bold text-(--color-text) uppercase tracking-wider mb-2 border-b border-(--color-border) pb-1">
                5. Parent Overrides
              </h3>
              {report.overrides.map((o: any, i: number) => (
                <div key={i} className="text-xs border-l-2 border-(--color-warning) pl-3 py-1 mb-1">
                  <span className="text-(--color-text-tertiary)">{o.timestamp?.split("T")[0]}</span>
                  {o.reason && <span className="text-(--color-text-secondary) ml-2">&ldquo;{o.reason}&rdquo;</span>}
                </div>
              ))}
            </section>
          )}

          {/* Attestation */}
          <section className="border-t-2 border-(--color-text) pt-4 print:break-before-page">
            <h3 className="text-sm font-bold text-(--color-text) uppercase tracking-wider mb-2">
              Parent Attestation
            </h3>
            {!attested ? (
              <div className="print:hidden">
                <p className="text-xs text-(--color-text-secondary) mb-3">
                  By signing below, I attest that this report accurately reflects the governance
                  decisions made during this period, and that I was in control of my children&apos;s
                  educational program at all times.
                </p>
                <textarea
                  value={attestText}
                  onChange={(e) => setAttestText(e.target.value)}
                  placeholder="I, [your name], confirm that this report is accurate and complete..."
                  className="w-full h-24 px-3 py-2 text-sm border border-(--color-border) rounded-[6px] resize-none mb-3 bg-(--color-surface) text-(--color-text)"
                />
                <Button variant="primary" size="md" onClick={attest} disabled={attestText.length < 10}
                  className="bg-(--color-text) hover:opacity-90">
                  Attest &amp; Sign
                </Button>
              </div>
            ) : (
              <Card className="bg-(--color-success-light) border-(--color-success)/30">
                <p className="text-sm text-(--color-success) font-medium mb-1">Report attested.</p>
                <p className="text-xs text-(--color-success)">&ldquo;{attestText}&rdquo;</p>
                <p className="text-xs text-(--color-success) mt-2">This attestation has been permanently recorded in the governance trail.</p>
              </Card>
            )}
          </section>
        </div>
      )}
    </div>
  );
}
