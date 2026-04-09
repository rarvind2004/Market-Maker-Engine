import cProfile
from market_maker.backtest.replay_engine import generate_synthetic_events
from market_maker.backtest.simulator import run_backtest


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    run_backtest(generate_synthetic_events("BTCUSD", 5000))
    profiler.disable()
    profiler.print_stats(sort="cumtime")
