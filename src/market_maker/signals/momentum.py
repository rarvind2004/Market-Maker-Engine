from market_maker.order_book.book import OrderBook


class MomentumSignal:
    def compute(self, book: OrderBook) -> float:
        hist = list(book.mid_history)
        if len(hist) < 5:
            return 0.0
        return (hist[-1] - hist[-5]) / max(hist[-5], 1e-9)
