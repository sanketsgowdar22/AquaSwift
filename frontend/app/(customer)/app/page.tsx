"use client";

import { useAuth } from "@/lib/auth";
import { Droplets, ChevronRight, Shield, Zap, Truck, CreditCard } from "lucide-react";
import Link from "next/link";
import WowLogo from "@/components/wow-logo";

const WATER_TYPES = [
  { label: "Drinking Water", desc: "Pure & Safe", icon: "💧", color: "bg-blue-50 border-blue-200" },
  { label: "Basic / Utility Water", desc: "For daily needs", icon: "🚿", color: "bg-cyan-50 border-cyan-200" },
];

const SIZES = [
  { label: "20 Ltr", sub: "Jar", icon: "🫙" },
  { label: "500 Ltr", sub: "", icon: "🛢️" },
  { label: "1000 Ltr", sub: "", icon: "🚰" },
  { label: "Tanker", sub: "", icon: "🚚" },
];

const FEATURES = [
  { icon: Shield, label: "100% Purified", desc: "RO + UV treated" },
  { icon: Zap, label: "Express 30-min", desc: "Instant delivery" },
  { icon: Truck, label: "Live Tracking", desc: "Real-time updates" },
  { icon: CreditCard, label: "Easy Payment", desc: "UPI, Cards, COD" },
];

export default function CustomerHomePage() {
  const { user } = useAuth();

  return (
    <div className="animate-fade-in">
      {/* Hero Card */}
      <div className="bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 mx-4 mt-4 rounded-2xl p-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-32 h-32 rounded-full bg-white/5 -translate-y-1/3 translate-x-1/3" />
        <div className="absolute bottom-0 left-0 w-24 h-24 rounded-full bg-accent-500/10 translate-y-1/3 -translate-x-1/3" />

        <div className="relative z-10">
          <WowLogo variant="icon" size="sm" className="mb-3 bg-white rounded-lg px-1.5 py-1" />
          <h1 className="text-white text-xl font-bold mb-1">Pure Water</h1>
          <h2 className="text-accent-400 text-2xl font-bold mb-2">On the Way!</h2>
          <p className="text-white/70 text-sm mb-4">
            Drinking water & basic utility water delivered safely to your doorstep.
          </p>
          <Link
            href="/app/product"
            className="inline-flex items-center gap-2 bg-white text-primary-700 font-semibold text-sm px-5 py-2.5 rounded-xl hover:bg-white/90 transition-colors"
          >
            Order Now <ChevronRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      {/* What do you need? */}
      <div className="px-4 mt-6">
        <h3 className="text-base font-semibold text-text-primary mb-3">What do you need?</h3>
        <div className="grid grid-cols-2 gap-3">
          {WATER_TYPES.map((type) => (
            <Link
              key={type.label}
              href="/app/product"
              className={`border rounded-xl p-4 flex flex-col items-center text-center hover:shadow-md transition-shadow ${type.color}`}
            >
              <span className="text-3xl mb-2">{type.icon}</span>
              <span className="text-sm font-semibold text-text-primary">{type.label}</span>
              <span className="text-xs text-text-secondary mt-0.5">{type.desc}</span>
            </Link>
          ))}
        </div>
      </div>

      {/* Popular Sizes */}
      <div className="px-4 mt-6">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-base font-semibold text-text-primary">Popular Sizes</h3>
          <Link href="/app/product" className="text-primary-600 text-xs font-medium flex items-center gap-1">
            View all <ChevronRight className="w-3 h-3" />
          </Link>
        </div>
        <div className="flex gap-3 overflow-x-auto pb-2 scrollbar-hide">
          {SIZES.map((size) => (
            <Link
              key={size.label}
              href="/app/product"
              className="flex-shrink-0 w-20 bg-white border border-border rounded-xl p-3 flex flex-col items-center text-center hover:border-primary-300 transition-colors"
            >
              <span className="text-2xl mb-1.5">{size.icon}</span>
              <span className="text-xs font-semibold text-text-primary">{size.label}</span>
              {size.sub && <span className="text-[10px] text-text-muted">{size.sub}</span>}
            </Link>
          ))}
        </div>
      </div>

      {/* Why Choose WoW */}
      <div className="px-4 mt-6 mb-6">
        <h3 className="text-base font-semibold text-text-primary mb-3">Why Choose WoW?</h3>
        <div className="grid grid-cols-2 gap-3">
          {FEATURES.map((f) => (
            <div key={f.label} className="bg-white border border-border rounded-xl p-3 flex items-start gap-3">
              <div className="w-9 h-9 rounded-lg bg-primary-50 flex items-center justify-center shrink-0">
                <f.icon className="w-4.5 h-4.5 text-primary-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-text-primary">{f.label}</p>
                <p className="text-xs text-text-muted">{f.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
