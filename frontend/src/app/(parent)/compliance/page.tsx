"use client";

import { useEffect, useState } from "react";
import { compliance } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import SectionHeader from "@/components/ui/SectionHeader";

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
    met: "\u2705", not_met: "\u274C", at_risk: "\u26A0\uFE0F", on_track: "\u2B50", unknown: "\u2753",
  };

  if (!selectedChild) return <div className="text-sm text-(--color-text-secondary)">Select a child.</div>;

  return (
    <div className="max-w-4xl">
      <PageHeader title="State Compliance" subtitle="Track requirements automatically." />

      <div className="flex items-center gap-3 mb-6">
        <select value={selectedState} onChange={(e) => setSelectedState(e.target.value)}
          className="px-3 py-2 text-sm border border-(--color-border) rounded-[6px] bg-(--color-surface)">
          <option value="">Select your state...</option>
          {states.map((s) => (
            <option key={s.code} value={s.code}>{s.name} ({s.strictness})</option>
          ))}
        </select>
      </div>

      {loading && <LoadingSkeleton variant="list" count={5} />}

      {result && !loading && (
        <div className="space-y-6">
          <Card className="flex items-center gap-6">
            <div className="relative w-20 h-20 shrink-0">
              <svg className="w-20 h-20 -rotate-90" viewBox="0 0 80 80">
                <circle cx="40" cy="40" r="34" fill="none" stroke="var(--color-border)" strokeWidth="6" />
                <circle cx="40" cy="40" r="34" fill="none"
                  stroke={result.score >= 80 ? "var(--color-success)" : result.score >= 50 ? "var(--color-warning)" : "var(--color-danger)"}
                  strokeWidth="6" strokeDasharray={`${(result.score / 100) * 213.6} 213.6`} strokeLinecap="round" />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-lg font-medium text-(--color-text)">{result.score}%</span>
              </div>
            </div>
            <div>
              <h2 className="text-sm font-medium text-(--color-text)">{result.state} Compliance</h2>
              <p className="text-xs text-(--color-text-secondary) capitalize">Strictness: {result.strictness}</p>
              <p className="text-xs text-(--color-text-secondary)">Total hours logged: {result.total_hours}h</p>
            </div>
          </Card>

          <Card padding="p-0">
            <div className="px-5 py-3 border-b border-(--color-border)">
              <SectionHeader title="Requirements" />
            </div>
            <div className="divide-y divide-(--color-border)/30">
              {(result.checks || []).map((c: any, i: number) => (
                <div key={i} className="flex items-start gap-3 px-5 py-3">
                  <span className="text-base mt-0.5">{statusIcon[c.status] || "\u2753"}</span>
                  <div className="flex-1">
                    <div className="text-sm text-(--color-text)">{c.requirement}</div>
                    {c.evidence && <p className="text-xs text-(--color-text-secondary)">{c.evidence}</p>}
                    {c.action && <p className="text-xs text-(--color-warning) mt-0.5">{c.action}</p>}
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {result.hours_by_subject && Object.keys(result.hours_by_subject).length > 0 && (
            <Card>
              <SectionHeader title="Hours by Subject" />
              <div className="space-y-2">
                {Object.entries(result.hours_by_subject).map(([subj, hrs]) => (
                  <div key={subj} className="flex items-center justify-between">
                    <span className="text-sm text-(--color-text)">{subj}</span>
                    <span className="text-sm font-mono text-(--color-text-secondary)">{hrs as number}h</span>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {result.special_notes && (
            <div className="bg-(--color-warning-light) border border-(--color-warning)/20 rounded-[10px] p-4 text-xs text-(--color-warning)">
              <span className="font-medium">Note:</span> {result.special_notes}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
