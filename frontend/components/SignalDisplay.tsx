"use client";

import React from "react";

interface SignalDisplayProps {
  lane: string;
  status: "RED" | "YELLOW" | "GREEN";
  remainingTime?: number;
}

export default function SignalDisplay({ lane, status, remainingTime }: SignalDisplayProps) {
  return (
    <div className="flex flex-col items-center gap-2">
      <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">{lane}</span>
      <div className="relative bg-navy-950 p-2 rounded-2xl border border-white/5 flex flex-col gap-2 shadow-inner">
        {/* Timer Overlay for Active Green */}
        {status === "GREEN" && (remainingTime ?? 0) > 0 && (
          <div className="absolute -right-2 top-0 bg-emerald-500 text-[9px] font-black text-white px-1.5 py-0.5 rounded shadow-lg shadow-emerald-500/40 tabular-nums animate-pulse">
            {remainingTime}s
          </div>
        )}
        {/* Red Light */}
        <div 
          className={`w-6 h-6 rounded-full transition-all duration-500 ${
            status === "RED" 
              ? "bg-rose-500 shadow-[0_0_15px_rgba(244,63,94,0.8)]" 
              : "bg-rose-950/30"
          }`}
        />
        {/* Yellow Light */}
        <div 
          className={`w-6 h-6 rounded-full transition-all duration-500 ${
            status === "YELLOW" 
              ? "bg-amber-500 shadow-[0_0_15px_rgba(245,158,11,0.8)]" 
              : "bg-amber-950/30"
          }`}
        />
        {/* Green Light */}
        <div 
          className={`w-6 h-6 rounded-full transition-all duration-500 ${
            status === "GREEN" 
              ? "bg-emerald-500 shadow-[0_0_15px_rgba(16,185,129,0.8)]" 
              : "bg-emerald-950/30"
          }`}
        />
      </div>
    </div>
  );
}
