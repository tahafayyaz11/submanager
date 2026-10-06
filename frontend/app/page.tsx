"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { CheckCircle2, XCircle, AlertCircle, RefreshCw, Server, Database, Globe, Layers, CreditCard } from "lucide-react";

interface HealthStatus {
  status: string;
  app_name?: string;
  environment?: string;
  database?: string;
  database_connected?: boolean;
  version?: string;
}

export default function Home() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [pingLatency, setPingLatency] = useState<number | null>(null);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const fetchHealth = useCallback(async () => {
    setLoading(true);
    setError(null);
    const startTime = performance.now();
    try {
      // Query detailed health endpoint
      const res = await fetch(`${apiUrl}/api/v1/health/detailed`);
      const latency = Math.round(performance.now() - startTime);
      setPingLatency(latency);
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      }
      const data = await res.json();
      setHealth(data);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Failed to connect to backend";
      setError(message);
      // Fallback: check basic health
      try {
        const basicRes = await fetch(`${apiUrl}/health`);
        if (basicRes.ok) {
          const basicData = await basicRes.json();
          setHealth(basicData);
          setError(null);
        }
      } catch {
        setHealth(null);
      }
    } finally {
      setLoading(false);
    }
  }, [apiUrl]);

  useEffect(() => {
    fetchHealth();
  }, [fetchHealth]);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-6 md:p-12 bg-slate-950 text-slate-100 selection:bg-indigo-500 selection:text-white">
      {/* Background Glow */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-4xl relative z-10 space-y-8">
        {/* Header */}
        <header className="text-center space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <Layers className="w-3.5 h-3.5" /> Phase 1 Foundation Active
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-indigo-300 bg-clip-text text-transparent">
            Subsfolio Platform
          </h1>
          <p className="text-sm md:text-base text-slate-400 max-w-xl mx-auto">
            AI-powered subscription intelligence, management, analytics, and renewal-tracking platform.
          </p>
          <div className="pt-2">
            <Link
              href="/subscriptions"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs transition shadow-lg shadow-indigo-600/25 active:scale-95"
            >
              <CreditCard className="w-4 h-4" /> Manage Subscriptions (Phase 2 CRUD)
            </Link>
          </div>
        </header>

        {/* Verification Pipeline Card */}
        <section className="bg-slate-900/80 backdrop-blur border border-slate-800 rounded-2xl p-6 md:p-8 shadow-2xl space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <h2 className="text-lg font-semibold text-white">Full-Stack Connectivity Pipeline</h2>
              <p className="text-xs text-slate-400">Verifying Browser → Next.js → FastAPI → PostgreSQL</p>
            </div>
            <button
              onClick={fetchHealth}
              disabled={loading}
              className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-700 active:scale-95 text-slate-200 border border-slate-700 transition"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
              {loading ? "Checking..." : "Re-test Connection"}
            </button>
          </div>

          {/* 4 Pipeline Stages */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Step 1: Client Browser */}
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-3">
              <div className="flex items-center justify-between">
                <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
                  <Globe className="w-5 h-5" />
                </div>
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              </div>
              <div>
                <p className="text-xs font-semibold text-white">Browser Client</p>
                <p className="text-[11px] text-slate-400">Client DOM active</p>
              </div>
              <span className="inline-block text-[10px] font-mono text-emerald-400">OK</span>
            </div>

            {/* Step 2: Next.js Frontend */}
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-3">
              <div className="flex items-center justify-between">
                <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
                  <Layers className="w-5 h-5" />
                </div>
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              </div>
              <div>
                <p className="text-xs font-semibold text-white">Next.js App</p>
                <p className="text-[11px] text-slate-400">React & TypeScript</p>
              </div>
              <span className="inline-block text-[10px] font-mono text-emerald-400">Port 3000</span>
            </div>

            {/* Step 3: FastAPI Backend */}
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-3">
              <div className="flex items-center justify-between">
                <div className={`p-2 rounded-lg ${health?.status === "ok" ? "bg-emerald-500/10 text-emerald-400" : "bg-rose-500/10 text-rose-400"}`}>
                  <Server className="w-5 h-5" />
                </div>
                {health?.status === "ok" ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                ) : (
                  <XCircle className="w-4 h-4 text-rose-400" />
                )}
              </div>
              <div>
                <p className="text-xs font-semibold text-white">FastAPI API</p>
                <p className="text-[11px] text-slate-400">
                  {health?.status === "ok" ? `${pingLatency}ms latency` : "Not reachable"}
                </p>
              </div>
              <span className={`inline-block text-[10px] font-mono ${health?.status === "ok" ? "text-emerald-400" : "text-rose-400"}`}>
                {health?.status === "ok" ? "GET /health 200" : "Offline"}
              </span>
            </div>

            {/* Step 4: PostgreSQL Database */}
            <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-3">
              <div className="flex items-center justify-between">
                <div className={`p-2 rounded-lg ${health?.database_connected ? "bg-emerald-500/10 text-emerald-400" : "bg-amber-500/10 text-amber-400"}`}>
                  <Database className="w-5 h-5" />
                </div>
                {health?.database_connected ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                ) : (
                  <AlertCircle className="w-4 h-4 text-amber-400" />
                )}
              </div>
              <div>
                <p className="text-xs font-semibold text-white">PostgreSQL</p>
                <p className="text-[11px] text-slate-400">
                  {health?.database_connected ? "Connected" : "Service standby"}
                </p>
              </div>
              <span className={`inline-block text-[10px] font-mono ${health?.database_connected ? "text-emerald-400" : "text-amber-400"}`}>
                {health?.database_connected ? "Connected" : "Disconnected"}
              </span>
            </div>
          </div>

          {/* Detailed Diagnostic Panel */}
          <div className="rounded-xl bg-slate-950/80 border border-slate-800 p-4 font-mono text-xs space-y-2">
            <div className="flex items-center justify-between text-slate-400 pb-2 border-b border-slate-800/60">
              <span>Backend Target: {apiUrl}</span>
              <span className="text-[11px]">API v1 /health/detailed</span>
            </div>
            {loading ? (
              <p className="text-slate-400 animate-pulse">Querying backend health endpoint...</p>
            ) : error ? (
              <div className="text-rose-400 space-y-1">
                <p className="font-semibold">Connection Error:</p>
                <p className="text-[11px] text-slate-400">{error}</p>
                <p className="text-[11px] text-slate-500 pt-1">
                  Ensure backend is running: <code className="text-indigo-300">uvicorn app.main:app --port 8000</code>
                </p>
              </div>
            ) : (
              <pre className="text-emerald-400 overflow-x-auto text-[11px]">
                {JSON.stringify(health, null, 2)}
              </pre>
            )}
          </div>
        </section>

        {/* Phase 1 Completion Summary */}
        <section className="bg-slate-900/40 border border-slate-800/60 rounded-xl p-5 text-xs text-slate-400 space-y-2">
          <p className="font-medium text-slate-300">Phase 1 Foundation Verified:</p>
          <ul className="list-disc list-inside space-y-1 text-slate-400">
            <li>FastAPI application configured with CORS, Pydantic v2 schemas, and Alembic migrations.</li>
            <li>Next.js App Router scaffolded with TypeScript, Tailwind CSS tokens, and shadcn/ui readiness.</li>
            <li>PostgreSQL connection layer initialized with SQLAlchemy ORM and health diagnostics.</li>
          </ul>
        </section>
      </div>
    </main>
  );
}
