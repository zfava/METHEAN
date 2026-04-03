"use client";

import { useEffect, useState } from "react";
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
  scheduled_date: string | null;
  child_name: string;
  child_id: string | null;
  plan_name: string;
  plan_id: string | null;
}

export default function QueuePage() {
  const [items, setItems] = useState<QueueItem[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [dismissing, setDismissing] = useState<Set<string>>(new Set());

  useEffect(() => { loadQueue(); }, []);

  async function loadQueue() {
    setLoading(true);
    try {
      const resp = await fetch(`${API}/governance/queue?limit=100`, { credentials: "include" });
      if (resp.ok) { const d = await resp.json(); setItems(d.items || []); setTotal(d.total || 0); }
    } catch {} finally { setLoading(false); }
  }

  async function doAction(activityId: string, planId: string, action: "approve" | "reject") {
    setDismissing((prev) => new Set(prev).add(activityId));
    const csrf = getCsrf();
    const body = action === "reject" ? JSON.stringify({ reason: "Rejected by parent" }) : undefined;
    await fetch(`${API}/plans/${planId}/activities/${activityId}/${action}`, {
      method: "PUT", credentials: "include",
      headers: { "Content-Type": "application/json", ...(csrf ? { "X-CSRF-Token": csrf } : {}) },
      body,
    });
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
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold text-slate-800">Approval Queue</h1>
          <p className="text-sm text-slate-500">
            {total === 0 ? "All caught up!" : `${total} activities need your review`}
          </p>
        </div>
        {selected.size > 0 && (
          <button onClick={bulkApprove} className="px-4 py-2 text-sm font-medium bg-green-600 text-white rounded-md hover:bg-green-700">
            Approve Selected ({selected.size})
          </button>
        )}
      </div>

      {total === 0 ? (
        <div className="bg-white rounded-lg border border-slate-200 py-16 text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-green-100 flex items-center justify-center">
            <span className="text-green-600 text-2xl">&#10003;</span>
          </div>
          <div className="text-base font-medium text-slate-700">All caught up!</div>
          <div className="text-sm text-slate-400 mt-1">No activities need your review right now.</div>
        </div>
      ) : (
        <>
          {items.length > 1 && (
            <div className="mb-3">
              <button onClick={toggleAll} className="text-xs text-blue-600 hover:underline">
                {selected.size === items.length ? "Deselect all" : "Select all"}
              </button>
            </div>
          )}
          <div className="space-y-8">
            {Object.entries(byChild).map(([childName, childItems]) => (
              <div key={childName}>
                <div className="flex items-center gap-2 mb-3">
                  <span className="w-7 h-7 rounded-full bg-blue-100 text-blue-700 text-xs font-bold flex items-center justify-center">
                    {childName.charAt(0)}
                  </span>
                  <h3 className="text-sm font-semibold text-slate-700">{childName}</h3>
                  <span className="text-xs text-slate-400">({childItems.length})</span>
                </div>
                <div className="space-y-2 ml-9">
                  {childItems.map((item) => (
                    <div
                      key={item.activity_id}
                      className={`bg-white rounded-lg border border-slate-200 p-4 transition-all duration-300 ${
                        dismissing.has(item.activity_id) ? "opacity-0 -translate-x-4" : "opacity-100"
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        <input type="checkbox" checked={selected.has(item.activity_id)}
                          onChange={() => toggleSelect(item.activity_id)} className="mt-1 rounded" />
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 flex-wrap">
                            <span className="text-sm font-medium text-slate-800">{item.title}</span>
                            <span className="text-[10px] px-1.5 py-0.5 bg-slate-100 text-slate-500 rounded font-medium uppercase">{item.activity_type}</span>
                            {item.difficulty && (
                              <span className="text-xs">
                                <span className="text-yellow-500">{"●".repeat(item.difficulty)}</span>
                                <span className="text-slate-300">{"●".repeat(5 - item.difficulty)}</span>
                              </span>
                            )}
                            {item.estimated_minutes && <span className="text-xs text-slate-400">{item.estimated_minutes}m</span>}
                            {item.scheduled_date && <span className="text-xs text-slate-400">{item.scheduled_date}</span>}
                          </div>
                          <div className="text-[11px] text-slate-400 mt-0.5">{item.plan_name}</div>
                          {item.ai_rationale && (
                            <div className="text-xs bg-blue-50 border border-blue-100 rounded px-2.5 py-1.5 mt-2">
                              <span className="font-medium text-blue-700">AI rationale: </span>
                              <span className="text-blue-600 italic">{item.ai_rationale}</span>
                            </div>
                          )}
                        </div>
                        <div className="flex gap-2 shrink-0">
                          <button onClick={() => item.plan_id && doAction(item.activity_id, item.plan_id, "approve")}
                            className="px-3 py-1.5 text-xs font-medium bg-green-600 text-white rounded-md hover:bg-green-700">Approve</button>
                          <button onClick={() => item.plan_id && doAction(item.activity_id, item.plan_id, "reject")}
                            className="px-3 py-1.5 text-xs font-medium text-red-600 border border-red-300 rounded-md hover:bg-red-50">Reject</button>
                        </div>
                      </div>
                    </div>
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
