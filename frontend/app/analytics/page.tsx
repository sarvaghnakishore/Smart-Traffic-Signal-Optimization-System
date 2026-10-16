"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import Link from "next/link";
import { ArrowLeft, BarChart3, Activity, ShieldCheck, RefreshCw } from "lucide-react";

const API = "http://localhost:8000";

interface HistoryRecord {
  lane_id?: string;
  vehicle_count?: number;
  vehicles?: number;
  congestion_level?: string;
  density?: string;
  timestamp?: string;
}

export default function Analytics() {
  const [data, setData] = useState<HistoryRecord[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchHistory = () => {
    setLoading(true);
    axios
      .get(`${API}/analytics/history`)
      .then((res) => {
        setData(res.data || []);
      })
      .catch((err) => {
        console.error("Analytics fetch error:", err);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="min-h-screen bg-navy-950 text-slate-200 p-6 md:p-10 font-sans">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link
              href="/dashboard"
              className="w-10 h-10 rounded-xl bg-navy-900 border border-white/10 flex items-center justify-center text-slate-400 hover:text-white hover:border-blue-500/40 transition-all"
            >
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <div>
              <h1 className="text-2xl font-black text-white uppercase italic tracking-tight flex items-center gap-2">
                <BarChart3 className="w-6 h-6 text-blue-400" />
                Historical Traffic Analytics
              </h1>
              <p className="text-xs text-slate-500 uppercase tracking-widest">
                Database Records & Congestion History
              </p>
            </div>
          </div>

          <button
            onClick={fetchHistory}
            className="flex items-center gap-2 bg-blue-600/10 hover:bg-blue-600/20 border border-blue-500/20 text-blue-400 px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition-all"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
            Refresh
          </button>
        </div>

        {/* Data List */}
        {loading ? (
          <div className="navy-card p-12 text-center text-slate-500">
            <RefreshCw className="w-8 h-8 text-blue-500 animate-spin mx-auto mb-3" />
            <p className="text-xs font-bold uppercase tracking-widest">Loading Analytics History...</p>
          </div>
        ) : data.length === 0 ? (
          <div className="navy-card p-12 text-center text-slate-500">
            <Activity className="w-10 h-10 text-slate-600 mx-auto mb-3" />
            <p className="text-xs font-bold uppercase tracking-widest">No historical records found</p>
            <p className="text-[10px] text-slate-600 mt-1">Run detection cycles on the dashboard to populate history</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {data.map((item, index) => {
              const count = item.vehicle_count ?? item.vehicles ?? 0;
              const density = item.congestion_level ?? item.density ?? "LOW";
              const lane = item.lane_id ?? "All";
              const timeStr = item.timestamp
                ? new Date(item.timestamp).toLocaleTimeString()
                : `Record #${index + 1}`;

              const densityColor =
                density === "HIGH"
                  ? "text-rose-400 bg-rose-500/10 border-rose-500/20"
                  : density === "MEDIUM"
                  ? "text-amber-400 bg-amber-500/10 border-amber-500/20"
                  : "text-emerald-400 bg-emerald-500/10 border-emerald-500/20";

              return (
                <div
                  key={index}
                  className="navy-card p-5 border border-white/5 hover:border-blue-500/30 transition-all flex flex-col justify-between gap-3"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-black text-white uppercase tracking-wider">
                      Lane: {lane}
                    </span>
                    <span
                      className={`text-[9px] font-black px-2.5 py-0.5 rounded-full border uppercase tracking-widest ${densityColor}`}
                    >
                      {density}
                    </span>
                  </div>

                  <div className="flex items-baseline justify-between pt-2 border-t border-white/5">
                    <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">
                      Vehicles Detected
                    </span>
                    <span className="text-xl font-black text-white tabular-nums">
                      {count} <span className="text-xs text-slate-500 font-normal">veh</span>
                    </span>
                  </div>

                  <div className="text-[9px] text-slate-500 font-mono text-right">
                    {timeStr}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
