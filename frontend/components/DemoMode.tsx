"use client";

import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import { Zap, Play, RefreshCw, ArrowRight, Timer, BarChart3, CheckCircle2 } from "lucide-react";

const API = "http://localhost:8000";

interface DemoData {
  before: Record<string, number>;
  after: Record<string, number>;
  savings: Record<string, number>;
  total_savings_seconds: number;
  vehicle_counts: Record<string, number>;
  priority_lane: string;
  explanation: string;
}

const LANES = ["North", "South", "East", "West"];

const DENSITY_COLORS: Record<string, string> = {
  North: "#3b82f6",
  South: "#10b981",
  East:  "#f59e0b",
  West:  "#a855f7",
};

interface DemoModeProps {
  isOpen: boolean;
  onClose: () => void;
  intersectionId: string;
}

export default function DemoMode({ isOpen, onClose, intersectionId }: DemoModeProps) {
  const [demo, setDemo] = useState<DemoData | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchDemo = useCallback(async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API}/traffic/demo/${intersectionId}`);
      setDemo(res.data);
    } catch {
      // Fallback demo data
      setDemo({
        before:       { North: 30, South: 30, East: 30, West: 30 },
        after:        { North: 46, South: 24, East: 16, West: 34 },
        savings:      { North: 0,  South: 6,  East: 14, West: 0 },
        total_savings_seconds: 20,
        vehicle_counts: { North: 18, South: 7, East: 3, West: 12 },
        priority_lane: "North",
        explanation: "AI optimizer gives North lane maximum green time (46s) because it has the most vehicles (18). Total signal-cycle savings: 20s per round."
      });
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (isOpen) fetchDemo();
  }, [isOpen, fetchDemo, intersectionId]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div className="bg-navy-900 border border-white/10 rounded-[2rem] w-full max-w-3xl shadow-2xl shadow-black/50 overflow-hidden">

        {/* Header */}
        <div className="flex items-center justify-between px-8 py-5 border-b border-white/5 bg-navy-950/60">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center">
              <Zap className="w-4 h-4 text-blue-400" />
            </div>
            <div>
              <h2 className="text-sm font-black text-white uppercase tracking-tight">
                Demo Mode — Before vs After
              </h2>
              <p className="text-[9px] text-slate-500 uppercase tracking-widest font-bold">
                AI Signal Optimization Comparison
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-500 hover:text-white text-xl font-bold transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Body */}
        <div className="p-8 space-y-6">
          {loading ? (
            <div className="flex flex-col items-center justify-center py-12 gap-3">
              <RefreshCw className="w-8 h-8 text-blue-500 animate-spin" />
              <p className="text-slate-400 text-xs font-bold uppercase tracking-widest">
                Loading comparison...
              </p>
            </div>
          ) : demo ? (
            <>
              {/* Grid Comparison */}
              <div className="grid grid-cols-3 gap-4">
                {/* Column Labels */}
                <div className="text-center">
                  <span className="text-[9px] text-slate-500 font-black uppercase tracking-widest">Lane</span>
                </div>
                <div className="text-center">
                  <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-rose-500/10 border border-rose-500/20 rounded-full">
                    <span className="text-[9px] text-rose-400 font-black uppercase tracking-widest">Before (Fixed)</span>
                  </div>
                </div>
                <div className="text-center">
                  <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-500/10 border border-emerald-500/20 rounded-full">
                    <span className="text-[9px] text-emerald-400 font-black uppercase tracking-widest">After (AI Optimized)</span>
                  </div>
                </div>

                {/* Lane Rows */}
                {LANES.map((lane) => {
                  const isWinner = lane === demo.priority_lane;
                  const saved = demo.savings[lane] || 0;
                  const gained = (demo.after[lane] || 0) - (demo.before[lane] || 0);
                  return (
                    <React.Fragment key={lane}>
                      {/* Lane Name */}
                      <div className={`flex items-center gap-2.5 px-3 py-3 rounded-xl border ${isWinner ? "bg-blue-500/10 border-blue-500/20" : "bg-navy-950/40 border-white/5"}`}>
                        <div className="w-2 h-2 rounded-full" style={{ backgroundColor: DENSITY_COLORS[lane] }} />
                        <span className="text-xs font-black text-white uppercase tracking-wide">{lane}</span>
                        <span className="text-[8px] text-slate-500">({demo.vehicle_counts[lane]} veh)</span>
                        {isWinner && (
                          <span className="ml-auto text-[7px] text-blue-400 font-black uppercase bg-blue-500/15 px-1.5 py-0.5 rounded-full">PRIORITY</span>
                        )}
                      </div>

                      {/* Before */}
                      <div className="flex items-center justify-center px-3 py-3 bg-navy-950/40 border border-white/5 rounded-xl">
                        <span className="text-lg font-black text-rose-300 tabular-nums">{demo.before[lane]}s</span>
                      </div>

                      {/* After */}
                      <div className={`flex items-center justify-between px-4 py-3 rounded-xl border ${isWinner ? "bg-emerald-500/10 border-emerald-500/25" : "bg-navy-950/40 border-white/5"}`}>
                        <span className={`text-lg font-black tabular-nums ${isWinner ? "text-emerald-400" : "text-slate-300"}`}>
                          {demo.after[lane]}s
                        </span>
                        {gained !== 0 && (
                          <span className={`text-[9px] font-black px-2 py-0.5 rounded-full ${gained > 0 ? "text-emerald-400 bg-emerald-500/10" : "text-rose-400 bg-rose-500/10"}`}>
                            {gained > 0 ? "+" : ""}{gained}s
                          </span>
                        )}
                      </div>
                    </React.Fragment>
                  );
                })}
              </div>

              {/* Savings Summary */}
              <div className="grid grid-cols-3 gap-4">
                <div className="col-span-1 bg-emerald-500/10 border border-emerald-500/20 rounded-2xl p-4 text-center">
                  <span className="block text-[9px] text-emerald-400/70 font-bold uppercase tracking-widest mb-1">Total Saved</span>
                  <span className="text-2xl font-black text-emerald-400">{demo.total_savings_seconds}s</span>
                  <span className="block text-[9px] text-emerald-400/60 mt-1">per cycle</span>
                </div>
                <div className="col-span-2 bg-navy-950/40 border border-white/5 rounded-2xl p-4">
                  <div className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-blue-400 mt-0.5 shrink-0" />
                    <p className="text-[10px] text-slate-300 leading-relaxed">{demo.explanation}</p>
                  </div>
                </div>
              </div>

              <button
                onClick={fetchDemo}
                className="w-full flex items-center justify-center gap-2 bg-blue-600/10 hover:bg-blue-600/20 border border-blue-500/20 text-blue-400 font-bold py-2.5 rounded-xl transition-all text-xs uppercase tracking-widest"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                Re-run Comparison with Live Data
              </button>
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
}
