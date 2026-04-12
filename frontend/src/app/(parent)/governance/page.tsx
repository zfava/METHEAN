"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { governance, household, type GovernanceEvent, type GovernanceRule } from "@/lib/api";
import { relativeTime } from "@/lib/format";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import StatusBadge from "@/components/StatusBadge";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import SectionHeader from "@/components/ui/SectionHeader";
import EmptyState from "@/components/ui/EmptyState";
import { cn } from "@/lib/cn";
import EvaluationChain from "@/components/EvaluationChain";

const RULE_TYPE_LABELS: Record<string, { label: string; icon: string }> = {
  approval_required: { label: "Approval", icon: "🛡️" },
  pace_limit: { label: "Pace Limits", icon: "⏱️" },
  content_filter: { label: "Content Filters", icon: "📋" },
  schedule_constraint: { label: "Schedule", icon: "📅" },
  ai_boundary: { label: "AI Boundaries", icon: "🤖" },
};

export default function GovernanceOverviewPage() {
  useEffect(() => { document.title = "Governance | METHEAN"; }, []);

  const [events, setEvents] = useState<GovernanceEvent[]>([]);
  const [rules, setRules] = useState<GovernanceRule[]>([]);
  const [pendingCount, setPendingCount] = useState(0);
  const [philSummary, setPhilSummary] = useState<{ philosophy: string; autonomy: string; boundaries: number }>({ philosophy: "", autonomy: "", boundaries: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [expandedEvent, setExpandedEvent] = useState<string | null>(null);
  const [govIntel, setGovIntel] = useState<any>(null);

  useEffect(() => { load(); }, []);

  async function load() {
    setLoading(true);
    setError("");
    try {
      const [evtsRaw, rulesRaw, qResp, philResp] = await Promise.all([
        governance.events(200),
        governance.rules(),
        governance.queue(1).catch(() => ({ items: [], total: 0 })),
        household.getPhilosophy().catch(() => ({})),
      ]);

      const evtsList: GovernanceEvent[] = (evtsRaw as any).items || evtsRaw;
      setEvents(Array.isArray(evtsList) ? evtsList : []);
      const rulesList = (rulesRaw as any).items || rulesRaw;
      setRules(Array.isArray(rulesList) ? rulesList : []);
      setPendingCount(qResp.total || 0);
      setPhilSummary({
        philosophy: (philResp.educational_philosophy || "").replace(/_/g, " "),
        autonomy: (philResp.ai_autonomy_level || "").replace(/_/g, " "),
        boundaries: (philResp.content_boundaries || []).length,
      });
      // Load governance intelligence
      governance.governanceIntelligence().then(setGovIntel).catch(() => {});
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't load governance data.");
    } finally {
      setLoading(false);
    }
  }

  if (loading) return <div className="max-w-5xl"><PageHeader title="Governance" /><LoadingSkeleton variant="card" count={4} /></div>;

  // ── Compute metrics ──
  const autoApproved = events.filter((e) => {
    const meta = (e as any).metadata_ || (e as any).metadata || {};
    return e.action === "approve" && (meta.source === "auto" || (e.reason || "").toLowerCase().includes("auto"));
  });
  const manualDecisions = events.filter((e) => {
    const meta = (e as any).metadata_ || (e as any).metadata || {};
    return meta.source === "manual" || (!meta.source && ["approve", "reject", "modify"].includes(e.action) && !(e.reason || "").toLowerCase().includes("auto"));
  });
  const parentControlPct = events.length > 0 ? Math.round((manualDecisions.length / events.length) * 100) : 100;
  const totalApproved = events.filter((e) => e.action === "approve").length;
  const totalRejected = events.filter((e) => e.action === "reject").length;
  const totalModified = events.filter((e) => e.action === "modify").length;
  const totalQueued = pendingCount;

  const constitutionalCount = rules.filter((r) => (r as any).tier === "constitutional" && r.is_active).length;

  // AI autonomy display
  const aiRule = rules.find((r) => r.rule_type === "ai_boundary" && r.is_active);
  const aiTransparency = aiRule ? ((aiRule.parameters as any).ai_transparency || "full") : "not set";
  const aiCanAct = aiRule ? (aiRule.parameters as any).ai_direct_action : false;

  // Rule coverage
  const ruleTypes = ["approval_required", "pace_limit", "content_filter", "schedule_constraint", "ai_boundary"];
  const coverage = ruleTypes.map((type) => {
    const typeRules = rules.filter((r) => r.rule_type === type && r.is_active);
    const hasConstitutional = typeRules.some((r) => (r as any).tier === "constitutional");
    return {
      type,
      ...RULE_TYPE_LABELS[type],
      count: typeRules.length,
      status: hasConstitutional ? "protected" : typeRules.length > 0 ? "covered" : "not_set",
    };
  });

  const recentEvents = events.slice(0, 10);
  const circ = 2 * Math.PI * 20;

  return (
    <div className="max-w-5xl">
      <PageHeader title="Governance" subtitle="You control what the AI can and cannot do." />

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button variant="ghost" size="sm" onClick={() => { setError(""); load(); }}>Retry</Button>
          </div>
        </Card>
      )}

      {/* ── Section 1: Health Bar ── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-8">
        {/* Parent Control Score */}
        <Card padding="p-4">
          <div className="flex items-center gap-3">
            <div className="relative w-12 h-12 shrink-0">
              <svg className="w-12 h-12 -rotate-90" viewBox="0 0 48 48">
                <circle cx="24" cy="24" r="20" fill="none" stroke="var(--color-border)" strokeWidth="3" />
                <circle cx="24" cy="24" r="20" fill="none"
                  stroke={parentControlPct > 50 ? "var(--color-success)" : parentControlPct > 20 ? "var(--color-warning)" : "var(--color-danger)"}
                  strokeWidth="3" strokeDasharray={`${(parentControlPct / 100) * circ} ${circ}`} strokeLinecap="round" />
              </svg>
              <span className="absolute inset-0 flex items-center justify-center text-xs font-bold text-(--color-text)">{parentControlPct}%</span>
            </div>
            <div>
              <div className="text-xs font-medium text-(--color-text)">Parent Control</div>
              <div className="text-[10px] text-(--color-text-tertiary)">{manualDecisions.length} of {events.length} decisions</div>
            </div>
          </div>
        </Card>

        {/* AI Autonomy Level */}
        <Card padding="p-4">
          <div className="flex items-center gap-3">
            <div className={cn("w-12 h-12 rounded-full flex items-center justify-center text-lg shrink-0",
              aiTransparency === "full" ? "bg-(--color-success-light) text-(--color-success)" :
              aiTransparency === "summary" ? "bg-(--color-warning-light) text-(--color-warning)" :
              "bg-(--color-danger-light) text-(--color-danger)")}>
              {aiTransparency === "full" ? "🛡️" : aiTransparency === "summary" ? "👁️" : "⚠️"}
            </div>
            <div>
              <div className="text-xs font-medium text-(--color-text)">AI Oversight</div>
              <div className="text-[10px] text-(--color-text-tertiary) capitalize">{aiTransparency}</div>
              <div className="text-[10px] text-(--color-text-tertiary)">{aiCanAct ? "Can act alone" : "Review required"}</div>
            </div>
          </div>
        </Card>

        {/* Pending Review */}
        <Card padding="p-4" href={pendingCount > 0 ? "/governance/queue" : undefined}>
          <div className="flex items-center gap-3">
            <div className={cn("w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold shrink-0",
              pendingCount > 0 ? "bg-(--color-warning-light) text-(--color-warning)" : "bg-(--color-success-light) text-(--color-success)")}>
              {pendingCount}
            </div>
            <div>
              <div className="text-xs font-medium text-(--color-text)">Pending Review</div>
              <div className="text-[10px] text-(--color-text-tertiary)">{pendingCount > 0 ? "Needs attention" : "All clear"}</div>
            </div>
          </div>
        </Card>

        {/* Constitutional Rules */}
        <Card padding="p-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-(--color-constitutional-light) text-(--color-constitutional) flex items-center justify-center text-lg font-bold shrink-0">
              {constitutionalCount}
            </div>
            <div>
              <div className="text-xs font-medium text-(--color-text)">Constitutional</div>
              <div className="text-[10px] text-(--color-text-tertiary)">{constitutionalCount} foundational rule{constitutionalCount !== 1 ? "s" : ""}</div>
            </div>
          </div>
        </Card>
      </div>

      {/* ── Section 1.5: Governance Intelligence ── */}
      <Card className="mb-8" padding="p-4 sm:p-5">
        <SectionHeader title="What METHEAN Has Learned From Your Reviews" />
        {!govIntel || !govIntel.sufficient_data ? (
          <p className="text-xs text-(--color-text-tertiary) mt-2">
            {govIntel?.event_count > 0
              ? `METHEAN has ${govIntel.event_count} governance events — it needs at least 10 to learn your patterns. Keep reviewing!`
              : "METHEAN needs more review history to learn your patterns. Keep reviewing, and insights will appear here."}
          </p>
        ) : (
          <div className="space-y-4 mt-3">
            {/* Auto-approve zone */}
            {govIntel.auto_approve_ceiling > 0 && (
              <div>
                <div className="text-xs font-medium text-(--color-text) mb-1.5">
                  Auto-approve zone: Difficulty 1–{govIntel.auto_approve_ceiling}
                </div>
                <div className="flex items-center gap-0.5">
                  {[1, 2, 3, 4, 5].map((d) => (
                    <div key={d} className={cn(
                      "flex-1 h-3 rounded-sm text-center",
                      d <= govIntel.auto_approve_ceiling ? "bg-(--color-success)" : d === govIntel.auto_approve_ceiling + 1 ? "bg-(--color-warning)" : "bg-(--color-border)"
                    )}>
                      <span className="text-[8px] text-white font-bold leading-3">{d}</span>
                    </div>
                  ))}
                </div>
                <p className="text-[10px] text-(--color-text-tertiary) mt-1">
                  Activities at difficulty 1–{govIntel.auto_approve_ceiling} are approved {Math.round((govIntel.approval_rate_by_difficulty[govIntel.auto_approve_ceiling] || 0) * 100)}% of the time.
                </p>
              </div>
            )}

            {/* Activity type preferences */}
            {Object.keys(govIntel.approval_rate_by_type || {}).length > 0 && (
              <div>
                <div className="text-xs font-medium text-(--color-text) mb-1.5">Activity preferences</div>
                <div className="space-y-1">
                  {Object.entries(govIntel.approval_rate_by_type)
                    .sort(([, a]: any, [, b]: any) => b - a)
                    .map(([type, rate]: [string, any]) => (
                      <div key={type} className="flex items-center gap-2">
                        <span className="text-[11px] text-(--color-text-secondary) w-24 capitalize truncate">{type.replace(/_/g, " ")}</span>
                        <div className="flex-1 h-2 rounded-full bg-(--color-border)">
                          <div className={cn("h-full rounded-full", rate >= 0.8 ? "bg-(--color-success)" : rate >= 0.5 ? "bg-(--color-warning)" : "bg-(--color-danger)")}
                            style={{ width: `${Math.round(rate * 100)}%` }} />
                        </div>
                        <span className="text-[10px] text-(--color-text-tertiary) w-8 text-right">{Math.round(rate * 100)}%</span>
                      </div>
                    ))}
                </div>
              </div>
            )}

            {/* Review time + event count */}
            <div className="flex items-center gap-6 text-xs text-(--color-text-tertiary)">
              {govIntel.avg_review_hours != null && (
                <span>Avg review time: <strong className="text-(--color-text)">{govIntel.avg_review_hours}h</strong></span>
              )}
              {govIntel.peak_review_time && (
                <span>Most active: <strong className="text-(--color-text) capitalize">{govIntel.peak_review_time}</strong></span>
              )}
              <span>{govIntel.event_count} decisions analyzed</span>
            </div>

            <p className="text-[10px] text-(--color-text-tertiary) italic border-t border-(--color-border) pt-2">
              These patterns inform planning but never bypass your rules. You always have final say.
            </p>
          </div>
        )}
      </Card>

      {/* ── Section 2: Decision Flow ── */}
      <Card className="mb-8" padding="p-5">
        <SectionHeader title="Decision Flow" />
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 sm:gap-0 mt-3">
          {/* AI Recommends */}
          <div className="flex-1 text-center py-3 px-2 rounded-lg bg-(--color-accent-light) border border-(--color-accent)/20">
            <div className="text-lg font-bold text-(--color-accent)">{events.length}</div>
            <div className="text-[10px] text-(--color-accent)">AI Recommendations</div>
          </div>
          <div className="hidden sm:block w-6 text-center text-(--color-border-strong)">→</div>
          <div className="sm:hidden text-center text-(--color-border-strong)">↓</div>
          {/* Rules Evaluate */}
          <div className="flex-1 text-center py-3 px-2 rounded-lg bg-(--color-constitutional-light) border border-(--color-constitutional)/20">
            <div className="text-lg font-bold text-(--color-constitutional)">{rules.filter((r) => r.is_active).length}</div>
            <div className="text-[10px] text-(--color-constitutional)">Active Rules</div>
          </div>
          <div className="hidden sm:block w-6 text-center text-(--color-border-strong)">→</div>
          <div className="sm:hidden text-center text-(--color-border-strong)">↓</div>
          {/* Outcomes */}
          <div className="flex-1 grid grid-cols-2 gap-2">
            <div className="text-center py-2 px-1 rounded-lg bg-(--color-success-light)">
              <div className="text-sm font-bold text-(--color-success)">{autoApproved.length}</div>
              <div className="text-[9px] text-(--color-success)">Auto-approved</div>
            </div>
            <div className="text-center py-2 px-1 rounded-lg bg-(--color-warning-light)">
              <div className="text-sm font-bold text-(--color-warning)">{totalQueued}</div>
              <div className="text-[9px] text-(--color-warning)">Queued</div>
            </div>
            <div className="text-center py-2 px-1 rounded-lg bg-(--color-success-light)">
              <div className="text-sm font-bold text-(--color-success)">{totalApproved - autoApproved.length}</div>
              <div className="text-[9px] text-(--color-success)">Parent OK</div>
            </div>
            <div className="text-center py-2 px-1 rounded-lg bg-(--color-danger-light)">
              <div className="text-sm font-bold text-(--color-danger)">{totalRejected}</div>
              <div className="text-[9px] text-(--color-danger)">Rejected</div>
            </div>
          </div>
        </div>
      </Card>

      {/* ── Section 3: Rule Coverage Matrix ── */}
      <Card className="mb-8" padding="p-5">
        <SectionHeader title="Rule Coverage" action="Manage rules" actionHref="/governance/rules" />
        <div className="mt-3 space-y-2">
          {coverage.map((c) => (
            <div key={c.type} className="flex items-center justify-between py-2 px-3 rounded-[10px] bg-(--color-page)">
              <div className="flex items-center gap-2">
                <span>{c.icon}</span>
                <span className="text-xs font-medium text-(--color-text)">{c.label}</span>
              </div>
              <div className="flex items-center gap-2">
                {c.status === "protected" && (
                  <span className="text-[10px] font-medium text-(--color-constitutional) flex items-center gap-1">🛡️ Protected</span>
                )}
                {c.status === "covered" && (
                  <span className="text-[10px] font-medium text-(--color-success) flex items-center gap-1">
                    <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
                    {c.count} rule{c.count !== 1 ? "s" : ""}
                  </span>
                )}
                {c.status === "not_set" && (
                  <Link href="/governance/rules" className="text-[10px] font-medium text-(--color-warning) hover:underline">
                    — Not set · Add
                  </Link>
                )}
              </div>
            </div>
          ))}
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-8">
        {/* ── Section 4: Recent Timeline ── */}
        <Card padding="p-0">
          <div className="px-5 py-3 border-b border-(--color-border)">
            <SectionHeader title="Recent Decisions" action="Full trace" actionHref="/governance/trace" />
          </div>
          {recentEvents.length === 0 ? (
            <div className="p-5">
              <EmptyState icon="empty" title="No decisions yet" description="As activities are approved and rules applied, every decision appears here." />
            </div>
          ) : (
            <div className="divide-y divide-(--color-border)/30 max-h-80 overflow-y-auto">
              {recentEvents.map((evt) => (
                <div key={evt.id}>
                  <button onClick={() => setExpandedEvent(expandedEvent === evt.id ? null : evt.id)}
                    className="w-full flex items-center justify-between px-5 py-2.5 text-left hover:bg-(--color-page) transition-colors">
                    <div className="flex items-center gap-2 min-w-0">
                      <StatusBadge status={evt.action} />
                      <span className="text-xs text-(--color-text) truncate">{evt.target_type.replace(/_/g, " ")}</span>
                    </div>
                    <span className="text-[10px] text-(--color-text-tertiary) shrink-0 ml-2">{relativeTime(evt.created_at)}</span>
                  </button>
                  {expandedEvent === evt.id && evt.metadata_?.evaluations && (
                    <div className="px-5 pb-2.5">
                      <EvaluationChain evaluations={evt.metadata_.evaluations} blockingRules={evt.metadata_.blocking_rules || []} />
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </Card>

        {/* ── Section 5: Philosophy Summary ── */}
        <Card href="/governance/philosophy" padding="p-5">
          <SectionHeader title="Philosophy" action="Edit" actionHref="/governance/philosophy" />
          <div className="mt-3 space-y-2">
            {philSummary.philosophy ? (
              <>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-(--color-text-secondary)">Approach</span>
                  <span className="text-xs font-medium text-(--color-text) capitalize">{philSummary.philosophy}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-(--color-text-secondary)">AI Autonomy</span>
                  <span className="text-xs font-medium text-(--color-text) capitalize">{philSummary.autonomy || "Not set"}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-(--color-text-secondary)">Content Boundaries</span>
                  <span className="text-xs font-medium text-(--color-text)">{philSummary.boundaries} defined</span>
                </div>
              </>
            ) : (
              <p className="text-xs text-(--color-text-secondary)">No philosophy configured yet. Set your family&apos;s foundational principles.</p>
            )}
          </div>
        </Card>
      </div>

      {/* ── Section 6: Quick Actions ── */}
      <div className="flex flex-wrap gap-3">
        <Button variant="primary" size="md" onClick={() => window.location.href = "/governance/rules"}>Add Rule</Button>
        <Button variant="secondary" size="md" onClick={() => window.location.href = "/governance/reports"}>Generate Report</Button>
        <Button variant="secondary" size="md" onClick={() => window.location.href = "/governance/queue"}>
          Review Queue {pendingCount > 0 && <span className="ml-1 px-1.5 py-0.5 text-[9px] bg-(--color-warning) text-white rounded-full">{pendingCount}</span>}
        </Button>
        <Button variant="ghost" size="md" onClick={() => window.location.href = "/governance/trace"}>Full Trace</Button>
      </div>
    </div>
  );
}
