"use client";

import { useState } from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";
import { RefreshCcw } from "lucide-react";

const TABS = ["All", "Ongoing", "Completed", "Cancelled"] as const;

type OrderStatus = "Delivered" | "In Transit" | "Pending" | "Cancelled";

const ORDERS: { id: string; date: string; items: string; price: number; status: OrderStatus }[] = [
  { id: "WOW125486", date: "11 May 2025, 11:45 AM", items: "20 Ltr Jar × 2", price: 60, status: "Delivered" },
  { id: "WOW124106", date: "1 May 2025, 09:30 AM", items: "500 Ltr × 1", price: 250, status: "Delivered" },
  { id: "WOW123907", date: "7 May 2025, 06:00 PM", items: "1000 Ltr × 1", price: 450, status: "Delivered" },
  { id: "WOW128821", date: "Today, 11:00 AM", items: "20 Ltr Jar × 3", price: 90, status: "In Transit" },
];

const STATUS_STYLES: Record<string, string> = {
  "Delivered": "bg-green-100 text-green-700",
  "In Transit": "bg-blue-100 text-blue-700",
  "Cancelled": "bg-red-100 text-red-700",
  "Pending": "bg-yellow-100 text-yellow-700",
};

export default function OrderHistoryPage() {
  const [activeTab, setActiveTab] = useState<typeof TABS[number]>("All");

  const filtered = ORDERS.filter((o) => {
    if (activeTab === "All") return true;
    if (activeTab === "Ongoing") return o.status === "In Transit" || o.status === "Pending";
    if (activeTab === "Completed") return o.status === "Delivered";
    if (activeTab === "Cancelled") return o.status === "Cancelled";
    return true;
  });

  return (
    <div className="animate-fade-in">
      <div className="px-4 pt-4 pb-2">
        <h1 className="text-xl font-bold text-text-primary">My Orders</h1>
      </div>

      {/* Tabs */}
      <div className="px-4 flex gap-2 overflow-x-auto pb-3 scrollbar-hide">
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={cn(
              "px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors",
              activeTab === tab
                ? "bg-primary-600 text-white"
                : "bg-white border border-border text-text-secondary hover:border-primary-300"
            )}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Orders */}
      <div className="px-4 space-y-3">
        {filtered.length === 0 ? (
          <div className="text-center py-16 text-text-muted">No orders found</div>
        ) : (
          filtered.map((order) => (
            <Link
              key={order.id}
              href={`/app/orders/${order.id}`}
              className="block bg-white border border-border rounded-2xl p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold text-text-primary">#{order.id}</span>
                <span className={cn("text-xs font-medium px-2.5 py-1 rounded-full", STATUS_STYLES[order.status] || "bg-gray-100 text-gray-700")}>
                  {order.status}
                </span>
              </div>
              <p className="text-xs text-text-muted mb-1">{order.date}</p>
              <div className="flex items-center justify-between mt-2">
                <span className="text-sm text-text-secondary">{order.items}</span>
                <span className="font-semibold text-text-primary">₹{order.price}</span>
              </div>
              {order.status === "Delivered" && (
                <button
                  onClick={(e) => { e.preventDefault(); }}
                  className="mt-3 w-full flex items-center justify-center gap-2 text-primary-600 font-medium py-2.5 rounded-xl border border-primary-200 bg-primary-50 hover:bg-primary-100 transition-colors text-sm"
                >
                  <RefreshCcw className="w-4 h-4" /> Repeat Order
                </button>
              )}
            </Link>
          ))
        )}
      </div>
    </div>
  );
}
