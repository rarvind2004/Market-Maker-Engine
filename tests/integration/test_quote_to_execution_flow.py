from market_maker.backtest.replay_engine import generate_synthetic_events
from market_maker.execution.execution_engine import ExecutionEngine


def test_quote_to_execution_flow_runs():
    engine = ExecutionEngine("BTCUSD")
    fills = []
    for event in generate_synthetic_events("BTCUSD", 20):
        _, new_fills = engine.on_market_event(event)
        fills.extend(new_fills)
    assert isinstance(fills, list)
