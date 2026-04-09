from market_maker.common.types import MarketEvent
from market_maker.order_book.book import OrderBook


def test_order_book_mid_and_spread():
    book = OrderBook("BTCUSD")
    book.apply_event(MarketEvent(ts_ns=1, symbol="BTCUSD", bid=100, ask=102, bid_size=2, ask_size=3))
    assert book.mid_price() == 101
    assert book.spread() == 2
