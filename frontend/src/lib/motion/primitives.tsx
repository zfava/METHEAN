"use client";

import {
  AnimatePresence,
  LayoutGroup,
  motion,
  useScroll,
  useTransform,
  type Transition,
  type Variants,
} from "framer-motion";
import {
  createContext,
  useContext,
  type CSSProperties,
  type ReactNode,
} from "react";

import { useMotion } from "@/lib/motion/MotionContext";
import { INSTANT_TRANSITION, SPRING_PRESS } from "@/lib/motion/springs";

/**
 * Physics-based motion primitives for the child surface.
 *
 * Every primitive:
 *   - reads useMotion() for the active vibe spring + reduceMotion,
 *   - accepts a `transition` override that takes precedence over the
 *     vibe default (but never over reduceMotion),
 *   - collapses to an instant transition under prefers-reduced-motion
 *     (non-overridable),
 *   - forwards children + className.
 *
 * Springs come from the vibe personality unless a primitive is
 * conceptually fixed (Press always feels crisp, etc.).
 */

type DivProps = {
  className?: string;
  style?: CSSProperties;
  children?: ReactNode;
};

// ── Stagger context ──────────────────────────────────────────────
// Fade detects whether it sits inside a <Stagger>. When it does it
// renders as a variant child and lets the parent orchestrate timing;
// standalone it drives its own initial/animate.
const StaggerContext = createContext<boolean>(false);

// ── Direction helpers ────────────────────────────────────────────

export type FadeDirection = "up" | "down" | "left" | "right";

function fadeOffset(direction: FadeDirection | undefined, distance: number) {
  switch (direction) {
    case "up":
      return { y: distance };
    case "down":
      return { y: -distance };
    case "left":
      return { x: distance };
    case "right":
      return { x: -distance };
    default:
      return {};
  }
}

// ── Fade ─────────────────────────────────────────────────────────

interface FadeProps extends DivProps {
  /** Optional directional drift accompanying the fade. */
  direction?: FadeDirection;
  /** Pixels of drift when `direction` is set. */
  distance?: number;
  /** Override the vibe spring. Ignored under reduced-motion. */
  transition?: Transition;
  /** Entrance delay in seconds (added to the resolved transition). */
  delay?: number;
}

export function Fade({
  direction,
  distance = 8,
  transition,
  delay,
  className,
  style,
  children,
}: FadeProps) {
  const { spring, reduceMotion } = useMotion();
  const inStagger = useContext(StaggerContext);
  const offset = fadeOffset(direction, distance);

  if (reduceMotion) {
    return (
      <motion.div
        className={className}
        style={style}
        variants={inStagger ? REDUCED_CHILD_VARIANTS : undefined}
        initial={inStagger ? undefined : false}
        animate={inStagger ? undefined : { opacity: 1, x: 0, y: 0 }}
        transition={INSTANT_TRANSITION}
      >
        {children}
      </motion.div>
    );
  }

  const resolved: Transition = { ...(transition ?? spring), ...(delay ? { delay } : {}) };

  if (inStagger) {
    const variants: Variants = {
      hidden: { opacity: 0, ...offset },
      show: { opacity: 1, x: 0, y: 0, transition: resolved },
    };
    return (
      <motion.div className={className} style={style} variants={variants}>
        {children}
      </motion.div>
    );
  }

  return (
    <motion.div
      className={className}
      style={style}
      initial={{ opacity: 0, ...offset }}
      animate={{ opacity: 1, x: 0, y: 0 }}
      transition={resolved}
    >
      {children}
    </motion.div>
  );
}

// ── Scale ────────────────────────────────────────────────────────

interface ScaleProps extends DivProps {
  /** Starting scale. Defaults to a subtle 0.92. */
  from?: number;
  transition?: Transition;
  delay?: number;
}

export function Scale({
  from = 0.92,
  transition,
  delay,
  className,
  style,
  children,
}: ScaleProps) {
  const { spring, reduceMotion } = useMotion();

  if (reduceMotion) {
    return (
      <motion.div
        className={className}
        style={style}
        initial={false}
        animate={{ opacity: 1, scale: 1 }}
        transition={INSTANT_TRANSITION}
      >
        {children}
      </motion.div>
    );
  }

  const resolved: Transition = { ...(transition ?? spring), ...(delay ? { delay } : {}) };

  return (
    <motion.div
      className={className}
      style={style}
      initial={{ opacity: 0, scale: from }}
      animate={{ opacity: 1, scale: 1 }}
      transition={resolved}
    >
      {children}
    </motion.div>
  );
}

// ── Slide ────────────────────────────────────────────────────────
// Presence-aware: when used as the keyed child of an <AnimatePresence
// custom={dir}> it enters from `dir` and exits to the opposite side.
// `dir` is +1 (forward) or -1 (back). Standalone it just enters.

export type SlideAxis = "x" | "y";

interface SlideProps extends DivProps {
  /** Travel axis. Horizontal by default. */
  axis?: SlideAxis;
  /** +1 forward (enter from the leading edge), -1 back. */
  dir?: 1 | -1;
  /** Pixels travelled. */
  distance?: number;
  transition?: Transition;
}

const slideVariants = (axis: SlideAxis, distance: number): Variants => ({
  enter: (dir: number) => ({
    opacity: 0,
    [axis]: dir >= 0 ? distance : -distance,
  }),
  center: { opacity: 1, x: 0, y: 0 },
  exit: (dir: number) => ({
    opacity: 0,
    [axis]: dir >= 0 ? -distance : distance,
  }),
});

export function Slide({
  axis = "x",
  dir = 1,
  distance = 24,
  transition,
  className,
  style,
  children,
}: SlideProps) {
  const { spring, reduceMotion } = useMotion();

  if (reduceMotion) {
    return (
      <motion.div
        className={className}
        style={style}
        custom={dir}
        variants={REDUCED_SLIDE_VARIANTS}
        initial="enter"
        animate="center"
        exit="exit"
        transition={INSTANT_TRANSITION}
      >
        {children}
      </motion.div>
    );
  }

  return (
    <motion.div
      className={className}
      style={style}
      custom={dir}
      variants={slideVariants(axis, distance)}
      initial="enter"
      animate="center"
      exit="exit"
      transition={transition ?? spring}
    >
      {children}
    </motion.div>
  );
}

// ── Press ────────────────────────────────────────────────────────
// Crisp tactile feedback. Always uses SPRING_PRESS regardless of
// vibe. No scale change under reduced-motion.

interface PressProps extends DivProps {
  /** Scale on tap. */
  to?: number;
  transition?: Transition;
}

export function Press({ to = 0.97, transition, className, style, children }: PressProps) {
  const { reduceMotion } = useMotion();

  if (reduceMotion) {
    return (
      <div className={className} style={style}>
        {children}
      </div>
    );
  }

  return (
    <motion.div
      className={className}
      style={{ display: "inline-flex", ...style }}
      whileTap={{ scale: to }}
      transition={transition ?? SPRING_PRESS}
    >
      {children}
    </motion.div>
  );
}

// ── Hover ────────────────────────────────────────────────────────
// Slight lift + shadow bump on hover. Inert under reduced-motion.

interface HoverProps extends DivProps {
  /** Lift distance in px (negative = up). */
  lift?: number;
  transition?: Transition;
}

export function Hover({ lift = -2, transition, className, style, children }: HoverProps) {
  const { spring, reduceMotion } = useMotion();

  if (reduceMotion) {
    return (
      <div className={className} style={style}>
        {children}
      </div>
    );
  }

  return (
    <motion.div
      className={className}
      style={style}
      whileHover={{
        y: lift,
        boxShadow: "0 12px 32px rgba(0,0,0,0.10), 0 4px 10px rgba(0,0,0,0.06)",
      }}
      transition={transition ?? spring}
    >
      {children}
    </motion.div>
  );
}

// ── Stagger ──────────────────────────────────────────────────────
// Orchestrates the entrance timing of its children. Children should be
// <Fade> (or any variant-aware motion element); they pick up the
// hidden/show states automatically via StaggerContext.

type StaggerTag = "div" | "ul" | "ol" | "section" | "nav";

interface StaggerProps extends DivProps {
  /** Delay before the first child enters (seconds). */
  delay?: number;
  /** Gap between successive children (seconds). */
  step?: number;
  as?: StaggerTag;
}

export function Stagger({
  delay = 0,
  step = 0.06,
  as = "div",
  className,
  style,
  children,
}: StaggerProps) {
  const { reduceMotion } = useMotion();
  const MotionTag = motion[as];

  if (reduceMotion) {
    const Tag = as;
    return (
      <StaggerContext.Provider value={true}>
        <Tag className={className} style={style}>
          {children}
        </Tag>
      </StaggerContext.Provider>
    );
  }

  const containerVariants: Variants = {
    hidden: {},
    show: {
      transition: { staggerChildren: step, delayChildren: delay },
    },
  };

  return (
    <StaggerContext.Provider value={true}>
      <MotionTag
        className={className}
        style={style}
        variants={containerVariants}
        initial="hidden"
        animate="show"
      >
        {children}
      </MotionTag>
    </StaggerContext.Provider>
  );
}

// ── AmbientFloat ─────────────────────────────────────────────────
// Looped vertical drift for idle/decorative elements. Suspended (held
// static) under reduced-motion.

interface AmbientFloatProps extends DivProps {
  /** Drift amplitude in px. */
  amplitude?: number;
  /** Loop duration in seconds (4-6s reads as "alive but calm"). */
  duration?: number;
}

export function AmbientFloat({
  amplitude = 6,
  duration = 5,
  className,
  style,
  children,
}: AmbientFloatProps) {
  const { reduceMotion } = useMotion();

  if (reduceMotion) {
    return (
      <div className={className} style={style}>
        {children}
      </div>
    );
  }

  return (
    <motion.div
      className={className}
      style={style}
      animate={{ y: [0, -amplitude, 0] }}
      transition={{ duration, ease: "easeInOut", repeat: Infinity }}
    >
      {children}
    </motion.div>
  );
}

// ── ParallaxOnScroll ─────────────────────────────────────────────
// Translates Y against window scroll. depth 0 = pinned in viewport
// (strong parallax), depth 1 = scrolls naturally with content.

interface ParallaxOnScrollProps extends DivProps {
  /** 0..1. 0 = static in viewport, 1 = moves with content. */
  depth?: number;
}

export function ParallaxOnScroll({
  depth = 0.5,
  className,
  style,
  children,
}: ParallaxOnScrollProps) {
  const { reduceMotion } = useMotion();
  const { scrollY } = useScroll();
  const factor = 1 - Math.min(Math.max(depth, 0), 1);
  const y = useTransform(scrollY, (v) => v * factor);

  if (reduceMotion) {
    return (
      <div className={className} style={style}>
        {children}
      </div>
    );
  }

  return (
    <motion.div className={className} style={{ ...style, y }}>
      {children}
    </motion.div>
  );
}

// ── SharedLayout / SharedItem ────────────────────────────────────
// Shared-layout morph helpers. SharedItem elements with the same
// layoutId morph (position + size) between renders. Under
// reduced-motion the morph is disabled.

interface SharedLayoutProps {
  id?: string;
  children: ReactNode;
}

export function SharedLayout({ id, children }: SharedLayoutProps) {
  return <LayoutGroup id={id}>{children}</LayoutGroup>;
}

interface SharedItemProps extends DivProps {
  layoutId: string;
  transition?: Transition;
  role?: string;
  "aria-label"?: string;
  onClick?: () => void;
}

export function SharedItem({
  layoutId,
  transition,
  className,
  style,
  children,
  onClick,
  ...rest
}: SharedItemProps) {
  const { spring, reduceMotion } = useMotion();

  if (reduceMotion) {
    return (
      <div className={className} style={style} onClick={onClick} {...rest}>
        {children}
      </div>
    );
  }

  return (
    <motion.div
      layout
      layoutId={layoutId}
      className={className}
      style={style}
      transition={transition ?? spring}
      onClick={onClick}
      {...rest}
    >
      {children}
    </motion.div>
  );
}

// ── RouteTransition ──────────────────────────────────────────────
// Page-level entry/exit. Uses a custom cubic-bezier (route fades are
// the one place the design calls for a curve, not a spring). Reduced
// motion: instant fade, no translate.

const ROUTE_EASE: [number, number, number, number] = [0.32, 0.72, 0, 1];

interface RouteTransitionProps extends DivProps {
  /** Stable key for the current route/view. Change triggers exit+enter. */
  routeKey: string;
}

export function RouteTransition({ routeKey, className, style, children }: RouteTransitionProps) {
  const { reduceMotion } = useMotion();

  if (reduceMotion) {
    return (
      <AnimatePresence mode="wait">
        <motion.div
          key={routeKey}
          className={className}
          style={style}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={INSTANT_TRANSITION}
        >
          {children}
        </motion.div>
      </AnimatePresence>
    );
  }

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={routeKey}
        className={className}
        style={style}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -8 }}
        transition={{ duration: 0.24, ease: ROUTE_EASE }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}

// ── Reduced-motion variant fallbacks ─────────────────────────────

const REDUCED_CHILD_VARIANTS: Variants = {
  hidden: { opacity: 1, x: 0, y: 0 },
  show: { opacity: 1, x: 0, y: 0 },
};

const REDUCED_SLIDE_VARIANTS: Variants = {
  enter: { opacity: 1, x: 0, y: 0 },
  center: { opacity: 1, x: 0, y: 0 },
  exit: { opacity: 1, x: 0, y: 0 },
};
