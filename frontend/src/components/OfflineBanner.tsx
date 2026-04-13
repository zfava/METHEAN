"use client";

import { useEffect, useState } from "react";

type Status = "online" | "offline" | "reconnected";

export default function OfflineBanner() {
  const [status, setStatus] = useState<Status>("online");

  useEffect(() => {
    if (!navigator.onLine) setStatus("offline");

    function goOffline() { setStatus("offline"); }
    function goOnline() {
      setStatus("reconnected");
      setTimeout(() => setStatus("online"), 3000);
    }

    window.addEventListener("offline", goOffline);
    window.addEventListener("online", goOnline);
    return () => {
      window.removeEventListener("offline", goOffline);
      window.removeEventListener("online", goOnline);
    };
  }, []);

  if (status === "online") return null;

  return (
    <div
      role="status"
      aria-live="polite"
      className="fixed left-0 right-0 z-50 flex items-center justify-center px-4 py-2 text-sm font-medium"
      style={{
        top: "calc(48px + var(--safe-top, 0px))",
        background: status === "offline" ? "var(--color-warning-light)" : "var(--color-success-light)",
        color: status === "offline" ? "var(--color-warning)" : "var(--color-success)",
        borderBottom: `1px solid ${status === "offline" ? "var(--color-warning)" : "var(--color-success)"}`,
      }}
    >
      {status === "offline"
        ? "You\u2019re offline. Showing cached data."
        : "Back online"}
    </div>
  );
}
