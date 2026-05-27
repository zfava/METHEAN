"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { PAYWALL_EVENT, type PaywallEventDetail } from "@/lib/api";
import SubscriptionRequired from "./SubscriptionRequired";

/**
 * Layout-level paywall handler. The api client dispatches PAYWALL_EVENT
 * on every 402; we listen here and swap children for the branded
 * SubscriptionRequired screen so the user never sees a crash or a raw
 * error toast. Apply once at the parent app layout; every gated page
 * inherits the behaviour without needing its own catch.
 *
 * The /billing page is exempt: when a user lands there to reactivate
 * after a lapse, we let the page render so its own subscribe button
 * works. The paywall would otherwise occlude the very screen the user
 * needs.
 */
export default function SubscriptionGate({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [paywall, setPaywall] = useState<PaywallEventDetail | null>(null);

  // Reset when the user navigates: a fresh page may not be gated.
  useEffect(() => {
    setPaywall(null);
  }, [pathname]);

  useEffect(() => {
    const onPaywall = (e: Event) => {
      const ce = e as CustomEvent<PaywallEventDetail>;
      if (!ce.detail) return;
      setPaywall(ce.detail);
    };
    window.addEventListener(PAYWALL_EVENT, onPaywall);
    return () => window.removeEventListener(PAYWALL_EVENT, onPaywall);
  }, []);

  if (paywall && pathname !== "/billing") {
    return <SubscriptionRequired status={paywall.status} />;
  }

  return <>{children}</>;
}
