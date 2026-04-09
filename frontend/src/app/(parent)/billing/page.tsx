"use client";

import { useEffect, useState } from "react";
import { billing } from "@/lib/api";
import { useToast } from "@/components/Toast";
import PageHeader from "@/components/ui/PageHeader";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import { cn } from "@/lib/cn";

export default function BillingPage() {
  useEffect(() => { document.title = "Billing | METHEAN"; }, []);

  const { toast } = useToast();
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { load(); }, []);

  async function load() {
    setLoading(true);
    try {
      const s = await billing.status();
      setStatus(s);
    } catch { setStatus({ status: "trial", stripe_configured: false }); }
    finally { setLoading(false); }
  }

  async function handleSubscribe() {
    try {
      const { checkout_url } = await billing.subscribe();
      window.location.href = checkout_url;
    } catch (err: any) {
      toast(err?.detail || "Couldn't start checkout", "error");
    }
  }

  async function handlePortal() {
    try {
      const { portal_url } = await billing.portal();
      window.location.href = portal_url;
    } catch (err: any) {
      toast(err?.detail || "Couldn't open billing portal", "error");
    }
  }

  async function handleCancel() {
    if (!confirm("Cancel your subscription? You'll keep access until the end of your billing period.")) return;
    try {
      await billing.cancel();
      toast("Subscription will cancel at period end", "info");
      await load();
    } catch (err: any) {
      toast(err?.detail || "Couldn't cancel", "error");
    }
  }

  if (loading) return <div className="max-w-2xl"><PageHeader title="Billing" /><LoadingSkeleton variant="card" count={2} /></div>;

  const isTrial = status?.status === "trial" || status?.status === "trialing";
  const isActive = status?.status === "active";
  const isCanceled = status?.status === "canceled";
  const trialEnd = status?.trial_ends_at ? new Date(status.trial_ends_at) : null;
  const subEnd = status?.subscription_ends_at ? new Date(status.subscription_ends_at) : null;
  const daysLeft = trialEnd ? Math.max(0, Math.ceil((trialEnd.getTime() - Date.now()) / 86400000)) : null;

  return (
    <div className="max-w-2xl">
      <PageHeader title="Billing" subtitle="Manage your METHEAN subscription." />

      {/* Current plan status */}
      <Card className="mb-5" borderLeft={isActive ? "border-l-(--color-success)" : isTrial ? "border-l-(--gold)" : "border-l-(--color-danger)"}>
        <div className="flex items-center justify-between mb-3">
          <div>
            <h3 className="text-sm font-semibold text-(--color-text)">
              {isActive ? "Active Subscription" : isTrial ? "Free Trial" : isCanceled ? "Subscription Canceled" : "No Active Plan"}
            </h3>
            <p className="text-xs text-(--color-text-secondary) mt-0.5">
              {isActive && subEnd && `Next billing: ${subEnd.toLocaleDateString()}`}
              {isTrial && daysLeft != null && `${daysLeft} days remaining in your trial`}
              {isCanceled && subEnd && `Access until ${subEnd.toLocaleDateString()}`}
            </p>
          </div>
          <span className={cn(
            "px-3 py-1 text-xs font-semibold rounded-full",
            isActive ? "bg-(--color-success-light) text-(--color-success)" :
            isTrial ? "bg-(--color-warning-light) text-(--color-warning)" :
            "bg-(--color-danger-light) text-(--color-danger)"
          )}>
            {isActive ? "Active" : isTrial ? "Trial" : isCanceled ? "Canceled" : "Inactive"}
          </span>
        </div>

        {isTrial && daysLeft != null && (
          <div className="mb-4">
            <div className="w-full h-2 rounded-full bg-(--color-border)">
              <div className="h-full rounded-full bg-(--gold) transition-all" style={{ width: `${Math.max(5, (daysLeft / 30) * 100)}%` }} />
            </div>
          </div>
        )}

        <div className="flex gap-2">
          {!isActive && (
            <Button variant="gold" size="lg" onClick={handleSubscribe} disabled={!status?.stripe_configured}>
              {isTrial ? "Upgrade Now — $99/month" : "Subscribe — $99/month"}
            </Button>
          )}
          {isActive && (
            <>
              <Button variant="secondary" size="md" onClick={handlePortal}>Manage Subscription</Button>
              <Button variant="ghost" size="sm" onClick={handleCancel}>Cancel</Button>
            </>
          )}
        </div>
        {!status?.stripe_configured && (
          <p className="text-[10px] text-(--color-text-tertiary) mt-3">Stripe is not configured. Billing will be enabled in production.</p>
        )}
      </Card>

      {/* Plan details */}
      <Card className="mb-5">
        <h3 className="text-sm font-semibold text-(--color-text) mb-3">What's included</h3>
        <div className="space-y-2">
          {[
            "Unlimited children",
            "AI-powered curriculum generation",
            "Socratic tutor for every subject",
            "51-state compliance tracking",
            "Full governance system with constitutional rules",
            "Learner intelligence profiles",
            "Multi-year education planning",
            "Email notifications and weekly digests",
            "Document generation (transcripts, IHIPs, reports)",
            "Priority support",
          ].map((feature) => (
            <div key={feature} className="flex items-center gap-2 text-xs text-(--color-text-secondary)">
              <svg className="w-4 h-4 text-(--color-success) shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
              </svg>
              {feature}
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
