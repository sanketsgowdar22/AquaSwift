import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "WoW — Water on Way | Water Delivery Platform",
  description:
    "Order water in any quantity — from 20-litre jars to 100,000-litre bulk tankers. Fast delivery, quality assured.",
  keywords: ["water delivery", "tanker water", "drinking water", "WoW", "Water on Way", "Hyderabad"],
  openGraph: {
    title: "WoW — Water on Way",
    description: "Pure water, on the way. Order water in any quantity.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
      </head>
      <body className="antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
