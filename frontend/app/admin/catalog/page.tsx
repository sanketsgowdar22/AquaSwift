"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { adminApi, type Purpose, type Quality, type DeliveryMethod } from "@/lib/api";
import { Droplets, Plus, X, Loader2 } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

type Tab = "purposes" | "qualities" | "methods" | "variants";

function AddItemModal({ title, onClose, onSubmit, loading }: { title: string; onClose: () => void; onSubmit: (name: string, description: string) => void; loading: boolean }) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-white rounded-2xl p-6 w-full max-w-md animate-fade-in" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-5">
          <h3 className="text-lg font-semibold">{title}</h3>
          <button onClick={onClose} className="p-1 rounded-lg hover:bg-gray-100"><X className="w-5 h-5" /></button>
        </div>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-text-primary mb-1.5">Name</label>
            <input value={name} onChange={(e) => setName(e.target.value)} className="w-full px-4 py-2.5 rounded-xl border border-border text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500" placeholder="e.g. Drinking Water" />
          </div>
          <div>
            <label className="block text-sm font-medium text-text-primary mb-1.5">Description</label>
            <textarea value={description} onChange={(e) => setDescription(e.target.value)} className="w-full px-4 py-2.5 rounded-xl border border-border text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/20 focus:border-primary-500 resize-none" rows={3} placeholder="Optional description..." />
          </div>
          <button disabled={!name.trim() || loading} onClick={() => onSubmit(name, description)}
            className="w-full py-2.5 rounded-xl bg-primary-500 text-white font-semibold hover:bg-primary-600 disabled:opacity-50 transition-colors">
            {loading ? <Loader2 className="w-4 h-4 animate-spin mx-auto" /> : "Create"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default function CatalogPage() {
  const [tab, setTab] = useState<Tab>("purposes");
  const [showAdd, setShowAdd] = useState(false);
  const qc = useQueryClient();

  const { data: purposes, isLoading: lp } = useQuery({ queryKey: ["purposes"], queryFn: adminApi.purposes });
  const { data: qualities, isLoading: lq } = useQuery({ queryKey: ["qualities"], queryFn: adminApi.qualities });
  const { data: methods, isLoading: lm } = useQuery({ queryKey: ["methods"], queryFn: adminApi.methods });
  const { data: variants, isLoading: lv } = useQuery({ queryKey: ["variants"], queryFn: () => adminApi.variants() });

  const createPurpose = useMutation({ mutationFn: (d: Partial<Purpose>) => adminApi.createPurpose(d), onSuccess: () => { qc.invalidateQueries({ queryKey: ["purposes"] }); setShowAdd(false); } });
  const createQuality = useMutation({ mutationFn: (d: Partial<Quality>) => adminApi.createQuality(d), onSuccess: () => { qc.invalidateQueries({ queryKey: ["qualities"] }); setShowAdd(false); } });
  const createMethod = useMutation({ mutationFn: (d: Partial<DeliveryMethod>) => adminApi.createMethod(d), onSuccess: () => { qc.invalidateQueries({ queryKey: ["methods"] }); setShowAdd(false); } });

  const tabs: { key: Tab; label: string; count: number }[] = [
    { key: "purposes", label: "Purposes", count: purposes?.length || 0 },
    { key: "qualities", label: "Quality Types", count: qualities?.length || 0 },
    { key: "methods", label: "Delivery Methods", count: methods?.length || 0 },
    { key: "variants", label: "Variants", count: variants?.length || 0 },
  ];

  const handleAdd = (name: string, description: string) => {
    if (tab === "purposes") createPurpose.mutate({ name, description });
    else if (tab === "qualities") createQuality.mutate({ name, description });
    else if (tab === "methods") createMethod.mutate({ name });
  };

  const loading = lp || lq || lm || lv;

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div><h1 className="text-2xl font-bold text-text-primary">Water Catalog</h1><p className="text-text-secondary text-sm mt-1">Manage purposes, quality types, delivery methods, and variants</p></div>
        {tab !== "variants" && (
          <button onClick={() => setShowAdd(true)} className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-primary-500 text-white font-semibold text-sm hover:bg-primary-600 shadow-lg shadow-primary-500/20 transition-all">
            <Plus className="w-4 h-4" /> Add {tab === "purposes" ? "Purpose" : tab === "qualities" ? "Quality" : "Method"}
          </button>
        )}
      </div>

      <div className="flex gap-2">
        {tabs.map((t) => (
          <button key={t.key} onClick={() => setTab(t.key)}
            className={cn("px-4 py-2 rounded-full text-sm font-medium transition-all", tab === t.key ? "bg-primary-500 text-white shadow-md shadow-primary-500/20" : "bg-white text-text-secondary border border-border hover:border-primary-300")}>
            {t.label} <span className="ml-1 text-xs opacity-70">({t.count})</span>
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {loading ? Array.from({ length: 6 }).map((_, i) => <div key={i} className="bg-white rounded-2xl border border-border/60 p-5 h-28 animate-shimmer" />) : (
          tab === "purposes" ? (purposes || []).map((p) => (
            <div key={p.id} className="bg-white rounded-2xl border border-border/60 p-5 hover:shadow-lg transition-all group">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-xl bg-primary-50 flex items-center justify-center"><Droplets className="w-5 h-5 text-primary-500" /></div>
                <div><h3 className="font-semibold text-text-primary">{p.name}</h3><p className="text-sm text-text-secondary mt-0.5">{p.description || "No description"}</p>
                  <span className={`mt-2 inline-flex px-2 py-0.5 rounded-full text-xs font-medium ${p.is_active ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"}`}>{p.is_active ? "Active" : "Inactive"}</span></div>
              </div>
            </div>
          )) : tab === "qualities" ? (qualities || []).map((q) => (
            <div key={q.id} className="bg-white rounded-2xl border border-border/60 p-5 hover:shadow-lg transition-all">
              <h3 className="font-semibold text-text-primary">{q.name}</h3>
              <p className="text-sm text-text-secondary mt-0.5">{q.description || "No description"}</p>
              <span className={`mt-2 inline-flex px-2 py-0.5 rounded-full text-xs font-medium ${q.is_active ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"}`}>{q.is_active ? "Active" : "Inactive"}</span>
            </div>
          )) : tab === "methods" ? (methods || []).map((m) => (
            <div key={m.id} className="bg-white rounded-2xl border border-border/60 p-5 hover:shadow-lg transition-all">
              <h3 className="font-semibold text-text-primary">{m.name}</h3>
              <span className={`mt-2 inline-flex px-2 py-0.5 rounded-full text-xs font-medium ${m.is_active ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"}`}>{m.is_active ? "Active" : "Inactive"}</span>
            </div>
          )) : (variants || []).map((v) => (
            <div key={v.id} className="bg-white rounded-2xl border border-border/60 p-5 hover:shadow-lg transition-all">
              <div className="flex items-center gap-2 flex-wrap">
                <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700">{v.purpose_name || v.purpose_id?.slice(0, 8)}</span>
                <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-purple-50 text-purple-700">{v.quality_name || v.quality_id?.slice(0, 8)}</span>
                <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-teal-50 text-teal-700">{v.delivery_method_name || v.delivery_method_id?.slice(0, 8)}</span>
              </div>
              <p className="text-sm text-text-secondary mt-2">{v.min_quantity_litres}L – {v.max_quantity_litres}L</p>
            </div>
          ))
        )}
      </div>

      {showAdd && <AddItemModal title={`Add ${tab.slice(0, -1)}`} onClose={() => setShowAdd(false)} onSubmit={handleAdd} loading={createPurpose.isPending || createQuality.isPending || createMethod.isPending} />}
    </div>
  );
}
