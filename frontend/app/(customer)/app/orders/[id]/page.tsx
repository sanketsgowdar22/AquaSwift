"use client";

import { useRouter } from "next/navigation";
import { ChevronLeft, MapPin, HelpCircle } from "lucide-react";

export default function OrderDetailPage() {
  const router = useRouter();

  return (
    <div className="animate-fade-in">
      {/* Header */}
      <div className="px-4 pt-4 pb-3 flex items-center gap-3">
        <button onClick={() => router.back()} className="w-9 h-9 rounded-xl bg-white border border-border flex items-center justify-center">
          <ChevronLeft className="w-5 h-5 text-text-primary" />
        </button>
        <h1 className="text-lg font-bold text-text-primary">Order Details</h1>
      </div>

      <div className="px-4 space-y-4">
        {/* Status */}
        <div className="bg-white border border-border rounded-2xl p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-text-muted">Order ID</span>
            <span className="font-semibold text-primary-600">#WOW125486</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-text-muted">Status</span>
            <span className="text-xs font-medium bg-green-100 text-green-700 px-2.5 py-1 rounded-full">Delivered</span>
          </div>
          <p className="text-xs text-text-muted mt-2">11 May 2025, 12:25 PM</p>
        </div>

        {/* Items */}
        <div className="bg-white border border-border rounded-2xl p-4">
          <h3 className="font-semibold text-text-primary mb-3">Items</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-text-secondary">20 Ltr Jar × 2</span>
              <span className="font-medium">₹60</span>
            </div>
          </div>
        </div>

        {/* Billing */}
        <div className="bg-white border border-border rounded-2xl p-4">
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-text-secondary">Delivery Charge</span>
              <span className="font-medium">₹20</span>
            </div>
            <div className="flex justify-between border-t border-border pt-2">
              <span className="font-semibold text-text-primary">Total</span>
              <span className="font-bold text-primary-600">₹80</span>
            </div>
          </div>
        </div>

        {/* Payment */}
        <div className="bg-white border border-border rounded-2xl p-4">
          <h3 className="font-semibold text-text-primary mb-2">Payment</h3>
          <p className="text-sm text-text-secondary">Paid via UPI <span className="float-right font-medium text-text-primary">₹80</span></p>
        </div>

        {/* Delivery Address */}
        <div className="bg-white border border-border rounded-2xl p-4">
          <h3 className="font-semibold text-text-primary mb-2">Delivery Address</h3>
          <div className="flex items-start gap-2">
            <MapPin className="w-4 h-4 text-primary-600 mt-0.5 shrink-0" />
            <p className="text-sm text-text-secondary">Home<br />Banavasi, Karnataka – 581288</p>
          </div>
        </div>

        {/* Need Help */}
        <button className="w-full flex items-center justify-center gap-2 text-primary-600 font-medium py-3 rounded-2xl border border-border hover:bg-primary-50 transition-colors mb-6">
          <HelpCircle className="w-5 h-5" /> Need Help? Contact Support
        </button>
      </div>
    </div>
  );
}
