"use client";

import React from "react";
import { Car as CarIcon, Clock as ClockIcon, AlertTriangle as AlertIcon, ArrowRight as RightIcon, ArrowDown as DownIcon, ArrowUp as UpIcon, ArrowLeft as LeftIcon } from "lucide-react";

interface DirectionData {
  vehicles: number;
  density: string;
  isActive: boolean;
  signal: {
    green: number;
    yellow: number;
    red: number;
  };
}

interface JunctionProps {
  data: Record<string, DirectionData> | null;
}

const getDensityColor = (density: string) => {
  switch (density) {
    case "LOW":
      return "text-emerald-400 bg-emerald-500/10 border-emerald-500/20";
    case "MEDIUM":
      return "text-amber-400 bg-amber-500/10 border-amber-500/20";
    case "HIGH":
      return "text-rose-400 bg-rose-500/10 border-rose-500/20";
    default:
      return "text-slate-400 bg-slate-800/50 border-white/5";
  }
};

const getDirectionIcon = (dir: string) => {
  switch (dir) {
    case "North": return <UpIcon className="w-3.5 h-3.5" />;
    case "South": return <DownIcon className="w-3.5 h-3.5" />;
    case "East": return <RightIcon className="w-3.5 h-3.5" />;
    case "West": return <LeftIcon className="w-3.5 h-3.5" />;
    default: return null;
  }
};

export default function JunctionStatus({ data }: JunctionProps) {
  if (!data) {
    return (
      <div className="bg-slate-900/40 backdrop-blur-xl rounded-[2rem] p-8 border border-white/5 text-center h-full flex flex-col items-center justify-center shadow-2xl">
        <div className="w-16 h-16 rounded-3xl bg-slate-950 border border-white/10 flex items-center justify-center mb-6">
          <AlertIcon className="w-8 h-8 text-amber-500/50 animate-pulse" />
        </div>
        <p className="text-slate-500 font-bold uppercase tracking-widest text-xs">Synchronizing Core...</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900/40 backdrop-blur-xl rounded-[2.5rem] border border-white/5 p-8 h-full shadow-2xl flex flex-col">
      <div className="flex items-center justify-between mb-8">
        <h2 className="text-base font-black text-white uppercase italic tracking-tighter flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.8)]" />
          Neural Optimizer
        </h2>
        <div className="px-3 py-1 bg-blue-500/10 border border-blue-500/20 rounded-lg">
           <span className="text-[10px] text-blue-400 font-bold uppercase tracking-widest">Active_Junction</span>
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        {Object.entries(data).map(([direction, info]) => (
          <div key={direction} className={`relative group rounded-3xl p-5 border transition-all duration-500 ${info.isActive ? 'bg-slate-950 border-blue-500/30' : 'bg-slate-900/50 border-white/5 grayscale-[0.3]'}`}>
            
            {info.isActive && (
               <div className="absolute top-0 right-6 -translate-y-1/2 bg-blue-500 text-[8px] font-black text-white px-2 py-0.5 rounded shadow-lg shadow-blue-500/40 tracking-widest uppercase italic">GO_PRIORITY</div>
            )}

            <div className="flex justify-between items-start mb-4">
              <div className="p-2 rounded-xl bg-slate-900 border border-white/5">
                {getDirectionIcon(direction)}
              </div>
              <span className={`text-[9px] px-2 py-0.5 rounded-full border font-black tracking-widest uppercase transition-colors duration-500 ${getDensityColor(info.density)}`}>
                {info.density}
              </span>
            </div>
            
            <div className="space-y-4">
              <div className="flex flex-col">
                <span className="text-[9px] text-slate-500 font-bold uppercase tracking-widest mb-1 flex items-center gap-1.5">
                  <CarIcon className="w-3 h-3 text-slate-400" /> Sensors
                </span>
                <span className="text-lg font-black text-white tabular-nums">{info.vehicles} <span className="text-[10px] text-slate-500 italic">VHC</span></span>
              </div>
              
              <div className="flex flex-col">
                <span className="text-[9px] text-slate-500 font-bold uppercase tracking-widest mb-1 flex items-center gap-1.5">
                  <ClockIcon className="w-3 h-3 text-emerald-500" /> Sequence
                </span>
                <span className={`text-sm font-black italic tabular-nums ${info.isActive ? 'text-emerald-400' : 'text-slate-400'}`}>{info.signal.green}s <span className="text-[9px] uppercase tracking-tighter">left</span></span>
              </div>
              
              <div className="pt-4 border-t border-white/5">
                <div className="flex items-center gap-2 bg-slate-950 p-2 rounded-2xl border border-white/5">
                    <div className={`w-2.5 h-2.5 rounded-full transition-all duration-500 ${!info.isActive ? 'bg-rose-500 shadow-[0_0_12px_rgba(244,63,94,0.6)]' : 'bg-slate-800'}`} />
                    <div className={`w-2.5 h-2.5 rounded-full bg-slate-800`} />
                    <div className={`w-2.5 h-2.5 rounded-full transition-all duration-500 ${info.isActive ? 'bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.6)] animate-pulse' : 'bg-slate-800'}`} />
                    <div className="ml-auto w-10 h-1 bg-slate-900 rounded-full overflow-hidden">
                       <div className={`h-full bg-emerald-500 transition-all duration-500 ${info.isActive ? 'w-full' : 'w-0'}`} />
                    </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
