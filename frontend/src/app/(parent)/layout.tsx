"use client";

import { useState, useEffect, useRef } from "react";
import { usePathname } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import PageTransition from "@/components/PageTransition";
import KeyboardShortcuts from "@/components/KeyboardShortcuts";
import { ChildProvider } from "@/lib/ChildContext";
import { useMobile } from "@/lib/useMobile";
import MobileHeader from "@/components/MobileHeader";
import BottomTabBar from "@/components/BottomTabBar";
import MobileNavSheet from "@/components/MobileNavSheet";
import BetaFeedbackButton from "@/components/BetaFeedbackButton";

function ParentLayoutInner({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isMobile = useMobile();
  const [navSheetOpen, setNavSheetOpen] = useState(false);
  const mainRef = useRef<HTMLElement>(null);
  const scrollPositions = useRef<Record<string, number>>({});

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
        <PageTransition>{children}</PageTransition>
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
