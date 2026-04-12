"use client";

import { useEffect, useState } from "react";
import { wellbeing, type WellbeingAnomalyItem, type WellbeingAnomalyDetail, type WellbeingSummary, type WellbeingConfigData } from "@/lib/api";
import { useToast } from "@/components/Toast";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import SectionHeader from "@/components/ui/SectionHeader";
import EmptyState from "@/components/ui/EmptyState";
import { cn } from "@/lib/cn";
import { relativeTime } from "@/lib/format";

// ── Anomaly type display ──

const TYPE_CONFIG: Record<string, { label: string; icon: string }> = {
  broad_disengagement: { label: "Engagement Change", icon: "\uD83D\uDCA1" },
  frustration_spike: { label: "Increased Difficulty", icon: "\uD83C\uDF0A" },
  performance_cliff: { label: "Performance Shift", icon: "\uD83D\uDCC9" },
  session_avoidance: { label: "Session Pattern Change", icon: "\uD83D\uDCC5" },
};

function severityLabel(s: number): string {
  if (s < 1.5) return "Mild change from typical patterns";
  if (s < 2.5) return "Moderate change from typical patterns";
  return "Notable change from typical patterns";
}

// ── Anomaly Card ──

function AnomalyCard({ anomaly, childId, onUpdate }: {
  anomaly: WellbeingAnomalyItem;
  childId: string;
  onUpdate: () => void;
}) {
  const { toast } = useToast();
  const [showNote, setShowNote] = useState(false);
  const [note, setNote] = useState("");
  const [confirming, setConfirming] = useState(false);
  const [detail, setDetail] = useState<WellbeingAnomalyDetail | null>(null);
  const [showEvidence, setShowEvidence] = useState(false);
  const cfg = TYPE_CONFIG[anomaly.anomaly_type] || { label: anomaly.anomaly_type, icon: "?" };

  async function handleStatus(status: string, response?: string) {
    try {
      await wellbeing.updateStatus(childId, anomaly.id, { status, parent_response: response });
      toast(status === "dismissed" ? "Noted. METHEAN will calibrate." : "Status updated.", "success");
      onUpdate();
    } catch (err: any) {
      toast(err?.detail || "Failed to update", "error");
    }
  }

  async function loadDetail() {
    if (detail) { setShowEvidence(!showEvidence); return; }
    try {
      const d = await wellbeing.anomalyDetail(childId, anomaly.id);
      setDetail(d);
      setShowEvidence(true);
    } catch { setShowEvidence(false); }
  }

  const isActive = !["dismissed", "resolved"].includes(anomaly.status);

  return (
    <Card>
      <div className="space-y-3">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-2">
            <span className="text-base">{cfg.icon}</span>
            <span className="text-xs font-medium text-(--color-text)">{cfg.label}</span>
          </div>
          <div className="flex items-center gap-1.5">
            {anomaly.status === "resolved" && <span className="text-[10px] text-(--color-success)">Resolved</span>}
            {anomaly.status === "dismissed" && <span className="text-[10px] text-(--color-text-tertiary)">Dismissed</span>}
            {anomaly.status === "acknowledged" && <span className="text-[10px] text-(--color-accent)">Acknowledged</span>}
            {anomaly.status === "notified" && <span className="w-2 h-2 rounded-full bg-(--color-warning)" />}
            <span className="text-[10px] text-(--color-text-tertiary)">{relativeTime(anomaly.created_at)}</span>
          </div>
        </div>

        {/* Parent message — the main content */}
        <p className="text-sm text-(--color-text) leading-relaxed">{anomaly.parent_message}</p>

        {/* Affected subjects */}
        <div className="flex flex-wrap gap-1.5">
          {anomaly.affected_subjects.map(s => (
            <span key={s} className="text-[10px] px-1.5 py-0.5 rounded-full bg-(--color-page) text-(--color-text-secondary) border border-(--color-border)">{s}</span>
          ))}
        </div>

        {/* Severity as natural language */}
        <div className="text-[10px] text-(--color-text-tertiary)">{severityLabel(anomaly.severity)}</div>

        {/* Actions */}
        {isActive && (
          <div className="flex items-center gap-2 pt-2 border-t border-(--color-border)">
            <button onClick={() => handleStatus("acknowledged")}
              className="px-3 py-1 text-xs text-(--color-text-secondary) border border-(--color-border) rounded-[10px] hover:bg-(--color-page) transition-colors">
              I've seen this
            </button>
            <button onClick={() => setShowNote(!showNote)}
              className="px-3 py-1 text-xs text-(--color-accent) border border-(--color-accent)/30 rounded-[10px] hover:bg-(--color-accent)/5 transition-colors">
              We're addressing it
            </button>
            {!confirming ? (
              <button onClick={() => setConfirming(true)}
                className="px-3 py-1 text-xs text-(--color-text-tertiary) hover:text-(--color-text-secondary) transition-colors">
                Not a concern
              </button>
            ) : (
              <div className="flex items-center gap-1.5 text-[10px]">
                <span className="text-(--color-text-secondary)">Dismissing helps METHEAN calibrate. Sure?</span>
                <button onClick={() => { handleStatus("dismissed"); setConfirming(false); }} className="font-medium text-(--color-accent)">Yes</button>
                <button onClick={() => setConfirming(false)} className="text-(--color-text-tertiary)">No</button>
              </div>
            )}
          </div>
        )}

        {/* Note input */}
        {showNote && (
          <div className="flex gap-2 items-center">
            <input value={note} onChange={(e) => setNote(e.target.value)} placeholder="What are you doing about it? (optional)"
              className="flex-1 px-3 py-1.5 text-xs border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text)" />
            <button onClick={() => { handleStatus("acknowledged", note); setShowNote(false); }}
              className="px-3 py-1.5 text-xs font-medium bg-(--color-accent) text-white rounded-[10px]">Save</button>
          </div>
        )}

        {/* Parent response */}
        {anomaly.parent_response && (
          <div className="text-[10px] text-(--color-text-secondary) bg-(--color-page) px-3 py-2 rounded-[10px]">Your note: {anomaly.parent_response}</div>
        )}

        {/* Evidence toggle */}
        <button onClick={loadDetail} className="text-[10px] text-(--color-accent) hover:underline">
          {showEvidence ? "Hide details" : "View details"}
        </button>

        {/* Evidence table */}
        {showEvidence && detail?.evidence_json && (
          <div className="overflow-x-auto">
            <table className="w-full text-[11px]">
              <thead>
                <tr className="border-b border-(--color-border)">
                  <th className="text-left py-1 pr-2 font-medium text-(--color-text-secondary)">Subject</th>
                  <th className="text-right py-1 px-2 font-medium text-(--color-text-secondary)">Usual</th>
                  <th className="text-right py-1 px-2 font-medium text-(--color-text-secondary)">Recent</th>
                  <th className="text-right py-1 pl-2 font-medium text-(--color-text-secondary)">Change</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(detail.evidence_json).map(([subj, data]: [string, any]) => {
                  if (typeof data !== "object" || !data) return null;
                  const baseline = data.baseline_mean ?? data.baseline_frequency ?? data.baseline_confidence ?? "--";
                  const recent = data.recent_mean ?? data.recent_frequency ?? data["7day_confidence"] ?? "--";
                  const dev = data.deviation_sd ?? data.deviation_7d_sd ?? data.ratio ?? "--";
                  return (
                    <tr key={subj} className="border-b border-(--color-border) last:border-0">
                      <td className="py-1 pr-2 text-(--color-text)">{subj}</td>
                      <td className="py-1 px-2 text-right text-(--color-text-secondary)">{typeof baseline === "number" ? baseline.toFixed(2) : baseline}</td>
                      <td className="py-1 px-2 text-right text-(--color-text-secondary)">{typeof recent === "number" ? recent.toFixed(2) : recent}</td>
                      <td className="py-1 pl-2 text-right font-medium" style={{ color: typeof dev === "number" && dev > 1.5 ? "var(--color-warning)" : "var(--color-text-secondary)" }}>
                        {typeof dev === "number" ? `${dev > 0 ? "-" : "+"}${Math.abs(dev).toFixed(1)} SD` : dev}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </Card>
  );
}

// ── Settings Section ──

function SettingsSection({ config, childId, onSave }: {
  config: WellbeingConfigData;
  childId: string;
  onSave: () => void;
}) {
  const { toast } = useToast();
  const [expanded, setExpanded] = useState(false);
  const [enabled, setEnabled] = useState(config.enabled);
  const [sensitivity, setSensitivity] = useState(config.sensitivity_level);

  async function save() {
    try {
      await wellbeing.updateConfig(childId, { enabled, sensitivity_level: sensitivity });
      toast("Settings saved", "success");
      onSave();
    } catch (err: any) {
      toast(err?.detail || "Failed to save", "error");
    }
  }

  const sensOptions = [
    { value: "conservative", label: "Conservative", desc: "Fewer alerts. Only flags significant changes." },
    { value: "balanced", label: "Balanced", desc: "Default. Flags moderate changes across multiple subjects." },
    { value: "sensitive", label: "Sensitive", desc: "More alerts. Flags smaller changes early." },
  ];

  return (
    <div>
      <button onClick={() => setExpanded(!expanded)} className="text-xs text-(--color-text-secondary) hover:text-(--color-text) transition-colors">
        {expanded ? "Hide settings" : "Settings"}
      </button>
      {expanded && (
        <Card>
          <div className="space-y-4">
            {/* Enable toggle */}
            <div className="flex items-center justify-between">
              <div>
                <div className="text-sm font-medium text-(--color-text)">Wellbeing Detection</div>
                <div className="text-xs text-(--color-text-secondary)">Monitor engagement and performance patterns</div>
              </div>
              <button onClick={() => setEnabled(!enabled)}
                className="relative w-11 h-6 rounded-full transition-colors"
                style={{ background: enabled ? "var(--color-success)" : "var(--color-border)" }}>
                <span className="absolute left-0.5 top-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform"
                  style={{ transform: enabled ? "translateX(20px)" : "translateX(0)" }} />
              </button>
            </div>

            {/* Sensitivity */}
            {enabled && (
              <div className="space-y-2 pt-2 border-t border-(--color-border)">
                <div className="text-xs font-medium text-(--color-text)">Sensitivity</div>
                {sensOptions.map(opt => (
                  <button key={opt.value} onClick={() => setSensitivity(opt.value)}
                    className={cn("w-full text-left p-3 rounded-[10px] border transition-colors",
                      sensitivity === opt.value ? "border-(--color-accent) bg-(--color-accent)/5" : "border-(--color-border) hover:bg-(--color-page)")}>
                    <div className="text-xs font-medium text-(--color-text)">{opt.label}</div>
                    <div className="text-[10px] text-(--color-text-secondary) mt-0.5">{opt.desc}</div>
                  </button>
                ))}
              </div>
            )}

            {/* Threshold adjustments display */}
            {Object.keys(config.threshold_adjustments).length > 0 && (
              <div className="pt-2 border-t border-(--color-border)">
                <div className="text-[10px] text-(--color-text-tertiary)">
                  METHEAN has self-adjusted based on your feedback:
                  {Object.entries(config.threshold_adjustments).map(([type, adj]) => (
                    <span key={type} className="ml-1">{TYPE_CONFIG[type]?.label || type} +{adj.toFixed(1)} SD</span>
                  ))}
                </div>
              </div>
            )}

            <button onClick={save}
              className="px-4 py-1.5 text-xs font-medium bg-(--color-accent) text-white rounded-[10px]">
              Save Settings
            </button>
          </div>
        </Card>
      )}
    </div>
  );
}

// ── Main Page ──

export default function WellbeingPage() {
  useEffect(() => { document.title = "Wellbeing | METHEAN"; }, []);

  const { selectedChild } = useChild();
  const { toast } = useToast();
  const [anomalies, setAnomalies] = useState<WellbeingAnomalyItem[]>([]);
  const [summary, setSummary] = useState<WellbeingSummary | null>(null);
  const [config, setConfig] = useState<WellbeingConfigData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { if (selectedChild) load(); }, [selectedChild]);

  async function load() {
    if (!selectedChild) return;
    setLoading(true);
    try {
      const [aRes, sRes, cRes] = await Promise.all([
        wellbeing.anomalies(selectedChild.id),
        wellbeing.summary(selectedChild.id),
        wellbeing.config(selectedChild.id),
      ]);
      setAnomalies(aRes.items);
      setSummary(sRes);
      setConfig(cRes);
    } catch { /* graceful */ }
    finally { setLoading(false); }
  }

  if (!selectedChild) return <EmptyState title="Select a child" description="Choose a child from the sidebar." icon="empty" />;
  if (loading) return <LoadingSkeleton />;

  const active = anomalies.filter(a => !["dismissed", "resolved"].includes(a.status));
  const resolved = anomalies.filter(a => a.status === "resolved");
  const isDisabled = config && !config.enabled;

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <PageHeader title="Wellbeing" subtitle={`Engagement and performance patterns for ${selectedChild.first_name}`} />

      {/* Status Banner */}
      {isDisabled && (
        <div className="bg-(--color-page) border border-(--color-border) rounded-[14px] px-4 py-3 text-xs text-(--color-text-secondary)">
          Wellbeing detection is turned off for {selectedChild.first_name}. Enable it in settings below.
        </div>
      )}
      {!isDisabled && active.length === 0 && (
        <div className="bg-(--color-success-light) border border-(--color-success)/10 rounded-[14px] px-4 py-3 text-xs text-(--color-success)">
          No concerns detected. METHEAN monitors engagement, effort, and performance patterns across subjects nightly.
        </div>
      )}
      {!isDisabled && active.length > 0 && (
        <div className="bg-(--color-warning-light) border border-(--color-warning)/10 rounded-[14px] px-4 py-3 text-xs text-(--color-warning)">
          {active.length} observation{active.length > 1 ? "s" : ""} for your review
        </div>
      )}

      {/* Active Anomalies */}
      {active.length > 0 && (
        <div className="space-y-3">
          {active.map(a => (
            <AnomalyCard key={a.id} anomaly={a} childId={selectedChild.id} onUpdate={load} />
          ))}
        </div>
      )}

      {/* Empty state */}
      {anomalies.length === 0 && !isDisabled && (
        <EmptyState
          title="No wellbeing observations yet"
          description={`METHEAN analyzes patterns across subjects nightly. If broad changes appear in ${selectedChild.first_name}'s engagement or performance, you'll see them here.`}
          icon="search"
        />
      )}

      {/* Resolved */}
      {resolved.length > 0 && (
        <details className="group">
          <summary className="text-xs text-(--color-text-secondary) cursor-pointer hover:text-(--color-text) transition-colors">
            {resolved.length} resolved observation{resolved.length > 1 ? "s" : ""}
          </summary>
          <div className="mt-3 space-y-2">
            {resolved.map(a => (
              <div key={a.id} className="flex items-start gap-2 p-3 bg-(--color-page) rounded-[10px]">
                <span className="text-(--color-success) mt-0.5">&#10003;</span>
                <div className="flex-1">
                  <div className="text-xs text-(--color-text)">{TYPE_CONFIG[a.anomaly_type]?.label || a.anomaly_type}</div>
                  <div className="text-[10px] text-(--color-text-tertiary)">Resolved {relativeTime(a.created_at)}</div>
                </div>
              </div>
            ))}
          </div>
        </details>
      )}

      {/* Settings */}
      {config && <SettingsSection config={config} childId={selectedChild.id} onSave={load} />}
    </div>
  );
}
