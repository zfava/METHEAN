"use client";

/**
 * Cross-platform microphone permission helpers.
 *
 * Safari (especially mobile) doesn't reliably support
 * ``navigator.permissions.query({ name: "microphone" })``; the
 * fallback path probes via ``getUserMedia`` directly and inspects
 * the rejection error to classify the state.
 */

export type PermissionState = "granted" | "denied" | "prompt" | "unsupported";

export async function checkMicPermission(): Promise<PermissionState> {
  if (typeof navigator === "undefined" || !navigator.mediaDevices?.getUserMedia) {
    return "unsupported";
  }
  // Prefer the explicit Permissions API where available.
  const perms = (
    navigator as unknown as {
      permissions?: { query: (descriptor: { name: string }) => Promise<PermissionStatus> };
    }
  ).permissions;
  if (perms) {
    try {
      const status = await perms.query({ name: "microphone" });
      const s = status.state as PermissionState;
      if (s === "granted" || s === "denied" || s === "prompt") return s;
    } catch {
      // Fall through to getUserMedia probe.
    }
  }
  return "prompt";
}

export async function requestMicPermission(): Promise<PermissionState> {
  if (typeof navigator === "undefined" || !navigator.mediaDevices?.getUserMedia) {
    return "unsupported";
  }
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    // Immediately release; the recorder opens its own stream when the
    // kid actually starts recording.
    for (const track of stream.getTracks()) track.stop();
    return "granted";
  } catch (err) {
    const name = (err as { name?: string } | null)?.name ?? "";
    if (name === "NotAllowedError" || name === "SecurityError") return "denied";
    if (name === "NotFoundError" || name === "OverconstrainedError") return "unsupported";
    return "denied";
  }
}
