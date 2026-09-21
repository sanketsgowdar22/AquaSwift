"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { Droplets, Home, ShoppingCart, ClipboardList, User } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const BOTTOM_NAV = [
  { label: "Home", icon: Home, href: "/app" },
  { label: "Orders", icon: ClipboardList, href: "/app/orders" },
  { label: "Profile", icon: User, href: "/app/profile" },
];

export default function CustomerLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) router.replace("/login");
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Droplets className="w-10 h-10 text-primary-500 animate-pulse" />
      </div>
    );
  }

  if (!isAuthenticated) return null;

  return (
    <div className="min-h-screen bg-background flex flex-col max-w-lg mx-auto relative">
      {/* Header */}
      <header className="sticky top-0 z-30 bg-white/90 backdrop-blur-lg border-b border-border/50 px-4 py-3 flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-primary-500 flex items-center justify-center">
          <Droplets className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-lg font-bold text-primary-700 leading-none">AquaSwift</h1>
          <p className="text-xs text-text-muted">Pure water, swift delivery</p>
        </div>
      </header>

      {/* Content */}
      <main className="flex-1 pb-20">{children}</main>

      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-lg bg-white border-t border-border/50 z-40">
        <div className="flex items-center justify-around py-2">
          {BOTTOM_NAV.map((item) => {
            const isActive = pathname === item.href || (item.href !== "/app" && pathname?.startsWith(item.href));
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex flex-col items-center gap-0.5 px-4 py-1.5 rounded-xl transition-all",
                  isActive ? "text-primary-500" : "text-text-muted hover:text-text-secondary"
                )}
              >
                <item.icon className={cn("w-5 h-5", isActive && "scale-110")} />
                <span className={cn("text-[10px] font-medium", isActive && "font-semibold")}>{item.label}</span>
                {isActive && <div className="w-1 h-1 rounded-full bg-primary-500 mt-0.5" />}
              </Link>
            );
          })}
        </div>
      </nav>
    </div>
  );
}
