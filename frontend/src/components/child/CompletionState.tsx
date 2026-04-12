"use client";

import Button from "@/components/ui/Button";

interface CompletionStateProps {
  activityTitle: string;
  masteryLevel?: string;
  previousMastery?: string;
  onNext: () => void;
  allDone: boolean;
  durationMinutes?: number;
}

const MASTERY_HEADINGS: Record<string, string> = {
  mastered: "Mastered! 🎯",
  proficient: "Great progress!",
  developing: "Building understanding!",
  emerging: "Getting started!",
};

export default function CompletionState({
  activityTitle, masteryLevel, previousMastery, onNext, allDone, durationMinutes,
}: CompletionStateProps) {
  const masteryChanged = masteryLevel && previousMastery && masteryLevel !== previousMastery;

  return (
    <div className="text-center py-12 px-6 max-w-md mx-auto">
      {masteryChanged ? (
        <>
          {/* Celebration circle */}
          <div className="relative w-20 h-20 mx-auto mb-6">
            <div className="w-20 h-20 rounded-full bg-(--color-success-light) flex items-center justify-center"
              style={{ animation: "celebration-pop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards" }}>
              <svg className="w-10 h-10 text-(--color-success)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            {/* Confetti dots */}
            {[0, 1, 2, 3, 4, 5, 6, 7].map((i) => (
              <span key={i} className="absolute rounded-full"
                style={{
                  width: 6 + (i % 3) * 2,
                  height: 6 + (i % 3) * 2,
                  top: "50%", left: "50%",
                  background: ["var(--color-success)", "var(--color-accent)", "var(--gold)", "var(--color-warning)"][i % 4],
                  animation: `confetti-burst 0.6s ${0.1 + i * 0.05}s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards`,
                  opacity: 0,
                  transform: `translate(-50%, -50%)`,
                  ["--confetti-x" as any]: `${Math.cos((i / 8) * Math.PI * 2) * 50}px`,
                  ["--confetti-y" as any]: `${Math.sin((i / 8) * Math.PI * 2) * 50}px`,
                }} />
            ))}
          </div>

          {/* Mastery heading */}
          <h2 className="text-2xl font-semibold text-(--color-text) mb-1">
            {MASTERY_HEADINGS[masteryLevel || ""] || "Nice work!"}
          </h2>

          {/* Mastery badge slides up */}
          <div className="inline-flex items-center gap-2 px-5 py-2.5 rounded-2xl bg-(--color-accent-light) text-(--color-accent) text-sm font-medium mb-2"
            style={{ animation: "slide-up-fade 0.3s 0.2s ease-out forwards", opacity: 0, transform: "translateY(10px)" }}>
            <span className="capitalize">{previousMastery?.replace(/_/g, " ")}</span>
            <span>→</span>
            <span className="capitalize font-bold">{masteryLevel?.replace(/_/g, " ")}</span>
          </div>

          <p className="text-sm text-(--color-text-secondary) mb-1">{activityTitle}</p>
          <p className="text-xs text-(--color-text-tertiary) mb-8">Keep going, you&apos;re building something amazing.</p>
        </>
      ) : (
        <>
          {/* Simple completion */}
          <div className="w-16 h-16 mx-auto mb-6 rounded-full bg-(--color-success-light) flex items-center justify-center"
            style={{ animation: "celebration-pop 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) forwards" }}>
            <svg className="w-8 h-8 text-(--color-success)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="text-2xl font-semibold text-(--color-text) mb-2">Activity Complete!</h2>
          <p className="text-sm text-(--color-text-secondary) mb-1">{activityTitle}</p>
          {durationMinutes && durationMinutes > 0 && (
            <p className="text-xs text-(--color-text-tertiary) mb-6">{durationMinutes} minutes</p>
          )}
          {!durationMinutes && <div className="mb-6" />}
        </>
      )}

      <Button onClick={onNext} variant={allDone ? "gold" : "primary"} size="lg" className="w-full max-w-xs mx-auto">
        {allDone ? "All Done for Today! ✨" : "Next Activity →"}
      </Button>

      {/* CSS keyframes */}
      <style>{`
        @keyframes celebration-pop {
          from { transform: scale(0); opacity: 0; }
          to { transform: scale(1); opacity: 1; }
        }
        @keyframes slide-up-fade {
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes confetti-burst {
          0% { opacity: 1; transform: translate(-50%, -50%) scale(0); }
          60% { opacity: 1; transform: translate(calc(-50% + var(--confetti-x)), calc(-50% + var(--confetti-y))) scale(1); }
          100% { opacity: 0; transform: translate(calc(-50% + var(--confetti-x) * 1.3), calc(-50% + var(--confetti-y) * 1.3)) scale(0.5); }
        }
      `}</style>
    </div>
  );
}
