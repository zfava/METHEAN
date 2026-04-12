"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { auth, children as childrenApi, governance, household, snapshots, usage, familyInsights, type User, type ChildState, type GovernanceEvent, type SnapshotItem, type FamilyInsightSummary, type FamilyInsightItem } from "@/lib/api";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import StatusBadge from "@/components/StatusBadge";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import MetricCard from "@/components/ui/MetricCard";
import SectionHeader from "@/components/ui/SectionHeader";
import MasteryChart from "@/components/MasteryChart";
import { ShieldIcon } from "@/components/ConstitutionalCeremony";
import { useChild } from "@/lib/ChildContext";
import { cn } from "@/lib/cn";
import EmptyState from "@/components/ui/EmptyState";
import { useStagger } from "@/lib/useStagger";

interface TodayActivity { id: string; title: string; activity_type: string; status: string; estimated_minutes: number | null; }
interface AlertItem { title: string; message: string; severity: string; }
interface ChildSummary { id: string; mastered: number; total: number; todayCount: number; }

function FamilyInsightsWidget({ childCount }: { childCount: number }) {
  const [summary, setSummary] = useState<FamilyInsightSummary | null>(null);
  const [topInsight, setTopInsight] = useState<FamilyInsightItem | null>(null);

  useEffect(() => {
    if (childCount < 2) return;
    familyInsights.summary().then(setSummary).catch(() => {});
    familyInsights.list({ per_page: 1 }).then(r => setTopInsight(r.items[0] || null)).catch(() => {});
  }, [childCount]);

  if (childCount < 2 || !summary) return null;
  if (summary.total_active === 0) return null;

  return (
    <Card>
      <div className="flex items-center justify-between mb-2">
        <SectionHeader title="Family Insights" actionHref="/family-insights" action="View all" />
      </div>
      <div className="flex items-center gap-3 mb-2">
        <span className="text-xs font-medium px-2 py-0.5 rounded-full border" style={{
          color: summary.total_active <= 3 ? "var(--color-warning)" : "var(--color-danger)",
          borderColor: summary.total_active <= 3 ? "var(--color-warning)" : "var(--color-danger)",
        }}>
          {summary.total_active} active
        </span>
        {summary.predictive_count > 0 && (
          <span className="text-[10px] text-(--color-accent)">{summary.predictive_count} predictive</span>
        )}
      </div>
      {topInsight && (
        <p className="text-xs text-(--color-text-secondary) leading-relaxed line-clamp-2">
          {topInsight.recommendation}
        </p>
      )}
    </Card>
  );
}

export default function DashboardPage() {
  useEffect(() => { document.title = "Dashboard | METHEAN"; }, []);

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
  const [subjectMastery, setSubjectMastery] = useState<Array<{ name: string; mastered: number; total: number; color: string }>>([]);
  const [dueForReview, setDueForReview] = useState<Array<{ title: string; due: string }>>([]);
  const [weeklyStats, setWeeklyStats] = useState({ completed: 0, minutes: 0, mastered: 0 });
  const [chartData, setChartData] = useState<Array<{ week: string; mastered: number; progressed: number; total_minutes: number }>>([]);
  const [govHealth, setGovHealth] = useState<{ rules: number; constitutional: number; transparency: string; pending: number }>({ rules: 0, constitutional: 0, transparency: "full", pending: 0 });
  const [aiUsagePct, setAiUsagePct] = useState<number | null>(null);
  const [error, setError] = useState("");

  useEffect(() => { init(); }, []);
  useEffect(() => { if (selectedChild) loadChildDetail(); }, [selectedChild]);

  async function init() {
    try { const me = await auth.me(); setUser(me); } catch { window.location.href = "/auth"; return; }
    try {
      const [qData, rResp, eResp] = await Promise.all([
        governance.queue(1),
        governance.rules(), governance.events(1),
      ]);
      setPendingReviews(qData.total || 0);
      const rules = (rResp as any).items || rResp;
      const rulesList = Array.isArray(rules) ? rules : [];
      setRulesCount(rulesList.length);
      const evts: GovernanceEvent[] = ((eResp as any).items || eResp);
      if (evts.length > 0) setLastDecision(new Date(evts[0].created_at).toLocaleString());
      // Governance health
      const constitutional = rulesList.filter((r: any) => r.tier === "constitutional" && r.is_active).length;
      const aiRule = rulesList.find((r: any) => r.rule_type === "ai_boundary" && r.is_active);
      const transparency = aiRule ? ((aiRule.parameters as any)?.ai_transparency || "full") : "full";
      setGovHealth({ rules: rulesList.filter((r: any) => r.is_active).length, constitutional, transparency, pending: qData.total || 0 });
      // Load AI usage
      usage.current().then((u) => setAiUsagePct(u?.pct_used ?? null)).catch(() => {});
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't load dashboard data. Check your connection.");
    }
    setLoading(false);
  }

  useEffect(() => {
    if (children.length === 0) return;
    children.forEach(async (c) => {
      try {
        const [state, todayResp] = await Promise.all([
          childrenApi.state(c.id).catch(() => null),
          childrenApi.today(c.id).catch(() => []),
        ]);
        setSummaries((prev) => ({ ...prev, [c.id]: { id: c.id, mastered: state?.mastered_count || 0, total: state?.total_nodes || 0, todayCount: Array.isArray(todayResp) ? todayResp.length : 0 } }));
      } catch (err: any) {
        setError(err?.detail || err?.message || "Couldn't load child summary.");
      }
    });
  }, [children]);

  async function loadChildDetail() {
    if (!selectedChild) return;
    try {
      const [state, todayResp, alertsResp] = await Promise.all([
        childrenApi.state(selectedChild.id).catch(() => null),
        childrenApi.today(selectedChild.id).catch(() => []),
        childrenApi.alerts(selectedChild.id).catch(() => ({ items: [] })),
      ]);
      setChildState(state);
      setTodayActivities(Array.isArray(todayResp) ? todayResp : []);
      const alertItems = (alertsResp as any).items || alertsResp;
      setAlerts(Array.isArray(alertItems) ? alertItems.slice(0, 5) : []);

      // Fetch per-subject mastery
      const subjectColors = ["#4A6FA5", "#2D6A4F", "#B8860B", "#6B4C9A", "#C97B2A", "#B5547A"];
      try {
        const mapStates = await childrenApi.allMapState(selectedChild.id);
        const subjects = mapStates.map((ms: any, i: number) => ({
          name: ms.map_name || "Subject",
          mastered: ms.nodes?.filter((n: any) => n.mastery === "mastered").length || 0,
          total: ms.nodes?.length || 0,
          color: subjectColors[i % subjectColors.length],
        }));
        setSubjectMastery(subjects);
      } catch { setSubjectMastery([]); }

      // Fetch due-for-review
      try {
        const retention = await childrenApi.retentionSummary(selectedChild.id);
        const now = Date.now();
        const sevenDays = 7 * 24 * 60 * 60 * 1000;
        const due = ((retention as any).nodes || [])
          .filter((n: any) => n.due_date && new Date(n.due_date).getTime() - now < sevenDays)
          .slice(0, 5)
          .map((n: any) => ({ title: n.title || n.node_id, due: n.due_date }));
        setDueForReview(due);
      } catch { setDueForReview([]); }

      // Weekly stats from today's activities
      const completedToday = Array.isArray(todayResp) ? todayResp.filter((a: any) => a.status === "completed").length : 0;
      const minutesToday = Array.isArray(todayResp) ? todayResp.reduce((s: number, a: any) => s + (a.estimated_minutes || 0), 0) : 0;
      setWeeklyStats({ completed: completedToday, minutes: minutesToday, mastered: state?.mastered_count || 0 });

      // Fetch mastery snapshots for chart
      try {
        const snapshotData = await snapshots.list(selectedChild.id, 20);
        const items = snapshotData?.items || snapshotData || [];
        if (Array.isArray(items)) {
          setChartData(items.map((s: SnapshotItem) => ({
            week: s.week_start,
            mastered: s.nodes_mastered,
            progressed: s.nodes_progressed,
            total_minutes: s.total_minutes,
          })));
        }
      } catch { setChartData([]); }
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't load activity details.");
    }
  }

  const cardVisibility = useStagger(children.length, 60);

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
          <Card href="/governance" padding="px-4 py-2.5" className="flex items-center gap-3">
            <ShieldIcon size={16} className="text-(--color-constitutional) shrink-0" />
            <span className="text-xs font-medium text-(--color-text)">{govHealth.rules} rules active</span>
            <div className="w-px h-3 bg-(--color-border) hidden sm:block" />
            <span className={cn("text-xs hidden sm:inline", govHealth.transparency === "full" ? "text-(--color-success)" : "text-(--color-warning)")}>
              AI: {govHealth.transparency}
            </span>
            <div className="w-px h-3 bg-(--color-border)" />
            <span className={cn("text-xs font-medium flex items-center gap-1", govHealth.pending > 0 ? "text-(--color-warning)" : "text-(--color-success)")}>
              {govHealth.pending > 0 && <span className="w-1.5 h-1.5 rounded-full bg-(--color-warning) animate-pulse shrink-0" />}
              {govHealth.pending > 0 ? `${govHealth.pending} pending` : "All clear"}
            </span>
            {govHealth.constitutional > 0 && (
              <span className="text-[10px] px-1.5 py-0.5 bg-(--color-constitutional-light) text-(--color-constitutional) rounded-full font-medium hidden sm:inline">{govHealth.constitutional} constitutional</span>
            )}
            {aiUsagePct != null && aiUsagePct > 0.8 && (
              <span className={cn("text-[10px] px-1.5 py-0.5 rounded-full font-medium hidden sm:inline",
                aiUsagePct >= 1.0 ? "bg-(--color-danger-light) text-(--color-danger)" : "bg-(--color-warning-light) text-(--color-warning)"
              )}>
                AI: {Math.round(aiUsagePct * 100)}% used
              </span>
            )}
          </Card>
        }
      />

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button variant="ghost" size="sm" onClick={() => { setError(""); init(); }}>Retry</Button>
          </div>
        </Card>
      )}

      {/* ── Child cards ── */}
      {children.length === 0 && !childLoading && (
        <EmptyState icon="empty" title="Welcome to METHEAN" description="Add your first child from the Family page to get started." action={<a href="/family" className="text-sm text-(--color-accent) hover:underline">Go to Family</a>} />
      )}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 mb-6">
        {children.map((c, idx) => {
          const s = summaries[c.id];
          const pct = s && s.total > 0 ? Math.round((s.mastered / s.total) * 100) : 0;
          const isSelected = selectedChild?.id === c.id;
          const circ = 2 * Math.PI * 20;
          return (
            <div key={c.id} className={cardVisibility[idx] ? "animate-fade-up" : "opacity-0"}>
            <Card onClick={() => setSelectedChild(c)} selected={isSelected} padding="p-4">
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
            </div>
          );
        })}
      </div>

      {selectedChild && (
        <>
          {/* ── Activities + Alerts ── */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
            <div className="lg:col-span-2">
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

          {/* ── Subject Mastery Rings ── */}
          {subjectMastery.length > 0 && (
            <Card className="mb-6">
              <SectionHeader title="Mastery by Subject" />
              <div className="flex gap-5 overflow-x-auto pb-2 mt-3">
                {subjectMastery.map((s) => {
                  const pct = s.total > 0 ? Math.round((s.mastered / s.total) * 100) : 0;
                  const c2 = 2 * Math.PI * 20;
                  return (
                    <div key={s.name} className="flex flex-col items-center gap-1.5 min-w-[80px] shrink-0">
                      <div className="relative w-14 h-14">
                        <svg className="w-14 h-14 -rotate-90" viewBox="0 0 48 48">
                          <circle cx="24" cy="24" r="20" fill="none" stroke="var(--color-border)" strokeWidth="3" />
                          <circle cx="24" cy="24" r="20" fill="none" stroke={s.color} strokeWidth="3"
                            strokeDasharray={`${(pct / 100) * c2} ${c2}`} strokeLinecap="round" />
                        </svg>
                        <span className="absolute inset-0 flex items-center justify-center text-[10px] font-bold text-(--color-text)">{pct}%</span>
                      </div>
                      <span className="text-xs font-medium text-(--color-text) text-center leading-tight">{s.name}</span>
                      <span className="text-[10px] text-(--color-text-tertiary)">{s.mastered}/{s.total}</span>
                    </div>
                  );
                })}
              </div>
            </Card>
          )}

          {/* ── Mastery Over Time ── */}
          <Card className="mb-6">
            <SectionHeader title="Mastery Over Time" />
            <div className="mt-3">
              <MasteryChart data={chartData} height={200} />
            </div>
            <div className="flex items-center gap-5 mt-2 text-[11px] text-(--color-text-tertiary)">
              <span className="flex items-center gap-1.5"><span className="w-3 h-0.5 bg-(--color-success) rounded" /> Mastered</span>
              <span className="flex items-center gap-1.5"><span className="w-3 h-0.5 bg-(--color-accent) rounded" style={{ backgroundImage: "repeating-linear-gradient(90deg, var(--color-accent) 0 4px, transparent 4px 7px)" }} /> Progressing</span>
            </div>
          </Card>

          {/* ── Due for Review ── */}
          {dueForReview.length > 0 && (
            <Card className="mb-6" padding="p-4">
              <SectionHeader title="Due for Review" />
              <div className="mt-2 space-y-1.5">
                {dueForReview.map((n, i) => {
                  const dueDate = new Date(n.due);
                  const today = new Date();
                  const diffDays = Math.ceil((dueDate.getTime() - today.getTime()) / 86400000);
                  const label = diffDays <= 0 ? "due today" : diffDays === 1 ? "due tomorrow" : `due in ${diffDays} days`;
                  return (
                    <div key={i} className="flex items-center gap-2 text-xs">
                      <span className="text-(--color-accent)">📗</span>
                      <span className="text-(--color-text)">{n.title}</span>
                      <span className={cn("text-[10px]", diffDays <= 0 ? "text-(--color-warning) font-medium" : "text-(--color-text-tertiary)")}>— {label}</span>
                    </div>
                  );
                })}
              </div>
            </Card>
          )}

          {/* ── Family Insights Widget ── */}
          <FamilyInsightsWidget childCount={children.length} />

          {/* ── Weekly Summary ── */}
          <div className="flex items-center gap-4 text-xs text-(--color-text-tertiary) mb-6">
            <span>Today: {weeklyStats.completed} completed</span>
            <span>{weeklyStats.minutes}m planned</span>
            <span>{weeklyStats.mastered} nodes mastered</span>
          </div>
        </>
      )}
    </div>
  );
}
