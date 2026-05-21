"use client";

/**
 * WidgetHost renders one declared widget.
 *
 * It resolves the component from the registry (rendering nothing for
 * an unknown type), isolates render failures behind an error boundary
 * (a misbehaving widget cannot crash the lesson), shows the optional
 * prompt, computes reduced-motion once, and fires the existing
 * "correct" sound cue when the child completes the widget.
 */

import { Component, useCallback, useEffect, useState, type ReactNode } from "react";
import { useSoundCue } from "@/lib/useSoundCue";
import { getWidget } from "./registry";
import type { WidgetSpec } from "./types";

class WidgetErrorBoundary extends Component<{ children: ReactNode }, { hasError: boolean }> {
  constructor(props: { children: ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) return null;
    return this.props.children;
  }
}

export function WidgetHost({ spec }: { spec: WidgetSpec }) {
  const playCue = useSoundCue();
  const [reducedMotion, setReducedMotion] = useState(false);

  useEffect(() => {
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setReducedMotion(mq.matches);
    const handler = (e: MediaQueryListEvent) => setReducedMotion(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);

  const handleComplete = useCallback(() => {
    playCue("correct");
  }, [playCue]);

  const Widget = getWidget(spec.widget);
  // Forward-compatible: a node may declare a type this build lacks.
  if (!Widget) return null;

  return (
    <WidgetErrorBoundary>
      <div className="my-4 rounded-2xl border border-(--color-border) bg-(--color-surface) p-5 shadow-[var(--shadow-card)]">
        {spec.prompt && <p className="mb-4 text-base text-(--color-text)">{spec.prompt}</p>}
        <Widget
          params={spec.params}
          target={spec.target}
          reducedMotion={reducedMotion}
          onComplete={handleComplete}
        />
      </div>
    </WidgetErrorBoundary>
  );
}

export default WidgetHost;
