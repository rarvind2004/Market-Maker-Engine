from market_maker.common.types import MarketEvent
from market_maker.order_book.book import OrderBook
from market_maker.signals.signal_engine import SignalEngine


def test_signal_engine_returns_alpha():
    book = OrderBook("BTCUSD")
    for i in range(12):
        book.apply_event(MarketEvent(ts_ns=i, symbol="BTCUSD", bid=100+i, ask=101+i, bid_size=2, ask_size=1))
    vector = SignalEngine().compute(book)
    assert isinstance(vector.alpha, float)
