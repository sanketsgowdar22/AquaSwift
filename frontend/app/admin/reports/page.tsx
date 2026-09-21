"use client";
import { useQuery } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import { formatINR, formatLitres } from "@/lib/utils";
import { BarChart3, TrendingUp, Truck, Droplets } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, type PieLabelRenderProps } from "recharts";

const COLORS = ["#1E56A0", "#4A8FE7", "#00BFA6", "#F59E0B"];

export default function ReportsPage() {
  const { data: sales } = useQuery({ queryKey: ["report-sales"], queryFn: () => adminApi.salesReport(30) });
  const { data: deliveryR } = useQuery({ queryKey: ["report-deliveries"], queryFn: () => adminApi.deliveryReport(30) });

  const pieData = [
    { name: "Drinking", value: 40 }, { name: "Daily Use", value: 30 },
    { name: "Construction", value: 20 }, { name: "Industrial", value: 10 },
  ];

  return (
    <div className="space-y-6 animate-fade-in">
      <div><h1 className="text-2xl font-bold text-text-primary">Reports</h1><p className="text-text-secondary text-sm mt-1">Business analytics and insights</p></div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        <div className="bg-white rounded-2xl border border-border/60 p-5">
          <div className="flex items-center gap-3 mb-3"><div className="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center"><TrendingUp className="w-5 h-5 text-primary-500" /></div><span className="text-sm text-text-secondary">Total Orders (30d)</span></div>
          <p className="text-3xl font-bold text-text-primary">{sales?.total_orders || 0}</p>
        </div>
        <div className="bg-white rounded-2xl border border-border/60 p-5">
          <div className="flex items-center gap-3 mb-3"><div className="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center"><Droplets className="w-5 h-5 text-blue-500" /></div><span className="text-sm text-text-secondary">Water Delivered (30d)</span></div>
          <p className="text-3xl font-bold text-text-primary">{formatLitres(sales?.total_litres || 0)}</p>
        </div>
        <div className="bg-white rounded-2xl border border-border/60 p-5">
          <div className="flex items-center gap-3 mb-3"><div className="w-10 h-10 rounded-xl bg-green-50 flex items-center justify-center"><Truck className="w-5 h-5 text-green-500" /></div><span className="text-sm text-text-secondary">Deliveries Done (30d)</span></div>
          <p className="text-3xl font-bold text-text-primary">{deliveryR?.completed_deliveries || 0}</p>
        </div>
        <div className="bg-white rounded-2xl border border-border/60 p-5">
          <div className="flex items-center gap-3 mb-3"><div className="w-10 h-10 rounded-xl bg-yellow-50 flex items-center justify-center"><BarChart3 className="w-5 h-5 text-yellow-500" /></div><span className="text-sm text-text-secondary">Est. Revenue (30d)</span></div>
          <p className="text-3xl font-bold text-text-primary">{formatINR((sales?.total_litres || 0) * 0.8)}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl border border-border/60 p-5">
          <h3 className="font-semibold text-text-primary mb-4">Water by Purpose</h3>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart><Pie data={pieData} cx="50%" cy="50%" outerRadius={100} dataKey="value" label={(props: PieLabelRenderProps) => `${props.name ?? ""} ${(((props.percent ?? 0) as number) * 100).toFixed(0)}%`}>
              {pieData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
            </Pie><Tooltip /></PieChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-2xl border border-border/60 p-5">
          <h3 className="font-semibold text-text-primary mb-4">Weekly Volume</h3>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={[{ d: "Mon", v: 1200 }, { d: "Tue", v: 1900 }, { d: "Wed", v: 1500 }, { d: "Thu", v: 2200 }, { d: "Fri", v: 2800 }, { d: "Sat", v: 2400 }, { d: "Sun", v: 1700 }]}>
              <XAxis dataKey="d" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: "#9CA3AF" }} />
              <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: "#9CA3AF" }} />
              <Tooltip contentStyle={{ borderRadius: "12px", border: "1px solid #E5E7EB" }} />
              <Bar dataKey="v" fill="#1E56A0" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
