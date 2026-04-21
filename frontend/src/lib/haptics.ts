/**
 * Haptic feedback — delegates to Capacitor native haptics when available,
 * falls back to web navigator.vibrate.
 *
 * Re-exports from the native bridge so existing imports continue to work.
 */
export { haptic } from "./native";
export type { } from "./native";
