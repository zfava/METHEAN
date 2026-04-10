"use client";

import { useMemo } from "react";

interface JourneyNode {
  id: string;
  title: string;
  mastery: string;
  is_next: boolean;
}

interface JourneyMapProps {
  nodes: JourneyNode[];
  subject: string;
  subjectColor?: string;
}

export default function JourneyMap({ nodes, subject, subjectColor = "var(--color-accent)" }: JourneyMapProps) {
  const orderedNodes = useMemo(() => {
    const mastered = nodes.filter((n) => n.mastery === "mastered");
    const current = nodes.filter((n) => n.is_next);
    const upcoming = nodes.filter((n) => n.mastery !== "mastered" && !n.is_next);
    return [...mastered, ...current, ...upcoming];
  }, [nodes]);

  if (orderedNodes.length === 0) return null;

  const nodeSize = 40;
  const spacing = 70;
  const amplitude = 60;
  const svgWidth = 320;
  const svgHeight = orderedNodes.length * spacing + 60;

  return (
    <div className="w-full overflow-hidden">
      <div className="text-xs font-medium text-(--color-text-secondary) mb-2">{subject}</div>
      <svg viewBox={`0 0 ${svgWidth} ${svgHeight}`} className="w-full max-w-xs" xmlns="http://www.w3.org/2000/svg">
        {/* Path connecting nodes */}
        {orderedNodes.length > 1 && (
          <path
            d={orderedNodes.map((_, i) => {
              const x = svgWidth / 2 + Math.sin(i * 0.8) * amplitude;
              const y = 30 + i * spacing;
              return `${i === 0 ? "M" : "L"} ${x} ${y}`;
            }).join(" ")}
            fill="none"
            stroke="var(--color-border)"
            strokeWidth="3"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        )}

        {/* Completed path overlay */}
        {(() => {
          const lastMastered = orderedNodes.findIndex((n) => n.mastery !== "mastered");
          const completedCount = lastMastered === -1 ? orderedNodes.length : lastMastered;
          if (completedCount < 2) return null;
          const pathD = orderedNodes.slice(0, completedCount).map((_, i) => {
            const x = svgWidth / 2 + Math.sin(i * 0.8) * amplitude;
            const y = 30 + i * spacing;
            return `${i === 0 ? "M" : "L"} ${x} ${y}`;
          }).join(" ");
          return <path d={pathD} fill="none" stroke={subjectColor} strokeWidth="3" strokeLinecap="round" />;
        })()}

        {/* Node circles */}
        {orderedNodes.map((node, i) => {
          const x = svgWidth / 2 + Math.sin(i * 0.8) * amplitude;
          const y = 30 + i * spacing;
          const isMastered = node.mastery === "mastered";
          const isCurrent = node.is_next;
          const isUpcoming = !isMastered && !isCurrent;

          return (
            <g key={node.id}>
              {/* Pulse animation for current */}
              {isCurrent && (
                <circle cx={x} cy={y} r={nodeSize / 2 + 6} fill="none" stroke={subjectColor} strokeWidth="2" opacity="0.3">
                  <animate attributeName="r" from={String(nodeSize / 2 + 4)} to={String(nodeSize / 2 + 12)} dur="1.5s" repeatCount="indefinite" />
                  <animate attributeName="opacity" from="0.4" to="0" dur="1.5s" repeatCount="indefinite" />
                </circle>
              )}

              {/* Node circle */}
              <circle
                cx={x} cy={y} r={nodeSize / 2}
                fill={isMastered ? subjectColor : isCurrent ? "white" : "var(--color-surface)"}
                stroke={isMastered ? subjectColor : isCurrent ? subjectColor : "var(--color-border)"}
                strokeWidth={isCurrent ? 3 : 2}
              />

              {/* Star for mastered */}
              {isMastered && (
                <text x={x} y={y + 5} textAnchor="middle" fontSize="16" fill="white">&#11088;</text>
              )}

              {/* Dot for current */}
              {isCurrent && (
                <circle cx={x} cy={y} r={6} fill={subjectColor} />
              )}

              {/* Title label */}
              <text
                x={x + (Math.sin(i * 0.8) > 0 ? -(nodeSize / 2 + 8) : nodeSize / 2 + 8)}
                y={y + 4}
                textAnchor={Math.sin(i * 0.8) > 0 ? "end" : "start"}
                fontSize="11"
                fill={isMastered ? "var(--color-text)" : isUpcoming ? "var(--color-text-tertiary)" : "var(--color-text)"}
                fontWeight={isCurrent ? "600" : "400"}
              >
                {node.title.length > 22 ? node.title.slice(0, 20) + "..." : node.title}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
