"""
Traffic System Pipeline — Orchestrates the full 12-step Activity Diagram flow.

Step 1:  Capture video from camera             (TrafficCamera)
Step 2:  Extract and preprocess frames          (VideoProcessor)
Step 3:  Detect vehicles using YOLO             (VehicleDetection)
Step 4:  Classify vehicle types                 (VehicleDetection)
Step 5:  Count vehicles per lane                (LaneAnalyzer)
Step 6:  Calculate traffic density              (DensityAnalyzer)
Step 7:  Check if congestion exists             (DensityAnalyzer)
Step 8:  Optimize signal timing                 (SignalOptimizer)
Step 9:  Send updated timing to controller      (TrafficSignalController)
Step 10: Update traffic signals                 (TrafficSignalController)
Step 11: Store data in database                 (MongoDB)
Step 12: Display results on dashboard           (MonitoringDashboard)
"""

import time
import datetime
from .classes import (
    SimulatedTrafficCamera, VideoProcessor, VehicleDetection,
    LaneAnalyzer, DensityAnalyzer, SignalOptimizer,
    TrafficSignalController, MonitoringDashboard
)
from ..database import (
    vehicle_detection_col, traffic_density_col, traffic_signal_col,
    signal_timing_history_col, system_logs_col
)


class TrafficSystemPipeline:
    """
    Orchestrates all pipeline components in strict Activity Diagram order.
    Follows the Sequence Diagram: Dashboard → Backend → Cameras →
    Detection → Lane/Density → Optimizer → Controller → DB → Dashboard.
    """

    LANES = ["North", "South", "East", "West"]

    def __init__(self, intersection_id: str = "MAIN_JUNC"):
        self.intersection_id = intersection_id
        # Initialize all pipeline components (Class Diagram)
        self.cameras = {
            lane: SimulatedTrafficCamera(intersection_id, lane)
            for lane in self.LANES
        }
        self.processor  = VideoProcessor()
        self.detector   = VehicleDetection()
        self.lane_analyzer    = LaneAnalyzer()
        self.density_analyzer = DensityAnalyzer()
        self.optimizer  = SignalOptimizer()
        self.controller = TrafficSignalController()
        self.dashboard  = MonitoringDashboard()

        # Shared in-memory state (returned on GET /traffic/state)
        self.latest_state: dict = {}
        self.latest_frames: dict = {}
        self._cycle_count: int = 0
        self._start_time: datetime.datetime = datetime.datetime.utcnow()
        import threading
        self._lock = threading.Lock()

    # ─────────────────────────────────────────────────────────────────────────
    # MAIN PIPELINE CYCLE
    # ─────────────────────────────────────────────────────────────────────────

    def run_cycle(self) -> tuple[dict, dict]:
        """
        Execute one full 12-step Activity Diagram cycle.
        Optimized for Batch Inference and Signal-Driven Video.
        """
        self._cycle_count += 1
        cycle_data: dict = {}
        lane_counts: dict = {}
        raw_frames: dict = {}
        
        # Get Current Signal State for Overlays
        current_phases = self.controller.current_phases
        remaining_time = self.controller.get_remaining_time()

        # ── Step 1: Capture video from all cameras (Batch Capture) ──────────
        for lane_id in self.LANES:
            camera = self.cameras[lane_id]
            is_green = current_phases.get(lane_id) == "GREEN"
            
            # Capture frame with signal-aware freeze logic and overlays
            raw_frames[lane_id] = camera.capture_frame(
                is_green=is_green,
                phase=current_phases.get(lane_id, "RED"),
                countdown=remaining_time,
                label=lane_id
            )

        # ── Step 2-4: Batch Discovery & Detection ──────────────────────────
        # Perform Batch Inference for all 4 lanes in ONE call
        all_detections, annotated_frames = self.detector.detect_batch(raw_frames)

        # ── Step 5-7: Lane Analysis & Density ──────────────────────────────
        for lane_id in self.LANES:
            detections = all_detections[lane_id]
            
            # Analyze lane counts
            lane_result = self.lane_analyzer.analyze(detections, lane_id)
            count = lane_result["total_count"]
            lane_counts[lane_id] = count

            # Calculate density
            density_level = self.density_analyzer.get_density_level(count)
            has_congestion = self.density_analyzer.has_congestion(density_level)
            
            if has_congestion:
                self.dashboard.add_alert(
                    alert_type="High Congestion",
                    lane_id=lane_id,
                    message=f"{lane_id} lane has {count} vehicles (HIGH density)",
                    severity="danger"
                )
                self._store_log("CONGESTION_ALERT",
                                f"{lane_id} lane: {count} vehicles — HIGH density", "danger")

            # Store detection & density data
            self._store_detection_data(lane_id, detections, count, density_level)

            cycle_data[lane_id] = {
                "count": count,
                "density": density_level,
                "congestion": has_congestion,
                "type_breakdown": lane_result["type_breakdown"]
            }

        if not lane_counts:
            self.latest_frames = annotated_frames
            return self.latest_state, annotated_frames

        # ── Step 8: Optimize signal timing ─────────────────────────────────
        # Check for manual/emergency overrides first.
        # If an override is active, we skip the optimization logic.
        if self.controller.is_override_active():
            phases = self.controller.current_phases
            timings = self.controller.timings
            priority_lane = self.controller.override_lane or self.LANES[0]
            selection_reason = "MANUAL_OVERRIDE_ACTIVE"
            optimized_green = timings.get(priority_lane, 0)
            reasoning = (
                f"[{self.intersection_id}] ⚠️ MANUAL OVERRIDE ACTIVE. "
                f"AI optimization suspended for {self.controller.get_remaining_time()}s."
            )
        elif self.controller.is_cycle_active():
            # CYCLE IN PROGRESS: Maintain previous decision but keep monitoring
            phases = self.controller.current_phases
            timings = self.controller.timings
            priority_lane = next((l for l, p in phases.items() if p == "GREEN"), self.LANES[0])
            selection_reason = "CYCLE_IN_PROGRESS"
            optimized_green = timings.get(priority_lane, 0)
            reasoning = (
                f"[{self.intersection_id}] AI COMMITTED to {priority_lane} lane. "
                f"Phase completes in {self.controller.get_remaining_time()}s. "
                f"Monitoring other lanes..."
            )
        else:
            # CYCLE COMPLETE: Time to switch or renew
            # Identify which lane was just active to ensure we switch (Congestion-Based Switching)
            current_active_lane = next((l for l, p in self.controller.current_phases.items() if p == "GREEN"), None)
            
            priority_lane, selection_reason = self.optimizer.select_priority_lane(lane_counts, current_active_lane)
            all_timings = self.optimizer.get_all_timings(lane_counts, priority_lane)
            optimized_green = all_timings[priority_lane]

            # ── Steps 9 & 10: Send timing to controller, update signals ────────
            phases, timings = self.controller.update_signals(priority_lane, optimized_green)

            # Build AI reasoning string for the NEW cycle
            count_val = lane_counts[priority_lane]
            density_val = cycle_data[priority_lane]["density"]
            if "anti_starvation" in selection_reason:
                reasoning = (
                    f"[{self.intersection_id}] Anti-starvation triggered for {priority_lane} lane "
                    f"after waiting {self.optimizer._starvation_counters.get(priority_lane, 0)} cycles. "
                    f"Green set to {optimized_green}s."
                )
            else:
                reasoning = (
                    f"[{self.intersection_id}] Switching to {priority_lane} lane due to "
                    f"{selection_reason.replace('_', ' ')} of {count_val} vehicles. "
                    f"Phase locked for {optimized_green}s."
                )

        # ── Step 11 (Part 2): Store signal decisions ───────────────────────
        self._store_signal_data(priority_lane, optimized_green, phases)

        # ── Step 12: Compose dashboard state ───────────────────────────────
        timestamp = datetime.datetime.utcnow().isoformat()
        with self._lock:
            self.latest_state = self.dashboard.compose_state(
                lane_data=cycle_data,
                priority_lane=priority_lane,
                phases=phases,
                timings=timings,
                reasoning=reasoning,
                selection_reason=selection_reason,
                timestamp=timestamp
            )
            self.latest_state["remaining_time"] = self.controller.get_remaining_time()
            self.latest_state["is_override"] = self.controller.is_override_active()
            self.latest_state["cycle"] = self._cycle_count
            self.latest_state["uptime_seconds"] = (
                datetime.datetime.utcnow() - self._start_time
            ).seconds

            self.latest_frames = annotated_frames
        return self.latest_state, annotated_frames

    # ─────────────────────────────────────────────────────────────────────────
    # EMERGENCY OVERRIDE
    # ─────────────────────────────────────────────────────────────────────────

    def emergency_override(self) -> dict:
        """Set all signals to RED immediately and log the event."""
        result = self.controller.emergency_override()
        alert = self.dashboard.add_alert(
            alert_type="Emergency Override",
            lane_id="ALL",
            message="All signals set to RED by emergency command",
            severity="danger"
        )
        self._store_log("EMERGENCY_OVERRIDE",
                        "All signals forced RED via emergency override", "danger")
        self.latest_state["phases"] = self.controller.current_phases
        self.latest_state["timings"] = self.controller.timings
        self.latest_state["reasoning"] = "⚠️ EMERGENCY OVERRIDE ACTIVE — All signals set to RED."
        return result

    def manual_override(self, lane_id: str, green_time: int) -> dict:
        """Manual override for a specific lane."""
        phases, timings = self.controller.manual_override(lane_id, green_time)
        self._store_log("MANUAL_OVERRIDE",
                        f"Manual override: {lane_id} set to GREEN for {green_time}s", "info")
        alert = self.dashboard.add_alert(
            alert_type="Manual Override",
            lane_id=lane_id,
            message=f"{lane_id} lane manually set to GREEN for {green_time}s",
            severity="info"
        )
        self.latest_state["phases"] = phases
        self.latest_state["timings"] = timings
        self.latest_state["reasoning"] = (
            f"Manual override: {lane_id} set to GREEN for {green_time}s."
        )
        return {"message": "Signal updated", "phases": phases, "timings": timings}

    # ─────────────────────────────────────────────────────────────────────────
    # DEMO MODE
    # ─────────────────────────────────────────────────────────────────────────

    def get_demo_comparison(self) -> dict:
        """
        Returns a before/after comparison of signal timings.
        'before' = naive fixed-time allocation (30s each)
        'after'  = AI-optimized based on current counts
        """
        if not self.latest_state or "lanes" not in self.latest_state:
            # Simulate if no real data yet
            demo_counts = {"North": 18, "South": 7, "East": 3, "West": 12}
        else:
            demo_counts = {
                lane: data["count"]
                for lane, data in self.latest_state["lanes"].items()
            }

        before = {lane: 30 for lane in demo_counts}  # naive fixed
        after = {}
        priority, _ = self.optimizer.select_priority_lane(demo_counts)
        for lane, count in demo_counts.items():
            if lane == priority:
                after[lane] = self.optimizer.optimize(count)
            else:
                after[lane] = self.optimizer.min_time

        savings = {
            lane: max(0, before[lane] - after[lane])
            for lane in demo_counts
        }
        total_savings = sum(savings.values())

        return {
            "before": before,
            "after": after,
            "savings": savings,
            "total_savings_seconds": total_savings,
            "vehicle_counts": demo_counts,
            "priority_lane": priority,
            "explanation": (
                f"[{self.intersection_id}] AI optimizer gives {priority} lane maximum green time "
                f"({after[priority]}s) because it has the most vehicles "
                f"({demo_counts[priority]}). "
                f"Total signal-cycle savings: {total_savings}s per round."
            )
        }

    def get_alerts(self, limit: int = 20) -> list:
        return self.dashboard.get_alerts(limit)

    # ─────────────────────────────────────────────────────────────────────────
    # DATABASE HELPERS (Step 11)
    # ─────────────────────────────────────────────────────────────────────────

    def _store_detection_data(self, lane_id: str, detections: list,
                               count: int, density: str):
        """Store vehicle detection and density data in MongoDB (ER Diagram)."""
        timestamp = datetime.datetime.utcnow()

        # vehicle_detection collection
        for d in detections:
            vehicle_detection_col.insert_one({
                "camera_id": f"CAM_{lane_id}",
                "lane_id": lane_id,
                "vehicle_type": d["type"],
                "confidence": d.get("confidence", 0.0),
                "timestamp": timestamp
            })

        # traffic_density collection
        traffic_density_col.insert_one({
            "lane_id": lane_id,
            "vehicle_count": count,
            "congestion_level": density,
            "timestamp": timestamp
        })

    def _store_signal_data(self, intersection_id: str, green_time: int, phases: dict):
        """Store signal decision and history in MongoDB (ER Diagram)."""
        timestamp = datetime.datetime.utcnow()

        # traffic_signal collection
        traffic_signal_col.insert_one({
            "intersection_id": self.intersection_id,
            "green_time": green_time,
            "red_time": self.optimizer.min_time,
            "current_status": phases,
            "priority_lane": intersection_id,
            "timestamp": timestamp
        })

        # signal_timing_history collection
        signal_timing_history_col.insert_one({
            "signal_id": f"SIG_{intersection_id}",
            "green_time_assigned": green_time,
            "updated_time": timestamp
        })

        # system_logs — signal update event
        self._store_log(
            "SIGNAL_UPDATE",
            f"Green → {intersection_id} for {green_time}s",
            "info"
        )

    def _store_log(self, event_type: str, description: str, severity: str = "info"):
        """Store a system event in the system_logs collection."""
        system_logs_col.insert_one({
            "event_type": event_type,
            "description": description,
            "severity": severity,
            "timestamp": datetime.datetime.utcnow()
        })
