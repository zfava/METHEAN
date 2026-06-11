"use client";

/**
 * Shown in place of any activity view when the backend's safety gates
 * blocked the learning context. Handles BOTH gates:
 *
 * - awaiting_human_safety_review: the content-review gate; a grown-up
 *   still needs to review this lesson's content.
 * - awaiting_qualified_human: the runtime presence gate; a qualified
 *   adult (named in the node's safety basis) must be physically present
 *   and a parent must attest that today before the activity opens.
 *
 * The card is intentionally calm and child-facing: it never frames the
 * block as the child's fault, and the only action is going back to
 * today's list. Unblocking happens on the parent's surface.
 */

import type { LearningContext } from "@/lib/api";

interface BlockedActivityCardProps {
  context: LearningContext;
  onBack: () => void;
}

export function BlockedActivityCard({ context, onBack }: BlockedActivityCardProps) {
  const presence = context.awaiting_qualified_human === true;
  const title = presence ? "A grown-up needs to be with you" : "Almost ready";
  const body = presence
    ? "This activity is hands-on and needs a qualified adult right there with you. Ask your parent; once they confirm someone is with you today, it will open up."
    : "A grown-up still needs to look over this activity before it opens. Check back soon, or pick something else for now.";

  return (
    <div className="max-w-md mx-auto text-center py-12" data-testid="blocked-activity-card">
      <div
        className="w-16 h-16 rounded-2xl mx-auto mb-5 flex items-center justify-center"
        style={{ background: "var(--color-accent-light)" }}
        aria-hidden="true"
      >
        <svg className="w-8 h-8 text-(--color-accent)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M16 11V7a4 4 0 10-8 0v4M5 11h14a1 1 0 011 1v7a2 2 0 01-2 2H6a2 2 0 01-2-2v-7a1 1 0 011-1z"
          />
        </svg>
      </div>
      <h2 className="text-xl font-bold text-(--color-text) mb-2">{title}</h2>
      <p className="text-sm text-(--color-text-secondary) leading-relaxed mb-2">{body}</p>
      <p className="text-xs text-(--color-text-tertiary) mb-8">{context.activity.title}</p>
      <button
        onClick={onBack}
        className="px-6 py-3 rounded-xl font-semibold text-sm press-scale bg-(--color-surface) border border-(--color-border) text-(--color-text)"
      >
        Back to today
      </button>
    </div>
  );
}
