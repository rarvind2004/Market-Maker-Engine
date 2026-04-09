from market_maker.common.enums import Side
from market_maker.common.types import Order, Quote
from market_maker.common.utils import order_id


class OrderManager:
    def quote_to_orders(self, quote: Quote, ts_ns: int) -> list[Order]:
        return [
            Order(order_id=order_id(), symbol=quote.symbol, side=Side.BUY, price=quote.bid_px, size=quote.bid_sz, ts_ns=ts_ns),
            Order(order_id=order_id(), symbol=quote.symbol, side=Side.SELL, price=quote.ask_px, size=quote.ask_sz, ts_ns=ts_ns),
        ]
