"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
  type ReactNode,
} from "react";

import { personalization as personalizationApi } from "@/lib/api";
import type {
  ChildPersonalization,
  PersonalizationLibrary,
} from "@/lib/personalization-types";

interface PersonalizationContextValue {
  /** Never undefined. Falls back to safe defaults during load. */
  profile: ChildPersonalization;
  /** Null during the very first library fetch. */
  library: PersonalizationLibrary | null;
  loading: boolean;
  error: Error | null;
  /** Optimistic update with rollback on PUT failure. */
  updateProfile: (patch: Partial<ChildPersonalization>) => Promise<void>;
  refetch: () => Promise<void>;
}

function defaultProfile(childId: string): ChildPersonalization {
  return {
    child_id: childId,
    companion_name: "",
    companion_voice: "",
    vibe: "calm",
    iconography_pack: "default",
    sound_pack: "soft",
    affirmation_tone: "warm",
    interest_tags: [],
    out_of_policy: [],
    onboarded: false,
  };
}

const PersonalizationContext = createContext<PersonalizationContextValue | null>(null);

export function PersonalizationProvider({
  childId,
  children,
}: {
  childId: string;
  children: ReactNode;
}) {
  const [profile, setProfile] = useState<ChildPersonalization>(() => defaultProfile(childId));
  const [library, setLibrary] = useState<PersonalizationLibrary | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  // Track in-flight optimistic updates so a race between two PUTs
  // doesn't corrupt the rollback target.
  const pendingRollback = useRef<ChildPersonalization | null>(null);

  // The library is session-stable so we fetch it once on mount and
  // never refetch on child change. A 404 or transport error degrades
  // gracefully; null `library` is a valid state and consumers handle it.
  useEffect(() => {
    let cancelled = false;
    personalizationApi
      .library()
      .then((lib) => {
        if (!cancelled) setLibrary(lib);
      })
      .catch((err: Error) => {
        if (!cancelled) setError(err);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const loadProfile = useCallback(
    async (signal?: AbortSignal): Promise<void> => {
      if (!childId) return;
      setLoading(true);
      try {
        const next = await personalizationApi.getForChild(childId);
        if (!signal?.aborted) {
          setProfile(next);
          setError(null);
        }
      } catch (err) {
        if (!signal?.aborted) setError(err as Error);
      } finally {
        if (!signal?.aborted) setLoading(false);
      }
    },
    [childId],
  );

  // Reset to defaults whenever childId changes so a stale profile from
  // the previous child can't flash on screen during the new fetch.
  useEffect(() => {
    setProfile(defaultProfile(childId));
    const controller = new AbortController();
    void loadProfile(controller.signal);
    return () => controller.abort();
  }, [childId, loadProfile]);

  const updateProfile = useCallback(
    async (patch: Partial<ChildPersonalization>): Promise<void> => {
      pendingRollback.current = profile;
      // Optimistic merge. The PUT echoes the resolved profile back,
      // which we trust over our local merge once it arrives.
      setProfile((prev) => ({ ...prev, ...patch }));
      try {
        const resolved = await personalizationApi.updateForChild(childId, patch);
        setProfile(resolved);
        setError(null);
      } catch (err) {
        if (pendingRollback.current) {
          setProfile(pendingRollback.current);
        }
        setError(err as Error);
        throw err;
      } finally {
        pendingRollback.current = null;
      }
    },
    [childId, profile],
  );

  const refetch = useCallback(async () => {
    await loadProfile();
  }, [loadProfile]);

  const value: PersonalizationContextValue = {
    profile,
    library,
    loading,
    error,
    updateProfile,
    refetch,
  };

  return (
    <PersonalizationContext.Provider value={value}>{children}</PersonalizationContext.Provider>
  );
}

export function usePersonalization(): PersonalizationContextValue {
  const ctx = useContext(PersonalizationContext);
  if (!ctx) {
    throw new Error(
      "usePersonalization must be used inside a <PersonalizationProvider>.",
    );
  }
  return ctx;
}
