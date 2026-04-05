/**
 * Utility for merging Tailwind class names.
 * Combines clsx-style conditional classes with deduplication.
 */
export function cn(...inputs: (string | undefined | null | false)[]): string {
  return inputs.filter(Boolean).join(" ");
}
