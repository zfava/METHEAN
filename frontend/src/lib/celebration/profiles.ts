import type { Particle, ParticleShape } from "./ParticleEngine";

// Particle profile catalog. Each celebration tier has a base profile
// (count, shapes, spawn pattern, velocities, colors, lifetime) that is
// then modulated by the active vibe and the reduced-motion preference.

export type CelebrationTier =
  | "activity_complete"
  | "mastery_up"
  | "day_complete"
  | "streak_7"
  | "streak_30"
  | "streak_100";

export type VibeId = "calm" | "field" | "orbit" | "workshop" | "studio" | "bold";

export interface ProfileContext {
  tier: CelebrationTier;
  vibe: VibeId;
  reducedMotion: boolean;
  centerX: number;
  centerY: number;
  canvasWidth: number;
  canvasHeight: number;
  rng: () => number; // seeded for testability
}

type RGB = [number, number, number];

interface VibeModulation {
  count: number;
  velocity: number;
  lifeDecay: number;
}

// count / velocity / lifeDecay multipliers per vibe. Higher lifeDecay =
// faster fade (shorter on-screen life).
const VIBE_MOD: Record<VibeId, VibeModulation> = {
  calm: { count: 0.6, velocity: 0.7, lifeDecay: 0.7 },
  field: { count: 0.9, velocity: 0.9, lifeDecay: 0.85 },
  orbit: { count: 1.0, velocity: 1.0, lifeDecay: 0.9 },
  workshop: { count: 0.9, velocity: 0.95, lifeDecay: 0.9 },
  studio: { count: 1.1, velocity: 1.1, lifeDecay: 1.0 },
  bold: { count: 1.2, velocity: 1.3, lifeDecay: 1.1 },
};

const REDUCED_MOD: VibeModulation = { count: 0.3, velocity: 0.5, lifeDecay: 1.5 };

// Per-vibe accent color used as the base for activity_complete.
const VIBE_ACCENT: Record<VibeId, RGB> = {
  calm: [45, 106, 79],
  field: [76, 154, 42],
  orbit: [91, 108, 240],
  workshop: [181, 114, 58],
  studio: [192, 86, 126],
  bold: [226, 83, 59],
};

// Named colors (spec hex values).
const WHITE: RGB = [255, 255, 255];
const WARM_WHITE: RGB = [255, 246, 224];
const SOFT_WHITE: RGB = [255, 244, 232];
const GOLD: RGB = [198, 162, 78]; // #C6A24E
const WARM_ORANGE: RGB = [232, 155, 92]; // #E89B5C
const ORANGE_RED: RGB = [255, 122, 69]; // #FF7A45
const DEEP_RED: RGB = [139, 30, 30];
const FIREFLY: RGB = [255, 233, 168];

function range(rng: () => number, min: number, max: number): number {
  return min + rng() * (max - min);
}

function pickShape(rng: () => number, weighted: Array<[ParticleShape, number]>): ParticleShape {
  const roll = rng();
  let acc = 0;
  for (const [shape, weight] of weighted) {
    acc += weight;
    if (roll <= acc) return shape;
  }
  return weighted[weighted.length - 1][0];
}

interface SpawnSpec {
  x: number;
  y: number;
  vx: number;
  vy: number;
  shape: ParticleShape;
  baseColor: RGB;
  endColor: RGB;
  size: number;
  lifetimeSec: number;
  gravity: number;
  opacity?: number;
}

function makeParticle(rng: () => number, mod: VibeModulation, spec: SpawnSpec): Particle {
  return {
    x: spec.x,
    y: spec.y,
    vx: spec.vx * mod.velocity,
    vy: spec.vy * mod.velocity,
    rotation: rng() * Math.PI * 2,
    rotationVelocity: range(rng, -4, 4) * mod.velocity,
    life: 1,
    lifeDecay: (1 / spec.lifetimeSec) * mod.lifeDecay,
    shape: spec.shape,
    baseColor: spec.baseColor,
    endColor: spec.endColor,
    size: spec.size,
    opacity: spec.opacity ?? 1,
    gravity: spec.gravity,
  };
}

function modFor(ctx: ProfileContext): VibeModulation {
  const v = VIBE_MOD[ctx.vibe];
  if (!ctx.reducedMotion) return v;
  return {
    count: v.count * REDUCED_MOD.count,
    velocity: v.velocity * REDUCED_MOD.velocity,
    lifeDecay: v.lifeDecay * REDUCED_MOD.lifeDecay,
  };
}

function scaledCount(base: number, mod: VibeModulation): number {
  return Math.max(1, Math.round(base * mod.count));
}

/** Build the immediate-wave particles for a tier. */
export function buildParticles(ctx: ProfileContext): Particle[] {
  switch (ctx.tier) {
    case "activity_complete":
      return buildActivityComplete(ctx);
    case "mastery_up":
      return buildMasteryUp(ctx);
    case "day_complete":
      return buildDayComplete(ctx);
    case "streak_7":
      return buildStreak7(ctx);
    case "streak_30":
      return buildStreak30(ctx);
    case "streak_100":
      return buildStreak100Wave1(ctx);
  }
}

function buildActivityComplete(ctx: ProfileContext): Particle[] {
  const mod = modFor(ctx);
  const n = scaledCount(24, mod);
  const accent = VIBE_ACCENT[ctx.vibe];
  const out: Particle[] = [];
  for (let i = 0; i < n; i++) {
    const angle = ctx.rng() * Math.PI * 2;
    const speed = range(ctx.rng, 80, 160);
    out.push(
      makeParticle(ctx.rng, mod, {
        x: ctx.centerX,
        y: ctx.centerY,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - 30, // slight upward bias
        shape: pickShape(ctx.rng, [
          ["circle", 0.7],
          ["sparkle", 0.3],
        ]),
        baseColor: accent,
        endColor: WHITE,
        size: range(ctx.rng, 4, 8),
        lifetimeSec: 1.2,
        gravity: 0,
      }),
    );
  }
  return out;
}

function buildMasteryUp(ctx: ProfileContext): Particle[] {
  const mod = modFor(ctx);
  const n = scaledCount(80, mod);
  const out: Particle[] = [];
  for (let i = 0; i < n; i++) {
    out.push(
      makeParticle(ctx.rng, mod, {
        x: ctx.rng() * ctx.canvasWidth,
        y: range(ctx.rng, ctx.canvasHeight * 0.08, ctx.canvasHeight / 3),
        vx: range(ctx.rng, -60, 60),
        vy: -range(ctx.rng, 50, 200),
        shape: pickShape(ctx.rng, [
          ["sparkle", 0.4],
          ["star", 0.3],
          ["ember", 0.3],
        ]),
        baseColor: GOLD,
        endColor: WARM_WHITE,
        size: range(ctx.rng, 3, 10),
        lifetimeSec: 2.5,
        gravity: 120,
      }),
    );
  }
  return out;
}

function buildDayComplete(ctx: ProfileContext): Particle[] {
  const mod = modFor(ctx);
  const n = scaledCount(40, mod);
  const out: Particle[] = [];
  for (let i = 0; i < n; i++) {
    out.push(
      makeParticle(ctx.rng, mod, {
        x: ctx.rng() * ctx.canvasWidth,
        y: ctx.canvasHeight,
        vx: range(ctx.rng, -15, 15),
        vy: -range(ctx.rng, 40, 80),
        shape: "ember",
        baseColor: WARM_ORANGE,
        endColor: SOFT_WHITE,
        size: range(ctx.rng, 2, 6),
        lifetimeSec: 4.0,
        gravity: 0,
        opacity: 0.9,
      }),
    );
  }
  return out;
}

function buildStreak7(ctx: ProfileContext): Particle[] {
  const mod = modFor(ctx);
  const n = scaledCount(60, mod);
  const out: Particle[] = [];
  for (let i = 0; i < n; i++) {
    const angle = ctx.rng() * Math.PI * 2;
    const speed = range(ctx.rng, 60, 180);
    out.push(
      makeParticle(ctx.rng, mod, {
        x: ctx.centerX,
        y: ctx.centerY,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        shape: "ember",
        baseColor: ORANGE_RED,
        endColor: DEEP_RED,
        size: range(ctx.rng, 2, 6),
        lifetimeSec: 1.8,
        gravity: 200,
      }),
    );
  }
  return out;
}

function buildStreak30(ctx: ProfileContext): Particle[] {
  const mod = modFor(ctx);
  const n = scaledCount(100, mod);
  const out: Particle[] = [];
  const leftX = ctx.canvasWidth / 3;
  const rightX = (ctx.canvasWidth * 2) / 3;
  for (let i = 0; i < n; i++) {
    const angle = ctx.rng() * Math.PI * 2;
    const speed = range(ctx.rng, 100, 220);
    out.push(
      makeParticle(ctx.rng, mod, {
        x: i % 2 === 0 ? leftX : rightX,
        y: ctx.centerY,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        shape: pickShape(ctx.rng, [
          ["sparkle", 0.5],
          ["star", 0.3],
          ["circle", 0.2],
        ]),
        baseColor: ctx.rng() < 0.5 ? GOLD : WHITE,
        endColor: WARM_WHITE,
        size: range(ctx.rng, 3, 9),
        lifetimeSec: 2.2,
        gravity: 60,
      }),
    );
  }
  return out;
}

// streak_100 is a three-wave sequence. buildParticles returns wave 1; the
// director schedules the rocket, its explosion, and the fireflies.

function buildStreak100Wave1(ctx: ProfileContext): Particle[] {
  const mod = modFor(ctx);
  const n = scaledCount(80, mod);
  const out: Particle[] = [];
  for (let i = 0; i < n; i++) {
    const angle = ctx.rng() * Math.PI * 2;
    const speed = range(ctx.rng, 100, 240);
    out.push(
      makeParticle(ctx.rng, mod, {
        x: ctx.centerX,
        y: ctx.centerY,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        shape: pickShape(ctx.rng, [
          ["sparkle", 0.5],
          ["star", 0.3],
          ["ember", 0.2],
        ]),
        baseColor: GOLD,
        endColor: WARM_WHITE,
        size: range(ctx.rng, 4, 12),
        lifetimeSec: 2.2,
        gravity: 100,
      }),
    );
  }
  return out;
}

/** A single rocket particle climbing from the bottom toward the apex. */
export function buildStreak100Rocket(ctx: ProfileContext): Particle[] {
  const mod = modFor(ctx);
  return [
    makeParticle(ctx.rng, mod, {
      x: ctx.centerX,
      y: ctx.canvasHeight,
      vx: range(ctx.rng, -20, 20),
      vy: -((ctx.canvasHeight - ctx.canvasHeight * 0.3) / 0.7), // reach apex in ~0.7s
      shape: "ember",
      baseColor: GOLD,
      endColor: WARM_ORANGE,
      size: 5,
      lifetimeSec: 0.75,
      gravity: 0,
    }),
  ];
}

/** Radial star explosion at the rocket's apex (30 stars). */
export function buildStreak100Explosion(ctx: ProfileContext, x: number, y: number): Particle[] {
  const mod = modFor(ctx);
  const n = scaledCount(30, mod);
  const out: Particle[] = [];
  for (let i = 0; i < n; i++) {
    const angle = (Math.PI * 2 * i) / n + ctx.rng() * 0.2;
    const speed = range(ctx.rng, 120, 260);
    out.push(
      makeParticle(ctx.rng, mod, {
        x,
        y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        shape: "star",
        baseColor: GOLD,
        endColor: WHITE,
        size: range(ctx.rng, 4, 9),
        lifetimeSec: 1.6,
        gravity: 150,
      }),
    );
  }
  return out;
}

/** Ambient fireflies that drift slowly for ~5s. */
export function buildStreak100Fireflies(ctx: ProfileContext): Particle[] {
  const mod = modFor(ctx);
  const n = scaledCount(30, mod);
  const out: Particle[] = [];
  for (let i = 0; i < n; i++) {
    out.push(
      makeParticle(ctx.rng, mod, {
        x: ctx.rng() * ctx.canvasWidth,
        y: range(ctx.rng, ctx.canvasHeight * 0.2, ctx.canvasHeight * 0.85),
        vx: range(ctx.rng, -20, 20),
        vy: range(ctx.rng, -20, 20),
        shape: ctx.rng() < 0.5 ? "sparkle" : "circle",
        baseColor: FIREFLY,
        endColor: WARM_WHITE,
        size: range(ctx.rng, 2, 4),
        lifetimeSec: 5.0,
        gravity: 0,
        opacity: 0.8,
      }),
    );
  }
  return out;
}
