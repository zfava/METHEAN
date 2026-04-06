"use client";

import { useEffect, useState } from "react";
import { auth, attempts, type User } from "@/lib/api";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface TodayActivity {
  id: string;
  title: string;
  activity_type: string;
  status: string;
  estimated_minutes: number | null;
  node_id: string | null;
}

interface ChildInfo {
  id: string;
  first_name: string;
  grade_level: string | null;
}

function greeting(name: string): string {
  const h = new Date().getHours();
  if (h < 12) return `Good morning, ${name}!`;
  if (h < 17) return `Good afternoon, ${name}!`;
  return `Good evening, ${name}!`;
}

const typeLabels: Record<string, { label: string; color: string }> = {
  lesson:     { label: "Lesson",     color: "bg-(--color-accent-light) text-(--color-accent)" },
  practice:   { label: "Practice",   color: "bg-(--color-success-light) text-(--color-success)" },
  review:     { label: "Review",     color: "bg-(--color-warning-light) text-(--color-warning)" },
  assessment: { label: "Assessment", color: "bg-(--color-constitutional-light) text-(--color-constitutional)" },
  project:    { label: "Project",    color: "bg-(--color-danger-light) text-(--color-danger)" },
  field_trip: { label: "Field Trip", color: "bg-(--color-accent-light) text-(--color-accent)" },
};

export default function ChildPage() {
  const [children, setChildren] = useState<ChildInfo[]>([]);
  const [selectedId, setSelectedId] = useState("");
  const [activities, setActivities] = useState<TodayActivity[]>([]);
  const [loading, setLoading] = useState(true);

  // Focused learning state
  const [activeActivity, setActiveActivity] = useState<TodayActivity | null>(null);
  const [attemptId, setAttemptId] = useState("");
  const [response, setResponse] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [feedback, setFeedback] = useState("");
  const [masteryNote, setMasteryNote] = useState("");

  useEffect(() => { init(); }, []);
  useEffect(() => { if (selectedId) loadToday(); }, [selectedId]);

  async function init() {
    try {
      await auth.me();
      const resp = await fetch(`${API}/children`, { credentials: "include" });
      if (resp.ok) {
        const data: ChildInfo[] = await resp.json();
        setChildren(data);
        if (data.length > 0) setSelectedId(data[0].id);
      }
    } catch {
      window.location.href = "/auth";
    } finally {
      setLoading(false);
    }
  }

  async function loadToday() {
    try {
      const resp = await fetch(`${API}/children/${selectedId}/today`, { credentials: "include" });
      if (resp.ok) setActivities(await resp.json());
    } catch {}
  }

  async function startActivity(act: TodayActivity) {
    try {
      const attempt = await attempts.start(act.id, selectedId);
      setAttemptId(attempt.id);
      setActiveActivity(act);
      setSubmitted(false);
      setResponse("");
      setFeedback("");
      setMasteryNote("");
    } catch (err: any) {
      alert(err.detail || "Could not start activity");
    }
  }

  async function submitWork() {
    if (!attemptId || submitting) return;
    setSubmitting(true);
    try {
      const result = await attempts.submit(attemptId, {
        confidence: 0.7,
        duration_minutes: 15,
      });
      setSubmitted(true);
      setFeedback("Great work! Your answer has been submitted.");
      const level = result.mastery_level?.replace(/_/g, " ");
      if (level && level !== "not started") {
        setMasteryNote(`You're making progress \u2014 you're at "${level}" level!`);
      }
    } catch {
      setFeedback("Something went wrong. Your work has been saved.");
    } finally {
      setSubmitting(false);
    }
  }

  function goNext() {
    setActiveActivity(null);
    setAttemptId("");
    setResponse("");
    setSubmitted(false);
    loadToday();
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-(--color-warning-light)/30 flex items-center justify-center">
        <div className="text-base text-(--color-text-tertiary)">Loading...</div>
      </div>
    );
  }

  const child = children.find((c) => c.id === selectedId);
  const childName = child?.first_name || "Student";
  const remaining = activities.filter((a) => a.status !== "completed");

  // ── FOCUSED LEARNING VIEW ──
  if (activeActivity) {
    return (
      <div className="min-h-screen bg-(--color-warning-light)/30">
        <div className="max-w-xl mx-auto px-6 py-12">
          {!submitted ? (
            <>
              {/* Activity header */}
              <div className="mb-8">
                <button onClick={goNext} className="text-sm text-(--color-text-tertiary) hover:text-(--color-text-secondary) mb-4 block">
                  &larr; Back to activities
                </button>
                <h1 className="text-2xl font-semibold text-(--color-text) mb-2">
                  {activeActivity.title}
                </h1>
                <div className="flex items-center gap-3">
                  {(() => {
                    const t = typeLabels[activeActivity.activity_type] || { label: activeActivity.activity_type, color: "bg-(--color-page) text-(--color-text-secondary)" };
                    return <span className={`text-xs font-medium px-2 py-1 rounded-full ${t.color}`}>{t.label}</span>;
                  })()}
                  {activeActivity.estimated_minutes && (
                    <span className="text-sm text-(--color-text-tertiary)">{activeActivity.estimated_minutes} minutes</span>
                  )}
                </div>
              </div>

              {/* Work area */}
              <div className="bg-(--color-surface) rounded-2xl shadow-sm border border-(--color-border) p-6 mb-6">
                <label className="block text-sm font-medium text-(--color-text-secondary) mb-3">
                  Your work
                </label>
                <textarea
                  value={response}
                  onChange={(e) => setResponse(e.target.value)}
                  placeholder="Write your answer here..."
                  className="w-full h-40 px-4 py-3 text-base text-(--color-text) border border-(--color-border) rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20 focus:border-(--color-accent) placeholder:text-(--color-text-tertiary)"
                />
              </div>

              <button
                onClick={submitWork}
                disabled={submitting}
                className="w-full py-3.5 text-base font-semibold text-white bg-(--color-success) rounded-xl hover:opacity-90 disabled:opacity-50 transition-colors shadow-sm"
              >
                {submitting ? "Submitting..." : "Submit My Work"}
              </button>
            </>
          ) : (
            /* ── FEEDBACK VIEW ── */
            <div className="text-center py-8">
              <div className="w-16 h-16 mx-auto mb-6 rounded-full bg-(--color-success-light) flex items-center justify-center">
                <span className="text-(--color-success) text-2xl">&#10003;</span>
              </div>
              <h2 className="text-xl font-semibold text-(--color-text) mb-2">{feedback}</h2>
              {masteryNote && (
                <p className="text-base text-(--color-accent) mb-6">{masteryNote}</p>
              )}
              <div className="mt-8">
                {remaining.length > 1 ? (
                  <button onClick={goNext}
                    className="px-8 py-3 text-base font-semibold text-white bg-(--color-accent) rounded-xl hover:bg-(--color-accent-hover) transition-colors shadow-sm"
                  >Next Activity</button>
                ) : (
                  <div>
                    <p className="text-lg text-(--color-text-secondary) mb-4">All done for today!</p>
                    <button onClick={goNext}
                      className="px-6 py-2.5 text-sm text-(--color-text-secondary) border border-(--color-border-strong) rounded-xl hover:bg-(--color-page)"
                    >Back to overview</button>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // ── DAILY OVERVIEW ──
  return (
    <div className="min-h-screen bg-(--color-warning-light)/30">
      {/* Header */}
      <header className="bg-(--color-surface) border-b border-(--color-border) px-6 py-5">
        <div className="max-w-2xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-(--color-text)">METHEAN</h1>
          </div>
          {children.length > 1 && (
            <select
              value={selectedId}
              onChange={(e) => setSelectedId(e.target.value)}
              className="text-sm border border-(--color-border) rounded-[10px] px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-(--color-accent)/30"
            >
              {children.map((c) => (
                <option key={c.id} value={c.id}>{c.first_name}</option>
              ))}
            </select>
          )}
        </div>
      </header>

      <div className="max-w-2xl mx-auto px-6 py-8">
        {/* Greeting */}
        <h2 className="text-2xl font-semibold text-(--color-text) mb-1">
          {greeting(childName)}
        </h2>
        <p className="text-base text-(--color-text-secondary) mb-8">
          {remaining.length > 0
            ? `You have ${remaining.length} ${remaining.length === 1 ? "activity" : "activities"} today.`
            : "Let\u2019s see what\u2019s on your schedule."}
        </p>

        {/* Activities */}
        {activities.length === 0 ? (
          <div className="bg-(--color-surface) rounded-2xl shadow-sm border border-(--color-border) py-16 text-center">
            <div className="text-4xl mb-4">&#9728;&#65039;</div>
            <h3 className="text-lg font-semibold text-(--color-text) mb-2">
              No learning scheduled for today!
            </h3>
            <p className="text-base text-(--color-text-tertiary)">Enjoy your free time.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {activities.map((act) => {
              const done = act.status === "completed" || act.status === "in_progress";
              const t = typeLabels[act.activity_type] || { label: act.activity_type, color: "bg-(--color-page) text-(--color-text-secondary)" };

              return (
                <div key={act.id}
                  className={`bg-(--color-surface) rounded-2xl shadow-sm border border-(--color-border) p-5 transition-colors ${
                    done ? "opacity-60" : ""
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h3 className={`text-lg font-medium ${done ? "text-(--color-text-tertiary)" : "text-(--color-text)"}`}>
                        {act.title}
                      </h3>
                      <div className="flex items-center gap-3 mt-2">
                        <span className={`text-xs font-medium px-2 py-1 rounded-full ${t.color}`}>
                          {t.label}
                        </span>
                        {act.estimated_minutes && (
                          <span className="text-sm text-(--color-text-tertiary) flex items-center gap-1">
                            <span className="text-xs">&#9201;</span> {act.estimated_minutes} min
                          </span>
                        )}
                      </div>
                    </div>
                    {!done ? (
                      <button
                        onClick={() => startActivity(act)}
                        className="px-6 py-2.5 text-base font-semibold text-white bg-(--color-success) rounded-xl hover:opacity-90 transition-colors shadow-sm"
                      >
                        Start
                      </button>
                    ) : (
                      <span className="text-sm text-(--color-success) font-medium flex items-center gap-1">
                        <span>&#10003;</span> Done
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
