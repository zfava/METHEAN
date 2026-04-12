"use client";

import { useEffect, useState } from "react";
import { styleVector, type StyleVectorData } from "@/lib/api";
import { useToast } from "@/components/Toast";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import SectionHeader from "@/components/ui/SectionHeader";
import EmptyState from "@/components/ui/EmptyState";
import { relativeTime } from "@/lib/format";

// ── Dimension metadata ──

interface DimMeta {
  key: string;
  label: string;
  hint: string;
  type: "float" | "int" | "str";
  min?: number;
  max?: number;
  values?: string[];
}

const DIMENSIONS: DimMeta[] = [
  { key: "optimal_session_minutes", label: "Session Length", hint: "Needs 20+ session durations", type: "int", min: 10, max: 60 },
  { key: "socratic_responsiveness", label: "Socratic Response", hint: "Needs 20+ tutor sessions", type: "float", min: 0, max: 1 },
  { key: "frustration_threshold", label: "Frustration Tolerance", hint: "Needs 20+ evaluated attempts", type: "float", min: 0, max: 1 },
  { key: "recovery_rate", label: "Recovery Speed", hint: "Needs 10+ difficulty setbacks", type: "float", min: 0, max: 1 },
  { key: "time_of_day_peak", label: "Peak Time", hint: "Needs 20+ attempts with time data", type: "int", min: 0, max: 23 },
  { key: "modality_preference", label: "Learning Modality", hint: "Needs 30+ total attempts", type: "str", values: ["visual", "auditory", "kinesthetic", "reading_writing", "mixed"] },
  { key: "pacing_preference", label: "Pacing", hint: "Needs 20+ mastery transitions", type: "float", min: -1, max: 1 },
  { key: "independence_level", label: "Independence", hint: "Needs 15+ tutor sessions", type: "float", min: 0, max: 1 },
  { key: "attention_pattern", label: "Attention Pattern", hint: "Needs 20+ session durations", type: "str", values: ["sustained", "burst", "variable"] },
];

// ── Helpers ──

function levelLabel(v: number): { text: string; color: string } {
  if (v < 0.3) return { text: "LOW", color: "var(--color-danger)" };
  if (v <= 0.7) return { text: "MODERATE", color: "var(--color-warning)" };
  return { text: "HIGH", color: "var(--color-success)" };
}

function formatValue(dim: DimMeta, value: any): string {
  if (value === null || value === undefined) return "--";
  if (dim.key === "optimal_session_minutes") return `${value} min`;
  if (dim.key === "time_of_day_peak") {
    const h = value as number;
    if (h < 12) return `${h} AM`;
    if (h === 12) return "12 PM";
    return `${h - 12} PM`;
  }
  if (dim.key === "modality_preference") {
    const labels: Record<string, string> = { visual: "Visual", auditory: "Auditory", kinesthetic: "Hands-on", reading_writing: "Reading/Writing", mixed: "Mixed" };
    return labels[value] || value;
  }
  if (dim.key === "attention_pattern") {
    const labels: Record<string, string> = { sustained: "Sustained", burst: "Burst", variable: "Variable" };
    return labels[value] || value;
  }
  if (dim.key === "pacing_preference") {
    const v = value as number;
    if (v > 0.3) return `+${v.toFixed(1)} (accelerate)`;
    if (v < -0.3) return `${v.toFixed(1)} (slower)`;
    return `${v.toFixed(1)} (standard)`;
  }
  if (typeof value === "number") return value.toFixed(2);
  return String(value);
}

function valueBadgeColor(dim: DimMeta, value: any): string {
  if (value === null || value === undefined) return "var(--color-text-tertiary)";
  if (dim.type === "float" && dim.min === 0 && dim.max === 1) return levelLabel(value as number).color;
  if (dim.key === "pacing_preference") {
    const v = value as number;
    if (Math.abs(v) < 0.3) return "var(--color-accent)";
    return v > 0 ? "var(--color-success)" : "var(--color-warning)";
  }
  return "var(--color-accent)";
}

// ── Dimension Card ──

function DimensionCard({ dim, vector, onOverride, onBounds }: {
  dim: DimMeta;
  vector: StyleVectorData;
  onOverride: (dimension: string, value: any, locked: boolean) => void;
  onBounds: (dimension: string, min: number | null, max: number | null) => void;
}) {
  const value = (vector as any)[dim.key];
  const isActive = value !== null && value !== undefined;
  const override = vector.parent_overrides?.[dim.key];
  const isLocked = override?.locked === true;
  const bounds = vector.parent_bounds?.[dim.key];

  const [showControls, setShowControls] = useState(false);
  const [overrideVal, setOverrideVal] = useState(isLocked ? String(override?.value ?? "") : "");
  const [boundsMin, setBoundsMin] = useState(bounds?.min !== undefined ? String(bounds.min) : "");
  const [boundsMax, setBoundsMax] = useState(bounds?.max !== undefined ? String(bounds.max) : "");

  return (
    <div
      className="p-3 rounded-[14px] border bg-(--color-surface) transition-shadow hover:shadow-md"
      style={{
        borderColor: isLocked ? "var(--color-accent)" : !isActive ? "var(--color-border)" : "var(--color-border)",
        opacity: isActive || isLocked ? 1 : 0.7,
      }}
    >
      <div className="flex items-start justify-between mb-2">
        <div className="text-xs font-medium text-(--color-text)">{dim.label}</div>
        <div className="flex items-center gap-1">
          {isLocked && (
            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-(--color-accent)/10 text-(--color-accent)">Locked</span>
          )}
          {bounds && (
            <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-(--color-warning)/10 text-(--color-warning)">Bounded</span>
          )}
        </div>
      </div>

      {isActive ? (
        <div className="mb-2">
          <span className="text-sm font-semibold px-2 py-0.5 rounded-full border" style={{ color: valueBadgeColor(dim, value), borderColor: valueBadgeColor(dim, value) }}>
            {formatValue(dim, value)}
          </span>
          {isLocked && value !== override?.value && (
            <div className="text-[10px] text-(--color-text-tertiary) mt-1">Computed: {formatValue(dim, value)}</div>
          )}
        </div>
      ) : (
        <div className="text-[10px] text-(--color-text-tertiary) mb-2">{dim.hint}</div>
      )}

      {/* Float dimensions get a level label */}
      {isActive && dim.type === "float" && dim.min === 0 && dim.max === 1 && (
        <div className="text-[10px] text-(--color-text-secondary) mb-2">
          {levelLabel(value as number).text}
        </div>
      )}

      {/* Controls toggle */}
      <button onClick={() => setShowControls(!showControls)} className="text-[10px] text-(--color-accent) hover:underline">
        {showControls ? "Hide controls" : "Parent controls"}
      </button>

      {showControls && (
        <div className="mt-2 pt-2 border-t border-(--color-border) space-y-2">
          {/* Override */}
          {dim.type !== "str" ? (
            <div className="flex items-center gap-1.5">
              <input
                type="number"
                step={dim.type === "int" ? 1 : 0.05}
                min={dim.min}
                max={dim.max}
                value={overrideVal}
                onChange={(e) => setOverrideVal(e.target.value)}
                placeholder="Override"
                className="w-20 px-2 py-1 text-[11px] border border-(--color-border) rounded-md bg-(--color-surface) text-(--color-text)"
              />
              <button
                onClick={() => {
                  const v = dim.type === "int" ? parseInt(overrideVal) : parseFloat(overrideVal);
                  if (!isNaN(v)) onOverride(dim.key, v, true);
                }}
                className="text-[10px] px-2 py-1 rounded-md bg-(--color-accent) text-white"
              >Lock</button>
              {isLocked && (
                <button
                  onClick={() => onOverride(dim.key, null, false)}
                  className="text-[10px] px-2 py-1 rounded-md border border-(--color-border) text-(--color-text-secondary)"
                >Unlock</button>
              )}
            </div>
          ) : (
            <div className="flex items-center gap-1.5">
              <select
                value={overrideVal}
                onChange={(e) => setOverrideVal(e.target.value)}
                className="px-2 py-1 text-[11px] border border-(--color-border) rounded-md bg-(--color-surface) text-(--color-text)"
              >
                <option value="">Select...</option>
                {dim.values?.map(v => <option key={v} value={v}>{v}</option>)}
              </select>
              <button
                onClick={() => { if (overrideVal) onOverride(dim.key, overrideVal, true); }}
                className="text-[10px] px-2 py-1 rounded-md bg-(--color-accent) text-white"
              >Lock</button>
              {isLocked && (
                <button
                  onClick={() => onOverride(dim.key, null, false)}
                  className="text-[10px] px-2 py-1 rounded-md border border-(--color-border) text-(--color-text-secondary)"
                >Unlock</button>
              )}
            </div>
          )}

          {/* Bounds (numeric only) */}
          {dim.type !== "str" && (
            <div className="flex items-center gap-1.5">
              <input type="number" step={dim.type === "int" ? 1 : 0.05} placeholder="Min" value={boundsMin} onChange={(e) => setBoundsMin(e.target.value)}
                className="w-16 px-2 py-1 text-[11px] border border-(--color-border) rounded-md bg-(--color-surface) text-(--color-text)" />
              <span className="text-[10px] text-(--color-text-tertiary)">to</span>
              <input type="number" step={dim.type === "int" ? 1 : 0.05} placeholder="Max" value={boundsMax} onChange={(e) => setBoundsMax(e.target.value)}
                className="w-16 px-2 py-1 text-[11px] border border-(--color-border) rounded-md bg-(--color-surface) text-(--color-text)" />
              <button
                onClick={() => {
                  const mn = boundsMin ? (dim.type === "int" ? parseInt(boundsMin) : parseFloat(boundsMin)) : null;
                  const mx = boundsMax ? (dim.type === "int" ? parseInt(boundsMax) : parseFloat(boundsMax)) : null;
                  onBounds(dim.key, mn, mx);
                }}
                className="text-[10px] px-2 py-1 rounded-md border border-(--color-warning)/30 text-(--color-warning)"
              >{bounds ? "Update" : "Set"} Bounds</button>
              {bounds && (
                <button onClick={() => { onBounds(dim.key, null, null); setBoundsMin(""); setBoundsMax(""); }}
                  className="text-[10px] text-(--color-text-tertiary) hover:underline">Clear</button>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ── Subject Affinity Chart ──

function SubjectAffinityChart({ data }: { data: Record<string, number> }) {
  const entries = Object.entries(data).sort((a, b) => b[1] - a[1]);
  if (entries.length === 0) return <div className="py-4 text-center text-xs text-(--color-text-tertiary)">No subject affinity data yet.</div>;

  return (
    <div className="space-y-2">
      {entries.map(([subject, score]) => (
        <div key={subject} className="flex items-center gap-3">
          <div className="w-24 text-xs text-(--color-text) truncate text-right">{subject.charAt(0).toUpperCase() + subject.slice(1)}</div>
          <div className="flex-1 h-5 bg-(--color-page) rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-300"
              style={{
                width: `${Math.max(score * 100, 4)}%`,
                background: score > 0.7 ? "var(--color-success)" : score > 0.4 ? "var(--color-accent)" : "var(--color-warning)",
              }}
            />
          </div>
          <div className="w-10 text-xs text-(--color-text-secondary) text-right">{(score * 100).toFixed(0)}%</div>
        </div>
      ))}
    </div>
  );
}

// ── Main Page ──

export default function StyleProfilePage() {
  useEffect(() => { document.title = "Learning Style Profile | METHEAN"; }, []);

  const { selectedChild } = useChild();
  const { toast } = useToast();
  const [vector, setVector] = useState<StyleVectorData | null>(null);
  const [obsCount, setObsCount] = useState(0);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => { if (selectedChild) load(); }, [selectedChild]);

  async function load() {
    if (!selectedChild) return;
    setLoading(true);
    setError("");
    try {
      const res = await styleVector.get(selectedChild.id);
      setVector(res.vector);
      setObsCount(res.vector?.data_points_count ?? res.observation_count ?? 0);
      setMessage(res.message || "");
    } catch (err: any) {
      setError(err?.detail || err?.message || "Couldn't load style profile.");
    } finally {
      setLoading(false);
    }
  }

  async function handleOverride(dimension: string, value: any, locked: boolean) {
    if (!selectedChild) return;
    try {
      await styleVector.setOverride(selectedChild.id, { dimension, value: value ?? 0, locked });
      toast(locked ? `${dimension} locked to ${value}` : `${dimension} unlocked`, "success");
      await load();
    } catch (err: any) {
      toast(err?.detail || "Failed to update override", "error");
    }
  }

  async function handleBounds(dimension: string, min: number | null, max: number | null) {
    if (!selectedChild) return;
    try {
      await styleVector.setBounds(selectedChild.id, { dimension, min, max });
      toast(min === null && max === null ? `Bounds cleared for ${dimension}` : `Bounds set for ${dimension}`, "success");
      await load();
    } catch (err: any) {
      toast(err?.detail || "Failed to update bounds", "error");
    }
  }

  if (!selectedChild) return <EmptyState title="Select a child" description="Choose a child from the sidebar." icon="empty" />;
  if (loading) return <LoadingSkeleton />;
  if (error) return <div className="p-6 text-center text-(--color-danger) text-sm">{error}</div>;

  if (!vector) {
    return (
      <div className="max-w-4xl mx-auto space-y-6">
        <PageHeader title="Learning Style Profile" subtitle="How your child learns best" />
        <EmptyState
          title="Building style profile"
          description={message || `${Math.max(0, 20 - obsCount)} more observations needed. The profile activates automatically as your child completes activities.`}
          icon="search"
        />
        <div className="text-center text-xs text-(--color-text-tertiary)">{obsCount} / 20 observations collected</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <PageHeader title="Learning Style Profile" subtitle="How your child learns best" />

      {/* Dimensions Grid */}
      <div>
        <SectionHeader title="Learning Dimensions" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {DIMENSIONS.map(dim => (
            <DimensionCard key={dim.key} dim={dim} vector={vector} onOverride={handleOverride} onBounds={handleBounds} />
          ))}
        </div>
      </div>

      {/* Subject Affinity */}
      {Object.keys(vector.subject_affinity_map || {}).length > 0 && (
        <div>
          <SectionHeader title="Subject Affinity" />
          <Card>
            <SubjectAffinityChart data={vector.subject_affinity_map} />
          </Card>
        </div>
      )}

      {/* Data Confidence */}
      <div className="text-center py-4 text-xs text-(--color-text-tertiary) border-t border-(--color-border)">
        Profile computed from {vector.data_points_count} observations. {vector.dimensions_active} of 10 dimensions active.
        {vector.last_computed_at && <> Last updated {relativeTime(vector.last_computed_at)}.</>}
      </div>
    </div>
  );
}
