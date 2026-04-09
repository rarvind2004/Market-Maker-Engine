from market_maker.common.types import Fill


def fill_notional(fill: Fill) -> float:
    return fill.fill_px * fill.fill_size
