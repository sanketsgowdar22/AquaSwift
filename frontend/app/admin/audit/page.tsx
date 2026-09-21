"use client";
import { useQuery } from "@tanstack/react-query";
import { adminApi } from "@/lib/api";
import { formatDate } from "@/lib/utils";
import { ClipboardList, Search } from "lucide-react";
import { useState } from "react";

export default function AuditPage() {
  const [entityType, setEntityType] = useState("");
  const params: Record<string, string> = {};
  if (entityType) params.entity_type = entityType;

  const { data, isLoading } = useQuery({ queryKey: ["audit-logs", entityType], queryFn: () => adminApi.auditLogs(params) });
  const logs = data?.items || [];
  const entityTypes = ["order", "delivery", "payment", "coupon", "inventory", "user", "vehicle"];

  return (
    <div className="space-y-6 animate-fade-in">
      <div><h1 className="text-2xl font-bold text-text-primary">Audit Logs</h1><p className="text-text-secondary text-sm mt-1">System activity trail</p></div>

      <div className="flex gap-2 flex-wrap">
        <button onClick={() => setEntityType("")} className={`px-3 py-1.5 rounded-full text-sm font-medium transition-all ${!entityType ? "bg-primary-500 text-white" : "bg-white text-text-secondary border border-border hover:border-primary-300"}`}>All</button>
        {entityTypes.map((t) => (
          <button key={t} onClick={() => setEntityType(t)} className={`px-3 py-1.5 rounded-full text-sm font-medium capitalize transition-all ${entityType === t ? "bg-primary-500 text-white" : "bg-white text-text-secondary border border-border hover:border-primary-300"}`}>{t}</button>
        ))}
      </div>

      <div className="bg-white rounded-2xl border border-border/60 overflow-hidden">
        <table className="w-full"><thead><tr className="border-b border-border/40 bg-gray-50/50">
          <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Action</th>
          <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Entity</th>
          <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Entity ID</th>
          <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Actor</th>
          <th className="text-left text-xs font-semibold text-text-muted uppercase px-5 py-3.5">Time</th>
        </tr></thead>
        <tbody className="divide-y divide-border/30">
          {isLoading ? Array.from({ length: 8 }).map((_, i) => <tr key={i}>{Array.from({ length: 5 }).map((_, j) => <td key={j} className="px-5 py-4"><div className="h-4 w-20 animate-shimmer rounded" /></td>)}</tr>) :
          logs.length > 0 ? logs.map((l) => (
            <tr key={l.id} className="hover:bg-gray-50/50"><td className="px-5 py-4"><span className="px-2 py-0.5 rounded-full text-xs font-medium bg-primary-50 text-primary-700">{l.action}</span></td>
            <td className="px-5 py-4 text-sm text-text-secondary capitalize">{l.entity_type}</td>
            <td className="px-5 py-4 text-sm font-mono text-text-muted">{String(l.entity_id).slice(0, 8)}…</td>
            <td className="px-5 py-4 text-sm text-text-secondary">{l.actor_id ? String(l.actor_id).slice(0, 8) + "…" : "System"}</td>
            <td className="px-5 py-4 text-sm text-text-secondary">{formatDate(l.created_at, true)}</td></tr>
          )) : <tr><td colSpan={5} className="px-5 py-16 text-center"><ClipboardList className="w-12 h-12 text-text-muted mx-auto mb-3" /><p className="text-text-secondary">No audit logs</p></td></tr>}
        </tbody></table>
      </div>
    </div>
  );
}
