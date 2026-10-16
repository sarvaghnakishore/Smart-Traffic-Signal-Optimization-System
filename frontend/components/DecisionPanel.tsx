"use client";

import React from "react";
import { Brain, Info } from "lucide-react";

interface DecisionPanelProps {
  reasoning: string;
  timestamp: string;
}

export default function DecisionPanel({ reasoning, timestamp }: DecisionPanelProps) {
  return (
    <div className="navy-card p-5 h-full flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Brain className="w-5 h-5 text-blue-400" />
          <h3 className="text-sm font-bold text-slate-200 uppercase tracking-widest">Decision Intelligence</h3>
        </div>
        <span className="text-[10px] text-slate-500 font-mono">
            {timestamp ? new Date(timestamp).toLocaleTimeString() : 'Awaiting Data...'}
        </span>
      </div>

      <div className="flex-1 bg-navy-950/50 rounded-xl border border-white/5 p-4 relative overflow-hidden group">
        <div className="absolute top-0 left-0 w-1 h-full bg-blue-500/40" />
        <div className="flex gap-3">
          <Info className="w-4 h-4 text-blue-500 mt-1 flex-shrink-0" />
          <p className="text-sm text-slate-300 leading-relaxed italic">
            {reasoning || "System initializing. Analyzing intersection traffic patterns for optimal throughput..."}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="bg-navy-900/40 p-3 rounded-lg border border-white/5">
            <span className="block text-[8px] text-slate-500 uppercase font-black mb-1">Optimization Mode</span>
            <span className="text-[10px] text-emerald-400 font-bold uppercase tracking-wider">Dynamic Throughput</span>
        </div>
        <div className="bg-navy-900/40 p-3 rounded-lg border border-white/5">
            <span className="block text-[8px] text-slate-500 uppercase font-black mb-1">Starvation Logic</span>
            <span className="text-[10px] text-blue-400 font-bold uppercase tracking-wider">Active Protection</span>
        </div>
      </div>
    </div>
  );
}
