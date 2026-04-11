"use client";

import { useEffect, useState, useMemo, useRef } from "react";
import { calibration, type CalibrationProfileData, type PredictionItem, type DriftPoint } from "@/lib/api";
import { useToast } from "@/components/Toast";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import SectionHeader from "@/components/ui/SectionHeader";
import EmptyState from "@/components/ui/EmptyState";
import { relativeTime } from "@/lib/format";

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

// ── Drift history chart ──

function DriftChart({ data }: { data: DriftPoint[] }) {
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

  const height = 180;
  const pL = 36, pR = 16, pT = 16, pB = 32;
  const plotW = containerW - pL - pR;
  const plotH = height - pT - pB;

  const { points, maxY, gridLines } = useMemo(() => {
    if (data.length < 2) return { points: [], maxY: 0, gridLines: [] };
    const rawMax = Math.max(...data.map(d => d.mean_drift), 1);
    const maxY = Math.ceil(rawMax * 1.2 * 10) / 10;
    const xStep = plotW / Math.max(data.length - 1, 1);
    const points = data.map((d, i) => ({
      x: pL + i * xStep,
      y: pT + plotH - (d.mean_drift / maxY) * plotH,
    }));
    const gridLines = [0.5, 1.0, 1.5, 2.0].filter(v => v <= maxY).map(val => ({
      y: pT + plotH - (val / maxY) * plotH,
      label: val.toFixed(1),
    }));
    return { points, maxY, gridLines };
  }, [data, plotW, plotH]);

  if (data.length < 2) {
    return <div className="py-8 text-center text-xs text-(--color-text-tertiary)">Drift history will appear after 2+ weeks of data.</div>;
  }

  const xStep = plotW / Math.max(data.length - 1, 1);

  // Threshold bands
  const y05 = pT + plotH - (0.5 / maxY) * plotH;
  const y10 = pT + plotH - (1.0 / maxY) * plotH;

  return (
    <div ref={containerRef} className="relative w-full">
      <svg viewBox={`0 0 ${containerW} ${height}`} className="w-full">
        {/* Green zone (drift < 0.5) */}
        <rect x={pL} y={y05} width={plotW} height={pT + plotH - y05} fill="var(--color-success)" opacity={0.04} />
        {/* Yellow zone (0.5 - 1.0) */}
        {y10 < y05 && <rect x={pL} y={y10} width={plotW} height={y05 - y10} fill="var(--color-warning)" opacity={0.04} />}
        {/* Red zone (> 1.0) */}
        {y10 > pT && <rect x={pL} y={pT} width={plotW} height={y10 - pT} fill="var(--color-danger)" opacity={0.04} />}

        {gridLines.map(gl => (
          <g key={gl.label}>
            <line x1={pL} y1={gl.y} x2={containerW - pR} y2={gl.y} stroke="var(--color-border)" strokeWidth={1} strokeDasharray="3 3" />
            <text x={pL - 6} y={gl.y + 3} textAnchor="end" fill="var(--color-text-tertiary)" fontSize={10}>{gl.label}</text>
          </g>
        ))}

        <line x1={pL} y1={pT + plotH} x2={containerW - pR} y2={pT + plotH} stroke="var(--color-border)" strokeWidth={1} />

        {/* X axis labels */}
        {data.map((d, i) => {
          const show = data.length < 10 || i % 2 === 0 || i === data.length - 1;
          if (!show) return null;
          const dt = new Date(d.week);
          const label = dt.toLocaleDateString("en-US", { month: "short", day: "numeric" });
          return <text key={i} x={pL + i * xStep} y={height - 6} textAnchor="middle" fill="var(--color-text-tertiary)" fontSize={10}>{label}</text>;
        })}

        {/* Line */}
        {points.length > 1 && (
          <polyline
            points={points.map(p => `${p.x},${p.y}`).join(" ")}
            fill="none"
            stroke="var(--color-accent)"
            strokeWidth={2}
            strokeLinejoin="round"
          />
        )}

        {/* Dots */}
        {points.map((pt, i) => (
          <circle key={i} cx={pt.x} cy={pt.y} r={hoverIdx === i ? 5 : 3}
            fill={data[i].mean_drift < 0.5 ? "var(--color-success)" : data[i].mean_drift < 1.0 ? "var(--color-warning)" : "var(--color-danger)"}
            stroke="var(--color-surface)" strokeWidth={1.5}
            style={{ transition: "r 0.15s" }} />
        ))}

        {/* Hover zones */}
        {data.map((_, i) => (
          <rect key={i} x={pL + i * xStep - xStep / 2} y={pT} width={xStep} height={plotH}
            fill="transparent"
            onMouseEnter={() => setHoverIdx(i)}
            onMouseLeave={() => setHoverIdx(null)} />
        ))}

        {hoverIdx !== null && (
          <line x1={pL + hoverIdx * xStep} y1={pT} x2={pL + hoverIdx * xStep} y2={pT + plotH}
            stroke="var(--color-text-tertiary)" strokeWidth={1} strokeDasharray="2 2" opacity={0.5} />
        )}
      </svg>

      {hoverIdx !== null && data[hoverIdx] && (
        <div className="absolute bg-(--color-surface) border border-(--color-border) rounded-[10px] shadow-lg px-3 py-2 text-xs pointer-events-none z-10"
          style={{ left: `${((pL + hoverIdx * xStep) / containerW) * 100}%`, top: 8, transform: "translateX(-50%)" }}>
          <div className="font-medium text-(--color-text) mb-0.5">Week of {new Date(data[hoverIdx].week).toLocaleDateString("en-US", { month: "short", day: "numeric" })}</div>
          <div>Mean drift: <span className="font-medium">{data[hoverIdx].mean_drift.toFixed(2)}</span></div>
          <div className="text-(--color-text-tertiary)">{data[hoverIdx].count} predictions</div>
        </div>
      )}
    </div>
  );
}

// ── Rating label ──

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
  if (drift <= 1) return "var(--color-warning)";
  return "var(--color-danger)";
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
      const [profileRes, predsRes, driftRes] = await Promise.all([
        calibration.profile(selectedChild.id),
        calibration.predictions(selectedChild.id, { reconciled_only: false, limit: 20 }),
        calibration.driftHistory(selectedChild.id, 12),
      ]);
      setProfile(profileRes.profile);
      setReconciledCount(profileRes.profile?.reconciled_predictions ?? profileRes.reconciled_predictions ?? 0);
      setThreshold(profileRes.threshold);
      setPredictions(predsRes.items);
      setDriftHistory(driftRes.series);
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
  const subjectEntries = profile ? Object.entries(profile.subject_drift_map) : [];

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <PageHeader title="Evaluator Calibration" subtitle="Track and correct systematic bias in evaluator scoring" />

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
        </div>
        {profile?.last_computed_at && (
          <div className="text-xs text-(--color-text-tertiary) mt-3 pt-3 border-t border-(--color-border)">
            Last computed {relativeTime(profile.last_computed_at)}
          </div>
        )}
      </Card>

      {/* Drift History Chart */}
      <div>
        <SectionHeader title="Drift History" />
        <Card>
          <DriftChart data={driftHistory} />
        </Card>
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
                    type="number"
                    step="0.01"
                    min="-0.15"
                    max="0.15"
                    value={overrideInput}
                    onChange={(e) => setOverrideInput(e.target.value)}
                    placeholder="Auto"
                    className="w-28 px-3 py-1.5 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text) focus:outline-none focus:border-(--color-accent)"
                  />
                  <button
                    onClick={handleSetOverride}
                    disabled={saving}
                    className="px-3 py-1.5 text-xs font-medium text-(--color-accent) border border-(--color-accent)/30 rounded-[10px] hover:bg-(--color-accent)/5 transition-colors"
                  >
                    {saving ? "Saving..." : "Apply"}
                  </button>
                </div>
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* Subject Drift Table */}
      {subjectEntries.length > 0 && (
        <div>
          <SectionHeader title="Per-Topic Drift" />
          <Card>
            <div className="overflow-x-auto">
              <table className="w-full text-xs">
                <thead>
                  <tr className="border-b border-(--color-border)">
                    <th className="text-left py-2 pr-3 font-medium text-(--color-text-secondary)">Topic</th>
                    <th className="text-right py-2 px-3 font-medium text-(--color-text-secondary)">Mean Drift</th>
                    <th className="text-right py-2 px-3 font-medium text-(--color-text-secondary)">Bias</th>
                    <th className="text-right py-2 pl-3 font-medium text-(--color-text-secondary)">Count</th>
                  </tr>
                </thead>
                <tbody>
                  {subjectEntries.map(([topic, data]) => (
                    <tr key={topic} className="border-b border-(--color-border) last:border-0">
                      <td className="py-2 pr-3 text-(--color-text) truncate max-w-[200px]">{topic}</td>
                      <td className="py-2 px-3 text-right font-medium" style={{ color: driftColor(data.mean_drift) }}>
                        {data.mean_drift.toFixed(2)}
                      </td>
                      <td className="py-2 px-3 text-right text-(--color-text-secondary)">
                        {data.bias > 0 ? "+" : ""}{data.bias.toFixed(2)}
                      </td>
                      <td className="py-2 pl-3 text-right text-(--color-text-tertiary)">{data.count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
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

      {/* Recent Predictions */}
      <div>
        <SectionHeader title="Recent Predictions" />
        {predictions.length === 0 ? (
          <EmptyState title="No predictions yet" description="Predictions appear as your child completes activities." icon="empty" />
        ) : (
          <Card>
            <div className="space-y-2 max-h-80 overflow-y-auto">
              {predictions.map((p) => (
                <div key={p.id} className="flex items-center justify-between py-2 border-b border-(--color-border) last:border-0">
                  <div className="flex-1 min-w-0">
                    <div className="text-xs text-(--color-text)">
                      Predicted: <span className="font-medium">{ratingLabel(p.predicted_fsrs_rating)}</span>
                      <span className="text-(--color-text-tertiary) ml-1">({(p.predicted_confidence * 100).toFixed(0)}%)</span>
                    </div>
                    {p.actual_outcome !== null && (
                      <div className="text-xs text-(--color-text-secondary)">
                        Actual: <span className="font-medium">{ratingLabel(p.actual_outcome)}</span>
                      </div>
                    )}
                    {p.calibration_offset_applied !== 0 && (
                      <div className="text-[10px] text-(--color-text-tertiary)">
                        Offset: {p.calibration_offset_applied > 0 ? "+" : ""}{p.calibration_offset_applied.toFixed(3)}
                      </div>
                    )}
                  </div>
                  <div className="flex items-center gap-3">
                    {p.drift_score !== null ? (
                      <span className="text-xs font-medium px-2 py-0.5 rounded-full border" style={{ color: driftColor(p.drift_score), borderColor: driftColor(p.drift_score) }}>
                        {p.drift_score === 0 ? "Match" : `Drift ${p.drift_score.toFixed(1)}`}
                      </span>
                    ) : (
                      <span className="text-[10px] text-(--color-text-tertiary)">Pending</span>
                    )}
                    <span className="text-[10px] text-(--color-text-tertiary) whitespace-nowrap">
                      {relativeTime(p.created_at)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
