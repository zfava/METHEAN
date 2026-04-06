"use client";

import { useState } from "react";
import type { LearningContext } from "@/lib/api";

interface FieldTripViewProps {
  context: LearningContext;
  onComplete: (data: { confidence: number; responses: Array<{ prompt: string; response: string }>; self_reflection: string }) => void;
}

export default function FieldTripView({ context, onComplete }: FieldTripViewProps) {
  const [responses, setResponses] = useState<Record<string, string>>({});
  const [phase, setPhase] = useState<"prep" | "reflect">("prep");

  const reflectionPrompts = [
    "What did you observe?",
    "What was surprising?",
    "How does this connect to what you've been learning?",
  ];

  function handleSubmit() {
    onComplete({
      confidence: 0.7,
      responses: reflectionPrompts.map((p) => ({ prompt: p, response: responses[p] || "" })),
      self_reflection: responses["extra"] || "",
    });
  }

  return (
    <div className="max-w-2xl mx-auto py-6">
      {phase === "prep" && (
        <>
          <h1 className="text-3xl font-semibold text-(--color-text) mb-2">{context.activity.title}</h1>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-(--color-accent-light) text-(--color-accent) text-sm mb-6">
            Field Trip · {context.activity.estimated_minutes} minutes
          </div>

          {context.activity.description && (
            <div className="bg-(--color-surface) rounded-2xl p-6 border border-(--color-border) mb-6">
              <h3 className="text-sm font-semibold text-(--color-text-secondary) uppercase tracking-wider mb-2">Preparation</h3>
              <p className="text-base text-(--color-text) leading-relaxed whitespace-pre-line">{context.activity.description}</p>
            </div>
          )}

          {context.lesson.resources_needed?.length > 0 && (
            <div className="bg-(--color-warning-light) rounded-2xl p-5 mb-6">
              <h3 className="text-sm font-semibold text-(--color-warning) mb-1">What to bring</h3>
              <p className="text-sm text-(--color-text-secondary)">{context.lesson.resources_needed.join(", ")}</p>
            </div>
          )}

          {context.lesson.objectives?.length > 0 && (
            <div className="bg-(--color-accent-light) rounded-2xl p-5 mb-6">
              <h3 className="text-sm font-semibold text-(--color-accent) mb-1">What to look for</h3>
              <ul className="text-sm text-(--color-text) space-y-1">
                {context.lesson.objectives.map((obj, i) => <li key={i}>• {obj}</li>)}
              </ul>
            </div>
          )}

          <button onClick={() => setPhase("reflect")}
            className="w-full py-4 text-lg font-semibold text-white bg-(--color-accent) rounded-2xl hover:opacity-90 transition-opacity">
            I'm back — time to reflect
          </button>
        </>
      )}

      {phase === "reflect" && (
        <>
          <h2 className="text-2xl font-semibold text-(--color-text) mb-6">How was the field trip?</h2>

          <div className="space-y-4 mb-6">
            {reflectionPrompts.map((prompt) => (
              <div key={prompt} className="bg-(--color-surface) rounded-2xl p-5 border border-(--color-border)">
                <p className="text-base font-medium text-(--color-text) mb-2">{prompt}</p>
                <textarea
                  value={responses[prompt] || ""}
                  onChange={(e) => setResponses({ ...responses, [prompt]: e.target.value })}
                  placeholder="Write your thoughts..."
                  className="w-full h-20 px-4 py-3 text-base border border-(--color-border) rounded-2xl resize-none bg-(--color-page) text-(--color-text) focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20"
                />
              </div>
            ))}
          </div>

          <button onClick={handleSubmit}
            className="w-full py-4 text-lg font-semibold text-white bg-(--color-success) rounded-2xl hover:opacity-90 transition-opacity">
            Complete Field Trip
          </button>
        </>
      )}
    </div>
  );
}
