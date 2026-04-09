"use client";

import { useState, useMemo } from "react";
import type { MapNodeState } from "@/lib/api";
import { cn } from "@/lib/cn";

// ── Layout constants ──
const NODE_W = 160;
const NODE_H = 72;
const MILESTONE_W = 180;
const MILESTONE_H = 80;
const ROOT_W = 120;
const ROOT_H = 56;
const GAP_X = 24;
const GAP_Y = 64;

function dims(type: string): [number, number] {
  if (type === "milestone") return [MILESTONE_W, MILESTONE_H];
  if (type === "root") return [ROOT_W, ROOT_H];
  return [NODE_W, NODE_H];
}

const TYPE_LABELS: Record<string, string> = {
  root: "ROOT", milestone: "MILESTONE", concept: "CONCEPT", skill: "SKILL",
  safety: "⚠️ SAFETY", knowledge: "KNOWLEDGE", technique: "TECHNIQUE",
  project: "PROJECT", certification_prep: "CERT PREP",
};

// ── Mastery colors as CSS var references ──
function masteryStyle(node: MapNodeState): { fill: string; stroke: string; opacity: number; dashed: boolean } {
  const m = node.mastery_level;
  const s = node.status;
  if (m === "mastered")   return { fill: "rgba(45,106,79,0.08)", stroke: "var(--color-success)", opacity: 1, dashed: false };
  if (m === "proficient") return { fill: "rgba(74,111,165,0.08)", stroke: "var(--color-accent)", opacity: 1, dashed: false };
  if (m === "developing") return { fill: "rgba(184,134,11,0.08)", stroke: "var(--color-warning)", opacity: 1, dashed: false };
  if (m === "emerging")   return { fill: "rgba(166,61,64,0.08)", stroke: "var(--color-danger)", opacity: 1, dashed: false };
  if (s === "available")  return { fill: "#FFFFFF", stroke: "rgba(45,106,79,0.3)", opacity: 1, dashed: true };
  return                         { fill: "var(--color-page)", stroke: "var(--color-border-strong)", opacity: 0.6, dashed: false };
}

interface DagGraphProps {
  nodes: MapNodeState[];
  onNodeClick?: (node: MapNodeState) => void;
}

export default function DagGraph({ nodes, onNodeClick }: DagGraphProps) {
  const [hoveredId, setHoveredId] = useState<string | null>(null);

  // Build tiers via BFS
  const { tiers, nodePositions, edges, svgW, svgH } = useMemo(() => {
    const byId = new Map(nodes.map((n) => [n.node_id, n]));
    const depths = new Map<string, number>();
    const queue: string[] = [];

    nodes.forEach((n) => {
      if (n.prerequisite_node_ids.length === 0) {
        depths.set(n.node_id, 0);
        queue.push(n.node_id);
      }
    });

    while (queue.length > 0) {
      const id = queue.shift()!;
      const d = depths.get(id) || 0;
      nodes.forEach((n) => {
        if (n.prerequisite_node_ids.includes(id)) {
          if ((depths.get(n.node_id) ?? -1) < d + 1) {
            depths.set(n.node_id, d + 1);
            queue.push(n.node_id);
          }
        }
      });
    }

    nodes.forEach((n) => { if (!depths.has(n.node_id)) depths.set(n.node_id, 0); });

    const maxDepth = Math.max(...depths.values(), 0);
    const tiers: MapNodeState[][] = Array.from({ length: maxDepth + 1 }, () => []);
    nodes.forEach((n) => tiers[depths.get(n.node_id) || 0].push(n));

    // Calculate positions
    const positions = new Map<string, { x: number; y: number; w: number; h: number }>();
    let maxTierW = 0;

    tiers.forEach((tier, tierIdx) => {
      const tierW = tier.reduce((sum, n) => sum + dims(n.node_type)[0] + GAP_X, -GAP_X);
      maxTierW = Math.max(maxTierW, tierW);
    });

    const svgWidth = Math.max(maxTierW + 80, 600);

    tiers.forEach((tier, tierIdx) => {
      const tierW = tier.reduce((sum, n) => sum + dims(n.node_type)[0] + GAP_X, -GAP_X);
      let x = (svgWidth - tierW) / 2;
      const y = tierIdx * (NODE_H + GAP_Y) + 20;

      tier.forEach((node) => {
        const [w, h] = dims(node.node_type);
        positions.set(node.node_id, { x, y, w, h });
        x += w + GAP_X;
      });
    });

    // Build edges
    const edgeList: Array<{ from: string; to: string }> = [];
    nodes.forEach((n) => {
      n.prerequisite_node_ids.forEach((pid) => {
        if (byId.has(pid)) edgeList.push({ from: pid, to: n.node_id });
      });
    });

    const svgHeight = (maxDepth + 1) * (NODE_H + GAP_Y) + 40;

    return { tiers, nodePositions: positions, edges: edgeList, svgW: svgWidth, svgH: svgHeight };
  }, [nodes]);

  // Hovered node's prerequisites for highlight
  const hoveredPrereqs = useMemo(() => {
    if (!hoveredId) return new Set<string>();
    const node = nodes.find((n) => n.node_id === hoveredId);
    return new Set(node?.prerequisite_node_ids || []);
  }, [hoveredId, nodes]);

  if (nodes.length === 0) return null;

  return (
    <div className="overflow-auto rounded-[14px] border border-(--color-border) bg-(--color-surface)" style={{ maxHeight: "70vh" }}>
      <svg
        width={svgW}
        height={svgH}
        viewBox={`0 0 ${svgW} ${svgH}`}
        className="block"
      >
        {/* Edges */}
        {edges.map((edge, i) => {
          const fromPos = nodePositions.get(edge.from);
          const toPos = nodePositions.get(edge.to);
          if (!fromPos || !toPos) return null;

          const fromNode = nodes.find((n) => n.node_id === edge.from);
          const toNode = nodes.find((n) => n.node_id === edge.to);
          const fromMastered = fromNode?.mastery_level === "mastered";
          const toMastered = toNode?.mastery_level === "mastered";
          const isHighlighted = hoveredId === edge.to && hoveredPrereqs.has(edge.from);

          const x1 = fromPos.x + fromPos.w / 2;
          const y1 = fromPos.y + fromPos.h;
          const x2 = toPos.x + toPos.w / 2;
          const y2 = toPos.y;
          const cy1 = y1 + GAP_Y * 0.4;
          const cy2 = y2 - GAP_Y * 0.4;

          return (
            <path
              key={i}
              d={`M ${x1} ${y1} C ${x1} ${cy1}, ${x2} ${cy2}, ${x2} ${y2}`}
              fill="none"
              stroke={isHighlighted ? "var(--color-accent)" : fromMastered && toMastered ? "rgba(45,106,79,0.2)" : fromMastered ? "rgba(45,106,79,0.4)" : "var(--color-border-strong)"}
              strokeWidth={isHighlighted ? 2.5 : 1.5}
              strokeDasharray={!fromMastered && !isHighlighted ? "4 3" : undefined}
              style={{ transition: "stroke 0.2s, stroke-width 0.2s" }}
            />
          );
        })}

        {/* Nodes */}
        {nodes.map((node) => {
          const pos = nodePositions.get(node.node_id);
          if (!pos) return null;
          const style = masteryStyle(node);
          const isMastered = node.mastery_level === "mastered";
          const isBlocked = node.status === "blocked";
          const isHovered = hoveredId === node.node_id;

          return (
            <g key={node.node_id}>
              <rect
                x={pos.x}
                y={pos.y}
                width={pos.w}
                height={pos.h}
                rx={14}
                fill={style.fill}
                stroke={isHovered ? "var(--color-accent)" : style.stroke}
                strokeWidth={isHovered ? 2 : 1.5}
                strokeDasharray={style.dashed ? "4 3" : undefined}
                opacity={style.opacity}
                style={{ cursor: "pointer", transition: "stroke 0.15s, stroke-width 0.15s" }}
                onMouseEnter={() => setHoveredId(node.node_id)}
                onMouseLeave={() => setHoveredId(null)}
                onClick={() => onNodeClick?.(node)}
              />
              <foreignObject x={pos.x} y={pos.y} width={pos.w} height={pos.h}
                style={{ pointerEvents: "none" }}>
                <div style={{ padding: "8px 10px", height: "100%", display: "flex", flexDirection: "column", justifyContent: "center", opacity: style.opacity }}>
                  <div style={{ fontSize: 9, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.05em", opacity: 0.5, marginBottom: 2, color: "var(--color-text-secondary)" }}>
                    {TYPE_LABELS[node.node_type] || node.node_type}
                  </div>
                  <div style={{
                    fontSize: 13, fontWeight: 500, color: "var(--color-text)",
                    overflow: "hidden", display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical",
                    lineHeight: "1.3",
                  }}>
                    {node.title}
                  </div>
                  {(node.attempts_count > 0 || node.time_spent_minutes > 0) && (
                    <div style={{ fontSize: 10, color: "var(--color-text-tertiary)", marginTop: 2 }}>
                      {node.attempts_count > 0 && `${node.attempts_count} attempts`}
                      {node.attempts_count > 0 && node.time_spent_minutes > 0 && " · "}
                      {node.time_spent_minutes > 0 && `${node.time_spent_minutes}m`}
                    </div>
                  )}
                </div>
              </foreignObject>
              {/* Mastered checkmark */}
              {isMastered && (
                <g transform={`translate(${pos.x + pos.w - 8}, ${pos.y - 4})`}>
                  <circle r={8} fill="var(--color-success)" />
                  <text x={0} y={3} textAnchor="middle" fill="white" fontSize={10} fontWeight="bold">✓</text>
                </g>
              )}
              {/* Blocked lock */}
              {isBlocked && !node.is_unlocked && (
                <g transform={`translate(${pos.x + pos.w - 8}, ${pos.y - 4})`}>
                  <circle r={8} fill="var(--color-text-tertiary)" />
                  <text x={0} y={3} textAnchor="middle" fill="white" fontSize={8}>🔒</text>
                </g>
              )}
            </g>
          );
        })}
      </svg>
    </div>
  );
}
