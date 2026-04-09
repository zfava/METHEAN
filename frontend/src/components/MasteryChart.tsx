"use client";

import { useState, useRef, useMemo } from "react";

interface DataPoint {
  week: string;
  mastered: number;
  progressed: number;
  total_minutes: number;
}

interface MasteryChartProps {
  data: DataPoint[];
  height?: number;
}

function shortDate(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

function cubicPath(points: Array<{ x: number; y: number }>): string {
  if (points.length < 2) return "";
  let d = `M ${points[0].x} ${points[0].y}`;
  for (let i = 1; i < points.length; i++) {
    const prev = points[i - 1];
    const curr = points[i];
    const cpx1 = prev.x + (curr.x - prev.x) * 0.4;
    const cpx2 = curr.x - (curr.x - prev.x) * 0.4;
    d += ` C ${cpx1} ${prev.y}, ${cpx2} ${curr.y}, ${curr.x} ${curr.y}`;
  }
  return d;
}

export default function MasteryChart({ data, height = 200 }: MasteryChartProps) {
  const [hoverIdx, setHoverIdx] = useState<number | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const paddingL = 36;
  const paddingR = 16;
  const paddingT = 16;
  const paddingB = 32;

  const chartW = 600;
  const chartH = height;
  const plotW = chartW - paddingL - paddingR;
  const plotH = chartH - paddingT - paddingB;

  const { masteredPts, progressedPts, maxY, gridLines, xLabels, areaPath } = useMemo(() => {
    if (data.length < 2) return { masteredPts: [], progressedPts: [], maxY: 0, gridLines: [], xLabels: [], areaPath: "" };

    const allVals = data.flatMap((d) => [d.mastered, d.progressed]);
    const rawMax = Math.max(...allVals, 1);
    const maxY = Math.ceil(rawMax * 1.15);

    const xStep = plotW / Math.max(data.length - 1, 1);

    const masteredPts = data.map((d, i) => ({
      x: paddingL + i * xStep,
      y: paddingT + plotH - (d.mastered / maxY) * plotH,
    }));
    const progressedPts = data.map((d, i) => ({
      x: paddingL + i * xStep,
      y: paddingT + plotH - (d.progressed / maxY) * plotH,
    }));

    const gridCount = 4;
    const gridLines = Array.from({ length: gridCount }, (_, i) => {
      const val = Math.round((maxY / gridCount) * (i + 1));
      const y = paddingT + plotH - (val / maxY) * plotH;
      return { y, label: String(val) };
    });

    const showEveryOther = data.length >= 8;
    const xLabels = data.map((d, i) => ({
      x: paddingL + i * xStep,
      label: shortDate(d.week),
      show: !showEveryOther || i % 2 === 0 || i === data.length - 1,
    }));

    // Area fill path under mastered line
    const linePath = cubicPath(masteredPts);
    const lastPt = masteredPts[masteredPts.length - 1];
    const firstPt = masteredPts[0];
    const areaPath = `${linePath} L ${lastPt.x} ${paddingT + plotH} L ${firstPt.x} ${paddingT + plotH} Z`;

    return { masteredPts, progressedPts, maxY, gridLines, xLabels, areaPath };
  }, [data, plotW, plotH]);

  if (data.length < 2) {
    return (
      <div className="flex items-center justify-center py-10 text-sm text-(--color-text-tertiary)">
        Mastery data will appear after your first full week.
      </div>
    );
  }

  const xStep = plotW / Math.max(data.length - 1, 1);

  return (
    <div ref={containerRef} className="relative w-full overflow-x-auto">
      <svg viewBox={`0 0 ${chartW} ${chartH}`} className="w-full" style={{ minWidth: 400 }}>
        {/* Grid lines */}
        {gridLines.map((gl) => (
          <g key={gl.label}>
            <line x1={paddingL} y1={gl.y} x2={chartW - paddingR} y2={gl.y}
              stroke="var(--color-border)" strokeWidth={1} strokeDasharray="3 3" />
            <text x={paddingL - 6} y={gl.y + 3} textAnchor="end" fill="var(--color-text-tertiary)" fontSize={10}>
              {gl.label}
            </text>
          </g>
        ))}

        {/* Baseline */}
        <line x1={paddingL} y1={paddingT + plotH} x2={chartW - paddingR} y2={paddingT + plotH}
          stroke="var(--color-border)" strokeWidth={1} />

        {/* X labels */}
        {xLabels.map((xl, i) => xl.show && (
          <text key={i} x={xl.x} y={chartH - 6} textAnchor="middle" fill="var(--color-text-tertiary)" fontSize={10}>
            {xl.label}
          </text>
        ))}

        {/* Area fill under mastered line */}
        <path d={areaPath} fill="var(--color-success)" opacity={0.06} />

        {/* Progressed line (dashed, behind) */}
        <path d={cubicPath(progressedPts)} fill="none" stroke="var(--color-accent)" strokeWidth={1.5} strokeDasharray="4 3" />

        {/* Mastered line */}
        <path d={cubicPath(masteredPts)} fill="none" stroke="var(--color-success)" strokeWidth={2} />

        {/* Data points */}
        {masteredPts.map((pt, i) => (
          <circle key={`m${i}`} cx={pt.x} cy={pt.y} r={hoverIdx === i ? 5 : 3}
            fill="var(--color-success)" stroke="var(--color-surface)" strokeWidth={1.5}
            style={{ transition: "r 0.15s" }} />
        ))}
        {progressedPts.map((pt, i) => (
          <circle key={`p${i}`} cx={pt.x} cy={pt.y} r={hoverIdx === i ? 4 : 2.5}
            fill="var(--color-accent)" stroke="var(--color-surface)" strokeWidth={1.5}
            style={{ transition: "r 0.15s" }} />
        ))}

        {/* Hover zones */}
        {data.map((_, i) => (
          <rect key={i} x={paddingL + i * xStep - xStep / 2} y={paddingT} width={xStep} height={plotH}
            fill="transparent"
            onMouseEnter={() => setHoverIdx(i)}
            onMouseLeave={() => setHoverIdx(null)}
          />
        ))}

        {/* Hover line */}
        {hoverIdx !== null && (
          <line
            x1={paddingL + hoverIdx * xStep}
            y1={paddingT}
            x2={paddingL + hoverIdx * xStep}
            y2={paddingT + plotH}
            stroke="var(--color-text-tertiary)" strokeWidth={1} strokeDasharray="2 2" opacity={0.5}
          />
        )}
      </svg>

      {/* Tooltip */}
      {hoverIdx !== null && data[hoverIdx] && (
        <div
          className="absolute bg-(--color-surface) border border-(--color-border) rounded-[10px] shadow-lg px-3 py-2 text-xs pointer-events-none z-10"
          style={{
            left: `${((paddingL + hoverIdx * xStep) / chartW) * 100}%`,
            top: 8,
            transform: "translateX(-50%)",
          }}
        >
          <div className="font-medium text-(--color-text) mb-0.5">Week of {shortDate(data[hoverIdx].week)}</div>
          <div className="text-(--color-success)">{data[hoverIdx].mastered} mastered</div>
          <div className="text-(--color-accent)">{data[hoverIdx].progressed} progressing</div>
          <div className="text-(--color-text-tertiary)">{data[hoverIdx].total_minutes}m total</div>
        </div>
      )}
    </div>
  );
}
