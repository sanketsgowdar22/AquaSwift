"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import WowLogo from "@/components/wow-logo";

export default function HomePage() {
  const { isAuthenticated, user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isLoading) return;
    if (!isAuthenticated) {
      router.replace("/login");
      return;
    }
    // Route based on role
    if (user?.roles?.includes("SUPER_ADMIN") || user?.roles?.includes("OPS_MANAGER")) {
      router.replace("/admin/dashboard");
    } else if (user?.roles?.includes("DRIVER")) {
      router.replace("/driver");
    } else {
      router.replace("/app");
    }
  }, [isAuthenticated, isLoading, user, router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-700 via-primary-600 to-primary-800">
      <div className="text-center animate-fade-in">
        <WowLogo variant="full" size="xl" dark className="mx-auto mb-4 items-center" />
        <p className="text-white/60 mt-4">Loading...</p>
      </div>
    </div>
  );
}

