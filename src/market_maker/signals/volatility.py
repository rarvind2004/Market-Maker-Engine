from market_maker.order_book.book import OrderBook


class VolatilitySignal:
    def compute(self, book: OrderBook) -> float:
        hist = list(book.mid_history)
        if len(hist) < 10:
            return 0.0
        mean = sum(hist) / len(hist)
        variance = sum((x - mean) ** 2 for x in hist) / len(hist)
        return variance ** 0.5 / max(mean, 1e-9)
