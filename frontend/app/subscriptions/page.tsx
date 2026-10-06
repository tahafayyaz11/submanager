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
import { SubscriptionForm } from "@/components/SubscriptionForm";
import { SubscriptionList } from "@/components/SubscriptionList";
import { Plus, ArrowLeft, User, RefreshCw, CheckCircle2, AlertTriangle } from "lucide-react";

export default function SubscriptionsPage() {
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // Development user identity switcher (supports testing user-isolation)
  const [userId, setUserId] = useState<string>("dev-user-0001");
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
        userId
      );
      setSubscriptions(data);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Failed to load subscriptions";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [statusFilter, userId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleCreateOrUpdate = async (
    payload: SubscriptionCreate | SubscriptionUpdate
  ) => {
    setError(null);
    try {
      if (editingSub) {
        await updateSubscription(editingSub.id, payload, userId);
        setSuccessMsg(`Successfully updated "${payload.service_name || editingSub.service_name}"`);
      } else {
        await createSubscription(payload as SubscriptionCreate, userId);
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
      await archiveSubscription(id, userId);
      setSuccessMsg("Subscription archived successfully");
      await loadData();
      setTimeout(() => setSuccessMsg(null), 4000);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Failed to archive subscription";
      setError(msg);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-12 selection:bg-indigo-500 selection:text-white">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Navigation & Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-6">
          <div className="space-y-1">
            <Link
              href="/"
              className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-indigo-400 transition mb-2"
            >
              <ArrowLeft className="w-3.5 h-3.5" /> Back to Dashboard
            </Link>
            <h1 className="text-3xl font-extrabold text-white tracking-tight">
              Subscription Management
            </h1>
            <p className="text-xs text-slate-400">
              Phase 2 Core CRUD — Scoped by user identity
            </p>
          </div>

          {/* Development User Switcher */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs">
              <User className="w-3.5 h-3.5 text-indigo-400" />
              <span className="text-slate-400">User:</span>
              <input
                type="text"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                placeholder="dev-user-0001"
                className="bg-transparent border-b border-slate-700 focus:border-indigo-500 focus:outline-none text-slate-200 text-xs w-32 font-mono"
                title="Change user ID to test isolation"
              />
            </div>

            <button
              onClick={() => {
                setEditingSub(null);
                setIsFormOpen(true);
              }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 active:scale-95 text-white font-medium text-xs transition shadow-lg shadow-indigo-600/20"
            >
              <Plus className="w-4 h-4" /> Add Subscription
            </button>
          </div>
        </div>

        {/* Notifications */}
        {successMsg && (
          <div className="flex items-center gap-2 p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs">
            <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        {error && (
          <div className="flex items-center gap-2 p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs">
            <AlertTriangle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Filter Toolbar */}
        <div className="flex items-center justify-between">
          <div className="inline-flex rounded-lg bg-slate-900 border border-slate-800 p-1 text-xs">
            {["active", "archived", "all"].map((status) => (
              <button
                key={status}
                onClick={() => setStatusFilter(status)}
                className={`px-3 py-1 rounded-md capitalize font-medium transition ${
                  statusFilter === status
                    ? "bg-indigo-600 text-white"
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
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-900 transition"
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
