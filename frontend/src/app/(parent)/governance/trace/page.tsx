"use client";

import { useEffect, useMemo, useState } from "react";
import { governance, type GovernanceEvent } from "@/lib/api";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import EmptyState from "@/components/ui/EmptyState";
import StatusBadge from "@/components/StatusBadge";
import Tooltip from "@/components/ui/Tooltip";
import Button from "@/components/ui/Button";
import { cn } from "@/lib/cn";
import { relativeTime } from "@/lib/format";
import EvaluationChain from "@/components/EvaluationChain";
import { ShieldIcon } from "@/components/ConstitutionalCeremony";

const PAGE_SIZE = 20;

const actionBorderClass: Record<string, string> = {
  approve: "border-l-(--color-success)",
  reject: "border-l-(--color-danger)",
  modify: "border-l-(--color-warning)",
  defer: "border-l-(--color-text-tertiary)",
};

type DateRangeId = "7d" | "30d" | "all";

const DATE_RANGES: { id: DateRangeId; label: string; days: number | null }[] = [
  { id: "7d", label: "Last 7 days", days: 7 },
  { id: "30d", label: "Last 30 days", days: 30 },
  { id: "all", label: "All time", days: null },
];

function SearchIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="11" cy="11" r="8" />
      <line x1="21" y1="21" x2="16.65" y2="16.65" />
    </svg>
  );
}

function absoluteTime(iso: string): string {
  return new Date(iso).toLocaleString("en-US", {
    weekday: "short", month: "short", day: "numeric",
    hour: "numeric", minute: "2-digit",
  });
}

export default function TracePage() {
  useEffect(() => { document.title = "Decision Trace | METHEAN"; }, []);

  const [events, setEvents] = useState<GovernanceEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  const [filterAction, setFilterAction] = useState("");
  const [filterCalibration, setFilterCalibration] = useState(false);
  const [dateRange, setDateRange] = useState<DateRangeId>("30d");
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);

  // The 200-event ceiling is intentionally preserved (no API
  // change). We render PAGE_SIZE at a time below to keep the DOM
  // light and let the parent skim a recent window first.
  useEffect(() => {
    governance.events(200)
      .then((d) => setEvents((d as any).items || d))
      .catch((err: any) => setError(err?.detail || err?.message || "Couldn't load governance events."))
      .finally(() => setLoading(false));
  }, []);

  function toggleExpand(id: string) {
    setExpanded((prev) => {
      const n = new Set(prev);
      if (n.has(id)) n.delete(id);
      else n.add(id);
      return n;
    });
  }

  const calibrationEvents = useMemo(
    () => events.filter((e) => e.target_type === "calibration_profile"),
    [events],
  );
  const actions = useMemo(() => [...new Set(events.map((e) => e.action))], [events]);

  // Calibration scope → date range → action → search. Memoized
  // so Load More clicks don't redo the work; visible slice is
  // computed downstream from the same `filtered` array.
  const filtered = useMemo(() => {
    let pool = filterCalibration ? calibrationEvents : events;
    if (dateRange !== "all") {
      const days = dateRange === "7d" ? 7 : 30;
      const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
      pool = pool.filter((e) => new Date(e.created_at).getTime() >= cutoff);
    }
    if (filterAction) {
      pool = pool.filter((e) => e.action === filterAction);
    }
    if (search.trim()) {
      const q = search.toLowerCase();
      pool = pool.filter((e) =>
        e.action.toLowerCase().includes(q) ||
        e.target_type.toLowerCase().includes(q) ||
        (e.reason ?? "").toLowerCase().includes(q),
      );
    }
    return pool;
  }, [events, calibrationEvents, dateRange, filterAction, filterCalibration, search]);

  // Reset pagination when filters change so a Load More click
  // never reveals items from a stale window.
  useEffect(() => { setVisibleCount(PAGE_SIZE); }, [search, filterAction, filterCalibration, dateRange]);

  const visible = filtered.slice(0, visibleCount);
  const hasMore = filtered.length > visibleCount;
  const filtersActive = !!search || !!filterAction || filterCalibration || dateRange !== "all";

  if (loading) return <div className="max-w-4xl"><LoadingSkeleton variant="list" count={10} /></div>;

  return (
    <div className="max-w-4xl">
      <PageHeader title="Decision Trace" subtitle="Every governance decision, with full reasoning. Parent sovereignty, recorded." />

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <p className="text-sm text-(--color-danger)">{error}</p>
        </Card>
      )}

      {/* Search + filter bar. Search is text-only across action,
          target_type, and reason — those are the closest things
          a GovernanceEvent has to a title and description. */}
      <div className="space-y-3 mb-5">
        <div className="relative">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-(--color-text-tertiary)">
            <SearchIcon />
          </span>
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search decisions, reasons, contexts…"
            className="w-full pl-9 pr-3 py-2.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text) placeholder:text-(--color-text-tertiary) focus:outline-none focus:border-(--color-accent)"
            aria-label="Search governance events"
          />
        </div>

        <div className="flex flex-wrap items-center gap-x-2 gap-y-2">
          <div className="flex flex-wrap items-center gap-1.5">
            {DATE_RANGES.map((r) => (
              <FilterPill
                key={r.id}
                active={dateRange === r.id}
                onClick={() => setDateRange(r.id)}
                tone="accent"
              >
                {r.label}
              </FilterPill>
            ))}
          </div>

          <span className="hidden sm:inline-block h-4 w-px bg-(--color-border) mx-1" />

          <div className="flex flex-wrap items-center gap-1.5">
            <FilterPill
              active={!filterAction && !filterCalibration}
              onClick={() => { setFilterAction(""); setFilterCalibration(false); }}
            >
              All actions
            </FilterPill>
            {actions.map((a) => (
              <FilterPill
                key={a}
                active={filterAction === a && !filterCalibration}
                onClick={() => { setFilterAction(a); setFilterCalibration(false); }}
              >
                <span className="capitalize">{a}</span>
                <span className={cn(
                  "tabular-nums",
                  filterAction === a && !filterCalibration ? "text-white/70" : "text-(--color-text-tertiary)",
                )}>
                  {events.filter((e) => e.action === a).length}
                </span>
              </FilterPill>
            ))}
            {calibrationEvents.length > 0 && (
              <FilterPill
                active={filterCalibration}
                onClick={() => { setFilterCalibration(true); setFilterAction(""); }}
                tone="accent"
              >
                Calibration
                <span className={cn(
                  "tabular-nums",
                  filterCalibration ? "text-white/70" : "text-(--color-text-tertiary)",
                )}>
                  {calibrationEvents.length}
                </span>
              </FilterPill>
            )}
          </div>
        </div>
      </div>

      {/* Count header — always rendered when there's data. */}
      {events.length > 0 && (
        <p className="text-xs text-(--color-text-secondary) mb-3">
          Showing <span className="font-medium text-(--color-text)">{visible.length}</span> of{" "}
          <span className="font-medium text-(--color-text)">{filtered.length}</span> governance{" "}
          {filtered.length === 1 ? "decision" : "decisions"}
          {filtersActive && events.length > filtered.length && (
            <span className="text-(--color-text-tertiary)"> · {events.length} total</span>
          )}
        </p>
      )}

      {filtered.length === 0 ? (
        events.length === 0 ? (
          <EmptyState
            icon="empty"
            title="No governance decisions recorded yet"
            description="As METHEAN's AI makes recommendations, every decision will appear here with full transparency."
          />
        ) : (
          <EmptyState
            icon="search"
            title="No decisions match these filters"
            description="Try clearing search or widening the date range."
          />
        )
      ) : (
        <div className="space-y-2.5">
          {visible.map((evt) => (
            <EventCard
              key={evt.id}
              evt={evt}
              isOpen={expanded.has(evt.id)}
              onToggle={() => toggleExpand(evt.id)}
            />
          ))}

          {hasMore && (
            <div className="pt-2 flex justify-center">
              <Button
                variant="secondary"
                size="sm"
                onClick={() => setVisibleCount((c) => c + PAGE_SIZE)}
              >
                Load {Math.min(PAGE_SIZE, filtered.length - visibleCount)} more
              </Button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function FilterPill({
  active, onClick, children, tone = "neutral",
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
  tone?: "neutral" | "accent";
}) {
  const activeClass = tone === "accent"
    ? "bg-(--color-accent) text-white"
    : "bg-(--color-text) text-white";
  return (
    <button
      onClick={onClick}
      className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-full transition-colors",
        active ? activeClass : "bg-(--color-page) text-(--color-text-secondary) hover:bg-(--color-border)",
      )}
    >
      {children}
    </button>
  );
}

function EventCard({
  evt, isOpen, onToggle,
}: {
  evt: GovernanceEvent;
  isOpen: boolean;
  onToggle: () => void;
}) {
  const isConstitutional = evt.target_type.includes("constitutional");
  const isCalibration = evt.target_type === "calibration_profile";
  const borderLeft = isConstitutional
    ? "border-l-(--color-constitutional)"
    : actionBorderClass[evt.action] || "border-l-(--color-text-tertiary)";

  // Without explicit AI-vs-parent fields on the event, user_id
  // is the cleanest signal: present means a parent-attributed
  // decision, absent means an AI/system-logged event.
  const isParentAction = !!evt.user_id;
  const evaluations = evt.metadata_?.evaluations || [];
  const blockingRules = evt.metadata_?.blocking_rules || [];
  const source = evt.metadata_?.source;

  return (
    <Card borderLeft={borderLeft} padding="p-0">
      <button
        onClick={onToggle}
        className="w-full text-left px-4 py-3.5 sm:px-5"
        aria-expanded={isOpen}
      >
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              {isConstitutional && <ShieldIcon size={12} className="text-(--color-constitutional)" />}
              <StatusBadge status={evt.action} />
              {isConstitutional && <StatusBadge status="constitutional" />}
              <span className="text-sm font-medium text-(--color-text) capitalize">
                {evt.target_type.replace(/_/g, " ")}
              </span>
            </div>
            {evt.reason && (
              <p className="text-xs text-(--color-text-secondary) mt-1.5 line-clamp-1">
                {evt.reason}
              </p>
            )}
          </div>
          <Tooltip content={absoluteTime(evt.created_at)} placement="top">
            <span className="shrink-0 text-xs text-(--color-text-tertiary) tabular-nums">
              {relativeTime(evt.created_at)}
            </span>
          </Tooltip>
        </div>
      </button>

      {isOpen && (
        <div className="px-4 sm:px-5 pb-4 pt-3 border-t border-(--color-border)/60 space-y-3">
          <Section label={isParentAction ? "Parent Decision" : "AI / System Action"}>
            <div className="flex items-center gap-2">
              <StatusBadge status={evt.action} />
              <span className="text-xs text-(--color-text-secondary)">
                on <span className="capitalize">{evt.target_type.replace(/_/g, " ")}</span>
              </span>
            </div>
          </Section>

          {evt.reason && (
            <Section label={isParentAction ? "Parent Notes" : "AI Recommendation"}>
              <div className={cn(
                "text-sm rounded-[10px] px-3 py-2.5 leading-relaxed",
                isConstitutional
                  ? "bg-(--color-constitutional-light) text-(--color-constitutional) italic"
                  : "bg-(--color-page) text-(--color-text)",
              )}>
                {isConstitutional ? `"${evt.reason}"` : evt.reason}
              </div>
            </Section>
          )}

          {evaluations.length > 0 && (
            <Section label="Governance Rules Applied">
              <EvaluationChain evaluations={evaluations} blockingRules={blockingRules} />
            </Section>
          )}

          {isCalibration && (
            <Section label="Calibration context">
              <div className="text-xs text-(--color-text-secondary) bg-(--color-accent-light) rounded-[10px] px-3 py-2 border border-(--color-accent)/15">
                Calibration profile updated. Future AI recommendations will weight this signal.
              </div>
            </Section>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-1 pt-2 border-t border-(--color-border)/60 text-[11px] text-(--color-text-tertiary)">
            <div>
              <span>Time: </span>
              <span className="text-(--color-text-secondary)">{absoluteTime(evt.created_at)}</span>
            </div>
            <div>
              <span>Target: </span>
              <span className="text-(--color-text-secondary) font-mono">{evt.target_id.slice(0, 12)}…</span>
            </div>
            {evt.user_id && (
              <div>
                <span>Actor: </span>
                <span className="text-(--color-text-secondary) font-mono">{evt.user_id.slice(0, 8)}…</span>
              </div>
            )}
            {source && (
              <div>
                <span>Source: </span>
                <span className="text-(--color-text-secondary) capitalize">{source}</span>
              </div>
            )}
          </div>
        </div>
      )}
    </Card>
  );
}

function Section({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <div className="text-[11px] font-medium uppercase tracking-[0.06em] text-(--color-text-tertiary) mb-1.5">
        {label}
      </div>
      {children}
    </div>
  );
}
