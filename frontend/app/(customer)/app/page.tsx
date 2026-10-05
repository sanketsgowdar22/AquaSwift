"use client";

import { useQuery } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { Droplets, ChevronRight, Star, Shield, Zap, MapPin } from "lucide-react";
import Link from "next/link";

const FEATURES = [
  { icon: Droplets, label: "Multiple Water Types", desc: "Drinking & Utility Water" },
  { icon: Zap, label: "Fast Delivery", desc: "Within 45-60 minutes" },
  { icon: Shield, label: "Quality Assured", desc: "100% safe & tested" },
  { icon: Star, label: "Ratings & Reviews", desc: "Rate your experience" },
];

const SIZES = [
  { label: "20L Jar", litres: 20, icon: "🫙" },
  { label: "500L", litres: 500, icon: "🛢️" },
  { label: "1000L", litres: 1000, icon: "🚰" },
  { label: "Tanker", litres: 5000, icon: "🚚" },
];

export default function CustomerHomePage() {
  const { user } = useAuth();
  const { data: purposes } = useQuery({ queryKey: ["purposes"], queryFn: adminApi.purposes });

  return (
    <div className="animate-fade-in">
      {/* Hero */}
      <div className="bg-gradient-to-br from-primary-500 via-primary-600 to-primary-700 px-5 pt-5 pb-8 rounded-b-3xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-40 h-40 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2" />
        <div className="absolute bottom-0 left-0 w-32 h-32 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2" />

        <div className="relative z-10">
          <div className="flex items-center gap-2 mb-4">
            <MapPin className="w-4 h-4 text-primary-200" />
            <span className="text-primary-200 text-sm">Deliver to</span>
            <span className="text-white text-sm font-medium">Current Location ▾</span>
          </div>

          <h2 className="text-2xl font-bold text-white leading-tight mb-2">
            Pure Water,<br />
            <span className="text-accent-400">On the Way!</span>
          </h2>
          <p className="text-primary-200 text-sm mb-5">
            Drinking water & utility water delivered safely to your doorstep.
          </p>

          <Link
            href="/app/catalog"
            className="inline-flex items-center gap-2 px-5 py-3 bg-white rounded-xl text-primary-600 font-semibold text-sm shadow-lg shadow-black/10 hover:shadow-xl transition-all"
          >
            Order Now <ChevronRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      {/* Welcome */}
      <div className="px-5 -mt-4">
        <div className="bg-white rounded-2xl border border-border/60 p-4 shadow-sm">
          <p className="text-sm text-text-secondary">
            Welcome back, <span className="font-semibold text-text-primary">{user?.full_name || "Guest"}</span> 👋
          </p>
        </div>
      </div>

      {/* Water Purposes */}
      <div className="px-5 mt-6">
        <h3 className="font-semibold text-text-primary mb-3">What do you need?</h3>
        <div className="grid grid-cols-2 gap-3">
          {(purposes || []).length > 0
            ? purposes!.map((p) => (
                <Link
                  key={p.id}
                  href={`/app/catalog?purpose=${p.id}`}
                  className="bg-white rounded-2xl border border-border/60 p-4 hover:shadow-lg hover:border-primary-200 transition-all group"
                >
                  <div className="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center mb-2 group-hover:bg-primary-100 transition-colors">
                    <Droplets className="w-5 h-5 text-primary-500" />
                  </div>
                  <h4 className="font-medium text-text-primary text-sm">{p.name}</h4>
                  <p className="text-xs text-text-muted mt-0.5 line-clamp-2">{p.description || "Premium quality"}</p>
                </Link>
              ))
            : [
                { name: "Drinking Water", desc: "RO + UV Purified" },
                { name: "Utility Water", desc: "For cleaning & daily use" },
              ].map((p) => (
                <Link
                  key={p.name}
                  href="/app/catalog"
                  className="bg-white rounded-2xl border border-border/60 p-4 hover:shadow-lg hover:border-primary-200 transition-all group"
                >
                  <div className="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center mb-2 group-hover:bg-primary-100 transition-colors">
                    <Droplets className="w-5 h-5 text-primary-500" />
                  </div>
                  <h4 className="font-medium text-text-primary text-sm">{p.name}</h4>
                  <p className="text-xs text-text-muted mt-0.5">{p.desc}</p>
                </Link>
              ))}
        </div>
      </div>

      {/* Popular Sizes */}
      <div className="px-5 mt-6">
        <h3 className="font-semibold text-text-primary mb-3">Popular Sizes</h3>
        <div className="flex gap-3 overflow-x-auto pb-2 -mx-5 px-5 scrollbar-hide">
          {SIZES.map((s) => (
            <Link
              key={s.label}
              href="/app/catalog"
              className="shrink-0 bg-white rounded-2xl border border-border/60 p-4 w-24 text-center hover:shadow-lg hover:border-primary-200 transition-all"
            >
              <span className="text-2xl">{s.icon}</span>
              <p className="text-xs font-semibold text-text-primary mt-2">{s.label}</p>
              <p className="text-[10px] text-text-muted">{s.litres}L</p>
            </Link>
          ))}
        </div>
      </div>

      {/* Features */}
      <div className="px-5 mt-6 mb-8">
        <h3 className="font-semibold text-text-primary mb-3">Key Features</h3>
        <div className="grid grid-cols-2 gap-3">
          {FEATURES.map((f) => (
            <div key={f.label} className="bg-white rounded-2xl border border-border/60 p-3.5 flex items-start gap-3">
              <div className="w-9 h-9 rounded-lg bg-primary-50 flex items-center justify-center shrink-0">
                <f.icon className="w-4 h-4 text-primary-500" />
              </div>
              <div>
                <p className="text-xs font-semibold text-text-primary leading-tight">{f.label}</p>
                <p className="text-[10px] text-text-muted mt-0.5">{f.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
