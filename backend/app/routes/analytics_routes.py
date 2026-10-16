from fastapi import APIRouter
from ..services.analytics_service import (
    get_density_history,
    get_signal_history,
    get_summary_stats,
    get_recent_alerts
)

router = APIRouter()


@router.get("/")
@router.get("/history")
async def get_analytics():
    """
    GET /analytics/ or /analytics/history
    Historical traffic density records for the Traffic Flow Analysis chart.
    """
    return get_density_history(limit=400)


@router.get("/signals")
async def get_signal_analytics():
    """
    GET /analytics/signals
    Historical signal timing records for the Average Wait Times chart.
    """
    return get_signal_history(limit=100)


@router.get("/summary")
async def get_analytics_summary():
    """
    GET /analytics/summary
    Aggregated statistics: avg green time, congestion frequency, lane averages,
    total detections, recent system logs.
    """
    return get_summary_stats()


@router.get("/alerts")
async def get_analytics_alerts():
    """
    GET /analytics/alerts
    Recent system events formatted as dashboard alerts.
    """
    return {"alerts": get_recent_alerts(limit=20)}
