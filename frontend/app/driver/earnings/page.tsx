"use client";

import { DollarSign, TrendingUp, Clock, Package } from "lucide-react";

const DELIVERIES = [
  { id: "WOW125486", amount: 110, status: "Delivered" },
  { id: "WOW124377", amount: 110, status: "Delivered" },
];

export default function DriverEarningsPage() {
  return (
    <div className="animate-fade-in">
      {/* Earnings Hero */}
      <div className="bg-gradient-to-br from-primary-700 via-primary-600 to-primary-800 mx-4 mt-4 rounded-2xl p-6 text-center relative overflow-hidden">
        <div className="absolute top-0 right-0 w-24 h-24 rounded-full bg-white/5 -translate-y-1/2 translate-x-1/2" />
        <p className="text-white/70 text-sm mb-1">Today&apos;s Earnings</p>
        <h1 className="text-4xl font-bold text-white mb-1">₹1,250</h1>
        <p className="text-white/60 text-sm">2 Orders Completed</p>
      </div>

      {/* Quick Stats */}
      <div className="px-4 mt-4 grid grid-cols-2 gap-3">
        {[
          { icon: Package, label: "Deliveries", value: "42", sub: "This month" },
          { icon: Clock, label: "Online Hours", value: "28.5", sub: "This month" },
          { icon: DollarSign, label: "Avg / Delivery", value: "₹16.30", sub: "Average" },
          { icon: TrendingUp, label: "Tips", value: "₹94.00", sub: "This month" },
        ].map((stat) => (
          <div key={stat.label} className="bg-white border border-border rounded-xl p-3">
            <div className="flex items-center gap-2 mb-2">
              <div className="w-7 h-7 rounded-lg bg-primary-50 flex items-center justify-center">
                <stat.icon className="w-3.5 h-3.5 text-primary-600" />
              </div>
              <span className="text-xs text-text-muted">{stat.label}</span>
            </div>
            <p className="text-lg font-bold text-text-primary">{stat.value}</p>
            <p className="text-[10px] text-text-muted">{stat.sub}</p>
          </div>
        ))}
      </div>

      {/* Recent Deliveries */}
      <div className="px-4 mt-6 mb-6">
        <h3 className="text-sm font-semibold text-text-primary mb-3">Recent Deliveries</h3>
        <div className="space-y-2">
          {DELIVERIES.map((d) => (
            <div key={d.id} className="bg-white border border-border rounded-xl p-3 flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-text-primary">{d.id}</p>
                <p className="text-xs text-text-muted">{d.status}</p>
              </div>
              <span className="font-semibold text-text-primary">₹{d.amount}</span>
            </div>
          ))}
        </div>

        <button className="w-full mt-4 py-3 rounded-xl border border-border text-primary-600 font-medium text-sm hover:bg-primary-50 transition-colors">
          View All Earnings
        </button>
      </div>
    </div>
  );
}
