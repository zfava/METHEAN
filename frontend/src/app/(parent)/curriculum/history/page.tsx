"use client";

import { useEffect, useState } from "react";
import { annualCurriculum } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import StatusBadge from "@/components/StatusBadge";
import EmptyState from "@/components/ui/EmptyState";
import { cn } from "@/lib/cn";

export default function CurriculumHistoryPage() {
  useEffect(() => { document.title = "History | METHEAN"; }, []);

  const { selectedChild } = useChild();
  const [history, setHistory] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [expandedYear, setExpandedYear] = useState<string | null>(null);

  useEffect(() => {
    if (selectedChild) {
      annualCurriculum.history(selectedChild.id)
        .then(setHistory)
        .finally(() => setLoading(false));
    }
  }, [selectedChild]);

  if (!selectedChild) return <div className="text-sm text-(--color-text-secondary)">Select a child.</div>;
  if (loading) return <div className="max-w-4xl"><LoadingSkeleton variant="list" count={5} /></div>;

  const years = history?.years || {};
  const sortedYears = Object.keys(years).sort().reverse();

  return (
    <div className="max-w-4xl">
      <PageHeader
        title="Curriculum History"
        subtitle={`${selectedChild.first_name}'s complete educational record across all years and subjects.`}
      />

      {sortedYears.length === 0 ? (
        <EmptyState icon="empty" title="No curriculum history yet" description="As you complete academic years, your full educational record will build here. Start by creating a curriculum from the Curriculum page." />
      ) : (
        <div className="space-y-6">
          {sortedYears.map((year) => {
            const curricula = years[year] as any[];
            const isExpanded = expandedYear === year;
            const totalCompleted = curricula.reduce((s, c) => s + (c.completed_weeks || 0), 0);
            const totalWeeks = curricula.reduce((s, c) => s + (c.total_weeks || 0), 0);

            return (
              <div key={year}>
                <button
                  onClick={() => setExpandedYear(isExpanded ? null : year)}
                  className="w-full text-left"
                >
                  <Card className={cn("transition-all", isExpanded && "ring-1 ring-(--color-accent)/20 border-(--color-accent)")}>
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-sm font-bold text-(--color-text)">{year}</h3>
                        <p className="text-xs text-(--color-text-tertiary)">
                          {curricula.length} subject{curricula.length !== 1 ? "s" : ""} · {totalCompleted}/{totalWeeks} weeks completed
                        </p>
                      </div>
                      <span className="text-xs text-(--color-text-tertiary)">{isExpanded ? "▲" : "▼"}</span>
                    </div>
                  </Card>
                </button>

                {isExpanded && (
                  <div className="ml-4 mt-2 space-y-2">
                    {curricula.map((c: any) => {
                      const pct = c.total_weeks > 0 ? Math.round((c.completed_weeks / c.total_weeks) * 100) : 0;
                      return (
                        <Card key={c.id} href={`/curriculum/year?id=${c.id}`}>
                          <div className="flex items-center justify-between">
                            <div>
                              <span className="text-sm font-medium text-(--color-text)">{c.subject_name}</span>
                              {c.grade_level && <span className="text-xs text-(--color-text-tertiary) ml-2">{c.grade_level}</span>}
                            </div>
                            <div className="flex items-center gap-3">
                              <StatusBadge status={c.status} />
                              <div className="w-24 h-1.5 rounded-full bg-(--color-border) overflow-hidden">
                                <div
                                  className="h-full rounded-full bg-(--color-success) transition-all"
                                  style={{ width: `${pct}%` }}
                                />
                              </div>
                              <span className="text-xs text-(--color-text-tertiary) w-10 text-right">{pct}%</span>
                            </div>
                          </div>
                          <div className="flex gap-4 mt-1.5 text-[10px] text-(--color-text-tertiary)">
                            <span>{c.completed_weeks}/{c.total_weeks} weeks</span>
                            <span>{c.hours_per_week}h/week</span>
                          </div>
                        </Card>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
