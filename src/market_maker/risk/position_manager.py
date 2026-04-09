from market_maker.common.enums import Side
from market_maker.common.types import Fill, PositionSnapshot


class PositionManager:
    def __init__(self, symbol: str) -> None:
        self.snapshot = PositionSnapshot(symbol=symbol)

    def apply_fill(self, fill: Fill) -> PositionSnapshot:
        qty_change = fill.fill_size if fill.side == Side.BUY else -fill.fill_size
        old_qty = self.snapshot.quantity
        new_qty = old_qty + qty_change

        if old_qty == 0 or (old_qty > 0 and qty_change > 0) or (old_qty < 0 and qty_change < 0):
            total_notional = self.snapshot.avg_price * abs(old_qty) + fill.fill_px * abs(qty_change)
            self.snapshot.quantity = new_qty
            self.snapshot.avg_price = total_notional / max(abs(new_qty), 1e-9)
        else:
            closing = min(abs(old_qty), abs(qty_change))
            if old_qty > 0:
                pnl = (fill.fill_px - self.snapshot.avg_price) * closing
            else:
                pnl = (self.snapshot.avg_price - fill.fill_px) * closing
            self.snapshot.realized_pnl += pnl - fill.fee
            self.snapshot.quantity = new_qty
            if new_qty == 0:
                self.snapshot.avg_price = 0.0
            elif abs(qty_change) > abs(old_qty):
                self.snapshot.avg_price = fill.fill_px
        return self.snapshot

    def mark(self, price: float) -> PositionSnapshot:
        self.snapshot.mark_price = price
        return self.snapshot
