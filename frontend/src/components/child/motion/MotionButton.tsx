"use client";

import { motion, type HTMLMotionProps } from "framer-motion";
import { forwardRef, type ReactNode } from "react";

import { useMotion } from "@/lib/motion/MotionContext";
import { useSoundCue } from "@/lib/useSoundCue";
import { MOTION_DURATIONS_SEC, MOTION_EASINGS } from "@/lib/motion/tokens";

type MotionButtonRest = Omit<
  HTMLMotionProps<"button">,
  "onClick" | "ref" | "children" | "whileHover" | "whileTap" | "style" | "className"
>;

/**
 * Tactile button primitive. Wraps a native button so a11y stays
 * intact. Variants mirror the existing /ui/Button system but the
 * primitive owns the physics:
 *   - 0.96 scale + brightness drop on press, micro easing, 120ms.
 *   - Gold rim glow on hover when variant="gold".
 *
 * Plays an "activity_start" cue at low volume on press. Sound system
 * already gates by sound_pack=off and pre-gesture; the call is
 * cheap when those gates are closed.
 */
interface MotionButtonProps {
  variant?: "gold" | "primary" | "ghost" | "success";
  size?: "sm" | "md" | "lg";
  onPress?: () => void;
  children: ReactNode;
  className?: string;
  disabled?: boolean;
  type?: "button" | "submit" | "reset";
  "aria-label"?: string;
  "aria-pressed"?: boolean;
  title?: string;
  style?: React.CSSProperties;
}

const VARIANT_CLASS: Record<NonNullable<MotionButtonProps["variant"]>, string> = {
  gold: "bg-(--color-brand-gold) text-(--color-text-inverse) border border-(--color-brand-gold) hover:opacity-95",
  primary: "bg-(--color-accent) text-white border border-(--color-accent) hover:opacity-95",
  ghost:
    "bg-transparent text-(--color-text) border border-(--color-border) hover:bg-(--color-page)",
  success: "bg-(--color-success) text-white border border-(--color-success) hover:opacity-95",
};

const SIZE_CLASS: Record<NonNullable<MotionButtonProps["size"]>, string> = {
  sm: "px-3 py-2 text-sm rounded-lg",
  md: "px-4 py-2.5 text-sm rounded-xl",
  lg: "px-6 py-3.5 text-base rounded-2xl",
};

export const MotionButton = forwardRef<HTMLButtonElement, MotionButtonProps>(function MotionButton(
  {
    variant = "primary",
    size = "md",
    onPress,
    children,
    className,
    disabled,
    type = "button",
    style,
    ...rest
  },
  ref,
) {
  const { reduceMotion, speed } = useMotion();
  const playCue = useSoundCue();

  const microDuration = MOTION_DURATIONS_SEC.micro / speed;

  const handleClick = () => {
    if (disabled) return;
    playCue("activity_start", { volume: 0.3 });
    onPress?.();
  };

  const variantClass = VARIANT_CLASS[variant];
  const sizeClass = SIZE_CLASS[size];

  const goldHaloStyle =
    variant === "gold"
      ? {
          boxShadow:
            "0 0 0 1px rgba(255,255,255,0.1) inset, 0 6px 18px rgba(198,162,78,0.20), 0 2px 4px rgba(198,162,78,0.18)",
        }
      : undefined;

  const goldHaloHover =
    variant === "gold"
      ? {
          boxShadow:
            "0 0 0 1px rgba(255,255,255,0.18) inset, 0 12px 32px rgba(198,162,78,0.40), 0 4px 8px rgba(198,162,78,0.28)",
        }
      : undefined;

  if (reduceMotion) {
    return (
      <button
        ref={ref}
        type={type}
        disabled={disabled}
        onClick={handleClick}
        className={[
          "inline-flex items-center justify-center font-medium transition-colors disabled:opacity-40 disabled:cursor-not-allowed",
          variantClass,
          sizeClass,
          className ?? "",
        ]
          .filter(Boolean)
          .join(" ")}
        style={{ ...goldHaloStyle, ...(style ?? {}) }}
        {...rest}
      >
        {children}
      </button>
    );
  }

  return (
    <motion.button
      ref={ref}
      type={type}
      disabled={disabled}
      onClick={handleClick}
      className={[
        "inline-flex items-center justify-center font-medium disabled:opacity-40 disabled:cursor-not-allowed",
        variantClass,
        sizeClass,
        className ?? "",
      ]
        .filter(Boolean)
        .join(" ")}
      style={{ ...goldHaloStyle, ...(style ?? {}) }}
      whileHover={disabled ? undefined : goldHaloHover}
      whileTap={
        disabled
          ? undefined
          : {
              scale: 0.96,
              filter: "brightness(0.96)",
              transition: { duration: microDuration, ease: MOTION_EASINGS.micro },
            }
      }
      {...(rest as MotionButtonRest)}
    >
      {children}
    </motion.button>
  );
});

export default MotionButton;
