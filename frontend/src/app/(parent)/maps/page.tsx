"use client";

import { useEffect, useState } from "react";
import { children as childrenApi, curriculum, type MapState, type MapNodeState } from "@/lib/api";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import { useChild } from "@/lib/ChildContext";

// ── Node card styling by mastery + status ──
function nodeStyle(node: MapNodeState): { bg: string; border: string; text: string } {
  const m = node.mastery_level;
  const s = node.status;
  if (m === "mastered")   return { bg: "bg-green-50",  border: "border-green-400",  text: "text-green-900" };
  if (m === "proficient") return { bg: "bg-blue-50",   border: "border-blue-400",   text: "text-blue-900" };
  if (m === "developing") return { bg: "bg-yellow-50", border: "border-yellow-400", text: "text-yellow-900" };
  if (m === "emerging")   return { bg: "bg-orange-50", border: "border-orange-400", text: "text-orange-900" };
  if (s === "available")  return { bg: "bg-white",     border: "border-green-300 border-dashed", text: "text-slate-700" };
  return                         { bg: "bg-slate-50",  border: "border-slate-300",  text: "text-slate-400" };
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

  if (!selectedChild) return <div className="text-sm text-slate-500">Select a child from the sidebar.</div>;
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
      <div className="mb-6">
        <h1 className="text-xl font-semibold text-slate-800">Learning Maps</h1>
        <p className="text-sm text-slate-500">{selectedChild.first_name}&apos;s curriculum &mdash; the full journey ahead</p>
      </div>

      {/* ── Map selector ── */}
      {mapStates.length > 1 && (
        <div className="flex gap-3 mb-6">
          {mapStates.map((ms) => (
            <button key={ms.learning_map_id} onClick={() => setSelectedMap(ms)}
              className={`px-4 py-2 text-sm rounded-lg border transition-colors ${
                selectedMap?.learning_map_id === ms.learning_map_id
                  ? "border-blue-500 bg-blue-50 text-blue-700 font-medium"
                  : "border-slate-200 text-slate-600 hover:border-slate-300"
              }`}
            >{ms.map_name}</button>
          ))}
        </div>
      )}

      {mapStates.length === 0 && (
        <div className="bg-white rounded-lg border border-slate-200 p-12 text-center text-sm text-slate-400">
          No maps enrolled. Complete onboarding to get started.
        </div>
      )}

      {selectedMap && (
        <>
          {/* ── Legend ── */}
          <div className="flex items-center gap-4 mb-4 text-xs text-slate-500">
            <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-sm bg-green-100 border border-green-400" /> Mastered</span>
            <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-sm bg-blue-100 border border-blue-400" /> Proficient</span>
            <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-sm bg-yellow-100 border border-yellow-400" /> Developing</span>
            <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-sm bg-orange-100 border border-orange-400" /> Emerging</span>
            <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-sm bg-white border border-dashed border-green-300" /> Available</span>
            <span className="flex items-center gap-1.5"><span className="w-3 h-3 rounded-sm bg-slate-100 border border-slate-300" /> Blocked</span>
          </div>

          {/* ── DAG visualization ── */}
          <div className="bg-white rounded-lg border border-slate-200 p-6">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-sm font-semibold text-slate-800">{selectedMap.map_name}</h2>
              <a href={`/curriculum/editor?map_id=${selectedMap.learning_map_id}`}
                className="text-xs text-blue-600 hover:underline">Edit Map</a>
            </div>

            <div className="space-y-1">
              {tiers.map((tier, tierIdx) => (
                <div key={tierIdx}>
                  {/* Connector lines from previous tier */}
                  {tierIdx > 0 && (
                    <div className="flex justify-center py-1">
                      <div className="w-px h-4 bg-slate-300" />
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
                          className={`relative w-52 rounded-lg border-2 p-3 ${style.bg} ${style.border} ${style.text}`}
                        >
                          {/* Checkmark for mastered */}
                          {isMastered && (
                            <span className="absolute -top-1.5 -right-1.5 w-5 h-5 rounded-full bg-green-500 text-white text-[10px] flex items-center justify-center font-bold">
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
                              className="mt-2 text-[10px] text-blue-600 hover:underline"
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
          </div>

          {/* ── Override modal ── */}
          {overrideNodeId && (
            <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
              <div className="bg-white rounded-lg border border-slate-200 p-6 w-96 shadow-lg">
                <h3 className="text-sm font-semibold text-slate-800 mb-1">Unlock Blocked Node</h3>
                <p className="text-xs text-slate-500 mb-4">
                  This bypasses the prerequisite requirement. Your reason will be recorded in the governance log.
                </p>
                <textarea
                  value={overrideReason}
                  onChange={(e) => setOverrideReason(e.target.value)}
                  placeholder="Why are you unlocking this node?"
                  className="w-full px-3 py-2 text-sm border border-slate-300 rounded-md mb-3 h-20 resize-none focus:outline-none focus:ring-1 focus:ring-blue-400"
                />
                <div className="flex gap-2 justify-end">
                  <button
                    onClick={() => { setOverrideNodeId(null); setOverrideReason(""); }}
                    className="px-3 py-1.5 text-xs text-slate-600 border border-slate-300 rounded-md hover:bg-slate-50"
                  >Cancel</button>
                  <button
                    onClick={handleOverride}
                    disabled={!overrideReason.trim() || overriding}
                    className="px-3 py-1.5 text-xs font-medium bg-amber-500 text-white rounded-md hover:bg-amber-600 disabled:opacity-50"
                  >{overriding ? "Unlocking..." : "Unlock Node"}</button>
                </div>
              </div>
            </div>
          )}

          {/* ── Override notice ── */}
          <div className="mt-4 px-4 py-3 bg-slate-50 rounded-lg border border-slate-200 text-xs text-slate-500">
            If you disagree with a prerequisite, you can unlock any blocked node.
            Every override is logged in your <a href="/governance/overrides" className="text-blue-600 hover:underline">governance trail</a>.
          </div>

          {/* ── Map metadata ── */}
          <div className="mt-4 flex items-center gap-6 text-xs text-slate-400">
            <span>{total} nodes</span>
            <span>{mastered} mastered</span>
            <span>{Math.round((selectedMap.progress_pct || 0) * 100)}% complete</span>
          </div>
        </>
      )}
    </div>
  );
}
