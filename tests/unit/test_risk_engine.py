from market_maker.common.types import MarketEvent, PositionSnapshot
from market_maker.order_book.book import OrderBook
from market_maker.strategy.strategy_engine import StrategyEngine
from market_maker.risk.risk_engine import RiskEngine
from market_maker.common.utils import now_ns


def test_risk_engine_allows_basic_quote():
    book = OrderBook("BTCUSD")
    ts = now_ns()
    for i in range(12):
        book.apply_event(MarketEvent(ts_ns=ts + i, symbol="BTCUSD", bid=100+i, ask=101+i, bid_size=2, ask_size=1))
    position = PositionSnapshot(symbol="BTCUSD")
    quote = StrategyEngine().on_book(book, position)
    decision = RiskEngine().evaluate(book, quote, position)
    assert decision.allowed
