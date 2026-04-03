"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { governance, type GovernanceEvent, type GovernanceRule } from "@/lib/api";
import LoadingSkeleton from "@/components/LoadingSkeleton";

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

function relativeTime(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

export default function GovernanceOverviewPage() {
  const [queue, setQueue] = useState<QueueItem[]>([]);
  const [queueTotal, setQueueTotal] = useState(0);
  const [rules, setRules] = useState<GovernanceRule[]>([]);
  const [events, setEvents] = useState<GovernanceEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [dismissing, setDismissing] = useState<Set<string>>(new Set());

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

  const actionBadge: Record<string, { bg: string; text: string; label: string }> = {
    approve: { bg: "bg-green-100", text: "text-green-800", label: "Approved" },
    reject: { bg: "bg-red-100", text: "text-red-800", label: "Rejected" },
    modify: { bg: "bg-yellow-100", text: "text-yellow-800", label: "Modified" },
    defer: { bg: "bg-slate-100", text: "text-slate-600", label: "Deferred" },
  };

  return (
    <div className="max-w-4xl">
      <div className="mb-6">
        <h1 className="text-xl font-semibold text-slate-800">Governance</h1>
        <p className="text-sm text-slate-500">You control what the AI can and cannot do.</p>
      </div>

      {/* ── APPROVAL QUEUE PREVIEW ── */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-semibold text-slate-700">Pending Your Review</h2>
          {queueTotal > 0 && (
            <Link href="/governance/queue" className="text-xs text-blue-600 hover:underline">
              View full queue ({queueTotal}) &rarr;
            </Link>
          )}
        </div>

        {queue.length === 0 ? (
          <div className="bg-white rounded-lg border border-slate-200 py-12 text-center">
            <div className="w-12 h-12 mx-auto mb-3 rounded-full bg-green-100 flex items-center justify-center">
              <span className="text-green-600 text-xl">&#10003;</span>
            </div>
            <div className="text-sm font-medium text-slate-700">All Clear</div>
            <div className="text-xs text-slate-400 mt-1">No activities need your review.</div>
          </div>
        ) : (
          <div className="space-y-2">
            {queue.map((item) => (
              <div
                key={item.activity_id}
                className={`bg-white rounded-lg border border-slate-200 p-4 transition-all duration-300 ${
                  dismissing.has(item.activity_id) ? "opacity-0 scale-95" : "opacity-100"
                }`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-700 text-[10px] font-bold flex items-center justify-center shrink-0">
                        {item.child_name.charAt(0)}
                      </span>
                      <span className="text-xs text-slate-500">{item.child_name}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-slate-800">{item.title}</span>
                      <span className="text-[10px] px-1.5 py-0.5 bg-slate-100 text-slate-500 rounded font-medium uppercase">{item.activity_type}</span>
                      {item.difficulty && (
                        <span className="text-xs text-yellow-600">
                          {"●".repeat(item.difficulty)}
                          <span className="text-slate-300">{"●".repeat(5 - item.difficulty)}</span>
                        </span>
                      )}
                      {item.estimated_minutes && <span className="text-xs text-slate-400">{item.estimated_minutes}m</span>}
                    </div>
                    {item.ai_rationale && (
                      <p className="text-xs text-slate-500 italic mt-1.5">&ldquo;{item.ai_rationale}&rdquo;</p>
                    )}
                  </div>
                  <div className="flex gap-2 shrink-0 pt-1">
                    <button
                      onClick={() => handleAction(item, "approve")}
                      className="px-3 py-1.5 text-xs font-medium bg-green-600 text-white rounded-md hover:bg-green-700"
                    >Approve</button>
                    <button
                      onClick={() => handleAction(item, "reject")}
                      className="px-3 py-1.5 text-xs font-medium text-red-600 border border-red-300 rounded-md hover:bg-red-50"
                    >Reject</button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ── ACTIVE RULES SUMMARY ── */}
      <div className="mb-8">
        <h2 className="text-sm font-semibold text-slate-700 mb-3">Active Rules</h2>
        <Link href="/governance/rules" className="block bg-white rounded-lg border border-slate-200 p-4 hover:border-blue-300 transition-colors">
          <div className="flex items-center gap-4">
            {Object.entries(ruleIcons).map(([type, { icon, label }]) => {
              const count = ruleCounts[type] || 0;
              if (count === 0) return null;
              return (
                <div key={type} className="flex items-center gap-1.5">
                  <span className="text-base">{icon}</span>
                  <span className="text-sm text-slate-700"><strong>{count}</strong> {label}</span>
                </div>
              );
            })}
            {rules.length === 0 && <span className="text-sm text-slate-400">No rules configured</span>}
          </div>
          <p className="text-xs text-slate-400 mt-2">You set these. You can change them anytime. &rarr;</p>
        </Link>
      </div>

      {/* ── RECENT DECISIONS ── */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-semibold text-slate-700">Recent Decisions</h2>
          <Link href="/governance/trace" className="text-xs text-blue-600 hover:underline">View full trace &rarr;</Link>
        </div>
        {events.length === 0 ? (
          <div className="bg-white rounded-lg border border-slate-200 p-6 text-center text-sm text-slate-400">
            No decisions yet.
          </div>
        ) : (
          <div className="bg-white rounded-lg border border-slate-200 divide-y divide-slate-50">
            {events.map((evt) => {
              const badge = actionBadge[evt.action] || actionBadge.defer;
              return (
                <div key={evt.id} className="flex items-center justify-between px-4 py-3">
                  <div className="flex items-center gap-3">
                    <span className={`text-[10px] font-medium px-1.5 py-0.5 rounded ${badge.bg} ${badge.text}`}>
                      {badge.label}
                    </span>
                    <span className="text-sm text-slate-700">{evt.target_type.replace(/_/g, " ")}</span>
                    {evt.reason && <span className="text-xs text-slate-400 truncate max-w-[200px]">{evt.reason}</span>}
                  </div>
                  <span className="text-xs text-slate-400 shrink-0">{relativeTime(evt.created_at)}</span>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
