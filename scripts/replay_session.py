from pathlib import Path
from market_maker.backtest.replay_engine import load_events_from_parquet
from market_maker.backtest.simulator import run_backtest


if __name__ == "__main__":
    path = Path("data/replays/session.parquet")
    events = load_events_from_parquet(path)
    result = run_backtest(events)
    print(result.metrics)
