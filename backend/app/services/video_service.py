import cv2
import numpy as np
import os
import glob
import time
from .detection_service import detect_vehicles
from .junction_service import process_real_junction

# Global variable to store the latest junction data
latest_junction_data = None

def load_sequence(prefix):
    base_path = "dataset/extracted_dataset/content/UA-DETRAC/DETRAC_Upload/images/train"
    # Ensure we use the absolute path relative to the backend folder
    full_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), base_path)
    pattern = os.path.join(full_path, f"{prefix}_img*.jpg")
    files = sorted(glob.glob(pattern))
    return files

def generate_frames():
    global latest_junction_data
    
    # Define 4 sequences for 4 lanes
    lanes = {
        "North": load_sequence("MVI_20011"),
        "South": load_sequence("MVI_20012"),
        "East": load_sequence("MVI_20032"),
        "West": load_sequence("MVI_20033")
    }

    # Verify we have at least some data
    for lane, files in lanes.items():
        if not files:
            print(f"⚠️ Warning: No frames found for lane {lane}. Falling back to dummy.")
            # If any lane is missing, we could fallback, but let's assume existence for 'real' mode
    
    max_frames = min(len(f) for f in lanes.values() if f)
    if max_frames == 0:
        print("❌ Critical: No image sequences found in dataset!")
        return

    idx = 0
    while True:
        # 1. Process all 4 lanes
        lane_counts = {}
        processed_frames = {}

        for lane, files in lanes.items():
            frame_path = files[idx % len(files)]
            frame = cv2.imread(frame_path)
            if frame is None:
                continue
            
            count, annotated = detect_vehicles(frame)
            lane_counts[lane] = count
            processed_frames[lane] = annotated

        # 2. Update Junction Logic with real counts
        latest_junction_data = process_real_junction(lane_counts)

        # 3. Determine which frame to show (the one that is currently active/green)
        active_lane = "North" # Default
        for lane, data in latest_junction_data.items():
            if data.get("isActive"):
                active_lane = lane
                break
        
        display_frame = processed_frames.get(active_lane)
        
        if display_frame is not None:
            # Add UI overlay to the frame
            cv2.putText(display_frame, f"LANE: {active_lane} (ACTIVE)", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(display_frame, f"VEHICLES: {lane_counts[active_lane]}", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Encode and yield
            ret, buffer = cv2.imencode('.jpg', display_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        idx += 1
        # Add a small delay to simulate real-time processing
        time.sleep(0.05)

