"use client";

import { motion } from "framer-motion";
import { useEffect } from "react";

import { MetheanMark } from "@/components/Brand";
import { useSoundCue } from "@/lib/useSoundCue";
import { useMotion } from "@/lib/motion/MotionContext";
import { MOTION_DURATIONS_SEC, MOTION_EASINGS } from "@/lib/motion/tokens";
import {
  AmbientField,
  MilestoneMoment,
  MotionButton,
  MotionCard,
  MotionText,
  ShieldDraw,
  Stagger,
} from "@/components/child/motion";

interface CompletionStateProps {
  activityTitle: string;
  masteryLevel?: string;
  previousMastery?: string;
  onNext: () => void;
  allDone: boolean;
  durationMinutes?: number;
  /** Child's first name for the warm "Great work today, X" message
   *  when the day is done. Optional so the older callsites still
   *  compile without it. */
  childName?: string;
  /** Counts displayed when allDone — replaces the confetti motif. */
  daySummary?: {
    activitiesCompleted: number;
    subjectsPracticed: number;
    masteryGains: Array<{ subject: string; from: string; to: string }>;
  };
}

const MASTERY_HEADINGS: Record<string, string> = {
  mastered: "Mastered",
  proficient: "Great progress",
  developing: "Building understanding",
  emerging: "Getting started",
};

/**
 * Soft halo around a node, used by single-activity completion. Stays
 * still under reduceMotion; otherwise blooms for 600ms then settles.
 */
function GlowHalo({ size = 80, color = "var(--color-success)" }: { size?: number; color?: string }) {
  const { reduceMotion, speed } = useMotion();
  if (reduceMotion) {
    return (
      <div
        className="relative mx-auto mb-6 rounded-full flex items-center justify-center"
        style={{
          width: size,
          height: size,
          background: `radial-gradient(circle, ${color}/20 0%, transparent 65%)`,
        }}
      />
    );
  }
  return (
    <motion.div
      className="relative mx-auto mb-6 rounded-full flex items-center justify-center"
      style={{
        width: size,
        height: size,
      }}
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: [0.8, 1.05, 1], opacity: [0, 1, 1] }}
      transition={{
        duration: MOTION_DURATIONS_SEC.slow / speed,
        ease: MOTION_EASINGS.cinematic,
        times: [0, 0.55, 1],
      }}
    >
      <motion.span
        aria-hidden="true"
        style={{
          position: "absolute",
          inset: 0,
          borderRadius: "9999px",
          background: `radial-gradient(circle, ${color} 0%, transparent 65%)`,
          opacity: 0.18,
        }}
        animate={{ opacity: [0.05, 0.28, 0.18] }}
        transition={{ duration: 0.6, ease: MOTION_EASINGS.composed }}
      />
    </motion.div>
  );
}

export default function CompletionState({
  activityTitle,
  masteryLevel,
  previousMastery,
  onNext,
  allDone,
  durationMinutes,
  childName,
  daySummary,
}: CompletionStateProps) {
  const masteryChanged = masteryLevel && previousMastery && masteryLevel !== previousMastery;
  const playCue = useSoundCue();
  const { speed, reduceMotion } = useMotion();

  // Activity-complete cue is fired by the parent screens via
  // playCue("activity_complete"); MilestoneMoment owns the day_complete
  // cue. For the masteryChanged branch we also fire the mastery cue
  // here so the cinematic-tier transitions get their dedicated sound.
  useEffect(() => {
    if (!allDone && masteryChanged) {
      playCue("mastery_up", { volume: 0.55 });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [allDone, masteryChanged]);

  // ── End-of-day milestone ──────────────────────────────────────────
  if (allDone) {
    const completed = daySummary?.activitiesCompleted ?? 0;
    const subjects = daySummary?.subjectsPracticed ?? 0;
    const gains = daySummary?.masteryGains ?? [];
    const dur = MOTION_DURATIONS_SEC.slow / speed;
    return (
      <MilestoneMoment trigger="end-of-day" soundCue="day_complete">
        <div className="text-center py-12 px-6 max-w-md mx-auto relative">
          {/* Soft brand ambient behind shield */}
          <div className="relative mx-auto mb-8" style={{ width: 96, height: 110 }}>
            <ShieldDraw size={96} color="var(--color-brand-gold)" />
          </div>

          <MotionText
            as="h2"
            weight
            entrance
            delay={0.6}
            className="type-heading-lg text-(--color-text) mb-3"
          >
            Great work today{childName ? `, ${childName}` : ""}.
          </MotionText>

          {(completed > 0 || subjects > 0) && (
            <motion.p
              initial={reduceMotion ? false : { opacity: 0, y: 6 }}
              animate={reduceMotion ? undefined : { opacity: 1, y: 0 }}
              transition={{ duration: dur, ease: MOTION_EASINGS.confident, delay: 1.1 }}
              className="text-sm text-(--color-text-secondary) mb-8"
            >
              You completed {completed} {completed === 1 ? "activity" : "activities"}
              {subjects > 0
                ? ` and practiced ${subjects} ${subjects === 1 ? "subject" : "subjects"}`
                : ""}
              .
            </motion.p>
          )}

          {gains.length > 0 && (
            <motion.div
              initial={reduceMotion ? false : { opacity: 0, y: 10 }}
              animate={reduceMotion ? undefined : { opacity: 1, y: 0 }}
              transition={{ duration: dur, ease: MOTION_EASINGS.confident, delay: 1.4 }}
              className="bg-(--color-surface) border border-(--color-border) rounded-[14px] px-4 py-3 mb-8 text-left shadow-[var(--shadow-card)]"
            >
              <div className="type-eyebrow-md text-(--color-text-tertiary) mb-2">
                Mastery moved up
              </div>
              <Stagger gap="generous" as="ul" className="space-y-1.5">
                {gains.map((g, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm">
                    <span className="text-(--color-success)" aria-hidden="true">↗</span>
                    <span className="text-(--color-text)">{g.subject}</span>
                    <span className="text-(--color-text-tertiary) text-xs ml-auto">
                      <span className="capitalize">{g.from.replace(/_/g, " ")}</span>
                      {" → "}
                      <span className="text-(--color-success) capitalize font-medium">
                        {g.to.replace(/_/g, " ")}
                      </span>
                    </span>
                  </li>
                ))}
              </Stagger>
            </motion.div>
          )}

          <motion.div
            initial={reduceMotion ? false : { opacity: 0, y: 8 }}
            animate={reduceMotion ? undefined : { opacity: 1, y: 0 }}
            transition={{ duration: dur, ease: MOTION_EASINGS.confident, delay: 2.0 }}
          >
            <MotionButton
              variant="gold"
              size="lg"
              onPress={onNext}
              className="w-full max-w-xs mx-auto"
            >
              See you tomorrow
            </MotionButton>
          </motion.div>
        </div>
      </MilestoneMoment>
    );
  }

  // ── Single-activity completion ────────────────────────────────────
  // Wrapped in a static ambient field so the page background stays
  // consistent with the dashboard surface. The card itself owns the
  // confident entrance.
  return (
    <div className="relative">
      <AmbientField mode="warm" intensity={0.7} />
      <div className="text-center py-12 px-6 max-w-md mx-auto relative">
        {masteryChanged ? (
          <>
            <GlowHalo color="var(--color-success)" />
            <MotionCard
              breathing={false}
              hoverLift={false}
              depth={0}
              className="bg-transparent"
            >
              <div className="w-16 h-16 mx-auto mb-5 rounded-full bg-(--color-success-light) flex items-center justify-center">
                <svg
                  className="w-9 h-9 text-(--color-success)"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2.5}
                  aria-hidden="true"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h2 className="type-heading-md text-(--color-text) mb-1">
                {MASTERY_HEADINGS[masteryLevel || ""] || "Nice work"}
              </h2>

              {/* Mastery pill grows in from the left after a 200ms beat. */}
              {!reduceMotion ? (
                <motion.div
                  className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-(--color-accent-light) text-(--color-accent) text-xs font-medium mb-3 overflow-hidden"
                  initial={{ opacity: 0, scaleX: 0.4, transformOrigin: "left center" }}
                  animate={{ opacity: 1, scaleX: 1 }}
                  transition={{
                    duration: MOTION_DURATIONS_SEC.slow / speed,
                    ease: MOTION_EASINGS.confident,
                    delay: 0.2,
                  }}
                >
                  <motion.span
                    className="capitalize"
                    initial={{ opacity: 1 }}
                    animate={{ opacity: [1, 0, 1] }}
                    transition={{
                      duration: MOTION_DURATIONS_SEC.slow / speed,
                      ease: MOTION_EASINGS.composed,
                      delay: 0.4,
                      times: [0, 0.5, 1],
                    }}
                  >
                    {previousMastery?.replace(/_/g, " ")}
                  </motion.span>
                  <motion.span aria-hidden="true"
                    initial={{ x: 0 }}
                    animate={{ x: [0, 4, 0] }}
                    transition={{
                      duration: MOTION_DURATIONS_SEC.slow / speed,
                      delay: 0.4,
                      ease: MOTION_EASINGS.composed,
                    }}
                  >
                    →
                  </motion.span>
                  <span className="capitalize font-semibold">
                    {masteryLevel?.replace(/_/g, " ")}
                  </span>
                </motion.div>
              ) : (
                <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-(--color-accent-light) text-(--color-accent) text-xs font-medium mb-3">
                  <span className="capitalize">{previousMastery?.replace(/_/g, " ")}</span>
                  <span aria-hidden="true">→</span>
                  <span className="capitalize font-semibold">
                    {masteryLevel?.replace(/_/g, " ")}
                  </span>
                </div>
              )}

              <p className="text-sm text-(--color-text-secondary) mb-1">{activityTitle}</p>
              <p className="text-xs text-(--color-text-tertiary) mb-8">
                Keep going — every step compounds.
              </p>
            </MotionCard>
          </>
        ) : (
          <MotionCard breathing={false} hoverLift={false} depth={0} className="bg-transparent">
            <GlowHalo size={72} color="var(--color-success)" />
            <h2 className="type-heading-md text-(--color-text) mb-2">
              Activity complete
            </h2>
            <p className="text-sm text-(--color-text-secondary) mb-1">{activityTitle}</p>
            {durationMinutes && durationMinutes > 0 && (
              <p className="text-xs text-(--color-text-tertiary) mb-6">{durationMinutes} minutes</p>
            )}
            {!durationMinutes && <div className="mb-6" />}
          </MotionCard>
        )}

        <MotionButton
          variant="primary"
          size="lg"
          onPress={onNext}
          className="w-full max-w-xs mx-auto"
        >
          Next activity
        </MotionButton>
      </div>
    </div>
  );
}
