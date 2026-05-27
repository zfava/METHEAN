"use client";

import { useEffect, useState } from "react";
import { subjects as subjectsApi, household } from "@/lib/api";
import Tabs from "@/components/ui/Tabs";
import Button from "@/components/ui/Button";
import { cn } from "@/lib/cn";
import {
  CONTENT_TIER_DESCRIPTIONS,
  CONTENT_TIER_ORDER,
  formatContentTier,
  type ContentTier,
} from "@/lib/mastery";

/**
 * Picker for content-tier-per-subject. Two responsibilities:
 *
 *  1. Lets the parent select a set of subjects and assign each one a
 *     content tier (foundational..mastery). Selection state lives in
 *     the parent via ``selected`` so it can be reused for generation,
 *     persistence, or both.
 *
 *  2. Renders a one-time contextual explainer above the picker that
 *     spells out what the five tiers actually mean. The explainer is
 *     dismissible and the dismissed state persists in
 *     ``households.ui_preferences.dismissed_tier_explainer`` so it does
 *     not re-appear on every visit (or on a different device).
 *
 * Display names come from ``@/lib/mastery``. The wire format
 * (foundational/developing/intermediate/advanced/mastery) is preserved
 * end-to-end so the backend's LEARNING_LEVELS lookup is unaffected.
 */

const TIER_PILL_TONES: Record<ContentTier, string> = {
  foundational: "bg-(--color-danger-light) text-(--color-danger)",
  developing: "bg-(--color-warning-light) text-(--color-warning)",
  intermediate: "bg-(--color-accent-light) text-(--color-accent)",
  advanced: "bg-(--color-success-light) text-(--color-success)",
  mastery: "bg-(--color-constitutional-light) text-(--color-constitutional)",
};

const DEFAULT_TIER: ContentTier = "developing";

const UI_PREF_KEY = "dismissed_tier_explainer";

interface SubjectLevelPickerProps {
  /** Map of subject_id to chosen tier (wire-format value, e.g.
   *  "foundational"). */
  selected: Record<string, string>;
  onChange: (levels: Record<string, string>) => void;
  showCustom?: boolean;
}

export default function SubjectLevelPicker({ selected, onChange, showCustom = true }: SubjectLevelPickerProps) {
  const [catalog, setCatalog] = useState<any>(null);
  const [tab, setTab] = useState<"academic" | "vocational" | "custom">("academic");
  const [newSubjectName, setNewSubjectName] = useState("");
  // The explainer defaults to visible so a brand-new user sees it once.
  // We hide it immediately while we await the per-household preference,
  // then show it again only if the household has not dismissed it.
  const [showExplainer, setShowExplainer] = useState<boolean>(false);
  const [explainerLoaded, setExplainerLoaded] = useState(false);

  useEffect(() => {
    subjectsApi.catalog().then(setCatalog).catch(() => {});
  }, []);

  useEffect(() => {
    let active = true;
    household
      .getUIPreferences()
      .then((prefs) => {
        if (!active) return;
        setShowExplainer(prefs?.[UI_PREF_KEY] !== true);
        setExplainerLoaded(true);
      })
      .catch(() => {
        // If we can't read prefs (offline, transient error), show the
        // explainer rather than swallowing it; a missed dismissal is
        // less bad than a parent never seeing the tier definitions.
        if (!active) return;
        setShowExplainer(true);
        setExplainerLoaded(true);
      });
    return () => {
      active = false;
    };
  }, []);

  async function dismissExplainer() {
    setShowExplainer(false);
    try {
      await household.updateUIPreferences({ [UI_PREF_KEY]: true });
    } catch {
      // The local state is already dismissed for this session; the
      // worst case is the explainer comes back on the next reload,
      // which is fine.
    }
  }

  if (!catalog) return <div className="text-xs text-(--color-text-tertiary)">Loading subjects...</div>;

  function toggleSubject(subjectId: string) {
    const next = { ...selected };
    if (next[subjectId]) {
      delete next[subjectId];
    } else {
      next[subjectId] = DEFAULT_TIER;
    }
    onChange(next);
  }

  function setLevel(subjectId: string, level: ContentTier) {
    onChange({ ...selected, [subjectId]: level });
  }

  async function addCustomSubject() {
    if (!newSubjectName.trim()) return;
    try {
      const result = await subjectsApi.addCustom({ name: newSubjectName });
      setCatalog((prev: any) => ({ ...prev, custom: [...(prev?.custom || []), result] }));
      setNewSubjectName("");
    } catch {}
  }

  const currentSubjects = tab === "academic" ? catalog.academic :
    tab === "vocational" ? catalog.vocational : catalog.custom || [];

  return (
    <div>
      {explainerLoaded && showExplainer && (
        <div
          role="region"
          aria-label="What the curriculum tiers mean"
          className="mb-4 rounded-[12px] border border-(--color-border) bg-(--color-surface) p-4"
        >
          <div className="flex items-start justify-between gap-3 mb-2">
            <div>
              <h4 className="text-xs font-semibold uppercase tracking-wider text-(--color-text-secondary)">
                What the tiers mean
              </h4>
              <p className="text-xs text-(--color-text-tertiary) mt-0.5">
                Choose where to start. You can change this later.
              </p>
            </div>
            <button
              type="button"
              onClick={dismissExplainer}
              className="text-xs text-(--color-text-secondary) hover:text-(--color-text) underline underline-offset-2 min-h-[36px] px-2"
              aria-label="Dismiss tier explainer"
            >
              Got it
            </button>
          </div>
          <ul className="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-1.5 mt-2">
            {CONTENT_TIER_ORDER.map((tier) => (
              <li key={tier} className="flex items-baseline gap-2 text-xs">
                <span
                  className={cn(
                    "px-1.5 py-0.5 rounded-[6px] text-[10px] font-medium shrink-0",
                    TIER_PILL_TONES[tier],
                  )}
                >
                  {formatContentTier(tier)}
                </span>
                <span className="text-(--color-text-secondary)">
                  {CONTENT_TIER_DESCRIPTIONS[tier]}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      <Tabs<"academic" | "vocational" | "custom">
        tabs={[
          { key: "academic", label: "Academic" },
          { key: "vocational", label: "Vocational" },
          ...(showCustom ? [{ key: "custom" as const, label: "Custom" }] : []),
        ]}
        active={tab}
        onChange={setTab}
      />

      <div className="mt-3 space-y-2">
        {currentSubjects.map((subj: any) => {
          const isSelected = subj.id in selected;
          const chosenTier = (selected[subj.id] as ContentTier | undefined) ?? DEFAULT_TIER;
          return (
            <div key={subj.id} className={cn(
              "rounded-[8px] border p-3 transition-colors",
              isSelected ? "border-(--color-accent) bg-(--color-accent-light)/30" : "border-(--color-border)"
            )}>
              <button
                onClick={() => toggleSubject(subj.id)}
                className="w-full text-left"
                aria-pressed={isSelected}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-xs font-medium text-(--color-text)">{subj.name}</span>
                    <span className="text-[10px] text-(--color-text-tertiary) ml-2">{subj.category}</span>
                  </div>
                  {isSelected && (
                    <span className="text-[10px] text-(--color-accent) font-medium">
                      {formatContentTier(chosenTier)}
                    </span>
                  )}
                </div>
                {subj.description && (
                  <p className="text-[10px] text-(--color-text-secondary) mt-0.5">{subj.description}</p>
                )}
              </button>

              {isSelected && (
                <div
                  className="flex gap-1 mt-2"
                  role="radiogroup"
                  aria-label={`Tier for ${subj.name}`}
                >
                  {CONTENT_TIER_ORDER.map((tier) => {
                    const active = chosenTier === tier;
                    return (
                      <button
                        key={tier}
                        type="button"
                        role="radio"
                        aria-checked={active}
                        onClick={() => setLevel(subj.id, tier)}
                        title={CONTENT_TIER_DESCRIPTIONS[tier]}
                        className={cn(
                          "flex-1 py-1.5 text-[10px] font-medium rounded-[6px] transition-colors min-h-[28px]",
                          active ? TIER_PILL_TONES[tier] : "bg-(--color-page) text-(--color-text-tertiary) hover:text-(--color-text)",
                        )}
                      >
                        {formatContentTier(tier)}
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}

        {currentSubjects.length === 0 && tab !== "custom" && (
          <p className="text-xs text-(--color-text-tertiary) py-4 text-center">No subjects in this category.</p>
        )}

        {tab === "custom" && showCustom && (
          <div className="flex gap-2 mt-2">
            <input value={newSubjectName} onChange={(e) => setNewSubjectName(e.target.value)}
              placeholder="New subject name"
              className="flex-1 px-3 py-2 text-xs border border-(--color-border) rounded-[10px] bg-(--color-surface)"
              onKeyDown={(e) => e.key === "Enter" && addCustomSubject()} />
            <Button variant="primary" size="sm" onClick={addCustomSubject} disabled={!newSubjectName.trim()}>Add</Button>
          </div>
        )}
      </div>
    </div>
  );
}
