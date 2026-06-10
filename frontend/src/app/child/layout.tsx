"use client";

import { useEffect, useState, type ReactNode } from "react";

import { PersonalizationProvider } from "@/lib/PersonalizationProvider";
import { VibeProvider } from "@/lib/VibeProvider";
import { ChildProvider } from "@/lib/ChildContext";
import { MotionProvider } from "@/lib/motion/MotionContext";
import { CelebrationProvider } from "@/lib/celebration/CelebrationDirector";
import { CompanionProvider } from "@/components/companion/state";
import { useSelectedChild } from "@/lib/useSelectedChild";
import { auth } from "@/lib/api";
import ExitGate from "@/components/child/ExitGate";

// The /child surface is auth-gated and depends on per-household
// state at runtime. Skipping static generation also keeps the
// PersonalizationProvider out of the build's pre-render path,
// where the auth lookup necessarily fails and there is no real
// child to seed the context with.
export const dynamic = "force-dynamic";

/**
 * Wrapping layout for every route under /child.
 *
 * Resolves the active child once (shared with the page below via
 * `useSelectedChild`) and stands up the personalization providers so
 * the entire subtree picks up the vibe tokens and companion identity.
 * The page itself can still call `useSelectedChild` to render the
 * multi-child switcher; the hook is keyed by an internal `useRef`
 * guard so the auth/list fetch only fires once per mount.
 */
export default function ChildLayout({ children }: { children: ReactNode }) {
  const { selectedId, unauthenticated } = useSelectedChild();

  // Send unauthenticated users out of the child surface entirely.
  // Centralising the redirect here keeps every nested route aligned
  // without each one re-checking auth.
  useEffect(() => {
    if (unauthenticated && typeof window !== "undefined") {
      window.location.href = "/auth";
    }
  }, [unauthenticated]);

  // Always wrap with the providers, even before a child is picked.
  // The PersonalizationProvider treats an empty childId as "no
  // fetch yet" and serves safe defaults, which lets the wrapped
  // page render its own skeleton without crashing on
  // `usePersonalization()`. The VibeProvider falls back to the calm
  // token bag when the library hasn't loaded, so the wrapper paints
  // with the design-system defaults during prerender.
  // ChildProvider is mounted here (rather than at root) because the
  // /child surface is the only place the MotionProvider needs to read
  // the active child's grade_level to derive the age-band default
  // motion intensity. PersonalizationProvider stays nested under it
  // unchanged.
  return (
    <ChildProvider>
      <PersonalizationProvider childId={selectedId}>
        <MotionProvider>
          <VibeProvider>
            <CelebrationProvider>
              <CompanionProvider>
                {children}
                <KidModeExit />
              </CompanionProvider>
            </CelebrationProvider>
          </VibeProvider>
        </MotionProvider>
      </PersonalizationProvider>
    </ChildProvider>
  );
}

/**
 * Always-available exit affordance for the whole /child surface.
 *
 * Lives in the layout (not the dashboard header) so a parent can
 * leave kid mode from every child route, including /child/welcome
 * where a brand-new learner lands before onboarding. The gate itself
 * verifies the parent PIN or password server-side; this button only
 * opens it.
 */
function KidModeExit() {
  const [open, setOpen] = useState(false);
  const [hasPin, setHasPin] = useState(true);

  // Choose PIN pad vs password upfront. /auth/me is allowlisted for
  // child-scoped tokens; on any failure keep the PIN-pad default and
  // let the server's pin_not_set response flip the gate to password.
  useEffect(() => {
    auth
      .me()
      .then((me) => setHasPin(Boolean(me.has_parent_pin)))
      .catch(() => {});
  }, []);

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        aria-label="Exit kid mode"
        title="Exit kid mode"
        className="fixed bottom-4 left-4 z-40 w-11 h-11 flex items-center justify-center rounded-full bg-(--color-surface)/80 backdrop-blur border border-(--color-border) text-(--color-text-tertiary) hover:text-(--color-text) shadow-sm press-scale"
      >
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9"
          />
        </svg>
      </button>
      <ExitGate open={open} onClose={() => setOpen(false)} hasPin={hasPin} />
    </>
  );
}
