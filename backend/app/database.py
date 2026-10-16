from pymongo import MongoClient
import os
from .config import MONGO_URI, DB_NAME

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    # Trigger a connection check
    client.server_info()
    db = client[DB_NAME]
    
    # ER Diagram Collections
    vehicle_detection_col = db["vehicle_detection"]
    traffic_density_col = db["traffic_density"]
    traffic_signal_col = db["traffic_signal"]
    signal_timing_history_col = db["signal_timing_history"]
    system_logs_col = db["system_logs"]

    print("✅ Connected to MongoDB")
except Exception:
    print("⚠️ MongoDB not found. Using in-memory mock database.")
    class MockCollection:
        def __init__(self, max_items=5000):
            self.data = []
            self.max_items = max_items
        def insert_one(self, doc):
            self.data.append(doc)
            if len(self.data) > self.max_items:
                self.data = self.data[-self.max_items:]
        def find(self, query=None, projection=None):
            class MockCursor:
                def __init__(self, data):
                    self.data = data
                def sort(self, *args, **kwargs):
                    return self
                def limit(self, n):
                    self.data = self.data[-n:]
                    return self
                def __iter__(self):
                    return iter(self.data)
                def __getitem__(self, i):
                    return self.data[i]
                def __len__(self):
                    return len(self.data)
            return MockCursor(self.data)

    vehicle_detection_col = MockCollection()
    traffic_density_col = MockCollection()
    traffic_signal_col = MockCollection()
    signal_timing_history_col = MockCollection()
    system_logs_col = MockCollection()
