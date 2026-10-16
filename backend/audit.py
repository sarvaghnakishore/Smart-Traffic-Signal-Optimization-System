import time
import cv2
import httpx
import contextlib
from ultralytics import YOLO

def run_audit():
    print("--- 2. Inference Time per Frame & 3. FPS ---")
    try:
        model = YOLO("yolov8n.pt")
        # Dummy frame
        import numpy as np
        frame = np.zeros((640, 640, 3), dtype=np.uint8)

        # Warmup
        model(frame, verbose=False)
        
        times = []
        for _ in range(10):
            t0 = time.time()
            model(frame, verbose=False)
            times.append((time.time() - t0) * 1000)
            
        avg_ms = sum(times) / len(times)
        print(f"Avg Inference Time: {avg_ms:.2f} ms")
        print(f"Min/Max Time: {min(times):.2f} / {max(times):.2f} ms")
        print(f"Est. FPS (raw YOLO): {1000 / avg_ms:.2f} FPS")
    except Exception as e:
        print(f"Inference error: {e}")

    print("\n--- 8. Backend API Performance ---")
    try:
        t0 = time.time()
        res = httpx.get("http://localhost:8000/traffic/state", timeout=2.0)
        api_ms = (time.time() - t0) * 1000
        print(f"GET /traffic/state: {api_ms:.2f} ms (Status: {res.status_code})")
        
        t0 = time.time()
        res2 = httpx.get("http://localhost:8000/traffic/density", timeout=2.0)
        api_ms2 = (time.time() - t0) * 1000
        print(f"GET /traffic/density: {api_ms2:.2f} ms (Status: {res2.status_code})")
    except Exception as e:
        print(f"API ping error: {e}")

if __name__ == "__main__":
    run_audit()
