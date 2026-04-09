from abc import ABC, abstractmethod
from market_maker.common.types import SignalVector
from market_maker.order_book.book import OrderBook


class Signal(ABC):
    @abstractmethod
    def compute(self, book: OrderBook) -> float:
        raise NotImplementedError
