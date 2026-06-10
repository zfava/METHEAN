"use client";

import Card from "@/components/ui/Card";
import Badge, { type BadgeVariant } from "@/components/ui/Badge";
import EmptyState from "@/components/ui/EmptyState";
import type { RecordMasteryEvidence } from "@/lib/api";

function levelBadge(level: string): { variant: BadgeVariant; label: string } {
  return level === "mastered"
    ? { variant: "mastered", label: "Mastered" }
    : { variant: "progressing", label: "Proficient" };
}

function monthKey(iso: string | null): string {
  if (!iso) return "Earlier";
  return new Date(iso).toLocaleDateString(undefined, { month: "long", year: "numeric" });
}

/**
 * Chronological achievements grouped by month, newest first. Each
 * entry opens the evidence drawer: the claim, then everything that
 * backs it up.
 */
export default function MasteryTimeline({
  evidence,
  onSelect,
}: {
  evidence: RecordMasteryEvidence[];
  onSelect: (item: RecordMasteryEvidence) => void;
}) {
  if (evidence.length === 0) {
    return (
      <EmptyState
        icon="empty"
        title="The record builds itself"
        description="As your child masters skills, each one lands here with its evidence attached: the work, the assessments, and your approval. Nothing to prepare, nothing to file."
      />
    );
  }

  const sorted = [...evidence].sort((a, b) => {
    const at = a.achieved_at ? new Date(a.achieved_at).getTime() : 0;
    const bt = b.achieved_at ? new Date(b.achieved_at).getTime() : 0;
    return bt - at;
  });

  const groups: { month: string; items: RecordMasteryEvidence[] }[] = [];
  for (const item of sorted) {
    const month = monthKey(item.achieved_at);
    const last = groups[groups.length - 1];
    if (last && last.month === month) last.items.push(item);
    else groups.push({ month, items: [item] });
  }

  return (
    <div data-testid="mastery-timeline" className="space-y-5">
      {groups.map((group) => (
        <div key={group.month}>
          <div className="type-eyebrow-md text-(--color-text-tertiary) mb-2">{group.month}</div>
          <div className="space-y-2">
            {group.items.map((item) => {
              const badge = levelBadge(item.mastery_level);
              return (
                <Card
                  key={item.node_id}
                  onClick={() => onSelect(item)}
                  padding="px-4 py-3"
                  className="cursor-pointer hover:border-(--color-border-strong)"
                >
                  <div className="flex items-center justify-between gap-3">
                    <div className="min-w-0">
                      <div className="text-sm font-medium text-(--color-text) truncate">{item.node_title}</div>
                      <div className="text-xs text-(--color-text-tertiary)">
                        {item.subject || "General"}
                        {item.achieved_at &&
                          ` · ${new Date(item.achieved_at).toLocaleDateString(undefined, { month: "short", day: "numeric" })}`}
                      </div>
                    </div>
                    <div className="flex items-center gap-2 shrink-0">
                      <Badge variant={badge.variant}>{badge.label}</Badge>
                      <span className="text-xs text-(--color-text-tertiary)">
                        {item.attempts.length + item.assessments.length + item.governance_events.length} evidence
                      </span>
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}
