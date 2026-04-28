"use client";

import { useMemo, useState, useRef, useEffect } from "react";

export interface JourneyNode {
  id: string;
  title: string;
  mastery: string;
  is_next: boolean;
  is_current?: boolean;
  type?: string;       // "milestone" for special rendering
  attempts_count?: number;
  mastered_at?: string;
  prerequisites?: string[];
}

interface JourneyMapProps {
  nodes: JourneyNode[];
  subject: string;
  subjectColor?: string;
}

// ── Helpers ──

function bezierPath(points: Array<{ x: number; y: number }>): string {
  if (points.length < 2) return "";
  let d = `M ${points[0].x} ${points[0].y}`;
  for (let i = 1; i < points.length; i++) {
    const prev = points[i - 1];
    const curr = points[i];
    const cpy1 = prev.y + (curr.y - prev.y) * 0.4;
    const cpy2 = curr.y - (curr.y - prev.y) * 0.4;
    d += ` C ${prev.x} ${cpy1}, ${curr.x} ${cpy2}, ${curr.x} ${curr.y}`;
  }
  return d;
}

function truncTitle(t: string, max = 20): string {
  return t.length > max ? t.slice(0, max - 2) + "\u2026" : t;
}

// ── Tooltip ──

function NodeTooltip({ node, x, y, onClose }: {
  node: JourneyNode; x: number; y: number; onClose: () => void;
}) {
  const isMastered = node.mastery === "mastered";
  const isCurrent = node.is_current || node.is_next;
  const isLocked = !isMastered && !isCurrent && node.mastery === "not_started";

  return (
    <foreignObject x={x - 80} y={y + 30} width={160} height={80}>
      <div onClick={onClose}
        className="bg-(--color-surface) border border-(--color-border) rounded-xl shadow-lg px-3 py-2 text-center cursor-pointer">
        <div className="text-[11px] font-medium text-(--color-text) truncate">{node.title}</div>
        {isMastered && node.mastered_at && (
          <div className="text-[9px] text-(--color-text-tertiary)">Mastered {new Date(node.mastered_at).toLocaleDateString()}</div>
        )}
        {isCurrent && (
          <div className="text-[9px] text-(--color-accent) capitalize">{node.mastery.replace(/_/g, " ")}</div>
        )}
        {isLocked && node.prerequisites && node.prerequisites.length > 0 && (
          <div className="text-[9px] text-(--color-text-tertiary)">Complete prerequisites first</div>
        )}
        {!isLocked && !isMastered && !isCurrent && (
          <div className="text-[9px] text-(--color-text-tertiary) capitalize">{node.mastery.replace(/_/g, " ")}</div>
        )}
      </div>
    </foreignObject>
  );
}

// ── Single Subject Map ──

function SubjectMap({ nodes, subjectColor }: { nodes: JourneyNode[]; subjectColor: string }) {
  const [tooltip, setTooltip] = useState<{ node: JourneyNode; x: number; y: number } | null>(null);

  const orderedNodes = useMemo(() => {
    // Preserve original order (topological from API)
    return nodes;
  }, [nodes]);

  const nodeSize = 18;
  const currentSize = 26;
  const spacing = 64;
  const amplitude = 55;
  const svgWidth = 300;
  const paddingTop = 40;
  const svgHeight = orderedNodes.length * spacing + paddingTop + 30;

  // Compute positions
  const positions = useMemo(() =>
    orderedNodes.map((_, i) => ({
      x: svgWidth / 2 + Math.sin(i * 0.75) * amplitude,
      y: paddingTop + i * spacing,
    })),
    [orderedNodes.length]
  );

  // Find split point: last mastered index
  const lastMasteredIdx = useMemo(() => {
    let idx = -1;
    for (let i = 0; i < orderedNodes.length; i++) {
      if (orderedNodes[i].mastery === "mastered") idx = i;
      else break;
    }
    return idx;
  }, [orderedNodes]);

  // Find current node index
  const currentIdx = useMemo(() =>
    orderedNodes.findIndex(n => n.is_current || n.is_next),
    [orderedNodes]
  );

  // Completed path points (through mastered + current)
  const completedEnd = currentIdx >= 0 ? currentIdx + 1 : lastMasteredIdx + 1;
  const completedPts = positions.slice(0, completedEnd);
  const allPts = positions;

  // Reduced motion check
  const [reducedMotion, setReducedMotion] = useState(false);
  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReducedMotion(mq.matches);
    const handler = (e: MediaQueryListEvent) => setReducedMotion(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  if (orderedNodes.length === 0) return null;

  return (
    <svg viewBox={`0 0 ${svgWidth} ${svgHeight}`} className="w-full" role="img"
      aria-label={`Learning journey with ${orderedNodes.length} topics`}>
      {/* Soft drop-shadow used by mastered nodes for a subtle weight. */}
      <defs>
        <filter id="masteredShadow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur in="SourceAlpha" stdDeviation="1.5" />
          <feOffset dy="1.5" />
          <feComponentTransfer>
            <feFuncA type="linear" slope="0.35" />
          </feComponentTransfer>
          <feMerge>
            <feMergeNode />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      {/* Full upcoming path (dashed). Smooth bezier curves between
          every node, not straight lines — bezierPath() in this file
          interpolates control points at 40% of the segment height. */}
      {allPts.length > 1 && (
        <path d={bezierPath(allPts)} fill="none" stroke="var(--color-border)" strokeWidth="2"
          strokeDasharray="6 4" strokeLinecap="round" />
      )}

      {/* Completed path (solid, subject color) */}
      {completedPts.length > 1 && (
        <path d={bezierPath(completedPts)} fill="none" stroke={subjectColor} strokeWidth="3"
          strokeLinecap="round" />
      )}

      {/* Nodes */}
      {orderedNodes.map((node, i) => {
        const pos = positions[i];
        const isMastered = node.mastery === "mastered";
        const isCurrent = node.is_current || node.is_next;
        const isLocked = node.mastery === "not_started" && !isCurrent;
        const isMilestone = node.type === "milestone";
        const r = isCurrent ? currentSize / 2 : isMilestone ? nodeSize / 2 + 4 : nodeSize / 2;
        const nodeFilter = isMastered ? "url(#masteredShadow)" : undefined;

        // Label position: alternate left/right
        const labelSide = Math.sin(i * 0.75) > 0 ? "left" : "right";
        const labelX = labelSide === "left" ? pos.x - r - 8 : pos.x + r + 8;
        const labelAnchor = labelSide === "left" ? "end" : "start";

        return (
          <g key={node.id} onClick={() => setTooltip(tooltip?.node.id === node.id ? null : { node, x: pos.x, y: pos.y })}
            className="cursor-pointer" role="button" tabIndex={0} aria-label={`${node.title}: ${node.mastery}`}
            onKeyDown={e => { if (e.key === "Enter") setTooltip(tooltip?.node.id === node.id ? null : { node, x: pos.x, y: pos.y }); }}>

            {/* Current node pulse — uses the design-system
                .animate-pulse-soft class wrapped on a <g> so the
                whole node breathes gently. SVG <animate> still drives
                the expanding outer ring for the "active step" feel. */}
            {isCurrent && !reducedMotion && (
              <circle cx={pos.x} cy={pos.y} r={r + 6} fill="none" stroke={subjectColor} strokeWidth="2" opacity="0.3">
                <animate attributeName="r" from={String(r + 4)} to={String(r + 14)} dur="2s" repeatCount="indefinite" />
                <animate attributeName="opacity" from="0.35" to="0" dur="2s" repeatCount="indefinite" />
              </circle>
            )}

            {/* Mastered glow */}
            {isMastered && (
              <circle cx={pos.x} cy={pos.y} r={r + 3} fill={subjectColor} opacity="0.12" />
            )}

            {/* Milestone shape: hexagon-ish */}
            {isMilestone ? (
              <polygon
                points={[0, 1, 2, 3, 4, 5].map(j => {
                  const angle = (Math.PI / 3) * j - Math.PI / 6;
                  return `${pos.x + (r + 2) * Math.cos(angle)},${pos.y + (r + 2) * Math.sin(angle)}`;
                }).join(" ")}
                fill={isMastered ? subjectColor : isCurrent ? "white" : "var(--color-surface)"}
                stroke={isMastered ? subjectColor : isCurrent ? subjectColor : isLocked ? "var(--color-border)" : "var(--color-border)"}
                strokeWidth={isCurrent ? 3 : 2}
                strokeDasharray={isLocked ? "3 2" : undefined}
                filter={nodeFilter}
                className={isCurrent && !reducedMotion ? "animate-pulse-soft" : undefined}
                style={isCurrent ? { transformOrigin: `${pos.x}px ${pos.y}px` } : undefined}
              />
            ) : (
              /* Regular circle */
              <circle cx={pos.x} cy={pos.y} r={r}
                fill={isMastered ? subjectColor : isCurrent ? "white" : isLocked ? "var(--color-page)" : "var(--color-surface)"}
                stroke={isMastered ? subjectColor : isCurrent ? subjectColor : "var(--color-border)"}
                strokeWidth={isCurrent ? 3 : 2}
                strokeDasharray={isLocked ? "3 2" : undefined}
                opacity={isLocked ? 0.5 : 1}
                filter={nodeFilter}
                className={isCurrent && !reducedMotion ? "animate-pulse-soft" : undefined}
                style={isCurrent ? { transformOrigin: `${pos.x}px ${pos.y}px` } : undefined}
              />
            )}

            {/* Mastered: checkmark */}
            {isMastered && (
              <path d={`M ${pos.x - 5} ${pos.y} l 3 3 7 -7`} fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            )}

            {/* Current: filled dot */}
            {isCurrent && !isMilestone && (
              <circle cx={pos.x} cy={pos.y} r={5} fill={subjectColor} />
            )}

            {/* Milestone flag for mastered milestones */}
            {isMilestone && isMastered && (
              <text x={pos.x} y={pos.y + 4} textAnchor="middle" fontSize="12" fill="white">{"\u2691"}</text>
            )}

            {/* Title */}
            <text x={labelX} y={pos.y + (isCurrent ? 0 : 4)}
              textAnchor={labelAnchor}
              fontSize={isCurrent ? "12" : "10"}
              fill={isMastered ? "var(--color-text-secondary)" : isLocked ? "var(--color-text-tertiary)" : "var(--color-text)"}
              fontWeight={isCurrent ? "600" : "400"}
              opacity={isLocked ? 0.6 : 1}>
              {truncTitle(node.title)}
            </text>

            {/* Current mastery label */}
            {isCurrent && (
              <text x={labelX} y={pos.y + 14} textAnchor={labelAnchor} fontSize="9"
                fill={subjectColor} className="capitalize">
                {node.mastery.replace(/_/g, " ")}
              </text>
            )}
          </g>
        );
      })}

      {/* Tooltip */}
      {tooltip && <NodeTooltip node={tooltip.node} x={tooltip.x} y={tooltip.y} onClose={() => setTooltip(null)} />}
    </svg>
  );
}

// ── Multi-Subject Tabbed View ──

export default function JourneyMap({ nodes, subject, subjectColor = "var(--color-accent)" }: JourneyMapProps) {
  // Single subject mode (backward compatible)
  if (nodes.length === 0) {
    return (
      <div className="w-full py-8 text-center">
        <p className="text-xs text-(--color-text-tertiary)">Your {subject} journey hasn't started yet.</p>
        <p className="text-[10px] text-(--color-text-tertiary) mt-1">Your parent is preparing the path.</p>
      </div>
    );
  }

  return (
    <div className="w-full overflow-hidden">
      <div className="flex items-center gap-2 mb-2">
        <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ background: subjectColor }} />
        <span className="text-xs font-medium text-(--color-text-secondary)">{subject}</span>
        <span className="text-[10px] text-(--color-text-tertiary) ml-auto">
          {nodes.filter(n => n.mastery === "mastered").length} / {nodes.length}
        </span>
      </div>
      <div className="overflow-y-auto max-h-[500px]">
        <SubjectMap nodes={nodes} subjectColor={subjectColor} />
      </div>
    </div>
  );
}

// ── Multi-Subject Carousel (used by child dashboard) ──

export function JourneyCarousel({ maps }: {
  maps: Array<{ map_id: string; subject: string; subject_color: string;
    nodes: JourneyNode[]; total_nodes: number; mastered_nodes: number }>;
}) {
  const [activeTab, setActiveTab] = useState(0);

  if (maps.length === 0) return null;

  return (
    <div>
      {/* Tab bar */}
      <div className="flex gap-1 overflow-x-auto pb-2 mb-2" role="tablist">
        {maps.map((m, i) => (
          <button key={m.map_id} onClick={() => setActiveTab(i)} role="tab" aria-selected={i === activeTab}
            className={`shrink-0 px-3 py-1.5 text-xs rounded-full transition-colors min-h-[36px] ${
              i === activeTab ? "text-white font-medium" : "text-(--color-text-secondary) bg-(--color-surface) border border-(--color-border)"
            }`}
            style={i === activeTab ? { background: m.subject_color } : undefined}>
            {m.subject}
            <span className="ml-1 opacity-70">{m.mastered_nodes}/{m.total_nodes}</span>
          </button>
        ))}
      </div>

      {/* Active map */}
      <div className="overflow-y-auto max-h-[500px]">
        <SubjectMap
          nodes={maps[activeTab].nodes}
          subjectColor={maps[activeTab].subject_color}
        />
      </div>
    </div>
  );
}
