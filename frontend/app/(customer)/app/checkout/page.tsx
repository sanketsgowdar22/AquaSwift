"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ChevronLeft, MapPin, Clock, Repeat, CreditCard, Banknote } from "lucide-react";
import { cn } from "@/lib/utils";

export default function CheckoutPage() {
  const router = useRouter();
  const [deliveryTime, setDeliveryTime] = useState<"instant" | "schedule">("instant");
  const [frequency, setFrequency] = useState<"onetime" | "subscription">("onetime");
  const [paymentMethod, setPaymentMethod] = useState<"upi" | "cod">("upi");

  return (
    <div className="animate-fade-in">
      {/* Header */}
      <div className="px-4 pt-4 pb-3 flex items-center gap-3">
        <button onClick={() => router.back()} className="w-9 h-9 rounded-xl bg-white border border-border flex items-center justify-center">
          <ChevronLeft className="w-5 h-5 text-text-primary" />
        </button>
        <h1 className="text-lg font-bold text-text-primary">Checkout</h1>
      </div>

      <div className="px-4 space-y-4">
        {/* Customer Info */}
        <div className="bg-white border border-border rounded-2xl p-4">
          <h3 className="font-semibold text-text-primary mb-3">Delivery Address</h3>
          <div className="flex items-start gap-3">
            <MapPin className="w-5 h-5 text-primary-600 mt-0.5 shrink-0" />
            <div>
              <p className="text-sm font-medium text-text-primary">Home</p>
              <p className="text-xs text-text-secondary mt-0.5">Banavasi, Karnataka – 581318</p>
              <button className="text-xs text-primary-600 font-medium mt-1">Change</button>
            </div>
          </div>
        </div>

        {/* Delivery Time */}
        <div className="bg-white border border-border rounded-2xl p-4">
          <h3 className="font-semibold text-text-primary mb-3 flex items-center gap-2">
            <Clock className="w-4 h-4 text-primary-600" /> Delivery Time
          </h3>
          <div className="grid grid-cols-2 gap-2">
            {[
              { key: "instant" as const, label: "Instant Delivery", sub: "Within 45 mins" },
              { key: "schedule" as const, label: "Schedule Delivery", sub: "Choose time" },
            ].map((opt) => (
              <button
                key={opt.key}
                onClick={() => setDeliveryTime(opt.key)}
                className={cn(
                  "border rounded-xl p-3 text-left transition-all",
                  deliveryTime === opt.key
                    ? "border-primary-600 bg-primary-50 ring-1 ring-primary-600"
                    : "border-border hover:border-primary-300"
                )}
              >
                <p className="text-sm font-medium text-text-primary">{opt.label}</p>
                <p className="text-xs text-text-muted mt-0.5">{opt.sub}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Delivery Frequency */}
        <div className="bg-white border border-border rounded-2xl p-4">
          <h3 className="font-semibold text-text-primary mb-3 flex items-center gap-2">
            <Repeat className="w-4 h-4 text-primary-600" /> Delivery Frequency
          </h3>
          <div className="flex bg-background rounded-xl p-1">
            {[
              { key: "onetime" as const, label: "One Time" },
              { key: "subscription" as const, label: "Subscription" },
            ].map((opt) => (
              <button
                key={opt.key}
                onClick={() => setFrequency(opt.key)}
                className={cn(
                  "flex-1 py-2 text-sm font-medium rounded-lg transition-all",
                  frequency === opt.key
                    ? "bg-primary-600 text-white shadow-sm"
                    : "text-text-secondary hover:text-text-primary"
                )}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>

        {/* Order Summary */}
        <div className="bg-white border border-border rounded-2xl p-4">
          <h3 className="font-semibold text-text-primary mb-3">Order Summary</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-text-secondary">20 Ltr Jar × 2</span>
              <span className="font-medium">₹60</span>
            </div>
            <div className="flex justify-between">
              <span className="text-text-secondary">Delivery Charge</span>
              <span className="font-medium">₹20</span>
            </div>
            <div className="border-t border-border pt-2 mt-2 flex justify-between">
              <span className="font-semibold text-text-primary">Total</span>
              <span className="font-bold text-primary-600 text-base">₹80</span>
            </div>
          </div>
        </div>

        {/* Payment Method */}
        <div className="bg-white border border-border rounded-2xl p-4">
          <h3 className="font-semibold text-text-primary mb-3">Payment Method</h3>
          <div className="space-y-2">
            {[
              { key: "upi" as const, icon: CreditCard, label: "UPI / Cards / Wallets" },
              { key: "cod" as const, icon: Banknote, label: "Cash on Delivery" },
            ].map((opt) => (
              <button
                key={opt.key}
                onClick={() => setPaymentMethod(opt.key)}
                className={cn(
                  "w-full flex items-center gap-3 border rounded-xl p-3 transition-all",
                  paymentMethod === opt.key
                    ? "border-primary-600 bg-primary-50 ring-1 ring-primary-600"
                    : "border-border hover:border-primary-300"
                )}
              >
                <opt.icon className="w-5 h-5 text-primary-600" />
                <span className="text-sm font-medium text-text-primary">{opt.label}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Place Order CTA */}
      <div className="sticky bottom-20 px-4 py-4">
        <button
          onClick={() => router.push("/app/confirmed")}
          className="w-full bg-primary-600 text-white font-semibold py-4 rounded-2xl shadow-lg shadow-primary-600/30 hover:bg-primary-700 transition-colors text-center"
        >
          Place Order · ₹80
        </button>
      </div>
    </div>
  );
}
