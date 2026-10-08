import React from "react";
import { Coins } from "lucide-react";

interface CurrencySelectorProps {
  currencies: string[];
  selectedCurrency: string;
  onSelectCurrency: (currency: string) => void;
  currencyCounts?: Record<string, number>;
}

export function CurrencySelector({
  currencies,
  selectedCurrency,
  onSelectCurrency,
  currencyCounts,
}: CurrencySelectorProps) {
  if (currencies.length <= 1) {
    return null; // No selector needed if user only has 1 or 0 currencies
  }

  return (
    <div className="flex items-center gap-2 p-1.5 rounded-2xl bg-slate-900/80 border border-slate-800 text-xs">
      <div className="flex items-center gap-1.5 px-2.5 py-1 text-slate-400 font-medium">
        <Coins className="w-3.5 h-3.5 text-indigo-400" />
        <span className="hidden sm:inline">Active Currency:</span>
      </div>
      <div className="flex items-center gap-1">
        {currencies.map((curr) => {
          const isSelected = curr === selectedCurrency;
          const count = currencyCounts?.[curr];
          return (
            <button
              key={curr}
              onClick={() => onSelectCurrency(curr)}
              className={`px-3 py-1 rounded-xl font-semibold transition flex items-center gap-1.5 ${
                isSelected
                  ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
            >
              <span>{curr}</span>
              {count !== undefined && (
                <span
                  className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                    isSelected ? "bg-indigo-700 text-indigo-100" : "bg-slate-800 text-slate-400"
                  }`}
                >
                  {count}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
