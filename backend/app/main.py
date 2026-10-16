
import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import traffic_routes, analytics_routes

app = FastAPI(
    title="Smart Traffic Signal Optimization System",
    description="""
## AI-Powered Traffic Signal Management

**Architecture:** Traffic Camera → Video Processing → Vehicle Detection → Lane Analysis → Density Analysis → Signal Optimization → Signal Controller → Dashboard

**Technology Stack:** YOLOv8 (Detection) · FastAPI (Backend) · MongoDB (Storage) · Next.js (Dashboard)

### Pipeline Steps (Activity Diagram)
1. Capture video from camera
2. Extract and preprocess frames
3. Detect vehicles using YOLOv8
4. Classify vehicle types
5. Count vehicles per lane
6. Calculate traffic density
7. Check congestion
8. Optimize signal timing
9. Send timing to signal controller
10. Update traffic signals
11. Store data in database
12. Display results on dashboard

### Signal Optimization Formula
`Green_Time = Base_Time(10) + (Vehicle_Count × Factor(2))`
Constraints: min=10s, max=60s | Anti-starvation threshold: 5 cycles
    """,
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register routers
app.include_router(traffic_routes.router, prefix="/traffic", tags=["Traffic Control"])
app.include_router(analytics_routes.router, prefix="/analytics", tags=["Analytics"])


@app.on_event("startup")
async def startup_event():
    """Log system boot and start the simulation manager."""
    try:
        from .database import system_logs_col
        system_logs_col.insert_one({
            "event_type": "SYSTEM_START",
            "description": "Smart Traffic Signal Optimization System v3.0 started",
            "severity": "info",
            "timestamp": datetime.datetime.utcnow()
        })
        print("✅ Smart Traffic System v3.0 started")
    except Exception as e:
        print(f"⚠️ Startup log failed: {e}")

    # Start the continuous multi-intersection simulation loop
    from .core.manager import intersection_manager
    import asyncio
    asyncio.create_task(intersection_manager.continuous_loop())
    print("🚀 Intersection Simulation Manager started in background")


@app.get("/", tags=["Root"])
def root():
    return {
        "system": "Smart Traffic Signal Optimization System",
        "version": "3.0.0",
        "status": "online",
        "architecture": "TrafficCamera → VideoProcessor → VehicleDetection → LaneAnalyzer → DensityAnalyzer → SignalOptimizer → TrafficSignalController → MonitoringDashboard",
        "endpoints": {
            "traffic": [
                "GET  /traffic/state",
                "GET  /traffic/density",
                "GET  /traffic/video_feed/{lane_id}",
                "POST /traffic/detect",
                "POST /traffic/signal/update",
                "POST /traffic/signal/emergency",
                "GET  /traffic/signal/status",
                "GET  /traffic/alerts",
                "GET  /traffic/demo"
            ],
            "analytics": [
                "GET /analytics/",
                "GET /analytics/signals",
                "GET /analytics/summary",
                "GET /analytics/alerts"
            ],
            "docs": "/docs"
        }
    }
