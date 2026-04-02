import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "METHEAN",
  description: "Learning governance operating system for homeschool families",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
