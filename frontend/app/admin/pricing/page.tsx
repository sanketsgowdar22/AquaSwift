"use client";
import { useQuery } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import { formatINR, formatDate } from "@/lib/utils";
import { DollarSign, Plus } from "lucide-react";

export default function PricingPage() {
  const { data, isLoading } = useQuery({ queryKey: ["pricing-rules"], queryFn: adminApi.pricingRules });
  const rules = data || [];

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold text-text-primary">Pricing Rules</h1><p className="text-text-secondary text-sm mt-1">Configure water pricing models</p></div>
        <button className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-primary-500 text-white font-semibold text-sm hover:bg-primary-600 shadow-lg shadow-primary-500/20"><Plus className="w-4 h-4" /> Add Rule</button>
      </div>
      <div className="bg-white rounded-2xl border border-border/60 overflow-hidden">
        <table className="w-full">
          <thead><tr className="border-b border-border/40 bg-gray-50/50">
            <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Model</th>
            <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Base Price</th>
            <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Customer Type</th>
            <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Status</th>
            <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Active From</th>
          </tr></thead>
          <tbody className="divide-y divide-border/30">
            {isLoading ? Array.from({ length: 4 }).map((_, i) => <tr key={i}>{Array.from({ length: 5 }).map((_, j) => <td key={j} className="px-5 py-4"><div className="h-4 w-20 animate-shimmer rounded" /></td>)}</tr>) :
            rules.length > 0 ? rules.map((r) => (
              <tr key={r.id} className="hover:bg-gray-50/50">
                <td className="px-5 py-4"><span className="px-2.5 py-1 rounded-full text-xs font-medium bg-primary-50 text-primary-700">{r.pricing_model}</span></td>
                <td className="px-5 py-4 text-sm font-medium">{formatINR(r.base_price)}</td>
                <td className="px-5 py-4 text-sm text-text-secondary">{r.customer_type || "All"}</td>
                <td className="px-5 py-4"><span className={`px-2 py-0.5 rounded-full text-xs font-medium ${r.is_active ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"}`}>{r.is_active ? "Active" : "Inactive"}</span></td>
                <td className="px-5 py-4 text-sm text-text-secondary">{formatDate(r.active_from)}</td>
              </tr>
            )) : <tr><td colSpan={5} className="px-5 py-16 text-center"><DollarSign className="w-12 h-12 text-text-muted mx-auto mb-3" /><p className="text-text-secondary">No pricing rules configured</p></td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}
