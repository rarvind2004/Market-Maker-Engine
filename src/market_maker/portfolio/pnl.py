from market_maker.common.types import PositionSnapshot


def total_pnl(position: PositionSnapshot) -> float:
    return position.realized_pnl + position.unrealized_pnl
