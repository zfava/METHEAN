"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { account } from "@/lib/api";
import { MetheanLogoVertical } from "@/components/Brand";
import Card from "@/components/ui/Card";

function VerifyContent() {
  const params = useSearchParams();
  const token = params.get("token") || "";

  const [state, setState] = useState<"verifying" | "success" | "error">("verifying");

  useEffect(() => {
    if (!token) {
      setState("error");
      return;
    }
    account
      .verifyEmail(token)
      .then(() => setState("success"))
      .catch(() => setState("error"));
  }, [token]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-(--color-page) px-4">
      <div className="w-full max-w-sm">
        <div className="flex justify-center mb-6">
          <MetheanLogoVertical markSize={40} wordmarkHeight={16} color="#0F1B2D" gap={8} />
        </div>

        <Card>
          <div className="text-center py-4">
            {state === "verifying" && (
              <p className="text-sm text-(--color-text-secondary)">Verifying your email...</p>
            )}
            {state === "success" && (
              <>
                <p className="text-base font-semibold text-(--color-text) mb-1">Email verified</p>
                <p className="text-sm text-(--color-text-secondary) mb-4">
                  Your account is fully unlocked. Welcome to METHEAN.
                </p>
                <Link href="/dashboard" className="text-sm text-(--color-accent) hover:underline">
                  Go to your dashboard
                </Link>
              </>
            )}
            {state === "error" && (
              <>
                <p className="text-base font-semibold text-(--color-text) mb-1">
                  That link didn&apos;t work
                </p>
                <p className="text-sm text-(--color-text-secondary) mb-4">
                  The verification link is invalid or has expired. Sign in and use the banner to
                  request a fresh one.
                </p>
                <Link href="/auth" className="text-sm text-(--color-accent) hover:underline">
                  Back to sign in
                </Link>
              </>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}

export default function VerifyPage() {
  return (
    <Suspense fallback={null}>
      <VerifyContent />
    </Suspense>
  );
}
