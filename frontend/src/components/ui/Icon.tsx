"use client";

import type { LucideIcon, LucideProps } from "@/lib/icons";

/**
 * Thin wrapper that enforces METHEAN icon defaults: stroke-width
 * 1.5, currentColor inheritance, and decorative-by-default a11y.
 *
 * If you need a one-off custom stroke or size, prefer setting them
 * on this wrapper rather than importing lucide-react directly so the
 * defaults remain the single source of truth.
 */
interface IconProps extends Omit<LucideProps, "ref" | "size" | "strokeWidth"> {
  icon: LucideIcon;
  /** Size in px. Default 16. The 4 canonical sizes: 14 (compact),
   *  16 (default UI), 20 (prominent), 24 (display). Pass an explicit
   *  number for anything outside the canonical set. */
  size?: 14 | 16 | 20 | 24 | number;
  /** Override stroke width. METHEAN default: 1.5.
   *  Use 1.75 for icons that need extra presence at small sizes;
   *  use 2 only when an existing semantic loud action depends on it. */
  strokeWidth?: number;
  /** If you pass a label, the icon is treated as semantic
   *  (aria-label set, aria-hidden removed). Default: decorative. */
  label?: string;
  className?: string;
}

export function Icon({
  icon: IconComponent,
  size = 16,
  strokeWidth = 1.5,
  label,
  className,
  ...rest
}: IconProps) {
  if (label) {
    return (
      <IconComponent
        size={size}
        strokeWidth={strokeWidth}
        aria-label={label}
        role="img"
        className={className}
        {...rest}
      />
    );
  }
  return (
    <IconComponent
      size={size}
      strokeWidth={strokeWidth}
      aria-hidden="true"
      className={className}
      {...rest}
    />
  );
}

export default Icon;
