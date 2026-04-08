"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState, useCallback, useRef } from "react";
import { auth, notifications as notificationsApi, type User } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import { cn } from "@/lib/cn";
import { MetheanLogo } from "@/components/Brand";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const govSub = [
  { href: "/governance/queue", label: "Approval Queue", badge: true },
  { href: "/governance/rules", label: "Rules" },
  { href: "/governance/philosophy", label: "Philosophy" },
  { href: "/governance/trace", label: "Decision Trace" },
  { href: "/governance/reports", label: "Reports" },
  { href: "/governance/overrides", label: "Overrides" },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { children, selectedChild, setSelectedChild, loading } = useChild();
  const [pendingCount, setPendingCount] = useState(0);
  const [user, setUser] = useState<User | null>(null);
  const [unreadNotifs, setUnreadNotifs] = useState(0);
  const [showNotifs, setShowNotifs] = useState(false);
  const [notifList, setNotifList] = useState<any[]>([]);
  const [bellPulse, setBellPulse] = useState(false);
  const prevUnread = useRef(0);

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
    fetch(`${API}/governance/queue?limit=1`, { credentials: "include" })
      .then((r) => r.ok ? r.json() : { total: 0 })
      .then((d) => setPendingCount(d.total || 0))
      .catch(() => {});
    auth.me().then(setUser).catch(() => {});
    loadNotifications();
    const interval = setInterval(loadNotifications, 60000);
    return () => clearInterval(interval);
  }, [loadNotifications]);

  const govActive = pathname.startsWith("/governance");

  function navItem(href: string, label: string, exact = false) {
    const active = exact ? pathname === href : (pathname === href || pathname.startsWith(href + "/"));
    return (
      <Link key={href} href={href}
        className={cn(
          "flex items-center px-4 py-2 text-[13px] rounded-r-lg ml-1 transition-colors duration-150",
          active
            ? "bg-(--color-sidebar-active) text-white font-medium border-l-2 border-(--color-accent)"
            : "text-(--color-text-sidebar) hover:text-white hover:bg-(--color-sidebar-hover) border-l-2 border-transparent",
        )}
      >{label}</Link>
    );
  }

  return (
    <aside className="w-[240px] min-h-screen bg-(--color-sidebar) flex flex-col shrink-0">
      <div className="px-5 pt-5 pb-4 flex items-center justify-between">
        <Link href="/dashboard" className="block">
          <MetheanLogo markSize={28} wordmarkHeight={14} color="#C6A24E" gap={10} />
        </Link>
        <button onClick={() => setShowNotifs(!showNotifs)} className="relative p-1.5 text-white/40 hover:text-white/70 transition-colors">
          <svg className="w-4.5 h-4.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
          </svg>
          {unreadNotifs > 0 && (
            <span className={cn("absolute -top-0.5 -right-0.5 w-3.5 h-3.5 bg-(--color-brand-gold) text-white text-[8px] font-bold rounded-full flex items-center justify-center", bellPulse && "notif-new")}>{unreadNotifs}</span>
          )}
        </button>
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
                <div key={n.id} className={cn("px-2 py-1.5 rounded-[6px] text-[10px]", n.is_read ? "text-white/30" : "text-white/70 bg-white/5")}>
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
            className="w-full px-3 py-2 text-sm bg-(--color-sidebar-hover) text-white border border-white/10 rounded-[6px] focus:outline-none focus:ring-1 focus:ring-(--color-accent)">
            {children.map((c) => (
              <option key={c.id} value={c.id}>{c.first_name} {c.last_name || ""}</option>
            ))}
          </select>
        </div>
      )}

      <nav className="flex-1 space-y-5 pb-4">
        <div>
          <div className="px-5 mb-1.5 text-[11px] font-medium text-white/30 tracking-wider">Overview</div>
          {navItem("/dashboard", "Dashboard", true)}
          {navItem("/family", "Family")}
          {navItem("/compliance", "Compliance")}
        </div>
        <div>
          <div className="px-5 mb-1.5 text-[11px] font-medium text-white/30 tracking-wider">Learning</div>
          {navItem("/curriculum", "Curriculum", true)}
          {navItem("/curriculum/year", "Year Plan")}
          {navItem("/curriculum/history", "History")}
          {navItem("/calendar", "Calendar")}
          {navItem("/plans", "Plans")}
          {navItem("/maps", "Maps")}
          {navItem("/curriculum/editor", "Map Editor")}
          {navItem("/assessment", "Assessment")}
          {navItem("/reading", "Reading Log")}
          {navItem("/resources", "Resources")}
          {navItem("/inspection", "Progress")}
        </div>
        <div>
          <div className="flex items-center justify-between px-5 mb-1.5">
            <span className="text-[11px] font-medium text-white/30 tracking-wider">Governance</span>
            {pendingCount > 0 && (
              <span className="bg-(--color-brand-gold) text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full">{pendingCount}</span>
            )}
          </div>
          <Link href="/governance"
            className={cn(
              "flex items-center px-4 py-2 text-[13px] rounded-r-lg ml-1 transition-colors duration-150",
              pathname === "/governance"
                ? "bg-(--color-sidebar-active) text-white font-medium border-l-2 border-(--color-accent)"
                : "text-(--color-text-sidebar) hover:text-white hover:bg-(--color-sidebar-hover) border-l-2 border-transparent",
            )}>Overview</Link>
          {govActive && govSub.map((item) => {
            const active = pathname.startsWith(item.href);
            return (
              <Link key={item.href} href={item.href}
                className={cn(
                  "flex items-center justify-between pl-9 pr-4 py-[5px] text-xs transition-colors duration-150",
                  active ? "text-white font-medium" : "text-white/30 hover:text-white/60",
                )}>
                {item.label}
                {item.badge && pendingCount > 0 && (
                  <span className="bg-(--color-brand-gold) text-white text-[9px] font-bold px-1 py-0.5 rounded-full">{pendingCount}</span>
                )}
              </Link>
            );
          })}
        </div>
      </nav>

      <div className="px-4 py-4 border-t border-white/5 space-y-2">
        {navItem("/settings", "Settings", true)}
        <Link href="/child" className="block px-1 py-1 text-xs text-white/25 hover:text-white/50 transition-colors duration-150">Child View</Link>
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
}
