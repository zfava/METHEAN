"use client";

import { motion } from "framer-motion";
import { useState, useEffect, useRef } from "react";
import type { LearningContext } from "@/lib/api";
import { useSoundCue } from "@/lib/useSoundCue";
import { usePersonalization } from "@/lib/PersonalizationProvider";
import VoiceTextarea from "@/components/child/VoiceTextarea";
import { MotionText } from "@/components/child/motion";
import { useMotion } from "@/lib/motion/MotionContext";
import { MOTION_DURATIONS_SEC, MOTION_EASINGS } from "@/lib/motion/tokens";

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
  const [currentIdx, setCurrentIdx] = useState(0);
  const [elapsed, setElapsed] = useState(0);
  const [submitted, setSubmitted] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const playCue = useSoundCue();
  // AssessmentView receives only context, not childId; source the
  // active learner from personalization so transcription usage is
  // attributed correctly. page.tsx is out of scope for this change.
  const { profile } = usePersonalization();

  const totalItems = items.length;
  const answeredCount = Object.values(responses).filter(r => r.trim().length > 0).length;

  useEffect(() => {
    timerRef.current = setInterval(() => setElapsed(e => e + 1), 1000);
    playCue("activity_start");
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function handleSubmit() {
    if (timerRef.current) clearInterval(timerRef.current);
    setSubmitted(true);
    playCue("activity_complete");
    onComplete({
      confidence: 0.7,
      responses: items.map((item, i) => ({ prompt: item.prompt, response: responses[i] || "" })),
      self_reflection: `Completed ${answeredCount} of ${totalItems} items.`,
    });
  }

  // Submitted state — no scores, no grades, no judgment
  if (submitted) {
    return (
      <div className="max-w-2xl mx-auto py-12 text-center">
        <div className="text-4xl mb-4">{"\uD83C\uDF1F"}</div>
        <h1 className="text-2xl font-medium text-(--color-text) mb-2">All done!</h1>
        <p className="text-base text-(--color-text-secondary) leading-relaxed">
          Your parent will review your work. You did great showing what you know.
        </p>
      </div>
    );
  }

  if (totalItems === 0) {
    return (
      <div className="max-w-2xl mx-auto py-8 text-center">
        <p className="text-(--color-text-secondary)">Assessment is being prepared. Check back soon.</p>
      </div>
    );
  }

  const item = items[currentIdx];

  return (
    <div className="max-w-2xl mx-auto py-8">
      {/* Header — "Show what you know", not "Test" */}
      <div className="mb-6">
        <h1 className="text-xl font-medium text-(--color-text)">Show What You Know</h1>
        <p className="text-sm text-(--color-text-tertiary)">{context.activity.title}</p>
      </div>

      {/* Progress — thin bar, non-pressuring */}
      <div className="flex items-center gap-2 mb-8">
        <div className="flex-1 h-1 bg-(--color-border) rounded-full">
          <div className="h-full bg-(--color-accent) rounded-full transition-all" style={{ width: `${((currentIdx + 1) / totalItems) * 100}%` }} />
        </div>
        <span className="text-xs text-(--color-text-tertiary)">{currentIdx + 1} of {totalItems}</span>
      </div>

      {/* One question at a time. Cinematic decelerate on the prompt
          card to convey the gravity of an assessment without
          bouncing. The prompt text itself shifts weight from regular
          to medium via MotionText so the question lands. */}
      <AssessmentQuestionCard prompt={item.prompt}>


        {item.type === "number" && (
          <input type="number" value={responses[currentIdx] || ""}
            onChange={e => setResponses(r => ({ ...r, [currentIdx]: e.target.value }))}
            placeholder="Your answer..."
            className="w-full px-4 py-3 rounded-xl border border-(--color-border) bg-(--color-page) text-base text-(--color-text) focus:outline-none focus:border-(--color-accent) min-h-[44px]" />
        )}
        {item.type === "multiple_choice" && item.options && (
          <div className="space-y-2">
            {item.options.map((opt, oi) => (
              <button key={oi} onClick={() => setResponses(r => ({ ...r, [currentIdx]: opt }))}
                className={`w-full text-left px-4 py-3 rounded-xl border-2 text-base transition-colors min-h-[48px] ${
                  responses[currentIdx] === opt ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border) bg-(--color-surface)"
                }`}>
                {String.fromCharCode(65 + oi)}. {opt}
              </button>
            ))}
          </div>
        )}
        {item.type === "true_false" && (
          <div className="flex gap-3">
            {["True", "False"].map(tf => (
              <button key={tf} onClick={() => setResponses(r => ({ ...r, [currentIdx]: tf }))}
                className={`flex-1 py-3 rounded-xl border-2 font-medium text-base min-h-[48px] ${
                  responses[currentIdx] === tf ? "border-(--color-accent) bg-(--color-accent-light)" : "border-(--color-border)"
                }`}>
                {tf}
              </button>
            ))}
          </div>
        )}
        {(item.type === "open_response" || item.type === "text" || !item.type) && (
          <VoiceTextarea value={responses[currentIdx] || ""}
            onChange={(next) => setResponses(r => ({ ...r, [currentIdx]: next }))}
            childId={profile.child_id}
            placeholder="Write your answer..." rows={4}
            className="w-full px-4 py-3 rounded-xl border border-(--color-border) bg-(--color-page) text-base text-(--color-text) focus:outline-none focus:border-(--color-accent) resize-none" />
        )}
      </AssessmentQuestionCard>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <button onClick={() => setCurrentIdx(i => Math.max(0, i - 1))} disabled={currentIdx === 0}
          className="py-3 px-5 text-sm text-(--color-text-secondary) disabled:opacity-30 min-h-[44px]">&larr; Previous</button>

        {currentIdx < totalItems - 1 ? (
          <button onClick={() => setCurrentIdx(i => i + 1)}
            className="py-3 px-8 text-base font-medium text-white bg-(--color-accent) rounded-2xl min-h-[44px]">
            Next
          </button>
        ) : !showConfirm ? (
          <button onClick={() => setShowConfirm(true)}
            className="py-3 px-8 text-base font-medium text-white bg-(--color-success) rounded-2xl min-h-[44px]">
            I&apos;m Finished
          </button>
        ) : (
          <div className="flex items-center gap-2">
            <span className="text-xs text-(--color-text-secondary)">Submit your work?</span>
            <button onClick={handleSubmit} className="py-2 px-5 text-sm font-medium text-white bg-(--color-success) rounded-xl min-h-[44px]">Yes</button>
            <button onClick={() => setShowConfirm(false)} className="py-2 px-5 text-sm text-(--color-text-secondary) min-h-[44px]">Go Back</button>
          </div>
        )}
      </div>

      {/* Elapsed time — subtle, not a countdown */}
      <div className="text-center mt-8">
        <span className="text-[10px] text-(--color-text-tertiary)">
          {Math.floor(elapsed / 60)}:{(elapsed % 60).toString().padStart(2, "0")} elapsed
        </span>
      </div>
    </div>
  );
}

/**
 * Wraps each assessment question in a card that enters with the
 * cinematic curve. Re-mounts on the prompt changing so the gravity
 * resets between questions. Skips animation under reduceMotion.
 */
function AssessmentQuestionCard({
  prompt,
  children,
}: {
  prompt: string;
  children: React.ReactNode;
}) {
  const { reduceMotion, speed } = useMotion();
  const dur = MOTION_DURATIONS_SEC.slow / speed;
  if (reduceMotion) {
    return (
      <div className="bg-(--color-surface) border border-(--color-border) rounded-2xl p-6 mb-6">
        <p className="text-lg text-(--color-text) leading-relaxed mb-4">{prompt}</p>
        {children}
      </div>
    );
  }
  return (
    <motion.div
      key={prompt}
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: dur, ease: MOTION_EASINGS.cinematic }}
      className="bg-(--color-surface) border border-(--color-border) rounded-2xl p-6 mb-6"
    >
      <MotionText
        as="p"
        weight
        entrance
        className="text-lg text-(--color-text) leading-relaxed mb-4"
      >
        {prompt}
      </MotionText>
      {children}
    </motion.div>
  );
}
