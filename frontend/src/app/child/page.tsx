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
import VocationalActivityDetail from "@/components/VocationalActivityDetail";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface TodayActivity {
  id: string;
  title: string;
  activity_type: string;
  status: string;
  estimated_minutes: number | null;
  node_id: string | null;
  error?: string;
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
  const [error, setError] = useState("");

  // Learning state
  const [activeActivity, setActiveActivity] = useState<TodayActivity | null>(null);
  const [attemptId, setAttemptId] = useState("");
  const [learningContext, setLearningContext] = useState<LearningContext | null>(null);
  const [completed, setCompleted] = useState(false);
  const [completionData, setCompletionData] = useState<{ mastery?: string; prevMastery?: string }>({});
  const startTimeRef = useRef<number>(0);

  // Theme
  const [theme, setTheme] = useState({ background: "plain", color_accent: "blue", font_size: "normal", avatar: "owl" });
  const [showSettings, setShowSettings] = useState(false);

  useEffect(() => { init(); }, []);
  useEffect(() => {
    const c = children.find((ch) => ch.id === selectedId);
    document.title = c ? `${c.first_name}'s Learning | METHEAN` : "Learning | METHEAN";
  }, [selectedId, children]);
  useEffect(() => {
    if (selectedId) {
      loadToday();
      fetch(`${API}/children/${selectedId}/theme`, { credentials: "include" })
        .then((r) => r.ok ? r.json() : {})
        .then((t) => setTheme({ background: t.background || "plain", color_accent: t.color_accent || "blue", font_size: t.font_size || "normal", avatar: t.avatar || "owl" }))
        .catch(() => {});
    }
  }, [selectedId]);

  async function init() {
    setLoading(true);
    setError("");
    try {
      await auth.me();
      const resp = await fetch(`${API}/children`, { credentials: "include" });
      if (!resp.ok) throw new Error("Couldn't load your learning page.");
      const data: ChildInfo[] = await resp.json();
      setChildren(Array.isArray(data) ? data : []);
      if (data.length > 0) setSelectedId(data[0].id);
    } catch (err: any) {
      if (err?.message?.includes("auth") || err?.status === 401) {
        window.location.href = "/auth";
        return;
      }
      setError(err?.message || "Something went wrong loading your learning page.");
    } finally {
      setLoading(false);
    }
  }

  async function loadToday() {
    setError("");
    try {
      const resp = await fetch(`${API}/children/${selectedId}/today`, { credentials: "include" });
      if (resp.ok) setActivities(await resp.json());
    } catch (err: any) {
      setError(err?.message || "Couldn't load today's activities. Try again in a moment.");
    }
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
      setActivities((prev) =>
        prev.map((a) => a.id === act.id ? { ...a, error: "Couldn't start this activity. Try again." } : a)
      );
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
    } catch (err: any) {
      setError(err?.message || "Couldn't save your work. Don't worry, try submitting again.");
    }
  }

  async function saveTheme(updates: Partial<typeof theme>) {
    const newTheme = { ...theme, ...updates };
    setTheme(newTheme);
    const csrf = document.cookie.match(/(?:^|; )csrf_token=([^;]*)/)?.[1];
    fetch(`${API}/children/${selectedId}/theme`, {
      method: "PUT", credentials: "include",
      headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": decodeURIComponent(csrf) } : {}) },
      body: JSON.stringify(newTheme),
    }).catch(() => {});
  }

  const bgStyles: Record<string, React.CSSProperties> = {
    plain: { background: "#FDF6E3" },
    meadow: { background: "linear-gradient(180deg, #E8F5E9 0%, #C8E6C9 100%)" },
    ocean: { background: "linear-gradient(180deg, #E3F2FD 0%, #BBDEFB 100%)" },
    forest: { background: "linear-gradient(180deg, #E8F0E4 0%, #C5D9BA 100%)" },
    space: { background: "linear-gradient(180deg, #1A1A2E 0%, #16213E 100%)", color: "#E0E0E0" },
    desert: { background: "linear-gradient(180deg, #FFF3E0 0%, #FFE0B2 100%)" },
    mountains: { background: "linear-gradient(180deg, #ECEFF1 0%, #CFD8DC 100%)" },
  };

  const avatarEmoji: Record<string, string> = {
    bear: "🐻", owl: "🦉", fox: "🦊", rabbit: "🐰", deer: "🦌", eagle: "🦅", wolf: "🐺",
  };

  const fontSizeClass = theme.font_size === "large" ? "text-lg" : theme.font_size === "extra-large" ? "text-xl" : "";

  function goNext() {
    setActiveActivity(null);
    setAttemptId("");
    setLearningContext(null);
    setCompleted(false);
    loadToday();
  }

  if (loading) {
    const bgStyle = bgStyles[theme.background] || bgStyles.plain;
    return (
      <div className="min-h-screen" style={bgStyle}>
        <header className="bg-(--color-surface) border-b border-(--color-border) px-6 py-4">
          <div className="max-w-2xl mx-auto flex justify-between items-center">
            <MetheanLogo markSize={24} wordmarkHeight={12} color="#0F1B2D" gap={8} />
            <div className="w-24 h-8 rounded-lg bg-(--color-border) animate-pulse" />
          </div>
        </header>
        <div className="max-w-2xl mx-auto px-6 py-8">
          <div className="h-8 w-48 rounded bg-(--color-border) animate-pulse mb-2" />
          <div className="h-5 w-64 rounded bg-(--color-border) animate-pulse mb-6" />
          <div className="h-2 rounded-full bg-(--color-border) animate-pulse mb-8" />
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-(--color-surface) border border-(--color-border) rounded-2xl p-5 mb-3">
              <div className="h-5 w-40 rounded bg-(--color-border) animate-pulse mb-3" />
              <div className="flex gap-2">
                <div className="h-4 w-16 rounded bg-(--color-border) animate-pulse" />
                <div className="h-4 w-12 rounded bg-(--color-border) animate-pulse" />
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    const bgStyle = bgStyles[theme.background] || bgStyles.plain;
    return (
      <div className="min-h-screen flex items-center justify-center" style={bgStyle}>
        <div className="text-center px-6 max-w-sm">
          <div className="text-5xl mb-4">🌧️</div>
          <h2 className="text-xl font-semibold text-(--color-text) mb-2">Oops! Something went wrong</h2>
          <p className="text-sm text-(--color-text-secondary) mb-6">{error}</p>
          <button
            onClick={() => { setError(""); init(); }}
            className="px-6 py-3 text-sm font-semibold text-white bg-(--color-accent) rounded-2xl hover:opacity-90 transition-opacity"
          >Try Again</button>
        </div>
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
      <div className={`min-h-screen ${fontSizeClass}`} style={bgStyles[theme.background] || bgStyles.plain}>
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
      <div className={`min-h-screen ${fontSizeClass}`} style={bgStyles[theme.background] || bgStyles.plain}>
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
    <div className={`min-h-screen ${fontSizeClass}`} style={bgStyles[theme.background] || bgStyles.plain}>
      {/* Header */}
      <header className="bg-(--color-surface) border-b border-(--color-border) px-6 py-5">
        <div className="max-w-2xl mx-auto flex items-center justify-between">
          <MetheanLogo markSize={24} wordmarkHeight={12} color="#0F1B2D" gap={8} />
          <div className="flex items-center gap-3">
            {children.length > 1 && (
              <select
                value={selectedId}
                onChange={(e) => setSelectedId(e.target.value)}
                className="text-sm border border-(--color-border) rounded-[14px] px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-(--color-accent)/30"
              >
                {children.map((c) => (
                  <option key={c.id} value={c.id}>{c.first_name}</option>
                ))}
              </select>
            )}
            <button onClick={() => setShowSettings(!showSettings)} className="p-1.5 text-(--color-text-tertiary) hover:text-(--color-text) transition-colors">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      {/* Settings panel */}
      {showSettings && (
        <div className="max-w-2xl mx-auto px-6 pt-4">
          <div className="bg-(--color-surface) rounded-2xl border border-(--color-border) p-5 mb-4">
            <h3 className="text-sm font-semibold text-(--color-text) mb-4">My Settings</h3>
            <div className="space-y-4">
              <div>
                <label className="text-xs text-(--color-text-secondary) mb-2 block">Background</label>
                <div className="flex gap-2 flex-wrap">
                  {(["plain", "meadow", "ocean", "forest", "space", "desert", "mountains"] as const).map((bg) => (
                    <button key={bg} onClick={() => saveTheme({ background: bg })}
                      className={`w-14 h-10 rounded-xl border-2 text-[9px] font-medium capitalize transition-all ${theme.background === bg ? "border-(--color-accent) ring-1 ring-(--color-accent)/20" : "border-(--color-border)"}`}
                      style={bgStyles[bg]}>{bg}</button>
                  ))}
                </div>
              </div>
              <div>
                <label className="text-xs text-(--color-text-secondary) mb-2 block">Avatar</label>
                <div className="flex gap-2">
                  {(["bear", "owl", "fox", "rabbit", "deer", "eagle", "wolf"] as const).map((a) => (
                    <button key={a} onClick={() => saveTheme({ avatar: a })}
                      className={`w-10 h-10 rounded-full text-xl border-2 transition-all ${theme.avatar === a ? "border-(--color-accent) ring-1 ring-(--color-accent)/20" : "border-(--color-border)"}`}>{avatarEmoji[a]}</button>
                  ))}
                </div>
              </div>
              <div>
                <label className="text-xs text-(--color-text-secondary) mb-2 block">Text Size</label>
                <div className="flex gap-2">
                  {([["normal", "Normal"], ["large", "Large"], ["extra-large", "Extra Large"]] as const).map(([val, label]) => (
                    <button key={val} onClick={() => saveTheme({ font_size: val })}
                      className={`px-3 py-1.5 text-xs rounded-lg border-2 transition-all ${theme.font_size === val ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border)"}`}>{label}</button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="max-w-2xl mx-auto px-6 py-8">
        {/* Greeting */}
        <h2 className="text-2xl font-semibold text-(--color-text) mb-1">
          {avatarEmoji[theme.avatar] || "🦉"} {greeting(childName)}
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
          <div className="text-center py-16">
            <div className="text-5xl mb-4">{avatarEmoji[theme.avatar] || "🦉"}</div>
            <h3 className="text-lg font-semibold text-(--color-text) mb-2">
              No learning scheduled for today!
            </h3>
            <p className="text-sm text-(--color-text-secondary)">
              Enjoy your free time, {childName}. Your next activities will show up here when they're ready.
            </p>
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
                  {act.error && (
                    <p className="text-xs text-(--color-danger) mt-2">{act.error}</p>
                  )}
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
