"use client";
import { useQuery } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import { formatLitres, formatDate } from "@/lib/utils";
import { MapPin } from "lucide-react";

export default function DeliveriesPage() {
  const { data, isLoading } = useQuery({ queryKey: ["deliveries"], queryFn: () => adminApi.deliveries() });
  const deliveries = data?.items || [];
  const statusColors: Record<string, string> = { PENDING_ASSIGNMENT: "bg-gray-50 text-gray-700", OFFERED: "bg-yellow-50 text-yellow-700", ASSIGNED: "bg-blue-50 text-blue-700", STARTED: "bg-indigo-50 text-indigo-700", ARRIVED: "bg-purple-50 text-purple-700", DELIVERED: "bg-green-50 text-green-700", CANCELLED: "bg-red-50 text-red-700" };

  return (
    <div className="space-y-6 animate-fade-in">
      <div><h1 className="text-2xl font-bold text-text-primary">Deliveries</h1><p className="text-text-secondary text-sm mt-1">Track and manage all deliveries</p></div>
      <div className="bg-white rounded-2xl border border-border/60 overflow-hidden">
        <table className="w-full"><thead><tr className="border-b border-border/40 bg-gray-50/50">
          <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Delivery</th>
          <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Order</th>
          <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Quantity</th>
          <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Status</th>
          <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Driver</th>
          <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Date</th>
          <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Action</th>
        </tr></thead>
        <tbody className="divide-y divide-border/30">
          {isLoading ? Array.from({ length: 6 }).map((_, i) => <tr key={i}>{Array.from({ length: 7 }).map((_, j) => <td key={j} className="px-5 py-4"><div className="h-4 w-20 animate-shimmer rounded" /></td>)}</tr>) :
          deliveries.length > 0 ? deliveries.map((d) => (
            <tr key={d.id} className="hover:bg-gray-50/50"><td className="px-5 py-4 text-sm font-mono text-text-secondary">{d.id.slice(0, 8)}…</td>
            <td className="px-5 py-4 text-sm text-primary-600">{d.order_id.slice(0, 8)}…</td>
            <td className="px-5 py-4 text-sm font-medium">{formatLitres(d.quantity_litres)}</td>
            <td className="px-5 py-4"><span className={`px-2.5 py-1 rounded-full text-xs font-medium ${statusColors[d.status] || ""}`}>{d.status.replace(/_/g, " ")}</span></td>
            <td className="px-5 py-4 text-sm text-text-secondary">{d.driver_id?.slice(0, 8) || "Unassigned"}</td>
            <td className="px-5 py-4 text-sm text-text-secondary">{formatDate(d.created_at)}</td>
            <td className="px-5 py-4">{d.status === "PENDING_ASSIGNMENT" && <button className="text-xs px-3 py-1.5 rounded-lg bg-primary-500 text-white hover:bg-primary-600">Assign</button>}</td></tr>
          )) : <tr><td colSpan={7} className="px-5 py-16 text-center"><MapPin className="w-12 h-12 text-text-muted mx-auto mb-3" /><p className="text-text-secondary">No deliveries yet</p></td></tr>}
        </tbody></table>
      </div>
    </div>
  );
}
