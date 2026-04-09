from market_maker.order_book.book import OrderBook


def microprice(book: OrderBook) -> float:
    if not book.bids or not book.asks:
        return 0.0
    bid = book.bids[0]
    ask = book.asks[0]
    total = bid.size + ask.size
    if total == 0:
        return book.mid_price()
    return (ask.price * bid.size + bid.price * ask.size) / total
