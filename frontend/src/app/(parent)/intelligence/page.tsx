"use client";

import { useEffect, useState } from "react";
import { intelligence } from "@/lib/api";
import { useToast } from "@/components/Toast";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import SectionHeader from "@/components/ui/SectionHeader";
import EmptyState from "@/components/ui/EmptyState";
import { cn } from "@/lib/cn";
import { relativeTime } from "@/lib/format";

export default function IntelligencePage() {
  useEffect(() => { document.title = "Learner Profile | METHEAN"; }, []);

  const { selectedChild } = useChild();
  const { toast } = useToast();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [newObs, setNewObs] = useState("");
  const [adding, setAdding] = useState(false);

  useEffect(() => { if (selectedChild) load(); }, [selectedChild]);

  async function load() {
    if (!selectedChild) return;
    setLoading(true);
    setError("");
    try {
      const d = await intelligence.get(selectedChild.id);
      setData(d);
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't load learner profile.");
    } finally {
      setLoading(false);
    }
  }

  async function addObservation() {
    if (!selectedChild || !newObs.trim()) return;
    setAdding(true);
    try {
      await intelligence.addObservation(selectedChild.id, newObs.trim());
      toast("Observation added", "success");
      setNewObs("");
      await load();
    } catch (err: any) {
      toast(err?.detail || "Couldn't add observation", "error");
    } finally {
      setAdding(false);
    }
  }

  async function removeObservation(index: number) {
    if (!selectedChild) return;
    try {
      await intelligence.removeObservation(selectedChild.id, index);
      toast("Observation removed", "info");
      await load();
    } catch (err: any) {
      toast(err?.detail || "Couldn't remove observation", "error");
    }
  }

  async function removeChip(field: string, subject: string, type: "strengths" | "struggles", text: string) {
    if (!selectedChild) return;
    const patterns = data?.raw?.subject_patterns || {};
    const subjectData = patterns[subject];
    if (!subjectData) return;
    const updated = (subjectData[type] || []).filter((s: any) => s.text !== text);
    try {
      await intelligence.override(selectedChild.id, `subject_patterns.${subject}.${type}`, updated);
      toast("Updated", "success");
      await load();
    } catch (err: any) {
      toast(err?.detail || "Couldn't update", "error");
    }
  }

  if (!selectedChild) return <div className="text-sm text-(--color-text-secondary)">Select a child from the sidebar.</div>;
  if (loading) return <div className="max-w-4xl"><PageHeader title="Learner Profile" /><LoadingSkeleton variant="card" count={3} /></div>;

  const summary = data?.summary;
  const raw = data?.raw;
  const isEmpty = !summary || Object.keys(summary).length === 0;
  const childName = selectedChild.first_name;

  if (isEmpty) {
    return (
      <div className="max-w-4xl">
        <PageHeader title={`${childName}'s Learner Profile`} subtitle="What METHEAN has learned, and what you know." />
        <EmptyState
          icon="search"
          title={`METHEAN is still learning about ${childName}`}
          description="Observations will appear here after their first few activities. You can add your own observations now."
        />
        {/* Still show parent observations even with empty AI data */}
        <div className="mt-6">
          <ParentObservations
            observations={raw?.parent_observations || []}
            newObs={newObs}
            setNewObs={setNewObs}
            adding={adding}
            onAdd={addObservation}
            onRemove={removeObservation}
            childName={childName}
          />
        </div>
      </div>
    );
  }

  const subjectPatterns = summary.subject_patterns || {};
  const engagement = summary.engagement || {};
  const pace = summary.pace || {};
  const govPrefs = summary.governance_preferences || {};
  const styleObs = summary.learning_style_observations || [];

  return (
    <div className="max-w-4xl">
      <PageHeader
        title={`${childName}'s Learner Profile`}
        subtitle="What METHEAN has learned, and what you know."
      />

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button variant="ghost" size="sm" onClick={() => { setError(""); load(); }}>Retry</Button>
          </div>
        </Card>
      )}

      {/* ── 1. Parent Observations (TOP — parent's word is law) ── */}
      <ParentObservations
        observations={raw?.parent_observations || []}
        newObs={newObs}
        setNewObs={setNewObs}
        adding={adding}
        onAdd={addObservation}
        onRemove={removeObservation}
        childName={childName}
      />

      {/* ── 2. Learning Style Observations ── */}
      {styleObs.length > 0 && (
        <Card className="mb-5" animate>
          <SectionHeader title="Learning Style Observations" />
          <div className="space-y-2 mt-3">
            {styleObs.map((obs: string, i: number) => (
              <div key={i} className="flex items-start gap-3 px-3 py-2 rounded-[10px] bg-(--color-page)">
                <span className="text-(--color-accent) mt-0.5 shrink-0">
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </span>
                <span className="text-sm text-(--color-text)">{obs}</span>
              </div>
            ))}
          </div>
        </Card>
      )}

      {/* ── 3. Subject Patterns ── */}
      {Object.keys(subjectPatterns).length > 0 && (
        <Card className="mb-5" animate>
          <SectionHeader title="Subject Patterns" />
          <div className="space-y-4 mt-3">
            {Object.entries(subjectPatterns).map(([subject, data]: [string, any]) => {
              const paceRate = pace.subject_rates?.[subject];
              return (
                <div key={subject} className="bg-(--color-page) rounded-[10px] p-4">
                  <div className="flex items-center justify-between mb-2.5">
                    <h4 className="text-sm font-semibold text-(--color-text) capitalize">{subject}</h4>
                    {paceRate != null && (
                      <span className={cn(
                        "text-[11px] font-medium px-2 py-0.5 rounded-full",
                        paceRate >= 0.7 ? "bg-(--color-success-light) text-(--color-success)" : "bg-(--color-warning-light) text-(--color-warning)"
                      )}>
                        {paceRate >= 0.9 ? "Ahead of plan" : paceRate >= 0.7 ? "On track" : "Needs attention"}
                      </span>
                    )}
                  </div>
                  {/* Strengths */}
                  {data.strengths?.length > 0 && (
                    <div className="mb-2">
                      <span className="text-[10px] font-medium text-(--color-text-tertiary) uppercase tracking-wide">Strengths</span>
                      <div className="flex flex-wrap gap-1.5 mt-1">
                        {data.strengths.map((s: string, i: number) => (
                          <span key={i} className="inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full bg-(--color-success-light) text-(--color-success)">
                            {s}
                            <button onClick={() => removeChip("subject_patterns", subject, "strengths", s)}
                              className="opacity-40 hover:opacity-80 transition-opacity" title="Remove">
                              <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                              </svg>
                            </button>
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  {/* Struggles */}
                  {data.struggles?.length > 0 && (
                    <div>
                      <span className="text-[10px] font-medium text-(--color-text-tertiary) uppercase tracking-wide">Areas for Growth</span>
                      <div className="flex flex-wrap gap-1.5 mt-1">
                        {data.struggles.map((s: string, i: number) => (
                          <span key={i} className="inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full bg-(--color-warning-light) text-(--color-warning)">
                            {s}
                            <button onClick={() => removeChip("subject_patterns", subject, "struggles", s)}
                              className="opacity-40 hover:opacity-80 transition-opacity" title="Remove">
                              <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                              </svg>
                            </button>
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </Card>
      )}

      {/* ── 4. Engagement Patterns ── */}
      {(engagement.avg_focus_minutes || engagement.best_time_of_day) && (
        <Card className="mb-5" animate>
          <SectionHeader title="Engagement Patterns" />
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-3">
            {engagement.avg_focus_minutes && (
              <div className="bg-(--color-page) rounded-[10px] p-3 text-center">
                <div className="text-2xl font-semibold text-(--color-text)">{Math.round(engagement.avg_focus_minutes)}</div>
                <div className="text-[10px] text-(--color-text-tertiary) mt-0.5">avg minutes before attention drops</div>
              </div>
            )}
            {engagement.best_time_of_day && (
              <div className="bg-(--color-page) rounded-[10px] p-3 text-center">
                <div className="text-2xl font-semibold text-(--color-text) capitalize">{engagement.best_time_of_day}</div>
                <div className="text-[10px] text-(--color-text-tertiary) mt-0.5">best learning time</div>
              </div>
            )}
            {summary.observation_count > 0 && (
              <div className="bg-(--color-page) rounded-[10px] p-3 text-center">
                <div className="text-2xl font-semibold text-(--color-text)">{summary.observation_count}</div>
                <div className="text-[10px] text-(--color-text-tertiary) mt-0.5">total observations</div>
              </div>
            )}
          </div>

          {/* Activity type preferences bar chart */}
          {engagement.preferred_activity_types && Object.keys(engagement.preferred_activity_types).length > 0 && (
            <div className="mt-4">
              <div className="text-[10px] font-medium text-(--color-text-tertiary) uppercase tracking-wide mb-2">Activity Completion Rates</div>
              <div className="space-y-1.5">
                {Object.entries(engagement.preferred_activity_types)
                  .sort(([, a]: any, [, b]: any) => b - a)
                  .map(([type, rate]: [string, any]) => (
                    <div key={type} className="flex items-center gap-2">
                      <span className="text-xs text-(--color-text-secondary) w-20 capitalize truncate">{type.replace(/_/g, " ")}</span>
                      <div className="flex-1 h-2 rounded-full bg-(--color-border)">
                        <div
                          className="h-full rounded-full bg-(--color-accent) transition-all"
                          style={{ width: `${Math.round(rate * 100)}%` }}
                        />
                      </div>
                      <span className="text-[10px] text-(--color-text-tertiary) w-8 text-right">{Math.round(rate * 100)}%</span>
                    </div>
                  ))}
              </div>
            </div>
          )}
        </Card>
      )}

      {/* ── 5. Pace Trends ── */}
      {pace.overall_mastery_rate != null && (
        <Card className="mb-5" animate>
          <SectionHeader title="Pace Trends" />
          <div className="mt-3">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-sm text-(--color-text-secondary)">Overall mastery rate:</span>
              <span className={cn(
                "text-sm font-semibold",
                pace.overall_mastery_rate >= 0.7 ? "text-(--color-success)" : "text-(--color-warning)"
              )}>
                {Math.round(pace.overall_mastery_rate * 100)}% upward transitions
              </span>
            </div>

            {Object.keys(pace.subject_rates || {}).length > 0 && (
              <div className="space-y-2">
                {Object.entries(pace.subject_rates).map(([subject, rate]: [string, any]) => (
                  <div key={subject} className="flex items-center justify-between px-3 py-2 rounded-[10px] bg-(--color-page)">
                    <span className="text-xs font-medium text-(--color-text) capitalize">{subject}</span>
                    <div className="flex items-center gap-2">
                      <div className="w-24 h-1.5 rounded-full bg-(--color-border)">
                        <div
                          className={cn("h-full rounded-full transition-all", rate >= 0.7 ? "bg-(--color-success)" : "bg-(--color-warning)")}
                          style={{ width: `${Math.round((rate || 0) * 100)}%` }}
                        />
                      </div>
                      <span className={cn(
                        "text-[10px] font-medium",
                        rate >= 0.9 ? "text-(--color-success)" : rate >= 0.7 ? "text-(--color-accent)" : "text-(--color-warning)"
                      )}>
                        {rate >= 0.9 ? "Ahead" : rate >= 0.7 ? "On track" : "Behind"}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </Card>
      )}

      {/* ── 6. Governance Preferences (read-only) ── */}
      {(govPrefs.auto_approve_difficulty_ceiling || govPrefs.rejected_activity_types?.length > 0) && (
        <Card className="mb-5" animate>
          <SectionHeader title="Governance Preferences" />
          <div className="mt-3 space-y-3">
            {govPrefs.auto_approve_difficulty_ceiling && (
              <div className="bg-(--color-page) rounded-[10px] p-3">
                <p className="text-xs text-(--color-text-secondary)">
                  Based on your review history: activities at difficulty <strong className="text-(--color-text)">1-{govPrefs.auto_approve_difficulty_ceiling}</strong> are
                  auto-approved with high confidence. Difficulty <strong className="text-(--color-text)">{govPrefs.auto_approve_difficulty_ceiling + 1}+</strong> may need review.
                </p>
              </div>
            )}
            {govPrefs.rejected_activity_types?.length > 0 && (
              <div className="bg-(--color-page) rounded-[10px] p-3">
                <p className="text-xs text-(--color-text-secondary)">
                  Activity types you&apos;ve frequently modified or rejected:
                </p>
                <div className="flex flex-wrap gap-1.5 mt-1.5">
                  {govPrefs.rejected_activity_types.map((t: string) => (
                    <span key={t} className="px-2 py-0.5 text-xs rounded-full bg-(--color-danger-light) text-(--color-danger) capitalize">
                      {t.replace(/_/g, " ")}
                    </span>
                  ))}
                </div>
              </div>
            )}
            <p className="text-[10px] text-(--color-text-tertiary) italic px-1">
              These patterns inform planning but never bypass your governance rules.
            </p>
          </div>
        </Card>
      )}

      {/* ── Metadata ── */}
      <div className="text-xs text-(--color-text-tertiary) mt-2 mb-8">
        {summary.observation_count > 0 && <span>{summary.observation_count} total observations</span>}
        {summary.last_updated && <span className="ml-3">Last updated {relativeTime(summary.last_updated)}</span>}
      </div>
    </div>
  );
}

// ── Parent Observations Component ──
function ParentObservations({
  observations,
  newObs,
  setNewObs,
  adding,
  onAdd,
  onRemove,
  childName,
}: {
  observations: any[];
  newObs: string;
  setNewObs: (v: string) => void;
  adding: boolean;
  onAdd: () => void;
  onRemove: (i: number) => void;
  childName: string;
}) {
  return (
    <Card className="mb-5" borderLeft="border-l-(--gold)" padding="p-5 sm:p-6">
      <SectionHeader title="Your Observations" />
      <p className="text-xs text-(--color-text-secondary) mt-1 mb-4">
        Your observations always take priority over the AI's. Add anything you know about how {childName} learns best.
      </p>

      {/* Existing observations */}
      {observations.length > 0 && (
        <div className="space-y-2 mb-4">
          {observations.map((obs: any, i: number) => (
            <div key={i} className="flex items-start justify-between gap-3 px-3 py-2.5 rounded-[10px] bg-(--color-page) group">
              <div className="flex-1 min-w-0">
                <p className="text-sm text-(--color-text)">{obs.observation}</p>
                {obs.created_at && (
                  <p className="text-[10px] text-(--color-text-tertiary) mt-0.5">{relativeTime(obs.created_at)}</p>
                )}
              </div>
              <button
                onClick={() => onRemove(i)}
                className="shrink-0 opacity-0 group-hover:opacity-60 hover:!opacity-100 transition-opacity text-(--color-text-tertiary) mt-0.5"
                title="Remove observation"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Add new observation */}
      <div className="flex gap-2">
        <textarea
          value={newObs}
          onChange={(e) => setNewObs(e.target.value)}
          placeholder={`"${childName} learns best through stories, not worksheets..."`}
          rows={2}
          className="flex-1 px-3 py-2 text-sm border border-(--color-border-strong) rounded-[10px] bg-(--color-surface) resize-none focus:outline-none focus:ring-1 focus:ring-(--gold)"
        />
        <Button
          variant="gold"
          size="md"
          disabled={!newObs.trim() || adding}
          onClick={onAdd}
          className="self-end"
        >
          {adding ? "..." : "Add"}
        </Button>
      </div>
    </Card>
  );
}
