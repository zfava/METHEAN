"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { betaFeedback, type BetaFeedbackItem } from "@/lib/api";
import { useMobile } from "@/lib/useMobile";
import { useToast } from "@/components/Toast";
import Button from "@/components/ui/Button";
import BottomSheet from "@/components/BottomSheet";

type FeedbackType = BetaFeedbackItem["feedback_type"];

const TYPES: { value: FeedbackType; label: string }[] = [
  { value: "bug", label: "Bug" },
  { value: "feature_request", label: "Feature request" },
  { value: "usability", label: "Usability" },
  { value: "content", label: "Content" },
  { value: "general", label: "General" },
];

export default function BetaFeedbackButton() {
  const pathname = usePathname();
  const isMobile = useMobile();
  const { toast } = useToast();
  const [open, setOpen] = useState(false);
  const [feedbackType, setFeedbackType] = useState<FeedbackType>("general");
  const [rating, setRating] = useState<number | null>(null);
  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);

  // Reset form when opening
  useEffect(() => {
    if (open) {
      setFeedbackType("general");
      setRating(null);
      setMessage("");
    }
  }, [open]);

  async function handleSubmit() {
    if (!message.trim()) return;
    setSubmitting(true);
    try {
      await betaFeedback.submit({
        feedback_type: feedbackType,
        page_context: pathname || undefined,
        rating: rating ?? undefined,
        message: message.trim(),
      });
      toast("Thanks! Your feedback was submitted.", "success");
      setOpen(false);
    } catch (err: any) {
      toast(err?.detail || "Couldn't submit feedback. Try again.", "error");
    } finally {
      setSubmitting(false);
    }
  }

  const form = (
    <div className="p-5 space-y-4">
      <div>
        <h2 className="text-lg font-semibold text-(--color-text)">Send beta feedback</h2>
        <p className="text-xs text-(--color-text-secondary) mt-1">
          Tell us what's working, what's not, or what you'd like to see.
        </p>
      </div>

      <div>
        <label className="block text-xs text-(--color-text-secondary) mb-1.5">Type</label>
        <div className="flex flex-wrap gap-1.5">
          {TYPES.map((t) => (
            <button
              key={t.value}
              type="button"
              onClick={() => setFeedbackType(t.value)}
              className={`px-3 py-1.5 text-xs rounded-[10px] border transition-colors ${
                feedbackType === t.value
                  ? "border-(--color-accent) bg-(--color-accent-light) text-(--color-accent)"
                  : "border-(--color-border) text-(--color-text-secondary)"
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      <div>
        <label className="block text-xs text-(--color-text-secondary) mb-1.5">
          Rating <span className="text-(--color-text-tertiary)">(optional)</span>
        </label>
        <div className="flex gap-1">
          {[1, 2, 3, 4, 5].map((n) => (
            <button
              key={n}
              type="button"
              onClick={() => setRating(rating === n ? null : n)}
              aria-label={`${n} star${n === 1 ? "" : "s"}`}
              className={`w-9 h-9 rounded-[10px] border text-base transition-colors ${
                rating !== null && n <= rating
                  ? "border-(--color-accent) bg-(--color-accent-light) text-(--color-accent)"
                  : "border-(--color-border) text-(--color-text-tertiary)"
              }`}
            >
              ★
            </button>
          ))}
        </div>
      </div>

      <div>
        <label className="block text-xs text-(--color-text-secondary) mb-1.5">
          What's on your mind?
        </label>
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          rows={5}
          placeholder="Describe what you're seeing or what you'd like to see..."
          className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text) resize-none"
        />
      </div>

      <div>
        <label className="block text-xs text-(--color-text-secondary) mb-1">
          Page this is about
        </label>
        <input
          value={pathname || ""}
          disabled
          className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-page) text-(--color-text-tertiary)"
        />
      </div>

      <div className="flex items-center justify-end gap-2 pt-2">
        <Button variant="ghost" size="sm" onClick={() => setOpen(false)}>
          Cancel
        </Button>
        <Button
          variant="primary"
          size="sm"
          disabled={!message.trim() || submitting}
          onClick={handleSubmit}
        >
          {submitting ? "Sending..." : "Send feedback"}
        </Button>
      </div>
    </div>
  );

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-label="Send beta feedback"
        className="fixed z-40 rounded-full bg-(--color-accent) text-white shadow-lg hover:bg-(--color-accent-hover) active:scale-[0.96] transition-all duration-150 flex items-center justify-center"
        style={{
          right: 20,
          bottom: isMobile
            ? "calc(56px + var(--safe-bottom) + 20px)"
            : 24,
          width: 52,
          height: 52,
        }}
      >
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path
            d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>

      {isMobile ? (
        <BottomSheet open={open} onClose={() => setOpen(false)} label="Send feedback">
          {form}
        </BottomSheet>
      ) : open ? (
        <div className="fixed inset-0 z-50" role="presentation">
          <div
            className="absolute inset-0 bg-black/40 animate-fade-in"
            onClick={() => setOpen(false)}
            aria-hidden="true"
          />
          <div
            role="dialog"
            aria-modal="true"
            aria-label="Send feedback"
            className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[min(520px,calc(100vw-32px))] bg-(--color-surface) rounded-[14px] shadow-[var(--shadow-card-hover)] border border-(--color-border) max-h-[85vh] overflow-y-auto"
          >
            {form}
          </div>
        </div>
      ) : null}
    </>
  );
}
