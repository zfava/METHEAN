"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { useChild } from "@/lib/ChildContext";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const mainNav = [
  { href: "/dashboard", label: "Dashboard", icon: "◉" },
  { href: "/maps", label: "Learning Maps", icon: "◎" },
  { href: "/plans", label: "Plans", icon: "▤" },
];

const govNav = [
  { href: "/governance", label: "Overview", exact: true },
  { href: "/governance/queue", label: "Approval Queue", badge: true },
  { href: "/governance/rules", label: "Rules" },
  { href: "/governance/trace", label: "Decision Trace" },
  { href: "/governance/overrides", label: "Overrides" },
];

const bottomNav = [
  { href: "/inspection", label: "AI Inspection", icon: "⬡" },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { children, selectedChild, setSelectedChild, loading } = useChild();
  const [pendingCount, setPendingCount] = useState(0);

  useEffect(() => {
    fetch(`${API_BASE}/governance/queue?limit=1`, { credentials: "include" })
      .then((r) => (r.ok ? r.json() : { total: 0 }))
      .then((d) => setPendingCount(d.total || 0))
      .catch(() => {});
  }, []);

  const govActive = pathname.startsWith("/governance");

  return (
    <aside className="w-56 min-h-screen bg-white border-r border-(--color-border) flex flex-col">
      <div className="px-5 py-6 border-b border-(--color-border)">
        <Link href="/dashboard" className="text-lg font-semibold tracking-tight text-(--color-text)">
          METHEAN
        </Link>
        <p className="text-xs text-(--color-text-secondary) mt-0.5">Learning OS</p>
      </div>

      {!loading && children.length > 0 && (
        <div className="px-4 py-3 border-b border-(--color-border)">
          <div className="text-[10px] font-medium text-(--color-text-secondary) uppercase tracking-wider mb-1.5">
            Active Child
          </div>
          <select
            value={selectedChild?.id || ""}
            onChange={(e) => {
              const child = children.find((c) => c.id === e.target.value);
              if (child) setSelectedChild(child);
            }}
            className="w-full px-2 py-1.5 text-sm border border-(--color-border) rounded-md bg-white focus:outline-none focus:ring-1 focus:ring-(--color-accent)/30"
          >
            {children.map((c) => (
              <option key={c.id} value={c.id}>
                {c.first_name} {c.last_name || ""} {c.grade_level ? `(${c.grade_level})` : ""}
              </option>
            ))}
          </select>
        </div>
      )}

      <nav className="flex-1 py-3">
        {mainNav.map((item) => {
          const active = pathname.startsWith(item.href);
          return (
            <Link key={item.href} href={item.href}
              className={`flex items-center gap-3 px-5 py-2.5 text-sm transition-colors ${
                active ? "bg-blue-50 text-(--color-accent) font-medium border-r-2 border-(--color-accent)" : "text-(--color-text-secondary) hover:bg-gray-50 hover:text-(--color-text)"
              }`}
            >
              <span className="text-base">{item.icon}</span>
              {item.label}
            </Link>
          );
        })}

        {/* Governance section */}
        <div className="mt-2 pt-2 border-t border-gray-100">
          <Link href="/governance"
            className={`flex items-center justify-between px-5 py-2.5 text-sm transition-colors ${
              govActive ? "bg-blue-50 text-(--color-accent) font-medium border-r-2 border-(--color-accent)" : "text-(--color-text-secondary) hover:bg-gray-50 hover:text-(--color-text)"
            }`}
          >
            <span className="flex items-center gap-3">
              <span className="text-base">◈</span>
              Governance
            </span>
            {pendingCount > 0 && (
              <span className="bg-amber-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full min-w-[18px] text-center">
                {pendingCount}
              </span>
            )}
          </Link>
          {govActive && (
            <div className="ml-8 border-l border-gray-200">
              {govNav.map((item) => {
                const active = item.exact ? pathname === item.href : pathname.startsWith(item.href);
                return (
                  <Link key={item.href} href={item.href}
                    className={`flex items-center justify-between pl-4 pr-5 py-1.5 text-xs transition-colors ${
                      active ? "text-(--color-accent) font-medium" : "text-(--color-text-secondary) hover:text-(--color-text)"
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
          )}
        </div>

        {bottomNav.map((item) => {
          const active = pathname.startsWith(item.href);
          return (
            <Link key={item.href} href={item.href}
              className={`flex items-center gap-3 px-5 py-2.5 text-sm transition-colors ${
                active ? "bg-blue-50 text-(--color-accent) font-medium border-r-2 border-(--color-accent)" : "text-(--color-text-secondary) hover:bg-gray-50 hover:text-(--color-text)"
              }`}
            >
              <span className="text-base">{item.icon}</span>
              {item.label}
            </Link>
          );
        })}
      </nav>
      <div className="px-5 py-4 border-t border-(--color-border)">
        <Link href="/child" className="flex items-center gap-2 text-sm text-(--color-text-secondary) hover:text-(--color-text)">
          <span className="text-base">◐</span> Child View
        </Link>
      </div>
    </aside>
  );
}
