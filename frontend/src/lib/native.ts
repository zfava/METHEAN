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

// ── Push Notifications ──

let _pushToken: string | null = null;

export async function registerPushNotifications(): Promise<string | null> {
  if (!isNative()) return null;
  try {
    const { PushNotifications } = await import("@capacitor/push-notifications");

    const permission = await PushNotifications.requestPermissions();
    if (permission.receive !== "granted") return null;

    await PushNotifications.register();

    return new Promise((resolve) => {
      PushNotifications.addListener("registration", (token) => {
        _pushToken = token.value;

        // Send token to backend
        fetch("/api/v1/notifications/devices", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({ token: token.value, platform: getPlatform() }),
        }).catch(() => {});

        resolve(token.value);
      });

      PushNotifications.addListener("registrationError", () => {
        resolve(null);
      });

      // Handle foreground notifications
      PushNotifications.addListener("pushNotificationReceived", () => {
        // In-app notifications are handled by the polling system
      });

      // Handle notification tap
      PushNotifications.addListener("pushNotificationActionPerformed", (action) => {
        const data = action.notification.data;
        if (data?.url && typeof window !== "undefined") {
          window.location.href = data.url;
        }
      });
    });
  } catch {
    return null;
  }
}

export async function unregisterPush(): Promise<void> {
  if (!isNative() || !_pushToken) return;
  try {
    await fetch(`/api/v1/notifications/devices/${encodeURIComponent(_pushToken)}`, {
      method: "DELETE",
      credentials: "include",
    });
    _pushToken = null;
  } catch {}
}

// ── App Badge ──

export async function setAppBadge(count: number): Promise<void> {
  if (!isNative()) {
    // PWA badge API (limited browser support)
    try {
      if (count > 0) (navigator as any).setAppBadge?.(count);
      else (navigator as any).clearAppBadge?.();
    } catch {}
    return;
  }
  try {
    const { Badge } = await import("@capawesome/capacitor-badge");
    if (count > 0) await Badge.set({ count });
    else await Badge.clear();
  } catch {}
}

// ── Native Share ──

export async function nativeShare(
  title: string,
  text: string,
  url?: string,
): Promise<void> {
  if (!isNative()) {
    if (typeof navigator !== "undefined" && navigator.share) {
      await navigator.share({ title, text, url });
    }
    return;
  }
  try {
    const { Share } = await import("@capacitor/share");
    await Share.share({ title, text, url, dialogTitle: "Share from METHEAN" });
  } catch {}
}

// ── Biometric Authentication ──

export async function biometricAvailable(): Promise<boolean> {
  if (!isNative()) return false;
  try {
    const mod = await import("capacitor-native-biometric");
    const result = await mod.NativeBiometric.isAvailable();
    return result.isAvailable;
  } catch {
    return false;
  }
}

export async function biometricVerify(): Promise<boolean> {
  if (!isNative()) return false;
  try {
    const mod = await import("capacitor-native-biometric");
    await mod.NativeBiometric.verifyIdentity({
      reason: "Log in to METHEAN",
      title: "Authentication",
    });
    return true;
  } catch {
    return false;
  }
}

export async function biometricSaveCredentials(refreshToken: string): Promise<void> {
  if (!isNative()) return;
  try {
    const mod = await import("capacitor-native-biometric");
    await mod.NativeBiometric.setCredentials({
      server: "methean.app",
      username: "methean-user",
      password: refreshToken,
    });
  } catch {}
}

export async function biometricGetCredentials(): Promise<string | null> {
  if (!isNative()) return null;
  try {
    const mod = await import("capacitor-native-biometric");
    const creds = await mod.NativeBiometric.getCredentials({ server: "methean.app" });
    return creds.password || null;
  } catch {
    return null;
  }
}
