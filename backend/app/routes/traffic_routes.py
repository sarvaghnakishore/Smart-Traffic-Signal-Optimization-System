from fastapi import APIRouter, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel
import cv2
import asyncio
import datetime

from ..core.manager import intersection_manager
from ..database import (
    traffic_density_col,
    traffic_signal_col,
    signal_timing_history_col,
    system_logs_col
)

router = APIRouter()

# ── Request Models ────────────────────────────────────────────────────────────

class SignalUpdateRequest(BaseModel):
    lane_id: str
    green_time: int


DEFAULT_INTERSECTION = "Intersection A"

# ── Video Streaming ───────────────────────────────────────────────────────────

@router.get("/video_feed/{lane_id}")
@router.get("/video_feed/{intersection_id}/{lane_id}")
async def video_feed(lane_id: str, intersection_id: str = DEFAULT_INTERSECTION):
    """
    MJPEG stream for a specific lane camera in a specific intersection.
    """
    if lane_id not in ["North", "South", "East", "West"]:
        raise HTTPException(status_code=400, detail="Invalid lane ID")
    try:
        pipeline = intersection_manager.get_pipeline(intersection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    async def frame_generator():
        while True:
            with pipeline._lock:
                frame = pipeline.latest_frames.get(lane_id)
                frame_copy = frame.copy() if frame is not None else None
            
            if frame_copy is not None:
                ret, buffer = cv2.imencode('.jpg', frame_copy, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                if ret:
                    yield (
                        b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n'
                        + buffer.tobytes()
                        + b'\r\n'
                    )
            await asyncio.sleep(0.001) 

    return StreamingResponse(
        frame_generator(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@router.get("/stream_sse")
@router.get("/stream_sse/{intersection_id}")
async def video_stream_sse(intersection_id: str = DEFAULT_INTERSECTION):
    """
    Multiplexed SSE stream for all camera lanes.
    Bypasses Chrome's 6-connection limit completely via a single HTTP pipeline!
    """
    try:
        pipeline = intersection_manager.get_pipeline(intersection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    async def event_generator():
        import json
        import base64
        while True:
            payload = {}
            with pipeline._lock:
                local_frames = dict(pipeline.latest_frames)
            
            if not local_frames:
                yield f"data: {json.dumps({'status': 'initializing'})}\n\n"
            else:
                for lane_id, frame in local_frames.items():
                    if frame is not None:
                        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
                        if ret:
                            payload[lane_id] = "data:image/jpeg;base64," + base64.b64encode(buffer).decode('utf-8')
                
                if payload:
                    yield f"data: {json.dumps(payload)}\n\n"
            
            await asyncio.sleep(0.01)
            
    return StreamingResponse(event_generator(), media_type="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "Connection": "keep-alive"
    })


# ── Core State Endpoints ──────────────────────────────────────────────────────

@router.get("/state")
@router.get("/state/{intersection_id}")
async def get_state(intersection_id: str = DEFAULT_INTERSECTION):
    """
    GET /traffic/state or /traffic/state/{intersection_id}
    Returns current system state for an intersection.
    """
    try:
        pipeline = intersection_manager.get_pipeline(intersection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
        
    with pipeline._lock:
        state = dict(pipeline.latest_state)
        
    if not state:
        return {"message": "Initializing simulation..."}
    return state


@router.get("/density")
@router.get("/density/{intersection_id}")
async def get_density(intersection_id: str = DEFAULT_INTERSECTION):
    """
    GET /traffic/density or /traffic/density/{intersection_id}
    Returns density and vehicle count breakdown for lanes.
    """
    try:
        pipeline = intersection_manager.get_pipeline(intersection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
        
    with pipeline._lock:
        state = dict(pipeline.latest_state)
        
    return {
        "intersection_id": intersection_id,
        "lanes": state.get("lanes", {}),
        "active_lane": state.get("active_lane", ""),
        "timestamp": state.get("timestamp", datetime.datetime.utcnow().isoformat())
    }


@router.post("/detect")
@router.post("/detect/{intersection_id}")
async def trigger_detect(intersection_id: str = DEFAULT_INTERSECTION):
    """
    POST /traffic/detect or /traffic/detect/{intersection_id}
    Manually trigger one full detection cycle.
    """
    try:
        pipeline = intersection_manager.get_pipeline(intersection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
        
    state, _ = await asyncio.to_thread(pipeline.run_cycle)
    return {
        "message": "Detection cycle complete",
        "state": state
    }


# ── Signal Control Endpoints ──────────────────────────────────────────────────

@router.post("/signal/update")
@router.post("/signal/update/{intersection_id}")
async def update_signal(request: SignalUpdateRequest, intersection_id: str = DEFAULT_INTERSECTION):
    """
    POST /traffic/signal/update or /traffic/signal/update/{intersection_id}
    Manual signal override.
    """
    try:
        pipeline = intersection_manager.get_pipeline(intersection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
        
    if request.lane_id not in ["North", "South", "East", "West"]:
        raise HTTPException(status_code=400, detail="Invalid lane ID")

    result = pipeline.manual_override(request.lane_id, request.green_time)
    return result


@router.post("/signal/emergency")
@router.post("/signal/emergency/{intersection_id}")
async def emergency_override(intersection_id: str = DEFAULT_INTERSECTION):
    """
    POST /traffic/signal/emergency or /traffic/signal/emergency/{intersection_id}
    Emergency override — immediately sets ALL signals to RED.
    """
    try:
        pipeline = intersection_manager.get_pipeline(intersection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
        
    result = pipeline.emergency_override()
    return {
        "message": f"⚠️ Emergency override activated for {intersection_id}.",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "phases": result.get("phases")
    }


@router.get("/signal/status")
@router.get("/signal/status/{intersection_id}")
async def signal_status(intersection_id: str = DEFAULT_INTERSECTION):
    """
    GET /traffic/signal/status or /traffic/signal/status/{intersection_id}
    """
    try:
        pipeline = intersection_manager.get_pipeline(intersection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return pipeline.controller.get_status()


# ── Alerts Endpoint ───────────────────────────────────────────────────────────

@router.get("/alerts")
@router.get("/alerts/{intersection_id}")
async def get_alerts(intersection_id: str = DEFAULT_INTERSECTION):
    """
    GET /traffic/alerts or /traffic/alerts/{intersection_id}
    """
    try:
        pipeline = intersection_manager.get_pipeline(intersection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
        
    alerts = pipeline.get_alerts(limit=20)
    return {"alerts": alerts, "count": len(alerts)}


# ── Demo Mode Endpoint ────────────────────────────────────────────────────────

@router.get("/demo")
@router.get("/demo/{intersection_id}")
async def get_demo(intersection_id: str = DEFAULT_INTERSECTION):
    """
    GET /traffic/demo or /traffic/demo/{intersection_id}
    Returns before/after comparison
    """
    try:
        pipeline = intersection_manager.get_pipeline(intersection_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
        
    return pipeline.get_demo_comparison()
