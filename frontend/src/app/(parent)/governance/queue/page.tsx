"use client";

import { useEffect, useState, useMemo } from "react";
import Link from "next/link";
import { governance, type GovernanceRule } from "@/lib/api";
import { useToast } from "@/components/Toast";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import StatusBadge from "@/components/StatusBadge";
import Badge from "@/components/ui/Badge";
import ProgressRing from "@/components/ui/ProgressRing";
import Tooltip from "@/components/ui/Tooltip";
import EvaluationChain from "@/components/EvaluationChain";
import BottomSheet from "@/components/BottomSheet";
import { ShieldIcon } from "@/components/ConstitutionalCeremony";
import { cn } from "@/lib/cn";
import { shortDate } from "@/lib/format";
import { useMobile } from "@/lib/useMobile";
import PullToRefresh from "@/components/PullToRefresh";
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

// Difficulty dots — kept as a small visual cue alongside the new
// ProgressRing-based confidence read.
function DifficultyDots({ level }: { level: number }) {
  return (
    <div className="flex items-center gap-0.5">
      {[1, 2, 3, 4, 5].map((i) => (
        <span
          key={i}
          className={cn(
            "w-2 h-2 rounded-full",
            i <= level ? "bg-(--color-warning)" : "bg-(--color-border)",
          )}
        />
      ))}
    </div>
  );
}

function hasConstitutionalViolation(item: QueueItem): boolean {
  const evals = item.governance_evaluation?.evaluations;
  if (!evals) return false;
  return evals.some((ev) => !ev.passed && ev.type === "constitutional");
}

/** Confidence as the ratio of passed-to-total evaluations. With no
 *  evaluations recorded, the AI didn't flag anything — render as 100%
 *  so the ring reads "no concerns". With blocking rules, penalize. */
function confidenceFor(item: QueueItem): number {
  const evals = item.governance_evaluation?.evaluations || [];
  const blocking = item.governance_evaluation?.blocking_rules || [];
  if (evals.length === 0) return blocking.length === 0 ? 100 : 50;
  const passed = evals.filter((e) => e.passed).length;
  const base = Math.round((passed / evals.length) * 100);
  return blocking.length > 0 ? Math.min(base, 60) : base;
}

/** Threshold above which "Approve all routine" treats an item as low-risk
 *  enough to batch-approve. Constitutional violations are excluded
 *  outright. */
const ROUTINE_CONFIDENCE_THRESHOLD = 90;

export default function QueuePage() {
  useEffect(() => { document.title = "Governance Queue | METHEAN"; }, []);
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
  const [expandedReasoning, setExpandedReasoning] = useState<Set<string>>(new Set());
  const [batchApproving, setBatchApproving] = useState(false);

  // Constitutional rules sidebar (desktop) / sheet (mobile)
  const [rules, setRules] = useState<GovernanceRule[]>([]);
  const [rulesOpen, setRulesOpen] = useState(false);

  const isMobile = useMobile();

  useEffect(() => { loadQueue(); loadRules(); }, []);

  async function loadQueue() {
    setLoading(true);
    setError("");
    try {
      const d = await governance.queue();
      setItems(d.items || []);
      setTotal(d.total || 0);
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't load governance queue.");
    } finally {
      setLoading(false);
    }
  }

  async function loadRules() {
    try {
      const r = await governance.rules();
      const rulesList = (r as any).items || r;
      setRules(Array.isArray(rulesList) ? rulesList : []);
    } catch {
      setRules([]);
    }
  }

  async function handleAction(item: QueueItem) {
    if (!activeAction || !item.plan_id) return;
    const { type } = activeAction;

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

      setDismissing((prev) => new Set(prev).add(item.activity_id));
      setActiveAction(null);
      setActionReason("");
      setModifyFields({});
      toast(
        type === "reject" ? "Proposal rejected" : type === "modify" ? "Proposal modified and approved" : "Proposal approved",
        type === "reject" ? "info" : "success",
      );

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

  function toggleReasoning(id: string) {
    setExpandedReasoning((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  // Items eligible for "Approve all routine" — high confidence and no
  // constitutional violations. Computed fresh from current items.
  const routineCandidates = useMemo(
    () =>
      items.filter(
        (it) =>
          !hasConstitutionalViolation(it) && confidenceFor(it) >= ROUTINE_CONFIDENCE_THRESHOLD,
      ),
    [items],
  );

  async function batchApproveRoutine() {
    if (routineCandidates.length === 0 || batchApproving) return;
    setBatchApproving(true);
    const approvedIds = new Set<string>();
    try {
      for (const it of routineCandidates) {
        if (!it.plan_id) continue;
        try {
          await governance.approve(it.plan_id, it.activity_id, "Batch-approved (routine, high AI confidence)");
          approvedIds.add(it.activity_id);
        } catch {
          // continue on individual failures so one bad item doesn't kill the batch
        }
      }
      if (approvedIds.size > 0) {
        setDismissing((prev) => {
          const next = new Set(prev);
          approvedIds.forEach((id) => next.add(id));
          return next;
        });
        toast(`Approved ${approvedIds.size} routine ${approvedIds.size === 1 ? "proposal" : "proposals"}`, "success");
        setTimeout(() => {
          setItems((prev) => prev.filter((i) => !approvedIds.has(i.activity_id)));
          setDismissing((prev) => {
            const n = new Set(prev);
            approvedIds.forEach((id) => n.delete(id));
            return n;
          });
          setTotal((t) => Math.max(0, t - approvedIds.size));
        }, 300);
      } else {
        toast("Couldn't batch-approve any proposals", "error");
      }
    } finally {
      setBatchApproving(false);
    }
  }

  const childBreakdown = useMemo(() => {
    const counts: Record<string, number> = {};
    items.forEach((i) => { counts[i.child_name] = (counts[i.child_name] || 0) + 1; });
    return Object.entries(counts);
  }, [items]);

  // ── Loading ──
  if (loading) {
    return (
      <div className="max-w-3xl">
        <header className="mb-6">
          <div className="flex items-center gap-2 mb-2">
            <ShieldIcon size={22} className="text-(--color-constitutional)" />
            <h1 className="text-[22px] sm:text-[26px] font-semibold tracking-tight text-(--color-text)">Governance Queue</h1>
          </div>
          <p className="text-sm text-(--color-text-secondary)">Loading proposals…</p>
        </header>
        <LoadingSkeleton variant="card" count={3} />
      </div>
    );
  }

  // ── Rules side panel content (shared between desktop sidebar and mobile sheet) ──
  function RulesPanel() {
    return (
      <div className="space-y-3">
        <div className="flex items-center gap-2">
          <ShieldIcon size={16} className="text-(--color-constitutional)" />
          <h3 className="text-sm font-semibold text-(--color-text)">Active rules</h3>
        </div>
        {rules.length === 0 ? (
          <p className="text-xs text-(--color-text-tertiary)">No rules ratified yet.</p>
        ) : (
          <ul className="space-y-2">
            {rules.filter((r: any) => r.is_active !== false).map((r: any) => {
              const isConstitutional = r.tier === "constitutional";
              return (
                <li
                  key={r.id}
                  className="rounded-[10px] border border-(--color-border) bg-(--color-surface) px-3 py-2"
                >
                  <div className="flex items-start justify-between gap-2 mb-1">
                    <span className="text-[13px] font-medium text-(--color-text) leading-tight">
                      {r.name || r.rule_type}
                    </span>
                    <Badge variant={isConstitutional ? "constitutional" : "info"} withDot={false}>
                      {isConstitutional ? "Constitutional" : "Standard"}
                    </Badge>
                  </div>
                  {r.created_at && (
                    <p className="text-[11px] text-(--color-text-tertiary)">
                      Ratified {shortDate(r.created_at)}
                    </p>
                  )}
                </li>
              );
            })}
          </ul>
        )}
        <Link
          href="/governance/rules"
          className="block text-xs text-(--color-accent) hover:underline pt-1"
        >
          Manage rules →
        </Link>
      </div>
    );
  }

  const auditFooter = (
    <div className="mt-8 flex items-center justify-between gap-3 px-1 text-xs text-(--color-text-tertiary)">
      <div className="flex items-center gap-2">
        <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2} aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
        </svg>
        Every decision is recorded immutably.
      </div>
      <Link href="/governance/trace" className="text-(--color-accent) hover:underline font-medium">
        View full audit trail →
      </Link>
    </div>
  );

  const content = (
    <div className="lg:grid lg:grid-cols-[minmax(0,1fr)_280px] lg:gap-8">
      <div className="max-w-3xl">
        {/* ── Hero ── */}
        <header className="mb-6 animate-fade-up">
          <div className="flex items-center gap-2 mb-2">
            <ShieldIcon size={22} className="text-(--color-constitutional)" />
            <h1 className="text-[22px] sm:text-[26px] font-semibold tracking-tight text-(--color-text)">
              Governance Queue
            </h1>
          </div>
          {items.length === 0 ? (
            <p className="text-sm text-(--color-success)">
              All proposals reviewed. Your governance is current.
            </p>
          ) : (
            <p className="text-sm text-(--color-text-secondary)">
              {items.length} {items.length === 1 ? "proposal" : "proposals"} awaiting review.
            </p>
          )}
          {isMobile && (
            <button
              onClick={() => setRulesOpen(true)}
              className="mt-3 inline-flex items-center gap-1.5 text-xs text-(--color-accent) hover:underline"
            >
              <ShieldIcon size={12} /> View active rules
            </button>
          )}
        </header>

        {error && (
          <Card className="mb-4" borderLeft="border-l-(--color-danger)">
            <div className="flex items-center justify-between gap-4">
              <p className="text-sm text-(--color-danger)">{error}</p>
              <Button variant="ghost" size="sm" onClick={() => { setError(""); loadQueue(); }}>Retry</Button>
            </div>
          </Card>
        )}

        {/* ── Empty state ── */}
        {items.length === 0 ? (
          <>
            <Card className="text-center py-10 animate-fade-up stagger-2">
              <div
                className="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center"
                style={{
                  background:
                    "radial-gradient(circle, rgba(198,162,78,0.18) 0%, rgba(198,162,78,0) 65%)",
                }}
              >
                <ShieldIcon size={32} className="text-(--color-brand-gold)" />
              </div>
              <h2 className="text-[18px] font-semibold text-(--color-text) mb-1">
                Your governance is current
              </h2>
              <p className="text-sm text-(--color-text-secondary) mb-5">
                METHEAN&apos;s AI is operating within your rules.
              </p>
              <div className="flex items-center justify-center gap-3 flex-wrap">
                <Link
                  href="/governance/trace"
                  className="text-sm text-(--color-accent) hover:underline"
                >
                  Review governance history
                </Link>
                <span className="text-(--color-text-tertiary)" aria-hidden="true">·</span>
                <Link
                  href="/governance/rules"
                  className="text-sm text-(--color-accent) hover:underline"
                >
                  Update rules
                </Link>
              </div>
            </Card>
            {auditFooter}
          </>
        ) : (
          <>
            {/* ── Summary + batch approve ── */}
            <div className="mb-5 flex items-start justify-between gap-3 flex-wrap animate-fade-up stagger-1">
              {childBreakdown.length > 0 && (
                <div className="flex items-center gap-2 flex-wrap">
                  {childBreakdown.map(([name, count]) => (
                    <span
                      key={name}
                      className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-(--color-surface) border border-(--color-border) text-xs text-(--color-text-secondary)"
                    >
                      <span className="w-4 h-4 rounded-full bg-(--color-accent-light) text-(--color-accent) text-[9px] font-bold flex items-center justify-center">
                        {name.charAt(0)}
                      </span>
                      {count} for {name}
                    </span>
                  ))}
                </div>
              )}
              {items.length >= 3 && routineCandidates.length > 0 && (
                <Tooltip content="Approves proposals where AI confidence exceeds your threshold. You can always review them later in the audit trail.">
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={batchApproveRoutine}
                    disabled={batchApproving}
                  >
                    {batchApproving
                      ? "Approving…"
                      : `Approve all routine (${routineCandidates.length})`}
                  </Button>
                </Tooltip>
              )}
            </div>

            {/* ── Proposal cards ── */}
            <div className="space-y-3">
              {items.map((item, idx) => {
                const isDismissing = dismissing.has(item.activity_id);
                const isActive = activeAction?.id === item.activity_id;
                const isConstitutional = hasConstitutionalViolation(item);
                const evals = item.governance_evaluation?.evaluations || [];
                const blockingRules = item.governance_evaluation?.blocking_rules || [];
                const isReasoningOpen = expandedReasoning.has(item.activity_id);
                const confidence = confidenceFor(item);
                const staggerClass = `stagger-${Math.min(8, idx + 1)}`;

                async function swipeApprove() {
                  if (!item.plan_id) return;
                  try {
                    await governance.approve(item.plan_id, item.activity_id);
                    setDismissing((prev) => new Set(prev).add(item.activity_id));
                    toast("Proposal approved", "success");
                    setTimeout(() => {
                      setItems((prev) => prev.filter((i) => i.activity_id !== item.activity_id));
                      setDismissing((prev) => { const n = new Set(prev); n.delete(item.activity_id); return n; });
                      setTotal((t) => Math.max(0, t - 1));
                    }, 300);
                  } catch (err: any) { toast(err?.detail || "Approve failed", "error"); }
                }

                async function swipeReject() {
                  startAction(item.activity_id, "reject");
                }

                const cardContent = (
                  <Card
                    padding="p-0"
                    borderLeft={
                      isConstitutional
                        ? "border-l-(--color-danger)"
                        : "border-l-(--color-constitutional)"
                    }
                  >
                    {/* ── Top row: child + type + flag + confidence ring ── */}
                    <div className="px-5 pt-4 pb-3 flex items-start gap-4">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 flex-wrap mb-2">
                          <span className="text-sm font-semibold text-(--color-text)">{item.child_name}</span>
                          <StatusBadge status={item.activity_type} />
                          {item.difficulty != null && item.difficulty > 0 && (
                            <DifficultyDots level={item.difficulty} />
                          )}
                          {isConstitutional ? (
                            <Badge variant="danger">Constitutional concern</Badge>
                          ) : (
                            <Badge variant="constitutional">Awaiting review</Badge>
                          )}
                        </div>
                        <h3 className="text-base font-medium text-(--color-text) mb-1">
                          {item.title}
                        </h3>
                        <div className="flex items-center gap-3 text-xs text-(--color-text-tertiary)">
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
                          <span className="truncate">{item.plan_name}</span>
                        </div>
                      </div>
                      <Tooltip
                        content={`AI confidence ${confidence}% (passed evaluations)`}
                        placement="top"
                      >
                        <ProgressRing
                          value={confidence}
                          size={56}
                          strokeWidth={5}
                          tone={isConstitutional ? "danger" : confidence >= ROUTINE_CONFIDENCE_THRESHOLD ? "success" : "accent"}
                        />
                      </Tooltip>
                    </div>

                    {/* ── AI rationale + collapsible reasoning ── */}
                    {item.ai_rationale && (
                      <div className="px-5 pb-3">
                        <div className="rounded-[10px] glass border border-(--color-border) px-3 py-2.5">
                          <span className="text-[10px] font-semibold text-(--color-accent) uppercase tracking-wide block mb-1">
                            AI recommendation
                          </span>
                          <p className="text-sm text-(--color-text-secondary) italic leading-relaxed">
                            {item.ai_rationale}
                          </p>
                        </div>
                      </div>
                    )}

                    {evals.length > 0 && (
                      <div className="px-5 pb-3">
                        <button
                          onClick={() => toggleReasoning(item.activity_id)}
                          className="flex items-center gap-1.5 text-xs font-medium text-(--color-text-secondary) hover:text-(--color-text)"
                          aria-expanded={isReasoningOpen}
                        >
                          <svg
                            className={cn(
                              "w-3 h-3 transition-transform",
                              isReasoningOpen && "rotate-90",
                            )}
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            strokeWidth={2.5}
                          >
                            <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                          </svg>
                          {isReasoningOpen ? "Hide" : "View"} reasoning
                          <span className="text-(--color-text-tertiary) font-normal">
                            ({evals.length} {evals.length === 1 ? "rule" : "rules"} evaluated)
                          </span>
                        </button>
                        {isReasoningOpen && (
                          <div className="mt-2 rounded-[10px] glass border border-(--color-border) p-3 animate-fade-up">
                            <EvaluationChain evaluations={evals} blockingRules={blockingRules} />
                          </div>
                        )}
                      </div>
                    )}

                    {/* ── Action area ── */}
                    {!isActive ? (
                      <div className="px-5 pt-3 pb-4 border-t border-(--color-border)/50 space-y-2">
                        <div className="flex items-center gap-2">
                          <Button
                            variant="success"
                            size="md"
                            className="flex-1"
                            onClick={() => startAction(item.activity_id, "approve")}
                          >
                            Approve
                          </Button>
                          <Button
                            variant="secondary"
                            size="md"
                            className="flex-1"
                            onClick={() => startAction(item.activity_id, "modify")}
                          >
                            Modify
                          </Button>
                        </div>
                        <div className="flex items-center justify-between gap-3 pt-1">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => startAction(item.activity_id, "reject")}
                          >
                            Reject
                          </Button>
                          <Link
                            href="/governance/trace"
                            className="text-xs text-(--color-accent) hover:underline"
                          >
                            Inspect AI prompt + response →
                          </Link>
                        </div>
                      </div>
                    ) : (
                      <div className="px-5 pt-3 pb-4 border-t border-(--color-border)/50 space-y-3">
                        <div className="flex items-center justify-between">
                          <span
                            className={cn(
                              "text-xs font-semibold capitalize",
                              activeAction.type === "approve" ? "text-(--color-success)"
                              : activeAction.type === "reject" ? "text-(--color-danger)"
                              : "text-(--color-accent)",
                            )}
                          >
                            {activeAction.type === "modify" ? "Modify & approve" : activeAction.type}
                          </span>
                          <button
                            onClick={cancelAction}
                            className="text-xs text-(--color-text-tertiary) hover:text-(--color-text-secondary)"
                          >
                            Cancel
                          </button>
                        </div>

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

                        <div className="flex gap-2">
                          <Button
                            variant={activeAction.type === "reject" ? "danger" : "success"}
                            size="md"
                            className="flex-1"
                            disabled={submitting || (activeAction.type === "reject" && actionReason.trim().length < 10)}
                            onClick={() => handleAction(item)}
                          >
                            {submitting ? "Submitting..." :
                              activeAction.type === "approve" ? "Confirm approval" :
                              activeAction.type === "reject" ? "Confirm rejection" :
                              "Approve with modifications"}
                          </Button>
                          <Button variant="ghost" size="md" onClick={cancelAction} disabled={submitting}>
                            Cancel
                          </Button>
                        </div>
                      </div>
                    )}
                  </Card>
                );

                return (
                  <div
                    key={item.activity_id}
                    className={cn(
                      "transition-all duration-300 overflow-hidden",
                      !isDismissing && `animate-fade-up ${staggerClass}`,
                    )}
                    style={{
                      opacity: isDismissing ? 0 : undefined,
                      transform: isDismissing ? "translateX(-20px) scale(0.98)" : undefined,
                      maxHeight: isDismissing ? 0 : undefined,
                      marginBottom: isDismissing ? 0 : undefined,
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
            {auditFooter}
          </>
        )}
      </div>

      {/* Desktop sidebar */}
      {!isMobile && (
        <aside className="hidden lg:block sticky top-6 self-start animate-slide-left stagger-2">
          <div className="rounded-[14px] border border-(--color-border) bg-(--color-surface) shadow-[var(--shadow-card)] p-4">
            <RulesPanel />
          </div>
        </aside>
      )}
    </div>
  );

  return (
    <>
      {isMobile ? <PullToRefresh onRefresh={loadQueue}>{content}</PullToRefresh> : content}
      {isMobile && (
        <BottomSheet open={rulesOpen} onClose={() => setRulesOpen(false)}>
          <div className="px-5 pb-6 pt-2">
            <RulesPanel />
          </div>
        </BottomSheet>
      )}
    </>
  );
}
