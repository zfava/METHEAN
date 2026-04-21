"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { useChild } from "@/lib/ChildContext";
import { notifications as notificationsApi } from "@/lib/api";
import { MetheanMark } from "@/components/Brand";
import BottomSheet from "@/components/BottomSheet";
import { haptic } from "@/lib/native";

export default function MobileHeader() {
  const { children, selectedChild, setSelectedChild, loading } = useChild();
  const [childSheetOpen, setChildSheetOpen] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    notificationsApi.list(false, 20)
      .then((data) => {
        const items = Array.isArray(data) ? data : (data as any).items || [];
        setUnreadCount(items.filter((n: any) => !n.is_read).length);
      })
      .catch(() => {});
  }, []);

  return (
    <>
      <header
        data-no-select
        className="fixed top-0 left-0 right-0 z-40 border-b border-(--color-border) md:hidden"
        style={{
          height: `calc(48px + var(--safe-top))`,
          paddingTop: "var(--safe-top)",
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          background: "rgba(255,255,255,0.85)",
        }}
      >
        <div className="flex items-center justify-between h-12 px-4">
          {/* Left: logo mark only */}
          <MetheanMark size={24} color="#C6A24E" />

          {/* Center: child selector pill */}
          {!loading && selectedChild && (
            children.length > 1 ? (
              <button
                onClick={() => setChildSheetOpen(true)}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-(--color-page) border border-(--color-border) press-scale"
                style={{ minHeight: 36 }}
              >
                <span className="text-sm font-medium text-(--color-text) truncate max-w-[120px]">
                  {selectedChild.first_name}
                </span>
                <svg className="w-3.5 h-3.5 text-(--color-text-tertiary)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
                </svg>
              </button>
            ) : (
              <span className="text-sm font-medium text-(--color-text)">{selectedChild.first_name}</span>
            )
          )}

          {/* Right: notification bell */}
          <button className="relative p-2" aria-label="Notifications">
            <svg className="w-5 h-5 text-(--color-text-secondary)" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
            </svg>
            {unreadCount > 0 && (
              <span className="absolute top-1 right-1 w-2.5 h-2.5 rounded-full bg-(--color-danger)" />
            )}
          </button>
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
