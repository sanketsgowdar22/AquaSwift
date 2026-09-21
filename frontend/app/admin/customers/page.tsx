"use client";

import { useQuery } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import { Users, Search, UserCheck, UserX } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

export default function CustomersPage() {
  const [search, setSearch] = useState("");
  const { data, isLoading } = useQuery({
    queryKey: ["admin-customers"],
    queryFn: () => adminApi.users({ role: "CUSTOMER" }),
  });

  const users = data?.items || [];
  const filtered = search
    ? users.filter((u) => u.full_name?.toLowerCase().includes(search.toLowerCase()) || u.phone?.includes(search) || u.email?.includes(search))
    : users;

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-text-primary">Customers</h1>
        <p className="text-text-secondary text-sm mt-1">{users.length} registered customers</p>
      </div>

      <div className="relative max-w-md">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
        <input placeholder="Search by name, phone, or email..." value={search} onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-border bg-white text-sm placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500" />
      </div>

      <div className="bg-white rounded-2xl border border-border/60 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border/40 bg-gray-50/50">
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3.5">Name</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3.5">Phone</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3.5">Email</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3.5">Status</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3.5">Joined</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/30">
              {isLoading ? Array.from({ length: 6 }).map((_, i) => (
                <tr key={i}>{Array.from({ length: 5 }).map((_, j) => <td key={j} className="px-5 py-4"><div className="h-4 w-24 animate-shimmer rounded" /></td>)}</tr>
              )) : filtered.length > 0 ? filtered.map((user) => (
                <tr key={user.id} className="hover:bg-gray-50/50 transition-colors">
                  <td className="px-5 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 text-sm font-semibold">
                        {user.full_name.charAt(0)}
                      </div>
                      <span className="text-sm font-medium text-text-primary">{user.full_name}</span>
                    </div>
                  </td>
                  <td className="px-5 py-4 text-sm text-text-secondary">{user.phone || "—"}</td>
                  <td className="px-5 py-4 text-sm text-text-secondary">{user.email || "—"}</td>
                  <td className="px-5 py-4">
                    {user.is_active ? (
                      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-green-50 text-green-700 border border-green-200">
                        <UserCheck className="w-3 h-3" /> Active
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-red-50 text-red-700 border border-red-200">
                        <UserX className="w-3 h-3" /> Inactive
                      </span>
                    )}
                  </td>
                  <td className="px-5 py-4 text-sm text-text-secondary">{formatDate(user.created_at)}</td>
                </tr>
              )) : (
                <tr><td colSpan={5} className="px-5 py-16 text-center">
                  <Users className="w-12 h-12 text-text-muted mx-auto mb-3" />
                  <p className="text-text-secondary font-medium">No customers found</p>
                </td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
