import asyncio
from market_maker.logger import get_logger
from market_maker.market_data.feed_manager import SimulatedFeedManager
from market_maker.execution.execution_engine import LiveCoordinator
from market_maker.monitoring.metrics import metrics_registry

logger = get_logger(__name__)


async def run_live_stack() -> None:
    manager = SimulatedFeedManager(["BTCUSD"])
    coordinator = LiveCoordinator()
    async for event in manager.stream_events():
        await coordinator.on_market_event(event)
        metrics_registry.market_events.inc()


if __name__ == "__main__":
    asyncio.run(run_live_stack())
