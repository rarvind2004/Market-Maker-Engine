from market_maker.constants import BPS


def inventory_skew(position_qty: float, max_position_abs: float, inventory_skew_bps: float = 7.0) -> float:
    if max_position_abs <= 0:
        return 0.0
    ratio = max(-1.0, min(1.0, position_qty / max_position_abs))
    return ratio * inventory_skew_bps * BPS
