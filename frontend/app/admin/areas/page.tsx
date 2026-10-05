"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import { Plus, Edit2, Trash2, ToggleLeft, ToggleRight, X, MapPin } from "lucide-react";
import { cn } from "@/lib/utils";

const MapView = dynamic(() => import("@/components/map-view"), { ssr: false });

interface Zone {
  id: string;
  name: string;
  description: string;
  deliveryCharge: number;
  minOrder: number;
  active: boolean;
  color: string;
  coords: [number, number][];
}

const DEMO_ZONES: Zone[] = [
  {
    id: "1", name: "Banavasi Central", description: "Core city area", deliveryCharge: 20,
    minOrder: 50, active: true, color: "#0160CD",
    coords: [[15.370, 75.118], [15.370, 75.132], [15.360, 75.132], [15.360, 75.118]],
  },
  {
    id: "2", name: "Banavasi East", description: "Extended east zone", deliveryCharge: 35,
    minOrder: 100, active: true, color: "#1BA169",
    coords: [[15.370, 75.132], [15.370, 75.145], [15.358, 75.145], [15.358, 75.132]],
  },
  {
    id: "3", name: "Rural Outskirts", description: "Long distance delivery", deliveryCharge: 60,
    minOrder: 200, active: false, color: "#F59E0B",
    coords: [[15.380, 75.105], [15.380, 75.118], [15.365, 75.118], [15.365, 75.105]],
  },
];

export default function AreasPage() {
  const [zones, setZones] = useState<Zone[]>(DEMO_ZONES);
  const [showForm, setShowForm] = useState(false);
  const [editingZone, setEditingZone] = useState<Zone | null>(null);
  const [newCoords, setNewCoords] = useState<[number, number][]>([]);

  const [formName, setFormName] = useState("");
  const [formDesc, setFormDesc] = useState("");
  const [formCharge, setFormCharge] = useState(20);
  const [formMinOrder, setFormMinOrder] = useState(50);

  const toggleZone = (id: string) => {
    setZones((prev) => prev.map((z) => z.id === id ? { ...z, active: !z.active } : z));
  };

  const deleteZone = (id: string) => {
    setZones((prev) => prev.filter((z) => z.id !== id));
  };

  const handleMapClick = (latlng: { lat: number; lng: number }) => {
    if (showForm) {
      setNewCoords((prev) => [...prev, [latlng.lat, latlng.lng]]);
    }
  };

  const handleSave = () => {
    if (formName && newCoords.length >= 3) {
      const newZone: Zone = {
        id: Date.now().toString(),
        name: formName,
        description: formDesc,
        deliveryCharge: formCharge,
        minOrder: formMinOrder,
        active: true,
        color: `hsl(${Math.random() * 360}, 70%, 50%)`,
        coords: newCoords,
      };
      setZones((prev) => [...prev, newZone]);
      resetForm();
    }
  };

  const resetForm = () => {
    setShowForm(false);
    setEditingZone(null);
    setNewCoords([]);
    setFormName("");
    setFormDesc("");
    setFormCharge(20);
    setFormMinOrder(50);
  };

  return (
    <div className="animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">Delivery Areas</h1>
          <p className="text-text-secondary text-sm mt-1">Configure delivery zones and pricing</p>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2.5 rounded-xl text-sm font-medium hover:bg-primary-700 transition-colors"
        >
          <Plus className="w-4 h-4" /> Add Zone
        </button>
      </div>

      {/* Map */}
      <div className="mb-6">
        <MapView
          center={[15.365, 75.125]}
          zoom={13}
          height="400px"
          polygons={zones.filter((z) => z.active).map((z) => ({
            id: z.id,
            coords: z.coords,
            color: z.color,
            label: `${z.name} — ₹${z.deliveryCharge} delivery`,
          }))}
          polygon={showForm && newCoords.length > 0 ? newCoords : undefined}
          onMapClick={showForm ? handleMapClick : undefined}
        />
        {showForm && (
          <p className="text-xs text-primary-600 mt-2 flex items-center gap-1">
            <MapPin className="w-3 h-3" /> Click on the map to draw zone vertices ({newCoords.length} points added)
          </p>
        )}
      </div>

      {/* Add/Edit Form */}
      {showForm && (
        <div className="bg-white border border-border rounded-2xl p-5 mb-6 animate-slide-up">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-text-primary">New Delivery Zone</h3>
            <button onClick={resetForm} className="text-text-muted hover:text-text-primary">
              <X className="w-5 h-5" />
            </button>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1">Zone Name</label>
              <input
                value={formName} onChange={(e) => setFormName(e.target.value)}
                className="w-full border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 outline-none"
                placeholder="e.g. North District"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1">Description</label>
              <input
                value={formDesc} onChange={(e) => setFormDesc(e.target.value)}
                className="w-full border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 outline-none"
                placeholder="e.g. Core urban area"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1">Delivery Charge (₹)</label>
              <input
                type="number" value={formCharge} onChange={(e) => setFormCharge(Number(e.target.value))}
                className="w-full border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1">Min Order (₹)</label>
              <input
                type="number" value={formMinOrder} onChange={(e) => setFormMinOrder(Number(e.target.value))}
                className="w-full border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 outline-none"
              />
            </div>
          </div>
          <div className="flex gap-3 mt-4">
            <button onClick={resetForm} className="flex-1 py-2.5 rounded-xl border border-border text-text-primary text-sm font-medium hover:bg-gray-50 transition-colors">
              Cancel
            </button>
            <button
              onClick={handleSave}
              disabled={!formName || newCoords.length < 3}
              className={cn(
                "flex-1 py-2.5 rounded-xl text-white text-sm font-medium transition-colors",
                formName && newCoords.length >= 3 ? "bg-primary-600 hover:bg-primary-700" : "bg-gray-300 cursor-not-allowed"
              )}
            >
              Save Zone
            </button>
          </div>
        </div>
      )}

      {/* Zone List */}
      <div className="space-y-3">
        {zones.map((zone) => (
          <div key={zone.id} className="bg-white border border-border rounded-2xl p-4 flex items-center gap-4">
            <div className="w-4 h-4 rounded-full shrink-0" style={{ backgroundColor: zone.color }} />
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <p className="font-medium text-text-primary">{zone.name}</p>
                {!zone.active && (
                  <span className="text-[10px] bg-gray-100 text-text-muted px-1.5 py-0.5 rounded">Inactive</span>
                )}
              </div>
              <p className="text-xs text-text-muted truncate">{zone.description}</p>
              <div className="flex gap-3 mt-1 text-xs text-text-secondary">
                <span>₹{zone.deliveryCharge} delivery</span>
                <span>Min ₹{zone.minOrder}</span>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button onClick={() => toggleZone(zone.id)} className="text-text-muted hover:text-primary-600 transition-colors">
                {zone.active ? <ToggleRight className="w-6 h-6 text-green-500" /> : <ToggleLeft className="w-6 h-6" />}
              </button>
              <button onClick={() => deleteZone(zone.id)} className="text-text-muted hover:text-red-500 transition-colors">
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
