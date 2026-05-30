"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";

// Companion state machine. The companion feels alive by moving between a
// small set of expressive states. Transitions are guarded by a priority +
// hold + debounce model so rapid event flapping (correct, incorrect,
// correct within a couple seconds) never causes a visual seizure.

export type CompanionState =
  | "idle" // resting default
  | "focus" // an activity is active; companion attends
  | "celebrate" // correct / mastery_up / activity_complete fired
  | "commiserate" // incorrect or struggling
  | "surprised" // unexpected event (e.g. a skipped mastery level)
  | "thinking" // mid-activity contemplation
  | "sleep"; // idle 5+ minutes

export type CompanionEvent =
  | "user_active"
  | "user_idle"
  | "activity_start"
  | "activity_complete"
  | "activity_end"
  | "correct"
  | "incorrect"
  | "mastery_up"
  | "surprised"
  | "thinking_start"
  | "thinking_end";

interface SetStateOpts {
  /** Minimum time (ms) the state is held before a same-or-lower priority
   *  transition is allowed to replace it. */
  holdMs?: number;
  /** Priority 0-4. Higher preempts during a hold. */
  priority?: number;
}

export interface CompanionContextValue {
  state: CompanionState;
  /** True after ~30s of inactivity (pre-sleep). Drives sleepy eyes
   *  without occupying a discrete state slot. */
  drowsy: boolean;
  setState: (s: CompanionState, opts?: SetStateOpts) => void;
  trackEvent: (event: CompanionEvent) => void;
}

const CompanionContext = createContext<CompanionContextValue>({
  state: "idle",
  drowsy: false,
  setState: () => {},
  trackEvent: () => {},
});

// Priority ladder. Sleep sits low here, but is special-cased: once asleep,
// only user_active can wake it (see trackEvent).
const PRIORITY: Record<CompanionState, number> = {
  sleep: 0,
  idle: 0,
  focus: 1,
  thinking: 1,
  commiserate: 2,
  surprised: 3,
  celebrate: 4,
};

const HOLD_MS: Partial<Record<CompanionState, number>> = {
  celebrate: 1500,
  commiserate: 800,
  surprised: 900,
};

const DEBOUNCE_MS = 200;
const IDLE_MS = 30_000; // 30s -> sleepy
const SLEEP_MS = 300_000; // 5min -> asleep

export function CompanionProvider({ children }: { children: ReactNode }) {
  const [state, setStateRaw] = useState<CompanionState>("idle");
  const [drowsy, setDrowsy] = useState(false);

  // Mutable scheduling refs (no re-render churn).
  const currentRef = useRef<CompanionState>("idle");
  const holdUntilRef = useRef<number>(0);
  const holdPriorityRef = useRef<number>(0);
  // Debounce window: keep the highest-priority request seen within 200ms.
  const pendingRef = useRef<{ s: CompanionState; priority: number; holdMs: number } | null>(null);
  const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  // The "real" base state to fall back to (focus when an activity is open,
  // else idle) once a transient hold expires.
  const baseRef = useRef<CompanionState>("idle");

  const commit = useCallback((s: CompanionState, holdMs: number, priority: number) => {
    currentRef.current = s;
    holdUntilRef.current = holdMs > 0 ? Date.now() + holdMs : 0;
    holdPriorityRef.current = priority;
    setStateRaw(s);
  }, []);

  const setState = useCallback(
    (s: CompanionState, opts?: SetStateOpts) => {
      const priority = opts?.priority ?? PRIORITY[s];
      const holdMs = opts?.holdMs ?? HOLD_MS[s] ?? 0;

      // Sleep can only be left via user_active (handled in trackEvent); a
      // lower/equal priority request cannot disturb it.
      if (currentRef.current === "sleep" && priority <= PRIORITY.sleep) return;

      // Respect an active hold unless we strictly outrank it.
      const now = Date.now();
      if (now < holdUntilRef.current && priority <= holdPriorityRef.current) {
        return;
      }

      // Debounce: collapse a burst of requests, keeping the highest priority.
      const pending = pendingRef.current;
      if (!pending || priority >= pending.priority) {
        pendingRef.current = { s, priority, holdMs };
      }
      if (debounceTimerRef.current) return;
      debounceTimerRef.current = setTimeout(() => {
        debounceTimerRef.current = null;
        const p = pendingRef.current;
        pendingRef.current = null;
        if (p) commit(p.s, p.holdMs, p.priority);
      }, DEBOUNCE_MS);
    },
    [commit],
  );

  // Resolve the base resting state once transient holds end.
  const settleToBase = useCallback(() => {
    if (Date.now() < holdUntilRef.current) return;
    setState(baseRef.current, { priority: PRIORITY[baseRef.current] });
  }, [setState]);

  const trackEvent = useCallback(
    (event: CompanionEvent) => {
      switch (event) {
        case "user_active":
          setDrowsy(false);
          // Any input wakes from sleep and returns to the real base state.
          if (currentRef.current === "sleep") {
            commit(baseRef.current, 0, PRIORITY[baseRef.current]);
          }
          return;
        case "user_idle":
          // Sleepy eyes: only from a resting/attending state. The 30s mark
          // does not change the discrete state; the 5min sleep timer does.
          if (currentRef.current === "idle" || currentRef.current === "focus") {
            setDrowsy(true);
          }
          return;
        case "activity_start":
          setDrowsy(false);
          baseRef.current = "focus";
          setState("focus", { priority: 1 });
          return;
        case "activity_complete":
          setState("celebrate");
          return;
        case "activity_end":
          // Activity closed: return to the resting idle baseline.
          baseRef.current = "idle";
          setState("idle", { priority: 0 });
          return;
        case "correct":
          setState("celebrate");
          return;
        case "mastery_up":
          setState("celebrate");
          return;
        case "incorrect":
          setState("commiserate");
          return;
        case "surprised":
          setState("surprised");
          return;
        case "thinking_start":
          baseRef.current = "focus";
          setState("thinking", { priority: 1 });
          return;
        case "thinking_end":
          baseRef.current = "focus";
          settleToBase();
          return;
        default:
          return;
      }
    },
    [setState, settleToBase, commit],
  );

  // After a transient hold (celebrate / commiserate / surprised) expires,
  // settle back to the base resting state.
  useEffect(() => {
    if (state !== "celebrate" && state !== "commiserate" && state !== "surprised") return;
    const hold = HOLD_MS[state] ?? 0;
    const t = setTimeout(() => settleToBase(), hold + 30);
    return () => clearTimeout(t);
  }, [state, settleToBase]);

  // Idle / sleep timers, reset on any input.
  useEffect(() => {
    if (typeof window === "undefined") return;
    let idleTimer: ReturnType<typeof setTimeout> | null = null;
    let sleepTimer: ReturnType<typeof setTimeout> | null = null;

    const clear = () => {
      if (idleTimer) clearTimeout(idleTimer);
      if (sleepTimer) clearTimeout(sleepTimer);
    };
    const arm = () => {
      clear();
      idleTimer = setTimeout(() => trackEvent("user_idle"), IDLE_MS);
      sleepTimer = setTimeout(() => {
        // Sleep only from a resting/attending state, never mid-celebration.
        if (currentRef.current !== "celebrate" && currentRef.current !== "commiserate") {
          setDrowsy(false);
          commit("sleep", 0, PRIORITY.sleep);
        }
      }, SLEEP_MS);
    };
    const onInput = () => {
      trackEvent("user_active");
      arm();
    };

    window.addEventListener("pointerdown", onInput);
    window.addEventListener("keydown", onInput);
    window.addEventListener("touchstart", onInput, { passive: true });
    window.addEventListener("pointermove", onInput, { passive: true });
    arm();
    return () => {
      clear();
      window.removeEventListener("pointerdown", onInput);
      window.removeEventListener("keydown", onInput);
      window.removeEventListener("touchstart", onInput);
      window.removeEventListener("pointermove", onInput);
    };
  }, [trackEvent, commit]);

  // Celebrate when Prompt 3 fires its window event.
  useEffect(() => {
    if (typeof window === "undefined") return;
    const onCelebration = () => setState("celebrate");
    window.addEventListener("metheanCelebration", onCelebration as EventListener);
    return () => window.removeEventListener("metheanCelebration", onCelebration as EventListener);
  }, [setState]);

  const value = useMemo<CompanionContextValue>(
    () => ({ state, drowsy, setState, trackEvent }),
    [state, drowsy, setState, trackEvent],
  );

  return <CompanionContext.Provider value={value}>{children}</CompanionContext.Provider>;
}

export function useCompanionState(): CompanionContextValue {
  return useContext(CompanionContext);
}
