from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from market_maker.common.types import MarketEvent


class MarketDataAdapter(ABC):
    @abstractmethod
    async def stream(self) -> AsyncIterator[MarketEvent]:
        raise NotImplementedError
