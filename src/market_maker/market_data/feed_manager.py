from __future__ import annotations
from collections.abc import AsyncIterator
from market_maker.common.types import MarketEvent
from market_maker.market_data.adapters.simulated_adapter import SimulatedAdapter


class SimulatedFeedManager:
    def __init__(self, symbols: list[str]) -> None:
        self.adapters = [SimulatedAdapter(symbol=s) for s in symbols]

    async def stream_events(self) -> AsyncIterator[MarketEvent]:
        # simple single symbol streaming for scaffold
        async for event in self.adapters[0].stream():
            yield event
