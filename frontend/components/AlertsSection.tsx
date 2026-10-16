"use client";

import React, { useEffect, useState, useRef, useCallback } from "react";
import axios from "axios";
import {
  AlertTriangle, Clock, ShieldAlert, ZapOff, Wifi,
  Info, CheckCircle2, RefreshCw
} from "lucide-react";

const API = "http://localhost:8000";

interface Alert {
  id?: number;
  type: "danger" | "warning" | "info";
  title: string;
  location: string;
  message?: string;
  timestamp: string;
}

const TYPE_STYLES: Record<string, string> = {
  danger:  "bg-rose-500/10 text-rose-400 border-rose-500/25",
  warning: "bg-amber-500/10 text-amber-400 border-amber-500/25",
  info:    "bg-blue-500/10 text-blue-400 border-blue-500/25",
};

const TYPE_ICONS: Record<string, React.ReactNode> = {
  danger:  <ShieldAlert className="w-4 h-4" />,
  warning: <AlertTriangle className="w-4 h-4" />,
  info:    <Info className="w-4 h-4" />,
};

function timeAgo(iso: string): string {
  const diff = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
  if (diff < 60)  return `${diff}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  return `${Math.floor(diff / 3600)}h ago`;
}

interface AlertsSectionProps {
  intersectionId: string;
}

const AlertsSection: React.FC<AlertsSectionProps> = ({ intersectionId }) => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [isLive, setIsLive] = useState(false);
  const [loading, setLoading] = useState(true);
  const seenIds = useRef<Set<number>>(new Set());
  const [newCount, setNewCount] = useState(0);

  const fetchAlerts = useCallback(async () => {
    try {
      const res = await axios.get(`${API}/traffic/alerts/${intersectionId}`);
      const incoming: Alert[] = res.data?.alerts || [];

      if (incoming.length > 0) {
        // Track new alerts
        const fresh = incoming.filter(
          (a) => a.id && !seenIds.current.has(a.id)
        );
        fresh.forEach((a) => a.id && seenIds.current.add(a.id));
        if (fresh.length > 0) setNewCount((p) => p + fresh.length);
        setAlerts(incoming);
        setIsLive(true);
      } else {
        // Fallback: pull from analytics alerts (DB-based)
        const res2 = await axios.get(`${API}/analytics/alerts`);
        const dbAlerts: Alert[] = (res2.data?.alerts || []).map(
          (a: any, i: number) => ({
            id: i,
            type: a.type || "info",
            title: a.title || "Event",
            location: a.location || "System",
            timestamp: a.timestamp || new Date().toISOString()
          })
        );
        setAlerts(dbAlerts);
        setIsLive(dbAlerts.length > 0);
      }
    } catch {
      setIsLive(false);
    } finally {
      setLoading(false);
    }
  }, [intersectionId]);

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000);
    return () => clearInterval(interval);
  }, []);

  // Fallback static alerts for demo when backend offline
  const displayAlerts: Alert[] = alerts.length > 0 ? alerts : [
    { type: "warning", title: "High Congestion", location: "North Lane",    timestamp: new Date(Date.now() - 120000).toISOString() },
    { type: "info",    title: "Signal Updated",  location: "East Lane",     timestamp: new Date(Date.now() - 300000).toISOString() },
    { type: "danger",  title: "Congestion Alert",location: "South Lane",    timestamp: new Date(Date.now() - 500000).toISOString() },
    { type: "info",    title: "Cycle Complete",   location: "Main Junction", timestamp: new Date(Date.now() - 900000).toISOString() },
  ];

  return (
    <div className="navy-card h-full flex flex-col">
      <div className="navy-card-header">
        <div className="flex items-center gap-2">
          <h2 className="text-xs font-black text-slate-400 uppercase tracking-[0.2em] italic">
            System Alerts
          </h2>
          {newCount > 0 && (
            <span className="bg-rose-500 text-white text-[8px] font-black px-1.5 py-0.5 rounded-full">
              {newCount}
            </span>
          )}
        </div>
        <div className="flex items-center gap-2">
          <div className={`w-1.5 h-1.5 rounded-full ${isLive ? "bg-emerald-500 animate-pulse" : "bg-slate-600"}`} />
          <span className="text-[9px] text-slate-500 font-bold uppercase">
            {isLive ? "Live" : "Cached"}
          </span>
        </div>
      </div>

      <div className="navy-card-body flex-1 overflow-y-auto space-y-2.5 pr-1 scrollbar-thin scrollbar-thumb-white/5 scrollbar-track-transparent">
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <RefreshCw className="w-5 h-5 text-blue-500 animate-spin" />
          </div>
        ) : (
          displayAlerts.map((alert, idx) => (
            <div
              key={alert.id !== undefined ? `${alert.id}-${idx}` : idx}
              className="group p-3 bg-navy-950/40 border border-white/5 rounded-xl flex gap-3 transition-all hover:bg-navy-950 hover:border-blue-500/20"
            >
              <div className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 border ${TYPE_STYLES[alert.type] || TYPE_STYLES.info} shadow-lg`}>
                {TYPE_ICONS[alert.type] || TYPE_ICONS.info}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between mb-0.5 gap-1">
                  <h3 className="text-[10px] font-black text-white uppercase tracking-wide truncate">
                    {alert.title}
                  </h3>
                  <span className="text-[8px] text-slate-500 font-bold uppercase shrink-0">
                    {timeAgo(alert.timestamp)}
                  </span>
                </div>
                <p className="text-[9px] text-slate-500 font-bold uppercase tracking-widest truncate">
                  {alert.location}
                </p>
                {alert.message && (
                  <p className="text-[9px] text-slate-600 mt-0.5 truncate">{alert.message}</p>
                )}
                <div className="flex gap-1 mt-1.5">
                  <div className={`h-0.5 w-6 rounded-full ${alert.type === "danger" ? "bg-rose-500" : alert.type === "warning" ? "bg-amber-500" : "bg-blue-500"}`} />
                  <div className="h-0.5 w-4 rounded-full bg-navy-800" />
                  <div className="h-0.5 w-3 rounded-full bg-navy-800" />
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      <div className="px-4 pb-3 pt-2 border-t border-white/5">
        <button
          onClick={() => { setNewCount(0); fetchAlerts(); }}
          className="w-full text-[9px] text-blue-500/60 hover:text-blue-400 font-bold uppercase tracking-widest transition-colors flex items-center justify-center gap-1.5"
        >
          <RefreshCw className="w-3 h-3" /> Refresh Alerts
        </button>
      </div>
    </div>
  );
};

export default AlertsSection;
