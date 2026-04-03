"use client";

import { createContext, useCallback, useContext, useEffect, useState } from "react";

interface ChildInfo {
  id: string;
  first_name: string;
  last_name: string | null;
  grade_level: string | null;
  enrollment_count: number;
}

interface ChildContextValue {
  children: ChildInfo[];
  selectedChild: ChildInfo | null;
  setSelectedChild: (child: ChildInfo) => void;
  loading: boolean;
}

const ChildContext = createContext<ChildContextValue>({
  children: [],
  selectedChild: null,
  setSelectedChild: () => {},
  loading: true,
});

export function useChild() {
  return useContext(ChildContext);
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export function ChildProvider({ children: reactChildren }: { children: React.ReactNode }) {
  const [childList, setChildList] = useState<ChildInfo[]>([]);
  const [selected, setSelected] = useState<ChildInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/children`, { credentials: "include" })
      .then((r) => (r.ok ? r.json() : []))
      .then((data: ChildInfo[]) => {
        setChildList(data);
        if (data.length > 0 && !selected) {
          setSelected(data[0]);
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

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
      }}
    >
      {reactChildren}
    </ChildContext.Provider>
  );
}
