"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { curriculum, type LearningMap, type MapDetail } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import LoadingSkeleton from "@/components/LoadingSkeleton";

export default function MapsPage() {
  const [maps, setMaps] = useState<LearningMap[]>([]);
  const [selectedMap, setSelectedMap] = useState<MapDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    curriculum.listMaps().then(setMaps).finally(() => setLoading(false));
  }, []);

  async function selectMap(mapId: string) {
    const detail = await curriculum.getMap(mapId);
    setSelectedMap(detail);
  }

  if (loading) return (
    <div className="max-w-6xl space-y-4">
      <LoadingSkeleton variant="text" count={1} />
      <LoadingSkeleton variant="card" count={3} />
    </div>
  );

  return (
    <div className="max-w-6xl">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-xl font-semibold">Learning Maps</h1>
      </div>

      <div className="grid grid-cols-3 gap-4 mb-8">
        {maps.map((m) => (
          <button
            key={m.id}
            onClick={() => selectMap(m.id)}
            className={`text-left bg-white rounded-lg border p-5 transition-colors ${
              selectedMap?.id === m.id
                ? "border-(--color-accent) ring-1 ring-(--color-accent)/20"
                : "border-(--color-border) hover:border-(--color-accent)"
            }`}
          >
            <div className="text-sm font-medium">{m.name}</div>
            <p className="text-xs text-(--color-text-secondary) mt-1">Version {m.version}</p>
            {m.description && (
              <p className="text-xs text-(--color-text-secondary) mt-2 line-clamp-2">{m.description}</p>
            )}
          </button>
        ))}
        {maps.length === 0 && (
          <div className="col-span-3 text-center py-12 text-sm text-(--color-text-secondary)">
            No learning maps yet. Complete onboarding to create one.
          </div>
        )}
      </div>

      {selectedMap && (
        <div className="bg-white rounded-lg border border-(--color-border)">
          <div className="px-5 py-4 border-b border-(--color-border) flex items-center justify-between">
            <div>
              <h2 className="text-sm font-semibold">{selectedMap.name}</h2>
              <p className="text-xs text-(--color-text-secondary)">{selectedMap.nodes.length} nodes, {selectedMap.edges.length} edges</p>
            </div>
          </div>
          <div className="p-5">
            <div className="grid gap-2">
              {selectedMap.nodes
                .sort((a, b) => a.sort_order - b.sort_order)
                .map((node) => {
                  const incoming = selectedMap.edges.filter((e) => e.to_node_id === node.id);
                  return (
                    <div key={node.id} className="flex items-center justify-between py-2 px-3 rounded-md bg-gray-50">
                      <div className="flex items-center gap-3">
                        <span className="text-xs font-mono text-(--color-text-secondary) w-16">{node.node_type}</span>
                        <span className="text-sm">{node.title}</span>
                      </div>
                      <div className="flex items-center gap-2 text-xs text-(--color-text-secondary)">
                        {incoming.length > 0 && (
                          <span>{incoming.length} prereq{incoming.length > 1 ? "s" : ""}</span>
                        )}
                        {node.estimated_minutes && <span>{node.estimated_minutes}m</span>}
                      </div>
                    </div>
                  );
                })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
