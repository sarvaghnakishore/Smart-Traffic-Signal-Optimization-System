import asyncio
import time
from app.core.manager import intersection_manager

def test_manual_override():
    pipeline = intersection_manager.get_pipeline("Intersection A")
    
    print("Applying manual override: North for 5 seconds...")
    pipeline.manual_override("North", 5)
    
    for i in range(7):
        # run_cycle is now synchronous!
        state, _ = pipeline.run_cycle()
        rem = state.get("remaining_time", -1)
        active = state.get("is_override", False)
        phrase = state.get("phases", {}).get("North")
        print(f"Sec {i}: Remaining={rem}s, IsOverride={active}, NorthPhase={phrase}")
        time.sleep(1)

if __name__ == "__main__":
    test_manual_override()
