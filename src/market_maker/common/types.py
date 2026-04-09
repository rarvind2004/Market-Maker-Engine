from __future__ import annotations
from pydantic import BaseModel, Field
from market_maker.common.enums import Side, OrderStatus


class BookLevel(BaseModel):
    price: float
    size: float


class MarketEvent(BaseModel):
    ts_ns: int
    symbol: str
    bid: float
    ask: float
    bid_size: float
    ask_size: float
    trade_price: float | None = None
    trade_size: float | None = None


class SignalVector(BaseModel):
    imbalance: float = 0.0
    momentum: float = 0.0
    mean_reversion: float = 0.0
    volatility: float = 0.0
    alpha: float = 0.0


class Quote(BaseModel):
    symbol: str
    bid_px: float
    ask_px: float
    bid_sz: float
    ask_sz: float
    fair_value: float
    alpha: float


class Order(BaseModel):
    order_id: str
    symbol: str
    side: Side
    price: float
    size: float
    ts_ns: int
    status: OrderStatus = OrderStatus.OPEN
    filled_size: float = 0.0


class Fill(BaseModel):
    order_id: str
    symbol: str
    side: Side
    fill_px: float
    fill_size: float
    ts_ns: int
    fee: float = 0.0


class PositionSnapshot(BaseModel):
    symbol: str
    quantity: float = 0.0
    avg_price: float = 0.0
    realized_pnl: float = 0.0
    mark_price: float = 0.0

    @property
    def unrealized_pnl(self) -> float:
        if self.quantity == 0:
            return 0.0
        sign = 1 if self.quantity > 0 else -1
        return sign * abs(self.quantity) * (self.mark_price - self.avg_price)


class RiskDecision(BaseModel):
    allowed: bool
    reason: str = "ok"
