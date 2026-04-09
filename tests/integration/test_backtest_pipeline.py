from market_maker.backtest.replay_engine import generate_synthetic_events
from market_maker.backtest.simulator import run_backtest


def test_backtest_pipeline_runs():
    result = run_backtest(generate_synthetic_events("BTCUSD", 50))
    assert result.metrics.trades >= 0
