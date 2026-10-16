import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def preprocess_frame(frame):
    # 1. Resize to 640x640 for optimal YOLOv8 performance
    resized = cv2.resize(frame, (640, 640))
    # 2. Noise reduction
    smoothed = cv2.GaussianBlur(resized, (3, 3), 0)
    # (YOLO natively handles 0-255 -> 0-1 normalization internally)
    return smoothed

def detect_vehicles(frame):
    processed_frame = preprocess_frame(frame)
    results = model(processed_frame)
    vehicle_count = 0
    
    for r in results:
        for box in r.boxes:
            cls = int(box.cls)
            if cls in [2,3,5,7]:
                vehicle_count += 1
                
    annotated_frame = results[0].plot()
    
    return vehicle_count, annotated_frame

