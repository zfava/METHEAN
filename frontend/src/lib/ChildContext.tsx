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
}

const ChildContext = createContext<ChildContextValue>({
  children: [],
  selectedChild: null,
  setSelectedChild: () => {},
  loading: true,
  refresh: async () => {},
});

export function useChild() {
  return useContext(ChildContext);
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export function ChildProvider({ children: reactChildren }: { children: React.ReactNode }) {
  const [childList, setChildList] = useState<ChildInfo[]>([]);
  const [selected, setSelected] = useState<ChildInfo | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchChildren = useCallback(async (): Promise<ChildInfo[]> => {
    try {
      const r = await fetch(`${API_BASE}/children`, { credentials: "include" });
      if (!r.ok) return [];
      return (await r.json()) as ChildInfo[];
    } catch {
      return [];
    }
  }, []);

  useEffect(() => {
    fetchChildren()
      .then((data) => {
        setChildList(data);
        if (data.length > 0 && !selected) {
          setSelected(data[0]);
        }
      })
      .finally(() => setLoading(false));
  }, [fetchChildren]);

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
      }}
    >
      {reactChildren}
    </ChildContext.Provider>
  );
}
