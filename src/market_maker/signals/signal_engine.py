from market_maker.common.types import SignalVector
from market_maker.order_book.book import OrderBook
from market_maker.signals.alpha_model import WeightedAlphaModel
from market_maker.signals.order_flow import OrderFlowSignal
from market_maker.signals.momentum import MomentumSignal
from market_maker.signals.mean_reversion import MeanReversionSignal
from market_maker.signals.volatility import VolatilitySignal


class SignalEngine:
    def __init__(self) -> None:
        self.order_flow = OrderFlowSignal()
        self.momentum = MomentumSignal()
        self.mean_reversion = MeanReversionSignal()
        self.volatility = VolatilitySignal()
        self.alpha_model = WeightedAlphaModel()

    def compute(self, book: OrderBook) -> SignalVector:
        vector = SignalVector(
            imbalance=self.order_flow.compute(book),
            momentum=self.momentum.compute(book),
            mean_reversion=self.mean_reversion.compute(book),
            volatility=self.volatility.compute(book),
        )
        return self.alpha_model.score(vector)
