"use client";

import { useEffect, useState } from "react";
import { children as childrenApi, governance, type DemotionFeedItem, type GovernanceEvent } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import { useMobile } from "@/lib/useMobile";
import StatusBadge from "@/components/StatusBadge";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import BottomSheet from "@/components/BottomSheet";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import EmptyState from "@/components/ui/EmptyState";

// A demotion paired with the child it belongs to. The feed endpoint is
// per-child, so we attach the child identity as we aggregate across children.
interface ChildDemotion extends DemotionFeedItem {
  childId: string;
  childName: string;
}

export default function OverridesPage() {
  useEffect(() => { document.title = "Overrides | METHEAN"; }, []);

  const isMobile = useMobile();
  const { children: childList } = useChild();
  const [overrides, setOverrides] = useState<GovernanceEvent[]>([]);
  const [demotions, setDemotions] = useState<ChildDemotion[]>([]);
  const [loading, setLoading] = useState(true);

  // Restore confirm state.
  const [restoring, setRestoring] = useState<ChildDemotion | null>(null);
  const [reason, setReason] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [restoreError, setRestoreError] = useState("");

  useEffect(() => {
    governance.events(200)
      .then((d) => {
        const all: GovernanceEvent[] = (d as any).items || d;
        // Overrides are governance events on child_node_state targets
        setOverrides(all.filter((e) => e.target_type === "child_node_state"));
      })
      .finally(() => setLoading(false));
  }, []);

  // Pull the demotion feed for every child and merge into one list, most
  // recent first. Runs whenever the child list resolves from context.
  useEffect(() => {
    if (childList.length === 0) return;
    let cancelled = false;
    Promise.all(
      childList.map((c) =>
        childrenApi.demotions(c.id)
          .then((d) =>
            d.items.map((item): ChildDemotion => ({
              ...item,
              childId: c.id,
              childName: c.first_name,
            })),
          )
          .catch(() => [] as ChildDemotion[]),
      ),
    ).then((lists) => {
      if (cancelled) return;
      const merged = lists.flat().sort(
        (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
      );
      setDemotions(merged);
    });
    return () => { cancelled = true; };
  }, [childList]);

  function openRestore(item: ChildDemotion) {
    setRestoreError("");
    setReason(
      `Restored to ${prettyLevel(item.explanation.from_level)} after parent review of the automated demotion.`,
    );
    setRestoring(item);
  }

  function closeRestore() {
    setRestoring(null);
    setReason("");
    setRestoreError("");
  }

  async function confirmRestore() {
    if (!restoring) return;
    if (!reason.trim()) {
      setRestoreError("A reason is required for the audit trail.");
      return;
    }
    setSubmitting(true);
    setRestoreError("");
    try {
      await childrenApi.masteryOverride(restoring.childId, restoring.node_id, {
        target_level: restoring.explanation.from_level,
        reason: reason.trim(),
      });
      // Optimistically drop the restored item from the demotions list.
      setDemotions((prev) => prev.filter((d) => d.id !== restoring.id));
      closeRestore();
    } catch (e) {
      setRestoreError(e instanceof Error ? e.message : "Could not restore this node. Try again.");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) return <div className="max-w-4xl"><LoadingSkeleton variant="list" count={4} /></div>;

  const restoreForm = restoring && (
    <div className="px-5 pb-6 pt-2 sm:p-6">
      <h3 className="text-base font-semibold text-(--color-text)">
        Restore {restoring.node_title || `node ${restoring.node_id.slice(0, 8)}`}
      </h3>
      <p className="text-sm text-(--color-text-secondary) mt-1">
        {restoring.childName} &middot; back to {prettyLevel(restoring.explanation.from_level)}
      </p>
      <p className="text-sm text-(--color-text) mt-3">{restoring.explanation.human_summary}</p>
      <label className="block text-xs font-medium text-(--color-text-secondary) mt-4 mb-1">
        Reason (recorded in the audit trail)
      </label>
      <textarea
        value={reason}
        onChange={(e) => setReason(e.target.value)}
        rows={3}
        className="w-full rounded-[10px] border border-(--color-border) bg-(--color-surface) px-3 py-2 text-sm text-(--color-text) focus:border-(--color-accent) focus:outline-none"
      />
      {restoreError && (
        <p className="text-sm text-(--color-danger) mt-2">{restoreError}</p>
      )}
      <div className="flex items-center justify-end gap-2 mt-4">
        <Button variant="ghost" onClick={closeRestore} disabled={submitting}>Cancel</Button>
        <Button variant="primary" onClick={confirmRestore} disabled={submitting}>
          {submitting ? "Restoring..." : "Restore"}
        </Button>
      </div>
    </div>
  );

  return (
    <div className="max-w-4xl">
      <PageHeader
        title="Override Log"
        subtitle="Prerequisite bypasses, manual mastery changes, and blocked node unlocks. This is the audit trail that proves parental sovereignty."
      />

      <section className="mb-8">
        <h2 className="text-sm font-semibold text-(--color-text) mb-2">Recent demotions</h2>
        {demotions.length === 0 ? (
          <EmptyState
            icon="empty"
            title="No automated demotions"
            description="When retention decays or a low-confidence attempt lowers a mastery level, it appears here so you can review and restore it."
          />
        ) : (
          <div className="space-y-2">
            {demotions.map((item) => (
              <Card key={item.id} padding="p-4" borderLeft="border-l-(--color-warning)" className="border-l-4">
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-sm font-medium text-(--color-text)">
                        {item.node_title || `Node ${item.node_id.slice(0, 8)}`}
                      </span>
                      <span className="text-xs text-(--color-text-secondary)">{item.childName}</span>
                    </div>
                    <p className="text-sm text-(--color-text)">{item.explanation.human_summary}</p>
                    <p className="text-xs text-(--color-text-secondary) mt-1">
                      {prettyLevel(item.explanation.from_level)} &rarr; {prettyLevel(item.explanation.to_level)}
                      {" · "}
                      {new Date(item.created_at).toLocaleString()}
                    </p>
                  </div>
                  <Button variant="secondary" size="sm" onClick={() => openRestore(item)}>
                    Restore
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        )}
      </section>

      <h2 className="text-sm font-semibold text-(--color-text) mb-2">Manual overrides</h2>
      {overrides.length === 0 ? (
        <EmptyState
          icon="empty"
          title="No overrides recorded yet"
          description="Overrides appear here when you unlock a blocked node or bypass a prerequisite."
        />
      ) : (
        <div className="space-y-2">
          {overrides.map((evt) => (
            <Card key={evt.id} padding="p-4" borderLeft="border-l-(--color-warning)" className="border-l-4">
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  <StatusBadge status={evt.action} />
                  <span className="text-sm font-medium text-(--color-text)">Override</span>
                </div>
                <span className="text-xs font-mono text-(--color-text-secondary)">
                  {new Date(evt.created_at).toLocaleString()}
                </span>
              </div>
              {evt.reason && (
                <p className="text-sm text-(--color-text) mt-1">&ldquo;{evt.reason}&rdquo;</p>
              )}
              <p className="text-xs text-(--color-text-secondary) mt-1">
                Target: {evt.target_type} &middot; {evt.target_id.slice(0, 8)}...
              </p>
            </Card>
          ))}
        </div>
      )}

      {/* Restore confirm: bottom sheet on mobile, centered modal on desktop. */}
      {isMobile ? (
        <BottomSheet open={!!restoring} onClose={closeRestore} label="Restore node">
          {restoreForm}
        </BottomSheet>
      ) : (
        restoring && (
          <div className="fixed inset-0 z-50 flex items-center justify-center" role="presentation">
            <div className="absolute inset-0 bg-black/40 animate-fade-in" onClick={closeRestore} aria-hidden="true" />
            <div
              role="dialog"
              aria-modal="true"
              aria-label="Restore node"
              className="relative w-full max-w-md mx-4 rounded-[16px] bg-(--color-surface) shadow-lg animate-fade-in"
            >
              {restoreForm}
            </div>
          </div>
        )
      )}
    </div>
  );
}

// Map a stored mastery level token to readable text for the parent.
function prettyLevel(level: string): string {
  return level.replace(/_/g, " ");
}
