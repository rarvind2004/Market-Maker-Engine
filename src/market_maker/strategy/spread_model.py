from market_maker.constants import BPS
from market_maker.common.types import SignalVector


def spread_fraction(base_spread_bps: float, signals: SignalVector) -> float:
    widen = max(0.0, signals.volatility) * 3
    tighten = min(0.0, signals.alpha) * -1
    return (base_spread_bps + widen - tighten) * BPS
