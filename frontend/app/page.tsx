"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { Droplets } from "lucide-react";

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
    <div className="min-h-screen flex items-center justify-center bg-primary-500">
      <div className="text-center animate-fade-in">
        <Droplets className="w-16 h-16 text-white mx-auto mb-4 animate-pulse" />
        <h1 className="text-3xl font-bold text-white">AquaSwift</h1>
        <p className="text-primary-200 mt-2">Loading...</p>
      </div>
    </div>
  );
}
