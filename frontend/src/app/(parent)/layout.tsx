"use client";

import { useState, useEffect, useRef } from "react";
import { usePathname } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import PageTransition from "@/components/PageTransition";
import KeyboardShortcuts from "@/components/KeyboardShortcuts";
import { ChildProvider, readKidModeCookie } from "@/lib/ChildContext";
import { useMobile } from "@/lib/useMobile";
import MobileHeader from "@/components/MobileHeader";
import BottomTabBar from "@/components/BottomTabBar";
import MobileNavSheet from "@/components/MobileNavSheet";
import BetaFeedbackButton from "@/components/BetaFeedbackButton";
import SubscriptionGate from "@/components/billing/SubscriptionGate";
import DunningBanner from "@/components/billing/DunningBanner";
import VerifyEmailGate from "@/components/VerifyEmailGate";
import { householdDeletion } from "@/lib/api";

/**
 * Banner shown while a household deletion is pending: states the purge
 * date and offers restore (password re-prompt, server re-authenticates).
 */
function DeletionPendingBanner() {
  const [purgeAfter, setPurgeAfter] = useState<string | null>(null);
  const [password, setPassword] = useState("");
  const [restoring, setRestoring] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    householdDeletion
      .status()
      .then((s) => setPurgeAfter(s.pending ? s.purge_after : null))
      .catch(() => {});
  }, []);

  if (!purgeAfter) return null;
  const dateStr = new Date(purgeAfter).toLocaleDateString(undefined, {
    year: "numeric", month: "long", day: "numeric",
  });

  return (
    <div className="bg-(--color-danger) text-white px-4 py-3 flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4">
      <p className="text-sm flex-1">
        This household is scheduled for permanent deletion on <strong>{dateStr}</strong>.
        Everything will be erased: learning records, documents, and your subscription.
      </p>
      <div className="flex items-center gap-2">
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password to restore"
          className="px-2 py-1.5 text-sm rounded-[8px] text-(--color-text) bg-white/95 border-0"
        />
        <button
          disabled={!password || restoring}
          onClick={async () => {
            setRestoring(true);
            setError("");
            try {
              await householdDeletion.restore(password);
              setPurgeAfter(null);
            } catch {
              setError("That password didn't work.");
            } finally {
              setRestoring(false);
            }
          }}
          className="px-3 py-1.5 text-sm font-semibold rounded-[8px] bg-white text-(--color-danger) disabled:opacity-50"
        >
          Restore
        </button>
      </div>
      {error && <p className="text-xs text-white/90">{error}</p>}
    </div>
  );
}

function ParentLayoutInner({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isMobile = useMobile();
  const [navSheetOpen, setNavSheetOpen] = useState(false);
  const mainRef = useRef<HTMLElement>(null);
  const scrollPositions = useRef<Record<string, number>>({});

  // Kid mode lockout: while the session is child-scoped the parent
  // surface must not render. The server already rejects every parent
  // API call with 403 (the cookie carries a child-scoped token), so
  // this mirrors the unauthenticated redirect in /child/layout.tsx
  // and routes back to the kid surface. Exit goes through the PIN
  // gate on /child, never through navigation.
  useEffect(() => {
    if (typeof window !== "undefined" && readKidModeCookie()) {
      window.location.replace("/child");
    }
  }, [pathname]);

  // Close nav sheet on route change
  useEffect(() => { setNavSheetOpen(false); }, [pathname]);

  // Scroll position memory
  useEffect(() => {
    const main = mainRef.current;
    if (!main) return;

    const saveScroll = () => {
      scrollPositions.current[pathname] = main.scrollTop;
    };
    main.addEventListener("scroll", saveScroll, { passive: true });

    const saved = scrollPositions.current[pathname];
    if (saved) {
      requestAnimationFrame(() => main.scrollTo(0, saved));
    } else {
      main.scrollTo(0, 0);
    }

    return () => main.removeEventListener("scroll", saveScroll);
  }, [pathname]);

  return (
    <div className="flex min-h-screen bg-(--color-page)">
      {/* Desktop sidebar — completely unchanged */}
      <div className="hidden md:block">
        <Sidebar />
      </div>

      {/* Mobile: header + bottom tab bar + nav sheet */}
      {isMobile && (
        <>
          <MobileHeader />
          <BottomTabBar onMorePress={() => setNavSheetOpen(true)} />
          <MobileNavSheet open={navSheetOpen} onClose={() => setNavSheetOpen(false)} />
        </>
      )}

      <main
        ref={mainRef}
        className="flex-1 overflow-y-auto overflow-x-hidden min-h-screen"
        style={isMobile ? {
          paddingTop: "calc(48px + var(--safe-top) + 16px)",
          paddingBottom: "calc(56px + var(--safe-bottom) + 16px)",
          paddingLeft: 16,
          paddingRight: 16,
        } : {
          paddingTop: 24,
          paddingBottom: 24,
          paddingLeft: 32,
          paddingRight: 32,
        }}
      >
        <DeletionPendingBanner />
        <DunningBanner />
        <PageTransition>
          <VerifyEmailGate>
            <SubscriptionGate>{children}</SubscriptionGate>
          </VerifyEmailGate>
        </PageTransition>
      </main>

      <BetaFeedbackButton />
      <KeyboardShortcuts />
    </div>
  );
}

export default function ParentLayout({ children }: { children: React.ReactNode }) {
  return (
    <ChildProvider>
      <ParentLayoutInner>{children}</ParentLayoutInner>
    </ChildProvider>
  );
}
