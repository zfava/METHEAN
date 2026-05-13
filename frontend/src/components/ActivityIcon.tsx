"use client";

import { useEffect, useState } from "react";

import { usePersonalization } from "@/lib/PersonalizationProvider";

export type ActivityType =
  | "lesson"
  | "practice"
  | "review"
  | "assessment"
  | "project"
  | "field_trip";

interface ActivityIconProps {
  type: ActivityType;
  size?: number;
  className?: string;
  /** Renders a specific pack instead of the active profile's. Useful
   *  for picker previews. */
  packOverride?: string;
}

const ACTIVITY_LABELS: Record<ActivityType, string> = {
  lesson: "Lesson",
  practice: "Practice",
  review: "Review",
  assessment: "Assessment",
  project: "Project",
  field_trip: "Field trip",
};

const KNOWN_PACKS = new Set<string>(["default", "orbit", "field", "workshop", "studio"]);

// Module-level cache: pack/type -> SVG markup. The 30 assets are
// static so we never refetch within a session. Misses fall back to
// the default pack and the resolved markup is cached under both
// keys so subsequent reads short-circuit.
const svgCache = new Map<string, string>();
// Tracks in-flight fetches so two simultaneous mounts of the same
// icon collapse into a single request.
const inflight = new Map<string, Promise<string | null>>();

async function fetchSvg(pack: string, type: ActivityType): Promise<string | null> {
  const key = `${pack}/${type}`;
  const cached = svgCache.get(key);
  if (cached) return cached;
  const pending = inflight.get(key);
  if (pending) return pending;
  const job = (async () => {
    try {
      const resp = await fetch(`/icons/${key}.svg`);
      if (!resp.ok) return null;
      const text = await resp.text();
      svgCache.set(key, text);
      return text;
    } catch {
      return null;
    } finally {
      inflight.delete(key);
    }
  })();
  inflight.set(key, job);
  return job;
}

/**
 * Renders the active iconography pack's icon for an activity type.
 *
 * SVGs live under /public/icons/<pack>/<type>.svg, use
 * stroke="currentColor", and are injected inline so the consuming
 * element's text color drives the stroke. Unknown packs and missing
 * files fall back to the default pack so a stale or out-of-policy
 * profile never paints a missing-image broken box.
 */
export function ActivityIcon({
  type,
  size = 20,
  className,
  packOverride,
}: ActivityIconProps) {
  const { profile } = usePersonalization();
  const requested = packOverride || profile.iconography_pack || "default";
  const pack = KNOWN_PACKS.has(requested) ? requested : "default";

  const [markup, setMarkup] = useState<string | null>(() => svgCache.get(`${pack}/${type}`) ?? null);

  useEffect(() => {
    let cancelled = false;
    const cacheKey = `${pack}/${type}`;
    const cached = svgCache.get(cacheKey);
    if (cached) {
      setMarkup(cached);
      return;
    }
    void fetchSvg(pack, type).then(async (resolved) => {
      if (cancelled) return;
      if (resolved) {
        setMarkup(resolved);
        return;
      }
      // Fall through to the default pack so an empty slot never
      // ships, even if the kid's pack is briefly out of sync.
      if (pack !== "default") {
        const fallback = await fetchSvg("default", type);
        if (!cancelled && fallback) setMarkup(fallback);
      }
    });
    return () => {
      cancelled = true;
    };
  }, [pack, type]);

  const label = ACTIVITY_LABELS[type];

  if (!markup) {
    // Reserve the layout slot during the brief fetch so cards
    // don't jump when the icon arrives.
    return (
      <span
        aria-hidden="true"
        style={{ width: size, height: size, display: "inline-block" }}
        className={className}
      />
    );
  }

  // Normalize width/height to the requested size while keeping the
  // 24x24 viewBox intact, then inject. The SVG source is shipped by
  // us as a static asset; there is no user-supplied content path.
  const sized = markup
    .replace(/width="[^"]*"/, `width="${size}"`)
    .replace(/height="[^"]*"/, `height="${size}"`);

  return (
    <span
      role="img"
      aria-label={label}
      style={{ width: size, height: size, display: "inline-block", lineHeight: 0 }}
      className={className}
      dangerouslySetInnerHTML={{ __html: sized }}
    />
  );
}

export default ActivityIcon;
