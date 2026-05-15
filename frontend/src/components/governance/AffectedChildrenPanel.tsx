"use client";

import { useCallback, useEffect, useState } from "react";

import { children as childrenApi, personalization } from "@/lib/api";
import type { ChildPersonalization } from "@/lib/personalization-types";

interface ChildSummary {
  id: string;
  first_name: string;
}

interface AffectedChildrenPanelProps {
  /** Bumped by the parent after a policy mutation so the panel
   *  refetches each child's profile and surfaces newly
   *  out-of-policy fields. */
  refreshKey: number;
}

// Defaults used by the per-field reset buttons. Mirrors the
// defaults the kid sees in MySpace + WelcomePage.
const DEFAULTS: Record<string, string> = {
  vibe: "calm",
  iconography_pack: "default",
  sound_pack: "soft",
  affirmation_tone: "warm",
  companion_voice: "default_warm",
};

const FIELD_LABELS: Record<string, string> = {
  vibe: "Vibe",
  iconography_pack: "Icons",
  sound_pack: "Sound",
  affirmation_tone: "Tone",
  companion_voice: "Companion voice",
  interest_tags: "Interests",
};

export function AffectedChildrenPanel({ refreshKey }: AffectedChildrenPanelProps) {
  const [children, setChildren] = useState<ChildSummary[]>([]);
  const [profiles, setProfiles] = useState<Record<string, ChildPersonalization>>({});
  const [loading, setLoading] = useState(true);
  const [confirmResetId, setConfirmResetId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const list = (await childrenApi.list()) as unknown as ChildSummary[];
      const arr = Array.isArray(list) ? list : [];
      setChildren(arr);
      const entries = await Promise.all(
        arr.map(async (c) => {
          try {
            const p = await personalization.getForChild(c.id);
            return [c.id, p] as const;
          } catch {
            return null;
          }
        }),
      );
      const next: Record<string, ChildPersonalization> = {};
      for (const e of entries) {
        if (e) next[e[0]] = e[1];
      }
      setProfiles(next);
    } catch {
      setError("Couldn't load children. Try again.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load, refreshKey]);

  async function resetField(childId: string, field: keyof ChildPersonalization) {
    const patch: Partial<ChildPersonalization> = {};
    if (field === "interest_tags") {
      patch.interest_tags = [];
    } else if (typeof DEFAULTS[field as string] === "string") {
      (patch as Record<string, unknown>)[field as string] = DEFAULTS[field as string];
    }
    try {
      const updated = await personalization.updateForChild(childId, patch);
      setProfiles((prev) => ({ ...prev, [childId]: updated }));
    } catch {
      setError("Couldn't reset that. Try again.");
    }
  }

  async function resetOnboarding(childId: string) {
    setConfirmResetId(null);
    try {
      const updated = await personalization.updateForChild(childId, { onboarded: false });
      setProfiles((prev) => ({ ...prev, [childId]: updated }));
    } catch {
      setError("Couldn't reset onboarding. Try again.");
    }
  }

  if (loading && children.length === 0) {
    return <p className="text-xs text-(--color-text-tertiary)">Loading children...</p>;
  }

  if (children.length === 0) {
    return <p className="text-sm text-(--color-text-secondary)">No children to show.</p>;
  }

  return (
    <div className="space-y-3">
      {error && (
        <div className="text-xs text-(--color-danger) bg-(--color-danger-light) rounded-xl px-3 py-2">
          {error}
        </div>
      )}
      {children.map((c) => {
        const p = profiles[c.id];
        const out = p?.out_of_policy ?? [];
        const summary = p
          ? buildSummary(p)
          : "Profile not yet loaded.";
        return (
          <div
            key={c.id}
            className="bg-(--color-surface) border border-(--color-border) rounded-2xl p-4 space-y-3"
          >
            <div className="flex items-start justify-between gap-3 flex-wrap">
              <div className="min-w-0">
                <h4 className="text-sm font-semibold text-(--color-text)">{c.first_name}</h4>
                <p className="text-xs text-(--color-text-secondary) mt-0.5 break-words">{summary}</p>
              </div>
              {confirmResetId === c.id ? (
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => setConfirmResetId(null)}
                    className="text-xs px-3 py-2 rounded-xl border border-(--color-border) text-(--color-text) min-h-[36px]"
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    onClick={() => void resetOnboarding(c.id)}
                    className="text-xs px-3 py-2 rounded-xl bg-(--color-danger) text-white min-h-[36px]"
                  >
                    Confirm
                  </button>
                </div>
              ) : (
                <button
                  type="button"
                  onClick={() => setConfirmResetId(c.id)}
                  className="shrink-0 text-xs text-(--color-text-secondary) hover:text-(--color-text) underline underline-offset-2 min-h-[36px] px-2"
                >
                  Reset onboarding
                </button>
              )}
            </div>

            {out.length > 0 && (
              <ul className="space-y-1.5">
                {out.map((field) => {
                  const label = FIELD_LABELS[field] ?? field;
                  const value =
                    field === "interest_tags"
                      ? (p?.interest_tags ?? []).join(", ") || "none"
                      : String((p as unknown as Record<string, unknown> | undefined)?.[field] ?? "");
                  const canReset = field === "interest_tags" || typeof DEFAULTS[field] === "string";
                  return (
                    <li
                      key={field}
                      className="flex items-center justify-between gap-3 text-xs bg-(--color-warning-light) border border-(--color-warning)/20 rounded-xl px-3 py-2"
                    >
                      <span className="text-(--color-warning) min-w-0 truncate">
                        <span className="font-semibold">{label}</span>
                        {value && <> ({value})</>} is no longer allowed.
                      </span>
                      {canReset && (
                        <button
                          type="button"
                          onClick={() => void resetField(c.id, field as keyof ChildPersonalization)}
                          className="shrink-0 text-xs font-medium text-(--color-accent) hover:underline min-h-[36px] px-2"
                        >
                          Reset to default
                        </button>
                      )}
                    </li>
                  );
                })}
              </ul>
            )}
          </div>
        );
      })}
    </div>
  );
}

function buildSummary(p: ChildPersonalization): string {
  const parts: string[] = [];
  parts.push(`Companion: ${p.companion_name || "unnamed"}`);
  parts.push(`Vibe: ${cap(p.vibe)}`);
  if (p.interest_tags.length > 0) {
    const sample = p.interest_tags.slice(0, 3).join(", ");
    parts.push(
      p.interest_tags.length > 3
        ? `Interests: ${sample}, +${p.interest_tags.length - 3} more`
        : `Interests: ${sample}`,
    );
  } else {
    parts.push("Interests: none picked");
  }
  return parts.join(" · ");
}

function cap(s: string): string {
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : "";
}
