"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import { useToast } from "@/components/Toast";
import { StepIconography } from "@/components/child/welcome/StepIconography";
import { StepInterests } from "@/components/child/welcome/StepInterests";
import { StepName } from "@/components/child/welcome/StepName";
import { StepPersona } from "@/components/child/welcome/StepPersona";
import { StepReady } from "@/components/child/welcome/StepReady";
import { StepSound } from "@/components/child/welcome/StepSound";
import { StepTone } from "@/components/child/welcome/StepTone";
import { StepVibe } from "@/components/child/welcome/StepVibe";
import {
  WelcomeShell,
  type WelcomeStepDef,
} from "@/components/child/welcome/WelcomeShell";
import { usePersonalization } from "@/lib/PersonalizationProvider";
import type {
  ChildPersonalization,
  Vibe,
  VoicePersona,
} from "@/lib/personalization-types";

const STEPS: readonly WelcomeStepDef[] = [
  { id: "persona", label: "Pick your study buddy" },
  { id: "name", label: "Name your buddy" },
  { id: "interests", label: "What are you into?" },
  { id: "vibe", label: "Pick your vibe" },
  { id: "iconography", label: "Pick your icon style" },
  { id: "sound", label: "How much sound?" },
  { id: "tone", label: "Pick a tone" },
  { id: "ready", label: "Ready" },
] as const;

export default function WelcomePage() {
  const router = useRouter();
  const { toast } = useToast();
  const { profile, library, updateProfile, loading } = usePersonalization();
  const [index, setIndex] = useState(0);

  // Set the document title once.
  useEffect(() => {
    document.title = "Welcome | METHEAN";
  }, []);

  // If the kid is already onboarded, route them straight in. The
  // dashboard owns the inverse redirect (sending unonboarded kids
  // here), so a refresh after completion never lands here again.
  useEffect(() => {
    if (loading) return;
    if (profile.onboarded) {
      router.replace("/child");
    }
  }, [loading, profile.onboarded, router]);

  // Local picks. Each step seeds from the profile, then writes back
  // optimistically. Local state lets a kid back up without burning
  // round trips on every step.
  const [draftPersona, setDraftPersona] = useState<string>(profile.companion_voice);
  const [draftVibe, setDraftVibe] = useState<string>(profile.vibe);
  const [draftIconography, setDraftIconography] = useState<string>(profile.iconography_pack);
  const [draftSound, setDraftSound] = useState<string>(profile.sound_pack);
  const [draftTone, setDraftTone] = useState<string>(profile.affirmation_tone);

  // Resync drafts whenever the canonical profile updates (e.g.,
  // after a successful PUT echo) so a back-then-forward sequence
  // never overwrites a fresh write with stale local state.
  useEffect(() => { setDraftPersona(profile.companion_voice); }, [profile.companion_voice]);
  useEffect(() => { setDraftVibe(profile.vibe); }, [profile.vibe]);
  useEffect(() => { setDraftIconography(profile.iconography_pack); }, [profile.iconography_pack]);
  useEffect(() => { setDraftSound(profile.sound_pack); }, [profile.sound_pack]);
  useEffect(() => { setDraftTone(profile.affirmation_tone); }, [profile.affirmation_tone]);

  const persistAndAdvance = useCallback(
    async (patch: Partial<ChildPersonalization>) => {
      try {
        await updateProfile(patch);
      } catch {
        toast("Couldn't save that yet, will try again.", "info");
      }
      setIndex((i) => Math.min(i + 1, STEPS.length - 1));
    },
    [updateProfile, toast],
  );

  const skipAll = useCallback(async () => {
    try {
      await updateProfile({ onboarded: true });
    } catch {
      // Routing anyway; the next /child load will retry the flag.
    }
    router.replace("/child");
  }, [updateProfile, router]);

  const selectedPersona: VoicePersona | null = useMemo(() => {
    if (!library) return null;
    return library.voice_personas.find((p) => p.id === draftPersona) ?? null;
  }, [library, draftPersona]);

  const selectedVibe: Vibe | null = useMemo(() => {
    if (!library) return null;
    return library.vibes.find((v) => v.id === draftVibe) ?? null;
  }, [library, draftVibe]);

  // Decorate the shell's step list with a vibe preview override on
  // the vibe step itself so the chrome behind the picker shows the
  // active vibe as the kid taps through.
  const stepsForShell = useMemo<WelcomeStepDef[]>(
    () =>
      STEPS.map((s) =>
        s.id === "vibe" ? { ...s, vibePreview: selectedVibe } : s,
      ),
    [selectedVibe],
  );

  if (loading || !library) {
    return (
      <div className="min-h-dvh flex items-center justify-center bg-(--color-page)">
        <div className="w-6 h-6 rounded-full border-2 border-(--color-accent) border-t-transparent animate-spin" />
      </div>
    );
  }

  return (
    <WelcomeShell
      steps={stepsForShell}
      currentIndex={index}
      onBack={() => setIndex((i) => Math.max(i - 1, 0))}
      onSkipStep={() => setIndex((i) => Math.min(i + 1, STEPS.length - 1))}
      onSkipAll={() => void skipAll()}
    >
      {index === 0 && (
        <StepPersona
          personas={library.voice_personas}
          selectedId={draftPersona}
          onSelect={(id) => {
            setDraftPersona(id);
            void updateProfile({ companion_voice: id }).catch(() =>
              toast("Couldn't save that yet, will try again.", "info"),
            );
          }}
          onContinue={() => setIndex(1)}
        />
      )}

      {index === 1 && (
        <StepName
          persona={selectedPersona}
          initialName={profile.companion_name}
          requiresReview={false /* policy flag not exposed here; my space surfaces it */}
          onContinue={(name) => void persistAndAdvance({ companion_name: name })}
        />
      )}

      {index === 2 && (
        <StepInterests
          tags={library.interest_tags}
          maxCount={library.max_interest_tags_per_child}
          initialSelected={profile.interest_tags}
          onContinue={(ids) => void persistAndAdvance({ interest_tags: ids })}
        />
      )}

      {index === 3 && (
        <StepVibe
          vibes={library.vibes}
          selectedId={draftVibe}
          onSelect={(id) => {
            setDraftVibe(id);
            void updateProfile({ vibe: id }).catch(() =>
              toast("Couldn't save that yet, will try again.", "info"),
            );
          }}
          onContinue={() => setIndex(4)}
        />
      )}

      {index === 4 && (
        <StepIconography
          packs={library.iconography_packs}
          selectedId={draftIconography}
          onSelect={(id) => {
            setDraftIconography(id);
            void updateProfile({ iconography_pack: id }).catch(() =>
              toast("Couldn't save that yet, will try again.", "info"),
            );
          }}
          onContinue={() => setIndex(5)}
        />
      )}

      {index === 5 && (
        <StepSound
          packs={library.sound_packs}
          selectedId={draftSound || "soft"}
          onSelect={(id) => {
            setDraftSound(id);
            void updateProfile({ sound_pack: id }).catch(() =>
              toast("Couldn't save that yet, will try again.", "info"),
            );
          }}
          onContinue={() => setIndex(6)}
        />
      )}

      {index === 6 && (
        <StepTone
          tones={library.affirmation_tones}
          selectedId={draftTone}
          onSelect={(id) => {
            setDraftTone(id);
            void updateProfile({ affirmation_tone: id }).catch(() =>
              toast("Couldn't save that yet, will try again.", "info"),
            );
          }}
          onContinue={() => setIndex(7)}
        />
      )}

      {index === 7 && (
        <StepReady
          companionName={profile.companion_name}
          companionVoice={profile.companion_voice}
          onLaunch={() => void skipAll()}
        />
      )}
    </WelcomeShell>
  );
}
