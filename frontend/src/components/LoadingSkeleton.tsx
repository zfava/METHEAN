"use client";

function Shimmer({ className = "" }: { className?: string }) {
  return <div className={`animate-shimmer rounded ${className}`} />;
}

function CardShell({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <div
      className={`bg-(--color-surface) rounded-[14px] border border-(--color-border) p-5 ${className}`}
    >
      {children}
    </div>
  );
}

export default function LoadingSkeleton({
  variant = "card",
  count = 1,
}: {
  variant?: "card" | "list" | "table" | "text" | "dashboard" | "child";
  count?: number;
}) {
  const items = Array.from({ length: count });

  if (variant === "dashboard") {
    return (
      <div className="space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[0, 1, 2].map((i) => (
            <CardShell key={`metric-${i}`}>
              <Shimmer className="h-3 w-1/3 mb-3" />
              <Shimmer className="h-7 w-1/2 mb-2" />
              <Shimmer className="h-3 w-2/3" />
            </CardShell>
          ))}
        </div>
        <CardShell>
          <Shimmer className="h-4 w-1/4 mb-4" />
          <Shimmer className="h-3 w-full mb-2" />
          <Shimmer className="h-3 w-5/6 mb-2" />
          <Shimmer className="h-3 w-3/4" />
        </CardShell>
        <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) divide-y divide-(--color-border)/30">
          {[0, 1, 2, 3].map((i) => (
            <div key={`row-${i}`} className="flex items-center gap-3 px-4 py-3">
              <Shimmer className="h-5 w-5 rounded-full shrink-0" />
              <div className="flex-1">
                <Shimmer className="h-3.5 w-1/3 mb-2" />
                <Shimmer className="h-3 w-2/3" />
              </div>
              <Shimmer className="h-3 w-16" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (variant === "child") {
    return (
      <div className="space-y-4">
        <CardShell>
          <div className="flex items-center gap-4">
            <Shimmer className="h-12 w-12 rounded-full shrink-0" />
            <div className="flex-1">
              <Shimmer className="h-5 w-1/3 mb-2" />
              <Shimmer className="h-3 w-1/4" />
            </div>
            <Shimmer className="h-9 w-24 rounded-[10px]" />
          </div>
        </CardShell>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[0, 1, 2, 3].map((i) => (
            <CardShell key={`stat-${i}`} className="p-4">
              <Shimmer className="h-3 w-2/3 mb-2" />
              <Shimmer className="h-6 w-1/2" />
            </CardShell>
          ))}
        </div>
        <div className="space-y-2">
          {[0, 1, 2, 3, 4].map((i) => (
            <div
              key={`activity-${i}`}
              className="flex items-center gap-3 px-4 py-3 bg-(--color-surface) rounded-[12px] border border-(--color-border)"
            >
              <Shimmer className="h-9 w-9 rounded-[8px] shrink-0" />
              <div className="flex-1">
                <Shimmer className="h-3.5 w-2/5 mb-1.5" />
                <Shimmer className="h-3 w-3/5" />
              </div>
              <Shimmer className="h-6 w-16 rounded-full" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (variant === "card") {
    return (
      <div className="grid grid-cols-3 gap-4">
        {items.map((_, i) => (
          <CardShell key={i}>
            <Shimmer className="h-4 w-2/3 mb-3" />
            <Shimmer className="h-3 w-full mb-2" />
            <Shimmer className="h-3 w-1/2" />
          </CardShell>
        ))}
      </div>
    );
  }

  if (variant === "list") {
    return (
      <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border) divide-y divide-(--color-border)/30">
        {items.map((_, i) => (
          <div key={i} className="flex items-center gap-3 px-4 py-3">
            <Shimmer className="h-5 w-5 rounded-full shrink-0" />
            <div className="flex-1">
              <Shimmer className="h-3.5 w-1/3 mb-2" />
              <Shimmer className="h-3 w-2/3" />
            </div>
            <Shimmer className="h-3 w-16" />
          </div>
        ))}
      </div>
    );
  }

  if (variant === "table") {
    return (
      <div className="bg-(--color-surface) rounded-[14px] border border-(--color-border)">
        <div className="flex gap-4 px-4 py-3 border-b border-(--color-border)">
          <Shimmer className="h-3 w-24" />
          <Shimmer className="h-3 w-16" />
          <Shimmer className="h-3 w-32" />
          <Shimmer className="h-3 w-40 ml-auto" />
        </div>
        {items.map((_, i) => (
          <div key={i} className="flex gap-4 px-4 py-3 border-b border-(--color-border)/30 last:border-0">
            <Shimmer className="h-3 w-24" />
            <Shimmer className="h-3 w-16" />
            <Shimmer className="h-3 w-32" />
            <Shimmer className="h-3 w-40 ml-auto" />
          </div>
        ))}
      </div>
    );
  }

  // variant === "text"
  return (
    <div className="space-y-3">
      {items.map((_, i) => (
        <div key={i}>
          <Shimmer className="h-4 w-1/4 mb-2" />
          <Shimmer className="h-3 w-full mb-1" />
          <Shimmer className="h-3 w-5/6" />
        </div>
      ))}
    </div>
  );
}
