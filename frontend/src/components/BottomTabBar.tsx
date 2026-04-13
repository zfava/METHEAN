"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { haptic } from "@/lib/haptics";

interface Tab {
  key: string;
  label: string;
  href?: string;
  icon: React.ReactNode;
}

const TABS: Tab[] = [
  {
    key: "dashboard",
    label: "Home",
    href: "/dashboard",
    icon: (
      <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 12l8.954-8.955a1.126 1.126 0 011.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
      </svg>
    ),
  },
  {
    key: "learning",
    label: "Learning",
    href: "/plans",
    icon: (
      <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
      </svg>
    ),
  },
  {
    key: "governance",
    label: "Govern",
    href: "/governance",
    icon: (
      <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
      </svg>
    ),
  },
  {
    key: "intelligence",
    label: "Insights",
    href: "/inspection",
    icon: (
      <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z" />
      </svg>
    ),
  },
  {
    key: "more",
    label: "More",
    icon: (
      <svg width="22" height="22" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" />
      </svg>
    ),
  },
];

function isTabActive(key: string, pathname: string): boolean {
  switch (key) {
    case "dashboard": return pathname === "/dashboard";
    case "learning": return pathname.startsWith("/plans") || pathname.startsWith("/calendar") || pathname.startsWith("/maps") || pathname.startsWith("/assessment") || pathname.startsWith("/reading") || pathname.startsWith("/resources");
    case "governance": return pathname.startsWith("/governance");
    case "intelligence": return pathname.startsWith("/inspection") || pathname.startsWith("/intelligence") || pathname.startsWith("/calibration") || pathname.startsWith("/style-profile") || pathname.startsWith("/family-insights") || pathname.startsWith("/wellbeing");
    default: return false;
  }
}

export default function BottomTabBar({ onMorePress }: { onMorePress: () => void }) {
  const pathname = usePathname();
  const router = useRouter();
  const [visible, setVisible] = useState(true);
  const lastScroll = useRef(0);
  const ticking = useRef(false);

  // Auto-hide on scroll down, reappear on scroll up
  useEffect(() => {
    const main = document.querySelector("main");
    if (!main) return;

    const onScroll = () => {
      if (ticking.current) return;
      ticking.current = true;
      requestAnimationFrame(() => {
        const y = main.scrollTop;
        if (y > lastScroll.current + 8 && y > 56) {
          setVisible(false);
        } else if (y < lastScroll.current - 4) {
          setVisible(true);
        }
        lastScroll.current = y;
        ticking.current = false;
      });
    };

    main.addEventListener("scroll", onScroll, { passive: true });
    return () => main.removeEventListener("scroll", onScroll);
  }, []);

  // Always show on route change
  useEffect(() => { setVisible(true); }, [pathname]);

  const handleTab = useCallback((tab: Tab) => {
    haptic("light");
    if (tab.key === "more") {
      onMorePress();
    } else if (tab.href) {
      router.push(tab.href);
    }
  }, [router, onMorePress]);

  return (
    <nav
      data-no-select
      role="tablist"
      aria-label="Main navigation"
      className="fixed bottom-0 left-0 right-0 z-40 border-t border-(--color-border) md:hidden"
      style={{
        height: `calc(56px + var(--safe-bottom))`,
        paddingBottom: "var(--safe-bottom)",
        backdropFilter: "blur(20px)",
        WebkitBackdropFilter: "blur(20px)",
        background: "rgba(255,255,255,0.85)",
        transform: visible ? "translateY(0)" : "translateY(100%)",
        transition: "transform 0.2s cubic-bezier(0.25, 0.1, 0.25, 1)",
        willChange: "transform",
      }}
    >
      <div className="flex items-center justify-around h-14">
        {TABS.map((tab) => {
          const active = isTabActive(tab.key, pathname);
          return (
            <button
              key={tab.key}
              role="tab"
              onClick={() => handleTab(tab)}
              className="flex flex-col items-center justify-center flex-1 h-14 gap-0.5"
              aria-label={tab.label}
              aria-selected={active}
            >
              <div
                style={{
                  color: active ? "var(--color-brand-gold)" : "var(--color-text-tertiary)",
                  transform: active ? "scale(1.05)" : "scale(1)",
                  transition: "color 0.15s, transform 0.15s",
                }}
              >
                {tab.icon}
              </div>
              <span
                className="text-[10px] font-medium"
                style={{ color: active ? "var(--color-brand-gold)" : "var(--color-text-tertiary)" }}
              >
                {tab.label}
              </span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}
