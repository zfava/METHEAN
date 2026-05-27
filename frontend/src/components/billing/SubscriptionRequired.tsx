"use client";

import Link from "next/link";
import { useState } from "react";
import { billing } from "@/lib/api";
import { ArrowRight } from "@/lib/icons";
import { Icon } from "@/components/ui/Icon";
import "@/components/landing/landing.css";

/**
 * Branded paywall shown whenever a gated API call returns 402. Lives
 * inside the parent-app shell, but inherits its visual language from
 * the landing page (navy hero + gold gradient headline + Fraunces +
 * JetBrains Mono eyebrows). It is intentionally NOT a system error
 * surface; this is the revenue moment.
 *
 * The primary CTA hits the real billing.subscribe() endpoint, which
 * creates a Stripe checkout session and returns its URL. We never
 * navigate to the relative checkout_url hint from the 402 payload
 * because that hint is not a Stripe-hosted page.
 *
 * Copy branches on `status`:
 *   - "trialing" / "active": should never reach here (gate passes); render
 *     a generic safe message just in case.
 *   - "canceled" / "past_due" / "paused" / "unpaid" / "incomplete_expired":
 *     lapsed-account copy. Trial is exhausted; CTA reads "Reactivate".
 *   - everything else (unknown, incomplete, never-subscribed): new-trial
 *     copy. CTA reads "Start Your Free Trial".
 */
interface SubscriptionRequiredProps {
  status?: string;
}

const LAPSED_STATUSES = new Set([
  "canceled",
  "past_due",
  "paused",
  "unpaid",
  "incomplete_expired",
]);

const SHIELD_PATH =
  "M 50 2 C 58 2, 80 11, 93 17 C 94 17.5, 94 18.5, 94 20 L 94 56 C 94 72, 88 86, 76 96 C 68 103, 58 109, 50 113 C 42 109, 32 103, 24 96 C 12 86, 6 72, 6 56 L 6 20 C 6 18.5, 6 17.5, 7 17 C 20 11, 42 2, 50 2 Z M 21.5 84.5 L 21 28 L 50 51 L 79 28 L 78.5 84.5 L 65.5 84.5 L 65 46 L 50 58.5 L 35 46 L 34.5 84.5 Z";

const ShieldMark = ({ size = 48 }: { size?: number }) => (
  <svg
    viewBox="0 0 100 115"
    width={size * 0.875}
    height={size}
    fill="none"
    aria-hidden="true"
  >
    <path fillRule="evenodd" clipRule="evenodd" d={SHIELD_PATH} fill="#C6A24E" />
  </svg>
);

const ArrowIcon = () => <Icon icon={ArrowRight} size={16} strokeWidth={2} />;

export default function SubscriptionRequired({ status }: SubscriptionRequiredProps) {
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const isLapsed = status ? LAPSED_STATUSES.has(status) : false;

  const eyebrow = isLapsed ? "Your METHEAN trial has ended" : "Founding Family · Now opening";
  const headline = isLapsed ? "Welcome back." : "Your children.";
  const headlineEm = isLapsed ? "Reactivate to continue." : "Your rules. Your system.";
  const subline = isLapsed
    ? "Your subscription has lapsed, so the curriculum builder, mastery records, governance trail, and your children's plans are paused. Reactivate to pick up exactly where you left off; nothing has been deleted."
    : "METHEAN is the first learning operating system built so the family stays sovereign. A full year of curriculum, drafted for your philosophy. Every AI recommendation routed through you before it touches your child. All fifty-one jurisdictions, unlimited children, one subscription.";

  const ctaLabel = isLapsed ? "Reactivate Subscription" : "Start Your Free Trial";
  const trialNote = isLapsed
    ? "14-day trial · $99 per household per month · Cancel any time"
    : "14-day free trial · $99 per household per month · Cancel any time";

  async function handleStart() {
    setError(null);
    setSubmitting(true);
    try {
      const { checkout_url } = await billing.subscribe();
      window.location.href = checkout_url;
    } catch (err: unknown) {
      const msg =
        err instanceof Error
          ? err.message
          : "We couldn't reach checkout. Please try again, or contact zack@methean.io.";
      setError(msg);
      setSubmitting(false);
    }
  }

  const features = [
    "Full year of curriculum, drafted to your philosophy",
    "Every AI recommendation routed through your approval",
    "All 51 jurisdictions, hour tracking, document generation",
    "Unlimited children on one subscription",
    "Mastery records with retention, not just completion",
    "Full export and deletion, your data stays yours",
  ];

  return (
    <div className="cinematic-landing subscription-required-screen">
      <section className="paywall-hero">
        <div className="hero-bg" aria-hidden />
        <div className="hero-grain" aria-hidden />
        <div className="hero-content paywall-wrap">
          <div className="paywall-mark" aria-hidden>
            <ShieldMark size={56} />
          </div>
          <div className="hero-status paywall-status">
            <span className="live-dot" />
            <span>{eyebrow}</span>
          </div>
          <h1 className="paywall-headline">
            <span className="ln">{headline}</span>
            <span className="ln">
              <span className="gradient">{headlineEm}</span>
            </span>
          </h1>
          <p className="paywall-sub">{subline}</p>

          <ul className="paywall-features">
            {features.map((f) => (
              <li key={f}>
                <span className="paywall-feature-dot" aria-hidden />
                {f}
              </li>
            ))}
          </ul>

          <div className="paywall-cta-row">
            <button
              type="button"
              onClick={handleStart}
              disabled={submitting}
              className="cin-btn cin-btn-gold paywall-cta"
            >
              {submitting ? "Opening checkout…" : ctaLabel}
              <ArrowIcon />
            </button>
            <Link href="/dashboard" className="cin-btn cin-btn-ghost paywall-back">
              Return to Dashboard
            </Link>
          </div>

          {error ? (
            <p className="paywall-error" role="alert">
              {error}
            </p>
          ) : (
            <p className="paywall-trust">{trialNote}</p>
          )}

          <p className="paywall-foot">
            Already subscribed?{" "}
            <Link href="/billing">Manage your billing</Link> · Questions?{" "}
            <a href="mailto:zack@methean.io">zack@methean.io</a>
          </p>
        </div>
      </section>
    </div>
  );
}
