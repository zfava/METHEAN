"use client";

import { useEffect, useState } from "react";
import { children as childrenApi, type MapState } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";

const statusColors: Record<string, string> = {
  mastered: "bg-green-500", in_progress: "bg-blue-500",
  available: "bg-amber-400", blocked: "bg-slate-300",
};

export default function ScopePage() {
  const { selectedChild } = useChild();
  const [maps, setMaps] = useState<MapState[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (selectedChild) {
      childrenApi.allMapState(selectedChild.id).then(setMaps).finally(() => setLoading(false));
    }
  }, [selectedChild]);

  if (!selectedChild) return <div className="text-sm text-slate-500">Select a child.</div>;
  if (loading) return <LoadingSkeleton variant="list" count={5} />;

  return (
    <div className="max-w-3xl print:max-w-none">
      <div className="flex items-center justify-between mb-6 print:mb-4">
        <div>
          <h1 className="text-xl font-semibold text-slate-800">Scope &amp; Sequence</h1>
          <p className="text-sm text-slate-500">{selectedChild.first_name} &middot; {selectedChild.grade_level || ""}</p>
        </div>
        <button onClick={() => window.print()} className="text-xs text-slate-400 hover:text-slate-600 print:hidden">Print</button>
      </div>

      <div className="space-y-8 print:space-y-4">
        {maps.map((ms) => {
          const mastered = ms.nodes.filter((n) => n.mastery_level === "mastered").length;
          const totalMins = ms.nodes.reduce((s, n) => s + n.time_spent_minutes, 0);
          return (
            <div key={ms.learning_map_id} className="bg-white rounded-lg border border-slate-200 print:border-0 print:shadow-none">
              <div className="px-5 py-4 border-b border-slate-100">
                <h2 className="text-sm font-bold text-slate-800">{ms.map_name}</h2>
                <div className="text-xs text-slate-500 mt-1">
                  {mastered}/{ms.nodes.length} mastered &middot; {Math.round(totalMins / 60)}h logged
                </div>
              </div>
              <div className="divide-y divide-slate-50">
                {ms.nodes.map((node, i) => (
                  <div key={node.node_id} className="flex items-center gap-3 px-5 py-2.5">
                    <span className={`w-2 h-2 rounded-full shrink-0 ${statusColors[node.status] || "bg-slate-300"}`} />
                    <div className="flex-1">
                      <span className="text-sm text-slate-700">{node.title}</span>
                      {node.node_type === "milestone" && (
                        <span className="ml-2 text-[9px] font-bold text-blue-600 uppercase">Milestone</span>
                      )}
                    </div>
                    <div className="flex items-center gap-3 text-xs text-slate-400">
                      <span className="capitalize">{node.mastery_level.replace(/_/g, " ")}</span>
                      {node.time_spent_minutes > 0 && <span>{node.time_spent_minutes}m</span>}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
        {maps.length === 0 && <p className="text-sm text-slate-400">No enrolled maps.</p>}
      </div>
    </div>
  );
}
