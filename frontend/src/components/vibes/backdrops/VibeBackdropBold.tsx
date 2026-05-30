"use client";

import { AmbientFloat } from "@/lib/motion";

import { BackdropRoot, StretchLayer } from "./shared";

// Bold: a vibrant sunset gradient, a faint chevron pattern, a single
// large floating accent circle, and a soft corner vignette. Harmonizes
// with the bold token accent (#FF6B35).
export function VibeBackdropBold() {
  return (
    <BackdropRoot>
      <StretchLayer>
        <defs>
          <linearGradient id="bold-sunset" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#FF4A5A" />
            <stop offset="100%" stopColor="#FFA040" />
          </linearGradient>
        </defs>
        <rect x="0" y="0" width="100" height="100" fill="url(#bold-sunset)" />
      </StretchLayer>

      {/* Chevron pattern overlay */}
      <svg width="100%" height="100%" style={{ position: "absolute", inset: 0, opacity: 0.08 }}>
        <defs>
          <pattern id="bold-chevron" width="40" height="40" patternUnits="userSpaceOnUse" patternTransform="scale(1)">
            <path d="M0 24 L20 8 L40 24" fill="none" stroke="#FFFFFF" strokeWidth="4" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#bold-chevron)" />
      </svg>

      {/* Large floating accent circle, top-left */}
      <AmbientFloat
        amplitude={10}
        duration={6}
        style={{
          position: "absolute",
          left: "-60px",
          top: "-60px",
          width: 400,
          height: 400,
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(255,208,64,0.15) 0%, rgba(255,208,64,0.15) 60%, rgba(255,208,64,0) 100%)",
        }}
      >
        <span />
      </AmbientFloat>

      {/* Corner vignette */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.25) 100%)",
        }}
      />
    </BackdropRoot>
  );
}

export default VibeBackdropBold;
