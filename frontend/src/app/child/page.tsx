"use client";

import { useEffect, useState, useRef } from "react";
import { auth, attempts, learn, children as childrenApi, achievements as achievementsApi, type LearningContext, type MapState } from "@/lib/api";
import { useToast } from "@/components/Toast";
import { MetheanLogo } from "@/components/Brand";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import JourneyMap from "@/components/child/JourneyMap";
import LessonView from "@/components/child/LessonView";
import PracticeView from "@/components/child/PracticeView";
import ReviewView from "@/components/child/ReviewView";
import AssessmentView from "@/components/child/AssessmentView";
import ProjectView from "@/components/child/ProjectView";
import FieldTripView from "@/components/child/FieldTripView";
import CompletionState from "@/components/child/CompletionState";
import VocationalActivityDetail from "@/components/VocationalActivityDetail";


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

const typeConfig: Record<string, { label: string; bg: string; icon: string }> = {
  lesson:     { label: "Lesson",     bg: "bg-(--color-accent-light)",         icon: "📖" },
  practice:   { label: "Practice",   bg: "bg-(--color-success-light)",        icon: "✏️" },
  review:     { label: "Review",     bg: "bg-(--color-warning-light)",        icon: "🔄" },
  assessment: { label: "Assessment", bg: "bg-(--color-constitutional-light)", icon: "📋" },
  project:    { label: "Project",    bg: "bg-(--color-danger-light)",         icon: "🔨" },
  field_trip: { label: "Field Trip", bg: "bg-(--color-accent-light)",         icon: "🧭" },
};

export default function ChildPage() {
  const { toast } = useToast();
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

  // Transition overlay state
  const [transitioning, setTransitioning] = useState(false);
  const [transitionActivity, setTransitionActivity] = useState<TodayActivity | null>(null);
  const [transitionVisible, setTransitionVisible] = useState(false);

  // Theme
  const [theme, setTheme] = useState({ background: "plain", color_accent: "blue", font_size: "normal", avatar: "owl" });
  const [showSettings, setShowSettings] = useState(false);

  // Achievements & streak
  const [streak, setStreak] = useState<{ current_streak: number; longest_streak: number } | null>(null);
  const [earnedAchievements, setEarnedAchievements] = useState<any[]>([]);
  const [totalMastered, setTotalMastered] = useState(0);
  const [journeyMaps, setJourneyMaps] = useState<MapState[]>([]);

  useEffect(() => { init(); }, []);
  useEffect(() => {
    const c = children.find((ch) => ch.id === selectedId);
    document.title = c ? `${c.first_name}'s Learning | METHEAN` : "Learning | METHEAN";
  }, [selectedId, children]);
  useEffect(() => {
    if (selectedId) {
      loadToday();
      childrenApi.theme(selectedId)
        .then((t) => setTheme({ background: t.background || "plain", color_accent: t.color_accent || "blue", font_size: t.font_size || "normal", avatar: t.avatar || "owl" }))
        .catch(() => {});
      achievementsApi.streak(selectedId).then(setStreak).catch(() => {});
      achievementsApi.list(selectedId).then((d) => setEarnedAchievements(d.earned || [])).catch(() => {});
      childrenApi.state(selectedId).then((s) => setTotalMastered(s?.mastered_count || 0)).catch(() => {});
      childrenApi.allMapState(selectedId).then(setJourneyMaps).catch(() => {});
    }
  }, [selectedId]);

  async function init() {
    setLoading(true);
    setError("");
    try {
      await auth.me();
      const data: ChildInfo[] = await childrenApi.list() as any;
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
      const todayData = await childrenApi.today(selectedId);
      setActivities(todayData);
    } catch (err: any) {
      setError(err?.message || "Couldn't load today's activities. Try again in a moment.");
    }
  }

  async function startActivity(act: TodayActivity) {
    // Show transition overlay
    setTransitionActivity(act);
    setTransitioning(true);
    // Trigger fade-in on next frame
    requestAnimationFrame(() => setTransitionVisible(true));

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

      // Fade out transition overlay
      setTransitionVisible(false);
      setTimeout(() => { setTransitioning(false); setTransitionActivity(null); }, 150);
    } catch (err: any) {
      // Dismiss overlay on error
      setTransitionVisible(false);
      setTimeout(() => { setTransitioning(false); setTransitionActivity(null); }, 150);
      toast("Couldn't start activity", "error");
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
      toast("Activity submitted", "success");
    } catch (err: any) {
      toast("Couldn't save your work", "error");
      setError(err?.message || "Couldn't save your work. Don't worry, try submitting again.");
    }
  }

  async function saveTheme(updates: Partial<typeof theme>) {
    const newTheme = { ...theme, ...updates };
    setTheme(newTheme);
    childrenApi.updateTheme(selectedId, newTheme).catch(() => {});
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

  // ── TRANSITION OVERLAY ──
  const transitionOverlay = transitioning && transitionActivity && (() => {
    const tc = typeConfig[transitionActivity.activity_type] || { label: transitionActivity.activity_type, bg: "bg-(--color-page)", icon: "📄" };
    return (
      <div
        className="fixed inset-0 z-50 flex items-center justify-center"
        style={{
          background: "var(--color-page)",
          opacity: transitionVisible ? 1 : 0,
          transition: transitionVisible ? "opacity 200ms ease-out" : "opacity 150ms ease-in",
        }}
      >
        <div className="text-center">
          <div className="w-16 h-16 rounded-2xl bg-(--color-surface) border border-(--color-border) flex items-center justify-center text-3xl mx-auto mb-4 shadow-sm">
            {tc.icon}
          </div>
          <p className="text-sm font-medium text-(--color-text) mb-4">{transitionActivity.title}</p>
          <div className="w-5 h-5 mx-auto border-2 border-(--color-accent) border-t-transparent rounded-full animate-spin" />
        </div>
      </div>
    );
  })();

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
        <div className="flex items-center gap-4 mb-2">
          <div className="w-12 h-12 rounded-full bg-(--color-accent-light) flex items-center justify-center text-2xl shrink-0">
            {avatarEmoji[theme.avatar] || "🦉"}
          </div>
          <div>
            <h2 className="text-2xl font-semibold text-(--color-text)">{greeting(childName)}</h2>
            <p className="text-sm text-(--color-text-secondary)">
              {activities.length > 0
                ? `You have ${activities.length} activities today. ${completedCount} completed.`
                : new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" })}
            </p>
          </div>
        </div>

        {/* Progress bar */}
        {activities.length > 0 && (
          <div className="mb-8 mt-4">
            <div className="w-full h-2 rounded-full bg-(--color-border)">
              <div
                className="h-full rounded-full bg-(--color-success) transition-all duration-500"
                style={{ width: `${activities.length > 0 ? (completedCount / activities.length) * 100 : 0}%` }}
              />
            </div>
          </div>
        )}

        {/* Stats row */}
        <div className="grid grid-cols-3 gap-2 mb-6">
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-3 text-center">
            <div className="text-xl font-bold text-(--color-text)">
              {streak && streak.current_streak > 0 ? (
                <>{streak.current_streak >= 7 && <span className="animate-pulse">🔥</span>} {streak.current_streak}</>
              ) : "0"}
            </div>
            <div className="text-[10px] text-(--color-text-tertiary)">day streak</div>
          </div>
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-3 text-center">
            <div className="text-xl font-bold text-(--color-success)">⭐ {totalMastered}</div>
            <div className="text-[10px] text-(--color-text-tertiary)">mastered</div>
          </div>
          <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) p-3 text-center">
            <div className="text-xl font-bold text-(--color-accent)">📚 {completedCount}</div>
            <div className="text-[10px] text-(--color-text-tertiary)">completed</div>
          </div>
        </div>

        {/* Recent achievements */}
        {earnedAchievements.length > 0 && (
          <div className="mb-6">
            <div className="flex items-center gap-1.5 mb-2">
              <span className="text-xs font-medium text-(--color-text-secondary)">Recent achievements</span>
            </div>
            <div className="flex gap-2 overflow-x-auto pb-1">
              {earnedAchievements.slice(0, 3).map((ach: any) => {
                const isNew = ach.earned_at && (Date.now() - new Date(ach.earned_at).getTime()) < 86400000;
                return (
                  <div key={ach.id} className={`shrink-0 bg-(--color-surface) rounded-[12px] border px-3 py-2 flex items-center gap-2 ${isNew ? "border-(--gold) ring-1 ring-(--gold)/20" : "border-(--color-border)"}`}>
                    <span className="text-lg">{ach.icon}</span>
                    <div>
                      <div className="text-xs font-medium text-(--color-text) flex items-center gap-1">
                        {ach.title}
                        {isNew && <span className="text-[8px] px-1 py-0.5 bg-(--gold) text-white rounded-full font-bold">NEW</span>}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Journey Maps */}
        {journeyMaps.length > 0 && (
          <div className="mb-6">
            <div className="text-xs font-medium text-(--color-text-secondary) mb-2">Your Learning Journey</div>
            <div className="flex gap-4 overflow-x-auto pb-2">
              {journeyMaps.slice(0, 3).map((ms) => {
                const journeyNodes = (ms.nodes || []).slice(0, 12).map((n: any) => ({
                  id: n.node_id,
                  title: n.title,
                  mastery: n.mastery_level || "not_started",
                  is_next: n.status === "available" && n.prerequisites_met,
                }));
                // Mark only the first available node as "next"
                let foundNext = false;
                for (const jn of journeyNodes) {
                  if (jn.is_next && !foundNext) { foundNext = true; }
                  else if (jn.is_next) { jn.is_next = false; }
                }
                return (
                  <div key={ms.learning_map_id} className="shrink-0">
                    <JourneyMap
                      nodes={journeyNodes}
                      subject={ms.map_name || "Learning Path"}
                    />
                  </div>
                );
              })}
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
          <div className="space-y-3">
            {/* Active activities */}
            {activities.filter((a) => a.status !== "completed").map((act, idx) => {
              const tc = typeConfig[act.activity_type] || { label: act.activity_type, bg: "bg-(--color-page)", icon: "📄" };
              return (
                <div key={act.id} className="animate-fade-up" style={{ animationDelay: `${idx * 60}ms` }}>
                <Card padding="p-4">
                  <div className="flex items-center gap-3">
                    <div className={`w-10 h-10 rounded-[10px] ${tc.bg} flex items-center justify-center text-xl shrink-0`}>
                      {tc.icon}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-sm font-medium text-(--color-text) truncate">{act.title}</h3>
                      <p className="text-xs text-(--color-text-tertiary)">{tc.label}{act.estimated_minutes ? ` · ${act.estimated_minutes} min` : ""}</p>
                    </div>
                    <Button variant="primary" size="sm" onClick={() => startActivity(act)}>
                      {act.status === "in_progress" ? "Continue" : "Start"}
                    </Button>
                  </div>
                  {act.error && <p className="text-xs text-(--color-danger) mt-2">{act.error}</p>}
                </Card>
                </div>
              );
            })}

            {/* Completed activities */}
            {activities.filter((a) => a.status === "completed").map((act) => {
              const tc = typeConfig[act.activity_type] || { label: act.activity_type, bg: "bg-(--color-page)", icon: "📄" };
              return (
                <Card key={act.id} padding="p-4" className="opacity-60">
                  <div className="flex items-center gap-3">
                    <div className={`w-10 h-10 rounded-[10px] ${tc.bg} flex items-center justify-center text-xl shrink-0`}>
                      {tc.icon}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-sm font-medium text-(--color-text-tertiary) line-through truncate">{act.title}</h3>
                      <p className="text-xs text-(--color-text-tertiary)">{tc.label}</p>
                    </div>
                    <span className="w-7 h-7 rounded-full bg-(--color-success-light) flex items-center justify-center shrink-0">
                      <svg className="w-4 h-4 text-(--color-success)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                      </svg>
                    </span>
                  </div>
                </Card>
              );
            })}
          </div>
        )}
      </div>

      {/* Transition overlay */}
      {transitionOverlay}
    </div>
  );
}
