"""
Density Service — wrapper around DensityAnalyzer class.
Thresholds per spec:
  LOW    → 0–5 vehicles
  MEDIUM → 6–15 vehicles
  HIGH   → 15+ vehicles
"""

from ..core.classes import DensityAnalyzer

_analyzer = DensityAnalyzer()


def calculate_density(count: int) -> str:
    """Convert vehicle count to density level using spec-compliant thresholds."""
    return _analyzer.get_density_level(count)


def is_congested(count: int) -> bool:
    """Return True if vehicle count indicates HIGH density."""
    return _analyzer.has_congestion(_analyzer.get_density_level(count))
