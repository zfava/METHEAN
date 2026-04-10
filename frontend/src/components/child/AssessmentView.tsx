"use client";

import { useState, useEffect, useRef } from "react";
import type { LearningContext } from "@/lib/api";

interface AssessmentItem {
  prompt: string;
  type: string;
  correct_answer?: string;
  options?: string[];
  rubric?: string;
  target_concept?: string;
}

interface AssessmentViewProps {
  context: LearningContext;
  onComplete: (data: { confidence: number; responses: Array<{ prompt: string; response: string }>; self_reflection: string }) => void;
}

export default function AssessmentView({ context, onComplete }: AssessmentViewProps) {
  const items: AssessmentItem[] = (context as any).assessment?.items || context.assessment?.prompts?.map((p: string) => ({ prompt: p, type: "open_response" })) || [];
  const [responses, setResponses] = useState<Record<number, string>>({});
  const [elapsed, setElapsed] = useState(0);
  const [submitted, setSubmitted] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const totalItems = items.length;
  const answeredCount = Object.values(responses).filter((r) => r.trim().length > 0).length;
  const estimatedMinutes = context.activity.estimated_minutes || 30;

  useEffect(() => {
    timerRef.current = setInterval(() => setElapsed((e) => e + 1), 1000);
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, []);

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  function handleSubmit() {
    if (timerRef.current) clearInterval(timerRef.current);
    setSubmitted(true);
    const durationMinutes = Math.round(elapsed / 60);
    onComplete({
      confidence: 0.7,
      responses: items.map((item, i) => ({ prompt: item.prompt, response: responses[i] || "" })),
      self_reflection: `Completed in ${durationMinutes} minutes. Answered ${answeredCount} of ${totalItems} items.`,
    });
  }

  if (submitted) {
    return (
      <div className="max-w-2xl mx-auto py-6 text-center">
        <div className="text-4xl mb-3">📝</div>
        <h1 className="text-2xl font-semibold text-(--color-text) mb-2">Assessment Submitted</h1>
        <p className="text-(--color-text-secondary)">Your work has been submitted for evaluation. Results will be available after review.</p>
        <p className="text-sm text-(--color-text-tertiary) mt-2">Time: {formatTime(elapsed)} · {answeredCount}/{totalItems} answered</p>
      </div>
    );
  }

  if (totalItems === 0) {
    return (
      <div className="max-w-2xl mx-auto py-6">
        <h1 className="text-2xl font-semibold text-(--color-text) mb-4">{context.activity.title}</h1>
        <div className="bg-(--color-surface) border border-(--color-border) rounded-xl p-6 text-center">
          <p className="text-(--color-text-secondary)">No assessment items available yet. Content is being generated.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto py-6">
      {/* Header with timer */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-xl font-semibold text-(--color-text)">{context.activity.title}</h1>
          <div className="text-sm text-(--color-text-tertiary)">Assessment · {estimatedMinutes} minutes suggested</div>
        </div>
        <div className={`font-mono text-lg px-3 py-1 rounded-lg ${elapsed > estimatedMinutes * 60 ? "bg-(--color-warning-light) text-(--color-warning)" : "bg-(--color-surface) text-(--color-text-secondary)"}`}>
          {formatTime(elapsed)}
        </div>
      </div>

      {/* Progress indicator */}
      <div className="flex items-center gap-2 mb-6">
        <div className="w-full h-1.5 bg-(--color-border) rounded-full overflow-hidden">
          <div className="h-full bg-(--color-accent) rounded-full transition-all duration-300" style={{ width: `${(answeredCount / totalItems) * 100}%` }} />
        </div>
        <span className="text-xs text-(--color-text-tertiary) whitespace-nowrap">{answeredCount}/{totalItems}</span>
      </div>

      {/* All items */}
      <div className="space-y-6">
        {items.map((item, idx) => (
          <div key={idx} className="bg-(--color-surface) border border-(--color-border) rounded-xl p-5">
            <div className="flex items-start justify-between mb-3">
              <span className="text-xs font-medium text-(--color-text-tertiary)">Question {idx + 1}</span>
              {item.target_concept && <span className="text-[10px] px-2 py-0.5 rounded-full bg-(--color-border) text-(--color-text-tertiary)">{item.target_concept}</span>}
            </div>
            <p className="text-(--color-text) mb-3">{item.prompt}</p>

            {item.type === "number" && (
              <input type="number" value={responses[idx] || ""} onChange={(e) => setResponses((r) => ({ ...r, [idx]: e.target.value }))} placeholder="Your answer..." className="w-full px-4 py-2 rounded-lg border border-(--color-border) bg-(--color-surface) text-(--color-text) focus:outline-none focus:border-(--color-accent)" />
            )}
            {item.type === "multiple_choice" && item.options && (
              <div className="space-y-2">
                {item.options.map((opt, oi) => (
                  <button key={oi} onClick={() => setResponses((r) => ({ ...r, [idx]: opt }))} className={`w-full text-left px-3 py-2 rounded-lg border text-sm transition-colors ${responses[idx] === opt ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border) hover:border-(--color-text-tertiary)"}`}>
                    {String.fromCharCode(65 + oi)}. {opt}
                  </button>
                ))}
              </div>
            )}
            {item.type === "true_false" && (
              <div className="flex gap-3">
                {["True", "False"].map((tf) => (
                  <button key={tf} onClick={() => setResponses((r) => ({ ...r, [idx]: tf }))} className={`flex-1 py-2 rounded-lg border font-medium text-sm transition-colors ${responses[idx] === tf ? "border-(--color-accent) bg-(--color-accent-light) text-(--color-accent)" : "border-(--color-border) text-(--color-text-secondary)"}`}>
                    {tf}
                  </button>
                ))}
              </div>
            )}
            {(item.type === "open_response" || item.type === "text" || !item.type) && (
              <textarea value={responses[idx] || ""} onChange={(e) => setResponses((r) => ({ ...r, [idx]: e.target.value }))} placeholder="Write your answer..." rows={4} className="w-full px-4 py-2 rounded-lg border border-(--color-border) bg-(--color-surface) text-(--color-text) focus:outline-none focus:border-(--color-accent) resize-none text-sm" />
            )}
          </div>
        ))}
      </div>

      {/* Submit area */}
      <div className="mt-8 sticky bottom-4">
        {!showConfirm ? (
          <button onClick={() => setShowConfirm(true)} className="w-full py-3 rounded-xl bg-(--color-constitutional) text-white font-medium hover:opacity-90 transition-opacity">
            Submit Assessment
          </button>
        ) : (
          <div className="bg-(--color-surface) border border-(--color-constitutional)/30 rounded-xl p-4">
            <p className="text-(--color-text) text-sm mb-3">You answered {answeredCount} of {totalItems} questions. {answeredCount < totalItems && <span className="text-(--color-warning)">Some questions are unanswered.</span>} Submit your assessment?</p>
            <div className="flex gap-3">
              <button onClick={handleSubmit} className="flex-1 py-2 rounded-lg bg-(--color-constitutional) text-white font-medium hover:opacity-90 transition-opacity">
                Yes, Submit
              </button>
              <button onClick={() => setShowConfirm(false)} className="flex-1 py-2 rounded-lg border border-(--color-border) text-(--color-text-secondary) hover:bg-(--color-page) transition-colors">
                Go Back
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
