"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { Droplets, Mail, Lock, Loader2, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

export default function LoginPage() {
  const { login, isAuthenticated } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  if (isAuthenticated) {
    router.replace("/");
    return null;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email, password);
      router.replace("/");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Login failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Panel — Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary-600 via-primary-500 to-primary-700 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-20 w-64 h-64 rounded-full bg-white/20 blur-3xl" />
          <div className="absolute bottom-20 right-20 w-96 h-96 rounded-full bg-accent-400/20 blur-3xl" />
        </div>
        <div className="relative z-10 flex flex-col justify-center px-16">
          <div className="flex items-center gap-3 mb-8">
            <div className="w-14 h-14 rounded-2xl bg-white/15 backdrop-blur-sm flex items-center justify-center">
              <Droplets className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white tracking-tight">AquaSwift</h1>
              <p className="text-primary-200 text-sm">Water Delivery Platform</p>
            </div>
          </div>

          <h2 className="text-4xl font-bold text-white leading-tight mb-4">
            Pure Water,<br />
            <span className="text-accent-400">Swift Delivery.</span>
          </h2>
          <p className="text-primary-200 text-lg leading-relaxed max-w-md">
            Manage orders, inventory, fleet, and deliveries — all from a single integrated platform.
          </p>

          <div className="mt-12 grid grid-cols-2 gap-4 max-w-sm">
            {[
              { label: "Orders Managed", value: "10K+" },
              { label: "Water Delivered", value: "500KL" },
              { label: "Active Drivers", value: "50+" },
              { label: "Happy Customers", value: "2K+" },
            ].map((stat) => (
              <div key={stat.label} className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
                <p className="text-2xl font-bold text-white">{stat.value}</p>
                <p className="text-primary-300 text-xs mt-1">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right Panel — Login Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <div className="w-full max-w-md animate-fade-in">
          <div className="lg:hidden flex items-center gap-3 mb-8">
            <div className="w-12 h-12 rounded-xl bg-primary-500 flex items-center justify-center">
              <Droplets className="w-7 h-7 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-primary-700">AquaSwift</h1>
          </div>

          <h2 className="text-2xl font-bold text-text-primary mb-1">Welcome back</h2>
          <p className="text-text-secondary mb-8">Sign in to access your dashboard</p>

          {error && (
            <div className="mb-6 flex items-start gap-3 p-4 bg-error/5 border border-error/20 rounded-xl text-error text-sm">
              <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-text-primary mb-2">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-text-muted" />
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-11 pr-4 py-3 rounded-xl border border-border bg-white text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 transition-all"
                  placeholder="admin@aquaswift.in"
                  required
                />
              </div>
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-text-primary mb-2">Password</label>
              <div className="relative">
                <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-text-muted" />
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-11 pr-4 py-3 rounded-xl border border-border bg-white text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 transition-all"
                  placeholder="Enter your password"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className={cn(
                "w-full py-3.5 rounded-xl font-semibold text-white transition-all duration-200",
                "bg-primary-500 hover:bg-primary-600 active:bg-primary-700",
                "focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:ring-offset-2",
                "disabled:opacity-60 disabled:cursor-not-allowed",
                "shadow-lg shadow-primary-500/25 hover:shadow-xl hover:shadow-primary-500/30"
              )}
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin mx-auto" />
              ) : (
                "Sign In"
              )}
            </button>
          </form>

          <p className="text-center text-text-muted text-sm mt-8">
            Admin: admin@aquaswift.in / admin123
          </p>
        </div>
      </div>
    </div>
  );
}
