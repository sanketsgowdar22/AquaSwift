"use client";
import { useQuery } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import { formatINR, formatDate } from "@/lib/utils";
import { DollarSign } from "lucide-react";

export default function PaymentsPage() {
  const { data, isLoading } = useQuery({ queryKey: ["payments"], queryFn: () => adminApi.payments() });
  const payments = data || [];
  const statusColors: Record<string, string> = { INITIATED: "bg-gray-50 text-gray-700", PENDING: "bg-yellow-50 text-yellow-700", SUCCESS: "bg-green-50 text-green-700", FAILED: "bg-red-50 text-red-700", REFUNDED: "bg-purple-50 text-purple-700" };

  return (
    <div className="space-y-6 animate-fade-in">
      <div><h1 className="text-2xl font-bold text-text-primary">Payments</h1><p className="text-text-secondary text-sm mt-1">Payment transactions and refunds</p></div>
      <div className="bg-white rounded-2xl border border-border/60 overflow-hidden">
        <table className="w-full">
          <thead><tr className="border-b border-border/40 bg-gray-50/50">
            <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Payment ID</th>
            <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Order</th>
            <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Amount</th>
            <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Gateway</th>
            <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Status</th>
            <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Date</th>
          </tr></thead>
          <tbody className="divide-y divide-border/30">
            {isLoading ? Array.from({ length: 5 }).map((_, i) => <tr key={i}>{Array.from({ length: 6 }).map((_, j) => <td key={j} className="px-5 py-4"><div className="h-4 w-20 animate-shimmer rounded" /></td>)}</tr>) :
            payments.length > 0 ? payments.map((p) => (
              <tr key={p.id} className="hover:bg-gray-50/50"><td className="px-5 py-4 text-sm font-mono text-text-secondary">{p.id.slice(0, 8)}…</td>
              <td className="px-5 py-4 text-sm text-primary-600">{p.order_id.slice(0, 8)}…</td>
              <td className="px-5 py-4 text-sm font-medium">{formatINR(p.amount)}</td>
              <td className="px-5 py-4 text-sm text-text-secondary capitalize">{p.gateway}</td>
              <td className="px-5 py-4"><span className={`px-2.5 py-1 rounded-full text-xs font-medium ${statusColors[p.status] || ""}`}>{p.status}</span></td>
              <td className="px-5 py-4 text-sm text-text-secondary">{formatDate(p.created_at)}</td></tr>
            )) : <tr><td colSpan={6} className="px-5 py-16 text-center"><DollarSign className="w-12 h-12 text-text-muted mx-auto mb-3" /><p className="text-text-secondary">No payments yet</p></td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
}
