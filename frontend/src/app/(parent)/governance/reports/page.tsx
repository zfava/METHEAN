"use client";

import { useState } from "react";
import LoadingSkeleton from "@/components/LoadingSkeleton";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

function getCsrf(): string | undefined {
  if (typeof document === "undefined") return undefined;
  const m = document.cookie.match(/(?:^|; )csrf_token=([^;]*)/);
  return m ? decodeURIComponent(m[1]) : undefined;
}

export default function ReportsPage() {
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
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold text-slate-800">Governance Report</h1>
          <p className="text-sm text-slate-500">Board meeting minutes for your homeschool.</p>
        </div>
        <button onClick={() => window.print()} className="text-xs text-slate-400 hover:text-slate-600 print:hidden">
          Print
        </button>
      </div>

      {/* Date range */}
      <div className="flex items-end gap-3 mb-6 print:hidden">
        <div>
          <label className="block text-xs text-slate-500 mb-1">From</label>
          <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)}
            className="px-3 py-1.5 text-sm border border-slate-300 rounded-md" />
        </div>
        <div>
          <label className="block text-xs text-slate-500 mb-1">To</label>
          <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)}
            className="px-3 py-1.5 text-sm border border-slate-300 rounded-md" />
        </div>
        <button onClick={generate} disabled={loading}
          className="px-4 py-1.5 text-sm font-medium bg-slate-800 text-white rounded-md hover:bg-slate-900 disabled:opacity-50">
          {loading ? "Generating..." : "Generate Report"}
        </button>
      </div>

      {loading && <LoadingSkeleton variant="text" count={5} />}

      {report && (
        <div className="space-y-6 print:space-y-4">
          {/* Header */}
          <div className="border-b-2 border-slate-800 pb-4">
            <h2 className="text-lg font-bold text-slate-800 uppercase tracking-wide">
              Governance Report
            </h2>
            <p className="text-sm text-slate-600">{report.household?.name}</p>
            <p className="text-xs text-slate-500">
              Period: {report.period?.start} to {report.period?.end} ({report.period?.days} days)
            </p>
            <p className="text-xs text-slate-400">Generated: {new Date(report.generated_at).toLocaleString()}</p>
          </div>

          {/* Executive Summary */}
          <section>
            <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider mb-2 border-b border-slate-200 pb-1">
              1. Executive Summary
            </h3>
            <div className="grid grid-cols-4 gap-3">
              {[
                { label: "Activities Approved", value: s?.activities_approved },
                { label: "Activities Rejected", value: s?.activities_rejected },
                { label: "Parent Overrides", value: s?.overrides_count },
                { label: "AI Acceptance Rate", value: s?.ai_acceptance_rate_pct != null ? `${s.ai_acceptance_rate_pct}%` : "N/A" },
              ].map((m) => (
                <div key={m.label} className="bg-slate-50 rounded p-3">
                  <div className="text-lg font-semibold text-slate-800">{m.value ?? 0}</div>
                  <div className="text-[10px] text-slate-500">{m.label}</div>
                </div>
              ))}
            </div>
          </section>

          {/* AI Oversight */}
          <section>
            <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider mb-2 border-b border-slate-200 pb-1">
              2. AI Oversight
            </h3>
            <p className="text-xs text-slate-600 mb-2">
              {report.ai_oversight?.total_ai_runs || 0} AI calls made. Acceptance rate: {report.ai_oversight?.acceptance_rate_pct ?? "N/A"}%.
            </p>
            {report.ai_oversight?.runs_by_role && (
              <div className="flex gap-3 text-xs text-slate-500">
                {Object.entries(report.ai_oversight.runs_by_role).map(([role, count]) => (
                  <span key={role} className="capitalize">{role}: {count as number}</span>
                ))}
              </div>
            )}
          </section>

          {/* Governance Decisions */}
          <section>
            <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider mb-2 border-b border-slate-200 pb-1">
              3. Governance Decisions ({report.governance_decisions?.length || 0})
            </h3>
            <div className="text-xs space-y-1 max-h-60 overflow-y-auto print:max-h-none">
              {(report.governance_decisions || []).slice(0, 20).map((d: any, i: number) => (
                <div key={i} className="flex justify-between py-1 border-b border-slate-50">
                  <div className="flex items-center gap-2">
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${
                      d.action === "approve" ? "bg-green-100 text-green-800" :
                      d.action === "reject" ? "bg-red-100 text-red-800" : "bg-slate-100 text-slate-600"
                    }`}>{d.action}</span>
                    <span className="text-slate-600">{d.target_type}</span>
                    {d.reason && <span className="text-slate-400 truncate max-w-xs">{d.reason}</span>}
                  </div>
                  <span className="text-slate-400 shrink-0">{d.timestamp?.split("T")[0]}</span>
                </div>
              ))}
            </div>
          </section>

          {/* Learning Progress */}
          <section>
            <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider mb-2 border-b border-slate-200 pb-1">
              4. Learning Progress
            </h3>
            <div className="space-y-2">
              {(report.learning_progress || []).map((cp: any) => (
                <div key={cp.child_id} className="bg-slate-50 rounded p-3 flex items-center justify-between">
                  <div>
                    <span className="text-sm font-medium text-slate-800">{cp.child_name}</span>
                    <span className="text-xs text-slate-500 ml-2">{cp.grade_level || ""}</span>
                  </div>
                  <div className="flex gap-4 text-xs text-slate-600">
                    <span>{cp.nodes_mastered}/{cp.nodes_total} mastered</span>
                    <span>{cp.total_hours}h logged</span>
                    <span>{cp.total_attempts} attempts</span>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Overrides */}
          {(report.overrides?.length || 0) > 0 && (
            <section>
              <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider mb-2 border-b border-slate-200 pb-1">
                5. Parent Overrides
              </h3>
              {report.overrides.map((o: any, i: number) => (
                <div key={i} className="text-xs border-l-2 border-amber-400 pl-3 py-1 mb-1">
                  <span className="text-slate-400">{o.timestamp?.split("T")[0]}</span>
                  {o.reason && <span className="text-slate-600 ml-2">&ldquo;{o.reason}&rdquo;</span>}
                </div>
              ))}
            </section>
          )}

          {/* Attestation */}
          <section className="border-t-2 border-slate-800 pt-4 print:break-before-page">
            <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider mb-2">
              Parent Attestation
            </h3>
            {!attested ? (
              <div className="print:hidden">
                <p className="text-xs text-slate-500 mb-3">
                  By signing below, I attest that this report accurately reflects the governance
                  decisions made during this period, and that I was in control of my children&apos;s
                  educational program at all times.
                </p>
                <textarea
                  value={attestText}
                  onChange={(e) => setAttestText(e.target.value)}
                  placeholder="I, [your name], confirm that this report is accurate and complete..."
                  className="w-full h-24 px-3 py-2 text-sm border border-slate-300 rounded-md resize-none mb-3"
                />
                <button onClick={attest} disabled={attestText.length < 10}
                  className="px-6 py-2 text-sm font-medium bg-slate-800 text-white rounded-md hover:bg-slate-900 disabled:opacity-50">
                  Attest &amp; Sign
                </button>
              </div>
            ) : (
              <div className="bg-green-50 border border-green-200 rounded p-4">
                <p className="text-sm text-green-800 font-medium mb-1">Report attested.</p>
                <p className="text-xs text-green-700">&ldquo;{attestText}&rdquo;</p>
                <p className="text-xs text-green-600 mt-2">This attestation has been permanently recorded in the governance trail.</p>
              </div>
            )}
          </section>
        </div>
      )}
    </div>
  );
}
