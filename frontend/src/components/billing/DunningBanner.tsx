"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { billing } from "@/lib/api";

/**
 * Global banner for failed-payment recovery (dunning), shown at the
 * parent layout level like DeletionPendingBanner so the family sees it
 * even if they never open the billing page. Hidden on /billing itself,
 * where the page renders its own fuller state card.
 *
 * grace: gentle fix-payment prompt, everything still works.
 * restricted: states plainly what is paused and that records and
 * exports remain available.
 * canceled: reactivation path.
 */
export default function DunningBanner() {
  const pathname = usePathname();
  const [state, setState] = useState<string>("none");
  const [graceEnds, setGraceEnds] = useState<string | null>(null);
  const [cancelsAt, setCancelsAt] = useState<string | null>(null);

  useEffect(() => {
    billing
      .status()
      .then((s) => {
        setState(s?.dunning_state || "none");
        setGraceEnds(s?.dunning_grace_ends_at || null);
        setCancelsAt(s?.dunning_cancels_at || null);
      })
      .catch(() => {});
  }, []);

  if (pathname === "/billing") return null;
  if (state !== "grace" && state !== "restricted" && state !== "canceled") return null;

  const fmt = (iso: string | null) =>
    iso ? new Date(iso).toLocaleDateString(undefined, { month: "long", day: "numeric" }) : null;

  async function openPortal() {
    try {
      const { portal_url } = await billing.portal();
      window.location.href = portal_url;
    } catch {
      window.location.href = "/billing";
    }
  }

  if (state === "grace") {
    return (
      <div className="bg-(--color-warning-light) text-(--color-text) px-4 py-3 flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4">
        <p className="text-sm flex-1">
          A payment didn&apos;t go through. Everything still works
          {fmt(graceEnds) ? <> through <strong>{fmt(graceEnds)}</strong></> : null}; updating your
          card takes about a minute.
        </p>
        <button
          onClick={openPortal}
          className="px-3 py-1.5 text-sm font-semibold rounded-[8px] bg-white text-(--color-text) shrink-0"
        >
          Update payment method
        </button>
      </div>
    );
  }

  if (state === "restricted") {
    return (
      <div className="bg-(--color-warning) text-(--color-text) px-4 py-3 flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4">
        <p className="text-sm flex-1">
          Paid features are paused while a payment is outstanding. Your family&apos;s records are
          safe and exportable
          {fmt(cancelsAt) ? (
            <>; the subscription cancels on <strong>{fmt(cancelsAt)}</strong> unless payment is updated</>
          ) : null}
          .
        </p>
        <button
          onClick={openPortal}
          className="px-3 py-1.5 text-sm font-semibold rounded-[8px] bg-white text-(--color-text) shrink-0"
        >
          Update payment method
        </button>
      </div>
    );
  }

  return (
    <div className="bg-(--color-danger) text-white px-4 py-3 flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4">
      <p className="text-sm flex-1">
        Your subscription was canceled after a payment problem. Your family&apos;s records remain
        intact and exportable; reactivate any time to pick up where you left off.
      </p>
      <a
        href="/billing"
        className="px-3 py-1.5 text-sm font-semibold rounded-[8px] bg-white text-(--color-danger) shrink-0 text-center"
      >
        Reactivate
      </a>
    </div>
  );
}
