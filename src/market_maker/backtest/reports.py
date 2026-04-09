from market_maker.backtest.metrics import BacktestMetrics


def build_summary(result) -> str:
    m = result.metrics
    return (
        f"trades={m.trades} total_pnl={m.total_pnl:.2f} "
        f"realized_pnl={m.realized_pnl:.2f} unrealized_pnl={m.unrealized_pnl:.2f} "
        f"final_position={m.final_position:.4f} max_abs_position={m.max_abs_position:.4f}"
    )
