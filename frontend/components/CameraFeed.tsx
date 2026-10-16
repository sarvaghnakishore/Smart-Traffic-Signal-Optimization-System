"use client";

import React from "react";
import { Camera, CheckCircle, MinusCircle, AlertTriangle } from "lucide-react";

export default function CameraFeed() {
  return (
    <div className="navy-card h-full flex flex-col group transition-all duration-700 hover:border-blue-500/20">
      
      {/* Dynamic Header Overlay */}
      <div className="navy-card-header bg-navy-950/40 border-b-0 absolute top-0 inset-x-0 z-20 p-6 flex items-center justify-between">
         <div className="flex items-center gap-3">
            <div className="w-2.5 h-2.5 rounded-full bg-rose-600 animate-pulse shadow-[0_0_8px_rgba(225,29,72,0.8)]" />
            <span className="text-[10px] font-black uppercase tracking-[0.3em] text-white">Live Intersection Camera</span>
         </div>
         <div className="flex gap-1.5 px-3 py-1 bg-navy-900 rounded-full border border-white/5">
            <span className="w-1.5 h-1.5 rounded-full bg-rose-500 shadow-[0_0_8px_rgba(244,63,94,0.4)]" />
            <span className="w-1.5 h-1.5 rounded-full bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.4)]" />
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.4)]" />
            <span className="w-1.5 h-1.5 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.4)]" />
         </div>
      </div>

      {/* Main Content Area */}
      <div className="relative flex-1 bg-black overflow-hidden rounded-t-[1.5rem]">
        
        {/* Digital Scanline Effect */}
        <div className="absolute inset-0 z-10 pointer-events-none opacity-[0.03] bg-[linear-gradient(to_bottom,transparent_50%,black_50%)] bg-[length:100%_4px]" />
        
        {/* Animated Scanning Line */}
        <div className="absolute inset-x-0 h-[100px] bg-gradient-to-b from-transparent via-blue-500/5 to-transparent z-10 animate-scanline pointer-events-none" />

        {/* The MJPEG Stream */}
        <img
          src="http://localhost:8000/traffic/video_feed"
          alt="Live Traffic Feed"
          className="w-full h-full object-cover brightness-[0.8] contrast-[1.1] transition-opacity duration-700 group-hover:brightness-100"
          onError={(e) => {
            (e.target as HTMLImageElement).style.display = 'none';
          }}
        />

        {/* Offline Placeholder */}
        <div className="absolute inset-0 flex flex-col items-center justify-center gap-4 pointer-events-none -z-10 bg-slate-950">
          <div className="w-16 h-16 rounded-3xl bg-slate-900 border border-white/5 flex items-center justify-center">
            <Camera className="w-8 h-8 text-slate-700" />
          </div>
          <p className="text-slate-600 text-[10px] font-black uppercase tracking-[0.3em] italic">Awaiting Signal Feed...</p>
        </div>
      </div>

      {/* Status Footer - Matching Reference Image */}
      <div className="navy-card-body bg-navy-950/60 p-5 flex flex-wrap items-center justify-around gap-6 rounded-b-[1.5rem] border-t border-white/5 font-sans">
         <div className="flex items-center gap-2.5">
            <CheckCircle className="w-4 h-4 text-emerald-500" />
            <span className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">North-South <span className="text-emerald-400">Green</span></span>
         </div>
         <div className="flex items-center gap-2.5">
            <MinusCircle className="w-4 h-4 text-rose-500" />
            <span className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">East-West <span className="text-rose-400">Red</span></span>
         </div>
         <div className="flex items-center gap-2.5">
            <AlertTriangle className="w-4 h-4 text-amber-500" />
            <span className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Pedestrian Signal: <span className="text-slate-500">OFF</span></span>
         </div>
      </div>
    </div>
  );
}
