"use client";

/**
 * Streaming TTS audio player.
 *
 * v2 implementation: receives base64-encoded MP3 chunks from the
 * SSE response, accumulates them, then plays the complete blob.
 * This works cross-browser (Chrome, Safari, Firefox) without MSE
 * complexity. A future iteration can add MSE-based progressive
 * playback for Chrome/Firefox to hit the 800ms-to-first-audio
 * budget; Safari has restrictive MSE for audio so it would always
 * use the blob path anyway.
 */

export interface StreamingPlayerOpts {
  onFirstChunk?: () => void;
  onEnd?: () => void;
  onError?: (err: Error) => void;
}

export interface StreamingAudioPlayer {
  playFromSSE: (url: string, body: BodyInit, opts?: StreamingPlayerOpts) => Promise<void>;
  stop: () => void;
  isPlaying: () => boolean;
}

interface SseEvent {
  event: string;
  data: string;
}

function* parseSse(buffer: string): Generator<SseEvent> {
  // Naive SSE parser. Splits on the double-newline boundary; yields
  // {event, data} pairs in order. Buffer should be the accumulated
  // text since the last call's residue.
  const blocks = buffer.split("\n\n");
  // Trailing partial block is left to the caller.
  for (let i = 0; i < blocks.length; i++) {
    const block = blocks[i].trim();
    if (!block) continue;
    let event = "message";
    let data = "";
    for (const line of block.split("\n")) {
      if (line.startsWith("event:")) event = line.slice(6).trim();
      else if (line.startsWith("data:")) data += line.slice(5).trim();
    }
    yield { event, data };
  }
}

function base64ToBytes(b64: string): Uint8Array {
  const bin = atob(b64);
  const arr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
  return arr;
}

export function createStreamingPlayer(): StreamingAudioPlayer {
  let currentAudio: HTMLAudioElement | null = null;
  let currentAbort: AbortController | null = null;
  let playing = false;

  function cleanup() {
    if (currentAudio) {
      currentAudio.pause();
      const src = currentAudio.src;
      currentAudio.src = "";
      if (src.startsWith("blob:")) URL.revokeObjectURL(src);
      currentAudio = null;
    }
    playing = false;
  }

  return {
    isPlaying: () => playing,

    stop() {
      currentAbort?.abort();
      cleanup();
    },

    async playFromSSE(url, body, opts) {
      this.stop();
      const ac = new AbortController();
      currentAbort = ac;
      playing = true;
      try {
        const resp = await fetch(url, {
          method: "POST",
          body,
          credentials: "include",
          headers: {
            "content-type": "application/json",
            "x-csrf-token": getCookie("csrf_token") ?? "",
            accept: "text/event-stream",
          },
          signal: ac.signal,
        });
        if (!resp.ok) throw new Error(`tts http ${resp.status}`);
        const reader = resp.body?.getReader();
        if (!reader) throw new Error("response has no body");
        const decoder = new TextDecoder("utf-8");
        const parts: Uint8Array[] = [];
        let firstChunkSeen = false;
        let leftover = "";
        let totalBytes = 0;

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          leftover += decoder.decode(value, { stream: true });
          const lastBoundary = leftover.lastIndexOf("\n\n");
          if (lastBoundary === -1) continue;
          const consumable = leftover.slice(0, lastBoundary);
          leftover = leftover.slice(lastBoundary + 2);
          for (const ev of parseSse(consumable)) {
            if (ev.event === "chunk") {
              const bytes = base64ToBytes(ev.data);
              parts.push(bytes);
              totalBytes += bytes.byteLength;
              if (!firstChunkSeen) {
                firstChunkSeen = true;
                opts?.onFirstChunk?.();
              }
            } else if (ev.event === "error") {
              throw new Error(`tts stream error: ${ev.data}`);
            }
            // meta + done events are ignored for playback purposes;
            // future MSE implementation will consume them.
          }
        }

        if (!firstChunkSeen || totalBytes === 0) {
          throw new Error("no audio in stream");
        }

        const blob = new Blob(parts as BlobPart[], { type: "audio/mpeg" });
        const audio = new Audio(URL.createObjectURL(blob));
        currentAudio = audio;
        audio.addEventListener("ended", () => {
          opts?.onEnd?.();
          cleanup();
        });
        audio.addEventListener("error", () => {
          opts?.onError?.(new Error("audio playback failed"));
          cleanup();
        });
        await audio.play().catch((err: Error) => {
          opts?.onError?.(err);
          cleanup();
          throw err;
        });
      } catch (err) {
        if ((err as { name?: string } | null)?.name === "AbortError") {
          cleanup();
          return;
        }
        opts?.onError?.(err as Error);
        cleanup();
        throw err;
      } finally {
        currentAbort = null;
      }
    },
  };
}

function getCookie(name: string): string | undefined {
  if (typeof document === "undefined") return undefined;
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : undefined;
}
