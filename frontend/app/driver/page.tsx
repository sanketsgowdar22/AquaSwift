"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import { MapPin, Phone, Navigation, CheckCircle2, XCircle, Droplets } from "lucide-react";
import { cn } from "@/lib/utils";

const MapView = dynamic(() => import("@/components/map-view"), { ssr: false });

type DriverState = "new_order" | "accepted" | "on_the_way" | "reached" | "delivered" | "idle";

const DEMO_ORDER = {
  id: "WOW125486",
  items: "Drinking Water 20 Ltr Jar × 5",
  price: 60,
  customer: "Manoj Shankar Gowda",
  address: "Banavasi, Karnataka",
  distance: "2.6 km away",
};

export default function DriverDashboardPage() {
  const [state, setState] = useState<DriverState>("new_order");
  const [timer, setTimer] = useState(30);

  // New Order
  if (state === "new_order") {
    return (
      <div className="animate-fade-in px-4 pt-4">
        <h1 className="text-lg font-bold text-text-primary mb-4 flex items-center gap-2">
          <Droplets className="w-5 h-5 text-primary-600" /> New Order
        </h1>

        <div className="bg-white border border-border rounded-2xl p-5 space-y-4">
          <div className="flex items-start gap-3">
            <div className="w-12 h-12 bg-primary-50 rounded-xl flex items-center justify-center text-xl">🫙</div>
            <div className="flex-1">
              <p className="font-semibold text-text-primary">{DEMO_ORDER.items}</p>
              <p className="text-primary-600 font-bold mt-1">₹{DEMO_ORDER.price}</p>
            </div>
          </div>

          <div className="border-t border-border pt-3 space-y-2">
            <p className="text-sm text-text-muted">Customer</p>
            <p className="text-sm font-medium text-text-primary">{DEMO_ORDER.customer}</p>
            <p className="text-xs text-text-secondary">{DEMO_ORDER.address}</p>
            <div className="flex items-center gap-1 text-xs text-primary-600">
              <MapPin className="w-3 h-3" /> {DEMO_ORDER.distance}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 pt-2">
            <button
              onClick={() => setState("idle")}
              className="flex items-center justify-center gap-2 py-3 rounded-xl bg-red-50 border border-red-200 text-red-600 font-semibold text-sm hover:bg-red-100 transition-colors"
            >
              <XCircle className="w-4 h-4" /> Reject
            </button>
            <button
              onClick={() => setState("accepted")}
              className="flex items-center justify-center gap-2 py-3 rounded-xl bg-green-500 text-white font-semibold text-sm hover:bg-green-600 transition-colors"
            >
              <CheckCircle2 className="w-4 h-4" /> Accept
            </button>
          </div>

          <p className="text-center text-xs text-text-muted">Auto accept in {timer} sec</p>
        </div>
      </div>
    );
  }

  // Accepted
  if (state === "accepted") {
    return (
      <div className="animate-fade-in px-4 pt-4">
        <h1 className="text-lg font-bold text-text-primary mb-4">Order Accepted</h1>
        <div className="bg-white border border-border rounded-2xl p-5 space-y-4">
          <div className="flex justify-between text-sm">
            <span className="text-text-muted">Order ID</span>
            <span className="font-semibold text-primary-600">#{DEMO_ORDER.id}</span>
          </div>
          <div className="border-t border-border pt-3">
            <p className="text-sm text-text-muted mb-1">Customer</p>
            <p className="font-medium">{DEMO_ORDER.customer}</p>
            <p className="text-xs text-text-secondary">{DEMO_ORDER.address}</p>
          </div>
          <div className="grid grid-cols-2 gap-3 pt-2">
            <button
              onClick={() => setState("on_the_way")}
              className="py-3 rounded-xl bg-primary-600 text-white font-semibold text-sm hover:bg-primary-700 transition-colors"
            >
              Start Trip
            </button>
            <button className="py-3 rounded-xl bg-white border border-border text-text-primary font-medium text-sm flex items-center justify-center gap-2 hover:bg-gray-50 transition-colors">
              <Navigation className="w-4 h-4 text-primary-600" /> Navigate
            </button>
          </div>
        </div>
      </div>
    );
  }

  // On The Way
  if (state === "on_the_way") {
    return (
      <div className="animate-fade-in">
        <div className="px-4 pt-4 pb-3">
          <h1 className="text-lg font-bold text-text-primary">On The Way</h1>
        </div>
        <div className="px-4 mb-4">
          <MapView
            center={[15.3647, 75.1240]}
            zoom={14}
            height="250px"
            markers={[
              { position: [15.3690, 75.1280], label: "You", type: "driver" },
              { position: [15.3647, 75.1240], label: DEMO_ORDER.customer, type: "customer" },
            ]}
            route={[[15.3690, 75.1280], [15.3675, 75.1265], [15.3660, 75.1250], [15.3647, 75.1240]]}
          />
        </div>
        <div className="px-4">
          <button
            onClick={() => setState("reached")}
            className="w-full py-4 rounded-2xl bg-primary-600 text-white font-semibold hover:bg-primary-700 transition-colors flex items-center justify-center gap-2"
          >
            <Navigation className="w-5 h-5" /> Navigate
          </button>
        </div>
      </div>
    );
  }

  // Reached
  if (state === "reached") {
    return (
      <div className="animate-fade-in px-4 pt-4">
        <h1 className="text-lg font-bold text-text-primary mb-4">Reached Location</h1>
        <div className="bg-white border border-border rounded-2xl p-5 text-center space-y-4">
          <div className="w-16 h-16 mx-auto bg-blue-100 rounded-full flex items-center justify-center">
            <MapPin className="w-8 h-8 text-primary-600" />
          </div>
          <p className="font-medium">Customer: {DEMO_ORDER.customer}</p>
          <div className="grid grid-cols-2 gap-3">
            <button className="py-3 rounded-xl border border-border text-text-primary flex items-center justify-center gap-2 text-sm font-medium hover:bg-gray-50 transition-colors">
              <Phone className="w-4 h-4 text-green-600" /> Call
            </button>
            <button
              onClick={() => setState("delivered")}
              className="py-3 rounded-xl bg-green-500 text-white font-semibold text-sm hover:bg-green-600 transition-colors"
            >
              Mark Arrived
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Delivered
  if (state === "delivered") {
    return (
      <div className="animate-fade-in flex flex-col items-center justify-center min-h-[60vh] px-6 text-center">
        <div className="w-20 h-20 rounded-full bg-green-100 flex items-center justify-center mb-6 animate-bounce-in">
          <CheckCircle2 className="w-12 h-12 text-green-500" />
        </div>
        <h2 className="text-xl font-bold text-text-primary mb-2">Delivered!</h2>
        <p className="text-text-secondary mb-1">Order Delivered!</p>
        <p className="text-text-muted text-sm mb-6">Thank you!</p>
        <button
          onClick={() => setState("idle")}
          className="bg-primary-600 text-white font-semibold px-8 py-3 rounded-2xl hover:bg-primary-700 transition-colors"
        >
          Confirm Delivery
        </button>
      </div>
    );
  }

  // Idle - no active orders
  return (
    <div className="animate-fade-in flex flex-col items-center justify-center min-h-[60vh] px-6 text-center">
      <div className="w-16 h-16 rounded-full bg-primary-50 flex items-center justify-center mb-4">
        <Droplets className="w-8 h-8 text-primary-600" />
      </div>
      <h2 className="text-lg font-bold text-text-primary mb-2">No Active Deliveries</h2>
      <p className="text-text-muted text-sm mb-6">Waiting for new orders...</p>
      <button
        onClick={() => setState("new_order")}
        className="text-primary-600 font-medium text-sm underline"
      >
        Simulate New Order
      </button>
    </div>
  );
}
