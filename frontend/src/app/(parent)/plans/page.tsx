"use client";

import { useEffect, useState } from "react";
import { plans, type Plan, type PlanDetail, type ActivityInPlan } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import LoadingSkeleton from "@/components/LoadingSkeleton";

export default function PlansPage() {
  const [planList, setPlanList] = useState<Plan[]>([]);
  const [selected, setSelected] = useState<PlanDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Plans are per-child; show all for now
    setLoading(false);
  }, []);

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
    await plans.lock(selected.id);
    await loadPlanDetail(selected.id);
  }

  async function handleUnlock() {
    if (!selected) return;
    await plans.unlock(selected.id);
    await loadPlanDetail(selected.id);
  }

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
      } else {
        byDay["Mon"].push(a);
      }
    });
    return byDay;
  }

  return (
    <div className="max-w-6xl">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-xl font-semibold">Plans</h1>
      </div>

      {!selected ? (
        <div className="bg-white rounded-lg border border-(--color-border) p-8 text-center">
          <p className="text-sm text-(--color-text-secondary)">
            Select a plan from the dashboard or generate one from a child&apos;s profile.
          </p>
          <p className="text-xs text-(--color-text-secondary) mt-2">
            Plans are generated per child via the governance-gated AI planner.
          </p>
        </div>
      ) : (
        <div>
          <div className="flex items-center justify-between mb-4 bg-white rounded-lg border border-(--color-border) px-5 py-4">
            <div>
              <h2 className="text-sm font-semibold">{selected.name}</h2>
              <div className="flex items-center gap-2 mt-1">
                <StatusBadge status={selected.status} />
                {selected.ai_generated && (
                  <span className="text-xs text-(--color-text-secondary)">AI generated</span>
                )}
              </div>
            </div>
            <div className="flex gap-2">
              {selected.status === "draft" && (
                <button onClick={handleLock} className="px-3 py-1.5 text-xs font-medium bg-(--color-accent) text-white rounded-md hover:bg-(--color-accent-hover)">
                  Lock Plan
                </button>
              )}
              {selected.status === "active" && (
                <button onClick={handleUnlock} className="px-3 py-1.5 text-xs font-medium border border-(--color-border) rounded-md hover:bg-gray-50">
                  Unlock
                </button>
              )}
            </div>
          </div>

          {/* Day columns */}
          <div className="grid grid-cols-5 gap-3">
            {days.map((day) => {
              const dayActivities = activitiesByDay(selected.activities)[day] || [];
              return (
                <div key={day} className="bg-white rounded-lg border border-(--color-border)">
                  <div className="px-3 py-2 border-b border-(--color-border) text-xs font-semibold text-(--color-text-secondary)">
                    {day}
                  </div>
                  <div className="p-2 space-y-2 min-h-32">
                    {dayActivities.map((a) => (
                      <div key={a.id} className="p-2.5 rounded-md border border-gray-100 bg-gray-50">
                        <div className="text-xs font-medium">{a.title}</div>
                        <div className="flex items-center gap-2 mt-1">
                          <StatusBadge status={a.status} />
                          {a.estimated_minutes && (
                            <span className="text-[10px] text-(--color-text-secondary)">{a.estimated_minutes}m</span>
                          )}
                        </div>
                        {a.status === "scheduled" && (
                          <div className="flex gap-1 mt-2">
                            <button
                              onClick={() => handleApprove(a.id)}
                              className="px-2 py-0.5 text-[10px] font-medium bg-emerald-50 text-emerald-700 rounded hover:bg-emerald-100"
                            >
                              Approve
                            </button>
                            <button
                              onClick={() => handleReject(a.id)}
                              className="px-2 py-0.5 text-[10px] font-medium bg-red-50 text-red-700 rounded hover:bg-red-100"
                            >
                              Reject
                            </button>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
