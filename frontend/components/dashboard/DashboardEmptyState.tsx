import React from "react";
import Link from "next/link";
import { PlusCircle, CreditCard, Sparkles, PieChart, ShieldCheck } from "lucide-react";

export function DashboardEmptyState() {
  return (
    <div className="flex flex-col items-center justify-center p-8 sm:p-16 rounded-3xl bg-slate-900/40 border border-slate-800/80 text-center max-w-2xl mx-auto space-y-6 shadow-2xl relative overflow-hidden">
      {/* Background radial glow */}
      <div className="absolute -top-24 left-1/2 -translate-x-1/2 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

      {/* Decorative Icon */}
      <div className="relative">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500/20 to-purple-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 shadow-xl shadow-indigo-500/10">
          <PieChart className="w-8 h-8" />
        </div>
        <div className="absolute -bottom-1 -right-1 p-1 rounded-full bg-slate-900 border border-slate-800 text-amber-400">
          <Sparkles className="w-3.5 h-3.5" />
        </div>
      </div>

      {/* Copy */}
      <div className="space-y-2 max-w-md">
        <h3 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
          No subscriptions yet
        </h3>
        <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
          Add your first subscription to start seeing spending insights, normalized monthly totals, service breakdowns, and upcoming renewals.
        </p>
      </div>

      {/* Action CTA */}
      <div className="pt-2 flex flex-col sm:flex-row items-center gap-3">
        <Link
          href="/subscriptions"
          className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 active:scale-95 text-white font-semibold text-xs sm:text-sm transition shadow-lg shadow-indigo-600/25"
        >
          <PlusCircle className="w-4 h-4" /> Add Subscription
        </Link>
      </div>

      {/* Feature teaser pills */}
      <div className="pt-4 border-t border-slate-800/60 flex flex-wrap items-center justify-center gap-4 text-[11px] text-slate-500">
        <span className="flex items-center gap-1.5">
          <CreditCard className="w-3.5 h-3.5 text-indigo-400" /> Multi-cycle Normalization
        </span>
        <span className="flex items-center gap-1.5">
          <PieChart className="w-3.5 h-3.5 text-purple-400" /> Spending Visualizations
        </span>
        <span className="flex items-center gap-1.5">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" /> Tenant-Isolated Storage
        </span>
      </div>
    </div>
  );
}
