import React from "react";

export function DashboardSkeleton() {
  return (
    <div className="space-y-8 animate-pulse">
      {/* Header Skeleton */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div className="space-y-2">
          <div className="h-4 w-32 bg-slate-800 rounded" />
          <div className="h-8 w-64 bg-slate-800 rounded-lg" />
          <div className="h-3 w-80 bg-slate-800/60 rounded" />
        </div>
        <div className="h-10 w-40 bg-slate-800 rounded-xl" />
      </div>

      {/* Summary Cards Skeleton */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <div
            key={i}
            className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3"
          >
            <div className="flex items-center justify-between">
              <div className="h-3 w-24 bg-slate-800 rounded" />
              <div className="w-8 h-8 rounded-xl bg-slate-800" />
            </div>
            <div className="h-7 w-32 bg-slate-800 rounded-lg" />
            <div className="h-3 w-20 bg-slate-800/60 rounded" />
          </div>
        ))}
      </div>

      {/* Charts & Breakdown Grid Skeleton */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-7 p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4">
          <div className="h-5 w-48 bg-slate-800 rounded" />
          <div className="h-64 w-full bg-slate-800/40 rounded-xl flex items-center justify-center">
            <div className="w-36 h-36 rounded-full border-8 border-slate-800 border-t-indigo-500 animate-spin" />
          </div>
        </div>

        <div className="lg:col-span-5 p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4">
          <div className="h-5 w-40 bg-slate-800 rounded" />
          <div className="space-y-3">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-12 w-full bg-slate-800/40 rounded-xl" />
            ))}
          </div>
        </div>
      </div>

      {/* Upcoming Renewals Skeleton */}
      <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4">
        <div className="h-5 w-44 bg-slate-800 rounded" />
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-24 bg-slate-800/40 rounded-xl" />
          ))}
        </div>
      </div>
    </div>
  );
}
