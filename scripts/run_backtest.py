from market_maker.backtest.replay_engine import generate_synthetic_events
from market_maker.backtest.simulator import run_backtest
from market_maker.backtest.reports import build_summary


def main() -> None:
    events = generate_synthetic_events(symbol="BTCUSD", steps=1000)
    result = run_backtest(events)
    print(build_summary(result))


if __name__ == "__main__":
    main()
