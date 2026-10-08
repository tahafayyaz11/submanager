"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import {
  Subscription,
  SubscriptionCreate,
  SubscriptionUpdate,
  getSubscriptions,
  createSubscription,
  updateSubscription,
  archiveSubscription,
} from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import { SubscriptionForm } from "@/components/SubscriptionForm";
import { SubscriptionList } from "@/components/SubscriptionList";
import {
  Plus,
  ArrowLeft,
  RefreshCw,
  CheckCircle2,
  AlertTriangle,
  ShieldCheck,
  UserCheck,
  LogIn,
  UserPlus,
  Sparkles,
} from "lucide-react";

export default function SubscriptionsPage() {
  const { user, token, isAuthenticated, login, signup } = useAuth();

  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const [statusFilter, setStatusFilter] = useState<string>("active");

  // Modal form state
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingSub, setEditingSub] = useState<Subscription | null>(null);

  const loadData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getSubscriptions(
        statusFilter === "all" ? undefined : statusFilter,
        token || undefined
      );
      setSubscriptions(data);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Failed to load subscriptions";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [statusFilter, token]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleCreateOrUpdate = async (
    payload: SubscriptionCreate | SubscriptionUpdate
  ) => {
    setError(null);
    try {
      if (editingSub) {
        await updateSubscription(editingSub.id, payload, token || undefined);
        setSuccessMsg(`Successfully updated "${payload.service_name || editingSub.service_name}"`);
      } else {
        await createSubscription(payload as SubscriptionCreate, token || undefined);
        setSuccessMsg(`Successfully added "${payload.service_name}"`);
      }
      setIsFormOpen(false);
      setEditingSub(null);
      await loadData();
      setTimeout(() => setSuccessMsg(null), 4000);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Submission failed";
      throw new Error(msg);
    }
  };

  const handleArchive = async (id: string) => {
    if (!confirm("Are you sure you want to archive this subscription?")) return;
    try {
      await archiveSubscription(id, token || undefined);
      setSuccessMsg("Subscription archived successfully");
      await loadData();
      setTimeout(() => setSuccessMsg(null), 4000);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to archive subscription";
      setError(msg);
    }
  };

  const handleQuickSwitch = async (email: string, name: string) => {
    setLoading(true);
    try {
      try {
        await login(email, "DemoPassword2026!");
      } catch {
        await signup(email, "DemoPassword2026!", name);
      }
      setSuccessMsg(`Switched to ${name}'s isolated workspace!`);
      setTimeout(() => setSuccessMsg(null), 4000);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Switch failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-12 selection:bg-indigo-500 selection:text-white">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Navigation & Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div className="space-y-1">
            <Link
              href="/"
              className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-indigo-400 transition mb-2"
            >
              <ArrowLeft className="w-3.5 h-3.5" /> Back to Dashboard
            </Link>
            <div className="flex items-center gap-3">
              <h1 className="text-3xl font-extrabold text-white tracking-tight">
                Subscription Management
              </h1>
              {isAuthenticated && (
                <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  <ShieldCheck className="w-3 h-3" /> Isolated Workspace
                </span>
              )}
            </div>
            <p className="text-xs text-slate-400">
              Phase 3 Authenticated CRUD — Enforcing 100% user ownership and tenant isolation
            </p>
          </div>

          {/* Action buttons */}
          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={() => {
                setEditingSub(null);
                setIsFormOpen(true);
              }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 active:scale-95 text-white font-semibold text-xs transition shadow-lg shadow-indigo-600/25"
            >
              <Plus className="w-4 h-4" /> Add Subscription
            </button>
          </div>
        </div>

        {/* Tenant Isolation & Identity Bar */}
        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-indigo-600/10 text-indigo-400 border border-indigo-500/20">
              <UserCheck className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-semibold text-slate-200">
                  Active User Tenant:
                </span>
                <span className="font-mono text-indigo-300">
                  {isAuthenticated && user
                    ? `${user.full_name || "User"} (${user.email})`
                    : "Development Environment Fallback"}
                </span>
              </div>
              <p className="text-[11px] text-slate-400">
                {isAuthenticated
                  ? "Bearer JWT token validated. Queries strictly scoped to your user ID in Postgres."
                  : "Sign in to activate full JWT-authenticated isolated storage."}
              </p>
            </div>
          </div>

          {/* Quick isolation testing buttons */}
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-amber-400" /> Test Isolation:
            </span>
            <button
              onClick={() => handleQuickSwitch("alice@subsfolio.local", "Alice Cooper")}
              className={`px-2.5 py-1 rounded-lg text-[11px] font-medium border transition ${
                user?.email === "alice@subsfolio.local"
                  ? "bg-indigo-600 text-white border-indigo-500"
                  : "bg-slate-950 text-slate-400 border-slate-800 hover:text-white"
              }`}
            >
              Alice
            </button>
            <button
              onClick={() => handleQuickSwitch("bob@subsfolio.local", "Bob Dylan")}
              className={`px-2.5 py-1 rounded-lg text-[11px] font-medium border transition ${
                user?.email === "bob@subsfolio.local"
                  ? "bg-indigo-600 text-white border-indigo-500"
                  : "bg-slate-950 text-slate-400 border-slate-800 hover:text-white"
              }`}
            >
              Bob
            </button>
            {!isAuthenticated && (
              <Link
                href="/login"
                className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-medium bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 hover:bg-indigo-600/30 transition"
              >
                <LogIn className="w-3 h-3" /> Log In
              </Link>
            )}
          </div>
        </div>

        {/* Notifications */}
        {successMsg && (
          <div className="flex items-center gap-2 p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs">
            <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        {error && (
          <div className="flex items-center gap-2 p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs">
            <AlertTriangle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Filter Toolbar */}
        <div className="flex items-center justify-between">
          <div className="inline-flex rounded-xl bg-slate-900 border border-slate-800 p-1 text-xs">
            {["active", "archived", "all"].map((status) => (
              <button
                key={status}
                onClick={() => setStatusFilter(status)}
                className={`px-3 py-1 rounded-lg capitalize font-medium transition ${
                  statusFilter === status
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {status}
              </button>
            ))}
          </div>

          <button
            onClick={loadData}
            disabled={loading}
            className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-900 border border-slate-800 transition"
            title="Refresh list"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          </button>
        </div>

        {/* Subscriptions Grid */}
        <SubscriptionList
          subscriptions={subscriptions}
          loading={loading}
          onEdit={(sub) => {
            setEditingSub(sub);
            setIsFormOpen(true);
          }}
          onArchive={handleArchive}
        />

        {/* Create / Edit Form Modal */}
        <SubscriptionForm
          isOpen={isFormOpen}
          initialData={editingSub}
          onSubmit={handleCreateOrUpdate}
          onCancel={() => {
            setIsFormOpen(false);
            setEditingSub(null);
          }}
        />
      </div>
    </main>
  );
}
