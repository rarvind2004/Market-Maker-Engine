from __future__ import annotations
import random
from market_maker.common.enums import OrderStatus
from market_maker.common.types import Fill, MarketEvent, Order


class SimulatedBroker:
    def __init__(self, maker_fee_bps: float = 1.0, partial_fill_probability: float = 0.35) -> None:
        self.maker_fee_bps = maker_fee_bps
        self.partial_fill_probability = partial_fill_probability

    def place(self, order: Order, event: MarketEvent) -> Fill | None:
        crossed = (
            order.side.value == "buy" and order.price >= event.ask
        ) or (
            order.side.value == "sell" and order.price <= event.bid
        )
        if not crossed:
            return None
        fill_size = order.size
        if random.random() < self.partial_fill_probability:
            fill_size = max(order.size * 0.5, 1e-6)
            order.status = OrderStatus.PARTIAL
        else:
            order.status = OrderStatus.FILLED
        fee = abs(order.price * fill_size) * self.maker_fee_bps * 1e-4
        order.filled_size += fill_size
        return Fill(
            order_id=order.order_id,
            symbol=order.symbol,
            side=order.side,
            fill_px=order.price,
            fill_size=fill_size,
            ts_ns=event.ts_ns,
            fee=fee,
        )
