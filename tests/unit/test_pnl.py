from market_maker.common.enums import Side
from market_maker.common.types import Fill
from market_maker.risk.position_manager import PositionManager


def test_position_manager_realizes_pnl():
    pm = PositionManager("BTCUSD")
    pm.apply_fill(Fill(order_id="1", symbol="BTCUSD", side=Side.BUY, fill_px=100, fill_size=1, ts_ns=1))
    snap = pm.apply_fill(Fill(order_id="2", symbol="BTCUSD", side=Side.SELL, fill_px=105, fill_size=1, ts_ns=2))
    assert snap.realized_pnl > 0
