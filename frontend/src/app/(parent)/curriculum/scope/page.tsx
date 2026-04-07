"use client";

import { useEffect, useState } from "react";
import { children as childrenApi, type MapState } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import { cn } from "@/lib/cn";

const statusColors: Record<string, string> = {
  mastered: "bg-(--color-success)", in_progress: "bg-(--color-accent)",
  available: "bg-(--color-warning)", blocked: "bg-(--color-border-strong)",
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

  if (!selectedChild) return <div className="text-sm text-(--color-text-secondary)">Select a child.</div>;
  if (loading) return <LoadingSkeleton variant="list" count={5} />;

  return (
    <div className="max-w-3xl print:max-w-none">
      <PageHeader
        title="Scope & Sequence"
        subtitle={`${selectedChild.first_name} \u00b7 ${selectedChild.grade_level || ""}`}
        actions={
          <Button onClick={() => window.print()} variant="ghost" size="sm" className="print:hidden">Print</Button>
        }
        className="print:mb-4"
      />

      <div className="space-y-8 print:space-y-4">
        {maps.map((ms) => {
          const mastered = ms.nodes.filter((n) => n.mastery_level === "mastered").length;
          const totalMins = ms.nodes.reduce((s, n) => s + n.time_spent_minutes, 0);
          return (
            <Card key={ms.learning_map_id} padding="p-0" className="print:border-0 print:shadow-none">
              <div className="px-5 py-4 border-b border-(--color-border)">
                <h2 className="text-sm font-bold text-(--color-text)">{ms.map_name}</h2>
                <div className="text-xs text-(--color-text-secondary) mt-1">
                  {mastered}/{ms.nodes.length} mastered &middot; {Math.round(totalMins / 60)}h logged
                </div>
              </div>
              <div className="divide-y divide-(--color-page)">
                {ms.nodes.map((node, i) => (
                  <div key={node.node_id} className="flex items-center gap-3 px-5 py-2.5">
                    <span className={`w-2 h-2 rounded-full shrink-0 ${statusColors[node.status] || "bg-(--color-border-strong)"}`} />
                    <div className="flex-1">
                      <span className="text-sm text-(--color-text)">{node.title}</span>
                      {node.node_type === "milestone" && (
                        <span className="ml-2 text-[9px] font-bold text-(--color-accent) uppercase">Milestone</span>
                      )}
                    </div>
                    <div className="flex items-center gap-3 text-xs text-(--color-text-secondary)">
                      <span className="capitalize">{node.mastery_level.replace(/_/g, " ")}</span>
                      {node.time_spent_minutes > 0 && <span>{node.time_spent_minutes}m</span>}
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          );
        })}
        {maps.length === 0 && <p className="text-sm text-(--color-text-secondary)">No enrolled maps yet. Create a curriculum to see your scope and sequence here.</p>}
      </div>
    </div>
  );
}
