from market_maker.order_book.book import OrderBook
from market_maker.order_book.microprice import microprice
from market_maker.common.types import SignalVector


def fair_value(book: OrderBook, signals: SignalVector) -> float:
    base = microprice(book) or book.mid_price()
    return base * (1 + 0.001 * signals.alpha)
