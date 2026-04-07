"use client";

import { useEffect, useState } from "react";
import { plans, type PlanDetail, type ActivityInPlan } from "@/lib/api";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import StatusBadge from "@/components/StatusBadge";
import EmptyState from "@/components/ui/EmptyState";
import { cn } from "@/lib/cn";

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];

const subjectColors: Record<string, string> = {
  mathematics: "border-l-(--color-accent)",
  math: "border-l-(--color-accent)",
  "language arts": "border-l-(--color-success)",
  reading: "border-l-(--color-success)",
  science: "border-l-(--color-warning)",
  "social studies": "border-l-(--color-constitutional)",
  history: "border-l-(--color-constitutional)",
  art: "border-l-(--color-danger)",
  music: "border-l-(--color-danger)",
  default: "border-l-(--color-border-strong)",
};

function getSubjectBorder(title: string): string {
  const lower = title.toLowerCase();
  for (const [key, cls] of Object.entries(subjectColors)) {
    if (key !== "default" && lower.includes(key)) return cls;
  }
  return subjectColors.default;
}

function getMonday(d: Date): Date {
  const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1);
  return new Date(d.getFullYear(), d.getMonth(), diff);
}

function formatDate(d: Date): string {
  return d.toISOString().split("T")[0];
}

function addDays(d: Date, n: number): Date {
  const r = new Date(d);
  r.setDate(r.getDate() + n);
  return r;
}

const typeLabels: Record<string, { label: string; color: string }> = {
  lesson: { label: "Lesson", color: "bg-(--color-accent-light) text-(--color-accent)" },
  practice: { label: "Practice", color: "bg-(--color-success-light) text-(--color-success)" },
  review: { label: "Review", color: "bg-(--color-warning-light) text-(--color-warning)" },
  assessment: { label: "Assessment", color: "bg-(--color-constitutional-light) text-(--color-constitutional)" },
  project: { label: "Project", color: "bg-(--color-danger-light) text-(--color-danger)" },
  field_trip: { label: "Field Trip", color: "bg-(--color-accent-light) text-(--color-accent)" },
};

export default function CalendarPage() {
  const { selectedChild } = useChild();
  const [weekStart, setWeekStart] = useState(() => getMonday(new Date()));
  const [planList, setPlanList] = useState<any[]>([]);
  const [activities, setActivities] = useState<ActivityInPlan[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (selectedChild) loadWeek();
  }, [selectedChild, weekStart]);

  async function loadWeek() {
    setLoading(true);
    setError("");
    try {
      const allPlans = await plans.list(selectedChild!.id);
      setPlanList(allPlans);

      // Find plan covering this week
      const ws = formatDate(weekStart);
      const we = formatDate(addDays(weekStart, 4));
      let weekActivities: ActivityInPlan[] = [];

      for (const p of allPlans) {
        if (p.start_date && p.end_date && p.start_date <= we && p.end_date >= ws) {
          const detail = await plans.detail(p.id);
          weekActivities = [
            ...weekActivities,
            ...(detail.activities || []).filter((a) => {
              if (!a.scheduled_date) return false;
              return a.scheduled_date >= ws && a.scheduled_date <= we;
            }),
          ];
        }
      }

      setActivities(weekActivities);
    } catch (err: any) {
      setError(err.detail || "Failed to load schedule");
    } finally {
      setLoading(false);
    }
  }

  function prevWeek() { setWeekStart(addDays(weekStart, -7)); }
  function nextWeek() { setWeekStart(addDays(weekStart, 7)); }
  function goToday() { setWeekStart(getMonday(new Date())); }

  function activitiesForDay(dayIndex: number): ActivityInPlan[] {
    const dayDate = formatDate(addDays(weekStart, dayIndex));
    return activities
      .filter((a) => a.scheduled_date === dayDate)
      .sort((a, b) => a.sort_order - b.sort_order);
  }

  const weekEnd = addDays(weekStart, 4);
  const weekLabel = `${weekStart.toLocaleDateString("en-US", { month: "short", day: "numeric" })} - ${weekEnd.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}`;

  if (!selectedChild) return <div className="text-sm text-(--color-text-secondary)">Select a child.</div>;

  return (
    <div className="max-w-6xl">
      <PageHeader
        title="Weekly Calendar"
        subtitle={selectedChild.first_name + "'s schedule"}
        actions={
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" onClick={prevWeek}>&larr;</Button>
            <button onClick={goToday} className="text-sm font-medium text-(--color-accent) hover:underline">Today</button>
            <Button variant="ghost" size="sm" onClick={nextWeek}>&rarr;</Button>
          </div>
        }
      />

      <div className="text-sm font-medium text-(--color-text) mb-4">{weekLabel}</div>

      {error && (
        <Card className="border-l-4 border-(--color-danger) mb-4">
          <p className="text-sm text-(--color-danger)">{error}</p>
          <Button variant="ghost" size="sm" onClick={loadWeek} className="mt-2">Try again</Button>
        </Card>
      )}

      {loading ? (
        <LoadingSkeleton variant="list" count={5} />
      ) : (
        <>
          {/* Desktop: 5-column grid */}
          <div className="hidden md:grid grid-cols-5 gap-3">
            {DAYS.map((day, dayIdx) => {
              const dayDate = addDays(weekStart, dayIdx);
              const isToday = formatDate(dayDate) === formatDate(new Date());
              const dayActivities = activitiesForDay(dayIdx);

              return (
                <div key={day} className="min-h-[300px]">
                  <div className={cn(
                    "text-xs font-bold uppercase tracking-wider mb-2 pb-1.5 border-b-2",
                    isToday ? "text-(--color-accent) border-(--color-accent)" : "text-(--color-text-secondary) border-(--color-border)"
                  )}>
                    {day}
                    <span className="ml-1 font-normal text-(--color-text-tertiary)">
                      {dayDate.getDate()}
                    </span>
                  </div>

                  <div className="space-y-2">
                    {dayActivities.map((act) => {
                      const t = typeLabels[act.activity_type] || { label: act.activity_type, color: "bg-(--color-page) text-(--color-text-secondary)" };
                      const isExpanded = expanded === act.id;
                      const done = act.status === "completed";

                      return (
                        <div key={act.id}>
                          <button
                            onClick={() => setExpanded(isExpanded ? null : act.id)}
                            className={cn(
                              "w-full text-left rounded-[8px] border border-(--color-border) p-2.5 border-l-[3px] transition-all",
                              getSubjectBorder(act.title),
                              done ? "opacity-50" : "hover:shadow-sm",
                              isExpanded && "ring-1 ring-(--color-accent)/20"
                            )}
                          >
                            <div className="flex items-start justify-between gap-1">
                              <span className={cn("text-xs font-medium leading-tight", done ? "text-(--color-text-tertiary) line-through" : "text-(--color-text)")}>
                                {act.title}
                              </span>
                              {done && (
                                <svg className="w-3.5 h-3.5 text-(--color-success) shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                                </svg>
                              )}
                            </div>
                            <div className="flex items-center gap-1.5 mt-1">
                              <span className={`text-[9px] font-medium px-1.5 py-0.5 rounded-full ${t.color}`}>{t.label}</span>
                              {act.estimated_minutes && (
                                <span className="text-[9px] text-(--color-text-tertiary)">{act.estimated_minutes}m</span>
                              )}
                            </div>
                          </button>

                          {isExpanded && (
                            <div className="mt-1 p-2.5 rounded-[6px] bg-(--color-page) text-[10px] text-(--color-text-secondary)">
                              {act.description && <p className="mb-1">{act.description}</p>}
                              <div className="flex items-center justify-between">
                                <StatusBadge status={act.status} />
                                {!done && (
                                  <select
                                    defaultValue=""
                                    onChange={async (e) => {
                                      if (!e.target.value) return;
                                      const targetIdx = parseInt(e.target.value);
                                      const targetDate = formatDate(addDays(weekStart, targetIdx));
                                      await plans.rescheduleActivity(act.id, targetDate);
                                      loadWeek();
                                    }}
                                    className="text-[9px] px-1.5 py-0.5 border border-(--color-border) rounded bg-(--color-surface)"
                                  >
                                    <option value="">Move to...</option>
                                    {DAYS.map((d, di) => di !== dayIdx && (
                                      <option key={d} value={di}>{d}</option>
                                    ))}
                                  </select>
                                )}
                              </div>
                            </div>
                          )}
                        </div>
                      );
                    })}

                    {/* Day total */}
                    {dayActivities.length > 0 && (
                      <div className="text-center text-[9px] text-(--color-text-tertiary) pt-2 border-t border-(--color-border)/30 mt-2">
                        {(() => {
                          const totalMin = dayActivities.reduce((s, a) => s + (a.estimated_minutes || 0), 0);
                          const h = Math.floor(totalMin / 60);
                          const m = totalMin % 60;
                          return h > 0 ? `${h}h ${m}m` : `${m}m`;
                        })()}
                      </div>
                    )}

                    {dayActivities.length === 0 && (
                      <div className="text-[10px] text-(--color-text-tertiary) text-center py-6">
                        No activities
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Mobile: single-day tabs */}
          <MobileCalendar
            weekStart={weekStart}
            activitiesForDay={activitiesForDay}
            expanded={expanded}
            setExpanded={setExpanded}
          />

          {activities.length === 0 && (
            <div className="mt-4">
              <EmptyState
                icon="empty"
                title="No activities scheduled this week"
                description="Generate a plan or add activities manually from the curriculum page."
                action={
                  <Button variant="primary" size="sm" onClick={() => {
                    plans.generate(selectedChild!.id, { week_start: formatDate(weekStart) }).then(loadWeek);
                  }}>Generate Plan</Button>
                }
              />
            </div>
          )}

          {/* Week summary */}
          {activities.length > 0 && (
            <div className="mt-4 flex items-center gap-6 text-xs text-(--color-text-tertiary)">
              <span>{activities.length} activities</span>
              <span>{activities.filter((a) => a.status === "completed").length} completed</span>
              <span>{activities.reduce((s, a) => s + (a.estimated_minutes || 0), 0)} min planned</span>
            </div>
          )}
        </>
      )}
    </div>
  );
}

function MobileCalendar({ weekStart, activitiesForDay, expanded, setExpanded }: {
  weekStart: Date;
  activitiesForDay: (dayIdx: number) => ActivityInPlan[];
  expanded: string | null;
  setExpanded: (id: string | null) => void;
}) {
  const [activeDay, setActiveDay] = useState(() => {
    const today = new Date().getDay();
    return today >= 1 && today <= 5 ? today - 1 : 0;
  });

  const dayActivities = activitiesForDay(activeDay);

  return (
    <div className="md:hidden">
      <div className="flex gap-1 mb-4">
        {DAYS.map((day, i) => (
          <button key={day} onClick={() => setActiveDay(i)}
            className={cn(
              "flex-1 py-2 text-xs font-medium rounded-[6px] transition-colors",
              activeDay === i ? "bg-(--color-text) text-white" : "bg-(--color-page) text-(--color-text-secondary)"
            )}>
            {day.slice(0, 3)}
          </button>
        ))}
      </div>

      <div className="space-y-2">
        {dayActivities.map((act) => {
          const t = typeLabels[act.activity_type] || { label: act.activity_type, color: "bg-(--color-page) text-(--color-text-secondary)" };
          const done = act.status === "completed";
          return (
            <Card key={act.id} className={cn("border-l-[3px]", getSubjectBorder(act.title), done && "opacity-50")}>
              <div className="flex items-center justify-between">
                <div>
                  <span className={cn("text-sm font-medium", done ? "text-(--color-text-tertiary) line-through" : "text-(--color-text)")}>{act.title}</span>
                  <div className="flex items-center gap-2 mt-1">
                    <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded-full ${t.color}`}>{t.label}</span>
                    {act.estimated_minutes && <span className="text-[10px] text-(--color-text-tertiary)">{act.estimated_minutes}m</span>}
                    <StatusBadge status={act.status} />
                  </div>
                </div>
                {done && (
                  <svg className="w-5 h-5 text-(--color-success)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                )}
              </div>
            </Card>
          );
        })}
        {dayActivities.length === 0 && (
          <div className="text-sm text-(--color-text-tertiary) text-center py-8">No activities for {DAYS[activeDay]}</div>
        )}
      </div>
    </div>
  );
}
