"use client";

import React from "react";
import { Subscription } from "@/lib/api";
import { Calendar, CreditCard, Edit2, Archive, AlertCircle } from "lucide-react";

interface SubscriptionListProps {
  subscriptions: Subscription[];
  loading: boolean;
  onEdit: (subscription: Subscription) => void;
  onArchive: (id: string) => void;
}

export function SubscriptionList({
  subscriptions,
  loading,
  onEdit,
  onArchive,
}: SubscriptionListProps) {
  if (loading) {
    return (
      <div className="p-8 text-center text-slate-400 animate-pulse text-sm">
        Loading subscriptions...
      </div>
    );
  }

  if (subscriptions.length === 0) {
    return (
      <div className="p-12 text-center rounded-2xl border border-dashed border-slate-800 text-slate-400 space-y-2">
        <AlertCircle className="w-8 h-8 mx-auto text-slate-600" />
        <p className="font-medium text-slate-300">No subscriptions found</p>
        <p className="text-xs text-slate-500">
          Click &quot;Add Subscription&quot; above to create your first recurring expense.
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {subscriptions.map((sub) => {
        const isArchived = sub.status === "archived";
        const isCancelled = sub.status === "cancelled";

        return (
          <div
            key={sub.id}
            className="flex flex-col justify-between p-5 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-slate-700 transition shadow-lg text-xs"
          >
            <div className="space-y-3">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-bold text-sm text-white">
                    {sub.service_name}
                  </h3>
                  {sub.plan_name && (
                    <p className="text-slate-400 text-[11px]">{sub.plan_name}</p>
                  )}
                </div>
                <span
                  className={`px-2 py-0.5 rounded-full text-[10px] font-semibold uppercase tracking-wider ${
                    isArchived
                      ? "bg-slate-800 text-slate-400 border border-slate-700"
                      : isCancelled
                      ? "bg-rose-500/10 text-rose-400 border border-rose-500/20"
                      : "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                  }`}
                >
                  {sub.status}
                </span>
              </div>

              <div className="flex items-baseline gap-1">
                <span className="text-xl font-extrabold text-white">
                  {sub.currency} {parseFloat(sub.price).toFixed(2)}
                </span>
                <span className="text-slate-400 text-[11px]">
                  / {sub.billing_cycle}
                </span>
              </div>

              <div className="pt-2 border-t border-slate-800/80 space-y-1.5 text-slate-400">
                <div className="flex items-center gap-1.5 text-[11px]">
                  <Calendar className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Renews: <strong className="text-slate-200">{sub.renewal_date}</strong></span>
                </div>
                {sub.category && (
                  <div className="flex items-center gap-1.5 text-[11px]">
                    <span className="inline-block w-2 h-2 rounded-full bg-indigo-500" />
                    <span>{sub.category}</span>
                  </div>
                )}
                {sub.payment_method && (
                  <div className="flex items-center gap-1.5 text-[11px]">
                    <CreditCard className="w-3.5 h-3.5 text-slate-500" />
                    <span>{sub.payment_method}</span>
                  </div>
                )}
                {sub.notes && (
                  <p className="text-[11px] text-slate-500 italic pt-1 truncate">
                    &quot;{sub.notes}&quot;
                  </p>
                )}
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-4 mt-3 border-t border-slate-800/60">
              <button
                onClick={() => onEdit(sub)}
                className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition"
                title="Edit subscription"
              >
                <Edit2 className="w-3.5 h-3.5" />
                <span>Edit</span>
              </button>
              {!isArchived && (
                <button
                  onClick={() => onArchive(sub.id)}
                  className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 transition"
                  title="Archive subscription"
                >
                  <Archive className="w-3.5 h-3.5" />
                  <span>Archive</span>
                </button>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
