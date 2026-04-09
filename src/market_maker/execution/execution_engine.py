from __future__ import annotations
from market_maker.common.types import Fill, MarketEvent, Quote
from market_maker.execution.broker.simulated_broker import SimulatedBroker
from market_maker.execution.order_manager import OrderManager
from market_maker.monitoring.metrics import metrics_registry
from market_maker.order_book.book_builder import BookBuilder
from market_maker.risk.position_manager import PositionManager
from market_maker.risk.risk_engine import RiskEngine
from market_maker.strategy.strategy_engine import StrategyEngine


class ExecutionEngine:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.book_builder = BookBuilder(symbol)
        self.position_manager = PositionManager(symbol)
        self.strategy_engine = StrategyEngine()
        self.risk_engine = RiskEngine()
        self.order_manager = OrderManager()
        self.broker = SimulatedBroker()
        self.last_quote: Quote | None = None
        self.last_fill: Fill | None = None

    def on_market_event(self, event: MarketEvent) -> tuple[Quote | None, list[Fill]]:
        book = self.book_builder.on_event(event)
        self.position_manager.mark(book.mid_price())
        quote = self.strategy_engine.on_book(book, self.position_manager.snapshot)
        decision = self.risk_engine.evaluate(book, quote, self.position_manager.snapshot)
        if not decision.allowed:
            metrics_registry.risk_rejects.inc()
            return None, []
        fills: list[Fill] = []
        for order in self.order_manager.quote_to_orders(quote, event.ts_ns):
            fill = self.broker.place(order, event)
            if fill:
                self.position_manager.apply_fill(fill)
                fills.append(fill)
                metrics_registry.fills.inc()
        self.last_quote = quote
        metrics_registry.quotes.inc()
        return quote, fills


class LiveCoordinator:
    def __init__(self, symbol: str = "BTCUSD") -> None:
        self.engine = ExecutionEngine(symbol)

    async def on_market_event(self, event: MarketEvent) -> None:
        self.engine.on_market_event(event)
