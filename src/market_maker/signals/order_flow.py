from market_maker.order_book.book import OrderBook
from market_maker.order_book.imbalance import imbalance


class OrderFlowSignal:
    def compute(self, book: OrderBook) -> float:
        return imbalance(book)
