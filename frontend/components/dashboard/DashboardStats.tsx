import React from "react";
import {
  CurrencySpendSummary,
  NearestRenewal,
} from "@/lib/api";
import {
  DollarSign,
  Calendar,
  Layers,
  Clock,
  Sparkles,
  ArrowUpRight,
} from "lucide-react";

interface DashboardStatsProps {
  summary: {
    currencies: Record<string, CurrencySpendSummary>;
    primary_currency: string | null;
    total_active_subscriptions: number;
    nearest_renewal: NearestRenewal | null;
  };
  activeCurrency: string;
}

function formatAmount(amountStr: string, currency: string) {
  const num = parseFloat(amountStr);
  if (isNaN(num)) return `${currency} 0.00`;
  return `${currency} ${num.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}

function formatDate(dateStr: string) {
  try {
    const d = new Date(dateStr);
    return d.toLocaleDateString("en-US", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  } catch {
    return dateStr;
  }
}

export function DashboardStats({ summary, activeCurrency }: DashboardStatsProps) {
  const currentCurrencySummary = summary.currencies[activeCurrency];

  const monthlySpendFormatted = currentCurrencySummary
    ? formatAmount(currentCurrencySummary.monthly_spend, activeCurrency)
    : `${activeCurrency || "USD"} 0.00`;

  const annualSpendFormatted = currentCurrencySummary
    ? formatAmount(currentCurrencySummary.annual_spend, activeCurrency)
    : `${activeCurrency || "USD"} 0.00`;

  const nearest = summary.nearest_renewal;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* 1. Monthly Recurring Spend Card */}
      <div className="p-5 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-900/60 border border-slate-800 shadow-lg relative overflow-hidden group hover:border-slate-700 transition">
        <div className="absolute top-0 right-0 w-24 h-24 bg-indigo-500/5 rounded-full blur-2xl pointer-events-none group-hover:bg-indigo-500/10 transition" />
        <div className="flex items-center justify-between pb-3">
          <span className="text-xs font-semibold text-slate-400">Monthly Spend</span>
          <div className="w-8 h-8 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center">
            <DollarSign className="w-4 h-4" />
          </div>
        </div>
        <div className="space-y-1">
          <div className="text-2xl font-extrabold text-white tracking-tight">
            {monthlySpendFormatted}
          </div>
          <p className="text-[11px] text-slate-400 flex items-center gap-1">
            <span className="text-emerald-400 font-semibold">Normalized</span> current recurring
          </p>
        </div>
      </div>

      {/* 2. Estimated Annual Spend Card */}
      <div className="p-5 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-900/60 border border-slate-800 shadow-lg relative overflow-hidden group hover:border-slate-700 transition">
        <div className="absolute top-0 right-0 w-24 h-24 bg-purple-500/5 rounded-full blur-2xl pointer-events-none group-hover:bg-purple-500/10 transition" />
        <div className="flex items-center justify-between pb-3">
          <span className="text-xs font-semibold text-slate-400">Annual Spend</span>
          <div className="w-8 h-8 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-400 flex items-center justify-center">
            <Calendar className="w-4 h-4" />
          </div>
        </div>
        <div className="space-y-1">
          <div className="text-2xl font-extrabold text-white tracking-tight">
            {annualSpendFormatted}
          </div>
          <p className="text-[11px] text-slate-400 flex items-center gap-1">
            <span className="text-indigo-400 font-semibold">Estimated</span> yearly projection
          </p>
        </div>
      </div>

      {/* 3. Active Subscriptions Count Card */}
      <div className="p-5 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-900/60 border border-slate-800 shadow-lg relative overflow-hidden group hover:border-slate-700 transition">
        <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-500/5 rounded-full blur-2xl pointer-events-none group-hover:bg-emerald-500/10 transition" />
        <div className="flex items-center justify-between pb-3">
          <span className="text-xs font-semibold text-slate-400">Active Subscriptions</span>
          <div className="w-8 h-8 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center">
            <Layers className="w-4 h-4" />
          </div>
        </div>
        <div className="space-y-1">
          <div className="text-2xl font-extrabold text-white tracking-tight">
            {summary.total_active_subscriptions}
          </div>
          <p className="text-[11px] text-slate-400">
            {currentCurrencySummary ? (
              <span>
                {currentCurrencySummary.active_subscriptions_count} in {activeCurrency}
              </span>
            ) : (
              "Total across all currencies"
            )}
          </p>
        </div>
      </div>

      {/* 4. Next Renewal Card */}
      <div className="p-5 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-900/60 border border-slate-800 shadow-lg relative overflow-hidden group hover:border-slate-700 transition">
        <div className="absolute top-0 right-0 w-24 h-24 bg-amber-500/5 rounded-full blur-2xl pointer-events-none group-hover:bg-amber-500/10 transition" />
        <div className="flex items-center justify-between pb-3">
          <span className="text-xs font-semibold text-slate-400">Next Renewal</span>
          <div className="w-8 h-8 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 flex items-center justify-center">
            <Clock className="w-4 h-4" />
          </div>
        </div>
        {nearest ? (
          <div className="space-y-1">
            <div className="flex items-center justify-between gap-2">
              <span className="text-base font-bold text-white truncate">
                {nearest.service_name}
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded-full font-semibold bg-amber-500/10 text-amber-300 border border-amber-500/20 flex-shrink-0">
                {nearest.days_until < 0
                  ? "Overdue"
                  : nearest.days_until === 0
                  ? "Today"
                  : `In ${nearest.days_until}d`}
              </span>
            </div>
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>{formatDate(nearest.renewal_date)}</span>
              <span className="font-semibold text-slate-200">
                {formatAmount(nearest.price, nearest.currency)}
              </span>
            </div>
          </div>
        ) : (
          <div className="text-xs text-slate-500 py-1">No upcoming renewals</div>
        )}
      </div>
    </div>
  );
}
