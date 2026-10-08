"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  SignInButton,
  SignUpButton,
  SignedIn,
  SignedOut,
  UserButton,
} from "@clerk/nextjs";
import {
  CreditCard,
  LogIn,
  UserPlus,
  ShieldCheck,
  Layers,
} from "lucide-react";

export function Navbar() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand */}
        <div className="flex items-center gap-6">
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-indigo-500 to-indigo-700 flex items-center justify-center text-white shadow-md shadow-indigo-600/30 group-hover:scale-105 transition">
              <Layers className="w-4 h-4" />
            </div>
            <div className="flex flex-col">
              <span className="font-extrabold text-white tracking-tight text-base leading-none">
                Subsfolio
              </span>
              <span className="text-[10px] text-indigo-400 font-mono tracking-wider">
                INTELLIGENCE
              </span>
            </div>
          </Link>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-1 text-xs font-medium">
            <Link
              href="/"
              className={`px-3 py-1.5 rounded-lg transition ${
                pathname === "/"
                  ? "bg-slate-800/80 text-white"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
              }`}
            >
              Overview
            </Link>
            <SignedIn>
              <Link
                href="/subscriptions"
                className={`px-3 py-1.5 rounded-lg transition flex items-center gap-1.5 ${
                  pathname === "/subscriptions"
                    ? "bg-indigo-600/20 text-indigo-300 border border-indigo-500/30"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
                }`}
              >
                <CreditCard className="w-3.5 h-3.5" /> Subscriptions
              </Link>
            </SignedIn>
            <SignedOut>
              <SignInButton mode="modal">
                <button
                  type="button"
                  className="px-3 py-1.5 rounded-lg transition flex items-center gap-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-900 text-xs font-medium"
                >
                  <CreditCard className="w-3.5 h-3.5" /> Subscriptions
                </button>
              </SignInButton>
            </SignedOut>
          </nav>
        </div>

        {/* Right side Clerk auth controls */}
        <div className="flex items-center gap-3">
          <SignedOut>
            <div className="flex items-center gap-2">
              <SignInButton mode="modal">
                <button className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-900 border border-slate-800 transition active:scale-95">
                  <LogIn className="w-3.5 h-3.5" /> Sign In
                </button>
              </SignInButton>
              <SignUpButton mode="modal">
                <button className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 active:scale-95 text-white transition shadow-lg shadow-indigo-600/20">
                  <UserPlus className="w-3.5 h-3.5" /> Sign Up
                </button>
              </SignUpButton>
            </div>
          </SignedOut>

          <SignedIn>
            <div className="flex items-center gap-3">
              <div className="hidden sm:flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                <span className="text-slate-300 font-medium">Clerk Auth</span>
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-mono">
                  Isolated
                </span>
              </div>
              <UserButton
                appearance={{
                  elements: {
                    userButtonAvatarBox: "w-8 h-8 rounded-full border border-indigo-500/40",
                  },
                }}
              />
            </div>
          </SignedIn>
        </div>
      </div>
    </header>
  );
}
