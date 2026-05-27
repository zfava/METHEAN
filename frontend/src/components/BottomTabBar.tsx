"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { haptic } from "@/lib/haptics";
import { Compass, Home, Menu, User } from "@/lib/icons";
import { Icon } from "@/components/ui/Icon";

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
    icon: <Icon icon={Home} size={22} strokeWidth={1.75} />,
  },
  {
    key: "child",
    label: "Child",
    href: "/child",
    icon: <Icon icon={User} size={22} strokeWidth={1.75} />,
  },
  {
    key: "governance",
    label: "Govern",
    href: "/governance/queue",
    icon: <Icon icon={Compass} size={22} strokeWidth={1.75} />,
  },
  {
    key: "more",
    label: "More",
    icon: <Icon icon={Menu} size={22} strokeWidth={1.75} />,
  },
];

function isTabActive(key: string, pathname: string): boolean {
  switch (key) {
    case "dashboard": return pathname === "/dashboard";
    case "child": return pathname.startsWith("/child");
    case "governance": return pathname.startsWith("/governance");
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
              className="flex flex-col items-center justify-center flex-1 h-14 gap-0.5 min-h-[44px]"
              aria-label={tab.label}
              aria-selected={active}
            >
              {/* Icon sits inside a pill that fills with the accent
                  light when active — Copilot-style. The icon color
                  flips to gold on the active pill. */}
              <div
                className="flex items-center justify-center h-7 w-12 rounded-full transition-all duration-200"
                style={{
                  background: active ? "var(--color-accent-light)" : "transparent",
                  color: active ? "var(--color-brand-gold)" : "var(--color-text-tertiary)",
                  transform: active ? "scale(1.02)" : "scale(1)",
                }}
              >
                {tab.icon}
              </div>
              <span
                className="text-[10px] font-medium transition-colors"
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
