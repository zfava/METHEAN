"use client";

import Button from "@/components/ui/Button";
import { MetheanMark } from "@/components/Brand";

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

function ShieldGlow() {
  return (
    <div
      className="relative w-20 h-20 mx-auto mb-6 rounded-full flex items-center justify-center animate-scale-in"
      style={{
        background: "radial-gradient(circle, rgba(198,162,78,0.15) 0%, rgba(198,162,78,0) 65%)",
      }}
    >
      <MetheanMark size={48} color="var(--color-brand-gold)" />
    </div>
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

  // ── End-of-day calm ──────────────────────────────────────────────
  if (allDone) {
    const completed = daySummary?.activitiesCompleted ?? 0;
    const subjects = daySummary?.subjectsPracticed ?? 0;
    const gains = daySummary?.masteryGains ?? [];
    return (
      <div className="text-center py-12 px-6 max-w-md mx-auto animate-scale-in">
        <ShieldGlow />
        <h2 className="text-[26px] font-semibold tracking-tight text-(--color-text) mb-2">
          Great work today{childName ? `, ${childName}` : ""}.
        </h2>
        {(completed > 0 || subjects > 0) && (
          <p className="text-sm text-(--color-text-secondary) mb-6">
            You completed {completed} {completed === 1 ? "activity" : "activities"}
            {subjects > 0 ? ` and practiced ${subjects} ${subjects === 1 ? "subject" : "subjects"}` : ""}.
          </p>
        )}

        {gains.length > 0 && (
          <div className="bg-(--color-surface) border border-(--color-border) rounded-[14px] px-4 py-3 mb-6 text-left animate-fade-up stagger-2">
            <div className="text-xs uppercase tracking-wide text-(--color-text-tertiary) mb-2">
              Mastery moved up
            </div>
            <ul className="space-y-1.5">
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
            </ul>
          </div>
        )}

        <Button onClick={onNext} variant="gold" size="lg" className="w-full max-w-xs mx-auto">
          See you tomorrow
        </Button>
      </div>
    );
  }

  // ── Single-activity completion (between-activity transition) ─────
  return (
    <div className="text-center py-12 px-6 max-w-md mx-auto animate-scale-in">
      {masteryChanged ? (
        <>
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
          <h2 className="text-[22px] font-semibold tracking-tight text-(--color-text) mb-1">
            {MASTERY_HEADINGS[masteryLevel || ""] || "Nice work"}
          </h2>
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-(--color-accent-light) text-(--color-accent) text-xs font-medium mb-3 animate-fade-up stagger-2">
            <span className="capitalize">{previousMastery?.replace(/_/g, " ")}</span>
            <span aria-hidden="true">→</span>
            <span className="capitalize font-semibold">{masteryLevel?.replace(/_/g, " ")}</span>
          </div>
          <p className="text-sm text-(--color-text-secondary) mb-1">{activityTitle}</p>
          <p className="text-xs text-(--color-text-tertiary) mb-8">
            Keep going — every step compounds.
          </p>
        </>
      ) : (
        <>
          <div className="w-14 h-14 mx-auto mb-5 rounded-full bg-(--color-success-light) flex items-center justify-center">
            <svg
              className="w-7 h-7 text-(--color-success)"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2.5}
              aria-hidden="true"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="text-[22px] font-semibold tracking-tight text-(--color-text) mb-2">
            Activity complete
          </h2>
          <p className="text-sm text-(--color-text-secondary) mb-1">{activityTitle}</p>
          {durationMinutes && durationMinutes > 0 && (
            <p className="text-xs text-(--color-text-tertiary) mb-6">{durationMinutes} minutes</p>
          )}
          {!durationMinutes && <div className="mb-6" />}
        </>
      )}

      <Button onClick={onNext} variant="primary" size="lg" className="w-full max-w-xs mx-auto">
        Next activity
      </Button>
    </div>
  );
}
