"use client";

import { useAuth } from "@/lib/auth";
import { useQuery } from "@tanstack/react-query";
import { api, type Delivery } from "@/lib/api";
import { formatLitres } from "@/lib/utils";
import { Truck, MapPin, Phone, CheckCircle2, Navigation, Clock } from "lucide-react";
import { cn } from "@/lib/utils";

export default function DriverDashboardPage() {
  const { user } = useAuth();

  const { data, isLoading } = useQuery({
    queryKey: ["driver-deliveries"],
    queryFn: () => api.get<{ items: Delivery[] }>("/drivers/me/deliveries"),
    refetchInterval: 15000,
  });

  const deliveries = data?.items || [];
  const activeDelivery = deliveries.find((d) => ["ASSIGNED", "STARTED", "ARRIVED"].includes(d.status));
  const pendingOffers = deliveries.filter((d) => d.status === "OFFERED");

  const statusSteps = ["ASSIGNED", "STARTED", "ARRIVED", "DELIVERED"];
  const currentStep = activeDelivery ? statusSteps.indexOf(activeDelivery.status) : -1;

  return (
    <div className="px-5 py-4 animate-fade-in">
      {/* Status Toggle */}
      <div className="bg-white rounded-2xl border border-border/60 p-4 mb-4 flex items-center justify-between">
        <div>
          <p className="text-sm text-text-secondary">Status</p>
          <p className="font-semibold text-green-600">🟢 Available</p>
        </div>
        <div className="w-14 h-7 bg-green-500 rounded-full relative cursor-pointer">
          <div className="absolute right-1 top-1 w-5 h-5 bg-white rounded-full shadow transition-all" />
        </div>
      </div>

      {/* Active Delivery */}
      {activeDelivery ? (
        <div className="bg-white rounded-2xl border-2 border-primary-200 p-5 mb-4 shadow-md shadow-primary-500/5">
          <div className="flex items-center gap-2 mb-4">
            <Truck className="w-5 h-5 text-primary-500" />
            <h3 className="font-semibold text-text-primary">Active Delivery</h3>
          </div>

          {/* Progress Steps */}
          <div className="flex items-center gap-1 mb-5">
            {statusSteps.map((step, i) => (
              <div key={step} className="flex-1">
                <div className={cn("h-1.5 rounded-full transition-all",
                  i <= currentStep ? "bg-primary-500" : "bg-gray-200"
                )} />
                <p className={cn("text-[10px] mt-1 text-center",
                  i <= currentStep ? "text-primary-600 font-medium" : "text-text-muted"
                )}>
                  {step.replace(/_/g, " ")}
                </p>
              </div>
            ))}
          </div>

          <div className="space-y-2 text-sm">
            <div className="flex items-center gap-2"><MapPin className="w-4 h-4 text-text-muted" /><span className="text-text-secondary">Order: {activeDelivery.order_id.slice(0, 8)}…</span></div>
            <div className="flex items-center gap-2"><Truck className="w-4 h-4 text-text-muted" /><span className="text-text-secondary">{formatLitres(activeDelivery.quantity_litres)}</span></div>
          </div>

          <div className="mt-4 grid grid-cols-2 gap-3">
            {activeDelivery.status === "ASSIGNED" && (
              <button className="col-span-2 py-3 rounded-xl bg-primary-500 text-white font-semibold text-sm hover:bg-primary-600 transition-colors flex items-center justify-center gap-2">
                <Navigation className="w-4 h-4" /> Start Trip
              </button>
            )}
            {activeDelivery.status === "STARTED" && (
              <button className="col-span-2 py-3 rounded-xl bg-accent-500 text-white font-semibold text-sm hover:bg-accent-600 transition-colors flex items-center justify-center gap-2">
                <MapPin className="w-4 h-4" /> Mark Arrived
              </button>
            )}
            {activeDelivery.status === "ARRIVED" && (
              <button className="col-span-2 py-3 rounded-xl bg-green-600 text-white font-semibold text-sm hover:bg-green-700 transition-colors flex items-center justify-center gap-2">
                <CheckCircle2 className="w-4 h-4" /> Confirm Delivery
              </button>
            )}
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-border/60 p-8 mb-4 text-center">
          <Truck className="w-12 h-12 text-text-muted mx-auto mb-3" />
          <p className="text-text-secondary font-medium">No active deliveries</p>
          <p className="text-text-muted text-sm mt-1">New orders will appear here</p>
        </div>
      )}

      {/* Pending Offers */}
      {pendingOffers.length > 0 && (
        <div>
          <h3 className="font-semibold text-text-primary mb-3">New Orders</h3>
          <div className="space-y-3">
            {pendingOffers.map((d) => (
              <div key={d.id} className="bg-white rounded-2xl border border-border/60 p-4 animate-fade-in">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm font-mono text-primary-600">{d.order_id.slice(0, 8)}…</span>
                  <div className="flex items-center gap-1 text-xs text-text-muted"><Clock className="w-3 h-3" /> Auto-reject in 30s</div>
                </div>
                <p className="text-sm text-text-primary font-medium mb-3">{formatLitres(d.quantity_litres)}</p>
                <div className="grid grid-cols-2 gap-3">
                  <button className="py-2.5 rounded-xl border-2 border-red-200 text-red-600 font-semibold text-sm hover:bg-red-50 transition-colors">Reject</button>
                  <button className="py-2.5 rounded-xl bg-green-600 text-white font-semibold text-sm hover:bg-green-700 transition-colors">Accept</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
