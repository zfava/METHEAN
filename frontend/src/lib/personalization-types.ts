/**
 * TypeScript counterparts for the backend personalization library
 * and per-child profile. Mirrors the schemas declared in
 * `backend/app/schemas/personalization.py`.
 *
 * Library entries share the LibraryEntry shape so the policy-aware
 * `available` flag is uniform across every picker in the UI.
 */

export interface LibraryEntry {
  id: string;
  label: string;
  description: string;
  available: boolean;
}

export interface Vibe extends LibraryEntry {
  tokens: Record<string, string>;
}

export interface InterestTag extends LibraryEntry {
  category: string;
  icon_keyword: string;
}

export interface VoicePersona extends LibraryEntry {
  default_companion_name: string;
  tone_summary: string;
  // TTS fields (Sprint v2 Prompt 2). Optional for back-compat.
  tts_voice_id?: string;
  tts_provider?: "openai" | "elevenlabs";
  speech_rate?: number;
  prosody_hints?: string;
}

export interface IconographyPack extends LibraryEntry {
  icons: Record<string, string>;
}

export interface SoundPack extends LibraryEntry {
  cues: Record<string, string | null>;
}

export interface AffirmationTone extends LibraryEntry {
  tone_summary: string;
}

export interface PersonalizationLibrary {
  vibes: Vibe[];
  interest_tags: InterestTag[];
  voice_personas: VoicePersona[];
  iconography_packs: IconographyPack[];
  sound_packs: SoundPack[];
  affirmation_tones: AffirmationTone[];
  max_interest_tags_per_child: number;
}

export interface ChildPersonalization {
  child_id: string;
  companion_name: string;
  companion_voice: string;
  vibe: string;
  iconography_pack: string;
  sound_pack: string;
  affirmation_tone: string;
  interest_tags: string[];
  out_of_policy: string[];
  onboarded: boolean;
}

export interface PersonalizationPolicy {
  allowed_vibes: string[];
  allowed_interest_tags: string[];
  allowed_voice_personas: string[];
  allowed_iconography_packs: string[];
  allowed_sound_packs: string[];
  allowed_affirmation_tones: string[];
  companion_name_requires_review: boolean;
  max_interest_tags_per_child: number;
  // Voice-input governance (Sprint v2 Prompt 1).
  voice_input_enabled: boolean;
  voice_minutes_daily_cap: number;
  whisper_provider: "openai" | "local";
  // Voice-output governance (Sprint v2 Prompt 2).
  voice_output_enabled: boolean;
  voice_output_minutes_daily_cap: number;
  tts_provider: "openai" | "elevenlabs";
}

export interface TranscribeResponse {
  text: string;
  duration_seconds: number;
  remaining_minutes: number;
  is_silent: boolean;
  safety_intervention: boolean;
  intervention_kind: string | null;
  suggested_response: string | null;
  provider: "openai" | "local";
}

/**
 * Hardcoded fallback used while the library is still loading or
 * when the backend can't be reached. Matches the `:root` defaults
 * in globals.css so swapping to it is visually a no-op.
 */
export const CALM_VIBE_FALLBACK: Vibe = {
  id: "calm",
  label: "Calm",
  description: "Default. Off-white surfaces, navy accent, room to breathe.",
  available: true,
  tokens: {
    "--color-page": "#FAFAF8",
    "--color-surface": "#FFFFFF",
    "--color-accent": "#4A6FA5",
    "--color-text": "#1A1A1A",
    "--color-text-secondary": "#6B6B6B",
    "--color-border": "rgba(0, 0, 0, 0.06)",
    "--color-brand-gold": "#C6A24E",
    "--radius-card": "14px",
    "--font-weight-heading": "600",
  },
};
