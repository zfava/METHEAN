"use client";

import { useState } from "react";
import type { LearningContext } from "@/lib/api";
import TutorChat from "./TutorChat";

interface PracticeViewProps {
  context: LearningContext;
  childId: string;
  onComplete: (data: { confidence: number; responses: Array<{ prompt: string; response: string }>; self_reflection: string }) => void;
}

export default function PracticeView({ context, childId, onComplete }: PracticeViewProps) {
  const [responses, setResponses] = useState<Record<number, string>>({});
  const [showTutor, setShowTutor] = useState(false);
  const [selfAssessment, setSelfAssessment] = useState<number | null>(null);
  const [phase, setPhase] = useState<"work" | "reflect">("work");

  const prompts = context.lesson.practice_prompts || [];

  function handleSubmit() {
    onComplete({
      confidence: selfAssessment ?? 0.6,
      responses: prompts.map((p, i) => ({ prompt: p, response: responses[i] || "" })),
      self_reflection: "",
    });
  }

  return (
    <div className="max-w-2xl mx-auto py-6">
      {phase === "work" && (
        <>
          <h1 className="text-3xl font-semibold text-(--color-text) mb-2">{context.activity.title}</h1>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-(--color-success-light) text-(--color-success) text-sm mb-6">
            Practice · {context.activity.estimated_minutes} minutes
          </div>

          {context.activity.description && (
            <p className="text-base text-(--color-text-secondary) mb-6">{context.activity.description}</p>
          )}

          <div className="space-y-4 mb-6">
            {prompts.length > 0 ? prompts.map((prompt, i) => (
              <div key={i} className="bg-(--color-surface) rounded-2xl p-5 border border-(--color-border)">
                <p className="text-base text-(--color-text) mb-3">{prompt}</p>
                <textarea
                  value={responses[i] || ""}
                  onChange={(e) => setResponses({ ...responses, [i]: e.target.value })}
                  placeholder="Your answer..."
                  className="w-full h-20 px-4 py-3 text-base border border-(--color-border) rounded-2xl resize-none bg-(--color-page) text-(--color-text) focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20"
                />
              </div>
            )) : (
              <div className="bg-(--color-surface) rounded-2xl p-5 border border-(--color-border)">
                <p className="text-base text-(--color-text) mb-3">Complete this practice activity, then mark it done below.</p>
              </div>
            )}
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
          <h2 className="text-2xl font-semibold text-(--color-text) mb-6">How did the practice go?</h2>
          <div className="space-y-3 mb-8">
            {[
              { label: "I've got this!", value: 0.9 },
              { label: "I'm getting better", value: 0.6 },
              { label: "I need more practice", value: 0.3 },
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
