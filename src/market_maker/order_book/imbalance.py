from market_maker.order_book.book import OrderBook


def imbalance(book: OrderBook) -> float:
    if not book.bids or not book.asks:
        return 0.0
    bid_size = book.bids[0].size
    ask_size = book.asks[0].size
    total = bid_size + ask_size
    if total == 0:
        return 0.0
    return (bid_size - ask_size) / total
