"use client";

import { useQuery } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import { Truck, Search, CircleDot } from "lucide-react";
import { useState } from "react";

export default function DriversPage() {
  const [search, setSearch] = useState("");
  const { data, isLoading } = useQuery({
    queryKey: ["admin-drivers"],
    queryFn: () => adminApi.users({ role: "DRIVER" }),
  });

  const users = data?.items || [];
  const filtered = search ? users.filter((u) => u.full_name?.toLowerCase().includes(search.toLowerCase()) || u.phone?.includes(search)) : users;

  return (
    <div className="space-y-6 animate-fade-in">
      <div><h1 className="text-2xl font-bold text-text-primary">Delivery Partners</h1><p className="text-text-secondary text-sm mt-1">{users.length} registered drivers</p></div>

      <div className="relative max-w-md">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
        <input placeholder="Search drivers..." value={search} onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-border bg-white text-sm placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {isLoading ? Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="bg-white rounded-2xl border border-border/60 p-5 animate-shimmer h-40" />
        )) : filtered.length > 0 ? filtered.map((driver) => (
          <div key={driver.id} className="bg-white rounded-2xl border border-border/60 p-5 hover:shadow-lg hover:shadow-primary-500/5 transition-all group">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-xl bg-primary-100 flex items-center justify-center text-primary-600 text-lg font-bold shrink-0">
                {driver.full_name.charAt(0)}
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-text-primary">{driver.full_name}</h3>
                <p className="text-sm text-text-secondary mt-0.5">{driver.phone || "No phone"}</p>
                <div className="flex items-center gap-3 mt-3">
                  <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${driver.is_active ? "bg-green-50 text-green-700 border border-green-200" : "bg-red-50 text-red-700 border border-red-200"}`}>
                    <CircleDot className="w-3 h-3" /> {driver.is_active ? "Active" : "Inactive"}
                  </span>
                </div>
                <p className="text-xs text-text-muted mt-2">Joined {formatDate(driver.created_at)}</p>
              </div>
            </div>
          </div>
        )) : (
          <div className="col-span-full py-16 text-center">
            <Truck className="w-12 h-12 text-text-muted mx-auto mb-3" />
            <p className="text-text-secondary font-medium">No drivers found</p>
          </div>
        )}
      </div>
    </div>
  );
}
