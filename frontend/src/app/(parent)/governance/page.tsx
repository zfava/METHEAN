"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { governance, type GovernanceEvent, type GovernanceRule } from "@/lib/api";
import { relativeTime } from "@/lib/format";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import SectionHeader from "@/components/ui/SectionHeader";
import EmptyState from "@/components/ui/EmptyState";
import StatusBadge from "@/components/StatusBadge";

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
  child_name: string;
  plan_id: string | null;
}


export default function GovernanceOverviewPage() {
  useEffect(() => { document.title = "Governance | METHEAN"; }, []);

  const [queue, setQueue] = useState<QueueItem[]>([]);
  const [queueTotal, setQueueTotal] = useState(0);
  const [rules, setRules] = useState<GovernanceRule[]>([]);
  const [events, setEvents] = useState<GovernanceEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [dismissing, setDismissing] = useState<Set<string>>(new Set());
  const [philSummary, setPhilSummary] = useState("");

  useEffect(() => { load(); }, []);

  async function load() {
    try {
      const [qResp, rResp, eResp] = await Promise.all([
        fetch(`${API}/governance/queue?limit=3`, { credentials: "include" }).then((r) => r.ok ? r.json() : { items: [], total: 0 }),
        governance.rules(),
        governance.events(5),
      ]);
      setQueue(qResp.items || []);
      setQueueTotal(qResp.total || 0);
      setRules((rResp as any).items || rResp);
      setEvents(((eResp as any).items || eResp).slice(0, 5));

      // Philosophy summary
      try {
        const philResp = await fetch(`${API}/household/philosophy`, { credentials: "include" });
        if (philResp.ok) {
          const phil = await philResp.json();
          const parts = [];
          if (phil.educational_philosophy) parts.push(phil.educational_philosophy.replace(/_/g, " "));
          if (phil.religious_framework && phil.religious_framework !== "secular") parts.push(phil.religious_framework);
          if (phil.ai_autonomy_level) parts.push(phil.ai_autonomy_level.replace(/_/g, " "));
          setPhilSummary(parts.join(" \u00b7 ") || "Not configured");
        }
      } catch {}
    } catch {} finally { setLoading(false); }
  }

  async function handleAction(item: QueueItem, action: "approve" | "reject") {
    if (!item.plan_id) return;
    setDismissing((prev) => new Set(prev).add(item.activity_id));

    const csrf = getCsrf();
    const url = `${API}/plans/${item.plan_id}/activities/${item.activity_id}/${action}`;
    const body = action === "reject" ? JSON.stringify({ reason: "Rejected from governance overview" }) : undefined;
    await fetch(url, {
      method: "PUT", credentials: "include",
      headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
      body,
    });

    // Animate out then reload
    setTimeout(() => load(), 300);
  }

  // Rule type counts
  const ruleCounts: Record<string, number> = {};
  rules.forEach((r) => { ruleCounts[r.rule_type] = (ruleCounts[r.rule_type] || 0) + 1; });

  const ruleIcons: Record<string, { icon: string; label: string }> = {
    approval_required: { icon: "\u26E8", label: "approval rules" },
    pace_limit: { icon: "\u23F1", label: "pace limits" },
    schedule_constraint: { icon: "\u2637", label: "schedule constraints" },
    content_filter: { icon: "\u2616", label: "content filters" },
    ai_boundary: { icon: "\u2B21", label: "AI boundaries" },
  };

  if (loading) return <div className="max-w-4xl space-y-6"><LoadingSkeleton variant="card" count={3} /><LoadingSkeleton variant="list" count={4} /></div>;

  return (
    <div className="max-w-4xl">
      <PageHeader title="Governance" subtitle="You control what the AI can and cannot do." />

      {/* ── PHILOSOPHY SUMMARY ── */}
      {philSummary && (
        <Card href="/governance/philosophy" className="mb-6" padding="px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-xs text-(--color-text-tertiary)">Philosophy:</span>
              <span className="text-sm font-medium text-(--color-text) capitalize">{philSummary}</span>
            </div>
            <span className="text-xs text-(--color-accent)">Edit &rarr;</span>
          </div>
        </Card>
      )}

      {/* ── APPROVAL QUEUE PREVIEW ── */}
      <div className="mb-8">
        <SectionHeader
          title="Pending Your Review"
          action={queueTotal > 0 ? `View full queue (${queueTotal}) →` : undefined}
          actionHref={queueTotal > 0 ? "/governance/queue" : undefined}
        />

        {queue.length === 0 ? (
          <EmptyState icon="check" title="All Clear" description="No activities need your review." />
        ) : (
          <div className="space-y-2">
            {queue.map((item) => (
              <Card
                key={item.activity_id}
                padding="p-4"
                className={`transition-all duration-300 ${
                  dismissing.has(item.activity_id) ? "opacity-0 scale-95" : "opacity-100"
                }`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="w-6 h-6 rounded-full bg-(--color-accent-light) text-(--color-accent) text-[10px] font-bold flex items-center justify-center shrink-0">
                        {item.child_name.charAt(0)}
                      </span>
                      <span className="text-xs text-(--color-text-secondary)">{item.child_name}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-(--color-text)">{item.title}</span>
                      <span className="text-[10px] px-1.5 py-0.5 bg-(--color-page) text-(--color-text-secondary) rounded font-medium uppercase">{item.activity_type}</span>
                      {item.difficulty && (
                        <span className="text-xs text-(--color-warning)">
                          {"●".repeat(item.difficulty)}
                          <span className="text-(--color-text-tertiary)">{"●".repeat(5 - item.difficulty)}</span>
                        </span>
                      )}
                      {item.estimated_minutes && <span className="text-xs text-(--color-text-tertiary)">{item.estimated_minutes}m</span>}
                    </div>
                    {item.ai_rationale && (
                      <p className="text-xs text-(--color-text-secondary) italic mt-1.5">&ldquo;{item.ai_rationale}&rdquo;</p>
                    )}
                  </div>
                  <div className="flex gap-2 shrink-0 pt-1">
                    <Button variant="success" size="sm" onClick={() => handleAction(item, "approve")}>Approve</Button>
                    <Button variant="danger" size="sm" className="bg-transparent text-(--color-danger) border border-(--color-danger)/30 hover:bg-(--color-danger-light) hover:opacity-100" onClick={() => handleAction(item, "reject")}>Reject</Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* ── ACTIVE RULES SUMMARY ── */}
      <div className="mb-8">
        <SectionHeader title="Active Rules" />
        <Card href="/governance/rules" padding="p-4">
          <div className="flex items-center gap-4">
            {Object.entries(ruleIcons).map(([type, { icon, label }]) => {
              const count = ruleCounts[type] || 0;
              if (count === 0) return null;
              return (
                <div key={type} className="flex items-center gap-1.5">
                  <span className="text-base">{icon}</span>
                  <span className="text-sm text-(--color-text)"><strong>{count}</strong> {label}</span>
                </div>
              );
            })}
            {rules.length === 0 && <span className="text-sm text-(--color-text-tertiary)">No rules configured</span>}
          </div>
          <p className="text-xs text-(--color-text-tertiary) mt-2">You set these. You can change them anytime. &rarr;</p>
        </Card>
      </div>

      {/* ── RECENT DECISIONS ── */}
      <div>
        <SectionHeader title="Recent Decisions" action="View full trace →" actionHref="/governance/trace" />
        {events.length === 0 ? (
          <EmptyState icon="empty" title="No decisions yet" />
        ) : (
          <Card padding="p-0" className="divide-y divide-(--color-border)/30">
            {events.map((evt) => (
              <div key={evt.id} className="flex items-center justify-between px-4 py-3">
                <div className="flex items-center gap-3">
                  <StatusBadge status={evt.action} />
                  <span className="text-sm text-(--color-text)">{evt.target_type.replace(/_/g, " ")}</span>
                  {evt.reason && <span className="text-xs text-(--color-text-tertiary) truncate max-w-[200px]">{evt.reason}</span>}
                </div>
                <span className="text-xs text-(--color-text-tertiary) shrink-0">{relativeTime(evt.created_at)}</span>
              </div>
            ))}
          </Card>
        )}
      </div>
    </div>
  );
}
