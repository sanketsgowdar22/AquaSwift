"use client";

import dynamic from "next/dynamic";
import { ChevronLeft, Phone, CheckCircle2, Truck, Package } from "lucide-react";
import { useRouter } from "next/navigation";
import { cn } from "@/lib/utils";

const MapView = dynamic(() => import("@/components/map-view"), { ssr: false });

const TIMELINE = [
  { label: "Order Accepted", time: "11:45 AM", done: true },
  { label: "On The Way", time: "11:50 AM", done: true },
  { label: "Delivered", time: "", done: false },
];

export default function TrackingPage() {
  const router = useRouter();

  return (
    <div className="animate-fade-in">
      {/* Header */}
      <div className="px-4 pt-4 pb-3 flex items-center gap-3">
        <button onClick={() => router.back()} className="w-9 h-9 rounded-xl bg-white border border-border flex items-center justify-center">
          <ChevronLeft className="w-5 h-5 text-text-primary" />
        </button>
        <h1 className="text-lg font-bold text-text-primary">Track Order</h1>
      </div>

      {/* Order ID */}
      <div className="px-4 mb-3">
        <p className="text-sm text-text-muted">Order ID: <span className="font-semibold text-primary-600">#WOW125486</span></p>
      </div>

      {/* Map */}
      <div className="px-4">
        <MapView
          center={[15.3647, 75.1240]}
          zoom={14}
          height="220px"
          markers={[
            { position: [15.3647, 75.1240], label: "Your Location", type: "customer" },
            { position: [15.3690, 75.1280], label: "Driver - Ramesh", type: "driver" },
          ]}
          route={[
            [15.3690, 75.1280],
            [15.3675, 75.1265],
            [15.3660, 75.1250],
            [15.3647, 75.1240],
          ]}
          interactive={false}
        />
      </div>

      {/* Delivery Partner */}
      <div className="px-4 mt-4">
        <div className="bg-white border border-border rounded-2xl p-4 flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-primary-100 flex items-center justify-center">
            <Truck className="w-6 h-6 text-primary-600" />
          </div>
          <div className="flex-1">
            <p className="font-semibold text-text-primary">Delivery Partner</p>
            <p className="text-sm text-text-secondary">Ramesh K.</p>
          </div>
          <button className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
            <Phone className="w-5 h-5 text-green-600" />
          </button>
        </div>
      </div>

      {/* Status Timeline */}
      <div className="px-4 mt-5 mb-6">
        <h3 className="font-semibold text-text-primary mb-4">Delivery Status</h3>
        <div className="space-y-0">
          {TIMELINE.map((step, i) => (
            <div key={step.label} className="flex gap-4">
              {/* Icon + Line */}
              <div className="flex flex-col items-center">
                <div className={cn(
                  "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
                  step.done ? "bg-green-100" : "bg-gray-100"
                )}>
                  {step.done ? (
                    <CheckCircle2 className="w-5 h-5 text-green-500" />
                  ) : (
                    <Package className="w-4 h-4 text-text-muted" />
                  )}
                </div>
                {i < TIMELINE.length - 1 && (
                  <div className={cn("w-0.5 h-8", step.done ? "bg-green-300" : "bg-border")} />
                )}
              </div>
              {/* Content */}
              <div className="pb-4">
                <p className={cn("text-sm font-medium", step.done ? "text-text-primary" : "text-text-muted")}>{step.label}</p>
                {step.time && <p className="text-xs text-text-muted">{step.time}</p>}
              </div>
            </div>
          ))}
        </div>

        <div className="bg-primary-50 border border-primary-200 rounded-xl p-3 mt-2 text-center">
          <p className="text-sm text-primary-700 font-medium">Estimated Delivery: 12:00 PM</p>
        </div>
      </div>
    </div>
  );
}
