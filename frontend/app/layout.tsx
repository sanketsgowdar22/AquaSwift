import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "AquaSwift — Water Delivery Platform",
  description:
    "Order water in any quantity — from 20-litre jars to 100,000-litre bulk tankers. Fast delivery, quality assured.",
  keywords: ["water delivery", "tanker water", "drinking water", "AquaSwift", "Hyderabad"],
  openGraph: {
    title: "AquaSwift — Water Delivery Platform",
    description: "Pure water, swift delivery. Order water in any quantity.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
