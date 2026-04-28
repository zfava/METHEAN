"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useChild } from "@/lib/ChildContext";
import { governance, notifications as notificationsApi } from "@/lib/api";
import { MetheanWordmark } from "@/components/Brand";
import BottomSheet from "@/components/BottomSheet";
import { haptic } from "@/lib/native";

export default function MobileHeader() {
  const { children, selectedChild, setSelectedChild, loading } = useChild();
  const pathname = usePathname();
  const [childSheetOpen, setChildSheetOpen] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);
  const [pendingGovernance, setPendingGovernance] = useState(0);

  // The child switcher only makes sense on child-scoped pages.
  // Restricting here keeps the home / settings / billing headers
  // clean while still surfacing the active child where it's used.
  const isChildScoped =
    pathname.startsWith("/child") ||
    pathname.startsWith("/dashboard") ||
    pathname.startsWith("/plans") ||
    pathname.startsWith("/calendar") ||
    pathname.startsWith("/intelligence") ||
    pathname.startsWith("/wellbeing");

  useEffect(() => {
    notificationsApi
      .list(false, 20)
      .then((data) => {
        const items = Array.isArray(data) ? data : (data as any).items || [];
        setUnreadCount(items.filter((n: any) => !n.is_read).length);
      })
      .catch(() => {});
    governance.queue(1).then((d) => setPendingGovernance(d.total || 0)).catch(() => {});
  }, []);

  // Combined badge: governance pending takes priority (red) since
  // it's the parent's primary attention sink; notifications use the
  // accent dot when there's no governance backlog.
  const showGovBadge = pendingGovernance > 0;
  const showNotifBadge = !showGovBadge && unreadCount > 0;

  return (
    <>
      <header
        data-no-select
        className="fixed top-0 left-0 right-0 z-40 border-b border-(--color-border) md:hidden glass"
        style={{
          height: `calc(48px + var(--safe-top))`,
          paddingTop: "var(--safe-top)",
        }}
      >
        <div className="flex items-center h-12 px-3">
          {/* Left: child switcher (only on child-scoped pages) */}
          <div className="flex-1 min-w-0 flex justify-start">
            {!loading && isChildScoped && selectedChild ? (
              children.length > 1 ? (
                <button
                  onClick={() => setChildSheetOpen(true)}
                  className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-full bg-(--color-page) border border-(--color-border) press-scale min-h-[36px]"
                  aria-label={`Switch from ${selectedChild.first_name}`}
                >
                  <span className="text-sm font-medium text-(--color-text) truncate max-w-[110px]">
                    {selectedChild.first_name}
                  </span>
                  <svg
                    className="w-3.5 h-3.5 text-(--color-text-tertiary) shrink-0"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2.5}
                    aria-hidden="true"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                  </svg>
                </button>
              ) : (
                <span className="text-sm font-medium text-(--color-text) truncate max-w-[140px]">
                  {selectedChild.first_name}
                </span>
              )
            ) : null}
          </div>

          {/* Center: METHEAN wordmark */}
          <Link href="/dashboard" className="shrink-0 flex items-center justify-center" aria-label="METHEAN home">
            <MetheanWordmark height={14} color="#0F1B2D" />
          </Link>

          {/* Right: notification bell. Pending governance items
              show a danger dot; new notifications show the accent
              dot. Tap routes to /governance/queue when there's
              governance pending (the most urgent call), otherwise
              /notifications. */}
          <div className="flex-1 flex justify-end">
            <Link
              href={showGovBadge ? "/governance/queue" : "/notifications"}
              className="relative p-2 min-h-[44px] min-w-[44px] flex items-center justify-center"
              aria-label={
                showGovBadge
                  ? `${pendingGovernance} governance ${pendingGovernance === 1 ? "item" : "items"} pending`
                  : "Notifications"
              }
            >
              <svg
                className="w-5 h-5 text-(--color-text-secondary)"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={1.8}
                aria-hidden="true"
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
              </svg>
              {showGovBadge && (
                <span className="absolute top-1.5 right-1.5 w-2.5 h-2.5 rounded-full bg-(--color-danger) ring-2 ring-(--color-surface)" />
              )}
              {showNotifBadge && (
                <span className="absolute top-1.5 right-1.5 w-2.5 h-2.5 rounded-full bg-(--color-accent) ring-2 ring-(--color-surface)" />
              )}
            </Link>
          </div>
        </div>
      </header>

      {/* Child selector sheet */}
      <BottomSheet open={childSheetOpen} onClose={() => setChildSheetOpen(false)} label="Select child">
        <div className="px-4 pt-2 pb-4">
          <h3 className="text-base font-semibold text-(--color-text) mb-3">Switch Child</h3>
          <div className="flex flex-col gap-2">
            {children.map((child) => {
              const isSelected = child.id === selectedChild?.id;
              return (
                <button
                  key={child.id}
                  onClick={() => { setSelectedChild(child); setChildSheetOpen(false); haptic("light"); }}
                  className={`flex items-center gap-3 p-3 rounded-xl press-scale transition-colors ${
                    isSelected ? "bg-(--color-accent-light) border-l-3 border-(--color-brand-gold)" : "bg-(--color-surface)"
                  }`}
                  style={{ minHeight: 56 }}
                >
                  <div className="w-10 h-10 rounded-full bg-(--color-border) flex items-center justify-center text-lg shrink-0">
                    {child.first_name.charAt(0)}
                  </div>
                  <div className="flex-1 min-w-0 text-left">
                    <div className="text-sm font-semibold text-(--color-text)">{child.first_name} {child.last_name || ""}</div>
                    <div className="text-xs text-(--color-text-secondary)">{child.grade_level || "No grade set"}</div>
                  </div>
                  {isSelected && (
                    <svg className="w-5 h-5 text-(--color-brand-gold) shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      </BottomSheet>
    </>
  );
}
