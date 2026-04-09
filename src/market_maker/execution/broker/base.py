from abc import ABC, abstractmethod
from market_maker.common.types import Fill, Order


class Broker(ABC):
    @abstractmethod
    def place(self, order: Order) -> Fill | None:
        raise NotImplementedError
