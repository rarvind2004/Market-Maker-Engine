from __future__ import annotations
from dataclasses import dataclass
from market_maker.backtest.metrics import BacktestMetrics
from market_maker.execution.execution_engine import ExecutionEngine
from market_maker.strategy.quote_policy import QuotePolicy


@dataclass
class BacktestResult:
    metrics: BacktestMetrics
    fills: list
    last_quote: object | None


def run_backtest(events, base_spread_bps: float = 4.0) -> BacktestResult:
    engine = ExecutionEngine("BTCUSD")
    engine.strategy_engine.quote_policy = QuotePolicy(base_spread_bps=base_spread_bps)
    fills = []
    max_abs_position = 0.0
    for event in events:
        quote, new_fills = engine.on_market_event(event)
        fills.extend(new_fills)
        max_abs_position = max(max_abs_position, abs(engine.position_manager.snapshot.quantity))
    snap = engine.position_manager.snapshot
    metrics = BacktestMetrics(
        trades=len(fills),
        realized_pnl=snap.realized_pnl,
        unrealized_pnl=snap.unrealized_pnl,
        total_pnl=snap.realized_pnl + snap.unrealized_pnl,
        final_position=snap.quantity,
        max_abs_position=max_abs_position,
    )
    return BacktestResult(metrics=metrics, fills=fills, last_quote=engine.last_quote)
