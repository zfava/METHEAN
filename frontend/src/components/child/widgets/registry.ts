/**
 * Widget registry: maps a widget type string to its component.
 *
 * To add a widget: write the component, then add one line here.
 * Unknown types resolve to null so the host can degrade gracefully
 * on a node that declares a widget this client build does not have.
 */

import CountingObjects from "./CountingObjects";
import NumberLine from "./NumberLine";
import type { MiniWidget } from "./types";

const WIDGET_REGISTRY: Record<string, MiniWidget> = {
  counting_objects: CountingObjects,
  number_line: NumberLine,
};

export function getWidget(type: string): MiniWidget | null {
  return WIDGET_REGISTRY[type] ?? null;
}
