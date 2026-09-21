"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard, ShoppingCart, Users, Truck, Droplets, Package,
  DollarSign, Tag, Warehouse, ClipboardList, BarChart3, Shield,
  Building2, Settings, LogOut, ChevronLeft, Bell, Search, Menu, Beaker, MapPin
} from "lucide-react";

const NAV_ITEMS = [
  { label: "Dashboard", icon: LayoutDashboard, href: "/admin/dashboard" },
  { label: "Orders", icon: ShoppingCart, href: "/admin/orders" },
  { label: "Customers", icon: Users, href: "/admin/customers" },
  { label: "Drivers", icon: Truck, href: "/admin/drivers" },
  { label: "Deliveries", icon: MapPin, href: "/admin/deliveries" },
  { type: "divider" as const, label: "Catalog & Pricing" },
  { label: "Water Catalog", icon: Droplets, href: "/admin/catalog" },
  { label: "Pricing Rules", icon: DollarSign, href: "/admin/pricing" },
  { label: "Coupons", icon: Tag, href: "/admin/coupons" },
  { type: "divider" as const, label: "Operations" },
  { label: "Inventory", icon: Warehouse, href: "/admin/inventory" },
  { label: "Sources", icon: Beaker, href: "/admin/sources" },
  { label: "Vehicles", icon: Package, href: "/admin/vehicles" },
  { type: "divider" as const, label: "Finance & Reports" },
  { label: "Payments", icon: DollarSign, href: "/admin/payments" },
  { label: "Reports", icon: BarChart3, href: "/admin/reports" },
  { label: "Audit Logs", icon: ClipboardList, href: "/admin/audit" },
  { type: "divider" as const, label: "B2B" },
  { label: "Businesses", icon: Building2, href: "/admin/businesses" },
];

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { user, logout, isAuthenticated, isLoading } = useAuth();
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Droplets className="w-10 h-10 text-primary-500 animate-pulse" />
      </div>
    );
  }

  if (!isAuthenticated) {
    router.replace("/login");
    return null;
  }

  const handleLogout = () => {
    logout();
    router.replace("/login");
  };

  return (
    <div className="min-h-screen flex bg-background">
      {/* Sidebar Overlay (mobile) */}
      {mobileOpen && (
        <div className="fixed inset-0 bg-black/50 z-40 lg:hidden" onClick={() => setMobileOpen(false)} />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed lg:sticky top-0 left-0 h-screen z-50 flex flex-col bg-sidebar transition-all duration-300 ease-out",
          collapsed ? "w-[72px]" : "w-64",
          mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        )}
      >
        {/* Logo */}
        <div className="flex items-center gap-3 px-4 h-16 shrink-0 border-b border-white/5">
          <div className="w-9 h-9 rounded-lg bg-primary-500 flex items-center justify-center shrink-0">
            <Droplets className="w-5 h-5 text-white" />
          </div>
          {!collapsed && (
            <span className="text-white font-bold text-lg tracking-tight animate-fade-in">
              AquaSwift
            </span>
          )}
          <button
            onClick={() => setCollapsed(!collapsed)}
            className="ml-auto hidden lg:flex w-7 h-7 items-center justify-center rounded-md hover:bg-white/10 text-white/50 hover:text-white transition-colors"
          >
            <ChevronLeft className={cn("w-4 h-4 transition-transform", collapsed && "rotate-180")} />
          </button>
        </div>

        {/* Nav */}
        <nav className="flex-1 overflow-y-auto py-3 px-2 space-y-0.5">
          {NAV_ITEMS.map((item, i) => {
            if (item.type === "divider") {
              if (collapsed) return <div key={i} className="my-3 border-t border-white/5" />;
              return (
                <p key={i} className="px-3 pt-5 pb-1.5 text-[11px] font-semibold text-white/30 uppercase tracking-wider">
                  {item.label}
                </p>
              );
            }
            const Icon = item.icon!;
            const isActive = pathname === item.href || pathname?.startsWith(item.href + "/");
            return (
              <Link
                key={item.href}
                href={item.href!}
                onClick={() => setMobileOpen(false)}
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150",
                  isActive
                    ? "bg-sidebar-active text-white shadow-lg shadow-primary-500/20"
                    : "text-white/60 hover:text-white hover:bg-sidebar-hover"
                )}
                title={collapsed ? item.label : undefined}
              >
                <Icon className="w-5 h-5 shrink-0" />
                {!collapsed && <span className="animate-fade-in">{item.label}</span>}
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="px-2 py-3 border-t border-white/5">
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 w-full px-3 py-2.5 rounded-lg text-sm font-medium text-white/50 hover:text-red-400 hover:bg-red-500/10 transition-colors"
            title={collapsed ? "Logout" : undefined}
          >
            <LogOut className="w-5 h-5 shrink-0" />
            {!collapsed && <span>Logout</span>}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Topbar */}
        <header className="sticky top-0 z-30 h-16 bg-white/80 backdrop-blur-lg border-b border-border flex items-center px-4 lg:px-6 gap-4">
          <button
            onClick={() => setMobileOpen(true)}
            className="lg:hidden w-9 h-9 flex items-center justify-center rounded-lg hover:bg-gray-100 text-text-secondary"
          >
            <Menu className="w-5 h-5" />
          </button>

          <div className="flex-1 max-w-md">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
              <input
                placeholder="Search orders, customers, drivers..."
                className="w-full pl-10 pr-4 py-2 rounded-lg border border-border bg-background text-sm placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 transition-all"
              />
            </div>
          </div>

          <div className="flex items-center gap-3 ml-auto">
            <button className="relative w-9 h-9 flex items-center justify-center rounded-lg hover:bg-gray-100 text-text-secondary transition-colors">
              <Bell className="w-5 h-5" />
              <span className="absolute top-1 right-1 w-2.5 h-2.5 bg-error rounded-full border-2 border-white" />
            </button>

            <div className="hidden sm:flex items-center gap-3 pl-3 border-l border-border">
              <div className="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center text-white text-sm font-semibold">
                {user?.full_name?.charAt(0) || "A"}
              </div>
              <div className="hidden md:block">
                <p className="text-sm font-medium text-text-primary leading-none">{user?.full_name}</p>
                <p className="text-xs text-text-muted mt-0.5">{user?.roles?.[0] || "Admin"}</p>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-4 lg:p-6">{children}</main>
      </div>
    </div>
  );
}
