"use client";
import { useQuery } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import { formatLitres, formatDate } from "@/lib/utils";
import { Beaker, Plus, CircleDot } from "lucide-react";

export default function SourcesPage() {
  const { data, isLoading } = useQuery({ queryKey: ["sources"], queryFn: adminApi.sources });
  const sources = data || [];
  const statusColors: Record<string, string> = { ACTIVE: "bg-green-50 text-green-700 border-green-200", INACTIVE: "bg-gray-50 text-gray-700 border-gray-200", MAINTENANCE: "bg-yellow-50 text-yellow-700 border-yellow-200" };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div><h1 className="text-2xl font-bold text-text-primary">Water Sources</h1><p className="text-text-secondary text-sm mt-1">Manage borewells, treatment plants, and tanker fills</p></div>
        <button className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-primary-500 text-white font-semibold text-sm hover:bg-primary-600 shadow-lg shadow-primary-500/20 transition-all"><Plus className="w-4 h-4" /> Add Source</button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {isLoading ? Array.from({ length: 3 }).map((_, i) => <div key={i} className="bg-white rounded-2xl border p-5 h-36 animate-shimmer" />) : sources.length > 0 ? sources.map((s) => (
          <div key={s.id} className="bg-white rounded-2xl border border-border/60 p-5 hover:shadow-lg transition-all">
            <div className="flex items-start gap-3 mb-3">
              <div className="w-11 h-11 rounded-xl bg-cyan-50 flex items-center justify-center shrink-0"><Beaker className="w-5 h-5 text-cyan-600" /></div>
              <div className="min-w-0">
                <h3 className="font-semibold text-text-primary truncate">{s.name}</h3>
                <p className="text-xs text-text-secondary capitalize">{s.type}</p>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-text-secondary">Capacity: <span className="font-medium text-text-primary">{formatLitres(s.capacity_litres)}</span></span>
              <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium border ${statusColors[s.status] || "bg-gray-50 text-gray-700 border-gray-200"}`}><CircleDot className="w-3 h-3" />{s.status}</span>
            </div>
            {s.gps_lat && s.gps_lng && <p className="text-xs text-text-muted mt-2">📍 {Number(s.gps_lat).toFixed(4)}, {Number(s.gps_lng).toFixed(4)}</p>}
          </div>
        )) : <div className="col-span-full py-16 text-center"><Beaker className="w-12 h-12 text-text-muted mx-auto mb-3" /><p className="text-text-secondary font-medium">No water sources</p><p className="text-text-muted text-sm mt-1">Add your first water source to get started</p></div>}
      </div>
    </div>
  );
}
