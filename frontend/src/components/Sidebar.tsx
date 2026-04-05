"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { auth, type User } from "@/lib/api";
import { useChild } from "@/lib/ChildContext";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const govSub = [
  { href: "/governance/queue", label: "Approval Queue", badge: true },
  { href: "/governance/rules", label: "Rules" },
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

  function navLink(href: string, label: string, icon: string, exact = false) {
    const active = exact ? pathname === href : pathname.startsWith(href);
    return (
      <Link key={href} href={href}
        className={`flex items-center gap-3 px-5 py-2 text-[13px] rounded-r-md transition-colors ${
          active
            ? "bg-slate-800 text-white font-medium border-l-2 border-blue-400"
            : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border-l-2 border-transparent"
        }`}
      >
        <span className="text-sm w-4 text-center opacity-70">{icon}</span>
        {label}
      </Link>
    );
  }

  return (
    <aside className="w-64 min-h-screen bg-slate-900 flex flex-col">
      {/* Logo */}
      <div className="px-5 py-6">
        <Link href="/dashboard" className="text-lg font-semibold tracking-tight text-white">
          METHEAN
        </Link>
      </div>

      {/* Child selector */}
      {!loading && children.length > 0 && (
        <div className="px-4 pb-4">
          <select
            value={selectedChild?.id || ""}
            onChange={(e) => {
              const c = children.find((ch) => ch.id === e.target.value);
              if (c) setSelectedChild(c);
            }}
            className="w-full px-3 py-2 text-sm bg-slate-800 text-white border border-slate-700 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            {children.map((c) => (
              <option key={c.id} value={c.id}>
                {c.first_name} {c.last_name || ""} {c.grade_level ? `\u00b7 ${c.grade_level}` : ""}
              </option>
            ))}
          </select>
        </div>
      )}

      <nav className="flex-1 space-y-6 px-2">
        {/* Overview */}
        <div>
          <div className="px-3 mb-1 text-[10px] font-semibold text-slate-500 uppercase tracking-widest">
            Overview
          </div>
          {navLink("/dashboard", "Dashboard", "\u25C9", true)}
        </div>

        {/* Learning */}
        <div>
          <div className="px-3 mb-1 text-[10px] font-semibold text-slate-500 uppercase tracking-widest">
            Learning
          </div>
          {navLink("/plans", "Plans", "\u25A4")}
          {navLink("/maps", "Maps", "\u25CE")}
          {navLink("/inspection", "Progress", "\u2B21")}
        </div>

        {/* Governance */}
        <div>
          <div className="px-3 mb-1 text-[10px] font-semibold text-slate-500 uppercase tracking-widest flex items-center justify-between">
            <span>Governance</span>
            {pendingCount > 0 && (
              <span className="bg-amber-500 text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full">
                {pendingCount}
              </span>
            )}
          </div>
          <Link href="/governance"
            className={`flex items-center gap-3 px-5 py-2 text-[13px] rounded-r-md transition-colors ${
              pathname === "/governance"
                ? "bg-slate-800 text-white font-medium border-l-2 border-blue-400"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border-l-2 border-transparent"
            }`}
          >
            <span className="text-sm w-4 text-center opacity-70">&#9672;</span>
            Overview
          </Link>
          {govSub.map((item) => {
            const active = pathname.startsWith(item.href);
            return (
              <Link key={item.href} href={item.href}
                className={`flex items-center justify-between pl-12 pr-5 py-1.5 text-xs rounded-r-md transition-colors ${
                  active
                    ? "text-white font-medium"
                    : "text-slate-500 hover:text-slate-300"
                }`}
              >
                {item.label}
                {item.badge && pendingCount > 0 && (
                  <span className="bg-amber-500 text-white text-[9px] font-bold px-1 py-0.5 rounded-full min-w-[14px] text-center">
                    {pendingCount}
                  </span>
                )}
              </Link>
            );
          })}
        </div>
      </nav>

      {/* Bottom: user + child view link */}
      <div className="px-4 py-4 border-t border-slate-800">
        <Link href="/child" className="flex items-center gap-2 px-1 py-1.5 text-xs text-slate-500 hover:text-slate-300 mb-2">
          <span>&#9680;</span> Child View
        </Link>
        {user && (
          <div className="flex items-center justify-between px-1">
            <span className="text-[11px] text-slate-500 truncate">{user.email}</span>
            <button
              onClick={() => auth.logout().then(() => (window.location.href = "/auth"))}
              className="text-[11px] text-slate-600 hover:text-slate-400"
            >
              Sign out
            </button>
          </div>
        )}
      </div>
    </aside>
  );
}
