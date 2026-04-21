"use client";

import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";
import BottomSheet from "@/components/BottomSheet";
import { haptic } from "@/lib/haptics";

const NAV_SECTIONS = [
  {
    label: "Overview",
    items: [
      { href: "/dashboard", label: "Dashboard" },
      { href: "/family", label: "Family" },
      { href: "/compliance", label: "Compliance" },
    ],
  },
  {
    label: "Curriculum",
    items: [
      { href: "/curriculum", label: "Curriculum" },
      { href: "/curriculum/year", label: "Year Plan" },
      { href: "/curriculum/scope", label: "Scope & Sequence" },
      { href: "/curriculum/history", label: "History" },
      { href: "/curriculum/editor", label: "Map Editor" },
      { href: "/curriculum/mapper", label: "Map Curriculum" },
    ],
  },
  {
    label: "Learning",
    items: [
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
    label: "Intelligence",
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
    label: "Governance",
    items: [
      { href: "/governance", label: "Overview" },
      { href: "/governance/queue", label: "Approval Queue" },
      { href: "/governance/rules", label: "Rules" },
      { href: "/governance/philosophy", label: "Philosophy" },
      { href: "/governance/trace", label: "Decision Trace" },
      { href: "/governance/reports", label: "Reports" },
      { href: "/governance/overrides", label: "Overrides" },
    ],
  },
];

const BOTTOM_ITEMS = [
  { href: "/billing", label: "Billing" },
  { href: "/settings", label: "Settings" },
  { href: "/child", label: "Child View" },
];

export default function MobileNavSheet({ open, onClose }: { open: boolean; onClose: () => void }) {
  const pathname = usePathname();
  const router = useRouter();
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});

  function toggleSection(label: string) {
    setExpanded((prev) => ({ ...prev, [label]: !prev[label] }));
  }

  function navigate(href: string) {
    haptic("light");
    router.push(href);
    onClose();
  }

  function isActive(href: string) {
    return pathname === href || pathname.startsWith(href + "/");
  }

  return (
    <BottomSheet open={open} onClose={onClose} snapPoints={[0.85]}>
      <div className="px-4 pb-6">
        {NAV_SECTIONS.map((section) => {
          const isOpen = expanded[section.label] ?? true;
          return (
            <div key={section.label} className="mb-1">
              <button
                onClick={() => toggleSection(section.label)}
                className="w-full flex items-center justify-between py-2.5"
              >
                <span className="text-[11px] font-semibold tracking-wider uppercase text-(--color-text-secondary)">
                  {section.label}
                </span>
                <svg
                  className="w-3.5 h-3.5 text-(--color-text-tertiary) transition-transform duration-150"
                  style={{ transform: isOpen ? "rotate(90deg)" : "rotate(0)" }}
                  fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                </svg>
              </button>
              {isOpen && (
                <div className="mb-2">
                  {section.items.map((item) => (
                    <button
                      key={item.href}
                      onClick={() => navigate(item.href)}
                      className="w-full flex items-center h-12 px-3 rounded-[10px] text-left text-sm transition-colors"
                      style={{
                        background: isActive(item.href) ? "var(--color-accent-light)" : "transparent",
                        color: isActive(item.href) ? "var(--color-accent)" : "var(--color-text)",
                        fontWeight: isActive(item.href) ? 500 : 400,
                      }}
                    >
                      {item.label}
                    </button>
                  ))}
                </div>
              )}
            </div>
          );
        })}

        {/* Divider */}
        <div className="h-px bg-(--color-border) my-2" />

        {/* Bottom items */}
        {BOTTOM_ITEMS.map((item) => (
          <button
            key={item.href}
            onClick={() => navigate(item.href)}
            className="w-full flex items-center h-12 px-3 rounded-[10px] text-left text-sm transition-colors"
            style={{
              color: isActive(item.href) ? "var(--color-accent)" : "var(--color-text-secondary)",
              fontWeight: isActive(item.href) ? 500 : 400,
            }}
          >
            {item.label}
          </button>
        ))}
      </div>
    </BottomSheet>
  );
}
