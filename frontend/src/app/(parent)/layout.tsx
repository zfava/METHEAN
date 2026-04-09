"use client";

import { useState, useEffect } from "react";
import { usePathname } from "next/navigation";
import Sidebar from "@/components/Sidebar";
import { ChildProvider, useChild } from "@/lib/ChildContext";
import { MetheanLogo } from "@/components/Brand";

function MobileTopBar({ onMenuOpen }: { onMenuOpen: () => void }) {
  const { children, selectedChild, setSelectedChild } = useChild();

  return (
    <header className="fixed top-0 left-0 right-0 h-14 bg-(--color-surface) border-b border-(--color-border) z-40 flex items-center justify-between px-4 md:hidden">
      {/* Logo */}
      <MetheanLogo markSize={22} wordmarkHeight={11} color="var(--color-brand-navy, #0F1B2D)" gap={8} />

      {/* Child selector (compact) */}
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

      {/* Hamburger */}
      <button onClick={onMenuOpen} className="p-2 text-(--color-text) hover:text-(--color-text-secondary) transition-colors">
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

  // Close sidebar on route change
  useEffect(() => {
    setSidebarOpen(false);
  }, [pathname]);

  return (
    <div className="flex min-h-screen bg-(--color-page)">
      {/* Desktop sidebar */}
      <div className="hidden md:block">
        <Sidebar />
      </div>

      {/* Mobile top bar */}
      <MobileTopBar onMenuOpen={() => setSidebarOpen(true)} />

      {/* Mobile sidebar drawer */}
      {sidebarOpen && (
        <Sidebar mobile onClose={() => setSidebarOpen(false)} />
      )}

      {/* Main content: pt-14 on mobile for fixed top bar */}
      <main className="flex-1 px-4 py-4 md:px-8 md:py-6 pt-18 md:pt-6 overflow-y-auto overflow-x-hidden min-h-screen">
        {children}
      </main>
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
