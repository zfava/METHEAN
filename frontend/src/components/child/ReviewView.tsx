"use client";

import { useState } from "react";
import type { LearningContext } from "@/lib/api";
import TutorChat from "./TutorChat";

interface ReviewViewProps {
  context: LearningContext;
  childId: string;
  onComplete: (data: { confidence: number; responses: Array<{ prompt: string; response: string }>; self_reflection: string }) => void;
}

export default function ReviewView({ context, childId, onComplete }: ReviewViewProps) {
  const [responses, setResponses] = useState<Record<number, string>>({});
  const [showTutor, setShowTutor] = useState(false);
  const [selfAssessment, setSelfAssessment] = useState<number | null>(null);
  const [phase, setPhase] = useState<"recall" | "reflect">("recall");

  const prompts = context.assessment.prompts?.length > 0
    ? context.assessment.prompts
    : context.lesson.key_questions || [];

  function handleSubmit() {
    onComplete({
      confidence: selfAssessment ?? 0.6,
      responses: prompts.map((p, i) => ({ prompt: p, response: responses[i] || "" })),
      self_reflection: "",
    });
  }

  return (
    <div className="max-w-2xl mx-auto py-6">
      {phase === "recall" && (
        <>
          <h1 className="text-3xl font-semibold text-(--color-text) mb-2">{context.activity.title}</h1>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-(--color-warning-light) text-(--color-warning) text-sm mb-4">
            Review · {context.activity.estimated_minutes} minutes
          </div>
          <p className="text-base text-(--color-text-secondary) mb-6">
            Let's see what you remember. Take your time and think carefully.
          </p>

          <div className="space-y-4 mb-6">
            {prompts.map((prompt, i) => (
              <div key={i} className="bg-(--color-surface) rounded-2xl p-5 border border-(--color-border)">
                <p className="text-base text-(--color-text) mb-3">{prompt}</p>
                <textarea
                  value={responses[i] || ""}
                  onChange={(e) => setResponses({ ...responses, [i]: e.target.value })}
                  placeholder="What do you remember?"
                  className="w-full h-20 px-4 py-3 text-base border border-(--color-border) rounded-2xl resize-none bg-(--color-page) text-(--color-text) focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20"
                />
              </div>
            ))}
          </div>

          <div className="flex items-center justify-between">
            {context.tutor_available && (
              <button onClick={() => setShowTutor(true)} className="text-sm text-(--color-accent) hover:underline">Ask your tutor</button>
            )}
            <button onClick={() => setPhase("reflect")}
              className="ml-auto py-3 px-8 text-base font-semibold text-white bg-(--color-accent) rounded-2xl hover:opacity-90 transition-opacity">
              Done
            </button>
          </div>
        </>
      )}

      {phase === "reflect" && (
        <>
          <h2 className="text-2xl font-semibold text-(--color-text) mb-6">How well do you remember this?</h2>
          <div className="space-y-3 mb-8">
            {[
              { label: "I remember it clearly", value: 0.9 },
              { label: "Some parts were fuzzy", value: 0.6 },
              { label: "I need to review again", value: 0.3 },
            ].map((opt) => (
              <button key={opt.value} onClick={() => setSelfAssessment(opt.value)}
                className={`w-full text-left px-5 py-4 rounded-2xl border-2 text-base font-medium transition-all ${selfAssessment === opt.value ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border) bg-(--color-surface)"}`}>
                {opt.label}
              </button>
            ))}
          </div>
          <button onClick={handleSubmit} disabled={selfAssessment === null}
            className="w-full py-4 text-lg font-semibold text-white bg-(--color-success) rounded-2xl hover:opacity-90 disabled:opacity-40 transition-opacity">
            Complete
          </button>
        </>
      )}

      {showTutor && <TutorChat activityId={context.activity.id} childId={childId} onClose={() => setShowTutor(false)} />}
    </div>
  );
}
