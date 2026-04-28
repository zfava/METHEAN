"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { auth, children as childrenApi, governance, household, snapshots, usage, familyInsights, wellbeing, type User, type ChildState, type GovernanceEvent, type SnapshotItem, type FamilyInsightSummary, type FamilyInsightItem, type WellbeingSummary } from "@/lib/api";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import StatusBadge from "@/components/StatusBadge";
import PageHeader from "@/components/ui/PageHeader";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import MetricCard from "@/components/ui/MetricCard";
import SectionHeader from "@/components/ui/SectionHeader";
import AnimatedNumber from "@/components/ui/AnimatedNumber";
import Badge from "@/components/ui/Badge";
import MasteryChart from "@/components/MasteryChart";
import { ShieldIcon } from "@/components/ConstitutionalCeremony";
import { useChild } from "@/lib/ChildContext";
import { cn } from "@/lib/cn";
import EmptyState from "@/components/ui/EmptyState";
import { useStagger } from "@/lib/useStagger";
import { useMobile } from "@/lib/useMobile";
import PullToRefresh from "@/components/PullToRefresh";
import SwipeAction from "@/components/SwipeAction";

interface TodayActivity { id: string; title: string; activity_type: string; status: string; estimated_minutes: number | null; }
interface AlertItem { title: string; message: string; severity: string; }
interface ChildSummary { id: string; mastered: number; total: number; todayCount: number; }

function ChartUpIcon({ className }: { className?: string }) {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className} aria-hidden="true">
      <polyline points="3 17 9 11 13 15 21 7" />
      <polyline points="14 7 21 7 21 14" />
    </svg>
  );
}

function CalendarIcon({ className }: { className?: string }) {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className} aria-hidden="true">
      <rect x="3" y="4" width="18" height="18" rx="2" />
      <line x1="16" y1="2" x2="16" y2="6" />
      <line x1="8" y1="2" x2="8" y2="6" />
      <line x1="3" y1="10" x2="21" y2="10" />
    </svg>
  );
}

function timeAwareGreeting(): string {
  const h = new Date().getHours();
  if (h < 12) return "Good morning";
  if (h < 17) return "Good afternoon";
  return "Good evening";
}

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

function WellbeingIndicator({ childId }: { childId: string | undefined }) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (!childId) return;
    wellbeing.summary(childId).then(s => setCount(s.total_active)).catch(() => {});
  }, [childId]);
  if (!childId || count === 0) return null;
  return (
    <Link href="/wellbeing" className="flex items-center gap-2 px-3 py-2 bg-(--color-warning-light) border border-(--color-warning)/10 rounded-[10px] text-xs text-(--color-warning) hover:bg-(--color-warning)/10 transition-colors">
      <span className="w-2 h-2 rounded-full bg-(--color-warning) animate-pulse-soft" />
      {count} wellbeing observation{count > 1 ? "s" : ""} to review
    </Link>
  );
}

/** Bento metric card: label + animated value + tone-tinted icon. */
function DashMetric({
  label,
  value,
  href,
  icon,
  tone,
  className,
}: {
  label: string;
  value: number;
  href?: string;
  icon: React.ReactNode;
  tone: "constitutional" | "success" | "accent";
  className?: string;
}) {
  const toneText =
    tone === "constitutional" ? "text-(--color-constitutional)"
    : tone === "success" ? "text-(--color-success)"
    : "text-(--color-accent)";
  const toneBg =
    tone === "constitutional" ? "bg-(--color-constitutional-light)"
    : tone === "success" ? "bg-(--color-success-light)"
    : "bg-(--color-accent-light)";

  const inner = (
    <div className={cn(
      "bg-(--color-surface) rounded-[14px] border border-(--color-border) p-5 h-full",
      "shadow-[var(--shadow-card)]",
      "transition-all duration-200 ease-[cubic-bezier(0.25,0.1,0.25,1)]",
      href && "press-scale hover:shadow-[var(--shadow-card-hover)] hover:-translate-y-[1px]",
      className,
    )}>
      <div className="flex items-start justify-between mb-3">
        <div className="text-xs text-(--color-text-tertiary) uppercase tracking-wide">{label}</div>
        <div className={cn("h-8 w-8 rounded-[8px] flex items-center justify-center", toneBg, toneText)}>
          {icon}
        </div>
      </div>
      <div className="text-[26px] sm:text-[30px] font-semibold tracking-tight text-(--color-text) leading-none">
        <AnimatedNumber value={value} />
      </div>
    </div>
  );
  return href ? <Link href={href} className="block h-full">{inner}</Link> : inner;
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
  const [queueItems, setQueueItems] = useState<any[]>([]);

  useEffect(() => { init(); }, []);
  useEffect(() => { if (selectedChild) loadChildDetail(); }, [selectedChild]);

  async function init() {
    try { const me = await auth.me(); setUser(me); } catch { window.location.href = "/auth"; return; }
    try {
      const [qData, rResp, eResp] = await Promise.all([
        governance.queue(3),
        governance.rules(), governance.events(1),
      ]);
      setPendingReviews(qData.total || 0);
      setQueueItems((qData.items || []).slice(0, 3));
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

  async function reload() {
    await init();
    if (selectedChild) await loadChildDetail();
  }

  async function handleQueueApprove(item: any) {
    if (!item.plan_id) return;
    try {
      await governance.approve(item.plan_id, item.activity_id);
      setQueueItems((prev) => prev.filter((i) => i.activity_id !== item.activity_id));
      setPendingReviews((p) => Math.max(0, p - 1));
    } catch {}
  }

  async function handleQueueReject(item: any) {
    if (!item.plan_id) return;
    try {
      await governance.reject(item.plan_id, item.activity_id, "Rejected from dashboard");
      setQueueItems((prev) => prev.filter((i) => i.activity_id !== item.activity_id));
      setPendingReviews((p) => Math.max(0, p - 1));
    } catch {}
  }

  const isMobile = useMobile();
  const cardVisibility = useStagger(children.length, 60);

  if (loading || childLoading) return (
    <div className="max-w-5xl"><LoadingSkeleton variant="dashboard" /></div>
  );

  const today = new Date().toLocaleDateString("en-US", { weekday: "long", year: "numeric", month: "long", day: "numeric" });
  const greeting = timeAwareGreeting();
  const ownerName = user?.display_name?.split(" ")[0] || "";
  const totalToday = Object.values(summaries).reduce((sum, s) => sum + (s?.todayCount || 0), 0);
  const heroSummary =
    children.length === 0
      ? "Add your first learner to get started."
      : totalToday === 0
        ? "All caught up for today."
        : `${totalToday} ${totalToday === 1 ? "activity" : "activities"} planned today across ${children.length} ${children.length === 1 ? "child" : "children"}.`;
  const totalMastered = Object.values(summaries).reduce((sum, s) => sum + (s?.mastered || 0), 0);
  const masterySegments = childState ? [
    { label: "Mastered", count: childState.mastered_count, color: "bg-(--color-success)" },
    { label: "In Progress", count: childState.in_progress_count, color: "bg-(--color-accent)" },
    { label: "Not Started", count: childState.not_started_count, color: "bg-(--color-border)" },
  ] : [];
  const masteryTotal = masterySegments.reduce((s, m) => s + m.count, 0);

  const content = (
    <div className="max-w-5xl">
      {/* ── Hero ── */}
      <header className="mb-6">
        <h1 className="text-[24px] sm:text-[28px] font-semibold tracking-tight text-(--color-text) animate-fade-up">
          {greeting}{ownerName ? `, ${ownerName}` : ""}
        </h1>
        <p className="mt-1 text-sm text-(--color-text-secondary) animate-fade-up stagger-1">
          {heroSummary} <span className="text-(--color-text-tertiary)">· {today}</span>
        </p>
      </header>

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button variant="ghost" size="sm" onClick={() => { setError(""); init(); }}>Retry</Button>
          </div>
        </Card>
      )}

      {/* ── Empty state for first-run households ── */}
      {children.length === 0 && !childLoading && (
        <div className="animate-fade-up stagger-2">
          <EmptyState
            icon="empty"
            title="Add your first child to get started"
            description="METHEAN tailors every plan to a specific learner. Once you add a child we'll build their first weekly schedule."
            action={
              <Link href="/onboarding" className="inline-flex items-center justify-center gap-2 rounded-[10px] font-medium px-5 py-2.5 text-[14px] bg-(--color-accent) text-white hover:bg-(--color-accent-hover) press-scale">
                Add a child
              </Link>
            }
          />
        </div>
      )}

      {/* ── Bento metric row ── */}
      {children.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 sm:gap-4 mb-6">
          <div className="animate-fade-up stagger-2">
            <DashMetric
              label="Governance"
              value={pendingReviews}
              href="/governance/queue"
              icon={<ShieldIcon size={16} />}
              tone="constitutional"
            />
          </div>
          <div className="animate-fade-up stagger-3">
            <DashMetric
              label="Mastery"
              value={totalMastered}
              icon={<ChartUpIcon className="h-4 w-4" />}
              tone="success"
            />
          </div>
          <div className="animate-fade-up stagger-4 col-span-2 sm:col-span-1">
            <DashMetric
              label="Today"
              value={totalToday}
              icon={<CalendarIcon className="h-4 w-4" />}
              tone="accent"
            />
          </div>
        </div>
      )}

      {/* ── Governance queue preview ── */}
      {children.length > 0 && (
        <div className="mb-6 animate-fade-up stagger-5">
          {pendingReviews > 0 ? (
            <Card borderLeft="border-l-(--color-constitutional)" className="flex items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="h-8 w-8 rounded-[8px] flex items-center justify-center bg-(--color-constitutional-light) text-(--color-constitutional) shrink-0">
                  <ShieldIcon size={16} />
                </div>
                <div>
                  <div className="text-sm font-medium text-(--color-text)">
                    {pendingReviews} {pendingReviews === 1 ? "item" : "items"} awaiting your review
                  </div>
                  <div className="text-xs text-(--color-text-secondary)">Approve or adjust before locking the plan.</div>
                </div>
              </div>
              <Link href="/governance/queue">
                <Button variant="secondary" size="sm">Review</Button>
              </Link>
            </Card>
          ) : (
            <Card className="flex items-center gap-3" borderLeft="border-l-(--color-success)">
              <div className="h-7 w-7 rounded-full flex items-center justify-center bg-(--color-success-light) text-(--color-success) shrink-0">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <polyline points="20 6 9 17 4 12" />
                </svg>
              </div>
              <div className="text-sm text-(--color-text)">Governance queue clear</div>
            </Card>
          )}
        </div>
      )}
      {isMobile ? (
        /* Mobile: horizontal snap-scroll carousel */
        <div className="mb-6">
          <div className="flex gap-4 overflow-x-auto snap-x snap-mandatory pb-3 -mx-4 px-4 scroll-fade-right">
            {children.map((c) => {
              const s = summaries[c.id];
              const pct = s && s.total > 0 ? Math.round((s.mastered / s.total) * 100) : 0;
              const isSelected = selectedChild?.id === c.id;
              const circ = 2 * Math.PI * 20;
              return (
                <div key={c.id} className="snap-center shrink-0 w-[85vw] max-w-[340px]">
                  <Card onClick={() => setSelectedChild(c)} selected={isSelected} padding="p-4" className="press-scale">
                    <div className="flex items-center gap-3">
                      <div className="relative w-12 h-12 shrink-0">
                        <svg className="w-12 h-12 -rotate-90" viewBox="0 0 48 48">
                          <circle cx="24" cy="24" r="20" fill="none" stroke="var(--color-border)" strokeWidth="3.5" />
                          <circle cx="24" cy="24" r="20" fill="none" stroke="var(--color-success)" strokeWidth="3.5"
                            strokeDasharray={`${(pct / 100) * circ} ${circ}`} strokeLinecap="round" />
                        </svg>
                        <div className="absolute inset-0 flex items-center justify-center text-xs font-medium text-(--color-text)">{pct}%</div>
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-[15px] font-medium text-(--color-text)">{c.first_name}</div>
                        <div className="text-[13px] text-(--color-text-secondary)">{c.grade_level || ""}</div>
                        <div className="text-[13px] text-(--color-text-tertiary) mt-0.5">
                          {s ? `${s.mastered}/${s.total} mastered · ${s.todayCount} today` : "..."}
                        </div>
                      </div>
                    </div>
                  </Card>
                </div>
              );
            })}
          </div>
          {children.length > 1 && (
            <div className="flex justify-center gap-1.5 mt-2">
              {children.map((c) => (
                <span key={c.id} className={cn("w-2 h-2 rounded-full transition-colors", selectedChild?.id === c.id ? "bg-(--color-accent)" : "bg-(--color-border-strong)")} />
              ))}
            </div>
          )}
        </div>
      ) : (
        /* Desktop: grid */
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
      )}

      {selectedChild && (
        <>
          {/* ── Activities + Alerts ── */}
          {isMobile ? (
            <>
              {/* Mobile: sticky header + full-width activity cards */}
              <div className="sticky z-10 bg-(--color-page) py-2 -mx-4 px-4" style={{ top: "calc(48px + var(--safe-top))" }}>
                <SectionHeader title={`${selectedChild.first_name}'s Activities`} />
              </div>
              {todayActivities.length === 0 ? (
                <div className="py-8 text-center text-sm text-(--color-text-tertiary)">No activities scheduled today.</div>
              ) : (
                <div className="space-y-2 mb-6">
                  {[...todayActivities].sort((a, b) => (a.status === "completed" ? 1 : 0) - (b.status === "completed" ? 1 : 0)).map((a) => {
                    const typeIcons: Record<string, string> = { lesson: "\uD83D\uDCD6", practice: "\u270F\uFE0F", review: "\uD83D\uDD04", assessment: "\uD83D\uDCCB", project: "\uD83D\uDD28", field_trip: "\uD83E\uDDED" };
                    const statusColor = a.status === "completed" ? "var(--color-success)" : a.status === "in_progress" ? "var(--color-warning)" : "var(--color-border-strong)";
                    return (
                      <div key={a.id} className={cn("flex items-center gap-3 p-3 rounded-xl bg-(--color-surface) border border-(--color-border) shadow-sm press-scale", a.status === "completed" && "opacity-50")} style={{ minHeight: 64 }}>
                        <div className="w-10 h-10 rounded-full flex items-center justify-center text-lg shrink-0" style={{ background: "var(--color-accent-light)" }}>
                          {typeIcons[a.activity_type] || "\uD83D\uDCC4"}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="font-semibold text-[15px] text-(--color-text) truncate">{a.title}</div>
                          <div className="text-[13px] text-(--color-text-secondary)">{a.activity_type}{a.estimated_minutes ? ` · ${a.estimated_minutes} min` : ""}</div>
                        </div>
                        <div className="w-3 h-3 rounded-full shrink-0" style={{ background: statusColor }} />
                      </div>
                    );
                  })}
                </div>
              )}

              {/* Mobile: governance queue preview with SwipeAction */}
              {queueItems.length > 0 && (
                <>
                  <div className="sticky z-10 bg-(--color-page) py-2 -mx-4 px-4" style={{ top: "calc(48px + var(--safe-top))" }}>
                    <SectionHeader title="Approval Queue" actionHref="/governance/queue" action={`View all (${pendingReviews})`} />
                  </div>
                  <div className="space-y-2 mb-6">
                    {queueItems.map((item) => (
                      <SwipeAction key={item.activity_id}
                        onSwipeRight={() => handleQueueApprove(item)}
                        onSwipeLeft={() => handleQueueReject(item)}
                        leftLabel="Approve" rightLabel="Reject"
                        leftColor="var(--color-success)" rightColor="var(--color-danger)">
                        <div className="p-3 bg-(--color-surface) border border-(--color-border) rounded-xl">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-[13px] font-bold text-(--color-text)">{item.child_name}</span>
                            <StatusBadge status={item.activity_type} />
                          </div>
                          <div className="text-sm text-(--color-text)">{item.title}</div>
                          {item.ai_rationale && <div className="text-xs text-(--color-text-tertiary) mt-1 line-clamp-1 italic">{item.ai_rationale}</div>}
                        </div>
                      </SwipeAction>
                    ))}
                  </div>
                </>
              )}

              {/* Mobile: alerts */}
              {alerts.length > 0 && (
                <>
                  <div className="sticky z-10 bg-(--color-page) py-2 -mx-4 px-4" style={{ top: "calc(48px + var(--safe-top))" }}>
                    <SectionHeader title="Attention Needed" />
                  </div>
                  <div className="space-y-2 mb-6">
                    {alerts.map((a, i) => (
                      <div key={i} className="flex items-start gap-2 p-3 bg-(--color-surface) border border-(--color-border) rounded-xl">
                        <span className={cn("mt-1 w-2 h-2 rounded-full shrink-0",
                          a.severity === "action_required" ? "bg-(--color-danger)" : a.severity === "warning" ? "bg-(--color-warning)" : "bg-(--color-accent)"
                        )} />
                        <div>
                          <div className="text-[13px] font-medium text-(--color-text)">{a.title}</div>
                          <div className="text-xs text-(--color-text-tertiary) line-clamp-2">{a.message}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </>
          ) : (
            /* Desktop: unchanged grid layout */
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
              <div className="lg:col-span-2 animate-fade-up stagger-6">
                <Card padding="p-0">
                  <div className="px-5 py-3 border-b border-(--color-border)">
                    <SectionHeader title={`${selectedChild.first_name}'s Activities Today`} />
                  </div>
                  {todayActivities.length === 0 ? (
                    <div className="px-5 py-8 text-center text-sm text-(--color-text-tertiary)">No activities scheduled for today. Generate a weekly plan or build a curriculum to get started.</div>
                  ) : todayActivities.map((a, idx) => {
                    const borderColor = a.status === "completed"
                      ? "border-l-(--color-success)"
                      : a.status === "in_progress"
                      ? "border-l-(--color-progress)"
                      : "border-l-(--color-blocked)";
                    const badgeVariant = a.status === "completed"
                      ? "mastered"
                      : a.status === "in_progress"
                      ? "progressing"
                      : "blocked";
                    return (
                      <div
                        key={a.id}
                        className={cn(
                          "flex items-center justify-between gap-3 px-5 py-3 border-b border-(--color-border)/50 last:border-0",
                          "border-l-[3px]", borderColor,
                          a.status === "completed" && "opacity-60",
                          `animate-fade-up stagger-${Math.min(8, idx + 1)}`,
                        )}
                      >
                        <div className="flex items-center gap-3 min-w-0">
                          <span className="text-sm text-(--color-text) truncate">{a.title}</span>
                          <Badge variant={badgeVariant} withDot={false}>{a.activity_type}</Badge>
                          {children.length > 1 && (
                            <span className="text-[11px] text-(--color-text-tertiary) shrink-0">{selectedChild.first_name}</span>
                          )}
                        </div>
                        {a.estimated_minutes && (
                          <span className="text-xs text-(--color-text-tertiary) shrink-0">{a.estimated_minutes}m</span>
                        )}
                      </div>
                    );
                  })}
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
          )}

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
          <div className="animate-fade-up stagger-7 mb-3">
            <FamilyInsightsWidget childCount={children.length} />
          </div>
          <div className="animate-fade-up stagger-8 mb-3">
            <WellbeingIndicator childId={selectedChild?.id} />
          </div>

          {/* ── Weekly Summary ── */}
          {isMobile ? (
            <div className="grid grid-cols-2 gap-3 mb-6">
              <MetricCard label="Completed" value={weeklyStats.completed} className="p-3" />
              <MetricCard label="Minutes" value={`${weeklyStats.minutes}m`} className="p-3" />
              <MetricCard label="Mastered" value={weeklyStats.mastered} color="text-(--color-success)" className="p-3" />
              <MetricCard label="Pending" value={pendingReviews} color={pendingReviews > 0 ? "text-(--color-warning)" : "text-(--color-success)"} className="p-3" />
            </div>
          ) : (
            <div className="flex items-center gap-4 text-xs text-(--color-text-tertiary) mb-6">
              <span>Today: {weeklyStats.completed} completed</span>
              <span>{weeklyStats.minutes}m planned</span>
              <span>{weeklyStats.mastered} nodes mastered</span>
            </div>
          )}
        </>
      )}
    </div>
  );

  return isMobile ? <PullToRefresh onRefresh={reload}>{content}</PullToRefresh> : content;
}
