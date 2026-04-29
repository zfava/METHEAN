"use client";

import { useEffect, useMemo, useState } from "react";
import { compliance, documents, household } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import Badge, { type BadgeVariant } from "@/components/ui/Badge";
import ProgressRing from "@/components/ui/ProgressRing";

type ComplianceCheck = {
  requirement: string;
  status: "met" | "not_met" | "at_risk" | "on_track" | "unknown";
  evidence?: string;
  action?: string;
};

type ComplianceResult = {
  state: string;
  state_code: string;
  strictness: string;
  compliant: boolean;
  score: number;
  checks: ComplianceCheck[];
  total_hours: number;
  hours_by_subject: Record<string, number>;
  special_notes: string;
};

const ACADEMIC_YEAR = "2026-2027";
const ACADEMIC_START = "2026-09-01";
const ACADEMIC_END = "2027-06-30";

// The compliance engine returns hours-related checks like
//   { requirement: "900 annual hours (1-5)",
//     evidence: "742 hours logged, 158 remaining" }
// Pull the numbers back out so the requirement card can render a
// progress bar + ring instead of a flat sentence.
function parseHoursProgress(check: ComplianceCheck) {
  if (!check.requirement.includes("annual hours")) return null;
  const reqMatch = check.requirement.match(/^(\d+)\s+annual hours/);
  const evMatch = check.evidence?.match(/([\d.]+)\s+hours logged,\s*([\d.]+)\s+remaining/);
  if (!reqMatch || !evMatch) return null;
  return {
    required: Number(reqMatch[1]),
    current: Number(evMatch[1]),
    remaining: Number(evMatch[2]),
  };
}

function statusBadge(status: ComplianceCheck["status"]): { variant: BadgeVariant; label: string } {
  switch (status) {
    case "met": return { variant: "mastered", label: "Met" };
    case "not_met": return { variant: "danger", label: "Not met" };
    case "at_risk": return { variant: "danger", label: "At risk" };
    case "on_track": return { variant: "progressing", label: "On track" };
    default: return { variant: "blocked", label: "Pending" };
  }
}

function CheckIcon() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12" />
    </svg>
  );
}
function WarnIcon() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z" />
      <line x1="12" y1="9" x2="12" y2="13" />
      <line x1="12" y1="17" x2="12.01" y2="17" />
    </svg>
  );
}
function AlertIcon() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  );
}
function DocIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
      <line x1="9" y1="13" x2="15" y2="13" />
      <line x1="9" y1="17" x2="15" y2="17" />
    </svg>
  );
}

export default function CompliancePage() {
  useEffect(() => { document.title = "Compliance | METHEAN"; }, []);

  const { selectedChild } = useChild();
  const [states, setStates] = useState<{ code: string; name: string; strictness: string }[]>([]);
  const [selectedState, setSelectedState] = useState("");
  const [householdState, setHouseholdState] = useState<string | null>(null);
  const [result, setResult] = useState<ComplianceResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Pull the household's configured home_state on mount so we can
  // pre-select the dropdown. The auto-run effect below will then
  // fire the check without parent action.
  useEffect(() => {
    compliance.states().then(setStates).catch(() => {});
    household.get()
      .then((d: any) => {
        if (d?.home_state) {
          setHouseholdState(d.home_state);
          setSelectedState((s) => s || d.home_state);
        }
      })
      .catch(() => {});
  }, []);

  async function runCheck() {
    if (!selectedChild || !selectedState) return;
    setLoading(true);
    setError("");
    try {
      const r = await compliance.check(selectedChild.id, selectedState);
      setResult(r as ComplianceResult);
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't check compliance status.");
    } finally { setLoading(false); }
  }

  useEffect(() => { if (selectedState && selectedChild) runCheck(); }, [selectedState, selectedChild]);

  // Persistent status banner: bucket checks into "real problems"
  // (not_met / at_risk → red overdue) vs "parent input pending"
  // (unknown → gold action-needed). Compliant overrides both.
  const banner = useMemo(() => {
    if (!result) return null;
    const actionItems = result.checks.filter((c) => c.status === "not_met" || c.status === "at_risk");
    const pendingItems = result.checks.filter((c) => c.status === "unknown");

    if (result.compliant) {
      return {
        tone: "success" as const,
        border: "border-l-(--color-success)",
        toneClass: "text-(--color-success)",
        icon: <CheckIcon />,
        title: `Your ${result.state} compliance is current.`,
        body: "All tracked requirements are met. Keep logging instruction hours and we'll surface anything new.",
        ringTone: "success" as const,
        items: [] as ComplianceCheck[],
      };
    }
    if (actionItems.length > 0) {
      return {
        tone: "danger" as const,
        border: "border-l-(--color-danger)",
        toneClass: "text-(--color-danger)",
        icon: <AlertIcon />,
        title: actionItems.length === 1 ? "Compliance action overdue." : `${actionItems.length} compliance items overdue.`,
        body: `${result.state}: the items below need immediate attention.`,
        ringTone: "danger" as const,
        items: actionItems,
      };
    }
    return {
      tone: "warning" as const,
      border: "border-l-(--color-warning)",
      toneClass: "text-(--color-warning)",
      icon: <WarnIcon />,
      title: pendingItems.length === 1 ? "1 item needs attention." : `${pendingItems.length} items need attention.`,
      body: `${result.state}: complete the steps below to bring your status to 100%.`,
      ringTone: "gold" as const,
      items: pendingItems,
    };
  }, [result]);

  if (!selectedChild) return <div className="text-sm text-(--color-text-secondary)">Select a child.</div>;

  return (
    <div className="max-w-5xl">
      <PageHeader title="State Compliance" subtitle="You're covered. Here's exactly where things stand." />

      {/* State selector — prominent at top. If household has a
          home_state, it's pre-selected and the auto-run effect
          fires the check without the parent pressing anything. */}
      <Card className="mb-6">
        <div className="flex flex-col sm:flex-row sm:items-end gap-3">
          <div className="flex-1">
            <label htmlFor="cstate" className="block text-[12px] uppercase tracking-[0.06em] text-(--color-text-tertiary) mb-1.5">
              Reporting state
            </label>
            <select
              id="cstate"
              value={selectedState}
              onChange={(e) => setSelectedState(e.target.value)}
              className="w-full px-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)"
            >
              <option value="">Select your state…</option>
              {states.sort((a, b) => a.name.localeCompare(b.name)).map((s) => (
                <option key={s.code} value={s.code}>{s.name} ({s.strictness} regulation)</option>
              ))}
            </select>
          </div>
          <p className="text-xs text-(--color-text-tertiary) sm:pb-2.5">
            {householdState && selectedState === householdState
              ? "Pre-selected from household settings"
              : `${states.length} states + DC supported`}
          </p>
        </div>
      </Card>

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-4">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button variant="ghost" size="sm" onClick={() => { setError(""); runCheck(); }}>Retry</Button>
          </div>
        </Card>
      )}

      {loading && <LoadingSkeleton variant="list" count={5} />}

      {result && !loading && banner && (
        <div className="space-y-6">
          {/* Persistent status banner. Spans full width on every
              breakpoint per spec. */}
          <Card borderLeft={banner.border}>
            <div className="flex items-start gap-4">
              <div className={`shrink-0 mt-0.5 ${banner.toneClass}`}>{banner.icon}</div>
              <div className="flex-1 min-w-0">
                <h2 className="text-[17px] font-semibold text-(--color-text) tracking-tight">{banner.title}</h2>
                <p className="text-sm text-(--color-text-secondary) mt-1">{banner.body}</p>
                {banner.items.length > 0 && (
                  <ul className="mt-3 space-y-1.5">
                    {banner.items.slice(0, 5).map((it, i) => (
                      <li key={i} className="text-sm text-(--color-text) flex items-start gap-2">
                        <span className="text-(--color-text-tertiary) shrink-0 mt-0.5">•</span>
                        <span>
                          <span className="font-medium">{it.requirement}</span>
                          {(it.action || it.evidence) && (
                            <span className="text-(--color-text-secondary)"> — {it.action || it.evidence}</span>
                          )}
                        </span>
                      </li>
                    ))}
                    {banner.items.length > 5 && (
                      <li className="text-xs text-(--color-text-tertiary) pl-4">+{banner.items.length - 5} more in the checklist below</li>
                    )}
                  </ul>
                )}
              </div>
              <div className="shrink-0 hidden sm:block">
                <ProgressRing
                  value={result.score}
                  size={72}
                  strokeWidth={6}
                  tone={banner.ringTone}
                />
              </div>
            </div>
          </Card>

          {/* Requirements checklist. 1 col mobile, 2 col on lg+
              per spec; status surfaces via Badge, hours
              requirements get an inline progress bar + ring. */}
          <div>
            <div className="flex items-baseline justify-between mb-3">
              <h3 className="text-[15px] font-semibold text-(--color-text)">Requirements</h3>
              <p className="text-xs text-(--color-text-tertiary) capitalize">{result.strictness} regulation</p>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
              {result.checks.map((c, i) => {
                const badge = statusBadge(c.status);
                const hours = parseHoursProgress(c);
                const ringTone = c.status === "met" ? "success" : c.status === "at_risk" || c.status === "not_met" ? "danger" : "gold";
                const barColor = c.status === "met"
                  ? "var(--color-success)"
                  : c.status === "at_risk"
                  ? "var(--color-danger)"
                  : "var(--color-brand-gold)";
                return (
                  <Card key={i}>
                    <div className="flex items-start justify-between gap-3 mb-1.5">
                      <h4 className="text-sm font-medium text-(--color-text) flex-1">{c.requirement}</h4>
                      <Badge variant={badge.variant}>{badge.label}</Badge>
                    </div>
                    {c.evidence && !hours && (
                      <p className="text-xs text-(--color-text-secondary)">{c.evidence}</p>
                    )}
                    {c.action && (
                      <p className="text-xs text-(--color-text-secondary)">{c.action}</p>
                    )}
                    {hours && (
                      <div className="mt-3 flex items-center gap-3">
                        <ProgressRing
                          value={(hours.current / hours.required) * 100}
                          size={56}
                          strokeWidth={5}
                          tone={ringTone}
                        />
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-medium text-(--color-text)">
                            {Math.round(hours.current)} of {hours.required} required hours
                          </div>
                          <div className="h-1.5 bg-(--color-border) rounded-full overflow-hidden mt-1.5">
                            <div
                              className="h-full rounded-full transition-all duration-500"
                              style={{
                                width: `${Math.min(100, (hours.current / hours.required) * 100)}%`,
                                background: barColor,
                              }}
                            />
                          </div>
                          <p className="text-xs text-(--color-text-tertiary) mt-1">
                            {hours.remaining > 0 ? `${Math.round(hours.remaining)} hours remaining` : "Goal reached"}
                          </p>
                        </div>
                      </div>
                    )}
                  </Card>
                );
              })}
            </div>
          </div>

          {/* State-specific guidance from the compliance engine.
              Many states have nuance the checklist can't capture
              (waivers, timing windows, etc.) — surface as a
              persistent note instead of a hover tooltip. */}
          {result.special_notes && (
            <Card borderLeft="border-l-(--color-warning)">
              <div className="text-xs text-(--color-text-secondary) leading-relaxed">
                <span className="font-medium text-(--color-warning)">{result.state} note: </span>
                {result.special_notes}
              </div>
            </Card>
          )}

          {/* Document generation. Each card is a download link to
              the existing API URLs — no API changes. The IHIP +
              quarterly reports only render for high-regulation
              states; attendance and transcript are universal. */}
          <div>
            <div className="flex items-baseline justify-between mb-3">
              <h3 className="text-[15px] font-semibold text-(--color-text)">Documents</h3>
              <p className="text-xs text-(--color-text-tertiary)">For {selectedChild.first_name} · {ACADEMIC_YEAR}</p>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {result.strictness === "high" && (
                <DocCard
                  title="Compliance Report (IHIP)"
                  subtitle="Individualized Home Instruction Plan — required for high-regulation states."
                  href={documents.ihip(selectedChild.id, ACADEMIC_YEAR, selectedState)}
                  primary
                />
              )}
              <DocCard
                title="Attendance Record"
                subtitle="School days and instruction hours, full academic year."
                href={documents.attendance(selectedChild.id, ACADEMIC_START, ACADEMIC_END)}
                primary={result.strictness !== "high"}
              />
              <DocCard
                title="Academic Transcript"
                subtitle="Cumulative record across all subjects and years."
                href={documents.transcript(selectedChild.id)}
              />
              {result.strictness === "high" && [1, 2, 3, 4].map((q) => (
                <DocCard
                  key={q}
                  title={`Q${q} Progress Report`}
                  subtitle={`Mastery, hours, and activities for quarter ${q}.`}
                  href={documents.quarterlyReport(selectedChild.id, q, ACADEMIC_YEAR)}
                />
              ))}
            </div>
          </div>

          {/* Hours-by-subject breakdown — secondary detail, kept
              at the bottom so it doesn't compete with the banner
              + checklist. */}
          {result.hours_by_subject && Object.keys(result.hours_by_subject).length > 0 && (
            <Card>
              <h3 className="text-[15px] font-semibold text-(--color-text) mb-3">Hours by subject</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6">
                {Object.entries(result.hours_by_subject).map(([subj, hrs]) => (
                  <div key={subj} className="flex items-center justify-between border-b border-(--color-border)/60 py-2">
                    <span className="text-sm text-(--color-text)">{subj}</span>
                    <span className="text-sm font-mono text-(--color-text-secondary)">{hrs as number}h</span>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}

function DocCard({ title, subtitle, href, primary = false }: {
  title: string; subtitle: string; href: string; primary?: boolean;
}) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener"
      className={`block group rounded-[14px] border transition-all duration-200 ease-[cubic-bezier(0.25,0.1,0.25,1)] hover:shadow-[var(--shadow-card-hover)] hover:-translate-y-[1px] p-4 ${
        primary
          ? "bg-(--color-accent-light) border-(--color-accent)/30 hover:border-(--color-accent)"
          : "bg-(--color-surface) border-(--color-border) hover:border-(--color-border-strong)"
      }`}
    >
      <div className="flex items-start gap-3">
        <div className={`shrink-0 mt-0.5 ${primary ? "text-(--color-accent)" : "text-(--color-text-secondary)"}`}>
          <DocIcon />
        </div>
        <div className="flex-1 min-w-0">
          <div className={`text-sm font-medium ${primary ? "text-(--color-accent)" : "text-(--color-text)"}`}>{title}</div>
          <div className="text-xs text-(--color-text-secondary) mt-0.5 leading-relaxed">{subtitle}</div>
        </div>
        <span className={`shrink-0 text-xs ${primary ? "text-(--color-accent)" : "text-(--color-text-tertiary)"} transition-transform group-hover:translate-x-0.5`}>
          →
        </span>
      </div>
    </a>
  );
}
