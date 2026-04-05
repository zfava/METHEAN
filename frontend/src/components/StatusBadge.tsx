"use client";

import { cn } from "@/lib/cn";

const styles: Record<string, string> = {
  mastered: "bg-(--color-success-light) text-(--color-success)",
  proficient: "bg-(--color-accent-light) text-(--color-accent)",
  developing: "bg-(--color-warning-light) text-(--color-warning)",
  emerging: "bg-orange-50 text-orange-700",
  not_started: "bg-(--color-page) text-(--color-text-tertiary)",
  available: "bg-(--color-accent-light) text-(--color-accent)",
  blocked: "bg-(--color-page) text-(--color-text-tertiary)",
  in_progress: "bg-(--color-warning-light) text-(--color-warning)",
  scheduled: "bg-(--color-accent-light) text-(--color-accent)",
  completed: "bg-(--color-success-light) text-(--color-success)",
  cancelled: "bg-(--color-page) text-(--color-text-tertiary)",
  approve: "bg-(--color-success-light) text-(--color-success)",
  reject: "bg-(--color-danger-light) text-(--color-danger)",
  modify: "bg-(--color-warning-light) text-(--color-warning)",
  defer: "bg-(--color-page) text-(--color-text-secondary)",
  draft: "bg-(--color-page) text-(--color-text-secondary)",
  active: "bg-(--color-accent-light) text-(--color-accent)",
  proposed: "bg-(--color-warning-light) text-(--color-warning)",
  approved: "bg-(--color-success-light) text-(--color-success)",
  rejected: "bg-(--color-danger-light) text-(--color-danger)",
  pending: "bg-(--color-warning-light) text-(--color-warning)",
  constitutional: "bg-(--color-constitutional-light) text-(--color-constitutional)",
  policy: "bg-(--color-page) text-(--color-text-secondary)",
  warning: "bg-(--color-warning-light) text-(--color-warning)",
  action_required: "bg-(--color-danger-light) text-(--color-danger)",
  info: "bg-(--color-accent-light) text-(--color-accent)",
};

export default function StatusBadge({ status, className = "" }: { status: string; className?: string }) {
  const style = styles[status] || "bg-(--color-page) text-(--color-text-secondary)";
  const label = status.replace(/_/g, " ");
  return (
    <span className={cn(
      "inline-block px-2 py-0.5 rounded-[4px] text-[11px] font-medium capitalize",
      style,
      className,
    )}>
      {label}
    </span>
  );
}
