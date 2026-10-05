"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { ChevronLeft, Plus, Minus, ShieldCheck, Leaf } from "lucide-react";
import Link from "next/link";

const PRODUCTS = [
  { id: 1, name: "20 Litre Jar", price: 30, unit: "jar", icon: "🫙", desc: "RO Purified drinking water" },
  { id: 2, name: "500 Litre", price: 250, unit: "load", icon: "🛢️", desc: "Utility & cleaning water" },
  { id: 3, name: "1000 Litre", price: 450, unit: "load", icon: "🚰", desc: "Bulk utility water" },
  { id: 4, name: "Tanker (5000L)", price: 1800, unit: "tanker", icon: "🚚", desc: "Construction & industrial" },
];

export default function ProductPage() {
  const router = useRouter();
  const [quantities, setQuantities] = useState<Record<number, number>>({});

  const updateQty = (id: number, delta: number) => {
    setQuantities((prev) => {
      const current = prev[id] || 0;
      const next = Math.max(0, current + delta);
      return { ...prev, [id]: next };
    });
  };

  const totalItems = Object.values(quantities).reduce((a, b) => a + b, 0);
  const totalPrice = PRODUCTS.reduce((sum, p) => sum + (quantities[p.id] || 0) * p.price, 0);

  return (
    <div className="animate-fade-in">
      {/* Header */}
      <div className="px-4 pt-4 pb-3 flex items-center gap-3">
        <button onClick={() => router.back()} className="w-9 h-9 rounded-xl bg-white border border-border flex items-center justify-center">
          <ChevronLeft className="w-5 h-5 text-text-primary" />
        </button>
        <h1 className="text-lg font-bold text-text-primary">Drinking Water</h1>
      </div>

      {/* Products */}
      <div className="px-4 space-y-3">
        {PRODUCTS.map((product) => {
          const qty = quantities[product.id] || 0;
          return (
            <div key={product.id} className="bg-white border border-border rounded-2xl p-4">
              <div className="flex items-start gap-4">
                <div className="w-16 h-16 bg-primary-50 rounded-xl flex items-center justify-center text-3xl">
                  {product.icon}
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-text-primary">{product.name}</h3>
                  <p className="text-xs text-text-muted mt-0.5">{product.desc}</p>
                  <p className="text-primary-600 font-bold mt-1">₹{product.price}<span className="text-text-muted font-normal text-xs">/{product.unit}</span></p>
                </div>
              </div>

              {/* Quantity Selector */}
              <div className="mt-3 flex items-center justify-between">
                <div className="flex items-center gap-3 bg-background rounded-xl px-1 py-1">
                  <button
                    onClick={() => updateQty(product.id, -1)}
                    className="w-8 h-8 rounded-lg bg-white border border-border flex items-center justify-center hover:bg-gray-50 transition-colors"
                    disabled={qty === 0}
                  >
                    <Minus className="w-4 h-4" />
                  </button>
                  <span className="w-8 text-center font-semibold text-text-primary">{qty}</span>
                  <button
                    onClick={() => updateQty(product.id, 1)}
                    className="w-8 h-8 rounded-lg bg-primary-600 text-white flex items-center justify-center hover:bg-primary-700 transition-colors"
                  >
                    <Plus className="w-4 h-4" />
                  </button>
                </div>
                {qty > 0 && (
                  <span className="text-sm font-semibold text-primary-600">₹{qty * product.price}</span>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Product Details */}
      <div className="px-4 mt-6 mb-6">
        <h3 className="text-sm font-semibold text-text-primary mb-3">Product Details</h3>
        <div className="flex gap-3">
          <div className="flex items-center gap-2 bg-green-50 border border-green-200 rounded-xl px-3 py-2">
            <ShieldCheck className="w-4 h-4 text-green-600" />
            <span className="text-xs font-medium text-green-700">RO Purified</span>
          </div>
          <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-200 rounded-xl px-3 py-2">
            <Leaf className="w-4 h-4 text-emerald-600" />
            <span className="text-xs font-medium text-emerald-700">Healthy & Safe</span>
          </div>
        </div>
      </div>

      {/* Add to Cart CTA */}
      {totalItems > 0 && (
        <div className="sticky bottom-20 px-4 pb-4">
          <Link
            href={`/app/checkout?items=${totalItems}&total=${totalPrice}`}
            className="w-full flex items-center justify-between bg-primary-600 text-white font-semibold px-6 py-4 rounded-2xl shadow-lg shadow-primary-600/30 hover:bg-primary-700 transition-colors"
          >
            <span>Add to Cart · {totalItems} {totalItems === 1 ? "item" : "items"}</span>
            <span>₹{totalPrice}</span>
          </Link>
        </div>
      )}
    </div>
  );
}
