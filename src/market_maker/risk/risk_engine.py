from market_maker.common.types import PositionSnapshot, Quote, RiskDecision
from market_maker.order_book.book import OrderBook
from market_maker.risk.checks import check_quote
from market_maker.risk.kill_switch import KillSwitch
from market_maker.risk.limits import RiskLimits


class RiskEngine:
    def __init__(self) -> None:
        self.limits = RiskLimits()
        self.kill_switch = KillSwitch()
        self.reject_count = 0

    def evaluate(self, book: OrderBook, quote: Quote, position: PositionSnapshot) -> RiskDecision:
        if self.kill_switch.active:
            return RiskDecision(allowed=False, reason=f"kill_switch:{self.kill_switch.reason}")
        decision = check_quote(book, quote, position, self.limits)
        if not decision.allowed:
            self.reject_count += 1
            if self.reject_count >= self.limits.reject_limit:
                self.kill_switch.trigger("reject_limit")
        return decision
