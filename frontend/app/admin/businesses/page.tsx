"use client";
import { useQuery } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import { Building2, Plus, Mail, Phone } from "lucide-react";

export default function BusinessesPage() {
  const { data, isLoading } = useQuery({ queryKey: ["businesses"], queryFn: adminApi.businesses });
  const businesses = data || [];

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold text-text-primary">B2B Businesses</h1><p className="text-text-secondary text-sm mt-1">Manage business accounts for bulk orders</p></div>
        <button className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-primary-500 text-white font-semibold text-sm hover:bg-primary-600 shadow-lg shadow-primary-500/20 transition-all"><Plus className="w-4 h-4" /> Add Business</button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {isLoading ? Array.from({ length: 3 }).map((_, i) => <div key={i} className="bg-white rounded-2xl border p-5 h-36 animate-shimmer" />) : businesses.length > 0 ? businesses.map((b) => (
          <div key={b.id} className="bg-white rounded-2xl border border-border/60 p-5 hover:shadow-lg transition-all">
            <div className="flex items-start gap-3 mb-3">
              <div className="w-11 h-11 rounded-xl bg-indigo-50 flex items-center justify-center shrink-0"><Building2 className="w-5 h-5 text-indigo-600" /></div>
              <div className="min-w-0">
                <h3 className="font-semibold text-text-primary truncate">{b.name}</h3>
                {b.registration_number && <p className="text-xs text-text-muted">{b.registration_number}</p>}
              </div>
              <span className={`ml-auto shrink-0 px-2 py-0.5 rounded-full text-xs font-medium ${b.is_active ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"}`}>{b.is_active ? "Active" : "Inactive"}</span>
            </div>
            <div className="space-y-1.5 text-sm text-text-secondary">
              {b.contact_email && <div className="flex items-center gap-2"><Mail className="w-3.5 h-3.5 text-text-muted" />{b.contact_email}</div>}
              {b.contact_phone && <div className="flex items-center gap-2"><Phone className="w-3.5 h-3.5 text-text-muted" />{b.contact_phone}</div>}
            </div>
          </div>
        )) : <div className="col-span-full py-16 text-center"><Building2 className="w-12 h-12 text-text-muted mx-auto mb-3" /><p className="text-text-secondary font-medium">No businesses registered</p></div>}
      </div>
    </div>
  );
}
