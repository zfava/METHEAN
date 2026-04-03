"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { auth, children, governance, plans, type User, type RetentionSummary, type GovernanceEvent, type Plan } from "@/lib/api";
import StatusBadge from "@/components/StatusBadge";
import LoadingSkeleton from "@/components/LoadingSkeleton";

interface ChildSummary {
  id: string;
  name: string;
  retention: RetentionSummary | null;
  currentPlan: Plan | null;
}

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const [childSummaries, setChildSummaries] = useState<ChildSummary[]>([]);
  const [events, setEvents] = useState<GovernanceEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    try {
      const me = await auth.me();
      setUser(me);
      const evts = await governance.events(10);
      setEvents(evts);
    } catch {
      window.location.href = "/auth";
    } finally {
      setLoading(false);
    }
  }

  if (loading) return (
    <div className="max-w-6xl space-y-8">
      <LoadingSkeleton variant="text" count={1} />
      <LoadingSkeleton variant="card" count={3} />
      <LoadingSkeleton variant="list" count={5} />
    </div>
  );

  return (
    <div className="max-w-6xl">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-xl font-semibold">Dashboard</h1>
          <p className="text-sm text-(--color-text-secondary) mt-0.5">
            Welcome back, {user?.display_name}
          </p>
        </div>
        <button
          onClick={() => auth.logout().then(() => (window.location.href = "/auth"))}
          className="text-sm text-(--color-text-secondary) hover:text-(--color-text)"
        >
          Sign out
        </button>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <Link href="/maps" className="bg-white rounded-lg border border-(--color-border) p-5 hover:border-(--color-accent) transition-colors">
          <div className="text-sm font-medium">Learning Maps</div>
          <p className="text-xs text-(--color-text-secondary) mt-1">View and manage curriculum DAGs</p>
        </Link>
        <Link href="/plans" className="bg-white rounded-lg border border-(--color-border) p-5 hover:border-(--color-accent) transition-colors">
          <div className="text-sm font-medium">Weekly Plans</div>
          <p className="text-xs text-(--color-text-secondary) mt-1">Generate and approve learning plans</p>
        </Link>
        <Link href="/inspection" className="bg-white rounded-lg border border-(--color-border) p-5 hover:border-(--color-accent) transition-colors">
          <div className="text-sm font-medium">AI Inspection</div>
          <p className="text-xs text-(--color-text-secondary) mt-1">Review every AI decision</p>
        </Link>
      </div>

      {/* Governance Activity */}
      <div className="bg-white rounded-lg border border-(--color-border) p-5">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-semibold">Recent Governance Activity</h2>
          <Link href="/governance" className="text-xs text-(--color-accent) hover:underline">View all</Link>
        </div>
        {events.length === 0 ? (
          <p className="text-sm text-(--color-text-secondary)">No governance events yet. Generate a plan to get started.</p>
        ) : (
          <div className="space-y-2">
            {events.slice(0, 8).map((evt) => (
              <div key={evt.id} className="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
                <div className="flex items-center gap-3">
                  <StatusBadge status={evt.action} />
                  <span className="text-sm">{evt.target_type}</span>
                  {evt.reason && (
                    <span className="text-xs text-(--color-text-secondary) truncate max-w-xs">{evt.reason}</span>
                  )}
                </div>
                <span className="text-xs text-(--color-text-secondary)">
                  {new Date(evt.created_at).toLocaleString()}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
