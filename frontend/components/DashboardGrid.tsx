"use client";

import React, { useEffect, useState } from "react";

interface LaneStreamProps {
  intersectionId: string;
  laneId: string;
  isActive: boolean;
  phase: "RED" | "YELLOW" | "GREEN";
  vehicleCount?: number;
  density?: string;
  frameData?: string;
}

const PHASE_BORDER: Record<string, string> = {
  GREEN:  "border-emerald-500 shadow-[0_0_24px_rgba(16,185,129,0.35)]",
  RED:    "border-rose-500/40",
  YELLOW: "border-amber-500 shadow-[0_0_20px_rgba(245,158,11,0.3)]",
};

const PHASE_DOT: Record<string, string> = {
  GREEN:  "bg-emerald-500 animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.8)]",
  RED:    "bg-rose-500",
  YELLOW: "bg-amber-500 animate-pulse",
};

const DENSITY_COLOR: Record<string, string> = {
  LOW:    "text-emerald-400 bg-emerald-500/15 border-emerald-500/30",
  MEDIUM: "text-amber-400 bg-amber-500/15 border-amber-500/30",
  HIGH:   "text-rose-400 bg-rose-500/15 border-rose-500/30",
};

function LaneStream({ intersectionId, laneId, isActive, phase, vehicleCount, density, frameData }: LaneStreamProps) {
  return (
    <div className={`relative aspect-video bg-slate-950 rounded-xl overflow-hidden border-2 transition-all duration-700 ${PHASE_BORDER[phase] || "border-white/5"}`}>

      {/* Top Header Overlay */}
      <div className="absolute top-0 left-0 right-0 p-2.5 bg-gradient-to-b from-black/90 to-transparent z-10 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${PHASE_DOT[phase] || "bg-slate-600"}`} />
          <span className="text-[10px] font-black uppercase tracking-tighter text-white">
            {laneId}
          </span>
        </div>
        <span className="text-[8px] bg-black/60 text-slate-400 px-2 py-0.5 rounded-full border border-white/10 font-bold uppercase tracking-widest">
          LIVE
        </span>
      </div>

      {/* Live Stream */}
      {frameData ? (
        <img
          src={frameData}
          alt={`${laneId} Traffic Feed`}
          className="w-full h-full object-cover relative z-0"
        />
      ) : (
        <img
          src="https://placehold.co/640x480/020617/1e293b?text=FEED+OFFLINE"
          alt={`${laneId} Offline`}
          className="w-full h-full object-cover relative z-0"
        />
      )}

      {/* Bottom Stats Overlay */}
      <div className="absolute bottom-0 left-0 right-0 p-2.5 bg-gradient-to-t from-black/90 to-transparent z-10 flex items-end justify-between">
        {/* Vehicle Count */}
        {vehicleCount !== undefined && (
          <div className="flex items-center gap-1.5">
            <span className="text-white font-black text-sm tabular-nums">{vehicleCount}</span>
            <span className="text-[9px] text-slate-400 uppercase font-bold">veh</span>
          </div>
        )}

        {/* Density Badge */}
        {density && (
          <span className={`text-[8px] px-2 py-0.5 rounded-full border font-black uppercase tracking-widest ${DENSITY_COLOR[density] || "text-slate-400 bg-slate-800/50 border-white/5"}`}>
            {density}
          </span>
        )}
      </div>

      {/* Signal Phase Badge (top-right corner) */}
      <div className={`absolute top-2 right-2 z-20 flex items-center gap-1 px-2 py-1 rounded-lg border backdrop-blur-md ${
        phase === "GREEN"
          ? "bg-emerald-900/60 border-emerald-500/40 text-emerald-400"
          : phase === "YELLOW"
          ? "bg-amber-900/60 border-amber-500/40 text-amber-400"
          : "bg-rose-900/40 border-rose-500/30 text-rose-400"
      }`}>
        <div className={`w-2 h-2 rounded-full ${
          phase === "GREEN" ? "bg-emerald-400" : phase === "YELLOW" ? "bg-amber-400" : "bg-rose-400"
        }`} />
        <span className="text-[8px] font-black uppercase tracking-widest">{phase}</span>
      </div>

      {/* Active Lane Glow Border Pulse */}
      {isActive && (
        <div className="absolute inset-0 border-2 border-emerald-500/20 rounded-xl animate-pulse pointer-events-none" />
      )}
    </div>
  );
}

interface DashboardGridProps {
  intersectionId: string;
  activeLane: string;
  phases?: Record<string, string>;
  lanes?: Record<string, { count: number; density: string }>;
}

export default function DashboardGrid({ intersectionId, activeLane, phases = {}, lanes = {} }: DashboardGridProps) {
  const laneList = ["North", "South", "East", "West"];
  const [frames, setFrames] = useState<Record<string, string>>({});

  useEffect(() => {
    // Single Server-Sent Events (SSE) connection for all live video feeds!
    // Bypasses both Chrome's HTTP connection limits AND Next.js WebSocket proxy drops seamlessly.
    const sseUrl = `http://localhost:8000/traffic/stream_sse/${encodeURIComponent(intersectionId)}`;
    const eventSource = new EventSource(sseUrl);
    
    eventSource.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        setFrames(payload);
      } catch (err) {
        console.error("SSE parsing error:", err);
      }
    };

    return () => {
      eventSource.close();
    };
  }, [intersectionId]);

  return (
    <div className="grid grid-cols-2 gap-3 content-start">
      {laneList.map((lane) => (
        <LaneStream
          key={lane}
          intersectionId={intersectionId}
          laneId={lane}
          isActive={lane === activeLane}
          phase={(phases[lane] as "RED" | "YELLOW" | "GREEN") || "RED"}
          vehicleCount={lanes[lane]?.count}
          density={lanes[lane]?.density}
          frameData={frames[lane]}
        />
      ))}
    </div>
  );
}
