"use client";

import { useEffect } from "react";
import Badge from "@/components/ui/Badge";
import HashLine from "@/components/record/HashLine";
import type { RecordMasteryEvidence } from "@/lib/api";

function formatDate(iso: string | null): string {
  if (!iso) return "";
  return new Date(iso).toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
}

function actionLabel(action: string, targetType: string): string {
  if (targetType === "mastery_override") return "Parent override";
  switch (action) {
    case "approve":
      return "Parent approved";
    case "reject":
      return "Parent rejected";
    case "modify":
      return "Parent decision";
    default:
      return "Governance decision";
  }
}

/**
 * Right-side slide-over showing the full evidence chain for one
 * mastery claim. Visual story: the claim on top, the evidence below,
 * the seal at the bottom.
 */
export default function EvidenceDrawer({
  item,
  onClose,
}: {
  item: RecordMasteryEvidence | null;
  onClose: () => void;
}) {
  useEffect(() => {
    if (!item) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [item, onClose]);

  if (!item) return null;

  return (
    <div className="fixed inset-0 z-50" role="dialog" aria-modal="true" aria-label={`Evidence for ${item.node_title}`}>
      <div className="absolute inset-0 bg-black/30 animate-fade-in" onClick={onClose} />
      <aside
        data-testid="evidence-drawer"
        className="absolute right-0 top-0 h-full w-full max-w-md bg-(--color-surface) border-l border-(--color-border) shadow-xl animate-slide-right overflow-y-auto"
      >
        {/* The claim */}
        <div className="sticky top-0 bg-(--color-surface)/95 backdrop-blur border-b border-(--color-border) px-5 py-4 flex items-start justify-between gap-3">
          <div>
            <div className="type-eyebrow-md text-(--color-text-tertiary) mb-0.5">{item.subject || "General"}</div>
            <h2 className="text-base font-semibold text-(--color-text)">{item.node_title}</h2>
            <div className="flex items-center gap-2 mt-1.5">
              <Badge variant={item.mastery_level === "mastered" ? "mastered" : "progressing"}>
                {item.mastery_level === "mastered" ? "Mastered" : "Proficient"}
              </Badge>
              {item.achieved_at && (
                <span className="text-xs text-(--color-text-tertiary)">{formatDate(item.achieved_at)}</span>
              )}
            </div>
          </div>
          <button
            onClick={onClose}
            aria-label="Close evidence panel"
            className="text-(--color-text-tertiary) hover:text-(--color-text) min-w-[36px] min-h-[36px] flex items-center justify-center"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>

        <div className="px-5 py-4 space-y-6">
          {/* The work */}
          <section>
            <h3 className="type-eyebrow-md text-(--color-text-tertiary) mb-2">Practice and work</h3>
            {item.attempts.length === 0 ? (
              <p className="text-xs text-(--color-text-tertiary)">
                No logged attempts for this skill. Mastery here rests on assessment or parent judgment below.
              </p>
            ) : (
              <div className="space-y-1.5">
                {item.attempts.map((a) => (
                  <div key={a.id} className="flex items-center justify-between text-sm px-3 py-2 rounded-[10px] bg-(--color-page)">
                    <div className="min-w-0">
                      <div className="text-(--color-text) text-[13px] truncate">{a.activity_title || "Activity"}</div>
                      <div className="text-[11px] text-(--color-text-tertiary)">
                        {formatDate(a.completed_at || a.started_at)}
                        {a.duration_minutes ? ` · ${a.duration_minutes} min` : ""}
                      </div>
                    </div>
                    {a.score !== null && (
                      <span className="text-[13px] font-medium text-(--color-text) shrink-0">{Math.round(a.score * 100)}%</span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </section>

          {/* The judgment */}
          <section>
            <h3 className="type-eyebrow-md text-(--color-text-tertiary) mb-2">Assessments</h3>
            {item.assessments.length === 0 ? (
              <p className="text-xs text-(--color-text-tertiary)">No separate assessments recorded for this skill.</p>
            ) : (
              <div className="space-y-1.5">
                {item.assessments.map((a) => (
                  <div key={a.id} className="px-3 py-2 rounded-[10px] bg-(--color-page)">
                    <div className="text-[13px] text-(--color-text)">{a.title}</div>
                    <div className="text-[11px] text-(--color-text-tertiary)">
                      {a.assessment_type.replace(/_/g, " ")}
                      {a.mastery_judgment ? ` · judged ${a.mastery_judgment}` : ""}
                      {a.assessed_at ? ` · ${formatDate(a.assessed_at)}` : ""}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </section>

          {/* The seal */}
          <section data-testid="drawer-seal">
            <h3 className="type-eyebrow-md text-(--color-text-tertiary) mb-2">Sealed decisions</h3>
            {item.governance_events.length === 0 ? (
              <p className="text-xs text-(--color-text-tertiary)">
                No parent decisions reference this skill yet. Approvals and overrides land here automatically.
              </p>
            ) : (
              <div className="space-y-2">
                {item.governance_events.map((g) => (
                  <div key={g.id} className="px-3 py-2.5 rounded-[10px] border border-(--color-border) bg-(--color-page)">
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-[13px] font-medium text-(--color-text)">
                        {actionLabel(g.action, g.target_type)}
                      </span>
                      <span className="text-[11px] text-(--color-text-tertiary)">{formatDate(g.created_at)}</span>
                    </div>
                    {g.reason && <p className="text-xs text-(--color-text-secondary) mt-1">{g.reason}</p>}
                    {g.event_hash && (
                      <div className="mt-2">
                        <HashLine value={g.event_hash} label="seal" />
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </section>
        </div>
      </aside>
    </div>
  );
}
