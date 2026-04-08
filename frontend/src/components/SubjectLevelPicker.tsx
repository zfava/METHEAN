"use client";

import { useEffect, useState } from "react";
import { subjects as subjectsApi } from "@/lib/api";
import Tabs from "@/components/ui/Tabs";
import Button from "@/components/ui/Button";
import { cn } from "@/lib/cn";

const LEVEL_ORDER = ["foundational", "developing", "intermediate", "advanced", "mastery"];
const LEVEL_LABELS: Record<string, string> = {
  foundational: "Fund", developing: "Dev", intermediate: "Int", advanced: "Adv", mastery: "Mast",
};
const LEVEL_COLORS: Record<string, string> = {
  foundational: "bg-(--color-danger-light) text-(--color-danger)",
  developing: "bg-(--color-warning-light) text-(--color-warning)",
  intermediate: "bg-(--color-accent-light) text-(--color-accent)",
  advanced: "bg-(--color-success-light) text-(--color-success)",
  mastery: "bg-(--color-constitutional-light) text-(--color-constitutional)",
};

interface SubjectLevelPickerProps {
  selected: Record<string, string>;  // subjectId -> level
  onChange: (levels: Record<string, string>) => void;
  showCustom?: boolean;
}

export default function SubjectLevelPicker({ selected, onChange, showCustom = true }: SubjectLevelPickerProps) {
  const [catalog, setCatalog] = useState<any>(null);
  const [tab, setTab] = useState<"academic" | "vocational" | "custom">("academic");
  const [newSubjectName, setNewSubjectName] = useState("");

  useEffect(() => {
    subjectsApi.catalog().then(setCatalog).catch(() => {});
  }, []);

  if (!catalog) return <div className="text-xs text-(--color-text-tertiary)">Loading subjects...</div>;

  function toggleSubject(subjectId: string) {
    const next = { ...selected };
    if (next[subjectId]) {
      delete next[subjectId];
    } else {
      next[subjectId] = "developing";
    }
    onChange(next);
  }

  function setLevel(subjectId: string, level: string) {
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
          return (
            <div key={subj.id} className={cn(
              "rounded-[8px] border p-3 transition-colors",
              isSelected ? "border-(--color-accent) bg-(--color-accent-light)/30" : "border-(--color-border)"
            )}>
              <button onClick={() => toggleSubject(subj.id)} className="w-full text-left">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-xs font-medium text-(--color-text)">{subj.name}</span>
                    <span className="text-[10px] text-(--color-text-tertiary) ml-2">{subj.category}</span>
                  </div>
                  {isSelected && (
                    <span className="text-[10px] text-(--color-accent) font-medium">Selected</span>
                  )}
                </div>
                {subj.description && (
                  <p className="text-[10px] text-(--color-text-secondary) mt-0.5">{subj.description}</p>
                )}
              </button>

              {isSelected && (
                <div className="flex gap-1 mt-2">
                  {LEVEL_ORDER.map((level) => (
                    <button key={level} onClick={() => setLevel(subj.id, level)}
                      className={cn(
                        "flex-1 py-1.5 text-[9px] font-medium rounded-[6px] transition-colors",
                        selected[subj.id] === level ? LEVEL_COLORS[level] : "bg-(--color-page) text-(--color-text-tertiary)"
                      )}>
                      {LEVEL_LABELS[level]}
                    </button>
                  ))}
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
