"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { auth, children as childrenApi, governance, type User, type ChildState, type GovernanceEvent } from "@/lib/api";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import { useChild } from "@/lib/ChildContext";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface TodayActivity {
  id: string;
  title: string;
  activity_type: string;
  status: string;
  estimated_minutes: number | null;
}

interface AlertItem {
  title: string;
  message: string;
  severity: string;
}

interface ChildSummary {
  id: string;
  mastered: number;
  total: number;
  todayCount: number;
}

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const { children, selectedChild, setSelectedChild, loading: childLoading } = useChild();

  // Per-child summary for the card row
  const [summaries, setSummaries] = useState<Record<string, ChildSummary>>({});

  // Selected child detail
  const [childState, setChildState] = useState<ChildState | null>(null);
  const [todayActivities, setTodayActivities] = useState<TodayActivity[]>([]);
  const [alerts, setAlerts] = useState<AlertItem[]>([]);

  // Governance
  const [pendingReviews, setPendingReviews] = useState(0);
  const [rulesCount, setRulesCount] = useState(0);
  const [lastDecision, setLastDecision] = useState<string | null>(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => { init(); }, []);
  useEffect(() => { if (selectedChild) loadChildDetail(); }, [selectedChild]);

  async function init() {
    try {
      const me = await auth.me();
      setUser(me);
    } catch {
      window.location.href = "/auth";
      return;
    }

    // Governance summary (household-level)
    try {
      const [qResp, rResp, eResp] = await Promise.all([
        fetch(`${API}/governance/queue?limit=1`, { credentials: "include" }),
        governance.rules(),
        governance.events(1),
      ]);
      if (qResp.ok) setPendingReviews((await qResp.json()).total || 0);
      const rules = (rResp as any).items || rResp;
      setRulesCount(Array.isArray(rules) ? rules.length : 0);
      const evts: GovernanceEvent[] = ((eResp as any).items || eResp);
      if (evts.length > 0) setLastDecision(new Date(evts[0].created_at).toLocaleString());
    } catch {}

    setLoading(false);
  }

  // Load summaries for all children (for the card row)
  useEffect(() => {
    if (children.length === 0) return;
    children.forEach(async (c) => {
      try {
        const [state, todayResp] = await Promise.all([
          childrenApi.state(c.id).catch(() => null),
          fetch(`${API}/children/${c.id}/today`, { credentials: "include" }).then((r) => r.ok ? r.json() : []).catch(() => []),
        ]);
        setSummaries((prev) => ({
          ...prev,
          [c.id]: {
            id: c.id,
            mastered: state?.mastered_count || 0,
            total: state?.total_nodes || 0,
            todayCount: Array.isArray(todayResp) ? todayResp.length : 0,
          },
        }));
      } catch {}
    });
  }, [children]);

  async function loadChildDetail() {
    if (!selectedChild) return;
    try {
      const [state, todayResp, alertsResp] = await Promise.all([
        childrenApi.state(selectedChild.id).catch(() => null),
        fetch(`${API}/children/${selectedChild.id}/today`, { credentials: "include" }).then((r) => r.ok ? r.json() : []).catch(() => []),
        fetch(`${API}/children/${selectedChild.id}/alerts`, { credentials: "include" }).then((r) => r.ok ? r.json() : { items: [] }).catch(() => ({ items: [] })),
      ]);
      setChildState(state);
      setTodayActivities(Array.isArray(todayResp) ? todayResp : []);
      const alertItems = (alertsResp as any).items || alertsResp;
      setAlerts(Array.isArray(alertItems) ? alertItems.slice(0, 5) : []);
    } catch {}
  }

  if (loading || childLoading) return (
    <div className="max-w-5xl space-y-6">
      <LoadingSkeleton variant="text" count={1} />
      <LoadingSkeleton variant="card" count={3} />
      <LoadingSkeleton variant="list" count={5} />
    </div>
  );

  const today = new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" });

  // Mastery bar segments
  const masterySegments = childState ? [
    { label: "Mastered", count: childState.mastered_count, color: "bg-green-500" },
    { label: "In Progress", count: childState.in_progress_count, color: "bg-blue-500" },
    { label: "Not Started", count: childState.not_started_count, color: "bg-slate-300" },
  ] : [];
  const masteryTotal = masterySegments.reduce((s, m) => s + m.count, 0);

  return (
    <div className="max-w-5xl">
      {/* ── HEADER ── */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold text-slate-800">Dashboard</h1>
          <p className="text-sm text-slate-500 mt-0.5">{today}</p>
        </div>
        <div className="flex items-center gap-4">
          {/* Governance badge */}
          <Link href="/governance/queue" className="bg-white border border-slate-200 rounded-lg px-4 py-2.5 hover:border-blue-400 transition-colors">
            <div className="flex items-center gap-3">
              <div className="text-center">
                <div className={`text-lg font-semibold leading-none ${pendingReviews > 0 ? "text-yellow-600" : "text-green-600"}`}>
                  {pendingReviews}
                </div>
                <div className="text-[10px] text-slate-500 mt-0.5">pending</div>
              </div>
              <div className="w-px h-6 bg-slate-200" />
              <div className="text-center">
                <div className="text-lg font-semibold leading-none text-slate-700">{rulesCount}</div>
                <div className="text-[10px] text-slate-500 mt-0.5">rules</div>
              </div>
            </div>
            {lastDecision && (
              <div className="text-[10px] text-slate-400 mt-1">Last: {lastDecision}</div>
            )}
          </Link>
          <button
            onClick={() => auth.logout().then(() => (window.location.href = "/auth"))}
            className="text-xs text-slate-400 hover:text-slate-600"
          >
            Sign out
          </button>
        </div>
      </div>

      {/* ── CHILD CARDS ── */}
      <div className="grid grid-cols-3 gap-3 mb-8">
        {children.map((c) => {
          const s = summaries[c.id];
          const pct = s && s.total > 0 ? Math.round((s.mastered / s.total) * 100) : 0;
          const isSelected = selectedChild?.id === c.id;
          const circumference = 2 * Math.PI * 20;
          const strokeDash = (pct / 100) * circumference;

          return (
            <button
              key={c.id}
              onClick={() => setSelectedChild(c)}
              className={`text-left bg-white rounded-lg border p-4 transition-all ${
                isSelected
                  ? "border-blue-500 ring-2 ring-blue-100"
                  : "border-slate-200 hover:border-slate-300"
              }`}
            >
              <div className="flex items-center gap-3">
                {/* Circular progress */}
                <div className="relative w-12 h-12 shrink-0">
                  <svg className="w-12 h-12 -rotate-90" viewBox="0 0 48 48">
                    <circle cx="24" cy="24" r="20" fill="none" stroke="#e2e8f0" strokeWidth="4" />
                    <circle cx="24" cy="24" r="20" fill="none" stroke="#22c55e" strokeWidth="4"
                      strokeDasharray={`${strokeDash} ${circumference}`} strokeLinecap="round" />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-xs font-semibold text-slate-700">{pct}%</span>
                  </div>
                </div>
                <div>
                  <div className="text-sm font-semibold text-slate-800">{c.first_name}</div>
                  <div className="text-xs text-slate-500">{c.grade_level || ""}</div>
                  <div className="text-[11px] text-slate-400 mt-0.5">
                    {s ? (s.todayCount > 0 ? `${s.todayCount} activities today` : "No activities today") : "..."}
                  </div>
                </div>
              </div>
            </button>
          );
        })}
      </div>

      {selectedChild && (
        <>
          {/* ── THIS WEEK ── */}
          <div className="grid grid-cols-3 gap-4 mb-6">
            <div className="col-span-2 bg-white rounded-lg border border-slate-200">
              <div className="px-5 py-3 border-b border-slate-100">
                <h2 className="text-sm font-semibold text-slate-800">
                  {selectedChild.first_name}&apos;s Activities Today
                </h2>
              </div>
              <div className="divide-y divide-slate-50">
                {todayActivities.length === 0 ? (
                  <div className="px-5 py-6 text-center text-sm text-slate-400">
                    No activities scheduled for today
                  </div>
                ) : (
                  todayActivities.map((a) => (
                    <div key={a.id} className="flex items-center justify-between px-5 py-3">
                      <div className="flex items-center gap-3">
                        <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${
                          a.status === "completed" ? "bg-green-500" :
                          a.status === "in_progress" ? "bg-blue-500" : "bg-slate-300"
                        }`} />
                        <span className="text-sm text-slate-700">{a.title}</span>
                        <span className="text-[10px] px-1.5 py-0.5 bg-slate-100 text-slate-500 rounded font-medium uppercase">
                          {a.activity_type}
                        </span>
                      </div>
                      <div className="flex items-center gap-2 text-xs text-slate-400">
                        {a.estimated_minutes && <span>{a.estimated_minutes}m</span>}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Attention needed */}
            <div className="bg-white rounded-lg border border-slate-200">
              <div className="px-4 py-3 border-b border-slate-100">
                <h2 className="text-sm font-semibold text-slate-800">Attention Needed</h2>
              </div>
              <div className="p-4">
                {alerts.length === 0 ? (
                  <div className="text-center py-4">
                    <div className="text-green-500 text-xl mb-1">&#10003;</div>
                    <div className="text-xs text-slate-500">All on track</div>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {alerts.map((a, i) => (
                      <div key={i} className="flex items-start gap-2">
                        <span className={`mt-0.5 w-1.5 h-1.5 rounded-full shrink-0 ${
                          a.severity === "action_required" ? "bg-red-500" :
                          a.severity === "warning" ? "bg-yellow-500" : "bg-blue-400"
                        }`} />
                        <div>
                          <div className="text-xs font-medium text-slate-700">{a.title}</div>
                          <div className="text-[11px] text-slate-400 line-clamp-2">{a.message}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* ── MASTERY PROGRESS ── */}
          {childState && masteryTotal > 0 && (
            <div className="bg-white rounded-lg border border-slate-200 p-5 mb-6">
              <h2 className="text-sm font-semibold text-slate-800 mb-3">Mastery Progress</h2>
              {/* Stacked bar */}
              <div className="flex rounded-full overflow-hidden h-3 bg-slate-100 mb-3">
                {masterySegments.map((seg) => (
                  seg.count > 0 && (
                    <div
                      key={seg.label}
                      className={`${seg.color} transition-all`}
                      style={{ width: `${(seg.count / masteryTotal) * 100}%` }}
                    />
                  )
                ))}
              </div>
              <div className="flex gap-4">
                {masterySegments.map((seg) => (
                  <div key={seg.label} className="flex items-center gap-1.5">
                    <span className={`w-2.5 h-2.5 rounded-sm ${seg.color}`} />
                    <span className="text-xs text-slate-600">
                      {seg.label} <span className="font-semibold">{seg.count}</span>
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
