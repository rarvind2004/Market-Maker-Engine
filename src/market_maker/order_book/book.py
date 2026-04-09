from __future__ import annotations
from collections import deque
from market_maker.common.types import BookLevel, MarketEvent


class OrderBook:
    def __init__(self, symbol: str, max_history: int = 128) -> None:
        self.symbol = symbol
        self.bids: list[BookLevel] = []
        self.asks: list[BookLevel] = []
        self.last_event: MarketEvent | None = None
        self.mid_history: deque[float] = deque(maxlen=max_history)

    def apply_event(self, event: MarketEvent) -> None:
        self.last_event = event
        self.bids = [BookLevel(price=event.bid, size=event.bid_size)]
        self.asks = [BookLevel(price=event.ask, size=event.ask_size)]
        self.mid_history.append(self.mid_price())

    def best_bid(self) -> float:
        return self.bids[0].price if self.bids else 0.0

    def best_ask(self) -> float:
        return self.asks[0].price if self.asks else 0.0

    def spread(self) -> float:
        return max(0.0, self.best_ask() - self.best_bid())

    def mid_price(self) -> float:
        if not self.bids or not self.asks:
            return 0.0
        return (self.best_bid() + self.best_ask()) / 2.0
