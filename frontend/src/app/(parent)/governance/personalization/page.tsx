"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import { ActivityIcon, type ActivityType } from "@/components/ActivityIcon";
import { CompanionAvatar } from "@/components/CompanionAvatar";
import { AffectedChildrenPanel } from "@/components/governance/AffectedChildrenPanel";
import { PolicyChecklist } from "@/components/governance/PolicyChecklist";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import PageHeader from "@/components/ui/PageHeader";
import { auth, personalization } from "@/lib/api";
import type {
  AffirmationTone,
  IconographyPack,
  InterestTag,
  PersonalizationLibrary,
  PersonalizationPolicy,
  SoundPack,
  Vibe,
  VoicePersona,
} from "@/lib/personalization-types";

type SectionKey =
  | "vibes"
  | "interest_tags"
  | "voice_personas"
  | "iconography_packs"
  | "sound_packs"
  | "affirmation_tones";

const SECTIONS: { key: SectionKey; label: string; description: string }[] = [
  { key: "vibes", label: "Vibes", description: "Page colors, surfaces, and rhythm." },
  { key: "interest_tags", label: "Interest tags", description: "Topics the AI weaves into examples." },
  { key: "voice_personas", label: "Companion personas", description: "Tone and presence of the AI buddy." },
  { key: "iconography_packs", label: "Icon packs", description: "Activity glyph styles." },
  { key: "sound_packs", label: "Sound packs", description: "Audio cues for activity events." },
  { key: "affirmation_tones", label: "Affirmation tones", description: "How the AI talks back during activities." },
];

const INTEREST_CATEGORY_LABELS: Record<string, string> = {
  nature_animals: "Nature and animals",
  space_science: "Space and science",
  vehicles: "Vehicles",
  sports_movement: "Sports and movement",
  arts_music: "Arts and music",
  fantasy_history: "Fantasy and history",
  building_making: "Building and making",
  food_cooking: "Food and cooking",
  everyday_world: "Everyday world",
};

const TONE_SAMPLES: Record<string, string> = {
  warm: "Solid work. I can tell you're getting this.",
  direct: "Correct. Next one.",
  playful: "Nailed it. Onward, captain.",
};

export default function PersonalizationPolicyPage() {
  const router = useRouter();
  const [library, setLibrary] = useState<PersonalizationLibrary | null>(null);
  const [policy, setPolicy] = useState<PersonalizationPolicy | null>(null);
  const [pending, setPending] = useState<Partial<PersonalizationPolicy> | null>(null);
  const [open, setOpen] = useState<SectionKey | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retryNonce, setRetryNonce] = useState(0);
  const [observer, setObserver] = useState(false);
  const [childrenRefreshKey, setChildrenRefreshKey] = useState(0);

  useEffect(() => {
    document.title = "Personalization | METHEAN";
  }, []);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const me = await auth.me();
      // Guardians only. Observers can land here by URL; the parent
      // backend rejects mutations with 403, but we hide the form so
      // they aren't tempted to try.
      const role = (me as { role?: string })?.role;
      setObserver(role === "observer");
      const [lib, pol] = await Promise.all([
        personalization.library(),
        personalization.getPolicy(),
      ]);
      setLibrary(lib);
      setPolicy(pol);
    } catch (e) {
      const detail = (e as { detail?: string; message?: string } | null);
      setError(detail?.detail ?? detail?.message ?? "Couldn't load personalization policy.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load, retryNonce]);

  // Optimistic update: apply the patch to local state, fire the
  // PUT, and roll back on failure. `pending` shadows the policy
  // for the in-flight write so concurrent toggles all merge against
  // the latest pre-write snapshot.
  const updatePolicy = useCallback(
    async (patch: Partial<PersonalizationPolicy>) => {
      if (!policy) return;
      const prior = policy;
      const optimistic: PersonalizationPolicy = { ...policy, ...patch };
      setPolicy(optimistic);
      setPending(patch);
      try {
        const updated = await personalization.updatePolicy(patch);
        setPolicy(updated);
        setError(null);
        setChildrenRefreshKey((k) => k + 1);
      } catch (e) {
        setPolicy(prior);
        const detail = (e as { detail?: string; message?: string } | null);
        setError(
          detail?.detail ?? detail?.message ?? "Couldn't save that change. Try again.",
        );
      } finally {
        setPending(null);
      }
    },
    [policy],
  );

  const counts = useMemo(() => {
    if (!library || !policy) return null;
    function expand(allowed: string[], full: string[]): number {
      if (allowed.length === 1 && allowed[0] === "*") return full.length;
      return new Set(allowed).size;
    }
    return {
      vibes: { sel: expand(policy.allowed_vibes, library.vibes.map((v) => v.id)), tot: library.vibes.length },
      interest_tags: { sel: expand(policy.allowed_interest_tags, library.interest_tags.map((t) => t.id)), tot: library.interest_tags.length },
      voice_personas: { sel: expand(policy.allowed_voice_personas, library.voice_personas.map((p) => p.id)), tot: library.voice_personas.length },
      iconography_packs: { sel: expand(policy.allowed_iconography_packs, library.iconography_packs.map((p) => p.id)), tot: library.iconography_packs.length },
      sound_packs: { sel: expand(policy.allowed_sound_packs, library.sound_packs.map((p) => p.id)), tot: library.sound_packs.length },
      affirmation_tones: { sel: expand(policy.allowed_affirmation_tones, library.affirmation_tones.map((t) => t.id)), tot: library.affirmation_tones.length },
    };
  }, [library, policy]);

  if (loading) {
    return (
      <div className="max-w-3xl">
        <PageHeader title="Personalization" />
        <LoadingSkeleton variant="card" count={4} />
      </div>
    );
  }

  if (observer) {
    return (
      <div className="max-w-3xl">
        <PageHeader title="Personalization" />
        <Card>
          <p className="text-sm text-(--color-text-secondary)">
            Observers can&apos;t edit the personalization policy. Ask an owner or co-parent.
          </p>
        </Card>
      </div>
    );
  }

  if (!library || !policy || !counts) {
    return (
      <div className="max-w-3xl">
        <PageHeader title="Personalization" />
        <Card borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-3">
            <p className="text-sm text-(--color-danger)">{error ?? "Couldn't load personalization policy."}</p>
            <Button variant="ghost" size="sm" onClick={() => setRetryNonce((n) => n + 1)}>
              Retry
            </Button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-3xl">
      <PageHeader
        title="Personalization"
        subtitle="Curate what your kids can pick from."
      />

      <Card className="mb-4">
        <p className="text-sm text-(--color-text-secondary) leading-relaxed">
          Your kids choose how their app looks, sounds, and feels from a library you control.
          Toggle items off to remove them from your kids&apos; picker. Toggle them on to allow them.
        </p>
      </Card>

      {error && (
        <Card className="mb-4" borderLeft="border-l-(--color-danger)">
          <div className="flex items-center justify-between gap-3">
            <p className="text-sm text-(--color-danger)">{error}</p>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => {
                setError(null);
                void load();
              }}
            >
              Retry
            </Button>
          </div>
        </Card>
      )}

      <div className="space-y-2.5 mb-6">
        {SECTIONS.map((s) => (
          <AccordionSection
            key={s.key}
            label={s.label}
            description={s.description}
            count={counts[s.key]}
            isOpen={open === s.key}
            onToggle={() => setOpen((cur) => (cur === s.key ? null : s.key))}
          >
            {s.key === "vibes" && (
              <PolicyChecklist<Vibe>
                title="Vibes"
                items={library.vibes}
                allowedIds={policy.allowed_vibes}
                onChange={(next) => void updatePolicy({ allowed_vibes: next })}
                renderPreview={(v) => <VibeSwatch v={v} />}
              />
            )}
            {s.key === "interest_tags" && (
              <PolicyChecklist<InterestTag>
                title="Interest tags"
                items={library.interest_tags}
                allowedIds={policy.allowed_interest_tags}
                onChange={(next) => void updatePolicy({ allowed_interest_tags: next })}
                renderPreview={(t) => <InterestBadge tag={t} />}
                groupBy="category"
                groupLabels={INTEREST_CATEGORY_LABELS}
                searchable
              />
            )}
            {s.key === "voice_personas" && (
              <PolicyChecklist<VoicePersona>
                title="Companion personas"
                items={library.voice_personas}
                allowedIds={policy.allowed_voice_personas}
                onChange={(next) => void updatePolicy({ allowed_voice_personas: next })}
                renderPreview={(p) => (
                  <span className="text-(--color-accent)">
                    <CompanionAvatar personaId={p.id} size={24} />
                  </span>
                )}
              />
            )}
            {s.key === "iconography_packs" && (
              <PolicyChecklist<IconographyPack>
                title="Icon packs"
                items={library.iconography_packs}
                allowedIds={policy.allowed_iconography_packs}
                onChange={(next) => void updatePolicy({ allowed_iconography_packs: next })}
                renderPreview={(p) => <IconographyMiniRow packId={p.id} />}
              />
            )}
            {s.key === "sound_packs" && (
              <PolicyChecklist<SoundPack>
                title="Sound packs"
                items={library.sound_packs}
                allowedIds={policy.allowed_sound_packs}
                onChange={(next) => void updatePolicy({ allowed_sound_packs: next })}
                renderPreview={(p) => <SoundSampleButton packId={p.id} />}
              />
            )}
            {s.key === "affirmation_tones" && (
              <PolicyChecklist<AffirmationTone>
                title="Affirmation tones"
                items={library.affirmation_tones}
                allowedIds={policy.allowed_affirmation_tones}
                onChange={(next) => void updatePolicy({ allowed_affirmation_tones: next })}
                renderPreview={(t) => <ToneSampleLine toneId={t.id} />}
              />
            )}
          </AccordionSection>
        ))}
      </div>

      {/* Companion names + max interests */}
      <Card className="mb-6">
        <h3 className="text-sm font-semibold text-(--color-text) mb-3">Companion names and limits</h3>
        <div className="space-y-4">
          <label className="flex items-start justify-between gap-3 cursor-pointer">
            <span className="min-w-0">
              <span className="text-sm text-(--color-text) block">Require my review of companion names</span>
              <span className="text-[11px] text-(--color-text-tertiary) leading-snug">
                The kid&apos;s chosen name is held pending until you approve it.
              </span>
            </span>
            <input
              type="checkbox"
              checked={policy.companion_name_requires_review}
              onChange={(e) =>
                void updatePolicy({ companion_name_requires_review: e.target.checked })
              }
              className="mt-1 w-4 h-4 accent-(--color-accent)"
            />
          </label>

          <div className="flex items-center justify-between gap-3">
            <span className="min-w-0">
              <span className="text-sm text-(--color-text) block">Maximum interests per child</span>
              <span className="text-[11px] text-(--color-text-tertiary) leading-snug">
                Between 1 and 15.
              </span>
            </span>
            <input
              type="number"
              min={1}
              max={15}
              value={policy.max_interest_tags_per_child}
              onChange={(e) => {
                const next = Math.max(1, Math.min(15, Number(e.target.value) || 1));
                if (next === policy.max_interest_tags_per_child) return;
                void updatePolicy({ max_interest_tags_per_child: next });
              }}
              className="w-20 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text) text-right"
              aria-label="Maximum interests per child"
            />
          </div>

          {pending && (
            <p className="text-[11px] text-(--color-text-tertiary)">Saving...</p>
          )}
        </div>
      </Card>

      {/* Voice */}
      <Card className="mb-6">
        <h3 className="text-sm font-semibold text-(--color-text) mb-3">Voice</h3>
        <p className="text-xs text-(--color-text-secondary) leading-relaxed mb-4">
          Kids can speak instead of typing. Audio never leaves memory; the
          transcript replaces nothing your kid wrote and the safety check runs
          before any text returns.
        </p>
        <div className="space-y-4">
          <label className="flex items-start justify-between gap-3 cursor-pointer">
            <span className="min-w-0">
              <span className="text-sm text-(--color-text) block">Allow voice input</span>
              <span className="text-[11px] text-(--color-text-tertiary) leading-snug">
                Microphone in every textarea, capped daily per child.
              </span>
            </span>
            <input
              type="checkbox"
              checked={policy.voice_input_enabled}
              onChange={(e) => void updatePolicy({ voice_input_enabled: e.target.checked })}
              className="mt-1 w-4 h-4 accent-(--color-accent)"
            />
          </label>

          <div className="flex items-center justify-between gap-3">
            <span className="min-w-0">
              <span className="text-sm text-(--color-text) block">Voice minutes per child per day</span>
              <span className="text-[11px] text-(--color-text-tertiary) leading-snug">0 to 480.</span>
            </span>
            <input
              type="number"
              min={0}
              max={480}
              value={policy.voice_minutes_daily_cap}
              onChange={(e) => {
                const next = Math.max(0, Math.min(480, Number(e.target.value) || 0));
                if (next === policy.voice_minutes_daily_cap) return;
                void updatePolicy({ voice_minutes_daily_cap: next });
              }}
              className="w-20 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text) text-right"
              aria-label="Voice minutes per child per day"
            />
          </div>

          <div>
            <span className="text-sm text-(--color-text) block mb-2">Transcription provider</span>
            <div className="flex gap-2">
              {(["openai", "local"] as const).map((p) => (
                <button
                  key={p}
                  type="button"
                  onClick={() => void updatePolicy({ whisper_provider: p })}
                  className={[
                    "px-3 py-2 text-xs rounded-full border min-h-[36px]",
                    policy.whisper_provider === p
                      ? "border-(--color-brand-gold) bg-(--color-accent-light) text-(--color-text) font-medium"
                      : "border-(--color-border) text-(--color-text-secondary)",
                  ].join(" ")}
                >
                  {p === "openai" ? "OpenAI (cloud)" : "Local Whisper (homestead)"}
                </button>
              ))}
            </div>
            <p className="text-[11px] text-(--color-text-tertiary) mt-1.5 leading-snug">
              The local option falls back to OpenAI automatically when the
              homestead service is unreachable.
            </p>
          </div>

          {/* Voice output (Sprint v2 Prompt 2) */}
          <div className="pt-3 border-t border-(--color-border)/60 mt-3">
            <h4 className="text-[11px] font-semibold uppercase tracking-[0.08em] text-(--color-text-secondary) mb-3">
              Voice output
            </h4>
            <div className="space-y-4">
              <label className="flex items-start justify-between gap-3 cursor-pointer">
                <span className="min-w-0">
                  <span className="text-sm text-(--color-text) block">Allow voice output</span>
                  <span className="text-[11px] text-(--color-text-tertiary) leading-snug">
                    Companion speaks tutor responses aloud in their persona voice.
                  </span>
                </span>
                <input
                  type="checkbox"
                  checked={policy.voice_output_enabled}
                  onChange={(e) => void updatePolicy({ voice_output_enabled: e.target.checked })}
                  className="mt-1 w-4 h-4 accent-(--color-accent)"
                />
              </label>

              <div className="flex items-center justify-between gap-3">
                <span className="min-w-0">
                  <span className="text-sm text-(--color-text) block">Voice output minutes per child per day</span>
                  <span className="text-[11px] text-(--color-text-tertiary) leading-snug">0 to 600.</span>
                </span>
                <input
                  type="number"
                  min={0}
                  max={600}
                  value={policy.voice_output_minutes_daily_cap}
                  onChange={(e) => {
                    const next = Math.max(0, Math.min(600, Number(e.target.value) || 0));
                    if (next === policy.voice_output_minutes_daily_cap) return;
                    void updatePolicy({ voice_output_minutes_daily_cap: next });
                  }}
                  className="w-20 px-3 py-2 text-sm border border-(--color-border) rounded-[10px] bg-(--color-surface) text-(--color-text) text-right"
                  aria-label="Voice output minutes per child per day"
                />
              </div>

              <div>
                <span className="text-sm text-(--color-text) block mb-2">TTS provider</span>
                <div className="flex gap-2">
                  {(["openai", "elevenlabs"] as const).map((p) => (
                    <button
                      key={p}
                      type="button"
                      onClick={() => void updatePolicy({ tts_provider: p })}
                      className={[
                        "px-3 py-2 text-xs rounded-full border min-h-[36px]",
                        policy.tts_provider === p
                          ? "border-(--color-brand-gold) bg-(--color-accent-light) text-(--color-text) font-medium"
                          : "border-(--color-border) text-(--color-text-secondary)",
                      ].join(" ")}
                    >
                      {p === "openai" ? "OpenAI (cloud)" : "ElevenLabs (premium)"}
                    </button>
                  ))}
                </div>
                <p className="text-[11px] text-(--color-text-tertiary) mt-1.5 leading-snug">
                  ElevenLabs requires a premium API key; selecting it without
                  one falls back to OpenAI for now.
                </p>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Affected children */}
      <section className="mb-10">
        <div className="flex items-baseline justify-between mb-3">
          <h3 className="text-[15px] font-semibold text-(--color-text)">Affected children</h3>
          <button
            type="button"
            onClick={() => router.push("/family")}
            className="text-xs text-(--color-text-secondary) hover:text-(--color-text) underline underline-offset-2"
          >
            Manage family
          </button>
        </div>
        <AffectedChildrenPanel refreshKey={childrenRefreshKey} />
      </section>
    </div>
  );
}

// ── Accordion (local, no shared component yet) ────────────────────

function AccordionSection({
  label,
  description,
  count,
  isOpen,
  onToggle,
  children,
}: {
  label: string;
  description: string;
  count: { sel: number; tot: number };
  isOpen: boolean;
  onToggle: () => void;
  children: React.ReactNode;
}) {
  return (
    <Card padding="p-0">
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={isOpen}
        className="w-full flex items-center gap-3 px-4 py-3.5 sm:px-5 text-left min-h-[44px]"
      >
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-semibold text-(--color-text)">{label}</h3>
          <p className="text-[11px] text-(--color-text-tertiary) leading-snug">{description}</p>
        </div>
        <span className="shrink-0 text-xs text-(--color-text-secondary) tabular-nums">
          {count.sel} of {count.tot} allowed
        </span>
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className={[
            "shrink-0 text-(--color-text-tertiary) transition-transform",
            isOpen ? "rotate-180" : "rotate-0",
          ].join(" ")}
        >
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </button>
      {isOpen && (
        <div className="px-4 pb-4 sm:px-5 border-t border-(--color-border)/60 pt-4">{children}</div>
      )}
    </Card>
  );
}

// ── Per-section preview renderers ────────────────────────────────

function VibeSwatch({ v }: { v: Vibe }) {
  return (
    <span
      aria-hidden="true"
      style={{
        width: 32,
        height: 32,
        display: "inline-block",
        borderRadius: 8,
        background: v.tokens["--color-page"],
        border: "1px solid var(--color-border)",
        position: "relative",
      }}
    >
      <span
        style={{
          position: "absolute",
          left: 4,
          bottom: 4,
          width: 14,
          height: 6,
          borderRadius: 3,
          background: v.tokens["--color-accent"],
        }}
      />
    </span>
  );
}

function InterestBadge({ tag }: { tag: InterestTag }) {
  return (
    <span
      aria-hidden="true"
      className="inline-flex items-center justify-center w-7 h-7 rounded-full bg-(--color-page) border border-(--color-border) text-[10px] font-bold text-(--color-text-secondary)"
    >
      {tag.icon_keyword.charAt(0).toUpperCase()}
    </span>
  );
}

const ICON_PREVIEW_ORDER: ActivityType[] = [
  "lesson",
  "practice",
  "review",
  "assessment",
  "project",
  "field_trip",
];

function IconographyMiniRow({ packId }: { packId: string }) {
  return (
    <span className="inline-flex items-center gap-1 text-(--color-text-secondary)" aria-hidden="true">
      {ICON_PREVIEW_ORDER.map((t) => (
        <ActivityIcon key={t} type={t} packOverride={packId} size={14} />
      ))}
    </span>
  );
}

function SoundSampleButton({ packId }: { packId: string }) {
  const isOff = packId === "off";
  return (
    <button
      type="button"
      disabled={isOff}
      onClick={(e) => {
        e.preventDefault();
        e.stopPropagation();
        if (isOff) return;
        try {
          const audio = new Audio(`/sounds/${packId}/correct.mp3`);
          audio.volume = 0.6;
          void audio.play().catch(() => {});
        } catch {
          // Ignore; sample is advisory.
        }
      }}
      className="text-xs font-medium text-(--color-accent) hover:underline min-h-[36px] px-2 disabled:opacity-40 disabled:hover:no-underline"
    >
      {isOff ? "No sound" : "Hear sample"}
    </button>
  );
}

function ToneSampleLine({ toneId }: { toneId: string }) {
  const line = TONE_SAMPLES[toneId] ?? "";
  return (
    <span className="text-[11px] italic text-(--color-text-secondary) max-w-[180px] truncate">
      {line ? `“${line}”` : ""}
    </span>
  );
}
