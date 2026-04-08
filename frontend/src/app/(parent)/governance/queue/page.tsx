"use client";

import { useEffect, useState } from "react";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import EmptyState from "@/components/ui/EmptyState";
import EvaluationChain from "@/components/EvaluationChain";
import { cn } from "@/lib/cn";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

function getCsrf(): string | undefined {
  if (typeof document === "undefined") return undefined;
  const m = document.cookie.match(/(?:^|; )csrf_token=([^;]*)/);
  return m ? decodeURIComponent(m[1]) : undefined;
}

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

export default function QueuePage() {
  useEffect(() => { document.title = "Approval Queue | METHEAN"; }, []);

  const [items, setItems] = useState<QueueItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [dismissing, setDismissing] = useState<Set<string>>(new Set());
  const [expandedDetail, setExpandedDetail] = useState<string | null>(null);
  const [actionForm, setActionForm] = useState<{ id: string; type: "approve" | "reject" } | null>(null);
  const [actionReason, setActionReason] = useState("");

  useEffect(() => { loadQueue(); }, []);

  async function loadQueue() {
    setLoading(true);
    setError("");
    try {
      const resp = await fetch(`${API}/governance/queue?limit=100`, { credentials: "include" });
      if (resp.ok) { const d = await resp.json(); setItems(d.items || []); setTotal(d.total || 0); }
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't load approval queue.");
    } finally { setLoading(false); }
  }

  async function doAction(activityId: string, planId: string, action: "approve" | "reject", reason?: string) {
    setDismissing((prev) => new Set(prev).add(activityId));
    const csrf = getCsrf();
    const body = reason ? JSON.stringify({ reason }) : (action === "reject" ? JSON.stringify({ reason: "Rejected by parent" }) : undefined);
    await fetch(`${API}/plans/${planId}/activities/${activityId}/${action}`, {
      method: "PUT", credentials: "include",
      headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
      body,
    });
    setActionForm(null);
    setActionReason("");
    setTimeout(() => {
      setItems((prev) => prev.filter((i) => i.activity_id !== activityId));
      setDismissing((prev) => { const n = new Set(prev); n.delete(activityId); return n; });
      setTotal((t) => Math.max(0, t - 1));
      setSelected((prev) => { const n = new Set(prev); n.delete(activityId); return n; });
    }, 300);
  }

  async function bulkApprove() {
    for (const item of items) {
      if (selected.has(item.activity_id) && item.plan_id) {
        await doAction(item.activity_id, item.plan_id, "approve");
      }
    }
  }

  function toggleSelect(id: string) { setSelected((p) => { const n = new Set(p); n.has(id) ? n.delete(id) : n.add(id); return n; }); }
  function toggleAll() { selected.size === items.length ? setSelected(new Set()) : setSelected(new Set(items.map((i) => i.activity_id))); }

  if (loading) return <div className="max-w-4xl"><LoadingSkeleton variant="list" count={6} /></div>;

  // Group by child
  const byChild: Record<string, QueueItem[]> = {};
  items.forEach((item) => { const k = item.child_name || "Unknown"; (byChild[k] ||= []).push(item); });

  return (
    <div className="max-w-4xl">
      <PageHeader
        title="Approval Queue"
        subtitle={total === 0 ? "All caught up!" : `${total} activities need your review`}
        actions={selected.size > 0 ? (
          <Button variant="success" size="md" onClick={bulkApprove}>
            Approve Selected ({selected.size})
          </Button>
        ) : undefined}
      />

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button variant="ghost" size="sm" onClick={() => { setError(""); loadQueue(); }}>Retry</Button>
          </div>
        </Card>
      )}

      {total === 0 ? (
        <EmptyState icon="check" title="All caught up!" description="No activities need your review right now." />
      ) : (
        <>
          {items.length > 1 && (
            <div className="mb-3">
              <button onClick={toggleAll} className="text-xs text-(--color-accent) hover:underline">
                {selected.size === items.length ? "Deselect all" : "Select all"}
              </button>
            </div>
          )}
          <div className="space-y-8">
            {Object.entries(byChild).map(([childName, childItems]) => (
              <div key={childName}>
                <div className="flex items-center gap-2 mb-3">
                  <span className="w-7 h-7 rounded-full bg-(--color-accent-light) text-(--color-accent) text-xs font-bold flex items-center justify-center">
                    {childName.charAt(0)}
                  </span>
                  <h3 className="text-sm font-semibold text-(--color-text)">{childName}</h3>
                  <span className="text-xs text-(--color-text-tertiary)">({childItems.length})</span>
                </div>
                <div className="space-y-2 ml-9">
                  {childItems.map((item) => (
                    <Card
                      key={item.activity_id}
                      padding="p-4"
                      className={`transition-all duration-300 ${
                        dismissing.has(item.activity_id) ? "opacity-0 -translate-x-4" : "opacity-100"
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        <input type="checkbox" checked={selected.has(item.activity_id)}
                          onChange={() => toggleSelect(item.activity_id)} className="mt-1 rounded" />
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 flex-wrap">
                            <span className="text-sm font-medium text-(--color-text)">{item.title}</span>
                            <span className="text-[10px] px-1.5 py-0.5 bg-(--color-page) text-(--color-text-secondary) rounded font-medium uppercase">{item.activity_type}</span>
                            {item.difficulty && (
                              <span className="text-xs">
                                <span className="text-(--color-warning)">{"●".repeat(item.difficulty)}</span>
                                <span className="text-(--color-text-tertiary)">{"●".repeat(5 - item.difficulty)}</span>
                              </span>
                            )}
                            {item.estimated_minutes && <span className="text-xs text-(--color-text-tertiary)">{item.estimated_minutes}m</span>}
                            {item.scheduled_date && <span className="text-xs text-(--color-text-tertiary)">{item.scheduled_date}</span>}
                          </div>
                          <div className="text-[11px] text-(--color-text-tertiary) mt-0.5">{item.plan_name}</div>
                          {item.ai_rationale && (
                            <div className="text-xs bg-(--color-accent-light) border border-(--color-accent)/20 rounded px-2.5 py-1.5 mt-2">
                              <span className="font-medium text-(--color-accent)">AI rationale: </span>
                              <span className="text-(--color-accent) italic">{item.ai_rationale}</span>
                            </div>
                          )}
                        </div>
                        {/* Action buttons or form */}
                        {actionForm?.id !== item.activity_id ? (
                          <div className="flex gap-2 shrink-0">
                            <Button variant="success" size="sm" onClick={() => { setActionForm({ id: item.activity_id, type: "approve" }); setActionReason(""); }}>Approve</Button>
                            <Button variant="danger" size="sm" onClick={() => { setActionForm({ id: item.activity_id, type: "reject" }); setActionReason(""); }}>Reject</Button>
                          </div>
                        ) : (
                          <div className="flex flex-col gap-2 shrink-0 w-48">
                            <input
                              value={actionReason}
                              onChange={(e) => setActionReason(e.target.value)}
                              placeholder={actionForm.type === "reject" ? "Reason (required)" : "Note (optional)"}
                              className="px-2 py-1.5 text-xs border border-(--color-border) rounded-[10px] bg-(--color-surface)"
                              autoFocus
                            />
                            <div className="flex gap-1.5">
                              <Button
                                variant={actionForm.type === "approve" ? "success" : "danger"}
                                size="sm"
                                disabled={actionForm.type === "reject" && !actionReason.trim()}
                                onClick={() => item.plan_id && doAction(item.activity_id, item.plan_id, actionForm.type, actionReason || undefined)}
                              >
                                Confirm
                              </Button>
                              <Button variant="ghost" size="sm" onClick={() => setActionForm(null)}>Cancel</Button>
                            </div>
                          </div>
                        )}
                      </div>

                      {/* Evaluation chain */}
                      {item.governance_evaluation?.evaluations && item.governance_evaluation.evaluations.length > 0 && (
                        <div className="mt-3 pt-3 border-t border-(--color-border)/50">
                          <button onClick={() => setExpandedDetail(expandedDetail === item.activity_id ? null : item.activity_id)}
                            className="text-xs font-medium text-(--color-accent) hover:underline">
                            {expandedDetail === item.activity_id ? "Hide evaluation" : "Why is this here?"}
                          </button>
                          {expandedDetail === item.activity_id && (
                            <div className="mt-2">
                              <EvaluationChain
                                evaluations={item.governance_evaluation.evaluations}
                                blockingRules={item.governance_evaluation.blocking_rules || []}
                              />
                            </div>
                          )}
                        </div>
                      )}
                    </Card>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
