"use client";

import { useEffect, useState, useMemo, useRef } from "react";
import {
  calibration,
  type CalibrationProfileData,
  type PredictionItem,
  type DriftPoint,
  type TemporalDriftResponse,
  type ConfidenceDistributionResponse,
  type SubjectCalibrationItem,
} from "@/lib/api";
import { useToast } from "@/components/Toast";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import SectionHeader from "@/components/ui/SectionHeader";
import EmptyState from "@/components/ui/EmptyState";
import { relativeTime } from "@/lib/format";

// ── Shared helpers ──

function ratingLabel(r: number): string {
  switch (r) {
    case 1: return "Again";
    case 2: return "Hard";
    case 3: return "Good";
    case 4: return "Easy";
    default: return String(r);
  }
}

function driftColor(drift: number | null): string {
  if (drift === null) return "var(--color-text-tertiary)";
  if (drift === 0) return "var(--color-success)";
  if (drift < 0.5) return "var(--color-success)";
  if (drift < 1.5) return "var(--color-warning)";
  return "var(--color-danger)";
}

function actionColor(action: string): string {
  switch (action) {
    case "well_calibrated": return "var(--color-success)";
    case "offset_active": return "var(--color-warning)";
    case "review_recommended": return "var(--color-danger)";
    default: return "var(--color-text-tertiary)";
  }
}

// ── Health badge ──

function HealthBadge({ profile, reconciledCount, threshold }: {
  profile: CalibrationProfileData | null;
  reconciledCount: number;
  threshold: number;
}) {
  if (!profile || reconciledCount < threshold) {
    const needed = threshold - reconciledCount;
    return (
      <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-(--color-page) text-(--color-text-tertiary) border border-(--color-border)">
        <span className="w-2 h-2 rounded-full bg-(--color-text-tertiary)" />
        {needed} more reviews needed
      </div>
    );
  }
  const drift = profile.mean_drift;
  const color = drift < 0.5 ? "var(--color-success)" : drift < 1.0 ? "var(--color-warning)" : "var(--color-danger)";
  const label = drift < 0.5 ? "Well Calibrated" : drift < 1.0 ? "Moderate Drift" : "High Drift";
  return (
    <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border" style={{ borderColor: color, color }}>
      <span className="w-2 h-2 rounded-full" style={{ background: color }} />
      {label} ({drift.toFixed(2)})
    </div>
  );
}

// ── SVG line chart (shared for drift history + temporal drift) ──

function LineChart({ data, height = 180, yKey = "mean_drift", hoverExtra }: {
  data: Array<{ week: string; mean_drift: number; count: number; [k: string]: any }>;
  height?: number;
  yKey?: string;
  hoverExtra?: (d: any) => React.ReactNode;
}) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [containerW, setContainerW] = useState(600);
  const [hoverIdx, setHoverIdx] = useState<number | null>(null);

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const ro = new ResizeObserver((entries) => {
      const w = entries[0]?.contentRect.width;
      if (w && w > 0) setContainerW(Math.max(w, 320));
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const pL = 36, pR = 16, pT = 16, pB = 32;
  const plotW = containerW - pL - pR;
  const plotH = height - pT - pB;

  const { points, maxY, gridLines } = useMemo(() => {
    if (data.length < 2) return { points: [], maxY: 0, gridLines: [] };
    const rawMax = Math.max(...data.map(d => (d as any)[yKey] as number), 1);
    const maxY = Math.ceil(rawMax * 1.2 * 10) / 10;
    const xStep = plotW / Math.max(data.length - 1, 1);
    const points = data.map((d, i) => ({
      x: pL + i * xStep,
      y: pT + plotH - (((d as any)[yKey] as number) / maxY) * plotH,
    }));
    const gridLines = [0.5, 1.0, 1.5, 2.0].filter(v => v <= maxY).map(val => ({
      y: pT + plotH - (val / maxY) * plotH,
      label: val.toFixed(1),
    }));
    return { points, maxY, gridLines };
  }, [data, plotW, plotH, yKey]);

  if (data.length < 2) {
    return <div className="py-8 text-center text-xs text-(--color-text-tertiary)">Need 2+ weeks of data to show chart.</div>;
  }

  const xStep = plotW / Math.max(data.length - 1, 1);
  const y05 = maxY > 0 ? pT + plotH - (0.5 / maxY) * plotH : pT + plotH;

  return (
    <div ref={containerRef} className="relative w-full">
      <svg viewBox={`0 0 ${containerW} ${height}`} className="w-full">
        {/* Green zone below 0.5 */}
        {maxY >= 0.5 && <rect x={pL} y={y05} width={plotW} height={pT + plotH - y05} fill="var(--color-success)" opacity={0.04} />}
        {/* Reference line at 0.5 */}
        {maxY >= 0.5 && (
          <line x1={pL} y1={y05} x2={containerW - pR} y2={y05} stroke="var(--color-success)" strokeWidth={1} strokeDasharray="4 4" opacity={0.4} />
        )}

        {gridLines.map(gl => (
          <g key={gl.label}>
            <line x1={pL} y1={gl.y} x2={containerW - pR} y2={gl.y} stroke="var(--color-border)" strokeWidth={1} strokeDasharray="3 3" />
            <text x={pL - 6} y={gl.y + 3} textAnchor="end" fill="var(--color-text-tertiary)" fontSize={10}>{gl.label}</text>
          </g>
        ))}

        <line x1={pL} y1={pT + plotH} x2={containerW - pR} y2={pT + plotH} stroke="var(--color-border)" strokeWidth={1} />

        {data.map((d, i) => {
          const show = data.length < 10 || i % 2 === 0 || i === data.length - 1;
          if (!show) return null;
          const dt = new Date(d.week);
          const label = dt.toLocaleDateString("en-US", { month: "short", day: "numeric" });
          return <text key={i} x={pL + i * xStep} y={height - 6} textAnchor="middle" fill="var(--color-text-tertiary)" fontSize={10}>{label}</text>;
        })}

        {points.length > 1 && (
          <polyline points={points.map(p => `${p.x},${p.y}`).join(" ")} fill="none" stroke="var(--color-accent)" strokeWidth={2} strokeLinejoin="round" />
        )}

        {points.map((pt, i) => {
          const val = (data[i] as any)[yKey] as number;
          return (
            <circle key={i} cx={pt.x} cy={pt.y} r={hoverIdx === i ? 5 : 3}
              fill={val < 0.5 ? "var(--color-success)" : val < 1.0 ? "var(--color-warning)" : "var(--color-danger)"}
              stroke="var(--color-surface)" strokeWidth={1.5}
              style={{ transition: "r 0.15s" }} />
          );
        })}

        {data.map((_, i) => (
          <rect key={i} x={pL + i * xStep - xStep / 2} y={pT} width={xStep} height={plotH}
            fill="transparent" onMouseEnter={() => setHoverIdx(i)} onMouseLeave={() => setHoverIdx(null)} />
        ))}

        {hoverIdx !== null && (
          <line x1={pL + hoverIdx * xStep} y1={pT} x2={pL + hoverIdx * xStep} y2={pT + plotH}
            stroke="var(--color-text-tertiary)" strokeWidth={1} strokeDasharray="2 2" opacity={0.5} />
        )}
      </svg>

      {hoverIdx !== null && data[hoverIdx] && (
        <div className="absolute bg-(--color-surface) border border-(--color-border) rounded-[10px] shadow-lg px-3 py-2 text-xs pointer-events-none z-10"
          style={{ left: `${((pL + hoverIdx * xStep) / containerW) * 100}%`, top: 8, transform: "translateX(-50%)" }}>
          <div className="font-medium text-(--color-text) mb-0.5">
            Week of {new Date(data[hoverIdx].week).toLocaleDateString("en-US", { month: "short", day: "numeric" })}
          </div>
          <div>Mean drift: <span className="font-medium">{data[hoverIdx].mean_drift.toFixed(2)}</span></div>
          <div className="text-(--color-text-tertiary)">{data[hoverIdx].count} predictions</div>
          {hoverExtra && hoverExtra(data[hoverIdx])}
        </div>
      )}
    </div>
  );
}

// ── Trend indicator ──

function TrendArrow({ trend, slope }: { trend: string; slope: number }) {
  const config: Record<string, { arrow: string; color: string; label: string }> = {
    improving: { arrow: "\u2193", color: "var(--color-success)", label: "Improving" },
    stable: { arrow: "\u2192", color: "var(--color-accent)", label: "Stable" },
    worsening: { arrow: "\u2191", color: "var(--color-danger)", label: "Worsening" },
    insufficient_data: { arrow: "\u2014", color: "var(--color-text-tertiary)", label: "Insufficient Data" },
  };
  const c = config[trend] || config.insufficient_data;
  return (
    <div className="inline-flex items-center gap-1.5 text-xs font-medium" style={{ color: c.color }}>
      <span className="text-base">{c.arrow}</span>
      {c.label}
      {trend !== "insufficient_data" && <span className="text-(--color-text-tertiary) font-normal">({slope > 0 ? "+" : ""}{slope.toFixed(4)}/wk)</span>}
    </div>
  );
}

// ── Confidence Distribution Histogram ──

function ConfidenceHistogram({ data }: { data: ConfidenceDistributionResponse }) {
  if (data.histogram.length === 0) {
    return <div className="py-8 text-center text-xs text-(--color-text-tertiary)">No confidence data yet.</div>;
  }
  const maxCount = Math.max(...data.histogram.map(b => b.count), 1);
  // FSRS band boundaries at 0.3, 0.55, 0.8
  const bandBoundaries = [3, 5.5, 8]; // index positions (out of 10 bands)

  return (
    <div className="space-y-3">
      {data.compression_warning && (
        <div className="bg-(--color-warning-light) border border-(--color-warning)/20 rounded-[10px] px-3 py-2 text-xs text-(--color-warning)">
          Low variance detected (std_dev: {data.std_dev.toFixed(3)}). The evaluator may not be discriminating between quality levels effectively.
        </div>
      )}
      <div className="flex items-end gap-1 h-28">
        {data.histogram.map((band, i) => {
          const pct = (band.count / maxCount) * 100;
          const isBoundary = bandBoundaries.some(b => Math.abs(i - b) < 0.6);
          return (
            <div key={band.band} className="flex-1 flex flex-col items-center gap-0.5">
              <div className="text-[9px] text-(--color-text-tertiary)">{band.count > 0 ? band.count : ""}</div>
              <div className="w-full rounded-t-sm" style={{
                height: `${Math.max(pct, 2)}%`,
                background: isBoundary ? "var(--color-accent)" : "var(--color-accent)",
                opacity: isBoundary ? 0.9 : 0.5,
              }} />
              <div className="text-[9px] text-(--color-text-tertiary)">{(i / 10).toFixed(1)}</div>
            </div>
          );
        })}
      </div>
      <div className="flex justify-between text-[10px] text-(--color-text-tertiary)">
        <span>Mean: {data.mean.toFixed(2)}</span>
        <span>Std Dev: {data.std_dev.toFixed(3)}</span>
        <span>Skew: {data.skew.toFixed(2)}</span>
        <span>n={data.total}</span>
      </div>
      {/* FSRS boundary labels */}
      <div className="flex text-[9px] text-(--color-text-tertiary) px-1">
        <div style={{ width: "30%" }} className="text-center border-r border-(--color-border)">Again</div>
        <div style={{ width: "25%" }} className="text-center border-r border-(--color-border)">Hard</div>
        <div style={{ width: "25%" }} className="text-center border-r border-(--color-border)">Good</div>
        <div style={{ width: "20%" }} className="text-center">Easy</div>
      </div>
    </div>
  );
}

// ── Subject Calibration Cards ──

function SubjectCards({ subjects }: { subjects: SubjectCalibrationItem[] }) {
  const filtered = subjects.filter(s => s.reconciled_count >= 10);
  if (filtered.length === 0) {
    return <div className="py-6 text-center text-xs text-(--color-text-tertiary)">No topics with 10+ predictions yet.</div>;
  }
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
      {filtered.map(s => (
        <div key={s.subject}
          className="p-3 rounded-[10px] border bg-(--color-surface)"
          style={{ borderColor: s.action === "review_recommended" ? "var(--color-danger)" : "var(--color-border)" }}
        >
          <div className="flex items-start justify-between mb-2">
            <div className="text-xs font-medium text-(--color-text) truncate max-w-[70%]">{s.subject}</div>
            <span className="text-[10px] font-medium px-1.5 py-0.5 rounded-full border shrink-0"
              style={{ color: actionColor(s.action), borderColor: actionColor(s.action) }}>
              {s.action === "well_calibrated" ? "Good" : s.action === "offset_active" ? "Offset" : s.action === "review_recommended" ? "Review" : "N/A"}
            </span>
          </div>
          {/* Drift gauge */}
          <div className="mb-2">
            <div className="flex justify-between text-[10px] text-(--color-text-tertiary) mb-0.5">
              <span>Drift: {s.mean_drift.toFixed(2)}</span>
              <span>Bias: {s.directional_bias > 0 ? "+" : ""}{s.directional_bias.toFixed(2)}</span>
            </div>
            <div className="h-1.5 rounded-full bg-(--color-page) overflow-hidden">
              <div className="h-full rounded-full transition-all"
                style={{
                  width: `${Math.min(s.mean_drift / 3 * 100, 100)}%`,
                  background: driftColor(s.mean_drift),
                }} />
            </div>
          </div>
          <div className="text-[10px] text-(--color-text-secondary) leading-snug">{s.recommendation}</div>
          <div className="text-[10px] text-(--color-text-tertiary) mt-1">{s.reconciled_count} predictions</div>
        </div>
      ))}
    </div>
  );
}

// ── Prediction Explorer ──

type SortKey = "date" | "drift" | "confidence";

function PredictionExplorer({ predictions: allPredictions, childId }: {
  predictions: PredictionItem[];
  childId: string;
}) {
  const [reconciledOnly, setReconciledOnly] = useState(false);
  const [minDrift, setMinDrift] = useState(0);
  const [sortBy, setSortBy] = useState<SortKey>("date");
  const [page, setPage] = useState(0);
  const pageSize = 15;

  const filtered = useMemo(() => {
    let items = [...allPredictions];
    if (reconciledOnly) items = items.filter(p => p.actual_outcome !== null);
    if (minDrift > 0) items = items.filter(p => p.drift_score !== null && p.drift_score >= minDrift);
    items.sort((a, b) => {
      if (sortBy === "drift") return ((b.drift_score ?? -1) - (a.drift_score ?? -1));
      if (sortBy === "confidence") return b.predicted_confidence - a.predicted_confidence;
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    });
    return items;
  }, [allPredictions, reconciledOnly, minDrift, sortBy]);

  const pageItems = filtered.slice(page * pageSize, (page + 1) * pageSize);
  const totalPages = Math.ceil(filtered.length / pageSize);

  if (allPredictions.length === 0) {
    return <EmptyState title="No predictions yet" description="Predictions appear as your child completes activities." icon="empty" />;
  }

  return (
    <div className="space-y-3">
      {/* Filters */}
      <div className="flex flex-wrap items-center gap-3 text-xs">
        <label className="flex items-center gap-1.5 cursor-pointer">
          <input type="checkbox" checked={reconciledOnly} onChange={(e) => { setReconciledOnly(e.target.checked); setPage(0); }}
            className="rounded border-(--color-border)" />
          <span className="text-(--color-text-secondary)">Reconciled only</span>
        </label>
        <div className="flex items-center gap-1.5">
          <span className="text-(--color-text-secondary)">Min drift:</span>
          <input type="range" min={0} max={3} step={0.5} value={minDrift}
            onChange={(e) => { setMinDrift(parseFloat(e.target.value)); setPage(0); }}
            className="w-20 accent-(--color-accent)" />
          <span className="text-(--color-text-tertiary) w-6">{minDrift > 0 ? minDrift.toFixed(1) : "Any"}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="text-(--color-text-secondary)">Sort:</span>
          {(["date", "drift", "confidence"] as SortKey[]).map(k => (
            <button key={k} onClick={() => { setSortBy(k); setPage(0); }}
              className="px-2 py-0.5 rounded-md transition-colors"
              style={{
                background: sortBy === k ? "var(--color-accent)" : "transparent",
                color: sortBy === k ? "white" : "var(--color-text-secondary)",
              }}>
              {k.charAt(0).toUpperCase() + k.slice(1)}
            </button>
          ))}
        </div>
        <span className="text-(--color-text-tertiary) ml-auto">{filtered.length} results</span>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-(--color-border)">
              <th className="text-left py-2 pr-2 font-medium text-(--color-text-secondary)">Predicted</th>
              <th className="text-left py-2 px-2 font-medium text-(--color-text-secondary)">Actual</th>
              <th className="text-right py-2 px-2 font-medium text-(--color-text-secondary)">Conf.</th>
              <th className="text-right py-2 px-2 font-medium text-(--color-text-secondary)">Drift</th>
              <th className="text-right py-2 px-2 font-medium text-(--color-text-secondary)">Offset</th>
              <th className="text-right py-2 pl-2 font-medium text-(--color-text-secondary)">Date</th>
            </tr>
          </thead>
          <tbody>
            {pageItems.map(p => (
              <tr key={p.id} className="border-b border-(--color-border) last:border-0">
                <td className="py-1.5 pr-2 text-(--color-text)">{ratingLabel(p.predicted_fsrs_rating)}</td>
                <td className="py-1.5 px-2 text-(--color-text)">
                  {p.actual_outcome !== null ? ratingLabel(p.actual_outcome) : <span className="text-(--color-text-tertiary)">--</span>}
                </td>
                <td className="py-1.5 px-2 text-right text-(--color-text-secondary)">{(p.predicted_confidence * 100).toFixed(0)}%</td>
                <td className="py-1.5 px-2 text-right font-medium" style={{ color: driftColor(p.drift_score) }}>
                  {p.drift_score !== null ? p.drift_score.toFixed(1) : "--"}
                </td>
                <td className="py-1.5 px-2 text-right text-(--color-text-tertiary)">
                  {p.calibration_offset_applied !== 0 ? (p.calibration_offset_applied > 0 ? "+" : "") + p.calibration_offset_applied.toFixed(3) : "--"}
                </td>
                <td className="py-1.5 pl-2 text-right text-(--color-text-tertiary) whitespace-nowrap">{relativeTime(p.created_at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-2">
          <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0}
            className="px-2 py-1 text-xs text-(--color-text-secondary) disabled:opacity-30">Prev</button>
          <span className="text-xs text-(--color-text-tertiary)">{page + 1} / {totalPages}</span>
          <button onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))} disabled={page >= totalPages - 1}
            className="px-2 py-1 text-xs text-(--color-text-secondary) disabled:opacity-30">Next</button>
        </div>
      )}
    </div>
  );
}

// ── Main Page ──

export default function CalibrationPage() {
  useEffect(() => { document.title = "Evaluator Calibration | METHEAN"; }, []);

  const { selectedChild } = useChild();
  const { toast } = useToast();
  const [profile, setProfile] = useState<CalibrationProfileData | null>(null);
  const [reconciledCount, setReconciledCount] = useState(0);
  const [threshold, setThreshold] = useState(50);
  const [predictions, setPredictions] = useState<PredictionItem[]>([]);
  const [driftHistory, setDriftHistory] = useState<DriftPoint[]>([]);
  const [temporalDrift, setTemporalDrift] = useState<TemporalDriftResponse | null>(null);
  const [confDist, setConfDist] = useState<ConfidenceDistributionResponse | null>(null);
  const [subjectDetail, setSubjectDetail] = useState<SubjectCalibrationItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Offset controls
  const [offsetActive, setOffsetActive] = useState(true);
  const [overrideInput, setOverrideInput] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => { if (selectedChild) load(); }, [selectedChild]);

  async function load() {
    if (!selectedChild) return;
    setLoading(true);
    setError("");
    try {
      const [profileRes, predsRes, driftRes, tempRes, confRes, subjRes] = await Promise.all([
        calibration.profile(selectedChild.id),
        calibration.predictions(selectedChild.id, { reconciled_only: false, limit: 100 }),
        calibration.driftHistory(selectedChild.id, 12),
        calibration.temporalDrift(selectedChild.id),
        calibration.confidenceDistribution(selectedChild.id),
        calibration.subjectDetail(selectedChild.id),
      ]);
      setProfile(profileRes.profile);
      setReconciledCount(profileRes.profile?.reconciled_predictions ?? profileRes.reconciled_predictions ?? 0);
      setThreshold(profileRes.threshold);
      setPredictions(predsRes.items);
      setDriftHistory(driftRes.series);
      setTemporalDrift(tempRes);
      setConfDist(confRes);
      setSubjectDetail(subjRes.subjects);
      if (profileRes.profile) {
        setOffsetActive(profileRes.profile.offset_active);
        setOverrideInput(profileRes.profile.parent_override_offset !== null ? String(profileRes.profile.parent_override_offset) : "");
      }
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't load calibration data.");
    } finally {
      setLoading(false);
    }
  }

  async function handleToggleOffset() {
    if (!selectedChild) return;
    setSaving(true);
    try {
      await calibration.updateOffset(selectedChild.id, { offset_active: !offsetActive });
      setOffsetActive(!offsetActive);
      toast("Calibration offset " + (!offsetActive ? "enabled" : "disabled"), "success");
    } catch (err: any) {
      toast(err?.detail || "Failed to update offset", "error");
    } finally {
      setSaving(false);
    }
  }

  async function handleSetOverride() {
    if (!selectedChild) return;
    setSaving(true);
    try {
      const val = overrideInput.trim() === "" ? null : parseFloat(overrideInput);
      if (val !== null && (isNaN(val) || val < -0.15 || val > 0.15)) {
        toast("Override must be between -0.15 and 0.15", "error");
        setSaving(false);
        return;
      }
      await calibration.updateOffset(selectedChild.id, { parent_override_offset: val });
      toast(val === null ? "Override cleared" : `Override set to ${val}`, "success");
      await load();
    } catch (err: any) {
      toast(err?.detail || "Failed to set override", "error");
    } finally {
      setSaving(false);
    }
  }

  async function handleExport() {
    if (!selectedChild) return;
    try {
      const data = await calibration.exportData(selectedChild.id);
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `calibration-${selectedChild.id}.json`;
      a.click();
      URL.revokeObjectURL(url);
      toast("Calibration data exported", "success");
    } catch (err: any) {
      toast(err?.detail || "Export failed", "error");
    }
  }

  if (!selectedChild) return <EmptyState title="Select a child" description="Choose a child from the sidebar." icon="empty" />;
  if (loading) return <LoadingSkeleton />;
  if (error) return <div className="p-6 text-center text-(--color-danger) text-sm">{error}</div>;

  const biasLabel = profile
    ? profile.directional_bias > 0.1
      ? "Evaluator tends to be too generous"
      : profile.directional_bias < -0.1
        ? "Evaluator tends to be too harsh"
        : "Evaluator is well-balanced"
    : null;

  const bandEntries = profile ? Object.entries(profile.confidence_band_accuracy) : [];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <PageHeader
        title="Evaluator Calibration"
        subtitle="Track and correct systematic bias in evaluator scoring"
        actions={
          <button onClick={handleExport} className="px-3 py-1.5 text-xs font-medium text-(--color-text-secondary) border border-(--color-border) rounded-[10px] hover:bg-(--color-page) transition-colors">
            Export Data
          </button>
        }
      />

      {/* Health + Bias overview */}
      <Card>
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="text-xs text-(--color-text-secondary) mb-1">Calibration Health</div>
            <HealthBadge profile={profile} reconciledCount={reconciledCount} threshold={threshold} />
          </div>
          {biasLabel && (
            <div>
              <div className="text-xs text-(--color-text-secondary) mb-1">Directional Bias</div>
              <div className="text-sm font-medium text-(--color-text)">{biasLabel}</div>
              <div className="text-xs text-(--color-text-tertiary)">Bias: {profile!.directional_bias.toFixed(3)}</div>
            </div>
          )}
          {profile && (
            <div>
              <div className="text-xs text-(--color-text-secondary) mb-1">Active Offset</div>
              <div className="text-sm font-medium text-(--color-text)">
                {profile.parent_override_offset !== null
                  ? `${profile.parent_override_offset > 0 ? "+" : ""}${profile.parent_override_offset.toFixed(3)} (override)`
                  : profile.recalibration_offset !== 0
                    ? `${profile.recalibration_offset > 0 ? "+" : ""}${profile.recalibration_offset.toFixed(3)}`
                    : "None"}
              </div>
              <div className="text-xs text-(--color-text-tertiary)">
                {profile.offset_active ? "Active" : "Disabled"} · {profile.reconciled_predictions} reconciled
              </div>
            </div>
          )}
          {temporalDrift && (
            <div>
              <div className="text-xs text-(--color-text-secondary) mb-1">Trend</div>
              <TrendArrow trend={temporalDrift.trend} slope={temporalDrift.trend_slope} />
            </div>
          )}
        </div>
        {profile?.last_computed_at && (
          <div className="text-xs text-(--color-text-tertiary) mt-3 pt-3 border-t border-(--color-border)">
            Last computed {relativeTime(profile.last_computed_at)}
          </div>
        )}
      </Card>

      {/* Drift History + Temporal Drift */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div>
          <SectionHeader title="Drift History" />
          <Card><LineChart data={driftHistory} /></Card>
        </div>
        <div>
          <SectionHeader title="Temporal Drift Analysis" />
          <Card>
            {temporalDrift ? (
              <LineChart
                data={temporalDrift.weekly_buckets}
                hoverExtra={(d: any) => <div className="text-(--color-text-secondary)">Bias: {d.bias > 0 ? "+" : ""}{d.bias?.toFixed(2)}</div>}
              />
            ) : (
              <div className="py-8 text-center text-xs text-(--color-text-tertiary)">Insufficient data.</div>
            )}
          </Card>
        </div>
      </div>

      {/* Confidence Distribution */}
      <div>
        <SectionHeader title="Confidence Distribution" />
        <Card>
          {confDist ? <ConfidenceHistogram data={confDist} /> : (
            <div className="py-8 text-center text-xs text-(--color-text-tertiary)">No confidence data yet.</div>
          )}
        </Card>
      </div>

      {/* Subject Calibration Cards */}
      <div>
        <SectionHeader title="Subject Calibration" />
        <SubjectCards subjects={subjectDetail} />
      </div>

      {/* Offset Controls */}
      {profile && (
        <div>
          <SectionHeader title="Offset Controls" />
          <Card>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm font-medium text-(--color-text)">Auto-calibration</div>
                  <div className="text-xs text-(--color-text-secondary)">Automatically apply computed offset to evaluator scores</div>
                </div>
                <button
                  onClick={handleToggleOffset}
                  disabled={saving}
                  className="relative w-11 h-6 rounded-full transition-colors duration-200 focus:outline-none"
                  style={{ background: offsetActive ? "var(--color-success)" : "var(--color-border)" }}
                >
                  <span className="absolute left-0.5 top-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform duration-200"
                    style={{ transform: offsetActive ? "translateX(20px)" : "translateX(0)" }} />
                </button>
              </div>

              <div className="border-t border-(--color-border) pt-4">
                <div className="text-sm font-medium text-(--color-text) mb-1">Manual Override</div>
                <div className="text-xs text-(--color-text-secondary) mb-2">Set a fixed offset (-0.15 to 0.15). Leave empty to use auto-computed value.</div>
                <div className="flex gap-2 items-center">
                  <input
                    type="number" step="0.01" min="-0.15" max="0.15"
                    value={overrideInput}
                    onChange={(e) => setOverrideInput(e.target.value)}
                    placeholder="Auto"
                    className="w-28 px-3 py-1.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text) focus:outline-none focus:border-(--color-accent)"
                  />
                  <button onClick={handleSetOverride} disabled={saving}
                    className="px-3 py-1.5 text-xs font-medium text-(--color-accent) border border-(--color-accent)/30 rounded-[10px] hover:bg-(--color-accent)/5 transition-colors">
                    {saving ? "Saving..." : "Apply"}
                  </button>
                </div>
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* Confidence Band Accuracy */}
      {bandEntries.length > 0 && (
        <div>
          <SectionHeader title="Confidence Band Accuracy" />
          <Card>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {bandEntries.map(([band, data]) => (
                <div key={band} className="text-center p-3 rounded-[10px] bg-(--color-page) border border-(--color-border)">
                  <div className="text-[10px] font-medium text-(--color-text-secondary) mb-1">{band}</div>
                  <div className="text-lg font-semibold text-(--color-text)">{(data.hit_rate * 100).toFixed(0)}%</div>
                  <div className="text-[10px] text-(--color-text-tertiary)">{data.total} predictions</div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}

      {/* Prediction Explorer */}
      <div>
        <SectionHeader title="Prediction Explorer" />
        <Card>
          <PredictionExplorer predictions={predictions} childId={selectedChild.id} />
        </Card>
      </div>
    </div>
  );
}
