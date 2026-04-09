from market_maker.backtest.simulator import run_backtest


def sweep(events, spreads=(2.0, 4.0, 6.0)) -> list[dict]:
    results = []
    for spread in spreads:
        result = run_backtest(events, base_spread_bps=spread)
        results.append({"spread": spread, "total_pnl": result.metrics.total_pnl})
    return results
