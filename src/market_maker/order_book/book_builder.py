from market_maker.order_book.book import OrderBook
from market_maker.common.types import MarketEvent


class BookBuilder:
    def __init__(self, symbol: str) -> None:
        self.book = OrderBook(symbol)

    def on_event(self, event: MarketEvent) -> OrderBook:
        self.book.apply_event(event)
        return self.book
