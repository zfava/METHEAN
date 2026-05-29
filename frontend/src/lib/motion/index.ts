/**
 * Motion foundation barrel.
 *
 * Spring presets + the physics-based primitives + the MotionContext.
 * Import from "@/lib/motion" everywhere in the child surface.
 */

export {
  SPRING_BY_VIBE,
  SPRING_PRESS,
  SPRING_GENTLE,
  SPRING_SETTLE,
  SPRING_BOUNCY,
  INSTANT_TRANSITION,
  vibeMotionIdFromVibe,
  type VibeMotionId,
} from "./springs";

export {
  MotionProvider,
  useMotion,
  ageBandFromGrade,
  type MotionState,
  type MotionStateBase,
  type MotionIntensity,
  type MotionPreference,
  type AgeBand,
} from "./MotionContext";

export {
  Fade,
  Scale,
  Slide,
  Press,
  Hover,
  Stagger,
  AmbientFloat,
  ParallaxOnScroll,
  SharedLayout,
  SharedItem,
  RouteTransition,
  type FadeDirection,
  type SlideAxis,
} from "./primitives";

export {
  MOTION_TOKENS,
  MOTION_EASINGS,
  MOTION_DURATIONS_MS,
  MOTION_DURATIONS_SEC,
  MOTION_STAGGER_MS,
  MOTION_STAGGER_SEC,
  type MotionEasing,
  type StaggerGap,
} from "./tokens";
