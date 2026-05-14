"use client";

import { useEffect, useMemo, useRef, type ReactNode } from "react";

import type { Vibe } from "@/lib/personalization-types";

export interface WelcomeStepDef {
  id: string;
  label: string;
  /** Optional inline override of the vibe tokens applied to the
   *  shell. Used by the vibe step to give a live preview before
   *  the kid commits. */
  vibePreview?: Vibe | null;
}

interface WelcomeShellProps {
  steps: readonly WelcomeStepDef[];
  currentIndex: number;
  onBack: () => void;
  onSkipStep: () => void;
  onSkipAll: () => void;
  children: ReactNode;
}

/**
 * Layout chrome for the kid welcome flow.
 *
 * - Progress dots up top.
 * - "Back" button hidden on step 0.
 * - "Skip" advances without writing on the current step.
 * - "Skip the whole thing" jumps to /child via the parent's
 *   onSkipAll handler (which is responsible for setting
 *   onboarded:true so the kid lands in a stable state).
 * - Inline vibe preview: the parent route passes the vibe entry on
 *   the vibe step so the shell paints its own backdrop with that
 *   vibe's tokens. Other steps render the active vibe (provider).
 */
export function WelcomeShell({
  steps,
  currentIndex,
  onBack,
  onSkipStep,
  onSkipAll,
  children,
}: WelcomeShellProps) {
  const total = steps.length;
  const step = steps[currentIndex];
  const announceRef = useRef<HTMLDivElement>(null);

  // a11y: announce step changes for screen readers without
  // re-announcing on rerenders that don't change the index.
  useEffect(() => {
    if (announceRef.current) {
      announceRef.current.textContent = `Step ${currentIndex + 1} of ${total}: ${step.label}`;
    }
  }, [currentIndex, total, step.label]);

  const previewStyle = useMemo<React.CSSProperties | undefined>(() => {
    if (!step.vibePreview) return undefined;
    return step.vibePreview.tokens as React.CSSProperties;
  }, [step.vibePreview]);

  return (
    <div
      className="min-h-dvh flex flex-col bg-(--color-page) text-(--color-text)"
      style={previewStyle}
      data-welcome-step={step.id}
    >
      <div ref={announceRef} aria-live="polite" className="sr-only" />

      {/* Header: progress + actions */}
      <header className="flex items-center justify-between gap-3 px-5 pt-5 pb-3">
        <button
          type="button"
          onClick={onBack}
          disabled={currentIndex === 0}
          aria-label="Go back"
          className={[
            "min-h-[44px] min-w-[44px] inline-flex items-center justify-center rounded-full text-(--color-text-secondary)",
            currentIndex === 0 ? "opacity-0 pointer-events-none" : "hover:bg-(--color-surface)",
          ].join(" ")}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M15 18L9 12l6-6" />
          </svg>
        </button>

        <div className="flex items-center gap-1.5" role="presentation" aria-hidden="true">
          {steps.map((s, i) => (
            <span
              key={s.id}
              className={[
                "h-1.5 rounded-full transition-all",
                i === currentIndex ? "w-6 bg-(--color-text)" : "w-1.5 bg-(--color-border)",
              ].join(" ")}
            />
          ))}
        </div>

        <button
          type="button"
          onClick={onSkipAll}
          className="text-xs text-(--color-text-tertiary) hover:text-(--color-text) min-h-[44px] px-2"
        >
          Skip the whole thing
        </button>
      </header>

      {/* Body: the step content owns its own scroll */}
      <main className="flex-1 overflow-y-auto px-5 pb-10">
        <div className="max-w-md mx-auto py-4">{children}</div>
      </main>

      {/* Footer: skip current step. Hidden on the final ready
          screen since that one has its own primary action. */}
      {currentIndex < total - 1 && (
        <footer className="px-5 pb-5">
          <div className="max-w-md mx-auto flex justify-end">
            <button
              type="button"
              onClick={onSkipStep}
              className="text-sm text-(--color-text-secondary) hover:text-(--color-text) min-h-[44px] px-3"
            >
              Skip this step
            </button>
          </div>
        </footer>
      )}
    </div>
  );
}
