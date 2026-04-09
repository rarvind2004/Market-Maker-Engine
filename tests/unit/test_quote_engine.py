from market_maker.common.types import MarketEvent, PositionSnapshot
from market_maker.order_book.book import OrderBook
from market_maker.strategy.strategy_engine import StrategyEngine


def test_quote_engine_bid_below_ask():
    book = OrderBook("BTCUSD")
    for i in range(12):
        book.apply_event(MarketEvent(ts_ns=i, symbol="BTCUSD", bid=100+i, ask=101+i, bid_size=2, ask_size=1))
    quote = StrategyEngine().on_book(book, PositionSnapshot(symbol="BTCUSD"))
    assert quote.bid_px < quote.ask_px
