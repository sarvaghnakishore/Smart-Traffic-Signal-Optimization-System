"""
Lane Service — wrapper around LaneAnalyzer class.
Provides lane-based vehicle counting as a service.
Maps to: Architecture → AI Layer → Lane Analysis
"""

from ..core.classes import LaneAnalyzer

_analyzer = LaneAnalyzer()


def count_vehicles_per_lane(detections: list, lane_id: str) -> dict:
    """
    Count and classify vehicles in a single lane.
    Returns: {lane_id, total_count, type_breakdown}
    """
    return _analyzer.analyze(detections, lane_id)


def get_dominant_lane(lane_counts: dict[str, int]) -> str:
    """Return the lane with the highest vehicle count."""
    if not lane_counts:
        return "North"
    return max(lane_counts, key=lane_counts.get)


def summarize_all_lanes(lane_counts: dict[str, int]) -> dict:
    """
    Summarize statistics across all four lanes.
    Returns: total vehicles, average, max lane, min lane.
    """
    if not lane_counts:
        return {}
    total = sum(lane_counts.values())
    return {
        "total_vehicles": total,
        "average_per_lane": round(total / len(lane_counts), 1),
        "max_lane": max(lane_counts, key=lane_counts.get),
        "min_lane": min(lane_counts, key=lane_counts.get),
        "lane_counts": lane_counts
    }
