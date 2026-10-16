"""
Signal Service — wrapper around SignalOptimizer class.
Uses the spec formula: Green_Time = Base_Time + (Vehicle_Count × Factor)
Constraints: min=10s, max=60s
"""

from ..core.classes import SignalOptimizer

_optimizer = SignalOptimizer(base_time=10, factor=2, min_time=10, max_time=60)


def optimize_signal(vehicle_count: int) -> dict:
    """
    Calculate signal timing using the formula-based SignalOptimizer.
    Returns: {green, yellow, red} in seconds.
    """
    green = _optimizer.optimize(vehicle_count)
    return {
        "green": green,
        "yellow": 3,   # Fixed transition time
        "red": max(10, 60 - green)
    }


def get_optimized_green(vehicle_count: int) -> int:
    """Return just the green time value."""
    return _optimizer.optimize(vehicle_count)
