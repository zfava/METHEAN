"use client";

const colors: Record<string, string> = {
  mastered: "bg-emerald-100 text-emerald-800",
  proficient: "bg-emerald-50 text-emerald-700",
  developing: "bg-amber-100 text-amber-800",
  emerging: "bg-amber-50 text-amber-700",
  not_started: "bg-gray-100 text-gray-600",
  available: "bg-blue-50 text-blue-700",
  blocked: "bg-gray-100 text-gray-500",
  in_progress: "bg-amber-100 text-amber-800",
  decaying: "bg-red-100 text-red-700",
  scheduled: "bg-blue-50 text-blue-700",
  completed: "bg-emerald-100 text-emerald-800",
  cancelled: "bg-gray-100 text-gray-500",
  approved: "bg-emerald-100 text-emerald-800",
  rejected: "bg-red-50 text-red-700",
  draft: "bg-gray-100 text-gray-600",
  active: "bg-blue-100 text-blue-800",
  pending: "bg-amber-100 text-amber-700",
  approve: "bg-emerald-100 text-emerald-800",
  reject: "bg-red-100 text-red-700",
  modify: "bg-amber-100 text-amber-800",
  defer: "bg-gray-100 text-gray-600",
};

export default function StatusBadge({ status, className = "" }: { status: string; className?: string }) {
  const style = colors[status] || "bg-gray-100 text-gray-600";
  const label = status.replace(/_/g, " ");
  return (
    <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium capitalize ${style} ${className}`}>
      {label}
    </span>
  );
}
