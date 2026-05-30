"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";

import { AmbientFloat, useMotion } from "@/lib/motion";

import { mulberry32, range } from "@/lib/vibe/rng";
import { BackdropRoot } from "./shared";

// Orbit: deep space with a jittered-grid starfield, a slow-drifting
// nebula, and a rare shooting star. Harmonizes with the orbit token page.

const STARS = (() => {
  const rng = mulberry32(0x5747);
  // Jittered grid (~15x14 = 210 cells) approximates Poisson-disc spread.
  const cols = 15;
  const rows = 14;
  const stars: Array<{ x: number; y: number; r: number; o: number }> = [];
  for (let cx = 0; cx < cols; cx++) {
    for (let cy = 0; cy < rows; cy++) {
      if (stars.length >= 200) break;
      stars.push({
        x: ((cx + range(rng, 0.1, 0.9)) / cols) * 100,
        y: ((cy + range(rng, 0.1, 0.9)) / rows) * 100,
        r: range(rng, 0.06, 0.16),
        o: range(rng, 0.4, 1.0),
      });
    }
  }
  return stars;
})();

function ShootingStar() {
  const { reduceMotion } = useMotion();
  const [shot, setShot] = useState<{ key: number; fromX: number; fromY: number; toX: number; toY: number } | null>(
    null,
  );

  useEffect(() => {
    if (reduceMotion) return;
    let timer: ReturnType<typeof setTimeout>;
    let key = 0;
    const schedule = () => {
      timer = setTimeout(
        () => {
          key += 1;
          setShot({
            key,
            fromX: 70 + Math.random() * 28,
            fromY: Math.random() * 18,
            toX: Math.random() * 24,
            toY: 70 + Math.random() * 26,
          });
          schedule();
        },
        30000 + Math.random() * 30000,
      );
    };
    schedule();
    return () => clearTimeout(timer);
  }, [reduceMotion]);

  if (reduceMotion || !shot) return null;
  return (
    <motion.div
      key={shot.key}
      initial={{ left: `${shot.fromX}%`, top: `${shot.fromY}%`, opacity: 0 }}
      animate={{ left: `${shot.toX}%`, top: `${shot.toY}%`, opacity: [0, 1, 1, 0] }}
      transition={{ duration: 1.1, ease: "easeIn" }}
      style={{ position: "absolute", width: 120, height: 2 }}
    >
      <div
        style={{
          width: "100%",
          height: "100%",
          transform: "rotate(35deg)",
          transformOrigin: "right center",
          background: "linear-gradient(90deg, rgba(240,232,216,0) 0%, #F0E8D8 100%)",
          borderRadius: 2,
        }}
      />
    </motion.div>
  );
}

export function VibeBackdropOrbit() {
  return (
    <BackdropRoot>
      <div style={{ position: "absolute", inset: 0, background: "#0A1530" }} />

      {/* Nebula: three overlapping radial glows, gently drifting */}
      <AmbientFloat
        amplitude={12}
        duration={22}
        style={{ position: "absolute", left: "30%", top: "35%", width: "40%", height: "30%" }}
      >
        <div style={{ position: "absolute", inset: 0, borderRadius: "50%", background: "radial-gradient(circle, rgba(142,111,184,0.22) 0%, rgba(142,111,184,0) 70%)" }} />
        <div style={{ position: "absolute", left: "20%", top: "10%", width: "70%", height: "80%", borderRadius: "50%", background: "radial-gradient(circle, rgba(74,122,184,0.2) 0%, rgba(74,122,184,0) 70%)" }} />
        <div style={{ position: "absolute", left: "-10%", top: "25%", width: "60%", height: "60%", borderRadius: "50%", background: "radial-gradient(circle, rgba(142,111,184,0.15) 0%, rgba(142,111,184,0) 70%)" }} />
      </AmbientFloat>

      {/* Starfield */}
      <svg
        width="100%"
        height="100%"
        viewBox="0 0 100 100"
        preserveAspectRatio="xMidYMid slice"
        style={{ position: "absolute", inset: 0, display: "block" }}
      >
        {STARS.map((s, i) => (
          <circle key={i} cx={s.x} cy={s.y} r={s.r} fill="#F0E8D8" opacity={s.o} />
        ))}
      </svg>

      <ShootingStar />
    </BackdropRoot>
  );
}

export default VibeBackdropOrbit;
