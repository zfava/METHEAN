"use client";

import { useEffect, type ReactNode } from "react";

import { PersonalizationProvider } from "@/lib/PersonalizationProvider";
import { VibeProvider } from "@/lib/VibeProvider";
import { useSelectedChild } from "@/lib/useSelectedChild";

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
  return (
    <PersonalizationProvider childId={selectedId}>
      <VibeProvider>{children}</VibeProvider>
    </PersonalizationProvider>
  );
}
