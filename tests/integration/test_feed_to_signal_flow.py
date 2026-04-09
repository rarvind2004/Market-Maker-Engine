from market_maker.backtest.replay_engine import generate_synthetic_events
from market_maker.execution.execution_engine import ExecutionEngine


def test_feed_to_signal_flow_runs():
    events = generate_synthetic_events("BTCUSD", 10)
    engine = ExecutionEngine("BTCUSD")
    for event in events:
        engine.on_market_event(event)
    assert engine.last_quote is not None
