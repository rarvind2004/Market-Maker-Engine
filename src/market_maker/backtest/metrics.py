from __future__ import annotations
from dataclasses import dataclass


@dataclass
class BacktestMetrics:
    trades: int
    realized_pnl: float
    unrealized_pnl: float
    total_pnl: float
    final_position: float
    max_abs_position: float
