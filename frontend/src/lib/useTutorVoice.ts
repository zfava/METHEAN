"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { createStreamingPlayer, type StreamingAudioPlayer } from "@/lib/audio/player";
import { usePersonalization } from "@/lib/PersonalizationProvider";

export interface TutorVoiceState {
  isPlaying: boolean;
  currentMessageId: string | null;
  error: Error | null;
}

export interface TutorVoiceControls {
  speak: (messageId: string, text: string, opts?: { voiceMode?: boolean }) => Promise<void>;
  stop: () => void;
  isEnabled: boolean;
  setSessionMuted: (muted: boolean) => void;
  sessionMuted: boolean;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

/**
 * Plays tutor messages aloud in the kid's chosen persona voice.
 *
 * ``isEnabled`` is true only when the household policy permits
 * voice output, the kid has a companion voice set, and the sound
 * pack is not "off". The session-mute toggle in TutorChat sits on
 * top of that as a kid-only override that doesn't change policy.
 */
export function useTutorVoice(): [TutorVoiceState, TutorVoiceControls] {
  const { profile } = usePersonalization();
  const playerRef = useRef<StreamingAudioPlayer | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentMessageId, setCurrentMessageId] = useState<string | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [sessionMuted, setSessionMuted] = useState<boolean>(() => {
    if (typeof window === "undefined") return false;
    return window.sessionStorage?.getItem("tutor_voice_muted") === "1";
  });

  useEffect(() => {
    if (typeof window === "undefined") return;
    window.sessionStorage?.setItem("tutor_voice_muted", sessionMuted ? "1" : "0");
  }, [sessionMuted]);

  // Lazy-create the player so SSR builds don't try to access Audio.
  const player = useMemo(() => {
    if (typeof window === "undefined") return null;
    if (!playerRef.current) playerRef.current = createStreamingPlayer();
    return playerRef.current;
  }, []);

  // Default to "soft" if the profile hasn't loaded yet (the
  // VibeProvider serves a soft default profile during fetch).
  const isEnabled = useMemo(() => {
    const personaSet = Boolean(profile.companion_voice);
    const soundOn = profile.sound_pack !== "off";
    // Note: the full check (voice_output_enabled policy flag) is
    // enforced server-side via the 403 path; the hook still attempts
    // to play and the API rejection surfaces as an error. Setting
    // the local flag from policy would require an extra fetch.
    return personaSet && soundOn && !sessionMuted;
  }, [profile.companion_voice, profile.sound_pack, sessionMuted]);

  const stop = useCallback(() => {
    player?.stop();
    setIsPlaying(false);
    setCurrentMessageId(null);
  }, [player]);

  const speak = useCallback(
    async (messageId: string, text: string, opts?: { voiceMode?: boolean }) => {
      if (!player) return;
      if (!isEnabled) return;
      // Stop any in-flight playback first.
      stop();
      setError(null);
      setCurrentMessageId(messageId);
      setIsPlaying(true);
      const url = `${API_BASE}/children/${profile.child_id}/tts/stream`;
      const body = JSON.stringify({
        text,
        persona_id: profile.companion_voice,
        voice_mode: Boolean(opts?.voiceMode),
        message_id: messageId,
      });
      try {
        await player.playFromSSE(url, body, {
          onEnd: () => {
            setIsPlaying(false);
            setCurrentMessageId(null);
          },
          onError: (e) => {
            setError(e);
            setIsPlaying(false);
            setCurrentMessageId(null);
          },
        });
      } catch (e) {
        setError(e as Error);
        setIsPlaying(false);
        setCurrentMessageId(null);
      }
    },
    [player, profile.child_id, profile.companion_voice, isEnabled, stop],
  );

  // Cleanup on unmount.
  useEffect(() => {
    return () => {
      playerRef.current?.stop();
    };
  }, []);

  return [
    { isPlaying, currentMessageId, error },
    { speak, stop, isEnabled, setSessionMuted, sessionMuted },
  ];
}
