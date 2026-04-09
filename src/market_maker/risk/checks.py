from market_maker.common.time import age_ms
from market_maker.common.types import PositionSnapshot, Quote, RiskDecision
from market_maker.order_book.book import OrderBook
from market_maker.risk.limits import RiskLimits


def check_quote(book: OrderBook, quote: Quote, position: PositionSnapshot, limits: RiskLimits) -> RiskDecision:
    if book.last_event and age_ms(book.last_event.ts_ns) > limits.stale_after_ms:
        return RiskDecision(allowed=False, reason="stale_market_data")
    if max(quote.bid_sz, quote.ask_sz) > limits.max_order_size:
        return RiskDecision(allowed=False, reason="order_size_limit")
    if abs(position.quantity) > limits.max_position_abs:
        return RiskDecision(allowed=False, reason="position_limit")
    if position.realized_pnl + position.unrealized_pnl < -limits.max_daily_loss:
        return RiskDecision(allowed=False, reason="daily_loss_limit")
    return RiskDecision(allowed=True)
