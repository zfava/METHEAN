import type { Metadata } from "next";
import { Fraunces, Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import ClientProviders from "@/components/ClientProviders";
import ServiceWorkerRegistration from "@/components/ServiceWorkerRegistration";
import OfflineBanner from "@/components/OfflineBanner";
import AppLifecycle from "@/components/AppLifecycle";

// Fraunces is loaded as a variable font with the optical-size
// (opsz) and softness (SOFT) axes exposed. The .type-* helpers in
// globals.css set those axes per visible size so the same family
// reads as crisp display copy at 72px and as soft editorial copy at
// 19px. Omitting `weight` is required to keep the variable font;
// next/font otherwise selects static cuts and drops the axes.
const fraunces = Fraunces({
  subsets: ["latin"],
  axes: ["opsz", "SOFT"],
  style: ["normal", "italic"],
  variable: "--font-fraunces",
  display: "swap",
});

// Inter is the app-wide sans. All UI labels and body copy. The
// per-size tracking lives in the .font-inter-* helpers; Inter
// itself doesn't expose an optical-size axis.
const inter = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-inter",
  display: "swap",
});

const jetbrains = JetBrains_Mono({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-jetbrains",
  display: "swap",
});

export const viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  viewportFit: "cover" as const,
};

export const metadata: Metadata = {
  title: "METHEAN, a learning operating system for families",
  description: "AI-powered homeschool platform with parent governance. You set the rules. AI follows them. 51-state compliance. Start free.",
  icons: {
    icon: "/favicon.svg",
    apple: "/icons/apple-touch-icon.png",
  },
  manifest: "/manifest.json",
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "METHEAN",
  },
  other: {
    "mobile-web-app-capable": "yes",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${fraunces.variable} ${inter.variable} ${jetbrains.variable}`}
    >
      <head>
        <meta name="theme-color" content="#0F1B2D" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
      </head>
      <body className="antialiased">
        <ServiceWorkerRegistration />
        <AppLifecycle />
        <OfflineBanner />
        <ClientProviders>{children}</ClientProviders>
      </body>
    </html>
  );
}
