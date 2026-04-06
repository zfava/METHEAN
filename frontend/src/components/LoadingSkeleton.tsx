"use client";

function Pulse({ className = "" }: { className?: string }) {
  return <div className={`animate-pulse bg-(--color-border) rounded ${className}`} />;
}

export default function LoadingSkeleton({
  variant = "card",
  count = 1,
}: {
  variant?: "card" | "list" | "table" | "text";
  count?: number;
}) {
  const items = Array.from({ length: count });

  if (variant === "card") {
    return (
      <div className="grid grid-cols-3 gap-4">
        {items.map((_, i) => (
          <div key={i} className="bg-(--color-surface) rounded-[10px] border border-(--color-border) p-5">
            <Pulse className="h-4 w-2/3 mb-3" />
            <Pulse className="h-3 w-full mb-2" />
            <Pulse className="h-3 w-1/2" />
          </div>
        ))}
      </div>
    );
  }

  if (variant === "list") {
    return (
      <div className="bg-(--color-surface) rounded-[10px] border border-(--color-border) divide-y divide-(--color-border)/30">
        {items.map((_, i) => (
          <div key={i} className="flex items-center gap-3 px-4 py-3">
            <Pulse className="h-5 w-5 rounded-full shrink-0" />
            <div className="flex-1">
              <Pulse className="h-3.5 w-1/3 mb-2" />
              <Pulse className="h-3 w-2/3" />
            </div>
            <Pulse className="h-3 w-16" />
          </div>
        ))}
      </div>
    );
  }

  if (variant === "table") {
    return (
      <div className="bg-(--color-surface) rounded-[10px] border border-(--color-border)">
        <div className="flex gap-4 px-4 py-3 border-b border-(--color-border)">
          <Pulse className="h-3 w-24" />
          <Pulse className="h-3 w-16" />
          <Pulse className="h-3 w-32" />
          <Pulse className="h-3 w-40 ml-auto" />
        </div>
        {items.map((_, i) => (
          <div key={i} className="flex gap-4 px-4 py-3 border-b border-(--color-border)/30 last:border-0">
            <Pulse className="h-3 w-24" />
            <Pulse className="h-3 w-16" />
            <Pulse className="h-3 w-32" />
            <Pulse className="h-3 w-40 ml-auto" />
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
          <Pulse className="h-4 w-1/4 mb-2" />
          <Pulse className="h-3 w-full mb-1" />
          <Pulse className="h-3 w-5/6" />
        </div>
      ))}
    </div>
  );
}
