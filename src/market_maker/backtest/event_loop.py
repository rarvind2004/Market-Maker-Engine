from collections.abc import Iterable
from market_maker.common.types import MarketEvent


def iter_events(events: Iterable[MarketEvent]):
    for event in events:
        yield event
