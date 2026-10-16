"""
Core Classes — Smart Traffic Signal Optimization System
Implements the full Class Diagram:
  TrafficCamera → VideoProcessor → VehicleDetection →
  LaneAnalyzer → DensityAnalyzer → SignalOptimizer →
  TrafficSignalController → MonitoringDashboard
"""

import cv2
import numpy as np
import os
import glob
import time
import datetime
from ultralytics import YOLO
from ..database import (
    vehicle_detection_col,
    traffic_density_col,
    traffic_signal_col,
    signal_timing_history_col,
    system_logs_col
)


# ─────────────────────────────────────────────────────────────────────────────
# DATA LAYER
# ─────────────────────────────────────────────────────────────────────────────

class SimulatedTrafficCamera:
    """
    Responsibility: Simulate a live video stream using dataset chunks.
    Maps to: Architecture → Data Layer → Camera
    Dynamic Simulation: Randomly jumps between dataset sequences to simulate
    varying traffic conditions (morning, peak, night) without hardcoded loops.
    """
    def __init__(self, intersection_id: str, lane_id: str):
        self.camera_id = f"CAM_{intersection_id}_{lane_id}"
        self.base_path = "dataset/extracted_dataset/content/UA-DETRAC/DETRAC_Upload/images/train"
        self.full_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            self.base_path
        )
        
        # Load and group all available images by sequence prefix (e.g. MVI_20011)
        all_files = glob.glob(os.path.join(self.full_path, "MVI_*_img*.jpg"))
        self.sequences = {}
        for f in all_files:
            prefix = os.path.basename(f).split('_img')[0]
            if prefix not in self.sequences:
                self.sequences[prefix] = []
            self.sequences[prefix].append(f)
            
        for prefix in self.sequences:
            self.sequences[prefix].sort()
            
        self.available_prefixes = list(self.sequences.keys())
        self.is_active = len(self.available_prefixes) > 0
        
        self.current_prefix = None
        self.current_idx = 0
        self.frames_in_current_chunk = 0
        
        # Randomize initial state so different intersections look different!
        import random
        self.chunk_size = random.randint(30, 80) 
        if self.is_active:
            self._pick_new_sequence()

    def _pick_new_sequence(self):
        import random
        self.current_prefix = random.choice(self.available_prefixes)
        files = self.sequences[self.current_prefix]
        self.current_idx = random.randint(0, max(0, len(files) - 1)) if files else 0
        self.frames_in_current_chunk = 0

    def capture_frame(self, is_green: bool = True, phase: str = "RED", countdown: int = 0, label: str = "Lane"):
        """
        Step 1 of Activity Diagram: Capture simulated video frame.
        Enhanced with Freeze Logic and OpenCV Overlays.
        """
        if not self.is_active or not self.current_prefix:
            frame = self._generate_fallback_frame()
            return self._render_overlay(frame, phase, countdown, label)

        # ── Signal-Driven Movement Logic ───────────────────────────────────
        # Switch Logic: if just turned GREEN, jump forward 3 frames (smooth transition)
        if is_green and not getattr(self, "was_green", False):
            self.current_idx += 3 
        
        self.was_green = is_green

        # If RED, return the same frame (freeze) to simulate waiting traffic
        if not is_green and hasattr(self, "last_frame_data"):
             return self._render_overlay(self.last_frame_data.copy(), phase, countdown, label)

        # ── Normal Frame Capture ──────────────────────────────────────────
        if self.frames_in_current_chunk >= self.chunk_size:
            self._pick_new_sequence()

        files = self.sequences[self.current_prefix]
        frame_path = files[self.current_idx % len(files)]
        
        frame = cv2.imread(frame_path)
        if frame is None:
            self._pick_new_sequence()
            return self.capture_frame(is_green, phase, countdown, label)

        # Resize to standard 640x640 for consistency and batching
        frame = cv2.resize(frame, (640, 640))
        
        # Store for freeze-frame
        self.last_frame_data = frame.copy()

        # Only advance index if signal is GREEN
        if is_green:
            self.current_idx += 1
            self.frames_in_current_chunk += 1

        return self._render_overlay(frame, phase, countdown, label)

    def _render_overlay(self, frame, phase: str, countdown: int, label: str):
        """Render professional HUD overlays directly on the frame."""
        h, w = frame.shape[:2]
        
        # 1. Virtual Stop Line
        cv2.line(frame, (0, h-100), (w, h-100), (100, 100, 100), 2)
        
        # 2. Status Box
        color = (50, 200, 50) if phase == "GREEN" else (50, 50, 255) # BGR
        cv2.rectangle(frame, (10, 10), (220, 80), (20, 20, 20), -1)
        cv2.rectangle(frame, (10, 10), (220, 80), color, 2)
        
        # 3. Phase Text
        cv2.putText(frame, f"{label}: {phase}", (25, 45), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 2)
        
        # 4. Timer Text
        timer_color = (200, 200, 200)
        cv2.putText(frame, f"REL-TIME: {countdown}s", (25, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, timer_color, 1)

        return frame

    def _generate_fallback_frame(self):
        """Generate a technical-looking fallback frame."""
        frame = np.zeros((640, 640, 3), dtype=np.uint8)
        frame[:] = (30, 20, 15)
        cv2.putText(frame, "SIMULATION ERROR: DATASET MISSING", (100, 300), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        return frame
    def get_status(self) -> dict:
        return {
            "camera_id": self.camera_id,
            "is_active": self.is_active,
            "current_prefix": self.current_prefix,
            "chunk_progress": f"{self.frames_in_current_chunk}/{self.chunk_size}"
        }



# ─────────────────────────────────────────────────────────────────────────────
# AI LAYER
# ─────────────────────────────────────────────────────────────────────────────

class VideoProcessor:
    """
    Responsibility: Extract and preprocess frames.
    Maps to: Architecture → AI Layer → Video Processing
    """
    def preprocess(self, frame):
        """Step 2 of Activity Diagram: Extract and preprocess frames."""
        if frame is None:
            return None
        # 1. Resize to 640×640 for optimal YOLOv8 performance
        resized = cv2.resize(frame, (640, 640))
        # 2. Noise reduction via Gaussian blur
        smoothed = cv2.GaussianBlur(resized, (3, 3), 0)
        return smoothed


class VehicleDetection:
    """
    Responsibility: Detect vehicles using YOLOv8.
    Maps to: Architecture → AI Layer → Vehicle Detection
    COCO class IDs: 2=car, 3=motorcycle, 5=bus, 7=truck
    """
    VEHICLE_CLASSES = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}

    def __init__(self, model_path: str = "yolov8n.pt"):
        self.model = YOLO(model_path)
        self.class_ids = list(self.VEHICLE_CLASSES.keys())

    def detect_batch(self, frames_dict: dict[str, np.ndarray]) -> tuple[dict, dict]:
        """
        Step 3 & 4: Detect and classify vehicles for ALL lanes in one batch.
        Optimized for high-performance GPUs.
        """
        lane_ids = list(frames_dict.keys())
        frames_list = [frames_dict[l] for l in lane_ids]
        
        # Perform Batch Inference
        results = self.model(frames_list, verbose=False)
        
        all_detections = {}
        annotated_frames = {}
        
        for i, r in enumerate(results):
            lane_id = lane_ids[i]
            detections = []
            for box in r.boxes:
                cls = int(box.cls)
                if cls in self.class_ids:
                    detections.append({
                        "type": self.VEHICLE_CLASSES.get(cls, "vehicle"),
                        "bbox": box.xyxy[0].tolist(),
                        "confidence": float(box.conf),
                        "class_id": cls
                    })
            all_detections[lane_id] = detections
            annotated_frames[lane_id] = r.plot()
            
        return all_detections, annotated_frames


class LaneAnalyzer:
    """
    Responsibility: Count vehicles per lane (North, South, East, West).
    Maps to: Architecture → AI Layer → Lane Analysis
    """
    LANES = ["North", "South", "East", "West"]

    def analyze(self, detections: list, lane_id: str) -> dict:
        """
        Step 5 of Activity Diagram: Count vehicles per lane.
        Returns detailed breakdown by vehicle type.
        """
        count = len(detections)
        type_breakdown = {}
        for d in detections:
            vtype = d["type"]
            type_breakdown[vtype] = type_breakdown.get(vtype, 0) + 1

        return {
            "lane_id": lane_id,
            "total_count": count,
            "type_breakdown": type_breakdown
        }


class DensityAnalyzer:
    """
    Responsibility: Convert vehicle count into density levels.
    Maps to: Architecture → AI Layer → Density Analysis

    Thresholds (per spec):
      LOW    → 0–5 vehicles
      MEDIUM → 6–15 vehicles
      HIGH   → 15+ vehicles
    """
    def get_density_level(self, count: int) -> str:
        """Step 6 of Activity Diagram: Calculate traffic density."""
        if count <= 5:
            return "LOW"
        elif count <= 15:
            return "MEDIUM"
        else:
            return "HIGH"

    def has_congestion(self, density_level: str) -> bool:
        """Step 7 of Activity Diagram: Check if congestion exists."""
        return density_level == "HIGH"


# ─────────────────────────────────────────────────────────────────────────────
# DECISION LAYER
# ─────────────────────────────────────────────────────────────────────────────

class SignalOptimizer:
    """
    Responsibility: Calculate optimal signal timing.
    Maps to: Architecture → Decision Layer → Signal Optimization

    Formula:  Green_Time = Base_Time + (Vehicle_Count × Factor)
    Constraints: min=10s, max=60s
    Anti-Starvation: every lane gets green every STARVATION_THRESHOLD cycles.
    """
    STARVATION_THRESHOLD = 5  # max cycles a lane can be red consecutively

    def __init__(
        self,
        base_time: int = 10,
        factor: int = 2,
        min_time: int = 10,
        max_time: int = 60
    ):
        self.base_time = base_time
        self.factor = factor
        self.min_time = min_time
        self.max_time = max_time
        self._starvation_counters = {lane: 0 for lane in ["North", "South", "East", "West"]}
        self._cycle_count = 0

    def optimize(self, vehicle_count: int) -> int:
        """Step 8 of Activity Diagram: Optimize signal timing using formula."""
        # Dynamic calculation: Base + (Count * Factor)
        raw = self.base_time + (vehicle_count * self.factor)
        return max(self.min_time, min(self.max_time, raw))

    def select_priority_lane(self, lane_counts: dict[str, int], current_lane: str | None = None) -> tuple[str, str]:
        """
        Determines which lane gets GREEN this cycle.
        If current_lane is provided, it prioritizes SWITCHING to a different lane
        if there is congestion, matching the user's request for 'remaining three lanes'.
        """
        self._cycle_count += 1
        
        # Candidate lanes are all lanes except the one that just finished (if any)
        # unless all other lanes are empty.
        other_lanes = {l: c for l, c in lane_counts.items() if l != current_lane}
        
        # Check starvation first — prevent any lane from indefinite red
        starved_lanes = [
            lane for lane, wait in self._starvation_counters.items()
            if wait >= self.STARVATION_THRESHOLD
        ]

        if starved_lanes:
            priority_lane = max(starved_lanes, key=lambda l: self._starvation_counters[l])
            reason = f"anti_starvation (waited {self._starvation_counters[priority_lane]} cycles)"
        elif any(count > 0 for count in other_lanes.values()):
            # Select most congested among CURRENTLY WAITING lanes
            priority_lane = max(other_lanes, key=other_lanes.get)
            reason = "max_congestion_among_waiting_queues"
        else:
            # Fallback for all lanes being empty or only the previous lane having data
            priority_lane = max(lane_counts, key=lane_counts.get)
            reason = "max_vehicle_count"

        # Update starvation counters
        for lane in self._starvation_counters:
            if lane == priority_lane:
                self._starvation_counters[lane] = 0
            else:
                self._starvation_counters[lane] += 1

        return priority_lane, reason

    def get_all_timings(self, lane_counts: dict[str, int], priority_lane: str) -> dict[str, int]:
        """
        Calculate green times for ALL lanes (not just the priority one).
        Non-priority lanes get proportional partial green time (min_time base).
        """
        timings = {}
        for lane, count in lane_counts.items():
            if lane == priority_lane:
                timings[lane] = self.optimize(count)
            else:
                # Give a minimal phase (base) — avoids full starvation
                timings[lane] = self.min_time
        return timings


class TrafficSignalController:
    """
    Responsibility: Apply signal updates (Red / Yellow / Green).
    Maps to: Architecture → Decision Layer → Signal Controller
    """
    LANES = ["North", "South", "East", "West"]
    YELLOW_DURATION = 3  # seconds

    def __init__(self):
        self.current_phases: dict[str, str] = {lane: "RED" for lane in self.LANES}
        self.timings: dict[str, int] = {lane: 30 for lane in self.LANES}
        self.emergency_active: bool = False
        self.override_lane: str | None = None
        self.cycle_expiry: datetime.datetime | None = None

    def update_signals(self, priority_lane: str, green_time: int, is_override: bool = False) -> tuple[dict, dict]:
        """
        Steps 9 & 10 of Activity Diagram: Send timing to controller and update lights.
        Priority lane → GREEN, others → RED.
        Unifies regular cycles and overrides into a single timer.
        """
        self.emergency_active = False
        new_phases = {}
        for lane in self.LANES:
            new_phases[lane] = "GREEN" if lane == priority_lane else "RED"
        
        self.current_phases = new_phases
        self.timings[priority_lane] = green_time
        self.override_lane = priority_lane if is_override else None
        
        # Set the unified expiry time
        self.cycle_expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=green_time)
        
        return self.current_phases, self.timings

    def is_cycle_active(self) -> bool:
        """Check if the current GREEN phase is still active."""
        if self.emergency_active:
            return True # Emergency keeps everything RED until cleared
        if self.cycle_expiry:
            if datetime.datetime.utcnow() < self.cycle_expiry:
                return True
            else:
                self.cycle_expiry = None
                self.override_lane = None
        return False

    def is_override_active(self) -> bool:
        """Check if a manual override or emergency is currently active."""
        if self.emergency_active:
            return True
        return self.is_cycle_active() and self.override_lane is not None

    def get_remaining_time(self) -> int:
        """Return remaining seconds in the current cycle."""
        if self.emergency_active:
            return 0
        if self.cycle_expiry:
            remaining = (self.cycle_expiry - datetime.datetime.utcnow()).total_seconds()
            return max(0, int(remaining))
        return 0

    def emergency_override(self) -> dict:
        """Emergency: set ALL lanes to RED immediately."""
        self.emergency_active = True
        self.override_lane = None
        self.cycle_expiry = None
        self.current_phases = {lane: "RED" for lane in self.LANES}
        self.timings = {lane: 0 for lane in self.LANES}
        return {"status": "EMERGENCY_OVERRIDE", "phases": self.current_phases}

    def manual_override(self, lane_id: str, green_time: int) -> tuple[dict, dict]:
        """Manual override for a specific lane with a countdown timer."""
        return self.update_signals(lane_id, green_time, is_override=True)

    def get_status(self) -> dict:
        return {
            "phases": self.current_phases,
            "timings": self.timings,
            "emergency_active": self.emergency_active,
            "override_lane": self.override_lane,
            "remaining_time": self.get_remaining_time()
        }


# ─────────────────────────────────────────────────────────────────────────────
# PRESENTATION LAYER
# ─────────────────────────────────────────────────────────────────────────────

class MonitoringDashboard:
    """
    Responsibility: Aggregate all data for display on the dashboard.
    Maps to: Architecture → Presentation Layer → Dashboard
    Displays:
      - Live video (handled by MJPEG stream endpoints)
      - Vehicle counts per lane
      - Density levels
      - Signal status
      - Decision reasoning
      - Alerts
    """
    def __init__(self):
        self._alerts: list[dict] = []
        self._max_alerts = 50

    def compose_state(
        self,
        lane_data: dict,
        priority_lane: str,
        phases: dict,
        timings: dict,
        reasoning: str,
        selection_reason: str,
        timestamp: str
    ) -> dict:
        """Compose the full dashboard state object."""
        return {
            "lanes": lane_data,
            "active_lane": priority_lane,
            "phases": phases,
            "timings": timings,
            "reasoning": reasoning,
            "selection_reason": selection_reason,
            "timestamp": timestamp,
            "alerts": self._alerts[-10:]  # latest 10 alerts
        }

    def add_alert(self, alert_type: str, lane_id: str, message: str, severity: str = "warning"):
        """Add a real-time alert to the dashboard."""
        alert = {
            "id": int(time.time() * 1000),
            "type": severity,  # "danger" | "warning" | "info"
            "title": alert_type,
            "location": lane_id,
            "message": message,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        self._alerts.append(alert)
        if len(self._alerts) > self._max_alerts:
            self._alerts = self._alerts[-self._max_alerts:]
        return alert

    def get_alerts(self, limit: int = 20) -> list[dict]:
        return list(reversed(self._alerts[-limit:]))

    def clear_alerts(self):
        self._alerts = []
