"use client";

import { useEffect, useState } from "react";
import { compliance } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";

export default function CompliancePage() {
  const { selectedChild } = useChild();
  const [states, setStates] = useState<{ code: string; name: string; strictness: string }[]>([]);
  const [selectedState, setSelectedState] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    compliance.states().then(setStates).catch(() => {});
  }, []);

  async function runCheck() {
    if (!selectedChild || !selectedState) return;
    setLoading(true);
    try {
      const r = await compliance.check(selectedChild.id, selectedState);
      setResult(r);
    } catch {} finally { setLoading(false); }
  }

  useEffect(() => { if (selectedState && selectedChild) runCheck(); }, [selectedState, selectedChild]);

  const statusIcon: Record<string, string> = {
    met: "\u2705", not_met: "\u274C", at_risk: "\u26A0\uFE0F", on_track: "\u2B50",
    unknown: "\u2753",
  };

  if (!selectedChild) return <div className="text-sm text-slate-500">Select a child.</div>;

  return (
    <div className="max-w-4xl">
      <div className="mb-6">
        <h1 className="text-xl font-semibold text-slate-800">Compliance</h1>
        <p className="text-sm text-slate-500">Track state homeschool requirements automatically.</p>
      </div>

      {/* State selector */}
      <div className="flex items-center gap-3 mb-6">
        <select value={selectedState} onChange={(e) => setSelectedState(e.target.value)}
          className="px-3 py-2 text-sm border border-slate-200 rounded-lg bg-white">
          <option value="">Select your state...</option>
          {states.map((s) => (
            <option key={s.code} value={s.code}>{s.name} ({s.strictness})</option>
          ))}
        </select>
      </div>

      {loading && <LoadingSkeleton variant="list" count={5} />}

      {result && !loading && (
        <div className="space-y-6">
          {/* Score */}
          <div className="bg-white rounded-lg border border-slate-200 p-6 flex items-center gap-6">
            <div className="relative w-20 h-20 shrink-0">
              <svg className="w-20 h-20 -rotate-90" viewBox="0 0 80 80">
                <circle cx="40" cy="40" r="34" fill="none" stroke="#e2e8f0" strokeWidth="6" />
                <circle cx="40" cy="40" r="34" fill="none"
                  stroke={result.score >= 80 ? "#22c55e" : result.score >= 50 ? "#eab308" : "#ef4444"}
                  strokeWidth="6" strokeDasharray={`${(result.score / 100) * 213.6} 213.6`} strokeLinecap="round" />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-lg font-bold text-slate-800">{result.score}%</span>
              </div>
            </div>
            <div>
              <h2 className="text-sm font-semibold text-slate-800">{result.state} Compliance</h2>
              <p className="text-xs text-slate-500 capitalize">Strictness: {result.strictness}</p>
              <p className="text-xs text-slate-500">Total hours logged: {result.total_hours}h</p>
            </div>
          </div>

          {/* Requirements checklist */}
          <div className="bg-white rounded-lg border border-slate-200">
            <div className="px-5 py-3 border-b border-slate-100">
              <h3 className="text-sm font-semibold text-slate-800">Requirements</h3>
            </div>
            <div className="divide-y divide-slate-50">
              {(result.checks || []).map((c: any, i: number) => (
                <div key={i} className="flex items-start gap-3 px-5 py-3">
                  <span className="text-base mt-0.5">{statusIcon[c.status] || "\u2753"}</span>
                  <div className="flex-1">
                    <div className="text-sm text-slate-800">{c.requirement}</div>
                    {c.evidence && <p className="text-xs text-slate-500">{c.evidence}</p>}
                    {c.action && <p className="text-xs text-amber-600 mt-0.5">{c.action}</p>}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Hours by subject */}
          {result.hours_by_subject && Object.keys(result.hours_by_subject).length > 0 && (
            <div className="bg-white rounded-lg border border-slate-200 p-5">
              <h3 className="text-sm font-semibold text-slate-800 mb-3">Hours by Subject</h3>
              <div className="space-y-2">
                {Object.entries(result.hours_by_subject).map(([subj, hrs]) => (
                  <div key={subj} className="flex items-center justify-between">
                    <span className="text-sm text-slate-700">{subj}</span>
                    <span className="text-sm font-mono text-slate-500">{hrs as number}h</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {result.special_notes && (
            <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 text-xs text-amber-800">
              <span className="font-semibold">Note:</span> {result.special_notes}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
