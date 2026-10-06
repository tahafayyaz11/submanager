"use client";

import React, { useState, useEffect } from "react";
import { Subscription, SubscriptionCreate, SubscriptionUpdate } from "@/lib/api";
import { X, Check } from "lucide-react";

interface SubscriptionFormProps {
  initialData?: Subscription | null;
  onSubmit: (data: SubscriptionCreate | SubscriptionUpdate) => Promise<void>;
  onCancel: () => void;
  isOpen: boolean;
}

const CATEGORIES = [
  "Entertainment",
  "AI Tools",
  "Productivity",
  "Cloud Storage",
  "Developer Tools",
  "Fitness",
  "Finance",
  "Gaming",
  "Education",
  "Other",
];

const BILLING_CYCLES = ["monthly", "yearly", "quarterly", "weekly"] as const;

export function SubscriptionForm({
  initialData,
  onSubmit,
  onCancel,
  isOpen,
}: SubscriptionFormProps) {
  const [serviceName, setServiceName] = useState("");
  const [planName, setPlanName] = useState("");
  const [price, setPrice] = useState("");
  const [currency, setCurrency] = useState("USD");
  const [billingCycle, setBillingCycle] = useState<"monthly" | "yearly" | "quarterly" | "weekly">("monthly");
  const [renewalDate, setRenewalDate] = useState("");
  const [category, setCategory] = useState("Other");
  const [paymentMethod, setPaymentMethod] = useState("");
  const [reminderDays, setReminderDays] = useState("7, 3, 1");
  const [notes, setNotes] = useState("");
  const [status, setStatus] = useState<"active" | "cancelled" | "archived" | "paused">("active");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (initialData) {
      setServiceName(initialData.service_name);
      setPlanName(initialData.plan_name || "");
      setPrice(initialData.price);
      setCurrency(initialData.currency);
      setBillingCycle(initialData.billing_cycle);
      setRenewalDate(initialData.renewal_date);
      setCategory(initialData.category);
      setPaymentMethod(initialData.payment_method || "");
      setReminderDays(initialData.reminder_days_before.join(", "));
      setNotes(initialData.notes || "");
      setStatus(initialData.status);
    } else {
      setServiceName("");
      setPlanName("");
      setPrice("");
      setCurrency("USD");
      setBillingCycle("monthly");
      // Default to 30 days from now
      const nextMonth = new Date();
      nextMonth.setDate(nextMonth.getDate() + 30);
      setRenewalDate(nextMonth.toISOString().split("T")[0]);
      setCategory("Other");
      setPaymentMethod("");
      setReminderDays("7, 3, 1");
      setNotes("");
      setStatus("active");
    }
    setError(null);
  }, [initialData, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!serviceName.trim()) {
      setError("Service name is required.");
      return;
    }

    const numPrice = parseFloat(price);
    if (isNaN(numPrice) || numPrice < 0) {
      setError("Price must be a valid non-negative number.");
      return;
    }

    if (currency.trim().length !== 3) {
      setError("Currency must be exactly three uppercase letters (e.g. USD, EUR, PKR).");
      return;
    }

    if (!renewalDate) {
      setError("Renewal date is required.");
      return;
    }

    const parsedDays = reminderDays
      .split(",")
      .map((d) => parseInt(d.trim(), 10))
      .filter((d) => !isNaN(d) && d >= 0);

    const payload: SubscriptionCreate = {
      service_name: serviceName.trim(),
      plan_name: planName.trim() || null,
      price: numPrice.toFixed(2),
      currency: currency.trim().toUpperCase(),
      billing_cycle: billingCycle,
      renewal_date: renewalDate,
      category,
      payment_method: paymentMethod.trim() || null,
      reminder_days_before: parsedDays.length > 0 ? parsedDays : [7, 3, 1],
      notes: notes.trim() || null,
      status,
    };

    setLoading(true);
    try {
      await onSubmit(payload);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "An error occurred";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto">
      <div className="w-full max-w-lg rounded-2xl bg-slate-900 border border-slate-800 p-6 shadow-2xl text-slate-100 my-8">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-4">
          <h2 className="text-xl font-bold">
            {initialData ? "Edit Subscription" : "Add New Subscription"}
          </h2>
          <button
            onClick={onCancel}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block font-medium text-slate-300 mb-1">
                Service Name *
              </label>
              <input
                type="text"
                value={serviceName}
                onChange={(e) => setServiceName(e.target.value)}
                placeholder="e.g. Netflix, Spotify"
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-100 focus:outline-none focus:border-indigo-500"
                required
              />
            </div>

            <div>
              <label className="block font-medium text-slate-300 mb-1">
                Plan Name
              </label>
              <input
                type="text"
                value={planName}
                onChange={(e) => setPlanName(e.target.value)}
                placeholder="e.g. Standard 4K, Pro"
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
            <div>
              <label className="block font-medium text-slate-300 mb-1">
                Price *
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                placeholder="10.99"
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-100 focus:outline-none focus:border-indigo-500"
                required
              />
            </div>

            <div>
              <label className="block font-medium text-slate-300 mb-1">
                Currency *
              </label>
              <input
                type="text"
                maxLength={3}
                value={currency}
                onChange={(e) => setCurrency(e.target.value.toUpperCase())}
                placeholder="USD"
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-100 focus:outline-none focus:border-indigo-500"
                required
              />
            </div>

            <div className="col-span-2 sm:col-span-1">
              <label className="block font-medium text-slate-300 mb-1">
                Billing Cycle
              </label>
              <select
                value={billingCycle}
                onChange={(e) => setBillingCycle(e.target.value as "monthly" | "yearly" | "quarterly" | "weekly")}
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-100 focus:outline-none focus:border-indigo-500"
              >
                {BILLING_CYCLES.map((cycle) => (
                  <option key={cycle} value={cycle}>
                    {cycle.charAt(0).toUpperCase() + cycle.slice(1)}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block font-medium text-slate-300 mb-1">
                Next Renewal Date *
              </label>
              <input
                type="date"
                value={renewalDate}
                onChange={(e) => setRenewalDate(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-100 focus:outline-none focus:border-indigo-500"
                required
              />
            </div>

            <div>
              <label className="block font-medium text-slate-300 mb-1">
                Category
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-100 focus:outline-none focus:border-indigo-500"
              >
                {CATEGORIES.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block font-medium text-slate-300 mb-1">
                Payment Method
              </label>
              <input
                type="text"
                value={paymentMethod}
                onChange={(e) => setPaymentMethod(e.target.value)}
                placeholder="e.g. Visa 4242, PayPal"
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div>
              <label className="block font-medium text-slate-300 mb-1">
                Status
              </label>
              <select
                value={status}
                onChange={(e) => setStatus(e.target.value as "active" | "cancelled" | "archived" | "paused")}
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-100 focus:outline-none focus:border-indigo-500"
              >
                <option value="active">Active</option>
                <option value="paused">Paused</option>
                <option value="cancelled">Cancelled</option>
                <option value="archived">Archived</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block font-medium text-slate-300 mb-1">
              Reminder Days Before (comma separated)
            </label>
            <input
              type="text"
              value={reminderDays}
              onChange={(e) => setReminderDays(e.target.value)}
              placeholder="7, 3, 1"
              className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-100 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div>
            <label className="block font-medium text-slate-300 mb-1">
              Notes
            </label>
            <textarea
              rows={2}
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Cancellation link or account details..."
              className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-slate-100 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
            <button
              type="button"
              onClick={onCancel}
              disabled={loading}
              className="px-4 py-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center gap-2 px-5 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium transition"
            >
              <Check className="w-4 h-4" />
              {loading ? "Saving..." : initialData ? "Save Changes" : "Create Subscription"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
