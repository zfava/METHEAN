"use client";

import { useEffect, useState } from "react";
import { familyInsights, type FamilyInsightItem, type FamilyInsightSummary, type FamilyInsightConfigData } from "@/lib/api";
import { useToast } from "@/components/Toast";
import { useMobile } from "@/lib/useMobile";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import SectionHeader from "@/components/ui/SectionHeader";
import EmptyState from "@/components/ui/EmptyState";
import { cn } from "@/lib/cn";
import { relativeTime } from "@/lib/format";

// ── Pattern type display config ──

const PATTERN_CONFIG: Record<string, { label: string; color: string; icon: string }> = {
  shared_struggle: { label: "Shared Struggle", color: "var(--color-warning)", icon: "\uD83D\uDC65" },
  curriculum_gap: { label: "Curriculum Gap", color: "var(--color-danger)", icon: "\uD83D\uDCC4" },
  pacing_divergence: { label: "Pacing Divergence", color: "var(--color-accent)", icon: "\u2194\uFE0F" },
  environmental_correlation: { label: "Environmental", color: "#8B5CF6", icon: "\uD83D\uDCC5" },
  material_effectiveness: { label: "Material Effectiveness", color: "#0D9488", icon: "\uD83D\uDCD6" },
};

function patternLabel(type: string): string {
  return PATTERN_CONFIG[type]?.label || type.replace(/_/g, " ");
}

function patternColor(type: string): string {
  return PATTERN_CONFIG[type]?.color || "var(--color-text-tertiary)";
}

// ── Insight Card ──

function InsightCard({ insight, onStatusChange }: {
  insight: FamilyInsightItem;
  onStatusChange: (id: string, status: string, response?: string) => void;
}) {
  const [showAction, setShowAction] = useState(false);
  const [actionNote, setActionNote] = useState("");
  const [confirming, setConfirming] = useState(false);
  const cfg = PATTERN_CONFIG[insight.pattern_type] || { label: insight.pattern_type, color: "var(--color-text-tertiary)", icon: "?" };

  return (
    <Card>
      <div className="space-y-3">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-2">
            <span className="text-base">{cfg.icon}</span>
            <span className="text-xs font-medium px-2 py-0.5 rounded-full border" style={{ color: cfg.color, borderColor: cfg.color }}>
              {cfg.label}
            </span>
            {insight.is_predictive && (
              <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-(--color-accent)/10 text-(--color-accent) font-medium">
                Predictive {insight.predictive_child ? `for ${insight.predictive_child.name}` : ""}
              </span>
            )}
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full" style={{
              background: insight.status === "detected" ? "var(--color-warning)" :
                insight.status === "acknowledged" ? "var(--color-accent)" :
                  insight.status === "acted_on" ? "var(--color-success)" : "var(--color-text-tertiary)",
            }} />
            <span className="text-[10px] text-(--color-text-tertiary) capitalize">{insight.status.replace(/_/g, " ")}</span>
          </div>
        </div>

        {/* Affected children + subjects */}
        <div className="flex flex-wrap gap-1.5">
          {insight.affected_children.map(c => (
            <span key={c.id} className="text-[10px] px-1.5 py-0.5 rounded-full bg-(--color-page) text-(--color-text-secondary) border border-(--color-border)">
              {c.name}
            </span>
          ))}
          {insight.affected_subjects.map(s => (
            <span key={s} className="text-[10px] px-1.5 py-0.5 rounded-full bg-(--color-accent)/5 text-(--color-accent)">
              {s}
            </span>
          ))}
        </div>

        {/* Recommendation */}
        <p className="text-sm text-(--color-text) leading-relaxed">{insight.recommendation}</p>

        {/* Confidence + nodes */}
        <div className="flex items-center justify-between text-[10px] text-(--color-text-tertiary)">
          <span>Confidence: {(insight.confidence * 100).toFixed(0)}%</span>
          {insight.affected_nodes.length > 0 && (
            <span>{insight.affected_nodes.map(n => n.title).join(", ")}</span>
          )}
          <span>{relativeTime(insight.created_at)}</span>
        </div>

        {/* Actions */}
        {insight.status !== "acted_on" && insight.status !== "dismissed" && (
          <div className="flex items-center gap-2 pt-2 border-t border-(--color-border)">
            {insight.status === "detected" && (
              <button onClick={() => onStatusChange(insight.id, "acknowledged")}
                className="px-3 py-1 text-xs font-medium text-(--color-accent) border border-(--color-accent)/30 rounded-[10px] hover:bg-(--color-accent)/5 transition-colors">
                Acknowledge
              </button>
            )}
            <button onClick={() => setShowAction(!showAction)}
              className="px-3 py-1 text-xs font-medium text-(--color-success) border border-(--color-success)/30 rounded-[10px] hover:bg-(--color-success)/5 transition-colors">
              Take Action
            </button>
            {!confirming ? (
              <button onClick={() => setConfirming(true)}
                className="px-3 py-1 text-xs text-(--color-text-tertiary) hover:text-(--color-danger) transition-colors">
                Dismiss
              </button>
            ) : (
              <div className="flex items-center gap-1.5">
                <span className="text-[10px] text-(--color-text-secondary)">Dismissing helps METHEAN learn. Sure?</span>
                <button onClick={() => { onStatusChange(insight.id, "dismissed"); setConfirming(false); }}
                  className="text-[10px] font-medium text-(--color-danger)">Yes</button>
                <button onClick={() => setConfirming(false)}
                  className="text-[10px] text-(--color-text-tertiary)">No</button>
              </div>
            )}
          </div>
        )}

        {/* Action note input */}
        {showAction && (
          <div className="flex flex-col sm:flex-row gap-2 items-stretch sm:items-center">
            <input value={actionNote} onChange={(e) => setActionNote(e.target.value)}
              placeholder="What action did you take? (optional)"
              className="flex-1 w-full px-3 py-1.5 text-xs border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)" />
            <button onClick={() => { onStatusChange(insight.id, "acted_on", actionNote); setShowAction(false); }}
              className="px-3 py-1.5 text-xs font-medium bg-(--color-success) text-white rounded-[10px]">
              Save
            </button>
          </div>
        )}

        {/* Parent response if exists */}
        {insight.parent_response && (
          <div className="text-[10px] text-(--color-text-secondary) bg-(--color-page) px-3 py-2 rounded-[10px]">
            Your note: {insight.parent_response}
          </div>
        )}
      </div>
    </Card>
  );
}

// ── Config Section ──

function ConfigSection({ config, onSave }: {
  config: FamilyInsightConfigData;
  onSave: (data: { enabled?: boolean; pattern_settings?: Record<string, object> }) => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const [settings, setSettings] = useState(config.pattern_settings);
  const [enabled, setEnabled] = useState(config.enabled);

  function togglePattern(key: string) {
    const cur = { ...settings };
    cur[key] = { ...cur[key], enabled: !cur[key]?.enabled };
    setSettings(cur);
  }

  return (
    <div>
      <button onClick={() => setExpanded(!expanded)} className="text-xs text-(--color-text-secondary) hover:text-(--color-text) transition-colors">
        {expanded ? "Hide" : "Show"} Configuration
      </button>
      {expanded && (
        <Card>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm font-medium text-(--color-text)">Family Intelligence</div>
                <div className="text-xs text-(--color-text-secondary)">Enable cross-child pattern detection</div>
              </div>
              <button onClick={() => setEnabled(!enabled)}
                className="relative w-11 h-6 rounded-full transition-colors"
                style={{ background: enabled ? "var(--color-success)" : "var(--color-border)" }}>
                <span className="absolute left-0.5 top-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform"
                  style={{ transform: enabled ? "translateX(20px)" : "translateX(0)" }} />
              </button>
            </div>

            {enabled && (
              <div className="space-y-2 pt-2 border-t border-(--color-border)">
                {Object.entries(settings).map(([key, val]) => (
                  <div key={key} className="flex items-center justify-between py-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs" style={{ color: patternColor(key) }}>{PATTERN_CONFIG[key]?.icon}</span>
                      <span className="text-xs text-(--color-text)">{patternLabel(key)}</span>
                    </div>
                    <button onClick={() => togglePattern(key)}
                      className={cn("text-[10px] px-2 py-0.5 rounded-full border transition-colors",
                        val?.enabled ? "border-(--color-success)/30 text-(--color-success)" : "border-(--color-border) text-(--color-text-tertiary)"
                      )}>
                      {val?.enabled ? "On" : "Off"}
                    </button>
                  </div>
                ))}
              </div>
            )}

            <button onClick={() => onSave({ enabled, pattern_settings: settings })}
              className="px-4 py-1.5 text-xs font-medium bg-(--color-accent) text-white rounded-[10px]">
              Save Configuration
            </button>
          </div>
        </Card>
      )}
    </div>
  );
}

// ── Main Page ──

export default function FamilyInsightsPage() {
  useEffect(() => { document.title = "Family Insights | METHEAN"; }, []);

  const { children } = useChild();
  const { toast } = useToast();
  const isMobile = useMobile();
  const [insights, setInsights] = useState<FamilyInsightItem[]>([]);
  const [summary, setSummary] = useState<FamilyInsightSummary | null>(null);
  const [config, setConfig] = useState<FamilyInsightConfigData | null>(null);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState("");
  const [filterPattern, setFilterPattern] = useState("");

  useEffect(() => { load(); }, [filterStatus, filterPattern]);

  async function load() {
    setLoading(true);
    try {
      const params: Record<string, string> = {};
      if (filterStatus) params.status = filterStatus;
      if (filterPattern) params.pattern_type = filterPattern;

      const [insightsRes, summaryRes, configRes] = await Promise.all([
        familyInsights.list(params),
        familyInsights.summary(),
        familyInsights.config(),
      ]);
      setInsights(insightsRes.items);
      setTotal(insightsRes.total);
      setSummary(summaryRes);
      setConfig(configRes);
    } catch {
      // Graceful degradation
    } finally {
      setLoading(false);
    }
  }

  async function handleStatusChange(id: string, status: string, response?: string) {
    try {
      await familyInsights.updateStatus(id, { status, parent_response: response });
      toast(`Insight ${status.replace(/_/g, " ")}`, "success");
      await load();
    } catch (err: any) {
      toast(err?.detail || "Failed to update", "error");
    }
  }

  async function handleConfigSave(data: { enabled?: boolean; pattern_settings?: Record<string, object> }) {
    try {
      await familyInsights.updateConfig(data);
      toast("Configuration saved", "success");
      await load();
    } catch (err: any) {
      toast(err?.detail || "Failed to save", "error");
    }
  }

  if (loading) return <LoadingSkeleton />;

  // Single-child household
  if (children.length < 2) {
    return (
      <div className="max-w-4xl mx-auto space-y-6">
        <PageHeader title="Family Insights" subtitle="Cross-child pattern detection" />
        <EmptyState
          title="Family Intelligence requires multiple children"
          description="Add another child to your household to enable cross-child pattern detection. METHEAN identifies shared struggles, curriculum gaps, and pacing divergence across siblings."
          icon="empty"
        />
      </div>
    );
  }

  const activeCount = summary?.total_active || 0;
  const statusBadgeColor = activeCount === 0 ? "var(--color-success)" : activeCount <= 3 ? "var(--color-warning)" : "var(--color-danger)";

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <PageHeader title="Family Insights" subtitle="Cross-child pattern detection across your household" />

      {/* Summary Bar */}
      <Card>
        <div className="flex flex-wrap items-center gap-4">
          <div>
            <div className="text-xs text-(--color-text-secondary) mb-1">Active Insights</div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border" style={{ borderColor: statusBadgeColor, color: statusBadgeColor }}>
              <span className="w-2 h-2 rounded-full" style={{ background: statusBadgeColor }} />
              {activeCount}
            </div>
          </div>
          {summary && Object.entries(summary.by_pattern_type).map(([type, count]) => (
            <div key={type} className="text-center">
              <div className="text-[10px] text-(--color-text-tertiary) mb-0.5">{patternLabel(type)}</div>
              <span className="text-xs font-medium" style={{ color: patternColor(type) }}>{count}</span>
            </div>
          ))}
          {summary && summary.predictive_count > 0 && (
            <div className="text-center">
              <div className="text-[10px] text-(--color-text-tertiary) mb-0.5">Predictive</div>
              <span className="text-xs font-medium text-(--color-accent)">{summary.predictive_count}</span>
            </div>
          )}
        </div>
      </Card>

      {/* Filters */}
      <div className="flex flex-wrap gap-2">
        <button onClick={() => { setFilterStatus(""); setFilterPattern(""); }}
          className={cn("px-3 py-1 text-xs rounded-full transition-colors",
            !filterStatus && !filterPattern ? "bg-(--color-text) text-white" : "bg-(--color-page) text-(--color-text-secondary)")}>
          All ({total})
        </button>
        {["detected", "acknowledged", "acted_on", "dismissed"].map(s => (
          <button key={s} onClick={() => { setFilterStatus(s); setFilterPattern(""); }}
            className={cn("px-3 py-1 text-xs rounded-full capitalize transition-colors",
              filterStatus === s ? "bg-(--color-text) text-white" : "bg-(--color-page) text-(--color-text-secondary)")}>
            {s.replace(/_/g, " ")}
          </button>
        ))}
        {Object.keys(PATTERN_CONFIG).map(p => (
          <button key={p} onClick={() => { setFilterPattern(p); setFilterStatus(""); }}
            className={cn("px-3 py-1 text-xs rounded-full transition-colors",
              filterPattern === p ? "text-white" : "text-(--color-text-secondary)")}
            style={{ background: filterPattern === p ? patternColor(p) : undefined }}>
            {patternLabel(p)}
          </button>
        ))}
      </div>

      {/* Insight Cards */}
      {insights.length === 0 ? (
        <EmptyState
          title="No family patterns detected"
          description="METHEAN analyzes cross-child patterns nightly. As your children progress, insights will appear here."
          icon="search"
        />
      ) : (
        <div className="space-y-3">
          {insights.map(insight => (
            <InsightCard key={insight.id} insight={insight} onStatusChange={handleStatusChange} />
          ))}
        </div>
      )}

      {/* Configuration */}
      {config && <ConfigSection config={config} onSave={handleConfigSave} />}
    </div>
  );
}
