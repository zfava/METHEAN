"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { auth, children as childrenApi, governance, type User, type ChildState, type GovernanceEvent } from "@/lib/api";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import StatusBadge from "@/components/StatusBadge";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import MetricCard from "@/components/ui/MetricCard";
import SectionHeader from "@/components/ui/SectionHeader";
import { useChild } from "@/lib/ChildContext";
import { cn } from "@/lib/cn";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface TodayActivity { id: string; title: string; activity_type: string; status: string; estimated_minutes: number | null; }
interface AlertItem { title: string; message: string; severity: string; }
interface ChildSummary { id: string; mastered: number; total: number; todayCount: number; }

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const { children, selectedChild, setSelectedChild, loading: childLoading } = useChild();
  const [summaries, setSummaries] = useState<Record<string, ChildSummary>>({});
  const [childState, setChildState] = useState<ChildState | null>(null);
  const [todayActivities, setTodayActivities] = useState<TodayActivity[]>([]);
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [pendingReviews, setPendingReviews] = useState(0);
  const [rulesCount, setRulesCount] = useState(0);
  const [lastDecision, setLastDecision] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { init(); }, []);
  useEffect(() => { if (selectedChild) loadChildDetail(); }, [selectedChild]);

  async function init() {
    try { const me = await auth.me(); setUser(me); } catch { window.location.href = "/auth"; return; }
    try {
      const [qResp, rResp, eResp] = await Promise.all([
        fetch(`${API}/governance/queue?limit=1`, { credentials: "include" }),
        governance.rules(), governance.events(1),
      ]);
      if (qResp.ok) setPendingReviews((await qResp.json()).total || 0);
      const rules = (rResp as any).items || rResp;
      setRulesCount(Array.isArray(rules) ? rules.length : 0);
      const evts: GovernanceEvent[] = ((eResp as any).items || eResp);
      if (evts.length > 0) setLastDecision(new Date(evts[0].created_at).toLocaleString());
    } catch {}
    setLoading(false);
  }

  useEffect(() => {
    if (children.length === 0) return;
    children.forEach(async (c) => {
      try {
        const [state, todayResp] = await Promise.all([
          childrenApi.state(c.id).catch(() => null),
          fetch(`${API}/children/${c.id}/today`, { credentials: "include" }).then((r) => r.ok ? r.json() : []).catch(() => []),
        ]);
        setSummaries((prev) => ({ ...prev, [c.id]: { id: c.id, mastered: state?.mastered_count || 0, total: state?.total_nodes || 0, todayCount: Array.isArray(todayResp) ? todayResp.length : 0 } }));
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
    <div className="max-w-5xl space-y-6"><LoadingSkeleton variant="text" count={1} /><LoadingSkeleton variant="card" count={3} /><LoadingSkeleton variant="list" count={5} /></div>
  );

  const today = new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" });
  const masterySegments = childState ? [
    { label: "Mastered", count: childState.mastered_count, color: "bg-(--color-success)" },
    { label: "In Progress", count: childState.in_progress_count, color: "bg-(--color-accent)" },
    { label: "Not Started", count: childState.not_started_count, color: "bg-(--color-border)" },
  ] : [];
  const masteryTotal = masterySegments.reduce((s, m) => s + m.count, 0);

  return (
    <div className="max-w-5xl">
      <PageHeader title="Dashboard" subtitle={today}
        actions={
          <Card href="/governance/queue" padding="px-4 py-2.5" className="flex items-center gap-4">
            <div className="text-center">
              <div className={cn("text-lg font-medium leading-none", pendingReviews > 0 ? "text-(--color-warning)" : "text-(--color-success)")}>{pendingReviews}</div>
              <div className="text-[10px] text-(--color-text-tertiary) mt-0.5">pending</div>
            </div>
            <div className="w-px h-6 bg-(--color-border)" />
            <div className="text-center">
              <div className="text-lg font-medium leading-none text-(--color-text)">{rulesCount}</div>
              <div className="text-[10px] text-(--color-text-tertiary) mt-0.5">rules</div>
            </div>
            {lastDecision && <div className="text-[10px] text-(--color-text-tertiary)">Last: {lastDecision}</div>}
          </Card>
        }
      />

      {/* ── Child cards ── */}
      {children.length === 0 && !childLoading && (
        <Card className="text-center py-10 mb-6">
          <p className="text-sm text-(--color-text-secondary)">Add your first child to get started.</p>
          <p className="text-xs text-(--color-text-tertiary) mt-1">Go to the <a href="/family" className="text-(--color-accent) hover:underline">Family page</a> to add children to your household.</p>
        </Card>
      )}
      <div className="grid grid-cols-3 gap-3 mb-6">
        {children.map((c) => {
          const s = summaries[c.id];
          const pct = s && s.total > 0 ? Math.round((s.mastered / s.total) * 100) : 0;
          const isSelected = selectedChild?.id === c.id;
          const circ = 2 * Math.PI * 20;
          return (
            <Card key={c.id} onClick={() => setSelectedChild(c)} selected={isSelected} padding="p-4">
              <div className="flex items-center gap-3">
                <div className="relative w-12 h-12 shrink-0">
                  <svg className="w-12 h-12 -rotate-90" viewBox="0 0 48 48">
                    <circle cx="24" cy="24" r="20" fill="none" stroke="var(--color-border)" strokeWidth="3.5" />
                    <circle cx="24" cy="24" r="20" fill="none" stroke="var(--color-success)" strokeWidth="3.5"
                      strokeDasharray={`${(pct / 100) * circ} ${circ}`} strokeLinecap="round" />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center text-xs font-medium text-(--color-text)">{pct}%</div>
                </div>
                <div>
                  <div className="text-sm font-medium text-(--color-text)">{c.first_name}</div>
                  <div className="text-xs text-(--color-text-secondary)">{c.grade_level || ""}</div>
                  <div className="text-[11px] text-(--color-text-tertiary) mt-0.5">
                    {s ? (s.todayCount > 0 ? `${s.todayCount} activities today` : "No activities today") : "..."}
                  </div>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {selectedChild && (
        <>
          {/* ── Activities + Alerts ── */}
          <div className="grid grid-cols-3 gap-4 mb-6">
            <div className="col-span-2">
              <Card padding="p-0">
                <div className="px-5 py-3 border-b border-(--color-border)">
                  <SectionHeader title={`${selectedChild.first_name}'s Activities Today`} />
                </div>
                {todayActivities.length === 0 ? (
                  <div className="px-5 py-8 text-center text-sm text-(--color-text-tertiary)">No activities scheduled for today. Generate a weekly plan or build a curriculum to get started.</div>
                ) : todayActivities.map((a) => (
                  <div key={a.id} className="flex items-center justify-between px-5 py-3 border-b border-(--color-border)/50 last:border-0">
                    <div className="flex items-center gap-3">
                      <span className={cn("w-1.5 h-1.5 rounded-full shrink-0",
                        a.status === "completed" ? "bg-(--color-success)" : a.status === "in_progress" ? "bg-(--color-accent)" : "bg-(--color-border-strong)"
                      )} />
                      <span className="text-sm text-(--color-text)">{a.title}</span>
                      <StatusBadge status={a.activity_type} />
                    </div>
                    {a.estimated_minutes && <span className="text-xs text-(--color-text-tertiary)">{a.estimated_minutes}m</span>}
                  </div>
                ))}
              </Card>
            </div>
            <Card padding="p-0">
              <div className="px-4 py-3 border-b border-(--color-border)">
                <SectionHeader title="Attention Needed" />
              </div>
              <div className="p-4">
                {alerts.length === 0 ? (
                  <div className="text-center py-4">
                    <div className="text-(--color-success) text-lg mb-1">&#10003;</div>
                    <div className="text-xs text-(--color-text-tertiary)">All on track</div>
                  </div>
                ) : alerts.map((a, i) => (
                  <div key={i} className="flex items-start gap-2 mb-3 last:mb-0">
                    <span className={cn("mt-0.5 w-1.5 h-1.5 rounded-full shrink-0",
                      a.severity === "action_required" ? "bg-(--color-danger)" : a.severity === "warning" ? "bg-(--color-warning)" : "bg-(--color-accent)"
                    )} />
                    <div>
                      <div className="text-xs font-medium text-(--color-text)">{a.title}</div>
                      <div className="text-[11px] text-(--color-text-tertiary) line-clamp-2">{a.message}</div>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* ── Mastery progress ── */}
          {childState && masteryTotal > 0 && (
            <Card className="mb-6">
              <SectionHeader title="Mastery Progress" />
              <div className="flex rounded-full overflow-hidden h-2.5 bg-(--color-page) mb-3">
                {masterySegments.map((seg) => seg.count > 0 && (
                  <div key={seg.label} className={seg.color} style={{ width: `${(seg.count / masteryTotal) * 100}%` }} />
                ))}
              </div>
              <div className="flex gap-5">
                {masterySegments.map((seg) => (
                  <div key={seg.label} className="flex items-center gap-1.5">
                    <span className={cn("w-2.5 h-2.5 rounded-sm", seg.color)} />
                    <span className="text-xs text-(--color-text-secondary)">{seg.label} <span className="font-medium text-(--color-text)">{seg.count}</span></span>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </>
      )}
    </div>
  );
}
