"use client";

import { useEffect, useState } from "react";
import { annualCurriculum } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import EmptyState from "@/components/ui/EmptyState";
import { cn } from "@/lib/cn";

export default function ScopePage() {
  useEffect(() => { document.title = "Scope & Sequence | METHEAN"; }, []);

  const { selectedChild } = useChild();
  const [curricula, setCurricula] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (selectedChild) loadData();
  }, [selectedChild]);

  async function loadData() {
    setLoading(true);
    setError("");
    try {
      setCurricula(await annualCurriculum.list(selectedChild!.id));
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't load scope data.");
    } finally {
      setLoading(false);
    }
  }

  if (!selectedChild) return <div className="text-sm text-(--color-text-secondary)">Select a child.</div>;
  if (loading) return <div className="max-w-6xl"><PageHeader title="Scope & Sequence" /><LoadingSkeleton variant="card" count={3} /></div>;

  // Compute current week number
  const now = new Date();

  function getWeekStatus(c: any, weekNum: number): "completed" | "current" | "upcoming" | "skipped" {
    const actual = c.actual_record?.weeks || {};
    if (actual[String(weekNum)]) return "completed";
    const weekStart = new Date(c.start_date);
    weekStart.setDate(weekStart.getDate() + (weekNum - 1) * 7);
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekEnd.getDate() + 7);
    if (now >= weekStart && now < weekEnd) return "current";
    if (now > weekEnd) return "skipped";
    return "upcoming";
  }

  const statusColors: Record<string, string> = {
    completed: "bg-(--color-success)",
    current: "bg-(--color-accent)",
    upcoming: "bg-(--color-border)",
    skipped: "bg-(--color-warning)",
  };

  return (
    <div className="max-w-6xl">
      <PageHeader title="Scope & Sequence" subtitle={`${selectedChild.first_name}'s year-long roadmap`} />

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <button onClick={() => { setError(""); loadData(); }} className="text-xs text-(--color-accent) hover:underline">Retry</button>
          </div>
        </Card>
      )}

      {curricula.length === 0 ? (
        <EmptyState icon="empty" title="No scope and sequence data" description="Build a curriculum first to see the year-long roadmap here." />
      ) : (
        <div className="space-y-4">
          {/* Legend */}
          <div className="flex items-center gap-4 text-[10px] text-(--color-text-tertiary)">
            <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-sm bg-(--color-success)" /> Completed</span>
            <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-sm bg-(--color-accent)" /> Current</span>
            <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-sm bg-(--color-border)" /> Upcoming</span>
            <span className="flex items-center gap-1"><span className="w-3 h-3 rounded-sm bg-(--color-warning)" /> Skipped</span>
            <span className="flex items-center gap-1">◆ Assessment</span>
          </div>

          {/* Timeline grid */}
          <Card padding="p-0" className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr>
                  <th className="sticky left-0 bg-(--color-surface) z-10 px-3 py-2 text-left text-xs font-medium text-(--color-text-secondary) border-b border-(--color-border) min-w-[120px]">Subject</th>
                  {Array.from({ length: 36 }, (_, i) => i + 1).map((w) => (
                    <th key={w} className={cn("px-0.5 py-2 text-center text-[9px] border-b border-(--color-border) min-w-[24px]",
                      w % 6 === 0 ? "text-(--color-constitutional) font-bold" : "text-(--color-text-tertiary) font-normal"
                    )}>{w}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {curricula.map((c: any) => (
                  <tr key={c.id} className="border-b border-(--color-border)/30">
                    <td className="sticky left-0 bg-(--color-surface) z-10 px-3 py-2">
                      <a href={`/curriculum/year?id=${c.id}`} className="text-xs font-medium text-(--color-text) hover:text-(--color-accent)">
                        {c.subject_name}
                      </a>
                      <div className="text-[9px] text-(--color-text-tertiary)">{c.academic_year}</div>
                    </td>
                    {Array.from({ length: c.total_weeks || 36 }, (_, i) => i + 1).map((w) => {
                      const status = getWeekStatus(c, w);
                      const isAssessment = w % 6 === 0;
                      return (
                        <td key={w} className="px-0.5 py-2 text-center">
                          <a href={`/curriculum/year?id=${c.id}`}
                            className={cn("inline-block w-4 h-4 rounded-sm transition-colors",
                              statusColors[status],
                              status === "current" && "ring-1 ring-(--color-accent) ring-offset-1"
                            )}
                            title={`Week ${w}: ${status}`}>
                            {isAssessment && <span className="text-[7px] text-white leading-none flex items-center justify-center h-full">◆</span>}
                          </a>
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>

          {/* Mobile: Subject cards with progress bars */}
          <div className="lg:hidden space-y-3 mt-4">
            {curricula.map((c: any) => {
              const totalWeeks = c.total_weeks || 36;
              const completedWeeks = Object.keys(c.actual_record?.weeks || {}).length;
              const pct = Math.round((completedWeeks / totalWeeks) * 100);
              return (
                <Card key={c.id} href={`/curriculum/year?id=${c.id}`} padding="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-(--color-text)">{c.subject_name}</span>
                    <span className="text-xs text-(--color-text-tertiary)">{completedWeeks}/{totalWeeks} weeks</span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-(--color-border) overflow-hidden">
                    <div className="h-full rounded-full bg-(--color-success) transition-all" style={{ width: `${pct}%` }} />
                  </div>
                </Card>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
