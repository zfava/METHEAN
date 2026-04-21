"use client";

import { useState } from "react";
import type { LearningContext } from "@/lib/api";
import TutorChat from "./TutorChat";

interface ReviewViewProps {
  context: LearningContext;
  childId: string;
  onComplete: (data: { confidence: number; responses: Array<{ prompt: string; response: string }>; self_reflection: string }) => void;
}

const EMOJI_SCALE = [
  { emoji: "\uD83D\uDE16", label: "I'm confused", value: 0.2 },
  { emoji: "\uD83E\uDD14", label: "Fuzzy", value: 0.4 },
  { emoji: "\uD83D\uDE10", label: "Sort of", value: 0.6 },
  { emoji: "\uD83D\uDE0A", label: "I remember", value: 0.8 },
  { emoji: "\uD83E\uDD29", label: "I totally get it", value: 0.95 },
];

export default function ReviewView({ context, childId, onComplete }: ReviewViewProps) {
  const [responses, setResponses] = useState<Record<number, string>>({});
  const [showTutor, setShowTutor] = useState(false);
  const [selfAssessment, setSelfAssessment] = useState<number | null>(null);
  const [phase, setPhase] = useState<"recall" | "reflect">("recall");
  const [currentPrompt, setCurrentPrompt] = useState(0);

  const prompts = context.assessment.prompts?.length > 0
    ? context.assessment.prompts
    : context.lesson.key_questions || [];

  // Last studied info from previous attempts
  const lastStudied = context.previous_attempts?.[0]?.date;
  const daysSince = lastStudied
    ? Math.round((Date.now() - new Date(lastStudied).getTime()) / 86400000)
    : null;

  function handleSubmit() {
    onComplete({
      confidence: selfAssessment ?? 0.6,
      responses: prompts.map((p, i) => ({ prompt: p, response: responses[i] || "" })),
      self_reflection: "",
    });
  }

  return (
    <div className="max-w-2xl mx-auto py-8">
      {phase === "recall" && (
        <>
          {/* Header with context */}
          <div className="text-center mb-8">
            <h1 className="text-2xl font-medium text-(--color-text) mb-2">Memory Check</h1>
            <p className="text-base text-(--color-text-secondary) leading-relaxed">
              {daysSince && daysSince > 0
                ? `You learned ${context.activity.title} ${daysSince === 1 ? "yesterday" : `${daysSince} days ago`}. Let's see what stuck.`
                : `Let's check what you remember about ${context.activity.title}.`}
            </p>
          </div>

          {/* Progress */}
          {prompts.length > 1 && (
            <div className="flex items-center gap-2 mb-6">
              <div className="flex-1 h-1 rounded-full bg-(--color-border)">
                <div className="h-full rounded-full bg-(--color-warning) transition-all"
                  style={{ width: `${((currentPrompt + 1) / prompts.length) * 100}%` }} />
              </div>
              <span className="text-xs text-(--color-text-tertiary)">{currentPrompt + 1} of {prompts.length}</span>
            </div>
          )}

          {/* One prompt at a time */}
          <div className="bg-(--color-surface) rounded-2xl p-6 border border-(--color-border) mb-6">
            <p className="text-lg text-(--color-text) leading-relaxed mb-4">{prompts[currentPrompt]}</p>
            <textarea
              value={responses[currentPrompt] || ""}
              onChange={(e) => setResponses({ ...responses, [currentPrompt]: e.target.value })}
              placeholder="What do you remember?"
              className="w-full h-24 px-4 py-3 text-base border border-(--color-border) rounded-2xl resize-none bg-(--color-page) text-(--color-text) focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20"
            />
          </div>

          <div className="flex items-center justify-between">
            <div className="flex gap-2">
              {currentPrompt > 0 && (
                <button onClick={() => setCurrentPrompt(p => p - 1)}
                  className="py-3 px-5 text-sm text-(--color-text-secondary) min-h-[44px]">&larr; Back</button>
              )}
              {context.tutor_available && (
                <button onClick={() => setShowTutor(true)}
                  className="py-3 px-5 text-sm text-(--color-accent) hover:underline min-h-[44px]">Need a hint?</button>
              )}
            </div>
            {currentPrompt < prompts.length - 1 ? (
              <button onClick={() => setCurrentPrompt(p => p + 1)}
                className="py-3 px-8 text-base font-medium text-white bg-(--color-accent) rounded-2xl min-h-[44px]">
                Next
              </button>
            ) : (
              <button onClick={() => setPhase("reflect")}
                className="py-3 px-8 text-base font-medium text-white bg-(--color-accent) rounded-2xl min-h-[44px]">
                Done
              </button>
            )}
          </div>
        </>
      )}

      {phase === "reflect" && (
        <div className="text-center">
          <h2 className="text-2xl font-medium text-(--color-text) mb-2">How well do you remember this?</h2>
          <p className="text-sm text-(--color-text-secondary) mb-8">Be honest — it helps us plan your next review.</p>

          <div className="flex justify-center gap-4 mb-10">
            {EMOJI_SCALE.map((opt) => (
              <button key={opt.value} onClick={() => setSelfAssessment(opt.value)}
                className={`flex flex-col items-center gap-1 p-3 rounded-2xl border-2 transition-all min-w-[64px] min-h-[80px] ${
                  selfAssessment === opt.value
                    ? "border-(--color-accent) bg-(--color-accent-light) scale-110"
                    : "border-(--color-border) bg-(--color-surface) hover:border-(--color-text-tertiary)"
                }`}
                aria-label={opt.label}>
                <span className="text-2xl">{opt.emoji}</span>
                <span className="text-[10px] text-(--color-text-secondary)">{opt.label}</span>
              </button>
            ))}
          </div>

          <button onClick={handleSubmit} disabled={selfAssessment === null}
            className="w-full py-4 text-lg font-medium text-white bg-(--color-success) rounded-2xl disabled:opacity-40 min-h-[52px]">
            Complete Review
          </button>
        </div>
      )}

      {showTutor && <TutorChat activityId={context.activity.id} childId={childId} onClose={() => setShowTutor(false)} />}
    </div>
  );
}
