"use client";

import { useQuery } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import { formatLitres } from "@/lib/utils";
import { Warehouse, AlertTriangle, Plus, ArrowDownToLine, ArrowUpFromLine } from "lucide-react";

export default function InventoryPage() {
  const { data: balances, isLoading } = useQuery({ queryKey: ["inventory-balances"], queryFn: adminApi.inventoryBalances });

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div><h1 className="text-2xl font-bold text-text-primary">Inventory</h1><p className="text-text-secondary text-sm mt-1">Water source balances and ledger</p></div>
        <button className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-primary-500 text-white font-semibold text-sm hover:bg-primary-600 shadow-lg shadow-primary-500/20 transition-all">
          <Plus className="w-4 h-4" /> Receive Water
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {isLoading ? Array.from({ length: 3 }).map((_, i) => <div key={i} className="bg-white rounded-2xl border border-border/60 p-6 h-44 animate-shimmer" />) : (balances || []).length > 0 ? (balances || []).map((b) => {
          const total = b.available_litres + b.reserved_litres + b.allocated_litres;
          const pctAvailable = total > 0 ? (b.available_litres / total) * 100 : 0;
          const isLow = b.available_litres < 5000;
          return (
            <div key={b.source_id} className="bg-white rounded-2xl border border-border/60 p-6 hover:shadow-lg transition-all">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className={`w-11 h-11 rounded-xl flex items-center justify-center ${isLow ? "bg-red-50" : "bg-primary-50"}`}>
                    {isLow ? <AlertTriangle className="w-5 h-5 text-red-500" /> : <Warehouse className="w-5 h-5 text-primary-500" />}
                  </div>
                  <div><h3 className="font-semibold text-text-primary">{b.source_name || b.source_id.slice(0, 8)}</h3></div>
                </div>
                {isLow && <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-red-50 text-red-600 border border-red-200">Low</span>}
              </div>
              <div className="mb-3">
                <div className="w-full h-2.5 bg-gray-100 rounded-full overflow-hidden">
                  <div className={`h-full rounded-full transition-all ${isLow ? "bg-red-500" : "bg-primary-500"}`} style={{ width: `${Math.min(pctAvailable, 100)}%` }} />
                </div>
              </div>
              <div className="grid grid-cols-3 gap-2 text-center">
                <div><p className="text-xs text-text-muted">Available</p><p className="text-sm font-semibold text-primary-600">{formatLitres(b.available_litres)}</p></div>
                <div><p className="text-xs text-text-muted">Reserved</p><p className="text-sm font-semibold text-yellow-600">{formatLitres(b.reserved_litres)}</p></div>
                <div><p className="text-xs text-text-muted">Allocated</p><p className="text-sm font-semibold text-purple-600">{formatLitres(b.allocated_litres)}</p></div>
              </div>
            </div>
          );
        }) : (
          <div className="col-span-full bg-white rounded-2xl border border-border/60 p-12 text-center">
            <Warehouse className="w-12 h-12 text-text-muted mx-auto mb-3" />
            <p className="text-text-secondary font-medium">No inventory data</p>
            <p className="text-text-muted text-sm mt-1">Add water sources and receive inventory to see balances here</p>
          </div>
        )}
      </div>
    </div>
  );
}
