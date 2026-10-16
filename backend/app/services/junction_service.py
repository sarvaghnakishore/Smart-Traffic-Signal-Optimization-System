from .detection_service import detect_vehicles
from .signal_service import optimize_signal
from .density_service import calculate_density
import random

# Process a 4-way junction given the real counts of all 4 cameras (North, South, East, West).
def process_real_junction(counts):
    """
    Processes a 4-way junction given real counts for all lanes.
    The algorithm dynamically calculates green times for all 4 ways.
    """
    # Find the lane with the highest number of vehicles
    highest_lane = max(counts, key=counts.get)

    junctions = {}
    for lane, count in counts.items():
        base_signal = optimize_signal(count)
        
        # Priority Logic: Only highest lane gets the green signal
        if lane == highest_lane:
            signal_data = base_signal
        else:
            signal_data = {
                "green": 0,
                "yellow": 0,
                "red": base_signal["green"] + base_signal["yellow"] + base_signal["red"]
            }

        junctions[lane] = {
            "vehicles": count, 
            "density": calculate_density(count), 
            "signal": signal_data,
            "isActive": lane == highest_lane
        }
    
    return junctions
