"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useCallback, useState } from "react";

import { childSession, ApiError } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import { useMotion } from "@/lib/motion/MotionContext";
import { MOTION_EASINGS } from "@/lib/motion/tokens";
import { MotionButton } from "@/components/child/motion";

const PIN_MIN = 4;
const PIN_MAX = 8;
const MAX_PIN_FAILURES = 5;

const PAD_KEYS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "back", "0", "go"] as const;

/**
 * Kid-friendly gate for leaving kid mode. A parent taps the door
 * button, types their PIN on a big tactile pad, and the session is
 * restored to parent scope server-side. Wrong PIN shakes (same
 * physics as PracticeView's wrong-answer card). After 5 failures (or
 * when the server locks the PIN path) the gate switches to the
 * parent-password fallback.
 */
export default function ExitGate({
  open,
  onClose,
  hasPin = true,
}: {
  open: boolean;
  onClose: () => void;
  hasPin?: boolean;
}) {
  const { reduceMotion, speed } = useMotion();
  const { refreshKidMode } = useChild();
  const [pin, setPin] = useState("");
  const [password, setPassword] = useState("");
  const [failures, setFailures] = useState(0);
  const [shaking, setShaking] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [passwordMode, setPasswordMode] = useState(!hasPin);

  const leave = useCallback(() => {
    refreshKidMode();
    window.location.href = "/dashboard";
  }, [refreshKidMode]);

  const fail = useCallback(() => {
    setShaking(true);
    setTimeout(() => setShaking(false), 400);
    setPin("");
    setFailures((f) => {
      const next = f + 1;
      if (next >= MAX_PIN_FAILURES) setPasswordMode(true);
      return next;
    });
  }, []);

  async function submit(secret: { pin?: string; password?: string }) {
    setBusy(true);
    setError("");
    try {
      await childSession.exit(secret);
      leave();
    } catch (err) {
      if (err instanceof ApiError && (err.detail === "pin_locked_use_password" || err.detail === "pin_not_set")) {
        setPasswordMode(true);
        setPin("");
      } else if (secret.pin !== undefined) {
        fail();
      } else {
        setError("That password didn't work. Try again.");
        setPassword("");
      }
    } finally {
      setBusy(false);
    }
  }

  function pressKey(key: (typeof PAD_KEYS)[number]) {
    if (busy) return;
    if (key === "back") {
      setPin((p) => p.slice(0, -1));
    } else if (key === "go") {
      if (pin.length >= PIN_MIN) submit({ pin });
    } else if (pin.length < PIN_MAX) {
      setPin((p) => p + key);
    }
  }

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm"
          initial={reduceMotion ? false : { opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={reduceMotion ? undefined : { opacity: 0 }}
          role="dialog"
          aria-modal="true"
          aria-label="Exit kid mode"
        >
          <motion.div
            className="bg-(--color-surface) border border-(--color-border) rounded-2xl p-6 w-[320px] max-w-[90vw] text-center shadow-xl"
            animate={
              reduceMotion || !shaking
                ? { x: 0 }
                : { x: [0, -6, 5, -4, 3, 0] }
            }
            transition={
              reduceMotion || !shaking
                ? undefined
                : { duration: 0.35 / speed, ease: MOTION_EASINGS.composed }
            }
          >
            <p className="text-base font-semibold text-(--color-text) mb-1">For grown-ups</p>

            {!passwordMode ? (
              <>
                <p className="text-xs text-(--color-text-secondary) mb-4">
                  Type the parent PIN to leave kid mode.
                </p>
                <div className="flex justify-center gap-2 mb-4 min-h-[16px]" aria-label="PIN entry">
                  {Array.from({ length: Math.max(pin.length, PIN_MIN) }).map((_, i) => (
                    <span
                      key={i}
                      className={`w-3 h-3 rounded-full border border-(--color-border-strong) ${
                        i < pin.length ? "bg-(--color-accent)" : "bg-transparent"
                      }`}
                    />
                  ))}
                </div>
                <div className="grid grid-cols-3 gap-2 mb-3">
                  {PAD_KEYS.map((key) => (
                    <MotionButton
                      key={key}
                      variant={key === "go" ? "primary" : "ghost"}
                      size="lg"
                      onPress={() => pressKey(key)}
                      disabled={busy || (key === "go" && pin.length < PIN_MIN)}
                      aria-label={key === "back" ? "Delete digit" : key === "go" ? "Unlock" : `Digit ${key}`}
                      className="min-h-[52px] text-lg font-semibold"
                    >
                      {key === "back" ? "⌫" : key === "go" ? "✓" : key}
                    </MotionButton>
                  ))}
                </div>
                {failures > 0 && failures < MAX_PIN_FAILURES && (
                  <p className="text-xs text-(--color-danger)">That PIN didn't work. Try again.</p>
                )}
              </>
            ) : (
              <>
                <p className="text-xs text-(--color-text-secondary) mb-4">
                  {failures >= MAX_PIN_FAILURES
                    ? "Ask your parent to type their password."
                    : "Type the parent password to leave kid mode."}
                </p>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && password) submit({ password });
                  }}
                  placeholder="Parent password"
                  autoFocus
                  className="w-full px-3 py-2 text-sm border border-(--color-border-strong) rounded-[10px] bg-(--color-surface) text-(--color-text) mb-3"
                />
                {error && <p className="text-xs text-(--color-danger) mb-2">{error}</p>}
                <MotionButton
                  variant="primary"
                  size="md"
                  onPress={() => password && submit({ password })}
                  disabled={busy || !password}
                  className="w-full"
                >
                  Unlock
                </MotionButton>
              </>
            )}

            <button
              onClick={onClose}
              className="mt-4 text-xs text-(--color-text-tertiary) hover:text-(--color-text) press-scale"
            >
              Back to learning
            </button>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
