"use client";
import { useQuery } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import { formatINR, formatDate } from "@/lib/utils";
import { Tag, Plus, Copy } from "lucide-react";

export default function CouponsPage() {
  const { data, isLoading } = useQuery({ queryKey: ["coupons"], queryFn: adminApi.coupons });
  const coupons = data || [];

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold text-text-primary">Coupons</h1><p className="text-text-secondary text-sm mt-1">Manage discount coupons</p></div>
        <button className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-primary-500 text-white font-semibold text-sm hover:bg-primary-600 shadow-lg shadow-primary-500/20"><Plus className="w-4 h-4" /> Create Coupon</button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {isLoading ? Array.from({ length: 3 }).map((_, i) => <div key={i} className="bg-white rounded-2xl border p-5 h-40 animate-shimmer" />) : coupons.length > 0 ? coupons.map((c) => (
          <div key={c.id} className="bg-white rounded-2xl border border-border/60 p-5 hover:shadow-lg transition-all relative overflow-hidden">
            <div className="absolute top-0 right-0 w-24 h-24 bg-primary-50 rounded-bl-[60px] -z-0" />
            <div className="relative z-10">
              <div className="flex items-center gap-2 mb-3">
                <Tag className="w-4 h-4 text-primary-500" />
                <code className="text-lg font-bold text-primary-700 tracking-wider">{c.code}</code>
              </div>
              <div className="flex items-center gap-2 mb-3">
                <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-primary-50 text-primary-700">{c.discount_type}</span>
                <span className="text-sm font-semibold text-text-primary">{c.discount_type === "PERCENTAGE" ? `${c.discount_value}%` : formatINR(c.discount_value)} off</span>
              </div>
              <div className="text-xs text-text-muted space-y-1">
                <p>Valid: {formatDate(c.valid_from)} – {formatDate(c.valid_to)}</p>
                <p>Usage: {c.current_usage_count}/{c.total_usage_limit || "∞"}</p>
              </div>
              <span className={`mt-2 inline-flex px-2 py-0.5 rounded-full text-xs font-medium ${c.is_active ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"}`}>{c.is_active ? "Active" : "Inactive"}</span>
            </div>
          </div>
        )) : <div className="col-span-full py-16 text-center"><Tag className="w-12 h-12 text-text-muted mx-auto mb-3" /><p className="text-text-secondary">No coupons yet</p></div>}
      </div>
    </div>
  );
}
