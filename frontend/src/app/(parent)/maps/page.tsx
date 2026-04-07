"use client";

import { useEffect, useState } from "react";
import { children as childrenApi, curriculum, type MapState, type MapNodeState } from "@/lib/api";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import { useChild } from "@/lib/ChildContext";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import EmptyState from "@/components/ui/EmptyState";
import { cn } from "@/lib/cn";

// ── Node card styling by mastery + status ──
function nodeStyle(node: MapNodeState): { bg: string; border: string; text: string } {
  const m = node.mastery_level;
  const s = node.status;
  if (m === "mastered")   return { bg: "bg-(--color-success-light)",  border: "border-(--color-success)",  text: "text-(--color-success)" };
  if (m === "proficient") return { bg: "bg-(--color-accent-light)",   border: "border-(--color-accent)",   text: "text-(--color-accent)" };
  if (m === "developing") return { bg: "bg-(--color-warning-light)",  border: "border-(--color-warning)",  text: "text-(--color-warning)" };
  if (m === "emerging")   return { bg: "bg-(--color-danger-light)",    border: "border-(--color-danger)",    text: "text-(--color-danger)" };
  if (s === "available")  return { bg: "bg-(--color-surface)",        border: "border-(--color-success)/50 border-dashed", text: "text-(--color-text)" };
  return                         { bg: "bg-(--color-page)",           border: "border-(--color-border-strong)",  text: "text-(--color-text-tertiary)" };
}

const typeLabel: Record<string, string> = {
  root: "ROOT", milestone: "MILESTONE", concept: "CONCEPT", skill: "SKILL",
};

// ── Build tier layout from DAG ──
function buildTiers(nodes: MapNodeState[]): MapNodeState[][] {
  const byId = new Map(nodes.map((n) => [n.node_id, n]));
  const depths = new Map<string, number>();

  // BFS from roots (no prerequisites)
  const queue: string[] = [];
  nodes.forEach((n) => {
    if (n.prerequisite_node_ids.length === 0) {
      depths.set(n.node_id, 0);
      queue.push(n.node_id);
    }
  });

  // Assign depth = max(parent depths) + 1
  while (queue.length > 0) {
    const id = queue.shift()!;
    const d = depths.get(id) || 0;
    // Find children: nodes that have this as a prerequisite
    nodes.forEach((n) => {
      if (n.prerequisite_node_ids.includes(id)) {
        const existing = depths.get(n.node_id);
        if (existing === undefined || d + 1 > existing) {
          depths.set(n.node_id, d + 1);
          queue.push(n.node_id);
        }
      }
    });
  }

  // Nodes not reachable from roots get depth 0
  nodes.forEach((n) => { if (!depths.has(n.node_id)) depths.set(n.node_id, 0); });

  // Group by depth
  const maxDepth = Math.max(...depths.values(), 0);
  const tiers: MapNodeState[][] = Array.from({ length: maxDepth + 1 }, () => []);
  nodes.forEach((n) => tiers[depths.get(n.node_id) || 0].push(n));
  return tiers;
}

export default function MapsPage() {
  useEffect(() => { document.title = "Maps | METHEAN"; }, []);

  const { selectedChild } = useChild();
  const [mapStates, setMapStates] = useState<MapState[]>([]);
  const [selectedMap, setSelectedMap] = useState<MapState | null>(null);
  const [loading, setLoading] = useState(true);
  const [overrideNodeId, setOverrideNodeId] = useState<string | null>(null);
  const [overrideReason, setOverrideReason] = useState("");
  const [overriding, setOverriding] = useState(false);

  useEffect(() => { if (selectedChild) loadMaps(); }, [selectedChild]);

  async function loadMaps() {
    if (!selectedChild) return;
    setLoading(true);
    try {
      const states = await childrenApi.allMapState(selectedChild.id);
      setMapStates(states);
      if (states.length > 0) setSelectedMap(states[0]);
    } catch {} finally { setLoading(false); }
  }

  async function handleOverride() {
    if (!selectedChild || !overrideNodeId || !overrideReason.trim()) return;
    setOverriding(true);
    try {
      await curriculum.override(selectedChild.id, overrideNodeId, overrideReason);
      setOverrideNodeId(null);
      setOverrideReason("");
      await loadMaps();
    } catch {} finally { setOverriding(false); }
  }

  if (!selectedChild) return <div className="text-sm text-(--color-text-secondary)">Select a child from the sidebar.</div>;
  if (loading) return <div className="max-w-5xl space-y-4"><LoadingSkeleton variant="text" count={1} /><LoadingSkeleton variant="card" count={3} /></div>;

  const mastered = selectedMap?.nodes.filter((n) => n.mastery_level === "mastered").length || 0;
  const total = selectedMap?.nodes.length || 0;
  const tiers = selectedMap ? buildTiers(selectedMap.nodes) : [];

  // Build a set of parent->child edges for drawing connectors
  const edges: { from: string; to: string }[] = [];
  if (selectedMap) {
    selectedMap.nodes.forEach((n) => {
      n.prerequisite_node_ids.forEach((pid) => edges.push({ from: pid, to: n.node_id }));
    });
  }

  return (
    <div className="max-w-5xl">
      <PageHeader
        title="Learning Maps"
        subtitle={`${selectedChild.first_name}'s curriculum \u2014 the full journey ahead`}
      />

      {/* ── Map selector ── */}
      {mapStates.length > 1 && (
        <div className="flex gap-3 mb-6">
          {mapStates.map((ms) => (
            <button key={ms.learning_map_id} onClick={() => setSelectedMap(ms)}
              className={cn(
                "px-4 py-2 text-sm rounded-[6px] border transition-colors",
                selectedMap?.learning_map_id === ms.learning_map_id
                  ? "border-(--color-accent) bg-(--color-accent-light) text-(--color-accent) font-medium"
                  : "border-(--color-border) text-(--color-text-secondary) hover:border-(--color-border-strong)"
              )}
            >{ms.map_name}</button>
          ))}
        </div>
      )}

      {mapStates.length === 0 && (
        <EmptyState
          icon="empty"
          title="No maps enrolled"
          description="Complete onboarding to get started."
        />
      )}

      {selectedMap && (
        <>
          {/* ── Legend ── */}
          <div className="flex items-center gap-4 mb-4 text-xs text-(--color-text-secondary)">
            <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-sm bg-(--color-success-light) border border-(--color-success)" /> Mastered</span>
            <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-sm bg-(--color-accent-light) border border-(--color-accent)" /> Proficient</span>
            <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-sm bg-(--color-warning-light) border border-(--color-warning)" /> Developing</span>
            <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-sm bg-(--color-danger-light) border border-(--color-danger)" /> Emerging</span>
            <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-sm bg-(--color-surface) border border-dashed border-(--color-success)/50" /> Available</span>
            <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-sm bg-(--color-page) border border-(--color-border-strong)" /> Blocked</span>
          </div>

          {/* ── DAG visualization ── */}
          <Card padding="p-6">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-sm font-semibold text-(--color-text)">{selectedMap.map_name}</h2>
              <a href={`/curriculum/editor?map_id=${selectedMap.learning_map_id}`}
                className="text-xs text-(--color-accent) hover:underline">Edit Map</a>
            </div>

            <div className="space-y-1">
              {tiers.map((tier, tierIdx) => (
                <div key={tierIdx}>
                  {/* Connector lines from previous tier */}
                  {tierIdx > 0 && (
                    <div className="flex justify-center py-1">
                      <div className="w-px h-4 bg-(--color-border-strong)" />
                    </div>
                  )}

                  {/* Nodes in this tier */}
                  <div className="flex flex-wrap justify-center gap-3">
                    {tier.map((node) => {
                      const style = nodeStyle(node);
                      const isBlocked = node.status === "blocked";
                      const isMastered = node.mastery_level === "mastered";

                      return (
                        <div key={node.node_id}
                          className={`relative w-52 rounded-[10px] border-2 p-3 ${style.bg} ${style.border} ${style.text}`}
                        >
                          {/* Checkmark for mastered */}
                          {isMastered && (
                            <span className="absolute -top-1.5 -right-1.5 w-5 h-5 rounded-full bg-(--color-success) text-white text-[10px] flex items-center justify-center font-bold">
                              &#10003;
                            </span>
                          )}

                          <div className="flex items-center gap-1.5 mb-1">
                            <span className="text-[9px] font-bold uppercase tracking-wider opacity-60">
                              {typeLabel[node.node_type] || node.node_type}
                            </span>
                          </div>
                          <div className={`text-sm font-medium ${isBlocked ? "opacity-50" : ""}`}>
                            {node.title}
                          </div>

                          {/* Stats row */}
                          <div className="flex items-center gap-2 mt-1.5 text-[10px] opacity-70">
                            {node.attempts_count > 0 && <span>{node.attempts_count} attempts</span>}
                            {node.time_spent_minutes > 0 && <span>{node.time_spent_minutes}m spent</span>}
                            {node.attempts_count === 0 && node.time_spent_minutes === 0 && !isMastered && (
                              <span>&mdash;</span>
                            )}
                          </div>

                          {/* Blocked unlock button */}
                          {isBlocked && !node.is_unlocked && (
                            <button
                              onClick={() => setOverrideNodeId(node.node_id)}
                              className="mt-2 text-[10px] text-(--color-accent) hover:underline"
                            >
                              Unlock
                            </button>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* ── Override modal ── */}
          {overrideNodeId && (
            <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
              <Card padding="p-6" className="w-96 shadow-lg">
                <h3 className="text-sm font-semibold text-(--color-text) mb-1">Unlock Blocked Node</h3>
                <p className="text-xs text-(--color-text-secondary) mb-4">
                  This bypasses the prerequisite requirement. Your reason will be recorded in the governance log.
                </p>
                <textarea
                  value={overrideReason}
                  onChange={(e) => setOverrideReason(e.target.value)}
                  placeholder="Why are you unlocking this node?"
                  className="w-full px-3 py-2 text-sm border border-(--color-border-strong) rounded-[6px] mb-3 h-20 resize-none focus:outline-none focus:ring-1 focus:ring-(--color-accent)"
                />
                <div className="flex gap-2 justify-end">
                  <Button
                    onClick={() => { setOverrideNodeId(null); setOverrideReason(""); }}
                    variant="secondary" size="sm"
                  >Cancel</Button>
                  <Button
                    onClick={handleOverride}
                    disabled={!overrideReason.trim() || overriding}
                    size="sm"
                    className="bg-(--color-warning) hover:opacity-90"
                  >{overriding ? "Unlocking..." : "Unlock Node"}</Button>
                </div>
              </Card>
            </div>
          )}

          {/* ── Override notice ── */}
          <div className="mt-4 px-4 py-3 bg-(--color-page) rounded-[10px] border border-(--color-border) text-xs text-(--color-text-secondary)">
            If you disagree with a prerequisite, you can unlock any blocked node.
            Every override is logged in your <a href="/governance/overrides" className="text-(--color-accent) hover:underline">governance trail</a>.
          </div>

          {/* ── Map metadata ── */}
          <div className="mt-4 flex items-center gap-6 text-xs text-(--color-text-secondary)">
            <span>{total} nodes</span>
            <span>{mastered} mastered</span>
            <span>{Math.round((selectedMap.progress_pct || 0) * 100)}% complete</span>
          </div>
        </>
      )}
    </div>
  );
}
