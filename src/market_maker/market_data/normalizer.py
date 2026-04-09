from market_maker.common.types import MarketEvent


def normalize_event(payload: dict) -> MarketEvent:
    return MarketEvent(**payload)
