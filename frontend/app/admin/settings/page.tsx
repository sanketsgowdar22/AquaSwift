"use client";

import { Building2, Bell, CreditCard, MapPin, Save } from "lucide-react";

export default function SettingsPage() {
  return (
    <div className="animate-fade-in">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-text-primary">Settings</h1>
        <p className="text-text-secondary text-sm mt-1">Configure your WoW platform</p>
      </div>

      <div className="space-y-6">
        {/* Business Info */}
        <div className="bg-white border border-border rounded-2xl p-5">
          <h3 className="font-semibold text-text-primary flex items-center gap-2 mb-4">
            <Building2 className="w-5 h-5 text-primary-600" /> Business Information
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1">Business Name</label>
              <input
                defaultValue="WoW — Water on Way"
                className="w-full border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1">Contact Phone</label>
              <input
                defaultValue="+91 98765 43210"
                className="w-full border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1">Contact Email</label>
              <input
                defaultValue="support@wow.in"
                className="w-full border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1">Address</label>
              <input
                defaultValue="Banavasi, Karnataka"
                className="w-full border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 outline-none"
              />
            </div>
          </div>
        </div>

        {/* Delivery Settings */}
        <div className="bg-white border border-border rounded-2xl p-5">
          <h3 className="font-semibold text-text-primary flex items-center gap-2 mb-4">
            <MapPin className="w-5 h-5 text-primary-600" /> Delivery Settings
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1">Default Delivery Radius (km)</label>
              <input
                type="number" defaultValue={10}
                className="w-full border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1">Minimum Order (₹)</label>
              <input
                type="number" defaultValue={50}
                className="w-full border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1">Default Delivery Charge (₹)</label>
              <input
                type="number" defaultValue={20}
                className="w-full border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1">Max Delivery Time (mins)</label>
              <input
                type="number" defaultValue={60}
                className="w-full border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 outline-none"
              />
            </div>
          </div>
        </div>

        {/* Notifications */}
        <div className="bg-white border border-border rounded-2xl p-5">
          <h3 className="font-semibold text-text-primary flex items-center gap-2 mb-4">
            <Bell className="w-5 h-5 text-primary-600" /> Notification Settings
          </h3>
          <div className="space-y-3">
            {[
              { label: "Order placed notifications", enabled: true },
              { label: "Delivery status updates", enabled: true },
              { label: "Payment received alerts", enabled: true },
              { label: "Low inventory warnings", enabled: false },
            ].map((item) => (
              <div key={item.label} className="flex items-center justify-between py-2">
                <span className="text-sm text-text-primary">{item.label}</span>
                <div className={`w-10 h-6 rounded-full relative cursor-pointer transition-colors ${item.enabled ? "bg-green-500" : "bg-gray-300"}`}>
                  <div className={`w-4 h-4 rounded-full bg-white absolute top-1 transition-transform ${item.enabled ? "translate-x-5" : "translate-x-1"}`} />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Payment Gateway */}
        <div className="bg-white border border-border rounded-2xl p-5">
          <h3 className="font-semibold text-text-primary flex items-center gap-2 mb-4">
            <CreditCard className="w-5 h-5 text-primary-600" /> Payment Gateway
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1">Provider</label>
              <select className="w-full border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 outline-none">
                <option>Razorpay</option>
                <option>Paytm</option>
                <option>PhonePe</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-text-secondary mb-1">API Key</label>
              <input
                type="password" defaultValue="rzp_live_xxxxxxxx"
                className="w-full border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 outline-none"
              />
            </div>
          </div>
        </div>

        {/* Save Button */}
        <button className="flex items-center gap-2 bg-primary-600 text-white px-6 py-3 rounded-xl font-medium hover:bg-primary-700 transition-colors">
          <Save className="w-5 h-5" /> Save Changes
        </button>
      </div>
    </div>
  );
}
