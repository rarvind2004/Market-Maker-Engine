from market_maker.common.types import PositionSnapshot, Quote, SignalVector
from market_maker.order_book.book import OrderBook
from market_maker.strategy.fair_value import fair_value
from market_maker.strategy.inventory_model import target_size
from market_maker.strategy.skew import inventory_skew
from market_maker.strategy.spread_model import spread_fraction


class QuotePolicy:
    def __init__(self, base_spread_bps: float = 4.0, inventory_skew_bps: float = 7.0, max_position_abs: float = 1.0) -> None:
        self.base_spread_bps = base_spread_bps
        self.inventory_skew_bps = inventory_skew_bps
        self.max_position_abs = max_position_abs

    def make_quote(self, book: OrderBook, signals: SignalVector, position: PositionSnapshot) -> Quote:
        fv = fair_value(book, signals)
        spread = spread_fraction(self.base_spread_bps, signals)
        skew = inventory_skew(position.quantity, self.max_position_abs, self.inventory_skew_bps)
        bid_sz, ask_sz = target_size(position)
        bid_px = fv * (1 - spread / 2 - skew)
        ask_px = fv * (1 + spread / 2 - skew)
        return Quote(
            symbol=book.symbol,
            bid_px=round(bid_px, 2),
            ask_px=round(ask_px, 2),
            bid_sz=round(bid_sz, 4),
            ask_sz=round(ask_sz, 4),
            fair_value=round(fv, 4),
            alpha=round(signals.alpha, 6),
        )
