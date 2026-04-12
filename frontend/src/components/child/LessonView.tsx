"use client";

import { useState } from "react";
import type { LearningContext } from "@/lib/api";
import TutorChat from "./TutorChat";
import { cn } from "@/lib/cn";

interface LessonViewProps {
  context: LearningContext;
  childId: string;
  onComplete: (data: { confidence: number; responses: Array<{ prompt: string; response: string }>; self_reflection: string }) => void;
}

type Phase = "setup" | "intro" | "guided" | "practice" | "reflect";

export default function LessonView({ context, childId, onComplete }: LessonViewProps) {
  const [phase, setPhase] = useState<Phase>("setup");
  const [currentStep, setCurrentStep] = useState(0);
  const [showTutor, setShowTutor] = useState(false);
  const [responses, setResponses] = useState<Record<number, string>>({});
  const [selfAssessment, setSelfAssessment] = useState<number | null>(null);
  const [reflection, setReflection] = useState("");

  const { lesson, activity, assessment } = context;
  const steps = lesson.steps || [];
  const prompts = lesson.practice_prompts || [];

  function handleSubmit() {
    const practiceResponses = prompts.map((p, i) => ({
      prompt: p,
      response: responses[i] || "",
    }));
    onComplete({
      confidence: selfAssessment ?? 0.6,
      responses: practiceResponses,
      self_reflection: reflection,
    });
  }

  return (
    <div className="max-w-2xl mx-auto">
      {/* Phase: Setup */}
      {phase === "setup" && (
        <div className="text-center py-8">
          <h1 className="text-3xl font-semibold text-(--color-text) mb-3">{activity.title}</h1>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-(--color-accent-light) text-(--color-accent) text-sm mb-6">
            Lesson · {activity.estimated_minutes} minutes
          </div>

          {lesson.objectives?.length > 0 && (
            <div className="text-left bg-(--color-surface) rounded-2xl p-6 mb-6">
              <h3 className="text-sm font-semibold text-(--color-text-secondary) uppercase tracking-wider mb-2">What you&apos;ll learn today</h3>
              <ul className="space-y-1.5">
                {lesson.objectives.map((obj, i) => (
                  <li key={i} className="text-base text-(--color-text) flex items-start gap-2">
                    <span className="text-(--color-accent) mt-1">•</span> {obj}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {lesson.resources_needed?.length > 0 && (
            <div className="text-left bg-(--color-warning-light) rounded-2xl p-5 mb-6">
              <h3 className="text-sm font-semibold text-(--color-warning) mb-1">What you&apos;ll need</h3>
              <p className="text-sm text-(--color-text-secondary)">{lesson.resources_needed.join(", ")}</p>
            </div>
          )}

          <button onClick={() => setPhase("intro")}
            className="w-full max-w-xs py-4 text-lg font-semibold text-white bg-(--color-accent) rounded-2xl hover:opacity-90 transition-opacity">
            Begin
          </button>
        </div>
      )}

      {/* Phase: Introduction */}
      {phase === "intro" && (
        <div className="py-6">
          <h2 className="text-2xl font-semibold text-(--color-text) mb-4">Let&apos;s get started</h2>
          {lesson.introduction && (
            <div className="text-base leading-relaxed text-(--color-text) mb-6 whitespace-pre-line">
              {lesson.introduction}
            </div>
          )}
          {lesson.real_world_connection && (
            <div className="bg-(--color-accent-light) rounded-2xl p-5 mb-6">
              <h3 className="text-sm font-semibold text-(--color-accent) mb-1">Why this matters</h3>
              <p className="text-sm text-(--color-text)">{lesson.real_world_connection}</p>
            </div>
          )}
          <button onClick={() => setPhase("guided")}
            className="w-full max-w-xs mx-auto block py-3.5 text-base font-semibold text-white bg-(--color-accent) rounded-2xl hover:opacity-90 transition-opacity">
            Continue
          </button>
        </div>
      )}

      {/* Phase: Guided Learning */}
      {phase === "guided" && steps.length === 0 && (
        <div className="py-6 text-center">
          <h2 className="text-lg font-semibold text-(--color-text) mb-4">Guided Learning</h2>
          <p className="text-base text-(--color-text-secondary) mb-6">
            Work through this activity at your own pace. When you&apos;re ready, move on to practice.
          </p>
          <button onClick={() => setPhase(prompts.length > 0 ? "practice" : "reflect")}
            className="py-3 px-8 text-base font-semibold text-white bg-(--color-accent) rounded-2xl hover:opacity-90 transition-opacity">
            Continue to {prompts.length > 0 ? "Practice" : "Reflection"}
          </button>
        </div>
      )}
      {phase === "guided" && steps.length > 0 && (
        <div className="py-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-(--color-text)">Guided Learning</h2>
            <span className="text-sm text-(--color-text-tertiary)">Step {currentStep + 1} of {steps.length}</span>
          </div>

          {/* Progress bar */}
          <div className="w-full h-1.5 rounded-full bg-(--color-border) mb-6">
            <div className="h-full rounded-full bg-(--color-accent) transition-all" style={{ width: `${((currentStep + 1) / Math.max(steps.length, 1)) * 100}%` }} />
          </div>

          {/* Previous steps (collapsed) */}
          {steps.slice(0, currentStep).map((step, i) => (
            <div key={i} className="mb-2 px-4 py-2 rounded-xl bg-(--color-page) text-sm text-(--color-text-tertiary)">
              {step.title}
            </div>
          ))}

          {/* Current step */}
          {steps[currentStep] && (
            <div className="bg-(--color-surface) rounded-2xl p-6 mb-4 border border-(--color-border)">
              <div className="flex items-center gap-2 mb-3">
                <span className={cn(
                  "text-xs font-bold uppercase px-2 py-0.5 rounded-lg",
                  steps[currentStep].type === "read" ? "bg-(--color-accent-light) text-(--color-accent)" :
                  steps[currentStep].type === "think" ? "bg-(--color-warning-light) text-(--color-warning)" :
                  steps[currentStep].type === "do" ? "bg-(--color-success-light) text-(--color-success)" :
                  "bg-(--color-page) text-(--color-text-secondary)"
                )}>
                  {steps[currentStep].type}
                </span>
                <h3 className="text-base font-medium text-(--color-text)">{steps[currentStep].title}</h3>
              </div>
              <p className="text-base leading-relaxed text-(--color-text) whitespace-pre-line">{steps[currentStep].content}</p>

              {(steps[currentStep].type === "think" || steps[currentStep].type === "write") && (
                <textarea
                  value={responses[currentStep] || ""}
                  onChange={(e) => setResponses({ ...responses, [currentStep]: e.target.value })}
                  placeholder={steps[currentStep].type === "think" ? "What do you think? (optional)" : "Write your response here..."}
                  className="w-full mt-4 h-24 px-4 py-3 text-base border border-(--color-border) rounded-2xl resize-none bg-(--color-page) text-(--color-text) focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20"
                />
              )}
            </div>
          )}

          <div className="flex items-center justify-between">
            {context.tutor_available && (
              <button onClick={() => setShowTutor(true)}
                className="text-sm text-(--color-accent) hover:underline">
                Talk to your tutor
              </button>
            )}
            <button
              onClick={() => {
                if (currentStep < steps.length - 1) setCurrentStep(currentStep + 1);
                else setPhase(prompts.length > 0 ? "practice" : "reflect");
              }}
              className="ml-auto py-3 px-8 text-base font-semibold text-white bg-(--color-accent) rounded-2xl hover:opacity-90 transition-opacity"
            >
              {currentStep < steps.length - 1 ? "Continue" : "Next"}
            </button>
          </div>
        </div>
      )}

      {/* Phase: Practice */}
      {phase === "practice" && (
        <div className="py-6">
          <h2 className="text-2xl font-semibold text-(--color-text) mb-2">Practice</h2>
          <p className="text-sm text-(--color-text-secondary) mb-6">
            {prompts.length > 0 ? "Work through these to build your skills." : "Write about what you learned, or describe your work in your own words."}
          </p>

          <div className="space-y-4 mb-6">
            {prompts.map((prompt, i) => (
              <div key={i} className="bg-(--color-surface) rounded-2xl p-5 border border-(--color-border)">
                <p className="text-base text-(--color-text) mb-3">{prompt}</p>
                <textarea
                  value={responses[100 + i] || ""}
                  onChange={(e) => setResponses({ ...responses, [100 + i]: e.target.value })}
                  placeholder="Your answer..."
                  className="w-full h-20 px-4 py-3 text-base border border-(--color-border) rounded-2xl resize-none bg-(--color-page) text-(--color-text) focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20"
                />
              </div>
            ))}
          </div>

          <div className="flex items-center justify-between">
            {context.tutor_available && (
              <button onClick={() => setShowTutor(true)} className="text-sm text-(--color-accent) hover:underline">
                Ask your tutor
              </button>
            )}
            <button onClick={() => setPhase("reflect")}
              className="ml-auto py-3 px-8 text-base font-semibold text-white bg-(--color-accent) rounded-2xl hover:opacity-90 transition-opacity">
              Continue
            </button>
          </div>
        </div>
      )}

      {/* Phase: Reflection & Submit */}
      {phase === "reflect" && (
        <div className="py-6">
          <h2 className="text-2xl font-semibold text-(--color-text) mb-6">How did it go?</h2>

          <div className="space-y-3 mb-8">
            {[
              { label: "I understand this well", value: 0.9, color: "bg-(--color-success-light) border-(--color-success)" },
              { label: "I'm getting there", value: 0.6, color: "bg-(--color-warning-light) border-(--color-warning)" },
              { label: "I need more help", value: 0.3, color: "bg-(--color-danger-light) border-(--color-danger)" },
            ].map((opt) => (
              <button key={opt.value} onClick={() => setSelfAssessment(opt.value)}
                className={cn(
                  "w-full text-left px-5 py-4 rounded-2xl border-2 text-base font-medium transition-all",
                  selfAssessment === opt.value ? opt.color : "border-(--color-border) bg-(--color-surface) text-(--color-text)"
                )}>
                {opt.label}
              </button>
            ))}
          </div>

          <div className="mb-8">
            <label className="block text-sm text-(--color-text-secondary) mb-2">
              Anything you want to tell your parent about today&apos;s lesson? (optional)
            </label>
            <textarea
              value={reflection}
              onChange={(e) => setReflection(e.target.value)}
              placeholder="How did the lesson go? What was interesting or tricky?"
              className="w-full h-24 px-4 py-3 text-base border border-(--color-border) rounded-2xl resize-none bg-(--color-surface) text-(--color-text) focus:outline-none focus:ring-2 focus:ring-(--color-accent)/20"
            />
          </div>

          <button
            onClick={handleSubmit}
            disabled={selfAssessment === null}
            className="w-full py-4 text-lg font-semibold text-white bg-(--color-success) rounded-2xl hover:opacity-90 disabled:opacity-40 transition-opacity"
          >
            Complete this activity
          </button>
        </div>
      )}

      {/* Tutor overlay */}
      {showTutor && (
        <TutorChat activityId={activity.id} childId={childId} onClose={() => setShowTutor(false)} />
      )}
    </div>
  );
}
