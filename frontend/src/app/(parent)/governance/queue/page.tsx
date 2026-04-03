"use client";

import { useEffect, useState } from "react";
import { plans } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import LoadingSkeleton from "@/components/LoadingSkeleton";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

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
}

function getCookie(name: string): string | undefined {
  if (typeof document === "undefined") return undefined;
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : undefined;
}

export default function QueuePage() {
  const [items, setItems] = useState<QueueItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Set<string>>(new Set());

  useEffect(() => { loadQueue(); }, []);

  async function loadQueue() {
    setLoading(true);
    try {
      const csrf = getCookie("csrf_token");
      const resp = await fetch(`${API_BASE}/governance/queue?limit=100`, {
        credentials: "include",
        headers: csrf ? { "X-CSRF-Token": csrf } : {},
      });
      if (resp.ok) {
        const data = await resp.json();
        setItems(data.items || []);
        setTotal(data.total || 0);
      }
    } catch {} finally { setLoading(false); }
  }

  async function approve(activityId: string, planId: string) {
    const csrf = getCookie("csrf_token");
    await fetch(`${API_BASE}/plans/${planId}/activities/${activityId}/approve`, {
      method: "PUT",
      credentials: "include",
      headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
    });
    await loadQueue();
  }

  async function reject(activityId: string, planId: string) {
    const reason = prompt("Reason for rejection:");
    if (!reason) return;
    const csrf = getCookie("csrf_token");
    await fetch(`${API_BASE}/plans/${planId}/activities/${activityId}/reject`, {
      method: "PUT",
      credentials: "include",
      headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
      body: JSON.stringify({ reason }),
    });
    await loadQueue();
  }

  async function bulkApprove() {
    for (const item of items) {
      if (selected.has(item.activity_id) && item.plan_id) {
        await approve(item.activity_id, item.plan_id);
      }
    }
    setSelected(new Set());
  }

  function toggleSelect(id: string) {
    const next = new Set(selected);
    next.has(id) ? next.delete(id) : next.add(id);
    setSelected(next);
  }

  function selectAll() {
    if (selected.size === items.length) setSelected(new Set());
    else setSelected(new Set(items.map((i) => i.activity_id)));
  }

  if (loading) return <div className="max-w-4xl"><LoadingSkeleton variant="list" count={5} /></div>;

  // Group by child
  const byChild: Record<string, QueueItem[]> = {};
  items.forEach((item) => {
    const key = item.child_name || "Unknown";
    if (!byChild[key]) byChild[key] = [];
    byChild[key].push(item);
  });

  return (
    <div className="max-w-4xl">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold">Approval Queue</h1>
          <p className="text-sm text-(--color-text-secondary)">
            {total === 0 ? "All caught up!" : `${total} activities need your review`}
          </p>
        </div>
        {selected.size > 0 && (
          <button onClick={bulkApprove} className="px-4 py-2 text-sm font-medium bg-emerald-600 text-white rounded-md hover:bg-emerald-700">
            Approve Selected ({selected.size})
          </button>
        )}
      </div>

      {total === 0 ? (
        <div className="bg-white rounded-lg border border-(--color-border) p-12 text-center">
          <div className="text-3xl mb-3 text-(--color-text-secondary)">&#10003;</div>
          <h2 className="text-sm font-semibold mb-1">All caught up!</h2>
          <p className="text-xs text-(--color-text-secondary)">No activities need your review right now.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {items.length > 1 && (
            <div className="flex items-center gap-2">
              <button onClick={selectAll} className="text-xs text-(--color-accent) hover:underline">
                {selected.size === items.length ? "Deselect all" : "Select all"}
              </button>
            </div>
          )}

          {Object.entries(byChild).map(([childName, childItems]) => (
            <div key={childName}>
              <h3 className="text-xs font-semibold text-(--color-text-secondary) uppercase tracking-wider mb-2">
                {childName}
              </h3>
              <div className="space-y-2">
                {childItems.map((item) => (
                  <div key={item.activity_id} className="bg-white rounded-lg border border-(--color-border) p-4">
                    <div className="flex items-start gap-3">
                      <input
                        type="checkbox"
                        checked={selected.has(item.activity_id)}
                        onChange={() => toggleSelect(item.activity_id)}
                        className="mt-1 rounded"
                      />
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-sm font-medium">{item.title}</span>
                          <StatusBadge status={item.activity_type} />
                          {item.difficulty && (
                            <span className="text-xs text-(--color-text-secondary)">
                              {"●".repeat(item.difficulty)}{"○".repeat(5 - item.difficulty)}
                            </span>
                          )}
                        </div>
                        <div className="text-xs text-(--color-text-secondary) mb-2">
                          {item.plan_name} &middot; {item.scheduled_date || "Unscheduled"}
                          {item.estimated_minutes && ` \u00b7 ${item.estimated_minutes}m`}
                        </div>
                        {item.ai_rationale && (
                          <div className="text-xs bg-blue-50 border border-blue-100 rounded p-2 mb-2">
                            <span className="font-medium text-blue-700">AI rationale:</span>{" "}
                            <span className="text-blue-600">{item.ai_rationale}</span>
                          </div>
                        )}
                      </div>
                      <div className="flex gap-2 shrink-0">
                        <button
                          onClick={() => item.plan_id && approve(item.activity_id, item.plan_id)}
                          className="px-3 py-1.5 text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-md hover:bg-emerald-100"
                        >
                          Approve
                        </button>
                        <button
                          onClick={() => item.plan_id && reject(item.activity_id, item.plan_id)}
                          className="px-3 py-1.5 text-xs font-medium bg-red-50 text-red-700 border border-red-200 rounded-md hover:bg-red-100"
                        >
                          Reject
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
