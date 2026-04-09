from market_maker.common.types import PositionSnapshot, Quote
from market_maker.order_book.book import OrderBook
from market_maker.signals.signal_engine import SignalEngine
from market_maker.strategy.quote_policy import QuotePolicy


class StrategyEngine:
    def __init__(self) -> None:
        self.signals = SignalEngine()
        self.quote_policy = QuotePolicy()

    def on_book(self, book: OrderBook, position: PositionSnapshot) -> Quote:
        vector = self.signals.compute(book)
        return self.quote_policy.make_quote(book, vector, position)
