from market_maker.common.types import PositionSnapshot


def target_size(position: PositionSnapshot, max_quote_size: float = 0.02) -> tuple[float, float]:
    penalty = min(0.8, abs(position.quantity) * 0.2)
    size = max_quote_size * (1 - penalty)
    return size, size
