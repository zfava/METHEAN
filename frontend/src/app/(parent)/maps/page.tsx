"use client";

import { useEffect, useState } from "react";
import { children as childrenApi, curriculum, type MapState, type MapNodeState, type LearningMap } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import { useChild } from "@/lib/ChildContext";

const statusColors: Record<string, string> = {
  mastered: "border-l-emerald-500 bg-emerald-50",
  in_progress: "border-l-blue-500 bg-blue-50",
  available: "border-l-amber-500 bg-amber-50",
  blocked: "border-l-gray-300 bg-gray-50",
};

export default function MapsPage() {
  const { selectedChild } = useChild();
  const [mapStates, setMapStates] = useState<MapState[]>([]);
  const [selectedMap, setSelectedMap] = useState<MapState | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (selectedChild) loadMaps();
  }, [selectedChild]);

  async function loadMaps() {
    if (!selectedChild) return;
    setLoading(true);
    try {
      const states = await childrenApi.allMapState(selectedChild.id);
      setMapStates(states);
      if (states.length > 0) setSelectedMap(states[0]);
    } catch {} finally {
      setLoading(false);
    }
  }

  if (!selectedChild) return <div className="text-sm text-(--color-text-secondary)">Select a child from the sidebar.</div>;
  if (loading) return <div className="max-w-6xl space-y-4"><LoadingSkeleton variant="text" count={1} /><LoadingSkeleton variant="card" count={3} /></div>;

  return (
    <div className="max-w-6xl">
      <div className="mb-6">
        <h1 className="text-xl font-semibold">Learning Maps</h1>
        <p className="text-sm text-(--color-text-secondary)">{selectedChild.first_name}&apos;s curriculum</p>
      </div>

      {/* Map selector */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        {mapStates.map((ms) => (
          <button
            key={ms.learning_map_id}
            onClick={() => setSelectedMap(ms)}
            className={`text-left bg-white rounded-lg border p-4 transition-colors ${
              selectedMap?.learning_map_id === ms.learning_map_id
                ? "border-(--color-accent) ring-1 ring-(--color-accent)/20"
                : "border-(--color-border) hover:border-(--color-accent)"
            }`}
          >
            <div className="text-sm font-medium">{ms.map_name}</div>
            <div className="flex items-center gap-2 mt-2">
              <div className="flex-1 bg-gray-100 rounded-full h-1.5">
                <div className="bg-(--color-mastered) h-1.5 rounded-full" style={{ width: `${Math.round(ms.progress_pct * 100)}%` }} />
              </div>
              <span className="text-xs text-(--color-text-secondary)">{Math.round(ms.progress_pct * 100)}%</span>
            </div>
            <div className="text-xs text-(--color-text-secondary) mt-1">{ms.nodes.length} nodes</div>
          </button>
        ))}
        {mapStates.length === 0 && (
          <div className="col-span-3 text-center py-12 text-sm text-(--color-text-secondary)">
            No maps enrolled. Complete onboarding to get started.
          </div>
        )}
      </div>

      {/* Node list for selected map */}
      {selectedMap && (
        <div className="bg-white rounded-lg border border-(--color-border)">
          <div className="px-5 py-4 border-b border-(--color-border)">
            <h2 className="text-sm font-semibold">{selectedMap.map_name}</h2>
            <div className="flex gap-4 mt-2 text-xs text-(--color-text-secondary)">
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-emerald-500" /> Mastered</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-blue-500" /> In Progress</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-amber-500" /> Available</span>
              <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-gray-300" /> Blocked</span>
            </div>
          </div>
          <div className="divide-y divide-gray-50">
            {selectedMap.nodes.map((node) => {
              const color = statusColors[node.status] || statusColors.blocked;
              return (
                <div key={node.node_id} className={`flex items-center justify-between px-5 py-3 border-l-4 ${color}`}>
                  <div className="flex items-center gap-3">
                    <span className="text-xs font-mono text-(--color-text-secondary) w-16 shrink-0">{node.node_type}</span>
                    <div>
                      <span className="text-sm">{node.title}</span>
                      {node.prerequisite_node_ids.length > 0 && (
                        <span className="text-[10px] text-(--color-text-secondary) ml-2">
                          {node.prerequisite_node_ids.length} prereq{node.prerequisite_node_ids.length > 1 ? "s" : ""}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <StatusBadge status={node.status} />
                    {node.attempts_count > 0 && (
                      <span className="text-xs text-(--color-text-secondary)">{node.attempts_count} attempts</span>
                    )}
                    {node.time_spent_minutes > 0 && (
                      <span className="text-xs text-(--color-text-secondary)">{node.time_spent_minutes}m</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
