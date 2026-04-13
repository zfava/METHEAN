/**
 * Unified native bridge for Capacitor.
 *
 * All imports are dynamic so this module works in both web and native contexts.
 * The `isNative` check gates native-only behavior — web falls back gracefully.
 */

let _isNative: boolean | null = null;

/** Returns true when running inside a Capacitor native shell. */
export function isNative(): boolean {
  if (_isNative !== null) return _isNative;
  try {
    // Capacitor injects this on the window object in native shells
    _isNative = typeof window !== "undefined" && !!(window as any).Capacitor?.isNativePlatform?.();
  } catch {
    _isNative = false;
  }
  return _isNative;
}

export function getPlatform(): "ios" | "android" | "web" {
  try {
    if (typeof window !== "undefined" && (window as any).Capacitor) {
      return (window as any).Capacitor.getPlatform?.() || "web";
    }
  } catch {}
  return "web";
}

export const isIOS = () => getPlatform() === "ios";
export const isAndroid = () => getPlatform() === "android";

// ── Haptics ──

type HapticStyle = "light" | "medium" | "heavy" | "success" | "error";

const webPatterns: Record<HapticStyle, number | number[]> = {
  light: 10,
  medium: 20,
  heavy: 30,
  success: [10, 50, 10],
  error: [30, 50, 30, 50, 30],
};

export async function haptic(style: HapticStyle = "light"): Promise<void> {
  if (isNative()) {
    try {
      const { Haptics, ImpactStyle, NotificationType } = await import("@capacitor/haptics");
      switch (style) {
        case "light": return void await Haptics.impact({ style: ImpactStyle.Light });
        case "medium": return void await Haptics.impact({ style: ImpactStyle.Medium });
        case "heavy": return void await Haptics.impact({ style: ImpactStyle.Heavy });
        case "success": return void await Haptics.notification({ type: NotificationType.Success });
        case "error": return void await Haptics.notification({ type: NotificationType.Error });
      }
    } catch {}
    return;
  }
  // Web fallback
  if (typeof navigator !== "undefined" && navigator.vibrate) {
    navigator.vibrate(webPatterns[style]);
  }
}

// ── Status Bar ──

export async function configureStatusBar(): Promise<void> {
  if (!isNative()) return;
  try {
    const { StatusBar, Style } = await import("@capacitor/status-bar");
    await StatusBar.setStyle({ style: Style.Dark });
    await StatusBar.setBackgroundColor({ color: "#0F1B2D" });
  } catch {}
}

// ── Splash Screen ──

export async function hideSplash(): Promise<void> {
  if (!isNative()) return;
  try {
    const { SplashScreen } = await import("@capacitor/splash-screen");
    await SplashScreen.hide({ fadeOutDuration: 300 });
  } catch {}
}

// ── Keyboard ──

export async function configureKeyboard(): Promise<void> {
  if (!isNative()) return;
  try {
    await import("@capacitor/keyboard");
    // Configuration is handled in capacitor.config.ts
  } catch {}
}

// ── Network ──

export async function getNetworkStatus(): Promise<boolean> {
  if (!isNative()) return typeof navigator !== "undefined" ? navigator.onLine : true;
  try {
    const { Network } = await import("@capacitor/network");
    const status = await Network.getStatus();
    return status.connected;
  } catch {
    return true;
  }
}
