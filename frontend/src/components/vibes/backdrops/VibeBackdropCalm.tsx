"use client";

import { AmbientFloat, ParallaxOnScroll } from "@/lib/motion";

import { BackdropRoot, StretchLayer, wavePath } from "./shared";

// Calm: a gentle dawn sky, three parallaxing horizon waves, and a soft
// floating sun. Harmonizes with the calm token page (#FAFAF8).
export function VibeBackdropCalm() {
  return (
    <BackdropRoot>
      {/* Dawn-sky gradient */}
      <StretchLayer>
        <defs>
          <linearGradient id="calm-sky" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#C8D7E0" />
            <stop offset="100%" stopColor="#F0E8D8" />
          </linearGradient>
        </defs>
        <rect x="0" y="0" width="100" height="100" fill="url(#calm-sky)" />
      </StretchLayer>

      {/* Soft sun, gently floating */}
      <AmbientFloat
        amplitude={4}
        duration={8}
        style={{
          // Anchored via calc rather than transform: AmbientFloat animates
          // transform (translateY), which would override a centering transform.
          position: "absolute",
          left: "calc(75% - 80px)",
          top: "calc(20% - 80px)",
          width: 160,
          height: 160,
          borderRadius: "50%",
          background: "radial-gradient(circle, #FFE9B0 0%, rgba(255,233,176,0) 70%)",
        }}
      >
        <span />
      </AmbientFloat>

      {/* Three horizon waves, each parallaxing at a different depth */}
      <ParallaxOnScroll depth={0.1} style={{ position: "absolute", inset: 0 }}>
        <StretchLayer>
          <path d={wavePath(70, 5, 6)} fill="#A4B5C2" opacity={0.4} />
        </StretchLayer>
      </ParallaxOnScroll>
      <ParallaxOnScroll depth={0.05} style={{ position: "absolute", inset: 0 }}>
        <StretchLayer>
          <path d={wavePath(78, 5, 6)} fill="#8DA0B0" opacity={0.6} />
        </StretchLayer>
      </ParallaxOnScroll>
      <ParallaxOnScroll depth={0} style={{ position: "absolute", inset: 0 }}>
        <StretchLayer>
          <path d={wavePath(86, 4, 6)} fill="#6F8694" opacity={0.8} />
        </StretchLayer>
      </ParallaxOnScroll>
    </BackdropRoot>
  );
}

export default VibeBackdropCalm;
