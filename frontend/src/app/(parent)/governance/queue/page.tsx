"use client";

import { useEffect, useState, useMemo } from "react";
import { governance } from "@/lib/api";
import { useToast } from "@/components/Toast";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import StatusBadge from "@/components/StatusBadge";
import EmptyState from "@/components/ui/EmptyState";
import SectionHeader from "@/components/ui/SectionHeader";
import EvaluationChain from "@/components/EvaluationChain";
import { cn } from "@/lib/cn";
import { shortDate } from "@/lib/format";
import { useMobile } from "@/lib/useMobile";
import SwipeAction from "@/components/SwipeAction";

interface QueueItem {
  activity_id: string;
  title: string;
  activity_type: string;
  estimated_minutes: number | null;
  difficulty: number | null;
  ai_rationale: string;
  scheduled_date: string | null;
  child_name: string;
  child_id: string | null;
  plan_name: string;
  plan_id: string | null;
  governance_evaluation: {
    source?: string;
    evaluations?: Array<{ rule: string; type: string; passed: boolean; reason: string }>;
    blocking_rules?: string[];
  };
}

type ActionType = "approve" | "reject" | "modify";

// ── Difficulty dots ──
function DifficultyDots({ level }: { level: number }) {
  return (
    <div className="flex items-center gap-0.5">
      {[1, 2, 3, 4, 5].map((i) => (
        <span
          key={i}
          className={cn(
            "w-2 h-2 rounded-full",
            i <= level ? "bg-(--color-warning)" : "bg-(--color-border)"
          )}
        />
      ))}
    </div>
  );
}

// ── Check for constitutional violations ──
function hasConstitutionalViolation(item: QueueItem): boolean {
  const evals = item.governance_evaluation?.evaluations;
  if (!evals) return false;
  return evals.some((ev) => !ev.passed && ev.type === "constitutional");
}

export default function QueuePage() {
  useEffect(() => { document.title = "Approval Queue | METHEAN"; }, []);
  const { toast } = useToast();

  const [items, setItems] = useState<QueueItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Per-item action state
  const [activeAction, setActiveAction] = useState<{ id: string; type: ActionType } | null>(null);
  const [actionReason, setActionReason] = useState("");
  const [modifyFields, setModifyFields] = useState<{ difficulty?: number; duration?: number; notes?: string }>({});
  const [submitting, setSubmitting] = useState(false);
  const [dismissing, setDismissing] = useState<Set<string>>(new Set());
  const [expandedItem, setExpandedItem] = useState<string | null>(null);
  const isMobile = useMobile();

  useEffect(() => { loadQueue(); }, []);

  async function loadQueue() {
    setLoading(true);
    setError("");
    try {
      const d = await governance.queue();
      setItems(d.items || []);
      setTotal(d.total || 0);
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't load approval queue.");
    } finally {
      setLoading(false);
    }
  }

  async function handleAction(item: QueueItem) {
    if (!activeAction || !item.plan_id) return;
    const { type } = activeAction;

    // Validate
    if (type === "reject" && actionReason.trim().length < 10) return;

    setSubmitting(true);
    try {
      if (type === "approve") {
        await governance.approve(item.plan_id, item.activity_id, actionReason || undefined);
      } else if (type === "reject") {
        await governance.reject(item.plan_id, item.activity_id, actionReason);
      } else if (type === "modify") {
        await governance.modify(item.plan_id, item.activity_id, {
          reason: actionReason || "Modified and approved by parent",
          difficulty: modifyFields.difficulty,
          estimated_minutes: modifyFields.duration,
          notes: modifyFields.notes,
        });
      }

      // Animate out
      setDismissing((prev) => new Set(prev).add(item.activity_id));
      setActiveAction(null);
      setActionReason("");
      setModifyFields({});
      toast(type === "reject" ? "Activity rejected" : type === "modify" ? "Activity modified and approved" : "Activity approved", type === "reject" ? "info" : "success");

      setTimeout(() => {
        setItems((prev) => prev.filter((i) => i.activity_id !== item.activity_id));
        setDismissing((prev) => { const n = new Set(prev); n.delete(item.activity_id); return n; });
        setTotal((t) => Math.max(0, t - 1));
      }, 300);
    } catch (err: any) {
      toast(err?.detail || err?.message || "Action failed", "error");
      setError(err?.detail || err?.message || "Action failed. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  function startAction(id: string, type: ActionType) {
    setActiveAction({ id, type });
    setActionReason("");
    setModifyFields({});
  }

  function cancelAction() {
    setActiveAction(null);
    setActionReason("");
    setModifyFields({});
  }

  // ── Child breakdown for header ──
  const childBreakdown = useMemo(() => {
    const counts: Record<string, number> = {};
    items.forEach((i) => { counts[i.child_name] = (counts[i.child_name] || 0) + 1; });
    return Object.entries(counts);
  }, [items]);

  if (loading) {
    return (
      <div className="max-w-3xl">
        <PageHeader title="Approval Queue" subtitle="Loading your review queue..." />
        <LoadingSkeleton variant="card" count={3} />
      </div>
    );
  }

  return (
    <div className="max-w-3xl">
      <PageHeader
        title="Approval Queue"
        subtitle="AI recommendations awaiting your decision."
      />

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button variant="ghost" size="sm" onClick={() => { setError(""); loadQueue(); }}>Retry</Button>
          </div>
        </Card>
      )}

      {/* ── Queue summary ── */}
      {items.length === 0 ? (
        <Card padding="p-8">
          <div className="text-center">
            <div className="w-14 h-14 rounded-full bg-(--color-success-light) flex items-center justify-center mx-auto mb-4">
              <svg className="w-7 h-7 text-(--color-success)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="text-lg font-semibold text-(--color-text) mb-1">All clear</h2>
            <p className="text-sm text-(--color-text-secondary) mb-1">No activities need your review right now.</p>
            <p className="text-xs text-(--color-text-tertiary)">Your governance rules are working.</p>
          </div>
        </Card>
      ) : (
        <>
          {/* ── Summary header ── */}
          <Card padding="p-4" className="mb-5">
            <div className="flex items-center justify-between flex-wrap gap-3">
              <div>
                <h2 className="text-base font-semibold text-(--color-text)">
                  {items.length} {items.length === 1 ? "activity" : "activities"} awaiting your review
                </h2>
                {childBreakdown.length > 0 && (
                  <div className="flex items-center gap-2 mt-1.5">
                    {childBreakdown.map(([name, count]) => (
                      <span key={name} className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-(--color-page) text-xs text-(--color-text-secondary)">
                        <span className="w-4 h-4 rounded-full bg-(--color-accent-light) text-(--color-accent) text-[9px] font-bold flex items-center justify-center">
                          {name.charAt(0)}
                        </span>
                        {count} for {name}
                      </span>
                    ))}
                  </div>
                )}
              </div>
              <div className="flex items-center gap-1.5 text-xs text-(--color-text-tertiary)">
                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Each review is logged in your governance trail
              </div>
            </div>
          </Card>

          {/* ── Queue items ── */}
          <div className="space-y-3">
            {items.map((item) => {
              const isDismissing = dismissing.has(item.activity_id);
              const isActive = activeAction?.id === item.activity_id;
              const isConstitutional = hasConstitutionalViolation(item);
              const evals = item.governance_evaluation?.evaluations || [];
              const blockingRules = item.governance_evaluation?.blocking_rules || [];
              const isExpanded = expandedItem === item.activity_id;

              async function swipeApprove() {
                if (!item.plan_id) return;
                try {
                  await governance.approve(item.plan_id, item.activity_id);
                  setDismissing((prev) => new Set(prev).add(item.activity_id));
                  toast("Activity approved", "success");
                  setTimeout(() => {
                    setItems((prev) => prev.filter((i) => i.activity_id !== item.activity_id));
                    setDismissing((prev) => { const n = new Set(prev); n.delete(item.activity_id); return n; });
                    setTotal((t) => Math.max(0, t - 1));
                  }, 300);
                } catch (err: any) { toast(err?.detail || "Approve failed", "error"); }
              }

              async function swipeReject() {
                startAction(item.activity_id, "reject");
                setExpandedItem(item.activity_id);
              }

              const cardContent = (
                <div onClick={isMobile && !isActive ? () => setExpandedItem(isExpanded ? null : item.activity_id) : undefined}>
                  <Card padding="p-0" borderLeft={isConstitutional ? "border-l-(--color-constitutional)" : undefined}>
                    {/* ── Top row ── */}
                    <div className="px-5 pt-4 pb-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="text-sm font-bold text-(--color-text)">{item.child_name}</span>
                        <StatusBadge status={item.activity_type} />
                        {item.difficulty != null && item.difficulty > 0 && (
                          <DifficultyDots level={item.difficulty} />
                        )}
                        <span className="ml-auto px-2 py-0.5 rounded-full bg-(--color-warning-light) text-(--color-warning) text-[10px] font-semibold">
                          Requires Review
                        </span>
                      </div>
                    </div>

                    {/* ── Content ── */}
                    <div className="px-5 pt-3 pb-4">
                      <h3 className="text-base font-medium text-(--color-text) mb-2">{item.title}</h3>

                      {/* AI rationale quote block */}
                      {item.ai_rationale && (
                        <div className="bg-(--color-page) border-l-2 border-(--color-accent) rounded-r-[8px] px-3 py-2 mb-3">
                          <span className="text-[10px] font-semibold text-(--color-accent) uppercase tracking-wide block mb-0.5">AI Rationale</span>
                          <p className="text-xs text-(--color-text-secondary) italic leading-relaxed">{item.ai_rationale}</p>
                        </div>
                      )}

                      {/* Metadata row */}
                      <div className="flex items-center gap-3 text-xs text-(--color-text-tertiary) mb-4">
                        {item.scheduled_date && (
                          <span className="flex items-center gap-1">
                            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                              <path strokeLinecap="round" strokeLinejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            {shortDate(item.scheduled_date)}
                          </span>
                        )}
                        {item.estimated_minutes && (
                          <span className="flex items-center gap-1">
                            <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                              <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            {item.estimated_minutes} min
                          </span>
                        )}
                        <span className="text-(--color-text-tertiary)">{item.plan_name}</span>
                      </div>

                      {/* ── Rule evaluation section (ALWAYS visible) ── */}
                      {evals.length > 0 && (
                        <div className="mb-4">
                          <div className="flex items-center gap-1.5 mb-2">
                            {isConstitutional ? (
                              <svg className="w-4 h-4 text-(--color-constitutional)" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 2.18l7 3.12v4.7c0 4.83-3.4 9.36-7 10.5-3.6-1.14-7-5.67-7-10.5V6.3l7-3.12z" />
                              </svg>
                            ) : (
                              <svg className="w-4 h-4 text-(--color-text-tertiary)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                              </svg>
                            )}
                            <span className={cn(
                              "text-xs font-semibold",
                              isConstitutional ? "text-(--color-constitutional)" : "text-(--color-text-secondary)"
                            )}>
                              {isConstitutional ? "Constitutional concern flagged" : "Why this needs your review"}
                            </span>
                          </div>
                          <EvaluationChain evaluations={evals} blockingRules={blockingRules} />
                        </div>
                      )}

                      {/* ── Action area ── */}
                      {!isActive ? (
                        <div className="flex items-center gap-2 pt-3 border-t border-(--color-border)/50">
                          <Button variant="success" size="lg" className="flex-1" onClick={() => startAction(item.activity_id, "approve")}>
                            <span className="flex items-center justify-center gap-1.5">
                              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                              </svg>
                              Approve
                            </span>
                          </Button>
                          <Button variant="danger" size="lg" className="flex-1" onClick={() => startAction(item.activity_id, "reject")}>
                            <span className="flex items-center justify-center gap-1.5">
                              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                              </svg>
                              Reject
                            </span>
                          </Button>
                          <Button variant="secondary" size="lg" onClick={() => startAction(item.activity_id, "modify")}>
                            Modify &amp; Approve
                          </Button>
                        </div>
                      ) : (
                        <div className="pt-3 border-t border-(--color-border)/50 space-y-3">
                          {/* Action confirmation header */}
                          <div className="flex items-center justify-between">
                            <span className={cn(
                              "text-xs font-semibold capitalize",
                              activeAction.type === "approve" ? "text-(--color-success)" :
                              activeAction.type === "reject" ? "text-(--color-danger)" :
                              "text-(--color-accent)"
                            )}>
                              {activeAction.type === "modify" ? "Modify & Approve" : activeAction.type}
                            </span>
                            <button onClick={cancelAction} className="text-xs text-(--color-text-tertiary) hover:text-(--color-text-secondary)">
                              Cancel
                            </button>
                          </div>

                          {/* Modify fields */}
                          {activeAction.type === "modify" && (
                            <div className="grid grid-cols-2 gap-3">
                              <div>
                                <label className="text-[11px] text-(--color-text-tertiary) mb-1 block">Difficulty (1-5)</label>
                                <input
                                  type="number" min={1} max={5}
                                  value={modifyFields.difficulty ?? item.difficulty ?? ""}
                                  onChange={(e) => setModifyFields({ ...modifyFields, difficulty: parseInt(e.target.value) || undefined })}
                                  className="w-full px-2.5 py-1.5 text-sm border border-(--color-border-strong) rounded-[10px] bg-(--color-surface) focus:outline-none focus:ring-1 focus:ring-(--color-accent)"
                                />
                              </div>
                              <div>
                                <label className="text-[11px] text-(--color-text-tertiary) mb-1 block">Duration (minutes)</label>
                                <input
                                  type="number" min={1}
                                  value={modifyFields.duration ?? item.estimated_minutes ?? ""}
                                  onChange={(e) => setModifyFields({ ...modifyFields, duration: parseInt(e.target.value) || undefined })}
                                  className="w-full px-2.5 py-1.5 text-sm border border-(--color-border-strong) rounded-[10px] bg-(--color-surface) focus:outline-none focus:ring-1 focus:ring-(--color-accent)"
                                />
                              </div>
                              <div className="col-span-2">
                                <label className="text-[11px] text-(--color-text-tertiary) mb-1 block">Notes</label>
                                <input
                                  value={modifyFields.notes ?? ""}
                                  onChange={(e) => setModifyFields({ ...modifyFields, notes: e.target.value })}
                                  placeholder="Any adjustments to note..."
                                  className="w-full px-2.5 py-1.5 text-sm border border-(--color-border-strong) rounded-[10px] bg-(--color-surface) focus:outline-none focus:ring-1 focus:ring-(--color-accent)"
                                />
                              </div>
                            </div>
                          )}

                          {/* Reason field */}
                          <div>
                            <label className="text-[11px] text-(--color-text-tertiary) mb-1 block">
                              {activeAction.type === "reject" ? "Reason (required, min 10 characters)" : "Note (optional)"}
                            </label>
                            <textarea
                              value={actionReason}
                              onChange={(e) => setActionReason(e.target.value)}
                              placeholder={
                                activeAction.type === "reject"
                                  ? "Explain why you're rejecting this recommendation..."
                                  : activeAction.type === "modify"
                                  ? "Explain your modifications..."
                                  : "Add an optional note about your approval..."
                              }
                              rows={2}
                              className="w-full px-3 py-2 text-sm border border-(--color-border-strong) rounded-[10px] bg-(--color-surface) resize-none focus:outline-none focus:ring-1 focus:ring-(--color-accent)"
                              autoFocus
                            />
                            {activeAction.type === "reject" && actionReason.length > 0 && actionReason.length < 10 && (
                              <p className="text-[10px] text-(--color-danger) mt-1">{10 - actionReason.length} more characters needed</p>
                            )}
                          </div>

                          {/* Confirm / Cancel */}
                          <div className="flex gap-2">
                            <Button
                              variant={activeAction.type === "reject" ? "danger" : "success"}
                              size="md"
                              className="flex-1"
                              disabled={submitting || (activeAction.type === "reject" && actionReason.trim().length < 10)}
                              onClick={() => handleAction(item)}
                            >
                              {submitting ? "Submitting..." :
                                activeAction.type === "approve" ? "Confirm Approval" :
                                activeAction.type === "reject" ? "Confirm Rejection" :
                                "Approve with Modifications"}
                            </Button>
                            <Button variant="ghost" size="md" onClick={cancelAction} disabled={submitting}>
                              Cancel
                            </Button>
                          </div>
                        </div>
                      )}
                    </div>
                  </Card>
                </div>
              );

              return (
                <div
                  key={item.activity_id}
                  className="transition-all duration-300 overflow-hidden"
                  style={{
                    opacity: isDismissing ? 0 : 1,
                    maxHeight: isDismissing ? 0 : 1200,
                    marginBottom: isDismissing ? 0 : undefined,
                    transform: isDismissing ? "translateX(-20px)" : "translateX(0)",
                  }}
                >
                  {isMobile ? (
                    <SwipeAction
                      onSwipeRight={swipeApprove}
                      onSwipeLeft={swipeReject}
                      leftLabel="Approve"
                      rightLabel="Reject"
                      leftColor="var(--color-success)"
                      rightColor="var(--color-danger)"
                    >
                      {cardContent}
                    </SwipeAction>
                  ) : cardContent}
                </div>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
}
