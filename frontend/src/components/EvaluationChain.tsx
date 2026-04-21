"use client";

import { cn } from "@/lib/cn";
import type { GovernanceEvaluation } from "@/lib/api";

interface EvaluationChainProps {
  evaluations: GovernanceEvaluation[];
  blockingRules?: string[];
}

export default function EvaluationChain({ evaluations, blockingRules = [] }: EvaluationChainProps) {
  if (!evaluations || evaluations.length === 0) return null;

  return (
    <div className="space-y-1.5">
      {evaluations.map((ev, i) => {
        const isBlocking = !ev.passed && blockingRules.includes(ev.rule);
        return (
          <div key={i} className={cn(
            "flex items-start gap-2 text-xs px-2.5 py-1.5 rounded-md",
            isBlocking ? "bg-(--color-warning-light) border-l-2 border-(--color-warning)" : "bg-(--color-page)"
          )}>
            <span className={cn("shrink-0 mt-0.5", ev.passed ? "text-(--color-success)" : "text-(--color-danger)")}>
              {ev.passed ? "✓" : "✗"}
            </span>
            <div className="min-w-0">
              <span className="font-medium text-(--color-text)">{ev.rule}</span>
              <span className="text-(--color-text-tertiary)"> ({ev.type})</span>
              <span className="text-(--color-text-secondary)"> — {ev.reason}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
