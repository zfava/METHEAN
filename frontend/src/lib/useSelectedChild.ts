"use client";

import { useEffect, useRef, useState } from "react";

import { auth, children as childrenApi } from "@/lib/api";

interface ChildInfo {
  id: string;
  first_name: string;
  grade_level: string | null;
}

interface UseSelectedChildResult {
  /** First active child in the household, or "" before load completes. */
  selectedId: string;
  /** Full list, in API order. */
  childrenList: ChildInfo[];
  loading: boolean;
  /** True when the auth check returned 401. */
  unauthenticated: boolean;
  /** Replace the selected child (used by the multi-child switcher). */
  setSelectedId: (id: string) => void;
}

/**
 * Shared child-selection logic for the /child route.
 *
 * Mirrors the bespoke loader that used to live inside
 * `/app/child/page.tsx`: authenticates, lists children, picks the
 * first one by default. Exposed as a hook so the route's wrapping
 * layout (which needs to seed the PersonalizationProvider with a
 * child id) and the page itself (which renders the multi-child
 * switcher) can both read the same selection without duplicating
 * the fetch.
 *
 * Concurrent mounts within the same render tree both fire `auth.me`
 * and `children.list`; the calls are cheap and React 19 will fold
 * them together with the request layer's GET retry guard.
 */
export function useSelectedChild(): UseSelectedChildResult {
  const [childrenList, setChildrenList] = useState<ChildInfo[]>([]);
  const [selectedId, setSelectedIdState] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);
  const [unauthenticated, setUnauthenticated] = useState<boolean>(false);
  const initialised = useRef<boolean>(false);

  useEffect(() => {
    if (initialised.current) return;
    initialised.current = true;
    let cancelled = false;
    (async () => {
      try {
        await auth.me();
        const data = (await childrenApi.list()) as unknown as ChildInfo[];
        if (cancelled) return;
        setChildrenList(Array.isArray(data) ? data : []);
        if (Array.isArray(data) && data.length > 0) {
          setSelectedIdState(data[0].id);
        }
      } catch (err: unknown) {
        const status = (err as { status?: number } | null)?.status;
        if (status === 401) {
          if (!cancelled) setUnauthenticated(true);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return {
    selectedId,
    childrenList,
    loading,
    unauthenticated,
    setSelectedId: setSelectedIdState,
  };
}
