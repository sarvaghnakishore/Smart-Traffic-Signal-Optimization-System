"use client";

import React, { useState } from "react";
import axios from "axios";
import {
  Power, Zap, AlertCircle, ChevronUp, ChevronDown,
  ShieldAlert, RefreshCw, Siren
} from "lucide-react";

const API = "http://localhost:8000";
const LANES = ["North", "South", "East", "West"];

interface ManualControlsProps {
  intersectionId: string;
  remainingTime?: number;
  isOverride?: boolean;
}

const ManualControls: React.FC<ManualControlsProps> = ({ intersectionId, remainingTime, isOverride }) => {
  const [selectedLane, setSelectedLane] = useState<string>("North");
  const [timer, setTimer] = useState<number>(30);
  const [loading, setLoading] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("");
  const [statusType, setStatusType] = useState<"success" | "error" | "warning">("success");

  const showStatus = (msg: string, type: "success" | "error" | "warning" = "success") => {
    setStatus(msg);
    setStatusType(type);
    setTimeout(() => setStatus(""), 4000);
  };

  const handleActivateGreen = async () => {
    setLoading("green");
    try {
      const url = `${API}/traffic/signal/update/${encodeURIComponent(intersectionId)}`;
      await axios.post(url, {
        lane_id: selectedLane,
        green_time: timer
      });
      showStatus(`✅ ${selectedLane} lane → GREEN for ${timer}s`, "success");
    } catch {
      showStatus("❌ Failed to update signal", "error");
    } finally {
      setLoading(null);
    }
  };

  const handleForceRed = async () => {
    setLoading("red");
    try {
      // Force red on all lanes by setting minimum green on a dummy — or call emergency
      const url = `${API}/traffic/signal/emergency/${encodeURIComponent(intersectionId)}`;
      await axios.post(url);
      showStatus("🔴 All lanes forced RED", "warning");
    } catch {
      showStatus("❌ Failed to force red", "error");
    } finally {
      setLoading(null);
    }
  };

  const handleEmergency = async () => {
    setLoading("emergency");
    try {
      const url = `${API}/traffic/signal/emergency/${encodeURIComponent(intersectionId)}`;
      await axios.post(url);
      showStatus("🚨 EMERGENCY OVERRIDE — All signals RED", "warning");
    } catch {
      showStatus("❌ Emergency override failed", "error");
    } finally {
      setLoading(null);
    }
  };

  const handleApplyTimer = async () => {
    setLoading("apply");
    try {
      const url = `${API}/traffic/signal/update/${encodeURIComponent(intersectionId)}`;
      await axios.post(url, {
        lane_id: selectedLane,
        green_time: timer
      });
      showStatus(`✅ ${selectedLane}: ${timer}s green applied`, "success");
    } catch {
      showStatus("❌ Failed to apply timer", "error");
    } finally {
      setLoading(null);
    }
  };

  const handleDetect = async () => {
    setLoading("detect");
    try {
      const url = `${API}/traffic/detect/${encodeURIComponent(intersectionId)}`;
      await axios.post(url);
      showStatus("🔄 Detection cycle triggered", "success");
    } catch {
      showStatus("❌ Detection failed", "error");
    } finally {
      setLoading(null);
    }
  };

  const incrementTimer = () => setTimer((p) => Math.min(p + 5, 120));
  const decrementTimer = () => setTimer((p) => Math.max(p - 5, 10));

  const statusBg: Record<string, string> = {
    success: "bg-emerald-500/10 border-emerald-500/30 text-emerald-400",
    error:   "bg-rose-500/10 border-rose-500/30 text-rose-400",
    warning: "bg-amber-500/10 border-amber-500/30 text-amber-400",
  };

  return (
    <div className="navy-card h-full flex flex-col">
      <div className="navy-card-header">
        <h2 className="text-xs font-black text-slate-400 uppercase tracking-[0.2em] italic">
          Manual Controls
        </h2>
        <Power className="w-3.5 h-3.5 text-blue-500/50" />
      </div>

      <div className="navy-card-body flex-1 flex flex-col gap-3">

        {/* Lane Selector */}
        <div>
          <label className="text-[9px] text-slate-500 font-bold uppercase tracking-widest block mb-1.5">
            Target Lane
          </label>
          <div className="grid grid-cols-4 gap-1">
            {LANES.map((lane) => (
              <button
                key={lane}
                onClick={() => setSelectedLane(lane)}
                className={`py-1.5 text-[9px] font-black uppercase rounded-lg border transition-all tracking-wider ${
                  selectedLane === lane
                    ? "bg-blue-600/20 border-blue-500/50 text-blue-400"
                    : "bg-navy-950/40 border-white/5 text-slate-500 hover:border-white/10"
                }`}
              >
                {lane[0]}
              </button>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <button
          onClick={handleActivateGreen}
          disabled={loading === "green" || (isOverride && (remainingTime ?? 0) > 0)}
          className={`btn-traffic-green w-full flex items-center justify-center gap-2 disabled:opacity-80 transition-all duration-500 ${
            isOverride && (remainingTime ?? 0) > 0 ? "scale-[0.98] brightness-125 shadow-emerald-500/20" : ""
          }`}
        >
          {loading === "green" ? (
            <RefreshCw className="w-4 h-4 animate-spin" />
          ) : isOverride && (remainingTime ?? 0) > 0 ? (
            <div className="flex items-center gap-2">
              <RefreshCw className="w-3.5 h-3.5 animate-spin duration-[3000ms]" />
              <span className="font-mono text-base font-black tracking-tighter">
                00:{String(remainingTime).padStart(2, "0")}
              </span>
            </div>
          ) : (
            <Zap className="w-4 h-4" />
          )}
          {isOverride && (remainingTime ?? 0) > 0 ? "OVERRIDE ACTIVE" : "ACTIVATE GREEN"}
        </button>

        <button
          onClick={handleForceRed}
          disabled={loading === "red"}
          className="btn-traffic-red w-full flex items-center justify-center gap-2 disabled:opacity-50"
        >
          {loading === "red" ? (
            <RefreshCw className="w-4 h-4 animate-spin" />
          ) : (
            <AlertCircle className="w-4 h-4" />
          )}
          FORCE RED ALL
        </button>

        {/* Emergency Override — Highlighted */}
        <button
          onClick={handleEmergency}
          disabled={loading === "emergency"}
          className="w-full flex items-center justify-center gap-2 bg-rose-900/30 hover:bg-rose-900/50 border border-rose-500/40 hover:border-rose-500/70 text-rose-400 font-black py-3 px-4 rounded-xl transition-all text-xs uppercase tracking-widest shadow-lg shadow-rose-950/20"
        >
          {loading === "emergency" ? (
            <RefreshCw className="w-4 h-4 animate-spin" />
          ) : (
            <ShieldAlert className="w-4 h-4" />
          )}
          🚨 EMERGENCY OVERRIDE
        </button>

        {/* Detect Trigger */}
        <button
          onClick={handleDetect}
          disabled={loading === "detect"}
          className="w-full flex items-center justify-center gap-2 bg-navy-800/50 border border-white/5 hover:bg-navy-700/50 text-slate-300 font-bold py-2.5 px-4 rounded-xl transition-all text-[11px] uppercase tracking-widest"
        >
          {loading === "detect" ? (
            <RefreshCw className="w-3.5 h-3.5 animate-spin" />
          ) : (
            <RefreshCw className="w-3.5 h-3.5" />
          )}
          TRIGGER DETECTION
        </button>

        {/* Timer Override */}
        <div className="mt-auto space-y-2">
          <h3 className="text-[9px] text-slate-500 font-bold uppercase tracking-widest">
            Override Timer — {selectedLane} Lane
          </h3>
          <div className="flex items-center gap-2">
            <div className="flex-1 bg-navy-950/50 border border-white/5 rounded-xl px-3 py-2 flex items-center justify-between">
              <span className="text-base font-mono font-bold text-blue-400 tabular-nums">
                {String(Math.floor(timer / 60)).padStart(2, "0")}:
                {String(timer % 60).padStart(2, "0")}
              </span>
              <div className="flex flex-col gap-0.5">
                <button onClick={incrementTimer} className="text-slate-500 hover:text-blue-400 transition-colors">
                  <ChevronUp className="w-3 h-3" />
                </button>
                <button onClick={decrementTimer} className="text-slate-500 hover:text-blue-400 transition-colors">
                  <ChevronDown className="w-3 h-3" />
                </button>
              </div>
            </div>
            <button
              onClick={handleApplyTimer}
              disabled={loading === "apply"}
              className="btn-traffic-blue whitespace-nowrap px-5 py-2.5 text-xs disabled:opacity-50"
            >
              {loading === "apply" ? (
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
              ) : (
                "APPLY"
              )}
            </button>
          </div>
        </div>

        {/* Status Feedback */}
        {status && (
          <div className={`text-[10px] font-bold px-3 py-2 rounded-lg border text-center transition-all ${statusBg[statusType]}`}>
            {status}
          </div>
        )}
      </div>
    </div>
  );
};

export default ManualControls;
