"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { EMAIL_NOT_VERIFIED_EVENT, account, auth } from "@/lib/api";

/**
 * Layout-level handler for the backend verified-email gate. The api
 * client dispatches EMAIL_NOT_VERIFIED_EVENT on every 403 whose detail
 * is "email_not_verified"; we listen here and swap children for a
 * dedicated verification banner so the raw gate code never reaches a
 * page's own error card (which would otherwise render it with a Retry
 * button). Mirrors SubscriptionGate (the 402 paywall): apply once at the
 * parent layout and every gated page inherits the behaviour without its
 * own catch.
 *
 * The gate resets on navigation. The verified-email gate only guards
 * child-data routes, so ungated surfaces (billing, data export, logout,
 * notification settings) never fire the event; the user can still reach
 * them from the sidebar to pay, leave, or simply wait for the link.
 */
export default function VerifyEmailGate({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [gated, setGated] = useState(false);
  const [email, setEmail] = useState<string | null>(null);
  const [sent, setSent] = useState(false);

  // A freshly navigated page may not be gated; clear on route change.
  useEffect(() => {
    setGated(false);
    setSent(false);
  }, [pathname]);

  useEffect(() => {
    const onGate = () => setGated(true);
    window.addEventListener(EMAIL_NOT_VERIFIED_EVENT, onGate);
    return () => window.removeEventListener(EMAIL_NOT_VERIFIED_EVENT, onGate);
  }, []);

  // Greet the user by the address the link was sent to. /auth/me is
  // ungated, so it resolves even while child data stays blocked.
  useEffect(() => {
    if (!gated || email) return;
    let cancelled = false;
    auth
      .me()
      .then((u) => {
        if (!cancelled) setEmail(u.email);
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, [gated, email]);

  if (!gated) return <>{children}</>;

  return (
    <div
      role="alert"
      className="bg-(--color-warning) text-(--color-text) rounded-[12px] px-5 py-4 flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-4"
    >
      <div className="flex-1">
        <p className="text-sm font-semibold">Verify your email to continue.</p>
        <p className="text-sm">
          {email ? `We sent a link to ${email}.` : "We sent a link to your inbox."}
        </p>
      </div>
      <button
        disabled={sent}
        onClick={async () => {
          try {
            await account.resendVerification();
          } finally {
            setSent(true);
          }
        }}
        className="px-3 py-1.5 text-sm font-semibold rounded-[8px] bg-white text-(--color-text) disabled:opacity-60 whitespace-nowrap"
      >
        {sent ? "Sent. Check your inbox." : "Resend email"}
      </button>
    </div>
  );
}
