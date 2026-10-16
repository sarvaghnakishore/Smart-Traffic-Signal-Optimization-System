"use client";

import React, { useEffect, useState, useCallback } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell,
  AreaChart, Area, Legend
} from "recharts";
import { TrendingUp, BarChart3, PieChart as PieIcon, Zap } from "lucide-react";
import axios from "axios";

const API = "http://localhost:8000";

const LANE_COLORS: Record<string, string> = {
  North: "#f43f5e",
  South: "#10b981",
  East:  "#f59e0b",
  West:  "#a855f7",
};

const TOOLTIP_STYLE = {
  contentStyle: {
    backgroundColor: "#070a1a",
    borderRadius: "12px",
    border: "1px solid rgba(255,255,255,0.05)",
    fontSize: "10px",
    fontWeight: "bold",
    color: "#f8fafc",
  },
};

interface AnalyticsChartsProps {
  historyData: any[];
}

export default function AnalyticsCharts({ historyData }: AnalyticsChartsProps) {
  const [chartData, setChartData] = useState<any[]>([]);
  const [signalData, setSignalData] = useState<any[]>([]);
  const [congestionData, setCongestionData] = useState<any[]>([]);
  const [summary, setSummary] = useState<any>(null);

  // Build traffic flow chart data from historyData prop
  useEffect(() => {
    if (!historyData || historyData.length === 0) return;
    const grouped: Record<string, any> = {};
    historyData.forEach((rec) => {
      const t = new Date(rec.timestamp).toLocaleTimeString([], {
        hour: "2-digit", minute: "2-digit", second: "2-digit",
      });
      if (!grouped[t]) grouped[t] = { time: t, North: 0, South: 0, East: 0, West: 0 };
      grouped[t][rec.lane_id] = rec.vehicle_count;
    });
    const formatted = Object.values(grouped).slice(-50);
    formatted.forEach((d: any) => {
      d.Total = (d.North || 0) + (d.South || 0) + (d.East || 0) + (d.West || 0);
    });
    setChartData(formatted);
  }, [historyData]);

  // Fetch analytics summary + signal history
  const fetchAnalytics = useCallback(async () => {
    try {
      const [sumRes, sigRes] = await Promise.all([
        axios.get(`${API}/analytics/summary`),
        axios.get(`${API}/analytics/signals`),
      ]);

      const sum = sumRes.data;
      setSummary(sum);

      // Congestion frequency pie chart
      const cf = sum.congestion_frequency || {};
      setCongestionData([
        { name: "LOW",    value: cf.LOW    || 0, color: "#10b981" },
        { name: "MEDIUM", value: cf.MEDIUM || 0, color: "#f59e0b" },
        { name: "HIGH",   value: cf.HIGH   || 0, color: "#f43f5e" },
      ]);

      // Signal wait time bar chart (last 7 records)
      const sigs = sigRes.data || [];
      const bars = sigs.slice(-7).map((r: any, i: number) => ({
        label: `T-${7 - i}`,
        wait: r.green_time_assigned || 0,
        signal_id: r.signal_id || "",
      }));
      setSignalData(bars.length > 0 ? bars : [
        { label: "Mon", wait: 28 },
        { label: "Tue", wait: 32 },
        { label: "Wed", wait: 24 },
        { label: "Thu", wait: 46 },
        { label: "Fri", wait: 38 },
        { label: "Sat", wait: 14 },
        { label: "Sun", wait: 10 },
      ]);
    } catch {
      // Fallback static signal data
      setSignalData([
        { label: "Mon", wait: 28 },
        { label: "Tue", wait: 32 },
        { label: "Wed", wait: 24 },
        { label: "Thu", wait: 46 },
        { label: "Fri", wait: 38 },
        { label: "Sat", wait: 14 },
        { label: "Sun", wait: 10 },
      ]);
    }
  }, []);

  useEffect(() => {
    fetchAnalytics();
    const interval = setInterval(fetchAnalytics, 10000);
    return () => clearInterval(interval);
  }, [fetchAnalytics]);

  const showEmpty =
    (!historyData || historyData.length === 0) &&
    chartData.length === 0;

  if (showEmpty) {
    return (
      <div className="bg-slate-900/40 backdrop-blur-xl rounded-[2rem] p-12 border border-white/5 flex flex-col items-center justify-center text-slate-500 shadow-2xl">
        <div className="w-20 h-20 rounded-[2rem] bg-slate-950 border border-white/5 flex items-center justify-center mb-6 shadow-inner">
          <BarChart3 className="w-10 h-10 opacity-20" />
        </div>
        <p className="text-sm font-bold uppercase tracking-[0.3em]">Historical Engine Standby</p>
        <p className="text-[10px] text-slate-600 mt-2">Run a detection cycle to populate charts</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">

      {/* ── Chart 1: Traffic Flow (Area) ──────────────────────────── */}
      <div className="xl:col-span-2 navy-card min-h-[380px]">
        <div className="navy-card-header">
          <div className="flex items-center gap-3">
            <TrendingUp className="w-4 h-4 text-blue-400" />
            <h3 className="text-[10px] text-slate-400 font-black uppercase tracking-[0.2em] italic">
              Traffic Flow Analysis — All Lanes
            </h3>
          </div>
        </div>
        <div className="navy-card-body h-[280px] w-full">
          <ResponsiveContainer width="100%" height="100%" minWidth={10} minHeight={10}>
            <AreaChart data={chartData} margin={{ top: 10, right: 10, bottom: 10, left: 10 }}>
              <defs>
                {Object.entries(LANE_COLORS).map(([lane, color]) => (
                  <linearGradient key={lane} id={`grad-${lane}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor={color} stopOpacity={0.15} />
                    <stop offset="95%" stopColor={color} stopOpacity={0} />
                  </linearGradient>
                ))}
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#ffffff04" vertical={false} />
              <XAxis
                dataKey="time"
                stroke="#475569"
                fontSize={8}
                tickMargin={8}
                axisLine={false}
                tickLine={false}
                interval={Math.max(1, Math.floor(chartData.length / 6))}
              />
              <YAxis stroke="#475569" fontSize={8} axisLine={false} tickLine={false} width={25} />
              <Tooltip {...TOOLTIP_STYLE} />
              {Object.entries(LANE_COLORS).map(([lane, color]) => (
                <Area
                  key={lane}
                  type="monotone"
                  dataKey={lane}
                  stroke={color}
                  strokeWidth={2}
                  fillOpacity={1}
                  fill={`url(#grad-${lane})`}
                />
              ))}
            </AreaChart>
          </ResponsiveContainer>
          {/* Legend */}
          <div className="flex justify-center gap-6 mt-3">
            {Object.entries(LANE_COLORS).map(([lane, color]) => (
              <div key={lane} className="flex items-center gap-1.5">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: color }} />
                <span className="text-[8px] text-slate-500 font-bold uppercase tracking-widest">{lane}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── Chart 2: Congestion Frequency (Pie) ──────────────────────── */}
      <div className="navy-card min-h-[380px]">
        <div className="navy-card-header">
          <div className="flex items-center gap-3">
            <PieIcon className="w-4 h-4 text-amber-400" />
            <h3 className="text-[10px] text-slate-400 font-black uppercase tracking-[0.2em] italic">
              Congestion Frequency
            </h3>
          </div>
        </div>
        <div className="navy-card-body h-[220px] flex flex-col items-center justify-center">
          {congestionData.some((d) => d.value > 0) ? (
            <>
              <ResponsiveContainer width="100%" height={160} minWidth={10} minHeight={10}>
                <PieChart>
                  <Pie
                    data={congestionData}
                    cx="50%"
                    cy="50%"
                    innerRadius={45}
                    outerRadius={70}
                    paddingAngle={3}
                    dataKey="value"
                  >
                    {congestionData.map((entry, index) => (
                      <Cell key={index} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={TOOLTIP_STYLE.contentStyle}
                    formatter={(value: any, name: any) => [`${value} records`, name]}
                  />
                </PieChart>
              </ResponsiveContainer>
              <div className="flex justify-center gap-4 mt-2">
                {congestionData.map((d) => (
                  <div key={d.name} className="flex flex-col items-center gap-0.5">
                    <div className="w-2 h-2 rounded-full" style={{ backgroundColor: d.color }} />
                    <span className="text-[7px] text-slate-500 font-black uppercase">{d.name}</span>
                    <span className="text-[9px] font-black text-white">{d.value}</span>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <div className="text-center text-slate-600 text-xs font-bold uppercase tracking-widest">
              Awaiting data...
            </div>
          )}
        </div>

        {/* Summary Stats */}
        {summary && (
          <div className="px-4 pb-4 grid grid-cols-2 gap-2">
            <div className="bg-navy-950/60 p-2.5 rounded-xl border border-white/5 text-center">
              <span className="block text-[8px] text-slate-500 uppercase font-bold">Avg Green</span>
              <span className="text-sm font-black text-emerald-400">{summary.average_green_time_seconds}s</span>
            </div>
            <div className="bg-navy-950/60 p-2.5 rounded-xl border border-white/5 text-center">
              <span className="block text-[8px] text-slate-500 uppercase font-bold">Detections</span>
              <span className="text-sm font-black text-blue-400">{summary.total_detections}</span>
            </div>
          </div>
        )}
      </div>

      {/* ── Chart 3: Signal Timing History (Bar) ─────────────────────── */}
      <div className="xl:col-span-3 navy-card min-h-[320px]">
        <div className="navy-card-header">
          <div className="flex items-center gap-3">
            <BarChart3 className="w-4 h-4 text-indigo-400" />
            <h3 className="text-[10px] text-slate-400 font-black uppercase tracking-[0.2em] italic">
              Signal Green Time History
            </h3>
          </div>
          {summary && (
            <div className="flex items-center gap-2">
              <Zap className="w-3 h-3 text-emerald-500" />
              <span className="text-[9px] text-emerald-400 font-bold">
                Avg: {summary.average_green_time_seconds}s
              </span>
            </div>
          )}
        </div>
        <div className="navy-card-body h-[220px] w-full">
          <ResponsiveContainer width="100%" height="100%" minWidth={10} minHeight={10}>
            <BarChart data={signalData} margin={{ top: 10, right: 20, bottom: 10, left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#ffffff04" vertical={false} />
              <XAxis
                dataKey="label"
                stroke="#475569"
                fontSize={9}
                tickMargin={8}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                stroke="#475569"
                fontSize={9}
                axisLine={false}
                tickLine={false}
                unit="s"
                width={30}
              />
              <Tooltip {...TOOLTIP_STYLE} cursor={{ fill: "rgba(59,130,246,0.05)" }} />
              <Bar dataKey="wait" fill="#3b82f6" radius={[6, 6, 0, 0]} barSize={36} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

    </div>
  );
}
