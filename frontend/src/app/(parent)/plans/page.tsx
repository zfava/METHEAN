"use client";

import { useEffect, useState } from "react";
import { plans, type Plan, type PlanDetail, type ActivityInPlan } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import { useChild } from "@/lib/ChildContext";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import EmptyState from "@/components/ui/EmptyState";
import { cn } from "@/lib/cn";

export default function PlansPage() {
  useEffect(() => { document.title = "Plans | METHEAN"; }, []);

  const { selectedChild } = useChild();
  const [planList, setPlanList] = useState<Plan[]>([]);
  const [selected, setSelected] = useState<PlanDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (selectedChild) loadPlans();
  }, [selectedChild]);

  async function loadPlans() {
    if (!selectedChild) return;
    setLoading(true);
    try {
      const data = await plans.list(selectedChild.id);
      const items = (data as any).items || data;
      setPlanList(items);
      if (items.length > 0) {
        const detail = await plans.detail(items[0].id);
        setSelected(detail);
      }
    } catch {} finally {
      setLoading(false);
    }
  }

  async function generatePlan() {
    if (!selectedChild) return;
    setGenerating(true);
    setError("");
    try {
      const today = new Date().toISOString().split("T")[0];
      const p = await plans.generate(selectedChild.id, { week_start: today, daily_minutes: 120 });
      await loadPlans();
      const detail = await plans.detail(p.id);
      setSelected(detail);
    } catch (e: any) {
      setError(e.detail || "Failed to generate plan");
    } finally {
      setGenerating(false);
    }
  }

  async function loadPlanDetail(planId: string) {
    const detail = await plans.detail(planId);
    setSelected(detail);
  }

  async function handleApprove(activityId: string) {
    if (!selected) return;
    await plans.approveActivity(selected.id, activityId);
    await loadPlanDetail(selected.id);
  }

  async function handleReject(activityId: string) {
    if (!selected) return;
    const reason = prompt("Reason for rejection:");
    if (!reason) return;
    await plans.rejectActivity(selected.id, activityId, reason);
    await loadPlanDetail(selected.id);
  }

  async function handleLock() {
    if (!selected) return;
    try {
      await plans.lock(selected.id);
      await loadPlanDetail(selected.id);
    } catch (e: any) {
      const detail = e.detail;
      if (typeof detail === "object" && detail.unapproved_activity_ids) {
        setError(`Cannot activate: ${detail.unapproved_activity_ids.length} unapproved activities remain.`);
      } else {
        setError(typeof detail === "string" ? detail : "Failed to lock plan");
      }
    }
  }

  async function handleUnlock() {
    if (!selected) return;
    await plans.unlock(selected.id);
    await loadPlanDetail(selected.id);
  }

  if (!selectedChild) return <div className="text-sm text-(--color-text-secondary)">Select a child from the sidebar.</div>;

  const days = ["Mon", "Tue", "Wed", "Thu", "Fri"];
  function activitiesByDay(activities: ActivityInPlan[]) {
    const byDay: Record<string, ActivityInPlan[]> = {};
    days.forEach((d) => (byDay[d] = []));
    activities.forEach((a) => {
      if (a.scheduled_date) {
        const dow = new Date(a.scheduled_date + "T00:00:00").getDay();
        const dayName = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][dow] || "Mon";
        if (byDay[dayName]) byDay[dayName].push(a);
        else byDay["Mon"].push(a);
      } else byDay["Mon"].push(a);
    });
    return byDay;
  }

  return (
    <div className="max-w-6xl">
      <PageHeader
        title="Plans"
        subtitle={`${selectedChild.first_name}'s weekly plans`}
        actions={
          <Button onClick={generatePlan} disabled={generating}>
            {generating ? "Generating..." : "Generate New Plan"}
          </Button>
        }
      />

      {error && <div className="mb-4 p-3 text-sm bg-(--color-danger-light) text-(--color-danger) rounded-[6px] border border-(--color-danger)/30">{error}</div>}

      {loading ? <LoadingSkeleton variant="card" count={3} /> : (
        <>
          {/* Plan selector */}
          {planList.length > 1 && (
            <div className="flex gap-2 mb-4 overflow-x-auto">
              {planList.map((p) => (
                <button
                  key={p.id}
                  onClick={() => loadPlanDetail(p.id)}
                  className={cn(
                    "shrink-0 px-3 py-1.5 text-xs rounded-[6px] border transition-colors",
                    selected?.id === p.id
                      ? "border-(--color-accent) bg-(--color-accent-light) text-(--color-accent)"
                      : "border-(--color-border) hover:bg-(--color-page)"
                  )}
                >
                  {p.name}
                </button>
              ))}
            </div>
          )}

          {selected ? (
            <div>
              <Card padding="px-5 py-4" className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-sm font-semibold text-(--color-text)">{selected.name}</h2>
                  <div className="flex items-center gap-2 mt-1">
                    <StatusBadge status={selected.status} />
                    {selected.ai_generated && <span className="text-xs text-(--color-text-secondary)">AI generated</span>}
                  </div>
                </div>
                <div className="flex gap-2">
                  {selected.status === "draft" && (
                    <Button onClick={handleLock} size="sm">
                      Activate Plan
                    </Button>
                  )}
                  {selected.status === "active" && (
                    <Button onClick={handleUnlock} variant="secondary" size="sm">
                      Unlock
                    </Button>
                  )}
                </div>
              </Card>

              <div className="grid grid-cols-5 gap-3">
                {days.map((day) => {
                  const dayActivities = activitiesByDay(selected.activities)[day] || [];
                  return (
                    <Card key={day} padding="p-0">
                      <div className="px-3 py-2 border-b border-(--color-border) text-xs font-semibold text-(--color-text-secondary)">{day}</div>
                      <div className="p-2 space-y-2 min-h-32">
                        {dayActivities.map((a) => (
                          <div key={a.id} className="p-2.5 rounded-[6px] border border-(--color-border) bg-(--color-page)">
                            <div className="text-xs font-medium text-(--color-text)">{a.title}</div>
                            <div className="flex items-center gap-2 mt-1">
                              <StatusBadge status={a.status} />
                              {a.estimated_minutes && <span className="text-[10px] text-(--color-text-secondary)">{a.estimated_minutes}m</span>}
                            </div>
                            {a.status === "scheduled" && (
                              <div className="flex gap-1 mt-2">
                                <button onClick={() => handleApprove(a.id)} className="px-2 py-0.5 text-[10px] font-medium bg-(--color-success-light) text-(--color-success) rounded-[4px] hover:opacity-80">Approve</button>
                                <button onClick={() => handleReject(a.id)} className="px-2 py-0.5 text-[10px] font-medium bg-(--color-danger-light) text-(--color-danger) rounded-[4px] hover:opacity-80">Reject</button>
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    </Card>
                  );
                })}
              </div>
            </div>
          ) : (
            <EmptyState
              icon="empty"
              title="No plans yet"
              description='Click "Generate New Plan" to create one.'
            />
          )}
        </>
      )}
    </div>
  );
}
