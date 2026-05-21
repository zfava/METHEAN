/**
 * Interactive widget contract.
 *
 * A widget is a self-contained React component that a child touches
 * to learn. Adding a new widget means writing one component that
 * accepts MiniWidgetProps and adding one line to the registry.
 * Nothing else changes.
 */

import type { ComponentType } from "react";

/** A widget declaration as it arrives from node content. */
export interface WidgetSpec {
  id: string;
  widget: string;
  params: Record<string, unknown>;
  prompt?: string;
  target?: unknown;
}

/** Props every widget component receives. */
export interface MiniWidgetProps {
  params: Record<string, unknown>;
  target?: unknown;
  /** Reports the widget's current value as the child interacts. */
  onValueChange?: (value: unknown) => void;
  /** Fired once when the child reaches the target. */
  onComplete?: () => void;
  /** Passed down from the host; widgets must honor it. */
  reducedMotion: boolean;
}

/** A widget component: a React component accepting MiniWidgetProps. */
export type MiniWidget = ComponentType<MiniWidgetProps>;
