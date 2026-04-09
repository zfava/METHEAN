"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { usePathname } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import PageTransition from "@/components/PageTransition";
import KeyboardShortcuts from "@/components/KeyboardShortcuts";
import { ChildProvider, useChild } from "@/lib/ChildContext";
import { MetheanLogo } from "@/components/Brand";

function MobileTopBar({ onMenuOpen }: { onMenuOpen: () => void }) {
  const { children, selectedChild, setSelectedChild } = useChild();

  return (
    <header className="fixed top-0 left-0 right-0 h-14 bg-(--color-surface) border-b border-(--color-border) z-40 flex items-center justify-between px-4 md:hidden">
      <MetheanLogo markSize={22} wordmarkHeight={11} color="var(--color-brand-navy, #0F1B2D)" gap={8} />
      {children.length > 0 && (
        <select
          value={selectedChild?.id || ""}
          onChange={(e) => { const c = children.find((ch) => ch.id === e.target.value); if (c) setSelectedChild(c); }}
          className="text-sm text-(--color-text) bg-transparent border-none focus:outline-none font-medium px-2 py-1 max-w-[140px] truncate"
        >
          {children.map((c) => (
            <option key={c.id} value={c.id}>{c.first_name}</option>
          ))}
        </select>
      )}
      <button onClick={onMenuOpen} className="p-2 text-(--color-text) hover:text-(--color-text-secondary) transition-colors" aria-label="Open menu">
        <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
    </header>
  );
}

function ParentLayoutInner({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const pathname = usePathname();
  const mainRef = useRef<HTMLElement>(null);
  const scrollPositions = useRef<Record<string, number>>({});

  // Close sidebar on route change
  useEffect(() => {
    setSidebarOpen(false);
  }, [pathname]);

  // Scroll position memory
  useEffect(() => {
    const main = mainRef.current;
    if (!main) return;

    const saveScroll = () => {
      scrollPositions.current[pathname] = main.scrollTop;
    };
    main.addEventListener("scroll", saveScroll, { passive: true });

    // Restore saved position for this route
    const saved = scrollPositions.current[pathname];
    if (saved) {
      requestAnimationFrame(() => main.scrollTo(0, saved));
    } else {
      main.scrollTo(0, 0);
    }

    return () => main.removeEventListener("scroll", saveScroll);
  }, [pathname]);

  // Global Escape handler — close sidebar drawer
  const handleEscape = useCallback((e: KeyboardEvent) => {
    if (e.key === "Escape" && sidebarOpen) {
      setSidebarOpen(false);
    }
  }, [sidebarOpen]);

  useEffect(() => {
    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, [handleEscape]);

  return (
    <div className="flex min-h-screen bg-(--color-page)">
      <div className="hidden md:block">
        <Sidebar />
      </div>

      <MobileTopBar onMenuOpen={() => setSidebarOpen(true)} />

      {sidebarOpen && (
        <Sidebar mobile onClose={() => setSidebarOpen(false)} />
      )}

      <main
        ref={mainRef}
        className="flex-1 px-4 py-4 md:px-8 md:py-6 pt-18 md:pt-6 overflow-y-auto overflow-x-hidden min-h-screen"
      >
        <PageTransition>{children}</PageTransition>
      </main>

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
