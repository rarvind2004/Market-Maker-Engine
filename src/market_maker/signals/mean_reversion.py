from market_maker.order_book.book import OrderBook


class MeanReversionSignal:
    def compute(self, book: OrderBook) -> float:
        hist = list(book.mid_history)
        if len(hist) < 10:
            return 0.0
        mean = sum(hist) / len(hist)
        return (mean - hist[-1]) / max(mean, 1e-9)
