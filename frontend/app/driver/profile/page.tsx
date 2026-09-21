"use client";

import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { User, Phone, LogOut, Shield } from "lucide-react";

export default function DriverProfilePage() {
  const { user, logout } = useAuth();
  const router = useRouter();

  return (
    <div className="px-5 py-4 animate-fade-in">
      <h2 className="text-xl font-bold text-text-primary mb-5">Profile</h2>
      <div className="bg-white rounded-2xl border border-border/60 p-5 mb-4">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white text-2xl font-bold shadow-lg shadow-primary-500/20">
            {user?.full_name?.charAt(0) || "D"}
          </div>
          <div>
            <h3 className="text-lg font-bold text-text-primary">{user?.full_name || "Driver"}</h3>
            {user?.phone && <div className="flex items-center gap-1.5 text-sm text-text-secondary mt-1"><Phone className="w-3.5 h-3.5" /> {user.phone}</div>}
            <div className="flex items-center gap-1.5 text-xs text-primary-600 mt-1"><Shield className="w-3 h-3" /> Delivery Partner</div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl border border-border/60 p-5 mb-4">
        <h4 className="font-medium text-text-primary mb-3">Quick Stats</h4>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div><p className="text-2xl font-bold text-primary-600">42</p><p className="text-xs text-text-muted">Total Trips</p></div>
          <div><p className="text-2xl font-bold text-green-600">4.8</p><p className="text-xs text-text-muted">Rating</p></div>
          <div><p className="text-2xl font-bold text-yellow-600">98%</p><p className="text-xs text-text-muted">Accept Rate</p></div>
        </div>
      </div>

      <button onClick={() => { logout(); router.replace("/login"); }}
        className="w-full flex items-center gap-3 px-5 py-4 bg-white rounded-2xl border border-red-200 text-red-600 hover:bg-red-50 transition-colors">
        <LogOut className="w-5 h-5" /><span className="text-sm font-medium">Logout</span>
      </button>
    </div>
  );
}
