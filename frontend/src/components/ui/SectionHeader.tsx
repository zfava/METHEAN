"use client";

export default function SectionHeader({
  title,
  action,
  actionHref,
}: {
  title: string;
  action?: string;
  actionHref?: string;
}) {
  return (
    <div className="flex items-center justify-between mb-3">
      <h2 className="text-base font-medium text-(--color-text)">{title}</h2>
      {action && actionHref && (
        <a href={actionHref} className="text-xs text-(--color-accent) hover:underline">{action}</a>
      )}
    </div>
  );
}
