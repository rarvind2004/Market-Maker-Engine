from __future__ import annotations
import asyncio
import random
from collections.abc import AsyncIterator
from market_maker.common.types import MarketEvent
from market_maker.common.utils import now_ns
from market_maker.market_data.adapters.base import MarketDataAdapter


class SimulatedAdapter(MarketDataAdapter):
    def __init__(self, symbol: str, mid: float = 65000.0, spread: float = 2.5) -> None:
        self.symbol = symbol
        self.mid = mid
        self.spread = spread

    async def stream(self) -> AsyncIterator[MarketEvent]:
        while True:
            drift = random.uniform(-3.0, 3.0)
            self.mid += drift
            bid = self.mid - self.spread / 2
            ask = self.mid + self.spread / 2
            yield MarketEvent(
                ts_ns=now_ns(),
                symbol=self.symbol,
                bid=round(bid, 2),
                ask=round(ask, 2),
                bid_size=round(random.uniform(0.1, 3.0), 4),
                ask_size=round(random.uniform(0.1, 3.0), 4),
                trade_price=round(random.choice([bid, ask, self.mid]), 2),
                trade_size=round(random.uniform(0.01, 0.5), 4),
            )
            await asyncio.sleep(0.025)
