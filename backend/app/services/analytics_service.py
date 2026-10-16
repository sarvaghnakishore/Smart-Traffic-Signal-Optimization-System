"""
Analytics Service — Aggregates historical data from MongoDB collections.
Maps to: Architecture → Presentation Layer (analytics feed)

Provides:
  - Per-lane vehicle count trends
  - Average green time history
  - Congestion frequency by lane
  - System event logs
"""

from ..database import (
    traffic_density_col,
    signal_timing_history_col,
    traffic_signal_col,
    system_logs_col,
    vehicle_detection_col
)
import datetime


def get_density_history(limit: int = 400) -> list[dict]:
    """
    Fetch historical traffic density records.
    Used by: Dashboard → Traffic Flow Analysis chart
    """
    data = list(
        traffic_density_col.find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(limit)
    )
    data.reverse()
    return data


def get_signal_history(limit: int = 100) -> list[dict]:
    """
    Fetch signal timing history.
    Used by: Dashboard → Average Wait Times chart
    """
    data = list(
        signal_timing_history_col.find({}, {"_id": 0})
        .sort("updated_time", -1)
        .limit(limit)
    )
    data.reverse()
    return data


def get_summary_stats() -> dict:
    """
    Aggregate summary statistics across all collections.
    Returns: avg green time, total detections, congestion counts, recent logs.
    """
    # Traffic density summary
    density_records = list(traffic_density_col.find({}, {"_id": 0}))
    total_records = len(density_records)

    congestion_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
    lane_totals = {"North": 0, "South": 0, "East": 0, "West": 0}
    lane_record_count = {"North": 0, "South": 0, "East": 0, "West": 0}

    for rec in density_records:
        lvl = rec.get("congestion_level", "LOW")
        lane = rec.get("lane_id", "")
        count = rec.get("vehicle_count", 0)
        if lvl in congestion_counts:
            congestion_counts[lvl] += 1
        if lane in lane_totals:
            lane_totals[lane] += count
            lane_record_count[lane] += 1

    lane_averages = {
        lane: round(lane_totals[lane] / max(lane_record_count[lane], 1), 1)
        for lane in lane_totals
    }

    # Signal timing summary
    sig_records = list(signal_timing_history_col.find({}, {"_id": 0}))
    green_times = [r.get("green_time_assigned", 0) for r in sig_records]
    avg_green = round(sum(green_times) / max(len(green_times), 1), 1)

    # Vehicle detection summary
    total_detections = len(list(vehicle_detection_col.find({}, {"_id": 0})))

    # Recent system logs
    recent_logs = list(
        system_logs_col.find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(20)
    )
    for log in recent_logs:
        if isinstance(log.get("timestamp"), datetime.datetime):
            log["timestamp"] = log["timestamp"].isoformat()

    return {
        "total_density_records": total_records,
        "total_detections": total_detections,
        "total_signal_updates": len(sig_records),
        "congestion_frequency": congestion_counts,
        "lane_averages": lane_averages,
        "average_green_time_seconds": avg_green,
        "recent_logs": recent_logs
    }


def get_recent_alerts(limit: int = 20) -> list[dict]:
    """
    Return recent system log events as alerts for the dashboard sidebar.
    """
    logs = list(
        system_logs_col.find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(limit)
    )
    alerts = []
    for log in logs:
        ts = log.get("timestamp")
        if isinstance(ts, datetime.datetime):
            ts = ts.isoformat()
        severity = log.get("severity", "info")
        alerts.append({
            "type": severity,
            "title": log.get("event_type", "EVENT"),
            "location": log.get("description", ""),
            "timestamp": ts
        })
    return alerts
