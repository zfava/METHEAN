"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { auth, type User } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";
import { cn } from "@/lib/cn";

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

  useEffect(() => {
    fetch(`${API}/governance/queue?limit=1`, { credentials: "include" })
      .then((r) => r.ok ? r.json() : { total: 0 })
      .then((d) => setPendingCount(d.total || 0))
      .catch(() => {});
    auth.me().then(setUser).catch(() => {});
  }, []);

  const govActive = pathname.startsWith("/governance");

  function navItem(href: string, label: string, exact = false) {
    const active = exact ? pathname === href : pathname.startsWith(href);
    return (
      <Link key={href} href={href}
        className={cn(
          "flex items-center px-4 py-[7px] text-[13px] rounded-r-lg ml-1 transition-colors duration-150",
          active
            ? "bg-(--color-sidebar-active) text-white font-medium border-l-2 border-(--color-accent)"
            : "text-(--color-text-sidebar) hover:text-white hover:bg-(--color-sidebar-hover) border-l-2 border-transparent",
        )}
      >{label}</Link>
    );
  }

  return (
    <aside className="w-[240px] min-h-screen bg-(--color-sidebar) flex flex-col shrink-0">
      <div className="px-5 pt-6 pb-5">
        <Link href="/dashboard" className="text-lg font-semibold tracking-[-0.03em] text-white">METHEAN</Link>
      </div>

      {!loading && children.length > 0 && (
        <div className="px-4 pb-4">
          <select value={selectedChild?.id || ""}
            onChange={(e) => { const c = children.find((ch) => ch.id === e.target.value); if (c) setSelectedChild(c); }}
            className="w-full px-3 py-2 text-sm bg-(--color-sidebar-hover) text-white border border-white/10 rounded-[6px] focus:outline-none focus:ring-1 focus:ring-(--color-accent)">
            {children.map((c) => (
              <option key={c.id} value={c.id}>{c.first_name} {c.last_name || ""}{c.grade_level ? ` \u00b7 ${c.grade_level}` : ""}</option>
            ))}
          </select>
        </div>
      )}

      <nav className="flex-1 space-y-5 pb-4">
        <div>
          <div className="px-5 mb-1.5 text-[11px] font-medium text-white/30 tracking-wider">Overview</div>
          {navItem("/dashboard", "Dashboard", true)}
          {navItem("/compliance", "Compliance")}
        </div>
        <div>
          <div className="px-5 mb-1.5 text-[11px] font-medium text-white/30 tracking-wider">Learning</div>
          {navItem("/curriculum", "Curriculum")}
          {navItem("/plans", "Plans")}
          {navItem("/maps", "Maps")}
          {navItem("/curriculum/editor", "Map Editor")}
          {navItem("/assessment", "Assessment")}
          {navItem("/inspection", "Progress")}
        </div>
        <div>
          <div className="flex items-center justify-between px-5 mb-1.5">
            <span className="text-[11px] font-medium text-white/30 tracking-wider">Governance</span>
            {pendingCount > 0 && (
              <span className="bg-(--color-warning) text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full">{pendingCount}</span>
            )}
          </div>
          <Link href="/governance"
            className={cn(
              "flex items-center px-4 py-[7px] text-[13px] rounded-r-lg ml-1 transition-colors duration-150",
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
                  <span className="bg-(--color-warning) text-white text-[9px] font-bold px-1 py-0.5 rounded-full">{pendingCount}</span>
                )}
              </Link>
            );
          })}
        </div>
      </nav>

      <div className="px-4 py-4 border-t border-white/5 space-y-2">
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
