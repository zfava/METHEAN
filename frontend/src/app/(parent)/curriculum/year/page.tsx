"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import { useSearchParams } from "next/navigation";
import { annualCurriculum } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import StatusBadge from "@/components/StatusBadge";
import { cn } from "@/lib/cn";

const statusColors: Record<string, string> = {
  completed: "bg-(--color-success) text-white",
  current: "bg-(--color-accent) text-white",
  upcoming: "bg-(--color-border) text-(--color-text-secondary)",
  skipped: "bg-(--color-warning) text-white",
};

const typeLabel: Record<string, string> = {
  lesson: "Lesson", practice: "Practice", assessment: "Assessment",
  review: "Review", project: "Project", field_trip: "Field Trip",
};

export default function YearViewPage() {
  useEffect(() => { document.title = "Year Plan | METHEAN"; }, []);

  const params = useSearchParams();
  const curriculumId = params.get("id") || "";
  const { selectedChild } = useChild();

  const [curriculum, setCurriculum] = useState<any>(null);
  const [allCurricula, setAllCurricula] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [expandedWeek, setExpandedWeek] = useState<number | null>(null);
  const [weekDetail, setWeekDetail] = useState<any>(null);
  const [weekNotes, setWeekNotes] = useState("");
  const [savingNotes, setSavingNotes] = useState(false);
  const [notesSaved, setNotesSaved] = useState(false);
  const notesTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const debouncedSaveNotes = useCallback((notes: string, weekNum: number) => {
    if (notesTimerRef.current) clearTimeout(notesTimerRef.current);
    setNotesSaved(false);
    notesTimerRef.current = setTimeout(async () => {
      setSavingNotes(true);
      await annualCurriculum.updateWeekNotes(curriculumId, weekNum, notes);
      setSavingNotes(false);
      setNotesSaved(true);
      setTimeout(() => setNotesSaved(false), 2000);
    }, 2000);
  }, [curriculumId]);

  useEffect(() => {
    if (curriculumId) {
      annualCurriculum.detail(curriculumId)
        .then(setCurriculum)
        .catch((err: any) => setError(err.detail || "Failed to load curriculum"))
        .finally(() => setLoading(false));
    } else if (selectedChild) {
      annualCurriculum.list(selectedChild.id)
        .then(setAllCurricula)
        .catch((err: any) => setError(err.detail || "Failed to load curricula"))
        .finally(() => setLoading(false));
    }
  }, [curriculumId, selectedChild]);

  async function toggleWeek(weekNumber: number) {
    if (expandedWeek === weekNumber) {
      setExpandedWeek(null);
      setWeekDetail(null);
      return;
    }
    setExpandedWeek(weekNumber);
    const detail = await annualCurriculum.weekDetail(curriculumId, weekNumber);
    setWeekDetail(detail);
    setWeekNotes(detail?.actual?.parent_notes || "");
  }

  async function saveNotes() {
    if (!expandedWeek) return;
    setSavingNotes(true);
    await annualCurriculum.updateWeekNotes(curriculumId, expandedWeek, weekNotes);
    setSavingNotes(false);
  }

  async function completeWeek(weekNumber: number) {
    await annualCurriculum.completeWeek(curriculumId, weekNumber, weekNotes || undefined);
    // Refresh
    const detail = await annualCurriculum.weekDetail(curriculumId, weekNumber);
    setWeekDetail(detail);
    annualCurriculum.detail(curriculumId).then(setCurriculum);
  }

  async function removeActivity(activityId: string) {
    if (!expandedWeek) return;
    await annualCurriculum.removeActivity(curriculumId, expandedWeek, activityId);
    const detail = await annualCurriculum.weekDetail(curriculumId, expandedWeek);
    setWeekDetail(detail);
  }

  if (loading) return <div className="max-w-4xl"><LoadingSkeleton variant="list" count={8} /></div>;

  // No ID: show curriculum picker
  if (!curriculumId) {
    return (
      <div className="max-w-4xl">
        <PageHeader title="Year Plan" subtitle="Select a curriculum to view." />
        {error && (
          <Card className="border-l-4 border-(--color-danger) mb-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
          </Card>
        )}
        {allCurricula.length === 0 && !error ? (
          <Card className="text-center py-12">
            <p className="text-sm text-(--color-text-secondary)">No year plans for {selectedChild?.first_name || "this child"} yet.</p>
            <p className="text-xs text-(--color-text-tertiary) mt-1">Build a curriculum first from the Curriculum page, then it will appear here as a year-long plan.</p>
          </Card>
        ) : (
          <div className="space-y-3">
            {allCurricula.map((c: any) => (
              <Card key={c.id} href={`/curriculum/year?id=${c.id}`}>
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-sm font-medium text-(--color-text)">{c.subject_name}</span>
                    <span className="text-xs text-(--color-text-tertiary) ml-2">{c.academic_year}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <StatusBadge status={c.status} />
                    <span className="text-xs text-(--color-text-tertiary)">{c.total_weeks} weeks</span>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    );
  }

  if (!curriculum) return <div className="text-sm text-(--color-text-secondary)">Curriculum not found.</div>;

  const weeks = curriculum.scope_sequence?.weeks || [];
  const actualWeeks = curriculum.actual_record?.weeks || {};
  const today = new Date();

  // Compute completed weeks count
  const completedCount = Object.keys(actualWeeks).length;
  const totalHoursPlanned = (curriculum.hours_per_week || 0) * (curriculum.total_weeks || 36);

  function weekStatus(wn: number): string {
    if (actualWeeks[String(wn)]) return "completed";
    const weekStart = new Date(curriculum.start_date);
    weekStart.setDate(weekStart.getDate() + (wn - 1) * 7);
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekEnd.getDate() + 5);
    if (today >= weekStart && today <= weekEnd) return "current";
    if (today > weekEnd) return "skipped";
    return "upcoming";
  }

  return (
    <div className="max-w-4xl">
      <PageHeader
        title={`${curriculum.subject_name} — ${curriculum.academic_year}`}
        subtitle={`${selectedChild?.first_name || "Child"} · ${curriculum.grade_level || ""} · ${curriculum.status}`}
        actions={
          <div className="flex items-center gap-3">
            <StatusBadge status={curriculum.status} />
            <span className="text-xs text-(--color-text-tertiary)">
              {completedCount} of {curriculum.total_weeks} weeks completed
            </span>
          </div>
        }
      />

      {/* Overview Card */}
      <Card className="mb-6">
        <p className="text-xs text-(--color-text-secondary) mb-2">{curriculum.scope_sequence?.overview || ""}</p>
        <div className="flex flex-wrap gap-3 sm:gap-6 text-xs text-(--color-text-tertiary)">
          <span>{curriculum.hours_per_week}h/week</span>
          <span>{curriculum.total_weeks} weeks</span>
          <span>{curriculum.start_date} → {curriculum.end_date}</span>
        </div>
      </Card>

      {/* Year Timeline */}
      <div className="space-y-2">
        {weeks.map((week: any) => {
          const wn = week.week_number;
          const status = weekStatus(wn);
          const isExpanded = expandedWeek === wn;
          const activityCount = (week.suggested_activities || []).length;
          const totalMins = (week.suggested_activities || []).reduce((s: number, a: any) => s + (a.minutes || 0), 0);
          const actualData = actualWeeks[String(wn)];

          return (
            <div key={wn}>
              <button
                onClick={() => toggleWeek(wn)}
                className={cn(
                  "w-full text-left rounded-[10px] border p-4 transition-all",
                  isExpanded ? "border-(--color-accent) ring-1 ring-(--color-accent)/20" : "border-(--color-border) hover:border-(--color-border-strong)",
                  "bg-(--color-surface)"
                )}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className={cn("w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold", statusColors[status] || statusColors.upcoming)}>
                      {wn}
                    </span>
                    <div>
                      <span className="text-sm font-medium text-(--color-text)">{week.title}</span>
                      <div className="text-xs text-(--color-text-tertiary)">
                        {activityCount} activities · {Math.round(totalMins / 60 * 10) / 10}h planned
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {actualData && (
                      <span className="text-xs text-(--color-success)">
                        {actualData.completed_activities}/{actualData.planned_activities} done
                      </span>
                    )}
                    <span className="text-xs text-(--color-text-tertiary)">{isExpanded ? "▲" : "▼"}</span>
                  </div>
                </div>
              </button>

              {/* Expanded Week Detail */}
              {isExpanded && weekDetail && (
                <Card className="mt-1 ml-10 border-l-2 border-(--color-accent)">
                  {/* Objectives */}
                  {weekDetail.planned?.objectives && (
                    <div className="mb-4">
                      <h4 className="text-xs font-bold text-(--color-text-secondary) uppercase tracking-wider mb-1">Objectives</h4>
                      <ul className="text-xs text-(--color-text-secondary) space-y-0.5">
                        {weekDetail.planned.objectives.map((obj: string, i: number) => (
                          <li key={i}>• {obj}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Activities */}
                  <h4 className="text-xs font-bold text-(--color-text-secondary) uppercase tracking-wider mb-2">Activities</h4>
                  <div className="space-y-1.5 mb-4">
                    {(weekDetail.activities || []).map((act: any) => (
                      <div key={act.id} className="flex items-center justify-between py-1.5 px-3 rounded-[6px] bg-(--color-page)">
                        <div className="flex items-center gap-2">
                          <StatusBadge status={act.status} />
                          <span className="text-xs text-(--color-text)">{act.title}</span>
                          <span className="text-[10px] text-(--color-text-tertiary)">{typeLabel[act.type] || act.type}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-[10px] text-(--color-text-tertiary)">{act.estimated_minutes}m</span>
                          {act.scheduled_date && <span className="text-[10px] text-(--color-text-tertiary)">{act.scheduled_date}</span>}
                          {status !== "completed" && (
                            <button onClick={(e) => { e.stopPropagation(); removeActivity(act.id); }}
                              className="text-[10px] text-(--color-danger) hover:opacity-80">×</button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Assessment Focus */}
                  {weekDetail.planned?.assessment_focus && (
                    <div className="mb-4 p-2.5 rounded-[6px] bg-(--color-warning-light) text-xs text-(--color-warning)">
                      <span className="font-medium">Assessment:</span> {weekDetail.planned.assessment_focus}
                    </div>
                  )}

                  {/* Actual Results */}
                  {weekDetail.actual && Object.keys(weekDetail.actual).length > 0 && (
                    <div className="mb-4 p-2.5 rounded-[6px] bg-(--color-success-light) text-xs text-(--color-success)">
                      <span className="font-medium">Completed:</span>{" "}
                      {weekDetail.actual.completed_activities}/{weekDetail.actual.planned_activities} activities ·{" "}
                      {weekDetail.actual.total_minutes}m total
                    </div>
                  )}

                  {/* Parent Notes */}
                  <div className="mb-3">
                    <h4 className="text-xs font-bold text-(--color-text-secondary) uppercase tracking-wider mb-1">Parent Notes</h4>
                    <textarea
                      value={weekNotes}
                      onChange={(e) => { setWeekNotes(e.target.value); debouncedSaveNotes(e.target.value, wn); }}
                      onBlur={() => { if (weekNotes && expandedWeek) saveNotes(); }}
                      placeholder={status === "completed" ? "What happened this week? Any observations?" : "Any special plans or adjustments?"}
                      className="w-full h-20 px-3 py-2 text-xs border border-(--color-border) rounded-[6px] resize-none bg-(--color-surface) text-(--color-text)"
                    />
                    <div className="flex items-center gap-2 mt-1.5">
                      {notesSaved && <span className="text-[10px] text-(--color-success)">Saved</span>}
                      {savingNotes && <span className="text-[10px] text-(--color-text-tertiary)">Saving...</span>}
                      <Button size="sm" variant="secondary" onClick={saveNotes} disabled={savingNotes}>
                        {savingNotes ? "Saving..." : "Save Notes"}
                      </Button>
                      {status !== "completed" && (
                        <Button size="sm" variant="primary" onClick={() => completeWeek(wn)}>
                          Mark Week Complete
                        </Button>
                      )}
                    </div>
                  </div>
                </Card>
              )}
            </div>
          );
        })}
      </div>

      {weeks.length === 0 && (
        <Card className="text-center py-12">
          <p className="text-sm text-(--color-text-secondary)">No weeks in this curriculum yet.</p>
          <p className="text-xs text-(--color-text-tertiary) mt-1">Generate a curriculum to see the year plan.</p>
        </Card>
      )}
    </div>
  );
}
