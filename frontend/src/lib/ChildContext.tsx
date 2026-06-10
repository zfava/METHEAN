"use client";

import { createContext, useCallback, useContext, useEffect, useState } from "react";

interface ChildInfo {
  id: string;
  first_name: string;
  last_name: string | null;
  grade_level: string | null;
  enrollment_count: number;
  curriculum_philosophy?: string;
  subject_philosophies?: Record<string, string>;
  preferences?: {
    subject_levels?: Record<string, string>;
    daily_duration_minutes?: number | null;
    parent_notes?: string | null;
  } | null;
}

interface ChildContextValue {
  children: ChildInfo[];
  selectedChild: ChildInfo | null;
  setSelectedChild: (child: ChildInfo) => void;
  loading: boolean;
  /** Re-fetch /children. Use after any mutation whose result should
   *  appear in the cached child list (e.g., Learning Profile save). */
  refresh: () => Promise<void>;
  /** True while the session is child-scoped (kid mode). Derived from
   *  the non-HttpOnly kid_mode cookie the server sets on enter; the
   *  HttpOnly token's scope claim is what the server actually
   *  enforces, so this is render state, never authority. */
  kidMode: boolean;
  /** Re-read the kid_mode cookie after an enter/exit call. */
  refreshKidMode: () => void;
}

/** Read the kid_mode marker cookie. Exported for layouts that need a
 *  cookie check without mounting the provider. */
export function readKidModeCookie(): boolean {
  if (typeof document === "undefined") return false;
  return /(?:^|; )kid_mode=1(?:;|$)/.test(document.cookie);
}

const ChildContext = createContext<ChildContextValue>({
  children: [],
  selectedChild: null,
  setSelectedChild: () => {},
  loading: true,
  refresh: async () => {},
  kidMode: false,
  refreshKidMode: () => {},
});

export function useChild() {
  return useContext(ChildContext);
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export function ChildProvider({ children: reactChildren }: { children: React.ReactNode }) {
  const [childList, setChildList] = useState<ChildInfo[]>([]);
  const [selected, setSelected] = useState<ChildInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [kidMode, setKidMode] = useState(false);

  const fetchChildren = useCallback(async (): Promise<ChildInfo[]> => {
    try {
      const r = await fetch(`${API_BASE}/children`, { credentials: "include" });
      if (!r.ok) return [];
      return (await r.json()) as ChildInfo[];
    } catch {
      return [];
    }
  }, []);

  const refreshKidMode = useCallback(() => {
    setKidMode(readKidModeCookie());
  }, []);

  useEffect(() => {
    refreshKidMode();
    fetchChildren()
      .then((data) => {
        setChildList(data);
        if (data.length > 0 && !selected) {
          setSelected(data[0]);
        }
      })
      .finally(() => setLoading(false));
  }, [fetchChildren, refreshKidMode]);

  const refresh = useCallback(async () => {
    const data = await fetchChildren();
    setChildList(data);
    // Keep the current selection if it still exists; otherwise pick
    // the first child. Re-pinning by id preserves any updated fields
    // (e.g., preferences) that came back in the new payload.
    setSelected((prev) => {
      if (!prev) return data[0] ?? null;
      return data.find((c) => c.id === prev.id) ?? data[0] ?? null;
    });
  }, [fetchChildren]);

  const selectChild = useCallback((child: ChildInfo) => {
    setSelected(child);
  }, []);

  return (
    <ChildContext.Provider
      value={{
        children: childList,
        selectedChild: selected,
        setSelectedChild: selectChild,
        loading,
        refresh,
        kidMode,
        refreshKidMode,
      }}
    >
      {reactChildren}
    </ChildContext.Provider>
  );
}
