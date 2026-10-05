"use client";

import { useQuery } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import { formatINR, formatLitres } from "@/lib/utils";
import {
  ShoppingCart, Truck, Users, Droplets, AlertTriangle, TrendingUp,
  ArrowUpRight, ArrowDownRight, Clock
} from "lucide-react";
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts";

// Mock chart data (replaced with real data in Phase 2)
const SALES_CHART_DATA = [
  { day: "Mon", orders: 12, revenue: 8400 },
  { day: "Tue", orders: 19, revenue: 13200 },
  { day: "Wed", orders: 15, revenue: 10500 },
  { day: "Thu", orders: 22, revenue: 15400 },
  { day: "Fri", orders: 28, revenue: 19600 },
  { day: "Sat", orders: 24, revenue: 16800 },
  { day: "Sun", orders: 17, revenue: 11900 },
];

const TOP_PRODUCTS_DATA = [
  { name: "20L Jar", percentage: 40, color: "#1E56A0" },
  { name: "500L Can", percentage: 25, color: "#4A8FE7" },
  { name: "1000L", percentage: 20, color: "#7AA4F5" },
  { name: "Tanker", percentage: 15, color: "#ADC8FF" },
];

interface StatCardProps {
  title: string;
  value: string | number;
  change?: string;
  changeType?: "positive" | "negative" | "neutral";
  icon: React.ElementType;
  iconBg: string;
  iconColor: string;
}

function StatCard({ title, value, change, changeType = "positive", icon: Icon, iconBg, iconColor }: StatCardProps) {
  return (
    <div className="bg-white rounded-2xl p-5 border border-border/60 hover:shadow-lg hover:shadow-primary-500/5 transition-all duration-300 group">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-text-secondary font-medium">{title}</p>
          <p className="text-2xl font-bold text-text-primary mt-1.5">{value}</p>
          {change && (
            <div className="flex items-center gap-1 mt-2">
              {changeType === "positive" ? (
                <ArrowUpRight className="w-3.5 h-3.5 text-success" />
              ) : changeType === "negative" ? (
                <ArrowDownRight className="w-3.5 h-3.5 text-error" />
              ) : null}
              <span className={`text-xs font-medium ${changeType === "positive" ? "text-success" : changeType === "negative" ? "text-error" : "text-text-muted"}`}>
                {change}
              </span>
            </div>
          )}
        </div>
        <div className={`w-11 h-11 rounded-xl ${iconBg} flex items-center justify-center group-hover:scale-110 transition-transform duration-300`}>
          <Icon className={`w-5 h-5 ${iconColor}`} />
        </div>
      </div>
    </div>
  );
}

function RecentOrdersTable() {
  const { data, isLoading } = useQuery({
    queryKey: ["admin-orders-recent"],
    queryFn: () => adminApi.orders({ page_size: "5" }),
  });

  const orders = data?.items || [];

  const statusColors: Record<string, string> = {
    PENDING_PAYMENT: "bg-yellow-50 text-yellow-700 border-yellow-200",
    CONFIRMED: "bg-blue-50 text-blue-700 border-blue-200",
    PROCESSING: "bg-indigo-50 text-indigo-700 border-indigo-200",
    DISPATCHED: "bg-purple-50 text-purple-700 border-purple-200",
    IN_TRANSIT: "bg-cyan-50 text-cyan-700 border-cyan-200",
    DELIVERED: "bg-green-50 text-green-700 border-green-200",
    CANCELLED: "bg-red-50 text-red-700 border-red-200",
  };

  return (
    <div className="bg-white rounded-2xl border border-border/60 overflow-hidden">
      <div className="px-5 py-4 border-b border-border/60 flex items-center justify-between">
        <h3 className="font-semibold text-text-primary">Recent Orders</h3>
        <a href="/admin/orders" className="text-sm text-primary-500 hover:text-primary-600 font-medium">
          View All →
        </a>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-border/40">
              <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3">Order ID</th>
              <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3">Customer</th>
              <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3">Quantity</th>
              <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3">Status</th>
              <th className="text-left text-xs font-semibold text-text-muted uppercase tracking-wider px-5 py-3">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/30">
            {isLoading ? (
              Array.from({ length: 5 }).map((_, i) => (
                <tr key={i}>
                  <td className="px-5 py-4"><div className="h-4 w-24 animate-shimmer rounded" /></td>
                  <td className="px-5 py-4"><div className="h-4 w-32 animate-shimmer rounded" /></td>
                  <td className="px-5 py-4"><div className="h-4 w-16 animate-shimmer rounded" /></td>
                  <td className="px-5 py-4"><div className="h-4 w-20 animate-shimmer rounded" /></td>
                  <td className="px-5 py-4"><div className="h-4 w-12 animate-shimmer rounded" /></td>
                </tr>
              ))
            ) : orders.length > 0 ? (
              orders.map((order) => (
                <tr key={order.id} className="hover:bg-gray-50/50 transition-colors">
                  <td className="px-5 py-4 text-sm font-mono text-primary-600">{order.order_number}</td>
                  <td className="px-5 py-4 text-sm text-text-primary">{order.customer_id?.slice(0, 8)}...</td>
                  <td className="px-5 py-4 text-sm text-text-secondary">{formatLitres(order.total_quantity_litres)}</td>
                  <td className="px-5 py-4">
                    <span className={`inline-flex px-2.5 py-1 rounded-full text-xs font-medium border ${statusColors[order.status] || "bg-gray-50 text-gray-700 border-gray-200"}`}>
                      {order.status.replace(/_/g, " ")}
                    </span>
                  </td>
                  <td className="px-5 py-4">
                    <a href={`/admin/orders/${order.id}`} className="text-sm text-primary-500 hover:text-primary-600 font-medium">
                      View
                    </a>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={5} className="px-5 py-12 text-center">
                  <ShoppingCart className="w-10 h-10 text-text-muted mx-auto mb-3" />
                  <p className="text-text-secondary text-sm">No orders yet</p>
                  <p className="text-text-muted text-xs mt-1">Orders will appear here as they come in</p>
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default function AdminDashboardPage() {
  const { data: dashboard, isLoading } = useQuery({
    queryKey: ["admin-dashboard"],
    queryFn: adminApi.dashboard,
    refetchInterval: 30000, // Refresh every 30s
  });

  const { data: salesReport } = useQuery({
    queryKey: ["admin-sales-report"],
    queryFn: () => adminApi.salesReport(30),
  });

  const d = dashboard || {
    active_orders: 0,
    today_orders: 0,
    pending_deliveries: 0,
    available_drivers: 0,
    low_inventory_alerts: 0,
    total_users: 0,
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-text-primary">Dashboard</h1>
        <p className="text-text-secondary text-sm mt-1">Overview of your operations</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <StatCard title="Total Orders" value={d.today_orders} change="+18%" changeType="positive" icon={ShoppingCart} iconBg="bg-primary-50" iconColor="text-primary-500" />
        <StatCard title="Active Orders" value={d.active_orders} change="" changeType="neutral" icon={Clock} iconBg="bg-blue-50" iconColor="text-blue-500" />
        <StatCard title="Completed" value={salesReport?.total_orders || 0} change="+12%" changeType="positive" icon={TrendingUp} iconBg="bg-green-50" iconColor="text-green-600" />
        <StatCard title="Pending Deliveries" value={d.pending_deliveries} change="" changeType="neutral" icon={Truck} iconBg="bg-orange-50" iconColor="text-orange-500" />
        <StatCard title="Available Drivers" value={d.available_drivers} change="" changeType="neutral" icon={Users} iconBg="bg-purple-50" iconColor="text-purple-500" />
        <StatCard title="Low Inventory" value={d.low_inventory_alerts} change={d.low_inventory_alerts > 0 ? "Action needed" : "All good"} changeType={d.low_inventory_alerts > 0 ? "negative" : "positive"} icon={AlertTriangle} iconBg="bg-red-50" iconColor="text-red-500" />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Sales Overview Chart */}
        <div className="xl:col-span-2 bg-white rounded-2xl border border-border/60 p-5">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-semibold text-text-primary">Sales Overview</h3>
              <p className="text-text-muted text-xs mt-1">Revenue this week</p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-bold text-text-primary">
                {formatINR(salesReport?.total_litres ? (salesReport.total_litres * 0.8) : 18240)}
              </span>
              <span className="text-xs text-success font-medium bg-green-50 px-2 py-0.5 rounded-full">+24%</span>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={240}>
            <AreaChart data={SALES_CHART_DATA}>
              <defs>
                <linearGradient id="salesGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#1E56A0" stopOpacity={0.15} />
                  <stop offset="95%" stopColor="#1E56A0" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="day" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: "#9CA3AF" }} />
              <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: "#9CA3AF" }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#fff",
                  border: "1px solid #E5E7EB",
                  borderRadius: "12px",
                  boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
                  fontSize: "13px",
                }}
              />
              <Area type="monotone" dataKey="revenue" stroke="#1E56A0" strokeWidth={2.5} fill="url(#salesGradient)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Top Products */}
        <div className="bg-white rounded-2xl border border-border/60 p-5">
          <h3 className="font-semibold text-text-primary mb-6">Top Products</h3>
          <div className="space-y-4">
            {TOP_PRODUCTS_DATA.map((product) => (
              <div key={product.name}>
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-sm text-text-primary font-medium">{product.name}</span>
                  <span className="text-sm text-text-secondary">{product.percentage}%</span>
                </div>
                <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-1000 ease-out"
                    style={{ width: `${product.percentage}%`, backgroundColor: product.color }}
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 pt-5 border-t border-border/40">
            <h4 className="text-sm font-medium text-text-secondary mb-3">Water Delivered</h4>
            <div className="flex items-baseline gap-2">
              <span className="text-2xl font-bold text-text-primary">
                {formatLitres(salesReport?.total_litres || 0)}
              </span>
              <span className="text-xs text-text-muted">last 30 days</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Orders */}
      <RecentOrdersTable />
    </div>
  );
}
