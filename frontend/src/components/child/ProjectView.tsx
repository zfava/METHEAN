"use client";

import { useEffect, useState } from "react";
import type { LearningContext } from "@/lib/api";
import { useSoundCue } from "@/lib/useSoundCue";
import VoiceTextarea from "@/components/child/VoiceTextarea";
import TutorChat from "./TutorChat";

interface ProjectViewProps {
  context: LearningContext;
  childId: string;
  onComplete: (data: { confidence: number; responses: Array<{ prompt: string; response: string }>; self_reflection: string }) => void;
  onSaveProgress?: (notes: string) => void;
}

export default function ProjectView({ context, childId, onComplete, onSaveProgress }: ProjectViewProps) {
  const [notes, setNotes] = useState("");
  const [showTutor, setShowTutor] = useState(false);
  const [selfAssessment, setSelfAssessment] = useState<number | null>(null);
  const [phase, setPhase] = useState<"work" | "reflect">("work");
  const playCue = useSoundCue();

  const steps = context.lesson.steps || [];

  useEffect(() => {
    playCue("activity_start");
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function handleSubmit() {
    playCue("activity_complete");
    onComplete({
      confidence: selfAssessment ?? 0.7,
      responses: [{ prompt: "Project work", response: notes }],
      self_reflection: "",
    });
  }

  return (
    <div className="max-w-2xl mx-auto py-6">
      {phase === "work" && (
        <>
          <h1 className="text-3xl font-semibold text-(--color-text) mb-2">{context.activity.title}</h1>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-(--color-danger-light) text-(--color-danger) text-sm mb-6">
            Project · {context.activity.estimated_minutes} minutes
          </div>

          {context.activity.description && (
            <div className="bg-(--color-surface) rounded-2xl p-5 border border-(--color-border) mb-6">
              <p className="text-base text-(--color-text) leading-relaxed whitespace-pre-line">{context.activity.description}</p>
            </div>
          )}

          {context.lesson.resources_needed?.length > 0 && (
            <div className="bg-(--color-warning-light) rounded-2xl p-5 mb-6">
              <h3 className="text-sm font-semibold text-(--color-warning) mb-1">What you need</h3>
              <p className="text-sm text-(--color-text-secondary)">{context.lesson.resources_needed.join(", ")}</p>
            </div>
          )}

          {steps.length > 0 && (
            <div className="mb-6">
              <h3 className="text-sm font-semibold text-(--color-text-secondary) uppercase tracking-wider mb-3">Instructions</h3>
              <ol className="space-y-2">
                {steps.map((step, i) => (
                  <li key={i} className="flex gap-3 text-base text-(--color-text)">
                    <span className="text-(--color-accent) font-semibold shrink-0">{i + 1}.</span>
                    <span>{step.content}</span>
                  </li>
                ))}
              </ol>
            </div>
          )}

          <div className="mb-6">
            <h3 className="text-sm font-semibold text-(--color-text-secondary) uppercase tracking-wider mb-2">Your work</h3>
            <VoiceTextarea
              value={notes}
              onChange={setNotes}
              placeholder="Describe what you're doing, take notes, or record your progress..."
              rows={6}
            />
          </div>

          <div className="flex gap-3">
            {onSaveProgress && (
              <button onClick={() => onSaveProgress(notes)}
                className="flex-1 py-3.5 text-base font-medium text-(--color-accent) border-2 border-(--color-accent) rounded-2xl hover:bg-(--color-accent-light) transition-colors">
                Save Progress
              </button>
            )}
            <button onClick={() => setPhase("reflect")}
              className="flex-1 py-3.5 text-base font-semibold text-white bg-(--color-success) rounded-2xl hover:opacity-90 transition-opacity">
              Submit Completed Project
            </button>
          </div>

          {context.tutor_available && (
            <button onClick={() => setShowTutor(true)} className="mt-4 text-sm text-(--color-accent) hover:underline block mx-auto">
              Talk to your tutor
            </button>
          )}
        </>
      )}

      {phase === "reflect" && (
        <>
          <h2 className="text-2xl font-semibold text-(--color-text) mb-6">How did the project go?</h2>
          <div className="space-y-3 mb-8">
            {[
              { label: "I'm really proud of this", value: 0.9 },
              { label: "It was good work", value: 0.6 },
              { label: "I had some trouble", value: 0.3 },
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
