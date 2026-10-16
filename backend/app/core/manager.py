import asyncio
from typing import Dict
from .pipeline import TrafficSystemPipeline

class IntersectionManager:
    """
    Manages multiple intersection pipelines concurrently.
    Provides true real-time multi-tenant traffic simulation.
    """
    def __init__(self, intersections: list[str] = ["Intersection A", "Intersection B", "Intersection C"]):
        self.intersections: Dict[str, TrafficSystemPipeline] = {
            i_id: TrafficSystemPipeline(intersection_id=i_id)
            for i_id in intersections
        }
        
    def get_pipeline(self, intersection_id: str) -> TrafficSystemPipeline:
        if intersection_id not in self.intersections:
            raise ValueError(f"Unknown intersection: {intersection_id}")
        return self.intersections[intersection_id]

    def get_all_ids(self) -> list[str]:
        return list(self.intersections.keys())

    def run_all_cycles_sync(self):
        """
        Runs one cycle inference for all intersections synchronously.
        This isolates PyTorch models from C-level thread deadlocks!
        """
        for p in self.intersections.values():
            try:
                p.run_cycle()
            except Exception as e:
                print(f"🚨 Pipeline Cycle Error for {p.intersection_id}:", e)
                import traceback
                traceback.print_exc()

    async def continuous_loop(self):
        """
        Main simulation loop. 
        Processes each intersection sequentially to avoid PyTorch/GIL deadlocks.
        """
        import asyncio
        print(f"📡 Manager: Starting sequential simulation for {len(self.intersections)} intersections...")
        
        while True:
            for p in self.intersections.values():
                try:
                    # Run each cycle in its own thread to keep the event loop responsive
                    await asyncio.to_thread(p.run_cycle)
                except Exception as e:
                    print(f"🚨 Manager Error for {p.intersection_id}: {e}")
            
            # Minimal sleep between full manager cycles to maximize FPS
            await asyncio.sleep(0.01)

# Global singleton instance
intersection_manager = IntersectionManager()
