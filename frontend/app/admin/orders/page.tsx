"use client";

import { useQuery } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import { formatLitres, formatDate } from "@/lib/utils";
import { ShoppingCart, Search, Filter, Eye } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

const STATUS_TABS = ["ALL", "PENDING_PAYMENT", "CONFIRMED", "PROCESSING", "DISPATCHED", "IN_TRANSIT", "DELIVERED", "CANCELLED"];

const statusColors: Record<string, string> = {
  PENDING_PAYMENT: "bg-yellow-50 text-yellow-700 border-yellow-200",
  CONFIRMED: "bg-blue-50 text-blue-700 border-blue-200",
  PROCESSING: "bg-indigo-50 text-indigo-700 border-indigo-200",
  DISPATCHED: "bg-purple-50 text-purple-700 border-purple-200",
  IN_TRANSIT: "bg-cyan-50 text-cyan-700 border-cyan-200",
  DELIVERED: "bg-green-50 text-green-700 border-green-200",
  CANCELLED: "bg-red-50 text-red-700 border-red-200",
};

export default function OrdersPage() {
  const [activeTab, setActiveTab] = useState("ALL");
  const [search, setSearch] = useState("");

  const params: Record<string, string> = {};
  if (activeTab !== "ALL") params.status = activeTab;

  const { data, isLoading } = useQuery({
    queryKey: ["admin-orders", activeTab],
    queryFn: () => adminApi.orders(params),
  });

  const orders = data?.items || [];
  const filteredOrders = search
    ? orders.filter((o) => o.order_number?.toLowerCase().includes(search.toLowerCase()))
    : orders;

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">Orders</h1>
          <p className="text-text-secondary text-sm mt-1">Manage all customer orders</p>
        </div>
      </div>

      {/* Status Tabs */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {STATUS_TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={cn(
              "px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all",
              activeTab === tab
                ? "bg-primary-500 text-white shadow-md shadow-primary-500/20"
                : "bg-white text-text-secondary border border-border hover:border-primary-300 hover:text-primary-600"
            )}
          >
            {tab === "ALL" ? "All" : tab.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Search */}
      <div className="relative max-w-md">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
        <input
          placeholder="Search by order number..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-border bg-white text-sm placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500"
        />
      </div>

      {/* Orders Table */}
      <div className="bg-white rounded-2xl border border-border/60 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border/40 bg-gray-50/50">
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3.5">Order ID</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3.5">Customer</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3.5">Items</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3.5">Quantity</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3.5">Status</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3.5">Date</th>
                <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3.5">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/30">
              {isLoading ? (
                Array.from({ length: 8 }).map((_, i) => (
                  <tr key={i}>
                    {Array.from({ length: 7 }).map((_, j) => (
                      <td key={j} className="px-5 py-4"><div className="h-4 w-20 animate-shimmer rounded" /></td>
                    ))}
                  </tr>
                ))
              ) : filteredOrders.length > 0 ? (
                filteredOrders.map((order) => (
                  <tr key={order.id} className="hover:bg-gray-50/50 transition-colors">
                    <td className="px-5 py-4 text-sm font-mono text-primary-600 font-medium">{order.order_number}</td>
                    <td className="px-5 py-4 text-sm text-text-primary">{order.customer_id?.slice(0, 8)}…</td>
                    <td className="px-5 py-4 text-sm text-text-secondary">{order.items?.length || "-"}</td>
                    <td className="px-5 py-4 text-sm text-text-primary font-medium">{formatLitres(order.total_quantity_litres)}</td>
                    <td className="px-5 py-4">
                      <span className={`inline-flex px-2.5 py-1 rounded-full text-xs font-medium border ${statusColors[order.status] || "bg-gray-50 text-gray-700"}`}>
                        {order.status.replace(/_/g, " ")}
                      </span>
                    </td>
                    <td className="px-5 py-4 text-sm text-text-secondary">{formatDate(order.created_at)}</td>
                    <td className="px-5 py-4">
                      <button className="text-primary-500 hover:text-primary-600 p-1.5 rounded-lg hover:bg-primary-50 transition-colors">
                        <Eye className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={7} className="px-5 py-16 text-center">
                    <ShoppingCart className="w-12 h-12 text-text-muted mx-auto mb-3" />
                    <p className="text-text-secondary font-medium">No orders found</p>
                    <p className="text-text-muted text-sm mt-1">
                      {activeTab !== "ALL" ? `No ${activeTab.replace(/_/g, " ").toLowerCase()} orders` : "Orders will appear here"}
                    </p>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
