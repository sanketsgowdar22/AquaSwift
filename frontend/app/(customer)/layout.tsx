"use client";

import { useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { Home, ShoppingBag, User, Droplets } from "lucide-react";
import Link from "next/link";
import { cn } from "@/lib/utils";
import WowLogo from "@/components/wow-logo";

const NAV = [
  { href: "/app", icon: Home, label: "Home" },
  { href: "/app/orders", icon: ShoppingBag, label: "Orders" },
  { href: "/app/profile", icon: User, label: "Profile" },
];

export default function CustomerLayout({ children }: { children: React.ReactNode }) {
  const { isLoading, isAuthenticated } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) router.replace("/login");
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Droplets className="w-10 h-10 text-primary-600 animate-pulse" />
      </div>
    );
  }

  if (!isAuthenticated) return null;

  return (
    <div className="min-h-screen bg-background flex flex-col max-w-lg mx-auto relative">
      {/* Header */}
      <header className="sticky top-0 z-30 bg-white border-b border-border px-4 py-3 flex items-center justify-between">
        <WowLogo variant="icon" size="sm" />
        <div className="flex items-center gap-1 text-sm text-text-secondary">
          <span className="text-xs text-text-muted">Deliver to</span>
          <span className="font-medium text-text-primary ml-1">Banavasi, Karnataka ▾</span>
        </div>
      </header>

      {/* Content */}
      <main className="flex-1 pb-20 overflow-y-auto">{children}</main>

      {/* Bottom Nav */}
      <nav className="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-lg bg-white border-t border-border flex z-30">
        {NAV.map((item) => {
          const active = pathname === item.href || (item.href !== "/app" && pathname.startsWith(item.href));
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex-1 flex flex-col items-center gap-1 py-2.5 text-[11px] font-medium transition-colors",
                active ? "text-primary-600" : "text-text-muted hover:text-text-secondary"
              )}
            >
              <item.icon className={cn("w-5 h-5", active && "fill-primary-600/10")} />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
