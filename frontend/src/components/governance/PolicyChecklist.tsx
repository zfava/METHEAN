"use client";

import { useMemo, useState, type ReactNode } from "react";

import type { LibraryEntry } from "@/lib/personalization-types";

interface PolicyChecklistProps<T extends LibraryEntry> {
  title: string;
  /** Full library, ordered as the kid sees them. */
  items: T[];
  /** Current policy value. ``["*"]`` is a sentinel meaning "any
   *  future library addition is automatically allowed". */
  allowedIds: string[];
  onChange: (nextAllowedIds: string[]) => void;
  /** Optional inline preview per row (avatar, swatch, etc.). */
  renderPreview?: (item: T) => ReactNode;
  /** Group items by a string-valued key. Useful for interest tags. */
  groupBy?: keyof T;
  searchable?: boolean;
  /** Human-readable mapping for group keys when groupBy is set. */
  groupLabels?: Record<string, string>;
}

/**
 * Reusable parent-side allowlist editor.
 *
 * Renders one row per library item with a checkbox, label, and an
 * optional inline preview. When the policy is the ``["*"]``
 * sentinel, the body collapses into a single "All allowed" pill
 * with a "Manage individually" conversion link; tapping that link
 * materializes the sentinel into the explicit ID list so the next
 * tap can begin disabling specific items.
 */
export function PolicyChecklist<T extends LibraryEntry>({
  title,
  items,
  allowedIds,
  onChange,
  renderPreview,
  groupBy,
  searchable,
  groupLabels,
}: PolicyChecklistProps<T>) {
  const [query, setQuery] = useState("");
  const isSentinel = allowedIds.length === 1 && allowedIds[0] === "*";
  const allowedSet = useMemo(() => new Set(allowedIds), [allowedIds]);

  function toggle(id: string) {
    if (isSentinel) return;
    if (allowedSet.has(id)) {
      onChange(allowedIds.filter((x) => x !== id));
    } else {
      onChange([...allowedIds, id]);
    }
  }

  function materializeSentinel() {
    onChange(items.map((i) => i.id));
  }

  const filtered = useMemo(() => {
    if (!searchable || !query.trim()) return items;
    const q = query.trim().toLowerCase();
    return items.filter((i) => i.label.toLowerCase().includes(q));
  }, [items, query, searchable]);

  const groups = useMemo(() => {
    if (!groupBy) return [["", filtered] as [string, T[]]];
    const map = new Map<string, T[]>();
    for (const item of filtered) {
      const key = String((item as unknown as Record<string, unknown>)[groupBy as string] ?? "");
      const list = map.get(key) ?? [];
      list.push(item);
      map.set(key, list);
    }
    return Array.from(map.entries());
  }, [filtered, groupBy]);

  if (isSentinel) {
    return (
      <div className="bg-(--color-success-light) border border-(--color-success)/20 rounded-2xl px-4 py-3 flex items-center justify-between gap-3">
        <div>
          <p className="text-sm font-medium text-(--color-success)">All allowed.</p>
          <p className="text-xs text-(--color-text-secondary) leading-snug mt-0.5">
            Any future {title.toLowerCase()} we ship will be enabled automatically.
          </p>
        </div>
        <button
          type="button"
          onClick={materializeSentinel}
          className="shrink-0 text-xs font-medium text-(--color-accent) hover:underline min-h-[36px] px-2"
        >
          Manage individually
        </button>
      </div>
    );
  }

  return (
    <div>
      {searchable && (
        <div className="mb-3">
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={`Search ${title.toLowerCase()}`}
            className="w-full px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text) placeholder:text-(--color-text-tertiary)"
            aria-label={`Search ${title.toLowerCase()}`}
          />
        </div>
      )}

      <div className="space-y-3">
        {groups.map(([groupKey, groupItems]) => (
          <div key={groupKey || "_root"}>
            {groupKey && (
              <h4 className="text-[11px] font-semibold uppercase tracking-[0.08em] text-(--color-text-secondary) mb-2">
                {groupLabels?.[groupKey] ?? groupKey.replace(/_/g, " ")}
              </h4>
            )}
            <ul className="space-y-1.5">
              {groupItems.map((item) => {
                const enabled = allowedSet.has(item.id);
                return (
                  <li key={item.id}>
                    <label
                      className={[
                        "flex items-center gap-3 px-3 py-2.5 rounded-xl border cursor-pointer min-h-[44px]",
                        "bg-(--color-surface)",
                        enabled
                          ? "border-(--color-border)"
                          : "border-(--color-border) opacity-60",
                      ].join(" ")}
                    >
                      <input
                        type="checkbox"
                        checked={enabled}
                        onChange={() => toggle(item.id)}
                        className="w-4 h-4 accent-(--color-accent) shrink-0"
                        aria-label={`Allow ${item.label}`}
                      />
                      {renderPreview && (
                        <span className="shrink-0 inline-flex items-center justify-center text-(--color-text-secondary)">
                          {renderPreview(item)}
                        </span>
                      )}
                      <span className="flex-1 min-w-0">
                        <span className="text-sm font-medium text-(--color-text) block">{item.label}</span>
                        {item.description && (
                          <span className="text-[11px] text-(--color-text-tertiary) line-clamp-2 leading-snug">
                            {item.description}
                          </span>
                        )}
                      </span>
                    </label>
                  </li>
                );
              })}
            </ul>
          </div>
        ))}
        {filtered.length === 0 && (
          <p className="text-xs text-(--color-text-tertiary) py-4 text-center">
            No matches.
          </p>
        )}
      </div>
    </div>
  );
}
