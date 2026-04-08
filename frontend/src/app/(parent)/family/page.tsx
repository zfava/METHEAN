"use client";

import { useEffect, useState } from "react";
import { children as childrenApi } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import StatusBadge from "@/components/StatusBadge";
import EmptyState from "@/components/ui/EmptyState";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import { cn } from "@/lib/cn";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface TodayActivity {
  id: string;
  title: string;
  activity_type: string;
  status: string;
  estimated_minutes: number | null;
}

interface ChildDayData {
  childId: string;
  activities: TodayActivity[];
  alerts: any[];
  loading: boolean;
}

const typeLabels: Record<string, { label: string; color: string }> = {
  lesson: { label: "Lesson", color: "bg-(--color-accent-light) text-(--color-accent)" },
  practice: { label: "Practice", color: "bg-(--color-success-light) text-(--color-success)" },
  review: { label: "Review", color: "bg-(--color-warning-light) text-(--color-warning)" },
  assessment: { label: "Assessment", color: "bg-(--color-constitutional-light) text-(--color-constitutional)" },
  project: { label: "Project", color: "bg-(--color-danger-light) text-(--color-danger)" },
  field_trip: { label: "Field Trip", color: "bg-(--color-accent-light) text-(--color-accent)" },
};

export default function FamilyPage() {
  useEffect(() => { document.title = "Family | METHEAN"; }, []);

  const { children, loading: childrenLoading } = useChild();
  const [childData, setChildData] = useState<Record<string, ChildDayData>>({});
  const [expanded, setExpanded] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [showAddChild, setShowAddChild] = useState(false);
  const [newName, setNewName] = useState("");
  const [newGrade, setNewGrade] = useState("");

  async function addChild() {
    if (!newName.trim()) return;
    await childrenApi.create({ first_name: newName, grade_level: newGrade || undefined });
    setNewName(""); setNewGrade(""); setShowAddChild(false);
    window.location.reload();
  }

  useEffect(() => {
    if (children.length > 0) loadAllChildren();
  }, [children]);

  async function loadAllChildren() {
    const data: Record<string, ChildDayData> = {};
    for (const child of children) {
      data[child.id] = { childId: child.id, activities: [], alerts: [], loading: true };
    }
    setChildData({ ...data });

    await Promise.all(children.map(async (child) => {
      try {
        const [todayResp, alertsResp] = await Promise.all([
          fetch(`${API}/children/${child.id}/today`, { credentials: "include" }),
          fetch(`${API}/children/${child.id}/alerts?limit=5`, { credentials: "include" }),
        ]);
        const activities = todayResp.ok ? await todayResp.json() : [];
        const alertsData = alertsResp.ok ? await alertsResp.json() : [];
        const alerts = Array.isArray(alertsData) ? alertsData : (alertsData.items || []);

        setChildData((prev) => ({
          ...prev,
          [child.id]: { childId: child.id, activities, alerts, loading: false },
        }));
      } catch (err: any) {
        setError(err?.detail || err?.message || "Couldn't load family data.");
        setChildData((prev) => ({
          ...prev,
          [child.id]: { childId: child.id, activities: [], alerts: [], loading: false },
        }));
      }
    }));
  }

  if (childrenLoading) return <div className="max-w-4xl"><PageHeader title="Family Overview" /><LoadingSkeleton variant="card" count={3} /></div>;

  const today = new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric", year: "numeric" });

  // Family-wide totals
  const allActivities = Object.values(childData).flatMap((d) => d.activities);
  const totalActivities = allActivities.length;
  const totalCompleted = allActivities.filter((a) => a.status === "completed").length;
  const totalMinutes = allActivities.reduce((s, a) => s + (a.estimated_minutes || 0), 0);

  return (
    <div className="max-w-4xl">
      <PageHeader title="Family Overview" subtitle={today} />

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button variant="ghost" size="sm" onClick={() => { setError(""); loadAllChildren(); }}>Retry</Button>
          </div>
        </Card>
      )}

      {/* Family summary */}
      {totalActivities > 0 && (
        <div className="flex items-center gap-6 mb-6 text-xs text-(--color-text-tertiary)">
          <span>{totalActivities} total activities</span>
          <span>{totalCompleted} completed</span>
          <span>{Math.round(totalMinutes / 60 * 10) / 10}h planned</span>
        </div>
      )}

      {/* Per-child rows */}
      <div className="space-y-3">
        {children.map((child) => {
          const data = childData[child.id];
          const isExpanded = expanded === child.id;

          if (!data || data.loading) {
            return (
              <Card key={child.id} padding="p-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-(--color-border) animate-pulse" />
                  <div className="h-4 w-32 bg-(--color-border) rounded animate-pulse" />
                </div>
              </Card>
            );
          }

          const completed = data.activities.filter((a) => a.status === "completed").length;
          const total = data.activities.length;
          const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
          const minutes = data.activities.reduce((s, a) => s + (a.estimated_minutes || 0), 0);
          const pendingAlerts = data.alerts.filter((a: any) => a.severity === "action_required" || a.severity === "warning");
          const allClear = total > 0 && completed === total;

          return (
            <div key={child.id}>
              <button
                onClick={() => setExpanded(isExpanded ? null : child.id)}
                className="w-full text-left"
              >
                <Card className={cn(
                  "transition-all",
                  isExpanded && "ring-1 ring-(--color-accent)/20 border-(--color-accent)"
                )}>
                  <div className="flex items-center gap-4">
                    {/* Avatar */}
                    <div className="w-10 h-10 rounded-full bg-(--color-accent) text-white flex items-center justify-center text-sm font-bold shrink-0">
                      {child.first_name.charAt(0)}
                    </div>

                    {/* Info */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-medium text-(--color-text)">{child.first_name}</span>
                        {child.grade_level && (
                          <span className="text-xs text-(--color-text-tertiary)">{child.grade_level}</span>
                        )}
                      </div>

                      {total > 0 ? (
                        <div className="flex items-center gap-3 mt-1">
                          <span className="text-xs text-(--color-text-secondary)">
                            {completed}/{total} activities
                          </span>
                          <span className="text-xs text-(--color-text-tertiary)">{minutes}m planned</span>
                          <div className="w-20 h-1.5 rounded-full bg-(--color-border) overflow-hidden">
                            <div
                              className="h-full rounded-full bg-(--color-success) transition-all duration-500"
                              style={{ width: `${pct}%` }}
                            />
                          </div>
                        </div>
                      ) : (
                        <span className="text-xs text-(--color-text-tertiary)">No activities today</span>
                      )}
                    </div>

                    {/* Status indicators */}
                    <div className="flex items-center gap-2 shrink-0">
                      {allClear && (
                        <span className="flex items-center gap-1 text-xs text-(--color-success) font-medium">
                          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                          </svg>
                          Done
                        </span>
                      )}
                      {pendingAlerts.length > 0 && (
                        <span className="text-xs text-(--color-warning) font-medium">
                          {pendingAlerts.length} alert{pendingAlerts.length !== 1 ? "s" : ""}
                        </span>
                      )}
                      <span className="text-xs text-(--color-text-tertiary)">{isExpanded ? "▲" : "▼"}</span>
                    </div>
                  </div>
                </Card>
              </button>

              {/* Expanded: today's activities */}
              {isExpanded && (
                <div className="ml-14 mt-2 space-y-1.5 mb-2">
                  {data.activities.length === 0 ? (
                    <div className="text-xs text-(--color-text-tertiary) py-4 text-center">
                      No activities scheduled for today.
                    </div>
                  ) : (
                    data.activities.map((act) => {
                      const t = typeLabels[act.activity_type] || { label: act.activity_type, color: "bg-(--color-page) text-(--color-text-secondary)" };
                      const done = act.status === "completed";
                      return (
                        <div key={act.id} className={cn(
                          "flex items-center justify-between px-3 py-2 rounded-[8px] bg-(--color-surface) border border-(--color-border)",
                          done && "opacity-50"
                        )}>
                          <div className="flex items-center gap-2">
                            {done ? (
                              <svg className="w-3.5 h-3.5 text-(--color-success)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                              </svg>
                            ) : (
                              <div className="w-3.5 h-3.5 rounded-full border-2 border-(--color-border-strong)" />
                            )}
                            <span className={cn("text-xs", done ? "text-(--color-text-tertiary) line-through" : "text-(--color-text)")}>{act.title}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className={`text-[9px] font-medium px-1.5 py-0.5 rounded-full ${t.color}`}>{t.label}</span>
                            {act.estimated_minutes && (
                              <span className="text-[9px] text-(--color-text-tertiary)">{act.estimated_minutes}m</span>
                            )}
                          </div>
                        </div>
                      );
                    })
                  )}

                  {/* Quick actions */}
                  <div className="flex gap-2 pt-1">
                    <a href={`/plans?child=${child.id}`} className="text-[10px] text-(--color-accent) hover:underline">View plan</a>
                    {pendingAlerts.length > 0 && (
                      <a href="/governance/queue" className="text-[10px] text-(--color-warning) hover:underline">Review alerts</a>
                    )}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Add child */}
      {showAddChild ? (
        <Card className="mt-3">
          <div className="flex flex-col sm:flex-row gap-3">
            <input value={newName} onChange={(e) => setNewName(e.target.value)} placeholder="Child's first name"
              className="flex-1 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)" />
            <input value={newGrade} onChange={(e) => setNewGrade(e.target.value)} placeholder="Grade (K, 1st, etc.)"
              className="w-32 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)" />
            <Button variant="primary" size="sm" onClick={addChild} disabled={!newName.trim()}>Add</Button>
            <Button variant="ghost" size="sm" onClick={() => setShowAddChild(false)}>Cancel</Button>
          </div>
        </Card>
      ) : (
        <button onClick={() => setShowAddChild(true)}
          className="mt-3 w-full py-3 border-2 border-dashed border-(--color-border) rounded-[14px] text-sm text-(--color-text-tertiary) hover:text-(--color-text-secondary) hover:border-(--color-border-strong) transition-colors">
          + Add Child
        </button>
      )}

      {children.length === 0 && !showAddChild && (
        <div className="mt-3">
          <EmptyState icon="empty" title="Your family is ready" description="Add your first child above to begin building their educational journey." />
        </div>
      )}
    </div>
  );
}
