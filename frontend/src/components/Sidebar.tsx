"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState, useCallback, useRef } from "react";
import { auth, governance, notifications as notificationsApi, type User } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import { cn } from "@/lib/cn";
import { MetheanLogo } from "@/components/Brand";

// ── Nav group definitions ──
const NAV_GROUPS = [
  {
    key: "overview",
    label: "Overview",
    collapsible: false,
    items: [
      { href: "/dashboard", label: "Dashboard", exact: true },
      { href: "/family", label: "Family" },
      { href: "/compliance", label: "Compliance" },
    ],
  },
  {
    key: "curriculum",
    label: "Curriculum",
    collapsible: true,
    defaultExpanded: true,
    items: [
      { href: "/curriculum", label: "Curriculum", exact: true },
      { href: "/curriculum/year", label: "Year Plan" },
      { href: "/curriculum/scope", label: "Scope & Sequence" },
      { href: "/curriculum/history", label: "History" },
      { href: "/curriculum/editor", label: "Map Editor" },
      { href: "/curriculum/mapper", label: "Map Curriculum" },
    ],
  },
  {
    key: "learning",
    label: "Learning",
    collapsible: true,
    defaultExpanded: true,
    items: [
      { href: "/calendar", label: "Calendar" },
      { href: "/plans", label: "Weekly Plans", exact: true },
      { href: "/plans/vision", label: "Education Plan" },
      { href: "/maps", label: "Maps" },
      { href: "/assessment", label: "Assessment" },
      { href: "/reading", label: "Reading Log" },
      { href: "/resources", label: "Resources" },
    ],
  },
  {
    key: "intelligence",
    label: "Intelligence",
    collapsible: true,
    defaultExpanded: false,
    items: [
      { href: "/inspection", label: "AI Inspection" },
      { href: "/intelligence", label: "Learner Profile" },
      { href: "/calibration", label: "Evaluator Calibration" },
      { href: "/style-profile", label: "Learning Style" },
      { href: "/family-insights", label: "Family Insights" },
      { href: "/wellbeing", label: "Wellbeing" },
    ],
  },
  {
    key: "governance",
    label: "Governance",
    collapsible: true,
    defaultExpanded: false,
    items: [
      { href: "/governance", label: "Overview", exact: true },
      { href: "/governance/queue", label: "Approval Queue", badge: true },
      { href: "/governance/rules", label: "Rules" },
      { href: "/governance/philosophy", label: "Philosophy" },
      { href: "/governance/trace", label: "Decision Trace" },
      { href: "/governance/reports", label: "Reports" },
      { href: "/governance/overrides", label: "Overrides" },
      // Guardian-only: observers can't mutate the personalization
      // policy and the page hides itself for them, so the nav link
      // is gated here too to avoid a 403-shaped dead end.
      { href: "/governance/personalization", label: "Personalization", guardianOnly: true },
    ],
  },
];

function getActiveGroup(pathname: string): string | null {
  for (const group of NAV_GROUPS) {
    if (group.items.some((item) => item.exact ? pathname === item.href : pathname.startsWith(item.href))) {
      return group.key;
    }
  }
  return null;
}

export default function Sidebar({ mobile = false, onClose }: { mobile?: boolean; onClose?: () => void }) {
  const pathname = usePathname();
  const { children, selectedChild, setSelectedChild, loading } = useChild();
  const [pendingCount, setPendingCount] = useState(0);
  const [user, setUser] = useState<User | null>(null);
  const [unreadNotifs, setUnreadNotifs] = useState(0);
  const [showNotifs, setShowNotifs] = useState(false);
  const [notifList, setNotifList] = useState<any[]>([]);
  const [bellPulse, setBellPulse] = useState(false);
  const prevUnread = useRef(0);

  // For mobile slide-in animation
  const [entered, setEntered] = useState(false);
  useEffect(() => {
    if (mobile) requestAnimationFrame(() => requestAnimationFrame(() => setEntered(true)));
  }, [mobile]);

  // Collapsible group state
  const activeGroup = getActiveGroup(pathname);
  const [expanded, setExpanded] = useState<Record<string, boolean>>(() => {
    const initial: Record<string, boolean> = {};
    for (const g of NAV_GROUPS) {
      if (!g.collapsible) {
        initial[g.key] = true;
      } else if (mobile) {
        // Mobile: only expand the active group
        initial[g.key] = g.key === activeGroup;
      } else {
        initial[g.key] = g.defaultExpanded || g.key === activeGroup;
      }
    }
    return initial;
  });

  // Auto-expand group when pathname changes to an item inside it
  useEffect(() => {
    if (activeGroup && !expanded[activeGroup]) {
      setExpanded((prev) => ({ ...prev, [activeGroup]: true }));
    }
  }, [activeGroup]);

  function toggleGroup(key: string) {
    setExpanded((prev) => ({ ...prev, [key]: !prev[key] }));
  }

  const loadNotifications = useCallback(async () => {
    try {
      const data = await notificationsApi.list(false, 10);
      const items = Array.isArray(data) ? data : (data as any).items || [];
      setNotifList(items);
      setUnreadNotifs(items.filter((n: any) => !n.is_read).length);
    } catch {}
  }, []);

  useEffect(() => {
    if (unreadNotifs > prevUnread.current) {
      setBellPulse(true);
      setTimeout(() => setBellPulse(false), 1200);
    }
    prevUnread.current = unreadNotifs;
  }, [unreadNotifs]);

  useEffect(() => {
    governance.queue(1)
      .then((d) => setPendingCount(d.total || 0))
      .catch(() => {});
    auth.me().then(setUser).catch(() => {});
    loadNotifications();
    const interval = setInterval(loadNotifications, 60000);
    return () => clearInterval(interval);
  }, [loadNotifications]);

  function handleNav() {
    if (mobile && onClose) onClose();
  }

  function navItem(href: string, label: string, exact = false, badge = false) {
    const active = exact ? pathname === href : (pathname === href || pathname.startsWith(href + "/"));
    return (
      <Link key={href} href={href} onClick={handleNav}
        aria-current={active ? "page" : undefined}
        className={cn(
          "flex items-center justify-between px-4 py-[7px] text-[13px] rounded-r-lg ml-1 transition-colors duration-150",
          active
            ? "bg-(--color-sidebar-active) text-white font-medium border-l-2 border-(--color-accent)"
            : "text-(--color-text-sidebar) hover:text-white hover:bg-(--color-sidebar-hover) border-l-2 border-transparent",
        )}
      >
        {label}
        {badge && pendingCount > 0 && (
          <span className="bg-(--color-brand-gold) text-white text-[9px] font-bold px-1 py-0.5 rounded-full">{pendingCount}</span>
        )}
      </Link>
    );
  }

  const sidebarContent = (
    <aside className={cn(
      "bg-(--color-sidebar) flex flex-col shrink-0",
      mobile ? "w-[280px] h-full" : "w-[240px] min-h-screen"
    )}>
      <div className="px-5 pt-5 pb-4 flex items-center justify-between">
        <Link href="/dashboard" onClick={handleNav} className="block">
          <MetheanLogo markSize={28} wordmarkHeight={14} color="#C6A24E" gap={10} />
        </Link>
        <div className="flex items-center gap-2">
          <button onClick={() => setShowNotifs(!showNotifs)} className="relative p-1.5 text-white/40 hover:text-white/70 transition-colors">
            <svg className="w-4.5 h-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
            </svg>
            {unreadNotifs > 0 && (
              <span className={cn("absolute -top-0.5 -right-0.5 w-3.5 h-3.5 bg-(--color-brand-gold) text-white text-[8px] font-bold rounded-full flex items-center justify-center", bellPulse && "notif-new")}>{unreadNotifs}</span>
            )}
          </button>
          {mobile && (
            <button onClick={onClose} className="p-1.5 text-white/40 hover:text-white/70 transition-colors">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
      </div>
      {showNotifs && (
        <div className="mx-3 mb-3 p-3 rounded-[8px] bg-(--color-sidebar-hover) border border-white/5 max-h-60 overflow-y-auto">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] font-medium text-white/50">Notifications</span>
            {unreadNotifs > 0 && (
              <button onClick={() => { notificationsApi.markAllRead(); setUnreadNotifs(0); setNotifList(notifList.map(n => ({...n, is_read: true}))); }}
                className="text-[9px] text-(--color-brand-gold) hover:underline">Mark all read</button>
            )}
          </div>
          {notifList.length === 0 ? (
            <p className="text-[10px] text-white/30 text-center py-3">No notifications</p>
          ) : (
            <div className="space-y-1.5">
              {notifList.map((n: any) => (
                <div key={n.id} className={cn("px-2 py-1.5 rounded-[10px] text-[10px]", n.is_read ? "text-white/30" : "text-white/70 bg-white/5")}>
                  <div className="font-medium">{n.title}</div>
                  <div className="text-white/30 mt-0.5">{n.message?.slice(0, 60)}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {!loading && children.length > 0 && (
        <div className="px-4 pb-4">
          <select value={selectedChild?.id || ""}
            onChange={(e) => { const c = children.find((ch) => ch.id === e.target.value); if (c) setSelectedChild(c); }}
            className="w-full px-3 py-2 text-sm bg-(--color-sidebar-hover) text-white border border-white/10 rounded-[10px] focus:outline-none focus:ring-1 focus:ring-(--color-accent)">
            {children.map((c) => (
              <option key={c.id} value={c.id}>{c.first_name} {c.last_name || ""}</option>
            ))}
          </select>
        </div>
      )}

      <nav aria-label="Main navigation" className="flex-1 space-y-1 pb-4 overflow-y-auto">
        {NAV_GROUPS.map((group) => {
          const isExpanded = expanded[group.key] ?? true;
          const isActive = group.key === activeGroup;
          const showBadge = group.key === "governance" && pendingCount > 0;

          return (
            <div key={group.key}>
              {group.collapsible ? (
                <button
                  onClick={() => toggleGroup(group.key)}
                  className="w-full flex items-center justify-between px-5 py-1.5 group"
                >
                  <span className={cn(
                    "text-[11px] font-medium tracking-wider uppercase",
                    isActive ? "text-white/50" : "text-white/30"
                  )}>
                    {group.label}
                  </span>
                  <div className="flex items-center gap-1.5">
                    {showBadge && (
                      <span className="bg-(--color-brand-gold) text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full">{pendingCount}</span>
                    )}
                    <svg
                      className={cn(
                        "w-3 h-3 text-white/20 transition-transform duration-150",
                        isExpanded ? "rotate-90" : "rotate-0"
                      )}
                      fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </button>
              ) : (
                <div className="px-5 py-1.5">
                  <span className="text-[11px] font-medium text-white/30 tracking-wider uppercase">{group.label}</span>
                </div>
              )}

              {isExpanded && (
                <div className="mt-0.5 mb-2">
                  {group.items
                    .filter((item) => !(item as { guardianOnly?: boolean }).guardianOnly || (user && user.role !== "observer"))
                    .map((item) =>
                      navItem(item.href, item.label, item.exact, (item as any).badge),
                    )}
                </div>
              )}
            </div>
          );
        })}
      </nav>

      <div className="px-4 py-4 border-t border-white/5 space-y-2">
        {navItem("/billing", "Billing")}
        {navItem("/settings", "Settings", true)}
        <Link href="/child" onClick={handleNav} className="block px-1 py-1 text-xs text-white/25 hover:text-white/50 transition-colors duration-150">Child View</Link>
        {user && (
          <div className="flex items-center justify-between px-1">
            <div className="flex items-center gap-2">
              <div className="w-5 h-5 rounded-full bg-(--color-accent) text-white text-[9px] font-bold flex items-center justify-center">{user.display_name.charAt(0)}</div>
              <span className="text-[11px] text-white/30 truncate max-w-[120px]">{user.email}</span>
            </div>
            <button onClick={() => auth.logout().then(() => (window.location.href = "/auth"))}
              className="text-[11px] text-white/20 hover:text-white/50 transition-colors duration-150">Out</button>
          </div>
        )}
      </div>
    </aside>
  );

  if (!mobile) return sidebarContent;

  return (
    <div className="fixed inset-0 z-50">
      <div
        className="absolute inset-0 bg-black/40 transition-opacity duration-250"
        style={{ opacity: entered ? 1 : 0 }}
        onClick={onClose}
      />
      <div
        className="absolute top-0 left-0 h-full transition-transform duration-250"
        style={{
          transform: entered ? "translateX(0)" : "translateX(-100%)",
          transitionTimingFunction: "cubic-bezier(0.25, 0.1, 0.25, 1)",
        }}
      >
        {sidebarContent}
      </div>
    </div>
  );
}
