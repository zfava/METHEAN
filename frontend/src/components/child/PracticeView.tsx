"use client";

import { useState, useCallback } from "react";
import type { LearningContext } from "@/lib/api";
import TutorChat from "./TutorChat";

interface PracticeItem {
  type: string;
  difficulty: number;
  prompt: string;
  expected_type: string;
  correct_answer?: string;
  hints?: string[];
  explanation?: string;
  options?: string[];
}

interface PracticeViewProps {
  context: LearningContext;
  childId: string;
  onComplete: (data: { confidence: number; responses: Array<{ prompt: string; response: string }>; self_reflection: string }) => void;
}

export default function PracticeView({ context, childId, onComplete }: PracticeViewProps) {
  const items: PracticeItem[] = (context as any).practice?.items || context.lesson?.practice_prompts?.map((p: string) => ({ type: "prompt", difficulty: 1, prompt: p, expected_type: "text" })) || [];
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answer, setAnswer] = useState("");
  const [checked, setChecked] = useState(false);
  const [correct, setCorrect] = useState(false);
  const [showHint, setShowHint] = useState(0);
  const [showTutor, setShowTutor] = useState(false);
  const [results, setResults] = useState<Array<{ prompt: string; response: string; correct: boolean | null }>>([]);
  const [phase, setPhase] = useState<"work" | "summary">("work");

  const item = items[currentIdx];
  const totalItems = items.length;

  const checkAnswer = useCallback(() => {
    if (!item) return;
    const isAutoCheck = ["number", "multiple_choice", "true_false"].includes(item.expected_type);
    let isCorrect = false;
    if (isAutoCheck && item.correct_answer) {
      const norm = (s: string) => s.toString().trim().toLowerCase().replace(/\s+/g, " ");
      isCorrect = norm(answer) === norm(item.correct_answer);
    }
    setChecked(true);
    setCorrect(isCorrect);
    setResults((prev) => [...prev, { prompt: item.prompt, response: answer, correct: isAutoCheck ? isCorrect : null }]);
  }, [item, answer]);

  const nextItem = useCallback(() => {
    if (currentIdx + 1 >= totalItems) {
      setPhase("summary");
      return;
    }
    setCurrentIdx((i) => i + 1);
    setAnswer("");
    setChecked(false);
    setCorrect(false);
    setShowHint(0);
  }, [currentIdx, totalItems]);

  const handleFinish = useCallback(() => {
    const correctCount = results.filter((r) => r.correct === true).length;
    const confidence = totalItems > 0 ? Math.min(0.95, 0.3 + (correctCount / totalItems) * 0.6) : 0.6;
    onComplete({
      confidence,
      responses: results.map((r) => ({ prompt: r.prompt, response: r.response })),
      self_reflection: `${correctCount}/${totalItems} correct`,
    });
  }, [results, totalItems, onComplete]);

  if (totalItems === 0) {
    return (
      <div className="max-w-2xl mx-auto py-6">
        <h1 className="text-2xl font-semibold text-(--color-text) mb-4">{context.activity.title}</h1>
        <div className="bg-(--color-surface) border border-(--color-border) rounded-xl p-6 text-center">
          <p className="text-(--color-text-secondary) mb-4">No practice items available for this activity yet.</p>
          <p className="text-sm text-(--color-text-tertiary)">Content is being generated. Try again in a few minutes.</p>
        </div>
      </div>
    );
  }

  if (phase === "summary") {
    const correctCount = results.filter((r) => r.correct === true).length;
    const openCount = results.filter((r) => r.correct === null).length;
    return (
      <div className="max-w-2xl mx-auto py-6">
        <h1 className="text-2xl font-medium text-(--color-text) mb-2">Practice Complete</h1>
        {/* Encouragement based on performance */}
        <p className="text-base text-(--color-text-secondary) mb-4 italic">
          {correctCount === totalItems ? "Perfect score. You clearly know this material."
            : correctCount >= totalItems * 0.7 ? "Strong work. You're building real understanding."
            : "Good effort. Every practice session makes you stronger."}
        </p>
        <div className="bg-(--color-surface) border border-(--color-border) rounded-2xl p-6 mb-4">
          <div className="flex items-center gap-6 mb-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-(--color-success)">{correctCount}</div>
              <div className="text-xs text-(--color-text-tertiary)">Correct</div>
            </div>
            {totalItems - correctCount - openCount > 0 && (
              <div className="text-center">
                <div className="text-3xl font-bold text-(--color-text-secondary)">{totalItems - correctCount - openCount}</div>
                <div className="text-xs text-(--color-text-tertiary)">To review</div>
              </div>
            )}
            {openCount > 0 && (
              <div className="text-center">
                <div className="text-3xl font-bold text-(--color-accent)">{openCount}</div>
                <div className="text-xs text-(--color-text-tertiary)">For parent review</div>
              </div>
            )}
          </div>
          <div className="space-y-2">
            {results.map((r, i) => (
              <div key={i} className="flex items-start gap-2 text-sm">
                <span className={r.correct === true ? "text-(--color-success)" : r.correct === false ? "text-(--color-danger)" : "text-(--color-accent)"}>{r.correct === true ? "✓" : r.correct === false ? "✗" : "○"}</span>
                <span className="text-(--color-text-secondary)">{r.prompt}</span>
              </div>
            ))}
          </div>
        </div>
        <button onClick={handleFinish} className="w-full py-3 rounded-xl bg-(--color-accent) text-white font-medium hover:opacity-90 transition-opacity">
          Submit Practice Results
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto py-6">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-xl font-semibold text-(--color-text)">{context.activity.title}</h1>
        <span className="text-sm text-(--color-text-tertiary)">{currentIdx + 1} of {totalItems}</span>
      </div>

      {/* Progress bar */}
      <div className="w-full h-1.5 bg-(--color-border) rounded-full mb-6 overflow-hidden">
        <div className="h-full bg-(--color-accent) rounded-full transition-all duration-300" style={{ width: `${((currentIdx) / totalItems) * 100}%` }} />
      </div>

      {/* Difficulty badge */}
      {item.difficulty && (
        <div className="mb-3">
          <span className={`inline-block px-2 py-0.5 rounded-full text-[10px] font-medium ${item.difficulty === 1 ? "bg-(--color-success-light) text-(--color-success)" : item.difficulty === 2 ? "bg-(--color-warning-light) text-(--color-warning)" : "bg-(--color-danger-light) text-(--color-danger)"}`}>
            {item.difficulty === 1 ? "Foundational" : item.difficulty === 2 ? "Standard" : "Challenge"}
          </span>
        </div>
      )}

      {/* Question */}
      <div className="bg-(--color-surface) border border-(--color-border) rounded-xl p-5 mb-4">
        <p className="text-(--color-text) text-lg leading-relaxed">{item.prompt}</p>
      </div>

      {/* Input area */}
      {!checked && (
        <div className="mb-4">
          {item.expected_type === "number" && (
            <input type="number" value={answer} onChange={(e) => setAnswer(e.target.value)} placeholder="Type your answer..." className="w-full px-4 py-3 rounded-xl border border-(--color-border) bg-(--color-surface) text-(--color-text) text-lg focus:outline-none focus:border-(--color-accent)" onKeyDown={(e) => e.key === "Enter" && answer && checkAnswer()} autoFocus />
          )}
          {item.expected_type === "text" && (
            <textarea value={answer} onChange={(e) => setAnswer(e.target.value)} placeholder="Write your answer..." rows={4} className="w-full px-4 py-3 rounded-xl border border-(--color-border) bg-(--color-surface) text-(--color-text) focus:outline-none focus:border-(--color-accent) resize-none" autoFocus />
          )}
          {item.expected_type === "multiple_choice" && item.options && (
            <div className="space-y-2">
              {item.options.map((opt, i) => (
                <button key={i} onClick={() => setAnswer(opt)} className={`w-full text-left px-4 py-3 rounded-xl border transition-colors ${answer === opt ? "border-(--color-accent) bg-(--color-accent-light) text-(--color-text)" : "border-(--color-border) bg-(--color-surface) text-(--color-text-secondary) hover:border-(--color-text-tertiary)"}`}>
                  {String.fromCharCode(65 + i)}. {opt}
                </button>
              ))}
            </div>
          )}
          {item.expected_type === "true_false" && (
            <div className="flex gap-3">
              {["True", "False"].map((tf) => (
                <button key={tf} onClick={() => setAnswer(tf)} className={`flex-1 py-4 rounded-xl border text-lg font-medium transition-colors ${answer === tf ? "border-(--color-accent) bg-(--color-accent-light) text-(--color-accent)" : "border-(--color-border) bg-(--color-surface) text-(--color-text-secondary) hover:border-(--color-text-tertiary)"}`}>
                  {tf}
                </button>
              ))}
            </div>
          )}

          <div className="flex items-center gap-3 mt-4">
            <button onClick={checkAnswer} disabled={!answer} className="flex-1 py-3 rounded-xl bg-(--color-accent) text-white font-medium disabled:opacity-40 hover:opacity-90 transition-opacity">
              Check Answer
            </button>
            {item.hints && item.hints.length > 0 && showHint < item.hints.length && (
              <button onClick={() => setShowHint((h) => h + 1)} className="px-4 py-3 rounded-xl border border-(--color-border) text-(--color-text-secondary) hover:bg-(--color-surface) transition-colors text-sm">
                Hint ({showHint}/{item.hints.length})
              </button>
            )}
          </div>
        </div>
      )}

      {/* Hints */}
      {showHint > 0 && item.hints && (
        <div className="mb-4 space-y-2">
          {item.hints.slice(0, showHint).map((h, i) => (
            <div key={i} className="px-4 py-2 rounded-lg bg-(--color-warning-light) border border-(--color-warning)/20 text-sm text-(--color-warning)">
              💡 {h}
            </div>
          ))}
        </div>
      )}

      {/* Result feedback */}
      {checked && (
        <div className={`mb-4 px-5 py-4 rounded-xl border ${correct ? "bg-(--color-success-light) border-(--color-success)/20" : item.expected_type === "text" ? "bg-(--color-accent-light) border-(--color-accent)/20" : "bg-(--color-danger-light) border-(--color-danger)/20"}`}>
          {correct && <p className="text-(--color-success) font-medium mb-1">✓ Correct!</p>}
          {!correct && item.expected_type !== "text" && <p className="text-(--color-danger) font-medium mb-1">✗ Not quite.</p>}
          {!correct && item.expected_type === "text" && <p className="text-(--color-accent) font-medium mb-1">○ Submitted for review.</p>}
          {item.explanation && <p className="text-sm text-(--color-text-secondary) mt-1">{item.explanation}</p>}
          {!correct && item.correct_answer && item.expected_type !== "text" && (
            <p className="text-sm text-(--color-text-secondary) mt-1">The answer is: <strong>{item.correct_answer}</strong></p>
          )}
          <button onClick={nextItem} className="mt-3 px-4 py-2 rounded-lg bg-(--color-accent) text-white text-sm font-medium hover:opacity-90 transition-opacity">
            {currentIdx + 1 >= totalItems ? "See Results" : "Next Question →"}
          </button>
        </div>
      )}

      {/* Help buttons */}
      <div className="flex items-center justify-center gap-4 mt-6">
        <button onClick={() => setShowTutor(true)} className="text-sm text-(--color-accent) hover:underline min-h-[44px]">
          Ask the Tutor
        </button>
        <button onClick={() => { setShowTutor(true); }}
          className="px-4 py-2 text-sm text-(--color-warning) border border-(--color-warning)/30 rounded-xl hover:bg-(--color-warning-light) transition-colors min-h-[44px]"
          aria-label="I'm stuck — opens tutor for help">
          I&apos;m stuck
        </button>
      </div>
      {showTutor && <TutorChat activityId={context.activity.id} childId={childId} onClose={() => setShowTutor(false)}
        activityTitle={context.activity.title} currentStep={currentIdx} totalSteps={totalItems} />}
    </div>
  );
}
