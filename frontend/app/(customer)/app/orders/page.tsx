"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { formatDate, formatLitres, formatINR } from "@/lib/utils";
import { cn } from "@/lib/utils";
import { ClipboardList, ChevronRight, RotateCcw } from "lucide-react";
import { useState } from "react";
import type { Order } from "@/lib/api";

const TABS = ["All", "Ongoing", "Completed", "Cancelled"];
const statusMap: Record<string, string> = { All: "", Ongoing: "CONFIRMED,PROCESSING,DISPATCHED,IN_TRANSIT", Completed: "DELIVERED", Cancelled: "CANCELLED" };

export default function CustomerOrdersPage() {
  const [tab, setTab] = useState("All");

  const { data, isLoading } = useQuery({
    queryKey: ["my-orders", tab],
    queryFn: () => api.get<{ items: Order[]; total: number }>(`/orders${statusMap[tab] ? `?status=${statusMap[tab]}` : ""}`),
  });

  const orders = data?.items || [];

  const statusColors: Record<string, string> = {
    PENDING_PAYMENT: "text-yellow-600", CONFIRMED: "text-blue-600", PROCESSING: "text-indigo-600",
    DISPATCHED: "text-purple-600", IN_TRANSIT: "text-cyan-600", DELIVERED: "text-green-600", CANCELLED: "text-red-600",
  };

  return (
    <div className="px-5 py-4 animate-fade-in">
      <h2 className="text-xl font-bold text-text-primary mb-4">My Orders</h2>

      {/* Tabs */}
      <div className="flex gap-2 mb-5 overflow-x-auto pb-1">
        {TABS.map((t) => (
          <button key={t} onClick={() => setTab(t)}
            className={cn("px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all",
              tab === t ? "bg-primary-500 text-white shadow-md" : "bg-white text-text-secondary border border-border"
            )}>
            {t}
          </button>
        ))}
      </div>

      {/* Order Cards */}
      <div className="space-y-3">
        {isLoading ? Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="bg-white rounded-2xl border border-border/60 p-4 h-28 animate-shimmer" />
        )) : orders.length > 0 ? orders.map((order) => (
          <div key={order.id} className="bg-white rounded-2xl border border-border/60 p-4 hover:shadow-md transition-all">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-mono font-medium text-primary-600">{order.order_number}</span>
              <span className={cn("text-xs font-semibold", statusColors[order.status] || "text-gray-600")}>
                {order.status.replace(/_/g, " ")}
              </span>
            </div>
            <p className="text-sm text-text-secondary">{formatDate(order.created_at)}</p>
            <div className="flex items-center justify-between mt-3">
              <span className="text-sm text-text-primary font-medium">{formatLitres(order.total_quantity_litres)}</span>
              <div className="flex items-center gap-2">
                {order.status === "DELIVERED" && (
                  <button className="text-xs px-3 py-1.5 rounded-lg bg-primary-50 text-primary-600 font-medium hover:bg-primary-100 transition-colors flex items-center gap-1">
                    <RotateCcw className="w-3 h-3" /> Reorder
                  </button>
                )}
                <ChevronRight className="w-4 h-4 text-text-muted" />
              </div>
            </div>
          </div>
        )) : (
          <div className="py-16 text-center">
            <ClipboardList className="w-12 h-12 text-text-muted mx-auto mb-3" />
            <p className="text-text-secondary font-medium">No orders yet</p>
            <p className="text-text-muted text-sm mt-1">Your orders will appear here</p>
          </div>
        )}
      </div>
    </div>
  );
}
