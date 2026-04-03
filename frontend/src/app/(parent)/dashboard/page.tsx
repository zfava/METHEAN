"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { auth, children as childrenApi, governance, plans, type User, type RetentionSummary, type GovernanceEvent, type Plan, type MapState } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import { useChild } from "@/lib/ChildContext";

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const [retention, setRetention] = useState<RetentionSummary | null>(null);
  const [mapStates, setMapStates] = useState<MapState[]>([]);
  const [events, setEvents] = useState<GovernanceEvent[]>([]);
  const [childPlans, setChildPlans] = useState<Plan[]>([]);
  const [alerts, setAlerts] = useState<{ title: string; severity: string }[]>([]);
  const [pendingReviews, setPendingReviews] = useState(0);
  const [rulesCount, setRulesCount] = useState(0);
  const [overridesCount, setOverridesCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const { selectedChild } = useChild();

  useEffect(() => {
    loadDashboard();
  }, [selectedChild]);

  async function loadDashboard() {
    setLoading(true);
    try {
      const me = await auth.me();
      setUser(me);
      const evts = await governance.events(10);
      setEvents(evts.items || evts);

      // Governance summary
      try {
        const [queueResp, rulesResp] = await Promise.all([
          fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"}/governance/queue?limit=1`, { credentials: "include" }),
          governance.rules(),
        ]);
        if (queueResp.ok) setPendingReviews((await queueResp.json()).total || 0);
        const allRules = (rulesResp as any).items || rulesResp;
        setRulesCount(Array.isArray(allRules) ? allRules.length : 0);
        const allEvents = (evts as any).items || evts;
        setOverridesCount(allEvents.filter((e: any) => e.target_type === "child_node_state").length);
      } catch {}

      if (selectedChild) {
        const [ret, maps, pls] = await Promise.all([
          childrenApi.retentionSummary(selectedChild.id).catch(() => null),
          childrenApi.allMapState(selectedChild.id).catch(() => []),
          plans.list(selectedChild.id).catch(() => ({ items: [] })),
        ]);
        setRetention(ret);
        setMapStates(maps);
        setChildPlans((pls as any).items || pls || []);

        // Fetch alerts
        try {
          const resp = await fetch(
            `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"}/children/${selectedChild.id}/alerts`,
            { credentials: "include" }
          );
          if (resp.ok) {
            const data = await resp.json();
            setAlerts((data.items || data).slice(0, 5));
          }
        } catch {}
      }
    } catch {
      window.location.href = "/auth";
    } finally {
      setLoading(false);
    }
  }

  if (loading) return (
    <div className="max-w-6xl space-y-8">
      <LoadingSkeleton variant="text" count={1} />
      <LoadingSkeleton variant="card" count={3} />
      <LoadingSkeleton variant="list" count={5} />
    </div>
  );

  return (
    <div className="max-w-6xl">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-xl font-semibold">Dashboard</h1>
          <p className="text-sm text-(--color-text-secondary) mt-0.5">
            Welcome back, {user?.display_name}
            {selectedChild && <> &mdash; viewing <strong>{selectedChild.first_name}</strong> ({selectedChild.grade_level || ""})</>}
          </p>
        </div>
        <button
          onClick={() => auth.logout().then(() => (window.location.href = "/auth"))}
          className="text-sm text-(--color-text-secondary) hover:text-(--color-text)"
        >
          Sign out
        </button>
      </div>

      {/* Retention summary */}
      {retention && (
        <div className="grid grid-cols-5 gap-3 mb-6">
          {[
            { label: "Total Nodes", value: retention.total_nodes, color: "" },
            { label: "Mastered", value: retention.mastered_count, color: "text-(--color-mastered)" },
            { label: "In Progress", value: retention.in_progress_count, color: "text-(--color-progress)" },
            { label: "Blocked", value: retention.blocked_count, color: "text-(--color-blocked)" },
            { label: "Decaying", value: retention.decaying_count, color: "text-(--color-decaying)" },
          ].map((s) => (
            <div key={s.label} className="bg-white rounded-lg border border-(--color-border) p-4">
              <div className={`text-2xl font-semibold ${s.color}`}>{s.value}</div>
              <div className="text-xs text-(--color-text-secondary) mt-0.5">{s.label}</div>
            </div>
          ))}
        </div>
      )}

      {/* Enrolled maps */}
      {mapStates.length > 0 && (
        <div className="grid grid-cols-3 gap-4 mb-6">
          {mapStates.map((ms) => (
            <Link key={ms.learning_map_id} href="/maps" className="bg-white rounded-lg border border-(--color-border) p-4 hover:border-(--color-accent) transition-colors">
              <div className="text-sm font-medium">{ms.map_name}</div>
              <div className="flex items-center gap-2 mt-2">
                <div className="flex-1 bg-gray-100 rounded-full h-1.5">
                  <div className="bg-(--color-mastered) h-1.5 rounded-full" style={{ width: `${Math.round(ms.progress_pct * 100)}%` }} />
                </div>
                <span className="text-xs text-(--color-text-secondary)">{Math.round(ms.progress_pct * 100)}%</span>
              </div>
            </Link>
          ))}
        </div>
      )}

      {/* Governance summary */}
      <Link href="/governance/queue" className="block mb-6 bg-white rounded-lg border border-(--color-border) p-4 hover:border-(--color-accent) transition-colors">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="text-center">
              <div className={`text-xl font-semibold ${pendingReviews > 0 ? "text-amber-600" : "text-(--color-mastered)"}`}>
                {pendingReviews}
              </div>
              <div className="text-[10px] text-(--color-text-secondary)">Pending Review</div>
            </div>
            <div className="w-px h-8 bg-gray-200" />
            <div className="text-center">
              <div className="text-xl font-semibold">{rulesCount}</div>
              <div className="text-[10px] text-(--color-text-secondary)">Active Rules</div>
            </div>
            <div className="w-px h-8 bg-gray-200" />
            <div className="text-center">
              <div className="text-xl font-semibold">{overridesCount}</div>
              <div className="text-[10px] text-(--color-text-secondary)">Overrides</div>
            </div>
          </div>
          <div className="text-xs text-(--color-accent)">Governance &rarr;</div>
        </div>
      </Link>

      <div className="grid grid-cols-2 gap-4 mb-6">
        {/* Alerts */}
        <div className="bg-white rounded-lg border border-(--color-border) p-5">
          <h2 className="text-sm font-semibold mb-3">Alerts</h2>
          {alerts.length === 0 ? (
            <p className="text-xs text-(--color-text-secondary)">No alerts</p>
          ) : (
            <div className="space-y-2">
              {alerts.map((a, i) => (
                <div key={i} className="flex items-center gap-2 py-1">
                  <StatusBadge status={a.severity} />
                  <span className="text-xs">{a.title}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Quick actions */}
        <div className="bg-white rounded-lg border border-(--color-border) p-5">
          <h2 className="text-sm font-semibold mb-3">Quick Actions</h2>
          <div className="space-y-2">
            <Link href="/plans" className="block text-xs text-(--color-accent) hover:underline">Generate a weekly plan</Link>
            <Link href="/maps" className="block text-xs text-(--color-accent) hover:underline">View learning maps</Link>
            <Link href="/inspection" className="block text-xs text-(--color-accent) hover:underline">Inspect AI decisions</Link>
            <Link href="/governance" className="block text-xs text-(--color-accent) hover:underline">Review governance log</Link>
          </div>
        </div>
      </div>

      {/* Recent governance activity */}
      <div className="bg-white rounded-lg border border-(--color-border) p-5">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-semibold">Recent Governance Activity</h2>
          <Link href="/governance" className="text-xs text-(--color-accent) hover:underline">View all</Link>
        </div>
        {events.length === 0 ? (
          <p className="text-sm text-(--color-text-secondary)">No governance events yet.</p>
        ) : (
          <div className="space-y-2">
            {events.slice(0, 8).map((evt) => (
              <div key={evt.id} className="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
                <div className="flex items-center gap-3">
                  <StatusBadge status={evt.action} />
                  <span className="text-sm">{evt.target_type}</span>
                  {evt.reason && <span className="text-xs text-(--color-text-secondary) truncate max-w-xs">{evt.reason}</span>}
                </div>
                <span className="text-xs text-(--color-text-secondary)">{new Date(evt.created_at).toLocaleString()}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
