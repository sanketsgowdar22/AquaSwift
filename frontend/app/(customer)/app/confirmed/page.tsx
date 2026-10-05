"use client";

import Link from "next/link";
import { CheckCircle2, MapPin, Home } from "lucide-react";

export default function OrderConfirmedPage() {
  return (
    <div className="animate-fade-in flex flex-col items-center justify-center min-h-[70vh] px-6 text-center">
      {/* Success Icon */}
      <div className="w-20 h-20 rounded-full bg-green-100 flex items-center justify-center mb-6 animate-bounce-in">
        <CheckCircle2 className="w-12 h-12 text-green-500 animate-check-pop" />
      </div>

      <h1 className="text-2xl font-bold text-text-primary mb-2">Order Confirmed!</h1>
      <p className="text-text-secondary mb-2">Your order has been placed successfully.</p>

      <div className="bg-white border border-border rounded-2xl p-5 w-full max-w-sm mt-4 space-y-3">
        <div className="flex justify-between text-sm">
          <span className="text-text-muted">Order ID</span>
          <span className="font-semibold text-primary-600">#WOW125486</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-text-muted">Estimated Delivery</span>
          <span className="font-medium text-text-primary">45 - 60 mins</span>
        </div>
        <p className="text-xs text-text-muted text-center pt-2 border-t border-border">
          We will deliver within 45 - 60 mins
        </p>
      </div>

      <div className="mt-8 space-y-3 w-full max-w-sm">
        <Link
          href="/app/tracking"
          className="w-full flex items-center justify-center gap-2 bg-primary-600 text-white font-semibold py-3.5 rounded-2xl shadow-lg shadow-primary-600/30 hover:bg-primary-700 transition-colors"
        >
          <MapPin className="w-5 h-5" /> Track Order
        </Link>
        <Link
          href="/app"
          className="w-full flex items-center justify-center gap-2 text-primary-600 font-medium py-3 rounded-2xl border border-border hover:bg-primary-50 transition-colors"
        >
          <Home className="w-5 h-5" /> Back to Home
        </Link>
      </div>
    </div>
  );
}
