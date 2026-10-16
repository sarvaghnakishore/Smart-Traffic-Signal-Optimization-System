"use client";

import { useState, useEffect, useCallback } from "react";
import axios from "axios";
import {
  Activity, Radio, Bell, LogOut, MapPin, Navigation,
  Timer, Settings, LayoutDashboard, Zap, Shield,
  ShieldAlert, Play, RefreshCw, Database, Cpu, Clock
} from "lucide-react";
import StatusCard       from "../../components/StatusCard";
import ManualControls   from "../../components/ManualControls";
import AlertsSection    from "../../components/AlertsSection";
import AnalyticsCharts  from "../../components/AnalyticsCharts";
import DashboardGrid    from "../../components/DashboardGrid";
import DecisionPanel    from "../../components/DecisionPanel";
import SignalDisplay    from "../../components/SignalDisplay";
import JunctionStatus   from "../../components/JunctionStatus";
import DemoMode         from "../../components/DemoMode";

const API = "http://localhost:8000";

const DENSITY_COLORS: Record<string, string> = {
  LOW:    "text-emerald-400",
  MEDIUM: "text-amber-400",
  HIGH:   "text-rose-400",
};

const DENSITY_BG: Record<string, string> = {
  LOW:    "bg-emerald-500/10 border-emerald-500/20",
  MEDIUM: "bg-amber-500/10 border-amber-500/20",
  HIGH:   "bg-rose-500/10 border-rose-500/20",
};

export default function Dashboard() {
  const [systemState, setSystemState]       = useState<any>(null);
  const [analyticsData, setAnalyticsData]   = useState<any[]>([]);
  const [isLive, setIsLive]                 = useState(false);
  const [currentTime, setCurrentTime]       = useState(new Date());
  const [isDemoOpen, setIsDemoOpen]         = useState(false);
  const [emergencyActive, setEmergencyActive] = useState(false);
  const [emergencyLoading, setEmergencyLoading] = useState(false);
  const [mounted, setMounted]               = useState(false);
  const [activeIntersection, setActiveIntersection] = useState("Intersection A");

  // Clock tick
  useEffect(() => {
    setMounted(true);
    const t = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  // Main data fetch (Sequence Diagram: Dashboard requests traffic data)
  const fetchData = useCallback(async () => {
    try {
      const [stateRes, analyticsRes] = await Promise.all([
        axios.get(`${API}/traffic/state/${encodeURIComponent(activeIntersection)}`),
        axios.get(`${API}/analytics/`),
      ]);

      if (stateRes.data) {
        setSystemState(stateRes.data);
        setIsLive(true);
        // Sync emergency state from controller
        setEmergencyActive(stateRes.data?.phases &&
          Object.values(stateRes.data.phases as Record<string, string>)
            .every((p) => p === "RED") &&
          stateRes.data.reasoning?.includes("EMERGENCY"));
      }
      if (analyticsRes.data) setAnalyticsData(analyticsRes.data);
    } catch (err) {
      console.error("Dashboard Sync Error:", err);
      setIsLive(false);
    }
  }, [activeIntersection, API]);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2500);
    return () => clearInterval(interval);
  }, [fetchData]);

  // Emergency override handler
  const handleEmergency = async () => {
    setEmergencyLoading(true);
    try {
      await axios.post(`${API}/traffic/signal/emergency/${activeIntersection}`);
      setEmergencyActive(true);
      await fetchData();
    } catch {
      // handle silently
    } finally {
      setEmergencyLoading(false);
    }
  };

  // Derived state
  const activeLane: string                  = systemState?.active_lane || "—";
  const phases: Record<string, string>      = systemState?.phases      || {};
  const lanes:  Record<string, any>         = systemState?.lanes       || {};
  const timings: Record<string, number>     = systemState?.timings     || {};
  const reasoning: string                   = systemState?.reasoning   || "";
  const timestamp: string                   = systemState?.timestamp   || "";
  const cycleCount: number                  = systemState?.cycle       || 0;
  const uptime: number                      = systemState?.uptime_seconds || 0;
  const remainingTime: number               = systemState?.remaining_time || 0;
  const isOverride: boolean                 = systemState?.is_override || false;

  // Junction data (for JunctionStatus component)
  const junctionData = Object.keys(lanes).length > 0
    ? Object.fromEntries(
        Object.entries(lanes).map(([lane, data]: [string, any]) => [
          lane,
          {
            vehicles: data.count || 0,
            density:  data.density || "LOW",
            isActive: lane === activeLane,
            signal: {
              green:  lane === activeLane ? (remainingTime > 0 ? remainingTime : timings[lane] || 0) : 0,
              yellow: 3,
              red:    lane !== activeLane ? 30 : 0,
            },
          },
        ])
      )
    : null;

  const totalVehicles = Object.values(lanes).reduce(
    (s: number, d: any) => s + (d?.count || 0), 0
  );

  const uptimeStr = uptime > 0
    ? `${Math.floor(uptime / 60)}m ${uptime % 60}s`
    : "Starting...";

  return (
    <div className="relative min-h-screen bg-navy-950 text-slate-200 p-4 md:p-5 font-sans">
      <div className="max-w-[1900px] mx-auto space-y-5">

        {/* ── HEADER ─────────────────────────────────────────────────── */}
        <header className="flex items-center justify-between py-2 px-4">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center shadow-lg shadow-blue-500/10">
              <LayoutDashboard className="w-5 h-5 text-blue-400" />
            </div>
            <div>
              <h1 className="text-xl font-black text-white tracking-tight uppercase italic opacity-90">
                Smart Traffic Command Center
              </h1>
              <p className="text-[10px] text-slate-500 uppercase tracking-widest">
                AI Signal Optimization — v3.0 · YOLOv8 Pipeline Active
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3 mt-4 lg:mt-0">
            {/* Intersection Selector */}
            <div className="flex items-center gap-1 bg-navy-900 border border-white/5 rounded-xl p-1 mr-2 hidden md:flex">
              {["Intersection A", "Intersection B", "Intersection C"].map((int) => (
                <button
                  key={int}
                  onClick={() => setActiveIntersection(int)}
                  className={`text-[9px] font-black uppercase tracking-widest px-3 py-1.5 rounded-lg transition-all ${
                    activeIntersection === int
                      ? "bg-blue-600/30 text-blue-400 border border-blue-500/30 shadow-lg"
                      : "text-slate-500 hover:text-slate-300 hover:bg-white/5 border border-transparent"
                  }`}
                >
                  {int.replace("Intersection ", "Int ")}
                </button>
              ))}
            </div>

            {/* System Live Indicator */}
            <div className="flex items-center gap-2 px-3 py-1.5 bg-navy-900 border border-white/5 rounded-full">
              <div className={`w-2 h-2 rounded-full ${isLive ? "bg-emerald-500 animate-pulse" : "bg-slate-600"}`} />
              <span className="text-[10px] font-black uppercase tracking-widest text-slate-400">
                {isLive ? "System Live" : "Standby"}
              </span>
            </div>

            {/* Clock */}
            <span className="text-slate-500 font-mono text-xs hidden md:block min-w-[80px] text-right">
              {mounted ? currentTime.toLocaleTimeString() : "..."}
            </span>

            {/* Demo Mode Button */}
            <button
              onClick={() => setIsDemoOpen(true)}
              className="flex items-center gap-2 bg-blue-600/10 hover:bg-blue-600/20 border border-blue-500/20 hover:border-blue-500/40 py-1.5 px-4 rounded-lg transition-all group text-blue-400"
            >
              <Play className="w-3.5 h-3.5 group-hover:text-blue-300" />
              <span className="text-[11px] font-bold uppercase tracking-wider">Demo</span>
            </button>

            {/* Emergency Override */}
            <button
              onClick={handleEmergency}
              disabled={emergencyLoading}
              className={`flex items-center gap-2 border py-1.5 px-4 rounded-lg transition-all group ${
                emergencyActive
                  ? "bg-rose-900/40 border-rose-500/50 text-rose-400 animate-pulse"
                  : "bg-navy-800/50 hover:bg-rose-900/20 border-white/5 hover:border-rose-500/30 text-slate-400 hover:text-rose-400"
              }`}
            >
              {emergencyLoading ? (
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
              ) : (
                <ShieldAlert className="w-3.5 h-3.5" />
              )}
              <span className="text-[11px] font-bold uppercase tracking-wider">
                {emergencyActive ? "EMERGENCY ON" : "Emergency"}
              </span>
            </button>
          </div>
        </header>

        {/* ── ROW 1: STATUS CARDS ──────────────────────────────────────── */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatusCard
            title="Active Intersection"
            value={activeIntersection}
            subValue="Downtown Control Zone"
            icon={<MapPin className="w-4 h-4" />}
          />
          <StatusCard
            title="Priority Lane"
            value={activeLane}
            active={isLive}
            subValue={`${timings[activeLane] || "--"}s green time`}
            icon={<Navigation className="w-4 h-4" />}
          />
          <StatusCard
            title="Total Vehicles"
            value={totalVehicles > 0 ? totalVehicles.toString() : "--"}
            subValue={`Cycle #${cycleCount} · ${cycleCount > 0 ? "Active" : "Idle"}`}
            icon={<Activity className="w-4 h-4" />}
            active={isLive}
          />
          <StatusCard
            title="System Uptime"
            value={isLive ? "ONLINE" : "OFFLINE"}
            active={isLive}
            subValue={uptimeStr}
            icon={<Cpu className="w-4 h-4" />}
          />
        </div>

        {/* ── ROW 2: CAMERAS + SIGNALS + DECISION ─────────────────────── */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">

          {/* 4-Camera Grid (7 cols) */}
          <div className="lg:col-span-7 navy-card p-4">
            <div className="flex items-center gap-2 mb-4">
              <Radio className="w-4 h-4 text-rose-500 animate-pulse" />
              <span className="text-[10px] font-black uppercase tracking-widest text-slate-400">
                Live 4-Way Intersection Feed
              </span>
              <span className="ml-auto text-[8px] text-slate-600 font-mono">
                MJPEG · YOLOv8 Annotated
              </span>
            </div>
            <DashboardGrid
              intersectionId={activeIntersection}
              activeLane={activeLane}
              phases={phases}
              lanes={lanes}
            />
          </div>

          {/* Signal Status + Density (2 cols) */}
          <div className="lg:col-span-2 flex flex-col gap-4">

            {/* Animated Signal Lights */}
            <div className="navy-card p-4 flex-1">
              <h3 className="text-[9px] text-slate-500 uppercase font-black tracking-widest mb-4">
                Signal Status
              </h3>
              <div className="grid grid-cols-2 gap-4">
                {["North", "South", "East", "West"].map((lane) => (
                  <SignalDisplay
                    key={lane}
                    lane={lane}
                    status={(phases[lane] as "RED" | "YELLOW" | "GREEN") || "RED"}
                    remainingTime={lane === activeLane ? remainingTime : 0}
                  />
                ))}
              </div>
            </div>

            {/* Per-Lane Density Pills */}
            <div className="navy-card p-4 space-y-2">
              <h3 className="text-[9px] text-slate-500 uppercase font-black tracking-widest mb-3">
                Lane Density
              </h3>
              {["North", "South", "East", "West"].map((lane) => {
                const d = lanes[lane]?.density || "N/A";
                return (
                  <div
                    key={lane}
                    className={`flex items-center justify-between px-3 py-2 rounded-lg border transition-all ${DENSITY_BG[d] || "bg-slate-800/30 border-white/5"}`}
                  >
                    <span className="text-[10px] text-slate-400 font-bold">{lane}</span>
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] font-bold text-slate-500 tabular-nums">
                        {lanes[lane]?.count ?? "--"} veh
                      </span>
                      <span className={`text-[9px] font-black uppercase ${DENSITY_COLORS[d] || "text-slate-500"}`}>
                        {d}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Manual Controls + Alerts (3 cols) */}
          <div className="lg:col-span-3 flex flex-col gap-4 lg:h-[580px]">
            <ManualControls 
              intersectionId={activeIntersection} 
              remainingTime={systemState?.remaining_time}
              isOverride={systemState?.is_override}
            />
            <div className="flex-1 overflow-hidden min-h-0">
              <AlertsSection intersectionId={activeIntersection} />
            </div>
          </div>
        </div>

        {/* ── ROW 3: JUNCTION STATUS ───────────────────────────────────── */}
        {junctionData && (
          <div>
            <JunctionStatus data={junctionData} />
          </div>
        )}

        {/* ── ROW 4: DECISION PANEL + ANALYTICS ──────────────────────── */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
          <div className="lg:col-span-3">
            <DecisionPanel reasoning={reasoning} timestamp={timestamp} />
          </div>
          <div className="lg:col-span-9">
            <AnalyticsCharts historyData={analyticsData} />
          </div>
        </div>

      </div>

      {/* Demo Mode Modal */}
      <DemoMode 
        isOpen={isDemoOpen} 
        onClose={() => setIsDemoOpen(false)} 
        intersectionId={activeIntersection} 
      />
    </div>
  );
}
