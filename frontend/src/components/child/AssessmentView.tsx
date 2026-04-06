"use client";

import { useState } from "react";
import type { LearningContext } from "@/lib/api";

interface AssessmentViewProps {
  context: LearningContext;
  onComplete: (data: { confidence: number; responses: Array<{ prompt: string; response: string }>; self_reflection: string }) => void;
}

export default function AssessmentView({ context, onComplete }: AssessmentViewProps) {
  const [responses, setResponses] = useState<Record<number, string>>({});
  const [currentPrompt, setCurrentPrompt] = useState(0);

  const prompts = context.assessment.prompts || [];

  function handleSubmit() {
    onComplete({
      confidence: 0.7,  // Assessments don't use self-assessment
      responses: prompts.map((p, i) => ({ prompt: p, response: responses[i] || "" })),
      self_reflection: "",
    });
  }

  return (
    <div className="max-w-2xl mx-auto py-6">
      <h1 className="text-3xl font-semibold text-(--color-text) mb-2">{context.activity.title}</h1>
      <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-(--color-constitutional-light) text-(--color-constitutional) text-sm mb-2">
        Assessment · {context.activity.estimated_minutes} minutes
      </div>
      <p className="text-sm text-(--color-text-tertiary) mb-8">
        Take your time and do your best. Your parent will review your work.
      </p>

      {prompts.length > 0 ? (
        <>
          {/* Progress */}
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm text-(--color-text-secondary)">Question {currentPrompt + 1} of {prompts.length}</span>
            <div className="w-32 h-1.5 rounded-full bg-(--color-border)">
              <div className="h-full rounded-full bg-(--color-constitutional) transition-all" style={{ width: `${((currentPrompt + 1) / prompts.length) * 100}%` }} />
            </div>
          </div>

          <div className="bg-(--color-surface) rounded-2xl p-6 border border-(--color-border) mb-6">
            <p className="text-lg text-(--color-text) mb-4">{prompts[currentPrompt]}</p>
            <textarea
              value={responses[currentPrompt] || ""}
              onChange={(e) => setResponses({ ...responses, [currentPrompt]: e.target.value })}
              placeholder="Write your answer here..."
              className="w-full h-32 px-4 py-3 text-base border border-(--color-border) rounded-2xl resize-none bg-(--color-page) text-(--color-text) focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20"
            />
          </div>

          {currentPrompt < prompts.length - 1 ? (
            <button onClick={() => setCurrentPrompt(currentPrompt + 1)}
              className="w-full py-4 text-base font-semibold text-white bg-(--color-accent) rounded-2xl hover:opacity-90 transition-opacity">
              Next Question
            </button>
          ) : (
            <button onClick={handleSubmit}
              className="w-full py-4 text-lg font-semibold text-white bg-(--color-success) rounded-2xl hover:opacity-90 transition-opacity">
              Submit Assessment
            </button>
          )}
        </>
      ) : (
        <>
          <div className="bg-(--color-surface) rounded-2xl p-6 border border-(--color-border) mb-6">
            <p className="text-base text-(--color-text) mb-4">{context.activity.description || "Complete this assessment activity."}</p>
            <textarea
              value={responses[0] || ""}
              onChange={(e) => setResponses({ ...responses, 0: e.target.value })}
              placeholder="Write your response..."
              className="w-full h-32 px-4 py-3 text-base border border-(--color-border) rounded-2xl resize-none bg-(--color-page) text-(--color-text) focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20"
            />
          </div>
          <button onClick={handleSubmit}
            className="w-full py-4 text-lg font-semibold text-white bg-(--color-success) rounded-2xl hover:opacity-90 transition-opacity">
            Submit Assessment
          </button>
        </>
      )}
    </div>
  );
}
