"use client";

interface CompletionStateProps {
  activityTitle: string;
  masteryLevel?: string;
  previousMastery?: string;
  onNext: () => void;
  allDone: boolean;
}

export default function CompletionState({
  activityTitle,
  masteryLevel,
  previousMastery,
  onNext,
  allDone,
}: CompletionStateProps) {
  const masteryChanged = masteryLevel && previousMastery && masteryLevel !== previousMastery;

  return (
    <div className="text-center py-12 px-6 max-w-md mx-auto">
      {/* Checkmark */}
      <div className="w-16 h-16 mx-auto mb-6 rounded-full bg-(--color-success-light) flex items-center justify-center">
        <svg className="w-8 h-8 text-(--color-success)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
        </svg>
      </div>

      <h2 className="text-2xl font-semibold text-(--color-text) mb-2">Activity Complete!</h2>
      <p className="text-base text-(--color-text-secondary) mb-6">{activityTitle}</p>

      {/* Mastery change */}
      {masteryChanged && (
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-2xl bg-(--color-accent-light) text-(--color-accent) text-sm font-medium mb-6">
          <span className="capitalize">{previousMastery?.replace("_", " ")}</span>
          <span>→</span>
          <span className="capitalize">{masteryLevel?.replace("_", " ")}</span>
        </div>
      )}

      <button
        onClick={onNext}
        className="w-full max-w-xs mx-auto py-4 text-base font-semibold text-white bg-(--color-success) rounded-2xl hover:opacity-90 transition-opacity"
      >
        {allDone ? "All Done for Today!" : "Next Activity"}
      </button>
    </div>
  );
}
