"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import {
  auth, attempts, learn, children as childrenApi,
  type LearningContext, type ChildDashboardResponse,
} from "@/lib/api";
import { useToast } from "@/components/Toast";
import { useMobile } from "@/lib/useMobile";
import { haptic } from "@/lib/haptics";
import { usePersonalization } from "@/lib/PersonalizationProvider";
import { useSoundCue } from "@/lib/useSoundCue";
import { ActivityIcon, type ActivityType } from "@/components/ActivityIcon";
import { MySpace } from "@/components/child/MySpace";
import JourneyMap, { JourneyCarousel } from "@/components/child/JourneyMap";
import LessonView from "@/components/child/LessonView";
import PracticeView from "@/components/child/PracticeView";
import ReviewView from "@/components/child/ReviewView";
import AssessmentView from "@/components/child/AssessmentView";
import ProjectView from "@/components/child/ProjectView";
import FieldTripView from "@/components/child/FieldTripView";
import CompletionState from "@/components/child/CompletionState";

// ── Types ──

interface ChildInfo { id: string; first_name: string; grade_level: string | null }

type DashActivity = ChildDashboardResponse["today"]["activities"][0];

const typeLabels: Record<string, { label: string; icon: string }> = {
  lesson: { label: "Lesson", icon: "\uD83D\uDCD6" },
  practice: { label: "Practice", icon: "\u270F\uFE0F" },
  review: { label: "Review", icon: "\uD83D\uDD04" },
  assessment: { label: "Assessment", icon: "\uD83D\uDCCB" },
  project: { label: "Project", icon: "\uD83D\uDD28" },
  field_trip: { label: "Field Trip", icon: "\uD83E\uDDED" },
};

const typeColors: Record<string, string> = {
  lesson: "rgba(59,130,246,0.1)",
  practice: "rgba(34,197,94,0.1)",
  review: "rgba(234,179,8,0.1)",
  assessment: "rgba(168,85,247,0.1)",
  project: "rgba(20,184,166,0.1)",
  field_trip: "rgba(249,115,22,0.1)",
};

/** Top-edge border colors per activity type for the new card layout.
 *  Spec mapping: lesson = blue accent, practice = brand gold,
 *  assessment = navy, project = green, field_trip = constitutional
 *  (warm brown), review keeps the gold ladder. Solid CSS variable
 *  references so the value tracks the design tokens. */
const typeTopBorder: Record<string, string> = {
  lesson: "var(--color-accent)",
  practice: "var(--color-brand-gold)",
  review: "var(--color-progress)",
  assessment: "var(--color-brand-navy)",
  project: "var(--color-success)",
  field_trip: "var(--color-constitutional)",
};

// ── Progress Ring ──

function ProgressRing({ completed, total, minutesRemaining, large }: {
  completed: number; total: number; minutesRemaining: number; large?: boolean;
}) {
  const pct = total > 0 ? completed / total : 0;
  const r = 36;
  const circ = 2 * Math.PI * r;
  const offset = circ * (1 - pct);
  const allDone = completed >= total && total > 0;
  const sizeClass = large ? "w-[120px] h-[120px] md:w-[140px] md:h-[140px]" : "w-24 h-24";

  return (
    <div className={`relative ${sizeClass} shrink-0`} role="img" aria-label={`${completed} of ${total} activities completed`}>
      <svg viewBox="0 0 80 80" className="w-full h-full">
        <circle cx="40" cy="40" r={r} fill="none" stroke="var(--color-border)" strokeWidth="4" />
        <circle cx="40" cy="40" r={r} fill="none"
          stroke={allDone ? "var(--color-success)" : "var(--color-accent)"}
          strokeWidth="4" strokeLinecap="round"
          strokeDasharray={circ} strokeDashoffset={offset}
          transform="rotate(-90 40 40)"
          className="transition-all duration-700" />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        {allDone ? (
          <span className="text-2xl" role="img" aria-label="complete">&#10003;</span>
        ) : (
          <>
            <span className={`${large ? "text-lg" : "text-sm"} font-bold text-(--color-text)`}>{completed}/{total}</span>
            <span className={`${large ? "text-xs" : "text-[10px]"} text-(--color-text-tertiary)`}>{minutesRemaining}m left</span>
          </>
        )}
      </div>
    </div>
  );
}

// ── Main Page ──

export default function ChildPage() {
  const { toast } = useToast();
  // Personalization is owned by the wrapping layout's
  // <PersonalizationProvider>; the VibeProvider already applies the
  // CSS-variable token bag to the subtree, so the page no longer
  // owns its own background style.
  const { profile, loading: profileLoading } = usePersonalization();
  const router = useRouter();

  // First-run gate: unonboarded kids bounce to /child/welcome.
  // We wait for the profile to load (so we don't redirect on the
  // default-shape profile the provider serves during fetch) and
  // we don't gate on the local `loading` flag, which only tracks
  // the auth + children list.
  useEffect(() => {
    if (profileLoading) return;
    if (!profile.onboarded) {
      router.replace("/child/welcome");
    }
  }, [profileLoading, profile.onboarded, router]);

  // Auth state
  const [childrenList, setChildrenList] = useState<ChildInfo[]>([]);
  const [selectedId, setSelectedId] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Dashboard data (single API call)
  const [dash, setDash] = useState<ChildDashboardResponse | null>(null);

  // Activity mode
  const [activeActivity, setActiveActivity] = useState<DashActivity | null>(null);
  const [attemptId, setAttemptId] = useState("");
  const [learningContext, setLearningContext] = useState<LearningContext | null>(null);
  const [completed, setCompleted] = useState(false);
  const [completionData, setCompletionData] = useState<{ mastery?: string; prevMastery?: string }>({});
  const startTimeRef = useRef(0);

  // Transition
  const [transitioning, setTransitioning] = useState(false);
  const [transitionAct, setTransitionAct] = useState<DashActivity | null>(null);
  const [transVisible, setTransVisible] = useState(false);

  const [showSettings, setShowSettings] = useState(false);
  const [showJourney, setShowJourney] = useState(false);
  const isMobile = useMobile();
  const [showCelebration, setShowCelebration] = useState(false);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Sound cues. The hook short-circuits when the kid's pack is
  // "off" or before the first user gesture, so wiring it here is
  // always safe.
  const playCue = useSoundCue();

  // Tracks the previous mastery_transitions_up count so a refresh
  // that brings the number up plays the mastery_up cue exactly
  // once per transition. Null on first load (don't fire for the
  // initial value, only for deltas).
  const prevMasteryUpRef = useRef<number | null>(null);

  // ── Init ──

  useEffect(() => { init(); }, []);
  useEffect(() => {
    if (selectedId) loadDashboard();
  }, [selectedId]);
  useEffect(() => {
    if (dash) document.title = `${dash.child.first_name}'s Learning | METHEAN`;
  }, [dash]);

  // Fire the mastery_up cue exactly once per upward transition.
  // First-load value is recorded without firing so refreshing the
  // page doesn't replay yesterday's celebration.
  useEffect(() => {
    if (!dash) return;
    const next = dash.progress.this_week.mastery_transitions_up;
    const prev = prevMasteryUpRef.current;
    if (prev !== null && next > prev) {
      playCue("mastery_up", { volume: 0.6 });
    }
    prevMasteryUpRef.current = next;
  }, [dash, playCue]);

  async function init() {
    setLoading(true);
    try {
      await auth.me();
      const data: ChildInfo[] = await childrenApi.list() as any;
      setChildrenList(Array.isArray(data) ? data : []);
      if (data.length > 0) setSelectedId(data[0].id);
    } catch (err: any) {
      if (err?.status === 401) { window.location.href = "/auth"; return; }
      setError("Something went wrong. Try refreshing.");
    } finally {
      setLoading(false);
    }
  }

  async function loadDashboard() {
    setError("");
    try {
      // Theme used to be fetched here. The PersonalizationProvider
      // now owns canonical vibe/companion state for the subtree.
      const d = await childrenApi.dashboard(selectedId);
      setDash(d);
    } catch {
      setError("Couldn't load your learning page. Try again in a moment.");
    }
  }

  // ── Timer ──

  useEffect(() => {
    if (activeActivity) {
      setElapsedSeconds(0);
      timerRef.current = setInterval(() => setElapsedSeconds((s) => s + 1), 1000);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [activeActivity?.id]);

  const formatTimer = (s: number) => `${Math.floor(s / 60)}:${(s % 60).toString().padStart(2, "0")}`;

  // ── Activity Lifecycle ──

  async function startActivity(act: DashActivity) {
    setTransitionAct(act);
    setTransitioning(true);
    requestAnimationFrame(() => setTransVisible(true));
    try {
      const attempt = await attempts.start(act.id, selectedId);
      setAttemptId(attempt.id);
      startTimeRef.current = Date.now();
      const ctx = await learn.context(act.id, selectedId);
      setLearningContext(ctx);
      setActiveActivity(act);
      setCompleted(false);
      setCompletionData({});
      setTransVisible(false);
      setTimeout(() => { setTransitioning(false); setTransitionAct(null); }, 150);
    } catch {
      setTransVisible(false);
      setTimeout(() => { setTransitioning(false); setTransitionAct(null); }, 150);
      toast("Couldn't start activity", "error");
    }
  }

  async function handleComplete(data: {
    confidence: number;
    responses: Array<{ prompt: string; response: string }>;
    self_reflection: string;
  }) {
    if (!attemptId) return;
    const dur = Math.max(1, Math.round((Date.now() - startTimeRef.current) / 60000));
    try {
      const result = await attempts.submit(attemptId, {
        confidence: data.confidence, duration_minutes: dur,
        feedback: { responses: data.responses, self_reflection: data.self_reflection },
      });
      setCompletionData({
        mastery: result.mastery_level?.replace(/_/g, " "),
        prevMastery: result.previous_mastery?.replace(/_/g, " "),
      });
      haptic("success");
      setShowCelebration(true);
      setTimeout(() => { setShowCelebration(false); setCompleted(true); }, 1500);
    } catch {
      toast("Couldn't save your work. Try again.", "error");
    }
  }

  function goNext() {
    setActiveActivity(null);
    setAttemptId("");
    setLearningContext(null);
    setCompleted(false);
    loadDashboard();
  }

  // Page background comes from the active vibe's CSS variable bag
  // that VibeProvider applies on the wrapper. The pre-
  // personalization gradient map is gone; My Space is the single
  // surface for theming changes.
  const pageBg: React.CSSProperties = { background: "var(--color-page)" };

  // ── Loading ──

  if (loading) {
    return (
      <div className="min-h-screen" style={pageBg}>
        <div className="max-w-2xl mx-auto px-8 py-12">
          <div className="h-8 w-48 rounded bg-(--color-border) animate-pulse mb-3" />
          <div className="h-5 w-72 rounded bg-(--color-border) animate-pulse mb-10" />
          {[1, 2, 3].map(i => (
            <div key={i} className="bg-(--color-surface) rounded-2xl border border-(--color-border) p-6 mb-4">
              <div className="h-5 w-40 rounded bg-(--color-border) animate-pulse" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={pageBg}>
        <div className="text-center px-8 max-w-sm">
          <p className="text-lg font-medium text-(--color-text) mb-2">Something went wrong</p>
          <p className="text-sm text-(--color-text-secondary) mb-6">{error}</p>
          <button onClick={() => { setError(""); init(); }}
            className="px-6 py-3 text-sm font-medium text-white bg-(--color-accent) rounded-2xl">Try Again</button>
        </div>
      </div>
    );
  }

  if (!dash) return null;

  const activities = dash.today.activities;
  const remaining = activities.filter(a => a.status !== "completed");
  const allDone = remaining.length === 0 && activities.length > 0;

  // ═══ PHASE 3: COMPLETION ═══
  if (activeActivity && completed) {
    const isReview = activeActivity.is_review;
    return (
      <div className={`min-h-screen`} style={pageBg}>
        <div className="max-w-xl mx-auto px-8 py-16">
          <CompletionState
            activityTitle={activeActivity.title}
            masteryLevel={completionData.mastery}
            previousMastery={completionData.prevMastery}
            onNext={goNext}
            allDone={remaining.length <= 1}
          />
          {isReview && !completionData.mastery?.includes("mastered") && (
            <p className="text-center text-sm text-(--color-text-secondary) mt-4 italic">Your memory is getting stronger.</p>
          )}
          <p className="text-center text-xs text-(--color-text-tertiary) mt-6">
            {remaining.length > 1 ? `${remaining.length - 1} activit${remaining.length - 1 === 1 ? "y" : "ies"} remaining today.` : ""}
          </p>
        </div>
      </div>
    );
  }

  // ═══ PHASE 2: ACTIVITY MODE ═══
  if (activeActivity && learningContext) {
    const t = activeActivity.type;
    return (
      <div className={`fixed inset-0 z-50 flex flex-col`} style={{ ...pageBg, paddingTop: "var(--safe-top)" }}>
        {/* Top bar */}
        <div className="flex items-center h-12 px-4 shrink-0 bg-(--color-surface)/80 backdrop-blur border-b border-(--color-border)/50">
          <button onClick={goNext} className="w-11 h-11 flex items-center justify-center press-scale" aria-label="Back">
            <svg className="w-5 h-5 text-(--color-text-secondary)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <div className="flex-1 text-center text-sm font-medium text-(--color-text) truncate px-2">{activeActivity.title}</div>
          <span className="text-xs text-(--color-text-tertiary) w-11 text-right">{formatTimer(elapsedSeconds)}</span>
        </div>

        {/* Activity content */}
        <div className="flex-1 overflow-y-auto">
          <div className="max-w-2xl mx-auto px-4 md:px-8 py-6">
            {t === "lesson" && <LessonView context={learningContext} childId={selectedId} onComplete={handleComplete} />}
            {t === "practice" && <PracticeView context={learningContext} childId={selectedId} onComplete={handleComplete} />}
            {t === "review" && <ReviewView context={learningContext} childId={selectedId} onComplete={handleComplete} />}
            {t === "assessment" && <AssessmentView context={learningContext} onComplete={handleComplete} />}
            {t === "project" && <ProjectView context={learningContext} childId={selectedId} onComplete={handleComplete} />}
            {t === "field_trip" && <FieldTripView context={learningContext} onComplete={handleComplete} />}
          </div>
        </div>
      </div>
    );
  }

  // ═══ TRANSITION OVERLAY ═══
  const overlay = transitioning && transitionAct && (
    <div className="fixed inset-0 z-50 flex items-center justify-center"
      style={{ background: "var(--color-page)", opacity: transVisible ? 1 : 0, transition: "opacity 200ms ease" }}>
      <div className="text-center">
        <div className="w-16 h-16 rounded-2xl bg-(--color-surface) border border-(--color-border) flex items-center justify-center mx-auto mb-4 text-(--color-text-secondary)">
          <ActivityIcon type={transitionAct.type as ActivityType} size={28} />
        </div>
        <p className="text-sm font-medium text-(--color-text) mb-4">{transitionAct.title}</p>
        <div className="w-5 h-5 mx-auto border-2 border-(--color-accent) border-t-transparent rounded-full animate-spin" />
      </div>
    </div>
  );

  // ═══ PHASE 1: MORNING VIEW / PHASE 4: ALL DONE ═══
  return (
    <div className={`min-h-screen`} style={pageBg}>
      {/* Header */}
      <header className="bg-(--color-surface) border-b border-(--color-border) px-8 py-5">
        <div className="max-w-2xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            {/* Companion identity. Persona-driven avatar lands in
                Prompt 4; for this wave the slot renders the
                companion's name (or a generic fallback) so the
                emoji-avatar pattern is gone everywhere outside
                the deprecated Settings panel picker. */}
            <div
              className="px-3 h-10 rounded-full bg-(--color-accent-light) flex items-center justify-center text-xs font-medium text-(--color-text)"
              aria-label="Your companion"
            >
              {profile.companion_name || "Companion"}
            </div>
            <span className="text-sm font-medium text-(--color-text)">{dash.child.first_name}</span>
            {dash.child.streak.current > 0 && (
              <span className="text-xs text-(--color-warning) font-medium flex items-center gap-1" aria-label={`${dash.child.streak.current} day streak`}>
                <span aria-hidden="true">{dash.child.streak.current >= 7 ? "\uD83D\uDD25" : "\u2B50"}</span>
                {dash.child.streak.current}
              </span>
            )}
          </div>
          <div className="flex items-center gap-2">
            {childrenList.length > 1 && (
              <select value={selectedId} onChange={e => setSelectedId(e.target.value)}
                className="text-sm border border-(--color-border) rounded-xl px-3 py-1.5 min-h-[44px]" aria-label="Switch child">
                {childrenList.map(c => <option key={c.id} value={c.id}>{c.first_name}</option>)}
              </select>
            )}
            <button onClick={() => setShowSettings(!showSettings)}
              className="p-2 text-(--color-text-tertiary) hover:text-(--color-text) min-h-[44px] min-w-[44px] flex items-center justify-center" aria-label="Settings">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" />
                <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      <MySpace open={showSettings} onClose={() => setShowSettings(false)} />

      <div className="max-w-2xl mx-auto px-8 py-10">
        {/* Hero: Greeting + Progress Ring */}
        {isMobile ? (
          <div className="text-center mb-6">
            <p className="text-sm text-(--color-text-tertiary) mb-2">
              {new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" })}
            </p>
            {dash.child.streak.current > 1 && (
              <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium mb-3"
                style={{ background: "rgba(198,162,78,0.15)", color: "var(--color-brand-gold)" }}>
                🔥 {dash.child.streak.current} day streak
              </span>
            )}
            <h1 className="text-xl font-medium text-(--color-text) leading-snug mb-4">
              {allDone ? `You finished everything today!` : dash.greeting}
            </h1>
            {activities.length > 0 && (
              <div className="flex justify-center mb-3">
                <ProgressRing completed={dash.today.completed} total={dash.today.total_activities}
                  minutesRemaining={dash.today.estimated_minutes_remaining} large />
              </div>
            )}
            {dash.encouragement && (
              <p className="text-sm text-(--color-text-secondary) italic">{dash.encouragement}</p>
            )}
          </div>
        ) : (
          <div className="flex items-start justify-between gap-6 mb-3">
            <div className="flex-1">
              <h1 className="text-2xl font-medium text-(--color-text) leading-snug mb-1">
                {allDone ? `You finished everything today. Well done, ${dash.child.first_name}.` : dash.greeting}
              </h1>
              {dash.encouragement && (
                <p className="text-base text-(--color-text-secondary) italic leading-relaxed">{dash.encouragement}</p>
              )}
            </div>
            {activities.length > 0 && (
              <ProgressRing completed={dash.today.completed} total={dash.today.total_activities}
                minutesRemaining={dash.today.estimated_minutes_remaining} />
            )}
          </div>
        )}

        {/* Achievements */}
        {dash.child.recent_achievements.length > 0 && (
          <div className="flex gap-2 mb-8 overflow-x-auto pb-1">
            {dash.child.recent_achievements.map((ach, i) => (
              <div key={i} className="shrink-0 bg-(--color-surface) rounded-xl border border-(--color-border) px-3 py-2 flex items-center gap-2">
                <span className="text-lg">{ach.icon}</span>
                <span className="text-xs font-medium text-(--color-text)">{ach.title}</span>
              </div>
            ))}
          </div>
        )}

        {/* Today's Activities */}
        {activities.length === 0 ? (
          <div className="text-center py-20">
            {/* Companion-named callout while the persona avatar
                is still iterated in Prompt 4. */}
            <div className="text-sm font-medium text-(--color-text-secondary) mb-4">
              {profile.companion_name || "Your companion"}
            </div>
            <h2 className="text-lg font-medium text-(--color-text) mb-2">No learning scheduled today</h2>
            <p className="text-sm text-(--color-text-secondary)">Enjoy your free time, {dash.child.first_name}.</p>
          </div>
        ) : (
          <div className="max-w-[640px] mx-auto flex flex-col gap-3 mb-10">
            {/* Uncompleted activities */}
            {activities.filter(a => a.status !== "completed").map((act, idx) => {
              const tl = typeLabels[act.type] || { label: act.type, icon: "\uD83D\uDCC4" };
              const isInProgress = act.status === "in_progress";
              const topColor = typeTopBorder[act.type] || "var(--color-accent)";
              const ctaLabel = isInProgress ? "Continue" : act.type === "review" ? "Review" : "Start";
              const staggerClass = `stagger-${Math.min(8, idx + 1)}`;
              return (
                <div
                  key={act.id}
                  className={`animate-fade-up ${staggerClass} bg-(--color-surface) rounded-[14px] border border-(--color-border) shadow-[var(--shadow-card)] overflow-hidden`}
                >
                  <div className="h-[3px] w-full" style={{ background: topColor }} aria-hidden="true" />
                  <div className="p-4 sm:p-5 flex items-center gap-4">
                    <div className="w-11 h-11 rounded-full flex items-center justify-center shrink-0 text-(--color-text-secondary)"
                      style={{ background: typeColors[act.type] || "var(--color-accent-light)" }}>
                      <ActivityIcon type={act.type as ActivityType} size={20} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-[15px] font-medium text-(--color-text) truncate">{act.title}</h3>
                      <div className="flex items-center gap-2 mt-1.5">
                        <span className="text-[12px] font-medium text-(--color-text-secondary)">{tl.label}</span>
                        {act.estimated_minutes && (
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full bg-(--color-page) border border-(--color-border) text-[11px] text-(--color-text-tertiary)">
                            {act.estimated_minutes} min
                          </span>
                        )}
                        {act.subject && (
                          <span className="text-[12px] text-(--color-text-tertiary) truncate">· {act.subject}</span>
                        )}
                      </div>
                    </div>
                    <button
                      onClick={() => startActivity(act)}
                      className="shrink-0 inline-flex items-center justify-center gap-1.5 rounded-[10px] font-medium px-4 py-2 text-[13px] bg-(--color-accent) text-white hover:bg-(--color-accent-hover) press-scale focus-visible:ring-2 focus-visible:ring-(--color-accent)/30 focus-visible:ring-offset-2 min-h-[44px]"
                      aria-label={`${ctaLabel} ${act.title}`}>
                      {ctaLabel}
                      <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5} aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                      </svg>
                    </button>
                  </div>
                </div>
              );
            })}

            {/* Completed activities */}
            {activities.filter(a => a.status === "completed").map((act, idx) => {
              const tl = typeLabels[act.type] || { label: act.type, icon: "\uD83D\uDCC4" };
              const topColor = typeTopBorder[act.type] || "var(--color-accent)";
              const staggerClass = `stagger-${Math.min(8, idx + 1)}`;
              return (
                <div
                  key={act.id}
                  className={`animate-fade-up ${staggerClass} bg-(--color-surface) rounded-[14px] border border-(--color-border) overflow-hidden opacity-60`}
                >
                  <div className="h-[3px] w-full" style={{ background: topColor }} aria-hidden="true" />
                  <div className="p-4 sm:p-5 flex items-center gap-4">
                    <div className="w-11 h-11 rounded-full flex items-center justify-center shrink-0 text-(--color-text-secondary)"
                      style={{ background: typeColors[act.type] || "var(--color-accent-light)" }}>
                      <ActivityIcon type={act.type as ActivityType} size={20} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="text-[15px] text-(--color-text-tertiary) line-through truncate">{act.title}</h3>
                      <span className="text-[12px] text-(--color-text-tertiary)">{tl.label}</span>
                    </div>
                    <span className="w-9 h-9 rounded-full bg-(--color-success-light) flex items-center justify-center shrink-0 animate-scale-in" aria-label="Completed">
                      <svg className="w-5 h-5 text-(--color-success)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                      </svg>
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Subject Progress */}
        {dash.progress.subjects.length > 0 && (
          <div className="mb-10">
            <h3 className="text-xs font-medium text-(--color-text-secondary) uppercase tracking-wide mb-3">Your Progress</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {dash.progress.subjects.map(s => (
                <div key={s.name} className="bg-(--color-surface) rounded-xl border border-(--color-border) p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="w-2.5 h-2.5 rounded-full" style={{ background: s.color }} />
                    <span className="text-xs font-medium text-(--color-text)">{s.name}</span>
                  </div>
                  <div className="h-1.5 rounded-full bg-(--color-border) mb-1">
                    <div className="h-full rounded-full transition-all" style={{ width: `${s.percentage}%`, background: s.color }} />
                  </div>
                  <span className="text-[10px] text-(--color-text-tertiary)">{s.mastered} of {s.total} mastered</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Journey Maps */}
        {dash.journey_maps.length > 0 && (
          <div className="mb-10">
            <button onClick={() => setShowJourney(!showJourney)}
              className="text-xs font-medium text-(--color-text-secondary) uppercase tracking-wide mb-3 flex items-center gap-1 min-h-[44px]">
              Your Learning Journey
              <svg className={`w-3 h-3 transition-transform ${showJourney ? "rotate-180" : ""}`} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            {showJourney && (
              <JourneyCarousel maps={dash.journey_maps.map(jm => ({
                ...jm,
                nodes: jm.nodes.map(n => ({
                  id: n.id, title: n.title, mastery: n.mastery,
                  is_next: n.is_next, is_current: n.is_current,
                })),
              }))} />
            )}
          </div>
        )}

        {/* Week stats */}
        {dash.progress.this_week.activities_completed > 0 && (
          <div className="text-center text-xs text-(--color-text-tertiary) py-4 border-t border-(--color-border)/50">
            This week: {dash.progress.this_week.activities_completed} activities &middot; {dash.progress.this_week.time_spent_minutes} minutes &middot; {dash.progress.this_week.mastery_transitions_up} mastered
          </div>
        )}
      </div>

      {overlay}

      {/* Celebration animation */}
      {showCelebration && (
        <div className="fixed inset-0 z-[60] flex flex-col items-center justify-center"
          style={{ background: "rgba(250,250,248,0.95)" }}
          onClick={() => { setShowCelebration(false); setCompleted(true); }}>
          <div style={{ animation: "celebration-pop 0.4s cubic-bezier(0.32, 0.72, 0, 1) both" }}>
            <div className="w-24 h-24 rounded-full flex items-center justify-center mb-4"
              style={{ background: "rgba(45,106,79,0.1)" }}>
              <svg className="w-14 h-14 text-(--color-success)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </div>
          </div>
          <p className="text-xl font-bold text-(--color-text) animate-fade-up" style={{ animationDelay: "200ms" }}>
            Great work!
          </p>
        </div>
      )}

      <style>{`
        @keyframes celebration-pop {
          0% { transform: scale(0); opacity: 0; }
          60% { transform: scale(1.1); opacity: 1; }
          100% { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </div>
  );
}
