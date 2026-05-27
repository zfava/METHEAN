"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { auth } from "@/lib/api";
import LandingPage from "@/components/landing/LandingPage";

// Public landing renders immediately so first paint shows the cinematic
// design (and so JS-disabled visitors still see the full page). A
// background auth check redirects authenticated visitors to the dashboard.
export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    auth
      .me()
      .then(() => router.replace("/dashboard"))
      .catch(() => {
        // Not signed in; stay on the landing.
      });
  }, [router]);

  return <LandingPage />;
}
