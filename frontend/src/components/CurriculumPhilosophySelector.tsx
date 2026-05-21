"use client";

/**
 * Lets a parent choose a child's educational philosophy. Six options,
 * each with a plain-language description. Choosing "Eclectic" reveals
 * a per-subject sub-selector that writes to subject_philosophies.
 *
 * Real radio and select semantics: keyboard-operable, labelled, and
 * the control only offers allowed values.
 */

import {
  type CurriculumPhilosophy,
  ECLECTIC_SUBJECT_OPTIONS,
  ECLECTIC_SUBJECTS,
  PHILOSOPHY_OPTIONS,
} from "@/lib/curriculum-philosophy";
import { cn } from "@/lib/cn";

interface CurriculumPhilosophySelectorProps {
  value: CurriculumPhilosophy;
  subjectPhilosophies: Record<string, string>;
  onChange: (philosophy: CurriculumPhilosophy, subjectPhilosophies: Record<string, string>) => void;
  /** Unique prefix so radio names and input ids do not collide. */
  idPrefix: string;
  disabled?: boolean;
}

/** Build a full per-subject map, defaulting each subject to traditional. */
function fullSubjectMap(existing: Record<string, string>): Record<string, string> {
  const full: Record<string, string> = {};
  for (const subject of ECLECTIC_SUBJECTS) {
    full[subject.id] = existing[subject.id] ?? "traditional";
  }
  return full;
}

export default function CurriculumPhilosophySelector({
  value,
  subjectPhilosophies,
  onChange,
  idPrefix,
  disabled,
}: CurriculumPhilosophySelectorProps) {
  function handlePhilosophyChange(next: CurriculumPhilosophy) {
    if (next === "eclectic") {
      // Reveal per-subject choices; each defaults to traditional.
      onChange("eclectic", fullSubjectMap(subjectPhilosophies));
    } else {
      onChange(next, subjectPhilosophies);
    }
  }

  function handleSubjectChange(subjectId: string, philosophy: string) {
    const next = fullSubjectMap(subjectPhilosophies);
    next[subjectId] = philosophy;
    onChange("eclectic", next);
  }

  return (
    <div>
      <fieldset disabled={disabled}>
        <legend className="text-[10px] font-medium text-(--color-text-secondary) mb-1.5">
          Educational philosophy
        </legend>
        <div className="flex flex-col gap-1.5">
          {PHILOSOPHY_OPTIONS.map((opt) => {
            const inputId = `${idPrefix}-philosophy-${opt.id}`;
            const descId = `${inputId}-desc`;
            const selected = value === opt.id;
            return (
              <label
                key={opt.id}
                htmlFor={inputId}
                className={cn(
                  "flex items-start gap-2 px-2.5 py-2 rounded-[var(--radius-input)] border cursor-pointer transition-colors",
                  selected
                    ? "border-(--color-accent) bg-(--color-accent-light)"
                    : "border-(--color-border) hover:border-(--color-text-tertiary)",
                )}
              >
                <input
                  type="radio"
                  id={inputId}
                  name={`${idPrefix}-philosophy`}
                  value={opt.id}
                  checked={selected}
                  onChange={() => handlePhilosophyChange(opt.id)}
                  aria-describedby={descId}
                  className="mt-0.5 accent-(--color-accent)"
                />
                <span className="min-w-0">
                  <span className="block text-xs font-medium text-(--color-text)">{opt.label}</span>
                  <span
                    id={descId}
                    className="block text-[10px] text-(--color-text-secondary) leading-snug"
                  >
                    {opt.description}
                  </span>
                </span>
              </label>
            );
          })}
        </div>
      </fieldset>

      {value === "eclectic" && (
        <div className="mt-3 pl-2.5 border-l-2 border-(--color-accent-light)">
          <p className="text-[10px] text-(--color-text-secondary) mb-1.5">
            Choose an approach for each subject.
          </p>
          <div className="flex flex-col gap-1.5">
            {ECLECTIC_SUBJECTS.map((subject) => {
              const selectId = `${idPrefix}-subject-${subject.id}`;
              return (
                <div key={subject.id} className="flex items-center justify-between gap-2">
                  <label htmlFor={selectId} className="text-xs text-(--color-text)">
                    {subject.label}
                  </label>
                  <select
                    id={selectId}
                    disabled={disabled}
                    value={subjectPhilosophies[subject.id] ?? "traditional"}
                    onChange={(e) => handleSubjectChange(subject.id, e.target.value)}
                    className="text-xs px-2 py-1 border border-(--color-border) rounded-[var(--radius-input)] bg-(--color-surface) text-(--color-text)"
                  >
                    {ECLECTIC_SUBJECT_OPTIONS.map((o) => (
                      <option key={o.id} value={o.id}>
                        {o.label}
                      </option>
                    ))}
                  </select>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
