"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-context";
import {
  Lock,
  Mail,
  Eye,
  EyeOff,
  LogIn,
  AlertCircle,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
} from "lucide-react";

export default function LoginPage() {
  const router = useRouter();
  const { login, signup } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [demoNotice, setDemoNotice] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      setError("Please enter both email and password.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      await login(email, password);
      router.push("/subscriptions");
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to log in";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickDemoLogin = async (demoEmail: string, demoName: string) => {
    setLoading(true);
    setError(null);
    setDemoNotice(`Setting up ${demoName}'s isolated account...`);
    const demoPassword = "DemoPassword2026!";
    try {
      // First attempt login
      try {
        await login(demoEmail, demoPassword);
      } catch {
        // If not registered yet, auto-register demo user
        await signup(demoEmail, demoPassword, demoName);
      }
      setDemoNotice(`Logged in as ${demoName}! Redirecting...`);
      setTimeout(() => {
        router.push("/subscriptions");
      }, 500);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Demo login failed";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-[calc(100vh-4rem)] flex flex-col items-center justify-center p-6 bg-slate-950 text-slate-100 relative overflow-hidden">
      {/* Background Glow */}
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[32rem] h-[32rem] bg-indigo-600/15 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md relative z-10 space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <ShieldCheck className="w-3.5 h-3.5" /> Phase 3 Authentication Active
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">
            Sign In to Subsfolio
          </h1>
          <p className="text-xs text-slate-400">
            Access your secure subscription intelligence dashboard
          </p>
        </div>

        {/* Login Card */}
        <div className="bg-slate-900/80 backdrop-blur-md border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-2xl space-y-5">
          {error && (
            <div className="flex items-center gap-2 p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {demoNotice && (
            <div className="flex items-center gap-2 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs">
              <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
              <span>{demoNotice}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email Field */}
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-slate-300">
                Email Address
              </label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  className="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-slate-100 placeholder-slate-500 text-xs transition"
                />
              </div>
            </div>

            {/* Password Field */}
            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <label className="text-xs font-medium text-slate-300">
                  Password
                </label>
              </div>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type={showPassword ? "text" : "password"}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-10 pr-10 py-2.5 rounded-xl bg-slate-950 border border-slate-800 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-slate-100 placeholder-slate-500 text-xs transition"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition"
                  tabIndex={-1}
                >
                  {showPassword ? (
                    <EyeOff className="w-4 h-4" />
                  ) : (
                    <Eye className="w-4 h-4" />
                  )}
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 active:scale-95 text-white font-semibold text-xs transition shadow-lg shadow-indigo-600/25 disabled:opacity-50"
            >
              <LogIn className="w-4 h-4" />
              {loading ? "Authenticating..." : "Sign In with Email"}
            </button>
          </form>

          {/* Quick Demo Isolation Switchers */}
          <div className="pt-2 border-t border-slate-800/80 space-y-2">
            <p className="text-[11px] text-slate-400 flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-amber-400" />
              <span>Test User Isolation (1-Click Accounts):</span>
            </p>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() =>
                  handleQuickDemoLogin("alice@subsfolio.local", "Alice Cooper")
                }
                disabled={loading}
                className="px-2.5 py-2 rounded-lg bg-slate-950 border border-slate-800 hover:border-indigo-500/50 hover:bg-slate-900 text-left text-xs transition group"
              >
                <div className="font-semibold text-slate-200 group-hover:text-indigo-400">
                  Alice (User A)
                </div>
                <div className="text-[10px] text-slate-500 truncate">
                  alice@subsfolio.local
                </div>
              </button>

              <button
                type="button"
                onClick={() =>
                  handleQuickDemoLogin("bob@subsfolio.local", "Bob Dylan")
                }
                disabled={loading}
                className="px-2.5 py-2 rounded-lg bg-slate-950 border border-slate-800 hover:border-indigo-500/50 hover:bg-slate-900 text-left text-xs transition group"
              >
                <div className="font-semibold text-slate-200 group-hover:text-indigo-400">
                  Bob (User B)
                </div>
                <div className="text-[10px] text-slate-500 truncate">
                  bob@subsfolio.local
                </div>
              </button>
            </div>
          </div>

          {/* Clerk Auth Section Badge */}
          <div className="pt-2 border-t border-slate-800/80">
            <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-semibold text-slate-300 flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                  Clerk Auth Ready
                </span>
                <span className="text-[10px] text-indigo-400 font-mono">
                  Ready to link
                </span>
              </div>
              <p className="text-[10px] text-slate-400">
                Configured with isolated JWT support and auto-provisioning for Clerk tokens.
              </p>
            </div>
          </div>
        </div>

        {/* Footer Link to Signup */}
        <p className="text-center text-xs text-slate-400">
          Don&apos;t have an account yet?{" "}
          <Link
            href="/signup"
            className="text-indigo-400 hover:text-indigo-300 font-medium inline-flex items-center gap-1"
          >
            Create account <ArrowRight className="w-3 h-3" />
          </Link>
        </p>
      </div>
    </main>
  );
}
