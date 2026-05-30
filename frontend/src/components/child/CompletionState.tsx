"use client";

import { motion } from "framer-motion";
import { useEffect } from "react";

import { MetheanMark } from "@/components/Brand";
import { useCelebration } from "@/lib/celebration/CelebrationDirector";
import { useMotion } from "@/lib/motion/MotionContext";
import { MOTION_DURATIONS_SEC, MOTION_EASINGS } from "@/lib/motion/tokens";
import { Check, TrendingUp } from "@/lib/icons";
import { Icon } from "@/components/ui/Icon";
import { formatMasteryState } from "@/lib/mastery";
import {
  AmbientField,
  MilestoneMoment,
  MotionButton,
  MotionCard,
  MotionText,
  Stagger,
} from "@/components/child/motion";
import { CompanionStage } from "@/components/companion/CompanionStage";

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

// Headline shown after an attempt that moves the kid up a rung.
// Stays tonal/celebratory rather than echoing the raw state name, which
// is rendered separately in the from -> to chip below the headline.
const MASTERY_HEADINGS: Record<string, string> = {
  mastered: "Mastered",
  proficient: "Confident now",
  developing: "Sticking",
  emerging: "Catching on",
  not_started: "First step",
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
  const { speed, reduceMotion } = useMotion();
  const celebration = useCelebration();

  // The CelebrationDirector is the single owner of celebration sound.
  // The day-complete moment (particles + day_complete cue + microcopy)
  // is dispatched here when the day's last activity finishes. The
  // mastery_up cue is owned by the dashboard-level trigger in
  // child/page.tsx, so this component no longer fires cues directly.
  useEffect(() => {
    if (allDone) {
      celebration.trigger({
        tier: "day_complete",
        microcopy: childName ? `Great work today, ${childName}` : "Great work today",
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [allDone]);

  // ── End-of-day milestone ──────────────────────────────────────────
  if (allDone) {
    const completed = daySummary?.activitiesCompleted ?? 0;
    const subjects = daySummary?.subjectsPracticed ?? 0;
    const gains = daySummary?.masteryGains ?? [];
    const dur = MOTION_DURATIONS_SEC.slow / speed;
    return (
      <MilestoneMoment trigger="end-of-day" muteCue>
        <div className="text-center py-12 px-6 max-w-md mx-auto relative">
          {/* The live companion is the centerpiece of the day-complete
              scene. The day_complete celebration trigger above puts it in
              its celebrate state as the scene mounts. */}
          <div className="relative mx-auto mb-8 flex items-center justify-center" style={{ width: 96, height: 110 }}>
            <CompanionStage size={96} />
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
                    <Icon icon={TrendingUp} size={14} className="text-(--color-success)" />
                    <span className="text-(--color-text)">{g.subject}</span>
                    <span className="text-(--color-text-tertiary) text-xs ml-auto">
                      <span>{formatMasteryState(g.from)}</span>
                      {" → "}
                      <span className="text-(--color-success) font-medium">
                        {formatMasteryState(g.to)}
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
                <Icon icon={Check} size={36} strokeWidth={2.5} className="text-(--color-success)" />
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
                    initial={{ opacity: 1 }}
                    animate={{ opacity: [1, 0, 1] }}
                    transition={{
                      duration: MOTION_DURATIONS_SEC.slow / speed,
                      ease: MOTION_EASINGS.composed,
                      delay: 0.4,
                      times: [0, 0.5, 1],
                    }}
                  >
                    {formatMasteryState(previousMastery)}
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
                  <span className="font-semibold">
                    {formatMasteryState(masteryLevel)}
                  </span>
                </motion.div>
              ) : (
                <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-(--color-accent-light) text-(--color-accent) text-xs font-medium mb-3">
                  <span>{formatMasteryState(previousMastery)}</span>
                  <span aria-hidden="true">→</span>
                  <span className="font-semibold">
                    {formatMasteryState(masteryLevel)}
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
