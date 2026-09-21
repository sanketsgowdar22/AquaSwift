"use client";

import { useAuth } from "@/lib/auth";
import { User, MapPin, Phone, Mail, ChevronRight, LogOut } from "lucide-react";
import { useRouter } from "next/navigation";

export default function CustomerProfilePage() {
  const { user, logout } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.replace("/login");
  };

  const menuItems = [
    { label: "My Addresses", icon: MapPin, href: "/app/addresses" },
    { label: "Notifications", icon: Mail, href: "/app/notifications" },
  ];

  return (
    <div className="px-5 py-4 animate-fade-in">
      <h2 className="text-xl font-bold text-text-primary mb-5">Profile</h2>

      {/* User Card */}
      <div className="bg-white rounded-2xl border border-border/60 p-5 mb-4">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white text-2xl font-bold shadow-lg shadow-primary-500/20">
            {user?.full_name?.charAt(0) || "U"}
          </div>
          <div>
            <h3 className="text-lg font-bold text-text-primary">{user?.full_name || "User"}</h3>
            {user?.phone && (
              <div className="flex items-center gap-1.5 text-sm text-text-secondary mt-1">
                <Phone className="w-3.5 h-3.5" /> {user.phone}
              </div>
            )}
            {user?.email && (
              <div className="flex items-center gap-1.5 text-sm text-text-secondary mt-0.5">
                <Mail className="w-3.5 h-3.5" /> {user.email}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Menu */}
      <div className="bg-white rounded-2xl border border-border/60 overflow-hidden mb-4">
        {menuItems.map((item) => (
          <a key={item.label} href={item.href}
            className="flex items-center gap-3 px-5 py-4 border-b border-border/30 last:border-0 hover:bg-gray-50 transition-colors">
            <item.icon className="w-5 h-5 text-text-muted" />
            <span className="flex-1 text-sm font-medium text-text-primary">{item.label}</span>
            <ChevronRight className="w-4 h-4 text-text-muted" />
          </a>
        ))}
      </div>

      {/* Logout */}
      <button
        onClick={handleLogout}
        className="w-full flex items-center gap-3 px-5 py-4 bg-white rounded-2xl border border-red-200 text-red-600 hover:bg-red-50 transition-colors"
      >
        <LogOut className="w-5 h-5" />
        <span className="text-sm font-medium">Logout</span>
      </button>
    </div>
  );
}
