"use client";
import { useQuery } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import { formatDate, formatLitres } from "@/lib/utils";
import { Package, Plus, CircleDot } from "lucide-react";

export default function VehiclesPage() {
  const { data, isLoading } = useQuery({ queryKey: ["vehicles"], queryFn: adminApi.vehicles });
  const vehicles = data || [];
  const statusColors: Record<string, string> = { ACTIVE: "bg-green-50 text-green-700 border-green-200", MAINTENANCE: "bg-yellow-50 text-yellow-700 border-yellow-200", RETIRED: "bg-red-50 text-red-700 border-red-200" };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold text-text-primary">Vehicles</h1><p className="text-text-secondary text-sm mt-1">Fleet management</p></div>
        <button className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-primary-500 text-white font-semibold text-sm hover:bg-primary-600 shadow-lg shadow-primary-500/20"><Plus className="w-4 h-4" /> Add Vehicle</button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {isLoading ? Array.from({ length: 6 }).map((_, i) => <div key={i} className="bg-white rounded-2xl border p-5 h-32 animate-shimmer" />) : vehicles.length > 0 ? vehicles.map((v) => (
          <div key={v.id} className="bg-white rounded-2xl border border-border/60 p-5 hover:shadow-lg transition-all">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-11 h-11 rounded-xl bg-primary-50 flex items-center justify-center"><Package className="w-5 h-5 text-primary-500" /></div>
              <div><h3 className="font-semibold text-text-primary">{v.registration_number}</h3><p className="text-xs text-text-secondary">{v.type}</p></div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-text-secondary">Capacity: {formatLitres(v.capacity_litres)}</span>
              <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium border ${statusColors[v.status] || "bg-gray-50 text-gray-700"}`}><CircleDot className="w-3 h-3" />{v.status}</span>
            </div>
          </div>
        )) : <div className="col-span-full py-16 text-center"><Package className="w-12 h-12 text-text-muted mx-auto mb-3" /><p className="text-text-secondary">No vehicles yet</p></div>}
      </div>
    </div>
  );
}
