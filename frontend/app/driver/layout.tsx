"use client";

import { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { Droplets, Truck, DollarSign, User } from "lucide-react";
import Link from "next/link";
import { cn } from "@/lib/utils";

const NAV = [
  { label: "Deliveries", icon: Truck, href: "/driver" },
  { label: "Earnings", icon: DollarSign, href: "/driver/earnings" },
  { label: "Profile", icon: User, href: "/driver/profile" },
];

export default function DriverLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) router.replace("/login");
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) return <div className="min-h-screen flex items-center justify-center"><Droplets className="w-10 h-10 text-primary-500 animate-pulse" /></div>;
  if (!isAuthenticated) return null;

  return (
    <div className="min-h-screen bg-background flex flex-col max-w-lg mx-auto relative">
      <header className="sticky top-0 z-30 bg-primary-600 px-4 py-3 flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-white/15 flex items-center justify-center"><Droplets className="w-5 h-5 text-white" /></div>
        <div><h1 className="text-lg font-bold text-white leading-none">AquaSwift</h1><p className="text-xs text-primary-200">Driver Portal</p></div>
      </header>
      <main className="flex-1 pb-20">{children}</main>
      <nav className="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-lg bg-white border-t border-border/50 z-40">
        <div className="flex items-center justify-around py-2">
          {NAV.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link key={item.href} href={item.href} className={cn("flex flex-col items-center gap-0.5 px-4 py-1.5 rounded-xl transition-all", isActive ? "text-primary-500" : "text-text-muted")}>
                <item.icon className={cn("w-5 h-5", isActive && "scale-110")} />
                <span className={cn("text-[10px] font-medium", isActive && "font-semibold")}>{item.label}</span>
              </Link>
            );
          })}
        </div>
      </nav>
    </div>
  );
}
