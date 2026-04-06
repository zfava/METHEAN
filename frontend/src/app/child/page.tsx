"use client";

import { useEffect, useState, useRef } from "react";
import { auth, attempts, learn, type LearningContext } from "@/lib/api";
import { MetheanLogo } from "@/components/Brand";
import LessonView from "@/components/child/LessonView";
import PracticeView from "@/components/child/PracticeView";
import ReviewView from "@/components/child/ReviewView";
import AssessmentView from "@/components/child/AssessmentView";
import ProjectView from "@/components/child/ProjectView";
import FieldTripView from "@/components/child/FieldTripView";
import CompletionState from "@/components/child/CompletionState";

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

  // Learning state
  const [activeActivity, setActiveActivity] = useState<TodayActivity | null>(null);
  const [attemptId, setAttemptId] = useState("");
  const [learningContext, setLearningContext] = useState<LearningContext | null>(null);
  const [completed, setCompleted] = useState(false);
  const [completionData, setCompletionData] = useState<{ mastery?: string; prevMastery?: string }>({});
  const startTimeRef = useRef<number>(0);

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
      // Start attempt and track time
      const attempt = await attempts.start(act.id, selectedId);
      setAttemptId(attempt.id);
      startTimeRef.current = Date.now();

      // Fetch learning context
      const ctx = await learn.context(act.id, selectedId);
      setLearningContext(ctx);
      setActiveActivity(act);
      setCompleted(false);
      setCompletionData({});
    } catch (err: any) {
      alert(err.detail || "Could not start activity");
    }
  }

  async function handleActivityComplete(data: {
    confidence: number;
    responses: Array<{ prompt: string; response: string }>;
    self_reflection: string;
  }) {
    if (!attemptId) return;

    // Calculate actual duration
    const durationMinutes = Math.max(1, Math.round((Date.now() - startTimeRef.current) / 60000));

    try {
      const result = await attempts.submit(attemptId, {
        confidence: data.confidence,
        duration_minutes: durationMinutes,
        feedback: {
          responses: data.responses,
          self_reflection: data.self_reflection,
        },
      });

      setCompletionData({
        mastery: result.mastery_level?.replace(/_/g, " "),
        prevMastery: result.previous_mastery?.replace(/_/g, " "),
      });
      setCompleted(true);
    } catch {
      setCompleted(true);
      setCompletionData({});
    }
  }

  function goNext() {
    setActiveActivity(null);
    setAttemptId("");
    setLearningContext(null);
    setCompleted(false);
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
  const completedCount = activities.filter((a) => a.status === "completed").length;

  // ── COMPLETION STATE ──
  if (activeActivity && completed) {
    return (
      <div className="min-h-screen bg-(--color-warning-light)/30">
        <div className="max-w-xl mx-auto px-6 py-12">
          <CompletionState
            activityTitle={activeActivity.title}
            masteryLevel={completionData.mastery}
            previousMastery={completionData.prevMastery}
            onNext={goNext}
            allDone={remaining.length <= 1}
          />
        </div>
      </div>
    );
  }

  // ── FOCUSED LEARNING VIEW ──
  if (activeActivity && learningContext) {
    const actType = activeActivity.activity_type;

    return (
      <div className="min-h-screen bg-(--color-warning-light)/30">
        {/* Top bar */}
        <header className="bg-(--color-surface)/80 backdrop-blur border-b border-(--color-border)/50 px-6 py-3">
          <div className="max-w-2xl mx-auto flex items-center justify-between">
            <button onClick={goNext} className="text-sm text-(--color-text-tertiary) hover:text-(--color-text-secondary) transition-colors">
              &larr; Back to activities
            </button>
            <span className="text-sm font-medium text-(--color-text)">{childName}</span>
          </div>
        </header>

        <div className="max-w-2xl mx-auto px-6 py-8">
          {actType === "lesson" && (
            <LessonView context={learningContext} childId={selectedId} onComplete={handleActivityComplete} />
          )}
          {actType === "practice" && (
            <PracticeView context={learningContext} childId={selectedId} onComplete={handleActivityComplete} />
          )}
          {actType === "review" && (
            <ReviewView context={learningContext} childId={selectedId} onComplete={handleActivityComplete} />
          )}
          {actType === "assessment" && (
            <AssessmentView context={learningContext} onComplete={handleActivityComplete} />
          )}
          {actType === "project" && (
            <ProjectView context={learningContext} childId={selectedId} onComplete={handleActivityComplete} />
          )}
          {actType === "field_trip" && (
            <FieldTripView context={learningContext} onComplete={handleActivityComplete} />
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
          <MetheanLogo markSize={24} wordmarkHeight={12} color="#0F1B2D" gap={8} />
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
        <p className="text-base text-(--color-text-secondary) mb-2">
          {new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" })}
        </p>

        {/* Progress bar */}
        {activities.length > 0 && (
          <div className="mb-8">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-(--color-text-secondary)">
                {completedCount} of {activities.length} activities completed
              </span>
              {completedCount === activities.length && activities.length > 0 && (
                <span className="text-sm font-medium text-(--color-success)">All done!</span>
              )}
            </div>
            <div className="w-full h-2 rounded-full bg-(--color-border)">
              <div
                className="h-full rounded-full bg-(--color-success) transition-all duration-500"
                style={{ width: `${activities.length > 0 ? (completedCount / activities.length) * 100 : 0}%` }}
              />
            </div>
          </div>
        )}

        {/* Activities */}
        {activities.length === 0 ? (
          <div className="bg-(--color-surface) rounded-2xl shadow-sm border border-(--color-border) py-16 text-center">
            <h3 className="text-lg font-semibold text-(--color-text) mb-2">
              No learning scheduled for today!
            </h3>
            <p className="text-base text-(--color-text-tertiary)">Enjoy your free time.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {/* Active activities first */}
            {activities.filter((a) => a.status !== "completed").map((act) => {
              const t = typeLabels[act.activity_type] || { label: act.activity_type, color: "bg-(--color-page) text-(--color-text-secondary)" };
              return (
                <div key={act.id}
                  className="bg-(--color-surface) rounded-2xl shadow-sm border border-(--color-border) p-5">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h3 className="text-lg font-medium text-(--color-text)">{act.title}</h3>
                      <div className="flex items-center gap-3 mt-2">
                        <span className={`text-xs font-medium px-2 py-1 rounded-full ${t.color}`}>{t.label}</span>
                        {act.estimated_minutes && (
                          <span className="text-sm text-(--color-text-tertiary)">{act.estimated_minutes} min</span>
                        )}
                      </div>
                    </div>
                    <button
                      onClick={() => startActivity(act)}
                      className="px-6 py-2.5 text-base font-semibold text-white bg-(--color-success) rounded-xl hover:opacity-90 transition-opacity shadow-sm"
                    >
                      {act.status === "in_progress" ? "Continue" : "Start"}
                    </button>
                  </div>
                </div>
              );
            })}

            {/* Completed activities */}
            {activities.filter((a) => a.status === "completed").map((act) => {
              const t = typeLabels[act.activity_type] || { label: act.activity_type, color: "bg-(--color-page) text-(--color-text-secondary)" };
              return (
                <div key={act.id}
                  className="bg-(--color-surface) rounded-2xl shadow-sm border border-(--color-border) p-5 opacity-60">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h3 className="text-lg font-medium text-(--color-text-tertiary)">{act.title}</h3>
                      <div className="flex items-center gap-3 mt-2">
                        <span className={`text-xs font-medium px-2 py-1 rounded-full ${t.color}`}>{t.label}</span>
                      </div>
                    </div>
                    <span className="text-sm text-(--color-success) font-medium flex items-center gap-1">
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                      </svg>
                      Done
                    </span>
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
