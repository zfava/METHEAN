"use client";

import { useEffect, useState, type ReactNode } from "react";
import { useRouter } from "next/navigation";

import BottomSheet from "@/components/BottomSheet";
import { CompanionAvatar } from "@/components/CompanionAvatar";
import { useToast } from "@/components/Toast";
import { IconographyPicker } from "@/components/child/pickers/IconographyPicker";
import { InterestChips } from "@/components/child/pickers/InterestChips";
import { PersonaPicker } from "@/components/child/pickers/PersonaPicker";
import { SoundPicker } from "@/components/child/pickers/SoundPicker";
import { TonePicker } from "@/components/child/pickers/TonePicker";
import { VibePicker } from "@/components/child/pickers/VibePicker";
import { usePersonalization } from "@/lib/PersonalizationProvider";
import { useMobile } from "@/lib/useMobile";
import type { ChildPersonalization, VoicePersona } from "@/lib/personalization-types";

interface MySpaceProps {
  open: boolean;
  onClose: () => void;
}

/**
 * The kid's personalization control panel.
 *
 * Every change persists immediately via updateProfile (optimistic;
 * on failure the provider already rolls the local profile back).
 * The same pickers used by the welcome flow drive the surfaces
 * here so the look is consistent across first-run and ongoing edits.
 *
 * Mobile: full-bleed BottomSheet. Desktop: a 560px centered modal
 * with a click-out backdrop.
 */
export function MySpace({ open, onClose }: MySpaceProps) {
  const { profile, library, updateProfile } = usePersonalization();
  const { toast } = useToast();
  const isMobile = useMobile();
  const router = useRouter();

  // Sub-flow modes that swap the body for an inline editor.
  const [mode, setMode] = useState<"main" | "edit_name" | "edit_buddy" | "confirm_reset">("main");
  const [pendingPersona, setPendingPersona] = useState<VoicePersona | null>(null);
  const [nameDraft, setNameDraft] = useState<string>(profile.companion_name);

  // Reset the local mode whenever the sheet opens.
  useEffect(() => {
    if (open) {
      setMode("main");
      setPendingPersona(null);
      setNameDraft(profile.companion_name);
    }
  }, [open, profile.companion_name]);

  async function patch(p: Partial<ChildPersonalization>) {
    try {
      await updateProfile(p);
    } catch {
      toast("Couldn't save that yet, will try again.", "info");
    }
  }

  async function resetEverything() {
    try {
      await updateProfile({
        onboarded: false,
        companion_name: "",
        companion_voice: "",
        vibe: "calm",
        iconography_pack: "default",
        sound_pack: "soft",
        affirmation_tone: "warm",
        interest_tags: [],
      });
    } catch {
      // The provider rolled back; route anyway since the kid asked
      // to restart and the welcome flow will repair state.
    }
    onClose();
    router.push("/child/welcome");
  }

  if (!library) {
    return isMobile ? (
      <BottomSheet open={open} onClose={onClose} label="My Space">
        <div className="px-5 py-12 flex justify-center">
          <div className="w-5 h-5 rounded-full border-2 border-(--color-accent) border-t-transparent animate-spin" />
        </div>
      </BottomSheet>
    ) : (
      <DesktopModal open={open} onClose={onClose}>
        <div className="px-6 py-16 flex justify-center">
          <div className="w-5 h-5 rounded-full border-2 border-(--color-accent) border-t-transparent animate-spin" />
        </div>
      </DesktopModal>
    );
  }

  const body = (
    <div className="px-5 pb-8 space-y-8">
      {/* Header */}
      <header className="pt-2">
        <h2 className="text-base font-semibold text-(--color-text)">My Space</h2>
      </header>

      {mode === "main" && (
        <>
          {/* Companion identity */}
          <section className="flex flex-col items-center gap-3 text-(--color-accent)">
            <CompanionAvatar personaId={profile.companion_voice || "default_warm"} size={96} />
            <div className="text-center">
              <div className="text-lg font-semibold text-(--color-text)">
                {profile.companion_name || "Your companion"}
              </div>
            </div>
            <div className="flex flex-wrap gap-2 justify-center">
              <button
                type="button"
                onClick={() => setMode("edit_name")}
                className="px-3 py-2 text-sm rounded-full border border-(--color-border) text-(--color-text) hover:bg-(--color-page) min-h-[44px]"
              >
                Change name
              </button>
              <button
                type="button"
                onClick={() => setMode("edit_buddy")}
                className="px-3 py-2 text-sm rounded-full border border-(--color-border) text-(--color-text) hover:bg-(--color-page) min-h-[44px]"
              >
                Change buddy
              </button>
            </div>
          </section>

          <Section title="Vibe">
            <VibePicker
              vibes={library.vibes}
              selectedId={profile.vibe}
              onSelect={(id) => void patch({ vibe: id })}
            />
          </Section>

          <Section title="Icons">
            <IconographyPicker
              packs={library.iconography_packs}
              selectedId={profile.iconography_pack}
              onSelect={(id) => void patch({ iconography_pack: id })}
            />
          </Section>

          <Section title="Interests">
            <InterestChips
              tags={library.interest_tags}
              selectedIds={profile.interest_tags}
              maxCount={library.max_interest_tags_per_child}
              onChange={(ids) => void patch({ interest_tags: ids })}
            />
          </Section>

          <Section title="Sound">
            <SoundPicker
              packs={library.sound_packs}
              selectedId={profile.sound_pack}
              onSelect={(id) => void patch({ sound_pack: id })}
            />
          </Section>

          <Section title="Tone">
            <TonePicker
              tones={library.affirmation_tones}
              selectedId={profile.affirmation_tone}
              onSelect={(id) => void patch({ affirmation_tone: id })}
            />
          </Section>

          <Section title="Voice mode style">
            <p className="text-xs text-(--color-text-secondary) leading-relaxed mb-3">
              How does the talk button work in voice mode?
            </p>
            <div className="grid grid-cols-2 gap-2">
              {([
                { id: "tap_toggle", label: "Tap to start, tap to stop", subline: "Easier" },
                { id: "press_hold", label: "Press and hold to talk", subline: "Like a walkie-talkie" },
              ] as const).map((opt) => {
                const selected =
                  ((profile as unknown as { voice_mode_style?: string }).voice_mode_style ?? "tap_toggle") === opt.id;
                return (
                  <button
                    key={opt.id}
                    type="button"
                    onClick={() =>
                      void patch({
                        ...(profile as Partial<typeof profile>),
                        // voice_mode_style is a JSONB extension field; the
                        // backend accepts arbitrary fields in personalization.
                        voice_mode_style: opt.id,
                      } as never)
                    }
                    className={[
                      "rounded-2xl border p-3 text-left min-h-[44px]",
                      selected
                        ? "ring-2 ring-(--color-brand-gold) border-(--color-brand-gold)"
                        : "border-(--color-border)",
                    ].join(" ")}
                  >
                    <div className="text-sm font-medium text-(--color-text)">{opt.label}</div>
                    <div className="text-[11px] text-(--color-text-tertiary)">{opt.subline}</div>
                  </button>
                );
              })}
            </div>
          </Section>

          <section className="pt-2">
            <button
              type="button"
              onClick={() => setMode("confirm_reset")}
              className="text-sm text-(--color-text-tertiary) hover:text-(--color-danger) underline underline-offset-2"
            >
              Start My Space over.
            </button>
          </section>
        </>
      )}

      {mode === "edit_name" && (
        <NameEditor
          initial={profile.companion_name}
          draft={nameDraft}
          onDraftChange={setNameDraft}
          onCancel={() => setMode("main")}
          onSave={async (next) => {
            await patch({ companion_name: next });
            setMode("main");
          }}
        />
      )}

      {mode === "edit_buddy" && (
        <BuddyEditor
          personas={library.voice_personas}
          currentVoice={profile.companion_voice}
          currentName={profile.companion_name}
          pendingPersona={pendingPersona}
          onPickPersona={setPendingPersona}
          onKeepName={async () => {
            if (!pendingPersona) return;
            await patch({ companion_voice: pendingPersona.id });
            setPendingPersona(null);
            setMode("main");
          }}
          onUseDefaultName={async () => {
            if (!pendingPersona) return;
            await patch({
              companion_voice: pendingPersona.id,
              companion_name: pendingPersona.default_companion_name,
            });
            setPendingPersona(null);
            setMode("main");
          }}
          onCancel={() => {
            setPendingPersona(null);
            setMode("main");
          }}
        />
      )}

      {mode === "confirm_reset" && (
        <ConfirmReset
          onCancel={() => setMode("main")}
          onConfirm={() => void resetEverything()}
        />
      )}
    </div>
  );

  if (isMobile) {
    return (
      <BottomSheet open={open} onClose={onClose} label="My Space">
        {body}
      </BottomSheet>
    );
  }
  return (
    <DesktopModal open={open} onClose={onClose}>
      {body}
    </DesktopModal>
  );
}

function Section({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section>
      <h3 className="text-[11px] font-semibold uppercase tracking-[0.08em] text-(--color-text-secondary) mb-3">
        {title}
      </h3>
      {children}
    </section>
  );
}

function DesktopModal({
  open,
  onClose,
  children,
}: {
  open: boolean;
  onClose: () => void;
  children: ReactNode;
}) {
  // Close on Escape; trap focus is delegated to BottomSheet on
  // mobile so we don't duplicate the focus management here.
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  if (!open) return null;
  return (
    <div
      className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-label="My Space"
      onClick={onClose}
    >
      <div
        className="bg-(--color-surface) rounded-2xl shadow-xl w-full max-w-[560px] max-h-[85vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {children}
      </div>
    </div>
  );
}

function NameEditor({
  initial,
  draft,
  onDraftChange,
  onCancel,
  onSave,
}: {
  initial: string;
  draft: string;
  onDraftChange: (v: string) => void;
  onCancel: () => void;
  onSave: (v: string) => void | Promise<void>;
}) {
  const trimmed = draft.trim();
  const ok = trimmed.length >= 1 && trimmed.length <= 30 && trimmed !== initial.trim();
  return (
    <section className="space-y-4">
      <h3 className="text-sm font-semibold text-(--color-text)">Change name</h3>
      <input
        autoFocus
        value={draft}
        onChange={(e) => onDraftChange(e.target.value)}
        maxLength={30}
        className="w-full px-4 py-3 text-base border border-(--color-border) rounded-2xl bg-(--color-surface) text-(--color-text) focus:outline-none focus:ring-2 focus:ring-(--color-accent)/30 min-h-[44px]"
        placeholder="Companion name"
      />
      <div className="flex gap-2 justify-end">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2.5 rounded-2xl text-sm border border-(--color-border) text-(--color-text) min-h-[44px]"
        >
          Cancel
        </button>
        <button
          type="button"
          disabled={!ok}
          onClick={() => void onSave(trimmed)}
          className="px-4 py-2.5 rounded-2xl text-sm bg-(--color-text) text-white disabled:opacity-40 min-h-[44px]"
        >
          Save
        </button>
      </div>
    </section>
  );
}

function BuddyEditor({
  personas,
  currentVoice,
  currentName,
  pendingPersona,
  onPickPersona,
  onKeepName,
  onUseDefaultName,
  onCancel,
}: {
  personas: VoicePersona[];
  currentVoice: string;
  currentName: string;
  pendingPersona: VoicePersona | null;
  onPickPersona: (p: VoicePersona | null) => void;
  onKeepName: () => void | Promise<void>;
  onUseDefaultName: () => void | Promise<void>;
  onCancel: () => void;
}) {
  return (
    <section className="space-y-4">
      <h3 className="text-sm font-semibold text-(--color-text)">Change buddy</h3>
      <PersonaPicker
        personas={personas}
        selectedId={pendingPersona?.id ?? currentVoice}
        onSelect={(id) => {
          const next = personas.find((p) => p.id === id) ?? null;
          onPickPersona(next);
        }}
      />
      {pendingPersona && currentName && pendingPersona.default_companion_name !== currentName && (
        <div className="bg-(--color-page) border border-(--color-border) rounded-2xl p-4 space-y-3">
          <p className="text-sm text-(--color-text)">
            Keep <span className="font-semibold">{currentName}</span> or use{" "}
            <span className="font-semibold">{pendingPersona.default_companion_name}</span>?
          </p>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => void onKeepName()}
              className="flex-1 py-2.5 rounded-2xl text-sm border border-(--color-border) text-(--color-text) min-h-[44px]"
            >
              Keep {currentName}
            </button>
            <button
              type="button"
              onClick={() => void onUseDefaultName()}
              className="flex-1 py-2.5 rounded-2xl text-sm bg-(--color-text) text-white min-h-[44px]"
            >
              Use {pendingPersona.default_companion_name}
            </button>
          </div>
        </div>
      )}
      {pendingPersona && (!currentName || pendingPersona.default_companion_name === currentName) && (
        <button
          type="button"
          onClick={() => void onUseDefaultName()}
          className="w-full py-3 rounded-2xl text-sm bg-(--color-text) text-white min-h-[44px]"
        >
          Use {pendingPersona.default_companion_name}
        </button>
      )}
      <button
        type="button"
        onClick={onCancel}
        className="w-full py-2.5 rounded-2xl text-sm border border-(--color-border) text-(--color-text-secondary) min-h-[44px]"
      >
        Cancel
      </button>
    </section>
  );
}

function ConfirmReset({
  onCancel,
  onConfirm,
}: {
  onCancel: () => void;
  onConfirm: () => void;
}) {
  return (
    <section className="space-y-4 bg-(--color-page) border border-(--color-border) rounded-2xl p-4">
      <h3 className="text-sm font-semibold text-(--color-text)">Start over?</h3>
      <p className="text-sm text-(--color-text-secondary) leading-relaxed">
        This clears your companion, vibe, icons, sound, tone, and interests, then walks
        you through setup again.
      </p>
      <div className="flex gap-2">
        <button
          type="button"
          onClick={onCancel}
          className="flex-1 py-2.5 rounded-2xl text-sm border border-(--color-border) text-(--color-text) min-h-[44px]"
        >
          Cancel
        </button>
        <button
          type="button"
          onClick={onConfirm}
          className="flex-1 py-2.5 rounded-2xl text-sm bg-(--color-danger) text-white min-h-[44px]"
        >
          Start over
        </button>
      </div>
    </section>
  );
}
