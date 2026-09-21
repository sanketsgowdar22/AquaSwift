"use client";

import { DollarSign, TrendingUp, CheckCircle2 } from "lucide-react";
import { formatINR } from "@/lib/utils";

export default function DriverEarningsPage() {
  // In production, this would come from a real API
  const earnings = {
    today: 1250,
    week: 8750,
    month: 34200,
    ordersToday: 5,
    deliveries: [
      { id: "WOW125486", amount: 110, status: "Delivered" },
      { id: "WOW125477", amount: 130, status: "Delivered" },
      { id: "WOW125467", amount: 95, status: "Delivered" },
    ],
  };

  return (
    <div className="px-5 py-4 animate-fade-in">
      <h2 className="text-xl font-bold text-text-primary mb-4">Earnings</h2>

      {/* Today's Earnings */}
      <div className="bg-gradient-to-br from-primary-500 to-primary-700 rounded-2xl p-6 mb-4 text-white relative overflow-hidden">
        <div className="absolute top-0 right-0 w-24 h-24 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2" />
        <p className="text-primary-200 text-sm mb-1">Today&apos;s Earnings</p>
        <p className="text-3xl font-bold">{formatINR(earnings.today)}</p>
        <p className="text-primary-200 text-sm mt-2">{earnings.ordersToday} Orders Completed</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 gap-3 mb-5">
        <div className="bg-white rounded-2xl border border-border/60 p-4">
          <div className="flex items-center gap-2 mb-2"><TrendingUp className="w-4 h-4 text-green-500" /><span className="text-xs text-text-muted">This Week</span></div>
          <p className="text-xl font-bold text-text-primary">{formatINR(earnings.week)}</p>
        </div>
        <div className="bg-white rounded-2xl border border-border/60 p-4">
          <div className="flex items-center gap-2 mb-2"><DollarSign className="w-4 h-4 text-primary-500" /><span className="text-xs text-text-muted">This Month</span></div>
          <p className="text-xl font-bold text-text-primary">{formatINR(earnings.month)}</p>
        </div>
      </div>

      {/* Recent Deliveries */}
      <h3 className="font-semibold text-text-primary mb-3">Recent Deliveries</h3>
      <div className="space-y-3">
        {earnings.deliveries.map((d) => (
          <div key={d.id} className="bg-white rounded-2xl border border-border/60 p-4 flex items-center justify-between">
            <div>
              <p className="text-sm font-mono text-primary-600">{d.id}</p>
              <div className="flex items-center gap-1 text-xs text-green-600 mt-1"><CheckCircle2 className="w-3 h-3" />{d.status}</div>
            </div>
            <p className="font-semibold text-text-primary">{formatINR(d.amount)}</p>
          </div>
        ))}
      </div>

      <button className="w-full mt-4 py-3 rounded-xl border-2 border-primary-200 text-primary-600 font-semibold text-sm hover:bg-primary-50 transition-colors">
        View All Earnings
      </button>
    </div>
  );
}
