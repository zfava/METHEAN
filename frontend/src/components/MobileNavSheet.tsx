"use client";

import { useEffect, useState } from "react";

import { usePathname, useRouter } from "next/navigation";
import BottomSheet from "@/components/BottomSheet";
import { haptic } from "@/lib/haptics";
import { auth, type User } from "@/lib/api";

// The sheet now collapses to four canonical groups per the spec.
// Items inside each group keep the existing routes; we just rewire
// the labels and group membership.
interface NavItem {
  href: string;
  label: string;
  guardianOnly?: boolean;
}

const NAV_SECTIONS: { label: string; items: NavItem[] }[] = [
  {
    label: "Learning",
    items: [
      { href: "/dashboard", label: "Dashboard" },
      { href: "/curriculum", label: "Curriculum" },
      { href: "/calendar", label: "Calendar" },
      { href: "/plans", label: "Weekly Plans" },
      { href: "/plans/vision", label: "Education Plan" },
      { href: "/maps", label: "Maps" },
      { href: "/assessment", label: "Assessment" },
      { href: "/reading", label: "Reading Log" },
      { href: "/resources", label: "Resources" },
    ],
  },
  {
    label: "Governance",
    items: [
      { href: "/governance/queue", label: "Approval Queue" },
      { href: "/governance/rules", label: "Rules" },
      { href: "/governance/philosophy", label: "Philosophy" },
      { href: "/governance/trace", label: "Decision Trace" },
      { href: "/governance/reports", label: "Reports" },
      { href: "/governance/overrides", label: "Overrides" },
      // Guardian-only: hidden for observers to avoid a 403 dead end.
      { href: "/governance/personalization", label: "Personalization", guardianOnly: true },
    ],
  },
  {
    label: "Insights",
    items: [
      { href: "/inspection", label: "AI Inspection" },
      { href: "/intelligence", label: "Learner Profile" },
      { href: "/family-insights", label: "Family Insights" },
      { href: "/wellbeing", label: "Wellbeing" },
      { href: "/style-profile", label: "Learning Style" },
      { href: "/calibration", label: "Evaluator Calibration" },
    ],
  },
  {
    label: "Settings",
    items: [
      { href: "/family", label: "Family" },
      { href: "/compliance", label: "Compliance" },
      { href: "/billing", label: "Billing" },
      { href: "/settings", label: "Settings" },
      { href: "/child", label: "Child View" },
    ],
  },
];

export default function MobileNavSheet({ open, onClose }: { open: boolean; onClose: () => void }) {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);

  // The auth call is cheap and cached server-side; we fire it once
  // when the sheet first becomes available so the guardian-only
  // filter doesn't flash the personalization link to an observer.
  useEffect(() => {
    let cancelled = false;
    auth.me().then((u) => { if (!cancelled) setUser(u); }).catch(() => {});
    return () => { cancelled = true; };
  }, []);

  function navigate(href: string) {
    haptic("light");
    router.push(href);
    onClose();
  }

  function isActive(href: string) {
    return pathname === href || pathname.startsWith(href + "/");
  }

  const isGuardian = user ? user.role !== "observer" : false;

  return (
    <BottomSheet open={open} onClose={onClose} snapPoints={[0.85]} label="Main navigation">
      <div className="px-4 pb-6 pt-1">
        {NAV_SECTIONS.map((section) => (
          <div key={section.label} className="mb-4 last:mb-0">
            {/* Static section header — no toggle. The sheet is short
                enough that hiding groups behind a tap was friction
                without payoff. */}
            <div className="px-1 pb-2">
              <span className="text-[11px] font-semibold tracking-wider uppercase text-(--color-text-tertiary)">
                {section.label}
              </span>
            </div>
            <div className="space-y-0.5">
              {section.items
                .filter((item) => !item.guardianOnly || isGuardian)
                .map((item) => {
                const active = isActive(item.href);
                return (
                  <button
                    key={item.href}
                    onClick={() => navigate(item.href)}
                    className="w-full flex items-center h-12 px-3 rounded-[10px] text-left text-sm transition-colors min-h-[44px]"
                    style={{
                      background: active ? "var(--color-accent-light)" : "transparent",
                      color: active ? "var(--color-accent)" : "var(--color-text)",
                      fontWeight: active ? 500 : 400,
                    }}
                  >
                    {item.label}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </BottomSheet>
  );
}
