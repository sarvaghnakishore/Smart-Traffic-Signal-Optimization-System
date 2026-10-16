import asyncio
from app.core.manager import intersection_manager
import time

async def main():
    print("Starting manual test cycle...")
    pipeline = intersection_manager.get_pipeline("Intersection A")
    print("Got pipeline. Running cycle...")
    start = time.time()
    
    state, frames = pipeline.run_cycle()
    
    print(f"Cycle finished in {time.time() - start:.2f}s")
    print("State populated?", bool(state))
    print("Frames populated?", bool(frames))

if __name__ == "__main__":
    asyncio.run(main())
